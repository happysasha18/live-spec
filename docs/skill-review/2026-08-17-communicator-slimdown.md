# `SKILL-REVIEW` — communicator, the rule histories move to references

Skill: communicator. Date: 2026-08-17. Range: 9efe559..HEAD.

Commits of the range touching `skills/communicator/`:

    cb26b70 communicator: the rule histories move to references, word for word

Verdict: ALLOW WITH FINDINGS. The word-for-word claim is true and nothing is orphaned, but one
sentence filed as history is an imperative the body no longer states anywhere, and all four pointers
claim a rule's whole provenance while the same rules keep dated provenance in the body.

## What changed

Twelve passages leave `skills/communicator/SKILL.md` and land in a new
`skills/communicator/references/rule-histories.md` (2,100 bytes, 38 lines), filed under four headings
in the order the rules appear in the body: rule 12 the capture echo, rule 13 narration, rule 6 plain
language, rule 10 the decision page. Four pointer lines are left behind, at lines 73, 136, 269 and
308. The body falls 45,861 to 44,881 bytes and 499 to 488 lines. `ARCHITECTURE.md` follows the text
with six renumbered line pins, and `guardrails/rule-census.json` gains the new file's entry and
restates the body's counts.

## The word-for-word claim, tested rather than believed

I checked it in both directions with a short `python3` comparison over `git show 9efe559:...` and the
working tree, whitespace-normalized so that re-wrapping does not count as a change. Every one of the
twelve excised fragments — from "No echo" through the parenthetical naming the screenshot of a bare
code chain — appears verbatim in the new file: twelve of twelve matched, none altered, none dropped,
none reworded. Running it the other way, every non-heading line of `rule-histories.md` except its own
four-line preamble was found verbatim in the body at 9efe559. Nothing was invented on the way across.
The only differences are line breaks: passages that were wrapped across two or three body lines are
single lines in the reference. The file's own promise that "every passage below reads exactly as it
read in the rule's body" holds.

I did not re-run the push gate or the suite. The prover record at
`docs/prover/2026-08-17-slimdown-pin-renumber.md` reports a sentence-stream audit of the same three
commits and reaches the same conclusion for this one; my check was made independently of it.

## The pointers

All four spell the same relative path, `references/rule-histories.md`, which resolves from the body's
directory to a file that exists. I re-read each of the seven `ARCHITECTURE.md` pins into this body
against the file as it now stands — 35, 175, 225, 276, 289, 341, 429 — and each lands on the line its
label names, so the renumber that rode along is correct.

Where they fall short is register. Skill-creator asks that reference files be pointed at from
SKILL.md with guidance on WHEN to read them, and this body already knows how: line 189 says to read
the page lifecycle "before clearing a page," and line 22 says field-examples is "loaded on demand."
The four new pointers say only what is in the file, never when to open it. The when — "read when a
rule's ORIGIN is wanted, and not before" — sits inside `rule-histories.md`, which is the one place a
reader who has not opened it cannot see.

The larger fault is that they over-claim. "Where this rule came from is in
`references/rule-histories.md`" reads as the whole of it, and for three of the four rules it is not.
Rule 13 keeps its offline-window tooth's origin at line 99. Rule 6 keeps two dated notes at lines 254
and 260. Rule 10 keeps one at line 300. A grep for dated and attributed provenance across the body
still returns roughly two dozen lines. A reader who follows the pointer for the origin of rule 6 and
finds only the calque trap and the task-list case will conclude the rest was never recorded, when in
fact it is four lines above the pointer. Either the pointers should say they carry part of the story,
or the rest should follow — and the second is the better repair, because it is what would make this
file worth its hop.

## Was this the right material, and did the cut earn a file

Eight of the twelve fragments are unambiguously provenance: dated attributions, an incident with a
lost suite run, the day a rule was born. Those belong out of the body under any reading of
progressive disclosure, and moving them costs the reader nothing, because a rule's birthday is never
needed to obey it.

