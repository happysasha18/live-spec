# Skill review — communicator, spec-author

SKILL-REVIEW

Skill: communicator
Skill: spec-author

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is disproportionate for two small additive sections and a
rule-count propagation)

Verdict: no blocking findings.

## What changed

`skills/communicator/references/writing-register.md` gained a genuinely new rule (rule 18,
CHANGELOG-vs-journal), with the file's own stated rule count moving 17→18, propagated to the
three other places that cite that count (`communicator/SKILL.md` twice, `communicator/
references/words.md` once) and to the one test asserting the literal string
(`tests/test_measurement_law_homes.py`). `skills/spec-author/SKILL.md` gained one new section
("Removing a shipped feature is a change too"), narrowed to the residual not already covered by
`live-spec-base` rule 10. `matrix/build-pipeline.md`'s M-101 row gained a "one home" pointer.

Two other candidates from the same batch (INV-70, INV-114) were drafted, then reverted after
independent review found both laws already fully homed in `PRODUCT_SPEC.md` itself (pinned by
`tests/test_traceability.py::test_parameter_default` and `tests/test_restructure_merge_gate.py`
respectively) — the original 11-item batch-2b classification had checked skill prose for
duplication but not the formal spec document, which is where the real normative home already
was for these two. No content from either survives in this commit.

## Findings

No blocking findings.

- `writing-register.md`'s rule numbering (1-18) is complete and sequential with no gaps or
  duplicates after the addition — checked independently by the adversarial reviewer, not just
  by the author.
- The new rule 18 sits under `## Voice`, which is a reasonable thematic fit (who a document
  speaks to — the end user vs. the builder) even though the file's numbering is historically
  non-sequential-by-position (rule 13 sits before rule 9 elsewhere in the same file, from an
  earlier addition) — this is the file's own established pattern, not a new inconsistency.
  `writing-register.md` grew 155→160 lines; `spec-author/SKILL.md` grew 270→276 lines — neither
  crosses a size threshold calling for restructuring.
- Two independent adversarial rounds (the implementing worker's own re-verification after the
  correction, and a separate reviewer agent that re-derived the base-rule-10 citation and the
  redundancy checks from scratch rather than trusting the correction's own account) confirm the
  kept content is non-redundant and the reverted content left no trace (`grep -n -i -E
  "INV-70|INV-114|tunable parameter|restructure/migration merge gate"` on both touched files:
  zero hits).
- `matrix/build-pipeline.md`'s M-101 edit converts an existing parenthetical aside into an
  em-dash clause to make room for the new "one home" pointer, rather than M-085's simpler pure
  insertion (M-085 had no pre-existing parenthetical to work around) — a minor stylistic
  divergence from the precedent it matches in spirit, noted by the adversarial reviewer as not
  worth blocking on since the row stays grammatical and loses no content.
- `scripts/sync-skills.sh` re-run after the edit: installed copies match source, no drift.

Re-verified independently (not just by the author): `python3 -m pytest -q
tests/test_measurement_law_homes.py tests/test_traceability.py
tests/test_communicator_register_extracted.py tests/test_communicator_body_thinned.py
tests/test_gate_common_table_rows.py tests/test_restructure_merge_gate.py` — 208 passed, 3
skipped (external product-prover canon clone absent locally — expected), 0 failed.
`scripts/spec-style-lint.py --tier universal` on all 5 non-test touched files: 0 errors
introduced (the 2 pre-existing errors and 1 pre-existing warning in `matrix/build-pipeline.md`,
rows M-313/M-275, predate this change — confirmed against `git show HEAD~1`).
