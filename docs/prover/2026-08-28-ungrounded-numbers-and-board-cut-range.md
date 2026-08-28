# Prover record — 2026-08-28 the ungrounded-numbers sweep and the board cut

PUSH-REVIEW

Range: e7fafcf..d8485f2 (16 commits). Base commit `e7fafcf`. Reviewed commits, in order:
`7f40238`, `6b2aad4`, `9602993`, `8ed2771`, `9582aea`, `2f873ab`, `c85fff7`, `30a7a8e`,
`7c60809`, `7cd90c1`, `20d0630`, `961b888`, `3785cca`, `d6a4bd2`, `829c6f3`, `d8485f2`.
Prover version that ran: product-prover 1.4.0 (`4503881`), under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Two movements. The first, across thirteen commits, is a sweep over every number in the tree that
nobody could trace to a source: each one is now either removed with its dead home, marked for what
it is, or turned into a stated config defect rather than an invented fallback. The second, in
`829c6f3`, cuts the board from 162 task rows to 63 by rotating the folded rows into an archive.
`d8485f2` is this review's own three repairs, described under Findings.

## How this review was run

Read to refuse, not to confirm. The code diffs were read directly; the `PLAN.md` and archive diff
was read by a separate reader with no knowledge of the rest, briefed to find reasons to refuse, so
the board cut got a second pair of eyes that had not already formed a view of the range. Every
claim the range makes about a cited source was checked against that source rather than taken from
the commit message.

Range: e7fafcf..d8485f2

