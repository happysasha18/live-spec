# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-12, 09:51)

Written for a session starting with clean context.

**Stage 2 batch 2 and stage 3 both closed this morning.** Root: his instruction 2026-08-12 07:55 to
run the next pass by the accepted plan. Batch 2 took base rule 32. Rule 31 stands first by price,
and it waits for his ruling on the two senses of "owner" (queue rows 536/539). The resume block's
own fallback says to take the next rule by the day-1 census price. Rule 32 fell 2,205 →
1,449 bytes with all ten requirements carried word for word, checked by a fresh reader against the
inventory. Three more items folded into the same batch. They are the retired rule number named at
the rulebook's head, four restorations in rule 7, and the rule count removed from three unguarded
copies. The rulebook stands at 72,466 bytes, down from 72,929 at the batch's open, so the batch's
own test passes. Verdict lines: `.live-spec/batch2-verdicts-2026-08-12.md`. Stage 3 ran all three
steps. It gathered evidence for the 25 checks with no dated catch, where the plan expected 24. Its
verdicts were 18 keep / 6 repair / 1 already removed. It executed no removal: the plan permits
removing one check, and the verdict recommends keeping it. Stage 3 as written cuts almost no
volume; it yields six repairs and six questions.

**Batch 3 starts on base rule 29** (2,138 bytes), the next-priced rule below 32 by the day-1 census,
while rule 31 waits for his word.

**Six questions wait for him.** Each is written into `DECISIONS.md` under the stage-3 heading with
the exact line it would take. They cover the class ruling for fifteen silent-rot keeps, and gates
ae, n, p, o and ab. Row 536's "owner" ruling and his «принято» on the plan text for row 594 also
stand open.

**Also repaired in this pass.** The rule-price page's 53 pins were re-derived, and 48 of them were
stale. The pin guard widened to read that page as well as `ARCHITECTURE.md`. Its verdict word now
matches its own findings. Thirteen pointers into the rulebook repointed after the rule edits moved
lines. The progress page's generator stopped writing a run-to-run comparison, which is why that
repair kept coming back. The mirror sync now tells an absent repository from a check that could not answer, and
it stops loudly on the second. The `product-prover` mirror exists, and its content matches the pack.
Stale volume figures corrected, and the "3,095" figure recorded in `DECISIONS.md` as a decision-time
reading with no log behind it. The worker-restore gate carries the tlvphotos finding of 2026-08-12
06:05:40, which the reply in `inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md` establishes
was declined by the harness and cost nothing.

**Three habits this pass paid for, named so the next session skips them.**
1. A worker cannot run the full suite. This environment moves any foreground command past 600
   seconds into the background, and the suite runs 18 to 21 minutes, so the worker stalls and
   returns an unfinished report as final. A brief names the exact test files that finish in
   seconds. The orchestrator runs one clean full suite at the end of the pass with no worker active.
2. A full suite run while workers edit the tree reds on files being written. Those reds mean
   nothing. The closing run stands alone.
3. A repair written into generated output is undone by the next generation. Fix the generator.

**The task list stays visible while work runs** (his word 2026-08-12 08:40, standing). Its items
carry the plan document's own step names, one item per step of the current pass. A spawned worker's
label carries the same number and title in the chat language. The plan file stays the one
source; the list holds the current pass alone.

**The next release earns a major number.** Rule 32's rewrite and rule 7's before it reworded rules a
host has vendored. Base rule 32 itself names that as earning a major. `MIGRATION.md` owes its
chapter. The release number is decided at campaign close.

**The plan is accepted and wears its statuses.** His word 2026-08-11 21:22: «мы же приняли
план». Statuses live in the plan file, `.live-spec/culling-plan-v3-2026-08-10.md`, as emoji on
every stage and decision (his 22:28 readability word). The page at the standing URL is a styled
render of that file. It is republished after every plan edit (his 17:09 order; the seat holds
the URL).

