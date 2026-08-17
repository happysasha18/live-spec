# `SKILL-REVIEW` — live-spec-base, the glossary and the worked examples leave the body

Skill: live-spec-base. Date: 2026-08-17. Range: 9efe559..HEAD.

Commits of the range touching `skills/live-spec-base/`:

    5295b06 live-spec-base: the glossary and the worked examples move to references, word for word

Verdict: ALLOW WITH FINDINGS. The move is the right shape and the text really does travel unchanged,
but one sentence that left the body was the body's own reading key, and the moved prose kept pronouns
that pointed back at the file it left.

## What changed

`skills/live-spec-base/SKILL.md` loses two kinds of material. The twenty-entry glossary under "The
words this file uses" becomes `references/glossary.md`, and three worked cases — the register guard
that was built as a list of patterns, rule 24's per-kind layers and proofs, and rule 32's 2.0.0
release — become `references/worked-examples.md`. Four pointers stay behind, one to the glossary and
three to the examples file. `ARCHITECTURE.md` follows the text with new line numbers for seventeen
pins, and `guardrails/rule-census.json` gains entries for the two new files. The body falls from 645
lines and 56,083 bytes to 602 lines and 52,466 bytes; the new files hold 48 and 30 lines.

## The word-for-word claim, tested

I did not take the commit message's word for it. I extracted every removed line from the diff, stripped
the marker, and compared the result against the new files.

The glossary is exact. `diff` between the 41 removed lines and lines 8 through 48 of
`references/glossary.md` reports no difference at all — not a character, not a line break. Every one of
the twenty entries, from *the pack* to *an agent card*, reads as it read.

The three worked cases are exact at the word, with whitespace reflowed. I compared each removed chunk
against its new section as a stream of whitespace-separated tokens. In all three the diff shows only
deletions and no insertions, which is the signature of a clean move: every word in the new file was
present in the removed text, and the words that appear as "removed but not arrived" are precisely the
sentences that stayed behind in the body. Those retained sentences are "A law naming a class is held by
a judge that reads meaning. If the answer to a class is a list, the design is wrong." under the rule of
thinking; "The layers themselves are the project's own." and "The proofs follow the same shape, each
kind naming the rungs its test ladder really has." under rule 24; and the closing half of rule 32's
sentence about a design-review finding that never blocks a lane. Each of those is in the new body. No
sentence was dropped, and none was silently reworded.

One place is a rewrite rather than a move, and the commit message does not distinguish it. Rule 32 had
said the 2.0.0 release is the boundary case, that its migration chapter records "Host action: none", so
by this rule it reads as a minor, and that it keeps its published number. The body now says only that
2.0.0 "is this rule's cited boundary case, written out in" the reference. That is new prose, not
surviving prose, and it is the one sentence in the change where the body asserts that a case exists
without saying what makes it one. It is honest and short, but "word for word" describes the reference
file, not the seam.

The section headings in `references/worked-examples.md` are correct: the layers-and-proofs case does
belong to rule 24, which stands at line 356 of the new body, and the boundary case does belong to rule
32 at line 512. The rule numbers are stable in this rulebook — rule 30 is a retired gap that is still
kept as a gap — so heading by rule number is safe.

Two copy artifacts survived the verbatim discipline. The rule 32 section opens with the word "The"
alone on its own line before "2.0.0 release is the boundary case", because the original line wrapped
there; and the rule 24 section carries mid-sentence breaks in the same way. Word-for-word was honoured
so literally that the old line wrapping came with it.

## The pointers

All four resolve. I walked every `references/*.md` link in the body against the skill directory: the
glossary, the worked examples and the pre-existing settings ladder all exist at the named path.
`guardrails/check-skill-loadability.sh`, which I ran, reports OK for eleven skills. The paths are
relative to `SKILL.md`, which is what the body's own "Where the paths and the codes in this file point"
section promises a `references/` path means.

The glossary pointer is written to the house standard. It says the terms are defined once, names the
module, says what it holds — every term from *the pack* to *an agent card*, each with the
`PRODUCT_SPEC.md` entry behind it — and then says when to go: "Open that module when a term is being
resolved, and not before." That is the same shape as the settings-ladder pointer further down the file,
which is this skill's best example of the form, and it is what skill-creator asks for when it says to
reference files clearly with guidance on when to read them.

