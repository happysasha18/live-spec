---
name: text-audit
description: Audit any human-facing text and repair what a stranger stops on. It runs the mechanical lints first. Then it hands the text to a fresh cold reader with zero context on the text's history. It takes the places that reader stops and repairs them from the source. It repeats until two consecutive reads return zero blocking findings. Use it when a person wants a text checked for comprehension before it ships. The ask sounds like "audit this text", "cold-read this", or "will a stranger understand this". It also sounds like "is this README clear", "check this for undefined terms", or "review this copy for clarity". It runs on a spec section, a README, a decision page, marketing copy, an article, or any prose a person will read. It states the register it holds a text to, and it ships the reader-prompt ready to paste. Design review of a spec belongs to product-prover, which argues with the claims. Grading taste and rewriting a voice stay with the person. Machine-read text needs no audit, because no stranger returns to a worker brief, a checkpoint, or an internal note.
metadata:
  version: 4.3.0
---

# text-audit — read a text as a stranger, fix where they stop

> Part of the **live-spec pack**. The shared working rules live once in the pack's base skill,
> `live-spec-base` (v4.3.0), together with the settings ladder. This skill points at them and covers only
> its own subject. Used on its own, this note is plain advice.

This skill checks whether a stranger understands a text, and repairs the places where they stop.

A **cold reader** is a fresh session that reads the text with no knowledge of its history. It holds no
earlier draft, no author's intent, and no project background beyond the words on the page. An author
cannot be their own cold reader. The author holds the context the text is missing, so the author reads a
meaning a stranger cannot reach. This skill supplies the stranger.

It runs on any text a person will read: a spec section, a README, a decision page, marketing copy, an
article, a release note.

The loop came from the spec-format comprehension gate. A panel of fresh readers found new blocking terms
on every pass, and the terms already repaired stayed repaired. The stream of findings reached zero only
under two clean reads in a row (`docs/spec-format.md`). This skill packages that loop for any text.

## When it fires

Load it when a human-facing text is about to ship and its clarity matters:

- a README before a push;
- a spec section after an edit;
- a decision page before it goes to the person;
- a piece of marketing copy or an article draft.

The trigger is a person asking whether a reader will understand the text: "audit this", "cold-read this",
"is this clear", "will a stranger get this".

## Work that belongs elsewhere

- **A design review of a spec** belongs to product-prover. That pass argues with the claims: a missing
  state, a false invariant, an unhandled transition. This skill reads whether the words land on a
  stranger, and it invents no answer about the design. The two passes read different failures on the same
  page, so run each for its own.
- **Taste and voice** stay with the person and with the marketing skills. This skill holds a text to the
  register it lists at the end, and it reports where a reader stops. It grades no voice, and it rewrites
  no style beyond those rules.
- **Machine-read text** needs no cold reader, because no stranger returns to it. A worker brief, a
  checkpoint, and an internal note are machine-read.

## The loop

The audit runs in four steps and closes on a stated condition.

1. **Run the mechanical lints, and fix every hit.** Run every check a script or a grep settles, before a
   reader spends attention on it. Fix each hit at this step. A machine catches the cheap classes: an
   undefined term, a known weak word, a sentence that names a thing by denying its neighbour. The cold
   reader then spends its whole attention on the classes no machine knows yet.
2. **Hand the text to a fresh cold reader.** The reader session has zero context on the text's history,
   and it works under the reader-prompt below. It returns the places a stranger stops, each one marked
   blocking or non-blocking. It repairs nothing.
   It writes down the guess it made in place of a missing answer, because that guess shows where the text
   sent the reader.
3. **Write each fix from the source.** For a blocking finding, take the fix from the material the text
   already rests on. That material is the source spec, the code, the recorded decision, or the author's
   own notes. A term gets the definition its source gives it. A relational word gets the reference point
   its source names.
   Where the source holds no answer, the finding is a real hole. Record it as a question for the person
   who owns the text, and invent nothing. That owner is the author, or whoever asked for the audit and
   can answer for the text's intent.
