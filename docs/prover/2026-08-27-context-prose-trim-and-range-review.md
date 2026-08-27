# Prover record — 2026-08-27 context-prose-trim-and-range-review

PUSH-REVIEW

Range: cf4366d2..01251b9d (14 commits)
- 01251b9d A task carries its links, its done, and its parallel cut
- 1eced2b6 The seven top tasks say what, why now, and when they are done
- 6bfa99b6 The probe leads with what matters now, across every category
- 7be31e21 Both readers follow PLAN.md's task-list merge, not the old Steps shape
- 293929f1 Seven tasks matter now; the other 153 stop asking for attention
- d4a2aa09 A fact is stated, never announced
- bc6f862b One list: ROADMAP's 142 rows join PLAN.md's tasks, on his word of 27.08
- 9fe0b8cc Rotation gate: an escaped pipe in a row's own text broke field counting
- 0a00fb18 communicator: point rule 9's mark legend at its one canonical home
- fcd85fdb Steps 10-17: names a person can read, and two steps he added today
- 8513d501 Blockers: what this afternoon established, and what it left open
- 1e2afe54 Six new steps, on the owner's word of 27.08
- 38438eaf Purge 94 provenance-orphaned ROADMAP rows on the owner's 27.08 order
- 0041c425 spec: strip build-status narration from Context prose

Files read: `spec/work-board.md`, `spec/design-spec-review.md`, `spec/parallel-lanes.md` (full diffs
of 0041c425, `git show 0041c425`); the 14 commits' messages and `git diff --stat cf4366d2..HEAD`
(17 files: PLAN.md, ROADMAP.md, the two rotated queue-archive files, check-doc-rotation.py,
guardrails/language-rules.json, scripts/plan_checks.py, scripts/render-board.sh,
scripts/state-probe.sh, skills/communicator/SKILL.md, the three spec files above,
tests/test_board_matches_the_canon.py, tests/test_plan_is_not_executable.py,
tests/test_tasks_parser_finds_every_task.py); current ROADMAP.md and one of the two rotated
archive files (docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md) to check where
row 55 (A-6's owning row) actually landed.

Checks run:
- `python3 -m pytest tests/test_spec_parts.py tests/test_style_lint_parts.py tests/test_style_lint_tiers.py -q`
  — 35 passed, 1 skipped (the seven spec-format gates' pytest layer, and the style-lint suite named
  in 0041c425's own commit message)
- `bash guardrails/check-shipped-language.sh` — OK, 0 offences
- `python3 -m pytest tests/test_tasks_parser_finds_every_task.py tests/test_board_matches_the_canon.py tests/test_plan_is_not_executable.py -q`
  — 12 passed (the tests the PLAN.md task-list/probe/board commits added or touched)
- `python3 -m pytest tests/test_doc_rotation.py -q` — 31 passed (gate t's own suite, covering the
  rotation mechanism the ROADMAP purge and the pipe-escaping fix both used)
- `python3 -m pytest tests/test_traceability.py -q` — 182 passed, 2 failed (see Findings and
  Blocking below)

Findings: the change this record was specifically asked to review is 0041c425, which removes three
build-status sentences from Context prose (`spec/work-board.md`: "Nothing of this scenario is built
yet."; `spec/design-spec-review.md` Requirement 102: "One leg runs live today; two are promised
targets."; `spec/parallel-lanes.md` Requirement 90: the sentence counting which branch-road
machines run today versus await build). Read against the full diff: each cut sentence stated
build status only, alongside separate intent sentences that are untouched. No requirement, User
Story, acceptance criterion, invariant, or anchor changed in any of the three files, and no
requirement number moved. The spec-format and style-lint suites and the shipped-language gate all
read clean over the current tree. This is a legitimate, narrow prose cut with nothing further to
find in it.

The wider range carries one real regression, found by running the full traceability suite rather
than a scoped one: `bc6f862b` and `38438eaf` retired ROADMAP.md from a 247-row live queue to a
36-line stub (its rows superseded into PLAN.md's Tasks section, on the owner's 27.08 word "нет
роадмапа нет бэклога есть только план") without updating the two tests that still assume the old
live-ROADMAP shape. `test_roadmap_class_vocabulary` looks for a "Wish (plain words)" header row
that no longer exists in the retired file. `test_targets_owned_by_open_rows` expects anchor A-6's
owning row (55) inside ROADMAP.md's active queue; row 55 is confirmed present in
`docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md`, marked *declined* 2026-08-27
under the same purge, and no longer anywhere the test reads as "active." Neither test was touched
by the two commits that broke its assumption — this is a real gap left by the ROADMAP retirement,
not a design choice the commits made on purpose.

Blocking:
- test_traceability.py::TestQueue.test_roadmap_class_vocabulary and
  test_traceability.py::TestTargetOwnership.test_targets_owned_by_open_rows are red, caused by
  `bc6f862b`/`38438eaf`'s ROADMAP.md retirement leaving two tests asserting the old live-ROADMAP
  shape. stands: out of scope for this pass — the task this record answers for is three named
  push-gate refusals (this freshness gate, pin drift, and the communicator skill-review gate), not
  a redesign of the ROADMAP-retirement tests, and closing it correctly needs a decision on where
  A-6's traceability now lives (PLAN.md's Tasks, or dropped with the row) that this pass has no
  standing to make. It does not block `guardrails/pre-push` locally: gate b (the full suite) stands
  down on the local chain by design and runs on the server only (`.github/workflows/gates.yml`,
  per `guardrails/pre-push`'s own comment at line 54). It will red CI's `python3 -m pytest -q` step
  on an actual push until it is closed.
