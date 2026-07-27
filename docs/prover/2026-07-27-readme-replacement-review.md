# Review — the handed-in README replacement, 2026-07-27

**What was reviewed.** `docs/handovers/2026-07-27-readme-replacement-draft.md`, a full replacement for the
repository's public README handed in by the promotion campaign window with its cover note
(`docs/handovers/2026-07-27-readme-replacement-note.md`), audited twice on that side. Reviewed here by a
seat that wrote none of the text, against the tree rather than against the cover note.

**Verdict: HOLD.** Eleven must-fix defects, ten should-fix. About two thirds of the draft is more accurate
than the page that ships today, and its correction of the guardrail section is the largest honesty gain
available to that page, so the draft returns for fixes rather than being set aside.

## Must-fix

1. The opening states that the tests passed because a race destroyed the judge's verdicts and a missing
   installed hook counted as a green skip. The race is real and no record ties it to a green suite, and
   the green skip belonged to a push gate rather than to the test run. State that the judge delivered no
   verdict at all, and name the gate as the place the skip counted.
2. "Three landings were reported finished" undercounts the day: more than three landed on 17 July, and
   three is the count of landings that drew an adversarial review. Say that.
3. "Everything was fixed before the release went out the next day" closes too cleanly. The release then
   failed a fresh review and was reissued hours later, which is the stronger and truer sentence.
4. Two events are fused: the same-session landing reviews of 17 July, which the records cite as
   successes, and the release pass of 18 July, which is where the same-session defect was recorded.
   Attribute the defect to the release pass.
5. The draft describes a gate that checks the review record exists, is dated, and names a different seat.
   No such gate ships: the push chain runs twenty-six gates and none is this one, and the only machine is
   a traceability test proving the pack's own text states the duty. State it as a discipline and describe
   the record a release gate may demand.
6. One sentence fails the pack's own style reading as an error, the construction that names a thing by
   denying its neighbour. The shipped README returns zero. Rewrite that clause.
7. The draft tells the reader that the installer prints the hook lines and leaves their hooks alone. The
   installer the reader was pointed at copies skills alone; the printing belongs to the adoption script,
   and the four lines live in the guardrails README. Name the right place.
8. A boundary is quoted as being stated "in the same words" in the scaffold's own README, and it shares
   almost no clause with the source. Quote it verbatim or drop the claim of sameness.
9. The account of the test-presence check is backwards: it reads the contents of every offending file to
   find the ones whose whole diff is version-shaped, and only when no test was touched at all; the
   user-facing set and the tests directory are config keys rather than fixed rules.
10. The completeness check is described as reading rendered output, and with no render command it reads
    the files the config names, which in this repository are two plain documents. The emptiness rule
    fires only when every matching line is empty. Both matter, because the page's own 10 July story turns
    on that config surface.
11. "Two projects run under this pack in production" is inherited verbatim from the page that ships, and
    the architecture and the matrix both name three real hosts. A reader who opens either document meets
    a contradiction on the page's own honesty claim. This one is the owner's call, and both sentences
    move together.

## Should-fix

The timestamp story joins two variants and credits the wrong cure; the authority-anchor block covers the
decisions record alone and is advisory elsewhere; the lane cap bounds how many lanes open at once and
says nothing about whether independent rows should have run in parallel; the three-way test's only home is
a dated audit document rather than the rulebook; a rule that breaks twice drops its mid-turn qualifier;
the clean-seat rule asks for a differently-contexted seat briefed from primary sources; the surface
setting was null rather than blank and is now armed by a red-proven test; the shipped line about a check
reding when a shipped behaviour has no requirement behind it is dropped and the paragraph loses its
teeth; the completeness check's second direction is omitted, and it is the direction the 10 July story
turns on; and one heading invites the reader to count the wrong file.

## Verified sound

The install block is byte-identical to the shipped one and no link is lost, seventeen surviving and three
added. Twenty-six gates on the push chain lettered a to z with no gaps; twenty-five carrying their own red
proof with one declared as riding the suite; the pre-commit chain and its parked-decision and
second-writer checks; the CI mirror belonging to this repository alone; thirty-four shared rules; more
than three hundred review records; four host checks; the declined gate's three recorded reasons and its
built, red-proven cap; and every element of the 10 July probe — the invited outsider, three planted
breaks, two blocked, the third a fake surface in a rendered artifact, and the null setting as its root
cause. No stray non-English content, and the owner's name appears exactly where it appears today.

## What the draft does better, to keep in any outcome

The four-script account replaces a wrong one: the page that ships says two checks decide a push where the
kit ships four and this repository runs twenty-six. The paragraph naming what those checks cannot see — a
changed calculation, a new sort order, an altered edge, a new field — exists nowhere today. The declined
gate links its own record rather than a directory. The pre-commit chain and the meta-gate appear for the
first time. The two blocked breaks in the 10 July probe make the miss land harder. The feedback skill's
description is corrected from a false claim about sending. The skill count matches the rulebook's own
heading. And the measurement limit, that a week of this has never been costed, is a boundary the page has
never carried.

## The stranger read

The headline earns attention and the first paragraph loses it: a reader meets landings, the suite, the
judge, a green skip, and a record before learning what the product is, and meets a coined word for the
working seat three times with no gloss. The page that ships earns its second paragraph in three sentences
because its scenario is one a stranger recognises. The recommendation is to open on that scenario, then
bring the incident as its proof, and move the clean-seat rule into the section about what is different.
The draft also runs from about 1,680 words to about 2,690.
