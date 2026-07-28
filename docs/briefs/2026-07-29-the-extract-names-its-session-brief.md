# Brief — the session extract names its session and stays out of the tree (findings F4, F5)

Written 2026-07-29 for one worker starting with an empty context. Every anchor below is named by path.

## Your job

A session's record is now read at both ends by a fresh agent. The script that feeds that agent is
`scripts/session-extract.py`, which landed tonight. It pulls the person's own turns out of one session
transcript and writes them to a compact file.

The script falls short of two promises the specification makes. It guesses which transcript it reads,
and it writes wherever the caller points it, including into this public repository.

Two findings land here: F4 and F5 of the prover record
`docs/prover/2026-07-29-night-landings-push-recheck.md`, committed at `3d1b9a2`. Read that record's
Phase 3 before you write anything. It carries the proof and the line anchors for each one.

## F4 — the run takes the newest transcript, and the criterion asks for one session's own

Criterion 10 of Requirement 303 sits at `PRODUCT_SPEC.md:2880`:

> *when* a session closes, the system *shall* run the extractor over that session's transcript before the
> handover is written. [INV-302]

The script picks by modification time instead. Line 204 reads `taken = found[-1]`, and `candidates` at
line 136 sorts the matching files with the newest last. Criterion 3 says which files are taken, and no
criterion says which one of them is read.

The prover ran `python3 scripts/session-extract.py --list` and states the result at lines 196 to 200:

> printed 183 transcripts naming this repository. Two of them were written within one minute of each
> other tonight, so the newest is decided by seconds.

Two live sessions are the normal state of this project, so this is the ordinary case. A closing session
on one lane picks up another lane's transcript, and its handover then reports another session's
decisions as its own.

### What you settle, and state in the code

Settle two questions from the repository, and write both answers into the script's own docstring:

- how a caller names the session it means, and how the closing step comes to know its own identity;
- what the run does when the answer is ambiguous or names no transcript.

The prover's proposal sits at lines 202 to 204. Give the script an option that names a session, and
match the transcript file named for that session. Refuse by name when the identity matches nothing.

Refusing with the candidates named beats guessing. A run that cannot tell two transcripts apart says so,
names what it found, and exits non-zero. A closing session then hands its own identity and gets the right
file.

Read how the transcript files are named before you choose the matching rule. The `--list` option prints
the real paths, and the naming pattern is what your option must match against.

Decide what happens where the option is absent. The current behaviour serves an operator running the
script by hand. Keep serving that person, while the closing step names its session every time.

State the selection rule as a criterion, so the document says which of many files a run reads.

## F5 — the privacy promise rests on the caller's choice of path

Criterion 8 of Requirement 303 sits at `PRODUCT_SPEC.md:2878`:

> The system *shall* write the session extract outside the repository, since a transcript holds private
> conversation. [INV-302]

Line 211 of the script writes to whatever `--out` names, and no line refuses a path under the repository
root. The ignore rule added in commit `9477afb` covers the file name shape `session-extract-*.md` alone,
at `.gitignore:32`.

So a closing agent writing `--out docs/handovers/2026-07-29-extract.md` lands the person's own turns in
the tree, and the next commit carries them to a public remote. The owner of that leak is the person whose
words it is.

The repair puts the promise in the code. Refuse an output path that resolves under the repository root,
name the path, and name the reason. The root is already computed by `default_repo()` at line 71, so the
check is short.

Resolve the path before you judge it. Judge a relative path, a symbolic link and a path holding `..` by
where each one lands.

Keep the ignore rule as the second net. Two nets over one promise is what this repository already does
elsewhere.

## The criteria you write

Requirement 303 starts at `PRODUCT_SPEC.md:2861` and carries 31 criteria in three cases. Criteria 1 to 10
hold the extract, 11 to 24 the closing step, and 25 to 31 the opening step.

Append your new criteria after criterion 31, under a case heading of your own. Inserting one after
criterion 10 renumbers every criterion above it, and three matrix rows claim ranges by number:
`R303.1..R303.10`, `R303.11..R303.24` and `R303.25..R303.31`. So appending is the road that keeps those
ranges true.

Write one criterion for the selection rule, one for the ambiguous case, and one for the refused output
path. Add more where a reader cannot derive a behaviour from the ones you wrote.

Every criterion follows the shape the requirement's other criteria carry. The keywords *when*, *while*,
*if*, *then* and *shall* sit in lowercase italics, and the invariant code trails in brackets. The code
for this requirement is INV-302. A refusal that stands down by name also carries INV-218.

## The tests

The script's tests live in `tests/test_session_extract.py`. Its helper `run` sits at line 61, and its
eight tests run from line 68 to line 167. They build a scratch transcript directory, so reuse that
fixture.

Write one test per new matrix row. Run each against the current code and see it red. Keep the red output.
Then write the fix and see it green. A test that never went red proves nothing about a defect.

Write no test that reads the person's real transcript directory. Every test stands on its own scratch
files.

## What is out of scope

Findings F1, F2 and F3 belong to another worker in this same tree. Findings F6, F7 and F8 are a taste
call for the owner, and none of them is yours.

Finding F6 touches Requirement 303 and row M-484, and it stays open. Leave that row and the handover gate
alone.

## The order of work

The method is `skills/build-pipeline/SKILL.md`, and its shared rules live in
`skills/live-spec-base/SKILL.md`. A defect enters that pipeline at the matrix step, with a test proved
red on the bug before any code exists.

Hold this order, and report each step as you finish it:

