# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-09, 15:35)

Written for a session starting with clean context.

**The campaign.** His plan of 2026-08-08 cuts this project's self-checking machinery over two weeks.
It sits at `.live-spec/culling-plan-2026-08-08.md`. Days 1 and 2 are delivered. Day 3, the install
repair, is the live day.

**Where it stands, in four numbers.** Rules cut: 0 of 88. Checks removed and still gone: 1 of 31.
Text the campaign wrote about itself: about 346 000 bytes. The rulebook it is cutting holds 66 435.
Commits since the last push of 2026-08-07: 26, all local.

**What the first day established.** Three lists of removal decisions were drawn. Fresh review
overturned all three. Twice the list came from summary tables, and the rule's own text said something
else. So a verdict row now quotes the rule's opening sentence and names who the rule reaches. No
verdict executes without a fresh review. A worker brief must forbid background jobs. Four of the
first five workers died waiting, and none since that line went in.

**The finding that decides the rest.** The plan's target is the rules inside
`skills/live-spec-base/SKILL.md`. That file holds 66 435 bytes of the 410 457 in the eleven skill
files. The keep-or-cut criterion protects 26 of the 35 rules. Deleting the rest moves 3.7 per cent.
The plan was written against 45 000 tokens read per session. Day 1 measured 18 400. The plan has not
been re-approved against that figure. Deleting unneeded rules stays worth doing. Rewriting what
survives shorter carries the volume, and it needs no keep-or-cut decision. One obstacle stands: the
plan gives three verdicts, keep, merge and remove. Review refused "shorten" as an unlawful fourth.
Adding it is his word.

**What waits on him.** None of these is answered as of 15:35.

1. Base rule 30 turns any machine-verifiable property into a blocking check. It is the engine behind
   thirty of them. Without an answer the machinery regrows the day the freeze ends.
2. Base rule 23.
3. Merging two review records into one per push.
4. Verifying the plugin install path, which changes what his own sessions load.
5. Adding "shorten" as a fourth verdict.

**Work needing nobody's word.** Queue row 541, the pointer check's own repair. Measuring how much the
rulebook repeats itself. Extending the runs-and-fires count from checks to rules, under landed row
391. Repairing the install so every path a skill names says which tree it lives in. That last one was
written today and failed its own review on seven findings. Its eight files sit at
`~/live-spec-carry/2026-08-09/`.

**Three habits that cost 2026-08-09, named so the next session skips them.**
1. His instruction and the tree's record disagreed. The session picked the record and worked on.
   Stop there, state the difference in one line, and wait. This is the one case that blocks.
2. His spoken settings landed in a state page nobody governs by. A standing setting belongs in the
   profile. A task belongs in `ROADMAP.md`. `scripts/session-extract.py` already pulls his own turns
   for a fresh reader, and what it finds has to land in one of those two homes.
3. A page was rewritten whole where three lines needed changing. Change what needs changing.

**Right now.** A fresh review of the push range refused it on three findings. All three arrived with
the repair pass. Its record is `docs/push-review/2026-08-09-the-culling-first-day.md`. One of the
three is structural. An `ARCHITECTURE.md` edit demands a fresh record under `docs/prover/` that
descends from it, and a push-review record leaves that gate unsatisfied.

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
