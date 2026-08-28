"""The commands that verify each plan task, in one home, plus the one parser for PLAN.md's
`## Tasks` section that both readers share.

A status board a person edits by hand must not also be an execution surface. `PLAN.md`
therefore holds only prose, and the commands that decide whether a task is really done live
here, keyed by the task's stable id (`plan-N` for a step carried over from the plan's own
numbered steps, `q-NNN` for a row folded in from the former ROADMAP.md queue) — stable across
title edits, unlike the title text. A task with no entry here falls back to the mark a person
typed in the plan (✅ · 🔄 · ⬜ · ⛔ · 👁️). A task with no check is reported DECLARED, not
invented — that is existing, correct behaviour, not a gap to fill.

Both readers of the plan import this module: `scripts/state-probe.sh` (the Canon a session
prints at its start) and `scripts/render-board.sh` (the same Canon as a page). Parsing PLAN.md's
`## Tasks` section lives here too, in `parse_tasks`, for the same reason the checks do: two
independent parses of the same heading shape already drifted apart once (the divergence
`tests/test_board_matches_the_canon.py` was written to catch) — one home means the two callers
cannot disagree about what a task's mark, group, priority or source is.
"""

import re

CHECKS = {
    "plan-0": "test -f PLAN.md && test -f scripts/state-probe.sh && ! test -d /private/tmp/ls-director && test -f attic/DIRECTOR_HANDOFF-2026-08-26-decisions.md",
    # plan-1's key was removed 2026-08-28 with its task: the board rotation folded plan-1 into
    # plan-11, and its check ("the render script exists and is executable") was the file-existence
    # proxy plan-10 names as a defect in its own text. plan-11 gets a key when its acceptance is met.
    "plan-2": 'test ! -f evals/director.md && test "$(git log -1 --format=%ct -- evals/director/traces)" -ge "$(git log -1 --format=%ct -- skills/director/SKILL.md)" && python3 evals/director/check.py --all 2>/dev/null | tail -1 | grep -qv " 0 of "',
    # Step 6 tore machinery down and, more often, proved a piece of it earned its place. What it
    # leaves behind that a command can see: the plan carries no executable line and neither reader
    # looks for one, the checks have this one home, and the read-only report on wiring a decision
    # into the push gate runs clean.
    # Every command in this file runs on the probe, and the probe is the first thing a session
    # does — so each one stays cheap. No test suite here: the guard for the line below is
    # tests/test_plan_is_not_executable.py, and the suite's home is the push gate and CI.
    "plan-6": "! grep -q '^<!-- check:' PLAN.md && ! grep -q '<!-- check:' scripts/state-probe.sh scripts/render-board.sh && test -f tests/test_plan_is_not_executable.py && python3 scripts/director-wire-report.py >/dev/null 2>&1",
    "plan-8": """test "$(cat VERSION)" != 5.0.0 && grep -q 'skills/director' MIGRATION.md""",
    "plan-9": "ls ~/tlvphotos/.claude/skills 2>/dev/null | grep -q director && test -f ~/tlvphotos/.live-spec/VERSION",
}

# A task header looks like "### <mark emoji> <Task Name> — id: <plan-N|q-N>" — no brackets
# around the mark, an em dash before "id:". The title is matched non-greedy so a title that
# itself contains an em dash still stops at the literal " — id: " that ends the heading.
_HEADER_RE = re.compile(r"^### (\S+) (.+?) — id: (\S+)$")
_GROUP_RE = re.compile(r"^\*\*Group:\*\*\s*(.+?)\s*·\s*\*\*Priority:\*\*\s*(.+)$")
_SOURCE_RE = re.compile(r"^\*\*Source:\*\*\s*(.+)$")
_COVERED_BY_RE = re.compile(r"^\*\*Covered by:\*\*\s*(.+)$")
_DEFERRED_RE = re.compile(r"^\*\*Deferred:\*\*\s*(.+)$")
_BLOCKED_BY_RE = re.compile(r"^\*\*Blocked by:\*\*\s*(.+)$")


def parse_tasks(text):
    """Parse PLAN.md's `## Tasks` section into a list of task dicts, in file order.

    Each dict carries: mark (the emoji as typed), title, id, group, priority, source, covered_by,
    deferred, blocked_by (each None if that line was missing), check (CHECKS.get(id)), and body —
    the remaining lines of the task's block (its full original prose and `**Acceptance:**` line,
    for the `plan-N` tasks that still carry them), for a caller that wants more than the summary
    fields.

    covered_by/deferred/blocked_by (27.08, his word) are what a reader uses to tell a task that
    only LOOKS idle apart: covered_by names the task that actually carries this work (a fold
    pointer); deferred names his own decision to postpone it, not an obstacle; blocked_by names
    a real, understood cause a ⛔ task can't move past on its own. A ⛔ task with none of the
    three is a mislabel, not a fourth state — see scripts/state-probe.sh's ranking, the one
    reader that acts on this distinction today.
    """
    tasks = []
    cur = None
    in_section = False
    for line in text.splitlines():
        if line.strip() == "## Tasks":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        m = _HEADER_RE.match(line.rstrip())
        if m:
            cur = {
                "mark": m.group(1),
                "title": m.group(2),
                "id": m.group(3),
                "group": None,
                "priority": None,
                "source": None,
                "covered_by": None,
                "deferred": None,
                "blocked_by": None,
                "check": CHECKS.get(m.group(3)),
                "body": [],
            }
            tasks.append(cur)
            continue
        if cur is None:
            continue
        stripped = line.strip()
        gm = _GROUP_RE.match(stripped)
        if gm and cur["group"] is None:
            cur["group"], cur["priority"] = gm.group(1), gm.group(2)
            continue
        sm = _SOURCE_RE.match(stripped)
        if sm and cur["source"] is None:
            cur["source"] = sm.group(1)
            continue
        cbm = _COVERED_BY_RE.match(stripped)
        if cbm and cur["covered_by"] is None:
            cur["covered_by"] = cbm.group(1)
            continue
        dm = _DEFERRED_RE.match(stripped)
        if dm and cur["deferred"] is None:
            cur["deferred"] = dm.group(1)
            continue
        bbm = _BLOCKED_BY_RE.match(stripped)
        if bbm and cur["blocked_by"] is None:
            cur["blocked_by"] = bbm.group(1)
            continue
        cur["body"].append(line)
    return tasks