1. the new acceptance criteria into `PRODUCT_SPEC.md`, under your new case in Requirement 303;
2. new rows in `TEST_MATRIX.md`;
3. one test per new row, run and seen red against the current code;
4. the code, until every one of those tests is green;
5. the generated index and the matrix reference rebuilt, both of them last;
6. the full suite, read from its log.

The rebuilds come last because the other worker edits the same two documents. A table rebuilt early goes
stale the moment either of you touches a criterion or a row.

## The matrix rows

Row M-483 at `TEST_MATRIX.md:195` covers the extractor today, and rows M-484 and M-485 cover the closing
and opening steps. Put your new rows in that same block.

Number your new rows M-489 and M-490, and take M-491 where a third is needed. The other worker holds
M-486 to M-488, so stay inside your own numbers.

Rewrite row M-483's fact so it names the selection rule and the refused output path. That row claims the
extract is written outside this repository, and today nothing holds that claim.

Pin each row's level in its own cell. The ladder is stated at `TEST_MATRIX.md:23` to `:33`. The `string`
level covers an assertion against a shipped file or a script's output, which is where row M-483 sits.

## The rebuilds and the gates over them

Rebuild the specification index with `python3 scripts/build-index.py PRODUCT_SPEC.md -o
PRODUCT_SPEC.index.md`. The same table is embedded in the specification under `## Reference`, starting at
`PRODUCT_SPEC.md:7371`, and the two copies must match line for line.

The push gate over the index is called at `guardrails/pre-push:214`, and the equality of the two copies
is asserted by `tests/test_formal_index.py::test_committed_index_equals_embedded_table`.

Rebuild the matrix reference with `python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o <file>`
and splice the table back. Its push gate is `guardrails/check-matrix-reference.py`, called at
`guardrails/pre-push:84`.

Check the row for INV-302 in both tables after the rebuild. In the index it reads `R303.1` through
`R303.31` today and must reach your highest new criterion. In the matrix reference it reads `M-483,
M-484, M-485` and must carry every row you added.

## The other worker in this tree

Two workers run in this one folder at the same time. The other one holds findings F1, F2 and F3, which
sit on gate aa and the census.

You own these files: `scripts/session-extract.py` and `tests/test_session_extract.py`. Any new test file
of yours is yours too.

The other worker owns `scripts/rule-census.py`, `guardrails/check-doc-findings-bound.py`,
`tests/test_doc_findings_bound.py` and `tests/test_rule_census_ratchet.py`. Leave all four alone.

You both edit `PRODUCT_SPEC.md`, `TEST_MATRIX.md` and their generated tables. So three rules hold over
every edit to those four files:

- make targeted edits to the lines you mean to change, since a whole-file rewrite destroys the other
  worker's concurrent edit;
- re-read the file immediately before each edit, since its line numbers move under you;
- rebuild the generated tables last, after your final edit to either document.

## What you must not do

Commit nothing and push nothing. The session lead does that.

Re-seed `guardrails/rule-census.json` never. A re-seed is no way to make a check green, and others read
that record through the day.

Leave `JOURNAL.md`, `ROADMAP.md` and `NEXT_STEPS.md` to the session lead. Report the line each of them
owes, and let the lead write it.

Write no extract into this repository while you work. Your own scratch runs go to your scratchpad
directory, which is the behaviour you are shipping.

## The free numbers

`NEXT_STEPS.md` states the free numbers at lines 87 and 88: requirement 304, INV-303, E-36, T-25, M-486,
and queue row 526.

Your matrix rows are M-489, M-490 and M-491. Your criteria need no new requirement and no new invariant
code, since INV-302 already owns this law.

Take queue row 527 where you must park something, and say so in your report. The other worker holds 526.

The line stating the free numbers is raised in the landing's own commit, which the session lead writes.
Report which numbers you took, and leave that line alone.

## The writing standard your prose is held to

Every document this repository ships is measured. Keep each sentence at or under 25 words. Use plain
product words. Keep an internal code out of the front of a sentence, where it names nothing to a reader.
A sentence that names a thing by denying its neighbour is refused.

`PRODUCT_SPEC.md` is recorded at 1831 findings and measures 1831 findings, so it carries no headroom at
all. One over-cap sentence added there reds gate aa on the next push. `TEST_MATRIX.md` stands at 76.

Measure every document you edited with `python3 scripts/rule-census.py <file>`, and report the count
beside the count that stood before your edit.

## The checks that close the work

Run each command from the repository root and record what it printed:

1. `python3 scripts/rule-census.py PRODUCT_SPEC.md TEST_MATRIX.md`
2. `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md`
3. `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md`
4. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md`
5. `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md`
6. `python3 guardrails/check-doc-findings-bound.py`
7. `python3 guardrails/check-handover-provenance.py`
8. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is
no test result, so quote the log.

## What done means

Report these eight things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- the two settled questions from F4, with the answer you chose for each and what in the repository
  settled it;
- the transcript naming pattern you matched against, quoted from a real path;
- the new criteria as they now stand, quoted from the specification, under the case heading you gave
  them;
- the new matrix row ids, the level each pins, and the words you changed inside row M-483;
- the name of each new test, its red output before the code, and its green output after;
- the refusal an in-tree output path now produces, quoted from a real run;
- the full-suite counts quoted from the suite log, and the census count for every document you edited
  beside the count it held before.

Report anything you found and left alone. Report the lines `JOURNAL.md`, `ROADMAP.md` and `NEXT_STEPS.md`
owe, in the words you would have written into each.
