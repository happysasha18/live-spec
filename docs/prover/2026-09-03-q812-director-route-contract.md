# Prover record — 2026-09-03 q-812, the Director's task-lifecycle contract

Prover version: 1.6.2 (external skill, `skills/product-prover/`). Mode: feature-fit review — one
route's fit against the document it already lives in, run before any code, on `PLAN.md` q-812's own
instruction that the contract be checked ahead of the proof.

Not a push review: no range is measured here, and this record carries none. The push that carries
this work owes its own.

Files read: `spec/message-first-read.md` (Requirements 313 and 314, whole), `spec/wish-intake.md`
(Requirement 4, whole), `scripts/checkpoint.py`, `scripts/plan_checks_core.py`,
`scripts/plan_checks.py`, `scripts/state-probe.sh`, `scaffold/status-view/state-probe.sh`,
`adopt/install-status-view.sh`, `matrix/director.md`, `evals/director/README.md`,
`evals/director/check.py`, `PLAN.md` q-812.

Checks run: `grep -rn "second checkpoint\|one checkpoint" guardrails/ scripts/ tests/` — one hit, a
comment; no gate. `python3 guardrails/check-index-generated.py …` — OK, 395 codes agree.
`python3 guardrails/check-matrix-reference.py …` — OK, 402 anchors agree.
`python3 scripts/spec-style-lint.py spec/message-first-read.md` — 0 errors, 0 warnings.

## What the route promises today

Three requirements carry it. Requirement 313 holds the first read: seven acts, read from the
situation, work started only behind an instruction, a correction or a decision. Requirement 314 holds
what accepted work writes down: the decision sheet, inside that work's own checkpoint, one checkpoint
for its whole life, and which of several open pieces runs next. Requirement 4 holds the row: written
before the work starts, never deleted, closed only with a named exit, and read as reopened when a
done mark's own acceptance command fails.

The contract is in good shape, and two of its clauses are unusually careful: 314 criterion 4 and
criterion 5 both name the checkpoint command as the thing that refuses, and both refusals are real —
a first-read-owned checkpoint cannot be created without a sheet, and a close is refused while the
file still names work in progress. Criterion 313.7 is the model for honesty in this document: it
states out loud that the first read stands on the reading skill's text and claims no command, gate or
hook.

## F1 — The one-checkpoint rule reads as mechanically enforced, and nothing enforces it

> "*while* one piece of work runs, the system *shall* keep it on the one checkpoint it opened and
> *shall* open no second checkpoint for it." — `spec/message-first-read.md` R314 criterion 3

Criterion 3 sits four lines above two criteria that name the checkpoint command as the enforcer, and
carries no sentence of its own about what holds it. Nothing does. No gate, script or test counts a
piece of work's checkpoint files; `new_checkpoint` against an existing path overwrites it rather than
refusing, and a second checkpoint written at any other path passes `checkpoint.py validate --all` and
every reader in the tree.

Who is affected and how: a test author reading this requirement writes an assertion for a guarantee
nobody built, or — the case in hand — writes no assertion at all because the sentence reads settled.
A Director that opens a second checkpoint mid-correction leaves two decision sheets for one piece of
work, and the next session picks whichever it reads first; nothing reports the split, and the probe
cannot see it, since the probe reads the queue.

Proposed action: state what holds criterion 3, in the shape criterion 313.7 already uses, and state
the mechanical half that is real. Two criteria, appended so nothing renumbers.

closed: `spec/message-first-read.md` R314 criteria 11 and 12, and their proof in `matrix/director.md`
M-631 → `tests/test_director_route_end_to_end.py::TestACorrectionLandsOnTheSameCheckpoint`, which
asserts the update path holds one file and says in its own name that nothing counts the second.

## F2 — The hazard is the lost first checkpoint, not the extra one

> "It always creates the file from a blank template … it is the 'start over' operation, not the
> 'edit' one." — `scripts/checkpoint.py`, `new_checkpoint` docstring

The document says a piece of work keeps one checkpoint. The command it would be written through has
two operations, and the wrong one silently discards the work already recorded: a second `new` against
the live path returns 0 and leaves a blank template where the DONE list was. A correction routed
through `new` therefore satisfies criterion 3 to the letter — one file — and loses the whole record.

