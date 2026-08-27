# Skill review — communicator (the audience rules)

SKILL-REVIEW

Skill: communicator

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings.

## What changed

One new section, "Who is on the other side," placed directly above "Work that belongs elsewhere,"
carrying three things: a pointer to `live-spec-base`'s new rule 36 as the one home for who the
reader is, and two standing rules the owner gave on 2026-08-27.

1. **The pointer, not a copy.** The section states no part of rule 36's content. It says where the
   fact lives and what the fact settles for this page. That is the pack's own one-home discipline:
   a second statement of who the reader is would drift from the first within a day.
2. **A rendered page is offered, never imposed.** Where a project has both a plain text list and a
   rendered page of the same thing, the list is the default and the page opens only on request.
   His word, after a session opened a board in his browser unprompted.
3. **One name for one thing, word for word, across every surface.** The same item carries the same
   name in the text list, in a rendered view, and in a reply — no paraphrase, no truncation, no
   re-titling.

## Checks against the skill-creator guide

- **Frontmatter description still accurate.** The description governs when the skill fires. Nothing
  in this change alters what the skill is for or when it triggers; it constrains how its existing
  output is addressed. No description edit is owed, and making one would have been the defect.
- **Progressive disclosure holds.** The section is six short paragraphs in the body, and the fact it
  depends on lives in the base skill, loaded once for every skill in the pack. Nothing new moved
  into a reference file because nothing here is long enough to earn one.
- **Placement.** It sits before "Work that belongs elsewhere" and before the rules themselves, so a
  reader learns who they are writing to before reading a single rule about how to write. Placing it
  after the twenty-two rules would have made every rule read first and be re-interpreted second.
- **Both new rules carry their own source.** Each names the date and the situation that produced it,
  in the body, so a later reader can weigh it rather than obey an unattributed sentence. This
  matches how the pack records the owner's own words elsewhere.
- **Register.** Both rules are stated as what to do, with the reason attached, and neither names a
  file, a script, or a code. That is the register the rules themselves demand.

## Consistency across the pack

`grep -rn "rule 36" skills/` returns this file's pointer and the rule's own home in
`live-spec-base/SKILL.md`. No third statement exists. The base skill's frontmatter rule count was
updated in the same change from twenty-one to twenty-two, and `grep -cE "^[0-9]+\. \*\*"` against
its body returns 22, so the self-count and the body agree. That count has gone stale twice before in
this repo's history, which is why it was checked by command rather than by eye.

Findings: none blocking.

Blocking: none
