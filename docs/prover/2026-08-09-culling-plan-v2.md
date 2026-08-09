# Prover record — the culling plan recompiled against the cost of a change, 2026-08-09

Adversarial review of `.live-spec/culling-plan-v2-2026-08-09.md`, committed as `49f246c`.
Reviewer: a fresh seat with clean context, distinct from the seat that wrote the plan (base rule 33).
Root: Alexander's order of 2026-08-09, 11:22, which named two faults in the first night's cut.
The cut was ordered by the wrong cost, and it covered one file out of a much larger machine.

Nothing in the plan has executed. No repository file was changed by this review except this record.
No commit, no push, no restoring command was run.

Verdict: this plan is not fit to execute today. Seven blocking findings and thirteen major findings
stand. The blocking ones sit in the cost table and in phase A, which is the plan's whole first move.

## Method

Read the plan first, then the frozen plan it replaces stage three of. Then the three day 1 censuses,
the day 2 measured price, and the two reviews that overturned the earlier verdicts. Then the redrawn
verdict list with its closing note.

Re-derived every figure in the inventory table and the tax table with my own command. Read
`guardrails/pre-push`, `guardrails/check-prover-record.sh`, `guardrails/check-skill-review.sh`,
`guardrails/check-push-review.sh`, `guardrails/check-tests.sh`, `guardrails/check-pin-drift.sh`,
`guardrails/check-freeze.sh` and `guardrails/pre-commit`. Ran the three review gates by hand.

Read the repository's own state with `git status`, `git ls-files -u` and `git diff --cached -M`.
Read two earlier records for form: `docs/prover/2026-08-09-redrawn-rule-verdicts.md` and
`docs/prover/2026-08-09-culling-day2-cuts.md`.

## What was read and run

- `.live-spec/culling-plan-v2-2026-08-09.md` whole, and `.live-spec/culling-plan-2026-08-08.md` whole.
- `.live-spec/day1-census-checks.md` whole, `.live-spec/day1-census-delivery.md` in part,
  `.live-spec/day1-census-rules.md` at its totals, `.live-spec/day1-measures-2026-08-09.md` whole.
- `.live-spec/day2-price-2026-08-09.md`, `.live-spec/rule-verdicts-redrawn-2026-08-09.md` and
  `.live-spec/day3-opening-2026-08-09.md`, all whole.
- `docs/prover/2026-08-09-culling-day2-cuts.md` and `docs/prover/2026-08-09-redrawn-rule-verdicts.md`.
- `skills/live-spec-base/SKILL.md`, its header, rules 10, 12 and 30, and its rule numbering.
- Every `skills/*/SKILL.md` for its numbered rules and its byte size.
- `guardrails/pre-push` whole gate roster, and the eight check scripts named in the method above.
- `NEXT_STEPS.md`, `JOURNAL.md` at its two 2026-08-09 entries, `ROADMAP.md` row 541,
  `.live-spec/PROBLEMS.md` at its fence row.
- Gates run by hand: `check-prover-record.sh --push` (exit 0), `check-skill-review.sh` (exit 0),
  `check-push-review.sh` (exit 1).
- Counts run: gate letters, base rules, skill rules, invariant codes, spec codes, matrix rows,
  test files, collected tests. No test suite was run, since no code changed here.

## Findings

Twenty-four findings follow. Seven block execution, thirteen are major, four are minor.

### 1. Blocking — the tree cannot take a commit, so no phase can land

`git ls-files -u` reports seven files carrying index stages one, two and three. They are
`ROADMAP.md`, `TEST_MATRIX.md`, `attic/MANIFEST.md`, `docs/PROGRESS.md`,
`docs/queue-archive/rotated-ROADMAP-2026-08.md`, `guardrails/README.md` and
`guardrails/rule-census.json`.

No merge is in progress. `.git/MERGE_HEAD` does not exist. The working copies carry no conflict
marker, so the resolution was written but never staged. `git commit` refuses a tree in this state.

The plan's own batch shape needs one commit per removal, at line 106. That shape cannot start here.

Repair: stage the seven resolved files, then verify with `git ls-files -u` returning nothing.