Who is affected and how: a session correcting work in flight, one command away from erasing what the
work has already finished, with an exit code of 0 and no warning.

Proposed action: name both operations in the requirement, so the reader knows which one the
correction route is. Do not add a refusal to `new`: the overwrite is the deliberate start-over
operation another caller uses, and a guard on it is machinery this row forbids.

closed: criterion 12 names both operations. `test_the_create_operation_is_the_one_that_would_lose_the_work`
proves the overwrite on a live host, and the same test shows the update path carrying the record
through.

## F3 — Can a task be marked done before its check passes? Verdict: the contract answers, reactively, and says so

> "The system *shall* let a row's mark be written by whoever edits the queue, and *shall* claim no
> check that reads a closing row's own acceptance before that mark changes." — `spec/wish-intake.md`
> R4 criterion 9

This is the clause q-812's fifth point puts pressure on, and it is a deliberate negative claim rather
than an omission. Read with criteria 10 and 13, the contract holds that the mark is a character
somebody types and the STATUS is computed: a done mark whose command fails reads reopened, and a
reopened row reads done again "on that command alone and with no further mark from a person". So the
state a reader receives cannot say done until the check passes, which is what the owner's clause
asks. What the contract declines is a gate ahead of the typing.

That decline is right, and it is the reviewer's own reading rather than the document's word: the
queue is a markdown file a person edits, and a check standing between a person and their own text
file is a hook on every edit — the exact machinery q-812's brief names and refuses. The reactive
guarantee is also the stronger of the two in one respect: a preventive gate passes once, at the
moment of marking, while the reactive one re-reads the command at every session start and reopens the
row the day the command stops passing.

No spec change. The gap was proof: no test walked a done mark against a failing key on a clean host
through the route's own readers.

closed: `matrix/director.md` M-632 → `TestADoneMarkWaitsOnItsCheck`, red proven by removing the
failing-key branch from `scripts/plan_checks_core.py` and watching the falsely-done row drop off the
open list.

## F4 — Does a fresh session resume the same work? Verdict: covered, and mechanically checkable

> "*when* several pieces of accepted work stand open at once, the system *shall* name which one runs
> next, read by `scripts/state-probe.sh` from the states the plan records rather than composed from
> memory." — `spec/message-first-read.md` R314 criterion 6

Criterion 6 names the reader and the source; criterion 7 names the ordering and forbids reading it
from anywhere else; the requirement's own context states that the sheet lives in the checkpoint so a
session starting fresh reads it with the conversation gone. Against duplication, Requirement 4
criterion 1 gives one wish one row, and Requirement 313 criteria 4 and 5 keep a resume turn — which
asks for nothing new — from opening anything.

So the data constrains the answer to one row, and that is a fact a test can hold without a model. The
half a test cannot hold is whether a session actually reads it, which is where it already sits: the
project's own boot file names the probe as the session's first action.

No spec change. The gap was proof.

closed: `matrix/director.md` M-633 → `TestTheRecordedStateNamesOneNextAction`, red proven by
replacing the probe's next-up read with the last open row.

## What I assumed

I read q-812's fifth clause — «Задача может стать ✅ только после её DOD и зелёной нужной проверки» —
as a claim about the state a reader is given, not about which characters a person may type into a
markdown file. Under the other reading, the contract fails the clause and only a commit hook could
satisfy it, which the same brief forbids in its first paragraph. Say so if the second reading was
meant.

## Open question, left open

Nothing in the three requirements says a row's mark and its checkpoint's status must agree. A closed
checkpoint beside an open row, or a done row over an open checkpoint, is a state the contract permits
and no reader reports. It is outside q-812's six clauses, and closing it needs either a new criterion
with an enforcer behind it or a deliberate decision to leave the two independent. Recorded here, not
acted on.

Findings: F1 (closed, spec delta), F2 (closed, spec delta), F3 (no change owed, verdict recorded),
F4 (no change owed, verdict recorded). One open question for the owner, non-blocking.

Blocking: none.
