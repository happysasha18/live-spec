# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-09-03, 19:26)

**Pushed. `origin/main` is `45a470b9`, 70 commits, all gates green.** Everything the 15:32 write
below left open for this session is now closed:

- **Director eval, full re-record (both sets), done.** 31 of 36 act-classification scenarios pass
  (was 30/35 on the same skill text before today's edits); 7 of 9 closing scenarios pass. Two
  closing reds are real, not noise — both are cases where the Director should have said `closes:
  false` (a taste call; a change to the definition of correct) and said `true` instead, the same
  over-correction class as the work-board finding below. Not fixed this session — recorded here so
  the next skill edit to `skills/director/SKILL.md` reads this before touching the closing rule
  again.
- **The comprehensive adversarial review of the whole pushed range, done.**
  `docs/prover/2026-09-03-full-range-adversarial-review.md` — one non-blocking finding (q-813 and
  q-815's closing notes overstated the suite as green at close time; corrected in place, citing the
  review, in the same commit that restored q-813's other over-retirement below).
- **`q-811`'s retirement did NOT need his word after all — re-tested by derivability and reversed.**
  The session that closed `q-813` retired `spec/work-board.md` Requirement 309 (99 criteria, an
  approved sketch) whole, past what the owner had already settled the morning before: his
  2026-09-02 12:46 word, on record at `.live-spec/turnkey-contract-composed.md:305`, kept R309 and
  deferred it to build after package 2 — never retired it. That word already answered the question
  q-813 left open; asking again would have been the same mistake `q-813`'s own text names (an
  amorphous marker treated as needing his word when an artifact already settles it). Restored
  (minus the one piece his same word did retire — the ~5s auto-refresh heartbeat, which stays cut)
  and requeued as `q-816`, carrying a real checkable trigger (package 2 closing) in place of
  `q-811`'s uncheckable "a real ask for it." Two follow-on findings from the restoration's own
  review (`docs/prover/2026-09-03-work-board-restoration-review.md`): 32 stale pointers naming the
  closed `q-166` instead of `q-816`, fixed the same session; one real scope gap
  (`spec/live-status-reporting.md` R310 criterion 10 promises something `q-816`'s own acceptance
  cannot reach) recorded as a `PLAN.md` Blockers entry for the owner's decision, not fixed
  unilaterally.
- **Full suite green on the quiet, fully merged tree**, twice in a row (2790 passed, 5 skipped, 0
  failed, both runs ~24 min) — pushed on that certification, per standing word.

**The push gate itself needed three follow-on records before it would pass** (SPEC INV-304, "one
record per push, naming the pushed range by commit"): a scoped record for the work-board
restoration's touch on `PRODUCT_SPEC.md`, one for a mechanical rename's touch on `ARCHITECTURE.md`,
and finally `docs/prover/2026-09-03-push-review.md` — the one record every earlier record's own
commit had itself left uncovered, since each new record commit becomes the newest commit in the
range. Worth a look before the next push: every one of these was a real, correctly-firing gate, not
a false positive, but four sequential records to land one already-fully-reviewed range suggests the
gate's own UX could tighten — nothing to fix tonight, just flagging the pattern.

**Two live findings recorded in `PLAN.md`'s Blockers, neither fixed, both correctly left
for a person:** the R310/`q-816` scope gap above, and the pre-existing five-check reviewing-skill
version mismatch (local install 1.6.0 vs. this project's pin 1.4.2) from the 31.08 write below,
still unresolved and still not this session's to fix.

## Open, for the next session

1. **Two closing-scenario reds in the director eval need a look before the closing rule in
   `skills/director/SKILL.md` is touched again** — see LIVE STATE. Not urgent; nothing depends on
   them today.
2. **The R310/`q-816` scope gap is a `PLAN.md` Blockers entry waiting on his policy call** (widen
   `q-816`'s acceptance, or give the criterion its own row — neither reading is derivable from an
   artifact already on file) — see LIVE STATE.
3. **The five-check reviewing-skill version mismatch (local 1.6.0 vs. this project's pin 1.4.2)
   is still open**, carried forward from 31.08 — the server stays the honest green reading.
4. **Not open, correctly so, no action needed unless he raises it:** `q-54` (onboarding, left
   alone on his own word), `q-48` (host-side leg is tlvphotos's own window's job, a wish already
   sitting in its inbox since 02.09), `q-385` (its own revisit trigger — a host declaring a real
   contract — hasn't fired), `q-816` (queued, waiting on package 2 to close).


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

**Everything below this line was rewritten 2026-09-03 19:26, this session's own close.** Check
`bash scripts/state-probe.sh` and this file's own LIVE STATE section above first; if things have
moved further since this was written, trust what you observe over this prompt.

Do not ask Alexander anything before doing the work below unless it's genuinely his — a taste
call, a policy question, or an act irreversible outside git. Re-test that before asking: two things
raised as questions to him earlier tonight turned out derivable from standing rules or his own
already-recorded word — check whether the answer is actually already written down before treating
anything as his.

**Everything the 15:32 write left as this session's own work is done and pushed**: the director
eval, the range-wide adversarial review, the work-board restoration (re-tested by derivability
rather than asked, per his own 2026-09-02 12:46 word already on record), and the push itself —
`origin/main` is `45a470b9`. Nothing here is blocking. The three genuinely open items are listed
above under "Open, for the next session," and none of them needs a session's first move — they wait
on his own decision (the R310/q-816 scope gap), on a look at the eval's own text (the two closing
reds), or on nothing this project controls (the reviewing-skill pin).

**The plan is closed except onboarding** (`q-54`, left alone on his own word) — `q-48` and `q-385`
stay open on their own real, unfired triggers, not on anyone's word. Nothing else to decide there.

**Method, proven again tonight:** up to ten parallel worktree lanes (`Agent` tool, his own raised
cap), each briefed with the row's own `PLAN.md` text pasted verbatim, the worker-restore rule
copied verbatim, and told explicitly not to rebase/merge/push — the orchestrator integrates. Merge
one row at a time, rebase onto main's tip first, re-verify independently from the merged tree, then
clean up the lane. Watch for two real collision classes that showed up tonight even with worktree
isolation: two lanes independently picking the same next-free matrix row id (check `grep -rhoE
"^\| M-[0-9]+" matrix/*.md` before trusting a new row number), and a lane forked before an earlier
lane's own landing carrying a now-stale copy of a shared map entry (`tests/test_traceability.py`'s
`TARGET_ROW_OWNERS`, most often) through its own rebase. Also watch for: running the full suite
inside one lane while committing to another moves that lane's own tree mid-run and reds a
completely unrelated test (`test_worker_restore_run_scope`) — happened twice tonight, both
self-caught; run one lane's full suite at a time with nothing else committing to it meanwhile.

Report in the Канон format his own boot file (`~/.claude/CLAUDE.md`) specifies —
`bash scripts/state-probe.sh`'s own printed plan, never a hand-typed summary — after every row
that lands, not only at the end.
