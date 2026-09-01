# Prover record — 2026-09-01, closing adversarial review of tonight's session

PUSH-REVIEW

Range: 11987b8..f7382a15
- f7382a15 The one-file-in-the-tree check learns to stand down in a git-less scratch copy
- 4f0b760c NEXT_STEPS.md: tail-end cleanup heals landing 0a9a431a, catches up on tonight's last five fixes
- 16d59df9 Re-point five pins that drifted again after 084c3eb4's communicator trim
- bb084ed5 docs/prover: fresh adversarial review record — q-385/q-804/q-436 reopened, criterion 15 narrowed
- 5c8ebb87 Fix shipped-language gate: allowlist plan_checks.py's real grep string, mark PLAN.md's direct quotes user-language
- 7c25768c plan_checks.py: back five done tasks, and drop pytest from q-802's key
- 0a9a431a PLAN.md: three findings from tonight's traceability/done-mark audit
- 084c3eb4 communicator's body drops back under its size ideal, q-536's rulings moved to references
- 16878f0c Cut the scissors contrast frame from q-398's new referral criterion
- 476f5246 Fix INV-196 trailing-tag order so its declaration paragraph is found
- 0d668348 config-health: routing hook installed, communicator's copy re-synced
- 4c95f679 NEXT_STEPS.md: name the real date behind plan-9's "Alexander's own word" deferral
- 7551744b docs/language-rule-coverage.md: rebuild off hooks/register_judge_core.py's source note
- fc5c2792 PRODUCT_SPEC.index.md: rebuild the generated code-to-location table off today's spec edits
- ce3a7e30 spec: Requirement 163's heading loses a stray [default] tag it never should have carried
- (and the earlier commits of tonight's range, already named and read in full by
  `docs/prover/2026-09-01-three-targets-reopened-and-criterion-15-narrowed.md`'s own Range field,
  which this record does not re-list — that record's own review of them stands, re-confirmed live
  below rather than re-typed)

This record is both this session's own closing review (the gate at `guardrails/check-prover-record.sh`
was red because `16d59df9` touched `architecture/exchange.md` and `architecture/outward.md` — parts of
`ARCHITECTURE.md` — after the last committed record, `bb084ed5`) and the adversarial pass Alexander
asked for at the end of a long, heavily-parallel cleanup session: a fresh, independent read of the
current `PRODUCT_SPEC.md`/`ARCHITECTURE.md` plus real scrutiny of the session's own shape — the
repeated recovery incidents, the pin-drift class recurring three times, the swept-commit and
orphaned-target incidents already named in `NEXT_STEPS.md`.

