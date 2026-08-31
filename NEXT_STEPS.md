# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-31, 18:28)

Written for a session starting with clean context.

**The director's own score is honest again, and one disagreement is named rather than buried**
(plan-2, re-measured 31.08). The stored score of 33 of 35 was a partial re-record: on 26.08 only the
nine scenarios that were red at the time were drawn again, so twenty-six were still being counted
against a skill version that had since moved. A full re-draw of all thirty-five found two real
things. Repeated draws of one unchanged skill version disagree with themselves on individual
scenarios, so a single run is a reading and never a verdict. And the skill's own text and the
grading disagreed: the text said naming one act too many costs a sentence, while the grading failed
the whole scenario for it. The grading now follows the text — an extra act alone is reported as a
note, a missing act still fails — and one scenario whose situation argued against itself was
repaired at the situation, leaving its expectation untouched. The honest score is 34 of 35. The one
that stands is `idea-for-another-project`: the skill and the fixture genuinely disagree about
whether an idea aimed at a different project is an act at all, and that disagreement is open. The
eval's own README now says a skill change requires re-recording all thirty-five, never a subset,
because a subset is how the stale number was made. Two graders are in play, so the movement is
stated twice rather than once: the old grader puts the 26.08 draw at 26 and today's at 30, and the
new grader puts today's at 34, so four scenarios are real improvement and the rest of the gap is the
corrected cost model.

**An adversarial read with clean context refused this push, and nine findings were repaired before
it went out.** Two of them were the grading change overreaching. It had been justified on six of
that day's nine reds when the true number is two, re-derived twice against the run's own recorded
traces. And it had gone one step too far: a turn the fixture expects to carry no act at all could
name one and still pass, which is exactly the failure the thank-you case exists to catch. An extra
act is now forgiven only where some act was expected. Four more were in the way out for a cleared
mistake, which counted four kinds of non-repair as a repair — a wildcard standing for the whole
tree, a directory already gone from disk, a commit that deletes the file rather than restoring it,
and a commit merely amended after the fact. Each now stays blocking, each proved by a test that
fails against the code as first written. One was the new attribution block reddening a sentence that
carries its date in the form this project writes dates in; it now reads the whole line. The rest
were counts and pointers that had drifted at the merge.

**A worker-restore finding stops blocking every push once the tree shows the work back** (q-527,
landed 31.08). The check that reads worker transcripts for a command that discards unsaved work made
findings that were true forever: a finished recovery cleared nothing, and every push after an
incident waited for the reading window to roll past it or for somebody to move the counting start by
hand. What counts as made good is now written once, in Requirement 301 — every file the command
named carries, in the repository that command ran in, a commit dated later than the command. The
check asks git that question afresh on every run, so nothing on disk records a clearing and the
answer flips the moment the commit exists; a cleared finding stays named in the report beside the
commit that answered for it. Three shapes never clear: a command that names no single file, a
finding the check cannot place in a repository, and a record with no timestamp. The verify arm, the
one that stands between a worker's result and its acceptance, never puts the question at all. The
counting start did not move, and no ledger, flag, date or counter was added.

**A sentence that names you and puts words in your mouth now reds on every live page** (q-497,
landed 31.08). The check that guards this reached two files before today — the decisions page and
its template — so a sentence crediting you with an instruction you never gave passed unnoticed
anywhere else, which is the kind of page the original incident used. It now blocks that sentence on
the 176 live pages of the tree, everything outside the dated records, the journal, the archives and
the working notes, which narrate what already happened and stay outside by design. The tree as it
stands passes. Two things it still does not catch, said here rather than left to be discovered: a
claim that names you only as a pronoun or a role, which is this project's own rule language on
nearly every page and stays a reported candidate on the two pages an attribution is first written
on, and a sentence that credits you with no authority word beside your name. The decisions page you
read back is the defence for both. The rule behind it now says what it always said — where a
recorded decision's authority comes from — and the half the incident was actually about: a session's
instructions come from you, from the tooling and from a wrapper at once, only yours carry your
authority, and where two of them conflict the reply says so and your standing word decides. It lives
in rule 13 of the base rulebook and in no second file, and the one-home check now holds it there.

