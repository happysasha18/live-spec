# Skill review — communicator (the page-clearing clause and the compacted tail)

`SKILL-REVIEW`

Skill: communicator
Date: 2026-07-27
Reviewer: skill-creator (Anthropic)

Verdict: passes, with one change folded — the pointer at the new reference page now says when to open
it. The frontmatter description, the rule placement, and the body/reference split all read clean.

## What changed

Rule 5 gained a closing sub-bullet: a rendered page is cleared once its reading is over (SPEC INV-286),
with the walk carried in the new normative reference `references/page-lifecycle.md`. The tail section
"Worked examples, forks, and anti-patterns" was compacted, and its three anti-patterns moved into
`references/field-examples.md` under a heading of their own.

## Findings

**F1 — folded. The pointer at the new reference page gave the reader no moment to open it.** The
sub-bullet closed with a bare link. Both other references in this body carry a load cue: the register
section says to load its file before drafting human-facing prose, and the intro says the examples file
loads on demand. A normative page reached by a bare link gets read by whoever happens to be curious.
The line now reads "Read the walk in `references/page-lifecycle.md` before clearing a page." The body
stays at 498 lines, and `tests/test_communicator_body_thinned.py` and `tests/test_rendered_sweep.py`
are both green after the edit.

**F2 — reviewed, no change. The clause sits under the right rule.** Rule 5 governs where a page is put
so the person actually meets it. The end of that same page's life belongs beside it. The clause landed
inside an existing rule, so the body's count of twenty-two rules stays true and no numbering moved.

**F3 — reviewed, no change. The relocation of the anti-patterns is whole.** All three lines arrived in
`references/field-examples.md` with their rule tags intact, so each anti-pattern still names the rule
it serves. The body's tail is now a pointer paragraph naming what waits in the reference file. Nothing
was cut.

**F4 — reviewed, no change. The frontmatter description still triggers where it should.** The clearing
fires while this skill is already in hand, since the showing is what loaded it. A housekeeping request
in its own words, such as "clean up those HTML files lying around", triggers neither this description
nor publish's. That path is covered by machines: `guardrails/check-rendered-sweep.py` reds while a
transient page still stands, and the release sweep runs from the publish walk. The description stays as
it is.

**F5 — reviewed, no duplication.** The clearing law states its walk once, in `references/page-lifecycle.md`.
The body carries a three-line summary and the link. `skills/publish/SKILL.md` states its own release
step. Each fact keeps one home.

**F6 — found, outside this review's write set.** `skills/communicator/README.md` still calls the skill
"seven cheap-to-follow rules" and heads a section "The seven rules (short)". The body carries
twenty-two. This predates the edit under review. It is reported here for the owner, since this session
was scoped to the files it was named to write.
