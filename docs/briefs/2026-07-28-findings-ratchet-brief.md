# Brief — the findings record moves down alone (Requirement 302, finding F1)

Written 2026-07-28 for one worker starting with an empty context. Every anchor is named below by path.

## Your job

This repository records one writing-defect count per document in `guardrails/rule-census.json`. The law is that a recorded count moves down alone. A document repaired to zero stays at zero, and no recorded number ever rises.

Gate aa holds that law over the documents. The record itself is held by nothing. Close the hole from both sides: the path that writes the record, and the path that edits it by hand.

## Where the hole is today

The gate is `guardrails/check-doc-findings-bound.py`. It measures every live document, compares each count against the record, and refuses the push on a rise.

The write path is `scripts/rule-census.py`. Its `--json` branch sits in `main` at lines 281 to 287. Line 284 writes `{r["file"]: r for r in rows if "unread" not in r}`, which stores whatever the text measures today. A risen number is stored with the rest.

The gate prints that same command as its own remedy, at `guardrails/check-doc-findings-bound.py:101` and again at line 110. So an operator whose push was refused holds, inside the refusal, the one command that turns the refusal into a pass.

The full reasoning is the prover record at `docs/prover/2026-07-28-requirement-302-findings-ratchet.md`, finding F1, lines 132 to 162.

## What is in scope

Finding F1 alone lands in this pass.

Read finding F7 at lines 270 to 290 of the prover record, and the "Top three to fold" section at lines 437 to 444. Both are context. Neither is yours to build here. Leave criterion 5 of Requirement 302 as it stands.

## The three criteria to land, word for word

These three sentences come from the prover record at lines 152 to 156. Copy them as they stand. Do not reword them.

> 9. No run *shall* raise a recorded count. [INV-301]
> 10. *when* the census writes the record and no live document stands above its recorded count, the system *shall* write each measured count back. [INV-301]
> 11. A raised recorded count *shall* be a hand edit to the record stating its reason, run through this same pipeline. [INV-301]

Each of the three sits at or under the 25-word cap already. Measure them again after you paste them.

## Where the criteria land

Requirement 302 starts at `PRODUCT_SPEC.md:7279` and its criteria run from line 7289 to line 7304. The criteria end at number 8, so the three new ones keep the numbers 9, 10 and 11.

Give them a case heading of their own, above criterion 9. The model is Requirement 297, whose case "the counts move only down" sits at `PRODUCT_SPEC.md:7110` over criteria 13 to 18. Read that case before you write yours, because it is the same law over a different record.

## The reason field already exists here

Requirement 245 governs the growable documents, and its own bound file is `guardrails/doc-bounds.json`. Each entry there carries a `reason` field holding a sentence of prose.

Its gate reads that field at `guardrails/check-doc-bound.py:95` and refuses an entry whose reason is empty, at lines 97 to 100. Follow that shape. Invent no second shape for the same idea.

## The two arms to build

**The writing arm.** The census refuses to write a record entry whose count stands above the count already recorded at that path. It names every document standing above its record, and it writes nothing at all in that case. This is criteria 9 and 10.

**The hand-edit arm.** Something reads `guardrails/rule-census.json` against its committed version and refuses a raised count that carries no reason beside it. This is criterion 11.

Once both arms stand, the command the gate prints at line 101 becomes honest. That command can then lower a number and never raise one.

## The design points you settle yourself

Four questions have no answer in the prover record. Settle each one, and state your answer in the code's own docstring.

- A re-seed rewrites every entry. A `reason` written by hand must survive that rewrite, or the hand-edit path is erased by the next census run.
- The hand-edit arm needs a home. The cheapest home is gate aa itself, which keeps one gate letter for one law. A new gate letter owes an entry in `guardrails/gate-red-proofs.json`, whose gate aa entry sits at lines 104 to 107.
- Reading the committed version of a file means asking git. Decide how, and decide what the arm does where git answers nothing.
- A record file that did not change between two runs must stay silent. A gate that reds on an unchanged tree blocks every push in the repository.

Where a criterion must carry one of these answers, add it as an indented bullet under criterion 11. Leave the three criterion lines themselves untouched.

## The order of work

The method is `skills/build-pipeline/SKILL.md`, and its shared rules live in `skills/live-spec-base/SKILL.md`. A defect enters that pipeline at the matrix step, with a test proved red on the bug before any code exists.

