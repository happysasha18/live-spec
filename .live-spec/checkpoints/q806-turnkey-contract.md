# q-806: turnkey product contract proven before code
Status: open
Owner: director

## DONE

- Two independent contract drafts written and composed into one (`.live-spec/turnkey-contract-composed.md`).
- product-prover pass 1 (this session): 3 defects, folded.
- product-prover pass 2 (Fable, independent): 12 defects + 3 recommendations, all folded (F1-F15).
- Live bug found and fixed along the way: checkpoints were gitignored, never reaching git (`ba7bc8e4`).

## IN PROGRESS

Nothing actively running. Contract text is stable pending nothing further known.

## NEXT

1) Confirm the contract reads clean end to end (no stray contradictions from the fold). 2) Close this ticket ✅ once confirmed. 3) Open q-807 (or next id) for package 2, the vertical path: ticket -> worker -> independent acceptance -> delivery -> done -> resume. 4) Separately: verify a clean/fresh worker can resume real work from state-probe.sh + PLAN.md + a checkpoint alone, no spoken handoff (owner's ask, 13:04) -- run this AS a real test in an isolated worktree, not the main tree.

## DECISION SHEET

Goal: a short Director/ticket/checkpoint contract, reviewed by product-prover twice, ready for test-author. Observable outcome: .live-spec/turnkey-contract-composed.md holds zero open defects and names any open owner-question by name. Dimensions: spec/architecture design, testing method. Known: two independent drafts composed, two prover passes done, 15+3 findings folded. Unknown: nothing structural; the one open item (time estimate) is answered and deferred to its own future ticket, not blocking this one. Risk: low -- no code, no push yet.
