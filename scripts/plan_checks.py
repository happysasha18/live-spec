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
    # --- written 2026-08-28 by plan-10 --------------------------------------------------------
    # Eleven rows, not thirty-seven. A key is worth its weight only where the row's subject is an
    # artifact that can drift back: a file, a script, a setting. The rows left without one are the
    # ones whose result is prose, a measurement, or a decision — a command reading those would only
    # restate them. Each command below is a grep, a `test`, or one guard that already exists and
    # was timed under half a second; guardrails/check-pin-drift.sh (37s) is deliberately NOT run
    # here, so q-588's key reads the gate's own reach instead.
    #
    # plan-3: prototype/ holds no tracked file, the transcripts are in the attic, and Fable's read
    # is where the step put it. (The directory itself survives, holding gitignored board mockups.)
    "plan-3": 'test -z "$(git ls-files prototype)" && test -d attic/transcripts && test -f .live-spec/PROBLEMS.md',
    # plan-7: the thirteen unbacked rules are in the attic and none of their numbers came back to
    # the rulebook — a retired number stays a hole, never reused.
    "plan-7": "test -f attic/live-spec-base-unbacked-rules-2026-08-26.md && ! grep -qE '^(11|14|15|18|19|20|21|23|28|30|32|33|34|35)\\. \\*\\*' skills/live-spec-base/SKILL.md",
    # plan-17: the measured floor stands in the plan, the per-step reader exists, and the project's
    # own boot file sends a session there rather than at the whole plan.
    "plan-17": "grep -q '17,575' PLAN.md && test -f scripts/plan-step.sh && grep -q 'plan-step.sh' CLAUDE.md",
    # q-458: the audit is its own external skill, installed, with this pack's binding and the lints
    # it declares per text surface.
    "q-458": 'test -d "$HOME/.claude/skills/text-audit" && test -f skills/text-audit-pack/SKILL.md && test -f .text-audit/lints.json',
    # q-537: both halves. The installed-vs-working comparison runs clean, the hook installer refuses
    # a registration already present, and the test that proves it is still there.
    "q-537": "bash guardrails/check-config-health.sh >/dev/null 2>&1 && grep -q 'already wired' scripts/install-session-hooks.sh && grep -q 'test_a_meter_wrapped_existing_entry_is_recognized_not_duplicated' tests/test_install_session_hooks.py",
    # q-588: the rule-price page still stands and the pin-drift gate still reaches it. Running the
    # gate itself would cost a session 37 seconds at every start.
    "q-588": "test -f .live-spec/r5-rule-prices-2026-08-11.md && grep -q 'r5-rule-prices-2026-08-11.md' guardrails/check-pin-drift.sh",
    # q-590: the rulebook's own head names the retired numbers, so a host reading it sees the holes.
    "q-590": "grep -q 'Rule 30 went first' skills/live-spec-base/SKILL.md",
    # q-592: the assertion is pinned to the bullet's own sentence, not to the bare invariant code.
    "q-592": "grep -q 'doc- and code-compaction stations run at every push' tests/test_compaction_discipline.py",
    # q-593: the count is derived from the body and asserted against the frontmatter in one home;
    # of the three copies that carried the literal number, one dropped it outright and two became
    # pointers at that home.
    "q-593": "grep -q 'the description of %s says %s rules' tests/test_request_classifier.py && grep -q 'This skill does not restate them' skills/build-pipeline/SKILL.md && grep -q 'states how many numbered rules it carries' skills/communicator/SKILL.md && grep -q 'states how many numbered rules it carries' skills/communicator/references/words.md",
    # q-595: the three restorations to rule 7 — the lead-in naming the bullets one family, the
    # pack-wide name for the shared document, and the by-hand route to the lane-opening script.
    "q-595": "grep -q 'The parallel-lanes rules sit underneath the fence' skills/live-spec-base/SKILL.md && grep -q 'convergence point the pen reconciles' skills/live-spec-base/SKILL.md && grep -q \"The script's own header states what it expects on disk\" skills/live-spec-base/SKILL.md",
    # q-598: the incident's record stands, and the gate reports each finding's outcome rather than
    # naming the command alone.
    "q-598": "grep -q 'step3-grid-derivation.json' DECISIONS.md && grep -q '_outcome_of' guardrails/check-worker-restore.py",
    # q-623: the gate reads where the command actually ran, and the three fixtures that fence the
    # narrowing are all present — one that reds nothing, two that still red.
    "q-623": "grep -q 'effective_dir' guardrails/check-worker-restore.py && grep -q 'test_an_unplaceable_cwd_with_a_neighbours_effective_dir_reds_nothing' tests/test_worker_restore.py && grep -q 'test_an_unplaceable_cwd_with_an_unknown_effective_dir_still_reds' tests/test_worker_restore.py && grep -q 'test_an_unplaceable_cwd_with_effective_dir_in_a_sibling_worktree_still_reds' tests/test_worker_restore.py",
    # q-624: the guard is installed on this machine, byte-identical to the copy in the tree, and
    # wired as a hook — the row's own "standing here, not merely built".
    "q-624": 'test -f "$HOME/.claude/hooks/worker-restore-guard.py" && cmp -s "$HOME/.claude/hooks/worker-restore-guard.py" hooks/worker-restore-guard.py && grep -q worker-restore-guard "$HOME/.claude/settings.json"',
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
