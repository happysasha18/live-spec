# Prover record — the day 2 culling cuts, rows 2.1 and 2.2, 2026-08-09

Adversarial review of the two gate removals of day 2. Reviewer: a fresh seat with clean context,
distinct from the seat that made the edits (base rule 33). Root: Alexander's order of 2026-08-08
22:17, the plan `.live-spec/culling-plan-2026-08-08.md`, and the frozen verdict list
`.live-spec/day2-verdicts-2026-08-09.md`, rows 2.1 and 2.2.

Range reviewed: commit `1b32d8f` (row 2.1, the architecture-pin drift gate) and the uncommitted
working tree on top of it (row 2.2, the handover-provenance gate). No repository file was changed
by this review except this record. No commit, no push, no restoring command was run.

Verdict: this delta is not fit to push today. Four blocking findings and six major findings
stand. One blocking finding is caused by the cut itself.

## Method

Read the frozen verdict list first, so each cut is judged against its own stated reason. Then read
`git show --stat 1b32d8f` and its full diff, and `git status` with `git diff HEAD` for the working
tree. Read two earlier records for form: `docs/prover/2026-08-06-suite-budget-row.md` and
`docs/prover/2026-08-07-night-order-adversarial.md`.

Swept the whole tree for both removed script names, for both gate letters, and for the renumbered
spec criteria. Ran the full test suite. Ran eleven guardrail checks by hand. Compared the shipped
rulebook against its installed copy.

## What was read and run

- The verdict list, and the plan's sections on the day's shape and its standing rules.
- Every file in the two diffs, apart from the regenerated progress page, which was read in part.
- `guardrails/pre-push`, `.github/workflows/gates.yml`, `guardrails/gate-red-proofs.json`,
  `guardrails/README.md`, `scripts/check-registry.json`.
- `skills/live-spec-base/SKILL.md`, rules 9, 30 and 35. `adopt/ADOPT.md`, phase 5.
- `PRODUCT_SPEC.md` Requirement 303 and Requirement 291, with both generated code tables.
- `TEST_MATRIX.md` rows M-082, M-154, M-483 to M-490, and the anchor table.
- `ARCHITECTURE.md`, the guardrails node's owns list and pins.
- `ROADMAP.md` rows 522 and 558, and `docs/queue-archive/rotated-ROADMAP-2026-08.md`.
- The full suite: `python3 -m pytest -q tests`. Result: 4 failed, 2483 passed, 1 skipped,
  1 error, 292 seconds. Log kept in this session's scratchpad.
- Guardrail checks run by hand: landing-next-steps, tree-counts, named-checks, doc-findings-bound,
  index-generated, size-ratchet, every-gate-can-fail, doc-bound, ci-mirror, skill-review,
  config-health, shipped-language.
- The published counts, reproduced with the commands the two front pages print.

## Findings

Ten findings follow. Four block the push. Six are major and should land with the delta.

### 1. Blocking — the shipped rulebook edit puts gate m red right now

`guardrails/check-config-health.sh` exits 1 today with the message "installed skill drifted from
source: live-spec-base". That gate is wired at `guardrails/pre-push:152` as gate m. Two suite tests
fail on the same cause: `tests/test_config_health.py::TestConfigHealth::
test_this_repo_installed_hooks_match_source` and
`tests/test_config_health.py::TestPermissionPathHealth::
test_real_personal_settings_stands_down_or_passes`.

The cause is row 2.2's edit to rule 35 at `skills/live-spec-base/SKILL.md:634-639`. The installed
copy still carries the old two sentences naming the removed gate. The plan's own standing rule 6
requires the installed copies to move on the same day their sources are touched.

Repair: run `scripts/sync-skills.sh` and re-run gate m. Two other projects run on those copies, so
the sync is the fix rather than a waiver.

### 2. Blocking — the suite is red, so gate b refuses the push

The run ended 4 failed, 1 error. Beyond finding 1, two more reds stand.

`tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes` fails because its nested run
reds. The nested run's own line reads "2477 passed, 11 skipped, 1 error". The error is the leak
fixture at `tests/conftest.py:136`, reporting `livespec-test-suite-log.IszOdO`.

The name comes from `guardrails/check-tests.sh:32`, which makes its log with the prefix
`livespec-test-`. That prefix is the suite's own leak prefix at `tests/conftest.py:121`. A bounded
pre-push run killed mid-flight leaves the log behind, and the fixture then reds. Three such files
sit in the temporary directory now, beside one `livespec-test-lane-` directory.

This red is not caused by either cut. It still refuses the push.

Repair: remove the stale files, and give `check-tests.sh` a log name outside the swept prefix or a
trap that removes it on any exit. The moratorium blocks a new check, and neither repair is one.

