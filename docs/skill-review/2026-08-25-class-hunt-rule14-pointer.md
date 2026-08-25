# Skill review — live-spec-base

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-25
Reviewer: skill-creator quality lens (applied by hand; disproportionate for a one-sentence
cross-reference wiring)

Verdict: no blocking findings.

## What changed

Rule 14's "the full four-move law lives in" cross-reference sentence in
`skills/live-spec-base/SKILL.md` now names `skills/director/references/class-hunt.md` as an
additional home alongside `skills/build-pipeline/SKILL.md`'s still-current bug entry. This is the
deferred fast-follow from an earlier commit today (`docs/prover/2026-08-25-class-hunt-director-home.md`)
that deliberately left this sentence untouched until the new file was itself committed and stable.

## Findings

No blocking findings.

- The two prior review rounds' formatting defect (a Markdown code span split across a line-wrap,
  rendering with a corrupted stray space) does not recur — both code spans in the new sentence
  sit entirely on one physical line each, independently verified.
- Line count unchanged (592), no ratchet impact.
- `tests/test_class_hunt.py`'s own module docstring "Homes:" line, previously stale (never
  updated when Director's home first landed), now lists all five real homes accurately.

Re-verified independently: `python3 -m pytest -q tests/test_class_hunt.py tests/test_traceability.py
tests/test_live_spec_base_body_thinned.py` — 202 passed, 3 skipped (pre-existing, unrelated).
`scripts/spec-style-lint.py --tier universal skills/live-spec-base/SKILL.md`: 0 errors, 8
pre-existing warnings, none near the edited lines. `guardrails/check-pin-drift.sh`: exits 0, no
FAIL lines.
