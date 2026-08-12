# Skill review — communicator (the base rulebook's count follows the cut)

SKILL-REVIEW

Skill: communicator

Date: 2026-08-12
Reviewer: skill-creator (Anthropic), run by a fresh reviewer with clean context. It did not author
the edit, and it wrote no file but this record.

Verdict: passes as a skill, and owes no repair of its own. The two edited sentences are the only
change, the description is untouched and still describes the body, every count this skill states about
itself and about the rulebook re-derives correctly, and no reference to the cut rule ever stood here.
One recommendation is carried for the pack, not for this file.

## What changed

Commit `3866a6c` changed one word in two sentences. The preamble of `skills/communicator/SKILL.md`
and the base-rules paragraph of `references/words.md` each said the base rulebook carries thirty-five
numbered rules; both now say thirty-four. No rule of this skill was touched, and the file's byte count
is unchanged, since the two number words are the same length.

## Findings

1. **The list of base rules this skill cites still matches the body.** Reviewed and clear.
   `references/words.md` names eight: 1 ask never guess, 2 plain words carry the meaning, 4 one
   canonical home per fact, 6 the checkpoint, 10 nothing silently deleted, 13 a claim needs its
   primary source, 16 a prototype stays a sketch, and 18 the name-collision law. A grep of the body
   returns exactly those eight and nothing above 18, so the cut rule was never cited here and the
   surviving citations all point at rules the rulebook still carries at their stated numbers.

2. **The skill's own counts hold.** Reviewed and clear, and re-derived rather than trusted. The body
   carries 22 inline rule tags numbering 1 to 22, which is the twenty-two `references/words.md`
   claims. The register's own tags in `references/writing-register.md` number 1 to 17, which is the
   seventeen claimed. The ten numbered heads in that file are its closing checklist, a separate list,
   which is what the words page says when it warns that two numbering systems share one tag form.

3. **The stated count of the rulebook's rules is a copy no machine reads.** Recommended for the pack.
   Two of the four homes of that number are in this skill, and a grep of `tests/` and `guardrails/`
   finds assertions only on the base's own frontmatter phrase. Both copies here are free to drift on
   the next rule change. Base rule 4 asks a restated fact to become a pointer, and both sentences
   already point at the rulebook by path; dropping the number from them would cost the reader nothing.

4. **The count carries the hole with it.** Named, and its repair belongs to the base. Thirty-four is
   the tally of rules present, while the rulebook numbers them 1 to 35 with 30 retired. This skill
   cites nothing above rule 18, so no reader of this page meets the gap. A reader who follows the
   pointer into the rulebook does, and the repair recommended in the live-spec-base record of the same
   date closes it for every page that points there.

5. **No dangling reference to the cut rule.** Reviewed and clear. A grep across `SKILL.md`, `README.md`
   and the four files under `references/` for the cut rule's number, for thirty-five, for INV-164 and
   for the generator wording returns nothing.

## The measures this review was held to

The census reads `skills/communicator/SKILL.md` at 175 findings and `references/words.md` at 4, each
unchanged from before the edit, with no register findings in either. Both files measure the same byte
count as before. The loadability gate passes. The installed copy at `~/.claude/skills/communicator` is
byte-identical to the repository copy.
