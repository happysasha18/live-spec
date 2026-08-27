#!/usr/bin/env python3
"""check-runaway-child.py — a finished worker leaves no runaway child that burns unseen (SPEC INV-213).

THE LAW. When a worker or task the run spawned COMPLETES, a descendant it left behind can keep
burning a full core unnoticed. The memory instance (2026-07-17): a difflib process burned one core
for forty-six minutes after its worker reported done, and a frozen status line masked it until the
next unexplained slowdown. The run owns that descendant — it sits in the run's own process group, or
it runs from under the run's own temp tree — so the run answers for it. At a stopping point the run
REPORTS a runaway descendant it provably owns: what it is, how much CPU it holds, and why the run
owns it. That is the minimum owed (the owner 2026-07-17 ~16:58, the same word that ordered row 417's
cleanup notice), so an unexpected burn is visible the moment it happens.

WHERE IT LIVES. This is a Stop-time notice, not a push gate: a push gate runs long after the runaway
would have burned its cores, so it takes no pre-push letter and stands beside the Stop-surface judges.

THE SAFETY DISCIPLINE (SPEC INV-162). This runs in process space, where a coarse scope does real
harm — a broad name-based sweep once closed the owner's real browser (base rule 17). So a runaway is
identified ONLY by PROVABLE OWNERSHIP, never by a program name:
  * a process in the run's OWN process group (a pgid the run holds), or
  * a process running from UNDER the run's own temp tree (a path the run owns).
`find_runaways` reads NO command/name field for its verdict. A process whose command merely matches a
known burner, but sits in a foreign process group and under no owned tree, is never targeted — the run
cannot prove it owns it, so a name match alone must not fire.

WHAT COUNTS AS A RUNAWAY. All four hold:
  * OWNED — proved by process group or owned tree, above;
  * ORPHANED — its owning parent is no longer alive (reparented to init, or a ppid absent from the
    live table): a live-and-working child whose parent is alive is NOT a runaway;
  * BURNING — its CPU share is at or above the threshold (default 50%);
  * NOT self — the notice mechanism and the group lead never report themselves.

NOTICE-FIRST. It REPORTS through the shared cleanup-notice module (`guardrails/cleanup_notice.py`,
row 417) and ends NO process. A reap gated on the same strict ownership proof is a later, optional
step; the first version reports, so the mechanism can never itself become the broad-sweep footgun it
guards against. As a Stop-time notice it always exits zero and never blocks a stop.

LIVE WIRING is a documented, owner-run install step, not an auto-wire into the running session's
Stop hook: wiring a process scanner into a live session mid-movement could report against that
session's own live background workers. The owner installs it when a session is quiet (guardrails/README.md).
"""
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, SCRIPT_DIR)
import cleanup_notice  # noqa: E402  (the shared notice shape, SPEC INV-204)

# A descendant at or above this CPU share is "burning". 50% kept — NOT ruled. 2026-08-15's survey
# (work/2026-08-15-unowned-numbers.md, row 4) flagged this and left it explicitly for the owner's
# word; a later comment here once cited a "decision-dossier-2026-08-15.md" as though a ruling
# existed — checked in full against the filesystem and git history on 2026-08-28, that file never
# existed. The one incident on record (a suite SIGKILLed mid-run, 2026-08-13/14) does not point at
# this number specifically; 50% matches the example rules tools like monit commonly show. Truth, not
# the earlier claim: this is a FIXED default today — no env var or config file is read for it. A host
# override is queued (not wired yet), and belongs in the settings ladder's package-defaults table
# (skills/live-spec-base/references/settings-ladder.md) once it exists.
CPU_THRESHOLD = 50.0


def _path_under(path, root):
    """True when `path` resolves to a location inside `root` — the owned-tree ownership proof."""
    if not path or not root:
        return False
    try:
        root_real = os.path.realpath(root)
        path_real = os.path.realpath(path)
    except OSError:
        return False
    if path_real == root_real:
        return True
    prefix = root_real if root_real.endswith(os.sep) else root_real + os.sep
    return path_real.startswith(prefix)


def _owned_via(proc, owned_pgids, owned_tree):
    """The proof the run owns this process, or None. Ownership is by process group or owned tree
    ONLY — never by the process's command or name. Returns a plain-words proof string."""
    if proc.get("pgid") in owned_pgids:
        return "pgid=%s (this run own process group)" % proc.get("pgid")
    if _path_under(proc.get("path"), owned_tree):
        return "path %s under the run own tree %s" % (proc.get("path"), owned_tree)
    return None