4. **Read again, and close on two clean reads.** After the fixes land, hand the text to a new fresh
   reader. The loop ends when two consecutive reads return zero blocking findings. Two reads rather than
   one is the stopping rule the spec-format gate observed. Each fresh reader catches a class the reader
   before it did not reach, so a single clean read can still hide a blocking class. The stream is shown to
   have thinned to zero when two reads in a row return nothing that blocks (`docs/spec-format.md`).

Per changed section the loop is cheap. A small edit puts one definition and a handful of sentences in
front of a reader. Audit the section the edit touched, and read a whole page only on the person's word.

## Running it on a spec section

A spec section here is one requirement with its Context paragraph, its User Story, and its acceptance
criteria. A short run of such requirements is also a section.

Ten requirements at a time is the working size, which runs to about 250 lines. A fresh reader holds that
much, and a repair inside those lines reaches nothing a hundred lines away.

Four things change on this surface.

**The requirement-shape lint applies here.** Run `python3 guardrails/check-requirement-shape.py FILE`
beside the other lints. It reads three things a README never owes. Context comes before criteria. Each
criterion carries one trigger and one response. Every judgment names a judge and a measure.

**A criterion and the prose around it take different rules.** A numbered acceptance criterion writes in
the third person and names the actor it binds. The Context paragraph beside it speaks to the reader
directly. A rule binds a block, so the two never judge one sentence.

**Every mark a machine reads survives the repair.** A requirement's number and its bracket anchors stay
exactly as they were. So do its headings, and any phrase a test quotes. A rewrite that moves one of them
breaks the code-to-location table, the test matrix, or a test.

**A fix comes from the spec's own neighbours.** The architecture document, the recorded decision, and the
test matrix hold the answers this text rests on. Where none of them answers, the finding is a real hole,
and it takes an inline `[GAP: what is missing]` note.

Four checks run after the section is repaired, and each one prints what it read:

- the test suite, which pins exact phrases from the spec, so a dropped phrase fails a test;
- a second reader who puts the old text and the new text side by side and reports every difference in
  meaning;
- the structure checks over requirement shape, the generated index, the matrix references, and the
  frozen baseline;
- the census, `python3 scripts/rule-census.py`, whose count for the file falls, or the batch is redone.

The measure of the work is a build test. Hand the repaired requirements to a fresh agent that holds no
other context. Ask it to implement them, and count how many it builds without asking a question. On
2026-07-27 that count was two of six.

## The mechanical lints

Run these before any reader. Each lint names a script and a grep fallback.

The scripts live in the live-spec repository, whose public home is `github.com/happysasha18/live-spec`.
They sit under its `guardrails/` and `scripts/` directories, and every path below is relative to that
repository's root. When that repository is on your disk, run the scripts from its root, whatever project
the audited text belongs to. When it is not on your disk, use the grep fallbacks. They need no scripts and
work anywhere, so the audit never waits on a download.

- **Every term is defined at first use.** Every domain noun the text uses carries a one-sentence
  definition, and the reader meets it before the noun's first working use.
    - Script: `python3 guardrails/check-vocabulary.py FILE`.
    - Grep fallback: list the capitalized and the coined nouns, then confirm each one has an introducing
      sentence above its first use.
- **A weak relational word fills the slot it opens.** Words such as *depends*, *related*, *handles*,
  *based on*, *corresponds to*, *proportional*, *larger*, *sufficient*, *appropriate*, *fast*, and
  *easily* open a slot. The slot takes a reference point, a measure, or a reason, and the sentence fills
  it where the word stands.
    - Script: `python3 guardrails/check-weak-words.py FILE`. The fuller list lives in
      `guardrails/weak-words.json`, seeded from the ISO 29148 and INCOSE vague-term lists. Those are two
      published requirements-writing standards, and each names the vague terms to avoid.
    - Grep fallback: search for the words this bullet lists, and read each hit for a filled slot nearby.
      The reader-prompt below repeats the same list.
- **A spec section owes the requirements genre.** Context comes before criteria, each criterion carries
  one trigger and one response, and every judgment names a judge and a measure. This lint reads a text
  written as a spec. Skip it for a README, an article, or marketing copy.
    - Script: `python3 guardrails/check-requirement-shape.py FILE`.
    - Grep fallback: read each requirement by hand against the three points above.
