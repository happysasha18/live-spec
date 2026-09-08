# A corrected definition of done leaves its prose copies behind

From: the global review of the push review path, 2026-09-08 21:36 (record:
`docs/prover/2026-09-08-the-mode-line-is-a-field-the-gate-never-reads.md`). Deposited rather than
worked, which is what the review contract this same push ships asks a review to do with anything
true it notices outside its own scope.

When the owner corrected q-827's definition of done mid-flight at 21:26, the correction landed on
`PLAN.md` and on the checkpoint's `DOD:` anchor, which now carries the new digest. Two prose copies
of the old done stayed where they were, and nothing on either says it has been superseded. The
checkpoint `.live-spec/checkpoints/q-827.md` still states the replaced done verbatim in its DECISION
SHEET — its digest is exactly the `previous hash:` PLAN.md records — so the row's own resume artifact
hands a future reader the contract the owner replaced. The comment above `CHECKS["q-827"]` in
`scripts/plan_checks.py` still says a global review runs only on the owner's word, which the
corrected done and the shipped skill both contradict with the second trigger. The shape is that a
mid-flight correction updates the plan row and the anchors while the prose copies of the same
sentence go on standing.
