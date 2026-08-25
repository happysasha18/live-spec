# Prover record — 2026-08-25 build-pipeline-cutover-slice-1

PUSH-REVIEW

Range: c7708e34..bec35cb8 (3 commits)
- bec35cb8 Fix two blockers from adversarial review of the reference-file move
- 33799829 Move 4 build-pipeline reference files to skills/director/references/
- 1da1f587 Move architecture-step-detail.md into skills/architect/references/

Files read: full diff of all three commits (23 files, 166 insertions / 48 deletions);
`skills/build-pipeline/SKILL.md`, `skills/director/SKILL.md`, `skills/architect/SKILL.md`
(current state, not just the diff); the 5 moved reference files in their new homes
(`skills/director/references/{delegation-protocol,excuses-table,lanes-and-pen,
guardrails-catalog}.md`, `skills/architect/references/architecture-step-detail.md`);
`tests/test_worker_restore.py` (full, `CLAUSE_HOMES`/`CLAUSE_SENTENCES`); `scripts/
sync-skills.sh` (full, before and after the fix); `architecture/guardrails.md` and
`architecture/pipeline-and-lanes.md` (the two citation repoints); `docs/director/
capability-map.md`'s cutover slice plan section this slice implements steps 1-2 of.

Checks run: two independent adversarial review rounds by the same reviewer agent (a
different agent than either author), briefed to find reasons to refuse, not confirm —
round 1 against `1da1f587`+`33799829`, round 2 against `bec35cb8` on top.

- Round 1 found two real, reproducible blockers: (a) 8 tests across 5 files
  (`test_cross_surface_policy.py`, `test_delegation_line.py`,
  `test_broad_kill_guardrail.py`, `test_orchestrator_read_discipline.py`,
  `test_deferred_revisit_cadence.py`, `test_lane_branch_road.py` x2,
  `test_brief_time_disjointness.py`) silently broken by the reference-file move — each
  read the moved content via `read_all`/`read_all_flat`'s `references/*.md` glob under
  `skills/build-pipeline/SKILL.md`, a surface that shrank when 4 files left it; (b)
  `scripts/sync-skills.sh` used `cp -r` (overlay-only), never pruning a file removed
  from source, so the installed mirror still held the 4 moved files and
  `guardrails/check-config-health.sh`'s gate m reds "installed skill drifted from
  source: build-pipeline" right after a sync.
- Both fixed in `bec35cb8`: the 8 tests rewired to read `skills/director/SKILL.md`'s
  surface instead (same class of fix already applied to 10 other tests in
  `test_traceability.py` in `33799829`); `sync-skills.sh` changed to
  `rm -rf "$DEST/$name"` before `cp -r` (remove-then-copy, not overlay), with a new
  regression test `tests/test_sync_skills_prune.py` (red on the pre-fix script via
  `git show 33799829:scripts/sync-skills.sh`, green after).
- Round 2 independently re-verified both fixes without trusting round 1's or the
  author's report: hand-wrote a standalone re-implementation of the `read_all`
  surface-glob logic (not importing `conftest`) and confirmed all 12 needle strings
  exist verbatim, post whitespace-collapse, in `skills/director/SKILL.md`'s surface;
  independently reproduced red-vs-green on `sync-skills.sh` by extracting the pre-fix
  script via `git show` and hand-building the same stale-file scenario; re-ran
  `scripts/sync-skills.sh` against the real `~/.claude/skills` twice (both report
  "everything fresh", installed `build-pipeline/references/` confirmed via `ls` to hold
  only the 8 files still in source); ran `guardrails/check-config-health.sh` directly
  (exit 0, no drift message, only the pre-existing declared `chat-law-hook.sh`
  override).
- Round 2 also re-swept beyond round 1's list: grepped all 111 `read_all`/
  `read_all_flat` call sites in `tests/*.py`, individually verified every remaining
  candidate, then ran the full ~44-file "mentions build-pipeline" sweep (815 passed, 13
  skipped — the documented `external_clone_or_skip` product-prover-clone fence, expected
  in this checkout — 1 failed). The 1 failure
  (`test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`) was confirmed
  NOT a regression from either commit (neither touches this test, and the state was
  already true right after `33799829`) — it is this exact record's own not-yet-written
  status, closed by this file landing.
- Orchestrator directly re-ran, independently: `tests/test_traceability.py` full file
  (181 passed), `tests/test_worker_restore.py` + `test_no_dramatization_law.py` +
  `test_architect_extraction.py` (152 passed), the 8 rewired tests plus
  `test_sync_skills_prune.py` together (all green), and the ~25-file build-pipeline
  sweep the reviewer's round-1 gap analysis called for (207 passed, 11 skipped).
- `bash scripts/sync-skills.sh` run by the orchestrator: 3 skills synced (architect,
  build-pipeline, director — the three this slice's file moves touch), then re-run
  clean ("everything fresh").
- `bash guardrails/check-config-health.sh` run by the orchestrator directly: clean, no
  drift.

Findings: two real blockers found in round 1 (see above), both fixed in `bec35cb8` and
independently re-verified in round 2 with the same rigor as round 1 — neither survives
into this pushed range. No other silent regression found across two independent broad
sweeps (round 2's 111-call-site grep + 44-file run; the orchestrator's own 25+27-file
sweep). `docs/director/capability-map.md` row 14's "Lives today in" cell for
delegation-protocol.md is now stale (names the pre-move path) — a documentation-drift
papercut noted by round 1, not functional, left for the handoff/capability-map sync
step that follows this push per the working cycle.

Blocking: none