Files read: `.github/workflows/gates.yml`, `guardrails/check-prover-record.sh`,
`guardrails/check-doc-rotation.py`, `guardrails/check-pin-drift.sh`, `guardrails/pre-push`,
`guardrails/check-board.py`, `guardrails/check-deposit-description.py`,
`guardrails/check-landing-next-steps.py`, `guardrails/check-runaway-child.py`,
`guardrails/check-skill-loadability.sh`, `guardrails/check-tier-refusal.py`,
`guardrails/check-worker-restore.py`, `guardrails/crosscut_counter.py`,
`guardrails/language-rules.json`, `guardrails/net_meter.py`, `guardrails/progress-baseline.json`,
`guardrails/reap_owned_group.py`, `guardrails/tier-refusal.json`,
`hooks/conduct-judge-collect.sh`, `hooks/register-judge-collect.sh`,
`hooks/register_judge_core.py`, `hooks/lean-orchestrator-scan.py`,
`scripts/install-external-skills.sh`, `scripts/check-eyes-marker.py`, `scripts/plan-step.sh`,
`scripts/plan_checks.py`, `scripts/state-probe.sh`, `scripts/progress-report.py`,
`scripts/preshow-register-lint.py`, `scripts/spec-redundancy-precheck.py`,
`scripts/spec-style-lint.py`, `scripts/measurements-table.py`, `scripts/check-shipped-language.py`,
`scripts/check-pack-update.sh`, `scripts/needle-extract.py`, `scripts/onboarding-card.py`,
`scripts/rotate-doc.py`, `templates/headless_harness.py`, `templates/test_scaffold.template.py`,
`tests/test_prover_adapter_contract.py`, `tests/test_eyes_marker_traces_to_owner.py`,
`tests/test_tier_refusal.py`, `tests/test_board_matches_the_canon.py`,
`tests/test_tasks_parser_finds_every_task.py`, `PLAN.md`, `ROADMAP.md`, `CLAUDE.md`,
`architecture/intake.md`, `docs/language-rules.md`,
`docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`,
`docs/queue-archive/2026-08-28-archived-no-acceptance.md`,
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`,
`docs/audits/2026-08-07-number-rulings.md`, `work/2026-08-15-unowned-numbers.md`,
`skills/product-prover-pack/SKILL.md`, `skills/live-spec-base/SKILL.md`.

Checks run: `bash guardrails/pre-push < /dev/null` at `829c6f3` — exit 1, two gates red,
gate a (no record for today) and gate t (doc rotation), every other gate green.
`python3 guardrails/check-doc-rotation.py` — red before the repair, green after.
`python3 -m pytest tests/test_eyes_marker_traces_to_owner.py -q` — 1 failed, 3 passed.
`python3 guardrails/check-tier-refusal.py` — exit 0 against the live config.
`gh run list -L 6` and `gh run view 33088876799 --log-failed` — five consecutive CI failures on
main since 27.08, all on the pinned prover canon being below the pack's floor.
`git ls-remote origin main` inside `skills/product-prover` — the 1.4.0 commit is the published tip.
`git rev-list --all --objects | grep decision-dossier` — no match anywhere in history.
`diff` of each changed hook against its installed copy under `~/.claude/hooks/` — identical.

Findings: ten, listed below — three defects this review repaired, three it found and left standing
because their repair lives in a file it was fenced out of, and four claims of the range's own that
were checked against their sources and hold.

1. **Gate t was red at `829c6f3`, and no local run before this one had seen it.**
   `docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md` was created carrying 94 rows that
   left the board, with no manifest line pointing at it anywhere in the tree. The 17 `Absorbed:`
   pointers in `PLAN.md` are prose the rotation check cannot read; the only manifest block is
   `ROADMAP.md:28-35` and it did not name the file. Under base rule 10 that content is archived
   without the note that says where to find it. Repaired in `d8485f2`: the archive opens with an
   index table, one line per folded row carrying its own number and the terminal status
   `superseded 2026-08-28`, and `ROADMAP.md`'s manifest block names all 92 numbered rows.
   `plan-1` and `plan-13` carried no row number and stand under their fold headings, which the
   archive's own header already states.

2. **CI has been red on main since 27.08, and every local run passed.**
   `.github/workflows/gates.yml` pinned the external product-prover canon at `540914d7`, version
   1.3.1, while `skills/product-prover-pack/SKILL.md` requires `>= 1.4.0`. The installer step
   failed on the floor and two suite assertions failed behind it, five runs in a row. The local
   clone is untracked and already at 1.4.0, so no local run could ever see it — the gap between
   what the pack asserts and what CI installs was invisible on exactly the machine that would have
   caught it. Repaired in `d8485f2`: repinned to `4503881483bb33e760b66fb845ca8d86b6eb11a0`, the
   1.4.0 tip of the prover repository's own main, confirmed against the remote rather than taken
   from the local clone alone.

3. **The range's own new test fails against the real board, and this one still stands.**
   `8ed2771` added `tests/test_eyes_marker_traces_to_owner.py`, whose fourth test asserts that no
   task on the live `PLAN.md` carries a needs-his-eyes mark with a Source line that is not the
   owner's word. Two commits later `829c6f3` marked `plan-9` and `plan-15` with that mark; neither
   Source line is his word — `plan-15`'s reads only "PLAN.md step 15.", which names no fact only he
   can supply. The test fails. It was already failing at `829c6f3`, before anything in `d8485f2`
   touched the tree: the function under test is byte-identical to the one that commit shipped, and
   this review changed neither the test nor `PLAN.md`. The push gate's own suite step is scoped by
   the diff's reach and did not reach this file; CI runs the suite whole and would red on it.
   Both candidate repairs — correcting the two markers, or correcting their Source lines — are
   edits to `PLAN.md`, which this review was fenced out of, and the choice between them is a
   judgment about the owner's own board rather than a mechanical fix. Left standing, named here.

4. **`PLAN.md` contradicts itself about `plan-9`.** `829c6f3` changed the task's heading mark to
   needs-his-eyes and left the note four lines below it reading "Marked ⬜, waiting on that session
   and the owner's own 'after the release' timing". The heading and the body now state different
   marks for one task. Same fenced file as finding 3, and the same repair moment.

5. **One archive from this range is named by no file at all.**
   `docs/queue-archive/2026-08-28-q405-agent-messaging-stale-premise.md` holds `q-405`;
   `PLAN.md:923` records that the row was archived and gives no path to it. It escapes the rotation
   check only because its filename does not match that check's `rotated-*.md` glob. Nothing is lost
   from git, and nothing points a reader at it either.

6. **`scripts/check-eyes-marker.py` ran only from the repo root.** Both its import of
   `plan_checks` and its open of `PLAN.md` resolved against the current directory, so it raised
   anywhere else, unlike every sibling script in `scripts/`, which resolve from their own path.
   Repaired in `d8485f2`.

7. **The range's central claim holds, checked independently.** Six comments across the tree cited a
   `decision-dossier-2026-08-15.md` as the ruling behind a kept number. Searching the full git
   object graph, not only the working tree, that file has never existed in this repository at any
   commit. `961b888` replaces all six citations with `work/2026-08-15-unowned-numbers.md`, which
   does exist and whose line 11 reads "No repair, no deletion, no ruling is made below." Every
   replacement citation resolves: `docs/audits/2026-08-07-number-census.md`,
   `docs/audits/2026-08-07-number-rulings.md` §3 and its representative-homes list, and
   `docs/prose-quality-gate-design.md` are all present and say what the comments claim.

8. **The judge deadline change is safe on the live machine.** `c85fff7` raises
   `DEFAULT_TIMEOUT_S` in `hooks/register_judge_core.py` from 25s to 120s and drops the explicit
   `REGISTER_JUDGE_TIMEOUT=120` from both collect scripts. Had the installed copies under
   `~/.claude/hooks/` still carried the old default, the judge would have started timing out at 25s
   on a call measured at ~33s — a working arm turned silent. All four changed hook files were
   compared against their installed copies and are identical, so the change lands whole.

9. **The two removals leave nothing dangling.** `min_reply_chars_judged` is gone from
   `guardrails/language-rules.json` and `docs/language-rules.md`, and no reader for that key remains
   anywhere in the tree. `2f873ab` removes the invented 1-to-99 phrase-width fallback from
   `guardrails/check-tier-refusal.py`; the live `guardrails/tier-refusal.json` declares 2 and 8, so
   no live verdict changes, and a config that omits the width is now reported as a config defect
   instead of passing almost any phrase silently.

10. **The board cut loses no row.** 100 task ids left the board. 94 are in the folded-rows archive,
    5 in `2026-08-28-archived-no-acceptance.md`, and `q-405` in its own file. Every `Absorbed:`
    line's claimed count matches the ids it lists, and the 17 lines sum to exactly 94.

Blocking: one item.
- stands: `tests/test_eyes_marker_traces_to_owner.py::test_clean_on_the_real_plan` fails on the live `PLAN.md` (finding 3). Both repairs available are edits to `PLAN.md`, which this review is fenced out of, and choosing between correcting the two markers and correcting their Source lines is a judgment about the owner's own board. Weakening or removing the assertion was refused: the check is right about `plan-15`, whose Source names no fact only he can supply. The range does not go out until whoever holds `PLAN.md` settles it, and that landing owes a fresh record, since it will carry a commit newer than this one.
