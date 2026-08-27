# Skill review — communicator

SKILL-REVIEW

Skill: communicator

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: the two changes are sound in substance and correctly placed — nothing here contradicts
existing rules or the skill's own conventions. Two real problems found and NOT folded in this
pass: the file now sits 16 lines over its own documented ~500-line ideal, and the new sub-rule
partly overlaps a bullet immediately above it. See Findings.

## What changed

`git diff cf4366d2..HEAD -- skills/communicator/` (this record supersedes
`2026-08-27-communicator.md`, stale against the skill's last change, `1eced2b6`). Two things,
both under rule 7 and rule 9:

1. **Rule 9's mark legend replaced by a pointer.** The bulleted status-map rule used to restate
   its own six-mark legend (✅ 🔄 ⏳ ⚠️ ⏱ 📖) inline. It now points at
   `~/.claude/playbook/CLAUDE.md`, section "How a reply to him looks," naming that as the one
   canonical home, per a 2026-08-27 review that found the mark vocabulary living in three homes
   with three different mark sets — the standing cause of a complaint made nine times.
2. **A new sub-rule under rule 7** (landed in two steps, `d4a2aa09` then expanded by `1eced2b6`):
   "A fact is stated, never announced, and never staged," with four nested bullets — no
   introduction-only sentences, no manufactured tension/drama, the finding leads and the reader
   judges how it lands, and the voice named as a professional running a technical project for the
   client paying for it. His own words, twice in one session, are quoted for both the ban and the
   voice framing.

## Findings

**Rule 9's pointer — checked, holds.** `~/.claude/playbook/CLAUDE.md:23` carries the section "How
a reply to him looks" and it does state a five-mark legend (✅ 🔄 ⬜ ⛔ 👁️) — confirmed by reading
the file directly, not assumed from the commit message. The pointer is honest: the old inline
legend (six marks) and the canonical home's legend (five marks) actually disagree, which is the
exact drift the change exists to stop by converging on one. Net length effect: roughly neutral
(one long line replaced by another of similar length) — this change contributes nothing to the
line-budget finding below.

**Real problem 1 — the file is now over its own budget.** `origin/main`'s `skills/communicator/SKILL.md`
was 499 lines; `HEAD`'s is 516 (`git show cf4366d2:… | wc -l` vs `git show HEAD:… | wc -l`), 16
over the ~500-line ideal `tests/test_communicator_body_thinned.py` holds (row 280, "Keep SKILL.md
under 500 lines" — the owner's own number, not this review's). The growth is almost entirely the
new rule-7 sub-rule: four nested bullets, each with its own bold lead and its own quoted evidence,
where the content could stand as one tighter bullet at the same nesting level as its neighbors.
Not folded here: rewriting the skill body risks colliding with a concurrent, uncommitted edit to
this exact file already in progress in a different session at review time (confirmed live via
`git diff --stat -- skills/communicator/SKILL.md` showing local, uncommitted changes to the same
paragraph this finding is about) — a second hand editing the same lines right now would land one
of the two edits silently on top of the other. Left as a named, unclosed finding rather than
raced.

**Real problem 2 — partial overlap with the bullet directly above it.** Rule 7 already opens with
"Don't sell a micro-fix as a breakthrough; drop the 'honestly / no sugar-coating' preambles and let
the result speak." That is the same defect family as the new sub-rule's first bullet ("no sentence
whose only job is to introduce the next sentence, and no label on a fact before the reader has
it") — both ban pre-framing a finding before the reader gets it. They are not identical (the new
bullet adds the specific banned phrases in Russian and English, which the old one doesn't carry),
so this is not a pure duplicate, but the two could read as one rule instead of two adjacent ones
making a similar point from different angles. A tighter edit would fold the "honestly" preamble
ban into the new sub-rule's first bullet rather than keeping both as separate entries under rule 7.

**Not a finding, checked and ruled out:** the fourth sub-bullet ("the voice is a professional
running a technical project for a client") reads at first as a persona/register statement that
might belong in `references/writing-register.md` (the skill's own home for voice rules,
cross-referenced twice elsewhere in this same file) rather than nested under rule 7's
result-honesty framing. Read in context, though, it is scoped narrowly to how a *finding* is
framed, not the whole writing register, so keeping it beside the sub-rule it qualifies is
defensible; this is a placement call within a fair range of taste rather than a defect.

**Frontmatter / Progressive Disclosure / Anatomy** — unaffected by these two changes; both stay
inside the existing rule 7 / rule 9 bullets, add no new file, and change no frontmatter line.
