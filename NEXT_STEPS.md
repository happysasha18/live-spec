# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-09-02, 22:45)

Written for a session starting with clean context, covering the night run in `9a300f9e..5fcf2326`
(this file's own last refresh, `4b898f65`, sat un-updated through that whole range — heals landing
`9a300f9e` (q-166) and `871e234a` (q-808), both of which closed a row without touching this file,
INV-242, the same shape prior ranges already carried).

**Two new standing rules, his own word, both in `skills/director/SKILL.md`.** He asked why a task
(`q-166`) should ever sit open on nothing but his own eye watching it, then, catching that this
session had just done real director-level work on that question but treated his very next remark
("you can always argue if you disagree") as a passing aside instead of the same kind of thing:
- **A shown result closes the work.** Writing the decision sheet already earned the right to
  close a row once the result is delivered and shown; a row's own "needs his eye" gate is now
  reserved for a taste call, an undecided trade-off, or a change to the definition of correct
  (rule 12/27's own three cases) — never for verifying an ordinary delivery a command or a plain
  read already confirms. His later disagreement opens a new task; it never reopens the one that
  shipped.
- **The Director states disagreement before executing.** Writing the decision sheet is also the
  one moment to weigh whether the request itself is right; a flaw the Director can see gets voiced
  before the checkpoint opens, not folded silently into how the work gets built.

Both landed with `DECISIONS.md` entries naming the dated exchange. A closing-rule eval (4-5 fresh
scenarios distinguishing an ordinary delivery, a genuine taste fork, and a flawed request) is in
flight under `evals/director/closing-scenarios.json`, separate from the existing 35-scenario
act-classification harness — check its own worker's report before assuming it landed.

**`q-166` closed under the new rule; `q-811` opened to carry what it didn't finish.** The daily
need (`board.html`) already ships; the larger unbuilt feature (worker lanes, given-vs-actual time,
per-agent attribution) had no real ask behind it since 08-06, so it moved to its own row, `q-811`,
rather than staying open on a gate the new rule just removed — the same repair shape `q-385`/`q-804`
already used for a promise a closed row stopped carrying (two `[target]` tags, `INV-308`/`INV-67`,
re-pointed in `tests/test_traceability.py`'s `TARGET_ROW_OWNERS`).

**`q-808` closed on a real outside-reader check**, not a session judging its own prose: a fresh
agent holding only `PLAN.md`'s open task headers read each cold; 8 of 11 held, 3 (`q-809`, `plan-9`,
`q-163`) were genuinely liable to mislead and got minimal title fixes in place.

**`q-812` opened, queued behind this range** — his own brief, kept verbatim in the row: prove the
Director's real route end to end (free message in → correct classification → exactly one task with
its own DOD → a worker executing it → a DOD-and-check-gated close → a fresh session resuming
without duplicating or guessing), on the actual mechanism (`PLAN.md`, `checkpoint.py`,
`state-probe.sh`, product-prover, test-author, `TEST_MATRIX.md`), no new machinery. Starts only
after this range's own open rows close.

**`q-809`, still open, two of its four remaining legs closed tonight:**
- The rulebook cut (`f6668634`, 40,443→22,683 bytes) and its own second-reading hostile review
  (four more genuine losses across rules 6/7/9/31) both landed *before* this session started
  (`33ee1b38`) — this session found the loss-verdicts checkpoint stale and marked it resolved
  after verifying the fix by direct grep, not from the commit message alone.
- **Decided: `DECISIONS.md` keeps its place**, not folded into `JOURNAL.md` — a wired push gate
  (`guardrails/check-authority-anchor.py`) reads it by name for a dated-exchange shape, it holds a
  retract mechanism and an open-questions section the journal has neither, and the 50% content
  overlap with the journal is expected cross-reference, not duplication. (This mirrors a verdict
  the 16:57 range had *already* reached under `c6ffc709` — this session re-derived it independently
  before finding that note here; same answer, worth reading this file before re-deriving next time.)
- Still open: the 35-scenario director eval re-record (mandatory — the skill changed twice
  tonight; in flight, its own worker briefed), a lightweight skill-creator structural pass (done,
  no defect — both files already fit the tool's own progressive-disclosure pattern; its heavier
  benchmark-and-browser loop was skipped as disproportionate for a prose skill with no gradeable
  file output), and a final re-measure once both land. The quarter he asked for was never reached
  and won't be tonight either — `.live-spec/checkpoints/q809-startup-weight.md` says why (the boot
  file is his; director's own cut was reverted against an eval that can't yet resolve a 3.7 KB
  question).

**`q-804`, in flight, not yet merged.** All three arms (merge-base caller via a new
`scripts/land-lane.sh`, worktree-line caller in `adopt/install-scaffold.sh`'s closing step, and a
new stale-lane arm in `guardrails/check-config-health.sh`) are built and hand-proven by its own
worker; a full-suite confirmation was outstanding as this was written, and nothing is committed on
its lane branch yet. Its own worker also found a real sibling-class finding: several guardrail
scripts (`check-delta-record.py`, `check-deposit-description.py`, `check-landing-next-steps.py`,
`check-tier-refusal.py`, `check-config-surface.py`) have tests but no real caller anywhere in the
tree — reported, not fixed, per this row's own scope.

