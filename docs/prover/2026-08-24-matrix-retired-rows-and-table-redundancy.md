# Prover record — 2026-08-24 matrix-retired-rows-and-table-redundancy

PUSH-REVIEW

Range: 91891a6c..025bb218
- 025bb218 Redundancy precheck stops skipping table rows outright
Files read: matrix/*.md (all 23), TEST_MATRIX.md, TEST_MATRIX.index.md, docs/test-matrix-format.md,
docs/spec-format.md, guardrails/archformat.py, guardrails/specformat.py, ARCHITECTURE.md,
architecture/guardrails.md, architecture/pipeline-and-lanes.md, architecture/outward.md,
architecture/rules-and-settings.md, architecture/runtime-and-placement.md, architecture/exchange.md,
PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, spec/guardrails-freshness.md, spec/doc-order-generated.md,
spec/live-status-reporting.md, spec/roles-and-agents.md, spec/queue-intake-priority.md,
spec/work-board.md, spec/push-gate-milestone-audit.md, attic/MANIFEST.md, docs/queue-archive/
2026-07-08-milestone-compaction.md, docs/prover/2026-08-18-retired-law-and-repeated-node.md,
docs/prover/2026-08-24-architecture-split.md, scripts/gate_common.py, scripts/spec-redundancy-precheck.py,
scripts/spec-debt-cap.json, scripts/progress-report.py, scripts/build-matrix-reference.py,
scripts/spec-done-gate.py, adopt/install-ratchet.sh, guardrails/pre-push, .github/workflows/gates.yml,
tests/test_traceability.py (matrix_covers_every_anchor and neighbours), tests/test_matrix_reference.py,
tests/test_convergence_locks.py, tests/test_prose_gate.py, tests/test_ratchet_kit.py,
tests/test_formal_index.py
Checks run: grep-audited every `*retired*` row across matrix/*.md (37 rows, 31 in matrix/guardrails.md
— matches the brief's own count) and traced each row's bracket code(s) against
PRODUCT_SPEC.index.md (the generated anchor universe test_matrix_covers_every_anchor actually reads),
architecture/*.md owns fields, and spec/*.md requirement text; confirmed by `ls`/`test -e` that every
named retired mechanism (check-far-tier.py, check-ci-mirror.sh, check-every-gate-can-fail.py,
check-judge-listed.py, rule-census.py/.json, check-doc-findings-bound.py, check-hooks-can-fire.py,
gen-tree-counts.py, check-tree-counts.py, check-registry.json, gates-manifest.json) is genuinely gone
from the live tree (attic/ or deleted outright). `python3 scripts/spec-redundancy-precheck.py` run
against TEST_MATRIX.md and each of the 23 matrix/*.md files individually, before and after the
gate_common.py fix. `python3 -m pytest -q tests/test_traceability.py tests/test_matrix_reference.py
tests/test_prose_gate.py tests/test_convergence_locks.py tests/test_ratchet_kit.py` — 250 passed, both
before and after the gate_common.py edit. `python3 scripts/progress-report.py --out <scratch>` — ran
clean against the widened spec-debt-cap.json. `python3 -c "import json; json.load(...)"` on the edited
spec-debt-cap.json — valid.
Findings: two items below — task 1 (matrix retired-row archival) investigated and NOT performed, a
genuine blocking conflict found between the brief and the document's own current contract; task 2
(redundancy precheck's table blind spot) fixed, verified safe, and landed in 025bb218. No blocking
defect in what is committed.
- **Task 1 was not performed.** The brief's premise — "у matrix-строк аналога нет" (matrix rows have
  no archival mechanism the way ROADMAP rows do) — does not hold on this tree today, and the correct
  reading (per docs/spec-format.md's back-reference and the 2026-08-18 precedent below) is the
  opposite of an oversight: it is a deliberate, currently-documented design choice.
  - `docs/test-matrix-format.md:42` and `TEST_MATRIX.md:35` both define the status vocabulary
    verbatim: "*retired* (the row is kept, never deleted)." Unlike `ROADMAP.md`'s queue rows — whose
    own law [INV-1] explicitly says a terminal-exit row *moves* to `docs/queue-archive/` — the
    matrix format's retired status carries no move clause. The two documents chose different
    policies for their own retired/closed material on purpose; matrix rows are meant to stay in
    place forever, grepable at their original row id.
  - This is not just a style preference — it is load-bearing. `tests/test_traceability.py::
    test_matrix_covers_every_anchor` requires every anchor in `PRODUCT_SPEC.index.md` (the generated,
    authoritative anchor universe) to be cited by at least one matrix row of ANY status — built,
    todo, or retired all count toward coverage. I traced each of the 37 retired rows' bracket
    code(s) against that index and against every other (non-retired) matrix row citing the same
    code. Result: for the majority of the 37 rows, the retired row is the ONLY matrix-row coverage
    that code has anywhere in the tree — INV-210, INV-212, INV-301, INV-271, INV-282, INV-305,
    INV-306 each have zero non-retired citers (spot-checked directly: `grep` for each code across
    matrix/*.md and TEST_MATRIX.md, excluding rows already flagged *retired*, returns nothing). All
    seven are still present in `PRODUCT_SPEC.index.md` with multiple criteria each (e.g. INV-305:
    `R306.1..R306.16`; INV-306: `R307.1..R307.14`) — moving the retired rows that cite them out of
    matrix/*.md would immediately red `test_matrix_covers_every_anchor`, not as an artifact of my
    edit but because those spec requirements are still formally indexed as needing matrix coverage.
  - Spot-checked the concrete claim behind that: `spec/guardrails-freshness.md` Requirement 306
    (INV-305) still states, as a live, unmarked-retired criterion, "The system *shall* run as gate ad
    on `guardrails/pre-push`" — but gate ad does not exist in `guardrails/pre-push` (confirmed by
    grep: zero matches). The spec text was never updated when the underlying gate retired; only the
    matrix row, the attic move, and the architecture `owns` annotation were. This mirrors exactly the
    kind of pre-existing, out-of-scope drift `docs/prover/2026-08-24-architecture-split.md` reported
    without fixing for `check-shipped-language.py`'s STRICT/DATED matching — a genuine inconsistency,
    reported here rather than invented a fix for, since correcting it means editing PRODUCT_SPEC.md's
    own requirement text, which this brief did not ask for and which touches the size ratchet
    (INV-264/265) and the delta classifier (INV-260..263) if done carelessly.
  - I looked for the precedent the brief pointed at — a fully, cleanly retired invariant — and found
    it: `docs/prover/2026-08-18-retired-law-and-repeated-node.md` (INV-234, the growable-doc byte
    ceiling). There, retiring the law removed its code from `PRODUCT_SPEC.index.md` entirely (zero
    occurrences today, confirmed by grep), and `tests/test_formal_index.py` carries a hand-pinned
    "expected holes" comment recording INV-234 by name and reason so the index test does not red on
    its absence. That is what a real retirement costs: a coordinated edit to PRODUCT_SPEC.md/spec's
    generated index AND a registered hole, not just a matrix-row and attic move. None of the 37 rows
    audited here have had that done — their codes are still fully indexed, which is the mechanical
    reason they cannot be safely archived out of matrix/*.md today without either (a) leaving those
    spec anchors with zero matrix coverage (breaks the traceability test) or (b) also retiring them
    from PRODUCT_SPEC.md's index the INV-234 way — a materially larger, cross-document delivery this
    brief did not scope and I did not invent unasked.
  - Row-by-row: applying the one signal that IS reliable — each retired row's own text explicitly
    claiming the underlying law still stands via a named alternate mechanism ("the law itself is
    untouched", "carried by X", "still stated in Y", "the two laws it carried stand") — 9 of the 37
    rows carry that explicit claim: M-404 (INV-223), M-403 (INV-222), M-414 (INV-233), M-346
    (INV-45), M-392 (INV-211), M-401 (INV-220), M-461 (INV-285), M-409 (INV-228), and M-484
    (INV-302, no "untouched" phrase in the row itself, but `spec/push-gate-milestone-audit.md`
    criterion 19 restates the exact same law — "A session handover *shall* name the transcript it was
    read from…" — live and unretired). These 9 are the "group B" the brief asked me to identify and
    leave alone regardless of the archival question. The other 28 rows' own text names only a
    retired mechanism with no continuation claim, and one (M-423, E-35) describes a planned field
    that was superseded before it was ever built — these would be the safe "group A" candidates BY
    TEXT, but per the traceability-test finding above, at least 26 of the 28 are mechanically blocked
    from removal today (only M-423 and possibly M-421's E-35/INV-239 pairing have coverage
    elsewhere) — too thin a remainder to justify standing up a new archive-file convention that
    would itself sit awkwardly beside the format's own "never deleted [i.e. never moved out]"
    definition. No matrix file, TEST_MATRIX.index.md, or archive file was touched.
- **Task 2 was performed and landed in 025bb218.** `scripts/gate_common.py`'s `segment_units()`
  (used only by `scripts/spec-redundancy-precheck.py`) skipped every line starting with `|` outright
  — table delimiter rows (correctly, they are punctuation) and every table DATA row's content
  (incorrectly — a matrix or spec table cell's prose was invisible to the check). Fixed by keeping
  the delimiter-row skip (a new `TABLE_DELIM_RE`, dashes/colons/pipes/whitespace only) and scanning a
  data row's cells through the same scrub-and-sentence-split path a prose line takes.
  `spec-redundancy-precheck.py` is confirmed NOT wired into `guardrails/pre-push` or either CI
  workflow (`gates.yml`, `stranger-monitor.yml`) for this repo — it is invoked only by
  `scripts/spec-done-gate.py` (an authoring-time "done" conjunction, itself not called from pre-push
  or CI here) and by `adopt/install-ratchet.sh` (ships the tool to ADOPTING host projects). Per the
  brief's own conditional this makes table-scanning safe to land without task 1 first, since nothing
  currently gates a push on its output. Ran the fixed check against TEST_MATRIX.md (0 candidates —
  it is now mostly the generated Reference table and the artifact inventory, no node-block prose) and
  each of the 23 matrix/*.md files: 1,041 open pairs total, ranging from 0 (7 files) to 459
  (matrix/guardrails.md, the largest and most heavily retired-row-laden file). Read a sample of the
  hits: they are overwhelmingly the matrix genre's own templated fixture-description boilerplate
  repeated near-verbatim across many rows ("red proven against the pre-fold text…", "the pre-delta
  tree…"), not paraphrased-requirement duplication the way `PRODUCT_SPEC.md`'s existing 119-pair
  ratchet tracks — expected for a document whose genre is one test-row-per-fact with a shared prose
  skeleton. Recorded this as a first honest baseline in `scripts/spec-debt-cap.json`'s
  `max_redundancy_open` (`TEST_MATRIX.md` and all 23 `matrix/*.md` paths, exact counts, with a
  `_reason_redundancy_TEST_MATRIX_and_matrix_parts` note explaining the number and that nothing reads
  it as a gate yet — `scripts/progress-report.py` only ever reads the `PRODUCT_SPEC.md` key). Verified
  `PRODUCT_SPEC.md` and `ARCHITECTURE.md`'s own measured redundancy is unchanged by the fix (both
  still 0 open — their few table rows produce candidates bucketed away from `open`, confirmed by
  direct run before committing), so `tests/test_convergence_locks.py::test_live_spec_sits_at_the_clean_
  floor` (which reruns the precheck live against both documents and compares against the ratchet cap)
  still passes; ran it explicitly, green.
Blocking: none

Task 1's non-performance is a reported finding, not a defect in what is committed — no matrix file was
touched, so nothing here regresses the format's existing "kept, never deleted" contract or the
traceability test that enforces it. The stale-spec drift on gate ad/ae (spec/guardrails-freshness.md
still describing retired gates as wired) is a pre-existing inconsistency, reported per the
2026-08-24-architecture-split precedent's own practice, not invented a fix for here.
