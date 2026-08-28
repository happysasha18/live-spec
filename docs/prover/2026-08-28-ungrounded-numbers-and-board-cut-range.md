# Prover record — 2026-08-28 the ungrounded-numbers sweep and the board cut

PUSH-REVIEW

Range: e7fafcf..5683773 (18 commits), reviewed as one pass. Base commit `e7fafcf`. Reviewed
commits, in order: `7f40238`, `6b2aad4`, `9602993`, `8ed2771`, `9582aea`, `2f873ab`, `c85fff7`,
`30a7a8e`, `7c60809`, `7cd90c1`, `20d0630`, `961b888`, `3785cca`, `d6a4bd2`, `829c6f3`,
`d8485f2`, `137f691`, `5683773`.

The first seventeen of those went out in one push, landing on the remote at `e067676`. CI reddened
on that push and its two catches are findings 11 and 12; `5683773` carries their repair. So the
range this record now sends is `e067676..5683773`, base commit `e067676`, and it is the same review
continued rather than a second one — one record per push, and one pass over one range.
Prover version that ran: product-prover 1.4.0 (`4503881`), under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Two movements. The first, across thirteen commits, is a sweep over every number in the tree that
nobody could trace to a source: each one is now either removed with its dead home, marked for what
it is, or turned into a stated config defect rather than an invented fallback. The second, in
`829c6f3`, cuts the board from 162 task rows to 63 by rotating the folded rows into an archive.
`d8485f2`, `137f691` and `5683773` are this review's own eight repairs, described under Findings.

## How this review was run

Read to refuse, not to confirm. The code diffs were read directly; the `PLAN.md` and archive diff
was read by a separate reader with no knowledge of the rest, briefed to find reasons to refuse, so
the board cut got a second pair of eyes that had not already formed a view of the range. Every
claim the range makes about a cited source was checked against that source rather than taken from
the commit message.

Range: e7fafcf..5683773

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
`docs/queue-archive/rotated-PLAN-2026-08-28-no-acceptance.md`,
`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md`,
`docs/audits/2026-08-07-number-rulings.md`, `work/2026-08-15-unowned-numbers.md`,
`skills/product-prover-pack/SKILL.md`, `skills/live-spec-base/SKILL.md`.

Checks run: `bash guardrails/pre-push < /dev/null` at `829c6f3` — exit 1, two gates red,
gate a (no record for today) and gate t (doc rotation), every other gate green.
`python3 guardrails/check-doc-rotation.py` — red before the repair, green after.
`python3 -m pytest tests/test_eyes_marker_traces_to_owner.py -q` — 1 failed, 3 passed.
`python3 guardrails/check-tier-refusal.py` — exit 0 against the live config.
`python3 -m pytest tests/test_eyes_marker_traces_to_owner.py -q` again at `137f691` — 4 passed.
`python3 scripts/check-eyes-marker.py` at `137f691` — clean, exit 0.
`gh run list -L 6` and `gh run view 33088876799 --log-failed` — five consecutive CI failures on
main since 27.08, all on the pinned prover canon being below the pack's floor.
`git ls-remote origin main` inside `skills/product-prover` — the 1.4.0 commit is the published tip.
`git rev-list --all --objects | grep decision-dossier` — no match anywhere in history.
`diff` of each changed hook against its installed copy under `~/.claude/hooks/` — identical.
`gh run watch 33158890831` on the first push of this range — failure, on two tests neither the
local chain nor the full local suite of the moment had reached.
`python3 -m pytest -q`, the whole suite the way CI runs it, at `5683773` — 2429 passed, 4 skipped,
exit 0, in 9m32s. Run because the push chain's suite gate defers the full run to the server, so a
green chain says nothing about a test the delta never reached.

Findings: twelve, listed below — eight defects this review found and repaired, and four claims of
the range's own that were checked against their sources and hold. Three of the eight needed a decision
about the owner's board rather than a mechanical fix; that decision is recorded under finding 3
and is the pack's own, made under his standing word of 28.08 00:53, not attributed to him.

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

