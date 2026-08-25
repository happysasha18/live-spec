# Prover record — 2026-08-25 build-pipeline-cutover-adapter

PUSH-REVIEW

Range: a8488c13..797028d5 (2 commits)
- f5384b3a Rewrite build-pipeline into a transitional adapter (Полоса B, п.6)
- 797028d5 Skill-review record for the build-pipeline cutover adapter

Files read: PRODUCT_SPEC.md, ARCHITECTURE.md; full diff of f5384b3a (17 files, 233 insertions,
889 deletions); the resulting `skills/build-pipeline/SKILL.md` and `README.md` in full (not just
the diff); the new `skills/director/references/build-craft.md` in full; every touched section of
`skills/communicator/SKILL.md`, `skills/publish/SKILL.md`, `skills/test-author/SKILL.md`,
`skills/director/SKILL.md`, `skills/architect/SKILL.md`, `skills/director/references/
request-kind-table.md`; the full diff of `tests/test_traceability.py` (201 lines),
`tests/test_request_classifier.py`, `tests/test_worker_restore.py`; the three architecture pin
files (`architecture/pipeline-and-lanes.md`, `architecture/outward.md`, `architecture/
exchange.md`); `matrix/build-pipeline.md`'s M-296 row; `.live-spec/r5-rule-prices-2026-08-11.md`'s
six re-pinned communicator ranges.

Checks run: this is the largest single slice of the build-pipeline cutover to date (§0.1.1 of the
director handoff) — three successive waves of worker-driven fixes, each round surfacing test
dependencies the prior round's classification had missed (25 failing tests after the first
rewrite, not the ~0 the plan's own premise predicted; down to 6 after a second wave; 0 after a
third). The orchestrator independently re-derived the classification for every one of the ~25
facts rather than trusting any single worker's summary — reading each failing test's full body,
grepping every candidate new home for an exact or near-exact quote before accepting a redirect,
and reading the old build-pipeline text directly (via `git diff`) to confirm what a "retire, no
redirect" decision was actually dropping.

Two corrections mid-slice, both caught before commit: (1) `test_craft_ladder`'s own docstring
states "the step->craft ladder's one home is build-pipeline" — an earlier this-session
conclusion that the fact was "already fully spec'd, safe to delete" was wrong at the skill level
(true only at the PRODUCT_SPEC.md level); the craft-ladder section was restored verbatim into the
new build-pipeline/SKILL.md rather than left deleted. (2) `test_closed_set_at_the_build_pipeline_
door`'s own helper method already read from `director/references/request-kind-table.md` (a sign
of partial migration from an earlier session step); finished that migration — moved the closed-set
framing prose there too and renamed the test to `test_closed_set_at_the_door`.

Independently re-verified: `python3 -m pytest -q tests/test_traceability.py
tests/test_request_classifier.py tests/test_worker_restore.py tests/test_setup_entry.py` —
348 passed. `bash guardrails/check-pin-drift.sh` — 180/180 ARCHITECTURE.md pins OK; the only
FAIL lines are the pre-existing `.live-spec/r5-rule-prices-2026-08-11.md` "end beyond file end"
entries for build-pipeline's now-much-shorter file (wave-1 fallout, documented as needing its own
full re-derivation pass, not a mechanical line-shift, since the priced content itself no longer
exists — left untouched, same call both prior workers this session made independently).
`bash guardrails/check-config-health.sh` and `bash scripts/sync-skills.sh` clean.

An independent adversarial reviewer (a different worker, briefed to find a reason to reject, not
confirm) re-ran the full targeted suite itself (348 passed, matching), re-grepped every redirected
quote against its claimed new home, re-read the three "just retire, no redirect" cases in full to
confirm the dropped assertion's fact really is covered elsewhere in the same test function, and
ran `check-pin-drift.sh` independently with the same result. It surfaced three real, previously
unnoticed stale cross-references this cutover's deletions made false — `architect/SKILL.md`'s
claim that build-pipeline still carries its own inline copy of the architecture method (step 3 is
gone), and `test-author/SKILL.md`'s "build-pipeline keeps the order" line (director does now).
Both fixed in this same range, independently re-verified (348 passed, unchanged). The third
(`live-spec-base/SKILL.md` rule 14's cross-reference to build-pipeline's now-removed bug-entry
text) is out of scope — live-spec-base is closed for this cutover per §0.1's Полоса A status —
and is recorded as known debt in the handoff and in this range's commit message, not silently
dropped.

Findings: two real classification errors caught and corrected mid-slice (craft ladder, closed-set
door — both described above), three stale cross-references caught by independent review and fixed
in this same range (architect, test-author — fixed; live-spec-base rule 14 — recorded as deferred,
out of scope). No other defect found across three worker-driven fix waves, one orchestrator
self-review pass, and one independent adversarial review pass.

Known, recorded, deliberately not fixed in this range (§5.6 — stop at the boundary):
`architecture/pipeline-and-lanes.md`'s `[node: build-pipeline]` responsibility statement and
owns-list still describe the old fixed pipeline; the "pack, whole" roster lines in
`test-author/SKILL.md` and `architect/SKILL.md` still name build-pipeline in its old shipping
role; `skills/live-spec-base/SKILL.md` rule 14's cross-reference. None is tested, none blocks this
push, all three need their own dedicated pass (the roster lines touch multiple skill files at
once — exactly the closing-roster trap §5.16/§5.17 already burned this session on once today).

Blocking: none
