# Prover record — 2026-08-27 declared-defined-and-counted

PUSH-REVIEW

Range: 9e8edea9..5d6535f4 (1 commit).

## What this range is

The word "declared" appeared in the probe's live output all evening with no entry in `PLAN.md`'s
own glossary — the owner caught it and asked directly whether it was an invented status. It is not:
`scripts/state-probe.sh:134` has printed exactly this "verified"/"declared" tag beside the five
canonical marks since this afternoon's rewiring, never a sixth mark of its own. The defect was that
nothing said so where a reader could check. Fixed: both words defined in "Words used here," stated
plainly as a trust qualifier on a mark, never a status of its own, and a declared ✅ named as a
claim rather than proof, per the owner's own rule that anything unverified counts as not-done. The
stale "Task — ten of them" entry, wrong since this afternoon's merge, is fixed alongside it to read
by count rather than by a frozen number.

## Why this record is honest rather than exhaustive

The claim that no other undocumented status word exists in the probe's output was checked by
reading every `print(f"...")` line in `scripts/state-probe.sh`, not assumed — two lines print
task-status text, and both are now accounted for. The count given to the owner (162 tasks, 6
verified, 156 declared, 20 of those declared ✅ with no command behind them) was computed by
importing `parse_tasks` directly and counting, not estimated from the probe's own truncated
top-of-list view.

Files read: `PLAN.md`'s prior glossary section; `scripts/state-probe.sh` in full for every printed
status-adjacent string.

Checks run: `python3 scripts/preshow-register-lint.py PLAN.md` (OK); `bash
guardrails/check-shipped-language.sh` (OK); `python3 -m pytest tests/ -k "board or plan or probe or
traceability" -q` (252 passed, 1 skipped); a direct import-and-count script over `parse_tasks`
against the live `PLAN.md`, output pasted to the owner verbatim.

Findings: none new. The 20-declared-done count itself is the standing finding plan-10 already
exists to close, restated with a real number rather than left as a general worry.

Blocking: none.
