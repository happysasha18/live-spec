#!/usr/bin/env python3
"""Gate: a done mark on the board stands on an acceptance receipt, never on a hand.

A row reaches ✅ through one route — `task-admission.py verify` writes the receipt, `close` reads
it and then writes the mark.  PLAN.md is also an ordinary markdown file a person can type into,
and typing the mark produced a done nothing had verified: the board published it, the probe
counted it, and the work behind it may never have been done at all (the read of 2026-09-06).

Two arms, and each one is deliberately narrow so this gate reds on a real defect and never on the
project's own history:

  NEW DONE.  A row that is ✅ here and was not ✅ at the diff base became done in what is about to
  be published.  It must carry a checkpoint, and that checkpoint must hold a passed receipt whose
  frozen done is the done the row now reads.

  KERNEL-ERA DONE.  A row with a checkpoint went through the state machine, so its ✅ must stand
  on a passed receipt whatever the diff says.  A row closed before checkpoints existed carries
  none and is judged by neither arm — history is not retroactively red.

Base: LIVE_SPEC_DIFF_BASE, origin/main by default, the base the rest of the push chain reads.  An
unreadable base drops the first arm and keeps the second.

Usage: check-close-receipt.py [--plan PLAN.md] [--checkpoints .live-spec/checkpoints]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import plan_checks_core  # noqa: E402
import checkpoint  # noqa: E402

DONE = "✅"
RECEIPT = "RECEIPT: "


def marks(text):
    """{row id: its mark} for one plan's text."""
    return {t["id"]: t["mark"] for t in plan_checks_core.parse_tasks(text)}


def base_marks(tree, base):
    """The marks the plan carried at the diff base, or None when the base is unreadable.

    Read in the tree that holds the plan, never in this file's own repository: the gate is run
    against a fixture host as well as against the pack, and each must be judged by its own base.
    """
    got = subprocess.run(["git", "show", "%s:PLAN.md" % base], cwd=str(tree),
                         capture_output=True, text=True)
    return marks(got.stdout) if got.returncode == 0 else None


def recorded_hash(block):
    """The row's own `**DOD hash.**` digest, or None."""
    for line in block:
        if line.startswith("**DOD hash.**"):
            rest = line[len("**DOD hash.**"):].split()
            return rest[0] if rest else None
    return None


def last_receipt(path):
    body = checkpoint.read_checkpoint(path)["sections"].get("DONE", "")
    for line in reversed(body.splitlines()):
        if line.startswith(RECEIPT):
            try:
                return json.loads(line[len(RECEIPT):])
            except ValueError:
                return None
    return None


def faults(plan_path, checkpoints_dir, base):
    text = Path(plan_path).read_text(encoding="utf-8")
    tasks = plan_checks_core.parse_tasks(text)
    was = base_marks(Path(plan_path).resolve().parent, base)
    out = []
    for task in tasks:
        if task["mark"] != DONE:
            continue
        cp = Path(checkpoints_dir) / (task["id"] + ".md")
        newly = was is not None and was.get(task["id"]) != DONE
        if not cp.exists():
            if newly:
                out.append("%s reads done and has no checkpoint: a row closes through `verify` "
                           "and `close`, which open one at admission. A done typed onto the plan "
                           "is not a close." % task["id"])
            continue
        receipt = last_receipt(cp)
        if not receipt:
            out.append("%s reads done and its checkpoint holds no acceptance receipt: run "
                       "`task-admission.py verify %s --by <someone who did not hold the row>`, "
                       "then `close`." % (task["id"], task["id"]))
            continue
        if receipt.get("verdict") != "passed":
            failed = ", ".join(c for c, code in receipt.get("checks", []) if code != 0)
            out.append("%s reads done over a FAILED acceptance receipt (%s did not pass). The "
                       "presence of a check is not success." % (task["id"], failed or "a check"))
            continue
        digest = recorded_hash(task["body"])
        if digest and receipt.get("dod_hash") != digest:
            out.append("%s reads done against a definition of done the receipt did not verify "
                       "(receipt %s, row %s): verify it again against the done as it now reads."
                       % (task["id"], receipt.get("dod_hash"), digest))
        if checkpoint.read_checkpoint(cp)["status"] != "closed":
            out.append("%s reads done with its checkpoint still open: the close writes the "
                       "mark after it closes the sheet, never instead of it." % task["id"])
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(ROOT / "PLAN.md"))
    parser.add_argument("--checkpoints", default=str(ROOT / ".live-spec" / "checkpoints"))
    parser.add_argument("--base", default=os.environ.get("LIVE_SPEC_DIFF_BASE", "origin/main"))
    args = parser.parse_args()

    if not Path(args.plan).exists():
        print("   (no PLAN.md in this tree — the gate stands down by name)")
        return 0
    bad = faults(args.plan, args.checkpoints, args.base)
    if not bad:
        print("   every done row on the board stands on a passed acceptance receipt.")
        return 0
    print("BLOCKED — a done mark that no receipt stands behind:")
    for line in bad:
        print("  " + line)
    return 1


if __name__ == "__main__":
    sys.exit(main())
