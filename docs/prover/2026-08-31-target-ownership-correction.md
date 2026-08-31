# Prover record — 2026-08-31 target-ownership correction

PUSH-REVIEW

Range: 16b1a300..f24871da
- f24871da Close the target-ownership gap for real: three tags were satisfied, not orphaned
- 058aa31e Correct the target-ownership diagnosis: the anchors are real, not orphaned
- b3bd531e The resume file catches up with tonight's landings and heals three
- 8da47015 Board: q-801 and q-55 marked done; q-386 checked honestly and stays open
- 66d31da8 q-55 lands: a joining project keeps its files as they were found
- 130a67e6 q-801 lands: release 6.1.0, a new project starts on one list
- 29db22d2 q-531 lands: a split or restructure is proved to have lost nothing
- 07463f9d A joining project keeps its files as they were found
- 8613bee5 Prover record: the one-list teaching, read against the tier law and the pins
- 176b1cef The row-format page still carries the retired document's name — a Blockers line
- cee24867 The matrix row for the footprint note follows the template to its new name
- e87c6656 Release 6.1.0: the one-list teaching, and the nothing it asks of a host
- ccb0773e The separate queue template retires, and its readers follow the one list
- e1769937 A new project starts on one list, and the skills stop naming a queue file
- 6d0257ac The board reads q-531 from its own command rather than a typed mark
- 7585e7e8 A split or restructure is proved to have lost no word and no mark (q-531)

