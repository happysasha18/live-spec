# Turnkey product contract — composed, 2026-09-02

Composed from two independent drafts (`turnkey-contract-draft-fable.md`,
`turnkey-contract-draft-orchestrator.md`), per the owner's word of 09:12. Source of every decision:
the owner's message at `.live-spec/next-phase-prompt-turnkey-productization.md`. A sentence that
goes beyond that message is marked *(derived)*. §11 lists where the drafts disagreed and what was
kept.

**Reviewed by product-prover twice, 2026-09-02.** First pass (orchestrator's own,
`docs/prover/2026-09-02-turnkey-contract-review.md`): three defects folded. The owner then reversed
the Requirement-309 retirement one of those defects had proposed (12:46: keep and build it, don't
retire it, past the auto-refresh heartbeat) and added the far-tier tag. A second, independent pass
(Fable's own reading, per the owner's routing preference,
`docs/prover/2026-09-02-turnkey-contract-review-fable.md`) then found twelve further defects and
three recommendations — a real fresh-eyes catch on the first pass's own fixes (F1/F3, the
checkpoint-timing fold, turned out heavier than needed) and on the reversal (F10, under-scoped).
All fifteen are folded in place below, marked by finding id. One open item remains: whether a
ticket carries a time estimate (§10) — the owner's word, not a defect. Ready for test-author once
that one answer lands.

## 1. What this contract covers

One person with an idea and taste speaks freely. The system reads what he did; only an
instruction, a correction, or a work-changing decision becomes work. Work is a ticket. A ticket
carries its own done. Code keeps the ticket's state, refuses the illegal moves, hands a worker the
ticket's exact text, and lets a new session resume it with no spoken recap. The owner is asked
rarely, and only when nothing else moves the work.

Covered: the Director's reading as it feeds state; the ticket, its pointers and its done; four
statuses and their transitions; who triggers each; four responsibilities; two Director proofs and
where they live; non-goals. Not covered: the rollout packages, the TEST_MATRIX revision, the TLV
Photos pilot, and the exact command-line shape of the code operation — package 2 fixes that
against the scripts named here.

## 2. Entities

**Ticket.** One entry in `PLAN.md § Tasks` (`### <mark> <title> — id: <id>`), the only home of a
piece of accepted work. It holds, and holds only: the goal in the owner's words; the observable
outcome; the context pointers; the done; the status mark; while in hand, the holder; while
blocked, the reason. No estimate, no priority beyond the existing `critical`. Its history is
`git log PLAN.md`, as the plan already rules — no inline log *(derived: closed tasks keep the
history paragraphs they have; new tickets are not written that way)*.

**The ticket is the unit — the owner's word, 2026-09-02 14:24.** Its `<title>` must say plainly
what the work is about, on its own, with no lookup required — descriptive prose, never a
paraphrase-proof code standing in for meaning. Anyone talking about a ticket, in chat or in a
report, leads with that title; the `id` trails in parentheses for the record, the same shape this
project's own plain-language rule already asks of every technical term. This is also the DOD's
own reading test: a ticket whose title, goal and outcome are legible on their own is auditable by
a person who has never opened the pointers behind it; one that reads as a code plus a link is not
yet a real unit, whatever box its DOD checks off.

**Context pointer.** One exact address into a document that exists: a spec code (`R-nnn`,
`INV-nnn`, `E-nnn`, `T-nnn`), an architecture node name, a matrix row id, a `path:line`, a test
name, a commit hash. Never a pasted copy. A ticket lists every pointer this work needs and no
other; the worker's brief is the ticket text, not the documents behind it.

