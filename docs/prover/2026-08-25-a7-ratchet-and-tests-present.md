# Prover record — 2026-08-25 a7-ratchet-and-tests-present

PUSH-REVIEW

Range: 9132c76e..25ce3d8e (1 commit)
- 25ce3d8e Lower the live-spec-base ratchet honestly with A.7's shrink (598)

Files read: full diff of 25ce3d8e (1 file, 10 insertions / 8 deletions);
`tests/test_live_spec_base_body_thinned.py`'s current state (not just the diff); the local
push-gate's `gate h` (tests-present) output that caught the missing test-directory change on the
prior push attempt.

Checks run: the local push attempt for A.7's compression (`6a99bf32`..`9132c76e`) hit
`FAIL (tests-present): user-facing file(s) changed with no change under tests/:
skills/live-spec-base/SKILL.md` — a change to this skill's body with no accompanying edit under
`tests/`. Fix: lowered `CURRENT_MAX_LINES` in `tests/test_live_spec_base_body_thinned.py` from
608 to 598, matching the same "ratchet moves down honestly with every real shrink, never left
stale" practice this file's own comment already documents for the prior 615→608 move — the body
actually landed at 592 after A.7's compression, so 608 was already 16 lines stale. Chose 598 to
keep the same ~6-line headroom the prior ratchet held over its own actual count (602 actual under
a 608 ceiling). This is a real test-directory change, not a cosmetic one that only exists to
satisfy the gate — the ratchet is the mechanism that would catch a future regrowth past this
session's work, and leaving it at 608 would silently permit 16 lines of regrowth before any gate
noticed.

Re-ran `python3 -m pytest -q tests/test_live_spec_base_body_thinned.py` — 6 passed, confirming the
new ratchet holds against the actual 592-line body with room to spare, and every other assertion
in this test file (headings present, reference modules exist, relocated text intact) is
unaffected by this one-line threshold change.

Findings: none beyond the gate catch itself, which is the mechanism working as designed.

Blocking: none
