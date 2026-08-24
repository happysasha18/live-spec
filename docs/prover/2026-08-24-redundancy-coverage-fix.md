# Prover record — 2026-08-24 redundancy-coverage-fix

PUSH-REVIEW

Range: e7f4883c..796e104d
- 86adc187 spec-redundancy-precheck: read core+parts, not the core file alone
- 796e104d ARCHITECTURE.md: fix the one real seam-principle duplicate, honestly re-floor the rest

Files read: `docs/prover/README.md` in full (the contract this record follows); the model records
`docs/prover/2026-08-24-live-spec-base-slimdown-push.md` and
`docs/prover/2026-08-24-matrix-retired-rows-and-table-redundancy.md` in full, for shape and rigor
only; full diffs of both commits (`git show 86adc187 --stat`, `git show 86adc187`, `git show
796e104d --stat`, `git show 796e104d`, every hunk); `scripts/spec-redundancy-precheck.py` in full
post-fix; `guardrails/specformat.py`'s `spec_paths()`, `_expand()`, `read_document()` in full;
`tests/test_redundancy_precheck_parts.py` in full; `architecture/by-project-kind.md` in full
(current state) plus `git log -p 796e104d -- architecture/by-project-kind.md` (full history through
this commit, to check for merge/revert artifacts inside the single commit); `tests/test_
composition_axes.py::test_architecture_table_covers_all_seven_kinds` in full; `tests/test_
convergence_locks.py` in full (both the diff and the resulting file, `test_debt_cap_only_downward`
and `test_live_spec_sits_at_the_clean_floor`); `scripts/spec-debt-cap.json` in full; `adopt/
install-ratchet.sh` (confirmed untouched by this range, and read the `VENDOR_FILES` arrays / the
`spec-redundancy-precheck.py` invocation at line 119 to understand the fallback path it exercises);
`tests/test_ratchet_kit.py` (`VENDOR_FILES` list and the vendored-run test) to confirm it is the
pre-existing test the commit message says regressed and was fixed by the optional import;
`scripts/spec-style-lint.py` around line 525-545 (confirmed the sibling direct-open bug the commit
message says is out of scope, left unfixed, and confirmed via diff that this file is untouched by
this range).

Checks run: `python3 scripts/spec-redundancy-precheck.py spec/roles-and-agents.md` (no Parts map,
plain part file) — runs clean, 12 open pairs, exit 1, no crash, no change in kind of output. `python3
scripts/spec-redundancy-precheck.py matrix/guardrails.md` (no Parts map, matrix part file) — 459 open
pairs, exit 1 — matches the exact count already recorded as a pre-fix baseline in `docs/prover/
2026-08-24-matrix-retired-rows-and-table-redundancy.md`'s own Checks-run section (459 for the same
file, run before this fix existed), directly confirming the "unaffected — same bytes" claim for
non-Parts-map files rather than trusting it. `python3 scripts/spec-redundancy-precheck.py
PRODUCT_SPEC.md` — `{"candidates":120,"open":116,"waived":0}`, run myself, matches the new cap
exactly (not merely `<=`). `python3 scripts/spec-redundancy-precheck.py ARCHITECTURE.md` —
`{"candidates":16,"open":14,"waived":0}`, run myself, matches the new cap exactly. Read every one of
the 14 open pairs' full detailed output and hand-classified each against `_reason_redundancy_
ARCHITECTURE`'s four named categories: 2 pairs are the Parts-map Topic/responsibility column echoing
a part's own opening line (lines 57&681, 52&374); 1 pair is the seven-word pin gloss coincidentally
contained in an unrelated flow-table cell (lines 251&688, "the graph picks the lane set at
queue-take"); 10 pairs are the four "none beyond the floor (an explicit stated decision)"
composition-axes rows — 6 row-to-row (C(4,2), lines 826/827/828/829 pairwise) plus 4 prose-to-row
(line 814 against each of the four) — exactly the "six pairwise-identical... plus four... echoing the
prose sentence" split the JSON reason states; 1 pair is the INV-125/INV-126 policy-uniformity prose
introducing the name before a table cites it (lines 759&770). 2+1+10+1 = 14, matching the reason
text's walk with no leftover, no new/unexplained pair. `python3 -c "import sys; sys.path.insert(0,
'guardrails'); import specformat as sf; print(len(sf.spec_paths(['PRODUCT_SPEC.md'])))"` — 31 (core +
30), matches `ls spec/*.md | wc -l` = 30 exactly, confirming full coverage of every spec part.
Same for ARCHITECTURE.md — `spec_paths` returns 16 (core + 15), matches `ls architecture/*.md | wc
-l` = 15 exactly. `python3 -m pytest tests/test_convergence_locks.py tests/test_composition_axes.py
tests/test_redundancy_precheck_parts.py tests/test_prose_gate.py tests/test_ratchet_kit.py tests/
test_gate_common_table_rows.py tests/test_architecture_format.py tests/test_traceability.py tests/
test_matrix_reference.py tests/test_formal_index.py -q` — 285 passed, run synchronously (no
background, no full-suite run, per the standing hang warning). `bash guardrails/check-pin-drift.sh` —
`OK (pin drift): 181 pin(s) checked` (65 line pins, 110 file-level, 6 unlabelled) plus `OK (pin drift,
r5): 48 range pin(s) checked` — both clean, run myself. `python3 guardrails/check-architecture-
reference.py ARCHITECTURE.md ARCHITECTURE.index.md` — `OK — matched 23 of 23 rows scanned; committed
Reference equals the fresh build; 401 anchors agree node-to-table`, run myself. `python3 -c "import
json; json.load(open('scripts/spec-debt-cap.json'))"` — valid JSON, no error. `git diff origin/
main..HEAD -- adopt/install-ratchet.sh | wc -l` — `0`, confirmed empty myself rather than trusting
the brief. `git diff origin/main..HEAD --stat` — exactly the 5 files the two commits' own `--stat`
output names (`architecture/by-project-kind.md`, `scripts/spec-debt-cap.json`, `scripts/spec-
redundancy-precheck.py`, `tests/test_convergence_locks.py`, `tests/test_redundancy_precheck_
parts.py`), nothing extra, nothing missing. `git diff origin/main..HEAD -- scripts/spec-style-
lint.py | wc -l` — `0`, confirming the sibling direct-open bug the commit message flags as
out-of-scope was genuinely left untouched.