The three worked-examples pointers are weaker. Two of them ("See references/worked-examples.md for the
per-kind illustration of both", and rule 32's "written out in") tell the reader what is there but never
when to go, and none of the three names the section it wants. The file has three headed sections, so a
reader arriving from rule 24 lands at the top and must scan past a case about a register guard to find
the one they came for. A pointer that named its heading would cost four words and would make the hop
one step instead of two. This is the difference between a bare link and a pointer, and skill-creator's
bar is the latter.

The reference files themselves carry their own when-to-open lines, which is good practice and covers
some of the gap from the other side.

## Was this the right material to move

Two of the three moves are exactly what progressive disclosure is for, and one is not.

The rule of thinking's worked failure is the archetype. The maxim stays inline — a law naming a class
is held by a judge that reads meaning — and the story of the guard that was a pattern list goes behind
the pointer. A reader can apply the rule without the story. Rule 24 is the same case: the operative
requirement stays whole in the body, including that a project records `project.kind`, `project.layers`
and `project.proofs` at founding, and only the illustrations leave — the photo site, the promotion
campaign, the music project. skill-creator explicitly asks for skills that are general rather than
narrow to specific examples, so moving four illustrations out of one rule is the guidance being
followed, not stretched.

Rule 32 is the one I would argue about. The 2.0.0 case is not an illustration of the rule; it is a
standing exception to it. The rule says a release's number reports what taking it costs a host, and
2.0.0 records "Host action: none" and yet keeps a major number. That is a carve-out the pack lives
with, and the body now asserts a boundary case exists while keeping the reason for it one hop away. It
does not break the rule — the operative content, that a patch is the default, that a higher tier must
be earned, and that no machine holds the call, is all still inline — but of the three cases this is the
one where the body lost something load-bearing rather than something illustrative.

The glossary is the move that needs the most care, and it is mostly right. A glossary is definitionally
reference-shaped, it is opened at a moment a reader can recognize, and this repository's own
skill-creator evaluation from 2026-07-05 recommended exactly this destination for exactly this kind of
material. But three things left the body that are not term definitions at all.

The first and most serious is this sentence, now at `references/glossary.md:18`: the glossary "records
the senior and the orchestrator as the source's other names for it, and this file adds a fourth, the
lead. The four names mean the one session." The body uses all four names. "Senior" appears at lines
106, 152, 155, 157, 160 and 268; "the lead" at 108 and five times through rule 25; "the orchestrator"
titles rules 25 and 27; "the seat" runs throughout. I grepped the whole tree for that sentence and it
exists in exactly one place, the new reference file — `PRODUCT_SPEC.md` does not carry it. So the only
statement anywhere that these four words name one session now sits behind a pointer whose instruction
is to open it when a term is being resolved. A reader who does not already know they are synonyms has
no reason to believe a term is being resolved: rule 25 simply reads as though a lead exists beside the
seat. That is the classic failure mode of a body-thinning — what moved out was not elaboration, it was
the key that makes the body's own prose parse. This sentence should come back inline, or the body
should settle on one name.

The second is the gate entry's closing clause: "Where a sentence here says a check *reds* something, it
means the check fails on it." That is a reading instruction for the rulebook's idiom, not a definition
of a gate. The body uses the verb three times, and the first use is at line 16 — thirty lines before
the glossary pointer appears at all. A reader meets the idiom before they are told the module exists.

The third is smaller: the queue-row entry's "This file calls it a row" is a statement about the
rulebook's naming convention, which now lives outside the rulebook.

## What is now orphaned, and what is now mis-anchored

Nothing is unreachable. Both new files are pointed at from the body, both are registered in
`guardrails/rule-census.json`, and both are tracked as rows 130 and 131 of `docs/PROGRESS.md`. The
seventeen `ARCHITECTURE.md` pins renumber correctly: I checked the arithmetic against the four hunk
headers, which shift the file by 36, then 40, then 43 lines, and every pin moved by exactly the shift
that applies at its old position — 108 to 68, 440 to 397, 604 to 561, and so on. Each pin lands on the
same content it named before.

What is mis-anchored is inside the moved text itself, and it is the price of moving word for word
without re-reading the words in their new home. `references/glossary.md` opens with the heading "The
words this file uses", copied from the body's section title, where "this file" meant `SKILL.md`; in its
new home the heading claims to be about the glossary's own vocabulary. The same deixis breaks three
more times inside it: "this file adds a fourth, the lead", "This file calls it a row", and "Where a
sentence here says a check *reds* something" — three pronouns that pointed at the rulebook and now
point at the reference. The entry "an agent — defined where the rule that binds it stands, at rule 31"
names a rule number with no document to hang it on. `references/worked-examples.md` has the same
problem lighter: "Its own worked failure" and "the clearest breach of this one" both had antecedents in
the body, and now lean on the section heading to recover them; the rule 32 section's "by this rule"
names no rule on the page.

One thing is missing rather than broken. `ARCHITECTURE.md` pins `references/settings-ladder.md` as an
owned artifact of this node, with a note that names the body line carrying its pointer. The two new
modules got no such pin, though the commit was already editing that pin block. And there is no
conservation test. The communicator carries `tests/test_communicator_body_thinned.py`, which asserts
that its reference file exists, that the body still points at it, that the relocated text is present in
the new file, and that the body stays under the 500-line ideal — with a comment deriving that number
from skill-creator by name. That is the house pattern for a body-thinning, and live-spec-base has no
equivalent. Nothing reds today if a later edit drops one of these four pointers or empties either file.

## Frontmatter, name, description

The frontmatter carries `name: live-spec-base`, matching its folder, a description, and
`metadata.version: 5.0.0`. The loadability gate passes on all four counts plus the required "Work that
belongs elsewhere" section, which the skill has.

The description is strong on triggering. It names its ten sibling skills by name, which is the surest
way this skill gets loaded, and it gives three distinct contexts — before using a pack skill, before
briefing a worker that will write files, and to resolve shared rules and settings. It is pushy in the
way skill-creator asks for without being vague. "Thirty-four rules in the body" is accurate: I counted
thirty-four numbered rules, running 1 to 35 with 30 standing as a retired gap.

It is now stale in one respect. The description still names `references/settings-ladder.md` as the
skill's on-demand module and says when it is opened, as though it were the only one. There are three
now. Metadata is the layer that is always in context, so an accurate one-line mention of the glossary
would earn its tokens more than most sentences in the body do. This commit added two modules and did
not touch the sentence that inventories them.

Separately, and not this commit's doing: `skills/live-spec-base/README.md` calls it "the three-step
settings ladder" while the body states four scopes. Pre-existing, out of range, noted only so it is not
lost.

## Length and structure

Better, and still short of the bar. 645 lines to 602 against skill-creator's under-500 ideal. The
guidance for a body at this size is to add a layer of hierarchy with clear pointers about where to go
next, and that is precisely the move this commit makes, so the direction is right even though the
number is not yet reached. Navigability improves most at the top of the file: a reader who opens
`SKILL.md` for the shared rules previously walked forty lines of definitions before reaching the rule
of thinking, and now reaches it in five. The three cuts inside rules 24 and 32 leave those rules
reading tighter. The 43-line saving is modest for the disruption, but the glossary was the single
densest block a reader had to cross to get to the rules, so the lines removed were better chosen than
their count suggests.

## The net

The claim in the commit message is true where it matters. I verified the glossary as byte-identical and
the three worked cases as token-identical, and I found no sentence altered, dropped or reworded in the
move. The pointers resolve, the pin renumber is arithmetically faithful, and the loadability gate is
green — I ran it. The prover record at `docs/prover/2026-08-17-slimdown-pin-renumber.md` reports
`check-pin-drift.sh` at exit 0 with 207 pins and the wider suite results for the three-commit packet; I
did not run those myself and do not claim them.

What this change owes before it ships, in order. First, the four-names sentence belongs back in the
body or the body needs one name — it is the only statement in the repository that lets a reader parse
seat, senior, orchestrator and lead as one session, and it is now behind a door the reader has no
reason to open. Second, the `reds` idiom note should return inline, since the body uses the verb thirty
lines before it names the module. Third, the four pronouns in the moved glossary text should be
re-anchored to name the rulebook now that they no longer sit inside it, and the copy artifacts — the
orphaned "The" opening rule 32's section, the mid-sentence wraps — should be reflowed. Fourth, the
three worked-examples pointers should name the section they want, and the frontmatter description
should stop implying the settings ladder is this skill's only module. Fifth, a conservation test on the
communicator's model would keep this review's verdict true after today.

None of these is a lost rule, and every one is a small edit against text that is already in the right
place. That is why this is ALLOW WITH FINDINGS and not BLOCK.

Reviewer: an independent adversarial read of commit 5295b06 against 9efe559, performed by a dedicated
reviewer agent for this range, working from the skill-creator discipline installed at
`~/.claude/skills/skill-creator`. No file was written or modified during the review.
