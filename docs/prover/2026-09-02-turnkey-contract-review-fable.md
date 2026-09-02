# Prover record — 2026-09-02 turnkey-contract-review-fable

Prover skill version: product-prover 4.3.0, with product-prover-pack bindings (live-spec-base 6.1.0).
Mode: FULL, on a product contract, not a push. No `Range:` is owed.
Independent of `docs/prover/2026-09-02-turnkey-contract-review.md` (the orchestrator's pass); its
three folds F1–F3 are re-examined below under their own numbers, not reused.

Files read: `.live-spec/turnkey-contract-composed.md` (whole, as of 12:51); `skills/director/SKILL.md`
(Execution section); `scripts/checkpoint.py` (`new_checkpoint`, `validate_checkpoint`,
`close_checkpoint`); `scripts/state-probe.sh` (mark computation, lines 35–184);
`scripts/plan_checks.py` (plan-2 key); `spec/message-first-read.md` R313–R315;
`spec/work-board.md` R309 criteria 7, 14, 23–25, 41–66, 70, 86–96; `matrix/work-board.md` M-540,
M-542; `spec/queue-intake-priority.md` R94; `spec/live-status-reporting.md` R239;
`evals/director/traces/correction-shouted-constraint.json` (field set); `.gitignore`;
`scripts/director-wire-report.py` (lines 17–28); `scripts/wind-down.py` (lines 25–28, 211–245);
`PLAN.md` q-805 (lines 1834–1900).

Checks run: `git ls-files .live-spec/checkpoints | wc -l` → 5; `git check-ignore -v` on a tracked
checkpoint → not ignored (tracked before the ignore line); `grep -c '^| M-' matrix/work-board.md`
→ 26; `grep -rln checkpoints guardrails/ scripts/ hooks/ tests/` → the readers named above;
`grep -n PLAN.md guardrails/pre-push` → no gate reads a task mark at push.

Findings: fifteen — twelve defects, three recommendations. Listed below with a fold column at the
end for the orchestrator, who folds; this pass edits the contract nowhere.

Blocking: F1, F2, F4, F5, F6, F10 stand until folded; the rest are defects that fold in one
sentence each or recommendations.

---

## Triage

`TRIAGE: PROCEED` — a state machine with entities, transitions, actors and proof obligations; the
paired spec, architecture and scripts are in reach, so claims about the shipped system are
checked against them, not against the contract's prose.

## Opening assessment

The contract says how a spoken message becomes one ticket in `PLAN.md`, how code keeps that
ticket honest through four statuses, and how the Director's reading is proved twice. Two things
work: every status is anchored to a real ticket the project has already lived through, and §9
lists every existing sentence the contract contradicts, so this review could check contradiction
against named lines instead of guessing. Two things need attention before test-author touches
it. First, the resume story rests on a file git never carries — `.live-spec/checkpoints/` is
ignored — so "a new session continues the same ticket" is true on one laptop only. Second, the
board reversal was folded as "keep everything but the five-second refresh", but Requirement 309
as written also promises its own task store, a per-task estimate, two extra statuses, and a
board that stands unasked; each of those collides with a rule the contract states elsewhere, and
§8/§9 name none of them. Confidence: needs another iteration — none of the fixes is large, but
three of them change what test-author would derive rows from.

## Phase 1 — the model

Entities and relationships:
- Ticket: one `### … — id:` entry in `PLAN.md § Tasks`; owns one Checkpoint (after F1-fold, from
  T1); carries goal, outcome, pointers, done list, mark, holder (while in hand), reason (while
  blocked), and — added 12:35 — an optional `someday` tag.
- Checkpoint: one file under `.live-spec/checkpoints/`; sections DECISION SHEET, DONE, IN
  PROGRESS, NEXT; `Status: open|closed`; `Owner:` header. No holder field exists in the format
  today (inferred: the contract needs one).
- Context pointer: value inside a Ticket; refers to a spec code, node, matrix row, `path:line`,
  test, or commit.
- Verdict: produced by the Director per message; carries acts and "at most one" operation.
- Board: a rendering of `PLAN.md` by `scripts/render-board.sh`; under the 12:46 reversal, R309's
  fuller board, minus the heartbeat.

States of Ticket: `queued` (entered by T1, or T6 park; exits T2, T9) · `in hand` (entered T2,
T5, T8; exits T3 self, T4, T6, T7, T9) · `blocked` (entered T4; exits T5) · `done` (entered T7;
exits T8, or the archive move by hand). Archived is not a status; it is the entry leaving the
list.

States of Checkpoint: open (from T1) → closed (T7). No transition closes it on T9.

Actors: Director (triggers T1–T8); resume operation (triggers T2 in a new session); a person's
hand (T9 and the archive move); Code (the only writer); worker (reports facts, never triggers);
independent acceptor (gives the verdict T7 waits on where a worker did the work); owner (the one
action a kind-three block waits on).

### What I assumed

- I read "holder" as a new header line the checkpoint format must gain; the contract says
  "exactly as `checkpoint.py` writes it today", which has no such field, and I treated that as a
  gap rather than reading `Owner:` as the holder (it cannot be — `Owner: director` is what makes
  the decision-sheet rule fire).
- I read "the ticket text" a worker receives as the `PLAN.md` entry plus the checkpoint's NEXT,
  as B row 4 says, and not the decision sheet — so the sheet's goal is not in the brief.
- I found no authoritative surface for the `someday` tag named in this document beyond the board;
  the spec's far tier (R94, R239, R309 crit 23) is the existing authority for that category, and
  the contract does not register with it.
- I treated the orchestrator's F1–F3 as part of the document under review, not as settled.

## Phase 2 — structural findings

F1 — After the F1 fold, three sentences still read "open checkpoint" as "in hand", and the format has no holder to read instead

> "the ticket in hand with an open checkpoint is the resume point" — §4 Resume; "probe on a tree with one open checkpoint → that id, holder, pointers, NEXT" — §7 B row 7; "refuses T2 on an id whose checkpoint already carries a holder" — §4 Duplicate

Once T1 opens a checkpoint for every queued ticket, a tree with four queued and one in-hand
ticket holds five open checkpoints. The resume rule and B row 7, as written, cannot pick one;
and T2 cannot write or read a holder because `checkpoint.py`'s header carries `Status:` and
`Owner:` only (`_serialize_checkpoint`, lines 241–258). The sweep found no fourth instance.

Key in-hand on the `PLAN.md` 🔄 mark, which `state-probe.sh` already reads, and add one header
line `Holder:` to `checkpoint.py`'s format, validated present when the mark is 🔄 and absent
otherwise. Rewrite the three sentences to say "the ticket marked 🔄" and "a tree with one 🔄
ticket". Strike "exactly as `checkpoint.py` writes it today" or add "plus a `Holder:` line".

`defect · internal-conflict (consistency)`

F2 — Checkpoints never reach git, so "a new session continues the same ticket" holds on one machine only

> "A new session reads it and continues; it never re-derives the ticket" — §2 Checkpoint; "whose checkpoint is missing entirely (a data fault, not a normal state — every `queued` ticket has one)" — §4 Duplicate

`.gitignore` line 1 is `.live-spec/checkpoints/`. The five files tracked today were added before
that line; any checkpoint T1 creates from now on stays local. `PLAN.md` law 9 records that this
machine has already lost a working tree once. A cloud seat, a second machine, or a re-clone after
a loss sees every queued and in-hand ticket as the contract's own "data fault": T2 refuses, the
worker brief (ticket plus NEXT) cannot be produced, and the resume rule has nothing to read —
while the ticket entries themselves, in git, look perfectly healthy.

Choose one: (a) track the directory — drop the ignore line, and ignore `wind-down-*.md` by name
instead, since `scripts/wind-down.py` writes those as scratch; one line, `checkpoint.py`
untouched, and the checkpoint travels with the ticket for its life; (b) move DONE / IN PROGRESS /
NEXT into the ticket entry and drop the checkpoint for tickets — no second file, but it
contradicts `PLAN.md § One plan`'s "a session edits exactly two things here". Prefer (a).

`defect · unenforceable-promise (discharge)`

F3 — Goal and outcome now live in two places with no sentence tying them, and the F1 fold made the heavier of two possible fixes

> "the entry in `PLAN.md § Tasks` **and** the one checkpoint, holderless, with the decision sheet" — §4 T1; "decision sheet and NEXT; the ticket's goal or done where the correction changed them" — §4 T3

The decision sheet's first two lines are goal and observable outcome; the ticket entry carries
the same two. T3 writes both. Nothing says which wins when they differ, and the brief (F1's
assumption, B row 4) reads the ticket, so a correction landed in the sheet alone changes nothing
a worker sees. The skill's sentence the fold cites — "opens a checkpoint before the first
specialist is called" — is about work being started; in the skill, accepted is started. The
contract splits the two, and the lighter fold keeps the sentence true: the checkpoint opens at
T2, and an instruction to do it now runs T1 and T2 as one operation. That also removes the
five-open-checkpoints situation F1 describes.

Either (a) open the checkpoint at T2 and let the queued ticket's entry be the whole of its
statement — the sheet is then written at T2 from the entry, and the entry stays the one home of
goal and outcome; or (b) keep T1 and add the tie: "the checkpoint's DECISION SHEET restates the
entry's goal and outcome word for word; the entry is the source, and the operation copies, never
the reverse." Prefer (a): one home, no copy rule, fewer files, and F1 and F2 shrink with it.

`defect · missing-rule (invariant)`

## Phase 3 — property findings

F4 — T7's recovery rule contradicts the document twice and leaves the half-done state with no lawful actor

> "On a crash between the two, `PLAN.md`'s own mark is authoritative" — §4 Crash recovery; "a ✅ whose command later fails is already flipped to ⛔ by `scripts/state-probe.sh`" — §2 Done; "✅ and checkpoint closed in one step" — §7 B row 6; "repaired by hand once" — §4 Crash recovery

Three collisions: the mark cannot be authoritative when §2 says the command overrides it; B row
6 still says "one step" after the fold said "two writes"; and the named recovery is a hand
repair, which §4 and §6 forbid ("code is the only writer", "the Director never edits by hand").
Walk the crash: checkpoint closed, mark still 🔄. Re-running T7 is the obvious repair, but
`close_checkpoint` raises "checkpoint is already closed" (line 396), so T7 refuses, and the
ticket is stuck in hand with a closed checkpoint until someone breaks the no-hand-edit rule.

Make T7 resumable instead of alarmed: inside T7, a checkpoint already closed is a no-op, and the
re-run sets the mark; that is the whole recovery. Keep the order checkpoint-then-mark (a closed
checkpoint with a live mark is recoverable by re-run; a ✅ over an open checkpoint is a ✅ over
open work, which nothing can tell from a real one). Drop the new alarm class from
`state-probe.sh` — it is a gate for an incident the re-run already repairs — and rewrite B row 6
as "T7 all green → ✅ and closed; re-running T7 on the half-done state completes it and changes
nothing else". Strike "the mark is authoritative".

`defect · unclear-recovery (rollback)`

F5 — "At most one operation" per verdict contradicts the mixed turn the contract itself requires

> "at most one state operation (§4)" — §2 Verdict; "issues one verdict with at most one operation" — §6 Director; "a mixed turn carrying two acts in one breath" — §7 A

The Director skill's own worked mixes are two operations: "always deploy without asking, and
deploy this one" (a decision recorded plus T1), and "stop X, do Y instead" (T6 on X plus T1 for
Y). Under the contract's limit the producer must drop one, silently — the exact failure the
skill's "no act absorbs another" paragraph exists to stop — and `check.py` cannot grade the
`operation` field "exactly" for a fixture whose right answer is two.

