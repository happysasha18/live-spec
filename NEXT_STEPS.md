# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-11, 22:17)

Written for a session starting with clean context.

**The plan is accepted.** His word 2026-08-11 21:22: «мы же приняли план». Statuses live in the
plan file, `.live-spec/culling-plan-v3-2026-08-10.md`. Its page is republished after every plan
edit (his 17:09 order; the seat holds the URL).

**Pushed 22:15.** 34 commits, `e82da27..dfa9f57`, all gates green. One review record per push
(D4 executed). Four review rounds ran; three blockers were raised and closed.

**Executed today.** D8 (`a829e8b`). D4 (`06cf3ae`). D5 — verification after each real change, the
two-hour alarm removed. R7 inventory (`fa6d6a9`): 41 escorts — 21 his word, 11 derived, 9
invented.

**Next session's first step.** Execute D2 — cut rule 30 from the rulebook (his «делай», 21:22,
recorded). The rule-23 broadening stands as a campaign-close post-action. Then phase 2 batches
open (plan accepted, D1 yes). Phase 3 opens on D2 plus D3.

**Open small items.** Rulebook-volume rows measure stale — R2 table, the plan's numbers row. The
"3,095" figure survives in five places, each citing `DECISIONS.md`. ROADMAP row 588 carries pin
rot. Reviewer finding 15: `docs/PROGRESS.md` went stale against the spec three times in one
range. A gate proposal sits parked under campaign rule 2, needing his word or campaign close.

**Scheduled and deferred.** D7 stays scheduled with him at the keyboard. D9, D10 and D11 are
decided at campaign close.

**Mirror sync ran post-push;** the seat verifies it.

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
