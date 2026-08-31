# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-09-01, 00:20)

Written for a session starting with clean context. Heals landing d470d2be, heals landing dbf0fc01,
heals landing 1bdd55c1. Alexander, 2026-09-01 ~00:05, on this window's context size: asked the
session to merge, push, and stop here so context can clear before continuing — this note is
written for that fresh session.

**Three rows landed since `bff2715a` pushed, in parallel worktree lanes, merged with no conflicts:**
`q-581` (a `PreToolUse(Bash)` hook, `hooks/dialog-warning-guard.py`, warns before a command known
to raise a macOS security dialog — the flat list this row's narrowed acceptance asked for, no
reaper, no registry), `q-489` (`tests/test_guardrail_fixture_proofs.py`: `check-prototype-fence.sh`
proven against a live fixture, a walking test that reds a future `guardrails/` check shipped with
no fixture, proven itself by planting one), and `q-235` (`scripts/wind-down.py`: signals every
locked worktree's worker unless it's the session's own controlling process, checkpoints, pushes
only on a green gate, one closing line). Also landed in the same range: three dead rows archived
(`plan-15`, `q-453`, `q-751` — `docs/queue-archive/rotated-PLAN-2026-08-31-hostile-review-archive.md`),
`q-48` correctly KEPT rather than archived (it owns spec anchor `INV-21` — archiving it would have
orphaned that promise), `q-398` narrowed (struck a bare threshold with no outside source), `q-536`
narrowed to its one real remaining leg (two of three wording disagreements the row named turned out
already resolved by later skill rewrites — verified directly, not assumed), and `plan-14` checked
honestly and left open (it's real install-infrastructure work, not a one-lane narrowing — see its
own `PLAN.md` note for why nothing was built there tonight).

**Two things a fresh clean-tree suite run found that the merge itself introduced, both fixed before
push:** `scripts/wind-down.py` named "Alexander" in a comment (shipped-language gate, INV-120/245
— fixed to read impersonally) and signaled a worker process without emitting the project's
`CLEANUP-NOTICE` line (INV-204 — fixed by wiring `guardrails/cleanup_notice.py` into
`signal_worker()`). Neither worker's own suite run caught these because each ran in its own
worktree, where the *other* two lanes' files weren't present yet to interact with — a reminder that
the merge is genuinely where defects hide, not just where they're found, and a clean full suite on
the MERGED tree is not optional.

**A lesson for how worker lanes were briefed tonight, worth fixing in the next round's briefs:**
all three of tonight's worker agents launched their own ~10-12 minute full-suite verification in
the background and then ended their own turn instead of blocking on it — the orchestrating session
had to notice, wait for each background run itself, and in two of three cases finish the commit and
`PLAN.md` closing note by hand (the code itself was already correct and complete in both cases;
only the "wait, then commit" tail was left undone). Next time: brief a worker explicitly to block on
its own suite run (e.g. "run it in the foreground, or if backgrounded, poll or wait before ending
your turn — do not report done until you have the actual pass/fail line").

**One more standing risk, unrelated to tonight, surfaced but not investigated:** two worker agents'
own full-suite runs reported `57 skipped` where this session's own runs on the same commit range
consistently show `6 skipped`. Not chased down before the stop — worth checking early next session
(`python3 -m pytest -q -rs 2>&1 | grep -A1 SKIPPED` on a clean tree, no other pytest running, to see
which 51 extra tests are skipping and why — likely something environment-specific to a fresh
worktree checkout rather than a real regression, but unverified).

**Everything unpushed went out.** `16b1a300..bff2715a`, 21 commits, `origin/main` carries it. CI
run `33436005985` was in progress at push time; check `gh run list --branch main --limit 1` if this
note is stale by more than a few minutes.

**The two real gate failures the 31.08 21:35 note left open are both closed, plus two more the
full suite surfaced that the same note had missed.**

1. `tests/test_traceability.py::TestTargetOwnership::test_targets_owned_by_open_rows` — closed
   honestly, not by weakening the test. Of `q-55`'s five orphaned `[target]` anchors: `A-6` is
   `q-55`'s own landed work. `E-6`, `E-10`, and `INV-17` — Requirement 102's "fence guardrail's
   two remaining legs" (`spec/design-spec-review.md`) — turned out already BUILT, by row 241
   (commit `f008e5b2`), well before tonight: `guardrails/pre-push` gate h runs
   `scaffold/guardrails/check_completeness.py` and `check_traces_to_spec.py`. Their `[target]` tags
   were simply stale and are now dropped. Only `E-7` (design-sync's declared-scope snapshot
   machinery, Requirement 247) is genuinely still unbuilt. A first attempt re-pointed it to `q-54`
   on the theory that `q-93` (design-sync) folded into `q-54` on 2026-08-28 — an adversarial push
   review (`docs/prover/2026-08-31-target-ownership-correction.md`, finding F4) caught that `q-54`'s
   own written acceptance never actually names design-sync, which would have silently re-orphaned
   `E-7` the moment `q-54`'s acceptance gets narrowed (which the hostile review below already
   flags it for). Archive research settled it: `E-7` was always row 55's own promise, historically
   (`docs/queue-archive/rotated-ROADMAP-2026-07.md` row 468), never row 93's — restored as its own
   row, `q-802`, the same way `q-437` was restored earlier tonight. `E-18` (design-sync the feature)
   stays `q-54`'s, unchanged; a non-blocking note in `docs/prover/2026-08-31-e-7-restored-as-q-802.md`
   flags that `E-18`'s `q-54` mapping rests on the same unproven fold claim and will need the same
   fix whenever `q-54` is next closed or narrowed — not done yet, watch for it.
