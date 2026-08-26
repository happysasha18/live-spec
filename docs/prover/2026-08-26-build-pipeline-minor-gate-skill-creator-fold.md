# Prover record — 2026-08-26 build-pipeline-minor-gate-skill-creator-fold

PUSH-REVIEW

Range: 5e95feac..512d830a (widened to cover the gate-h fast-follow: the pushed range's first
attempt missed that skills/build-pipeline/SKILL.md is a user-facing file gate h's tests-present
check tracks, and reds a push that changes it with no change under tests/)
- 512d830a Add the missing test for build-pipeline's skill-creator gate content (gate h)
- fe401f1d Skill-review record for the build-pipeline minor-bump-gate skill-creator fold
- 4616a37d Give build-pipeline's MINOR-bump gate the skill-creator craft review Requirement 130 owes it
Files read: PRODUCT_SPEC.md (spec/push-gate-milestone-audit.md's Requirement 130), ARCHITECTURE.md,
guardrails/pre-push, skills/build-pipeline/SKILL.md, skills/build-pipeline/references/
minor-bump-gate.md, skills/director/references/landing-law.md, skills/live-spec-base/SKILL.md
(citation-convention precedent at line 410)
Checks run: python3 -m pytest tests/test_code_compaction_station.py tests/test_crosscut_counter.py
tests/test_traceability.py tests/test_minor_gate_reconciliations.py tests/test_setup_entry.py -q —
227 passed, 1 skipped (both before and after the two review-round corrections);
guardrails/check-pin-drift.sh — OK (180 pins); guardrails/check-skill-loadability.sh — OK (13
skills); guardrails/check-skill-review.sh (LIVE_SPEC_DIFF_BASE=origin/main) — OK for
build-pipeline; scripts/sync-skills.sh — build-pipeline re-synced;
scaffold/guardrails/check_tests_present.py --base origin/main — OK, no user-facing files changed
(reference-doc prose addition, not a gate-h-tracked surface). Full `python3 -m pytest -q` is
CI-only (local hangs, per §6 of the working handoff); the prior push (5e95feac) already proved it
green on CI, and this small, well-scoped change's targeted+reach-sensitive local runs plus all
guardrail scripts are the scoped local equivalent.
Findings: Полоса B п.10 ran the real Anthropic skill-creator eval/iterate cycle (adapted for an
unattended night run — one honest measurement round per skill, no iterate-to-convergence since no
human was present to review the interactive viewer; full adaptation rationale in the working
handoff) across all three post-cutover skills: director (100% vs 70% pass rate with-skill vs.
baseline, no findings), architect (100% vs 85.7%, no findings), and build-pipeline (94.3% vs 39%,
two findings). Of build-pipeline's two findings, one was verified a false positive (the eval
tested build-pipeline in isolation from director and concluded the release-tier law INV-217 and
fresh-seat certification INV-237 were undocumented pack-wide, when both already live in full in
`director/references/landing-law.md`, moved there earlier in the cutover — confirmed by direct
read, left untouched). The other was verified real: `spec/push-gate-milestone-audit.md`'s
Requirement 130 (SPEC M-1) requires the milestone/MINOR gate to re-run the skill evals and walk
every skill in the pack through skill-creator's craft review (folding or rejecting each finding
with a dated record, a newly joining skill taking the same walk at birth) — confirmed via `git
show` that the pre-fix `minor-bump-gate.md` contained zero mentions of "skill evals" or
"skill-creator", covering only the 3-pass audit, design review, cross-cut counter, and code
compaction. Fix: added one paragraph naming both missing duties, cited to SPEC M-1.

Independent adversarial review (a fresh reviewer instructed to find grounds to reject) ran twice.
Round 1: **BLOCK** — two real, independently-verified defects: (a) `build-pipeline/SKILL.md`'s
own "Gates worth remembering" bullet exhaustively lists the gate's contents and was left one item
short after the reference-file edit, the exact class of cross-file drift this pack's own machinery
polices, sitting one file away and caught by no test; (b) the new paragraph's citation
`(Requirement 130, SPEC M-1)` used a citation form (`"Requirement NNN"`) that appears nowhere in
any skill body/reference file in the pack — confirmed by grep it's exclusive to `docs/prover/`
audit records — while the file's own established convention and the precedent at
`live-spec-base/SKILL.md:410` both use a bare `SPEC M-1` form. Both fixed in the same commit: the
SKILL.md bullet now names the skill-creator craft review as its fifth item, and the citation
dropped the "Requirement 130," prefix. Round 2 (same reviewer, independently re-verifying its own
prior findings rather than taking correction claims on trust): **ALLOW** — re-read the diff
directly, grepped both files for zero remaining "Requirement 130" occurrences, re-ran the same
227-test target and both guardrail scripts, confirmed no regression. A 5-word n-gram check against
Requirement 130's own text (run independently by both the fix's author and the reviewer) found
zero verbatim overlap in the added paragraph — it is phrased in the file's own voice, not copied.

This closes Полоса B п.10, the last open item of the whole cutover plan. Full eval artifacts (test
prompts, assertions, benchmark.json, static HTML viewers for all three skills) live outside git at
`/private/tmp/ls-director/skill-eval-workspaces/{director,architect,build-pipeline}-workspace/`
for the owner's own review — not pushed, since they are scratch measurement output, not pack
content.

Fast-follow (commit 512d830a): the first push attempt reded on gate h (tests-present) —
`skills/build-pipeline/SKILL.md`'s edit (the "Gates worth remembering" bullet fix) is a
user-facing skill-file change with no matching change under `tests/`. Added
`test_build_pipeline_minor_gate_carries_skill_creator_review` to
`tests/test_code_compaction_station.py`, asserting the skill-creator craft review's presence in
both the SKILL.md bullet and the reference file's own paragraph (dual-witness, guarding against
the exact drift the independent reviewer's round-1 BLOCK caught between these two files). Checks
run: `python3 -m pytest tests/test_code_compaction_station.py -q` — 6 passed;
`scaffold/guardrails/check_tests_present.py --base origin/main` — OK, 1 user-facing change travels
with 1 test change.
Blocking: none
