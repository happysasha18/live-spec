# Skill review — one heading renamed in every skill

`SKILL-REVIEW`

Skills: build-pipeline, communicator, design-reviewer, feedback-collector, feedback-intake,
live-spec-base, product-prover, publish, spec-author, test-author, text-audit.
Date: 2026-07-28
Reviewer: this session, against the skill-creator criteria. One record covers the eleven skills,
because one change reached all of them and each file took the same single edit.

Verdict: passes. No finding.

## What changed

Every skill states where its work stops and another skill's begins. That section carried a word in
capitals for emphasis, which this project's writing rules refuse, and it carried four different
wordings across the eleven files:

- `## When NOT to use` — product-prover, design-reviewer, text-audit, communicator, publish;
- `## When NOT to use it` — test-author;
- `## When NOT to fire` — feedback-collector, feedback-intake, design-reviewer;
- `## When NOT to run it` — build-pipeline;
- `## When NOT to load this` — live-spec-base;
- `## When not to use` — spec-author.

Every one of them now reads `## Work that belongs elsewhere`. The section bodies are untouched, and
the sentences that referred to the section by its old name moved with it.

## What was checked

- **The full suite is green**: 2217 passed, 0 failed, read from the run's own last line.
- **No section body changed.** The diff on each skill is the heading line, plus a by-name reference
  inside product-prover.
- **The gate that reads this section moved with it.** `guardrails/check-skill-loadability.sh`
  searched every skill for the literal `when NOT to`, so the rename would have turned the push red
  for every renamed skill. The gate now searches for the new heading, and its test and its matrix row
  (M-081) carry the same wording. The gate reads OK over 11 skills.
- **One name for one thing.** Four wordings became one, so a reader meeting a second skill finds the
  section where the first one taught them to look.
- **The counters fell.** The heading was the last finding standing between two of these skills and
  zero: `skills/product-prover/SKILL.md` and `skills/product-prover/README.md` now measure zero.

## What a fresh reviewer should look at

Whether `Work that belongs elsewhere` reads right over a section that states when a skill stays
silent, rather than where its work goes. Two skills are that shape: feedback-collector and
feedback-intake both head a list of occasions they refuse to fire. The wording was chosen for one
name across eleven files, and a better single wording is worth a second opinion.
