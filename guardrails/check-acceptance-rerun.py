#!/usr/bin/env python3
"""Gate: every done row's own acceptance command is RUN, here, at this commit.

The receipt a close reads is plain text in a checkpoint, and the tree hash that pins the evidence
deliberately leaves that directory out.  So a hand-written `RECEIPT: {"verdict": "passed"}` line
satisfied both the close and the receipt gate, and the board published a done nobody had earned
(the owner's word, 2026-09-07).  A text nobody re-runs cannot be the source of a passing
acceptance.  This check is that source: it takes the commit as it stands and runs each done row's
recorded acceptance command itself.  A forged receipt buys nothing here, because nothing here
reads a receipt.

WHAT IT RUNS.  The command the tree's own check table records for the row, and only where that
command is the one the row was ADMITTED with — the checkpoint carries the admitted command's
digest under `ACCEPT: `, and a row whose table entry no longer matches it is reported as a changed
acceptance and reds, rather than being run.  A row admitted before that anchor existed carries
none; its command is run and the line says the anchor is missing, which is the non-retroactive
line this pack takes with every anchor.

WHICH ROWS RUN (the owner's word, 2026-09-07 22:00: "CI runs a fixed release core and only a
limited set of actually-affected obligations"). The release core is a list of GATES —
`run_modes.release.core` in `guardrails.config.json` — and this script is one member of that
list (gate v). It is not a list of PLAN.md rows, and this gate reads no such list: the two are
different kinds of thing, and mixing them here was a category error, corrected 2026-09-08. What
this gate selects, on its own, is the AFFECTED obligations alone: a done row whose own contract or
own files moved in the pushed range — its `Done when` text or its `DOD hash.` line in PLAN.md
changed, the acceptance command recorded for it in `scripts/plan_checks.py` changed, or a file its
acceptance command names changed. The pushed range is read the same way `check-prover-record.sh`
reads it: `LIVE_SPEC_DIFF_BASE` if it resolves, else `origin/main`, else `HEAD~1`.
When no base resolves at all (a single-commit tree with no upstream — a synthetic tree, never a
real push), nothing can be compared against, so every done row runs — the same lean the prover
record's own carve-out takes ("the carve-out cannot be judged and the full gate runs"), never the
other way around into running nothing.
A done row that is not affected — with a base that DID resolve — never runs here, and the summary
line below says why every row that DID run was selected.

WHERE IT IS MEANT TO RUN.  In CI, on a pushed commit, in a fresh checkout — see the gates
workflow.  It runs locally too, and says so; the point of the CI placement is that the machine
running the check is not the machine that wrote the receipt.

WHAT REDS.  A selected row whose acceptance command fails.  A selected row whose acceptance
command was changed after admission.  A selected row with no acceptance command at all is
REPORTED and does not red: rows admitted before the acceptance became a condition of admission
carry none, and this gate is not a retroactive demand on them.

Usage: check-acceptance-rerun.py [--plan PLAN.md] [--checkpoints DIR] [--jobs N]
"""

import argparse
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import plan_checks_core  # noqa: E402
import checkpoint  # noqa: E402
import run_modes  # noqa: E402 — this script's own guardrails/ dir, the run-mode contract's reader

DONE = "✅"
ACCEPT_ANCHOR = "ACCEPT: "
# EMERGENCY STOP on one command, and nothing else. It exists so a process this run owns that has
# hung ends by name instead of holding the whole gate open — it takes no part in any verdict, and
# its value is never derived from how fast any machine runs a check (rule 43,
# skills/live-spec-base/SKILL.md: "a clock never certifies a budget"). 300s is the pack's existing
# figure, carried over unchanged; nothing here re-measures or re-derives it.
EMERGENCY_STOP_SECONDS = 300


def digest(text):
    import hashlib
    return hashlib.sha256(" ".join(str(text).split()).encode("utf-8")).hexdigest()


class CheckpointUnreadable(Exception):
    """A selected row's own checkpoint would not load, so its admitted acceptance is unknown."""