2. `tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` — was already clear
   at session start, confirmed.
3. **New, found only by running the full suite clean (the prior session's diagnosis had not run it
   since its last edit):** `guardrails/check-authority-anchor.py`'s date scanner is ISO-only
   (`\d{4}-\d{2}-\d{2}`); a sentence crediting Alexander in `NEXT_STEPS.md` dated `31.08` rather than
   `2026-08-31` hard-failed the gate on every surface, not just decision records. Fixed by writing
   the date in full. **Lesson for whoever writes this file next: dates near a sentence naming
   Alexander need the full `YYYY-MM-DD` form, not the short `DD.MM` form used everywhere else in
   this project's prose — the short form reads fine to a person and reds the gate.**
4. **New:** three same-day `live-spec-base` skill-review records (`instruction-authority`,
   `gate-clause-reach`, `one-list-for-a-new-project`) each predate the merge commit (`130a67e6`)
   that actually landed them on `main`, since each was written on its own lane branch before the
   merge. `guardrails/check-skill-review.sh` wants a record whose own commit is at or after the
   skill's last change, and none of the three alone qualified — a fourth record
   (`docs/skill-review/2026-08-31-live-spec-base-merge-lands.md`) ties them together without
   re-reviewing content already covered. **Lesson: a multi-lane merge into `main` can make every
   lane's own same-day review look stale by commit-clock, even when nothing about the reviewed
   content actually changed — check this before assuming a real content gap.**

**A hostile read of the remaining board found five rows to archive, one already done, and eleven
overbuilt — and a second, independent skeptical pass over the same rows (run because Alexander
asked directly not to trust the first pass blindly) corrected five of its findings.** Full findings
in `.live-spec/checkpoints/night-run-2026-08-28.md`. The corrections, layered on top of that
checkpoint's own buckets:

- **`q-386` is NOT moot-close, contrary to the first pass.** Its own row text (edited 21:14, after
  the first pass closed) says one leg has no check at all: nothing today proves the lane-opening
  script and the written law describe parallel-work the same way, so the two could drift apart with
  nothing to catch it. Build only that one leg; do not close as moot.
- **`q-54` is nearly done, not a fresh build.** `grep -q 'project.kind'`, `'project.layers'`,
  `'project.proofs'` already pass against `~/tlvphotos/.live-spec/profile.md` — only the line naming
  who the project is founded for is missing there. This is a one-line edit in ANOTHER project's
  tree; this window may only drop a wish into `~/tlvphotos/inbox/`, not write it directly. Not done
  yet.
- **`q-163`'s first acceptance clause may already be satisfied** — `test-author` passes
  `check-skill-loadability.sh` today. Re-check before dispatching a worker on the row as originally
  scoped; it is likely narrower than the checkpoint's own bucket assumed.
- **`q-536` rests on an unwritten self-ruling.** Its "his final call is not owed" note has no
  corresponding text anywhere on disk — write the actual ruling into its source file first; a
  worker dispatched on the row as currently worded would be proving a decision that was never made.
- **`q-398`'s acceptance text still contains the forbidden bare threshold** ("the preamble carries
  its own declared size cap") that the first pass said to strike. The strike itself never landed in
  `PLAN.md`. Edit the row's own acceptance text before dispatching a worker — handing the
  un-narrowed wording to a fresh agent is exactly the `q-55` failure mode this whole run keeps
  citing as the thing not to repeat.
- The other narrowing calls (`q-581`, `q-576`, `q-437`, `plan-14`, `q-489`, `q-235`) and the
  solid/archive buckets (`plan-10`, `q-591`, `plan-15`, `q-453`, `q-48`, `q-751`) held up under the
  second pass; build/archive as the checkpoint already scopes them.

