# Skill review — director

SKILL-REVIEW

Skill: director

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is designed for authoring/tuning a skill from test-prompt
benchmarks and is disproportionate for this slice's three small additive paragraphs)

Verdict: no blocking findings; one non-blocking note recorded (pointer-wiring deferred to
cutover step 3, by design).

## What changed

Three paragraphs, 23 lines total, added to three existing `skills/director/references/` files
(`lanes-and-pen.md`, `work-kind-table.md`, `guardrails-catalog.md`) — content already
adversarially reviewed twice for fidelity to its build-pipeline source (see
`docs/prover/2026-08-25-batch-2b-slice-1-lane-kind-reach.md`). This review checks the skill-
authoring dimension that review didn't: does the addition read well in place, and does it keep
each reference file within its progressive-disclosure role.

## Findings

No blocking findings.

- `director/SKILL.md`'s own frontmatter and body are untouched by this slice — no re-check of its
  description-triggering or line budget is owed.
- All three touched files stay reference material, not body prose. `lanes-and-pen.md` grew
  55→67 lines, `work-kind-table.md` 18→26, `guardrails-catalog.md` 21→27 — none crosses a size
  threshold that would call for a table of contents or a split. Each addition reads as a
  continuation of its file's existing register (verbatim-quote style in `lanes-and-pen.md`,
  table-preamble prose in `work-kind-table.md`, guardrail-bullet style in
  `guardrails-catalog.md`) rather than a jarring change of voice.
- **Not blocking, noted for the record:** `grep -n "lanes-and-pen\|guardrails-catalog"
  skills/director/SKILL.md` returns nothing — neither file is cited from `skills/director/
  SKILL.md` itself today. Their only live pointer is still `skills/build-pipeline/SKILL.md`'s
  own text (lines 666 and 608 respectively), which cutover step 3 will remove whole.
  `work-kind-table.md` is the one exception: it already has a second live pointer, from
  `skills/live-spec-base/SKILL.md` rule 15. So the honest status is "content now lives in the
  right file, in the right words" — not yet "independently reachable once build-pipeline's body
  is gone." Wiring a director-side (or base-rule-side, matching the work-kind-table precedent)
  pointer for `lanes-and-pen.md` and `guardrails-catalog.md` is left to cutover step 3, the same
  step that removes the pointers this slice's content still rides on — wiring it piecemeal per
  batch-2b item now would mean re-touching `director/SKILL.md` up to 11 separate times instead
  of once, holistically, when the old pointers actually break.
- `scripts/sync-skills.sh` re-run after the edit: installed copies match source, no drift.

Re-verified: `python3 -m pytest -q tests/test_redoor_independence_rebuild.py
tests/test_traceability.py tests/test_guardrails_unit.py` — pass (subset of the full record's
run in the prover record above).