**Two process lessons from this session, worth carrying forward:**
- A worktree created fresh by `git worktree add` does not carry `skills/product-prover/`'s or
  `skills/text-audit/`'s own nested external-skill clones (untracked, gitignored) — a full suite
  run there shows ~50 unrelated failures, all the same "external clone … not installed" message.
  Not a regression; filter on that string or copy the two clones in for a clean read.
- Running the full suite inside an isolated worktree can leave `docs/MEASUREMENTS.md` mutated as a
  side effect (some test writes it without cleaning up) — a real, separate bug, not this session's
  own work. If it shows modified and you didn't touch it: `git show HEAD:docs/MEASUREMENTS.md`,
  write those exact bytes back with the file-writing tool, never `git checkout` it (the
  worker-restore guard here refuses that command and says the same).
- Do not land a commit to the primary tree while a full-suite run against that same tree is still
  in flight — this session did exactly that once tonight and its own suite run caught it
  (`test_worker_restore_run_scope` reds on a HEAD that moved mid-run). Land, then run the suite
  clean with nothing else committing meanwhile.

**`q-809` — the weight a session loads. Honest partial, stays open.** Measured by the probe's own
line: 80,122 bytes before, 63,541 after, 18,501 tokens to 14,793. He asked for about a quarter of
the original and it is not reached. The three parts of the answer:

- **The rulebook, 40,443 to 22,683 (`f6668634`).** Each of the twenty-two shared rules is now one
  instruction with its SPEC codes and the check that reads it; the sub-laws under rules 6, 7, 13
  and 31 are one line each. Citations, histories, justifications and worked examples moved to
  `skills/live-spec-base/references/rule-origins.md`, 6,539 bytes, which holds background only —
  a rule restated there would be the second home rule 4 and INV-13 forbid, and
  `tests/test_one_home_per_rule.py` holds that line. Two rules were genuinely lost in the first
  pass and restored: rule 6's worker-liveness apparatus (worker id, briefed write-set, liveness
  checks, the ~60 s heartbeat, INV-76, the leave-word extension INV-95) and rule 7's single pen
  with INV-49. 44 tests went red across the pass; the pin sweep in `architecture/*.md` closed the
  rest.
- **Director, cut and reverted (`43d5f388`).** It went 25,613 to 21,900, then back. Two full
  re-records of the 35-scenario eval ran the same afternoon, one producer per scenario, opaque
  labels: the skill as it stands scores 30 of 35, the cut scores 29. One scenario is inside what
  the method can see, so 3.7 KB was not worth an unresolved question at the pack's front door.
- **The boot file, untouched.** 4,386 bytes, his own by his word of 26.08.

**What blocks the rest, and it is the measurement.** While the second re-record was still
finishing, its partial trace set graded 32, then 31, then 30 as the last producers landed — the
grader unchanged and re-checked as deterministic on a fixed set. So one bare run carries about two
scenarios of producer variance. `evals/director/README.md` now says that, says to compare only
differences larger than it, and says to grade a complete trace set. Reaching the quarter means
taking director to about 5 KB, which is a rewrite of the door, and it needs a check that can see a
small change first: more fixtures, or a grader that scores per act instead of per scenario.

**His four standing changes, all landed.** From two messages, 02.09:

- Blocked and reopened are two states (`37c40c7e`, then `72a52a4b`). A done row whose acceptance
  command fails wore ⛔ since 28.08, which spent the blocked mark on a row nothing outside holds
  up. It went to ⬜ on his first correction, then to its own mark 🔁 on his second. Blocked keeps
  its meaning, a real outside cause in `blocked_by`; queued keeps its own, never started. Written
  into `spec/wish-intake.md` Requirement 4 clauses 10-11 (INV-321).
- Done tasks are not counted by default; the summary line leads with the open count.
- Every printed row opens with its own id, padded to the widest id in the plan.
  Both in `spec/message-first-read.md` Requirement 314 clauses 7-9 (INV-319).
- Up to ten lanes in parallel, each with its own worktree and a clean merge, and sonnet workers by
  default with a stronger tier as the justified exception. Both recorded in the personal profile.

**The standing-file census (`c6ffc709`).** Every standing document in the tree has a script, test,
skill or hook that reads it by name — none answers "nothing breaks". His own named question,
whether `DECISIONS.md` still earns its place beside the journal: it does. 26 of its 56 entries
appear nowhere in `JOURNAL.md`; it holds his words verbatim, a retraction section and an
open-questions section the journal has none of; and `guardrails/check-authority-anchor.py` reads it
by name as a push gate. Of the 34 dated one-off notes in `.live-spec/` that no script reads, 26 are
cited by the prover records under `docs/`, so removing them would leave a review pointing at
nothing; the other 8 are gone. `docs/` itself, 941 files and 12 MB, was flagged and not censused.

