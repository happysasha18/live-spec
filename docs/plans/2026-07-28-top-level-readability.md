# Plan — the top-level documents read for a stranger

Written 2026-07-28 on Alexander's instruction, to be executed by a session starting with a clean
context. Everything the executing session needs is on this page: the goal, the order, the commands, the
self-checks, and the stopping rule. It needs no other file to begin.

## The goal, stated as a test

A person who has never seen this project opens ONE requirement of `PRODUCT_SPEC.md`, one node of
`ARCHITECTURE.md`, one row of `ROADMAP.md`, or one case of `TEST_MATRIX.md`, and acts on it without
asking anyone a question.

The unit is one requirement. Nobody reads 7599 lines; a reader reads the requirement they were sent to.

## What the previous attempt proved, so it is not repeated

The night of 2026-07-27 rewrote 93 acceptance criteria, then ran nine cold readings of one 340-line
page. Blocking stops went 11, 8, 12, 6, 5, 5, 6, 5, 8 and never reached zero. Three findings stand:

- **The reading unit was too big.** Each repair added words, and the next reader stopped where the new
  words met the old. A repair could open a fresh stop a hundred lines from the one it answered.
- **The measure and the reader disagreed.** The measures count sentence length. The readers stopped on a
  load-bearing noun used before the text grounds it. Repairing the measured thing left the read thing
  standing.
- **Rewriting loses meaning at about one in thirteen.** Seven of the 93 rewrites lost meaning: the suite
  caught three, an independent read caught four. A rewriting pass without both readings ships silent
  defects.

## The seven rules, and the measure of each

| # | rule | measure |
|---|---|---|
| 1 | One sentence carries one rule and stays under its surface's word cap | 35 words for a criterion, 25 for prose — `guardrails/check-criterion-readability.py` arm A |
| 2 | A term is defined in the glossary before the body uses it | `guardrails/check-vocabulary.py` |
| 3 | No definition stands inside a criterion | arm B of the readability check |
| 4 | A sentence closes on a clause carrying a finite verb | arm C |
| 5 | Codes trail at the line's end and never lead a sentence | arm D |
| 6 | A sentence naming a set gives that set's members | `guardrails/check-weak-words.py`, and the reader |
| 7 | A requirement grounds its load-bearing noun inside its own Context block | **step 1 builds this check** |

## Step 1 — give rule 7 a machine, before any rewriting

Rule 7 is what readers actually stop on, and today only a paid reading finds it. It is mechanical:

> For each requirement, take every glossary term used in its User Story and its acceptance criteria.
> A term that appears nowhere in that requirement's own Context block is ungrounded.

Build `guardrails/check-noun-grounding.py`:

- input: `PRODUCT_SPEC.md`, its glossary section, and its 301 requirement blocks;
- output: per requirement, the ungrounded terms, with a total count;
- it is red-proven on a fixture requirement that uses a glossary term its Context omits, and silent on
  one that grounds every term;
- its count per file joins `guardrails/rule-census.json` as a sixth measure.

This turns the expensive reading into a free count and gives the batches their real ordering.

## Step 2 — order the requirements by who is sent to them

Two keys, in this order:

1. **Inbound pointers.** A requirement something points a reader at is rewritten first. Collect them:
   `grep -oE '\b(INV|E|T|M|ACT|B|S)-[0-9]+' README.md OVERVIEW.md adopt/ADOPT.md docs/*.md skills/*/SKILL.md`
   and map each code to its requirement through `PRODUCT_SPEC.index.md`.
2. **Score.** Everything else falls in worst-first order by the six measures.

The ordered list is written to `docs/audit/2026-07-28-requirement-order.md` before batch one.

## Step 3 — the batch loop

One batch is **ten requirements**. Per batch:

1. Record the six measures for those ten requirements. This is the "before" number.
2. Rewrite them in one pass against the seven rules. The rewriting session works from the rules and the
   requirement text, and holds the bracket codes untouched.
3. **Self-check A — meaning.** The bracket-code set of each requirement is identical before and after,
   or every difference is named in the delivery note. Run `python3 scripts/spec-freeze.py --check`.
