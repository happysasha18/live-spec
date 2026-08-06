# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-07, 01:20)

The night session closed after his four complaints of 00:17. The work is slow. The context is
huge. He wants the board for correcting state by eye. Work blocks start with no grounding he can
see. The complaints stand as rows 568, 570, 166 (field evidence), and 569. His three answers of ~01:10 are in
DECISIONS.md. No numeric caps: the one text standard is no redundancy. No self-invented numeric
standards anywhere. The test plan derives from the settled specifications.
Two repairs landed the same night. The record-freshness check gained a work road, so a clean tree
reads green after midnight (row 571, archived). The suite's scratch self-run now remembers its
last green digest and skips while the checks are byte-identical (row 573, archived). Law 7 — every
act and report opens by naming its root — rides the session-rules reminder on every prompt. The
cost-map page is docs/audits/2026-08-07-cost-map.md; his answers close its questions 1, 3 and 4.

His 01:06 order for the next session stands in force. Present one plan covering all four
complaints before any work, in plain words. Execute it without deviation. The result must
survive an adversarial review. Start there. The board state stands as recorded in the journal's
2026-08-06 22:01 chapter and its checkpoint file.

## Forward queue

1. His 01:06 order: the plan over rows 568, 569, 570, presented first, then executed without
   deviation, then adversarially reviewed by a fresh seat. Rows 572 and 574 ride it as repairs.
2. Row 166 resumes after that: the fresh adversarial review of the board's specification, the
   stage-ladder re-map, the task-graph criteria. Its page revision reads the kanban-tools study
   in ~/live-spec-carry/2026-08-06/.
3. Row 567 (bug): the session rules name a register check no host tree holds. Ship it with the
   pack or re-word the law.
4. Row 566: board-ready statements for the whole queue, in batches through the entry check.
5. Rows 558-565 and 532-546 stand as before; see the queue.
6. A tlvphotos inbox deposit (system dialogs need announcing) arrived ~01:20, measured, unswept.
   The morning sweep takes it.

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
aloud whether a request is one-time or standing before acting.
