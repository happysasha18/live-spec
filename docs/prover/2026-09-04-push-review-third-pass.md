# Prover record — 2026-09-04 third pass, before push

PUSH-REVIEW

Prover skill version: product-prover (installed under `skills/product-prover/`), read beside
`skills/product-prover-pack/SKILL.md` v6.1.0 (pack bindings) and `skills/live-spec-base/SKILL.md`.

Range: 0a90c786..37a68368
- 37a68368 Gate s matched a skill's own name in prose, not its Skill: field; live-spec-base's rule 41 reviewed
- 0696bc11 The push-review record's Blocking field, fixed to the gate's literal shape
- 8a2d04fa Third prover pass before push: the liveness fixture's own defect, found and folded
- 86c7b420 checkpoint: refresh suite-green fingerprint cache
- a4c90991 This session's own re-check: the liveness fixture proved a value, not a read
- d9075a70 checkpoint: refresh suite-green fingerprint cache
- ab789ecc checkpoint: refresh suite-green fingerprint cache
- 5db3d847 Two architecture pins re-pointed after skills/live-spec-base/SKILL.md's line shift
- 15b1afac The resume file is refreshed for the recheck-fix landing and q-825's own rise and fall
- 915ef1c9 checkpoint: refresh suite-green fingerprint cache
- ce06c9f7 The prover's re-check findings on today's repairs, repaired (R1, R2/R3, R5, R6, R9, R12)
- b2f57c17 wip: partial work on the prover re-check's blocking findings, saved before shutdown
- cfae513b The shutdown note carries what the day actually turned into
- 5daf46e2 A defect is a gap between what was promised and what happens (rule 41)
- c746316c A defect that opens a row carries the way to see it (rule 41)
- 96d7a53f Delete today's own machinery, and put the door test in its place (rule 41)
- d71e2384 A finding is not a row, and the board says what raised each one (PLAN q-825)
- 175d6064 Where this stands at shutdown: five rows closed, three blocking defects open, nothing pushed
- 12f084c9 The success-measure promise the prover caught this session dropping (PLAN q-824)
- 3d30e495 A test that only passed when its neighbours ran first now puts the path there itself
- dc7a9447 The resume file is refreshed for the day's five landings, and the load-weight row opens (PLAN q-822)
- e9fe5a0e Merge branch 'lane/q818-prover-fixes'
- a8c54239 Fix what the suite caught: a duplicate row id, a satisfied promise still tagged, and two checks the probe should not carry
- 523b67a1 wip: the prover's six blocking findings
- 56d783b4 Every skill measured by the tool with its verdict quoted, and the reading defect that pass found (PLAN q-817, q-821)
- 5436d680 A project's live numbers print beside its rows, and the cadence comes from whoever owns the fetch (PLAN q-48)
- 3c90fcc2 One status renderer for every project, and a next move derived from a written rule (PLAN q-818, q-819)
- 8fceae92 Merge branch 'lane/q818'
- 1f3a7391 wip q-818: one status renderer, its extras hook, and the drift check
- 9dc63706 Skill-creator review on record for product-prover, the one skill the 2026-09-04 pass had not reached (PLAN q-817)
- bb684786 The rulebook's readability pass, and the reviews the changed skills owe (PLAN q-817)
- d582e5bd The skill-review gate reads the tool's own verdict, and a suffixed invariant id stops being invisible
- 336a9081 Merge branch 'lane/q817'
- e71e3ed8 wip q-817 gate
- a94cea98 A correction replans work already running and opens no row (PLAN q-820)