### 2. Blocking — tax row 1 names the suite's cost and phase A2 removes something else

Line 37 reads "the whole test suite runs inside one of the checks", priced at 451 s of 486 s, firing
every push. Line 54 makes that row phase A2 and calls it "the single largest number in the whole
machine".

The 451.45 s belongs to gate b, which is the suite itself. `.live-spec/day1-census-checks.md:54`
names it, and lines 32 to 34 record that it was timed as the full unscoped run.

The nested run is two tests inside that suite, at `tests/test_guardrails.py:339`. Lines 360 to 366
show they ride the reach map and skip unless the diff touches gate machinery. So the nested run is
neither 451 s nor paid every push.

The frozen plan priced the same nested run at 150 s, at `.live-spec/culling-plan-2026-08-08.md:15`.
The plan cites that batch as its own precedent at line 55 while replacing its number.

Repair: time the nested run alone, put that number in the row, and restate the trigger.

### 3. Blocking — phase A3 cannot be built as written, and it edits a gate under the freeze

Line 56 says one fresh review covering the push satisfies both gates, because both read the push
range.

Gate a does not work that way. `guardrails/check-prover-record.sh:74` looks for a file named
`docs/prover/<today>*.md`. Lines 124 to 161 judge it by commit ancestry against `PRODUCT_SPEC.md`
and `ARCHITECTURE.md`. The push range is read only for the inbox carve-out, at lines 43 to 71.

Gate s wants a different file in a different place. `guardrails/check-skill-review.sh:110` to 122
require a committed record under `docs/skill-review/`. That record must carry the marker
`SKILL-REVIEW`, a line matching `^Verdict:`, and the changed skill's name as a word.

One file holds one path. Satisfying both from one record means changing a gate script. The frozen
plan's rule 2 gives that exception to him alone, at `.live-spec/culling-plan-2026-08-08.md:35`.

Repair: put A3 to him as a decision, or drop it and keep the batch economy the day shape already buys.

### 4. Blocking — the phase A1 carve-out is his to grant, and the plan takes it

Lines 51 to 53 give the culling a carve-out from the deletion bookkeeping on the seat's own word.

Base rule 10 holds that bookkeeping, at `skills/live-spec-base/SKILL.md:226-228`. It names the attic
move, the manifest line, the dated spec tombstone and the retired matrix rows. It cites SPEC INV-7,
A-4 and A-9. Its own last clause puts deletion approval with the person.

Base rule 12 settles it plainly, at `skills/live-spec-base/SKILL.md:235-237`. Irreversible moves and
authored-content moves are proposed with a recommendation and executed on the person's word.

The frozen plan's rule 2 adds the second lock. A moratorium exception is his alone.

Repair: carry A1 to him as one decision card with its measured saving, and hold phase A until he rules.

### 5. Blocking — the A1 mechanism cannot batch the two artifacts it says it will batch

Line 52 says the tombstone and the retired-row bookkeeping run once per batch instead of once per item.

A retired matrix row is per item by construction. `tests/test_traceability.py:245` holds every matrix
block against an architecture node, and lines 251 onward hold each row under its owning node. Five
removals own five sets of rows.

A spec tombstone is per item for the same reason. Each removed thing has its own requirement codes.

So A1 promises a saving its own machinery cannot deliver. What batching really saves is the review
passes, which the day shape already batches at line 107.

Repair: state which artifact truly batches, and drop the two that cannot.

### 6. Blocking — the pointer check is already back without its fix

Lines 93 to 96 say the restore and the fix land together, so the check proves a pointer against its
own line.

The restore has landed already, and it carries no fix. `git diff --cached -M` reports
`attic/check-pin-drift.sh` renamed to `guardrails/check-pin-drift.sh` at similarity index 100 per
cent. The window still reads plus or minus twenty-five lines, at
`guardrails/check-pin-drift.sh:57-58`. The gate is wired at `guardrails/pre-push:89`.

So the tree now runs a check the plan itself calls unearned, and the queue row that closes the gap is
unstarted.

Repair: say in the plan that the restore landed first, and give row 541 a place in phase A.

