#!/usr/bin/env python3
"""reap_owned_group.py — a worker's teardown reaps its own process group (SPEC INV-230, ROADMAP 393).

INV-213 landed the NOTICE: `guardrails/check-runaway-child.py` finds an owned, orphaned, burning
descendant and REPORTS it, ending nothing — notice-first, so the mechanism can never become the
broad-sweep footgun it guards against. This module lands the remaining two arms of the same class.

ARM 1 — THE REAP. A worker's teardown reaps its OWN process group: a scoped kill of the process group
the RUN itself owns. It is safe because it is the run's own group, exactly INV-162's owned-identity
discipline. The reap takes a NUMERIC process group and refuses any group it cannot prove the run owns —
a program name is not even expressible here, so the broad name-based sweep that once closed the owner's
real browser (base rule 17) cannot be written through this door. The reap targets the group with
`os.killpg`: the run started its children into their own group (a `setsid` / start-new-session at
spawn), so the reaper stands outside that group and the kill reaches the children, not itself. Every
reap reports through the shared cleanup-notice shape (`guardrails/cleanup_notice.py`, row 417,
INV-204), so the reap says what it ended and the proof the run owned it.

ARM 2 — THE IDLE-OUTPUT DETECTION HABIT. A worker whose status reads "running" while its output file
has stopped growing is caught by reading the output's mtime — the liveness-via-mtime read (INV-76). The
memory instance (2026-07-17): a background worker returned its full result and finished ~48 minutes
before anyone noticed, its status line still reading "running", while a `difflib` child burned a full
core on a widget's single-line blob. `find_idle_output_workers` reads mtime alone and returns the
stalled workers with their owned process group, so the caller confirms with `ps` and reaps the owned
group. Detection and reap are two steps, and only an owned group is ever reaped.

SAFETY. This module NEVER reaps a process the run cannot prove it owns: the reap is refused unless the
target process group is in the run's own owned set, and the target is a numeric group, never a name.
"""
import os
import signal
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import cleanup_notice  # noqa: E402  (the shared cleanup-notice shape, SPEC INV-204)

# A worker whose status reads "running" while its output mtime is at least this many seconds behind the
# clock is idle-output. 120s kept — ruled 2026-08-15 (decision-dossier-2026-08-15.md, Number 4):
# matches the shipped two-minute window; the one incident on record (JOURNAL.md row 393 / INV-230, a
# worker found idle 48 minutes late) does not pin the number itself. No single recommended replacement
# value, so today's value stands. Truth, not the earlier claim: this is a FIXED default today — no env
# var or config file is read for it. A host override is queued (not wired yet), and belongs in the
# settings ladder's package-defaults table (skills/live-spec-base/references/settings-ladder.md) once
# it exists.
IDLE_THRESHOLD = 120.0


class UnownedReapRefused(Exception):
    """Raised when a reap is asked for a group the run cannot prove it owns. The reap ends nothing."""


def reap_owned_group(pgid, owned_pgids, what, sig=signal.SIGTERM, killpg=None, out=None):
    """Reap the process group `pgid` — ONLY when the run can prove it owns that group.

    `pgid` is a numeric process group id; `owned_pgids` is the set of groups THIS RUN spawned and
    holds; `what` is a plain-words label for the notice. A name is not a legal target: `pgid` must be
    an int, and it must be in `owned_pgids`, or the reap is refused and ends nothing — the
    owned-identity discipline (SPEC INV-162). On a proven-owned group it sends `sig` to the whole group
    with `os.killpg` (injectable as `killpg` for tests) and emits one CLEANUP-NOTICE line through the
    shared shape, naming what it ended and the proof of ownership. Returns the emitted notice line.
    Raises UnownedReapRefused when ownership cannot be proven.
    """
    if killpg is None:
        killpg = os.killpg
    owned = set(owned_pgids or ())
    if not isinstance(pgid, int) or isinstance(pgid, bool):
        raise UnownedReapRefused(
            "a reap targets a numeric process group, not %r — a program name is not a legal reap "
            "target (SPEC INV-162)" % (pgid,))
    if pgid not in owned:
        raise UnownedReapRefused(
            "refused: pgid=%s is not in the run's own owned groups %s — a reap acts only on what the "
            "run provably owns, never a group it cannot prove it holds (SPEC INV-162)"
            % (pgid, sorted(owned)))
    killpg(pgid, sig)
    return cleanup_notice.cleanup_notice(
        ended="pgid=%d" % pgid,
        what=what,
        owned_via="pgid=%d (this run's own process group, spawned by this run)" % pgid,
        out=out)


def find_idle_output_workers(workers, now, idle_threshold=IDLE_THRESHOLD):
    """The idle-output detection habit (SPEC INV-230, kin of INV-76): a worker reading "running" whose
    output file has stopped growing.

    `workers` is a list of dicts carrying at least `status`, `output_mtime` (epoch seconds, or None
    when the worker has produced no output yet), and `pgid`. A worker is idle-output when its status is
    "running" AND its output mtime is at least `idle_threshold` seconds behind `now`. The read is mtime
    alone — the liveness-via-mtime law [INV-76]. It ENDS nothing: it returns each stalled worker with
    an `idle_for` and a `why`, carrying its owned `pgid`, so the caller confirms with `ps` and reaps
    the owned group through `reap_owned_group`. A worker with no output timestamp is not judged here —
    there is nothing to read idleness from, and "never grew" is a different case from "grew then went
    idle".
    """
    out = []
    for w in workers:
        if (w.get("status") or "").lower() != "running":
            continue
        mtime = w.get("output_mtime")
        if mtime is None:
            continue
        idle_for = now - mtime
        if idle_for < idle_threshold:
            continue
        r = dict(w)
        r["idle_for"] = idle_for
        r["why"] = ('status reads "running" but the output file has been idle %.0fs by its mtime — '
                    "the liveness-via-mtime read [INV-76]; confirm with ps and reap the owned group"
                    % idle_for)
        out.append(r)
    return out


if __name__ == "__main__":
    # A tiny self-check that ends nothing: with a fake killpg, show the reap's notice line, and refuse
    # an unowned group, so the module's two behaviours are exercisable on demand.
    calls = []
    print(reap_owned_group(0, {0}, "(self-check group)", killpg=lambda p, s: calls.append((p, s)),
                           out=sys.stdout))
    try:
        reap_owned_group(999999, {0}, "(unowned)", killpg=lambda p, s: calls.append((p, s)))
    except UnownedReapRefused as e:
        print("refused as expected: %s" % e)