Coverage note: the earlier part of this range, up through 12f084c9, was already read
adversarially by two records committed inside it —
`docs/prover/2026-09-04-status-renderer-priority-and-feed-delta.md` and
`docs/prover/2026-09-04-repairs-recheck.md`. This pass reads that part for continuity and gives
its own fresh, adversarial read to everything after it: d71e2384 through 37a68368 — rule 41's
rise and fall of PLAN q-825, the four repairs the recheck record demanded (R1, R5, R6, R9, R12,
folded with R2/R3), this session's own housekeeping (two stale architecture pins, the resume-file
refresh, the checkpoint cache), and — surfaced by this record's own three commits at its tail — a
real bug in gate s itself, met and closed while getting this very push through it.

Files read: PRODUCT_SPEC.md (spec/live-status-reporting.md), ARCHITECTURE.md
(architecture/guardrails.md, architecture/rules-and-settings.md, architecture/pipeline-and-lanes.md),
TEST_MATRIX.md (matrix/guardrails.md), guardrails/check-status-view-drift.py,
adopt/install-status-view.sh, scripts/plan_checks_core.py, scripts/state-probe.sh,
scaffold/status-view/state-probe.sh, templates/PLAN.template.md, NEXT_STEPS.md,
tests/test_status_view_drift.py, tests/test_status_view_install.py, tests/test_priority_order.py,
tests/test_director_route_end_to_end.py, skills/live-spec-base/SKILL.md (rule-41 addition, the
readability pass's line shift), guardrails/check-skill-review.sh, tests/test_skill_review.py,
docs/skill-review/2026-09-04-architect.md, docs/skill-review/2026-09-04-director-correction-
counting.md, docs/skill-review/2026-09-04-live-spec-base-rule-41.md.

Checks run: `python3 -m pytest -q` — 2,847 passed, 5 skipped; pin-drift, style-lint and the
row-origin-orphan grep below, each read by hand.
- `python3 -m pytest -q` — 2,847 passed, 5 skipped (full range on this commit; the one prior red,
  the prover-record gate itself, is answered by this record; the one prior teardown error is the
  suite's own checkpoint-cache write, a known, accepted self-write this record's own commit closes).
- `bash guardrails/check-pin-drift.sh ARCHITECTURE.md` — 190 pins checked, none drifted.
- `bash guardrails/pre-push` (a real push attempt) — surfaced gate s (skill review) failing on
  'director', matched to the wrong covering record; traced to `check-skill-review.sh` grepping a
  changed skill's name across a candidate record's WHOLE body rather than its own `Skill:` field,
  so `docs/skill-review/2026-09-04-architect.md` — which names "director" only in a sentence
  comparing its own findings to an earlier director review — wrongly stood in for director's real
  record. Reproduced in a scratch repo (`tests/test_skill_review.py::test_a_sibling_records_
  prose_naming_this_skill_is_not_its_covering_record`), red under the old match, green under a
  `^Skill: <name>$` field match. `python3 /Users/sashaabramovich/.claude/skills/skill-creator/
  scripts/quick_validate.py skills/live-spec-base` — `Skill is valid!` (exit 0), quoted in the new
  `docs/skill-review/2026-09-04-live-spec-base-rule-41.md`. `bash guardrails/check-skill-review.sh`
  — clean after both fixes.
- `git diff -q 3d30e495..cfae513b -- architecture/guardrails.md spec/live-status-reporting.md` —
  read by hand to resolve the rebase conflict cleanly; both sides' independent edits (main's
  INV-324 wording, this lane's INV-325 wording and Requirement 320 criterion 7a) kept, neither
  dropped.
- `python3 scripts/spec-style-lint.py --gate ARCHITECTURE.md` / `PRODUCT_SPEC.md` — clean, after
  rewriting the INV-325 entry's own em-dash contrast cut plain.
- `grep -rn "INV-321\|check-row-origin\|test_row_origin\|Requirement 321"` across the tree — the
  deleted row-origin machinery (rule 41's own predecessor) left no orphan; the `INV-321` hits that
  remain are a pre-existing, unrelated invariant (criteria naming their own enforcement machinery)
  that happens to share the number with the deleted top-level `Requirement 321` — a different
  numbering sequence, not a collision.

Findings: two defects (F1, F2), both folded in this same landing, and one non-blocking
recommendation (R1), detailed below.

F1 (defect, folded in this same landing) — `test_the_next_answer_follows_the_recorded_state_
rather_than_standing_still` (tests/test_director_route_end_to_end.py), as R2/R3 left it, asserted
the identical string ("route-2") both before and after the state change it drove, because route-1
was never a NEXT candidate on either side of that change under rule 38. A frozen or memoized NEXT
computation would have passed the test unchanged. Closed: rewrote the test to close route-2 (the
row actually winning NEXT) instead of route-1, so the answer genuinely changes — NEXT has nobody
left to name once both rows are non-candidates — and a stale reading is now distinguishable from a
live one. Proven green on the current renderer; the renderer itself was not touched.
`defect · undefined-path (transitions)`

F2 (defect, folded in this same landing) — `guardrails/check-skill-review.sh`'s
`find_covering_record` matched a candidate record for a changed skill by grepping the skill's name
as a whole word anywhere in the record's body (`grep -qw "$name"`), rather than reading the
record's own `Skill: <name>` field every record already carries by convention. Met live on this
push: `docs/skill-review/2026-09-04-architect.md` mentions "director" once, in a sentence
comparing its own findings to an earlier director review, and that mention — not a real director
review — is what the gate matched, then correctly failed on for quoting no validator output,
masking the true state (director actually has its own fresh, correct record, and live-spec-base
did not). A skill whose real covering record happened to be named or ordered differently than its
false match could have had the false match's tool-quote checked instead, or, had that false match
carried a quote, passed on a review that never touched it. Closed: matched `^Skill:[[:space:]]+
$name$` instead. Proven with a scratch-repo repro building the exact failure shape — a sibling
skill's record landing after the changed skill's own edit, naming it once in prose — red under the
old match, green under the field match; the whole `tests/test_skill_review.py` suite (30 tests)
still passes.
`defect · boundary-issue (composition)`

R1 (recommendation) — `guardrails/check-status-view-drift.py`'s relative-pack-root resolution
(R12) always succeeds on POSIX (`os.path.relpath` does not raise short of a cross-drive path), so
the `pack_root` recorded by `adopt/install-status-view.sh` is always relative on this platform,
however far the pack sits from the host — a deeply nested, unrelated location produces a long
`../../..`-chain rather than falling back to absolute. This still resolves correctly wherever the
same relative arrangement is reproduced (the stated sibling-checkout case, and any CI layout that
preserves it), and a pack genuinely unreachable from the host already stands the check down by
name regardless of the path's form, so nothing observable breaks. Recorded as a note for the
`[default]` this design already carries rather than a defect: the fallback-to-absolute branch is
live only off POSIX.
`recommendation · later · edge-condition (bounds)`

Class lens: swept — the before/after-liveness shape F1 names was checked against the other new
tests this range added (`tests/test_status_view_drift.py`, `tests/test_status_view_install.py`,
`tests/test_priority_order.py`, 46 test functions total): none of the others carry a two-probe
before/after pair, each being a single red-then-green assertion, so the class is confined to the
two director-route fixtures R2/R3 already touched, both now proven. F2's class — a name-match
standing in for a structured field's own value — was checked against the prover-record gate
(`guardrails/check-prover-record.sh`) sharing this gate's shape: it matches a record by the
`PUSH-REVIEW` marker plus dated-filename convention, not a body-wide name grep, so it does not
carry the same class. No other same-day gate does a body-wide `grep -qw` for an identifier this
review found.

Blocking: none

F1 is closed in commit a4c90991; F2 in commit 37a68368 (with `docs/skill-review/2026-09-04-
live-spec-base-rule-41.md` closing the substantive skill-review demand F2's own fix then let
through correctly). Both per rule 41 and this pass's own no-park convention (INV-140) — nothing
stands open against the push.
