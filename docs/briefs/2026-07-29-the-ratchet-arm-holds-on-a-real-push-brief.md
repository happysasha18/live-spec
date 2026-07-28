# Brief — the ratchet's second arm holds on a real push (findings F1, F2, F3)

Written 2026-07-29 for one worker starting with an empty context. Every anchor below is named by path.

## Your job

This repository records one writing-defect count per document in `guardrails/rule-census.json`. The law
is that a recorded count moves down alone. Gate aa holds that law, and its second arm holds the record
itself against a hand raise.

That second arm reports nothing on a real push. Make it hold on the push. Prove it with a test
that walks the push's own path. State it in the specification. Then close one neighbouring hole in the
census write path.

Three findings land here: F1, F2 and F3 of the prover record
`docs/prover/2026-07-29-night-landings-push-recheck.md`, committed at `3d1b9a2`. Read that record's
Phase 3 before you write anything. It carries the proof, the probe and the line anchors for each one.

## F1 — the arm compares the wrong two copies

Gate aa is `guardrails/check-doc-findings-bound.py`. Its second arm landed hours ago. It reads
`guardrails/rule-census.json` on disk, asks git for the copy `HEAD` holds, and refuses an entry whose
recorded count rose with no reason beside it.

The two copies it compares are the working folder and `HEAD`. The gate runs from
`guardrails/pre-push:232` and from `.github/workflows/gates.yml:100`. At both of those moments the raise
is already committed, so the two copies agree and the arm reports nothing.

The prover proved it on a scratch repository. A record was committed with `total` 0, raised by hand to 9
with no reason, and committed again. The gate printed this, quoted from the prover record at lines 131
to 134:

> The gate printed "fell: CLEAN.md — recorded 9, measured 0" and then "OK (doc-findings-bound): 1 live
> documents", exit 0.

So the arm reaches an uncommitted edit alone, and a push never carries one. The arm is protection in
name on the one path that matters.

The reading of the arm's own code sits at `guardrails/check-doc-findings-bound.py:83` to `:123`. The
function `committed_record` asks git, and `hand_raises` compares the two dictionaries. The docstring
states the current design at lines 28 to 51, and it must state your new design when you are done.

### What you settle, and state in the code

The honest anchor for a gate on the push chain is the state the remote already holds. So the comparison
reaches for the upstream branch.

Settle these four questions from the repository, and write each answer into the gate's own docstring:

- how this repository names the state the remote holds, and how a run resolves it;
- what the arm does where no such state is reachable, which covers a fresh clone, a machine with no
  network, and the first push of a new branch;
- how the continuous-integration mirror answers the same question, since it runs the same gate;
- whether a record identical to the reachable copy stays silent, which it must, because a gate that reds
  on an unchanged tree blocks every push here.

The precedent for resolving that state is `guardrails/check-prover-record.sh:40` to `:49`. It reads a
ladder: the environment value `LIVE_SPEC_DIFF_BASE` when it resolves to a commit, then `origin/main`,
then `HEAD~1`. The continuous-integration run passes the event's base commit into that environment
value. Read the whole passage before you choose, and follow what you find there.

The precedent for the unreachable case is the arm's own current behaviour. It stands down by name and
says what it read nothing of, which is the shape invariant INV-218 carries. Keep that shape for every
case where the reachable copy cannot be found.

### The test that walks the real path

The test behind the arm today stands on the wrong tree. The prover states it at lines 133 to 134:

> The fixture behind M-482 raises the count in the working tree and never commits it. The test and the
> running gate therefore stand on different trees.

Those tests are `test_a_raised_recorded_count_with_no_reason_reds` and its three neighbours, at
`tests/test_doc_findings_bound.py:122` to `:151`. Their fixture helper `seed` sits at line 54.

Write a test that walks the push's own path in a scratch repository:

1. a record committed with a count;
2. that count raised by hand with no reason, and committed;
3. a reachable copy of the record that lacks the raise, standing where a remote's copy would stand;
4. the gate run, and its refusal read from its output.