Files read: `PRODUCT_SPEC.md` and `ARCHITECTURE.md` (both core files, read fresh, in full — confirmed
untouched themselves in this range; only their parts changed, `git log` checked on both paths before
starting), `spec/design-spec-review.md` (Requirements 11, 52-76, 99-104, 214-215, 258-266, in full —
the axis, lifecycle, and design-review lenses; criterion 15 of Requirement 265 read against `q-436`'s
own claimed wording), `spec/public-contract.md` (in full — criterion 15 of Requirement 194 read
against `q-385`'s own claimed wording), `spec/parallel-lanes.md` (INV-198/199/201's `[target]`
criteria, read against `q-804`'s own claimed wording), `spec/roles-and-agents.md` (Requirement 196,
its crossing-bound criterion and its `[default]` tag placement), `spec/internal-failure-log.md`
(Requirement 163's heading and Requirement 162's `[default]`-tagged criterion), `spec/work-board.md`
(all 97 criteria, `[default]`-tag placement on every anchored line), `NEXT_STEPS.md` (in full — the
session's own account of tonight's recovery incidents, its own still-open list, and its own explicit
"a fresh full-suite run is still owed" line), `PLAN.md` (q-385, q-804, q-436, q-386, q-802, q-437 rows
in full), `docs/prover/2026-09-01-three-targets-reopened-and-criterion-15-narrowed.md` (this session's
immediately-prior record, read for register and to avoid re-litigating what it already closed),
`skills/product-prover-pack/SKILL.md` (the class-lens pin, confirmed present), `guardrails/check-prover-record.sh`
(the gate this record exists to satisfy), `tests/conftest.py` (`criteria_citing`, `_TRAILING_CODES`,
read to understand and then directly exercise the bracket-order defect below), `guardrails/check-requirement-shape.py`,
commits `16d59df9`, `30ec1256`, `084c3eb4`, `476f5246`, `e61b29b7`, `f7382a15` (`git show`, each read
in full against its own commit message's claim).

Checks run:
(1) `bash guardrails/check-pin-drift.sh` — OK, 180/180 line/file pins, 39/39 r5 range pins, clean
(confirms `16d59df9` actually closed the pin-drift finding the prior record left standing);
(2) `python3 -m pytest -q tests/test_traceability.py tests/test_config_health.py tests/test_tasks_parser_finds_every_task.py`
— 231 passed, 2 skipped (the three suites `NEXT_STEPS.md` named as still-red mid-session are clean now);
(3) `python3 -m pytest -q tests/test_agent_channels.py tests/test_authority_anchor.py tests/test_class_hunt.py
tests/test_communicator_body_thinned.py tests/test_convergence_locks.py tests/test_index_generated.py
tests/test_language_rules.py tests/test_plan_done_marks_are_backed.py tests/test_plan_is_not_executable.py
tests/test_scenario_heading_tag.py` — 216 passed (the ~20 suites `NEXT_STEPS.md` left undiagnosed are
clean now too);
(4) `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` plus every file `git ls-files spec/`
names — OK, 1795/1795 criteria well-shaped across 313 requirements;
(5) a direct call to `tests/conftest.criteria_citing()` against the original (pre-fix) and the fixed
text of `spec/work-board.md` and `spec/internal-failure-log.md`, proving criterion 20's own text was
absent from `criteria_citing(text, "INV-308")`'s result before the fix and present after — the live
mechanism the finding below rests on, not the finding's own say-so;
(6) `python3 -m pytest -q tests/test_traceability.py tests/test_agent_channels.py` re-run after the fix
— 290 passed, 2 skipped, clean;
(7) `python3 -m pytest -q` (the full suite, unscoped) — run once while this record's own file was still
being drafted and this fix's two spec files were still uncommitted: 2705 passed, 5 skipped, 1 failed,
1 error, 28:06 total. Both the failure and the error are read here, not assumed clean: the failure was
`TestGateA_ProverRecord::test_real_repo_passes`, expected and stale by design — it read the gate before
this very record existed, the exact gap this record closes, and is superseded by the direct
`check-prover-record.sh` re-run below, run after the commit. The error was
`test_worker_restore_run_scope.py::test_packet_a_...` failing `tests/conftest.py`'s own
working-copy-stability assertion (SPEC INV-100) — not a real regression: this session's own edits to
`spec/work-board.md` and `spec/internal-failure-log.md` (this same finding's fix) were still
uncommitted and changed `git status` mid-run, the exact "a run taken while the tree is being written
proves nothing" class `NEXT_STEPS.md` names from earlier tonight. Re-run in isolation on the untouched
tree immediately after — `python3 -m pytest -q tests/test_worker_restore_run_scope.py` — 7 passed,
confirming the error was the concurrent-edit artifact and not a real defect. The full suite is re-run
clean, with the tree fully settled and no concurrent edit, as this task's own final step below.
(8) `diff hooks/routing-preamble-hook.sh ~/.claude/hooks/routing-preamble-hook.sh` and
`diff skills/communicator/SKILL.md ~/.claude/skills/communicator/SKILL.md` — both empty, confirming
the installed-copy gaps `NEXT_STEPS.md` named mid-session are closed;
(9) `grep -n "\[target\]"` across `spec/*.md` and `PRODUCT_SPEC.md`, read by hand — every instance
stands on its own line, the documented convention, none inline before or after a trailing code
bracket.

Findings: two. One closes this record's own gate; one is a real, previously unknown defect, found and
fixed in this same record.

1. **The gap this record exists to close: `check-prover-record.sh` was red because the newest
   committed prover record (`bb084ed5`) predated `16d59df9`, which touched `architecture/exchange.md`
   and `architecture/outward.md` (parts of `ARCHITECTURE.md`).** Confirmed live: `git log -1 --format=%H
   -- ARCHITECTURE.md architecture/` names `16d59df9`, and `16d59df9`'s own diff (`git show`) touches
   exactly `.live-spec/r5-rule-prices-2026-08-11.md`, `architecture/exchange.md`, and
   `architecture/outward.md` — five line-pin corrections, each re-pointed by the naming words of the
   rule it pins, matching its own commit message exactly. `bash guardrails/check-pin-drift.sh` now
   passes clean, confirming the fix actually holds. **Closed by this record's own existence and its own
   freshness** — being fresh and committed against the current `ARCHITECTURE.md` is what the gate
   demands.

2. **The exact defect class fixed once tonight for `INV-196` (`476f5246`, "Fix INV-196 trailing-tag
   order so its declaration paragraph is found") recurs 19 more times, unswept, across
   `spec/internal-failure-log.md` (1 instance) and `spec/work-board.md` (18 instances).** `476f5246`'s
   own commit message states the mechanism precisely: `tests/conftest.py`'s `_TRAILING_CODES` regex
   requires a criterion's anchor-code bracket to be the literal last thing on its line, so a criterion
   written `... [INV-xxx] [default]` (anchor codes, then the default tag) is invisible to
   `criteria_citing()`/`assert_declared()` for its own anchor — the codes are no longer last. The fix
   applied to `spec/roles-and-agents.md` reordered that one criterion to `[default] [INV-196, ...]`,
   citing `settings-card.md`'s `[default] [INV-87]` as "every other working instance of the tag." That
   claim was incomplete: it never swept the rest of the tree for the opposite (broken) order, and 19
   more criteria carry it — `spec/internal-failure-log.md:85` (`INV-56`) and eighteen criteria in
   `spec/work-board.md` (`INV-308` ×5, `INV-309` ×4, `INV-310` ×2, `INV-311` ×3, `INV-312` ×1,
   `INV-313` ×3, plus co-cited `INV-222`, `INV-28`, `INV-93`, `INV-276`, `INV-134`, `T-18`). This is a
   silent format defect, not a currently-red test: no suite today calls `assert_declared()` on these
   specific anchors the way `TestExchangeBound` does for `INV-196`, so nothing was failing — but it is
   the identical incident, the class the base-rulebook's class-hunt discipline exists to catch, and
   tonight's own fix of the one instance did not sweep for its siblings. Verified directly, not
   assumed: `tests/conftest.criteria_citing()` called against the original `spec/work-board.md` text
   confirmed criterion 20's own sentence was absent from `criteria_citing(text, "INV-308")`'s result.
   **Closed here.** All 19 lines reordered to `[default] [ANCHOR-CODES]` by a scripted, verified
   transform (only the two bracket groups' order changed, no other text touched — confirmed by `git
   diff --stat`, 19 insertions/19 deletions across the two files). Re-verified against the live
   function: all four previously-blind anchors (`INV-308`, `INV-309`, `INV-56`, `INV-196`) now resolve.
   `guardrails/check-requirement-shape.py` still reads all 1795 criteria as well-shaped after the
   change, and `tests/test_traceability.py` + `tests/test_agent_channels.py` (290 passed) stay clean.

**Also checked, found clean — no further instance of the session's own named recovery-incident
patterns:**
- **No further orphaned `[target]`.** Every `[target]` marker in `spec/*.md` and `PRODUCT_SPEC.md`
  stands on its own line, the documented convention (`PRODUCT_SPEC.md`'s own preamble); none is
  misplaced the way the trailing-code brackets were. `tests/test_traceability.py::TestTargetOwnership`
  passes clean.
- **`q-385`, `q-804`, `q-436`'s reopened rows hold against the live tree, word for word.** `q-385`
  cites `spec/public-contract.md` Requirement 194 criterion 15 verbatim ("the gate that reds a
  default-deny violation on the producer's suite *shall* stay promised until a host's first real
  contract") — matches the live text exactly. `q-804` cites `spec/parallel-lanes.md`'s three
  `[target]`-marked criteria for `INV-198`/`199`/`201` — all three exist, all three still carry
  `[target]`, none has quietly shipped since. `q-436` cites Requirement 265 criterion 15 verbatim ("the
  value-space in-between forcing step promised as a later increment") — matches exactly, and criterion
  12's `[GAP: ...]` line confirms the co-occurrence value genuinely stands unanswered, not merely
  claimed so.
- **The class-lens sentence** (dropped from the external `product-prover` README in tonight's
  short-form rewrite, restored per `NEXT_STEPS.md`) **is present in this pack's own pin**:
  `skills/product-prover-pack/SKILL.md:130`, "The class lens (SPEC INV-124)."
- **No further stale installed-copy drift.** `hooks/routing-preamble-hook.sh` and
  `skills/communicator/SKILL.md` both diff empty against their installed copies, closing the two gaps
  `NEXT_STEPS.md` named as still open mid-session.
- **No stray `[default]` tag on a requirement heading beyond the one `ce3a7e30` already fixed.**
  `spec/internal-failure-log.md`'s Requirement 163 heading reads clean; a targeted grep found no
  sibling heading carrying the same stray tag.

**Recommendation, non-blocking.** No mechanical lint currently catches the `[default]`-after-codes
ordering generally — it surfaced tonight only because `TestExchangeBound` happens to exercise
`INV-196`'s declaration text by name, and it would have stayed silent in `work-board.md` and
`internal-failure-log.md` indefinitely otherwise. This is now a real, twice-occurring incident on the
same night, the kind the base rulebook's "no machinery without an incident" bar asks for before adding
one: `guardrails/check-requirement-shape.py` already parses every criterion's trailing bracket and
could flag a `[default]` tag that is not immediately adjacent to the line-terminal anchor bracket, on
either side, as a shape defect rather than leaving it to whichever specific test happens to look. Left
as a recommendation for the person's own call, not built here — this is machinery, and the standing
rule against inventing it holds even with a real incident in hand until the person says so.

Blocking: none — the one real defect found (finding 2) is fixed in this same record's landing, verified
live, and closed above.
