# PUSH-REVIEW — the published tree counts follow the slimmed bodies

Date: 2026-08-17 22:52 local. Range: ca2d31f..5478ede (one commit, 5478ede).
Root: server run 32059996840 on main failed on gate ad alone — README.md publishes a
generated skills-lines block, the slimming packet changed the skill line counts, and
the generator was not re-run inside the packet's range. This record covers the repair.

Files read: README.md (the one generated line, before and after); the gate's own
output naming the three counts it judges.

Checks run:
- `python3 scripts/gen-tree-counts.py` — rebuilt the generated blocks; README.md took
  one changed line, `guardrails/README.md` rebuilt byte-identical.
- `python3 guardrails/check-tree-counts.py` — OK, matched 3 of 3 rows (gate-roster,
  scaffold-checks, skills-lines), 0.2 s. This is the exact check the server run failed.
- `git show --stat 5478ede` — the commit carries README.md alone, 1 insertion,
  1 deletion; docs/PROGRESS.md stays out of it.

Findings: none beyond the root above. The failure was mechanical staleness of a
generated count after the slimming, not a wrong count published by hand.

Blocking:
- none.

Standing note for the night lanes: every packet that changes a skill's size re-runs
`gen-tree-counts.py` and carries README.md in the same packet — written into the
night brief addendum.
