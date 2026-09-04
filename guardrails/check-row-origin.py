#!/usr/bin/env python3
"""check-row-origin.py — every open row on the board says what raised it (rule 41, SPEC INV-327).

THE INCIDENT. The owner, twice on 2026-09-04, across two of his own projects: he reads a board of
rows whose titles are plain and whose origin is invisible to him, so he sees work producing work
and cannot tell which of it he ever asked for. On the live-spec board that day, four of five open
rows had been raised by the pack's own reviews rather than by him. The pack had already met this
disease once — a findings log where 47 of 59 entries came from its own reviews, retired the night
before — and it grew straight back in the rows.

WHAT THIS REFUSES. An open row in the plan's `## Tasks` section whose `**Group:** … · **Priority:**
…` line carries no `· **Raised:** <word>`, or carries a word outside the three rule 41 names:

  asked  the person raised it.
  found  the pack's own machinery raised it — a check, a review, a test, a reading — and the person
         then took it. A finding never becomes a row on a session's own word.
  sent   another project raised it, through the inbox or a published contract.

Closed rows are not read: the finished work lives in a table that never carried the field, and
reading it would make this assert on the shape of the archive rather than on the work in hand.

Usage: check-row-origin.py [plan-path]   (default: PLAN.md under the repo root)
Exit 0 when every open row names its origin; exit 1 naming each row that does not. Stdlib only.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))


def main(argv):
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        root = os.getcwd()
    plan = argv[1] if len(argv) > 1 else os.path.join(root, "PLAN.md")
    if not os.path.isfile(plan):
        print("OK (row origin): no plan at %s — nothing to read." % plan)
        return 0

    sys.path.insert(0, os.path.join(root, "scripts"))
    import plan_checks_core as core

    with open(plan, encoding="utf-8") as fh:
        tasks = core.parse_tasks(fh.read())

    missing, unknown = [], []
    for t in tasks:
        if t["mark"] == "✅":
            continue
        raised = (t["raised"] or "").strip().lower()
        if not raised:
            missing.append(t["id"])
        elif raised not in core.RAISED_WORDS:
            unknown.append("%s (%s)" % (t["id"], raised))

    if missing or unknown:
        if missing:
            print("FAIL (row origin): these open rows do not say what raised them: %s"
                  % ", ".join(missing))
        if unknown:
            print("FAIL (row origin): these open rows name something outside the three words: %s"
                  % ", ".join(unknown))
        print("  Fix: add `· **Raised:** asked|found|sent` to each row's Group/Priority line.")
        print("  asked — the person raised it. found — a check, review, test or reading did, and the")
        print("  person then took it. sent — another project did. A finding never becomes a row on a")
        print("  session's own word (rule 41).")
        return 1

    open_rows = sum(1 for t in tasks if t["mark"] != "✅")
    print("OK (row origin): all %d open row(s) say what raised them." % open_rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
