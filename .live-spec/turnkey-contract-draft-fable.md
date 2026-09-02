# Turnkey product contract — draft (Fable half), 2026-09-02

One of two independent drafts. Goes nowhere until it is composed with the other and passed to
product-prover. Source of every decision below: the owner's message saved at
`.live-spec/next-phase-prompt-turnkey-productization.md`. Sentences that go beyond that message
are marked *(derived)* so the prover and the composing pass can see where a decision was made
for him.

## 1. What this contract covers

The one person with an idea and taste speaks freely. The system reads what he did, and only an
instruction, a correction or a work-changing decision turns into work. Work is a ticket. A ticket
carries its own done. Code keeps the ticket's state, refuses the illegal moves, hands a worker the
ticket's exact text, and lets a new session resume it with no spoken recap. The owner is asked
rarely, and only when nothing else can move the work.

This contract covers: the Director's act reading as it feeds state; the ticket, its context
pointers and its done; the four statuses and their transitions; who may trigger each; the four
responsibilities; the two kinds of Director proof and where they live; and the non-goals. It does
not cover the rollout packages, the TEST_MATRIX revision or the TLV Photos pilot.

## 2. Entities

**Ticket.** One entry in `PLAN.md § Tasks` (`### <mark> <title> — id: <id>`). It is the only home
of a piece of accepted work. It holds, and holds only: the goal in the owner's words; the
observable outcome; the context pointers; the done; the status mark; and, while in hand, who holds
it. No estimate, no priority beyond `critical`, no prose that is not one of those fields *(derived:
the current task bodies carry history paragraphs; those stay for closed tasks and are not written
for new ones)*.

**Context pointer.** One exact address into a document that already exists: a spec code
(`R-nnn`, `INV-nnn`, `E-nnn`, `T-nnn`), an architecture node name, a matrix row id, a
`path:line`, a test name, a commit hash. A pointer is never a pasted copy of what it points at. A
ticket lists every pointer this work needs and no other; a worker brief is the ticket text, not the
documents behind it.

**Done (DOD).** The ticket's own list of the conditions that apply to it, each one checkable by a
command or by a named reader. The closed set of condition kinds, from his message: an observable
result for a person; the delivery target (which file, page, host, branch); the checks that must be
green; delivery to `origin/main` by the project's own push rules; independent acceptance when a
worker did the work. A ticket lists only the kinds that apply and says why an omitted kind does not
*(derived: the "why omitted" line, so an absent condition is a decision, not a gap)*. `✅` is
refused while any listed condition is unproven.

**Checkpoint.** The resume file under `.live-spec/checkpoints/` that a ticket in hand owns:
`DECISION SHEET`, `DONE`, `IN PROGRESS`, `NEXT`, `Status: open|closed`, exactly as
`scripts/checkpoint.py` already writes it. One ticket, one checkpoint, for the ticket's whole life.
A ticket that is `queued` has no checkpoint yet; a ticket that is `done` has a closed one.

**Status.** One of four: `queued` ⬜ · `in hand` 🔄 · `blocked` ⛔ · `done` ✅. The set is
closed. `👁️ needs his eyes` is retired (see §9).

**Verdict.** What the Director hands to code after reading a message: the acts it found, and at
most one state operation to run (§4). A verdict is the seam between proof A and proof B.

## 3. The four statuses, defined on real tickets

| Status | Means | Real example from `PLAN.md` |
|---|---|---|
| `queued` | Accepted into work: pointers resolve, done is written. Waiting only on order or on the parallelism cap. Not a blocker. | plan-9 today: dry run proven, the owner's own "after the release" is an ordering decision, so it is queued, not blocked. |
| `in hand` | One holder (session or worker) has it now and its checkpoint is open. | queue row 241 (archived) while its cloud worker held it: checkpoint `.live-spec/checkpoints/row241-worker.md`, briefed by `docs/briefs/2026-07-10-row241-guardrails-brief.md`. |
| `blocked` | Continuing is objectively impossible right now, for exactly one of three reasons, named on the ticket: a technical limit, an outside dependency, or one required owner action. | plan-9 on 27.08 morning: `install-external-skills.sh` failed against any host tree (technical limit). Unblocked the same morning by commit `8a076e76`. |
| `done` | Every done condition proven; the archive move by a person's hand follows the project's existing rule. | plan-2: `python3 evals/director/check.py --all` green on fresh traces, the command lives in `scripts/plan_checks.py`. |

What is **not** a blocker, with the ticket it came from: waiting behind another ticket in the queue
(plan-9 behind the release); a taste or wording choice the system can make with the ordinary
answer and mark `[default]` for him to retune (q-536's three wording calls would today be decided
and marked, not parked under 👁️); a worker that has not been assigned yet (that is `queued`).

Where the old 👁️ went: a decision only he can make, and without which the work cannot move, is
`blocked` with reason "one owner action: <the action>". A decision he *could* make but the work can
move without, is not a status at all — the system chooses the ordinary solution and says so
in one line, and the ticket stays `in hand`.

## 4. The state machine

