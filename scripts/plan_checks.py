"""THIS PROJECT'S OWN commands that verify each plan task, in one home.

A status board a person edits by hand must not also be an execution surface. `PLAN.md`
therefore holds only prose, and the commands that decide whether a task is really done live
here, keyed by the task's stable id (`plan-N` for a step carried over from the plan's own
numbered steps, `q-NNN` for a row folded in from the former ROADMAP.md queue) — stable across
title edits, unlike the title text. A task with no entry here falls back to the mark a person
typed in the plan (✅ · 🔄 · 🔁 · ⬜ · ⛔ — five marks since 2026-09-04, his word: 👁️
"needs his eyes" retired, needing a person's word is a question asked in the reply, not a task
state; ⛔ "blocked" stays, narrowed to a real outside cause — an expired key, a dead credential, a
service that is down — never merely waiting on someone). A task with no check is reported
DECLARED, not invented — that is existing, correct behaviour, not a gap to fill.

**Every command below names this project's own files, and belongs to this project alone.** How a
plan is PARSED, how a mark is spelled, and how a row's state is computed from its command are a
different thing entirely — they hold for any project, and they live in `scripts/plan_checks_core.py`,
which this module imports and re-exports. That split is what lets a host install the probe and the
board (`adopt/install-status-view.sh`) and write its own commands in its own copy of this file,
instead of inheriting the table below.

The readers of the plan import this module rather than the core: `scripts/state-probe.sh` (the
Canon a session prints at its start) and `scripts/render-board.sh` (the same Canon as a page).
They get `parse_tasks` with this project's own commands already attached, so no reader has to know
the check map exists — one home means two callers cannot disagree about what a task's mark, group,
priority or source is.
"""

from plan_checks_core import (  # noqa: F401  (re-exported for this module's own callers)
    evaluate,
    key_failure_note,
    normalize_mark,
    reads_outside_the_tree,
)
from plan_checks_core import parse_tasks as _parse_tasks