**Done (DOD).** The ticket's own list of the conditions that apply to it, each checkable by a
command or by a named reader. The closed menu, from his message: an observable result for a
person; the delivery target (file, page, host, branch — named; when the target repository isn't
this one, the condition names that repository and is proven by its own probe, never this one's —
Fable's F15, since e.g. `plan-9`'s delivery is into `~/tlvphotos`, which this window cannot write);
the checks that must be green (named); delivery to `origin/main` under the project's own push
rules — or, for the same ticket, in the same push as the commit carrying its own ✅ mark (Fable's
F13: requiring a strictly separate, later push per ticket costs a full ~20-minute gate re-run per
close with nothing it actually protects, since no push gate reads a task mark today); independent
acceptance when a worker did the work, its verdict landing as one line in the checkpoint's `DONE`
section — `accepted by <who>: <what was checked>` — which T7 requires present for every
reader-judged condition before it can pass (Fable's F9: a condition only a reader can judge needs
somewhere code can actually read "yes, checked" rather than passing every ticket on sight or none).
A ticket lists only the kinds that apply and says in one line why an omitted kind does not
*(derived)*. The done is written when the ticket opens, may be sharpened by a correction, and is
never written or reworded at closing to fit what shipped. Where a command can decide a condition,
the condition is that command, in `scripts/plan_checks.py` as today; a ✅ whose command later fails
is already flipped to ⛔ by `scripts/state-probe.sh` and stays a contract violation, not a style
note.