### 3. Blocking — gate s will red the moment row 2.2 is committed

`guardrails/check-skill-review.sh` today prints "the push changes no skill body", because the
rulebook edit is still uncommitted. The gate reads the committed push range, described in its own
header at lines 14 to 34. Once committed, the edit becomes a substantive skill change. The gate then
demands a committed review record for `live-spec-base`, at least as new as that change.

The newest such record is `docs/skill-review/2026-08-07-live-spec-base.md`, older than the coming
commit.

Repair: run the skill-creator review over the rule 35 edit and commit its record in the same
commit, which the gate's freshness rule allows.

### 4. Blocking — the pending journal entry belongs to other work and cites untracked files

`git diff HEAD -- JOURNAL.md` adds one entry titled "2026-08-07, 14:23–16:15 — the diagnosis and
recovery plan, landed as a proposal". It names
`docs/plans/2026-08-07-recovery-plan.md` and `docs/prover/2026-08-07-recovery-plan-adversarial.md`.
Both files are untracked, as `git status` shows. Committing the entry alone publishes two dead
pointers.

Neither row 2.1 nor row 2.2 has a journal entry of its own. `git show 1b32d8f --stat` names no
journal. Base rule 9 at `skills/live-spec-base/SKILL.md:217` requires the dated reason behind every
movement to reach `JOURNAL.md` the same session.

Repair: add the two files to the same commit, or hold the entry back. Write a dated entry for each
of the two cuts.

### 5. Major — rule 35 now contradicts rule 30 inside one shipped file

Rule 35 reads, at `skills/live-spec-base/SKILL.md:638-639`, "Both ends stay a discipline the seat
holds, since no gate reads either one today." Rule 30 reads, at line 492, that any property the
project can check mechanically is wired as a blocking gate on every push.

The handover's three provenance lines are such a property. A machine read them until tonight, and
that machine still exists under `attic/`. A stranger installs both rules together and meets the
clash on one page.

The verdict list parks rule 30 on Alexander's word and leaves it untouched today. That leaves the
clash standing in the shipped text.

Repair: state in rule 35 that the step was held by a gate the culling withdrew, or bring rule 30's
answer forward. The second choice is his.

### 6. Major — the pin cut reaches a stranger through the adoption page

`adopt/ADOPT.md:230` now reads "A landing holds every pin level by hand." Before the cut it told an
adopting project to wire `guardrails/check-pin-drift.sh` so a stale pin is reported.

The verdict list's reason for row 2.1 reads that a stranger installs skills and never reads this
repository's architecture. The adoption page addressed a different reader. It addressed a stranger
building their own architecture document, with their own pins. This pack's own rule gives that
document pins, where the name is normative and the line a cache.

The frozen criterion keeps a thing that protects a stranger using the pack. On the adoption path
this gate did that, so the verdict's stated ground does not cover it.

Repair: put the fact in front of Alexander with the measured cost, since the criterion is his. A
smaller answer is to say on the adoption page that the pack ships no pin check today.

### 7. Major — row M-082 is retired as unheld while a live test still holds two of its arms

`TEST_MATRIX.md:555` reads "retired, no owning test". `tests/test_traceability.py:198`,
`test_architecture_pins_exist`, still reds a pinned file that is missing and a pin beyond the end
of its file. Only the label-drift arm and the machine-local carve-out went with the gate.

The row now understates the coverage the tree really carries. The same reading applies to the M-154
edit, which struck the machine-local clause from the mirror row.

Repair: name the surviving test in the M-082 row and say which arm went.

### 8. Major — the file every session reads first still counts thirty-one checks

`NEXT_STEPS.md:20-22` reads "Thirty-one checks cost 486 seconds together" and "Six of the
thirty-one have a dated real catch on record". Line 34 reads "Day 2 is next". Twenty-nine gate
letters stand today, which
`grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push | sort -u | wc -l` returns.

`guardrails/check-landing-next-steps.py` passes, because neither commit reads as a landing to it.
The staleness stands anyway, in the one file a session opens first.

Repair: refresh the live-state block with the day 2 result before the push.

### 9. Major — commit `1b32d8f` carries day 1 work, so the row does not revert alone

The commit changes `docs/PROGRESS.md` by 205 lines and moves
`guardrails/progress-baseline.json` from 2026-08-07 and 4,804 findings to 2026-08-09 and 4,875
findings. That movement of 71 findings belongs to day 1, and the page itself says findings changed
by 0 since the last run.

The verdict list promises each row lands as its own commit, so any one of them reverts alone. A
revert of `1b32d8f` would also pull the progress page and its baseline back to the 2026-08-07
state.