Every transition is one deterministic operation on the ticket, run by code, with the Director's
verdict as input. Code never reads the message; the Director never edits a file. A transition
that fails validation leaves both `PLAN.md` and the checkpoint unchanged and prints the one
reason.

| # | From → To | Trigger (act) | Who may trigger | Code requires | What code does |
|---|---|---|---|---|---|
| T1 | — → `queued` | instruction, or a decision that changes no running work, or an idea he explicitly wants kept for later | Director | no open ticket with the same goal line or the same pointer set; goal, outcome, ≥1 pointer and a done list present | appends the ticket to `PLAN.md § Tasks` |
| T2 | `queued` → `in hand` | the holder takes it (a session starts it, or a worker is briefed) | Director, or the resume operation in a new session | holder named; lane cap not exceeded; no other open checkpoint for this id | opens the one checkpoint with the decision sheet |
| T3 | `in hand` → `in hand` | correction | Director | targets the id already in hand; a correction never creates a ticket | rewrites the checkpoint's decision sheet and `NEXT`, and the ticket's goal or done where the correction changed them |
| T4 | `in hand` → `blocked` | a fact from a worker, a check, or the owner | Director, or a worker through its report | reason is one of the three kinds and names the concrete thing (a command that fails, a dependency by name, an owner action by name) | writes the reason on the ticket and in `IN PROGRESS` |
| T5 | `blocked` → `in hand` | the named reason is gone (commit, reply, dependency) | Director | the reason line names what cleared it | clears the reason |
| T6 | `in hand` → `queued` | halt: park | Director | — | closes nothing; checkpoint stays open with `NEXT` = what remains, holder cleared |
| T7 | `in hand` → `done` | the done conditions are proven | Director, after the independent acceptor's verdict where a worker did the work | every done condition passes its command or names its reader and their verdict; `IN PROGRESS` and `NEXT` empty; delivery commit on `origin/main` where delivery is a condition | flips the checkpoint to closed and the mark to ✅ in the same step |
| T8 | `done` → `in hand` | the original done turned out false | Director | the ticket names which condition was false and the evidence | reopens the same id; never a copy |
| T9 | `in hand`/`queued` → archived | halt: abandon | a person's hand, by the existing archive rule | the halt's reason on the archive line | ticket leaves the list; nothing else changes |

Acts that run no operation: question, musing, observation without a beyond-doubt repair, decision
that changes no work, thank-you, an answer to the Director's own question. For these the verdict
carries `operation: none` and code is not called. A conversation stays in the transcript.

**Improvement after delivery.** A request to make a delivered result better runs T1 (a new
ticket) unless the Director can name the original done condition that was false, in which case it
runs T8. Code accepts T8 only with that condition named.

**Duplicate.** Code refuses T1 when an open ticket has the same goal line or the same pointer
set, and refuses T2 when the id already holds an open checkpoint. Semantic near-duplicates are the
Director's job (proof A), not code's *(derived: this is the honest limit of a deterministic check)*.

**Resume.** A new session runs the existing probe; the ticket `in hand` with an open checkpoint is
the resume point, and the session continues it (T2 with the same holder kind) without the owner
saying anything. If nothing is in hand, the top `queued` ticket is offered, not started.

## 5. When the owner is asked

The system asks him in exactly three situations, and otherwise decides and says what it decided:

1. **A block whose reason is one owner action** (T4, kind three): the ask names the one action.
2. **The Director cannot tell one result from two** — whether a message wants one deliverable or
   two, or whether a halt parks or abandons: one short question in his words, as the Director skill
   already rules.
