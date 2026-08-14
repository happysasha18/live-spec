# `SKILL-REVIEW` — live-spec-base, the settings ladder moves to a reference module

Skill: live-spec-base. Date: 2026-08-14. Range: be4e4f0..c73c6e4.

Commit `b2fc1af` moves the settings ladder out of `SKILL.md` into
`references/settings-ladder.md`, loaded on demand when a setting is being resolved. An
independent adversarial review on 2026-08-14 returned ALLOW-WITH-NOTES: the ladder's wording is
preserved byte for byte; every rule stays mandatory; 16 guards were proven red on the moved state
and green after the pointer repairs; the full suite's node-id set is identical to the base
(2,552 collected). The two notes are non-blocking and recorded in
`docs/prover/2026-08-14-push-review.md`. Verdict: passes.
