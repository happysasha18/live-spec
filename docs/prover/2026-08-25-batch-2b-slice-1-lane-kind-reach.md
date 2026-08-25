# Prover record — 2026-08-25 batch-2b-slice-1-lane-kind-reach

PUSH-REVIEW

Range: 48476d45..2453c160 (2 commits)
- c0465e00 Give three batch-2b build-pipeline facts a home in director/references
- 2453c160 Skill-review record for batch-2b slice 1 (director)

Files read: full diff (3 files, 23 insertions); `skills/director/references/{lanes-and-pen,
work-kind-table,guardrails-catalog}.md` (current state, not just the diff); the corresponding
source passages in `skills/build-pipeline/SKILL.md` (lines 151-159 for INV-131, 291-297 for
INV-12, 488-493 for INV-45); `skills/director/SKILL.md` and `skills/live-spec-base/SKILL.md`
rule 15 (to confirm the door-re-fire trigger these additions assume is still live pack-wide,
not a retired concept); `docs/director/capability-map.md`'s cutover slice plan section.

Checks run: two rounds by the same independent adversarial reviewer agent (a different agent
than the author), briefed to find reasons to reject, not confirm.

- Round 1 (against the first draft) found two real, reproducible blockers: (a)
  `lanes-and-pen.md`'s INV-131 addition was a paraphrase of the build-pipeline source, not a
  word-for-word copy — the file's own line 5 states "every line below reads exactly as it read
  in the body," a load-bearing self-description every other bullet in the file honours; (b)
  `work-kind-table.md`'s `(SPEC INV-12)` citation sat on the paragraph's generic topic sentence
  instead of the specific clause it supports in the source ("standing a step down requires a
  named kind, the ask riding the row").
- Both fixed: the INV-131 bullet now reproduces the source's exact wording and its exact inline
  bold span, verified word-for-word equal to the source after whitespace normalization (checked
  programmatically, not by eye); the INV-12 citation moved to the correct clause, matching the
  source's attachment point exactly.
- Round 2 (against the fix) re-diffed both files against source byte ranges directly, confirmed
  both fixes exact, and reconfirmed the untouched `guardrails-catalog.md` INV-45 addition was
  never in question (approved unchanged in round 1 already — faithful non-lossy paraphrase,
  citation placement matches source; this file carries no "verbatim" self-contract, so a
  paraphrase there was never a defect).

Independently: `python3 -m pytest -q tests/test_redoor_independence_rebuild.py
tests/test_traceability.py tests/test_guardrails_unit.py tests/test_lane_branch_road.py
tests/test_deferred_revisit_cadence.py tests/test_cross_surface_policy.py
tests/test_guardrails.py` — 364 passed, 4 skipped (first run, before the fix) and the same
narrower set re-run clean after the fix (275 passed, 2 skipped — `test_guardrails.py` excluded
from the re-run since it was untouched by the two-line fix and it does a `git stash`). A wide
content grep across all of `tests/*.py` for the added phrases ("re-runs the independence
edges", "The contract stands before the table", "standing a step down requires a named kind",
"Reach map", "reach_classes", "every check the diff can reach") surfaced only files already in
the targeted run above — no test outside that set reads this content by phrase.
`scripts/spec-style-lint.py --tier universal` on all three files: 0 errors.

Findings: two real blockers found in round 1 (see above), both fixed and independently
re-verified in round 2 with the same rigor. No other defect found. `build-pipeline/SKILL.md`
is untouched by this slice — its now-duplicated INV-131/INV-12/INV-45 text is left in place
until cutover step 3 removes the whole displaced body in one movement, per the mandate's ban
on a partial excision.

Batch 2b still has 8 items open (INV-70, recurring-bug-redoor, CHANGELOG-vs-journal, INV-114,
Step 7 INV-62/63, push-mechanics INV-82/106, removal-of-shipped-feature, docs-layout pass
INV-111) — this slice closes 3 of the 11 (INV-131, INV-12+safety-net, INV-45).

Blocking: none