- **Style and register.** A sentence stays between 15 and 25 words, and one past 25 is a hit. No word
  stands in capitals for emphasis, though an acronym and a code identifier pass. No sentence names a thing
  by denying its neighbour, and no adjective grades a result's size.
    - Scripts: `python3 scripts/spec-style-lint.py FILE` for a spec section, and `python3
      scripts/preshow-register-lint.py FILE` for any human-facing surface.
    - Grep fallback: read for those four classes by hand. The last one shows up as *big*, *huge*, *minor*,
      or *breakthrough*.
- **One name per thing.** No artifact appears under two names.
    - Script: `python3 guardrails/check-one-name.py FILE`.
    - Grep fallback: list each named artifact, and confirm one name carries it throughout.

A mechanical hit is fixed before the cold reader runs, so no reader spends a finding on a class a machine
already owns.

## The cold reader

Hand the text to a fresh session under the prompt below. Two rules govern the pass.

The reader holds **zero context on the text's history**: no earlier draft, no project background, no
author's intent beyond the page. In this pack that means a fresh worker with the pack not loaded, reading
the text from outside (`docs/spec-style.md`, the clean-agent split).

Every finding is **marked blocking or non-blocking**. A finding blocks when the reader cannot act on the
text, or cannot trust it, until the answer arrives. An undefined term the rest of the text leans on blocks.
So does a relational word whose slot decides what the reader does, and a claim with no findable ground. A
non-blocking finding is a place the text still reads and the fix would only sharpen it. A smoother
ordering, a shorter sentence, and a term that helps without carrying weight are non-blocking. The loop
closes on zero blocking findings, and the non-blocking ones queue for a taste call.

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

That last instruction keeps the reader catching words the list does not know yet. When a reader reports a
new slot-opening word, the auditor adds it by hand to the weak-word list before the next run. The list is
`guardrails/weak-words.json` where the repository is on disk, and the project's own copy of the list
otherwise. Each catch added this way is one more class the mechanical layer holds from then on.

## Fixes come from the source, never from invention

A fix comes from the material the text rests on, and from nowhere else.

- A **term** gets the definition its source gives it, written at the term's first use.
- A **relational word** gets the reference point, the measure, or the reason its source names, written
  where the word stands.
- A **judgment word** gets its judge and its inputs, from the source that decides the judgment.
- A **claim** gets its ground stated, or the claim shrinks to what the source supports.

Sometimes the source holds no answer: the spec is silent, the decision was never made, the number was
never set. That finding is a genuine hole. Record it as a question for the person, and leave a visible
mark at the spot, so the open question travels with the text. The mark takes the text's own form. A spec
section takes an inline `[GAP: what is missing]` note. A README, an article, or a piece of copy takes a
bracketed query in the draft.

Inventing an answer to close a finding is the one move this skill forbids. An invented definition reads
clean to the next reader, while the text now states something no source backs.

## This file is held to the rules it lists

This SKILL.md obeys the register below. Four of those rules show on every page of it:

- its sentences are plain and positive;
- every term is defined at its first use;
- no coined metaphor does the talking;
- no sentence names a thing by denying its neighbour.

It is a human-facing surface, so `scripts/preshow-register-lint.py` is the register check that applies to
it, and that run is clean. A change to this file re-runs that lint, and it runs one cold-reader loop on
the changed section before it ships.

<!-- generated:human-prose-rules — scripts/gen-language-consumers.py owns the block below -->

## The rules it holds a text to

These are every rule binding human-prose. They are printed here out of `guardrails/language-rules.json`, which is where each one is edited. A change made in this block is overwritten by the next run of `scripts/gen-language-consumers.py`.

Each entry names the class of mistake, states the rule, gives the question to ask of a sentence, and carries one recorded case under it. The case is written text on the left and its repair on the right. Every case the class was built from lives in the rule home.

- **an ordinary word carrying a private project meaning** (`r01`)
  A word keeps its everyday meaning. A term this project needs holds one glossary entry, written in plain words. The body then uses that term unchanged, with no definition attached.
  *Ask:* Would a person outside this project recognize this word, or does the text gloss it in plain words where it first appears?
    - `The system shall red a branch whose merge-base sits behind main's tip.` → `The system shall refuse a branch whose merge-base sits behind main's tip.`
