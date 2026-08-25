# Skill review — live-spec-base

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-25
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is disproportionate for an in-place prose compression that adds
no new capability)

Verdict: no blocking findings.

## What changed

Rules 6, 14, 19, 29, and 31 in `skills/live-spec-base/SKILL.md` were compressed in place — merging
short declarative sentences into colon/dash/semicolon-joined ones, cutting pure connective
filler, and replacing one confirmed duplicate (rule 6's leave-word restatement) with a
cross-reference. No rule's meaning, INV-code citation, or named mechanism changed. One
line-number pin in `architecture/rules-and-settings.md` (rule 22) was re-pointed as a mechanical
follow-up to the resulting line shift.

## Findings

No blocking findings.

- Body: 598 → 592 lines, further under the 608-line ratchet (`tests/
  test_live_spec_base_body_thinned.py`). All 34 rule headings (1-29, 31-35) survive unchanged —
  only bodies were touched.
- Every test-pinned substring across the 5 rules was identified BEFORE drafting (not discovered
  by trial and error) and verified present after, independently, by a different reviewer than the
  implementer.
- One real defect caught and fixed before this record: a first attempt at rule 14's cross-reference
  sentence tried to wire it to `director/references/class-hunt.md`, a file from a separate,
  concurrent, still-under-review task. An independent reviewer correctly flagged this as scope
  creep coupling a pure-compression change to an unstable external file; reverted to the original
  wording. That cross-reference is deferred to its own follow-up commit, landed only after the
  other task is independently approved.
- `scripts/sync-skills.sh` re-run after the edit: installed copy matches source, no drift.

Re-verified independently: `python3 -m pytest -q tests/test_live_spec_base_body_thinned.py
tests/test_checkpoint_closes.py tests/test_leave_command.py tests/test_class_hunt.py
tests/test_deferral_marker.py tests/test_agent_channels.py tests/test_request_classifier.py
tests/test_traceability.py tests/test_minor_gate_reconciliations.py` — 346 passed, 4 skipped
(pre-existing, unrelated). `scripts/spec-style-lint.py --tier universal`: 0 errors (8 pre-existing
advisory warnings, unchanged in count from before this edit). `guardrails/check-pin-drift.sh`:
exits 0, no FAIL lines.
