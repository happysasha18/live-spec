# live-spec — Resume state

Tasks, their states, priorities and order live only in `PLAN.md` and its generated board. This file
never repeats them and never carries a forward queue (SPEC INV-48).

## TRANSIENT EXECUTION STATE (2026-09-05)

None. Read `PLAN.md` for all planned work.

When an interruption leaves state that the board and version control cannot reconstruct, replace
`None` with only the unfinished write-set, live worker identity, or failing command and current
hypothesis needed to resume safely. Remove it once recovered.