**`plan-0` reads green again.** Its acceptance held a fourth clause, an empty `git status
--porcelain`, so a finished row reported itself unfinished on any session that had edits in hand.

## Open, for the next session

1. Two push gates are red, neither from this run. The shipped-language gate names Cyrillic a
   previous session pasted into `PLAN.md`'s q-809, q-807 and q-808 source lines; his words belong
   in `DECISIONS.md` and the row states the requirement impersonally. The prover-record gate wants
   a review record newer than the last `PRODUCT_SPEC.md` change. Both had lanes running at the time
   this note was written; check them before assuming.
2. `q-806` is marked done with neither an acceptance command nor a reading line, so
   `tests/test_plan_done_marks_are_backed.py` is red on it.
3. The director cut is available if a sharper check ever lands: the run and its numbers are in
   `evals/director/README.md`, the reverted text in `43d5f388`'s parent.


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
into the background, and the suite runs 18 to 24 minutes. A worker that starts it stalls and then
returns an unfinished report as final, or worse, reports a stale background run against a worktree
the orchestrator has already reclaimed — happened twice tonight, both self-diagnosed correctly by
the worker rather than acted on. A brief names the exact test files that finish in seconds. The
orchestrator runs one clean full suite at the end of a pass with no worker active. A run taken
while workers write the tree reds on files being written, and its reds carry no verdict.

**Tonight's addition: a worker process can die silently, mid-task, with no crash report** — just
gone from the agent list, its real uncommitted work still sitting safe on disk in its own worktree.
Happened once tonight (`q-804`). The recovery is not to redo the work: inspect `git status`/`git
diff` in the worktree, verify what's there for real (don't trust it because it looks done), finish
whatever's missing, and commit. Never run a destructive git command on a dead worker's worktree to
"clean up" — that would destroy real, unrecovered work.

## Prompt for the next session

**Everything below this line was written 2026-09-02 01:25, right after tonight's overnight run
(`534cb16b..49b4813f`) moved six of the prompt's own eight rows (three closed, two honest partials,
one returned to the queue) and fixed the two prose regressions the quiet-tree suite caught. A second
full-suite run and the push are still owed as this is written — check `bash scripts/state-probe.sh`
and this file's own LIVE STATE section above first; if both already show green and pushed, this
prompt is stale and you're likely looking at a later state than the one this was written against.**

Do not ask Alexander anything before doing the work below unless it's genuinely his — a taste call,
a policy question, or an act irreversible outside git. His standing word already covers pushing
tonight's range once the suite is confirmed green.

**If the suite and push aren't done yet:** finish that first — `python3 -m pytest -q` alone on a
quiet tree, `0 failed, 0 errors`, then push, per the LIVE STATE section above.

**If everything above is already green and pushed**, the next real work is the saved productization
phase: `.live-spec/next-phase-prompt-turnkey-productization.md`. Read it whole before starting — it
carries its own precondition (verify the current PLAN.md's state against the real repo, nothing
taken on faith) and its own five serial CI-green packages. Do not start it opportunistically; it
was deliberately deferred to either his own word or a morning check with nothing further from him.

**Still open on the board, each correctly left that way — do not start any of these without a real
reason to revisit:**
- `q-166` — a taste call: its own acceptance names his eye over one real stretch of work as the
  check, no command decides it.
- `plan-14` — real install-infrastructure work spanning the pack's install/adopt walk; a wrong
  wiring choice here is hard to unwind once every future adoption depends on it.
- `plan-9` — held by his own prior word.
- `q-163`, `q-48`, `q-54` — each has a real remaining leg that only a `~/tlvphotos` session can
  close (this window is read-only there beyond one inbox wish).
- `q-385` — its own revisit trigger (a host declaring its first real contract) hasn't fired.

**Method, proven again tonight, unchanged:** up to three parallel worktree lanes (`Agent` tool),
each briefed with the row's own `PLAN.md` text pasted verbatim, the worker-restore rule copied
verbatim, and told explicitly not to rebase/merge/push — the orchestrator integrates. Merge one row
at a time, rebase onto main's tip first, re-verify from the merged tree, then clean up the lane.
Watch for two real collision classes that showed up tonight even with worktree isolation: two lanes
independently picking the same next-free matrix row id (check `grep -rhoE "^\| M-[0-9]+"
matrix/*.md` before trusting a new row number), and a lane forked before an earlier lane's own
landing carrying a now-stale copy of a shared map entry (`tests/test_traceability.py`'s
`TARGET_ROW_OWNERS`, most often) through its own rebase.

Report in the Канон format his own boot file (`~/.claude/CLAUDE.md`) specifies —
`bash scripts/state-probe.sh`'s own printed plan, never a hand-typed summary — after every row
that lands, not only at the end.
