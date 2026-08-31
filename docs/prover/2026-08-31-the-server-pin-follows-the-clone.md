# Prover record — 2026-08-31, the server's prover pin follows the clone to 1.6.0

PUSH-REVIEW

Range: `a27e1332..HEAD`. Base commit `a27e1332`, the head origin/main carried before this push.
Commits reviewed: `0ad53184` (the pin fix), `49f8f4ea` (its merge commit).

Prover version that ran: product-prover 1.6.0 as installed on this machine, under the pack bindings
in `skills/product-prover-pack/SKILL.md` 6.0.0.

## What changed

The external `product-prover` skill was released three times today — 1.4.3, 1.5.0, 1.6.0 — on the
owner's own instruction, each time from this session. `.github/workflows/gates.yml` pinned the
server's copy at `efe05faa0f11ceeea0be63f14f5943b0ccf139b4` (v1.4.2) throughout, so after 1.6.0 the
local clone and the server's fetched copy disagreed. This was finding 12 in the three-lanes-merged
record above, left open there.

`0ad53184` moves the pin to `90d2d5c897ace1879ca6653c079e86d4119bfa0b` (v1.6.0), derived by
dereferencing the annotated tag rather than typed by hand — the same method that reproduces the old
pin from `v1.4.2`, so the derivation is checked against a known case before being trusted on a new
one. The pin remains a commit SHA, not a moving tag ref, per the standing rule this repo already
carries (`tests/test_the_canon_is_pinned_to_a_commit_and_the_pin_is_verified`).

Files read: `.github/workflows/gates.yml`, `tests/test_minor_gate_reconciliations.py`,
`tests/test_node_fitness_test.py`, `tests/test_restructure_merge_gate.py`,
`tests/test_second_sibling_intake.py`, and the external clone's `SKILL.md`,
`reference/review-modes.md`, `reference/architecture-lens.md`, `reference/code-lenses.md`.

Checks run: five, each with its result. Read each of the five previously-failing tests against
1.6.0's actual content, confirmed the needle each asserts still ships (moved into a reference file
the 1.6.0 split created, never removed), and rewrote each to read the skill's full surface — body
plus its `reference/*.md` files — the same way four other prover tests in this suite already do,
rather than the body alone. One test (`test_merge_gate_judges_the_delta_in_the_external_canon`) was
split: the gate's headline stayed asserted against the body alone, on the ground that a body which
drops its own headline should still red regardless of where the supporting detail lives. Ran the full
suite twice — once to reproduce the six red before the fix, once after — and the gate chain once more
before this record.

Findings: four, one repaired, three standing with their reason.

1. **The pin was three releases stale.** Real, confirmed, repaired in `0ad53184`.
2. **`skills/product-prover-pack/SKILL.md:28`** still says three lenses transfer to code; 1.4.3 made
   it two. Real drift, not repaired here: editing that skill body fires gate (s) and owes its own
   committed skill-creator review record, which does not belong bundled into a pin fix. Left as its
   own small landing, named so it is not lost.
3. **`matrix/build-pipeline.md` M-184** calls the architecture lens "Phase 0's lens" with six checks;
   the canon arms it in Phase 0 and runs it in Phase 3e with seven. This contradiction predates
   today's releases (it is a stale spec cross-reference, not a version-pin question) and is left for
   whoever next touches that matrix row.
4. **`matrix/product-prover.md` M-253** names a home for the restructure-merge-gate law that has since
   moved to `skills/director/references/landing-law.md`. Same shape as the open `q-591`, a different
   row; not repaired here.

None of 2-4 is blocking. Each is named so a future pass does not have to re-discover it.



Suite: 2617 passed, 4 skipped, 0 failed. Chain: `bash guardrails/pre-push` — gate a is this record;
every other gate reachable from this range read green on the run just before this file was written.

Blocking: none
