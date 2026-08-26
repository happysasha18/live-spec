# Skill review — spec-author

SKILL-REVIEW

Skill: spec-author

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for this gate-close pass)

Verdict: PASS — no blocking findings. The one change since the last record (`2026-08-26-spec-author.md`,
commit `c73d87cd`) is a version-stamp bump plus the same stale-URL fix that record already made,
carried through a later merge commit that re-touched the file on the path but changed nothing further.

## What changed

Push gate s (SPEC INV-208) requires the record covering a skill's last change to be an ancestor-or-equal
of that change, not merely chronologically later. `spec-author`'s last commit that touched the file
under `git log -1 -- skills/spec-author` is `02e70190` (a merge, 2026-08-26 23:15), and the existing
record's own commit `c73d87cd` (22:55) is an ancestor of `02e70190`, not equal to or descending from it
— so the gate correctly calls the record stale even though nothing further actually changed. Diffing
`origin/main..HEAD -- skills/spec-author/` confirms the total content delta is exactly two lines: the
`version: 5.0.0` → `6.0.0` frontmatter stamp (exempt by the gate's own carve-out) and the
`product-prover` cross-link, corrected from the dead in-repo path
(`https://github.com/happysasha18/live-spec/tree/main/skills/product-prover`) to the live external repo
(`https://github.com/happysasha18/product-prover`) — the exact fix `2026-08-26-spec-author.md` already
made and explained. `git show 02e70190 -- skills/spec-author/` (a merge of two branches, one carrying
the VERSION 6.0.0 chapter, the other the gate-h/gate-a work) is TREESAME to neither parent for this
path only because it resolves the two branches' independent version-line edits — it carries no new
prose. This record exists only to give the gate a record whose own commit lands after `02e70190`.

## Findings

None blocking, nothing new to fix. Reconfirmed against the same checklist the prior pass used:

- **Frontmatter description** — unchanged, still states WHAT (start/grow/sync a spec) and draws the two
  negative boundaries (setup belongs to `build-pipeline`; retro-docs and spec-less prototypes stay
  outside) precisely.
- **Anatomy of a Skill / Progressive Disclosure** — unchanged: 276-line body, nine reference files, all
  reachable from the body (re-verified by grepping each filename against `SKILL.md` — still no orphans).
- **The `product-prover` link** — now reads `https://github.com/happysasha18/product-prover` at
  `SKILL.md:21`, matching the two correct links already in this skill's own `README.md`. Resolves live.
- **Lack of Surprise / writing style** — no lines changed here since the prior pass; both still hold.