Hold this order, and report each step as you finish it:

1. The three acceptance criteria into `PRODUCT_SPEC.md`, under their new case.
2. The generated index rebuilt, both copies of it.
3. New rows in `TEST_MATRIX.md`, and the matrix Reference rebuilt.
4. A test per new row, run and seen red against the current code.
5. The code, until every one of those tests is green.
6. The full suite, read from its log.

## The matrix rows

Row M-479 covers gate aa today. It sits at `TEST_MATRIX.md:587`, inside the block `### [node: guardrails [target]]` that opens at line 529. Put the new rows in that same block.

The highest row id in the document is M-479, so number the new rows from M-480 upward. New behaviour owes new rows, and the old row keeps the behaviour it already covers.

Pin each row's level in its own cell. The matrix's level ladder is stated at `TEST_MATRIX.md:27` to `:33`. The `string` level covers an assertion against a shipped file or a script's output. The `browser-computed` level covers a fact a real git must compute on a live repository.

Rebuild the matrix Reference with `python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o <file>` and splice the table back. The push gate over it is `guardrails/check-matrix-reference.py`, called at `guardrails/pre-push:84`.

## The tests

The gate's tests live in `tests/test_doc_findings_bound.py`. Its `seed` helper at line 28 builds a one-document tree and a record naming that document's ceiling. Reuse it.

A test over the census write path can take a new file beside `tests/test_rule_census_prose_units.py`.

One rule holds over every test you write: no test may write `guardrails/rule-census.json`. A test that re-seeds the real record destroys the record for everyone else working today.

Note one difference between the two scripts. The gate takes `--root` and `--record`, and the census takes neither. The census measures the repository root or the paths named on its command line. Give a test a scratch record path and positional document paths, or add a `--root` option to the census for parity with the gate.

## The spec index

Adding criteria changes the code-to-location table. The row for INV-301 reads `R302.1` through `R302.8` today and must reach `R302.11`.

Rebuild it with `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md`. The same table is embedded in the spec under `## Reference`, starting at `PRODUCT_SPEC.md:7307`, and the two copies must match line for line.

The push gate is called at `guardrails/pre-push:214`, and the equality of the two copies is asserted by `tests/test_formal_index.py::test_committed_index_equals_embedded_table`.

## What you must not touch

Another worker is editing three files in this same tree right now: `hooks/chat-law-hook.sh`, `tests/test_chat_law_hook.py`, and `docs/language-reads/2026-07-28-read16-chat-law-hook.md`. Leave all three alone.

Make every change as a targeted edit to the lines you mean to change. A whole-file rewrite in a shared tree destroys another worker's concurrent edit.

Commit nothing and push nothing. The session lead does that.

Re-seed `guardrails/rule-census.json` never. Others re-seed it through the day, and a re-seed is not a way to make a check green.

Leave `JOURNAL.md` and `ROADMAP.md` to the session lead. Report the line each of them owes, and let the lead write it.

## The writing standard your prose is held to

Every document this repository ships is measured. Keep each sentence under 25 words. Use plain product words. Keep an internal code out of the front of a sentence, where it names nothing to a reader. A sentence that names a thing by denying its neighbour is refused.

The spec is recorded at 1831 findings and measures 1831 findings, so it carries no headroom at all. One over-cap sentence added to `PRODUCT_SPEC.md` reds gate aa on the next push. The matrix is recorded at 76.

Measure your own prose before you report, with `python3 scripts/rule-census.py <file>` over each document you changed. The count it prints must be the count that stood before your edit.

## The checks that close the work

Run each command from the repository root and record what it printed:

1. `python3 scripts/rule-census.py PRODUCT_SPEC.md TEST_MATRIX.md`
2. `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md`
3. `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md`
4. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md`
5. `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md`
6. `python3 guardrails/check-doc-findings-bound.py`
7. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log.

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is not a test result, so quote the log.

## What done means

Report these six things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- the three criteria as they now stand in the spec, quoted from the file;
- the new matrix row ids and the level each one pins;
- the name of each new test, its red output before the code, and its green output after;
- the full-suite counts quoted from the suite log;
- the census count for every document you edited, beside the count it held before.

Report the four design points you settled, with the answer you chose for each. Report anything you found and left alone.
