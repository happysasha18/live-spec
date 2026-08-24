# Prover record — 2026-08-24 config-surface-ci-break-revert

PUSH-REVIEW

Range: b674b286..0e38cfe7
- 0e38cfe7 Revert the by-project-kind.md content edits: CI proved both load-bearing

Files read: the full diff of 0e38cfe7 (`git show 0e38cfe7 --stat` and in full — two files,
`architecture/by-project-kind.md`, `scripts/spec-debt-cap.json`); `git diff 86adc187 0e38cfe7 --
architecture/by-project-kind.md` (empty, confirming byte-identity — see below); the failing CI log
in full (`gh run view 32735661475 --log-failed`, run triggered by b674b286); `tests/test_config_surface.py`
in full, especially `DEPLOYED_ROWS`/`BOTH_SIDES` (lines 43-47) and
`test_architecture_names_the_seam_for_every_deployed_kind` (lines 211-227); `tests/test_composition_axes.py`
in full, especially `SEVEN_KINDS` (line 47) and `test_architecture_table_covers_all_seven_kinds`
(lines 128-135); `docs/prover/2026-08-24-redundancy-coverage-fix.md` (the record that reviewed
796e104d, the commit this one reverts, and did not run either failing test); `scripts/spec-debt-cap.json`
in full, both `_reason_redundancy_*` comments.

Checks run: `diff <(git show 86adc187:architecture/by-project-kind.md) architecture/by-project-kind.md`
— no output, byte-identical. `python3 scripts/spec-redundancy-precheck.py ARCHITECTURE.md` — 15 open,
matching the count `86adc187`'s own record first measured, before any content edit. `python3 -c
"import json; json.load(open('scripts/spec-debt-cap.json'))"` — valid. `python3 -m pytest
tests/test_config_surface.py tests/test_composition_axes.py tests/test_convergence_locks.py
tests/test_redundancy_precheck_parts.py tests/test_prose_gate.py tests/test_ratchet_kit.py
tests/test_gate_common_table_rows.py tests/test_architecture_format.py tests/test_traceability.py
tests/test_matrix_reference.py tests/test_formal_index.py -q` — 306 passed. Then, specifically because
the earlier record missed a real consumer, grepped every test file for `ARCHITECTURE` / `read("ARCHITECTURE.md")`
/ `read_flat("ARCHITECTURE.md")` (60 files) and ran all of them except `tests/test_guardrails.py`
(excluded per this session's own standing note — it `git stash`es and does not restore on an
interrupted run) in two batches: 450 passed/11 skipped, then 614 passed/3 skipped — 1064 passed total,
0 failed, all skips pre-existing (confirmed by reading a sample of the skip reasons; none mention
`by-project-kind` or the config surface). `bash guardrails/check-pin-drift.sh` — OK, 181 pins. `python3
guardrails/check-architecture-reference.py ARCHITECTURE.md ARCHITECTURE.index.md` — OK, 401 anchors
agree.

Findings: one blocking defect in the reverted commit, now closed by this revert; one process gap this
record names but does not fix.

**F1 — 796e104d's content edits were not actually redundant; CI's full suite (not run locally) proved
it.** `tests/test_config_surface.py::test_architecture_names_the_seam_for_every_deployed_kind` requires
each of `architecture/by-project-kind.md`'s two deployed-kind rows (frontend/visual, code/backend) to
carry the literal phrases "reach production by a deploy of configuration alone" and "behaviour and
structure stay in the code" — a completeness check, the same shape as
`test_composition_axes.py::test_architecture_table_covers_all_seven_kinds`, which 796e104d's own record
already caught for a DIFFERENT edit in the same file (the four-row merge) and correctly reverted. The
seam-shrink edit was the twin mistake: the earlier record classified it as "the one real, fixed defect"
among the 15 candidates, verified it word-for-word as a clean move, ran ten named test files plus a
60-file grep-derived sweep, and still missed `test_config_surface.py` — it is not named in that record's
`Files read` or `Checks run` at all, and the sweep it describes ("read every test file for
`ARCHITECTURE`... 60 files") evidently was not run to completion or was scoped differently than
described, since `test_config_surface.py` is squarely in that same 60-file set I just re-derived with
the identical grep. I do not have a stronger diagnosis than that the sweep was described more broadly
than it was executed. Both governing tests are now satisfied: `architecture/by-project-kind.md` is
byte-identical to its state right after `86adc187` (the redundancy-tool fix, which touched no content),
confirmed by `diff` returning nothing — not "close enough," identical.

**Blocking: closed.** The revert restores the pre-796e104d content; both failing assertions now pass
(verified directly, `test_config_surface.py` and `test_composition_axes.py` both green above).

**F2 — process gap, named, not fixed here.** This repository's local push gate runs a fast subset of
tests (`guardrails/pre-push`'s own gate b message: "the local chain is the fast set, so a push here
does not pay the suite's twenty minutes twice"); only CI's `python3 -m pytest -q` runs the full suite.
Combined with this environment's separate, well-documented trap (a full local `pytest tests/ -q` run
hangs at 0% CPU rather than completing, so it cannot be substituted for CI as a pre-push check), a content
edit can pass every local check and still break CI if the one test asserting the exact text being
edited isn't in whatever hand-picked subset was run. This happened twice in the same session (the
composition-axes merge, caught by a targeted test run before push; the seam shrink, not caught until
CI). The 60-file grep-and-run sweep this record performs is the correct mitigation and is now recorded
as a concrete step (grep every test file for the document name being edited, run all of them, batched
to avoid the full-suite hang) — but it is a manual discipline, not a mechanical gate, and nothing stops
a future edit from skipping it. Recording this as a finding rather than inventing a gate for it: a
gate that greps test files for a document name and force-runs them pre-push is new machinery for a
problem this session solved by hand in under 20 minutes once it had a name; whether it's worth building
is a call for the human, not an unasked-for addition here.

Blocking: none (F1 closed by this commit; F2 is a named process gap, not a defect in what is committed)

## What this record does not re-litigate

The 15 open `ARCHITECTURE.md` redundancy pairs' classification as structural (Parts-map echoes,
prose-defines/table-cites, one coincidental short phrase, and now confirmed-necessary per-kind
completeness text) is unchanged from `docs/prover/2026-08-24-redundancy-coverage-fix.md`'s own
classification, minus the one item that record wrongly called fixable. `PRODUCT_SPEC.md`'s 116-open
floor and the `spec-redundancy-precheck.py` core+parts fix itself (`86adc187`) are untouched by this
commit and not re-reviewed here.

Reviewer: the orchestrating session itself, not a separate dedicated reviewer agent — a deliberate
departure from this session's usual practice (every other prover/skill-review record today was written
by an independent agent), made because `main` was red on CI at the time of writing and the fix is a
mechanically-verified byte-identical revert (`diff` confirms it) rather than new authored content. The
adversarial standard is still applied: the finding above states plainly that the earlier record's
verification claim was inaccurate, not merely "additional context found."