Repair: no action on the landed commit. Keep the regenerations out of the row 2.2 commit, and say
in the evening summary what a revert of `1b32d8f` would carry with it.

### 10. Major — row 558's decline answers the mechanism and drops the defect

`docs/queue-archive/rotated-ROADMAP-2026-08.md:10` records row 558 as "declined 2026-08-09 (day 2
row 2.2: gate ab and `guardrails/check-handover-provenance.py` retired — no gate left to extend)".

The row's own text carries an observed failure: three sessions closed without writing a handover
and nothing noticed. The newest handover under `docs/handovers/` is dated 2026-07-29. The decline
answers the extension, and the observed failure leaves the queue with no row.

Rotating a declined row is legal here. The archive's header states that declined stands as a
terminal exit.

Repair: mint one queue row carrying the observed failure, or record in the decline that the failure
is accepted and unheld.

## Smaller notes

These do not block and are cheap to fold.

- `tests/test_opening_decision_sweep.py:1` still cites R303.19 to R303.23. Row M-485 now claims
  R303.20 to R303.26. The docstring was already stale before the cut, and the renumbering was the
  moment to correct it.
- `guardrails/archformat.py` lost its `--pins` mode. Requirement 291's context still names each
  node's pins among what the one reader serves. The audit road used in
  `docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md:33` is gone with it.
- Measured bytes per criterion rose from 184.6 to 184.8, visible in the `docs/PROGRESS.md` diff.
  The published target column beside it reads "falls or holds". The gate stays green, because the
  recorded bound in `guardrails/spec-ratchet.json` is 207.2.
- `ROADMAP.md:198`, row 522, still reads that gate ab reds a handover naming no transcript. The row
  is landed and its text reads as history, so this is a reader's stumble rather than a false claim.

## What was checked and found sound

Named so a later reader knows the sweep's reach.

- No live reference to either removed script stands anywhere. Every remaining mention sits in the
  attic manifest, dated journal entries, prover records, rotated queue rows, the day 1 censuses, or
  the prototype folder.
- Both removals are complete in the push hook, the continuous-integration workflow, the gate
  red-proof ledger and the gate roster. `check-every-gate-can-fail` reports 29 gates, each with a
  proof. `check-ci-mirror` passes.
- The gate roster count of 29 matches the published command's answer.
- The two published tree counts match the tree: 6,410 lines and 5,175 body lines under `skills/`.
- No anchor is orphaned. The traceability tests over nodes, owned anchors and matrix rows all pass.
  `check-index-generated` matches 398 of 398 rows. `check-matrix-reference` passes.
- The spec renumbering of Requirement 303 is consistent. Both generated code tables agree, and
  `scripts/session-extract.py` and `tests/test_session_extract.py` were repointed.
- `retired` is a legal matrix status, declared at `TEST_MATRIX.md:35` and accepted at
  `tests/test_traceability.py:100`.
- `check-named-checks` passes over 32 registry entries; neither removed script was ever registered.
- No deleted test had a subject wider than its gate. `tests/test_handover_provenance.py` tested
  that gate alone. Of the pin tests, only `test_machine_local_pins_skip_in_ci_only` reached wider,
  and its subject was that same script's behaviour under continuous integration.
- Both commit messages hold. Commit `1b32d8f` claims the gate and its whole tail, and the tail is
  complete apart from finding 7's overstatement in the matrix row.

## Verdict

Not fit to push today.

Four findings block the push.

- Finding 1: the installed rulebook copy drifted from source, and gate m reds.
- Finding 2: the suite is red on a leaked temporary log, and gate b reds.
- Finding 3: gate s reds once the rulebook edit is committed, with no fresh review record.
- Finding 4: the pending journal entry cites untracked files, and neither cut is journalled.

Six findings are major: findings 5 to 10.

One further red is closed by this record. `tests/test_guardrails.py::TestGateA_ProverRecord::
test_real_repo_passes` demanded a prover record dated today, and this file is it once committed.

Finding 1 is the only blocking finding the cut itself caused. Findings 2 and the gate a red stood
before it.

## Reach

Commits read: `1b32d8f` in full, and `e68b8c3` and `73840dc` for the day's frame. Working tree read
through `git status` and `git diff HEAD`, every file except the regenerated progress page read
whole.

Suite run once, complete, at 03:48 to 03:53 local time: 4 failed, 2483 passed, 1 skipped, 1 error
in 292.06 seconds. Twelve guardrail checks run by hand, each result quoted above where it matters.

Read for form: `docs/prover/2026-08-06-suite-budget-row.md` and
`docs/prover/2026-08-07-night-order-adversarial.md`.

Files written by this review: this record alone.