CHECKS = {
    # plan-0: corrected 2026-09-01 — the old arm was four bare `test -f`/`test -d` clauses, the
    # exact file-existence proxy plan-10's own text names as a defect. The row's own acceptance
    # ("state-probe.sh confirms it matches origin/main, the tree is clean") cannot be read as
    # "zero commits ahead of origin/main" — that is the tree's ordinary working state, not a
    # defect, and a check demanding it would red on every session carrying unpushed work. What the
    # row actually left behind that stays true across ordinary work: this tree tracks
    # `origin/main` as its upstream, the stray `/private/tmp/ls-director` directory the migration
    # cleared stays gone, and the archived handoff carries its own real content, not just a path
    # that resolves.
    #
    # A fourth clause, `git status --porcelain` empty, was dropped 2026-09-02. It repeated the
    # same defect the paragraph above names one step over: it red on every session that had edits
    # in hand, so the row reported itself unfinished all day for a reason the row is not about.
    # The row's own "the tree is clean" means this is a real git tree with no project files left
    # outside it — the 133 outside-git files it checked — and says nothing about uncommitted work.
    "plan-0": 'test "$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)" = "origin/main" && ! test -d /private/tmp/ls-director && grep -q "Владелец подтвердил" attic/DIRECTOR_HANDOFF-2026-08-26-decisions.md',
    # q-807: the reopened mark is assigned once, and the blocked branch beside it is guarded by the
    # row's own blocked_by — so a merely-unfinished row cannot be painted blocked again. Anchored on
    # the assignment and on the guard, the two smallest things that must survive any rewording of
    # that block; an earlier arm pinned one exact expression and reddened the same afternoon the
    # expression was extended (02.09); the greps are fixed-string, since a bracket in a pattern is a
    # character class.
    # Re-pointed 2026-09-03 (plan-14): until then this read the same two expressions out of BOTH
    # readers, because both carried their own copy of the state computation. The copies are gone —
    # `evaluate()` in scripts/plan_checks_core.py is the one home, and the status view a host installs
    # runs that same function — so the first two arms read the one home and the last two prove both
    # readers still go through it rather than growing a copy back. The end-to-end proof is
    # tests/test_plan_is_not_executable.py::TestADoneMarkCannotOutliveItsKey; a check the probe runs
    # at every session start stays cheap, so it reads the code instead of running that suite.
    "q-807": 'grep -qF \'["icon"] = "🔁"\' scripts/plan_checks_core.py && grep -qF \'failing_key"] and t["blocked_by"]\' scripts/plan_checks_core.py && grep -qF \'evaluate(\' scripts/state-probe.sh && grep -qF \'evaluate(\' scripts/render-board.sh',
    # plan-1's key was removed 2026-08-28 with its task: the board rotation folded plan-1 into
    # plan-11, and its check ("the render script exists and is executable") was the file-existence
    # proxy plan-10 names as a defect in its own text.
    # plan-11: the three arms of its own acceptance. The queue file is gone from the tree and
    # findable where it was put; every task on the list is drawn on the board, so the page and the
    # list cannot hold different sets of rows; and every open row carries its group and its
    # priority, the exceptions printed by id rather than counted.
    "plan-11": """test ! -e ROADMAP.md && test -f attic/ROADMAP.md && python3 -c "
import os, sys
sys.path.insert(0, 'scripts')
from plan_checks import parse_tasks
tasks = parse_tasks(open('PLAN.md', encoding='utf-8').read())
if not os.path.exists('board.html'):
    print('the board has not been drawn here yet: run bash scripts/render-board.sh')
    sys.exit(1)
board = open('board.html', encoding='utf-8').read()
undrawn = [t['id'] for t in tasks if t['id'] not in board]
unmarked = [t['id'] for t in tasks if t['mark'] != '✅' and not (t['group'] and t['priority'])]
if undrawn:
    print('not drawn on the board: ' + ', '.join(undrawn))
if unmarked:
    print('open with no group or no priority: ' + ', '.join(unmarked))
sys.exit(1 if undrawn or unmarked else 0)
" """,
    "plan-2": 'test ! -f evals/director.md && test "$(git log -1 --format=%ct -- evals/director/traces)" -ge "$(git log -1 --format=%ct -- skills/director/SKILL.md)" && python3 evals/director/check.py --all 2>/dev/null | tail -1 | grep -qv " 0 of "',
    # Step 6 tore machinery down and, more often, proved a piece of it earned its place. What it
    # leaves behind that a command can see: the plan carries no executable line and neither reader
    # looks for one, the checks have this one home, and the read-only report on wiring a decision
    # into the push gate runs clean.
    # Every command in this file runs on the probe, and the probe is the first thing a session
    # does — so each one stays cheap. No test suite here: the guard for the line below is
    # tests/test_plan_is_not_executable.py, and the suite's home is the push gate and CI.
    "plan-6": "! grep -q '^<!-- check:' PLAN.md && ! grep -q '<!-- check:' scripts/state-probe.sh scripts/render-board.sh && test -f tests/test_plan_is_not_executable.py && python3 scripts/director-wire-report.py >/dev/null 2>&1",
    # q-821: the joining installer writes the style block under a letter nothing else spends, in
    # the chain's own shape, and sweeps an old block instead of doubling it.
    # q-821: the installer writes the style block under its own letter, in the chain's own colon
    # shape, and the kit's own suite still holds the replace-rather-than-double half. The suite call
    # this line used to make ran a whole test file at every session start, which the probe's own
    # cheapness rule forbids (tests/test_plan_is_not_executable.py) — that file still runs in the
    # push suite, where it belongs, and this line reads the shipped installer instead.
    "q-821": "grep -q 'live-spec:gate-v' adopt/install-style-gates.sh && grep -q 'gate v: style gate' adopt/install-style-gates.sh && grep -q 'def test_' tests/test_style_gate_kit.py",
    "plan-8": """test "$(cat VERSION)" != 5.0.0 && grep -q 'skills/director' MIGRATION.md""",
    # plan-9's key left with its row on 2026-09-04. The row tracked another project's catch-up, so
    # its command read that project's tree and failed here every session while the row read as done;
    # the work belongs to that project's own window, and this file cannot prove work it cannot do.
    # --- written 2026-08-28 by plan-10 --------------------------------------------------------
    # Thirteen rows, out of thirty-seven. A key is worth its weight only where the row's subject is an
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
    # The positive arm is there on purpose: a bare "the numbers are absent" would go green on a
    # rulebook that had been deleted.
    "plan-7": "test -f attic/live-spec-base-unbacked-rules-2026-08-26.md && grep -q '^36\\. \\*\\*' skills/live-spec-base/SKILL.md && ! grep -qE '^(11|14|15|18|19|20|21|23|28|30|32|33|34|35)\\. \\*\\*' skills/live-spec-base/SKILL.md",
    # plan-17: the per-step reader exists and the project's own boot file sends a session there
    # rather than at the whole plan. The arm that grepped the plan for the literal token count
    # `17,575` came off 2026-08-28: the floor moves every time the pack grows a paragraph (17,676
    # by that evening), so the arm redded the moment somebody corrected the plan's number to the
    # measured one — a check that punishes the repair it is supposed to protect. The number itself
    # is a past measurement, and the plan says so in its own words ("a past measurement is not a
    # state a check can re-read"). No bound replaces it: any bound here would be a threshold
    # nobody measured, and the opening report already prints today's figure.
    # plan-16: its own acceptance, in one command. The first arm names one home per rule and reds on
    # a second copy of any of the three; the second arm reads the sentence that lets the director
    # name the home of a rule it has never seen.
    # It runs the check directly rather than through the suite: the probe runs every command in
    # this table at the start of every session, and a suite in here once hung the owner's morning
    # command (tests/test_plan_is_not_executable.py holds that law).
    "plan-16": ("python3 tests/test_one_home_per_rule.py > /dev/null"
                " && grep -q 'the one house whose declared sentence it extends'"
                " skills/director/SKILL.md"),
    # plan-17: tightened 2026-09-06. `test -x` decided only that the file is executable; the row
    # promises a session can open ONE row instead of the whole plan, so the script is run and
    # its output has to be that one row's heading and no other's.
    "plan-17": "test \"$(bash scripts/plan-step.sh plan-17 | grep -c '^### ')\" = 1 && bash scripts/plan-step.sh plan-17 | grep -q 'id: plan-17$' && grep -q 'plan-step.sh' CLAUDE.md",
    # plan-12: the row's four acceptance legs, one arm each, and a fifth that runs the gate itself
    # rather than reading only the source that carries it. The first read has its requirement and its
    # node. The roster names the first read, and the check that proves roster and coverage table agree
    # now also reds a name standing on a scenario the spec itself marks promised. The two parts-map
    # faults each carry their own red proof, since a fault with no red proof is a claim.
    # A sixth arm was added at the close on 31.08, for the row's own third bullet: the decision
    # sheet gains the line that names which open piece runs next. Both sides are read, the skill's
    # field and the spec's claim on it, because the field came out once already when only one side
    # could be written from a worktree.
    # Re-armed the same day, at the merge review. Three arms had read `def test_<name>` out of a
    # test file, which decides that a function is NAMED and nothing about what it asserts: the
    # INV-322 reader could be emptied to `return []`, leaving the gate blind to a stray part, and
    # this key still exited 0. The proofs run for real now, by direct execution rather than through
    # a suite, the way plan-16's key already does — 0.4s for both files together.
    # Re-pointed 2026-09-06: the "What runs next" field moved with the rest of execution out of
    # director (which now classifies and routes only) into the pipeline's execution reference.
    # The arm read the old owner and red on a move it should have followed.
    "plan-12": "grep -q 'What runs next' skills/build-pipeline/references/accepted-work-execution.md && grep -q 'which piece runs next where other accepted work stands open' spec/message-first-read.md && grep -q '^## Requirement 313' spec/message-first-read.md && grep -q '^### .node: director.$' architecture/pipeline-and-lanes.md && grep -q '^| F-first-read | director |' architecture/feature-coverage.md && PYTHONPATH=tests python3 -m unittest -q test_traceability.TestFeatureCoverage > /dev/null 2>&1 && python3 tests/test_spec_parts.py TestTheMapNamesEveryPart TestOneNumberNamesOneRequirement > /dev/null 2>&1 && python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md >/dev/null",
    # q-458: corrected 2026-09-01 — the old arm was three bare `test -f`/`test -d` clauses, the
    # exact file-existence proxy plan-10's own text names as a defect. Now reads the substance:
    # the external skill is installed with real content (not an empty directory), the pack's own
    # binding names the dependency, and the declared lint list carries exactly the six commands
    # the row's own text counts, including the two it names by name.
    "q-458": """test -f "$HOME/.claude/skills/text-audit/SKILL.md" && grep -q 'text-audit >= ' skills/text-audit-pack/SKILL.md && test "$(grep -c '"command"' .text-audit/lints.json)" = "6" && grep -q 'spec-style-lint.py' .text-audit/lints.json && grep -q 'preshow-register-lint.py' .text-audit/lints.json""",
    # q-531: the command stands and both directions run for real — a legitimate split prints an
    # empty difference, and each thing dropped on purpose prints and reds. The two fixture classes
    # are executed rather than grepped for (0.5s); the two real splits they sit beside read 800 KB
    # out of git history and stay in the suite.
    "q-531": "test -f scripts/nothing-lost.py && python3 tests/test_nothing_lost.py TestALegitimateSplitPrintsNothing TestADroppedThingReds > /dev/null 2>&1",
    # q-817: every skill under skills/ carries a record quoting the validator's own output, and
    # the gate itself now demands that quote. The coverage script reads the records rather than a
    # claim about them, and costs a fraction of a second.
    "q-817": "grep -q 'but it quotes no' guardrails/check-skill-review.sh && test -x guardrails/skill_review_verdict.py && python3 scripts/check-skill-review-coverage.py >/dev/null",
    # q-48, the pack side: the shared renderer prints a project's live numbers through the pack's
    # one checker, and the checker takes the refresh cadence from the feed rather than from a
    # number this tree chose. The host leg — writing the fetch tooling — is another window's job.
    "q-48": "grep -q 'SINCE IT SHIPPED' scaffold/status-view/state-probe.sh && grep -q 'from-feed' scripts/check-success-measure-feed.py && test -f tests/test_success_measure_view.py",
    # q-818: one renderer ships from the pack, the pack's own copy is byte-identical to it, and the
    # drift check reads the two files. cmp costs nothing; the check's own red-proof lives in
    # tests/test_status_view_drift.py rather than being re-run at every session start.
    "q-818": "cmp -s scaffold/status-view/state-probe.sh scripts/state-probe.sh && test -x guardrails/check-status-view-drift.py && grep -q 'state-probe-extras.sh' scaffold/status-view/state-probe.sh",
    # q-819: the plan says what a priority means and how its words rank, one reader carries that
    # statement, and the renderer derives the next move from it rather than from a row's position.
    "q-819": "grep -q '^- \\*\\*Priority\\*\\* —' PLAN.md && grep -q '^  1\\. `critical`' PLAN.md && grep -q 'def read_priority_order' scripts/plan_checks_core.py && grep -q 'PRIORITY_ORDER = core.read_priority_order' scaffold/status-view/state-probe.sh && grep -q 'next_reason' scaffold/status-view/state-probe.sh",
    # q-820: the four scenarios where a person corrects work already running pass in the recorded
    # run; the skill says in the numbers a verdict carries that replanning opens no row; and the
    # eval's README states that one run's score is never the result. The grader is deterministic
    # over a fixed trace set, so this costs a fraction of a second and reads the real verdicts.
    "q-820": "! python3 evals/director/check.py --all 2>/dev/null | grep -qE '^FAIL  (correction-|mixed-you-invented)' && grep -q 'the count of new pieces of work the turn' skills/director/SKILL.md && grep -q 'a scenario counts as failing when it fails on two separate recordings' evals/director/README.md",
    # q-537: both halves. The installed-vs-working comparison runs clean, the hook installer refuses
    # a registration already present, and the test that proves it is still there.
    "q-537": "bash guardrails/check-config-health.sh >/dev/null 2>&1 && grep -q 'already wired' scripts/install-session-hooks.sh && grep -q 'test_a_meter_wrapped_existing_entry_is_recognized_not_duplicated' tests/test_install_session_hooks.py",
    # q-588: the rule-price page still stands and the pin-drift gate still reaches it. Running the
    # gate itself would cost a session 37 seconds at every start.
    "q-588": "test -f .live-spec/r5-rule-prices-2026-08-11.md && grep -q 'r5-rule-prices-2026-08-11.md' guardrails/check-pin-drift.sh",
    # q-590: the rulebook's own head names the retired numbers, so a host reading it sees the holes.
    "q-590": "grep -q 'Rule 30 went first' skills/live-spec-base/SKILL.md",
    # q-592: the assertion is pinned to the bullet's own sentence, not to the bare invariant code.
    # q-592: tightened 2026-09-06. The arm grepped the assertion's own literal out of the test
    # FILE, which decides only that the line is typed there — the test could red and this key
    # still exited 0, the exact vacuous-anchor defect this row was opened to remove. It runs
    # the strengthened test now (0.1s), so the assertion has to pass, not merely exist.
    "q-592": "PYTHONPATH=tests python3 -m unittest -q test_compaction_discipline.TestCompactionIsContinuous.test_landing_law_carries_compaction_every_pass >/dev/null 2>&1",
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
    # --- written 2026-09-01 by plan-10's second pass: fourteen rows the first pass left declared
    # but neither backed by a command nor read and dated. Each command below reads the row's own
    # acceptance, not merely a path's presence.
    #
    # q-801: the retired template stays retired (not merely present somewhere), the file it was
    # replaced with exists, the manifest names the move, three of the eleven repointed files carry
    # the converged sentence, and the migration chapter both exists and names the queue question
    # it answers.
    "q-801": ('test -f attic/ROADMAP.template.md && test ! -f templates/ROADMAP.template.md'
              ' && test -f templates/PLAN.template.md && grep -q "ROADMAP.template.md" attic/MANIFEST.md'
              ' && grep -q "the plan and the queue in one document" skills/design-reviewer/SKILL.md'
              ' && grep -q "the plan and the queue in one document" skills/communicator/references/words.md'
              ' && grep -q "the plan and the queue in one document" skills/product-prover-pack/SKILL.md'
              ' && grep -q "^### 6.1.0" MIGRATION.md'
              ' && grep -q "queue file as the place a wish lands" MIGRATION.md'),
    # q-802: the fixture suite proving the snapshot's advance-on-delivery asymmetry runs clean,
    # Requirement 1's criterion 4 no longer names E-7 (only the still-planned design-sync machine,
    # E-18), and the snapshot machinery itself — the manifest and the one function that writes it
    # — is really on disk. Corrected 2026-09-01: the original arm ran `python3 -m pytest`, the
    # exact shape tests/test_plan_is_not_executable.py forbids in this table (the probe runs every
    # key here at every session start, and a suite once hung the owner's morning command). The
    # module carries its own `__main__`, so it runs directly instead, the way q-55/q-489/q-235 and
    # the rows below already do.
    "q-802": ('python3 tests/test_snapshot_baseline.py >/dev/null 2>&1'
              ' && grep -qF "The system *shall* mark as planned the design-sync machine. [E-18]" spec/doc-order-generated.md'
              ' && test -f .live-spec/snapshot/MANIFEST.md && test -f .live-spec/snapshot/baseline.py'),
    # q-490: the dedicated suite for the chainless-selector fix runs clean (22 tests, incl. the
    # named regression case), and the neighbouring register lint states out loud when its own
    # judge stands down rather than printing a clean pass over a check that never ran.
    "q-490": """PYTHONPATH=tests python3 -c "
import test_legibility_floor as m
[f() for n, f in vars(m).items() if n.startswith('test_') and callable(f)]
" >/dev/null 2>&1 && grep -q 'judge stood down' scripts/preshow-register-lint.py""",
    # q-497: the gate itself runs clean on the tree as it stands, the test proving both directions
    # in one holds, the rule the row wrote (instruction authority) stands in its one home, and the
    # one-home-per-rule suite that would catch a second copy passes.
    "q-497": ("""python3 guardrails/check-authority-anchor.py >/dev/null 2>&1 && PYTHONPATH=tests python3 -c "
import tempfile, pathlib
import test_authority_anchor as m
d = tempfile.TemporaryDirectory()
m.test_a_named_attribution_reds_on_any_surface_and_the_tree_as_it_stands_passes(pathlib.Path(d.name))
d.cleanup()
" >/dev/null 2>&1 && grep -q 'A claim needs its primary source' skills/live-spec-base/SKILL.md && python3 tests/test_one_home_per_rule.py >/dev/null 2>&1"""),
    # q-527: the definition of "made good" the row asked be written once stands in the requirement
    # it cites, and the test proving both directions over one fixture repository — red without the
    # repair, clean with it, nothing else changed between the two readings — passes. Run directly
    # (not through pytest) since the probe runs every key in this table on every session start, and
    # a suite in here once hung the owner's morning command (see the module's own docstring).
    "q-527": """grep -q '^21\\. A finding \\*shall\\* count as made good' spec/guardrails-freshness.md && PYTHONPATH=tests python3 -c "
import tempfile, pathlib
import test_worker_restore_made_good as m
d = tempfile.TemporaryDirectory()
m.test_the_repair_clears_the_finding_and_its_absence_keeps_it_red(pathlib.Path(d.name))
d.cleanup()
" >/dev/null 2>&1""",
    # q-55: the joining script is executable and named as step two of the attach walk's own text,
    # and its four-way suite (committed as found, a later change diffs against that commit, all
    # three fail when the step is skipped, a project with its own history gains no commit) passes,
    # run directly rather than through pytest (the module already carries its own `__main__`).
    "q-55": "python3 tests/test_starting_state.py >/dev/null 2>&1 && test -x adopt/record-starting-state.sh && grep -q '2\\. \\*\\*Keep the files as they were found' adopt/ADOPT.md",
    # q-567: the install script ships the check scripts a host's hooks call (not the hooks alone),
    # proven by the two tests that plant a scratch repo and watch a missing check stop the commit
    # rather than passing silently, run through `unittest` rather than pytest, and the README
    # states by hand how a host takes the one chain that cannot travel whole.
    "q-567": "PYTHONPATH=tests python3 -m unittest -q test_guardrails.TestInstalledHooksReachTheirChecks >/dev/null 2>&1 && grep -q 'adapted by hand' guardrails/README.md",
    # q-581: the guard's own test functions, called directly against the module's own command list
    # (every listed command warns, an ordinary command passes clean, malformed input stands down),
    # and the flat list the row's narrowed acceptance asked for is the mechanism actually wired.
    "q-581": """PYTHONPATH=tests python3 -c "
import test_dialog_warning_guard as m
for name, command in m.KNOWN_EXAMPLES:
    m.test_each_listed_command_is_warned_before_it_runs(name, command)
for command in m.ORDINARY:
    m.test_ordinary_commands_pass_silently(command)
m.test_malformed_input_stands_down_rather_than_guessing()
" >/dev/null 2>&1 && grep -q 'KNOWN_DIALOG_COMMANDS' hooks/dialog-warning-guard.py""",
    # q-586: the class of the fix — judging where the bytes end up rather than which word came
    # first — is proven by calling the test class's own methods directly against every named and
    # every assembled discarding form and watching all of them red, and the refusal's own
    # recommended route no longer points at the command that used to slip past it.
    "q-586": """PYTHONPATH=tests python3 -c "
import tempfile, pathlib
import test_worker_restore as m
inst = m.TestGateRedsOnADiscardingCommand()
d = tempfile.TemporaryDirectory(); inst.test_the_lived_case_reds_and_names_its_path(pathlib.Path(d.name)); d.cleanup()
for which, command in sorted(m.DISCARDING.items()):
    d = tempfile.TemporaryDirectory(); inst.test_each_named_command_reds(pathlib.Path(d.name), which, command); d.cleanup()
for command in m.ALSO_DISCARDING:
    d = tempfile.TemporaryDirectory(); inst.test_the_other_forms_the_prose_names_red_too(pathlib.Path(d.name), command); d.cleanup()
" >/dev/null 2>&1 && grep -q 'write the file deliberately' hooks/worker-restore-guard.py""",
    # q-489: the one check the row's acceptance asked be proven end to end, plus the walk over
    # every check in guardrails/ and its forward-looking arm (a check arriving with no fixture
    # reds the walk), all five fixture-proof tests, run directly (the module carries its own
    # `__main__`) rather than through pytest.
    "q-489": "python3 tests/test_guardrail_fixture_proofs.py >/dev/null 2>&1",
    # q-597: the commit the row cites for the removal is real, and none of the mirror-sync
    # machinery (the script itself, the three tests that guarded it) is in the tree to guard.
    "q-597": "git cat-file -e 7b2980df 2>/dev/null && test ! -f scripts/sync-mirrors.sh && test ! -f tests/test_mirror_editions.py && test ! -f tests/test_mirror_autosync.py && test ! -f tests/test_mirror_release_history.py",
    # q-625: the commit the row cites for the removal is real, and neither the generated rulebook
    # nor the check that read it is in the tree to guard.
    "q-625": "git cat-file -e e61b29b7 2>/dev/null && test ! -f guardrails/hook-red-proofs.json && test ! -f guardrails/check-hooks-can-fire.py",
    # q-427: the settings ladder's package-defaults table carries exactly the eighteen rows the
    # row's own closing text counts — a script reads the table between its own header and its own
    # end, not a grep for the word "setting".
    "q-427": "test -f skills/live-spec-base/references/settings-ladder.md && "
             "test \"$(grep -c '^| `' skills/live-spec-base/references/settings-ladder.md)\" = \"18\"",
    # q-529: the two pieces of machinery the row names (the generated rulebook and the gate that
    # read it, already retired for q-625 above) stay out of the tree, and the matrix page records
    # the old mechanism as retired rather than silently dropped. The clause that used to sit here
    # too — the spec size ratchet stating it never writes its own config — went with that gate on
    # 2026-09-02 (q-805): no ceiling seeded from a document's own past state is left to check.
    "q-529": 'test ! -f scripts/rule-census.py && test ! -f guardrails/check-doc-findings-bound.py && test ! -f guardrails/rule-census.json && test ! -f guardrails/check-size-ratchet.py && grep -q "M-479.*retired" matrix/guardrails.md',
    # q-235: the command's own six-test suite (each of the four acceptance legs red if skipped,
    # the red-gate path withholds the push instead of bypassing it, the command's own controlling
    # process is never signalled) runs clean.
    "q-235": "python3 tests/test_wind_down.py >/dev/null 2>&1",
    # q-805: the row's own acceptance, read as four facts rather than four absent files. (1) No gate
    # in the tree compares a document against a bound seeded from its own past state: the size
    # ratchet's three files are gone, the empty numbers they left are pinned with their reason, and
    # scripts/spec-debt-cap.json carries no per-document redundancy ceiling. (2) The near-duplicate
    # reading survives as a reading — the script still runs and still prints its JSON summary over
    # the live spec. (3) The host kit vendors the style lint under a name that seeds nothing, and
    # nothing in it writes a lock test. (4) The prose shaved to satisfy the retired ratchet is back,
    # byte for byte, against the commit before the shave.
    "q-805": (
        'test ! -f guardrails/check-size-ratchet.py && test ! -f guardrails/spec-ratchet.json && '
        'grep -q "264, 265" tests/test_formal_index.py && '
        'python3 -c "import json,sys; sys.exit(0 if \'max_redundancy_open\' not in '
        'json.load(open(\'scripts/spec-debt-cap.json\')) else 1)" && '
        '{ python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md || true; } | grep -q \'"open"\' && '
        'test ! -f adopt/install-ratchet.sh && '
        '! grep -q LOCK_TEST_TEMPLATE adopt/install-style-gates.sh && '
        # The criteria the retired size ratchet forced short still carry their restored, longer
        # wording. This clause used to compare the whole file against 49b4813f^, which read as a
        # freeze on a live spec chapter: q-48 added three real criteria to it on 2026-09-04 and the
        # row went red over an addition it has no quarrel with. What the row actually promises is
        # that the shortening was undone and stayed undone, so the clause reads the restored
        # sentences themselves.
        'grep -q "carrying a label, a value, and a unit" spec/success-measure-feed.md && '
        'grep -q "each variant its own label and its own non-empty metrics list" spec/success-measure-feed.md'
    ),
    # --- written 2026-09-01, closing the second round of gaps test_plan_done_marks_are_backed.py
    # found: five more rows landed ✅ tonight with no command and no named reading. Each below
    # reads the row's own stated acceptance, run directly rather than through pytest (the modules
    # carry their own `__main__`), matching the rest of this table.
    #
    # plan-10: its own acceptance, run against itself — the same test this table's whole second
    # pass exists to satisfy.
    "plan-10": "python3 tests/test_plan_done_marks_are_backed.py >/dev/null 2>&1",
    # q-437: the duty's two homes carry their text, and the sibling-axis-verdict case (the row's
    # own definition of done) runs clean.
    "q-437": "grep -q 'INV-244' skills/spec-author/references/facet-sweep.md && grep -q 'blank-answer' skills/product-prover-pack/SKILL.md && PYTHONPATH=tests python3 -m unittest -q test_composition_axes.TestAxisVerdictSweep >/dev/null 2>&1",
    # q-436: the sibling half of q-437's promise. The duty's two homes carry their text, the spec
    # names the built step and drops its old "promised as a later increment" line, and the row's
    # own definition-of-done case (a poles-answered axis with no named co-occurrence value reds)
    # runs clean.
    "q-436": "grep -q 'value-space in-between forcing step:' spec/design-spec-review.md && ! grep -q 'promised as a later increment' spec/design-spec-review.md && grep -q 'co-occurrence value lens' skills/product-prover-pack/SKILL.md && grep -q 'Naming the value in between two poles' skills/spec-author/references/facet-sweep.md && PYTHONPATH=tests python3 -m unittest -q test_composition_axes.TestCooccurrenceValueForcingStep >/dev/null 2>&1",
    # q-591: the matrix reference checker runs clean over the corrected row, and the renamed test
    # it now cites runs clean too.
    "q-591": "python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md >/dev/null 2>&1 && python3 tests/test_compaction_discipline.py >/dev/null 2>&1",
    # q-398: the vendored hook is in the tree, executable, and its fixture suite (the red-proof on
    # a foreign-zone prompt, the installer wiring, the adoption gate) runs clean.
    "q-398": "test -x hooks/routing-preamble-hook.sh && python3 tests/test_routing_preamble_hook.py >/dev/null 2>&1",
    # q-386: the law's own bullet and the script's live run converge, proven to actually catch
    # drift (the row's closing paragraph), not merely pass today.
    "q-386": "python3 tests/test_lane_open_act_convergence.py >/dev/null 2>&1 && grep -q 'The lane-open act' skills/live-spec-base/SKILL.md",
    # q-803: the row's own acceptance grep, run for real rather than by eye — every "his word" /
    # "owner's word" hit left in skill rule prose pairs with no date, which is what makes it the
    # behavioural-actor sense and not a citation (test_no_inline_provenance_citation.py). The one
    # exemption (rule-histories.md, the document already built to hold this skill's dated origin
    # notes) still declares its own purpose, so the exemption stays warranted.
    "q-803": "python3 tests/test_no_inline_provenance_citation.py >/dev/null 2>&1",
    # ------------------------------------------------------------------ 2026-09-06 sweep
    # Every ✅ row was re-run against its own acceptance this night. The rows below were closed on
    # a named reading, which this plan's own law allows only where the result is prose, a
    # measurement or a decision — each of these left behind a file, a script or a test that CAN
    # drift back, so each now writes the command it owed. The rows left on their reading are the
    # honest cases: q-205 and q-584 name plan-17 as what covers them (a second key would be two
    # homes for one fact), q-612's subject is a frozen one-off review record nothing regenerates,
    # and the rest close on a judgement or a person's read no command can stand in for.
    #
    # q-163: the pack-side half of the promise — director still names the derivation specialist,
    # the matrix still carries its row, and the traceability test that ties the two runs for real.
    # The field-project half of the row's acceptance names another project's tree and stays out.
    "q-163": "grep -q 'skills/test-author' skills/director/SKILL.md && grep -q 'M-620' matrix/test-author.md && PYTHONPATH=tests python3 -m unittest -q test_traceability.TestProblemLedger.test_director_names_test_author_at_the_derivation_step >/dev/null 2>&1",
    # q-611: both halves of the row — the review's public page still names the class duty, and a
    # record carrying a point finding with no class line is still refused.
    "q-611": "PYTHONPATH=tests python3 -m unittest -q test_class_hunt.TestClassHunt.test_readme_names_the_class_lens test_class_hunt.TestClassLineFixtures.test_a_point_finding_with_no_class_line_reds >/dev/null 2>&1",
    # q-608: the row IS the agreement between two texts, so both sides are read — the filename
    # shape the skill tells a reviewer to write, and the shape the gate actually enforces.
    # Re-aimed 2026-09-06: the second arm greped `<slug>.md`, which occurs in that gate only
    # inside its `echo "Fix: ..."` repair lines — deleting the enforcement outright and leaving
    # the advice behind passed it. The date shape below is the gate's own selector
    # (guardrails/check-prover-record.sh:156) and occurs once in the file.
    "q-608": "grep -q 'YYYY-MM-DD-<slug>.md' skills/product-prover-pack/SKILL.md && grep -qF '/[0-9]{4}-[0-9]{2}-[0-9]{2}.*\\.md$' guardrails/check-prover-record.sh",
    # q-536: the fourteen rulings the row settled live in the histories reference (moved there
    # 04.09 off SKILL.md). Counted rather than pinned to one wording, so re-phrasing a ruling is
    # not a red while losing one is.
    "q-536": "test \"$(grep -c 'q-536 ruling' skills/communicator/references/rule-histories.md)\" -ge 14",
    # q-815: the row's own definition of done, red-then-green — a discard recorded against the
    # repository the gate's file lives in no longer blocks a different pushing host, and the same
    # discard in the host's own history still does. Called directly rather than through pytest
    # (the house style above), which is what makes it 0.3s and affordable at every session start.
    "q-815": """PYTHONPATH=tests python3 -c "
import tempfile, pathlib
import test_worker_restore as m
inst = m.TestOwnRepoFollowsThePushingHostNotWhereTheFileLives()
for name in ('test_a_discard_where_the_scripts_own_file_lives_no_longer_blocks_a_different_pushing_host',
             'test_the_same_discard_in_the_pushing_hosts_own_history_still_blocks'):
    d = tempfile.TemporaryDirectory(); getattr(inst, name)(pathlib.Path(d.name)); d.cleanup()
" >/dev/null 2>&1""",
    # q-804: the row's own 2026-09-02 correction demanded the REAL caller be proven, after two of
    # three scripts turned out to be built and never invoked. These three arms are exactly that:
    # the landing walk calls the merge-base check, config-health reds a stale lane with no row,
    # and the adoption walk reds a host with no vendored worktree line.
    "q-804": "PYTHONPATH=tests python3 -m unittest -q test_lane_net_arms.TestTheLandingWalkRunsTheMergeBaseCheck.test_the_walk_reds_a_lane_that_never_rebased_and_leaves_main_where_it_was test_lane_net_arms.TestStaleLaneArm.test_a_lane_branch_with_no_row_at_all_reds test_scaffold_install.TestAdoptionGateWorktreeLine.test_the_adoption_walk_reds_a_host_with_no_worktree_line >/dev/null 2>&1",
    # q-501: the row's acceptance is a first-time reader's read, which no command replaces. What a
    # command CAN hold is the two false claims the close names by name (the discovery-pattern
    # claim, the project count) and the two lints the close ran — so the page cannot silently
    # regrow what the rewrite removed.
    "q-501": """PYTHONPATH=tests python3 -m unittest -q test_readme_stance.TestReadmeKnownIssuesNoFalseDiscoveryPatternClaim >/dev/null 2>&1 && PYTHONPATH=tests python3 -c "
import test_host_count_agrees as m
m.test_the_front_page_states_no_project_count()
" >/dev/null 2>&1 && python3 scripts/preshow-register-lint.py README.md >/dev/null 2>&1 && python3 guardrails/check-one-name.py README.md >/dev/null 2>&1""",
    # q-810: the closing rule is proven where it actually runs — director's own recorded closing
    # scenarios, rather than by reading the sentence that states it.
    "q-810": """PYTHONPATH=tests python3 -c "
import json
import test_director_scenarios as m
c = json.load(open(m.CLOSING, encoding='utf-8'))
m.test_the_closing_suite_tests_both_outcomes(c)
m.test_every_closing_verdict_matches_its_scenario(c)
m.test_the_closing_grader_fails_a_wrong_verdict(c)
" >/dev/null 2>&1""",
    # q-806: the contract and both independent reviews of it are in the tree, the contract still
    # carries the two-proof section the row turned on, and the checkpoints are TRACKED — the
    # .gitignore fault this row's own review caught cannot come back silently.
    "q-806": "test -f .live-spec/turnkey-contract-composed.md && test -f docs/prover/2026-09-02-turnkey-contract-review.md && test -f docs/prover/2026-09-02-turnkey-contract-review-fable.md && grep -q '^## 7. Two proofs for the Director' .live-spec/turnkey-contract-composed.md && git ls-files .live-spec/checkpoints/ | grep -q .",
    # q-814: the carve-out red-then-green, both halves — a byte-identical vendor sync asks for no
    # new record, and a hand edit to never-reviewed content still reds with the carve-out present.
    "q-814": """PYTHONPATH=tests python3 -c "
import test_skill_review as m
m.test_vendor_sync_of_previously_reviewed_content_needs_no_new_record()
m.test_hand_edit_to_never_reviewed_content_still_reds_with_carveout_present()
" >/dev/null 2>&1""",
    # q-570: the measuring line the row left behind is still wired and still measures. The extras
    # script is READ, not run: running it reaches into the person's home for the real figure, which
    # would red on a fresh clone for a reason about the machine rather than the project.
    "q-570": "grep -q 'state-probe-extras.sh' scripts/state-probe.sh && grep -q 'required context (boot + profile + base + director)' scripts/state-probe-extras.sh && grep -q 'CTX_TOK=' scripts/state-probe-extras.sh",
    # q-576: the two numbers the sweep could not source carry their own admission at the number,
    # which is what the row landed instead of deleting working defaults, and the sweep's report
    # stays in the tree.
    "q-576": "grep -q 'No incident or source behind either figure below; engineering defaults, not policy decisions.' scripts/wind-down.py && grep -q 'No source behind the exact 3 (2026-08-07 census, row 15)' guardrails/check-vocabulary.py && test -f docs/prover/2026-09-01-every-number-in-the-tree.md",
    # plan-4: the glossary's convergence entry for the name this row settled, both halves — the one
    # name kept, and the source's other names recorded as its aliases rather than dropped.
    "plan-4": "grep -q 'The glossary keeps the one name' skills/live-spec-base/references/glossary.md && grep -q \"records the senior and the orchestrator as the source's other names for it\" skills/live-spec-base/references/glossary.md",
    # plan-5: the pack-side half only. The reviewer body itself is an external canonical clone
    # (skills/product-prover/ holds its own .git and no file of it is tracked here), so a check
    # reading it would red on a fresh clone for a reason about the machine. What this tree owns is
    # the binding: the code request routes to Code mode and points at the prover's code lenses.
    "plan-5": "grep -q '^## Code mode' skills/product-prover-pack/SKILL.md && grep -q '| `CODE-REVIEW` | Code mode' skills/product-prover-pack/SKILL.md && grep -q 'reference/code-lenses.md' skills/product-prover-pack/SKILL.md",
    # plan-14: what the row actually left installable — both adoption walks call the status-view
    # installer, and the probe reads its host roster from a profile line instead of the hard-coded
    # five-host list the row removed, so no host name can creep back in. The scratch-host suite
    # (tests/test_status_view_install.py) proves the same thing and costs 8s, too much to run at
    # every session start for one row; it runs in the suite.
    "plan-14": "grep -q 'install-status-view.sh' adopt/ADOPT.md && grep -q 'install-status-view.sh' MIGRATION.md && grep -q 'hosts.watch:' scripts/state-probe.sh && ! grep -qE 'tlvphotos|track-coach' scripts/state-probe.sh",
    # q-166: the board's own columns are still defined and a real render still stands every row
    # in exactly one of them. The generator is run against a THROWAWAY tree, never this one — it
    # recomputes every command in this table, so a key that rendered the real board would run the
    # whole table inside one of its own entries.
    #
    # Re-aimed twice. 2026-09-06 (morning): the four-column pseudo-kanban this key was written
    # against became the work board's own awaiting-validation / ready / in-work / done, and the key
    # was pinned to the old tuples' literal text. 2026-09-06 (night): the two arms that greped
    # `board.html` were unconditional template text in a file `.gitignore` keeps out of the tree —
    # red on a fresh clone for a reason about the machine, and green on a page that had dropped
    # every row into one column. It calls the real test of that promise now, directly rather than
    # through pytest (0.5s, the house style above).
    "q-166": """grep -q '("inwork", "In work"' scripts/render-board.sh && grep -q '("done", "Done"' scripts/render-board.sh && PYTHONPATH=tests python3 -c "
import json, pathlib, tempfile
import test_work_board as m
d = tempfile.TemporaryDirectory()
tree = m._build_tree(pathlib.Path(d.name))
assert m._run(tree).returncode == 0
m.test_m523_every_row_stands_in_exactly_one_column(
    {'tree': tree, 'page': pathlib.Path(tree, 'board.html').read_text(encoding='utf-8'),
     'model': json.loads(m._run(tree, '--json').stdout)})
d.cleanup()
" >/dev/null 2>&1""",
    # q-816: Requirement 309 whole, minus only the retired auto-refresh heartbeat. The rendering
    # half — a card per task in columns, the lanes, the given-vs-actual time, the per-agent craft,
    # the one registered link — is proven by rendering a THROWAWAY tree and calling the matrix's
    # own tests on the page that comes out, plus the registry row read off `SURFACES.md`. The
    # statement half (criteria 41-62, matrix rows M-531 to M-535) is proven the same way: the five
    # owning tests are called directly, each in its own throwaway tree, never through pytest. The
    # last arm reads this row's OWN statement and validation record, because the gate is only real
    # when the row that built it went through it.
    #
    # Re-aimed 2026-09-06 (night). Until then four arms greped `board.html`, which `.gitignore`
    # keeps out of the tree: on a fresh clone the row read red for a reason about the machine, and
    # the strings it looked for (`col inwork`, `lanes busy`, `Waiting on you`) are written by the
    # template on every render, so they stood whether or not a single row had landed in the right
    # column. The direct calls below fail when the promise fails.
    #
    # The last arm is criterion 8, the one stable published link the row's own acceptance names.
    # It is unbuilt: `spec/work-board.md` still carries its own-line `[target]` marker under
    # Requirement 309 and under criterion 8, and by this project's own S-0 convention a
    # landed promise drops its marker in the same commit. So this key reds while the link is
    # unbuilt, which is what a blocked row's command must do — a passing command on a ⛔ row
    # draws it back as done (`scripts/plan_checks_core.py`'s `evaluate`).
    #
    # NOTHING HERE MAY DEPEND ON q-816's OWN MARK, and nothing here renders THIS tree. The board
    # runs this key while drawing itself, so a marker that only appears when q-816 is open (an open
    # card's chip, say) would make the row oscillate: the key passes, the row draws as done, the
    # marker disappears, the key fails, the row draws as open again. The fixture tree carries its
    # own plan and its own empty check map, so nothing below reads a real row's state.
    "q-816": """PYTHONPATH=tests python3 -c "
import json, pathlib, tempfile
import test_work_board as m
d = tempfile.TemporaryDirectory()
tree = m._build_tree(pathlib.Path(d.name))
assert m._run(tree).returncode == 0
b = {'tree': tree, 'page': pathlib.Path(tree, 'board.html').read_text(encoding='utf-8'),
     'model': json.loads(m._run(tree, '--json').stdout)}
m.test_m519_one_surface_one_source_file_one_stable_link(b)
m.test_m525_lanes_match_the_cap_free_lanes_read_free_parked_row_kept(b)
m.test_m526_card_reads_as_a_task_at_a_glance(b)
m.test_m530_the_craft_set_has_one_home_and_no_skill_name_reaches_a_card(b)
m.test_m536_the_row_carries_the_time_it_was_given_beside_the_time_it_took(b)
d.cleanup()
" >/dev/null 2>&1 && PYTHONPATH=tests python3 -c "
import pathlib, tempfile
import test_statement_validation as v
for name in ('test_m531_a_statement_holds_its_four_fields_in_the_rows_own_entry',
             'test_m532_no_task_enters_work_before_its_statement_passes_validation',
             'test_m533_a_passed_validation_writes_the_dated_ready_state',
             'test_m534_the_wording_freezes_at_take_up_and_a_later_change_is_refused',
             'test_m535_the_plans_expected_parallel_steps_meet_the_lane_decision_at_take_up'):
    d = tempfile.TemporaryDirectory()
    getattr(v, name)(pathlib.Path(d.name))
    d.cleanup()
" >/dev/null 2>&1 && PYTHONPATH=scripts python3 -c "
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location('ta', 'scripts/task-admission.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
plan = pathlib.Path('PLAN.md').read_text(encoding='utf-8')
start, end, _, _ = m._row_span(plan, 'q-816')
row = plan[start:end]
assert m.read_statement(row), 'q-816 carries no statement'
assert (m.read_validation(row) or {}).get('status') == 'ready', 'q-816 has no passed validation'
" >/dev/null 2>&1 && grep -q 'def time_pair' scripts/render-board.sh && grep -q 'CRAFTS = (' scripts/render-board.sh && grep -q '| work-board |' SURFACES.md && grep 'M-519' matrix/work-board.md | grep -q '[*]built[*]' && test \"$(grep -c '^ *\\[target\\]$' spec/work-board.md)\" -eq 0""",
    # q-813: all four things the row landed — director's own idea-act outcomes, the restored
    # Requirement 309, the retired idea-shelf requirement staying retired, and no second list.
    "q-813": "grep -q 'a passing thought is answered and not recorded' skills/director/SKILL.md && grep -q '^## Requirement 309' spec/work-board.md && test -f attic/spec-message-first-read-R315.md && ! grep -q '^## Requirement 315' spec/message-first-read.md && test ! -f IDEA_SHELF.md",
    # q-812: the route proven on the mechanism, not the instructions — a done mark reads reopened
    # until its own check passes. One node of the end-to-end file rather than all eleven: the rest
    # build disposable hosts and cost 8s, which no session start should pay for one row.
    "q-812": "PYTHONPATH=tests python3 -m unittest -q test_director_route_end_to_end.TestADoneMarkWaitsOnItsCheck.test_a_done_mark_reads_reopened_until_the_check_passes_and_then_reads_done >/dev/null 2>&1 && grep -q 'M-630' matrix/build-pipeline.md && test -f docs/prover/2026-09-03-q812-director-route-contract.md",
    # q-822: the row's own Done-when, one clause per arm, all of them cheap enough for the probe
    # to run at every session start. The full proofs are four suite files this key deliberately
    # does NOT run — `tests/test_front_door_boundaries.py`, `tests/test_next_steps_boundary.py`,
    # `tests/test_task_admission.py` and `tests/test_director_scenarios.py`, 31 tests in 1.2s,
    # which is 1.2s more than a morning command should pay and which the neighbouring test
    # `test_every_check_is_cheap_enough_for_the_probe` forbids outright. What stays here is the
    # smallest thing that reds if any arm is undone:
    #   - the Director holds a route contract and no execution procedure (no `## Execution`
    #     heading, no mention of the checkpoint script it must never run);
    #   - a question, musing or conversation loads no pipeline;
    #   - the pipeline's execution reference is where the checkpoint lives instead;
    #   - `NEXT_STEPS.md` carries no task id, so it cannot be a second board;
    #   - the two required-context files this tree owns are lighter than at the row's opening
    #     (34,057 + 33,294 = 67,351 then; 34,057 + 21,977 now). The boot file and the person's
    #     profile make up the rest of the figure the probe prints and live outside git, so a key
    #     reading them would red on a fresh clone for a reason about the machine;
    #   - the cut holds under this project's own definition of a defect: two independent
    #     recordings against the cut skill share no red. A score floor stood here until
    #     2026-09-06 and was the wrong instrument — a number that moves with producer
    #     variance said nothing about the cut, while this directory's own rule is that a
    #     red on one recording and green on the next is a draw. The pair clause reads the
    #     behavioural form instead: whatever either run got wrong, the two agree on none of it.
    "q-822": "grep -q '^## Route contract' skills/director/SKILL.md && ! grep -q 'scripts/checkpoint.py' skills/director/SKILL.md && ! grep -q '^## Execution' skills/director/SKILL.md && grep -q 'answered without loading a pipeline' skills/director/SKILL.md && grep -q 'scripts/checkpoint.py' skills/build-pipeline/references/accepted-work-execution.md && ! grep -qE '(q|plan)-[0-9]+' NEXT_STEPS.md && test \"$(cat skills/live-spec-base/SKILL.md skills/director/SKILL.md | wc -c | tr -d ' ')\" -lt 67351 && python3 evals/director/check.py --pair evals/director/traces evals/director/recordings/2026-09-06-pair-6 2>/dev/null | grep -q '^shared reds: 0'",
    # q-823: one instruction travels the whole path. The row's own Verification runs five suite
    # files in 23s, which no session start may pay and which the probe's own cheapness rule
    # forbids outright, so this key runs the smallest thing that reds if any arm is undone:
    #   - the eight section-7B facts still trace, each from a matrix row reading built to a test
    #     that is really defined under tests/ (one unittest node, 0.2s — the row's heaviest
    #     clause and the only one a grep cannot decide);
    #   - the eight transitions past admission are really in the one file that writes ticket
    #     state, and the checkpoint's reopen half beside them;
    #   - admission refuses a ticket that carries no context pointers;
    #   - all 36 fixtures name an operation, all 36 recorded traces really carry the field,
    #     and the row's own pair of independent recordings shares no red — the form this
    #     project calls a defect. A score floor stood in this arm until 2026-09-06 and was
    #     removed: a number that moves with producer variance says nothing about whether the
    #     Director is right, and the row had already closed once on a grader arm that read
    #     the grader's own conditional line rather than a result. The closed vocabulary is
    #     held by `test_every_scenario_names_its_operation` in the suite: reading it here
    #     would need an inline program, which the probe's own honesty rule refuses.
    "q-823": "PYTHONPATH=tests python3 -m unittest -q test_traceability.TestStateMachineFactsAreTraced >/dev/null 2>&1 && test \"$(grep -cE '^def (correct|block|unblock|park|close|reopen|abandon|worker_brief)' scripts/task-admission.py)\" = 8 && grep -q 'def reopen_checkpoint' scripts/checkpoint.py && grep -q 'a ticket carries at least one context pointer' scripts/task-admission.py && test \"$(grep -c '\"operation\": \\[' evals/director/scenarios.json)\" = 36 && test \"$(grep -l '\"operation\"' evals/director/traces/*.json | wc -l | tr -d ' ')\" -eq 36 && python3 evals/director/check.py --pair evals/director/traces evals/director/recordings/2026-09-06-pair-6 2>/dev/null | grep -q '^shared reds: 0'",
    # q-609: the rule now names who enforces it, in the spec that carries it.
    "q-609": "grep -q 'shall\* place its enforcement with the author who writes the law' spec/design-spec-review.md",
}


def parse_tasks(text):
    """PLAN.md's rows, with THIS project's own acceptance command attached to each.

    The parsing itself is `plan_checks_core.parse_tasks`, which any project's copy of the status
    view runs; this wrapper is the one place this project's `CHECKS` meets it. `CHECKS` is read at
    call time rather than bound here, so a caller that edits the map (the fixtures in
    `tests/test_plan_is_not_executable.py` do) is honoured.
    """
    return _parse_tasks(text, CHECKS)