- **a coined, loan-translated, or respelled word standing where a plain standard word exists** (`r02`)
  Where the industry has a word, the text writes the industry's word. A term this project coined is replaced by the standard word, or defined where it first appears. In the reader's own language, a term is written as a real word of that language.
  *Ask:* Does a standard word already name this thing? Is the word used here that standard word, written as a real word of the reader's own language?
    - `the door` → `the entry point`
- **a name stacking two nouns with no relation between them** (`r03`)
  A name holds one noun. Where two nouns belong together, a verb or a preposition between them carries the relation.
  *Ask:* Does this name run two nouns together, and can a reader say how the second relates to the first?
    - `chat-law reminder` → `the reminder that carries the chat laws`
- **one thing answering to a second name** (`r04`)
  One thing carries one name in every sentence, from its first use onward.
  *Ask:* Does any thing named here appear under a different word somewhere else in this document or its neighbours?
    - `the mechanical checks, in the README, for the step the skill body calls the mechanical lints` → `the mechanical lints, in both places`
- **a predicate applied to a subject that cannot carry it** (`r05`)
  A verb or an adjective attaches to a subject that can carry it. Where the subject cannot act, the sentence names the actor that can: a person, a script, a hook, or a model.
  *Ask:* Can the thing this sentence names as its subject perform this verb, or hold this quality?
    - `the numbers do not show red` → `name the actor that shows a colour, or state what the numbers do`
- **a number standing with no ground** (`r06`)
  Every number says what it counts, what it is compared against, and which direction is better. A number chosen rather than derived says that it was chosen.
  *Ask:* Can a reader say what this number is measured against and which way is better?
    - `the register targets 15-25 words, and a sentence past ~25 words is a hit` → `a sentence stays between 15 and 25 words, and one past 25 is a hit`
- **a set pointed at by a count, a pointer, or a position, with its members never given** (`r07`)
  A sentence that depends on a set gives that set, or points by name to the one place holding it. A part of a set is named by what its members are.
  *Ask:* Can a person who reads this sentence alone name the members of the set it points at?
    - `**Case: the three legs**` → `**Case: the prototype-reference leg, the completeness scan, and the behaviour-traces-to-spec check**`
- **a sentence carrying more than one rule, running past its word cap, or piling up clauses** (`r08`)
  One sentence carries one rule and no definitions. It stays under the word cap for its surface, and it holds at most one subordinate clause.
  *Ask:* Does this sentence state one rule a reader could cite on its own? Does it stay under the cap for its surface? Does it hold its subject in view from its first word to its last?
    - `the orchestration law that the session keeps pulling unblocked queue work while any remains.` → `state the law in one short sentence, and put its parts in a list`
- **a text breaking a rule it states** (`r09`)
  A text ships once it obeys every rule it states. The sentence stating a rule is the first place to check that rule.
  *Ask:* Does the sentence stating this rule obey the rule it states?
    - `a 62-word sentence inside the file that states the 25-word cap` → `the same rule in three sentences, the longest of them 41 words`
- **a thing named by denying its neighbour** (`r10`)
  A sentence says what a thing is, in its own words. A boundary worth naming gets its own plain sentence.
  *Ask:* Does the denied half give the reader anything the reader did not already have?
    - `X, not Y` → `Say what the thing IS in its own sentence`
- **an internal code leading a sentence to the reader** (`r11`)
  Plain words carry the meaning, and an internal code trails. In chat the code sits in parentheses at the sentence's end. In a document it sits in square brackets at the line's end.
  *Ask:* Does the sentence still carry its meaning with the code removed, and does the code stand anywhere other than at the end?
    - `INV-141 gives the design review a pass of its own.` → `The design review runs as a pass of its own [INV-141].`
- **a word grading how important or how good a thing is** (`r12`)
  A text states what a thing is or does, and lets the reader weigh it. A word grading importance or quality stands only beside a concrete fact.
  *Ask:* Does this sentence tell the reader how much to care about what it reports?
    - `Two constraints, and they are hard ones.` → `Two constraints.`
- **a sentence grading the person, or grading the writer's own act** (`r13`)
  A remark from the person is answered, and the answer says what follows from it. A text lets its own honesty and rigour show through what it reports.
  *Ask:* Does this sentence carry a fact, or a verdict on the person's remark or on the writer's own work?
    - `good question` → `answer it, and say what follows from the answer`
