# Skill review — product-prover-pack

SKILL-REVIEW

Skill: product-prover-pack

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over twelve skills, PLAN.md step 8)

Verdict: clean — no blocking findings.

## What changed

This is not a review of a specific edit. It is the plan-mandated pack-wide skill-creator pass over
every live-spec working skill ahead of PLAN.md step 8 ("Релиз наружу") and its push gate s, which
otherwise reds a substantive skill change with no matching record. `product-prover-pack` is reviewed
fresh here as part of that full set — as its own working skill, on its own merits: the pin map, the
pack paths a review reads, the record shape the push gate checks, and the mode names, not the external
`product-prover` skill's own review logic, which sits outside this pack's `skills/` directory and is
out of this review's scope.

## Findings

None blocking. Checked against the skill-creator checklist:

- **Frontmatter description** — unusually precise about what this skill is not: "It carries what the
  prover body no longer does... It reviews nothing itself." That negative framing is exactly right for
  a binding/adapter skill, and it heads off the natural mistriggering (someone loading this expecting a
  review to run). Matches the body precisely: every section is a table (mode names, pack paths, pin map)
  or a procedural note (the record shape, version discipline), never a review step.
- **Anatomy of a Skill** — a single 120-line `SKILL.md`, no `references/` directory. Appropriate: the
  content is entirely reference tables meant to be read inline, not offloaded material.
- **Progressive Disclosure** — 120 lines, well under the guideline.
- **Principle of Lack of Surprise** — nothing misleading. The `requires: product-prover >= 1.3.0` line
  in the frontmatter states the external dependency plainly, and "Version discipline" explains the
  installer's minimum-version refusal and that the installed copy is untracked — a reader is not
  surprised by where the real prover logic lives or how it gets there.
- **Writing style** — imperative, and the pin map's own framing explains its own maintenance contract
  well ("When a lens moves or renames in a prover release, this table is the one place the pack
  updates") — a good instance of stating why a table exists, not just listing it.
- **Reference-file consistency** — no `references/` directory exists; not applicable. Cross-file paths
  the body cites into the rest of the pack (`skills/build-pipeline/references/minor-bump-gate.md`,
  `skills/test-author/SKILL.md`, `skills/live-spec-base/SKILL.md`) were spot-checked and resolve.
