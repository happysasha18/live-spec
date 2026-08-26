# Skill review — architect

SKILL-REVIEW

Skill: architect

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over 12 skills)

Verdict: clean; no findings that block

## What changed

This is not a review of one edit — it is the plan-mandated pack-wide skill-creator pass over every
working skill (PLAN.md step 8, "Релиз наружу"), read fresh here for `architect`.

## Findings

- **Frontmatter description** — states both what (writes/updates ARCHITECTURE.md from a proven
  spec: node structure, pins, budgets, runtime/placement views, fitness test) and when ("here's a
  proven spec, produce or update the architecture" is a complete task; also names it as a step
  Director calls). Not vague, appropriately concrete, matches the body's actual scope — no
  overpromise found.
- **Anatomy of a Skill** — SKILL.md (202 lines) plus one reference file
  (`references/architecture-step-detail.md`, 36 lines) used exactly as Progressive Disclosure
  intends: the body carries the load-bearing rules, the reference carries the "words the step first
  used" verbatim passages the body points to four separate times. No missing bundled resource —
  this skill produces prose (a markdown document), not code, so no scripts/ of its own is expected;
  it correctly points to the *host project's* `scripts/build-architecture-reference.py` and
  `guardrails/check-architecture-reference.py` rather than bundling copies.
- **Progressive Disclosure** — 202 lines, well under 500; no hierarchy pressure. The one reference
  file is 36 lines, well under the 300-line table-of-contents threshold.
- **Principle of Lack of Surprise** — nothing misleading; the skill is explicit about its own
  boundaries ("Work that belongs elsewhere") and doesn't claim to judge its own output (that's
  `product-prover`) or derive the test matrix (that's `test-author`).
- **Writing style** — imperative and explanatory throughout; each rule states its *why* (e.g. "the
  spec is fixed to the shipped truth, always in that one direction, never the reverse" gives the
  reason before the rule). No bare ALL-CAPS MUST/NEVER walls.
- **Reference-file consistency** — the one reference file
  (`references/architecture-step-detail.md`) is linked correctly four times with matching relative
  paths; `grep -rn "architecture-step-detail"` confirms the file exists and every mention resolves.
  No orphan files under `skills/architect/references/` — the directory holds exactly the one file
  the body cites.

No structural or content defect found. The closing pack roster line matches the twelve-skill roster
in `skills/live-spec-base/SKILL.md` byte-for-byte in substance (same names, same one-line duties).
