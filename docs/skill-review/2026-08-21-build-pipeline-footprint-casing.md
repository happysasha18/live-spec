# SKILL-REVIEW — build-pipeline, footprint casing sync

Skill: build-pipeline
Date: 2026-08-21
Range: 0ec4822a..528aa8cb (skill's own last change: `528aa8cb`)

## Scope read

Read the full changed file, `skills/build-pipeline/references/footprint-read.md`, cold, and the
part of `skills/build-pipeline/SKILL.md` it is a verbatim copy of (the intake-line bullet at line 134,
and the reference's own line 5 disclaimer: "Every line below reads exactly as it read in the body").
`0ec4822a` lowercased `FOOTPRINT` to `footprint` in the SKILL.md body (a readability-ceiling pass) but
left the reference file's copy of that same sentence, and the test asserting the body's wording, on the
old casing — a rename that missed two of its own dependent copies. `528aa8cb` is the fix: it lowercases
the same word in both places, nothing else.

## Cold-read verdict

The two changed lines now read identically to the SKILL.md body line they are required to mirror or
assert against — checked by direct comparison, not by trusting the diff. Confirmed by running
`grep -rn "FOOTPRINT" --include='*.py' --include='*.md' .` from the repo root: the only remaining
all-caps `FOOTPRINT` hits are outside this skill's live surface — this test file's own top-of-file
docstring (not asserted by any test), `prototype/2026-07-23-matrix-format/proof.py` (a word-frequency
table, coincidental capital-letter key, unrelated to this skill), `docs/queue-archive/` and
`docs/attic/` (frozen archival copies, out of scope by convention), and this skill's own 2026-08-20
review record recounting the earlier rename. None of these is a live consumer of the SKILL.md body text
that this reference file or this test are required to track, so no third dependent copy was left
stranded. `tests/test_impact_analysis_entry.py::test_build_pipeline_reads_the_footprint` passes;
`python3 -m pytest tests/test_impact_analysis_entry.py -q` — 9 passed, 1 skipped.

The reference file's own claim — "Every line below reads exactly as it read in the body" — holds for
the one line this change touches; no wider verbatim drift between the two files was introduced or
found.

Verdict: ALLOW — a two-line casing sync that completes an earlier rename, verified word-for-word
against its source line, with no other live consumer left out of sync.
