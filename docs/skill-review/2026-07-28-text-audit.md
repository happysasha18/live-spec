# Skill review — text-audit (the reader-prompt's fifth part)

`SKILL-REVIEW`

Skill: text-audit
Date: 2026-07-28
Reviewer: skill-creator (Anthropic)

Verdict: passes with findings, handed back — this review wrote its record and touched no other
file, so nothing below is applied. Two findings name a live contradiction inside the pack's own
text and are handed to the owner with a proposed repair each; the description and the file's
length are reviewed with a reason and stand as they are.

## What changed

The reader-prompt's entry shape grew from four parts to five: a new fourth part asks the cold
reader to write the guess it made in place of a missing answer, and the blocking/non-blocking
call moved from fourth to fifth (`skills/text-audit/SKILL.md:147-154`). The sentence that followed
the list, "Do not fix anything. Do not guess the missing answer. Report only where you stopped and
why," lost its middle clause, since that clause forbade the thing part four now asks for; "Do not
fix anything" stayed (`skills/text-audit/SKILL.md:156`). The change brings this prompt into line
with `docs/language-defects.md`, which already asks a cold reader for that guess and states why:
the guess is what shows the writer where the text sent them.

## The check this review was asked for: does the prompt state one thing with docs/language-defects.md?

It does. `skills/text-audit/SKILL.md:147-154` now reads:

> For each stop, write one entry with five parts:
> 1. the quoted phrase;
> 2. where it sits (the heading or the opening words of its paragraph);
> 3. what a stranger cannot tell from the page alone;
> 4. the guess you made in place of the missing answer;
> 5. blocking or non-blocking — blocking means a reader cannot act on or trust the text until
>    this is answered; non-blocking means the text still reads and the fix would only sharpen
>    it.

`docs/language-defects.md:87-94` reads:

> A reading comes back as a file naming what the reader was given and asked for, followed by a
> numbered list of the stops, each carrying five things:
>
> - the phrase the reader stopped on;
> - where that phrase sits on the page;
> - what a stranger cannot tell from the page alone;
> - the guess the reader made in place of the missing answer;
> - whether the stop blocked the reader, or the reader noticed it and read on.

Five parts, in the same order, carrying the same five facts. Part 3 is worded identically in both.
Parts 1, 2, 4, and 5 differ only in the person each file addresses: the skill's prompt speaks to
the reader directly ("the quoted phrase", "the guess you made"), while the defects page describes
the reading afterward, in the third person ("the phrase the reader stopped on", "the guess the
reader made"). Part 2 in the skill adds an operational detail the defects page leaves general
(the heading or the paragraph's opening words, versus "on the page"), which sharpens the
instruction without changing what it asks for. Before this change the two disagreed outright — four
parts against five, and "do not guess" against "write the guess" — which is the contradiction the
task that produced this delivery names as its reason. That disagreement is gone.

## Findings

**F1 — handed back. `skills/text-audit/SKILL.md:58` still says the reader guesses no
answers, and the reader-prompt now requires one.** Step 2 of "The loop" reads: "The reader returns
the places a stranger stops, each classified blocking or non-blocking. It fixes nothing and
guesses no answers; its whole job is to mark where it stopped and why." That sentence was true of
the old four-part prompt, which forbade a guess in the same words. The new prompt asks for the
guess as its fourth part, so this sentence is now false of the loop it summarizes, and a reader who
reaches the prompt a page later meets the contradiction the source task describes — except now
inside this file rather than between this file and `docs/language-defects.md`. Proposed repair:
"The reader returns the places a stranger stops, each classified blocking or non-blocking, with
the guess it made where an answer was missing. It fixes nothing; its whole job is to mark where it
stopped, why, and what it guessed."

**F2 — handed back. `skills/text-audit/README.md:22` carries the same sentence and the same
contradiction.** "It returns the places a stranger stops, each marked blocking or non-blocking. It
fixes nothing and guesses no answers." This is the same class as F1 — one sentence, stated twice,
both now false of the prompt this skill ships — and it sits in the file a person reads first, before
the SKILL.md body. Proposed repair: "It returns the places a stranger stops, each marked blocking
or non-blocking, with the guess it made wherever an answer was missing. It fixes nothing."

**F3 — reviewed, no change. The reader-prompt collects the guess but never says what becomes of
it, and that is the right scope for this file.** Nothing in "Fixes drawn from the source, never
invented" (`skills/text-audit/SKILL.md:172-188`) reads the guess field back; the fix step still
draws only on the text's own source material. `docs/language-defects.md` is the file that spends
the guess — its rule-folding procedure records "the guess the reader made there" as the first step
of turning a repeated stop into a rule (`docs/language-defects.md:296-297`). text-audit runs on any
project's text, not only this one's rulebook, so the consuming procedure belongs to the caller, not
to the generic prompt. No change is owed here.

**F4 — reviewed, no change. The frontmatter description still says when to load this skill and
when to leave it alone.** It names the trigger phrases and the texts this skill runs on, and it
names the three places that route elsewhere: a design review of a spec (product-prover), taste and
voice (the person and the marketing skills), and machine-read text no stranger returns to. The
changed lines sit inside the reader-prompt, three sections below the description, and touch none of
those three boundaries or the trigger list. The description's own count of what a reading returns
("the reader-prompt it hands the cold reader, ready to paste") stays true without needing to name a
part count.

**F5 — reviewed, no change. The file's length leaves room, but a reader still stops early because
of F1.** The body runs 238 lines, well under the 500-line point where Anthropic's guidance asks for
another layer of hierarchy; no split is owed on size alone. The stop this delivery leaves behind is
not a length problem: a reader who reads "The loop" in order meets the false sentence at line 58
first, about ninety lines before the prompt it describes, and files the wrong expectation before
ever seeing the guess requirement. Fixing F1 removes that stop; nothing else in the body invites
one.

## The gate

`bash guardrails/check-skill-review.sh` returns:

```
OK (skill review): the push changes no skill body (a pure version-stamp diff owes no review),
  so the skill-creator-review gate stands down by name (SPEC INV-208).
```

It compared `origin/main` against `HEAD`, both at commit `a25ab3c`. The SKILL.md change this
review covers is uncommitted working-tree content — `git diff origin/main -- skills/text-audit/SKILL.md`
shows it, `git diff origin/main HEAD -- skills/text-audit/SKILL.md` shows nothing, because the gate
only reads committed history. The green above is not a verdict on this delivery; it is the gate
finding no committed skill change yet. Once `skills/text-audit/SKILL.md` is committed, the gate
will require a committed record under `docs/skill-review/` naming `text-audit` with a `Verdict:`
line, no older than that commit — this file, once committed alongside it or after it, is that
record.

## The test suite

`python3 -m pytest tests -q` reports **2207 passed, 2 skipped** in 113.84s, no failures. This
review wrote only this file and ran no other command that touches the tree, so nothing in this run
traces to it.
