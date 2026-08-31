# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-31, 14:59)

Written for a session starting with clean context.

**The spec now says what stands behind each rule it states.** Four answers, and a requirement says
which one it has: a command the machine runs, an instruction a session reads and follows, a surface
drawn when somebody asks for it, or nothing yet. Requirement 316 holds the rule. The point of it is
that until now a rule read the same whichever answer was true, so a reader could not tell a law a
machine holds from one that rests on a session remembering it.

**The first read of a message has its own requirements and its own node.** Requirements 313 to 315 in
`spec/message-first-read.md`, the `director` node in `architecture/pipeline-and-lanes.md`, and its
rows in `matrix/director.md`. What executes is named where it executes: `scripts/checkpoint.py`
refuses a first-read-owned checkpoint with no decision sheet in it, and `scripts/state-probe.sh` marks
the reading's score a replay whenever the recorded runs are older than the skill. What does not
execute is said plainly in the spec's own sentences — nothing on this machine puts a message through
the reading, and the boot file's line is the whole of the door. The idea shelf is Requirement 315 and
carries the promised marker, because nothing in the tree keeps one.

**The roster of feature names went from seventeen to ten**, and the rule behind it is mechanical:
a requirement carrying a feature name and a `[target]` marker at once reds in the coverage check.
`F-contract` and `F-work-board` retired to `attic/feature-names-retired-2026-08-31.md`; the five names
for attaching the pack to a project converged on `F-attach`; `F-wish` and `F-feature-map` kept their
names and had their requirements repaired instead, since both name something real once the requirement
stops overstating it. `F-first-read` is new. Requirement 224 changed with them — it had said a
promised scenario keeps its tag, which is the opposite of what now holds.

**Two new faults ride the reference gates of the format family.** A `.md` file sitting among a
document's parts that its parts map names nowhere, and two parts opening one requirement number.
Both were verified as real holes first, by dropping each into a copy of the tree and watching every
gate pass over it. The readers live in `guardrails/specformat.py`; `guardrails/check-index-generated.py`,
`check-matrix-reference.py` and `check-architecture-reference.py` call them; `tests/test_spec_parts.py`
carries a red proof for each with its clean twin. The rules for a writer are in `docs/spec-format.md`
and Requirement 317.

**Two things this task left open, both a line's work for you.** q-437 — checking for similar cases at
every level — was folded into `plan-12` when the board was cut, and that work is untouched while the
spec still promises it, so the row stays queued rather than ticked even though its acceptance runs
green. And the decision sheet's own ordering line: the ordering law has its home in the spec and its
node now, read off the plan's recorded states by command, but the field on the sheet itself edits a
skill file, and the installed copies then differ from the source until `scripts/sync-skills.sh` runs
from outside a worktree. It was written, the suite named the drift, and it came back out. Both stand
in §Blockers.

**One older question still waits on the owner.** `PLAN.md` lets a session change a task's status
and §Blockers and nothing else without his say-so; the 28.08 evening pass rewrote what finished
looks like on twenty-one open tasks and widened the bar for what counts as queued. A sibling session
in the same range read the rule the other way and stood down on a correction of its own. §Blockers
carries the question in his own language, first entry. Nothing is reverted while it stands open, and
no other work waits on his answer.

**Owed and unwritten:** a `JOURNAL.md` entry for the prover-description movement (`85b659d1`).

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. Build it with `python3 scripts/measurements-table.py`. A number stated to the person who decides
what ships names four things. They are what it counts, the decision it informs, the command
that produced it, and the value it aims at.

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
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `PLAN.md`. Read it before you claim a number.

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