Files read: PRODUCT_SPEC.md (assembled, via `read()`/`spec_paths()`), PRODUCT_SPEC.index.md,
spec/design-spec-review.md (Requirement 102), spec/doc-order-generated.md (Requirements 1, 247),
tests/test_traceability.py (`TestTargetOwnership`, `TARGET_ROW_OWNERS`, `target_marker_anchors`,
`roadmap_rows`), guardrails/pre-push (gate h wiring), scaffold/guardrails/check_completeness.py,
scaffold/guardrails/check_traces_to_spec.py, guardrails/check-authority-anchor.py (date regex),
NEXT_STEPS.md, PLAN.md (q-531, q-801, q-55, q-386, q-54 rows and their Absorbed/Closes history),
docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md (q-93's original text and fold note),
docs/skill-review/2026-08-31-live-spec-base-merge-lands.md, adopt/record-starting-state.sh,
adopt/ADOPT.md, adopt/START.md, scripts/nothing-lost.py, tests/test_nothing_lost.py,
tests/test_starting_state.py, tests/test_footprint_note.py, tests/test_setup_entry.py,
templates/PLAN.template.md, attic/MANIFEST.md, MIGRATION.md, VERSION, .claude-plugin/plugin.json,
and every changed `skills/*/SKILL.md` and reference page in the range's diffstat.

Checks run:
- `python3 -m pytest -q` at f24871da (this HEAD), reported by the orchestrating session:
  2,656 passed, 6 skipped, 0 failed. Not re-run here (standing rule: one full-suite run at a time).
- `python3 -m pytest -q tests/test_traceability.py` — 185 passed, 2 skipped. Independently
  confirms `TARGET_ROW_OWNERS` now agrees exactly with the assembled spec's own-line `[target]`
  markers, and that every owning row (including `q-54`, `q-386`'s reach, etc.) is open in `PLAN.md`.
- `python3 -m pytest -q tests/test_nothing_lost.py tests/test_starting_state.py
  tests/test_footprint_note.py tests/test_setup_entry.py` — 51 passed.
- `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK,
  matched 404 of 404 rows; the committed index equals a fresh build off the edited body.
- `python3 guardrails/check-authority-anchor.py` — OK; independently confirmed its `DATE` regex
  (`\b(\d{4})-(\d{2})-(\d{2})\b`) is ISO-only, so the `31.08` → `2026-08-31` edit in `NEXT_STEPS.md`
  was a real, necessary fix rather than cosmetic.
- `bash guardrails/check-skill-review.sh` — OK, all six touched skills carry a fresh record.
- `bash guardrails/check-prover-record.sh` — currently FAILS on this tree (as expected: it names
  `PRODUCT_SPEC.md`'s last change as `f24871da` with no record since); this record is written to
  close exactly that gap.
- `git log --oneline --diff-filter=A -- scaffold/guardrails/check_completeness.py
  scaffold/guardrails/check_traces_to_spec.py` — both shipped whole by `f008e5b2`, well before this
  range; read both scripts directly (not taken on the commit message's word): `check_completeness.py`
  reads the surface registry and checks both directions (registered-but-absent /
  registered-but-empty against the rendered content, and — when a discovery pattern is set —
  rendered-but-unregistered the other way); `check_traces_to_spec.py` requires every registry row to
  cite at least one anchor and every cited anchor to exist in the assembled spec. Both match what
  Requirement 102's corrected Context block claims almost exactly.
- `grep -n "gate h" guardrails/pre-push` — confirmed gate h invokes exactly these two scripts (plus
  `tests_present` and `conflicts`) against `scaffold/guardrails/check_*.py`, unconditionally, on
  every push.
- `git diff 4420abb1 HEAD -- skills/live-spec-base/` and `git diff e87c6656 HEAD --
  skills/live-spec-base/`, read in full (75 and 36 lines): both contain only the version stamp and
  content already covered by the three earlier same-day skill-review records the new
  `2026-08-31-live-spec-base-merge-lands.md` record cites. The merge-timestamp claim is real.
- `git log --oneline PLAN.md` search and `grep -n "design-sync\|snapshot" PLAN.md` — see Findings.

Findings: five, one blocking.

**F1 — the target-ownership correction (E-6, E-10, INV-17, A-6) is real, not a rubber stamp.**
Independently re-derived rather than trusted: `guardrails/pre-push` gate h does run
`check_completeness.py` and `check_traces_to_spec.py` on every push, both scripts do implement a
two-directional completeness scan and a spec-anchor trace check, and both were shipped by `f008e5b2`
well before tonight. The edited acceptance criteria in `spec/design-spec-review.md` Requirement 102
and `spec/doc-order-generated.md` Requirement 1 read correctly after the edit, with no dangling
reference; `PRODUCT_SPEC.index.md`'s changes match a fresh regeneration exactly (`check-index-
generated.py` OK). `tests/test_traceability.py`'s `TARGET_ROW_OWNERS` map agrees with the spec body
exactly (test passes). No defect found here.

**F2 — the merge-timestamp skill-review record is real, not a second look dressed as a formality.**
Read both cited diffs myself in full; neither contains anything beyond the version stamp and content
three earlier same-day records already covered. No defect found here.

**F3 — the `NEXT_STEPS.md` date fix is a genuine mechanical necessity.** Confirmed
`check-authority-anchor.py`'s date regex is ISO-only; `31.08` would not have been recognized as a
date at all, which is a real (if minor) gap the fix closes, not a style preference.

**F4 (blocking) — `q-54` is not shown to be an honest home for `E-7`'s design-sync/snapshot
promise, and no better candidate exists in the live plan either.** The correction re-points `E-7`
(`spec/doc-order-generated.md` Requirement 247: the declared-scope snapshot machinery backing
design-sync) from the closed `q-55` to `q-54`, reasoning that "`q-93` (design-sync) was folded into
`q-54` on 2026-08-28" — the same reasoning the pre-existing (untouched by this range) `E-18` mapping
already rests on. Checked directly: `q-54`'s own written Acceptance in `PLAN.md` ("New projects
learn who they're building for") names only a "field leg" — a joining project's profile carrying
`project.kind`/`project.layers`/`project.proofs` — and never mentions design-sync or the snapshot
machinery anywhere in its Source, Closes, Absorbed, or Acceptance text. `git log -p -- PLAN.md`
shows the strings "design-sync" and "snapshot" have never appeared in `PLAN.md`'s history, at any
point — not before this range, not after. The archived fold note for `q-93`
(`docs/queue-archive/rotated-PLAN-2026-08-28-folded-rows.md`) shows `q-93` itself carried a `⛔`
(blocked) mark even before folding, and its one-line "Covered by `q-54`... folded by the relevance
pass" gives no textual link to what `q-54` actually promises. `grep -n "design-sync\|snapshot"
PLAN.md` today returns nothing — there is no live row, `q-54` or otherwise, whose written acceptance
claims this promise. Compounding this: tonight's own hostile review (recorded in `NEXT_STEPS.md`)
independently flags `q-54` as "real but overbuilt — narrow the row's acceptance... before dispatching
a worker on it" — meaning the row most likely to be worked next is likely to be narrowed to exactly
the field-leg text already there, closed, and mark `E-7` (and the pre-existing `E-18`) orphaned again
with nothing having caught it — reproducing, by a different mechanical path, the exact defect this
whole correction pass exists to fix. `tests/test_traceability.py::test_targets_owned_by_open_rows`
cannot catch this: it only checks that the named row exists and is not `✅`, never that the row's own
acceptance text covers the anchor's promise. This is a real gap in the plan, not a style nit, and it
is spec/policy judgment rather than a mechanical fix — I did not force one.

**F5 — nothing else in the range shows a defect.** `q-531`'s tool
(`scripts/nothing-lost.py`) is well-tested, including against two real historical splits in this
repository's own history (verified by running `tests/test_nothing_lost.py` directly). `q-55`'s
`adopt/record-starting-state.sh` is idempotent, correctly ordered after the `.gitignore` write in
`adopt/ADOPT.md`'s Phase 0 so heavy artifacts are excluded from the first commit, and tested four
ways (`tests/test_starting_state.py`, run directly, 4 passed). The eleven-plus `ROADMAP.md` →
`PLAN.md` repoints (skills, glossaries, templates, tests) are consistent throughout; no orphaned use
of the word "queue" naming the retired file was found in a spot check of the skills changed here.

Blocking:
- **F4 — `E-7`'s ownership by `q-54` is asserted, not demonstrated, and no better row exists either.**
  stands: this needs a real decision (write an explicit line into `q-54`'s Acceptance naming the
  design-sync/snapshot leg it now owes, open a fresh row for the design-sync/snapshot promise instead,
  or make a documented case that the field-leg work genuinely subsumes it), not a mechanical patch,
  and it affects the pre-existing `E-18` mapping too. Left for the orchestrating session and, per this
  pack's own rule, the owner's word before either anchor's row is touched again.