def find_runaways(procs, owned_pgids, owned_tree=None, cpu_threshold=CPU_THRESHOLD, self_pids=()):
    """The pure core: the owned, orphaned, CPU-burning descendants in a process table.

    `procs` is a list of dicts with pid, ppid, pgid, pcpu, and optionally path (and command, which
    this function never reads for its verdict). Ownership is proved by process group or owned tree;
    a bare command/name match can never make a process a runaway. Returns each runaway dict with an
    added `owned_via` proof string and `why` summary.
    """
    owned_pgids = set(owned_pgids or ())
    self_pids = set(self_pids or ())
    live_pids = {p.get("pid") for p in procs}
    out = []
    for p in procs:
        if p.get("pid") in self_pids:
            continue
        owned_via = _owned_via(p, owned_pgids, owned_tree)
        if owned_via is None:
            continue                                   # not provably owned — never targeted
        ppid = p.get("ppid")
        orphaned = (ppid == 1) or (ppid not in live_pids)
        if not orphaned:
            continue                                   # parent alive: a live worker at work
        try:
            cpu = float(p.get("pcpu", 0) or 0)
        except (TypeError, ValueError):
            cpu = 0.0
        if cpu < cpu_threshold:
            continue                                   # owned and orphaned, but idle
        r = dict(p)
        r["owned_via"] = owned_via
        r["why"] = "orphaned (owning parent ended) and holding %.1f%% CPU" % cpu
        out.append(r)
    return out


def _describe(proc):
    """A plain-words label for the report: the command as read, never trusted for the verdict."""
    cmd = proc.get("command") or "(unknown)"
    return "%s (pid %s, an orphaned worker descendant)" % (cmd, proc.get("pid"))


def run(procs, owned_pgids, owned_tree=None, cpu_threshold=CPU_THRESHOLD, self_pids=(), out=None):
    """Report every runaway through the shared notice and return an exit code.

    Report-only: it ends no process, and always returns 0 so a Stop is never blocked by the notice.
    """
    if out is None:
        out = sys.stderr
    runaways = find_runaways(procs, owned_pgids, owned_tree, cpu_threshold, self_pids)
    for r in runaways:
        cleanup_notice.runaway_notice(
            _describe(r), "%.1f" % float(r.get("pcpu", 0) or 0), r["owned_via"], out=out)
    if runaways:
        out.write("runaway-child: %d owned runaway descendant(s) reported above — each still alive and "
                  "burning; the run owns them, so they are surfaced rather than left to the next "
                  "unexplained slowdown (SPEC INV-213). This is a report; it ends nothing.\n"
                  % len(runaways))
        out.flush()
    return 0


def _read_process_table():
    """The live process table, or a simulated one from LIVE_SPEC_RUNAWAY_PROCS_JSON for a test.

    A test injects a table through the env so the mechanism is exercisable without ever spawning a
    runaway on the real machine. Live, it reads `ps` and parses pid/ppid/pgid/cpu/command.
    """
    injected = os.environ.get("LIVE_SPEC_RUNAWAY_PROCS_JSON")
    if injected:
        return json.loads(injected)
    try:
        res = subprocess.run(
            ["ps", "-Ao", "pid=,ppid=,pgid=,pcpu=,comm="],
            capture_output=True, text=True, check=False)
    except (OSError, ValueError):
        return []
    procs = []
    for line in res.stdout.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        try:
            pid, ppid, pgid = int(parts[0]), int(parts[1]), int(parts[2])
            cpu = float(parts[3])
        except ValueError:
            continue
        comm = parts[4].strip()
        procs.append({"pid": pid, "ppid": ppid, "pgid": pgid, "pcpu": cpu,
                      "command": comm, "path": comm})
    return procs


def _owned_pgids_from_env():
    raw = os.environ.get("LIVE_SPEC_OWNED_PGIDS")
    if raw:
        vals = set()
        for tok in raw.replace(",", " ").split():
            try:
                vals.add(int(tok))
            except ValueError:
                pass
        return vals
    try:
        return {os.getpgrp()}
    except OSError:
        return set()


def main():
    owned_pgids = _owned_pgids_from_env()
    owned_tree = os.environ.get("LIVE_SPEC_OWNED_TREE", os.path.join(REPO_ROOT, ".live-spec"))
    self_pids = {os.getpid()}
    try:
        self_pids.add(os.getppid())
    except OSError:
        pass
    procs = _read_process_table()
    return run(procs, owned_pgids, owned_tree=owned_tree, self_pids=self_pids, out=sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
