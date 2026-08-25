# Prover record — 2026-08-25 director-redesign-gaps

PUSH-REVIEW

Range: 828813b3..b693f9c9 (2 commits)
- b693f9c9 Skill-review record for the director redesign-gap additions
- 1373ef63 Close 3 narrow gaps left by director's redesign, in director's own vocabulary

Files read: full diff of both commits (3 files, 68 insertions / 4 deletions); the full current
`skills/director/SKILL.md` and `skills/director/references/verify-step-detail.md` (not just the
diff, to confirm both additions read coherently in context); `docs/director/capability-map.md`
(checked for an open-item entry to close — none found naming these 3 items, so none added).

Checks run: this slice follows Lane B's own §0.1 finding earlier this session that
`skills/director/SKILL.md` never uses the words "door"/"work-kind"/"footprint" (0 hits) — it
replaced build-pipeline's door-based classification with its own acts/dimensions model. Research
found 3 build-pipeline concepts (one-wish-one-story T-17's ask-fallback, refactor-intake's
verification breadth, docs-only's re-check recipe) only PARTIALLY covered by that redesign — the
general judgment already exists in director's own words, but each was missing one narrow,
concrete detail. The fix drafted three small additions in director's own existing vocabulary,
explicitly rejecting a literal port of build-pipeline's door-language prose (director's own text
elsewhere already rejects porting old bureaucracy verbatim, re: `delegation-protocol.md`'s
discarded tier ladders).

Two independent adversarial-review rounds, briefed to find reasons to refuse:
- Round 1 found one real, reproducible blocker: the refactor high-stakes condition's original
  draft used invented, undefined recipe terminology ("visual-sample comparison," "matrix audit of
  every row whose section moved") traced back to an unrelated TEST_MATRIX row-coverage concept
  that doesn't generalize to an arbitrary code refactor with no rows/sections — making the
  trigger impractical/untestable as written and violating the slice's own design constraint
  (director's existing vocabulary only, no new invented mechanics). Everything else passed clean:
  the "(see below)" cross-reference verified to point at a real, later section; no internal
  contradiction between the new third condition and the existing two; no conflict with the
  Execution section's description of the verifier's job; both targeted test files green.
- Fix: dropped the invented recipe, replaced with routing the refactor case into the file's own
  already-defined generic fresh-checker mechanism ("earns a fresh checker on the same footing as
  either of the other two") — no new terms introduced.
- Round 2 (re-verification of the fix only): confirmed every term in the revised sentence is
  either defined earlier in the same paragraph or is director's own established vocabulary
  ("dimensions"); confirmed no contradiction with condition 1 (mutually exclusive on the
  surface/behaviour axis); re-read the full section start to finish, coherent. Tests re-run green.
  Verdict: APPROVE.

A separate independent skill-creator-lens review (gate s) found PASS, non-blocking notes only:
both additions fit their files' existing terse style and parallel structure, frontmatter
unaffected, line budgets comfortable, one minor (non-blocking) antecedent-distance note on the
docs-only sentence's "that re-check" phrasing. Committed as `b693f9c9`,
`docs/skill-review/2026-08-25-director-redesign-gaps.md`.

Test runs (targeted, `run_in_background: true`, never bare `pytest tests/ -q`), both adversarial
rounds: `tests/test_traceability.py` — 181 passed each run. `tests/test_requirement_shape.py` —
10 passed each run. No stray pytest processes left running (checked after each round).

Findings: the delta is exactly what it claims — three narrow, well-scoped additions in director's
own vocabulary closing gaps its redesign left partially open, with one real defect (imported,
non-generalizing vocabulary) found and fixed before landing, and independent re-verification
confirming the fix. `docs/director/capability-map.md` has no matching open-item entry for these 3
narrow prose gaps, so none was added or closed there.
Blocking: none
