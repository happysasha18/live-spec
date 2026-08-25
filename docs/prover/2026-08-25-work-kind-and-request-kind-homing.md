# Prover record — 2026-08-25 work-kind-and-request-kind-homing

PUSH-REVIEW

Range: 2fde7955..32665d67 (3 commits)
- 32665d67 Skill-review record for the work-kind/request-kind homing slice
- f244fe84 Fix stale M-085 matrix row after the work-kind-table move
- 2a9bbc2a Move 4 build-pipeline reference files to skills/director/references/

Files read: full diff of both commits (10 files, 32 insertions / 19 deletions);
`skills/build-pipeline/SKILL.md`, `skills/director/SKILL.md`, `skills/live-spec-base/SKILL.md`
(current state, not just the diff); the 4 moved reference files in their new homes
(`skills/director/references/{request-kind-table,work-kind-table,footprint-read,
mockup-first-entry}.md`); `tests/test_worker_restore.py` (full, `CLAUSE_HOMES` — none of the
4 moved files are in that list); `tests/test_setup_entry.py`, `tests/test_skill_kind_review.py`,
`tests/test_traceability.py` (full, before and after both the move and the M-085 fix);
`matrix/build-pipeline.md` (M-085 row and its neighbours M-084/M-108/M-109/M-115);
`docs/director/capability-map.md`'s "no home anywhere in the tree" section this slice closes.

Checks run: two independent research passes (one Sonnet, one Fable) cross-checked the source
classification (which build-pipeline sections genuinely have no other home) before any file
moved — see `DIRECTOR_HANDOFF.md` §0.1 Lane B for the reconciled table. Then one independent
adversarial review round by a different agent, briefed to find reasons to refuse, not confirm,
re-run a second time after a fix.

- Round 1 found one real, reproducible blocker: `matrix/build-pipeline.md:43` (row M-085) still
  asserted "per-kind table's one home: build-pipeline SKILL.md" after the move had already
  repointed `skills/live-spec-base/SKILL.md:239` and `skills/build-pipeline/SKILL.md:287-288` to
  the new home — a self-contradicting repo. Everything else in round 1 passed: the 4 renames are
  pure (byte-identical), no dangling copies, no other stale literal-path reference anywhere in
  `tests/`, `skills/`, or `docs/director/capability-map.md`, `CLAUSE_HOMES` unaffected, the
  `live-spec-base` sentence reads grammatically correct in full paragraph context, and the
  `test_traceability.py` needle split was verified against the moved files' real content rather
  than taken on trust. Full targeted test run (never bare `pytest tests/ -q`):
  `test_setup_entry.py` 25 passed, `test_skill_kind_review.py` 4 passed, `test_traceability.py`
  181 passed, `test_worker_restore.py` 134 passed, plus `test_director_scenarios.py`,
  `test_footprint_note.py`, `test_finding_kind.py`, `test_touchpoint_kind.py`,
  `test_sync_skills_prune.py` (42 passed, 4 skipped) — all green.
- Fix (commit `f244fe84`): M-085's fact text updated to the new home, consistent with the other
  two files; `test_traceability.py:791`'s stale assertion-error message reworded to match (this
  half was flagged non-blocking, fixed anyway in the same pass).
- Round 2 (re-verification of the fix only): M-085 confirmed to now agree with both SKILL.md
  files; a fresh repo-wide grep for the old claim found only two remaining hits, both historical
  (`docs/research/2026-07-10-originality-audit.md`, `JOURNAL.md`), correctly left untouched;
  `test_traceability.py` re-run in full, 181 passed. Verdict: APPROVE.

`scripts/sync-skills.sh` run after commit — 3 skills updated (build-pipeline, director,
live-spec-base), all still version 5.0.0 (no per-skill version bump, per INV-178/§5.14).

Gate s (skill review) required a fresh skill-creator-lens record for the 3 changed skills before
this record was written — a further independent agent applied that lens by hand (full eval/iterate
tooling would be disproportionate for a mechanical relocation) and found PASS, non-blocking notes
only: citation clarity preserved through the repoint, director's frontmatter/body not yet citing
the 4 newly-landed files is the documented deliberate transitional state (not a fresh oversight),
no dangling or decorative citation. Committed as `32665d67`,
`docs/skill-review/2026-08-25-work-kind-and-request-kind-homing.md`.

Findings: the delta is exactly what it claims — four reference files relocated to their real
home, six pointer links repointed, one dangling live-spec-base cross-reference repointed, two
tests followed the moved content to its new surface, and one stale matrix-row claim (missed by
the implementer, caught by adversarial review) corrected. No other stale reference found on
re-check. `DIRECTOR_HANDOFF.md` §0.1 Lane B and `docs/director/capability-map.md` both updated
in this same sitting to record the four files as homed.
Blocking: none