def admitted_acceptance(cp):
    """The digest of the acceptance command the row was admitted with, or None.

    A checkpoint that will not parse raises rather than returning None: unknown-anchor and
    no-anchor are different states, and reading the first as the second would run whatever the
    check table happens to say today for a row whose admission nobody can read. Before this, an
    unreadable checkpoint took the whole gate down with a traceback and no verdict at all.
    """
    if not cp.exists():
        return None
    try:
        parsed = checkpoint.read_checkpoint(cp)
    except (ValueError, OSError) as exc:
        raise CheckpointUnreadable(str(exc))
    body = parsed["sections"].get("DONE", "")
    for line in reversed(body.splitlines()):
        if line.startswith(ACCEPT_ANCHOR):
            return line[len(ACCEPT_ANCHOR):].strip() or None
    return None


class TableUnreadable(Exception):
    """The one file this whole gate stands on did not load."""


def acceptance_table(tree):
    """The tree's own check table. A table that will not load STOPS this gate.

    It used to return an empty map on any import error, which turned every done row keyless and
    the gate green — fail-open on the single file the gate depends on (the adversarial read of
    2026-09-07).
    """
    keys = Path(tree) / "scripts" / "plan_checks.py"
    if not keys.exists():
        raise TableUnreadable("no scripts/plan_checks.py in %s, so no row has an acceptance "
                              "command to run" % tree)
    import importlib.util
    spec = importlib.util.spec_from_file_location("host_plan_checks", keys)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        raise TableUnreadable("scripts/plan_checks.py does not load: %s" % exc)
    table = getattr(module, "CHECKS", None)
    if not isinstance(table, dict):
        raise TableUnreadable("scripts/plan_checks.py names no CHECKS table")
    return table


