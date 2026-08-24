# Prover record — 2026-08-25 requirement-306-ci-fix

PUSH-REVIEW

Range: 5745d949..dd98fda3 (1 commit: `dd98fda3` "guardrails-freshness: fix Requirement 306
item 15's wording (CI fix)")

Files read: `spec/guardrails-freshness.md`'s Requirement 306 in full (both before and after
this fix), its two sibling retired-requirement precedents at lines 239 and 683 (the shape
`check-requirement-shape.py` expects), `docs/spec-style.md`'s scissors-tell definition
("naming a thing by denying its neighbour — a dash or comma appositive"), the redundancy
pair CI actually reported (`PRODUCT_SPEC.md` lines 5898/6342/6601 — the retirement clause
duplicating two other files' retirement notes once isolated into its own sentence).

Checks run: independently re-ran every gate CI's push flagged, plus the ones a wider
`test_traceability.py` sweep could plausibly catch, before pushing again — the exact rule
16 gap that caused this CI round in the first place (this file wasn't in the narrow test
list either time; running it broadly this time, not just grepping filenames).

- `python3 scripts/spec-style-lint.py --tier full PRODUCT_SPEC.md` — clean (0 errors); the
  first fix attempt tripped a `scissors` finding on a `(..., not a running gate)`
  comma-appositive — removed, not just reworded, since the style rule bans that exact shape
  regardless of phrasing.
- `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md <all 30 parts>` — OK, 1749
  criteria well-shaped across 308 requirements. The fix adds a genuine `*shall*` response
  ("The system *shall* leave gate ad ... retired"), matching line 239's precedent shape
  (a real `*shall*` clause, then a trailing retirement note) rather than a bare "Retired:"
  label with no response verb.
- `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md` — `{"open": 116}`, back at
  the recorded floor (`scripts/spec-debt-cap.json`'s `max_redundancy_open.PRODUCT_SPEC.md`
  unchanged, not raised — the fix is real, not a ratchet bump). Kept as one sentence (comma
  before "never re-armed", not a period) so the clause doesn't isolate into a fragment that
  duplicates the two other retirement notes elsewhere in the same file.
- `python3 -m pytest tests/test_convergence_locks.py tests/test_requirement_shape.py -k
  "test_live_spec_sits_at_the_clean_floor or test_armed_passes_on_the_real_spec"
  tests/test_gate_common_table_rows.py -q` — 2 passed (plus the unrelated fixture-file
  tests, unaffected as expected).
- `python3 -m pytest tests/test_traceability.py -q` — 181 passed, run precisely because
  this touches `PRODUCT_SPEC.md` (a shared/enumerated document) and this project's own
  operating rule 16 says a broad-reach edit needs more than the two narrowly-known-relevant
  test files.
- `git diff origin/main --stat` (before this commit) confirmed the change is a single line
  in a single file, no scope creep.

Findings: none blocking. Both CI failures traced to real, fixable defects in this session's
own wording, not to anything pre-existing or out of scope; neither required touching
`scripts/spec-debt-cap.json`'s ceiling.

Blocking: none
