---
name: text-audit
description: Audit any human-facing text and fix what a stranger stops on — run the mechanical lints, then a fresh cold reader with zero context on the text's history, take the places a reader stops, fix them from the source, and repeat until two consecutive reads return zero blocking findings. Use when the user wants a text checked for comprehension before it ships — "audit this text", "cold-read this", "will a stranger understand this", "is this README/section/page clear", "check this for undefined terms", "does this read", "review this copy for clarity" — on a spec section, a README, a decision page, marketing copy, an article, or any prose a person will read. It states the register it holds a text to and the reader-prompt it hands the cold reader, ready to paste. NOT for reviewing whether a spec HOLDS TOGETHER as a design (that is product-prover, which argues with the claims); NOT for grading taste or rewriting a voice; and NOT for machine-read text — worker briefs, checkpoints, internal notes no human returns to.
metadata:
  version: 4.3.0
---

# text-audit — read a text as a stranger, fix where they stop

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live
> ONCE in the pack's base skill, `live-spec-base` (v4.3.0), together with the settings ladder — this skill
> references them and elaborates only its own domain. Used standalone, this note is plain advice.

This skill audits a piece of human-facing text for comprehension and fixes what it finds. A **cold reader**
is a fresh session that reads the text with no knowledge of its history — no prior draft, no author's
intent, no project background beyond the words on the page. The author of a text cannot be its cold reader,
because the author already holds the context the text is missing, so the author reads meaning that a
stranger cannot. This skill supplies the stranger.

It runs on any text a person will read: a spec section, a README, a decision page, marketing copy, an
article, a release note. It came out of the spec-format comprehension gate, where a panel of fresh readers
found new blocking terms on every pass while fixed items stayed fixed, and the finding stream thinned toward
zero only under consecutive clean reads (`docs/spec-format.md`). This skill packages that loop for any text.

## When it fires

Load it when a human-facing text is about to ship and its clarity matters: a README before a push, a spec
section after an edit, a decision page before it goes to the person, a piece of marketing copy, an article
draft. The trigger is a person asking whether a reader will understand the text — "audit this", "cold-read
this", "is this clear", "will a stranger get this".

## When NOT to use

- **A design review of a spec** belongs to product-prover. That pass argues with the claims — a missing
  state, a false invariant, an unhandled transition. This skill reads for whether the words land on a
  stranger, and it invents no answers about the design. Run the prover for the design and this skill for the
  prose; they read different failures on the same page.
- **Taste and voice** stay with the person and with the marketing skills. This skill holds a text to a
  register — a stated set of writing rules, listed in full below under "The register it holds a text to" —
  and reports where a reader stops. It does not grade a voice or rewrite for style beyond that rule set.
- **Machine-read text** — a worker brief, a checkpoint, an internal note, anything written for a program or
  for the agent's own consumption — needs no cold reader, because no stranger returns to it.

## The loop

The audit runs in four steps, and the loop closes on a stated condition.

1. **Mechanical lints first, and fix every hit here.** Run every free check that a script or a grep can
   settle before a reader spends attention, and fix each hit it reports at this step, before the cold reader
   runs. A machine catches the cheap classes — an undefined term, a known weak word, a contrast-by-denial
   frame (a sentence that names a thing by denying its neighbour, such as "X, not Y"). The cold reader then
   spends its whole attention on the classes no machine knows yet.
2. **A fresh cold reader.** Hand the text to a session with zero context on its history, under the
   reader-prompt below. The reader returns the places a stranger stops, each classified blocking or
   non-blocking. It fixes nothing, and it writes down the guess it made in place of a missing answer, since that guess shows the writer where the text sent the reader. Its whole job is to mark where it stopped, what it guessed, and why.
3. **Fixes drawn from the source.** For each blocking finding, write the fix from the material the text
   already rests on — the source spec, the code, the recorded decision, the author's own notes. A term gets
   the definition its source gives it; a relational word gets the reference point its source names. Where the
   source holds no answer, the finding is a real hole: record it as a question for the person who owns the
   text — its author, or whoever requested the audit and can answer for its intent — and invent nothing.
4. **Read again, and close on two clean reads.** After the fixes land, hand the text to a new fresh reader.
   The loop ends when two consecutive reads return zero blocking findings. Two reads rather than one is the
   stopping rule the spec-format gate observed. Each fresh reader catches a class the reader before it did not
   reach. A single clean read can therefore still hide a blocking class that no reader has found yet. The stream is
   shown to have thinned to zero only when two reads in a row return nothing that blocks (`docs/spec-format.md`).

Per changed section the loop is cheap: a small edit puts one definition and a handful of sentences in front
of a reader. Audit the section the edit touched; read a whole page only on the person's word.