Findings: five, all non-blocking.

**1 — the core+parts fix is real and necessary, verified by full coverage counts, not by trusting
the commit message.** Before this range, `spec_paths(['PRODUCT_SPEC.md'])` and `spec_paths(
['ARCHITECTURE.md'])` did not exist in the precheck's own read path — `main()` opened the named file
directly. Running the fixed tool now resolves `PRODUCT_SPEC.md` to 31 files (core + all 30 `spec/
*.md` parts, matching `ls` exactly) and `ARCHITECTURE.md` to 16 (core + all 15 `architecture/*.md`
parts, matching `ls` exactly). Every requirement and every architecture node living in a part file
was invisible to this checker before 86adc187, silently, for as long as the two documents have
carried a Parts map. The fix closes a real blind spot, not a cosmetic one.

**2 — the fallback path for files without a Parts map is unaffected, checked on two real
non-core files, not asserted.** `spec/roles-and-agents.md` and `matrix/guardrails.md` — one a spec
part file, one a matrix part file, neither carrying a `## Parts map` — both ran clean under the
fixed tool with no crash. `matrix/guardrails.md`'s 459 open pairs exactly reproduces the count
already on record from a prior, independent prover session's run of the *pre-fix* tool against the
same file (`docs/prover/2026-08-24-matrix-retired-rows-and-table-redundancy.md`), which is direct
proof — not an inference from reading the code — that a file with no Parts map is scanned
byte-for-byte identically before and after this fix, exactly as `tests/test_redundancy_precheck_
parts.py::test_plain_file_matches_direct_read_byte_for_byte` also locks.