The verdict carries a list of operations, one per act that changes state, each naming its
ticket id; "a question changes nothing" reads the empty list. B's first row and A's mixed
fixture then agree.

`defect · direct-contradiction (contradiction)`

F6 — Every transition is written from `in hand` outward; `queued` and `blocked` have no correction, no block, and no landing when a holder is gone

> "T3 | `in hand` → `in hand` | correction" — §4; "T4 | `in hand` → `blocked`" — §4; "T5 | `blocked` → `in hand`" — §4; "T8 | `done` → `in hand`" — §4

Walk the range ends: the owner says "on the photo-site ticket, skip the backup step" while plan-9
is queued. T3 refuses (not in hand); T1 refuses (same goal line — the duplicate gate); the
correction has nowhere to land. A queued ticket's dependency vanishes before anyone takes it —
plan-9's installer defect was found by a dry run, not by a holder — and T4 cannot record it. A
block clears at night with no session holding the ticket, and T5 lands it "in hand" with no one.
T8 reopens "in hand" with no holder named either.

Extend the table: T3 ranges over `queued` (rewrites goal or done in place); T4 ranges over
`queued`; T5 lands where the ticket stood before the block — `queued` when no holder, `in hand`
when the holder still stands; T8 lands in `queued` unless the reopening names a holder. Class:
the four rows above are the sweep; no other row ranges wrong.