### 7. Blocking — every phase declares a measure the frozen plan does not govern the day by

The frozen plan gives four measures and one law over them. Line 30 of
`.live-spec/culling-plan-2026-08-08.md` says each day declares which of the four it must move. Two
days without movement stop the work.

The four are the install's reach, the rulebook bytes, the full test run, and the checks before a
publish. They stand with a command each at `.live-spec/day1-measures-2026-08-09.md:9-14`.

Phase A declares seconds per push and artifacts per removed item, at line 59. Phase B declares
blocked commits per landing, at line 67. Phase C declares invariants, at line 74. None of the three
is one of the four. Only phase D's measure is, at line 84.

This replaces the frozen day shape. Rule 1 of the frozen plan gives that change to him.

Repair: map each phase onto one of the four measures, or put the new measure set to him.

### 8. Major — the inventory's check count is wrong at the hour the plan was written

Line 23 reads twenty-nine checks on every push.

`JOURNAL.md:2519`, written at 11:35 the same morning, reads "The gate roster stands at 30". The
command the project publishes returns 30 on this tree. It returns 29 at commit `d80a7e0`, which the
plan cites at line 5, and 29 at `49f246c`.

The restore of gate g is the difference, and the plan's own closing section is what restored it.

Repair: read the count as 30, and say the restore moved it.

### 9. Major — "all requirement codes in the product spec, 390" matches nothing in the tree

Line 20 gives 390.

The generated index carries 398 code rows, which gate x holds equal to the body. A sweep of the body
returns 400 unique codes; `D-1` and `D-6` are the two the index does not carry. Requirement headings
number 310.

Repair: use 398, the number the gate holds, and name the command beside it.

### 10. Major — there are ten working skills, and the 53 rules sit in six of them

Line 18 reads "rules inside the other nine skills". Line 79 reads "the nine working skills' 53 rules".

The rulebook's own header says ten, at `skills/live-spec-base/SKILL.md:8` and line 12. Eleven folders
sit under `skills/`, the base among them.

The count of 53 holds, and it is drawn from six skills. Four working skills carry no numbered rule at
all: `product-prover`, `publish`, `feedback-intake` and `feedback-collector`. Their bodies hold
94 673 bytes together, and phase D1 reaches none of it.

Repair: say ten, and say which six skills the 53 come from.

### 11. Major — phase D's own measure cannot register phase D1

Line 84 declares the measure as bytes a session reads before work, by the repaired command.

That command counts every markdown file under `skills/live-spec-base/` plus the personal profile. It
stands at `.live-spec/day1-measures-2026-08-09.md:12`, with its repair at lines 62 to 63. It returns
73 503 bytes today.

Phase D1 cuts rules in the other ten skills. Not one byte of those files enters the number. The day
would report no movement, and the frozen plan's line 30 would stop the work on the second such day.

Repair: give D1 its own measure over the working skills' bodies, and say so in the phase.

### 12. Major — the tax total of 486 seconds cannot stand beside the same table's 29 checks

Line 37 reads "486 s all checks cost". Line 23 reads twenty-nine checks.

The census total of 486.48 s is the sum over 31 gates, at `.live-spec/day1-census-checks.md:89`.
Removing gate g at 6.49 s and gate ab at 0.06 s leaves 479.93 s over 29. Restoring gate g leaves
486.42 s over 30.

The two figures in the plan therefore describe two different trees. The phase A measure "from 486
down" rests on a baseline that moved twice within twelve hours.

Repair: re-time the roster as it stands after the restore, and state the date of the timing.

### 13. Major — tax row 2's trigger understates when the review is owed

Line 38 says the adversarial review record is owed "because the spec changed", and fires "nearly
every landing".

The push road of gate a demands a record dated today on every push. `check-prover-record.sh:34-38`
sets that road, lines 73 to 98 refuse a push without today's file. The only exemption is a diff that
is exactly one new file under `inbox/`.

So the row fires on every push, whatever the diff touches. The spec change controls the freshness
arm alone.

Repair: restate the trigger as every push, and keep the spec clause for the freshness arm.

### 14. Major — the tax table misses a third review record, which is red on this tree right now

