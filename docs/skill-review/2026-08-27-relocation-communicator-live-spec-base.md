# Skill review — communicator and live-spec-base (relocation, not new content)

SKILL-REVIEW

Skill: communicator, live-spec-base

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings.

## What changed

Both surface laws already reviewed and approved in
`docs/skill-review/2026-08-27-audience-rule-communicator.md` and
`docs/skill-review/2026-08-27-audience-rule-live-spec-base.md` — a rendered page offered rather
than opened unasked, and one item carrying one name across every surface — moved out of
`communicator/SKILL.md`'s "Who is on the other side" section and into `live-spec-base/SKILL.md`'s
rule 36, where they belong: they follow from who the reader is, which is rule 36's own subject, not
from anything specific to the communicator skill. `communicator` keeps a single pointer, folded
into its existing frontmatter-adjacent paragraph rather than a standalone section.

## Why this earned its own review rather than riding the earlier one

`git diff` between the two records shows no wording changed — the two laws' text is
byte-for-byte what the earlier review already read, just under a different heading in a different
file. But `communicator/SKILL.md`'s body length is under a measured ~500-line ideal
(`tests/test_communicator_body_thinned.py`), and the standalone section had pushed it 21 lines
over. This move is the fix for that, not a new idea, and the gate that demands a review for
"communicator changed in a real way" cannot itself tell "moved" from "written," so it earns the
record anyway.

## Checks against the skill-creator guide

- **Frontmatter description.** Unchanged in both files; this move alters nothing about when either
  skill fires.
- **Progressive disclosure.** The content is no shorter or longer, and it sits at the same
  disclosure depth (the body, not a reference file) in its new home. `communicator`'s pointer is
  one clause inside an existing paragraph, which is lighter than the section it replaces.
- **One home.** The laws now live in exactly one file. `grep -rn "richer view is offered\|one item
  carries one name" skills/` returns only `live-spec-base/SKILL.md`'s statement.
- **Size budget.** `wc -l skills/communicator/SKILL.md` returns 499, the file's length before rule
  36 was ever added — checked by command, not assumed from the diff.

Findings: none blocking.

Blocking: none