**3 — the optional-import fallback is narrowly scoped and does not swallow real errors.** The
`try/except ImportError` around `import specformat as sf` in `scripts/spec-redundancy-precheck.py`
catches exactly one failure mode (the module is absent, as it will be in a vendored host repo via
`adopt/install-ratchet.sh`'s `VENDOR_FILES`, confirmed by reading that array and its invocation of
this exact script at line 119) and falls through to the pre-fix direct-open behavior — it does not
catch or hide any error from within `specformat.read_document()` itself (a missing part file, a bad
encoding) once `sf` is successfully imported; those propagate normally. `specformat.py`'s own `_
expand()` catches `(OSError, UnicodeDecodeError)` on the *named* file only, pre-existing code
untouched by this range, and defers rather than hides the failure — a subsequent `open()` inside
`read_document()`'s own read loop raises the same error with a normal traceback if the file is truly
unreadable. `tests/test_ratchet_kit.py`'s `VENDOR_FILES`-based test and the new `tests/test_
redundancy_precheck_parts.py::TestVendoredStandaloneFallback` both exercise the no-`guardrails/`-dir
case directly and pass.

**4 — the `by-project-kind.md` cell edit loses no fact; both new in-cell pointers resolve correctly
against the paragraph they cite.** Read the full removed/added cell text for both the frontend/visual
and code/backend rows word for word. The removed text repeated the full seam definition (the
experiment-switch/copy/threshold/toggle enumeration, `SPEC INV-291`) verbatim in both rows; the added
text replaces each with `**the build/configuration seam** (SPEC INV-291, stated in full below the
table)`. Confirmed the referenced paragraph exists exactly where claimed: `architecture/by-project-
kind.md:52` opens `**The seam between the build and the configuration** (SPEC INV-291) is the
principle every deployed kind carries...` and continues through the full mechanism — the `project.
config-surface` line, the deployed/not-deployed kind list, the build-vs-configuration test, and
`guardrails/check-config-surface.py`'s three-way report — all of which the frontend row's *old* check
column described piecemeal and the paragraph below the table now states in full. Both new
check-column pointers ("the seam is declared and checked as the paragraph below the table states" /
"the seam's declaration and check are the same mechanism the row above cites") are mutually
consistent and each resolves to real prose, not a dangling reference.

**5 — the composition-axes merge-then-revert inside 796e104d landed clean, no artifact of the
intermediate state survives in the committed diff.** `git show 796e104d -- architecture/by-project-
kind.md` shows exactly one hunk, touching only the two design-principle table rows described in
finding 4 — no line near the composition-axes table (`book`/`CLI`/`skill pack`/`custom` rows) appears
in the committed diff at all, confirming the merge-then-revert canceled out to a true no-op on that
section before the commit was made, not merely "close enough." The four rows in the current file
(lines 94-97) are byte-identical in shape to what `tests/test_composition_axes.py::test_
architecture_table_covers_all_seven_kinds` requires (a distinct `|`-prefixed row per project.kind),
confirmed by that test passing in the run above.

Also checked, not written up as its own finding: the candidates-vs-open-vs-waived arithmetic
(`PRODUCT_SPEC.md`: 120 candidates, 116 open, 0 waived, 4 unaccounted; `ARCHITECTURE.md`: 16
candidates, 14 open, 0 waived, 2 unaccounted) is not a discrepancy — read `main()`'s loop and
confirmed the `parallel-structure` bucket is filtered out of both `open_pairs` and `waived` before
either list is built, so `candidates - open - waived` is exactly the count of sibling-bullet pairs
the tool itself judges "similar by design" and never reports. `tests/test_convergence_locks.py`'s
`test_live_spec_sits_at_the_clean_floor` reruns the live gate and asserts `open <= doc_floor` (not a
weaker check) for both documents — read the assertion body directly rather than assuming from the
docstring; it is a real, re-executed regression lock, not a rubber stamp on the JSON file's own
number.

Blocking: none

## What I went looking for and did not find

The adversarial question this range poses is whether the tool fix is real (does it actually see the
part files now, and does it leave non-Parts-map files alone) and whether the two numeric floor moves
(`PRODUCT_SPEC.md` 119→116, `ARCHITECTURE.md` 0→14) are the honest output of that fix rather than a
number picked to make a red gate go green. I ran both checks myself rather than trusting the commit
messages' arithmetic: the `spec_paths()` file counts match `ls` exactly for both documents, and both
declared caps (116, 14) are the exact live output of the fixed tool today, not merely satisfied by a
looser `<=`. I hand-classified all 14 `ARCHITECTURE.md` open pairs against the JSON's four named
categories and found a clean, exhaustive match — no stray fifteenth pattern the reason text is silent
about. I checked the one file the commit message names as having an identical unfixed bug
(`scripts/spec-style-lint.py`) and confirmed it is genuinely untouched, not quietly patched without
being mentioned. I checked the one vendored consumer (`adopt/install-ratchet.sh`) for a diff and found
none, and traced its `VENDOR_FILES` array and invocation site to confirm the optional-import fallback
this range depends on is exercised by a real call site, not a hypothetical one. I did not find a
silent behavior change on non-Parts-map files, a swallowed exception, a lost fact in the edited table
cells, a leftover artifact from the merge-then-revert, or an ARCHITECTURE.md open-pair category the
JSON reason does not account for. The range is clean.

Reviewer note: `tests/test_guardrails.py` was not run, per this session's standing warning that it
`git stash`es the tree without restoring on an interrupted run; neither `guardrails/pre-push` nor
`guardrails/README.md` is touched by this range. The full `pytest -q` suite was not run, per this
session's standing warning that it hangs in this environment (`guardrails/reap_owned_group.py`); the
ten targeted suites run above cover every file this range's diff touches (the precheck script, its
new test, the composition-axes table and its test, the convergence-lock test, and the neighbouring
prose/ratchet/traceability/matrix-reference/architecture-format/formal-index suites the model records
in this directory already treat as this delta's blast radius).
