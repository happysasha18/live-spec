### [node: test-author]

**responsibility** — the test method's one home. It derives TEST_MATRIX.md from the proven spec through the proven architecture, and it writes the tests. Its parts are the level ladder, real-artifact assertions, red-first proof, the pinned skip-set, and traceability as a standing test (row 163).

**owns** — E-27, INV-77, INV-78, INV-79, INV-80, INV-100, INV-102, INV-155, INV-157, INV-158, INV-160, INV-162, INV-204

**pins** —
- `skills/test-author/SKILL.md:1` (name + description)
- the level-ladder table and the two step sections in the same file
- `templates/headless_harness.py:1` (the canonical hardened and muted harness template; shell-first resolution and launch frame probe; the cleanup-notice emitter at each reap)
- `guardrails/cleanup_notice.py:1` (the shared cleanup-notice shape, INV-204)
- `guardrails/check-cleanup-notice.sh:1` (the notice gate, INV-204)

**notes** —
- also carries the canonical browser test harness the pack ships once as a template. A consumer adopts it by updating, and layers its own methods on (row 327, INV-157/158).
- the harness's process-group reap reports what it ended, INV-204

### [node: skill-evals]

**responsibility** — behaviour tests for the pack's own skills: per working skill one scenario, red proven bare, re-run at milestones (row 94)

**owns** — E-19

**pins** — `evals/README.md:1` (the method + honest boundary), `evals/` (one file per working skill), `tests/test_traceability.py` (`test_skill_evals_present`, self-closing over skills/)

### [node: snapshot] [target]

**responsibility** — saved baseline of the last accepted run; declared-scope diff (ROADMAP row 55)

**owns** — E-7, A-6

**pins** — — (specified; code still ahead)