Run that test against the current code and see it red. Keep its red output. Then write the fix and see
it green. A test that never went red proves nothing about a defect.

Write a second test for the lawful raise on the same path, where the entry carries a reason and the gate
passes. Write a third for the unreachable case, where the arm stands down by name.

Leave the four existing tests in place. They cover the working-folder shape, and the row keeps the
behaviour it already covers.

## F2 — the specification states no arm at all

No acceptance criterion of Requirement 302 states this arm. Criterion 11's third bullet says "the arm",
and no criterion before it names one. A reader meets a subject the document never introduced.

Requirement 302 starts at `PRODUCT_SPEC.md:7331`. Its criteria run to number 11. Criterion 11 and its
three bullets sit at lines 7365 to 7368, under the case "the record moves only down".

Row M-482 at `TEST_MATRIX.md:593` meanwhile claims a whole blocking machine. So a gate arm that refuses
a push rides the chain with no clause behind it.

Write the criteria that state the arm. The prover proposes one sentence at lines 158 to 161:

> *if* a recorded count stands above the count the base commit holds and carries no reason, *then* the
> system *shall* refuse the push.

Take that sentence as your starting point and adjust it to whatever you settled for F1. The words must
match the machine you shipped, so a sentence naming a state the gate never reads is a defect of its own.

Number the new criteria from 12 upward, inside the same case. The case ends the requirement, so nothing
after it renumbers.

Move criterion 11's third bullet under the new criterion, where its subject now exists. Criterion 11
then carries the hand-edit rule and its two remaining bullets.

Add the criteria the four settled questions need. The stand-down case and the silent-unchanged case each
state a behaviour a reader cannot derive from the others.

Every criterion follows the shape the requirement's other criteria carry. The keywords *when*, *while*,
*if*, *then* and *shall* sit in lowercase italics, and the invariant code trails in brackets. The code
for this requirement is INV-301, and the stand-down clause also carries INV-218.

## F3 — the census writes the record before it knows a reading refused

This is separate code in `scripts/rule-census.py`, and it rides the same landing.

The write sits at lines 328 to 332. Line 334 then computes which readings refused, and line 335 returns
1. So a run whose lint call failed scores that reading 0, writes the 0 into the record, prints that it
wrote the file, and exits 1 afterwards. The ratchet then holds the hollow floor as the ceiling, and only
a hand edit with a reason raises it back.

The prover probed it at lines 176 to 180:

> An entry recorded at total 7 was rewritten to total 0, the run printed "wrote ...record.json", and it
> exited 1. The written entry even carries `'refused': 'the reading refused to run'`.

The repair is to compute the refusals above the write, and to write nothing at all when any reading
refused or any file went unread. That is the shape criterion 9 already gives the risen case at lines 313
to 324 of the same file.

Queue row 525 owns the neighbouring case, where a check produces no count at all and scores 0 with no
refusal. Read that row before you write. Your repair covers the refused reading, and the two want one
repair between them where one serves both.

State this behaviour as a criterion too, beside the ones you write for F2. Criterion 10 today promises a
write when nothing rose, and it says nothing about a reading that never ran.

Add a test beside `tests/test_rule_census_ratchet.py`, whose four tests sit at lines 56 to 91. Prove it
red against the current code before you write the fix.

## What is out of scope

Findings F4 and F5 belong to another worker in this same tree. Findings F6, F7 and F8 are a taste call
for the owner, and none of them is yours.

The seven open findings of `docs/prover/2026-07-28-requirement-302-findings-ratchet.md` stay where they
are. File nothing that repeats them.

## The order of work

The method is `skills/build-pipeline/SKILL.md`, and its shared rules live in
`skills/live-spec-base/SKILL.md`. A defect enters that pipeline at the matrix step, with a test proved
red on the bug before any code exists.

Hold this order, and report each step as you finish it:

