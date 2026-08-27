# Prover record — 2026-08-27 queued-gets-a-criterion

PUSH-REVIEW

Range: c9b8cfdd..f4bad2f8 (1 commit).

## What this range is

The owner's refinement to the two-states question this evening: "принято в работу" — a task
qualifies for ⬜ only when it is clear what to do and it is well-formalized. Written into the
glossary as a bar rather than a feeling: ⬜ requires resolving links and a real command as done;
🔄 requires an actual worker holding it under the take-or-decline rule already stated in the task
shape. No new mark — this gives two of the existing five a checkable criterion.

## Why this record is honest rather than exhaustive

The wording was checked against the task-shape section already on the page before being written,
so the new criterion quotes rather than duplicates ("a task pointing at nothing is the finding, not
a task ready to hand out"), keeping the one-home-per-fact law this same evening's other edits have
been enforcing.

Files read: the task-shape section and glossary as they stood before this edit.

Checks run: `python3 scripts/preshow-register-lint.py PLAN.md` (OK); `bash
guardrails/check-shipped-language.sh` (OK); `python3 -m pytest tests/ -k "board or plan or probe or
traceability" -q` (252 passed, 1 skipped).

Findings: none. No requirement, criterion, invariant or anchor touched.

Blocking: none.
