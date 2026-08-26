# Skill review — test-author

SKILL-REVIEW

Skill: test-author

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over twelve skills, PLAN.md step 8)

Verdict: clean; one non-blocking observation on frontmatter thinness relative to its siblings.

## What changed

This is not a review of a specific edit. It is the plan-mandated pack-wide skill-creator pass over
every live-spec working skill ahead of PLAN.md step 8 ("Релиз наружу") and its push gate s, which
otherwise reds a substantive skill change with no matching record. `test-author` is reviewed fresh here
as part of that full set.

## Findings

- **Frontmatter description (non-blocking observation).** "Use to derive a test matrix and write tests
  from a proven spec and architecture. Not a substitute for reviewing the spec itself." This correctly
  states WHAT and one clear WHEN-NOT, and is accurate — nothing it claims is unmet by the body. But
  measured against its eleven siblings in this same pass, it is the thinnest description in the set: it
  names no concrete trigger phrasing ("derive the matrix," "pin test levels," "write regression tests
  for X") the way `build-pipeline` or `feedback-intake` do, and it does not name the failure mode the
  body itself opens with — tests passing at the wrong level while the user-visible behavior is still
  wrong. Skill-creator's own guidance is to make a description "a little bit pushy" specifically because
  models under-trigger; a reader skimming only the frontmatter gets the boundary but not the concrete
  hook. Not blocking — the body's own "Work that belongs elsewhere" section covers routing correctly
  ("write tests for X" alone routes to `director` first) — but worth tightening if this skill's
  description is revisited.
- **Anatomy of a Skill** — a single 230-line `SKILL.md`, no `references/` directory. The body is one
  continuous method (deriving the matrix, the level ladder, writing the tests) and reads as
  appropriately self-contained at this length rather than needing offload.
- **Progressive Disclosure** — 230 lines, well under the guideline.
- **Principle of Lack of Surprise** — nothing misleading; the skill is explicit about what it does not
  own ("Not for reviewing documents... Not for the mechanical gates themselves... this skill DERIVES
  what they later enforce").
- **Writing style** — imperative, and grounded in a real, named incident up front (two user-visible bugs
  shipped past ~660 green tests because the facts were pinned at the wrong level) that motivates the
  entire level-ladder method that follows — exactly the "explain why" pattern the guide recommends over
  a bare rule list.
- **Reference-file consistency** — no `references/` directory exists; not applicable. Cross-file paths
  the body cites into `tests/` (`test_traceability.py`, `test_interface_coverage.py`) and `director`
  (`references/build-craft.md`) were spot-checked and exist.