`defect · undefined-path (transitions)`

F7 — T9 abandons the ticket and leaves its checkpoint open forever

> "T9 | … | ticket leaves the list; nothing else changes" — §4

An abandoned ticket's checkpoint stays `Status: open` with IN PROGRESS or NEXT filled;
`close_checkpoint` refuses to close over open content, and no operation clears it, so
`checkpoint.py validate --all` lists an open checkpoint belonging to no ticket from that day on —
and after F2's fold (a) it is in git too.

T9 clears IN PROGRESS and NEXT with the halt's reason as their last line and closes the
checkpoint in the same step; the archive line names the checkpoint path.

`defect · no-exit (dead-end)`

F8 — T8 reopens "the same id", but a done ticket has already left `PLAN.md` for the archive

> "reopens the same id; never a copy" — §4 T8; "The archive move by a person's hand follows the plan's existing rule" — §3

A month after a page ships, the owner reports it broken; its done was false. The entry is in
`docs/queue-archive/`, not in `PLAN.md § Tasks`. T8 finds nothing to reopen, and the Director's
only move is the copy T8 forbids.

Choose: (a) T8 brings the entry back from the archive page under its own id and marks the
archive line reopened — two files, a new archive rule; or (b) T8 exists only until the archive
move; after it, an improvement is T1 with the archived id and its archive line as pointers, and
the new ticket's goal says "the original done was false". Prefer (b): one rule less, and the
pointer kinds already cover it.