- **a sentence carrying no information** (`r14`)
  Every sentence shown to the person advances the finding, the decision, or the action. A sentence carrying a fact the reader would otherwise lose stays, however short.
  *Ask:* Does the reader do anything differently because this sentence is here?
    - `Its whole job is to mark where it stopped, what it guessed, and why.` → `deleted, since the two sentences above it already say this`
- **a word inflating a statement while adding nothing** (`r15`)
  A word earns its place by adding information. A phrase whose deletion changes nothing is deleted.
  *Ask:* Does removing this word change what the sentence says?
    - `really` → `delete`
- **the language each surface is written in** (`r18`)
  Documents, commits, code, and artifacts are written in English, and conversation runs in the human's pinned language.
  *Ask:* Is this text in the language its surface is pinned to?
    - `a commit message in Russian, in a repository whose documents are pinned to English` → `the message in English, with the conversation about it staying Russian`
- **English that reads as compressed or poetic** (`r20`)
  English in a document or an artifact reads like a native technical writer: short subject-verb-object sentences, common words, and no poetic compression.
  *Ask:* Could a native technical writer have written this sentence for an open-source project?
    - `the sketch itself carries the look` → `name the actor and say plainly what it does`
- **a word standing in all capitals** (`r23`)
  Every word is written in ordinary case. Force comes from the declarative statement itself.
  *Ask:* Is this word in capitals because it is a name the project has defined, or to make the sentence louder?
    - `CHANGES` → `changes`
- **the person an explanatory sentence speaks in** (`r25`)
  Explanatory text addresses the reader as `you` for what a person does, and names the component for what software does.
  *Ask:* Does this sentence tell the reader what they do, in words spoken to them?
    - `one` → `you`
- **a sentence with no actor, or its action buried in a noun** (`r26`)
  A rule sentence says who does what and when, in the active voice with a named actor. Its action lives in a verb.
  *Ask:* Does this sentence answer who does this, to what, and when? Does its action live in a verb?
    - `the verification of the claim occurs` → `the suite verifies the claim`
- **an opener saying what a thing is not** (`r27`)
  A sentence opens with what a thing is.
  *Ask:* Does the opening clause say what the thing is before it says what it is not?
    - `It doesn't know what a PRD is. It knows entities, states, transitions, invariants.` → `It works from entities, states, transitions, and invariants, rather than from a document's genre.`
- **a judgment with no judge and no measure** (`r32`)
  Every judgment names its judge and its inputs.
  *Ask:* Who decides whether this is true, and by what measure?
    - `broken` → `name the judge and the measure`
- **a relational word leaving its slot empty** (`r33`)
  A relational word fills every slot it opens, right where the word stands.
  *Ask:* Relative to what, by what measure, or else what alternative?
    - `a few` → `state the exact quantity`
- **a pronoun with no antecedent in its own sentence** (`r39`)
  `it`, `this`, and `they` stand with an unambiguous antecedent in the same sentence. Where none stands, the noun is repeated.
  *Ask:* Can a reader say which thing this pronoun points at without looking back a sentence?
    - `It returns the places a stranger stops.` → `That session returns the places a stranger stops.`
- **an example restating a rule that was already clear** (`r41`)
  An example earns its place by resolving an ambiguity, and it uses realistic values. One worked case per rule is enough.
  *Ask:* Could a reader have read this rule two ways without this example? Does this example stand in prose, outside a rule entry in the rule home?
    - `Grep fallback: read for the four classes by hand - sentences past ~25 words, all-capital words used for emphasis, denial frames, and adjectives that grade a result's size.` → `Grep fallback: read for those four classes by hand. The last one shows up as big, huge, minor, or breakthrough.`
- **an abstraction standing where a concrete noun would do** (`r43`)
  The text prefers the concrete noun. A required abstraction is grounded with a two- or three-item example at its first use.
  *Ask:* Can the reader picture the thing this noun names?
    - `an entity` → `A screen, a panel, a saved file`