3. **An irreversible step** the decision sheet's risk line names: deleting outside the repo,
   publishing outside, spending money *(derived from the sheet's existing "risk and
   irreversibility" line)*.

Everything else — a library, a layout, a default, a wording — is the ordinary solution, chosen,
marked `[default]` where the spec format already allows it, and said in one line.

## 6. Responsibilities, strictly

| Who | Does | Never does |
|---|---|---|
| **Director** (the main model, applying the skill's short contract inside its normal turn) | reads the act; names dimensions and specialists; writes the decision sheet; issues one verdict with at most one operation | calls a second model to read the message; edits `PLAN.md` or a checkpoint by hand; opens a second ticket for a correction |
| **Code** (`scripts/checkpoint.py`, `scripts/plan_checks.py`, `scripts/state-probe.sh`, extended, no new store) | stores and validates ticket and checkpoint state; refuses duplicates, refuses ✅ over a failed done, refuses close over open work; hands a worker the ticket's exact text and pointers; restores the in-hand ticket in a new session | reads meaning; classifies a message by wording or file path; picks what runs next by anything but the recorded states |
| **Product-prover** | proves this contract complete and consistent with the spec, the architecture and the skills as they stand, including every edge case in §4 and §5 | writes tests; edits the contract |
| **Test-author** | from the proven contract and the architecture derives the TEST_MATRIX rows of §7 and the tests behind them | invents a second test track; grades the Director's reading |

## 7. Two proofs for the Director, both as TEST_MATRIX rows

**A. Live model-evals** — `evals/director/` as it already stands: real messages with their
situation, a fresh producer that never sees the expected verdict, `check.py` as grader. What this
contract adds:

- the fixture set proves each of: question, instruction, correction, decision, halt, and a mixed
  turn — one fixture per kind at least, named in `scenarios.json`;
- every expected verdict carries the **operation** (§4) beside the acts, so the same fixture
  feeds proof B;
- traces count only when drawn after the last change to `skills/director/SKILL.md`, to its
  reference files, or to the model named in the run; `scripts/plan_checks.py`'s plan-2 command
  already compares trace time to skill time and is extended to the other two;
- the run is on demand, at those three changes, never per message and never on a timer.

**B. Deterministic state-machine tests** — take a verdict as input, never a message, and assert
on `PLAN.md` and the checkpoint file. Eight facts, one row each in `matrix/director.md`:

| Fact | Asserts |
|---|---|
| a question changes nothing | verdict `none` → both files byte-identical |
| an instruction opens exactly one ticket | T1 → one new entry with pointers and a done list; a second T1 with the same goal refused |
| a correction changes the ticket in hand | T3 → same id, sheet rewritten, ticket count unchanged |
| a worker gets the exact text | the brief handed out equals the ticket entry plus its checkpoint's `NEXT` |
| a failed done forbids ✅ | T7 with one failing condition → refused, mark unchanged |
| a proven done with delivery gives ✅ | T7 with all conditions green and the delivery commit on `origin/main` → ✅ and checkpoint closed in one step |
| a new session continues the same ticket | probe on a tree with one open checkpoint → that id, its holder, its `NEXT` |
| a real blocker names its cause | T4 without a concrete reason refused; with one → ⛔ and the reason on the ticket |

Test level: `browser-computed` for the rows a real git must compute (delivery, resume), `string`
for the rest, per the matrix's own ladder. Both proofs land in the existing `matrix/director.md`
block and the existing `## Reference`; no new directory, no new runner.

## 8. Non-goals

- No separate ROADMAP, task base, session plan or lane plan. `PLAN.md` is the one canon.
- No board server, event log, background render, HTML automation or standing board page. The
  board is `scripts/render-board.sh` run on an explicit request and nothing more.
- No inbox for the owner's thoughts, no idea shelf. "Keep this for later" is T1; everything else
  is the transcript. *(Scope: the cross-agent `inbox/` door of `matrix/inbox.md` is neither
  created nor retired by this contract.)*
- No per-message Director model call, no conduct judge on the reading, no timer.
- No fifth status. No `needs his eyes`, no `cancelled` (abandon is the archive move, T9).
- No new counter, threshold or size in this contract. The lane cap is the profile's existing one.

## 9. What this contract changes in documents that already exist

Listed so the prover can check for contradiction, not so anyone edits them now.

| Where | Today | Under this contract |
|---|---|---|
| `spec/message-first-read.md` R315, E-37, INV-320 | an idea shelf keeps ideas in his words | retire: an idea stays in the transcript or becomes a `queued` ticket on his explicit word |
| R313 crit 4–5 | work starts on instruction, correction, work-changing decision; questions open nothing | unchanged; B's first two rows are its tests |
| R314 crit 6–7, INV-319 | five states, "needs the person's eyes" among them | sharpen: four states |
| `PLAN.md § Words used here` | five marks | four marks; the 👁️ sentence retired |
| `scripts/state-probe.sh` | a 👁️ bucket ranks first | bucket removed; ⛔ carries the owner-action case with its reason printed |
| `skills/director/SKILL.md` acts table, "Idea for later" row | put it on the idea shelf | say it was heard; open a ticket only on his explicit "keep it" |
| `skills/director/SKILL.md` § Execution | opens/updates/closes the checkpoint by three commands | the same three, plus the ticket-side operations of §4, all under one entry point *(derived: one command with sub-operations is the smallest change to what exists)* |
| R309, `matrix/work-board.md`, q-166 | standing live board page, specified and unbuilt | sharpen to on-demand render; q-166's "live" leg falls out of scope |
| `evals/director/scenarios.json` `expect` block | `acts`, `creates_work`, `work_items`, the shelf and attach fields, dimensions and specialists by inclusion | the shelf field retired; `operation` (§4) added, graded exactly |

## 10. Questions the prover should settle

1. Is "same goal line or same pointer set" a sufficient duplicate gate, or does an open ticket
   whose pointers merely overlap need the Director's confirmation before T1?
2. T6 (park) leaves the checkpoint open with no holder; a second park of another ticket makes two
   open checkpoints with none in hand. Does the resume rule (§4) pick the most recently touched, or
   ask?
3. A worker's `blocked` report (T4) reaches code through the Director. Is a worker allowed to run
   T4 directly, and if so what stops it from parking work that merely got hard?
4. Delivery to `origin/main` is a done condition; the push gate runs after ✅ would be written.
   Order: T7 runs only after the push, so the mark is written on a tree that already carries the
   delivery — confirm that this does not deadlock with the gate that checks the mark.
