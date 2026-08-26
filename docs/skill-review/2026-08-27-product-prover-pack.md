# Skill review — product-prover-pack

SKILL-REVIEW

Skill: product-prover-pack

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings. Real content addition (a new mode, a new section) checked
against the external prover skill it binds to and against `director`'s matching reference; both
consistent.

## What changed

`product-prover-pack`'s last change is `c9ca711a` ("Wire the prover's code mode into director and the
pack adapter"). Its own 2026-08-26 review (`docs/skill-review/2026-08-26-product-prover-pack.md`,
commit `c73d87cd`) predates it. `git diff origin/main..HEAD -- skills/product-prover-pack/` (44 lines):

1. **`requires: product-prover >= 1.3.0` → `>= 1.4.0`**, alongside the version stamp.
2. **A new row in the mode-names table**: `CODE-REVIEW` → `Code mode`.
3. **A new "## Code mode" section**: three of the prover's lenses — class-based defect analysis,
   closed-set completeness, sibling-defect search — transfer to reading code directly with no document
   as input. States what does NOT transfer (cross-cutting laws, lifecycle sweeps, provisional defaults,
   three-source disagreement — each needs a stated intent to check against, which code alone does not
   carry), and that a code-mode finding is pinned `file:line` rather than to a `PRODUCT_SPEC.md`
   requirement, so the pin map further down the page does not apply to it.

## Findings

None blocking. Checked against both the source this page binds to and the page's own consumer:

- **The version requirement is real, not aspirational** — the vendored `skills/product-prover/
  SKILL.md` at `~/live-spec/skills/product-prover/` is stamped `version: 1.4.0`, and
  `skills/product-prover/reference/code-lenses.md` (the file this page's Code mode section cites as
  carrying "the full procedure") exists at that path. The `>= 1.4.0` bump is not a guess.
- **Cross-file consistency with `director`** — `skills/director/SKILL.md`'s specialist table now reads
  "a mistake in the statement of the problem would be expensive, or shipped code needs a class-based
  defect hunt with no document to check it against" for the Product prover row (reviewed separately in
  this session). This page's own wording — "Director calls this when shipped code needs the same
  defect hunt a spec review runs, and no document governs the surface being checked" — describes the
  same trigger from the other side. Neither file overclaims what the other promises.
- **The exclusion list is itself checked, not just asserted** — the four excluded capabilities
  (cross-cutting laws, lifecycle sweeps, provisional defaults, three-source disagreement) are named
  elsewhere in the pack as duties that read a spec's stated intent, which code alone cannot supply;
  the boundary is a real distinction from the three included lenses, not an arbitrary split.
- **The pin map correctly stays silent on code mode** — checked the "pin map" section further down the
  page: it maps `PRODUCT_SPEC.md` requirement codes to lenses, and code-mode findings are `file:line`-
  pinned instead, so the section's silence on `CODE-REVIEW` is a correct omission, not a gap.
- **Frontmatter / Progressive Disclosure** — the description's own last sentence, "It reviews nothing
  itself," still holds: the new section documents what the external skill does, adding no review logic
  of this page's own. Body length and structure are otherwise unaffected.