4. **Self-check B — the suite.** `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the log's
   own summary line. A green exit code is not the verdict; the printed counts are.
5. **Self-check C — the gates.** `bash guardrails/run-all.sh` (or the pre-commit gate the host wires),
   and every gate's reach line is read, not only its exit code.
6. **Self-check D — the numbers only fall.** Re-run `python3 scripts/rule-census.py --json
   guardrails/rule-census.json` and confirm no file's count rose.
7. **Self-check E — a reader.** A fresh reader with no context reads the ten rewritten requirements
   alone, about 250 lines, under the prompt in `skills/text-audit/SKILL.md`. Two consecutive readings
   with no blocking stop close the batch. A batch failing twice is re-cut rather than patched again.
8. Commit the batch on its own, with the before-and-after numbers in the message.

## Step 4 — the pilot decides the rest

**Batch one is a pilot and its numbers are reported before batch two starts.** Report: how many readings
batch one needed, how many meaning losses the two guards caught, and what the batch cost. The remaining
batches are committed to only after those three numbers are in hand.

This exists because the two-clean-readings bar has never yet been met on this project's own text. The
pilot measures whether a 25-line unit meets it.

## The honest total, so the work can be stopped

`PRODUCT_SPEC.md` holds 301 requirements — about 30 batches. The 2026-07-27 night, which was one
rewriting pass plus nine readings, consumed a large share of a weekly budget. Thirty batches at that
rate exceed the budget by a wide margin, so **finishing all 301 is not the commitment.** The commitment
is: the requirements a reader is actually sent to, in order, banking value at every batch, stopping on
the owner's word with everything landed still landed.

## Out of scope, said plainly

Document SIZE is a different axis. `PRODUCT_SPEC.md` is 651 KB because it holds 301 requirements, and
compaction is not this plan.

The skill bodies, the reader docs, and the templates carry 3143 of the census's 5429 findings. They wait
until the top-level documents are done.

## What I can actually do, said honestly

**Reliable.** Running a measure over a file and reporting the number. Rewriting a sentence to a stated
word cap. Building and red-proving a check. Holding bracket codes untouched across a rewrite when the
codes are checked afterwards. Following a written procedure when the procedure is on the page in front
of me.

**Reliable only with a guard.** Keeping meaning across a rewrite: measured at one loss in thirteen on
2026-07-27, caught only because a test pinned a phrase and an independent read looked. Every batch needs
both guards, and neither is optional.

**Unreliable.** Judging my own text as a reader would. I wrote nine rounds of repairs to one page and a
fresh reader stopped 5 to 12 times on every one of them, including on the sentences I had just repaired.
I cannot stand in for the cold reader; the reading has to be run by a session that has not seen the text.

**Unreliable.** Holding a rule by habit across a long session. The rule against loan-translating this
project's words into the working language is written in four places and I broke it in this very session.
A rule reaches the work through a check or through a fresh short-context worker, and never through my
memory of it.

**Impossible.** Knowing whether a rewrite lost a meaning nobody wrote down. Where a criterion's meaning
lives only in the sentence being rewritten, the rewrite is a bet. This is why the pilot batch reports
its meaning-loss count before the rest is committed to.

**Impossible.** Holding 301 requirements in one context. Any plan that needs me to remember batch three
while doing batch seventeen fails. The plan is built so each batch stands alone.

## Built for a context that gets wiped

Every batch is a closed unit: its inputs are this page, the ordered list, and the ten requirements it
touches. Nothing carries from one batch to the next except committed files and numbers on disk.

- **The state lives on disk, never in a session.** `guardrails/rule-census.json` holds the counts,
  `docs/audit/2026-07-28-requirement-order.md` holds the order, and git holds the text. A session that
  starts cold reads those three and knows where the work stands.
- **A batch commits before the next begins.** A wipe mid-batch loses at most one batch, and the counts on
  disk say which one.
- **The rewriting is done by a fresh short-context worker**, briefed with the seven rules, the ten
  requirements, and nothing else. This follows the rule that a marinated session writes in the project's
  own private vocabulary — the defect this whole movement exists to remove. The briefing session must
  not also be the writing session.
- **The reading is done by another fresh worker**, which is what makes it a cold reading at all.
- **The briefing session holds no text.** It reads numbers, writes briefs, and accepts results. This is
  what keeps its context small enough to survive thirty batches.

## What this plan is good at

- **It banks value at every batch.** Ten requirements land readable and stay landed, whatever happens next.
- **It measures the thing readers stop on.** Step 1 gives rule 7 a machine, so the ordering stops
  optimizing sentence length while readers stop on ungrounded nouns.
- **It fails cheap.** The pilot reports three numbers before the other 29 batches are committed to.
- **It cannot silently regress.** The census counts on disk only fall, and a check refuses a push that
  raises one.
- **It survives a wiped context**, because no step needs a session to remember an earlier step.

## What this plan is weak at

- **It does not finish.** 301 requirements at this rate exceed the budget. The plan explicitly trades
  completeness for a reader-path ordering, so the tail stays unrewritten and the census will show it.
- **Rule 7's check is an approximation.** A glossary term absent from a Context block is a good proxy for
  an ungrounded noun, and it will miss a noun that is grounded badly rather than not at all, and will
  flag a term whose meaning the sentence itself makes plain.
- **The two-clean-readings bar is unproven on a 25-line unit.** The pilot is the first evidence either
  way. If a 25-line unit also fails to converge, this plan needs a different bar and the pilot is where
  that shows.
- **Meaning loss is bounded, never eliminated.** Two guards caught seven of seven last time, which is not
  proof they catch all of them.
- **A batch of ten is a guess.** Small enough to read, large enough to be worth a landing — chosen, not
  measured. The pilot can move it.

## Where the numbers live

- `docs/audit/2026-07-28-rule-census.md` — every live document measured, 106 files, 5429 findings.
- `guardrails/rule-census.json` — the same counts as data, which is the limit that only falls.
- `docs/audit/2026-07-28-requirement-order.md` — written by step 2, the order the batches run in.
