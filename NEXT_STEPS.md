# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-09, 00:30)

The culling runs. Day 1, the preparation batch, opened at 00:19 on his order of
2026-08-08, 22:17.

Three pages hold it. The plan sits at `.live-spec/culling-plan-2026-08-08.md`. Its
four-round review record sits beside it at `.live-spec/culling-plan-2026-08-08-review.md`.
The audit behind both is `.live-spec/crisis-audit-2026-08-08.md`. The plan is frozen, and
his word alone changes it.

The audit verdict in one line: the quality machinery became the project's main consumer.
The product is 5.7% of the tree. 61% of recent queue rows serve the machinery itself. The
installer ships 183 dangling references that no gate sees. The cure is a freeze on new
machinery. Then a gate diet, from 27 blocking gates toward about five. Then a rulebook cut
to one sitting's read. Adoption stands at the head of the queue after that.

He read the audit page at ~21:30 on 08-08 and agreed with the diagnosis. He flagged one
fabricated line, a monetization goal he never stated. The project is open source, and its
goal is to be useful. A source sweep found three more unsourced numbers. All four are
corrected on the page.

The plan's own calendar:

- day 1 — preparation
- day 2 — a trial cut that prices the work
- day 3 — the install fix
- days 4-10 — the rule cut, one batch a day, thickest files first
- days 11-12 — a dress rehearsal by a stranger agent in an empty folder
- to day 14 — the closing page and the standing rule against regrowth

The calendar numbers are an estimate. Day 2 measures the real price, and the calendar is
recounted then.

Day 1 owes four things. The two red tests go green. The four starting measures are
recorded. Three censuses are written: every check, every rule with the places it is wired,
and everything a person lacks after installing the pack. A queue page is prepared for him
to strike rows from, and it holds no work.

How each day runs. A verdict list comes in the morning. One cut is one commit carrying its
row number. A fresh agent checks every two hours, in three lines. The evening brings a full
circle of the four measures and a digest to him. His veto is one revert. Every work block
opens with a line naming the day, the batch and the step, or it does not start. Each day
declares in advance which of the four measures it must move. Two days in a row without that
move stop the work, and he gets a page saying why.

Rules for the two weeks. Nothing new is built. No new check, rule or hook appears, and only
he can grant an exception. A problem found on the way earns one queue row and waits. Only
what blocks the day's batch is fixed at once. A red test from another area is named in the
evening digest. His brake word is «стоп чистка».

Drift signals he watches, four of them. A first reply doing anything besides starting the
day. A work block missing its opening line. A proposal to improve or reword the plan. A new
check or rule appearing.

Two timers stand in the running session. One started day 1 and is spent. The other checks
every two hours. Both live in that session alone, and they die with it.

The 08-07 plan's six steps stay archived under the 08-08 pages. The plan page stands at
docs/plans/2026-08-07-night-plan.md, and his 01:41 word released it. Two task statements are
frozen through the clean-reader check, spoken letter for letter. They are "what a feature
costs" (row 568) and "the rulebook cut" (row 570). The rulebook cut's remaining files stay
on the row with the before-measurements. They are the pipeline, the spec writer, the
reporting skill and the smaller ones.

The night's own landings and the morning's two orders stand in the journal's 2026-08-07
chapters. Open: he reads the two pages, "what a feature costs" and the number rulings.

## Forward queue

The recovery plan's six steps enter this queue only once he gives his word on the plan.
Until then they stay at `docs/plans/2026-08-07-recovery-plan.md`.

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
