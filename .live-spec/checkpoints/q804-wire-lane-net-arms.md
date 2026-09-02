# The parallel-lanes machinery still netted by git and the prover ships for real
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

(nothing yet)

## NEXT

(nothing yet)

## DECISION SHEET

Goal: the two already-built, already-red-proven net scripts (check-merge-base.sh, check-worktree-line.sh) get real callers, and INV-199's still-missing stale-lane check gets built -- per the 2026-09-02 hostile review finding 2, a script nothing calls does not keep a promise. Outcome: check-merge-base.sh is invoked ahead of the landing gate in the real landing walk (open-lane.sh / lanes-and-pen.md path), and reds live when a lane has not rebased onto main's tip; check-worktree-line.sh is invoked at the adoption/catch-up walk (adopt/ADOPT.md, START.md, MIGRATION.md) for a HOST project only -- never wired into this repo's own push chain, since Requirement 88 criterion 3 leaves that write shut until the owner speaks; a new stale-lane check (Requirement 86 criterion 6, INV-199 residual) reds a lane worktree or lane/* branch with no open PLAN.md row. Dimensions: architecture (the concurrency-safety net itself), quality/safety (this is literally the machinery that protects against simultaneous writes -- the exact class the seat mis-handled twice earlier tonight per its own prior-session note: a test nailed to text, and a commit over someone else's run). Known: both scripts exist and pass their own fixture tests (tests/test_lane_net_arms.py); grep confirms no real caller exists for either outside those tests. Unknown: the exact right call site inside open-lane.sh (before or wrapping the worker handoff) and inside the adopt walk steps. Risk: this IS the concurrent-write protection; a wrong wiring could false-negative (net doesn't fire) or false-positive (blocks legitimate lanes). HIGH CARE. Specialist: opus-tier worker in lane/q-804-wire-lane-net-arms, briefed to red-prove every wiring by mutation (plant the violation on a hermetic scratch repo, confirm red; remove it, confirm green) exactly as tests/test_lane_net_arms.py already does for the scripts themselves -- never trust a green from prose. The seat re-checks the diff and the red-proof transcript itself before accepting, per base rule 5. Evidence: tests/test_lane_net_arms.py gains real-caller assertions (grep for the call site, not just the script's own logic); a new stale-lane test red-proves the same way; full suite green. Next: dispatch worker with this brief plus PLAN.md's own q-804 body verbatim as primary source.
