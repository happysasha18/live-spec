#!/usr/bin/env python3
"""Flag a 👁️ ("needs his eyes") task whose own Source line is not his word.

27.08, his own word: three 👁️ tasks (q-527, q-529, q-536) turned out to trace to
`Source: found <date>` — an agent's own discovery during an earlier audit — not a quote of him.
None of them needed his eyes at all (see PLAN.md's Blockers). director's own act-classifier
never catches this class: it decides what a *live* message from him means, and none of these
three arrived that way — they were marked 👁️ by an earlier pass over old ROADMAP.md rows, then
never re-tested. `profile.md`'s `deferral` rule already says a marker is re-tested by
derivability every time it's touched; this script is the cheap, mechanical half of that re-test
for the one class that's checkable without judgment — whether the task's own Source line is
actually his word.

This is advisory, not wired into the push gate: a Source line starting with something other than
"owner" is a strong signal, not proof — some legitimate 👁️ tasks may cite an incident's date
before quoting him inline. Read the flagged rows; don't treat a clean run as license to stop
re-testing markers by hand.

Run: python3 scripts/check-eyes-marker.py
"""
import os
import sys

# Resolved from this file's own location, the way every sibling script in scripts/ resolves it: a
# cwd-relative "scripts" and "PLAN.md" made this script runnable only from the repo root.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from plan_checks import parse_tasks  # noqa: E402


def find_suspect_eyes_markers(text):
    tasks = parse_tasks(text)
    suspects = []
    for t in tasks:
        if t["mark"] != "👁️":
            continue
        source = (t["source"] or "").strip()
        if not source.lower().startswith("owner"):
            suspects.append(t)
    return suspects


def main():
    with open(os.path.join(REPO_ROOT, "PLAN.md"), encoding="utf-8") as f:
        text = f.read()
    suspects = find_suspect_eyes_markers(text)
    if not suspects:
        print("no 👁️ task with a non-owner Source line — clean")
        return 0
    print(f"{len(suspects)} 👁️ task(s) whose Source doesn't read as his own word:")
    for t in suspects:
        print(f"  {t['id']}: {t['title']}")
        print(f"    Source: {t['source']}")
    print("\nRe-test each by derivability (profile.md's deferral rule) before asking him.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
