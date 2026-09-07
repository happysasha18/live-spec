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

WHERE IT IS MEANT TO RUN.  In CI, on a pushed commit, in a fresh checkout — see the gates
workflow.  It runs locally too, and says so; the point of the CI placement is that the machine
running the check is not the machine that wrote the receipt.

WHAT REDS.  A done row whose acceptance command fails.  A done row whose acceptance command was
changed after admission.  A done row with no acceptance command at all is REPORTED and does not
red: rows admitted before the acceptance became a condition of admission carry none, and this
gate is not a retroactive demand on them.

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

DONE = "✅"
ACCEPT_ANCHOR = "ACCEPT: "
# One command's own budget. Every key in this pack's table is a grep, a `test`, or one small
# program — the state probe runs the whole set at every session start — so a key past this is a
# key that hung, and a hung key must red by name rather than take the runner down with it.
PER_KEY_SECONDS = 300


def digest(text):
    import hashlib
    return hashlib.sha256(" ".join(str(text).split()).encode("utf-8")).hexdigest()


def admitted_acceptance(cp):
    """The digest of the acceptance command the row was admitted with, or None."""
    if not cp.exists():
        return None
    body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
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


def run_one(tree, command):
    try:
        done = plan_checks_core.run_key(command, mark=True, cwd=tree, timeout=PER_KEY_SECONDS)
    except subprocess.TimeoutExpired:
        return 1, "the check did not finish inside %ds" % PER_KEY_SECONDS
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)
    text = (done.stdout or b"") if isinstance(done.stdout, bytes) else (done.stdout or "")
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    first = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    return done.returncode, first


def judge(plan_path, checkpoints_dir, jobs):
    tree = Path(plan_path).resolve().parent
    tasks = plan_checks_core.parse_tasks(Path(plan_path).read_text(encoding="utf-8"))
    table = acceptance_table(tree)
    ran, faults, unanchored, keyless, offmachine = [], [], [], [], []

    to_run = []
    for task in tasks:
        if task["mark"] != DONE:
            continue
        command = (table.get(task["id"]) or "").strip()
        # The anchor is read FIRST. Read after the keyless arm, deleting the row's one line from
        # the check table turned a forged done into a row this gate merely reported and passed —
        # the whole of claim one defeated in one deleted line (the adversarial read of
        # 2026-09-07). A row admitted through the kernel always carries an anchor, so an anchor
        # standing over a missing key is a key somebody removed.
        anchor = admitted_acceptance(Path(checkpoints_dir) / (task["id"] + ".md"))
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
                code, first = future.result()
            except Exception as exc:  # noqa: BLE001 - a key that threw is a key that failed
                code, first = 1, "the check did not finish: %s" % exc
            ran.append(rid)
            if code != 0:
                faults.append("%s: its acceptance command failed here, at this commit%s"
                              % (rid, (" — " + first[:120]) if first else ""))
    return ran, faults, unanchored, keyless, offmachine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(ROOT / "PLAN.md"))
    parser.add_argument("--checkpoints", default=str(ROOT / ".live-spec" / "checkpoints"))
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()

    if not Path(args.plan).exists():
        print("   (no PLAN.md in this tree — the gate stands down by name)")
        return 0
    # The keys the probe runs are marked, so one of them starting a reader is caught by the
    # re-entry breaker rather than fanning out; this process is not itself a reader.
    os.environ.pop("LIVE_SPEC_EVALUATING", None)
    try:
        ran, faults, unanchored, keyless, offmachine = judge(
            args.plan, args.checkpoints, max(1, args.jobs))
    except TableUnreadable as exc:
        print("BLOCKED — the acceptance table this gate runs from is unreadable, so nothing here "
              "judged anything: %s" % exc)
        return 1

    print("   ran %d done row(s)' own acceptance command at this commit." % len(ran))
    if unanchored:
        print("   %d of them predate the acceptance anchor, so what ran is the command the tree "
              "records now: %s" % (len(unanchored), ", ".join(sorted(unanchored))))
    if offmachine:
        print("   %d done row(s) hold a key that reads this machine rather than the tree, which a "
              "checkout cannot judge; admission refuses such a key today: %s"
              % (len(offmachine), ", ".join(sorted(offmachine))))
    if keyless:
        print("   %d done row(s) record no acceptance command and were not run (admitted before "
              "one was required): %s" % (len(keyless), ", ".join(sorted(keyless))))
    if not faults:
        print("   every done row's acceptance passes here.")
        return 0
    print("BLOCKED — a done row whose acceptance does not pass at this commit:")
    for line in faults:
        print("  " + line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