Gate ac is wired at `guardrails/pre-push:239`. `guardrails/check-push-review.sh:18-31` requires a
committed dated record under `docs/push-review/` carrying six named fields.

Run by hand just now, it exits 1. Its message names commit `49f246c` as the newest reviewed commit,
against a record from 2026-08-07.

The gate has a dated real catch on record, at `.live-spec/day1-census-checks.md:65` and lines 114 to
117. It costs a full adversarial pass per push, which is the same order of cost as rows 2 and 3.

Phase A3 merges two review records and leaves this one standing. The saving it claims is a third of
the real load.

Repair: add gate ac as its own tax row, and say what A3 does about it.

### 15. Major — the tax table misses the installed-copy sync, which day 2 priced by name

`.live-spec/day2-price-2026-08-09.md:45-48` lists a sync of the installed copies among the tail of
one small gate removal. `docs/prover/2026-08-09-culling-day2-cuts.md:48-62` records it as a blocking
finding, with gate m red until the sync ran.

The frozen plan makes it a standing duty, at `.live-spec/culling-plan-2026-08-08.md:39`. Copies are
updated the same day their sources are touched, and two other projects run on those copies.

The trigger is the same as tax row 3, every skill-text change. The table carries no row for it.

Repair: add the sync as its own row, with the two dependent projects named.

### 16. Major — row 6's five artifacts is understated by the one measurement in evidence

Line 42 gives five artifacts per removed thing.

Day 2's two removals touched 19 files and 26 files, at `.live-spec/day2-price-2026-08-09.md:10-11`.

Removing a check owes four more artifacts. Gate w wants an entry in
`guardrails/gate-red-proofs.json`. Gate u wants a mirrored step in `.github/workflows/gates.yml`.
Gate ae wants a line in `scripts/check-registry.json`. The architecture node's owns list wants the
name struck. None of the four is among the five.

The row's conclusion survives, since the true figure is larger. Its number does not.

Repair: replace five with the measured file count, and name the four gate artifacts.

### 17. Major — row 4's blocked commits have no evidence, and this ratchet cannot block a commit

Line 40 prices the prose ratchets at four blocked commits. Line 67 makes "blocked commits per
landing, from four down" phase B's declared measure.

`guardrails/pre-commit` runs three checks: future timestamps, the deferral marker, and a staged-file
overlap test. None is a lint. Gate aa sits at the push, at `guardrails/pre-push:233`.

A sweep of `JOURNAL.md`, the censuses and the two prover records finds no record of four such blocks.
The only occurrences of the phrase in the tree are the plan's own two lines.

Repair: cite the four events with dates, or replace the row's cost with a measured one.

### 18. Major — phase B's "four checks" is one gate reading three linters

Line 63 says four checks read the same documents with four different rules.

One gate reads them. `guardrails/check-doc-findings-bound.py` is gate aa, and it reads
`guardrails/rule-census.json`. `scripts/rule-census.py:16-30` names the three readings that fill that
file: the word cap, the style lint, and the register lint.

So keeping the register reading and judging the other two is an edit inside one script. It is not
three checks to remove.

Repair: restate phase B as one gate with three readings, and say which reading goes.

### 19. Major — row 7 counts one night's accident as a standing cost

Line 43 prices the fence at two blocked commits and one broken partial commit, firing every commit.

The fence is off unless armed, at `guardrails/pre-commit:57-59` and `guardrails/README.md:118-119`.
It reds only when the repository tip moved since the arming session recorded it.

Its habit of blocking a session's own next commit was a recorded problem, marked solved on 2026-08-07
by row 572, at `.live-spec/PROBLEMS.md:21`. The broken partial commit is finding 1 above, which is one
revert left unstaged.

Repair: restate the trigger as a tip that moved, and drop the accident from the cost column.

### 20. Major — phase B contradicts rule 30, which the plan itself parks on his word

Line 64 judges three prose ratchets against the criterion.

Rule 30 names two of them by name. `skills/live-spec-base/SKILL.md:492-495` reads that any
mechanically checkable property is a blocking gate, and gives "the register clean" and "the
redundancy gone" as worked cases.

