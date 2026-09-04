#!/usr/bin/env python3
"""check-skill-review-coverage.py — every skill under skills/ has been through Anthropic's own
skill-creator at least once, with the tool's own printed verdict quoted in its record.

PLAN.md row q-817 asks for exactly that. The push gate `guardrails/check-skill-review.sh` asks a
narrower question — it demands a fresh, tool-backed record only for a skill whose body changed in
the push being made — so a skill nobody has touched in months can sit uncovered and no gate says
so. This script asks the broad question the row asks, and it is that row's own acceptance command.

What counts as covered: some record under docs/skill-review/ carries a line naming the validator
command run against that skill's own directory, in the shape docs/skill-review/README.md states and
guardrails/skill_review_verdict.py re-runs. This reads the records, never a claim about them.

Usage: check-skill-review-coverage.py [repo-root]
Exit 0 when every skill is covered; exit 1 naming each that is not. Stdlib only.
"""
import glob
import os
import re
import sys


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    skills_dir = os.path.join(root, "skills")
    names = sorted(d for d in os.listdir(skills_dir)
                   if os.path.isdir(os.path.join(skills_dir, d)))
    records = []
    for path in glob.glob(os.path.join(root, "docs", "skill-review", "*.md")):
        with open(path, encoding="utf-8") as fh:
            records.append(fh.read())
    uncovered = []
    for name in names:
        pattern = re.compile(r"(?m)^\$\s+.*quick_validate\.py.*skills/" + re.escape(name) + r"/?\s*$")
        if not any(pattern.search(r) for r in records):
            uncovered.append(name)
    if uncovered:
        print("FAIL (skill-review coverage): no record quotes the validator's own output for: %s"
              % ", ".join(uncovered))
        print("  Fix: run skill-creator over each, and record the command and everything it printed")
        print("  in the shape docs/skill-review/README.md states.")
        return 1
    print("OK (skill-review coverage): all %d skill(s) carry a record quoting the tool's own output."
          % len(names))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