## The mechanical lints

Run these before any reader. Each lint names a script and a grep fallback. The scripts live in the
live-spec repository (public home: `github.com/happysasha18/live-spec`), under its `guardrails/` and
`scripts/` directories, and every script path below is relative to that repository's root. When that
repository is on your disk, run the scripts from its root, whatever project the audited text belongs to.
When it is not, use each lint's grep fallback — the fallbacks need no scripts and work anywhere, so the
audit never requires obtaining the repository.

- **Vocabulary — every term is defined at first use.** Every domain noun the text uses has a one-sentence
  definition the reader meets before the noun's first working use. Script: `python3
  guardrails/check-vocabulary.py FILE`. Grep fallback: list the capitalized or coined nouns and confirm each
  has an introducing sentence above its first use.
- **Weak relational words with unfilled slots.** A word like *depends*, *related*, *handles*, *based on*,
  *corresponds to*, *proportional*, *larger*, *sufficient*, *appropriate*, *fast*, *easily* opens a slot — a
  reference point, a measure, or a reason — that the sentence must fill where the word stands. Script:
  `python3 guardrails/check-weak-words.py FILE` (the fuller list lives in `guardrails/weak-words.json`,
  seeded from the ISO 29148 and INCOSE vague-term lists — two published requirements-writing standards that
  each name the vague terms to avoid). Grep fallback: search for the words this bullet itself lists, and
  read each hit for a filled slot nearby; the reader-prompt below repeats the same list.
- **Requirement shape, where the text is a spec.** A spec section owes the requirements genre — context
  before criteria, one trigger and one response per criterion, a judge and a measure on every judgment.
  Script: `python3 guardrails/check-requirement-shape.py FILE`. Grep fallback: read each requirement by hand
  and confirm the context comes before the criteria, each criterion carries one trigger and one response, and
  every evaluative phrase names who judges and by what. This lint applies only to a text written as a spec;
  skip it for a README, an article, or marketing copy.
- **Style and register.** Sentence length (the register targets 15–25 words; a sentence past ~25 words is a
  hit), no all-capital words used for emphasis (acronyms and code identifiers are fine), no
  contrast-by-denial frames, no grading adjectives. Scripts: `python3 scripts/spec-style-lint.py FILE` for a
  spec section, and `python3 scripts/preshow-register-lint.py FILE` for any human-facing surface. Grep
  fallback: read for the four classes by hand — sentences past ~25 words, all-capital words used for
  emphasis, "X, not Y" denial frames, and adjectives that grade a result's size (big, huge, minor,
  breakthrough).
- **One name per thing.** No artifact appears under two names. Script: `python3
  guardrails/check-one-name.py FILE`. Grep fallback: list each named artifact and confirm one name carries
  it throughout, with no second name for the same thing.

A mechanical hit is fixed before the cold reader runs, so the reader never spends a finding on a class a
machine already owns.

## The cold reader

Hand the text to a fresh session under the prompt below. Two rules govern the pass:

- The reader has **zero context on the text's history.** No prior draft, no project background, no author's
  intent beyond the page. In this pack, that means a fresh worker with the pack not loaded reading the text
  as an outside reader (`docs/spec-style.md`, the clean-agent split).
- Every finding is **classified blocking or non-blocking.** A blocking finding is a place a reader cannot
  act on the text or cannot trust it until the answer arrives — an undefined term the rest of the text leans
  on, a relational word whose slot decides what the reader does, a claim with no findable ground. A
  non-blocking finding is a place the text still reads and the fix would only sharpen it — a smoother
  ordering, a shorter sentence, a term that helps but is not load-bearing. The loop closes on zero
  **blocking** findings; the non-blocking ones queue for a taste call.

### The reader-prompt — ready to paste

Paste this verbatim to the cold-reader session, with the text appended:

```
You are reading a piece of text for the first time. You have no background on it: no
project history, no earlier draft, no knowledge of what the author meant beyond the words
on the page. Read it once, straight through, as a stranger who needs to understand it and
act on it.

Mark every place you stop. A stop is any one of these:
- a term used before it is defined, or never defined on the page;
- a relational word — depends, related, handles, based on, corresponds to, proportional,
  larger, sufficient, appropriate, fast, easily — with no stated what, how, or how-much
  beside it;
- a sentence you had to read twice to parse;
- a claim whose ground you cannot find anywhere in the text;
- a judgment word — broken, worth, better, enough, larger-than — with no stated judge or
  measure.

