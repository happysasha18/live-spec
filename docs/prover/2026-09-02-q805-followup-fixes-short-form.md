# Prover short-form — the q-805 second-review fixes (2026-09-02 ~03:03)

Short-form per the cadence for a small delta: commit `2d7f42ab` is entirely fixes for the six
findings `docs/prover/2026-09-02-q805-and-followups-review.md` already identified and verified —
no new ground, no undiscovered surface.

Checked each fix against what that review actually asked for, not just that something changed:
`adopt/install-style-gates.sh` now deletes an already-adopted host's leftover
`tests/test_ratchet_lock.py` and strips `max_redundancy_open` from `scripts/spec-debt-cap.json`
(finding 2), proven by two new tests that fail without the fix (`assertFalse` on file existence) and
pass with it — `python3 -m pytest -q tests/test_style_gate_kit.py`, 22 passed. `MAX_REASONLESS`
re-seeded 4→3 against the live count the gate itself reports (finding 3); `python3
guardrails/check-language-rules.py` still exits 0 at the new cap. `docs/language-worked-example.md`'s
one live dangling reference repointed, its two quoted before/after drafts (lines 94, 494) left
untouched, checked by reading. Both skill-review records corrected in place rather than
superseded — `spec-author`'s third file (`how-it-reads.md`) added with the same
no-incident-behind-the-number pattern already used for its siblings; `writing-register.md` reviewed
where it actually belongs, its false cross-reference removed. `spec/guardrails-freshness.md`
Requirement 268 gained criterion 7 naming exactly the repair-and-cleanup behavior `M-327` already
claimed; `PRODUCT_SPEC.index.md` and `TEST_MATRIX.index.md` regenerated and byte-checked against a
fresh build — no drift.

The heal-phrase miss (finding 1, blocking) is fixed by this commit's own message, which carries
`heals landing 51d2d402` literally. `check-landing-next-steps.py` reads the commit message itself,
so the real check is running that script, this line is only a pointer to it.

Red-proven where a fix could plausibly not hold: the two new installer tests, run once with the fix
reverted (a local, uncommitted check) to confirm they fail without it, then restored and re-run
green. Not a repeat of round two's own full sweep — this record only covers whether round two's own
findings actually got fixed, and none of them touched a surface that review didn't already read in
full.

Full suite: not run from this record alone; the orchestrating session runs one clean pass on the
whole merged tree before push, per this project's own standing rule against reporting a red suite
as basically done.
