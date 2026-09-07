# Archived off PLAN.md: a row superseded before it landed

Date: 2026-09-07. `q-824` closes here, superseded by `q-825` (PLAN.md), which carries its own
`**Supersedes.** q-824 (PLAN.md)` paragraph naming what is new and why. The owner's ruling of
2026-09-07 22:10 governs the move: a row replaced by another carries no status of its own, so it
leaves the open list and is named by the row that replaced it, not by a stub of its own.

Superseded, not landed — it was admitted against an acceptance command that runs pytest, which the session-start probe forbids, and the acceptance is frozen at admission, so the row had no road out.

## Index

One line for the archived row, findable by its own number.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
| --- | --- | --- | --- | --- |
| 824 | Admission reads the record before it writes a row | surface | superseded 2026-09-07 | admitted against an acceptance command that runs pytest, which the session-start probe forbids, and the acceptance is frozen at admission, so the row had no road out; superseded by q-825 (PLAN.md), which carries the same work with a check the probe can run |

### ⬜ Admission reads the record before it writes a row — id: q-824
**Group:** Pack quality · **Priority:** normal
**Source:** owner 2026-09-07 20:52 — before admitting any new or continued work, read the current row, its definition of done and its next step, the closed rows related to it, the decisions on record, and the latest related commits; his own words stand in DECISIONS.md under that date.

**Outcome:** a person whose project has a long record stops getting rows that repeat finished work, because the door reads the plan, the queue archive, the decision record and the log before it writes one

**Statement.** Echo-name: Nothing settled gets started over. Description: this project keeps a long written record — the list of tasks, the archive of tasks already closed, the page of decisions the owner has made, and the commit history. Nothing read any of it before a new task was created, so work already finished, or a way of checking already ruled out, could be started over. The change makes the step that creates a task read all four first, refuse a task that repeats one already there, and name the earlier task and the file it stands in when it does. Plan: 1) have the check for a repeated task title read the archive of closed tasks as well as the live list, and name the earlier task and its file when it refuses 2) require every new task to carry what was read and what it found, refusing any task id, commit or decision date that turns out not to exist 3) allow one written override for a deliberate repeat, which has to name the earlier task, what is new this time, and why the earlier decision misses it, all three kept on the new task 4) add one command that prints every task, decision line and commit message containing the words a person gives it 5) state the rule as product law in the specification, so a project that installs the pack inherits it without reading any code. Estimate: 3–5 hours — basis: the author's own reading of the plan, with no closed task in this project whose recorded duration the range could rest on.

**Validation.** 2026-09-07 · floor: passed · reader: passed · echo-name placed: yes · status: ready

**Frozen at take-up 2026-09-07.**

**Done when:** the admission door refuses a route carrying no read of the record and refuses any reference that resolves to no row, no commit and no dated decision entry; the duplicate scan reaches the queue archive beside the live plan and its refusal names the row and the file it stands in; that refusal lifts only against a supersedes record naming the row, what is new and why the earlier decision misses it, all three landing on the admitted row; one command prints what the plan, the archive, the decision record and the log hold about a set of words, with no score and no cutoff; the law stands in the spec as Requirement 321 under INV-327, with matrix rows M-651 to M-655 each red-proved against the door as it stood at 186dc4a2

**Read before admission.** q-823 (PLAN.md), q-822 (PLAN.md), 2026-09-04 (DECISIONS.md), 186dc4a2 (commit 186dc4a2). Finding: No row on the record covers reading the record at the door. q-823 and q-822 moved the closure kernel and split the Director, and neither touched what admission reads before it writes. The decision record holds nothing on repeating closed work, and 186dc4a2 is the range this lands on. The nearest standing law is Requirement 43's three-source impact read, which reads the spec, the architecture and the code — the product's own sources, and not the project's record of what it already settled.

**DOD hash.** afe916ae94919256f9d7059cb98aa261f8cdcc4e887afa51d53ac04ea5817406

**Verification:** PYTHONPATH=tests python3 -m pytest -q tests/test_task_admission.py, plus the row's own recorded acceptance key in scripts/plan_checks.py

**Context pointers.** INV-327; spec/queue-intake-priority.md Requirement 321; scripts/task-admission.py:admit; M-651; 186dc4a2
