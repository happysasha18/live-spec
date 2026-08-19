# Prover record — 2026-08-19 cut-matrix-stop

PUSH-REVIEW

Range: 7ecff93..cf3315b1
- cf3315b1 ROADMAP row 625: TEST_MATRIX.md's cut is investigated and blueprinted, not started
Files read: TEST_MATRIX.md, ARCHITECTURE.md, PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, spec/*.md,
guardrails/specformat.py, scripts/build-index.py, guardrails/check-index-generated.py,
scripts/build-matrix-reference.py, guardrails/check-matrix-reference.py, docs/test-matrix-format.md,
docs/spec-format.md, docs/roadmap-format.md, docs/prover/2026-08-18-spec-split-move.md,
docs/prover/README.md, tests/conftest.py, tests/test_traceability.py, guardrails/check-doc-rotation.py,
guardrails/node-file-cap.json, guardrails/progress-baseline.json, guardrails/check-prover-record.sh,
guardrails/pre-push, ROADMAP.md, docs/roadmap-format.md, git log/show on commit 2e2f167c
Checks run: python3 -m pytest tests/test_traceability.py -q — 181 passed; git merge-base
--is-ancestor 2e2f167c HEAD — confirmed the doc-bounds.json removal is already on this branch;
find . -iname "doc-bounds*" / "check-doc-bound*" outside attic — zero hits, confirming the file and
its gate no longer exist; grep for TEST_MATRIX.md across tests/ and open()-vs-read() call sites —
62 test files name it, 44 already route through tests/conftest.py's read()/read_flat(), 9 still open
it by path; bash guardrails/pre-push < /dev/null — RED, but only at gate m (config-health:
"installed hook drifted from source: pre-push"), a shared-hooks-directory drift this session made no
change toward; the other 27 gates in that run, including gate x (check-index-generated), gate t
(doc-rotation), gate w (every-gate-can-fail), all read OK
Findings: Asked to cut TEST_MATRIX.md (then ARCHITECTURE.md) using PRODUCT_SPEC.md's proven
core-plus-parts split as the pattern, this pass checked four claimed risks against the real tree
rather than trusting the notes that raised them, and did not cut either document. (1) TRUE —
scripts/build-matrix-reference.py and guardrails/check-matrix-reference.py each read exactly one
path; no multi-file plumbing exists for the matrix today, though the spec's siblings
(scripts/build-index.py, guardrails/check-index-generated.py) already carry the generic version of
it in guardrails/specformat.py (spec_paths, read_document, parts_map), reusable rather than
reinventable. (2) TRUE but overstated — of 62 test files naming TEST_MATRIX.md, 44 already read it
through tests/conftest.py's shared read()/read_flat(); only nine open it by path directly
(test_class_hunt.py, test_config_health.py, test_cross_surface_policy.py,
test_gesture_overlay_parity.py, test_founding_set_version.py, test_impact_analysis_entry.py,
test_paired_transition.py, test_prose_gate.py, test_scenario_entry_exit.py) and would need
converting. (3) FALSE as a blocker — INV-xxx anchors trailing a matrix row are plain text read
per-row wherever the row physically lives; a file split does not disturb them, confirmed by reading
guardrails/check-matrix-reference.py's per-row parser. (4) FALSE — guardrails/doc-bounds.json and
its watcher guardrails/check-doc-bound.py (gate z) do not exist in this tree; both were removed by
commit 2e2f167c "Every invented ceiling goes, and the watcher that enforced them" (2026-08-18),
already an ancestor of this branch's HEAD (confirmed by git merge-base --is-ancestor). No byte
ceiling governs TEST_MATRIX.md or ARCHITECTURE.md today, so the claimed size-headroom reason to
prefer cutting one over the other does not hold — there is no ceiling-driven urgency for either.
Beyond the four claims, this pass found its own block risk by reading the actual code: the matrix's
`## Reference` section is documented in docs/test-matrix-format.md as EMBEDDED in the body, and
specformat.read_document concatenates a named core's own full text before any of its parts. A core
that kept its embedded Reference would place it ahead of every part, so the twenty-three node blocks
now sized 634 bytes to 126 kilobytes each, once moved to matrix/*.md parts, would land AFTER the
Reference and break the parser that expects the Reference last. PRODUCT_SPEC.md hit the identical
shape and solved it by moving its Reference out to a separate committed file
(PRODUCT_SPEC.index.md), re-synthesized at read time and appended after the whole concatenation
(tests/conftest.py's _with_reference_tail). The matrix needs the same move, and making it changes
docs/test-matrix-format.md's own documented shape — a change that owes the format family's
comprehension gate (mechanical lints, then a panel of cold readers, passing only after two
consecutive reads return zero blocking findings) before it can land. That review loop is not
something one agent's single pass closes honestly alone, so this pass stopped before cutting either
document and instead recorded the full blueprint as ROADMAP row 625, open, for the session that
picks it up next. Stopping here is the deliverable this pass owed, not a deferral of it: the task
asked for the investigation to gate the cut, the investigation found a real design gap the cut would
otherwise have papered over at day's end on a file every part of the system cites by name, and the
row now carries that gap named rather than hidden.
Blocking: none — this pass changes only ROADMAP.md and its own prover record, and the pre-existing
gate-m hook drift the pre-push dry run shows is environmental (the shared hooks directory, drifted
by another session's install), not a finding against this diff; the coordinator is already handling
it through delivery order and guardrails/install.sh was not run here.