Two are not provenance, and one of those is the finding of this review. The sentence "Do NOT rely on
the harness's own task list or spinner for this: a browser-seated session never shows them, and even
locally they stop updating through a long run of tool calls" is an imperative with a mechanism behind
it, and it is now filed under "where the rules came from." I grepped the body and all five reference
files: no imperative survivor exists. What remains at line 124 is the softer "never the status's
home," which states the conclusion without the fact that makes it obeyable — that a browser seat
shows no panel at all. The reference file's own preamble says "the operational text of every rule
stays in `SKILL.md`," and this sentence is the counterexample to its own claim. The second, the
Identity tooth's "a reader dropping in mid-session can tell what is being worked without scrolling
back," was the sufficiency test for that tooth; without it the tooth lists what to name but no longer
says how much naming is enough. The third candidate, rule 6's own-coinage trap, I judged safe:
`references/field-examples.md` lines 28 to 30 carry the same law with a worked pair, and rule 6
already points there at line 264.

On whether under a kilobyte earns a new file, the byte count is the wrong measure and flatters the
change less than the line count does. Skill-creator's stated bar is a body under 500 lines, and this
body stood at 499 — one line from the ceiling, with no headroom for the next rule. It now stands at
488. That is the metric the discipline actually names, and against it the move is not cosmetic. The
file also earns its place prospectively, as the home the remaining two dozen dated markers should
migrate into. Judged only on what landed today, it is a thin hop; judged as the first course of a
wall, it is the right first course, and the pointers' over-claim is the debt that says so.

## Orphans, and what a move can break here

Nothing is unreachable. All four histories name rules that still exist and still carry those names,
the file's order matches the body's order, and no history describes a retired rule. A grep across
`tests/`, `guardrails/`, `hooks/` and `scripts/` for the moved sentences returns nothing, so no gate
or test was reading text that has since moved — the move breaks no machine. `guardrails/rule-census.json`
gained the new file's entry in the same commit. `docs/PROGRESS.md` also lists the file, at row 75,
but that edit is uncommitted in this worktree, so the published progress table does not yet know the
file exists.

## Frontmatter, and the body's shape after the cut

The frontmatter is untouched and meets the bar: `name: communicator` matches the directory, and the
description states what the skill does, names five triggering situations, and then does the rarer and
more useful thing of naming three situations that are NOT reasons to load it. That negative half is
what keeps a skill this large from firing on every passing narration line, and it is better than most
descriptions I read. `metadata.version` stays at 5.0.0 across a substantive body change, which is
worth a note only because the house itself treats a text move as substantive — the prover record says
plainly that moving text out of a body is not the version-stamp bump gate s exempts.

Navigability is better in three places and worse in two. Rules 12 and 10 read cleaner with the
parenthetical asides gone. Rule 13's live-status tooth reads worse: the "So" at line 123 used to
follow from the prohibition that was removed and now leans on the sentence before it, which does not
support it in the same way. And the edit did not re-wrap what it cut. Lines over 120 characters go
from 31 to 37 in a file wrapped near 110: the four pointers run 143 to 158 characters each, and the
joins left behind at lines 94 and 260 run 135 and 147. A commit that removed 980 bytes made six of
this file's lines longer than any line it deleted. That is cosmetic, but it is the kind of cosmetic
that a body at the length cap cannot afford to accumulate.

## The net

The claim on the tin is true, the machine is undisturbed, and the pins hold. Two things are owed
before this stops being a hop the reader pays for and starts being a structure that repays it: the
harness-panel prohibition returns to rule 13 as an imperative with its reason, leaving only the dated
words in the reference; and the four pointers either narrow their claim or the body's remaining dated
provenance follows the twelve passages across. Neither is a rewrite. Both are the difference between
a file that holds provenance and a file that holds some of it.

Reviewer: an independent adversarial read of commit cb26b70 against 9efe559, performed by a dedicated
reviewer agent for this range, working from the skill-creator discipline installed at
`~/.claude/skills/skill-creator`. No file was written or modified during the review.
