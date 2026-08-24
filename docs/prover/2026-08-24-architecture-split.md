# Prover record — 2026-08-24 architecture-split

PUSH-REVIEW

Range: 0cf487d7..92429812
- b344d33c ARCHITECTURE.md split, move: 23 nodes out of ARCHITECTURE.md into 15 architecture/*.md parts
- d861b0a6 Repoint every direct-path reader of ARCHITECTURE.md to its core-plus-parts join
- b117a75e Gate z (architecture-reference) reads a core plus parts, and gains a node/part router table
- 92429812 Revert the gate-z router table: multi-file support alone was the load-bearing fix
Files read: ARCHITECTURE.md, architecture/*.md (15 parts), ARCHITECTURE.index.md, guardrails/specformat.py,
guardrails/archformat.py, guardrails/crosscut_counter.py, guardrails/check-pin-drift.sh, guardrails/pre-push,
guardrails/check-prover-record.sh, scripts/build-architecture-reference.py, guardrails/check-architecture-reference.py,
tests/conftest.py, tests/test_architecture_format.py, tests/test_architecture_pins.py, tests/test_architecture_reference.py,
tests/test_traceability.py, and the ~120 other test_*.py files that read ARCHITECTURE.md by grepping the tree for the
string; docs/prover/2026-08-18-spec-split-move.md and docs/prover/2026-08-20-matrix-parts.md as process precedent.
Checks run: a byte-for-byte verification script (rebuilt independently from the ORIGINAL pre-split
ARCHITECTURE.md, never from the split script's own in-memory state) confirmed every one of the 15 parts
equals its exact source span, the whole tail region (Seams..Decisions) reconstructs byte-for-byte, and the
core's preserved prefix and Nodes-intro are unmodified substrings of the original — ALL OK, re-run after
every commit including the router-table revert. `python3 guardrails/check-architecture-reference.py
ARCHITECTURE.md ARCHITECTURE.index.md` — OK, 23 of 23 nodes, 401 anchors agree, committed Reference equals a
fresh build (also diffed byte-for-byte against the pre-split committed ARCHITECTURE.index.md: identical).
`bash guardrails/check-pin-drift.sh` — OK, 181 pins checked (65 line, 110 file-level, 6 unlabelled), identical
output to a `git stash`-restored pre-split run. `python3 guardrails/crosscut_counter.py ROADMAP.md` — 16 node
pairs flagged, identical output to the pre-split run (diffed). `python3 scripts/check-shipped-language.py` and
`python3 guardrails/check-config-surface.py` — both OK. `python3 -m pytest -q` targeted: 224 passed over the
architecture/traceability files; 722 passed + 13 skipped over ~52 other test files that read ARCHITECTURE.md
through conftest.read() with no code change of their own; 41 passed over test_guardrails_unit.py; 34 passed
over test_config_health.py (after `bash guardrails/install.sh`); and the 9 test files repointed off a raw
`open(ARCHITECTURE.md)` onto the shared reader — all previously-passing assertions still pass, now against
the whole document rather than the ~5.6 KB core. `tests/test_guardrails.py::TestGateA_ProverRecord` and
`::TestGateG_PinDrift` (the two classes this delivery's guardrails/pre-push and check-prover-record.sh edits
touch) were run individually rather than as their full slow classes in one shot, per this session's standing
caution against whole-suite runs; `test_real_repo_passes` on each class was proved directly: the pin-drift one
green in 37.65s (matching the ~56s precedent figure for real subprocess work, not a hang), the prover-record
one red exactly as expected — a freshness gate correctly reporting no docs/prover/ record yet covers the
architecture change b344d33c introduced, which this record now closes.
Findings: six items below — content-preservation and byte-accounting proofs, two real gaps found and
fixed (understated blast radius on consumers; two infra files not scoped to architecture/), one
pre-existing gap reported but not fixed (check-shipped-language.py's STRICT/DATED matching, shared with
the earlier spec/matrix splits), and one process note (the router table's implement-then-withdraw). No
blocking defect.
- The split is a pure physical move. Every node's and every trailing section's text was sliced from the
  ORIGINAL ARCHITECTURE.md using guardrails/archformat.py's own `### [node: ...]` and `## ` heading
  boundaries (never a hand-counted line range, since the design predates the actual cut), and every
  resulting architecture/*.md file was diffed byte-for-byte against that exact source span before the
  core was rewritten. The core's kept prefix (preamble through "The shape at a glance") and its kept
  "## Nodes" heading-plus-intro paragraph are unmodified substrings of the original file. No word of any
  node's responsibility, owns list, pins, or notes changed; no word of Seams, Feature coverage, Runtime
  view, Placement view, the three project.kind tables, Quality budgets, or Decisions changed.
- The byte accounting closes exactly: the original file was 101,934 bytes; the new core (5,596 bytes)
  plus its 15 parts (98,660 bytes) sum to 104,256 — a delta of +2,322 bytes, and 2,322 is exactly the
  size of the new `## Parts map` table the core gained. Nothing was summarised and nothing invented.
- The design's own starter consumer list (tests/test_architecture_pins.py, guardrails/check-pin-drift.sh,
  guardrails/crosscut_counter.py, guardrails/check-architecture-reference.py,
  scripts/build-architecture-reference.py, scripts/check-shipped-language.py, scripts/spec-style-lint.py,
  guardrails/check-config-surface.py) undercounted its own blast radius the same way the spec split's
  design did (docs/prover/2026-08-18-spec-split-move.md: "a design's count of its own blast radius is a
  guess until someone moves the thing"). Of the eight named, four were real and needed fixing
  (test_architecture_pins.py, check-pin-drift.sh — fixed centrally in archformat.py rather than in the
  shell script itself, since check-pin-drift.sh only ever named archformat.py's own CLI — crosscut_counter.py,
  check-architecture-reference.py/build-architecture-reference.py); two were false positives that never
  open ARCHITECTURE.md's content at all (spec-style-lint.py, check-config-surface.py — both only mention
  the string in prose or docstrings); and one (check-shipped-language.py) is a REAL, confirmed gap that
  this delivery does NOT fix, named below. A parallel search (an independent agent, plus this session's own
  sweep) found six more direct-path readers the starter list missed entirely: tests/test_founding_set_version.py,
  test_config_health.py, test_legibility_floor.py, test_gesture_overlay_parity.py, test_host_count_agrees.py
  (the only one with no conftest import at all), and test_hedge_arm.py; plus two tests that were passing
  vacuously rather than honestly (test_skill_count_agrees.py's local read() only became architecture-aware
  for a sentence that happens to still sit in the retained core; test_prover_adapter_contract.py's
  no-external-pin scan was reading zero of the ~181 pins that actually exist, all of them now in parts).
  All eight are fixed and green.
- Two infrastructure files needed a fix beyond the design's own list, found by tracing what
  guardrails/check-prover-record.sh and guardrails/pre-push actually do rather than by grep alone:
  check-prover-record.sh's ARCH_COMMIT scoped its `git log` to the literal path `ARCHITECTURE.md` only,
  so a commit touching only a part would never refresh the freshness bound — widened to
  `ARCHITECTURE.md architecture/`, mirroring SPEC_COMMIT's existing `PRODUCT_SPEC.md spec/` scope from
  the earlier spec split (the same file already carried the fix for the sibling document; the
  architecture arm had simply never been asked to catch up when architecture/ didn't yet exist).
  guardrails/pre-push's gate_g_can_skip case arm named `ARCHITECTURE.md` but not `architecture/*`, so a
  diff editing only a moved pin would have wrongly stood gate g down; widened the same way. Both proven:
  TestGateA_ProverRecord::test_real_repo_passes now reds correctly on a stale record (this record closes
  that), and check-pin-drift.sh's own manual run reads all 181 pins whether the diff touches the core or
  a part.
- One real, confirmed architectural inconsistency is NOT fixed here, by design (the brief: describe, do
  not invent an architectural repair). scripts/check-shipped-language.py's STRICT_PROJECT_FILES /
  DATED_PROJECT_FILES foreign-project-name check matches a scanned file's `os.path.basename(rel)` against
  a literal tuple of two names. This is not new: PRODUCT_SPEC.md's own split (2026-08-18) left
  spec/*.md out of STRICT_PROJECT_FILES, and TEST_MATRIX.md's split (2026-08-20) left matrix/*.md out of
  DATED_PROJECT_FILES — both confirmed still true on this tree today. architecture/*.md now joins that
  same standing gap: general Cyrillic/owner-name scanning still covers every part (EXCLUDE_DIRS does not
  name architecture/), but the STRICT bare-project-name check now covers only the ~5.6 KB core rather
  than the whole document, exactly mirroring the spec and matrix precedent. Fixing this for all three
  split documents at once is a genuine follow-on architectural change (a directory-aware or parts-map-aware
  match instead of a basename literal), not something this delivery invents alone for architecture only.
  scripts/spec-freeze.py (the session-local, gitignored, dormant `guardrails/check-freeze.sh`) carries
  the same single-path-open pattern for all three documents (PRODUCT_SPEC.md, ARCHITECTURE.md,
  TEST_MATRIX.md) and was never fixed for the earlier two splits either; also left alone, also named here.
- The router table originally planned as this delivery's item 5 — a second generated table
  `| Node | Part | Responsibility |` in ARCHITECTURE.index.md, plus the builder/gate code to build and
  check it — was implemented, then withdrawn on the coordinator's mid-delivery course correction
  (ceremony, not necessity). ARCHITECTURE.index.md is confirmed byte-identical to the version committed
  before this delivery began; only the Anchor table's builder/gate gained multi-file support, which is
  what the split actually requires (without it, gate z would parse the ~5.6 KB core alone and either
  false-red on zero nodes or, far worse, silently validate nothing). The Parts map table already lists
  each group's node names explicitly in its own "Nodes" column, which is what the coordinator asked the
  router table be replaced with — that column existed from the first commit and needed no further change.
Blocking: none. The one open architectural finding above (check-shipped-language.py's STRICT/DATED
project-file matching) is pre-existing across all three split documents and is reported, not fixed, per
this delivery's own brief.
