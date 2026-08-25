# Skill review — director

SKILL-REVIEW

Skill: director

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is disproportionate for two small sentence-level additions) by
an agent independent of whoever wrote the change and independent of the two mechanical
adversarial-review rounds already run over it (recorded separately in
`docs/prover/2026-08-25-director-redesign-gaps.md`).

Verdict: PASS. No blocking findings.

## What changed

Two small additions closing narrow gaps left by director's redesign of an older door/work-kind
classification system into its own acts/dimensions model: an ask-at-intake fallback in
`skills/director/SKILL.md` for split-count ambiguity, and in
`skills/director/references/verify-step-detail.md` a third high-stakes trigger condition
(behaviour-neutral refactor reshaping many files) plus a concrete light-path recipe for
documentation-only changes.

## Findings

1. **Non-blocking — `SKILL.md` addition fits the file's style.** The new sentence (lines 104-106)
   mirrors the file's own established idiom for the same discipline elsewhere ("Ask one short
   question only when guessing wrong would change the result," line 136). Reads as a natural
   continuation, not bolted on. The forward pointer "(see below)" correctly targets "### When the
   act is unclear" (line 131), which does appear later in the same document.

2. **Non-blocking — frontmatter unaffected.** The `description` field already covers Director at
   the act-classification / dimension-naming / execution level; this addition is a refinement
   within that existing scope, not a new capability the description would need to name.

3. **Non-blocking — line budget comfortable.** `SKILL.md` is 328 lines (net +2), well inside this
   pack's SKILL.md range and below the median of larger skills (build-pipeline 728, live-spec-base
   602). `verify-step-detail.md` is 59 lines (was 48), within director's own references/ range.

4. **Non-blocking — third high-stakes condition fits the file's parallel structure.** Extends
   "means one of three things" with a third "Or the change is..." clause matching the first two's
   exact syntax, and correctly routes to the file's own existing generic mechanism rather than
   inventing new terminology — consistent with the fix applied after the first adversarial-review
   round.

5. **Non-blocking — minor antecedent distance.** "That re-check" (line ~28) correctly refers back
   to "the Director's own re-check" two sentences earlier, though the intervening "call a fresh
   checker" sentence names a similar-sounding concept, creating a small parse hiccup on first
   read. Not a substantive ambiguity (the distinct terms disambiguate on a careful read) — worth a
   mental note if this paragraph is touched again, not a fix owed now.

No progressive-disclosure or "unclear when to open me" issues found; both additions stay within
director's own existing vocabulary, as intended (the alternative — porting build-pipeline's old
door-language prose verbatim — was explicitly rejected during design, see
`docs/prover/2026-08-25-director-redesign-gaps.md`).