`defect · missing-scenario (state-space)`

F9 — A reader-judged done condition has no home code can read at T7

> "each checkable by a command or by a named reader" — §2 Done; "every condition passes its command or names its reader and verdict" — §4 T7

Independent acceptance is the fifth condition kind and is always reader-judged. The contract
names the reader but not where the verdict lands. Code at T7 either passes every reader-judged
condition on sight (the gate anchored on nothing — the shape this project has already caught in a
comment-anchored gate) or refuses every one of them. Either way the "independent acceptance"
condition is decorative.

The verdict lands as one line in the checkpoint's DONE section in a fixed shape — `accepted by
<who>: <what was checked>` — and T7 requires that line for each reader-judged condition. The
verify-step reference the Director already carries (`references/verify-step-detail.md`) names
who writes it.

`defect · missing-outcome-check (postcondition)`

F10 — The board reversal cuts two rows, but Requirement 309 as it stands collides with four rules the contract states elsewhere, and §8/§9 name none of them

> "the fuller board (Requirement 309, worker lanes, per-task chips, context pointers shown per row) is scheduled to be built, not retired … The one piece actually cut is the periodic auto-refresh heartbeat (M-540/M-542)" — §8; "The rest of M-519–M-544 stays *todo*" — §9

Read R309 criterion by criterion against the contract:

- crit 7 and 42: "one source file in the host's tree" holding "a task's statement and its
  validation record … keyed by the queue row's id" — a second task store, against §8's first
  bullet and `PLAN.md § One plan`.
- crit 41, 49, 61–66: every task carries a time estimate, frozen at take-up, settled against
  actual at close — against §2's "no estimate". That §2 line is marked *(derived)*; the owner's
  message never mentions estimates, so R309, which is spec, outranks it unless he says otherwise.
- crit 25, 45, 55: statuses `ready` and `deferred`, columns awaiting validation / ready / in work
  / done — against §2's closed set of four, which is the owner's own word.
- crit 14, 86, 88: "standing whether or not anyone asks", "update at every pipeline stage change,
  at take-up, and at a worker's spawn and finish", and the stamp refreshed on the chat's
  heartbeat — against §8's "a generated page a person opens on request". The heartbeat cut named
  in §8 is crit 90 and 96 (M-540, M-542); crit 88 is the same heartbeat by another sentence and is
  not named.

Consequence: test-author derives rows from R309 as it stands and writes tests for a `ready`
status, an estimate field, and a source file the state machine cannot produce; or it derives from
the contract and leaves R309's rows red. Also, F2-as-folded is coarser than it looks: M-540
carries INV-312, which crit 86 cites too, so "struck whole" would take crit 86 with it, and
q-805's own pattern (an invariant left as an empty number pinned in `tests/test_formal_index.py`
`EXPECTED_GAPS` with its reason; the matrix row going whole) applies cleanly only to INV-313.

Replace §9's R309 row with a per-criterion list: 7 and 42 sharpen — the source file is `PLAN.md`
and the statement is the ticket entry; 41, 49, 61–66 — owner's call (Phase 5 Q1), and if kept,
the estimate is a ticket field written at T1 and frozen at T2, which is crit 61–62 already; 25,
45, 55 sharpen — `ready` is `queued` with its done written, awaiting validation is "not yet a
ticket", `deferred` is `queued`; 14 and 86 sharpen — the state operation re-renders the board
file as its last step, so the board is fresh at every transition with no timer and no process
(`scripts/render-board.sh` and `tests/test_board_matches_the_canon.py` already exist for exactly
this); 88, 90, 96 retire — INV-313 to `EXPECTED_GAPS` with the reason, INV-312 sharpened not
emptied, M-540 rewritten to keep "delays that stage not at all", M-542 split.

`defect · direct-contradiction (contradiction)`

F11 — `someday` renames the far tier the spec already has, and the resume offer does not skip it

> "A `queued` ticket may carry one display tag, `someday`, so the on-request board groups it apart from the runnable head" — §3; "Nothing in hand: the top `queued` ticket is offered" — §4 Resume

R94 already defines "a far tier the runnable report stands down by name", R239 its rare
surfacing, and R309 crit 23 keeps it off the board by that name. `PLAN.md` law 6 is one term, one
word. And nothing in §4 keeps a `someday` ticket at the head of `queued` order from being the one
resume offers.

Call it the far tier in §3 and §9 (retire nothing), and add to Resume: "the offer skips the far
tier, as R94's runnable report already does".

`defect · missing-rule (invariant)`

F12 — Proof A's freshness on "the model named in the run" has nothing to read

> "traces count only when drawn after the last change to … the model named in the run" — §7 A

A trace carries `skill_version` and no model id (`traces/correction-shouted-constraint.json`).
The model changes; every trace stays fresh by time; the contract's own rule that another
version's traces prove nothing fails silently on the one axis it cannot see.

The producer writes one `model` field per trace; plan-2's key compares it to the model the run
is configured with.

`defect · unenforceable-promise (discharge)`

F13 — §10 Q4, answered: no gate deadlocks on the mark, but every close costs a second push

> "Delivery to `origin/main` is a done condition and the push gate runs before ✅ is written" — §10 Q4; "the delivery commit on `origin/main` where delivery is a condition" — §4 T7

No push gate reads a task mark (`guardrails/pre-push` and its checks name `PLAN.md` only for the
freeze, rotation and reach checks). So no deadlock. But the ✅ edit is itself a `PLAN.md` commit,
and it may be written only after the delivery is on `origin/main` — two commits and two gate
walks per ticket, and this project's push walk re-arms a twenty-minute gate on each. Sessions
will batch marks or defer them, which is the drift the plan exists to stop.

Let the condition read "the delivery commit is on `origin/main`, or is in the same push as the
commit carrying the mark"; the probe's existing failing-key rule (`state-probe.sh` lines 75–81)
already flips a ✅ whose push never landed to ⛔, so nothing new enforces it.

`recommendation · now · hard-to-operate (ops-ux)`

F14 — "Same pointer set" as a mechanical duplicate gate refuses legitimate siblings

> "Code refuses T1 on the same goal line or the same pointer set" — §4 Duplicate

q-436 and q-437 are siblings from one tlvphotos inbox message and cite the same sources; two bugs
on one requirement cite one code. The second is refused by a gate meant for copies.

Gate on the goal line alone; print "shares every pointer with q-436" as a note the Director
reads. The judgment already belongs to proof A by the contract's own words.

`recommendation · now · over-general (abstraction)`

F15 — A delivery target in another repository names no `origin/main`

> "delivery to `origin/main` under the project's own push rules" — §2 Done

plan-9 delivers into `~/tlvphotos`, which this window may not write. The condition as written
points at this repository's main.

Have the delivery condition name the repository when it is not this one, and state that such a
ticket's delivery is proven by that repository's own probe, not this one's.

`recommendation · later · missing-prerequisite (precondition)`

### Coverage

| Entity | Create | Read | Update | Delete | Notes |
|---|---|---|---|---|---|
| Ticket | covered (T1) | covered (probe, brief) | partial (T3 in-hand only — F6) | partial (T9, archive by hand; reopen after archive — F8) | |
| Checkpoint | covered (T1) | partial (not in git — F2) | covered (T3–T6) | missing (T9 orphan — F7) | holder field absent — F1 |
| Verdict | covered | covered (check.py) | — | — | one-operation limit — F5 |
| Board | covered (render on request / at transition) | covered | partial (R309 collisions — F10) | — | |

| State | Invariants stated | Invariants missing |
|---|---|---|
| queued | done written, pointers resolve, no duplicate | correction and block reachable (F6); far-tier skipped by resume (F11) |
| in hand | one holder, checkpoint open | holder readable (F1); goal one home (F3) |
| blocked | one of three named reasons | landing after clear with no holder (F6) |
| done | every condition proven, checkpoint closed | half-done recovery (F4); acceptance line home (F9); reopen after archive (F8) |

Authorization: a single-owner local tool; the actor split (Director triggers, code writes, a
worker only reports, a hand archives) is stated in §6 and holds. No table is owed.

| Surface | Declared laws | Edge-condition | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| Ticket (`PLAN.md`) | N/A — the contract declares no cross-cutting law; it becomes spec text at spec-author, where the twin habit writes the clauses | hit — F6 | hit — F10 (statuses on the board vs the ticket) | hit — F8 | hit — F11 |
| Checkpoint | N/A — same | clean | clean | hit — F7 | hit — F2 (a fresh clone), F1 (many open) |
| Verdict / evals | N/A — same | hit — F5 (two acts) | clean | clean | hit — F12 |
| Board | N/A — same | clean | hit — F10 | clean | hit — F10 (crit 14, 86, 88) |

Class lens: swept — sentences keyed on open-checkpoint-as-in-hand (F1, three instances);
transitions written from in-hand outward (F6, four rows); R309 criteria colliding with the
four-status and one-store rules (F10, four groups); two homes for one ticket fact (F3, goal and
outcome).

## Phase 3.5 — acknowledged gaps

§10 Q4 stands unanswered in the document; F13 answers it by inspection. §1 leaves the operation's
command-line shape to package 2 — right, and F1's `Holder:` line and F9's acceptance line are
the two format facts that package must then carry. The document carries six *(derived)* markers
and no `[default]` tag; it is not spec text yet, so no `[default]` count is owed.

`acknowledged · undefined-path (transitions)`

## Phase 4 — human and operational factors

Nothing beyond F13. The visible words — queued, in hand, blocked, done, far tier — are the
owner's or the spec's; no internal name leaks onto a surface a person reads. Security and privacy
are out of scope for a single-owner local tool, named here as a skip.

## Phase 5 — closing

1. Fix before test-author: F2 (checkpoints into git, or into the ticket), F10 (R309 per
   criterion, not two rows), F5 (a list of operations per verdict). F1, F3, F4, F6 follow from
   the first two and fold in the same pass.
2. Sentences to paste in: "The `PLAN.md` entry is the one home of a ticket's goal and outcome; a
   checkpoint restates neither." "Every ticket's checkpoint is tracked in git for the ticket's
   life." "A verdict carries zero or more operations, one per act that changes state, each naming
   its ticket." "T7 run on a half-closed ticket completes it and changes nothing else." "The
   resume offer skips the far tier."
3. One question only the owner can answer: does a ticket carry a time estimate? R309 (crit 41,
   49, 61–66) says yes and settles it against actual at close; his 09-02 message is silent; the
   contract's "no estimate" is a derived line. If yes, the estimate is a ticket field frozen at
   T2 and R309 stands; if no, those criteria retire by the q-805 pattern with his word as the
   reason.
4. Recommendations for a taste call: F13 (delivery condition allows same-push), F14 (goal-line
   gate only), F15 (foreign-repo delivery names its repository).
5. No `[default]` tags in this document.

Readiness: needs another iteration. The fold is one sitting — nothing here changes the owner's
decisions, and only Q1 needs his word — but F2, F5 and F10 change what test-author would derive
rows from, so it must not start before they land.

---

## Fold column

| Finding | Kind | Folded / rejected |
|---|---|---|
| F1 | defect | open |
| F2 | defect | open |
| F3 | defect | open |
| F4 | defect | open |
| F5 | defect | open |
| F6 | defect | open |
| F7 | defect | open |
| F8 | defect | open |
| F9 | defect | open |
| F10 | defect | open |
| F11 | defect | open |
| F12 | defect | open |
| F13 | recommendation | open |
| F14 | recommendation | open |
| F15 | recommendation | open |