3. **The range's own new test failed against the real board.**
   `8ed2771` added `tests/test_eyes_marker_traces_to_owner.py`, whose fourth test asserts that no
   task on the live `PLAN.md` carries a needs-his-eyes mark with a Source line that is not the
   owner's word. Two commits later `829c6f3` marked `plan-9` and `plan-15` with that mark; neither
   Source line is his word — `plan-15`'s reads only "PLAN.md step 15.", which names no fact only he
   can supply. The test fails. It was already failing at `829c6f3`, before anything in `d8485f2`
   touched the tree: the function under test is byte-identical to the one that commit shipped, and
   this review changed neither the test nor `PLAN.md`. The push gate's own suite step is scoped by
   the diff's reach and did not reach this file; CI runs the suite whole and would red on it.
   Repaired in `137f691`, in the direction the test points. The markers were placed by the cull
   pass on a brief, not on any word of his, and the deferral rule re-tests such a marker by
   derivability every time it is touched: both are derivable, so neither is his. Both rows also
   name work belonging to other projects' windows — `plan-9` the photo site's move, `plan-15` the
   promoter project's update — and one window serves one project, so this window cannot execute
   either regardless. They stand as ordinary queued rows for the window that owns each. The test
   was left untouched.

4. **`PLAN.md` contradicted itself about `plan-9`.** `829c6f3` changed the task's heading mark to
   needs-his-eyes and left the note four lines below it reading "Marked ⬜, waiting on that session
   and the owner's own 'after the release' timing". The note states the real status; the heading now
   agrees with it, in the same `137f691`, `5683773`.

5. **One archive from this range was named by no file at all.**
   `docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md` holds `q-405`;
   `PLAN.md`'s Blockers section recorded the row being archived and gave no path to it. It escapes
   the rotation check only because its filename does not match that check's `rotated-*.md` glob, so
   nothing mechanical would ever have pointed a reader at it. The path is now written where the
   archiving is recorded, in `137f691`, `5683773`.

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
    5 in `rotated-PLAN-2026-08-28-no-acceptance.md`, and `q-405` in its own file. Every `Absorbed:`
    line's claimed count matches the ids it lists, and the 17 lines sum to exactly 94.

11. **Four target owners pointed at rows the cut folded away, and one of them had nowhere to point.**
    Found by CI on the first push of this range, not by any local run. `PRODUCT_SPEC.md`'s
    `[target]` markers are mapped to an owning task in `tests/test_traceability.py`, and `829c6f3`
    folded four of those owners off the board: `E-18` stood on `q-93`, `INV-21` on `q-96`,
    `INV-185` on `q-385`, `INV-244` on `q-437`. Repaired in `5683773` by re-owning each to the row
    that absorbed it — `q-54`, `q-48`, `q-398` and `plan-12` — read off the fold archive rather
    than guessed. No tag was dropped and no assertion loosened; every target still carries an open
    owner.
    Behind the fourth sat a defect of the 27.08 merge itself, which is the finding worth keeping.
    That merge gave the board two id shapes, `q-<N>` and `plan-<N>`, and the ownership map's reader
    only ever matched `q-<N>`. Half the board was therefore invisible to it, so any target whose row
    was folded into one of `PLAN.md`'s own steps read as an orphan with no home it could be
    re-owned to. The reader now matches both, which is what lets `INV-244` name `plan-12` at all.

12. **A test asserted that an archived row was still on the board.**
    `tests/test_listener_tripwire.py` asserted `PLAN.md` still carries `q-405`'s mechanical revisit
    trigger. The row left the board on his word of 28.08 and was archived whole, its trigger with
    it. Repaired in `5683773`: the assertion follows the row to
    `docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md` and keeps what it always
    guarded, that a session needing the deferral again finds the trigger beside the row instead of
    re-deriving it from memory. `INV-231` itself stays guarded by the three tests above it, which
    read the spec, the architecture and the matrix and are untouched. The test is renamed for where
    the row now lives, and matrix row M-412's citation of it moves in the same commit.

Blocking: one item, closed.
- closed: `tests/test_eyes_marker_traces_to_owner.py::test_clean_on_the_real_plan` failed on the live `PLAN.md` (finding 3) and passes at `137f691`, verified by running that file directly rather than through the push chain, whose suite gate is scoped by the diff's reach and defers the full run to the server. The needs-his-eyes marks came off `plan-9` and `plan-15`; the test itself was not loosened, skipped, or excepted.
