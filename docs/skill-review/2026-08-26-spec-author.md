# Skill review — spec-author

SKILL-REVIEW

Skill: spec-author

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over twelve skills, PLAN.md step 8)

Verdict: one non-blocking finding, fixed in this review — a stale cross-repo link; everything
else checked clean.

## What changed

This is not a review of a specific edit. It is the plan-mandated pack-wide skill-creator pass over
every live-spec working skill ahead of PLAN.md step 8 ("Релиз наружу") and its push gate s, which
otherwise reds a substantive skill change with no matching record. `spec-author` is reviewed fresh here
as part of that full set.

## Findings

None blocking. Checked against the skill-creator checklist:

- **Frontmatter description** — states what (start a new spec, add a feature, keep a spec in sync) and
  draws two precise negative boundaries in the same sentence: setup lives earlier at `build-pipeline`'s
  entry, and retro-documentation / a spec-less prototype sketch stay outside. That is a strong,
  accurate WHAT+WHEN+WHEN-NOT description, matching the body's own "Work that belongs elsewhere."
- **Anatomy of a Skill** — this is the heaviest-disclosure skill of the twelve: a 276-line `SKILL.md`
  plus nine reference files (`glossary.md`, `how-it-reads.md`, `the-spine.md`, `composition-sweep.md`,
  `facet-sweep.md`, `primary-unit.md`, `change-record.md`, `completeness-pass.md`, `anti-patterns.md`).
  Every one of the nine is named from the body at exactly the point a reader needs it — checked by
  grepping each filename against the body; none are orphaned. This is the pattern the guide recommends
  for a skill this large: keep the body as a walked procedure and push each substantial sub-topic (the
  spine, the facet list, the primary-unit table, the anti-pattern list) into its own file with a clear
  pointer left behind.
- **Progressive Disclosure** — 276 lines in the body itself, comfortably under the ~500-line guideline
  even before counting the nine offloaded reference files — the disclosure structure is doing real work
  here, not just present nominally.
- **Principle of Lack of Surprise** — nothing misleading; the pairing table with `product-prover` at the
  close states the division of labor precisely (writes & grows vs. reviews), and the "Work that belongs
  elsewhere" section is explicit about what this skill refuses (retro-documentation, prototypes,
  single-file skip-boundary edits).
- **Writing style** — imperative throughout, and the "one rule" callout near the top ("If a situation
  the system can reach isn't in the spec, the spec is incomplete, even if the code 'works'") is a strong
  instance of grounding the whole skill in one memorable why before the mechanics start.
- **Reference-file consistency** — all nine files confirmed linked from the body; no dead local
  links, no orphans found. One dead *external* link: `SKILL.md:21` pointed `product-prover` at
  `https://github.com/happysasha18/live-spec/tree/main/skills/product-prover`, a path that no
  longer resolves now that `product-prover` was extracted to its own repository (this same skill's
  own `README.md` already correctly links `https://github.com/happysasha18/product-prover` twice).
  Fixed directly in this review — a one-line, mechanical stale-path correction, no other prose
  touched.
