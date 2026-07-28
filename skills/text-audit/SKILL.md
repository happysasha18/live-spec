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

<!-- generated:human-prose-rules — scripts/gen-language-consumers.py owns the block below -->

## The rules it holds a text to

These are every rule binding human-prose. They are printed here out of `guardrails/language-rules.json`, which is where each one is edited. A change made in this block is overwritten by the next run of `scripts/gen-language-consumers.py`.

Each line gives the rule, then the question to ask of a sentence.

- **an ordinary word carrying a private project meaning** — A word keeps its everyday meaning. A term this project needs holds one glossary entry, written in plain words. The body then uses that term unchanged, with no definition attached. *Ask:* Would a person outside this project recognize this word, or does the text gloss it in plain words where it first appears? (`r01`)
- **a coined, loan-translated, or respelled word standing where a plain standard word exists** — Where the industry has a word, the text writes the industry's word. A term this project coined is replaced by the standard word, or defined where it first appears. In the reader's own language, a term is written as a real word of that language. *Ask:* Does a standard word already name this thing, and is the word here that standard word — a real word of the reader's own language, carrying the meaning this project gives it? (`r02`)
- **a name stacking two nouns with no relation between them** — A name holds one noun. Where two nouns belong together, a verb or a preposition between them carries the relation. *Ask:* Does this name run two nouns together, and can a reader say how the second relates to the first? (`r03`)
- **one thing answering to a second name** — One thing carries one name in every sentence, from its first use onward. *Ask:* Does any thing named here appear under a different word somewhere else in this document or its neighbours? (`r04`)
- **a predicate applied to a subject that cannot carry it** — A verb or an adjective attaches to a subject that can carry it. Where the subject cannot act, the sentence names the actor that can: a person, a script, a hook, or a model. *Ask:* Can the thing this sentence names as its subject perform this verb, or hold this quality? (`r05`)
- **a number standing with no ground** — Every number says what it counts, what it is compared against, and which direction is better. A number that was simply chosen says that it was chosen. *Ask:* Can a reader say what this number is measured against and which way is better? (`r06`)
- **a set named by a count, a pointer, or a position instead of given** — A sentence that depends on a set gives that set, or points by name to the one place holding it. A part of a set is named by what its members are. *Ask:* Can a person who reads this sentence alone name the members of the set it points at? (`r07`)
- **a sentence carrying more than one rule, running past its word cap, or piling up clauses** — One sentence carries one rule and no definitions. It stays under the word cap for its surface, and it holds at most one subordinate clause. *Ask:* Does this sentence state one rule a reader could cite on its own, stay under the cap for its surface, and hold its subject in view from its first word to its last? (`r08`)
- **a text breaking a rule it states** — A text ships once it obeys every rule it states. The sentence stating a rule is the first place to check that rule. *Ask:* Does the sentence stating this rule obey the rule it states? (`r09`)
- **a thing named by denying its neighbour** — A sentence says what a thing is, in its own words. A boundary worth naming gets its own plain sentence. *Ask:* Does the denied half give the reader anything the reader did not already have? (`r10`)
- **an internal code leading a sentence to the reader** — Plain words carry the meaning, and an internal code trails. In chat the code sits in parentheses at the sentence's end. In a document it sits in square brackets at the line's end. *Ask:* Does the sentence still carry its meaning with the code removed, and does the code stand anywhere other than at the end? (`r11`)
- **a word grading how important or how good a thing is** — A text states what a thing is or does, and lets the reader weigh it. A word grading importance or quality stands only beside a concrete fact. *Ask:* Does this sentence tell the reader how much to care, rather than what happened? (`r12`)
- **a sentence grading the person, or grading the writer's own act** — A remark from the person is answered, and the answer says what follows from it. A text lets its own honesty and rigour show through what it reports. *Ask:* Does this sentence carry a fact, or a verdict on the person's remark or on the writer's own work? (`r13`)
- **a sentence carrying no information** — Every sentence shown to the person advances the finding, the decision, or the action. A sentence carrying a fact the reader would otherwise lose stays, however short. *Ask:* Would the reader lose a fact if this sentence were deleted? (`r14`)
- **a word inflating a statement while adding nothing** — A word earns its place by adding information. A phrase whose deletion changes nothing is deleted. *Ask:* Does removing this word change what the sentence says? (`r15`)
- **the language each surface is written in** — Documents, commits, code, and artifacts are written in English, and conversation runs in the human's pinned language. *Ask:* Is this text in the language its surface is pinned to? (`r18`)
- **English that reads as compressed or poetic** — English in a document or an artifact reads like a native technical writer: short subject-verb-object sentences, common words, and no poetic compression. *Ask:* Could a native technical writer have written this sentence for an open-source project? (`r20`)
- **a word standing in all capitals** — Every word is written in ordinary case. Force comes from the declarative statement itself. *Ask:* Is this word in capitals because it is a name the project has defined, or to make the sentence louder? (`r23`)
- **the person an explanatory sentence speaks in** — Explanatory text addresses the reader as `you` for what a person does, and names the component for what software does. *Ask:* Does this sentence tell the reader what they do, in words spoken to them? (`r25`)
- **a sentence with no actor, or its action buried in a noun** — A rule sentence says who does what and when, in the active voice with a named actor. Its action lives in a verb. *Ask:* Does this sentence answer who does this, to what, and when, and is its action a verb rather than a noun? (`r26`)
- **an opener saying what a thing is not** — A sentence opens with what a thing is. *Ask:* Does the opening clause say what the thing is before it says what it is not? (`r27`)
- **a judgment with no judge and no measure** — Every judgment names its judge and its inputs. *Ask:* Who decides whether this is true, and by what measure? (`r32`)
- **a relational word leaving its slot empty** — A relational word fills every slot it opens, right where the word stands. *Ask:* Relative to what, by what measure, or else what alternative? (`r33`)
- **a pronoun with no antecedent in its own sentence** — `it`, `this`, and `they` stand with an unambiguous antecedent in the same sentence. Where none stands, the noun is repeated. *Ask:* Can a reader say which thing this pronoun points at without looking back a sentence? (`r39`)
- **an example restating a rule that was already clear** — An example earns its place by resolving an ambiguity, and it uses realistic values. One worked case per rule is enough. *Ask:* Could a reader have read this rule two ways without this example, and is this prose rather than a rule entry in the rule home? (`r41`)
- **an abstraction standing where a concrete noun would do** — The text prefers the concrete noun. A required abstraction is grounded with a two- or three-item example at its first use. *Ask:* Can the reader picture the thing this noun names? (`r43`)
- **a paragraph carrying more than one point** — One paragraph carries one point, stated in its first sentence, with the rest supporting it. *Ask:* Does a reader who reads only the first sentences of this section still follow it? (`r44`)
- **a long flat run of peer items at one level** — A document is a tree of grouped topics, and its levels nest without skipping. A long run of peer items is gathered under headed parents. *Ask:* Does this level hold a run of peer items with no grouping over them? (`r45`)
- **a reply that buries its answer** — A reply opens with the answer — the outcome, the decision, or the finding — in a few lines the reader may stop at, and puts reasoning, evidence, and options underneath. *Ask:* Can the reader stop after the opening block and still hold the answer? (`r46`)
- **an offer to do work the writer could already derive** — A derivable act is done and reported done, and a work item is parked for the human only after a fresh test of whether it can be derived now. *Ask:* Does this sentence offer to do something the writer already has everything to do? (`r48`)
- **a mistake expanded into a self-audit paragraph** — A mistake is owned in one line and fixed. *Ask:* Does this passage explain the writer's own failure at more length than the fix takes? (`r49`)
- **a working note handed to the reader unmarked, or a choice with no open answer** — Dense working notes are marked so the reader can skip them, and they carry one idea per line. Every choice offered leaves room for a free-form answer. *Ask:* Can the reader tell at a glance which lines are notes, and can they answer outside the options given? (`r50`)
- **a task-list subject written in machine words** — The session's task list on the human's screen speaks plain product words in the documents' language, understandable at a glance. *Ask:* Does a person glancing at this task subject know what is being done? (`r52`)
- **human-facing prose drafted by a writer holding the project's own vocabulary** — The first draft of prose a human will read is written by a fresh writer with no package rules loaded, working from a plain brief. The brief states the facts, names the intended reader, and lists the rules binding the surface. A person who has read the rulebook then reviews and revises that draft. *Ask:* Was this sentence first written by someone who had never read this project's skills, working from a brief? (`r53`)
- **a changed section shipped before two clean cold readings** — A changed section is read by fresh readers who carry no project context, until two consecutive reads return zero blocking findings. A finding blocks when the reader could not go on, or would have applied the text wrongly. *Ask:* Did a reader with no project context read this section and stop nowhere? (`r54`)
- **one fact stated a second time in another place** — One fact lives in one home, and every other place points at that home rather than restating it. *Ask:* Does another place in this project already state this fact? (`r56`)
- **a phrase the human cut returning in a later draft** — A phrasing the human killed in a review round stays out of every later draft of that artifact, and an approved text takes exactly the correction the human named. *Ask:* Has the human already cut this wording from this artifact? (`r57`)
- **a defect recorded as examples with no class behind them** — When a text stops a reader, the writer names the class of mistake, defines it, and enters that class in the rule home. The examples under an entry are the recorded evidence that produced the class. *Ask:* Does the entry state what the mistake IS, so a writer can find an instance nobody has met yet? (`r61`)
- **a sentence open to two readings, or hiding its cause or what it leaves out** — A reader reaches one interpretation of a sentence, sees what causes what, and can tell what the text leaves out. *Ask:* Can a reader read this sentence one way only, name what it makes happen, and say which alternatives it passed over? (`r62`)
- **a thing named by its number, so the reader must leave the sentence to learn what it is** — A sentence names a thing by what it is, and its number trails at the line's end. *Ask:* Does this sentence say what the thing IS, or does it give only a number, a position, or a count that the reader must go and resolve? (`r63`)
- **parallel items run together inside one sentence** — Two or more parallel items become a bulleted or numbered list under a one-line lead, one item per line. *Ask:* Does this sentence run several items together where a list would put one on each line? (`r64`)

<!-- /generated:human-prose-rules -->

The rules above are the whole set a human-prose audit holds a text to. They live in one place,
`guardrails/language-rules.json`, and every page and every checker in the pack is built from it, so
one edit reaches all of them. The writer's page `docs/language-rules.md` gives each rule with its
examples, its exceptions, and its thresholds. One short document walked end to end against these
rules, with the rule named at each fix, stands at `docs/language-worked-example.md`.

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
