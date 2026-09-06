---
name: build-pipeline
description: >-
  Execute work after director has classified the human's message and returned a route contract. Derive the observable outcome and definition of done, admit new work to the one board, update existing work in place, call only needed specialists, verify, close and report. Also use when asked to attach live-spec, adopt live-spec, install live-spec, onboard a codebase with live-spec, set live-spec up, set a project up on live-spec, add live-spec, found or start a new project with live-spec, or update live-spec, and for the MINOR-bump gate.
metadata:
  version: 6.1.0
---

# build-pipeline — accepted work from admission to close

> Part of the **live-spec pack**. The shared working rules, the settings ladder, and the pack's
> glossary live in `live-spec-base` (v6.1.0). This skill does not restate them. Loaded alone, every
> section below still runs.

Director is the only first reader. It classifies every act, says whether the turn proposes new work
or changes existing work, and returns a route contract. This skill never reclassifies the message.
It begins only after that contract exists, and owns everything from a candidate's observable
outcome and definition of done through verification and close.

## Accepted-work pipeline

Read [references/accepted-work-execution.md](references/accepted-work-execution.md) for the full
execution procedure whenever Director routes new or existing work here.

For a new-work candidate, derive these facts before changing the board:

- the source: the person's request, or a promised behaviour plus the reproduction an outside user
  meets;
- one observable outcome the person could want on its own;
- a definition of done that a command, test, artifact read, or independent verifier can decide
  without making the person the checker;
- the project and scope the result belongs to;
- the existing row that already covers it, or an explicit finding that none does.

Missing any one means no new row. Continue reading the project to derive it; ask the person only
for a product choice no artifact settles. A review opinion, another project's note, a mismatched
internal number, or a red check about document shape is not a candidate and returns to the review
that produced it.

Pass the route through `python3 scripts/task-admission.py --route <route.json>`. This is the one
write door for a new heading-shaped PLAN: it validates source, outcome, DOD, verification, project,
scope, context pointers and duplicate title, then writes exactly one row and its pipeline-owned
checkpoint. A route for a question writes nothing; a correction names existing work and writes
nothing new.

Admission also derives the task's statement onto that row — an echo-name of two to five words, a
description a stranger can act on, a plan whose steps stand in the order they run, and a time
estimate given as a range with the basis it rests on. The person never writes those fields, and no
default fills one in. Before the task is taken up, `python3 scripts/task-admission.py validate <id>
--reader <file>` runs the mechanical floor and a clean-context reader's record over that statement;
`hold` refuses a row whose validation has not passed. See
[the execution reference](references/accepted-work-execution.md) for who writes the reader's file
and what take-up freezes.

A correction, decision or halt targets the existing row and checkpoint named by Director and
creates zero new work. A new candidate that passes admission creates exactly one row. `PLAN.md` and
its generated board are the only task state; `NEXT_STEPS.md` is never read or written as a queue.

After admission, assemble the smallest graph that reaches the outcome. Load only the specialists
Director named, add or remove one when a new fact changes the graph, and keep one checkpoint for the
whole piece of work. The definition of done is the closing contract: meet it, verify it without the
producer's self-report, close the checkpoint and row, show the result, and continue without waiting
for the person's attention.

## The closing kernel

A row is closed against the definition of done it was admitted on, never against what shipped.
Three commands carry that, and a session holding only this page can run them:

- `python3 scripts/task-admission.py correct <id> --done "<new>" --source "<who asked>" --reason
  "<why>"` — the only door through a done already fixed;
- `python3 scripts/task-admission.py verify <id> --by <name> --command "<cmd>" [--surface <path>]`
  — the acceptance receipt, refused when `--by` names the row's own holder;
- `python3 scripts/task-admission.py close <id>` — which reads that receipt.

Every refusal prints one reason, exits 2, and leaves the row's mark where it was.

The ten clauses this rule stands on — who may change a done and what that keeps, what the verifier
receives, what voids the evidence, what `blocked` may mean, and why the presence of a test is not a
test that passes — are in
[references/accepted-work-execution.md](references/accepted-work-execution.md), which is their one
home.

Execution references live here, not in Director: [class hunt](references/class-hunt.md),
[verification](references/verify-step-detail.md), and [landing law](references/landing-law.md).

| Specialist | Pipeline call condition | Where it lives |
|---|---|---|
| Test author | the evidence and the regressions have to be chosen | `skills/test-author/SKILL.md` |

## The craft ladder — which craft's standards judge each step (SPEC INV-33)

Each artifact is judged by its own craft's standards. The **spec** is judged as a strong product
manager judges it: the user's journey, the product's words. **Prove** and **prove architecture**
are judged as the prover's formal-methods reviewer judges them. The **architecture** is judged as
a software architect judges it: nodes, seams, one responsibility each. The **matrix** is judged as
a QA automation lead deriving coverage. The **test** is judged as the same QA engineer writing it.
The **code** is judged as a senior developer. **Verify** is judged by the visitor's own fresh eyes,
the builder's own view set aside. **Commit & show** is judged as a careful release manager whose
reader is the human.

The craft takes the work-kind's form (SPEC INV-22, INV-33). On a prose product the code step is
worked as a strong writer. On infra it is worked as a toolsmith. The ladder names the archetypes,
and the kind says what their standards look like in its medium.

## Setting a project up on the pack

A session that hears "attach live-spec to this project", "found a new project on live-spec", or
"update live-spec here" runs a setup walk first. Read
[references/project-setup.md](references/project-setup.md), the routing card beside this page. It
resolves the pack tree, reads the project tree, and names the walk this project takes. The setup
entry stands outside the derivation chain. When the walk finishes, the first wish enters through
`director` like any other request.

## Gates worth remembering

- **Before a MINOR (0.x.0) bump:** see
  [references/minor-bump-gate.md](references/minor-bump-gate.md) for the full gate procedure — the
  3-pass preventive audit, the full design review, the cross-cut counter, code compaction as a
  station beside doc compaction, and the skill-creator craft review.

## How it relates to the other skills

- `director` (`skills/director/SKILL.md`) — reads the human's message and stops at the route
  contract. It names possible specialists; this pipeline calls them after admission.
- `live-spec-base` — the shared rulebook, the settings ladder, and the glossary every term on this
  page resolves against.

## Work that belongs elsewhere

Understanding what the human just did belongs to Director. Authoring the spec, architecture,
matrix, tests, code and release artifacts belongs to the specialists this pipeline calls. This
skill owns admission, orchestration, evidence and close; it does not absorb their craft.
