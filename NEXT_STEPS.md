# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-07, 15:02)

The 01:06 order is closed. Its tail was the final full suite and the push. The suite ran
green at 2,502 tests in 539 seconds. Commit 7a178f4 carries the sweep and the counts
refresh, and the push sends it with this block.

The inbox is empty. Three deposits from the tlvphotos window were swept this pass. The
system-dialogs deposit became queue row 581. The focus-and-draft-cost deposit became rows
582 and 583. The token-and-context-thrift deposit became row 584. Each deposit is recorded
in the feedback ledger and archived under docs/queue-archive/. The sweep also found the
earned-message gate refusing the template its own home prints, which is row 585.

The night's own landings and the morning's two orders stand in the journal's 2026-08-07
chapters. Open: he reads the two pages, "what a feature costs" and the number rulings.

The plan page stands at docs/plans/2026-08-07-night-plan.md; his 01:41 word released it. Two
task statements are frozen through the clean-reader check, spoken letter for letter: "what a
feature costs" (row 568) and "the rulebook cut" (row 570). The rulebook cut's
remaining files (the pipeline, the spec writer, the reporting skill and the smaller ones)
stay on the row with the before-measurements.

## Forward queue

1. Row 576: the invented-numbers table — the seat rules on each enumerated number, removals
   land in named batches, the table goes to him.
2. Row 166 resumes: the fresh adversarial review of the board's specification, the
   stage-ladder re-map, the task-graph criteria. Its page revision reads the kanban-tools
   study in ~/live-spec-carry/2026-08-06/.
3. Row 567 (bug): the session rules name a register check no host tree holds. Ship it with
   the pack or re-word the law.
4. Row 566: board-ready statements for the whole queue, in batches through the entry check.
5. Rows 581-585, this morning's intake: the system-dialog announcement, the thread in hand,
   the early showing, the thrift rule, and the earned-message gate's own form.
6. Rows 558-565 and 532-546 stand as before; see the queue.

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
