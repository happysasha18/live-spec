# Prover record — 2026-08-27 verbatim-task-brief-correction

PUSH-REVIEW

Range: a490b0ed..42df9786 (1 commit).

## What this range is

One tightening in `PLAN.md`'s task-shape section, on the owner's own correction this evening: a
worker's brief is now stated as the task's exact board entry pasted unchanged, not a brief derived
or composed from the task's links. Closes the gap he named — "полная совместимость" between the
board's own words and what a worker is actually told.

## Why this record is honest rather than exhaustive

No new mechanism, no new file, no gate. One sentence in an existing section, checked against the
owner's own quoted correction before being written. `hooks/scissors-scan.py` and
`hooks/affirmation-scan.py` were also read directly this evening, not taken on memory, to answer
his question about whether either is a literal phrase list or an expensive check: the first is two
structural regex patterns (a grammar shape, not a word list), the second is ten enumerated phrase
families (bounded, evadable by novel wording — stated plainly rather than oversold); both measured
at ~30ms per local invocation, no model call, no token cost.

Files read: `PLAN.md`'s prior task-shape text; `hooks/scissors-scan.py`,
`hooks/affirmation-scan.py` in full.

Checks run: `python3 scripts/preshow-register-lint.py PLAN.md` (OK); `bash
guardrails/check-shipped-language.sh` (OK); `python3 -m pytest tests/ -k "board or plan or probe or
traceability" -q` (252 passed, 1 skipped).

Findings: none. No requirement, criterion, invariant or anchor touched.

Blocking: none.