def _load_checks_text(text):
    """A CHECKS table from some other point in history, loaded the same way acceptance_table
    loads the tree's current one. Text that fails to load reads as an empty table — its commands
    are simply unknown at that point in history, which makes every one of the tree's current
    commands read as having moved (the same lean-toward-running default a missing base file
    takes below), never as unreadable-therefore-silent."""
    import importlib.util
    import tempfile
    fd, temp_path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        spec = importlib.util.spec_from_file_location("host_plan_checks_base_%d" % os.getpid(),
                                                       temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        table = getattr(module, "CHECKS", None)
        return table if isinstance(table, dict) else {}
    except Exception:  # noqa: BLE001 - a base version that won't load names nothing
        return {}
    finally:
        os.unlink(temp_path)


def _git(tree, *args):
    return subprocess.run(["git", *args], cwd=str(tree), capture_output=True, text=True)


def diff_base(tree):
    """The pushed range's base commit, read exactly as check-prover-record.sh reads it:
    `LIVE_SPEC_DIFF_BASE` if it resolves, else `origin/main`, else `HEAD~1` — so the two never
    disagree about what "pushed" means. None when nothing resolves at all."""
    def resolves(ref):
        return _git(tree, "rev-parse", "--verify", "--quiet", ref + "^{commit}").returncode == 0

    env_base = os.environ.get("LIVE_SPEC_DIFF_BASE", "")
    if env_base and env_base != "0" * 40 and resolves(env_base):
        return env_base
    if resolves("origin/main"):
        return "origin/main"
    if resolves("HEAD~1"):
        return "HEAD~1"
    return None


def changed_paths(tree, base):
    """Paths that differ between base and HEAD, or an empty set when no range resolves."""
    if base is None:
        return set()
    out = _git(tree, "diff", "--name-only", base, "HEAD")
    return {p for p in out.stdout.splitlines() if p.strip()}


def file_at(tree, ref, relpath):
    """relpath's text as of ref, or None where it did not exist there."""
    out = _git(tree, "show", "%s:%s" % (ref, relpath))
    return out.stdout if out.returncode == 0 else None


def dod_signature(task):
    """The row's own contract, read off its two fixed PLAN.md lines: what counts as done, and the
    hash pinned at first verification. Either line moving is the row's contract moving."""
    return "\n".join(line for line in task.get("body", [])
                     if line.startswith("**Done when:**") or line.startswith("**DOD hash.**"))


def contract_moved(tree, base, current_tasks):
    """Task ids whose Done-when text or DOD hash line differs between base and HEAD."""
    if base is None:
        return set()
    base_text = file_at(tree, base, "PLAN.md")
    base_tasks = plan_checks_core.parse_tasks(base_text) if base_text is not None else []
    base_sig = {t["id"]: dod_signature(t) for t in base_tasks}
    return {t["id"] for t in current_tasks if base_sig.get(t["id"]) != dod_signature(t)}


def acceptance_moved(tree, base, current_table):
    """Task ids whose recorded acceptance command in scripts/plan_checks.py differs between base
    and HEAD."""
    if base is None:
        return set()
    base_text = file_at(tree, base, "scripts/plan_checks.py")
    base_table = _load_checks_text(base_text) if base_text is not None else {}
    return {tid for tid, cmd in current_table.items()
            if (base_table.get(tid) or "").strip() != (cmd or "").strip()}


def files_named_moved(current_table, changed):
    """Task ids whose acceptance command's own text names one of the changed paths.

    A textual read only, by design (kept simple on purpose): a changed path is checked for
    appearing literally inside the command string, rather than parsing the command's shell or
    globbing its arguments. A changed path necessarily exists in the tree at one end of the diff,
    so a command whose text carries it is a command naming a file that moved.
    """
    if not changed:
        return set()
    moved = set()
    for tid, cmd in current_table.items():
        cmd = cmd or ""
        if any(path and path in cmd for path in changed):
            moved.add(tid)
    return moved


def select(tree, tasks, table):
    """The affected obligations, and the reason each selected row was picked. Returns
    (reasons: {id: str}, done_tasks: [task, ...]).

    No release-core list is read here. The release core (`run_modes.release.core` in
    `guardrails.config.json`) is a fixed list of GATES — this script is one entry in it (gate v)
    — and a gate does not also select rows off its own membership in that list; that would be a
    gate asking whether it is a gate. What this gate selects, on its own, is the affected
    obligations alone: the rows this push actually touched.
    """
    base = diff_base(tree)
    done_tasks = [t for t in tasks if t["mark"] == DONE]

    if base is None:
        # Nothing to compare against — the prover record's own carve-out takes the same lean
        # ("the carve-out cannot be judged and the full gate runs"): every done row runs, rather
        # than a range nobody could measure silently excusing all of history.
        return ({t["id"]: "no pushed range resolved here, so the full historical sweep ran"
                for t in done_tasks}, done_tasks)

    changed = changed_paths(tree, base)
    moved_contract = contract_moved(tree, base, tasks)
    moved_accept = acceptance_moved(tree, base, table)
    moved_files = files_named_moved(table, changed)

    reasons = {}
    for task in done_tasks:
        tid = task["id"]
        if tid in moved_contract:
            reasons[tid] = "its Done-when text or DOD hash moved in the pushed range"
        elif tid in moved_accept:
            reasons[tid] = "its recorded acceptance command moved in the pushed range"
        elif tid in moved_files:
            reasons[tid] = "a file its acceptance command names changed in the pushed range"
        # else: closed history — never walked, never even table-looked-up below.
    return reasons, done_tasks


def run_one(tree, command):
    """Returns (code, first_line, stopped). `stopped` is True only when the emergency stop ended
    the process before it could return a verdict — that case never carries a `code` a caller
    should read as pass or fail (criterion 11: a runtime timeout takes no part in the verdict)."""
    try:
        done = plan_checks_core.run_key(command, mark=True, cwd=tree, timeout=EMERGENCY_STOP_SECONDS)
    except subprocess.TimeoutExpired:
        return (None,
                "the check hit the emergency stop before finishing (%ds)" % EMERGENCY_STOP_SECONDS,
                True)
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc), False
    text = (done.stdout or b"") if isinstance(done.stdout, bytes) else (done.stdout or "")
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    first = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    return done.returncode, first, False


