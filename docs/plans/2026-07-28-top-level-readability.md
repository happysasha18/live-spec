# Plan — make the spec buildable from its own text

## Who reads this document

The agent that builds from it. `PRODUCT_SPEC.md` is loaded by the working session, by the prover that
reviews it, and by a host's agent at adoption. Alexander reads a requirement now and then. The everyday
reader is a model.

## What goes wrong today, measured

On 2026-07-27 a fresh agent with no other context was given six requirements from this spec and asked to
implement them. The result:

- it implemented **two** from the text alone;
- for **one** it wrote down the questions the text left open and built nothing;
- **three** it did not attempt, because they depend on lists and on default values the text gives
  nowhere.

A model does not stop when a text is unclear. It guesses, and the wrong thing gets built. Two of six is
the number this work moves.

## The test this plan is measured by

Hand ten requirements to a fresh agent with no other context. Count how many it implements without
asking a question. Today that count is 2 in 6.

The count is taken before and after each batch, on the same requirements, by two different fresh agents.

## What has to be fixed, and in what order of importance

The rules this project holds its own writing to are 53, of which 42 bind the spec body. They fall into
six families. The first two are what stop an agent from building; the rest make the text hold together.

### 1. Nothing is left hanging — this is what blocks a build

| rule | the defect |
|---|---|
| r07 | a set named by a count, a pointer, or a position instead of its members |
| r33 | a relational word with an empty slot: larger than what, sufficient for what |
| r06 | a number standing with no ground |
| r32 | a judgment with no judge and no measure: who decides, against what |
| r40 | a conditional leaving a case unaccounted for |
| r62 | a sentence open to two readings |
| r34 | a hole in the source closed by an invention |

### 2. Every word is explained before it is used

| rule | the defect |
|---|---|
| r21 | a domain noun with no glossary entry |
| r01 | an ordinary word carrying a private project meaning |
| r35 | a term defined in place inside a criterion |
| r02 | a coined, loan-translated, or respelled word where a standard word exists |

### 3. One sentence carries one thought

| rule | the defect |
|---|---|
| r08 | a sentence past its word cap, carrying more than one rule, more than one subordinate clause, or a pile-up of participial phrases |
| r37 | a criterion carrying more than one trigger or more than one response |
| r44 | a paragraph carrying more than one point |
| r45 | a long flat run of peer items with no grouping over them |

### 4. Every sentence has an actor and a finished action

| rule | the defect |
|---|---|
| r26 | a sentence with no actor, or its action buried in a noun |
| r36 | a criterion closing on a phrase with no finite verb |
| r39 | a pronoun with no antecedent in its own sentence |
| r05 | an action given to a subject that cannot perform it |
| r30 | a rule narrated in the future tense |
| r24 | a normative sentence in the wrong person |

### 5. Nothing extra

| rule | the defect |
|---|---|
| r41 | an example restating a rule that was already clear |
| r56 | one fact stated a second time in another place |
| r15 | a word inflating a statement while adding nothing |
| r12 | a word grading how important or how good a thing is |
| r29 | a sentence reassuring or inviting the reader |
| r31 | a birth-story standing inside a normative sentence |
| r27 | an opener saying what a thing is not |
| r10 | a thing named by denying its neighbour |
| r43 | an abstraction standing where a concrete noun would do |

### 6. The page's furniture stays where it is

| rule | the defect |
|---|---|
| r11 | an internal code leading a sentence |
| r55 | an anchor, marker, heading, or literal changed by a rewrite |
| r04 | one thing answering to a second name |
| r03 | a name stacking two nouns with no relation between them |
| r23 | a word standing in all capitals |
| r09 | a text breaking a rule it states |
| r19 | an owner or personal name inside a shipped artifact |
| r18 | the wrong language for the surface |
| r20 | English that reads as compressed or poetic |