1. the new acceptance criteria into `PRODUCT_SPEC.md`, under the case "the record moves only down";
2. new rows in `TEST_MATRIX.md`;
3. one test per new row, run and seen red against the current code;
4. the code, until every one of those tests is green;
5. the generated index and the matrix reference rebuilt, both of them last;
6. the full suite, read from its log.

The rebuilds come last because the other worker edits the same two documents. A table rebuilt early goes
stale the moment either of you touches a criterion or a row.

## The matrix rows

Put the new rows in the block `### [node: guardrails [target]]`, which opens at `TEST_MATRIX.md:532`.
Row M-482 at line 593 covers the arm today, and rows M-479 to M-481 cover its neighbours.

Number your new rows M-486, M-487 and M-488. The other worker takes M-489 upward, so stay inside your
three. Take fewer where fewer serve, and leave the gap.

Rewrite row M-482's fact so it names the state the arm now compares against. The words "as HEAD holds
it" stand in that row twice, and both are wrong once your fix lands.

Pin each row's level in its own cell. The ladder is stated at `TEST_MATRIX.md:23` to `:33`. The `string`
level covers an assertion against a shipped file or a script's output. The `browser-computed` level
holds a fact a real git must compute on a live repository, which is where row M-482 already sits.

## The rebuilds and the gates over them

Rebuild the specification index with `python3 scripts/build-index.py PRODUCT_SPEC.md -o
PRODUCT_SPEC.index.md`. The same table is embedded in the specification under `## Reference`, starting at
`PRODUCT_SPEC.md:7371`, and the two copies must match line for line.

The push gate over the index is called at `guardrails/pre-push:214`, and the equality of the two copies
is asserted by `tests/test_formal_index.py::test_committed_index_equals_embedded_table`.

Rebuild the matrix reference with `python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o <file>`
and splice the table back. Its push gate is `guardrails/check-matrix-reference.py`, called at
`guardrails/pre-push:84`.

Check the row for INV-301 in both tables after the rebuild. It reads `M-479, M-480, M-481, M-482` today
and must carry every row you added.

## The other worker in this tree

Two workers run in this one folder at the same time. The other one holds findings F4 and F5.

You own these files: `scripts/rule-census.py`, `guardrails/check-doc-findings-bound.py`,
`tests/test_doc_findings_bound.py` and `tests/test_rule_census_ratchet.py`. Any new test file of yours
is yours too.

The other worker owns `scripts/session-extract.py` and `tests/test_session_extract.py`. Leave both
alone.

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

Write no test that writes the real `guardrails/rule-census.json`. A test that re-seeds the live record
destroys it for everyone else working today.

## The free numbers

`NEXT_STEPS.md` states the free numbers at lines 87 and 88: requirement 304, INV-303, E-36, T-25, M-486,
and queue row 526.

Your matrix rows are M-486, M-487 and M-488. Your criteria need no new requirement and no new invariant
code, since INV-301 already owns this law.

Take queue row 526 where you must park something, and say so in your report. The other worker takes 527
if it needs one.

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
7. `python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the counts out of that log

Write the suite log to your scratchpad directory. Read its last line for the counts. An exit status is
no test result, so quote the log.

## What done means

Report these eight things, each one checkable by a reader:

- the list of files you changed, one line each, with what changed in it;
- the four settled questions from F1, with the answer you chose for each and where the repository settled
  it;
- the new criteria as they now stand, quoted from the specification, and what became of criterion 11's
  third bullet;
- the new matrix row ids, the level each pins, and the words you changed inside row M-482;
- the name of each new test, its red output before the code, and its green output after;
- the census write path as it now stands, with the probe that shows a refused reading writes nothing;
- the full-suite counts quoted from the suite log;
- the census count for every document you edited, beside the count it held before.

Report anything you found and left alone. Report the lines `JOURNAL.md`, `ROADMAP.md` and `NEXT_STEPS.md`
owe, in the words you would have written into each.
