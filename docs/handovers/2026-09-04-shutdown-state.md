# Where this stands at shutdown — 2026-09-04, 15:59

The machine is being turned off. Nothing was pushed. Everything below is committed in
`~/live-spec` on `main` and on one side branch, and a bundle of every branch sits at
`~/live-spec-bundles/2026-09-04-live-spec-unpushed.bundle`, off the volatile path.

## What is done and committed

Five rows closed: q-820, q-818, q-819, q-817, q-48. Four rows opened: q-822 (a session starts
light), q-823 (the rulebook stops using words it never explains), q-824 (a feature's success
measure is bound to a number a machine reads for it). Each carries its own definition of done.

## What is NOT done, and it is what stands between here and a push

The prover reviewed today's spec delta twice. The first review found seven defects, six of them
blocking; those were repaired. **The second review found the repairs opened four new blocking
defects**, and it is right about all four. The record is
`docs/prover/2026-09-04-repairs-recheck.md`.

One of the four is repaired and committed: the `[target]` promise this session dropped is back,
Requirement 102 clause 5 says what counts as keeping it, and q-824 owns it.

**Three are open**, and a lane was working them when the machine went down. Its partial work is
committed on the branch `lane/recheck-fixes` at `2221098d` — a save point, incomplete and
unverified. Its brief is `docs/handovers/2026-09-04-recheck-fixes-brief.md`, rescued out of the
wiped path. The three:

1. **R1, the worst.** `guardrails/check-status-view-drift.py` decides whether it is looking at the
   pack or at a host by asking whether the repo carries a `VERSION` file. Host repositories carry
   `VERSION` files. A host with one, with a recorded pack root and with a genuinely drifted copy,
   prints "0 vendored file(s) checked … no drift" and exits 0. The honest silence this check had
   before became a false green, which is worse than what it replaced. The general form matters more
   than the discriminator: **a comparison that compared nothing must never print a pass.**
2. **R2.** The next move is picked from the queued rows alone, so a reopened row can never win it,
   and the reason line under it can read "nothing of higher priority is free" with the higher-ranking
   free row printed one line above. The decision is already made and written in the brief: the
   candidate set is the reopened rows first, then the queued ones, and a blocked row never wins.
3. **R5.** `templates/PLAN.template.md` names a priority word its own seeded statement does not
   name, so the template's own worked example ranks last by its own rule.

Riding with them, non-blocking: R3, R6, R9, R12, all stated in the brief.

## The suite

Two full runs today. The second read 5 failed, 2831 passed, in 36 minutes. Three of those five are
already repaired since that run started (the prover record is committed, the `[target]` owner is
restored, the resume file is refreshed). Two are real and open:
`tests/test_director_route_end_to_end.py`'s two next-action cases still expect the old rule, where
a row already in hand won the next move. Rule 38 says the next move is the topmost row nobody is
working yet, the renderer now follows rule 38, and those two fixtures have to follow it too. That
repair belongs with R2 and is not done.

## The order to pick this up in

1. Finish R1, R2, R5 from the brief, and the two director-route fixtures with R2.
2. Fold in R3, R6, R9, R12.
3. Run the prover once more over the whole delta. If that record is clean, the push goes.
4. If it finds more blocking defects, cut the push down to a smaller slice and say which — the
   review loop has run twice and each round has found real things, so a third round finding more is
   a signal to land less rather than to keep repairing.

## Two things worth knowing before touching any of it

The session's own context ran to nearly 100,000 bytes of reading that a worker should have done.
The lesson is written at `~/.claude/projects/-Users-sashaabramovich/memory/`.

The rulebook cannot be made smaller by rewriting it. That was measured today end to end: its bare
claim text is 30,337 characters against a 32,000-byte file. Row q-822 carries the shape of the work
that can make a session lighter, and the stop sign is the director's own scenarios rather than a
byte count.