- **a paragraph carrying more than one point** (`r44`)
  One paragraph carries one point, stated in its first sentence, with the rest supporting it.
  *Ask:* Does a reader who reads only the first sentences of this section still follow it?
    - `one paragraph carrying the author's blindness, three example defects, and the loop's origin` → `the author's blindness in its own paragraph, the three defects as a list, and the origin in a paragraph after them`
- **a long flat run of peer items at one level** (`r45`)
  A document is a tree of grouped topics, and its levels nest without skipping. A long run of peer items is gathered under headed parents.
  *Ask:* Does this level hold a run of peer items with no grouping over them?
    - `a bullet running the rule, its script, and its grep fallback together in one paragraph` → `the rule as the bullet, with the script and the grep fallback nested under it`
- **a reply that buries its answer** (`r46`)
  A reply opens with the answer: the outcome, the decision, or the finding. The opening runs a few lines, and the reader may stop there. Reasoning, evidence, and options stand underneath.
  *Ask:* Can the reader stop after the opening block and still hold the answer?
    - `a report opening with the method it ran, and the finding in its last paragraph` → `the finding in the opening lines, and the method underneath it`
- **an offer to do work the writer could already derive** (`r48`)
  A derivable act is done and reported done. A backlog item is parked for the human only after a fresh test of whether the answer can be derived now.
  *Ask:* Does this sentence offer to do something the writer already has everything to do?
    - `just say the word` → `do the act and report it done`
- **a mistake expanded into a self-audit paragraph** (`r49`)
  A mistake is owned in one line and fixed.
  *Ask:* Does this passage explain the writer's own failure at more length than the fix takes?
    - `Direct answer: yes, I broke the method... (a paragraph auditing my own failure)` → `name the fix in one line, make it, and go on`
- **a working note handed to the reader unmarked, or a choice with no open answer** (`r50`)
  Dense working notes are marked so the reader can skip them, and they carry one idea per line. Every choice offered leaves room for a free-form answer.
  *Ask:* Can the reader tell at a glance which lines are notes, and can they answer outside the options given?
    - `a dense working note handed to the reader with no mark on it` → `the same note opening with a marker that says it is a working note, one idea per line`
- **a task subject written in machine words** (`r52`)
  The harness task panel on the human's screen speaks plain product words in the documents' language, understandable at a glance.
  *Ask:* Does a person glancing at this task subject know what is being done?
    - `run gen-language-consumers.py and splice AUDIT_SKILL_REL` → `print the writing rules into the audit skill`
- **human-facing prose drafted by a writer holding the project's own vocabulary** (`r53`)
  The first draft of prose a human will read is written by a fresh writer with no package rules loaded, working from a plain brief. The brief states the facts, names the intended reader, and lists the rules binding the surface. A person who has read the rulebook then reviews and revises that draft.
  *Ask:* Was this sentence first written by someone who had never read this project's skills, working from a brief?
    - `a paragraph drafted by the session that held the whole pack loaded` → `the paragraph drafted by a fresh writer from a plain brief, then revised by someone who has read the rules`
- **a changed section shipped before two clean cold readings** (`r54`)
  A changed section is read by fresh readers who carry no project context, until two consecutive reads return zero blocking findings. A finding blocks when the reader could not go on, or would have applied the text wrongly.
  *Ask:* Did a reader with no project context read this section and stop nowhere?
    - `a section shipped after one reading that returned five stops` → `the section read again after the repairs, and shipped once two readings in a row returned nothing that blocks`
- **one fact stated a second time in another place** (`r56`)
  One fact lives in one home. Every other place points at that home.
  *Ask:* Does another place in this project already state this fact?
    - `the writing rules written out a second time inside another skill` → `the rules in one file, and the second skill pointing at that file`
- **a phrase the human cut returning in a later draft** (`r57`)
  A phrasing the human cut in a review round stays out of every later draft of that artifact. An approved text takes exactly the correction the human named.
  *Ask:* Has the human already cut this wording from this artifact?
    - `«X — not Y» returning in a later draft, after the human cut it` → `the sentence saying what the thing is, in its own words`
- **a defect recorded as examples with no class behind them** (`r61`)
  When a text stops a reader, the writer names the class of mistake, defines it, and enters that class in the rule home. The examples under an entry are the recorded evidence that produced the class.
  *Ask:* Does the entry state what the mistake is, so a writer can find an instance nobody has met yet?
    - `a list of banned words: leg, goes red, station, door` → `the class - a coined word standing where a standard word exists - with those four as its recorded evidence`