**Checkpoint.** The resume file under `.live-spec/checkpoints/` a ticket owns from the moment it has
a holder: `DECISION SHEET`, `DONE`, `IN PROGRESS`, `NEXT`, `Status: open|closed`, exactly as
`scripts/checkpoint.py` writes it today. One ticket, one checkpoint, for life — opened at T2, when
a holder is actually named. `queued` has none yet, so `PLAN.md`'s own entry is the whole of a
queued ticket's statement (goal, outcome, pointers, done — one home, never copied into a sheet that
doesn't exist yet). An instruction accepted right now runs T1 and T2 as one operation, which is
exactly the skill's own "opens a checkpoint before the first specialist is called" sentence for the
immediate case; an idea he explicitly wants kept runs T1 alone, with no checkpoint until a holder
takes it later *(the composing pass first wrote checkpoint-at-T1 for every queued ticket to match
that same skill sentence — product-prover's F1 — but a fresh independent pass, Fable's, found that
reading created five open, holder-less checkpoints for five queued tickets with no format field to
tell them apart, and the lighter fix below removes the problem instead of patching around it:
2026-09-02, docs/prover/2026-09-02-turnkey-contract-review-fable.md F1/F3)*. `done` has a closed
one. A new session reads whichever exists — the checkpoint if one is open, the `PLAN.md` entry
otherwise — and continues; it never re-derives the ticket or asks the owner to re-explain **— which
requires the checkpoint actually be in git.** `.gitignore` line 1 today is
`.live-spec/checkpoints/`; the five checkpoints tracked now predate that line, and every one T1/T2
opens from here on stays on one machine (Fable's F2, checked live: `git check-ignore` confirms it).
A resume on a second machine, a cloud seat, or after a lost tree (this project has already lost one
— `PLAN.md` law 9) reads a "missing checkpoint" as the contract's own data-fault case for a ticket
that's actually healthy. Fixed the same session this was found: dropped the ignore line, ignoring
`wind-down-*.md` by name instead, since that's the only thing under that directory meant to stay
local scratch.

**Status.** Four, closed set: `queued` ⬜ · `in hand` 🔄 · `blocked` ⛔ · `done` ✅. `👁️ needs his
eyes` is retired (§3, §9).

**Verdict.** What the Director hands to code after reading a message: the acts found, and zero or
more state operations, one per act that changes state, each naming its ticket id (a mixed turn —
"stop X, do Y instead" — is a real T6 plus a real T1 in one verdict; a pure question's list is
empty) *(the composing pass first wrote "at most one operation," which cannot grade this project's
own mixed-turn eval fixtures — Fable's F5)*. The verdict is the seam between proof A and proof B.

## 3. The four statuses, on real tickets

| Status | Means | Real example from `PLAN.md` |
|---|---|---|
| `queued` | Accepted into work: pointers resolve, done is written. Waiting only on order or the lane cap — scheduling, not impossibility. | plan-9 today: dry run proven; the owner's "after the release" is an ordering decision, so queued, not blocked. |
| `in hand` | One holder (session or worker) has it now; its checkpoint is open. | queue row 241 (archived) while its cloud worker held it: `.live-spec/checkpoints/row241-worker.md`, brief `docs/briefs/2026-07-10-row241-guardrails-brief.md`. |
| `blocked` | Continuing is objectively impossible now, for exactly one of three named reasons: a technical limit, an outside dependency, one required owner action. Rare by construction. | plan-9 on 27.08 morning: `install-external-skills.sh` failed against any host tree. Cleared the same morning by `8a076e76`. |
| `done` | Every done condition proven against the real tree and git, not narrated. The archive move by a person's hand follows the plan's existing rule. | plan-2: `python3 evals/director/check.py --all` green on fresh traces; the command lives in `scripts/plan_checks.py`. |

Not a blocker, with the ticket it came from: waiting behind another ticket (plan-9 behind the
release); no worker assigned yet (`queued`); a taste or wording choice the system can make with the
ordinary answer and mark `[default]` for him to retune (q-536's three wording calls would today be
decided and marked, not parked under 👁️).

Where 👁️ went: a decision only he can make, without which the work cannot move, is `blocked` with
"one owner action: <the action>". A decision he *could* make but the work moves without is no
status: the system picks the ordinary solution, says so in one line, and stays `in hand`. A live
question is answered in chat and is not a ticket.

**The far tier, added on the owner's word (2026-09-02 12:35).** A `queued` ticket may carry one
display tag so the on-request board (§8) groups it apart from the runnable head — so a thing worth
keeping doesn't get lost, without inventing a second store. Named the **far tier**, not "someday":
the spec already owns this exact category — `Requirement 94`'s "a far tier the runnable report
stands down by name," `Requirement 239`'s rare surfacing, `Requirement 309` criterion 23 keeping it
off the board by that name — and a new word for the same thing is the one-term-one-fact rule's own
violation (`PLAN.md § Words used here`; Fable's F11). It is still an ordinary T1 ticket: same
duplicate check, same goal/pointers/done shape, same dedup rule as every other `queued` row. The
tag changes nothing about the state machine — it is metadata Code reads when rendering the board,
not a fifth status and not a shelf.

## 4. The state machine

Every transition is one deterministic operation on the ticket, run by code, with the Director's
verdict as input. Code never reads the message; the Director never edits `PLAN.md` or a checkpoint
by hand. A transition that fails validation leaves both files unchanged and prints the one reason
(duplicate, done not met, no blocker reason, open work at close).

| # | From → To | Trigger (act) | Who triggers | Code requires | Code writes |
|---|---|---|---|---|---|
| T1 | — → `queued` | instruction; a decision changing no running work; an idea he explicitly wants kept | Director | no open ticket with the same goal line (Fable's F14: pointer overlap alone never refuses — q-436/q-437 share every pointer and are both real) | the entry in `PLAN.md § Tasks` |
| T2 | `queued` → `in hand` | a holder takes it: the session starts it, or a worker is briefed | Director, or the resume operation in a new session | holder named; lane cap not exceeded; no checkpoint already open for this id | the one checkpoint, with the decision sheet restating the entry's goal and outcome (the entry stays their one source) |
| T3 | `in hand` or `queued` → same status | correction | Director | targets an id that exists; never creates a ticket | `in hand`: decision sheet and `NEXT`, plus the entry's goal/done where changed. `queued`: the entry's goal/done rewritten in place, no checkpoint touched (Fable's F6: a correction on a queued ticket — e.g. its dependency vanishing before anyone takes it, as `plan-9`'s installer fix did — has to land somewhere) |
| T4 | `in hand` or `queued` → `blocked` | a fact from a worker's report, a check, or the owner | Director | reason of one of the three kinds, naming the concrete thing: the failing command, the dependency, the owner action | reason on the ticket, and in `IN PROGRESS` where a checkpoint is open (Fable's F6: a queued ticket can go bad before anyone takes it) |
| T5 | `blocked` → `queued` or `in hand` | the named reason is verifiably gone | Director | a line naming what cleared it (commit, reply, dependency), never "assumed cleared" | clears the reason; lands `in hand` if the ticket still names a holder, `queued` otherwise (Fable's F6: a block can clear with nobody holding the ticket) |
| T6 | `in hand` → `queued` | halt: park | Director | — | holder cleared; checkpoint stays open with `NEXT` = what remains |
| T7 | `in hand` → `done` | done conditions proven | Director, after the independent acceptor's verdict where a worker did the work | every condition passes its command or names its reader and verdict (a reader-judged one, e.g. independent acceptance, needs a `DONE`-section line first — see Done below, Fable's F9); `IN PROGRESS` and `NEXT` empty; the delivery commit on `origin/main`, or in the same push as the mark (Fable's F13), where delivery is a condition | checkpoint closed, then the `PLAN.md` mark set to ✅ — two file writes, not one; T7 run again on a ticket whose checkpoint is already closed is a no-op that only (re)writes the mark, never an error (Fable's F4: this is the whole crash-recovery rule — a crash between the two writes leaves a closed checkpoint and a stale mark, and re-running T7 finishes it) |
| T8 | `done` → `in hand` (`queued` if no holder is named) | the original done turned out false | Director | the false condition named, with evidence; the ticket is still in `PLAN.md § Tasks` (a done ticket already moved to the archive is not this transition's business — see below, Fable's F8) | reopens the same id; never a copy |
| T9 | `in hand`/`queued` → archived | halt: abandon | a person's hand, by the existing archive rule | the halt's reason on the archive line | ticket leaves the list; its checkpoint's `IN PROGRESS`/`NEXT` are cleared with that reason as their last line and it closes in the same step (Fable's F7: an abandoned ticket must not leave an orphaned open checkpoint) |

Acts that run no operation: question, musing, observation without a beyond-doubt repair, decision
changing no work, thank-you, an answer to the Director's own question. The verdict carries
`operation: none`; code is not called; the conversation stays in the transcript.

**Improvement after delivery** runs T1 unless the Director names the original done condition that
was false and the ticket is still in `PLAN.md § Tasks`, in which case T8. Where the ticket already
moved to the month's archive, T8 has nothing to reopen (Fable's F8) — that improvement is T1,
citing the archived id and its archive line as pointers, its goal stating plainly that the original
done was false. One rule fewer than reopening from the archive, and the pointer kinds already carry
it. Code accepts T8 only with the false condition named, and only against a `PLAN.md § Tasks`
entry.

**Duplicate.** Code refuses T1 on the same goal line alone; sharing every pointer with an existing
ticket is printed as a note for the Director to read, never a mechanical refusal (Fable's F14:
two real, separate bugs on one requirement — q-436, q-437 — cite the same sources, and a gate
built for copies must not catch siblings). Code refuses T2 on an id that already holds an open
checkpoint. Semantic near-duplicates past the goal-line match are the Director's job, proved by A
*(derived: the honest limit of a deterministic check)*.

**Recovering a half-closed ticket (Fable's F4).** T7's own two writes — checkpoint closed, then the
`PLAN.md` mark set — are not atomic. A crash between them leaves a closed checkpoint on a ticket
still marked 🔄. This is not a fault needing a hand repair or a new alarm: running T7 again on a
ticket whose checkpoint is already closed is a no-op except for writing the mark, and that is the
whole recovery. Code never edits by hand; it just runs the same operation again.

**Resume.** A new session runs `scripts/state-probe.sh`; the ticket in hand with an open
checkpoint is the resume point and the session continues it (T2 with the same holder kind) with
its exact pointers and `NEXT`, the owner saying nothing. Given a ticket id explicitly, the same.
Nothing in hand: the top `queued` ticket is offered, not started — by `PLAN.md`'s own existing
order, never by which checkpoint was touched most recently (product-prover's answer to §10 Q2:
this project tracks queue position, not a last-touched time, so recency is not a signal available
to read), and the offer skips the far tier the same way `Requirement 94`'s own runnable report
already does (Fable's F11).

## 5. When the owner is asked

Three situations; otherwise the system decides and says what it decided:

1. **A block whose reason is one owner action** (T4, kind three): the ask names that action.
2. **One result or two** — the Director cannot tell whether a message wants one deliverable or
   two, or whether a halt parks or abandons: one short question in his words, as the Director
   skill already rules.
3. **An irreversible step** the decision sheet's risk line names: deleting outside the repo,
   publishing outside, spending money *(derived from the sheet's existing risk line)*.

Everything else — a library, a layout, a default, a wording — is the ordinary solution, chosen,
marked `[default]` where the spec format allows, and said in one line.

## 6. Responsibilities, strictly

| Who | Does | Never does |
|---|---|---|
| **Director** — the main model applying the skill's short contract inside its normal turn; the seven-act table in `skills/director/SKILL.md` is the classifier, unchanged | reads the act; names dimensions and specialists; writes the decision sheet; issues one verdict carrying zero or more operations, one per state-changing act (Fable's F5) | calls a second model to read the message; edits `PLAN.md` or a checkpoint by hand; opens a second ticket for a correction |
| **Code** — `scripts/checkpoint.py`, `scripts/plan_checks.py`, `scripts/state-probe.sh`, extended; no new store | the only writer of ticket and checkpoint state; refuses duplicates, ✅ over a failed done, close over open work, `blocked` without a reason, T4 whose reason restates difficulty rather than naming one of the three kinds (product-prover's answer to §10 Q3: a worker never triggers T4 itself — it reports a fact, and only a named technical limit, dependency, or owner action passes Code's own gate); hands a worker the ticket's exact stored text and pointers; restores the in-hand ticket in a new session | reads meaning; classifies by wording or file path; orders work by anything but the recorded states |
| **Product-prover** | proves this contract complete and consistent with the spec, architecture and skills as they stand, including the edge cases of §4–§5 | writes tests; edits the contract |
| **Test-author** | from the proven contract and the architecture derives the TEST_MATRIX rows of §7 and their tests, by its existing method | invents a second test track; grades the Director's reading |

## 7. Two proofs for the Director, both as TEST_MATRIX rows

The Director already stands as a node in `architecture/pipeline-and-lanes.md` and an 8-row block
in `matrix/director.md`; both proofs extend that block and the generated `## Reference`. No new
directory, runner, or test surface.

**A. Live model-evals** — `evals/director/` as it stands: real messages with their situation, a
fresh producer that never sees the expected verdict, `check.py` as grader. Added:

- at least one fixture each for question, instruction, correction, decision, halt, and a mixed
  turn carrying two acts in one breath, named in `scenarios.json`;
- every expected verdict carries the **operation** (§4) beside the acts, graded exactly, so the
  same fixture feeds B;
- traces count only when drawn after the last change to `skills/director/SKILL.md`, its
  `references/`, or the model named in the run; plan-2's command in `scripts/plan_checks.py`
  already compares trace time to skill time and is extended to the other two — which needs one new
  field first: today's traces carry a `skill_version` and no model id at all (Fable's F12), so the
  producer writes one `model` field per trace and the command compares it to the model the run is
  actually configured with, or the "model named in the run" freshness rule reads nothing to check;
- runs on those three changes only — never per message, never per push, never on a timer.

**B. Deterministic state-machine tests** — take a verdict as input, never a message, and assert on
`PLAN.md` and the checkpoint file. Eight facts, one row each:

| Fact | Asserts |
|---|---|
| a question changes nothing | verdict `none` → both files byte-identical |
| an instruction opens exactly one ticket | T1 → one new entry with pointers and a done list; a second T1 with the same goal refused |
| a correction changes the ticket in hand | T3 → same id, sheet rewritten, ticket count unchanged |
| a worker gets the exact text | the brief handed out equals the ticket entry plus its checkpoint's `NEXT`, no paraphrase |
| a failed done forbids ✅ | T7 with one failing condition → refused, mark unchanged |
| a proven done with delivery gives ✅ | T7 all green, delivery commit on `origin/main` (or the same push) → checkpoint closed, then ✅; re-running T7 on an already-closed checkpoint only (re)writes ✅ and changes nothing else (Fable's F4) |
| a new session continues the same ticket | probe on a tree with one open checkpoint → that id, holder, pointers, `NEXT` |
| a real blocker names its cause | T4 without a concrete reason refused; with one → ⛔ and the reason on the ticket |

Level per the matrix's own ladder: `browser-computed` where a real git must compute (delivery,
resume), `string` for the rest.

## 8. Non-goals

- No separate ROADMAP, task base, session plan or lane plan. `PLAN.md` is the one canon; this
  contract adds fields and a state machine to its existing entry shape, not a store.
- No board *server*, event log, or standing background process. **Reversed in part, owner's word
  2026-09-02 12:46:** the board is still never a second source of truth — it renders `PLAN.md`'s
  own Canon and nothing else — but the fuller board (`Requirement 309`, worker lanes, per-task
  chips, context pointers shown per row) is scheduled to be *built*, not retired, right after
  package 2 (the vertical path). The one piece actually cut is the periodic auto-refresh heartbeat
  (`matrix/work-board.md` M-540/M-542's "re-reads itself about every five seconds") — removed
  wherever it's promised, including the spec text once package 2 lands. A generated page a person
  opens on request is not a "server," so this does not reopen the no-server rule above; it reopens
  only the earlier draft's mistaken retirement of `Requirement 309` itself (see §9).
  **Added to this same future scope, owner's word 2026-09-02 13:14:** the board and the Canon
  should make it visible which open tickets can run side by side without colliding, and name a
  worktree for each so a session doesn't have to work that out by hand every time. This is not a
  new stored field to keep in sync by hand — it's the same judgment
  `skills/director/SKILL.md`'s Execution section already states in prose ("independent when
  neither depends on the other's output and neither rewrites the same section or behaviour"),
  computed live from the context pointers package 2 puts on every ticket, the same way
  `state-probe.sh` already computes a done mark's real status from its command rather than
  trusting the stored character. Two open tickets whose pointer sets don't overlap render as a
  pair (with a suggested `lane/<id>` name apiece); an overlap renders as a warning, never a
  silent grouping. This needs package 2's pointers to exist to be real rather than guessed from
  prose, so it lands with the board work, not before it.
- No inbox for the owner's thoughts, no idea shelf. "Keep this for later" is T1; everything else is
  the transcript. *(Scope: the cross-agent `inbox/` door of `matrix/inbox.md` is neither created
  nor retired here.)*
- No per-message Director model call, no conduct judge on the reading, no timer.
- No fifth status: no `needs his eyes`, no `needs review`, no `cancelled` (abandon is T9).
- No new counter, threshold or size. The lane cap is the profile's existing one.

## 9. What this contract changes in documents that already exist

For the prover's contradiction check, not for editing now.

| Where | Today | Under this contract |
|---|---|---|
| `spec/message-first-read.md` R315, E-37, INV-320 | an idea shelf keeps ideas in his words | retire: an idea stays in the transcript or becomes `queued` on his explicit word |
| R313 crit 4–5 | work starts on instruction, correction, work-changing decision; questions open nothing | unchanged; B's first two rows are its tests |
| R314 crit 6–7, INV-319 | five states, "needs the person's eyes" among them | sharpen: four states |
| `PLAN.md § Words used here` | five marks | four; the 👁️ sentence retired |
| `scripts/state-probe.sh` | a 👁️ bucket ranks first | bucket removed; ⛔ carries the owner-action case with its reason printed |
| `skills/director/SKILL.md` acts table, "Idea for later" row | put it on the idea shelf | say it was heard; open a ticket only on his explicit "keep it" |
| `skills/director/SKILL.md` § Execution | opens/updates/closes the checkpoint by three commands | the same three plus the ticket-side operations of §4, under one entry point *(derived: smallest change to what exists)* |
| R309 crit 7, 42 (its own task-statement source file) | "one source file in the host's tree... keyed by the queue row's id" | sharpen, don't build as written: it is a second task store, against §8's one-canon rule. The source file is `PLAN.md` itself; the "statement" is the ticket entry. |
| R309 crit 41, 49, 61–66 (a time estimate, frozen at take-up, settled against actual at close) | every task carries one | **owner's word needed (Fable's F10/§Phase-5-Q1) — not settled by this pass:** R309 says yes; §2's "no estimate" was only ever a `(derived)` guess with no basis in his message. If yes: the estimate is a ticket field, written at T1, frozen at T2, and crit 61–62 already state that freezing rule. If no: these criteria retire by the q-805 pattern, his word as the reason. |
| R309 crit 25, 45, 55 (statuses `ready`, `deferred`; columns awaiting-validation / ready / in-work / done) | two statuses beyond this contract's four | sharpen: `ready` is `queued` with its done already written; "awaiting validation" is "not yet a ticket" (T1 hasn't run); `deferred` is the far tier, not a fifth status |
| R309 crit 14, 86 (the board stands whether or not anyone asks; updates at every stage change, take-up, and a worker's spawn/finish) | a standing, self-updating page | sharpen, not cut: the state operation re-renders the board file as its own last step on every transition — no timer, no background process, `scripts/render-board.sh` and `tests/test_board_matches_the_canon.py` already do exactly this |
| R309 crit 88, 90, 96; `matrix/work-board.md` M-540, M-542 (a ~5-second heartbeat refresh; INV-312/INV-313) | a periodic auto-refresh loop | **retire, owner's word 2026-09-02 12:46** — the one piece actually cut. `INV-313` goes to `tests/test_formal_index.py`'s `EXPECTED_GAPS` with its reason, the q-805 shape; `INV-312` is *sharpened*, not emptied, since crit 86 (kept, above) cites it too — M-540 keeps "delays that stage not at all" and drops only the heartbeat clause; M-542 splits into its still-true half (empty/broken-board wording) and its retired half (the 5-second re-read) |
| the rest of `matrix/work-board.md` (M-519–M-539, M-541, M-543–M-544) and q-166 | 20 `*todo*` facts | kept, not retired. Scheduled to build after package 2 (owner's word 2026-09-02 12:46) |
| `evals/director/scenarios.json` `expect` block | `acts`, `creates_work`, `work_items`, the shelf and attach fields, dimensions and specialists by inclusion | the shelf field retired; `operation` added, graded exactly |

## 10. Questions settled, and the one left

The four questions this section originally asked (duplicate-gate strength, resume order on two
parked tickets, whether a worker can trigger a block directly, the push/mark ordering) were all
answered by product-prover's first pass and are folded in place above (§4 Duplicate, §4 Resume,
§6 Code, §2 Done) — none reopened by the second, independent pass.

**One question only the owner can answer, raised by that second pass (Fable's F10):** does a
ticket carry a time estimate? `Requirement 309` says yes and settles it against the actual at
close; the owner's 2026-09-02 message never mentions one; §2's "no estimate" line was only ever a
guess with no basis in his words. See §9's R309-estimate row for both answers' consequences.

## 11. Points of divergence between the two drafts, resolved

| Point | Fable draft | Orchestrator draft | Kept, and why |
|---|---|---|---|
| Ticket history | git log only, no inline prose on new tickets | an inline "who moved it, why" history, said to match the git-log convention | Git log. `PLAN.md § One plan` already rules every edit goes to git with a reason; an inline log would be a second home for the same fact. The blocked reason and the false-done condition are the only inline state lines. |
| When the done is written | implied at T1 | explicit: at creation or next status change, never invented at closing | Folded in (§2): at T1, sharpened only by T3, never at T7. A real constraint the Fable draft left implicit. |
| Clearing a block | "the reason is gone" | "verified cleared, never assumed cleared" | Folded in as T5's requirement: a line naming what cleared it. |
| Who triggers a move | Director (or resume) triggers; code validates and writes | table lists Code as the setter of `in hand`, `blocked`, `done` | Director triggers, code is the only writer — which the orchestrator's own responsibilities section also says; its status table conflated trigger with writer. |
| Owner's word needed | three outcomes: blocked-with-action, live question, or the ordinary answer marked `[default]` | two: blocked or a question | Three. His message says the system "chooses ordinary solutions"; the `[default]` marker already exists in the spec format, so the third path costs nothing new. |
| Director's place in the chain | extends the existing node and 8-row matrix block | "a new node in that same chain" | Existing. `architecture/pipeline-and-lanes.md` carries `### node: director` and `matrix/director.md` has 8 rows (plan-12's own check greps both). Adding a node would trigger a re-prove the architecture says only a new node earns. |
| Pointer schema and code interface | pointer kinds fixed to the existing code vocabulary; scripts named, no new store | left to packages 1–2 | Split: pointer kinds and the no-new-store constraint stay (they are cheap and testable now); the command-line shape of the operation goes to package 2, as the orchestrator said. |
| Fifth-status names | `needs his eyes`, `cancelled` | `needs his eyes`, `needs review` | All three named in §8. |
| Real examples per status | one per status from `PLAN.md` | none | Kept. His message asks statuses be defined on real examples before implementation. |
| §9 delta table, §10 prover questions | present | absent | Kept, per the coordinator's instruction. |
