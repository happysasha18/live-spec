# Prover record — 2026-08-25 build-pipeline-cutover-adapter

PUSH-REVIEW

Range: a8488c13..c72db817 (8 commits) — widened a second time to cover the CI red-fix (the first
push's local gates all passed, but CI's full suite — gate b, never run locally — found 25 more
failing tests the local targeted runs never touched) and its own skill-review update, per the gate
a self-naming arm (one record names the base plus every non-exempt commit together)
- f5384b3a Rewrite build-pipeline into a transitional adapter (Полоса B, п.6)
- 797028d5 Skill-review record for the build-pipeline cutover adapter
- 25fa1b7c Prover record for the build-pipeline cutover adapter
- 2e0064e8 Fast-follow: loadability section + r5 pricing retirement for the adapter
- 6faad09e Widen the build-pipeline cutover skill-review record to cover the fast-follow
- 1694c56e Widen the build-pipeline cutover prover record to cover the fast-follow
- dadb67db Fix CI: redirect 25 tests off build-pipeline's now-empty surface
- c72db817 Widen the build-pipeline cutover skill-review record to cover the CI red-fix

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

The first local push attempt (against 25fa1b7c) itself caught two more real gaps neither the
orchestrator's self-review nor the independent adversarial review had run locally: gate f
(loadability) reds — the new short `build-pipeline/SKILL.md` had no "Work that belongs elsewhere"
section (row 80) — and the r5 leg of gate g (pin drift) reds on nine `.live-spec/
r5-rule-prices-2026-08-11.md` range pins pricing text from build-pipeline's old fixed nine-step
sequence, genuinely deleted (not moved) by this same cutover. Both fixed in 2e0064e8: added the
missing section (names `director` as the sole destination, matching the rest of the page);
retired the nine r5 rows exactly as this same pricing file's own 2026-08-18 precedent retired
text-audit's five rows after that extraction — removed rather than repointed, remaining 39 rows
and per-rule sections renumbered 1-39, totals recomputed by direct arithmetic on the nine removed
rows' own body-byte/pinned-test/price columns (48->39 rules, 39,921->18,471 bytes, 314->149
pinned-test hits, 40,235->18,620 price) and cross-checked against the file's own internal
consistency (price = bytes + pinned-test count, per-row, both before and after). Re-verified
independently after the fix: `bash guardrails/check-skill-loadability.sh` — OK, 13 skills load;
`bash guardrails/check-pin-drift.sh` — both legs OK (180 ARCHITECTURE.md pins, 39 r5 range pins);
the targeted suite unchanged at 348 passed. The second local push attempt (against 2e0064e8) then
caught gate a and gate s wanting fresher records for the fast-follow commit itself — this range's
own widening (6faad09e, this record) closes that loop.

The push against 6faad09e went out and CI's full suite (gate b — `python3 -m pytest -q` over
every test file, run only on CI, never locally per this session's own standing rule that it hangs
unattended) reds: 25 tests spread across ~20 files this session's local runs never covered (only
`test_traceability.py`/`test_request_classifier.py`/`test_worker_restore.py`/`test_setup_entry.py`
had run locally). Every one asserted a fact that used to live on build-pipeline's own surface as a
second witness beside PRODUCT_SPEC.md or an architecture doc — genuinely deleted, not moved, by
the cutover, the same root cause as every earlier wave in this same slice, just a wider blast
radius than the earlier waves' targeted local runs could see. Read all 25 failing tests' full
bodies (docstrings included) directly rather than trusting the CI log's truncated assertion text.
Classified each: 7 already had exact-or-near-exact homes from earlier in this same cutover slice
(`architect/SKILL.md`, `design-reviewer/SKILL.md`, `test-author/SKILL.md`,
`director/references/class-hunt.md`/`footprint-read.md`/`lanes-and-pen.md`) — repointed with
grep-verified quotes, two honest near-misses (a "the"/"that" wording mismatch, a capitalization
mismatch) resolved by using the real target text rather than forcing the historical phrase. Eight
facts had no existing second home anywhere — pulled their exact source text from the pre-cutover
file (`git show a8488c13:skills/build-pipeline/SKILL.md`) into a new consolidated reference,
`director/references/landing-law.md`, with one pointer added to `director/SKILL.md`'s Execution
section (the range's second and last touch to that file). Two more (`test_ci_verdict.py`'s pair)
needed `publish/SKILL.md`'s existing push-mechanics section extended with the fuller original
wording a shortened first draft had paraphrased away. Two were unrelated collateral, not the
content-deletion pattern: `communicator/SKILL.md` crossed its own 500-line size ideal by 6 lines
(this same slice's earlier defaults-telling addition) — compressed to one line, 504 -> 499; and
`architecture/pipeline-and-lanes.md` picked up a caps-shout register-lint violation from an
earlier edit in this slice quoting "WHICH"/"FORM" verbatim out of `work-kind-table.md` — reworded
to lowercase in the pin's own description (the source file's own capitalization is untouched,
noted as a cosmetic, non-blocking mismatch by the independent reviewer below).

A different worker, briefed to find a reason to reject rather than confirm, independently re-read
`landing-law.md` in full, re-grepped every redirected quote against its claimed new home, re-ran
the full targeted suite independently (476 passed, 9 skipped, 0 failed — matching), re-ran
`check-pin-drift.sh`/`check-skill-loadability.sh`/`check-config-health.sh` (all clean), re-read
`director/SKILL.md` end to end to confirm the second pointer paragraph didn't duplicate existing
content or disturb the document's structure, and confirmed `publish/SKILL.md`'s push-mechanics
section and the new `landing-law.md` cover genuinely different ground (remote/README/CI-verdict
mechanics vs. tripwire/merge-gate/compaction/release-tier/skill-review/verify-station/docs-layout/
removal-accounting) with no real duplication between them. No blocker found.

Findings: two real classification errors caught and corrected mid-slice (craft ladder, closed-set
door — both described above), three stale cross-references caught by independent review and fixed
in this same range (architect, test-author — fixed; live-spec-base rule 14 — recorded as deferred,
out of scope), two real local-push-gate gaps (loadability, r5 pin drift) caught by the push gate
itself and fixed in the same range, one red CI run (25 tests, full-suite-only reach) caught after
the first push and fixed in this same range, one cosmetic pin-description casing mismatch noted
and left (no test or gate reads it). No other defect found across three worker-driven fix waves,
two orchestrator self-review passes, two independent adversarial review passes, two local push
gate attempts, and one CI run.

Known, recorded, deliberately not fixed in this range (§5.6 — stop at the boundary):
`architecture/pipeline-and-lanes.md`'s `[node: build-pipeline]` responsibility statement and
owns-list still describe the old fixed pipeline; the "pack, whole" roster lines in
`test-author/SKILL.md` and `architect/SKILL.md` still name build-pipeline in its old shipping
role; `skills/live-spec-base/SKILL.md` rule 14's cross-reference. None is tested, none blocks this
push, all three need their own dedicated pass (the roster lines touch multiple skill files at
once — exactly the closing-roster trap §5.16/§5.17 already burned this session on once today).

Blocking: none
