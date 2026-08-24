# Prover record — 2026-08-25 guardrails-freshness-306-retire

PUSH-REVIEW

Range: dd963fb7..eb943918 (1 commit: `eb943918` "guardrails-freshness: mark Requirement
306 item 15 retired (gate ad)")

Files read: full re-read of Requirement 306 (`spec/guardrails-freshness.md:895-947`),
`matrix/guardrails.md:114-127` (the already-retired M-498..M-504 rows this edit matches),
`tests/test_gate_common_table_rows.py` (confirmed its "gate ad" references are unrelated
fixture text, not a dependency on this file).

Checks run: confirmed `guardrails/check-tree-counts.py` and `scripts/gen-tree-counts.py`
do not exist on disk (`ls` both paths — no such file) and neither is wired in
`guardrails/pre-push` or `.github/workflows/gates.yml` (grepped both, zero hits) —
the retirement claim is a fact about the tree, not an assertion taken on faith.
`python3 scripts/spec-style-lint.py --tier full PRODUCT_SPEC.md` — clean (also a live
exercise of yesterday's Parts-map fix, since `guardrails-freshness.md` is a part-file).
`python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md` — 118 open candidates, none
touching this edit's location (nearest flagged pairs are at unrelated lines 1391/1404,
4927/4993, 4933/4999) — pre-existing backlog, not introduced by this change.
`git diff --stat` — exactly one file, one line changed.

Findings: none. This is a one-line text alignment (spec now says what the matrix already
says) with zero code or behavior change. No test asserts on the old wording.

Blocking: none