Lines 100 to 102 of the plan say rule 30 stays his and carries his own instructions. So phase B
proposes work that a parked rule forbids, and the plan never joins the two sentences.

Repair: say in phase B that its outcome waits on his ruling over rule 30.

### 21. Minor — the restore raises the very number phase A2 sets out to lower

Gate g costs 6.49 s, the third most expensive check, at `.live-spec/day1-census-checks.md:57`. The
same census records no real catch for it, at lines 140 to 143.

His word of 11:22 settles the keep, and the ground he gave is sound. The plan should still say that
phase A starts 6.49 s above the number the frozen plan measured.

Repair: state the restored cost in the phase A measure line.

### 22. Minor — "eighty-eight rules" inherits the wrong 53

Line 25 sums 35 and 53. The 53 is right as a count and wrong as a description, by finding 10.

Repair: keep 88 and correct the sentence that explains it.

### 23. Minor — phase E points at a page that carries the same miscount

Line 89 sends the reader to `.live-spec/day3-opening-2026-08-09.md`. That page reads "the other nine
skills" at line 35 and "each of the nine working skills" at line 53.

Repair: correct both pages in one pass, since the number travels between them.

### 24. Minor — a batch worked overnight cannot satisfy gate a on one push

Line 107 gives one push a day and one review pass over it. Day 1 and day 2 both ran from after
midnight to early morning, per `JOURNAL.md:2455`.

Gate a's push road wants a prover record whose filename carries the push day's date, at
`check-prover-record.sh:74`. A batch that starts before midnight and pushes after it needs a record
dated the second day.

Repair: say that the review record takes the push day's date.

## The seven lines of the order, answered directly

**Every number in the two tables.** Five inventory rows hold and two fail. The 35 base rules, 314
invariants, 551 matrix rows, and 203 test files with 2 492 tests all re-derive exactly. The check
count reads 30 today, against the plan's 29, by finding 8. The requirement-code total is 398 where
the plan gives 390, by finding 9. The 53
skill rules is a right count under a wrong description, by finding 10. In the tax table, rows 2, 3
and 5 hold their figures. Row 1 is wrong by finding 2. Row 4 is unevidenced by finding 17. Row 6 is
understated by finding 16, and row 7 is overstated by finding 19.

**Is the per-change tax the right cost?** The framing is right and the table is incomplete. Reading
is paid once per session and the tax compounds, so the plan's correction of the first night stands.
The table misses gate ac by finding 14 and the installed-copy sync by finding 15. Both fire as often
as the rows beside them and cost as much. Row 7 is the row that counts an accident as structure.

**Can one record satisfy both review gates?** No, as the gates are written. Finding 3 gives the file
paths and the evidence fields. A3 is a change to a gate, and the moratorium's exception is his.

**Is the A1 carve-out the seat's to grant?** No. Base rule 12 settles it, with base rule 10's own
approval clause behind it and the frozen plan's rule 2 beside it. Finding 4 carries the citations.

**Is phase A truly first?** No, on two counts. Finding 1 says nothing can commit until the index is
resolved. Findings 4 and 3 say two of phase A's three steps wait on his word. What can start today
is A2, once its number is re-derived by finding 2.

**What the plan omits.** The suite itself, at 451 s, is the largest per-push cost, and no phase
touches it. The queue holds 210 rows in its table today, and `NEXT_STEPS.md:24` records 109 of them serving
the quality machinery. No phase reaches the queue. The `hooks/` folder holds 21 files, unreached.
The settings ladder and the personal profile are roughly a fifth of the measure phase D declares, and
no verdict can move either. The four rule-less working skills hold 94 673 bytes, by finding 10.
Leaving these means phase A's own measure cannot fall far, and the queue regrows the machinery the
campaign removes.

**The pointer check's window and its 29 stale pointers.** Both hold.
`guardrails/check-pin-drift.sh:11` states the rule. Lines 57 to 58 compute a window of plus or minus
25 lines around the pinned line, which is 51 lines. `ROADMAP.md:217`, row 541, records the pass of
2026-08-05. It found 29 stale pins across three skill files under a green gate. One pin labelled
rule 20 landed on rule 19's opening line. The claim that the restore and the fix land together is
false by finding 6.