**Earlier the same night, 02:28–05:38.** Stage-2 batch 1 closed on rule 7, 5,476 → 5,171 bytes
(`56c9473`). Rule 30 was cut whole from the rulebook (`3866a6c`, records `d07f2d0`). Rulebook
volume 73,578 → 72,929.

**Next session's first step.** Stage-2 batch 3 on base rule 29, by the S1–S5 recipe in the plan.
Where his ruling on rule 31's "owner" has arrived, rule 31 becomes the batch. Rule 31's
S1 inventory is already written. Then stage 3's own six repairs, each already noted against its
queue row: 553, 588, 530, 585, 550, and 526 with 532. The skill-creator review record the push gate
demands is run before each push. The recipe edit that would make it standing waits his «принято» on
the plan text (row 594).

**Open small items.** A gate proposal sits parked under campaign rule 2, needing his word or
campaign close. `MIGRATION.md` owes a chapter at the next release: a host that adopted 2.0.0
still carries rule 30 (`DECISIONS.md`, 2026-08-12). The `product-prover` skill owes one full read by
the orchestrator seat before its mirror is re-synced. This is his standing ask, restated
2026-08-12 08:18. The mirror at `happysasha18/product-prover` currently matches the pack.

**Scheduled and deferred.** D7 stays scheduled with him at the keyboard. D9, D10 and D11 are
decided at campaign close.

**The morning pass stands unpushed.** That is the next session's first act. Everything above is
committed and sits on `main` ahead of `origin/main` from `e8900d9` onward. No full suite has run
since the pass began. This environment moves a foreground command past 600 seconds into the
background, and the suite runs 18 to 21 minutes. Every partial run today was taken while workers
were writing the tree, so its reds carry no verdict. The push rule reads a suite log's own printed
verdict, so the push waits for one clean run with no worker active. The order to follow:
`python3 -m pytest -q > <scratch>/suite.log 2>&1` alone, read the last line, then
`bash guardrails/pre-push`, then push. The skill-creator review record the gate demands is part of
that walk. His standing authorization covers the push itself (2026-08-12 08:01, «пуш, деплой, все
разрешаю»).

**Pushed twice earlier the same night.** 04:20: nine commits, `dfa9f57..aec167a`, the rule-30 cut
with its record. 06:35: eight commits, `aec167a..e8900d9`, batch 1 with its record
(`docs/prover/2026-08-12-batch1-range.md`). That push re-derived the suite wall-time budget to
≤ 800 s in the architecture's own row. The mirror sync it ran reported "no mirror repo yet" for
every skill, which was the sync's own defect and is repaired (queue row 597).

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

Keep the session's task list visible for the whole of a pass, one item per step. Word each item as
the plan document words that step. Give every spawned worker a label carrying the same number and
title in the chat language (his word 2026-08-12 08:40, standing). Three surfaces then say one
thing: the agents panel, the task list, and the plan. The plan file stays the one source, and the
list holds the current pass alone. This line owes a copy in the personal profile, which lives in
another repository and waits for a session that owns it.

A worker never runs the full suite. This environment moves a foreground command past 600 seconds
into the background, and the suite runs 18 to 21 minutes. A worker that starts it stalls and then
returns an unfinished report as final. A brief names the exact test files that finish in seconds.
The orchestrator runs one clean full suite at the end of a pass with no worker active. A run taken
while workers write the tree reds on files being written, and its reds carry no verdict.

## Prompt for the next session

Continue live-spec by the plan. First act: one clean full suite alone, started in the background,
with its last line read. Then `bash guardrails/pre-push`, then push the whole range from `e8900d9`,
then `bash scripts/sync-mirrors.sh`. His authorization for the push stands (2026-08-12 08:01). Then
stage-2 batch 3 on base rule 29. Where his ruling on the two senses of "owner" has arrived, rule 31
becomes the batch, since its S1 inventory is already written. Then the standing ask he restated on
2026-08-12 08:18. It is one full read of the product-prover skill by the orchestrator seat. Its
findings land in the pack, and the mirror is re-synced afterwards.
