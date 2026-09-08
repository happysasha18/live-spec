# Prover record — 2026-09-08 q-827 closes on its own acceptance

PUSH-REVIEW

Mode: closure
Range: 7c72c11e..cb7610ad
- cb7610ad q-827 closes on a passed acceptance
- 7c72c11e The record covers the two repairs the push chain asked for (base)

This is the closure review the row's own close stands on, written down by the seat that carried the
work from the verdict of the pass that produced none of it. The pass read the reach closure names
and nothing beyond it — the row's definition of done, its recorded acceptance command, the diff of
the range that delivered it, and the paths that diff touches. It is the first use of this mode as a
row's own verification, which is what the closure kernel already asks for: the producer never issues
its own verdict.

Files read: PLAN.md (the q-827 block and its current `**Done when:**`), `scripts/plan_checks.py`
(`CHECKS["q-827"]`), `.live-spec/checkpoints/q-827.md` (its `DOD:` and `ACCEPT:` anchors),
`skills/product-prover-pack/SKILL.md` (the two mode sections), `docs/prover/README.md` (the record
shape), `guardrails/check-prover-record.sh` (the field loop and the mode arm),
`tests/test_review_modes.py`, `tests/test_push_review.py`, and the diff 4b87ff28..7c72c11e that
delivered the row.

Checks run: eight, each with its result.

- `CHECKS["q-827"]` run verbatim from the repo root — exit 0.
- `python3 -m pytest -q tests/test_review_modes.py tests/test_push_review.py` — 33 passed.
- twelve further test files that read the changed paths — 340 passed, 3 skipped.
- `guardrails/check-pin-drift.sh`, since the range re-points two ARCHITECTURE pins — OK, 195 pins,
  none drifting.
- `scripts/sync-skills.sh`, since the range edits a skill body — everything fresh, no change.
- `guardrails/check-skill-review.sh` and `check-skill-loadability.sh` — OK.
- the done digest recomputed over the current `**Done when:**` — matches the row's `**DOD hash.**`
  and the checkpoint's `DOD:` anchor, so the row closes against the contract it was admitted with,
  including the owner's 21:26 correction.
- the acceptance digest recomputed over `CHECKS["q-827"]` — matches the checkpoint's `ACCEPT:`
  anchor, so the command that ran is the command the row was admitted against.

Findings: none material. The five clauses of the current definition of done were read one by one and
none falls short: the two modes are named; closure's reach, its material-failure-alone blocking set
and its one-inbox-deposit rule are stated, and the range practised the rule rather than only writing
it; global's two triggers are written with the scope named outright and the reach bounded to
reproducible material failure of that surface; the record shape carries the mode and the gate reads
it, which is the clause the range had to repair mid-flight and did; and both modes are proved
through the gate against a planted record of each shape, the negative arms each returning the gate's
own refusal rather than passing quietly. Nothing in the diff breaks a path it touches, and no claim
in the range's commit messages was found false — the one that was is named and repaired inside the
range itself.

Blocking: none