## What was checked and found sound

Named so a later reader knows this sweep's reach.

- The criterion is carried unchanged. The plan's line 8 matches the frozen plan's line 25.
- One removal, one commit, at line 106, matches the frozen plan's line 26.
- The batch review economy at line 107 is real and already measured, at
  `.live-spec/day2-price-2026-08-09.md:52-56`.
- Tax rows 2 and 3 carry the right minutes and the right outcomes, from
  `.live-spec/day2-price-2026-08-09.md:40-43`.
- Tax row 5 is accurate. `guardrails/check-freeze.sh:23` guards exactly the spec, the architecture
  and the matrix, and skips with a note when no baseline exists.
- Row 6 is the right row to call the trap, even with the wrong count. Deletion bookkeeping is what
  makes each cut expensive.
- The measured claim at lines 32 to 33 holds. A 0.06-second gate with no recorded catch took the
  night, and `.live-spec/day2-price-2026-08-09.md:45-48` lists what it carried.
- Rules 30 and 23 are correctly held for his word at lines 100 to 102, and the plan says so plainly.
- Phase D's grouping answers the day 2 lesson. Ruling one rule at a time from summary tables produced
  two overturned lists, and the plan names that at line 77.
- The plan is honest about its own root, its own hour and its own commit.

## Verdict

Not fit to execute today.

Seven findings block execution.

- Finding 1: seven files sit unmerged in the index, so no commit can land.
- Finding 2: phase A2's 451 seconds is the suite's cost, and the nested run is something smaller.
- Finding 3: the two review gates read different directories, so one record cannot serve both.
- Finding 4: the phase A1 carve-out is the person's to grant, under base rules 10 and 12.
- Finding 5: the tombstone and the retired rows cannot batch, so A1's saving is not there.
- Finding 6: the pointer check is already restored without the fix the plan pairs it with.
- Finding 7: three of four phases declare a measure the frozen plan does not govern the day by.

Thirteen findings are major: findings 8 to 20. Four are minor: findings 21 to 24.

Findings 2, 4, 12 and 16 are one failure repeated. The plan carried numbers forward from the day 1
census. It never re-derived them against the tree the day 2 cuts and the morning restore left behind.
That is the same failure the two earlier reviews named in the verdict lists.

## Reach

Files read whole:

- the plan, and the frozen plan it replaces stage three of;
- the day 1 checks census, and the day 1 measures page;
- the day 2 price, the redrawn verdicts, and the day 3 opening;
- the two prover records of this morning.

Files read in part:

- `.live-spec/day1-census-rules.md` at its totals;
- `.live-spec/day1-census-delivery.md` at its headline and its method;
- `skills/live-spec-base/SKILL.md` at its header and rules 10, 12 and 30;
- `JOURNAL.md` at its two entries of 2026-08-09;
- `NEXT_STEPS.md` at its live-state block, and `ROADMAP.md` at row 541;
- `.live-spec/PROBLEMS.md` at its fence row;
- `tests/test_guardrails.py` at its gate b class;
- `tests/test_traceability.py` at its matrix tests.

Scripts read: `guardrails/pre-push`, `pre-commit`, `check-prover-record.sh`, `check-skill-review.sh`,
`check-push-review.sh`, `check-tests.sh`, `check-pin-drift.sh`, `check-freeze.sh`,
`check-doc-findings-bound.py`, `check-deletion-only-push.sh`, `scripts/rule-census.py`, `install.sh`.

Commands run:

- the gate-letter count, on three revisions;
- counts of base rules, skill rules, invariant codes and spec codes;
- counts of index rows, matrix rows, test files and collected tests;
- byte sums over the skill bodies and over the rulebook measure;
- `git status`, `git ls-files -u` and `git diff --cached -M`.

Three gates were run by hand, with their exit codes recorded above.

Not read: `~/.claude` and its installed copies, which the order placed out of bounds. No test suite
was run, since nothing in the plan has executed and no code changed here.

Files written by this review: this record alone.
