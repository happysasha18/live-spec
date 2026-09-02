# Turnkey productization — product contract (draft, orchestrator)

Independent draft. Written with no sight of the parallel Fable draft. Scope: the short contract
that goes to product-prover before any code starts — not the rollout plan, not code.

## Why this contract exists

`PLAN.md`'s own Goal section already states the target: a single author dumps ideas in any order,
the system lines them up into spec/architecture/tests, ships them, and interrupts him rarely. What
is missing is the Director's own place in that chain — it exists as prose (`skills/director/SKILL.md`)
but has no ticket model, no state machine, and no TEST_MATRIX coverage of its own decisions. This
contract defines that missing piece: the ticket, its states, its DOD, and who owns which part of
the lifecycle. It changes nothing about PRODUCT_SPEC/ARCHITECTURE/TEST_MATRIX's own existing
mechanics — it adds the Director/ticket layer as a new node in that same chain.

## Entities

**Ticket.** One row in `PLAN.md` (unchanged home — see Non-goals). A ticket carries:
- a goal, in the owner's own sense, one sentence
- a status (below)
- a Definition of Done (DOD): the specific, checkable conditions this ticket's own work must meet,
  written into the ticket at creation or at its next status change, never invented afterward to fit
  what shipped
- context pointers: file:line references into PRODUCT_SPEC, ARCHITECTURE, TEST_MATRIX, code and
  whatever prior check/verdict is relevant — never copied document text. A ticket that needs a
  paragraph from PRODUCT_SPEC cites `PRODUCT_SPEC.md:1834` (or a requirement/criterion id), not the
  paragraph.
- a history: who moved it through which status, and why, inline (matches PLAN.md's existing
  git-log-is-the-history convention — nothing new here)

**Checkpoint.** The saved, resumable state of one ticket's own work in progress: which context
pointers were already resolved, what the worker was told, what it produced so far. A new session
resuming a ticket reads its checkpoint and continues — it does not re-derive the ticket from
scratch or ask the owner to re-explain.

**Status.** Exhaustively four values, each with a hard trigger and a hard exit condition:

| Status | Entered when | Exits when | Who may set it |
|---|---|---|---|
| `queued` | Director accepts an instruction as work, or a ticket's blocker clears | a worker is assigned and begins | Director, or Code releasing a blocker |
| `in hand` | a worker (human-directed agent) begins the ticket's own work | DOD is met and delivered, or a genuine blocker is hit, or the owner halts it | Code, on worker assignment |
| `blocked` | continuing is *objectively* impossible right now: a technical limit, an external dependency, or one owner action with no substitute | the blocking condition is verified cleared (never assumed cleared) | Code, only with a named, checkable reason attached |
| `done` | the ticket's own DOD is verified true against the real repo/git state, not narrated | never (see re-open rule) | Code, only after DOD verification passes |

Queue order and a cap on parallel lanes are never `blocked` — they are scheduling, not
impossibility. `blocked` is rare by construction: most "can't do it now" cases are actually
`queued` behind something else, and the contract must not let that distinction blur. There is no
fifth status ("needs his eyes," "needs review," etc.) — a ticket needing the owner's word is
`blocked` with that reason named, or it is a question, which is not a ticket at all (see Director
below).

**Done, precisely.** A ticket's DOD includes only the conditions that actually apply to it, chosen
from this fixed menu at authoring time — never invented at closing time to match what happened:
- an observable result for the human (what changed that he can see or use)
- the real delivery location (a file, a URL, a running service — named, not implied)
- the checks that must pass (tests, a script, a manual read — named)
- delivery into git/main under this project's own push rules (already enforced by the existing
  guardrails chain — this contract does not re-invent that gate, it requires DOD to name it when
  it applies)
- independent acceptance of a worker's own output, when a worker did the work (someone other than
  the worker verifies the DOD — this session's own tonight's pattern: hostile review after landing)

`✅` (done) is forbidden in the ticket text until every applicable condition above is checked
against the real repository, not asserted. A ticket marked done whose DOD command later fails is a
contract violation, not a style issue — `plan_checks.py`'s existing acceptance-command pattern
already gives this a mechanical anchor; this contract requires every new ticket's DOD to be
expressible that way where a command exists, and to name a manual read where it does not.

