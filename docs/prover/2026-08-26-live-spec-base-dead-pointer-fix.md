# Prover record — 2026-08-26 live-spec-base-dead-pointer-fix

PUSH-REVIEW

Range: 2fa1a181..e9637206
- e9637206 Skill-review record for the live-spec-base dead-pointer fix
- d07fb961 Fix a dead pointer to build-pipeline's now-empty bug entry in live-spec-base rule 14
Files read: PRODUCT_SPEC.md, ARCHITECTURE.md, guardrails/pre-push, skills/live-spec-base/SKILL.md
(lines 210-235), skills/director/references/class-hunt.md, skills/build-pipeline/SKILL.md,
skills/build-pipeline/references/*.md, tests/test_class_hunt.py
Checks run: python3 -m pytest tests/test_class_hunt.py tests/test_traceability.py -q — 196
passed, 3 skipped (both before and after the fix); guardrails/check-pin-drift.sh — OK (180 pins,
every line pin still resolving within ±2 lines after the file shrank by one line);
guardrails/check-skill-loadability.sh — OK (13 skills); guardrails/check-skill-review.sh
(LIVE_SPEC_DIFF_BASE=origin/main) — OK for live-spec-base. Full `python3 -m pytest -q` is
CI-only (local hangs, per §6 of the working handoff); the prior push (2fa1a181) already proved it
green on CI, and this one-sentence, two-file change's targeted+reach-sensitive local runs plus
both guardrail scripts are the scoped local equivalent.
Findings: Полоса B п.9 (final wide sweep for build-pipeline cutover leftovers, across
TEST_MATRIX.md, ARCHITECTURE.md, adopt/, MIGRATION.md, and other skills' rosters) found no
mechanically-gated breakage (no category-(c) finding), but did surface a live, operationally-real
dead pointer: base rule 14 (INV-124's class hunt) in `skills/live-spec-base/SKILL.md` still named
`skills/build-pipeline/SKILL.md`'s bug entry as one of the four-move law's homes, though that
prose fully moved to `skills/director/references/class-hunt.md` earlier in the cutover —
confirmed by grep that build-pipeline's SKILL.md (now 66 lines) carries zero mentions of "bug".
Unlike the sweep's other (b)-category findings (stale role-description prose in TEST_MATRIX.md,
ARCHITECTURE.md/index, MIGRATION.md, spec-author/SKILL.md, and six "pack, whole" closing rosters
— none gated by any test, all describing build-pipeline's old pipeline-entry-point role, a
broader rewrite deferred to a future, separate slice per the classification below), this one sits
in live-spec-base — the file every session of every skill loads first — so it was fixed now
rather than deferred. Fix: corrected the sentence to name only the current home and the spec
anchor. Independent adversarial review ran twice on this single-sentence change: round 1
**BLOCK** — its own repo-wide grep (the same discipline rule 14 itself demands: sweep every
sibling in the same change) caught that `tests/test_class_hunt.py`'s module docstring still
listed "build-pipeline's bug entry" as a live parallel home, even though that test's own body had
already been redirected to director in an earlier commit (`dadb67db`) — the docstring was simply
never updated to match; also flagged a stylistically foreign parenthetical historical gloss
("moved there from build-pipeline in the build-pipeline cutover") as out of register with
live-spec-base's evergreen, migration-history-free prose. Both fixed in the same commit: the
docstring now correctly says "former" bug entry, and the SKILL.md sentence dropped the
parenthetical entirely, matching the file's existing flat-list style. Round 2 (same reviewer,
re-verifying its own prior findings independently rather than on trust): **ALLOW** — re-ran the
same grep (one hit remaining: the now-correctly-historicized docstring line itself, expected and
safe), re-ran the same test target, re-confirmed pin-drift green.

Deferred, non-blocking (b)-category debt from the same п.9 sweep, tracked in the working handoff
for a future, separate slice: stale build-pipeline-owns-the-pipeline prose in `TEST_MATRIX.md`
(Parts map), `ARCHITECTURE.md`/`ARCHITECTURE.index.md` (node ownership of T-1..T-6/M-1/dozens of
INV-* anchors), `MIGRATION.md` (docs-only-door claim), `skills/spec-author/SKILL.md` (step
ownership), and six "pack, whole" closing rosters across `communicator`/`feedback-intake`/
`architect`/`test-author`/`design-reviewer`/`live-spec-base` (all repeat "**build-pipeline** ships
the change"). None is caught by any current gate (anchor-parity tests check set completeness, not
prose accuracy) and none blocks anything live — a larger, design-level rewrite of build-pipeline's
described architectural role, out of scope for this single-sentence dead-pointer fix.
Blocking: none
