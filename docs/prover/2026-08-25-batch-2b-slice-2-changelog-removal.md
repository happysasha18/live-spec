# Prover record — 2026-08-25 batch-2b-slice-2-changelog-removal

PUSH-REVIEW

Range: ca6181db..6b0cd76f (2 commits)
- 8875ca80 Give 2 more batch-2b build-pipeline facts a home (slice 2)
- 6b0cd76f Skill-review record for batch-2b slice 2 (communicator, spec-author)

Files read: full diff of 8875ca80 (6 files, 17 insertions / 6 deletions);
`skills/communicator/references/writing-register.md`, `skills/communicator/SKILL.md`,
`skills/communicator/references/words.md`, `skills/spec-author/SKILL.md`,
`matrix/build-pipeline.md`, `tests/test_measurement_law_homes.py` (current state, not just the
diff); the corresponding source passages in `skills/build-pipeline/SKILL.md` (the CHANGELOG-vs-
journal paragraph, the removal-of-a-shipped-feature paragraph); `skills/live-spec-base/SKILL.md`
rule 10; `tests/test_traceability.py::test_parameter_default`,
`tests/test_restructure_merge_gate.py` in full (the two tests whose closed home-sets caught the
misclassification below); `PRODUCT_SPEC.md` and `spec/design-spec-review.md`,
`spec/project-setup-tuning.md` (the formal-spec homes for INV-70 and INV-114, which the original
batch-2b classification had not checked).

Checks run: an initial implementation drafted 4 items (INV-70, CHANGELOG-vs-journal, INV-114,
removal-of-shipped-feature) against the batch-2b list inherited from a prior session's two
independent adversarial rounds. Before sending that draft to review, the orchestrator
independently re-checked each item's target test file for a closed home-set assertion (the same
pattern that governs INV-131/INV-12/INV-45 in the prior slice) and found two real
misclassifications:

- **INV-70** — `tests/test_traceability.py::test_parameter_default` pins this law's homes to
  exactly `PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`, and `skills/build-pipeline/SKILL.md`.
  `PRODUCT_SPEC.md` already carries the full formal requirement (`spec/design-spec-review.md`,
  four numbered `*shall*` clauses). The prior session's classification checked only skill prose
  for duplication, not the spec document itself, and concluded (wrongly) that this was a gap.
- **INV-114** — `tests/test_restructure_merge_gate.py::test_the_split_covers_every_home_the_law_
  has` pins this law's homes to exactly `PRODUCT_SPEC.md`, `skills/build-pipeline/SKILL.md`, and
  `skills/product-prover/SKILL.md` (the external canon). `PRODUCT_SPEC.md` already carries the
  full requirement (`spec/project-setup-tuning.md`, a User Story plus numbered `*shall*`
  clauses). Same class of miss.

Both drafted additions were fully reverted (verified: `grep -n -i -E "INV-70|INV-114|tunable
parameter|restructure/migration merge gate"` on both touched files returns zero hits, and the
surrounding section transitions carry no stray blank lines or dangling references).

The other two items were re-checked the same way and held up:

- **CHANGELOG-vs-journal** — grepped `PRODUCT_SPEC.md` and every file under `spec/` for
  "CHANGELOG speaks"/"speaks to the user": no hits outside historical archives
  (`docs/queue-archive/`, `docs/attic/`). Genuinely homed only in `skills/build-pipeline/
  SKILL.md` before this slice (cited by `[T-6]`, not a formally spec'd `INV-` code). Kept, landed
  as writing-register.md's new rule 18.
- **removal-of-shipped-feature** — `skills/live-spec-base/SKILL.md` rule 10 already states the
  tombstone + retired-matrix-rows half verbatim-equivalent ("A removed feature leaves a dated
  tombstone in the spec and retired matrix rows"). The narrower residual — test deletion + doc
  sweep, same session — has no home outside `build-pipeline/SKILL.md` and its own skill-local
  README (grepped `PRODUCT_SPEC.md`, all of `spec/*.md`, and `live-spec-base/SKILL.md`: no hits).
  Kept, narrowed to cite base rule 10 rather than restate it, landed in `spec-author/SKILL.md`.

An independent adversarial reviewer (a different agent than the implementer, briefed to find
reasons to reject) re-derived every check above from scratch rather than trusting the
correction's own account: re-confirmed rule 10's exact text, re-grepped for redundancy on both
kept items, re-verified the two reverts left no trace, checked the M-101 punctuation reads
grammatically before and after, and re-ran the test suite and lint independently. Verdict:
APPROVE, no blocking findings (one minor stylistic note on M-101's edit — an existing
parenthetical had to become an em-dash clause to make room for the new pointer, since M-085 had
no such pre-existing aside to work around — judged not worth blocking on).

Independently: `python3 -m pytest -q tests/test_measurement_law_homes.py
tests/test_traceability.py tests/test_communicator_register_extracted.py
tests/test_communicator_body_thinned.py tests/test_gate_common_table_rows.py
tests/test_restructure_merge_gate.py` — 208 passed, 3 skipped (external product-prover canon
clone absent locally, expected), 0 failed, run twice independently (implementer, then
reviewer) with matching results. `scripts/spec-style-lint.py --tier universal` on all 5
non-test touched files: 0 errors introduced (the 2 pre-existing errors and 1 pre-existing
warning in `matrix/build-pipeline.md`, rows M-313/M-275, confirmed unchanged against
`git show ca6181db:matrix/build-pipeline.md`). `bash scripts/sync-skills.sh`: installed copies
match source, no drift. `bash guardrails/check-config-health.sh`: clean.

Findings: two real misclassifications caught before push (see above), both cleanly reverted and
independently re-verified. No other defect found. `build-pipeline/SKILL.md` is untouched by this
slice — its now-duplicated text is left in place until cutover step 3 removes the whole displaced
body in one movement.

Batch 2b originally listed 11 items; this session's work across slices 1-2 has now shown the
original count included at least 2 misclassifications (INV-70, INV-114), so the true remaining
count is smaller than "11 minus what's closed" suggests. Closed across both slices: INV-131,
INV-12+safety-net, INV-45 (slice 1), CHANGELOG-vs-journal, removal-of-shipped-feature-residual
(slice 2) — 5 real items landed. Removed from the list as never-actually-gaps: INV-70, INV-114.
Still open, NOT yet independently re-verified against PRODUCT_SPEC.md the same way (a real risk
given the two misses just found): recurring-bug-redoor, Step 7 INV-62/63, push-mechanics
INV-82/106, docs-layout pass INV-111 — each needs the same closed-home-set check against
PRODUCT_SPEC.md and spec/*.md before drafting any addition, not just a skill-prose duplication
check.

Blocking: none
