# Prover record — 2026-08-26 build-pipeline-director-orphan-cleanup

PUSH-REVIEW

Range: fd177f52..d262c12e (4 commits) — widened to cover the CI red-fix (the first push's local
gates all passed, but CI's full suite — gate b, never run locally — found a third orphaned test
the local targeted runs never touched) and its own skill-review update, per the gate a
self-naming arm (one record names the base plus every non-exempt commit together)
- d262c12e Widen the build-pipeline/director orphan-cleanup skill-review record to cover the CI red-fix
- d9e77d61 Restore the lost "adversarial by nature" audit definition, redirect the third orphaned test
- 5ffa2fa5 Skill-review record for the build-pipeline/director orphan-reference cleanup
- ccb3d9fb Give drafter-applier-example.md a real home in director/, retire the dead verify-step-detail.md duplicate
Files read: PRODUCT_SPEC.md, ARCHITECTURE.md, guardrails/pre-push, skills/build-pipeline/SKILL.md,
skills/director/references/lanes-and-pen.md, skills/director/references/drafter-applier-example.md,
skills/director/references/verify-step-detail.md, tests/test_drafter_applier_form.py,
tests/test_traceability.py (test_adversarial_verify_option and TestDirectorRedesignGaps),
tests/conftest.py (_skill_surface/read_all/read_all_flat/read_flat)
Checks run: python3 -m pytest tests/test_drafter_applier_form.py tests/test_traceability.py
tests/test_worker_restore.py tests/test_setup_entry.py -q — 337 passed (first pass); after the
read_flat stylistic fix, python3 -m pytest tests/test_traceability.py -q — 184 passed;
guardrails/check-pin-drift.sh — OK (180 pins); guardrails/check-skill-loadability.sh — OK (13
skills); guardrails/check-skill-review.sh (LIVE_SPEC_DIFF_BASE=origin/main) — OK for both
build-pipeline and director. Full `python3 -m pytest -q` is CI-only (local hangs, per §6 of the
working handoff) — the prior push (fd177f52) already proved it green on CI, and this range's
local targeted+reach-sensitive runs plus the two guardrail scripts are the scoped local
equivalent for a two-file-move, two-test-edit change under skills/*/references/.
Findings: Полоса B п.7's classification audit of all 41 test files mentioning "build-pipeline"
(fresh general-purpose agent, not the orchestrator's own pass) found 37 needing no action and 4
carrying real technical debt, all traced to the same root cause: two files under
skills/build-pipeline/references/ (drafter-applier-example.md, verify-step-detail.md) survived
past the point where their real content moved to director/, because conftest.py's
read_all/read_all_flat glob every references/*.md file regardless of whether SKILL.md still
points at it. drafter-applier-example.md was additionally orphaned by a dead relative link in
director/references/lanes-and-pen.md (introduced during Полоса B п.1's move of lanes-and-pen.md,
never caught since nothing tests markdown link resolution in this pack). Fix: moved
drafter-applier-example.md to director/references/ (fixing the link, and its own self-referencing
pointer sentence), deleted the dead verify-step-detail.md duplicate, redirected
test_drafter_applier_form.py's HOME and test_traceability.py's test_adversarial_verify_option to
director's real (since-expanded, partly reworded) text — two of that test's four needles needed
rewording, not just a path swap, since director's rewrite changed "senior's own plan" to
"Director's own plan" and dropped the bare "REQUIRED" clause for a longer "fires when...
high-stakes AND its only review... is the author's own" sentence. Independent adversarial review
(a fresh agent instructed to find grounds to reject) returned ALLOW WITH FINDINGS: substance
verified correct (needles checked character-by-character against director's live text, link
resolution confirmed, byte-identical move confirmed modulo the one corrected sentence); two
non-blocking findings (stale paths in the auto-generated docs/PROGRESS.md, and the pre-existing,
already-tracked docs/director/capability-map.md desync from Полоса B п.6) are documentation-only,
outside this change's file set, and left for a later docs-sync pass per the working handoff. A
third, purely stylistic finding (read_all_flat behaving identically to the simpler read_flat on a
non-SKILL.md path) was folded: swapped to read_flat, re-ran test_traceability.py green (184
passed).

Fast-follow (commits d9e77d61, d262c12e): the first push's CI run (gate b, full suite) failed on
`tests/test_periodic_full_audit.py::test_audit_is_defined_adversarial_by_nature_once`, a third
test depending on the deleted build-pipeline/references/verify-step-detail.md surviving via
read_all's glob, missed by the classification audit's original 4-item list and by the local
targeted test run. Its needle, "An audit is adversarial by nature: a whole-read that sets out to
break the work, refute its claims, and find its holes," had dropped out of director's rewritten
verify-step-detail.md during Полоса B п.6's rewrite — a pre-existing, latent content loss the
dead build-pipeline duplicate had been silently masking, exposed only once that duplicate was
deleted. Restored the sentence verbatim into director/references/verify-step-detail.md's "The
audit protocol, once it has fired" section and redirected the test's read path/docstring to
director. Checks run: python3 -m pytest tests/test_periodic_full_audit.py tests/test_traceability.py
tests/test_drafter_applier_form.py tests/test_worker_restore.py tests/test_setup_entry.py -q — 342
passed; guardrails/check-pin-drift.sh — OK (180 pins); guardrails/check-skill-loadability.sh — OK
(13 skills); scripts/sync-skills.sh — director re-synced (its references/ content changed again
after the first sync); guardrails/check-skill-review.sh (LIVE_SPEC_DIFF_BASE=origin/main) — OK for
director once the skill-review record was widened. A second, independent adversarial review (a
different fresh reviewer than the first round, same instruction to find grounds to reject)
verified the restored sentence character-for-character against `git show
ccb3d9fb^:skills/build-pipeline/references/verify-step-detail.md` (the pre-deletion source),
checked line-wrap quality, re-ran the same 342-test target set, ran both guardrail scripts, and
grepped for any other "adversarial audit"/"An audit is adversarial by nature" collision (found
none — the phrase is now defined in exactly one normative place, per INV-46/C8's "once"
requirement) — verdict ALLOW, no findings.

Lesson for future orphan-file cleanups: grepping by the deleted file's own path/name is not
enough — a test can depend on its CONTENT via read_all's glob without ever naming the file, so
every distinguishing sentence/phrase inside a file about to be deleted needs its own grep across
tests/*.py before deletion, not just the file's path.
Blocking: none
