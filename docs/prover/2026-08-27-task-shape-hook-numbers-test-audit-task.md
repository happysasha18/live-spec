# Prover record — 2026-08-27 task-shape-hook-numbers-test-audit-task

PUSH-REVIEW

Range: bd43ce6b..9796c61c (1 commit).

## What this range is

Three additions to `PLAN.md`, all prompted by the owner's own pushback this evening rather than by
this session's own initiative: the task-shape section (plan-11) gains four lines grounded in this
same afternoon's real collision incident — one worker owns one task including its subtasks, a
worker reads and declares taken-or-declined before touching anything, write-set disjointness is
checked by whoever hands out work before handing it out, and the worker proves its own done by
command in addition to the accepter's independent re-check; a new task, q-751, applies plan-6's own
already-proven sampled-measurement method to the test suite's size instead of guessing at it; and
the hook-cut Blocker entry gets the 11.08 meter numbers it was missing, so "decide what to bring
back" has real fire-rate evidence (scissors-scan 131/3288, affirmation-scan 37/2612, hedge-scan
4/3023) behind it instead of a guess.

## Why this record is honest rather than exhaustive

The claim that the 26.08 hook cut was "blanket, not a verdict on any one hook" was checked against
`PLAN.md`'s own prior text before being restated, not assumed. The fire-rate numbers were read
directly from `.live-spec/r3-rule-fires-2026-08-11.md`'s own table, quoted, not estimated. No new
gate, hook, script or storage location was created by this range — all three additions are prose in
an existing document, per the owner's own caution tonight against building machinery without an
incident behind it.

Files read: `PLAN.md`'s prior task-shape and Blockers text; `.live-spec/r3-rule-fires-2026-08-11.md`
in full for the meter table; `plan-6`'s own text as the method q-751 cites.

Checks run: `python3 scripts/preshow-register-lint.py PLAN.md` (OK); `bash
guardrails/check-shipped-language.sh` (OK, after marking one quoted owner phrase); `python3 -m
pytest tests/ -k "board or plan or probe or traceability" -q` (252 passed, 1 skipped, re-run after
the edit); `bash scripts/state-probe.sh` (re-run, confirms the board's top is unchanged by this
prose-only range).

Findings: none. No requirement, criterion, invariant or anchor touched.

Blocking: none.