For each stop, write one entry with five parts:
1. the quoted phrase;
2. where it sits (the heading or the opening words of its paragraph);
3. what a stranger cannot tell from the page alone;
4. the guess you made in place of the missing answer;
5. blocking or non-blocking — blocking means a reader cannot act on or trust the text until
   this is answered; non-blocking means the text still reads and the fix would only sharpen
   it.

Do not fix anything. Report only where you stopped and why. Return the entries as a numbered
list. If you stopped nowhere, say so in one line.

At every relational word, ask the three questions and write which one is unanswered: relative
to what? by what measure? or else what alternatives? A word the list above does not name, that
still stopped you, is a real find — report it and note that it is new.

--- TEXT ---
<paste the text here>
```

The last instruction keeps the reader catching the words the list does not know yet. When a reader reports
a new slot-opening word, the auditor adds it by hand to the weak-word list before the next run — to
`guardrails/weak-words.json` where the repository is on disk, or to the project's own copy of the list
otherwise. Each catch added this way is one more class the mechanical layer holds from then on.

## Fixes drawn from the source, never invented

A fix comes from the material the text rests on, and from nowhere else.

- A **term** gets the definition its source gives it, added at the term's first use.
- A **relational word** gets the reference point, the measure, or the reason its source names, written where
  the word stands.
- A **judgment word** gets its judge and its inputs, from the source that decides the judgment.
- A **claim** gets its ground stated, or the claim is cut to what the source supports.

Where the source holds no answer — the spec is silent, the decision was never made, the number was never set
— the finding is a genuine hole. Record it as a question for the person and leave a visible mark at the spot,
so the open question travels with the text instead of being filled silently. The mark takes the text's own
form: an inline `[GAP: what is missing]` note for a spec section, or a bracketed query in the draft for a
README, an article, or a piece of copy. Inventing an answer to close a cold reader's finding is the one move
this skill forbids, because an invented definition reads clean to the next reader while the text now states
something no source backs.

## The register it holds a text to

The audit holds every text to one register. A text that meets it reads cleanly for a stranger on the first
pass.

- **One idea per sentence.** A sentence carries a single fact. A sentence packing three parallel facts is
  split, or the facts become a list.
- **Plain words.** The text speaks in ordinary language and in the product's own terms. It carries no
  internal handle doing the talking — no code, no coined metaphor a reader never chose to learn.
- **Every term defined at first use.** A domain noun meets its one-sentence definition before its first
  working use. A coined word is replaced by a defined standard term, or it is defined on the page.
- **Positive framing.** The text says what a thing is and what happens. The contrast-by-denial frame that
  names a thing by denying its neighbour — "X, not Y", an em-dash or comma leading into the denied
  alternative — is replaced by a sentence that states what the thing is in its own words. Genuine
  prohibitions stay, written as a plain imperative.
- **No significance inflation, in either direction.** The text states a result at its true size. It does not
  dress a small change as a breakthrough, and it does not shrink a real one. It carries no self-praise for
  its own honesty or directness.
- **Native short-SVO English, or the text's own language.** Sentences run subject-verb-object and stay
  short. A text written in another language holds to the same shape in that language.
- **Answer-first ordering, for a text that answers a question.** A text whose job is to answer opens with
  the answer, then gives the ground. A reader gets the outcome before the reasoning.

This register is the same one the pack's communicator and spec-author hold their prose to; its full home is
`skills/communicator/references/writing-register.md`. This skill states the working subset it audits
against.

## The skill's own text is held to its register

This SKILL.md is held to the register above: plain positive sentences, every term defined at first use, no
coined metaphor doing the talking, no contrast-by-denial frame. It is a human-facing surface, so
`scripts/preshow-register-lint.py` is the register check that applies to it, and that run is clean. A change
to this file re-runs that lint and one cold-reader loop on the changed section before it ships.

## What it is not

- **Not the prover.** product-prover argues with a spec's claims and finds design holes; this skill reads
  prose for whether a stranger understands it. Different failures, same page.
- **Not a rewriter of voice.** It holds a text to a register and reports where a reader stops. Taste and
  voice stay with the person.
- **Not a machine that invents answers.** A finding with no source answer is a question for the person, never
  a gap the skill fills from imagination.

> The pack, whole: **live-spec-base** holds the shared rules and defaults · **spec-author** writes the spec ·
> **product-prover** reviews it · **design-reviewer** judges the design behind it · **build-pipeline** ships
> the change · **test-author** derives the matrix and writes the tests · **communicator** makes the human
> exchange land · **feedback-intake** brings what comes back to its home · **feedback-collector** offers a
> rare private note up to the authors · **text-audit** reads a text as a stranger and fixes where they stop · **publish** sees the work out the door, owing its kind's checklist.