**Every rule the pack states now has one place it lives, and a check keeps it there** (plan-16,
landed 31.08). Three rules had been written in several places that disagreed: the report Alexander
reads at the top of every reply, the law about running work in parallel, and the duty to ask rather
than guess. Each converged to one home, and everywhere a copy used to stand there is a pointer at
that home. Six skills stopped advertising three rules retired in August. The check is
`tests/test_one_home_per_rule.py` — it names one home per rule, reds if a second copy appears on any
surface that tells a session how to work, and passes on a pointer; its reach and its blind spot are
written in its own opening. Two pieces are deliberately unfinished and both are recorded: `PLAN.md`
itself still holds three copies (§Blockers says which, and why the lane could not write that page),
and the report format's own two homes in Alexander's personal layer still state its length two ways
— seven to ten lines in his boot file against ten or fewer in his profile — which only the window
that owns that layer can settle. The director can now name the home of a rule it has never seen: the
five houses and their declared sentences are in its request-kind reference, and two worked runs are
in `docs/skill-review/2026-08-31-one-home-per-rule.md`.

**There is one list now, and it is `PLAN.md`.** The wish queue that stood beside it is retired: it
had held no rows since 27.08, yet the lane-opening script, the rotation gate, the state probe and a
dozen tests still read it, so a second list went on existing in the machinery after it had stopped
existing in the work. The file itself now rests at `attic/ROADMAP.md` with its manifest line, and
its rotation pointers moved whole into `PLAN.md`'s own "What has been rotated off this list"
section, so every archived row stays findable from the one live list.

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

**The roster of feature names went from seventeen to twelve**, and the rule behind it is mechanical:
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

**Both of the things that task left open are closed, and `plan-12` is ticked.** The decision sheet
has its ordering line — which open piece of accepted work runs next and why that one, read off the
states the plan records — written from the main tree with `scripts/sync-skills.sh` run in the same
breath, so ten installed skills match their source and `tests/test_config_health.py` is green.
Requirement 314 claims the field again. And q-437, checking for similar cases at every level, is back
on the board as its own open row: it was folded into `plan-12` on 27.08 and never worked, so the
promise the spec still carries now names an open row instead of a finished one. Its definition of
done names the command that will decide it. The same promise has a second half, the value-space
forcing step that was q-436's, and nothing owns that one; it is written up in `PLAN.md`'s §Blockers
for the owner.

**The merge is where the defects were, and two fresh readers found them.** Neither had a part in
building any of it, and both were briefed to refuse. Five repairs landed. The one-home check could be
switched off with no red anywhere — its arms run once per rule in a table, so emptying the table gave
three skipped cases and a clean exit; the floor is named in the file now. The check that keeps a
feature name off an unbuilt scenario read the promised-marker anywhere in a requirement, so a leg
still promised inside a scenario the product does give a person read as a promised scenario; fifteen
of the nineteen markers in the spec are exactly that kind, and it passed today only by luck of
placement. The proof that the opening probe tells a stale score from a fresh one was five string
searches over the probe's own source, and survived the comparison being reversed; the branch is lifted
out and run both ways now. `plan-12`'s acceptance command read three function names out of two test
files, so the whole stray-part fault could be emptied to a bare return with the command still green;
it runs the two proofs for real now, in four tenths of a second. And the feature roster went from
seventeen names to twelve, not ten — the number was wrong in this file, the plan and the journal.

**A line number written in one tree stops being true when another tree inserts lines above it.**
Sixteen pointers across the project named the wrong line after the merge. One reddened the pin gate;
the other fifteen passed only because that gate forgives a two-line miss. All sixteen were re-read
against the files and corrected. Two more sit inside `PLAN.md`, where that page's own rule forbids the
edit, and they are written up in its §Blockers.

**Three things stand in §Blockers rather than repaired.** The suite is red on five checks because the
external reviewing skill installed on this machine is three releases ahead of what this project pins;
the server installs the pinned version and is green, and moving the pin is its own piece of work. The
idea shelf is promised in the spec and owned by no row, because the check that demands an owner reads
the marker by the line above it and this one sits under a heading — the same argument that put q-437
back on the board, applied to the promise this landing made. And "a question you ask never turns into
a task" is ticked while its acceptance command fails: it asks that the recorded runs of the reading be
newer than the skill they grade, and commit `98a003b5` edited that skill. The behaviour did not
regress; the proof lapsed, and re-recording the runs is a session's own work against the skill.

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
