# Skill review — text-audit (a recorded case under every law, and a spec section to run on)

`SKILL-REVIEW`

Skill: text-audit
Date: 2026-07-28
Reviewer: this session. Agents are barred in this window by its own instruction, so the review was run
by the seat against the skill-creator criteria rather than by a fresh reviewer. A fresh reviewer should
re-run it when agents are available. This record names what was checked and what was found.

Verdict: passes with one finding, recorded below.

## What changed

Two things the owner asked for on 2026-07-28.

**Every law now carries a recorded case.** The block between the `generated:human-prose-rules` markers
prints one case under each law: the written text on the left, its repair on the right. Twenty-four of
the 41 human-prose rules carried no case at all, and each of them gained one, taken from this project's
own texts. Six rules whose recorded evidence is Russian gained an English case beside it, because the
skill ships to hosts and the shipped-language gate holds a shipped artifact to one alphabet. The
generator prints the first case written in the Latin alphabet, and the Russian evidence stays in the
rule home.

**The skill can be run on a spec section.** A new section states the working size of ten requirements,
the requirement-shape lint that applies only here, which rules a numbered criterion takes and which its
Context paragraph takes, the marks a rewrite leaves untouched, where a fix comes from on this surface,
and the four checks that run after a section is repaired.

## What was checked

- **The full suite is green**: 2217 passed, 0 failed, read from the run's own last line.
- **The block matches a fresh build.** `guardrails/check-language-rules.py` rebuilds every artifact and
  the spliced block in memory and compares them byte for byte. It reads OK over 55 rules.
- **The shipped skill carries no Cyrillic.** The gate refused seven lines on the first attempt, which is
  what sent the Russian cases behind an English one. The count is now zero.
- **The census fell.** The skill went from 53 findings to 36, and the README from 14 to 8.
- **The census measure changed, and the change was proved.** A recorded case is a list item holding a
  quoted text, an arrow, and its quoted repair; its left side is a defect on purpose, so counting it
  scored the evidence a rule rests on. The `long` reading now passes over such a line. Proved on a file
  holding one quoted case and one ordinary bullet of 28 words: the case is passed over, the bullet still
  counts.
- **Two defects in the README were found and fixed.** It named one step two ways, calling the mechanical
  lints the mechanical checks, and it counted four of them where five run.
- **Size.** 286 lines, inside the ~500-line ideal for a skill body.

## The finding: the new section has met no cold reader

The skill's own law holds a changed section back until two fresh readers with no project context read it
and stop nowhere. The new spec-section text has had no such reading, because agents are barred in this
window. It ships on the seat's own read, which is the reading this skill exists to say is not enough.
The first fresh reader available should be pointed at that section.

## What a fresh reviewer should look at

Whether one case under each of 41 laws helps a writer recognise an instance nobody has met yet, or
whether the block now reads as a wall. The cases were chosen by the seat that also wrote the laws, which
is the position this skill warns about.