**Re-opening.** A request to improve an already-delivered result opens the *old* ticket only if its
original DOD is shown to have been false (the delivery didn't actually meet what the ticket
claimed). Otherwise it is new work: a new ticket, even if it targets the same feature. This keeps a
ticket's own history honest — it never quietly grows scope after closing.

## Responsibilities, strictly separated

1. **Prompt/Director** (the main model reading the message, no separate model call per message —
   see Non-goals): classifies the act (the existing seven-act table in `skills/director/SKILL.md`
   is unchanged and is the classifier), and for an accepted instruction, names which
   spec/architecture/test-matrix areas it touches and which specialists it needs. Decides,
   proposes; touches no ticket state directly.
2. **Code** (a deterministic operation, not free-form file edits — see Non-goals): the only thing
   that writes ticket state. One call takes {ticket id or "new", target status, DOD-check result if
   moving to done, blocker reason if moving to blocked} and either applies it or refuses with a
   named reason (duplicate ticket, DOD not met, missing blocker reason). Owns checkpoint
   read/write, so a new session resuming a ticket gets the exact prior context, not a re-derivation.
3. **Product-prover**: reviews this very contract (and later, product contracts written under it)
   for completeness and internal contradiction against the existing spec/architecture — the gate
   this contract itself must pass before any code lands.
4. **Test-author**: once product-prover clears a contract, derives TEST_MATRIX rows and tests from
   it and from ARCHITECTURE — the existing test-author method, unchanged, now given the
   Director/ticket contract as one more thing it derives tests for.

## Director's two kinds of proof

Both live as TEST_MATRIX rows, under product-prover and test-author's existing method — never a
second, parallel test surface for Director alone.

**A. Live model-evals.** Run only when Director's own prompt, policy or underlying model changes
(not on every push). Real messages and real context, covering: a question, an instruction, a
correction, a decision, a halt, and at least one mixed/ambiguous message combining two acts in one
breath. A prior version's traces are never evidence for a changed version — the eval reruns live
against the version being shipped.

**B. Deterministic state-machine tests.** Take a Director decision as already given (mocked or
fixture-supplied — these tests do not re-test Director's own judgment, that's eval A's job) and
assert the mechanical consequence: a question changes no ticket; an accepted instruction creates
exactly one ticket with its context pointers and DOD populated; a correction changes the ticket
already in flight rather than opening a second one; a worker assigned to a ticket receives its
exact stored text (no paraphrase); a DOD-check failure blocks `done`; a DOD-check pass with real
delivery allows `done`; a new session given a ticket id resumes it from its checkpoint with the
same context pointers; a `blocked` ticket carries a specific, named reason, never a bare label.

## Non-goals — explicitly out of scope for this contract

- No second task database. `PLAN.md` stays the one plan, queue and full ticket text in one list;
  this contract adds fields and a state machine to that same file's own row shape, not a new store.
- No Board server, event log, background renderer, HTML automation pipeline, or standalone
  dashboard. A board, if ever built, is an optional, on-request *view* of PLAN.md's own state —
  never a second source of truth, never something kept running.
- No inbox or idea shelf as a persistent store. An idea the owner wants kept is a normal `queued`
  ticket with a goal and a DOD; anything else lives in the conversation transcript, not in a file.
- No per-message model call for Director. The main model already reads every message; it applies
  the Director's existing short contract inline. State changes go through Code's one deterministic
  operation — never free-form multi-file edits done "because the Director said so."
- No fifth status. `needs his eyes` does not exist; that shape is either `blocked` (owner action is
  the one thing unblocking it, named) or not a ticket at all (a live question, answered in chat).

## What this contract does not decide (left to the implementation packages)

The exact schema of a context pointer, the exact shape of the Code operation's interface, and the
worker-restoration mechanics beyond "checkpoint holds exact prior context" are implementation
choices for package 1/2 of the rollout, not this contract. This contract fixes the entities, the
state machine, the responsibility boundaries and the proof obligations; it does not fix file
formats.