The full text of every rule, with its reader test and its exceptions, is `docs/language-rules.md`,
generated from `guardrails/language-rules.json`.

## What it looks like

A real acceptance criterion from the spec today, at 72 words, carrying four separate rules in one
sentence:

> 3. The system *shall* red a branch whose merge-base sits behind main's tip in the merge-base check,
> red a lane worktree or a lane branch carrying no open queue row and a primary tree that does not hold
> main in the config-health check, red a host whose project instructions carry no worktree line in the
> adoption gate, and red a lane opened past the cap in the board's lane-count check. [T-23, INV-150]

The same criterion after the fixes:

> 3. The system *shall* refuse each of the four faults below. [T-23, INV-150]
>
> - the merge-base check: a branch whose merge-base sits behind main's tip;
> - the config-health check: a lane worktree or lane branch with no open queue row, and a primary tree
>   that does not hold main;
> - the adoption gate: a host whose project instructions carry no worktree line;
> - the lane-count check: a lane opened past the cap.

Three families did the work. Family 3 split one sentence of 72 words into a line of 12 and four items.
Family 1 gave the set its members instead of the count "four faults". Family 2 removed "red", which is
this project's private word for a check that refuses something.

## What we do

The spec holds 301 requirements. Ten requirements are fixed at a time, then checked, then saved, then
the next ten.

Ten is about 250 lines. A fresh agent can hold that much and attempt a build from it, and a fix inside
those lines cannot break something a hundred lines away.

## The order

1. First, the requirements something sends a reader to: every requirement named in `README.md`,
   `OVERVIEW.md`, `adopt/ADOPT.md`, or a skill body. These are what a host's agent meets first.
2. Then the rest, worst first by the counts.

The ordered list is written once, before batch one, into `docs/audit/2026-07-28-requirement-order.md`.

## No new script is built, and here is why

The first draft of this plan opened by building a script to count family 2's first defect, a word used
before anything explains it. The idea was tested against the spec before being written: a probe over
every criterion returned 139 matches, and the visible ones are mostly false. "two minutes" is a
duration. "one of two values, confident or likely" lists its members in the same clause. A script
cannot separate a domain noun from an ordinary word, and family 1's missing lists have the same shape.

So the two families that block a build are not counted by a script. They are found by the build test:
hand the requirements to a fresh agent and count what it can implement. That test is already in this
plan and it measures the goal directly.

The four families that a script does count — 3, 4, 5, and 6 — are counted by what already exists:
`guardrails/check-criterion-readability.py` with its five arms, `scripts/spec-style-lint.py`,
`guardrails/check-weak-words.py`, and `scripts/rule-census.py` over all of them.

A real example of family 2, from Requirement 248 of the spec today:

> for a lens the prover applies, it may ask whether that lens's dual applies to the document here

The word `dual` is explained nowhere, here or in the glossary. A reading agent guesses or skips.

## What runs after each batch of ten

**1. The build test — does the text still say enough to build from.** Two fresh agents each attempt the
ten requirements from their text alone. Record how many each implements without asking a question. This
is the number the plan exists to move.

**2. The test suite — did a rewrite drop a phrase something depends on.** The suite pins exact phrases
from the spec, so a dropped phrase fails a test. Run it into a file and read the printed counts:

```
python3 -m pytest -q > <scratch>/suite.log 2>&1
tail -1 <scratch>/suite.log        # e.g. "2215 passed, 2 skipped in 116.42s"
```

The exit code alone is not the verdict. It comes back zero when the run dies before any test starts.

**3. The meaning check — did a rewrite change what a rule says.** A second agent puts the old text and
the new text side by side and reports every difference in meaning. On 27 July this caught 4 of the 7
meaning losses among 93 rewrites; the suite caught the other 3.

**4. The four structure checks.** Each one prints what it read, and that report is what is read back,
not the exit code. Their readings on 2026-07-28 before any batch:

