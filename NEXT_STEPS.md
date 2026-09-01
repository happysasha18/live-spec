# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-09-01, 16:46)

Written for a session starting with clean context, covering everything that landed in
`11987b80..HEAD` (this morning's push through this note). Heals landing 62394f45, heals landing
b9708261, heals landing 7e3f32e1, heals landing 4f86dfd9, heals landing 24152152, heals landing
2858c023, heals landing e3b745b1 — seven commits in that range closed rows without touching this
file (`tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` red on exactly
those seven), all healed forward here rather than rewritten into history — two of the seven
(`4f86dfd9`, `e3b745b1`) needed a second heal commit because the first one's message wrapped the
heal phrase across a line break and missed the checker's own regex; this line is that second
commit's own NEXT_STEPS.md touch.

**Verification and board hygiene.** `plan-10` (`bf319751`, `a488854f`, `b9708261`) built the
instrument first — a checker reading `PLAN.md` and `scripts/plan_checks.py` together that fails a
done mark backed by neither a real command nor a named reading — then used it: sixteen previously
bare ✅ marks (`q-801`, `q-490`, `q-497`, `q-527`, `q-55`, `q-567`, `q-581`, `q-586`, `q-489`,
`q-597`, `q-625`, `q-427`, `q-529`, `q-235`, `plan-0`, `q-458`) now carry a real check or a dated
reading; none turned out false on re-verification. `q-437` (`7e3f32e1`) made the axis-verdict sweep
`spec-author`/`product-prover-pack` already ran for sibling axes run at every composition level, not
just siblings, red-proven by `tests/test_composition_axes.py`. `plan-2` (`14808ef2`, `3147d6e2`) redrew
all thirty-five director-specialist traces fresh (the freshness rule fired because `skills/director/
SKILL.md` changed 31.08): 32 of 35 hold, one prior disagreement resolved, three new close calls
named rather than forced to match. `q-591` (`4f86dfd9`) fixed one stale matrix citation — M-313 now
points at the requirement that actually moved. `q-386` (`67bd98d1`) closed its one real remaining
leg: `tests/test_lane_open_act_convergence.py` reads `skills/live-spec-base/SKILL.md` rule 7's
lane-open bullet live at run time and checks a real `open-lane.sh` run against it, red-proven by
mutating the law's branch pattern on a throwaway copy and watching it catch the drift.

**New rule, and the row that follows from it.** Alexander, 2026-09-01 10:37: parallel work without
worktree isolation or a stated disjointness check has cost real tokens more than once. `5aacf3aa`
added "No unprotected concurrency" beside rule 7's existing brief-time-disjointness bullet in
`skills/live-spec-base/SKILL.md:150` — two writers run at once only under a stated safety measure,
and a repo nested inside another repo's own directory (a skill's own git clone under this tree)
counts as sharing the tree, judged by path. `q-803` (`3d4b8ae4`) was filed, not built: his own
objection to one inline "his word, DATE" citation in that same rule's prose swept to 31 hits for
"his word"/"owner's word" across `skills/*/SKILL.md` and `references/*.md` pack-wide — provenance
belongs in `JOURNAL.md` and each row's own `**Source:**` line, not restated in the rule text a
session executes. Acceptance written; the sweep and strip itself is still open.

**Numbers and citations.** `q-576` (`c8adff22`, `62394f45`) finished the number-provenance sweep:
`docs/prover/2026-09-01-every-number-in-the-tree.md` re-read the whole tree independent of the
27–28.08 pass and found thirteen more numbers with nothing behind them — twelve census survivors
the labelling pass had skipped, one new constant pair from a file that landed 31.08 — all now carry
the same source-admission every other number in the tree already does. Zero ungrounded numbers
left as of that read.

