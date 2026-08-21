# Prover record — 2026-08-21 footprint-casing-sync

PUSH-REVIEW

Range: 73edd273..dff7d0b5
- dff7d0b5 Add skill-review record for the footprint casing sync
- 528aa8c Sync footprint-read reference and its test to the lowercase wording

Files read: PRODUCT_SPEC.md (INV-128 clause and Formal-index row), ARCHITECTURE.md
(boundary-health law), guardrails/pre-push, guardrails/check-prover-record.sh,
guardrails/check-skill-review.sh, guardrails/check-doc-findings-bound.py, the full diff of
528aa8c (`git show 528aa8c`), skills/build-pipeline/SKILL.md (the intake-line bullet at line 134
and the `footprint` glossary entry), skills/build-pipeline/references/footprint-read.md in full,
tests/test_impact_analysis_entry.py in full, docs/skill-review/2026-08-20-build-pipeline-worker-restore.md
(the prior record whose follow-up section names this same rename).

Checks run:
- `git show 528aa8c` — read adversarially: is the casing change complete, or does it leave a
  third dependent copy stranded? The reference file's line 5 obliges it to read word-for-word as
  the SKILL.md body; the changed bullet in both files now matches exactly.
- `grep -rn "FOOTPRINT" --include='*.py' --include='*.md' .` from the repo root — every remaining
  all-caps hit checked by hand: `tests/test_impact_analysis_entry.py`'s own top-of-file module
  docstring (prose summary, not asserted by any test — the asserted string,
  `test_build_pipeline_reads_the_footprint`, already reads lowercase in this diff);
  `prototype/2026-07-23-matrix-format/proof.py` (a word-frequency table keyed by a coincidental
  capitalised token, unconnected to this skill); `docs/queue-archive/JOURNAL-archive-2026-07-29.md`
  and `docs/attic/2026-07-22-pre-format/TEST_MATRIX.md` (frozen archival copies, out of scope by
  this project's own attic-never-delete/archive convention); this skill's own
  `docs/skill-review/2026-08-20-...md` review record, which narrates the original rename in past
  tense. None of these is a live consumer that skills/build-pipeline/SKILL.md's body or this
  reference/test pair are required to track — no third dependent copy was found missed.
- `python3 -m pytest -q tests/test_impact_analysis_entry.py tests/test_footprint_note.py
  tests/test_crosscut_counter.py` — 25 passed, 1 skipped (the skip is
  `test_prover_carries_three_source_lens`, gated by `external_clone_or_skip` on an uninstalled
  external clone, unrelated to this diff).
- `python3 guardrails/check-doc-findings-bound.py` — exit 0; 188 live documents, 28 held at zero,
  none above its recorded ceiling. `skills/build-pipeline/references/footprint-read.md` shows
  `fell: recorded 12, measured 11` (the lowercase word is one character shorter, so its long-line
  count did not change; the fall traces to something else on the r08 measure and is a fall, not a
  rise) — this is informational only: the gate's own rule is that a fallen count never blocks a
  push, only a risen one does, and this run confirms none rose.
- `bash guardrails/check-prover-record.sh --push` and `bash guardrails/check-skill-review.sh` — run
  before this record existed, to see the exact FAIL text the push gate produces (gate a: no
  2026-08-21 record; gate s: build-pipeline substantively changed with no fresh review record).
  Both are the reason this record and the paired skill-review record exist.
- A full local `python3 -m pytest -q` run was attempted twice and stalled both times partway
  through collection (once past `tests/test_founding_layers_proofs.py`/`test_gates_manifest.py`,
  once with zero output at all) at 0% CPU, isolated down to `tests/test_guardrails.py` alone also
  stalling in this sandboxed worktree. That file is untouched by this diff (`git show 528aa8c`
  touches only `skills/build-pipeline/references/footprint-read.md` and
  `tests/test_impact_analysis_entry.py`) and carries no footprint/FOOTPRINT content, so this looks
  like a pre-existing sandbox limitation (no network egress for whatever `test_guardrails.py`'s
  many subprocess/git-fixture tests need) rather than a regression from this change. Recorded here
  rather than silently omitted: the full-suite green claimed in CI's "2555 passed" baseline was not
  independently reproduced end-to-end in this sandbox; the targeted runs above are what this
  session could actually execute and verify.

`dff7d0b5` adds only the skill-review record itself
(`docs/skill-review/2026-08-21-build-pipeline-footprint-casing.md`), written by this same review
pass; it carries no change beyond that record.

Findings: none against the reviewed diff. The change is exactly the two-line casing sync its
commit message describes, both changed lines now match their required source word-for-word, and no
other live file was found still carrying the old `FOOTPRINT` casing for the same phrase.

Blocking: none.
