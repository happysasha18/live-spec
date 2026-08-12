# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-12, 16:38)

Written for a session starting with clean context.

**The morning pass is pushed.** Root: his standing authorization of 2026-08-12 08:01, and his
instruction of 12:59 to carry the work to a push. The range `e8900d9..4a0b982` went to `origin/main`
at 16:33, 33 commits. The mirror sync ran after it. `product-prover` is up to date; every other skill
reports no mirror repository yet, which is the true state.

**The closing full suite is green: 2,497 passed, 0 failed.** It ran alone with no worker writing the
tree. Two full runs fed the wall-time budget, and `ARCHITECTURE.md` is their home. One measured
1,159.75 s inside the pre-push gate set on a quiet machine. The other measured 993.31 s standalone,
while three worker sessions shared the machine.

**Batch 3 has not opened.** It takes base rule 29 (2,138 bytes), the next-priced rule below 32 by the
day-1 census. Rule 31 still waits on his ruling about the two senses of "owner" (queue rows 536/539). That is a
policy call: it fixes which skill runs a design review, and the precedence among fourteen rule
collisions. Rule 31's own S1 inventory is already written, at
`.live-spec/s1-rule-31-2026-08-12.md`. Step S1 for rule 29 is the next act. The whole pass of 12:53-16:33 went to the closing run, the gate and the push.

**Seven things wait on his word.** Six are in `DECISIONS.md` under the stage-3 heading, each with the
exact line it would take. They are the class ruling for fifteen silent-rot keeps, and gates ae, n, p,
o and ab. The seventh is row 536's "owner" ruling, open since 2026-08-05. His «принято» on the plan
text for row 594 also stands open.

**What the closing run and the gate found, and what it cost.** The suite came back 3 failed at 12:53.
One failure was real and two read it back. Four documents stood above their recorded prose ceilings.
`NEXT_STEPS.md` had been cleared to zero and carried 21 over-cap sentences after the 09:51 and 09:53
rewrites. A cleared document stays cleared. Its sentences were split, and its ceiling held. `guardrails/README.md` and `ROADMAP.md` came back to their own ceilings. The tlvphotos reply
was measured into the record at its own seven findings, because it holds another project's words.

**The push review of the range raised sixteen findings.** Four blocked and all four are closed inside
the range. They were the prose ratchet, the published tree counts, three missing skill review
records, and one repair that could not run. `scripts/sync-mirrors.sh` was rewritten to stop loudly.
Under `set -euo pipefail` its assignment killed the script before any branch could print. Two tests
now read the script's own lines and run them under a failing `gh`. Both were proven red against the
pre-fix script. Row 597 is reopened, corrected and closed a second time.

**Seven architecture pins landed five lines short.** The pin guard passed every one. Its five-line
window is satisfied by any word of four characters or more. The words that carried them were `this`,
`when`, `work`, `live`, `session`, `SPEC` and `defaults`. All seven are repaired. Row 599 holds the
guard's own repair.

**The suite wall-time budget is re-derived at 1280 s.** The gate refused the push at 800 s. The rise
was measured before the row was touched. `tests/test_guardrails.py` costs 640.59 s of a full run,
against the near-282 s that row had claimed for it since 2026-08-06. One file is over half of every
run. Row 553 owns the work that narrows it and now carries the fresh figure. Write the number with no
thousands separator: the gate reads it with `grep -oE '≤ *[0-9]+'`.

**Nine queue rows opened today, 599 through 607.** They are:

- 599, the pin guard's five-line window.
- 600, the tree-counts rebuild missing from the batch recipe.
- 601, a batch's reached size held by no machine.
- 602, the migration chapter still walking a host to the cut rule 30.
- 603, the rulebook's rule count derived by nothing.
- 604, the worker-restore gate's per-record outcome read.
- 605, the 2026-07-28 discard that ran in this tree.
- 606, a dead field publishing a stale figure.
- 607, the skill-review gate matching a record by any mention of a name.

Row 588 is closed, its acceptance line met and verified.

**The prover skill's full read is done, and its five findings are queue rows 608 through 612.**
Root: his standing ask, restated 2026-08-12 08:18. Both parts were read whole by the orchestrator
seat. The record is `docs/prover/2026-08-12-product-prover-full-read.md`. All five rows are now
closed, across two review records. The first record,
`docs/skill-review/2026-08-12-product-prover.md`, closed rows 608 and 612. The
record filename in the meta rules now names `docs/prover/YYYY-MM-DD-<slug>.md`, matching the string
the push gate's own repair line demands. The lifecycle lead-in now reads so that six bullets under a
stated five make sense on first reading. The second record,
`docs/skill-review/2026-08-12-product-prover-2.md`, closed rows 609, 610 and 611. Row 609 answered
that INV-226 is the
spec-author's writing duty, and the answer lives in criterion R264.5 and the prover's cross-surface
uniformity sweep. Row 610 answered that the cross-link mode skips Phase 3's property analysis, steps
3a through 3d. That answer lives in the mode's own paragraph in both copies. Row 611 answered that
the class lens owes one line per pass. That answer lives in the class-lens tier of both copies, and
in the record shape beneath the verdict table. The mirror re-sync his ask names comes after these are
pushed, because the sync reads the committed tree.

