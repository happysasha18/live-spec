# Skill review — live-spec-base

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings. This is a real, large edit (fourteen rules retired, the
seat/senior rename, a glossary-entry restructure), and every claim it makes about itself checks out
against the file and the rest of the pack. One non-blocking, pre-existing (not caused by tonight's
work) cross-cutting finding carried forward: four leftover "senior" instances survive outside this
skill's own files.

## What changed

The prior record for this skill, `2026-08-26-live-spec-base-dead-pointer-fix.md` (commit `e9637206`,
02:06), covered an earlier fix and predates tonight's larger edit — `live-spec-base`'s own last change
(`git log -1 -- skills/live-spec-base`) is `3dcf7b82` (22:50), roughly 20 hours later, and
`e9637206` is not an ancestor of it. `git diff origin/main..HEAD -- skills/live-spec-base/` (415 lines)
is far more than the version-stamp exemption covers. The substantive content:

1. **Fourteen more rules retired**: 11, 14, 15, 18, 19, 20, 21, 23, 28, 32, 33, 34, 35 (rule 30 had
   already been cut earlier and stays listed as already-retired). The retirement note names the reason
   — "each covered by neither an eval fixture nor an executable script — a wish, not a rule, per
   PLAN.md step 7" — and the destination, `attic/live-spec-base-unbacked-rules-2026-08-26.md`.
2. **The frontmatter's own rule count** — "thirty-four rules" → "twenty-one rules."
3. **"senior/orchestrator/lead" → "seat"** as the one name the rules use, with the other three now
   recorded only as the source's alternate names in `references/glossary.md`.
4. Rule 14's old cross-reference to itself as "its mechanism inside a code change" is rewritten to
   point at the actual current mechanism, `director`'s class-hunt reference, since rule 14 (the class-
   hunt rule of thinking) is itself one of the fourteen retired numbers and the mechanism it used to
   cite by number needed a description instead.

## Findings

None blocking. Every checkable claim in the diff was checked, not assumed:

- **Rule count, verified by counting, not trusted from the frontmatter.**
  `grep -oE "^[0-9]+\." skills/live-spec-base/SKILL.md` returns exactly 21 numbered rules
  (1–10, 12, 13, 16, 17, 22, 24–27, 29, 31 — the fourteen listed as retired plus the already-open 30
  are the only gaps), matching the frontmatter's "twenty-one rules in the body" exactly.
- **The attic file exists and is committed** — `attic/live-spec-base-unbacked-rules-2026-08-26.md`
  is on disk (16 KB) and its rule 18 entry, checked directly, reads "One name-collision law" —
  confirming the citation removed from `communicator` in this same push pointed at the right rule.
- **No dangling references to a retired rule number anywhere under `skills/`** — checked all fourteen
  numbers with `grep -rn "rule <N>\b" skills/` (word-boundary, so "rule 14" does not false-match "rule
  140"): zero hits for any of them. The rename sweep that removed these citations (in `communicator`,
  `build-pipeline`, and `director`, each reviewed separately in this session) reached every citation
  under `skills/`.
- **The seat rename is internally consistent inside this file** — `grep -n "senior" skills/live-spec-
  base/SKILL.md` after the change: one hit, at line 220 ("Opening a prototype home is a repo write
  that belongs to the assigned senior alone"), and `git blame` dates that line to 2026-07-09 — it
  predates tonight's rename entirely and was not touched by this diff, so it is not a regression this
  commit introduced. Non-blocking, but real: it is the same pre-existing usage as `references/
  settings-ladder.md:52` ("senior may override, logged," blamed 2026-08-14) and the two instances in
  `director/references/delegation-protocol.md` (flagged separately in this session's `director`
  review). All four are the same class — the rename swept the rule text itself but not every older
  prose mention of the role by its old name across the pack. Worth a follow-up sweep; does not block
  this push, since none of the four sits inside content this push actually touched.
- **Frontmatter description / Anatomy of a Skill / Progressive Disclosure** — the body is 415 lines,
  still under the ~500-line guideline; the three on-demand reference modules
  (`references/glossary.md`, `references/worked-examples.md`, `references/settings-ladder.md`) are
  still the only ones the frontmatter promises, and all three still exist and are pointed at from the
  body at the place each is needed.
