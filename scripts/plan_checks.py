"""The commands that verify each plan step, in one home.

A status board a person edits by hand must not also be an execution surface. `PLAN.md` therefore
holds only prose, and the commands that decide whether a step is really done live here, keyed by
the step's number — stable across title edits, unlike the title text. A step with no entry here
falls back to the mark a person typed in the plan (`[x]`, `[~]`, `[ ]`, `[!]`).

Both readers of the plan import this module: `scripts/state-probe.sh` (the Canon a session prints
at its start) and `scripts/render-board.sh` (the same Canon as a page). One home, so the two can
never disagree about what "done" means for a step.
"""

CHECKS = {
    "0": "test -f PLAN.md && test -f scripts/state-probe.sh && ! test -d /private/tmp/ls-director && test -f attic/DIRECTOR_HANDOFF-2026-08-26-decisions.md",
    "1": "test -x scripts/render-board.sh",
    "2": 'test ! -f evals/director.md && test "$(git log -1 --format=%ct -- evals/director/traces)" -ge "$(git log -1 --format=%ct -- skills/director/SKILL.md)" && python3 evals/director/check.py --all 2>/dev/null | tail -1 | grep -qv " 0 of "',
    "6": "false",
    "8": """test "$(cat VERSION)" != 5.0.0 && grep -q 'skills/director' MIGRATION.md""",
    "9": "ls ~/tlvphotos/.claude/skills 2>/dev/null | grep -q director && test -f ~/tlvphotos/.live-spec/VERSION",
}
