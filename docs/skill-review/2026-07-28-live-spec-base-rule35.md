# Skill review — live-spec-base (rule 35, the session's record read at both ends)

`SKILL-REVIEW`

Skill: live-spec-base
Date: 2026-07-28
Reviewer: skill-creator (Anthropic), run in a clean context with no part of the authoring session

Verdict: passes with findings — one folded, one rejected with its reason, one pre-existing and left,
one reviewed and left. The review wrote no file and edited none; the fold below was made by the
authoring session after reading the findings.

## What changed

The body gained rule 35 at `skills/live-spec-base/SKILL.md:482`, the thirty-fifth numbered rule: a
session's record is read at both ends by an agent that did not live it. The rule names the session
extract that `scripts/session-extract.py` writes, the closing step where a fresh agent writes the
session handover from that extract, the three provenance lines a handover carries, the mechanical arm
`guardrails/check-handover-provenance.py`, and the opening step where a fresh agent lists the
decisions the person made and compares them against `DECISIONS.md` and `NEXT_STEPS.md`. The
frontmatter description moved from "thirty-four rules in the body" to "thirty-five".

## Findings

1. **The rule names its referent "the person" while the file's dominant term is "the human"** —
   rejected, with the reason. The file already carries all three terms today: "the human" 36 times,
   "the owner" 13, "the person" 5. So rule 35 introduces no third name. The new law lives in two
   homes, this rule and Requirement 303, and the specification's criteria say "the person". Holding
   one wording across both homes serves a reader crossing them better than matching this file's
   in-house majority. The dated closing sentence uses "the owner", which is what rules 32 and 34
   already do.

2. **A doubled blank line stands before `## Work that belongs elsewhere`** — pre-existing, left
   alone. The two blank lines were in the file before this change; the edit inserted the rule above
   them and moved nothing. Repairing a shared file's whitespace while two other workers hold it buys
   nothing and costs a diff.

3. **The closing paragraph echoes rule 33's argument with no pointer to it** — folded. Rules 29 and
   34 name their kin by number when they reuse a pattern, and this one did not. One sentence was
   added: "Rule 33 draws the same line for a release's clean-context review."

4. **The bold title says "read" where the closing half is about authorship** — reviewed and left.
   The title is literally right, since the extract is what gets read at both ends, and the rule's
   second sentence about the close says plainly who writes the handover.

## The measures this fold was held to

The census reads this file at 229 findings, its recorded count, before the change and after it: 141
sentences past the word cap and 88 style findings, both unmoved. Two words written in capitals were
caught by that measure during the work and lowered before the rule landed.
