# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-12, 03:30)

Written for a session starting with clean context.

**The plan is accepted and wears its statuses.** His word 2026-08-11 21:22: «мы же приняли
план». Statuses live in the plan file, `.live-spec/culling-plan-v3-2026-08-10.md`, as emoji on
every stage and decision (his 22:28 readability word). The page at the standing URL is a styled
render of that file. It is republished after every plan edit (his 17:09 order; the seat holds
the URL).

**Executed this night, 02:28–05:38.** Stage-2 batch 1 closed (`56c9473`). Rule 7 fell 5,476 →
5,171 bytes with all nine requirements carried. Rulebook volume 73,578 → 72,929; suite 2,485
green. Verdict lines: `.live-spec/batch1-verdicts-2026-08-12.md`. Earlier: The plan readability pass (`99481e0`, insert-only). D2 —
rule 30 cut whole from the rulebook (`3866a6c`). Its number stays a hole between 29 and 31, and
the count reads thirty-four in every home. The spec's generator clause now reads: a check is
born from a second dated break (rule 23) or the owner's word. Records in every home
(`d07f2d0`). Suite 2484 passed / 0 failed; freeze re-frozen byte-identical; installed skill
copies synced. Queue row 589 records the executing worker stopping mid-run with an invented
report; acceptance read the tree and the worker's finished report then matched it.

**Next session's first step — the pass plan (his request 2026-08-12 07:55).** Stage-2 batch 2.
The rule: rule 31 if his word on the two senses of "owner" has arrived (queue rows 536/539; its
S1 inventory is ready); absent that word, the next rule by the day-1 census price. Row 588 opens
the pass: re-derive the R5 price pins (38 of 53 rotted) or stamp the table as a dated snapshot,
because the fallback pick reads that table. The batch folds the queued rows that land with a
rulebook-touching batch: 590, 591, 592, 593, 595. Row 589 lands as its one-line worker-brief
edit. The batch gets a fresh skill-creator review record (row 594's finding; the recipe edit
itself waits his «принято» on the plan text). Stage 3 (D2 and D3 both hold) runs after the batch
wherever both touch `tests/test_guardrails.py`. A small-items sweep closes the pass: the stale
rulebook-volume rows (R2 table, the plan's numbers row), the "3,095" figure in five places, and
the `docs/PROGRESS.md` self-comparison class, fourth occurrence 2026-08-12. Items needing him at
the keyboard or his word stay out of the pass by his 07:55 instruction.

**Open small items.** A gate proposal sits parked under campaign rule 2, needing his word or
campaign close. `MIGRATION.md` owes a chapter at the next release: a host that adopted 2.0.0
still carries rule 30 (`DECISIONS.md`, 2026-08-12).

**Scheduled and deferred.** D7 stays scheduled with him at the keyboard. D9, D10 and D11 are
decided at campaign close.

**Pushed twice.** 04:20: nine commits, `dfa9f57..aec167a`, the rule-30 cut with its record
(`docs/prover/2026-08-12-the-rule-30-cut.md`, three passes, five blockers closed) and three
skill-review records. 06:35: eight commits, `aec167a..e8900d9`, batch 1 with its record
(`docs/prover/2026-08-12-batch1-range.md`, five blockers closed across two rounds). That push
also re-derived the suite wall-time budget to ≤ 800 s in the architecture's own row and added
the batch's level lock test. Mirror sync ran post-push; every mirror reported "no mirror repo
yet". Review findings live as queue rows 589–595.

**Three habits that cost 2026-08-09, named so the next session skips them.**
1. His instruction and the tree's record disagreed. The session picked the record and worked on.
   Stop there, state the difference in one line, and wait. This is the one case that blocks.
2. His spoken settings landed in a state page nobody governs by. A standing setting belongs in the
   profile. A task belongs in `ROADMAP.md`. `scripts/session-extract.py` already pulls his own turns
   for a fresh reader, and what it finds has to land in one of those two homes.
3. A page was rewritten whole where three lines needed changing. Change what needs changing.

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. Build it with `python3 scripts/measurements-table.py`. A number stated to the person who decides
what ships names four things. They are what it counts, the decision it informs, the command
that produced it, and the value it aims at. `guardrails/tree-counts.json` is the home for every count this
repository publishes about its own tree, re-measured by gate ad on every push.

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When the commit it names differs from the one you recorded at the
start of your session, read what changed and run `bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs `git checkout -- <path>`,
`git checkout .`, or `git restore` outside `--staged`. The same holds for `git stash` in every
form, for `git reset` with `--hard`, `--merge` or `--keep`, and for `git clean` with `-f` or
`-x`. To put a file back, write back the bytes you read before you changed it.

Never give two workers the same file. A test result is the printed count of passes and failures.
Run `python3 -m pytest -q > <scratch>/suite.log 2>&1` and read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py
--freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

`bash guardrails/pre-push` runs the whole push gate set, listed in `guardrails/README.md`. New
requirements, invariants and queue rows take the next identifier above the highest one in use in
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md`. Read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask.
Publish once the suite passes. Write documents in plain English. Speak of every task by its board
echo-name in every communication. Before you ask the person who decides what ships anything,
check whether a document already answers it. If it does, act on that answer and cite it. Say
aloud whether a request is one-time or standing before acting. Guard Fable tokens hard (his word
2026-08-11 14:52, standing). A Fable seat spends its own turns only on decisions and acceptance.
Reads, drafts and sweeps go to workers on cheaper tiers, and replies stay short. The campaign
plan itself always carries execution statuses, kept current by point edits with delta pages (his
word 2026-08-11).