- **a sentence open to two readings, or hiding its cause or what it leaves out** (`r62`)
  A reader reaches one interpretation of a sentence, sees what causes what, and can tell what the text leaves out.
  *Ask:* Can a reader read this sentence one way only, name what it makes happen, and say which alternatives it passed over?
    - `it hands the text to a fresh reader who has no knowledge of its history and marks every place a stranger stops` → `it hands the text to a fresh reader who knows nothing of its history, and that reader marks every place a stranger stops`
- **a thing named by its number, so the reader must leave the sentence to learn what it is** (`r63`)
  A sentence names a thing by what it is, and its number trails at the line's end.
  *Ask:* Does this sentence say what the thing is? Does it give only a number, a position, or a count the reader must go and resolve?
    - `Requirement 233 states the orchestration laws.` → `The requirement on how work is routed between tiers states the orchestration laws [INV-241].`
- **parallel items run together inside one sentence** (`r64`)
  Two or more parallel items become a bulleted or numbered list under a one-line lead, one item per line.
  *Ask:* Does this sentence run several items together where a list would put one on each line?
    - `The system shall refuse a branch behind main's tip, a lane with no open row, a host with no worktree line, and a lane past the cap.` → `The system shall refuse each of the four faults below. - a branch behind main's tip; - a lane with no open row; - a host with no worktree line; - a lane past the cap.`
- **a rare word standing where an everyday word says the same thing** (`r65`)
  A sentence takes the everyday word wherever an everyday word carries the meaning. A rare or bookish word stands only where no everyday word says the same thing. A term of the profession stays as it is, and the words around it come down.
  *Ask:* Would a professional reader whose first language is other than English reach for a dictionary on this word?
    - `a writer marinated in this project's own vocabulary` → `a writer who has already read this project's rules`
- **a document written in the register of the message that asked for it** (`r66`)
  The register of a request settles nothing about the register of the document. A person writes a request however is fastest for them. Every document is written to the rules of its surface, whatever the request looked like.
  *Ask:* Did this sentence take its tone from the message that asked for the work?
    - `ok so the gate basically checks the counts and yells when something is off` → `The gate measures every live document and refuses a push where a count stands above its record.`
- **a defined term standing in a file that is read apart from its definition** (`r67`)
  A term defined in one home stands in another file only where that file gives its reader a path to the definition. A file read on its own carries the terms it uses, or it names where each one is defined.
  *Ask:* Reading this file alone, could I reach the definition of this term?
    - `together with the settings ladder` → `together with the four scopes that settle a setting: the session's live word, the host profile, the personal profile, and the package default`
- **a placeholder word standing where the thing's own name fits** (`r68`)
  A sentence carries the name of the thing it is about. A pronoun or a general word stands only where the name would clutter the sentence. A status word stands only where the sentence has already stated the condition behind it.
  *Ask:* Does this word name the thing, or does the reader have to carry the name in from an earlier sentence?
    - `This keeps the leading context clear enough to hold the campaign.` → `The leading session then holds enough room to carry the campaign.`

<!-- /generated:human-prose-rules -->

The rules above are the whole set a human-prose audit holds a text to. They live in one place,
`guardrails/language-rules.json`. Every page and every checker in the pack is built from that file, so one
edit reaches all of them. The writer's page `docs/language-rules.md` gives each rule with its
examples, its exceptions, and its thresholds. One short document walked end to end against these rules,
with the rule named at each fix, stands at `docs/language-worked-example.md`.

## The pack this skill belongs to

- **live-spec-base** holds the shared rules and the defaults.
- **spec-author** writes the spec.
- **product-prover** reviews it.
- **design-reviewer** judges the design behind it.
- **build-pipeline** ships the change.
- **test-author** derives the matrix and writes the tests.
- **communicator** carries the work to the human.
- **feedback-intake** files what comes back.
- **feedback-collector** offers a rare private note up to the authors.
- **text-audit** reads a text as a stranger and repairs where they stop.
- **publish** runs the checks a publication owes its reader.