**The range `4a0b982..HEAD` goes out this pass.** Count it with `git log`, since a number written
here rots between passes. The day's later work carries the plan repair, this resume file, and the
prover read with its queue rows. Beside those sit the two prover fixes with their review record, and
the queue row for the install defect the tlvphotos window reported. Above them sit this walk's own
answers. They are the repairs the push review demanded, the two tests the gate chain demanded, and
the review record itself. One commit in the range edits a skill body, so the push also needs the
full suite green.
`guardrails/check-prover-record.sh --push` reds until the record lands, because it compares the
newest record commit against the newest reviewed commit.

**The plan wears its statuses.** `.live-spec/culling-plan-v3-2026-08-10.md` is the one copy. A full
read of it today found four cells disagreeing with their own text, and all four are repaired.
Batch 3 had no marker at all. Stage 3's header had no overall marker. The stage-2 queue line still
called the 53 rules unmeasured while R5 stands done. And decision D6 carried a withdrawal marker
beside a live recommendation. The delta page is `.live-spec/plan-v3-delta-2026-08-12-4.md`.

**Three habits this pass paid for, named so the next session skips them.**
1. A run whose verdict line you grep for must be grepped by the string it actually prints. The gate
   prints "All gates green — push allowed." A watcher waiting for the upper-case form of those words waits forever.
2. `git push` fires the gate chain again, and that is twenty minutes. Run `bash guardrails/pre-push`
   yourself, read its verdict, then push with `--no-verify` on the same unchanged tree.
3. Raising a budget without measuring what moved writes a number nobody believes. Measure the term
   that grew, name it in the row, and point at the queue row that brings it down.

**The next release earns a major number.** Rule 32's rewrite and rule 7's before it reworded rules a
host has vendored. Base rule 32 names that as earning a major. `MIGRATION.md` owes its chapter, and
row 602 holds it. The release number is decided at campaign close.

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

Continue live-spec. Open by asking Alexander in plain Russian what he wants done, using the four
choices below. Ask before starting any of them. He said on 2026-08-12 at 18:04 that he wants to be
asked in human language rather than handed a plan.

**First act, and he asked for it by name at 2026-08-12 23:58.** The campaign stated several goals,
written down across earlier sittings. Find them in the session
transcripts, since that is where he says they live. Send cheap reader workers at those transcripts
and read their summaries here, which is his word of 00:03. Derive from them the parameters the campaign is
actually judged by, then put every one under watch in the plan's status block. Each parameter carries
the command that measures it, and the pass that rewrites the block runs that command. Today the block
watches one number, the rulebook's byte count. The second stated goal, making the machinery cheaper,
is measured by nothing. The full run's budget rose from 800 to 1280 to 1410 seconds inside one day,
and the only place that noticed is queue row 553. Queue row 617 holds this work.

Before asking, do these three reads so the question is informed. Read this whole file. Read
`.live-spec/culling-plan-v3-2026-08-10.md`, whose head block says where the campaign stands. Read
`git log --oneline origin/main..HEAD` to see what still stands unpushed, and count it there rather
than trusting a number written here.

The four choices to put to him:

1. **Ship what is waiting.** Whatever `git log --oneline origin/main..HEAD` lists sits unpushed. The walk is a fresh adversarial review record
   over `origin/main..HEAD`, then one clean full suite alone in the background. Then
   `bash guardrails/pre-push < /dev/null` in the background, then `git push --no-verify`, then
   `bash scripts/sync-mirrors.sh`. Budget about 45 minutes. His authorization for the push stands.
2. **Answer the seven open questions.** Six sit in `DECISIONS.md` under the stage-3 heading, about
   whether five named gates keep earning their place. The seventh is what "owner" means in base rule 31.
   It has been open since 2026-08-05, and it keeps the queue's most expensive rule out of the
   campaign. Each is a policy call only he can make. Answering them unblocks real cutting.
3. **Run the next shortening batch.** Batch 3 on base rule 29, 2,138 bytes, by the S1-S5 recipe.
   Where he has answered the "owner" question, rule 31 becomes the batch instead, and its inventory
   is already written.
4. **Finish the prover skill's three open findings.** Rows 609, 610 and 611. Each asks a scope
   question about what the skill owes a verdict for, so each needs a decision before an edit.

Say the four in two sentences each at most. Recommend one, and say why in one line. Then wait.

Never open by narrating what a previous session did. He has read the report already.
