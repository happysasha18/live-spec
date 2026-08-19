# Prover record — 2026-08-19 cut-matrix-stop

PUSH-REVIEW

Range: 38a2ae3..e8417655 (re-ranged a second time, origin/main having moved again mid-review;
the row this record covers moved from id 625 to id 750 in the first re-merge, and the range below
carries both merges and that move)
- e8417655 Merge remote-tracking branch 'origin/main' into fix/2026-08-19-cut-matrix
- e1b57af6 ROADMAP row 750: fix style-lint findings the merge's renumber left in place
- 7adcfbd9 Merge remote-tracking branch 'origin/main' into fix/2026-08-19-cut-matrix
- 37f95fcb Merge remote-tracking branch 'origin/main' into fix/2026-08-19-cut-matrix
- cf3315b1 ROADMAP row 625 (renumbered to 750 by the merge): TEST_MATRIX.md's cut is investigated
  and blueprinted, not started
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
(doc-rotation), gate w (every-gate-can-fail), all read OK. After the two re-merges and the renumber:
python3 -m pytest tests/test_row_id_uniqueness.py -q — 2 passed (no id claimed twice, live body plus
every docs/queue-archive/rotated-ROADMAP-*.md); python3 guardrails/check-matrix-reference.py
TEST_MATRIX.md — OK, 540/540 matched, Reference unchanged; python3 guardrails/check-doc-findings-
bound.py — OK, 164 live documents, none above its record; python3 -m pytest tests/test_traceability.py
tests/test_row_id_uniqueness.py tests/test_gates_manifest.py tests/test_worker_restore.py
tests/test_measurements_html_optin.py -q — 331 passed, 1 failed
(TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts), which
scans this machine's own real agent transcripts for worker-restore violations and found live ones
from other concurrent sessions on this host (unrelated repos, unrelated worktrees) — the same
already-open condition ROADMAP row 624 records, not a fault this diff introduced or can close.
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
This record is now re-ranged onto origin/main's tip after two further merges (37f95fcb, 7adcfbd9):
origin/main had, in the meantime, appended its own new row at id 625 (the gate-device manifest,
commit 3447b667's lineage) and separately caught and fixed a same-day id collision of its own
between two OTHER packages (commit 53e6523e), landing tests/test_row_id_uniqueness.py to catch the
next one mechanically. The ROADMAP.md merge conflict was a same-shape collision a third time: both
branches had appended a new row at 625. Per the coordinator's rule for this exact shape (the row
already in main keeps its number; the row that has not shipped moves), the row this record covers
renumbered 625 -> 750, with margin above the post-merge maximum (700, already claimed by the earlier
repair) and clear of 633, named as claimed by a neighbouring in-flight lane. tests/test_row_id_
uniqueness.py and guardrails/check-matrix-reference.py both read clean after the renumber (2 passed;
540/540 matched, Reference unchanged since the row carries no matrix anchor). The renumber alone
also raised guardrails/check-doc-findings-bound.py's measured ROADMAP.md count from 215 to 232
against a recorded ceiling of 215 — the row's own caps-emphasis words and one "X, not Y" appositive,
carried over unchanged from the first commit, tripped the style lint once the row's line number
changed made it visible in this pass's own re-check. Reworded the same verdicts (italics in place of
shouting capitals, a "rather than" in place of the appositive denial) with no change to content or
conclusion; measured is back to 215/207, matching the committed record.
Blocking: none
This pass changes only ROADMAP.md and its own prover record. The gate-m hook drift the pre-push
dry run shows is environmental (the shared hooks directory, drifted by another session's install),
not a finding against this diff; the coordinator is already handling it through delivery order, and
guardrails/install.sh was not run here.