**Board-status corrections — real work found already done, or found not yet started.** `q-166`
(`d673c75c`, `adceb60b`) was re-marked ⬜ from 👁️ (nothing built yet for his eye to check), then
found that `board.html` + `render-board.sh` (built 31.08) already answer the daily ask he's repeated
four times — "one page to look at instead of asking the agent." What's left of the row is a
separate, larger, optional feature (worker lanes, per-agent time — `spec/work-board.md` Requirement
309, for a host project's own task queue), not a gap in what he sees today; nobody has asked for
that larger feature since 08-06. `q-800` (`2858c023`) closed: the playbook repo's own ordered
command list from `docs/reports/2026-08-31-playbook-repo.md` was already run and pushed there on
31.08 (`803924a`, `380d33b`, `3108b92`, `c648cf5`); nothing new to move today. One loose end from
that report stays open and untouched by this row: `plan-16` landed 31.08 without folding
`PLAYBOOK.md`'s two orphan rules into the pack, so those citations still stand — already tracked in
`PLAN.md`'s own Blockers section. `q-163` (`24152152`, and its matrix row re-committed for real in
`287e019c` — see the incident note below) partially landed: the pack side already stood
(`skills/test-author/SKILL.md` v6.1.0, `check-skill-loadability.sh` passing, the Director's
specialist table naming it), and what was missing — `matrix/test-author.md`'s row `M-620` proving
that wiring rather than leaving it prose, backed by
`tests/test_traceability.py::TestProblemLedger::test_director_names_test_author_at_the_derivation_step`
— now exists, red-proven live by deleting the specialist-table row from a working copy and watching
it fail. What's left is the field leg: one real host's own test matrix, written by this method,
landing in that host's tree (`~/tlvphotos`, candidate) — needs a session inside that project's own
window, not this one. `q-48` (`c30491b9`) corrected a month-stale framing: the row called itself
"deferred, trigger not yet fired" when the trigger — Alexander posting tlvphotos.com into three
Telegram groups — fired 24.07, GA4 property 544252011 has been live since, and
`~/tlvphotos/scripts/ga_report.py` already reports real numbers by hand
(`~/tlvphotos/inbox/handled/2026-07-27-from-promoter-ga-campaign-numbers.md`). What's actually built:
the human-triggered half (`FEEDBACK.md`'s field-evidence route, `INV-21`). What's still open,
pack-side: the automatic-fetch contract itself needs its own spec delta through `spec-author` before
code — no generic fetch interface exists yet to build against. What's separately open, host-side,
out of this window's tree: wiring tlvphotos's own status view to `ga_report.py` and Cloudflare,
which waits on the pack-side contract existing first.

**New builds.** `q-398` (`e2a0e8c4`) shipped a vendored routing-preamble hook that reaches an
adopted host project automatically, red-proven. `q-802` (`67f9ce6e`) built design-sync's snapshot
machinery: `.live-spec/snapshot/MANIFEST.md` carries one line per surface (baseline delivery id,
content hash, storage form), `baseline.py`'s `advance_baseline` moves a baseline only for the
surfaces a delivery actually declares, proven by `tests/test_snapshot_baseline.py` walking a
fixture delivery and checking an undeclared surface's line, bytes and mtime come back untouched.
`spec/doc-order-generated.md`'s Requirement 1 no longer cites `E-7` under `[target]`; the still-open
`E-18` (design-sync the feature) stays `q-54`'s.

**q-501 and the guard against its own recurrence.** `q-501` (`e3b745b1`) fixed the front page's
real Known-Issues defect: README's "Known issues" section carried a false claim (`surface_discovery_
pattern` supposedly can't match markdown, so `check_completeness.py` silently passes) that had
already been declared false once (2026-08-18), regenerated via a later cold-read pass (2026-08-26),
and survived a follow-up that patched only the syntax trap, not the substance, on 2026-08-27 — this
is its third appearance. Verified live before fixing: the pattern and the completeness check are
both correct and armed, proven by planting a real unregistered surface in a scratch copy and
watching it red. `cf244b5b` then added the guard against a fourth return:
`TestReadmeKnownIssuesNoFalseDiscoveryPatternClaim` in `tests/test_readme_stance.py` scans README's
Known Issues section for either half of the claim under paraphrase (not a brittle exact match) and
runs on every push via gate b — verified red against both historical wordings and a third invented
paraphrase, green on the real restored README. `q-501` itself stays 👁️: the row's other open
pieces (project count, the July gap, a full first-time-reader pass) are untouched.

**Cull.** One dead file removed, evidence-based, not by volume:
`attic/inbox-2026-08-05-from-tlvphotos-rotation-gate-reads-only-numbered-rows.md`
(`caa7f6a7`) — its own fix landed the same day 27 days ago, confirmed still live in
`scripts/check-shipped-language.py`, and grepped clean of every other citation. Everything else in
`attic/` and `docs/queue-archive/`/`docs/handovers/`/`docs/prover/` was checked and left alone —
each is either still cited by a live document, or its retention was already an owner's call this
pass had no standing to reopen (`docs/handovers/`, declined 2026-08-27 as queue row 524).

**README.md: a rewrite is in progress, uncommitted as of this note.** `git status` shows README.md
modified against `e3b745b1` (the last commit that touched it) — a working copy that reflows the
opening section's prose and cuts roughly a hundred lines net. Not this session's to finish or
judge; check `git log -1 -- README.md` and `git diff README.md` before touching that file, since it
may already be committed by the time you read this.

**The parallel-work incident, stated plainly for the next session.** Today's session ran unusually
heavy parallel worker load directly on this shared primary tree — not worktree-isolated — and it
got genuinely messy at points. The pre-commit worker-restore guard caught several stale-stage races
and blocked unsafe commits; it worked as designed and nothing was lost. But three pieces of
already-verified work got reverted to uncommitted working-tree state by a recovery commit
(`54bde341`, reverting three files a different concurrent worker's `q-398` commit had accidentally
swept in) and were never re-committed in that session's own churn: `q-163`'s `M-620` matrix row,
`q-536`'s fourteen communicator rulings, and `q-386`'s convergence test. The main seat found this
and re-committed all three cleanly afterward, with no content changes from what each row's own
worker originally wrote and verified — `287e019c`, `1280cd99`, `67bd98d1`. This is exactly the class
of incident the new "no unprotected concurrency" rule (`5aacf3aa`, above) exists to prevent going
forward: sequencing is the default now, parallelism the exception that states its own proof at
brief-time.

**What's still genuinely open on the board.** `q-803` — the strip itself (31 pack-wide "his word"
citations out of `skills/*/SKILL.md` and `references/*.md`), acceptance written, not yet swept.
`q-163`'s host leg — a real host's own test-matrix row written by the test-author method, landing
in that host's tree; candidate `~/tlvphotos`, needs a session in that project's own window. `q-48`'s
two remaining legs — pack-side, the automatic-fetch spec delta through `spec-author`, not yet
authored; host-side, wiring tlvphotos's status view to `ga_report.py`, waiting on the pack-side leg
first. The bigger `work-board`/Requirement 309 feature (worker lanes, per-agent time, on a host's
own task queue) — real, scoped, not asked for again since 08-06, deliberately not folded into
`q-166`'s now-closed daily-need scope. `plan-9` — tlvphotos's own move to new tools, deferred on
Alexander's own word until after the release, not blocked; the walk brief already sits at
`~/tlvphotos/inbox/2026-08-27-live-spec-6.0.0-catchup.md` waiting for that project's own session.
`plan-14` — a host's own status-view/plan/probe/board template, deliberately held back from a
worker lane 31.08 as real install-infrastructure work, not a mechanical narrowing; still true today,
still needs its own dedicated pass. `q-54`'s field leg — the wish already sits in
`~/tlvphotos/inbox/2026-08-31-from-livespec-q54-founding-line.md`, nothing to do here until that
session acts on it.

**Suite state, checked writing this note:** `python3 -m pytest -q tests/test_landing_next_steps.py`
— confirm green after this commit lands (it was the one red test; this note's heal citations are
what clears it). Run the full suite before trusting anything else about the tree's state; this note
does not claim one clean full run on its own.

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
