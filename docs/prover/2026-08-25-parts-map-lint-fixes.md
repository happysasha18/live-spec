# Prover record — 2026-08-25 parts-map-lint-fixes

PUSH-REVIEW

Range: 982e71d8..671f5160 (1 commit: `671f5160` "spec-style-lint, check-shipped-language:
read core+parts, not core alone")

Files read: full diff of both scripts against the precedent commit `86adc187`, both fixes'
new/changed tests, `guardrails/specformat.py`'s `spec_paths()`/`read_document()`,
`adopt/install-ratchet.sh`'s vendor lists, `guardrails/check-skill-review.sh`'s scoping
logic.

`scripts/spec-style-lint.py`, `scripts/check-shipped-language.py` (both full diffs),
`guardrails/specformat.py:379-427`, `adopt/install-ratchet.sh` (VENDOR_FILES, both the
shell array and the Python-side list), `guardrails/check-skill-review.sh` (full, to confirm
its scope is `skills/` only and neither changed script trips it), `tests/test_guardrails.py`
(the two new `GateShippedLanguage` cases), `tests/test_style_lint_parts.py` (new file, full).

Checks run: independent adversarial review, not self-check — a different agent than the
one that wrote either fix, following up twice after truncated intermediate reports until a
complete verdict was produced.

- Confirmed both fixes route through `specformat.read_document()`/`spec_paths()` the same
  way the precedent (`86adc187`) does — same `sys.path.insert(0, GUARDRAILS)` /
  `import specformat as sf` pattern, correct argument shapes (`sf.read_document([src])`,
  `sf.spec_paths([core_path], root=root)`).
- Confirmed `spec-style-lint.py`'s optional-import fallback (plain `open().read()` when
  `specformat` isn't importable) is a real, intentional degradation, not an accidental gap:
  the script IS in `adopt/install-ratchet.sh`'s `VENDOR_FILES` (vendored standalone,
  `specformat.py` not vendored alongside it); `check-shipped-language.py` is NOT vendored,
  so its unconditional `import specformat` (no fallback) is correctly asymmetric.
- Traced `check-shipped-language.py`'s rel-path membership check for false positive/
  negative risk — `shipped_set()` builds `rel` from `git ls-files` (root-relative,
  forward-slash), `_split_doc_rels` builds its set via `os.path.relpath` against the same
  root — no normalization mismatch on POSIX.
- Independently recomputed every claimed number rather than trusting the workers' reports:
  PRODUCT_SPEC.md expands to 31 files (30 parts + core), ARCHITECTURE.md to 16 (15+core),
  TEST_MATRIX.md to 24 (23+core) — cross-checked against `find spec|architecture|matrix
  -name '*.md' | wc -l` (30/15/23, summing to the claimed 68 part-files) and against
  `sf.read_document()`'s own char counts (670,456 chars / 31 files for PRODUCT_SPEC.md) —
  all matched exactly.
- Live-ran both scripts against the real repo: `spec-style-lint.py --tier full` on both
  core docs, exit 0 clean; `check-shipped-language.sh` full-repo scan, exit 0,
  `{"offences":0}` — independently re-confirmed, not trusted from a prior report.
- Verified the red-first claim by genuine revert/restore (not `git stash`, given this
  project's own documented warning that `tests/test_guardrails.py` does internal stash
  operations that don't restore cleanly on an interrupted run — used `git show HEAD:path`
  content swaps instead): both fixes' new tests fail on the pre-fix code and pass on the
  restored fix, diff stat identical after restore, no stash left dangling.
- Confirmed scope: only the 4 files in this commit changed;
  `scripts/spec-redundancy-precheck.py` (the precedent, out of scope) untouched
  (`git diff origin/main -- scripts/spec-redundancy-precheck.py` empty).
- Confirmed `guardrails/check-skill-review.sh` scopes to `skills/` only by reading its own
  file-selection logic — neither changed script is under `skills/`, so INV-208 correctly
  does not apply to this push.
- `python3 -m pytest tests/test_style_lint_parts.py tests/test_guardrails.py -k
  GateShippedLanguage -q` — 4 + 24 = 28 passed, re-run independently by both the reviewer
  and the orchestrator.
- `python3 -m pytest tests/test_guardrails.py -q` (full file, all 106 tests, not just the
  filtered subset) — 106 passed, run by the orchestrator directly (took ~16 minutes; this
  file shells out to a fresh `python3` per test, per its own documented cost, not a hang).

Findings: no blocking issues raised across either fix, the shared-helper usage, the
vendoring boundary, the test coverage, or the scope. The review took three exchanges to
reach a complete verdict — the reviewing agent twice deferred mid-report waiting on its own
background test run before finally reporting synchronously; noted here for the record, not
treated as a finding against the change itself, since the eventual verdict re-derived every
number independently rather than resting on the earlier incomplete replies.

Blocking: none