**Not touched, not needed:** no new queue row for the fence's two "remaining legs" — they turned
out already shipped (see point 1 above). One new row was genuinely needed and added: `q-802`.

**Still owed, unwritten, carried forward from an earlier note:** a `JOURNAL.md` entry for
the prover-description-test movement (`85b659d1`, from 31.08 morning) and for tonight's
whole `16b1a300..bff2715a` range.

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

**Everything below this line was written 2026-09-01 00:20, right after the range this LIVE STATE
describes pushed clean (CI to be confirmed by you — check `gh run list --branch main --limit 1`
first thing). Read `bash scripts/state-probe.sh` and this file's own LIVE STATE section above
first — this prompt only tells you what to do with what they show you. This session was stopped
deliberately by Alexander (context had grown large after ~2 hours autonomous), not because
anything is stuck — pick up exactly where this leaves off.**

Do not ask Alexander anything before doing the work below. His standing word for this run (28.08
00:53, repeated 31.08 12:12, 18:32, 22:07, and again ~00:00 confirming "да" to stopping and
resuming): carry the plan to the end, do not ask him, push and deploy are pre-authorized on green.

**First, the two open loose ends from the note above, both quick:**
1. Confirm CI is green on the just-pushed range.
2. Spend five minutes on the `57 skipped` vs `6 skipped` question (see LIVE STATE) before starting
   new work — if it's real, it's worth knowing before building on top of it; if it's a worktree
   quirk, say so and move on.

**Then walk the remaining hostile-review rows, same method as before** (checkpoint at
`.live-spec/checkpoints/night-run-2026-08-28.md`, corrections layered by this file's LIVE STATE
history — read it, not just the checkpoint, before trusting any one row's old bucket):
- **Solid, build as written:** `plan-10`, `q-591`.
- **Keep open, build only the one real gap:** `q-386` — the lane-opening-script-vs-written-law
  drift check, nothing else.
- **Narrow before build, already narrowed, ready to dispatch:** `q-576` (the sweep already ran;
  this is publishing its page — small), `q-437` (the one red-proof case named in its own
  `PLAN.md` text, nothing wider), `q-802` (new: design-sync's declared-scope snapshot machinery,
  Requirement 247 in `spec/doc-order-generated.md` — its `PLAN.md` row states the exact scope).
- **`q-536`:** narrowed to its one remaining leg — read the current `q-536` row in `PLAN.md` for
  the full ruling on the other two (already resolved, don't re-open them). The leg left: check
  each of communicator's fourteen rule collisions
  (`~/context-slimdown/reports/communicator-audit-sweep.md`, read-only, another project's tree)
  against today's `skills/communicator/SKILL.md`, and write a one-line ruling for each into that
  skill's own text.
- **`plan-14`:** deliberately NOT narrowed for a worker lane — its own `PLAN.md` row explains why
  (real install-infrastructure work spanning the pack's install/adopt walk, not a mechanical
  narrowing). If picked up, it deserves its own dedicated pass, not a shared lane with three other
  rows.
- **`q-163`:** stays parked with `plan-9` — do not start it. Its own `PLAN.md` history already
  notes it may be more than half-done; re-check before ever dispatching a worker on it.
- **`q-54`:** the wish is already sitting in `~/tlvphotos/inbox/2026-08-31-from-livespec-q54-founding-line.md` — nothing to do here until that project's own session acts on it.

**Method, unchanged from the whole run:** up to three parallel worktree lanes (`Agent` tool,
`isolation: "worktree"`), each briefed with the row's own PLAN.md text pasted verbatim as the
definition of done — **and explicitly told to BLOCK on its own full-suite run before ending its
turn, not background it and stop** (see LIVE STATE's note on tonight's briefing gap). Merge by a
dedicated pass that reads both sides on conflict; run ONE clean full suite on the merged tree with
NO worker active (a run taken while a worker writes the tree proves nothing); then an adversarial
re-read from a genuinely fresh context (SPEC INV-237 — never a fork of the orchestrating seat,
never the agent that wrote the fix) before push. This caught real defects on nearly every merge
tonight — most recently the shipped-language and cleanup-notice gaps in this very range, introduced
by the merge itself and invisible to each lane's own isolated suite run. Do not skip it as a
shortcut, and expect a review's finding to sometimes need its own fresh follow-up review in turn —
that's the check working, not a sign of trouble.

Three rows wait on Alexander's own read and take no further work: `q-800`, `q-166`, `q-501`.

Report in the Канон format his own boot file (`~/.claude/CLAUDE.md`) specifies —
`bash scripts/state-probe.sh`'s own printed plan, never a hand-typed summary — after every row
that lands, not only at the end.
