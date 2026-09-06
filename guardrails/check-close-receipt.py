#!/usr/bin/env python3
"""Gate: a done mark on the board stands on an acceptance receipt, never on a hand.

A row is meant to reach ✅ through one route — `task-admission.py verify` writes the receipt,
`close` reads it and then writes the mark.  PLAN.md is also an ordinary markdown file a person can
type into, and typing the mark produced a done nothing had verified: the board published it, the
probe counted it, and the work behind it may never have been done at all (the read of 2026-09-06).

WHAT THIS GATE CANNOT HOLD, said rather than left to be discovered.  A receipt is plain text in
the checkpoint, and `tree_hash` deliberately leaves the checkpoint directory out of the tree it
pins, so a hand-written RECEIPT line satisfies this gate exactly as a real one does.  What the
gate buys is that forging a done takes a forged receipt naming a verifier, a verdict and the
admitted done's own digest, sitting in the diff for a reader — instead of one typed character.

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
import re
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


ZEROS = re.compile(r"^0{7,40}$")


def resolve_base(tree, base):
    """The commit-ish this gate compares against, or None when there is none to compare against.

    The two sibling gates (check-prover-record.sh, check-skill-review.sh) already guard this and
    this one did not: an EMPTY base — which is what `LIVE_SPEC_DIFF_BASE: ${{ github.event.before }}`
    sets on a pull request — left `git show :PLAN.md` reading the INDEX and exiting 0, so the base
    marks equalled the current marks, no row was ever "newly done", and the first arm below stood
    down on every PR run in silence (the adversarial read of 2026-09-06). An all-zero base, which
    is what a branch's first push carries, did the same.
    """
    base = (base or "").strip()
    if not base or ZEROS.match(base):
        base = "origin/main"
    ok = subprocess.run(["git", "rev-parse", "--verify", "--quiet", base + "^{commit}"],
                        cwd=str(tree), capture_output=True, text=True)
    return base if ok.returncode == 0 else None


def base_marks(tree, base):
    """The marks the plan carried at the diff base, or None when the base names no commit.

    Read in the tree that holds the plan, never in this file's own repository: the gate is run
    against a fixture host as well as against the pack, and each must be judged by its own base.
    """
    resolved = resolve_base(tree, base)
    if resolved is None:
        return None
    got = subprocess.run(["git", "show", "%s:PLAN.md" % resolved], cwd=str(tree),
                         capture_output=True, text=True)
    return marks(got.stdout) if got.returncode == 0 else None


def recorded_hash(block):
    """The row's own `**DOD hash.**` digest, or None."""
    for line in block:
        if line.startswith("**DOD hash.**"):
            rest = line[len("**DOD hash.**"):].split()
            return rest[0] if rest else None
    return None


def read_dod_anchor(path):
    """The digest of the done the row was admitted with, off its checkpoint, or None."""
    body = checkpoint.read_checkpoint(path)["sections"].get("DONE", "")
    for line in reversed(body.splitlines()):
        if line.startswith("DOD: "):
            return line[len("DOD: "):].strip() or None
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
        # The anchor the checkpoint carries from admission. `verify` is the only other reader of
        # it and never runs again on a closed row, so without this arm deleting the row's
        # `**DOD hash.**` line after the close left `digest` None, the comparison below skipped,
        # and the row published green against a done nobody verified — the same contract swap the
        # anchor was added to catch, one step later (the adversarial read of 2026-09-06).
        anchor = read_dod_anchor(cp)
        if anchor and not digest:
            out.append("%s reads done and no longer carries the hash of its definition of done, "
                       "while its checkpoint still holds the one it was admitted with (%s): "
                       "removing the hash is not a new contract. Put the line back."
                       % (task["id"], anchor))
            continue
        if anchor and digest and anchor != digest:
            out.append("%s reads done against a definition of done it was not admitted with "
                       "(checkpoint holds %s, the row now reads %s): a done changes through "
                       "`correct`, which keeps the previous text and hash."
                       % (task["id"], anchor, digest))
            continue
        for name, value in (("row", digest), ("checkpoint anchor", anchor)):
            if value and receipt.get("dod_hash") != value:
                out.append("%s reads done against a definition of done the receipt did not verify "
                           "(receipt %s, %s %s): verify it again against the done as it now reads."
                           % (task["id"], receipt.get("dod_hash"), name, value))
                break
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
