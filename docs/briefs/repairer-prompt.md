# Repairer prompt — repair one document from the sources it rests on

Hand this file to a fresh worker, word for word, with the three paths below filled in.

## What the caller fills in

- Document path: `<the document to repair>`
- Stop list path: `<the reading report that holds the stops>`
- Report path: `<the file where the repair record is written>`

## Your job

You repair every blocking stop in the stop list.

Each fix comes from the material the document already rests on. You invent nothing.

## What you read first

Read all four of these before your first edit:

- the document at the document path, from its first line to its last;
- the stop list at the stop list path;
- `guardrails/language-rules.json`, the one home of this project's writing rules;
- `docs/language-rules.md`, which prints each rule with its examples and its exceptions.

## Where a fix comes from

Every fix comes from a source the document already rests on. These are the sources:

- `PRODUCT_SPEC.md` for a defined term and for a stated requirement;
- `ARCHITECTURE.md` for a component, a mechanism, and a boundary between components;
- `TEST_MATRIX.md` and the files under `tests/` for the behaviour a test pins;
- `DECISIONS.md` and `JOURNAL.md` for a decision the project already took;
- the script or the skill a sentence describes, for what that script or skill does.

Four kinds of stop take four kinds of fix:

- a term takes the definition its source gives it, written at the term's first use;
- a relational word takes the reference point or the measure its source names, written where the word stands;
- a judgment takes its judge and its inputs from the source that decides the judgment;
- a claim takes its ground stated in the sentence, or the claim shrinks to what the source supports.

Name the source for every fix you make. The repair record carries that name.

## When no source holds the answer

Sometimes every source stays silent. That stop is a real hole in what the project has decided.

Record a question, and leave the document honest about the hole:

- put an inline note `[GAP: what is missing]` at the spot in a specification file;
- put a bracketed query at the spot in a README, a skill body, an article, or a piece of copy;
- list the question in the repair record, under the heading for open questions.

Inventing an answer is the one move this work forbids. An invented sentence reads clean to the next reader, and the project then stands behind something no source states.

## Non-blocking stops

Repair the blocking stops.

Copy each non-blocking stop into the repair record under its own heading, and leave that text as it stands. The person who owns the document decides those.

## What survives a rewrite byte for byte

A machine reads some of the marks in this document. Each mark below stays exactly as it stands today:

- every heading, at its level and in its words;
- every anchor in square brackets, such as `[INV-241]` or `[E-24]`;
- every requirement number, and every list number a table points at;
- every code identifier, file path, command name, and function name;
- every phrase a test quotes, and every phrase the generated index quotes;
- every fenced block holding a command, a prompt to paste, or a sample of output.

Moving one of these marks breaks the code-to-location table, the test matrix, or a test. Repair the prose around such a mark, and leave the mark itself alone.

## The writing rules this repair is held to

The full set of 59 rules lives in `guardrails/language-rules.json`, and every sentence you write obeys all of them.

These twelve settle most repairs:

- one sentence carries one rule, holds at most one subordinate clause, and stays at or under 25 words;
- one paragraph carries one point, stated in its first sentence, with the rest supporting that point;
- every sentence says what a thing is, in its own words, and a boundary worth naming takes its own plain sentence;
- every term is defined at its first use, or the document names the file that defines the term;
- one thing carries one name in every sentence of the document;
- one fact lives in one place, and every other place points at that place;
- every rule sentence names its actor, runs in the active voice, and keeps its action in a verb;
- every judgment names its judge and its measure;
- every relational word fills the slot it opens, right where the word stands;
- every number says what it counts, what it is measured against, and which direction is better;
- an internal code trails at the end of its line, inside square brackets;
- every word stands in ordinary case, and an acronym or a code identifier passes.

Use the everyday word wherever an everyday word carries the meaning. A term of the profession stays as it is, and the words around that term become everyday words.

Repeat the name of a thing in each sentence about that thing. A pronoun stands only where the name would clutter the sentence.

## The meaning stays

A repair changes the wording and keeps the claim.

Put the old sentence and the new sentence side by side before you accept a fix. Record any repair that changes what the document claims, and name the source that authorises the change.

## The checks that close the repair

Run each command below from the repository root after your last edit, and record what each one printed:

1. `python3 scripts/rule-census.py <document path>`, whose total for the file reads zero.
2. `python3 scripts/spec-style-lint.py --tier full <document path>`, which reports clean.
3. `python3 scripts/preshow-register-lint.py <document path>`, which reports clean.
4. `python3 guardrails/check-one-name.py <document path>`, which reports clean.

Three further checks read a document written as a specification, with a glossary and numbered acceptance criteria. Run all three on such a document, and record what each printed:

5. `python3 guardrails/check-vocabulary.py <document path>`, which reports clean.
6. `python3 guardrails/check-weak-words.py <document path>`, which reports clean.
7. `python3 guardrails/check-requirement-shape.py <document path>`, which reports clean.

Each of those three refuses on a README, a skill body, or an article. A refusal there says the document holds no glossary and no criteria, so record the refusal and move on.

Run `python3 -m pytest -q` as well when a test quotes the repaired document. Record the counts the suite printed.

A check reporting a finding calls for one more repair pass. Repair the finding, then run every command above again.

## Where the report goes

Write the repair record to the report path named at the top of this prompt, in this shape:

- a first line naming the document path, the stop list path, and the date;
- one line per repaired stop: the stop number, the old phrase quoted, the new phrase quoted, and the source of the fix;
- a heading for open questions, holding every stop that no source answered;
- a heading for non-blocking stops, holding every stop you left alone;
- the printed result of each check above;
- a closing line carrying the census total for the document.

Edit the document in place. The repair record is the one new file you create.
