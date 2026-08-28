# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-08-28
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: the change is sound and correctly placed, after one repair the review itself made. The
sentence it added was true but had grown into an account of how the tool works; it now says the one
thing the reader has to do differently and lets the tool's own output say the rest.

## What changed

`git diff 7159fed6..HEAD -- skills/communicator/SKILL.md`. One bullet, item 5 of the pre-show
checks, the legibility floor. Two commits touched it in this range and both edit the same sentence:
`c62fef2`'s lane added the reach note when the lint gained its stand-down line, and `c7c4ab68`
corrected that note after the lint's gradient reading changed. Nothing else in the file moved: no
other rule, no frontmatter, no version bump.

## Findings

**1. The bullet had grown into tool documentation, and it is repaired here.** As written it ran to
1,279 characters, against 761 for the bullet below it and 255 for the one above — the longest in the
file's checklist by a wide margin. What it spent that length on was the lint's internals: which
surfaces it cannot measure (an image, a see-through surface, a gradient), and what it does at each
end of a gradient. A reader of this skill needs one instruction — read the verdict line, not only
the exit code — and the lint's own output already names the pairs it stood down on, in the words of
the work, at the moment they matter. Progressive disclosure says the detail belongs where the tool
speaks, not in the checklist a session reads every time. Trimmed to 966 characters, with the
instruction kept and the mechanism dropped.

**2. The instruction the sentence adds is real and was missing.** This is not decoration. The lint's
exit code stopped being the whole verdict when it gained a partial stand-down, so a session reading
only the exit code would show a page carrying pairs nobody has looked at — the precise defect the
lint's own change was made to end. A checklist item that says "a red blocks the showing" and nothing
else teaches a reader to watch one number. The added clause is the smallest correction to that, and
it belongs in this file rather than in the lint, because it governs what the person does next.

**3. The frontmatter description still describes the skill.** Nothing in this change alters when the
skill fires or what it is for, so the description needs no edit; checked against it rather than
assumed.

**4. The file's size ideal holds.** 499 lines, at the ideal `tests/test_communicator_body_thinned.py`
guards; that test passes (5 passed, run directly). The repair above is what keeps it there — the
bullet as first written pushed the file's weight up for no gain to a reader.

**5. The overlap finding carried open from 2026-08-27 is untouched and still stands.** Rule 7's
first nested bullet still overlaps the "honestly / no sugar-coating" bullet above it. Neither commit
in this range goes near it, and it is not closed on the back of an unrelated edit.

Blocking: none.
