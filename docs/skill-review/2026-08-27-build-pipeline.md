# Skill review — build-pipeline

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings. Two small wording fixes beyond the version stamp, both checked
for consistency with the rest of the pack; both hold.

## What changed

`git diff origin/main..HEAD -- skills/build-pipeline/` is not stamp-only, so the gate's version-bump
exemption does not cover it — it correctly demands this record. The non-stamp lines:

1. **`SKILL.md`** — the craft-ladder line naming who judges each step swaps "Commit & show is judged
   as a careful release **hand**" for "a careful release **manager**". This continues the same
   metaphor pattern the sentence already used for the other steps ("a senior developer" for code, "a
   QA automation lead" for the matrix, "the same QA engineer" for the test) — a professional-role
   stand-in for the judging eye, now applied consistently at Commit & show too. Checked
   `grep -rn "release hand\|release manager" skills/` — one occurrence, no orphaned reference to the
   old wording anywhere else in the pack.
2. **`references/minor-bump-gate.md`** — "opens the duplication's own compaction row at that moment
   (rule 19's owner)" loses the `rule 19's owner` parenthetical (rule 19 — the problem ledger — was
   one of the fourteen rules `live-spec-base` retired tonight) and gains "(the problem ledger's own
   owner)" in its place: a description that survives the retirement instead of a citation that would
   have gone stale. `grep -rn "rule 19" skills/` after this change: no hits — clean.

## Findings

None blocking. Checked against the skill-creator checklist:

- **Frontmatter description / Progressive Disclosure** — unchanged from the prior pass
  (`2026-08-26-build-pipeline.md`, whose one non-blocking finding — the description omits the
  craft-ladder section — is unaffected by tonight's two wording fixes and remains open, not
  reintroduced or worsened here).
- **Reference consistency** — both fixes remove a citation to a rule number that no longer exists
  rather than leaving one dangling; `references/minor-bump-gate.md` in particular now reads cleanly
  without the reader needing to chase a retired rule number.
- **Lack of Surprise** — neither change is misleading; both are same-register polish.
