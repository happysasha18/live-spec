# Prover record — 2026-08-25 request-classifier-design-principles-ci-fix

PUSH-REVIEW

Range: 2720cb7d..62b5ec52 (1 commit)
- 62b5ec52 Fix 2 more tests broken by the work-kind-table/request-kind-table move

Files read: full diff of the commit (2 files, 17 insertions / 10 deletions);
`skills/director/SKILL.md` and everything under `skills/director/references/` (current state);
`skills/build-pipeline/SKILL.md` (current state, to confirm the asserted strings genuinely left
its body and did not survive there in duplicate form by accident); `tests/conftest.py`'s
`_skill_surface()`/`read_all()`/`read_all_flat()` (lines 213-236, the glob mechanism this whole
bug class runs through).

Checks run: `origin/main` (`2720cb7d`) went red on CI's full `pytest -q` run after the prior
push — two tests, `tests/test_design_principles.py::TestDesignPrinciplesLaw::
test_verify_feel_pass_reads_design_principles` and `tests/test_request_classifier.py::
TestRequestClassifierEntryLayer::{test_closed_set_at_the_build_pipeline_door,
test_intake_moment_back_check}`, asserted on TEXT content that had physically moved to
`skills/director/references/{work-kind-table,request-kind-table}.md` in the prior push, without
naming the moved files by path — so the prior slice's filename-only grep for
`request-kind-table|work-kind-table|footprint-read|mockup-first-entry` did not surface them. A
4th failure, `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes`, was a
derivative meta-test wrapping the suite as its own subtest and failed only because the two real
failures above did — not a separate root cause.

Diagnosed via `gh api repos/happysasha18/live-spec/actions/jobs/<id>/logs` (the formatted
`gh run view --log`/`--log-failed` output was truncated before the full FAILURES section). Fixed
by retargeting the three assertions to read `skills/director/SKILL.md`'s surface instead — the
same fix pattern already applied to `tests/test_skill_kind_review.py` and
`tests/test_traceability.py` in the earlier commit `2a9bbc2a` of this same slice.

To avoid repeating a filename-only grep's blind spot, self-check plus one independent adversarial
reviewer both did a **content-based** sweep instead: extracted distinctive substrings from all 4
moved files and searched every test file's `assertIn`/`assertEqual` literal for a match against
build-pipeline's surface specifically (not just the 4 filenames). Orchestrator's own script found
2 additional candidate hits, both confirmed false positives on inspection (`test_crosscut_counter.py`
asserts against `ARCHITECTURE.md`, `test_traceability.py:1394`'s `self.skill()` reads
`feedback-intake/SKILL.md` — neither actually reads build-pipeline's surface for the flagged
string). The independent reviewer ran the same class of check by reading all 4 moved files in
full and grepping ~25 unique phrases across `tests/*.py`, and separately confirmed: no test
remains that reads moved-file content exclusively via build-pipeline's surface without a
body-level duplicate. Verdict: APPROVE.

Test runs (targeted, `run_in_background: true`, never bare `pytest tests/ -q`):
`tests/test_design_principles.py` + `tests/test_request_classifier.py` — 28 passed, 2 skipped.
Reviewer's broader set (`test_design_principles.py`, `test_request_classifier.py`,
`test_traceability.py`, `test_skill_kind_review.py`, `test_setup_entry.py`) — 238 passed, 2
skipped (the 2 skips are the documented `external_clone_or_skip()` case, expected on a bare
checkout). A stray bare `pytest tests/ -q` the reviewer started as an unrequested "bonus" check
was found still running afterward (PID 14631, plus two waiter shells) and killed by the
orchestrator — this environment's full local suite reliably hangs, per prior sessions' own
recorded finding; it is never required locally, only on CI.

Findings: the fix is exactly what the CI failure called for — no unrelated content changed, the
retargeted assertions' literal strings verified present in director's surface by direct read (not
trusted from the diff), and a genuinely broader content-based sweep (not a repeat of the same
filename grep that missed these two tests originally) found no further gap.
Blocking: none