def judge(plan_path, checkpoints_dir, jobs, mode):
    tree = Path(plan_path).resolve().parent
    tasks = plan_checks_core.parse_tasks(Path(plan_path).read_text(encoding="utf-8"))
    table = acceptance_table(tree)
    reasons, done_tasks = select(tree, tasks, table)
    # The mode's own composition binds what this run may take. `release` carries no cap and admits
    # the affected set whatever its size; `row` admits one target and `integration` five, so a run
    # named as either of those over a wider selection is refused here by the cap, naming the mode,
    # the cap and what was asked for. The selection above never grew with the corpus or with the
    # board's length, and this is what holds that in place rather than a comment saying so.
    run_modes.admit_targets(mode, sorted(reasons))
    ran, faults, unanchored, keyless, offmachine, unjudged = [], [], [], [], [], []

    to_run = []
    for task in done_tasks:
        if task["id"] not in reasons:
            continue
        command = (table.get(task["id"]) or "").strip()
        # The anchor is read FIRST. Read after the keyless arm, deleting the row's one line from
        # the check table turned a forged done into a row this gate merely reported and passed —
        # the whole of claim one defeated in one deleted line (the adversarial read of
        # 2026-09-07). A row admitted through the kernel always carries an anchor, so an anchor
        # standing over a missing key is a key somebody removed.
        try:
            anchor = admitted_acceptance(Path(checkpoints_dir) / (task["id"] + ".md"))
        except CheckpointUnreadable as exc:
            faults.append("%s: its own checkpoint does not load, so what it was admitted against "
                          "cannot be read here (%s). An unreadable admission is not a passed "
                          "one." % (task["id"], exc))
            continue
        if anchor and not command:
            faults.append("%s: it was admitted against an acceptance command whose digest is %s, "
                          "and the check table names none for it now. A removed check is not a "
                          "passed one." % (task["id"], anchor))
            continue
        if not command:
            keyless.append(task["id"])
            continue
        if anchor and anchor != digest(command):
            faults.append("%s: the acceptance command is not the one it was admitted with "
                          "(the checkpoint holds %s). A check rewritten after admission is not "
                          "the check the work was accepted against." % (task["id"], anchor))
            continue
        if plan_checks_core.reads_outside_the_tree(command):
            # The key reaches past what git carries, so a fresh checkout cannot judge it at all
            # and unknown is not failure — the same carve-out the plan readers already make.
            # No row admitted from 2026-09-07 on can carry such a key: `admit` refuses it, so
            # this arm covers the rows that predate that rule and closes with them.
            offmachine.append(task["id"])
            continue
        if not anchor:
            unanchored.append(task["id"])
        to_run.append((task["id"], command))

    # Every timeout lives in run_one, on the child itself. An `as_completed(timeout=...)` here
    # raised past this block and then blocked forever inside the pool's own exit, which waits for
    # the very threads the timeout was meant to escape — a deadline that made the hang worse.
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run_one, tree, cmd): (rid, cmd) for rid, cmd in to_run}
        for future in concurrent.futures.as_completed(futures):
            rid, cmd = futures[future]
            try:
                code, first, stopped = future.result()
            except Exception as exc:  # noqa: BLE001 - a key that threw is a key that failed
                code, first, stopped = 1, "the check did not finish: %s" % exc, False
            if stopped:
                # The emergency stop ended the process before it returned a verdict. Criterion 11:
                # that never counts as a failed acceptance and never turns the gate red on its own.
                unjudged.append("%s: %s" % (rid, first))
                continue
            ran.append(rid)
            if code != 0:
                faults.append("%s: its acceptance command failed here, at this commit%s"
                              % (rid, (" — " + first[:120]) if first else ""))
    return ran, faults, unanchored, keyless, offmachine, unjudged, len(tasks), len(done_tasks), reasons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(ROOT / "PLAN.md"))
    parser.add_argument("--checkpoints", default=str(ROOT / ".live-spec" / "checkpoints"))
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()

    if not Path(args.plan).exists():
        print("   (no PLAN.md in this tree — the gate stands down by name)")
        return 0

    # THE RUN NAMES ITS MODE BEFORE IT SELECTS A TARGET (Requirement 322 criterion 1, INV-328).
    # This is the acceptance run itself — gate v of the release core — so it is the place where a
    # mode and its composition are known: which rows this run may take, how many of them, and
    # whether what it returns is a verdict at all. A run that named no mode is refused here rather
    # than resolved to a default: `run_modes.resolve_mode` answers "row" for an empty environment,
    # which is the right answer to "what did this environment ask for" and the wrong thing for an
    # automatic run to be handed. CI names the mode on the step (.github/workflows/gates.yml), and
    # a person running this by hand names it too.
    try:
        mode = run_modes.named_mode()
    except ValueError as exc:
        print("BLOCKED — %s" % exc)
        return 1
    if mode is None:
        print("BLOCKED — this run named no mode, so nothing here knows what it may cover or "
              "whether it decides a verdict. Name one: LIVE_SPEC_RUN_MODE=%s (or "
              "LIVE_SPEC_PUSH_FULL, which names release)." % "|".join(run_modes.MODES))
        return 1
    # Criterion 8's first half, which nothing held: a manual run never STANDS as a CI or release
    # gate. `in_ci: false` sat in the config with no reader, so naming manual on a CI step turned
    # this gate into a one-word green — the faults printed and the step passed (the adversarial
    # read of 2026-09-08). A mode that may not stand as a gate is refused where a gate is what it
    # would be standing as, and the run says which variable made it a CI run.
    ci_marker = next((name for name in ("GITHUB_ACTIONS", "CI") if os.environ.get(name)), None)
    if ci_marker and not run_modes.stands_as_a_gate(mode):
        print("BLOCKED — this is a CI run (%s is set) and mode %r may never stand as a CI or "
              "release gate: it decides no verdict, so it can neither pass nor fail this step. "
              "Name the mode this gate actually is." % (ci_marker, mode))
        return 1
    # The keys the probe runs are marked, so one of them starting a reader is caught by the
    # re-entry breaker rather than fanning out; this process is not itself a reader.
    os.environ.pop("LIVE_SPEC_EVALUATING", None)
    try:
        ran, faults, unanchored, keyless, offmachine, unjudged, total, total_done, reasons = judge(
            args.plan, args.checkpoints, max(1, args.jobs), mode)
    except TableUnreadable as exc:
        print("BLOCKED — the acceptance table this gate runs from is unreadable, so nothing here "
              "judged anything: %s" % exc)
        return 1
    except run_modes.ModeCapExceeded as exc:
        # The mode's own cap refused this run's selection, and a run that may not take what it
        # selected returns no verdict on it. Caught by its own type: a bare ValueError here read
        # every fault inside judge() as a mode refusal and said so in the mode's words.
        print("BLOCKED — %s. Name the mode this run actually is, or narrow what it covers." % exc)
        return 1

    print("   %d row(s) in the plan, %d marked done, %d selected here (closed history is never "
          "walked): %s"
          % (total, total_done, len(reasons),
             ", ".join("%s — %s" % (tid, reasons[tid]) for tid in sorted(reasons)) or "(none)"))
    print("   run mode: %s — %s" % (mode, "it decides the verdict below"
                                    if run_modes.decides_verdict(mode)
                                    else "an explicit audit, and it decides no verdict"))
    print("   ran %d of the selected row(s)' own acceptance command at this commit." % len(ran))
    if unanchored:
        print("   %d of them predate the acceptance anchor, so what ran is the command the tree "
              "records now: %s" % (len(unanchored), ", ".join(sorted(unanchored))))
    if offmachine:
        print("   %d selected row(s) hold a key that reads this machine rather than the tree, "
              "which a checkout cannot judge; admission refuses such a key today: %s"
              % (len(offmachine), ", ".join(sorted(offmachine))))
    if keyless:
        print("   %d selected row(s) record no acceptance command and were not run (admitted "
              "before one was required): %s" % (len(keyless), ", ".join(sorted(keyless))))
    if unjudged:
        print("   %d selected row(s) UNJUDGED — the emergency stop ended the run before it could "
              "decide, so it is not a verdict and never a failed acceptance:" % len(unjudged))
        for line in unjudged:
            print("  " + line)
    if not faults:
        if unjudged:
            print("   %d selected row(s) that returned a verdict pass here; the %d UNJUDGED above "
                  "were decided by nothing." % (len(ran), len(unjudged)))
        else:
            print("   every selected row's acceptance passes here.")
        return 0
    for line in faults:
        print("  " + line)
    if not run_modes.decides_verdict(mode):
        # Criterion 8: a manual run never stands as a CI or release gate and decides no verdict.
        # What it found is printed above, in full, and it ends green because the reading it did is
        # a person's audit rather than a gate's judgement. A mode that decides no verdict cannot
        # block, and a run that wants to block names a mode that decides one.
        print("   the %r run reports the row(s) above and decides no verdict on them." % mode)
        return 0
    print("BLOCKED — a selected row whose acceptance does not pass at this commit (above).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