| command | what it holds | reading today |
|---|---|---|
| `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` | every requirement keeps its Context, User Story, and criteria in named cases | 1555 criteria across 301 requirements, all well-shaped |
| `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` | the code-to-location table is built from the spec, never kept by hand | 384 codes agree, body to table |
| `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md` | every code in the spec stands in the test matrix | 391 anchors agree |
| `bash guardrails/check-freeze.sh` | the three guarded documents match their recorded baseline, so every change is deliberate | 3 files match |

**5. The counts only fall.** `python3 scripts/rule-census.py --json guardrails/rule-census.json`, and no
file's count is higher than before. A batch that raises one is wrong and is redone.

**A new script is trusted only after it refuses a bad case.** It is run against a deliberately broken
example and must report the fault, and against a correct one and must stay silent. Both runs are shown
in the batch's record.

## Batch one is a trial

Batch one runs, and then four numbers are reported before batch two starts:

- the build count before and after — how many of the ten a fresh agent could implement, each way;
- how many meaning losses the checks caught;
- what batch one cost.

The remaining batches are agreed only after those numbers exist.

## How the work survives a wiped context

Nothing is carried in anyone's head between batches. What a session needs is on disk: this page, the
ordered list, `guardrails/rule-census.json`, and git.

- A batch is saved to git before the next begins. A wipe loses at most one batch.
- Each batch is rewritten by a separate short-lived worker, briefed with the six families and the ten
  requirements and nothing else. A session soaked in this project's own vocabulary writes in that
  vocabulary, which is the defect being removed.
- The build test and the meaning check are run by other fresh workers, which is what makes them honest.
- The session running the work holds numbers and briefs only.

## What I can and cannot do

**Reliably:** run a measure and report the number · rewrite a sentence to a word limit · build a script
and prove it refuses a bad case · leave the bracket codes untouched when a check verifies them
afterwards · follow a procedure written on the page in front of me.

**Reliably only with a check watching:** keep the meaning across a rewrite. One loss in thirteen on
27 July, caught only because a test pinned a phrase and a second agent compared old with new.

**Badly:** judge my own text as a fresh reader would. Nine rounds of repairs to one page, and a fresh
reader got stuck 5 to 12 times on every round, including on sentences just repaired.

**Badly:** hold a rule by memory through a long session. The rule against translating this project's
private words into Russian is written in four places, and I broke it in this session.

**Not at all:** know that a rewrite dropped a meaning nobody ever wrote down. Where a rule's meaning
lives only in the sentence being rewritten, the rewrite is a bet.

**Not at all:** hold 301 requirements in one context. Each batch here stands alone for that reason.

## What is good about this plan

- It measures the thing that matters: how many requirements a fresh agent can build from.
- Every batch banks value. Ten requirements land buildable and stay landed.
- It fails cheaply. Four numbers from batch one decide whether the rest happens.
- It cannot quietly go backwards, because the counts on disk only fall.
- It survives a wiped context, because no step needs anyone to remember an earlier step.

## What is weak about this plan

- **It does not finish.** 301 requirements cost more than the budget allows. The plan trades finishing
  for doing the requirements a host's agent meets first. The rest stay as they are.
- **The build test is expensive.** Two fresh agents attempting ten requirements is the largest cost in
  each batch, and it is also the only honest measure of the goal. Batch one shows what it really costs.
- **The script for family 2 is an approximation.** It misses a word explained badly rather than not at
  all, and it flags a word the sentence itself makes obvious.
- **Meaning loss is reduced, never removed.** Two checks caught 7 of 7 in July, which is not proof they
  catch every one.
- **Ten per batch is a guess.** Batch one can change it.

## Where the numbers are

- `docs/audit/2026-07-28-rule-census.md` — every live document measured. 106 files, 5429 defects.
- `guardrails/rule-census.json` — the same counts as data. The file that only falls.
- `docs/audit/2026-07-28-requirement-order.md` — written before batch one.
