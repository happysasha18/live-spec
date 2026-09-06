# Accepted-work execution detail

Read this reference when Director routes new or existing work into the accepted-work pipeline. It
preserves the execution behaviour that used to sit in Director; classification stays in Director
and nothing here reclassifies the person's message.


For accepted work, write this and stop.

These are questions to answer, not a form to fill. A line with nothing behind it gets one
word or goes. A one-line bug fix does not need a risk paragraph, and a sheet longer than
the work it describes means the work was over-read.

- **Goal in the human's words** — what they want, as they said it
- **Observable outcome** — what will be true afterwards that is not true now
- **Dimensions touched** — with a reason for each
- **Known** — the facts that already settle part of this
- **Unknown** — what must be found out before or during
- **Risk and irreversibility** — anything that cannot be undone, named
- **Specialists** — who is needed, what each is for, what can run in parallel
- **Evidence** — what will show the goal was reached, not merely that steps ran
- **What runs next** — where other accepted work stands open, which piece runs next and why that
  one, read off the states the plan records rather than composed from memory
- **Documents that must change** — only those whose sentences actually change

The last line is where ceremony collects. A refactor that changes no behaviour changes no
product spec. A bug fix changes a test and the code. Listing a document because it is
important, rather than because it is now wrong, is the habit that line exists to break.

For a question, an idea, an observation Director routed as evidence, or a halt there is no
sheet. There is a sentence.

### A sheet at the size the work deserves

> **Message.** "the export button is greyed out for users on the free plan, that's wrong"
>
> **Act.** Observation whose repair follows beyond doubt — free-plan export is a stated
> entitlement, so this is a defect, not a preference.
>
> - **Goal** — free-plan users can press export again
> - **Observable outcome** — the button is live for a free-plan account
> - **Dimensions** — product behaviour (a stated entitlement is not honoured); quality (it
>   shipped without a test that would have caught it)
> - **Known** — the entitlement is specified; the button reads plan state
> - **Unknown** — whether the plan check or the entitlement data is wrong
> - **Risk** — none; the change is reversible
> - **Specialists** — developer; test author for the regression test. No spec author: the
>   spec is right and the code disagrees with it
> - **Evidence** — a test that fails on today's code and passes after
> - **Documents** — none. The spec already says what should happen
>
> Nine lines, because the work is small. A cross-cutting feature earns more.

## Execution

The pipeline acts on an admitted route. A question, an idea, an observation Director routed as
evidence, or a halt gets no sheet, per above —
and nothing below applies to it. What follows runs only for work that just earned a
decision sheet: an instruction, a correction, a decision, or the settled half of a
conditional. Earning a sheet and creating work are two different things: an instruction and
a settled conditional can name a goal nothing already covers, so they create work; a
correction and a decision write their sheet onto work that was already running, and create
none.

**Before that sheet turns into a checkpoint, the pipeline says so if it disagrees with the
work itself.** Writing the sheet is not only deciding how to build the thing asked for; it is
also the one moment to weigh whether the thing asked for is right. A flaw the pipeline can see
— a wrong assumption, a step that undoes an earlier one, a goal that conflicts with a standing
decision already on record — gets stated plainly, with the reason, in the same reply that would
otherwise just begin the work. This is not a question thrown back to stall: the pipeline still
proceeds once heard out, on the human's word either way; what it never does is execute a request
it believes is wrong without having said so first. Silent agreement is its own kind of failure —
it looks like competence and is actually the pipeline skipping the one check only it, holding
the fuller picture of what is already built and decided, can run.

**A task enters work only through a validated statement.** The skill body carries the four fields
admission derives and the command that validates them, and is not repeated here; what it defers to
this page is who writes the reader's file and what take-up freezes. That `<file>` carries the
answers of a fresh agent holding no project vocabulary, given only the Statement paragraph and
three questions — what is to be done, why, and how long — plus the short name it places on the
work. A failed floor or a failed reader leaves the row out of work until the statement is rewritten
and validated again. `hold <id> --holder <name> [--lanes <n>]` then takes the row up: it freezes the wording, and it writes the plan's own
expectation of what runs side by side against the lane decision `<n>` actually makes, naming any
divergence on the checkpoint's `LANES` line. From that freeze on the task is spoken in those words
letter for letter — in the chat, in a worker's brief, at the close — and the close carries the
estimate beside the actual and that divergence into the delivery trail. The number of rows standing
in hand at once is bounded by the same profile cap rule 7 carries: the board splits the in-work
column into exactly that many lanes, so a row past the cap is a row with no lane to stand in. A done row
is refused a take-up and comes back through T8 `reopen`, which is where the false condition and its
evidence are recorded. A row the halt abandoned is the other closed shape, and taking it up again
reopens the sheet the halt left, with a line saying the work resumes rather than starts fresh —
refusing it there sent it to `reopen`, which takes only a done row, and left an abandoned row that
no transition could move at all.

**New work opens a checkpoint before the first specialist is called; work already in
flight updates the one it already has — never a second `new` on the same work.** An
instruction naming a goal nothing already covers opens a fresh checkpoint: run `python3
scripts/checkpoint.py new <path> --title "<goal, short>" --owner pipeline --decision-sheet
"<the decision sheet above, verbatim>"`, `<path>` under `.live-spec/checkpoints/`, named
for the work, not for the pipeline. A correction, or a decision that changes work already
running, targets a checkpoint that already exists — it never runs `new` again on that
path, which would either silently overwrite the existing DONE section (`new_checkpoint`
always writes a blank template) or, at a different path, open the duplicate this file
elsewhere forbids. It runs `python3 scripts/checkpoint.py update <path> --decision-sheet
"<the revised sheet>"` (and `--next`/`--in-progress` where those changed too) against the
SAME path the original instruction opened, so one piece of work keeps one checkpoint for
its whole life. The decision sheet is not duplicated prose — it is the checkpoint's
DECISION SHEET section, the one place this work's goal, knowns, unknowns and risk live
while the work is in flight. This is what makes a resumed window real instead of a
promise: the next agent reads this file, not this conversation.

**A specialist gets a brief, not a copy** — see "The specialist brief" at the end of this
file for the exact shape. This is the whole of delegation's procedure.
`skills/build-pipeline/references/delegation-protocol.md` is kept beside it as the wording
source for the delegation line and the worker-brief shape. The tier ladders, escrow law and
reporting bureaucracy that file also carries were built for one mandatory pipeline; none of
that is a specialist's job here, and none of it is part of this procedure — no bureaucracy
without a working need this pack still has.

**Independent pieces of work run in parallel through the existing lane mechanism, not a new
one.** `scripts/open-lane.sh` already opens a worktree-isolated branch under the profile's
lane cap — `skills/live-spec-base/SKILL.md` rule 7 carries the lane law in full and is not
repeated here. What this step adds is the judgment: two pieces of accepted work are
independent when neither depends on the other's output and neither rewrites the same
section or behaviour. Work that merely shares a canonical document —
`PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`, `PLAN.md` — is not thereby
dependent; every write to a shared document goes through one integration owner (the
pipeline itself, or whichever specialist currently holds the pen) one lane at a time, so
the document stays a convergence point, not a lock two lanes wait on.

**Anything the pipeline starts — a worker, a test run, a render — has an expected duration, and the
seat looks at what is still running at every wake-up and between stages (`ps` with elapsed time)
instead of waiting for a notification.** A process past its expected time with no output is
inspected, and one that does nothing is ended and named in the report; a check is never left
running unlooked-at.

**When the same thing has gone round twice — a cascade restarted, a red that came back, a fix
applied again — the seat monitors every round of every spawn from then on and intervenes at once.**
The same rule binds a lead over its own spawns, and their spawns. Past the second or third round,
nobody fiddles further: the cause is fixed at the root or an alternative is taken, and the report
names which.

**A new fact can change the remaining graph.** Read a specialist's answer, a failed check,
or a fact the human adds mid-work against the plan just made — not filed for later. When
it changes what remains, run `python3 scripts/checkpoint.py update <path> --next "<...>"`
against this work's own checkpoint and add to or cut the specialist list; never carry a
stale plan forward silently. When it does not change anything, say so and continue —
replanning on every unremarkable update is its own kind of noise.

**Accepted work that turns out to be a confirmed bug still owes a sweep before it counts as
finished.** Name the mistake's class and search for its siblings in the same change; a point fix
that leaves relatives standing stays a status until the sweep lands. See
[the class hunt](class-hunt.md) for the full four moves, including when the
class boundary calls for the human's judgment.

**The verifier gets the goal and the artifacts, never the executor's self-report.** See
[the verifier detail](verify-step-detail.md) for the full
protocol: when a fresh checker is required (SPEC INV-46) versus when the pipeline's own
re-check against the decision sheet's observable outcome is enough, the worker-restore
gate, and the audit walk. The short version: a check that did not produce the work is
handed the observable outcome and the paths the work actually touched, and checks the
claim against them directly. That closing check reaches the product on real data — the thing as it
actually runs, over the records it really reads — never a stand-in built for the test, and never
the producer's own test alone.

**Closing the work closes the checkpoint in the same step, never a later one.** Once the
verifier is satisfied, clear the checkpoint's IN PROGRESS and NEXT sections to reflect what
actually remains — usually nothing — and run `python3 scripts/checkpoint.py close <path>`.
It refuses to close over content still marked open, so a checkpoint that will not close is
telling the truth about work that is not actually finished.

**A shown result closes the work; the human's own eye is never the gate on an ordinary
delivery.** Once the verifier confirms the observable
outcome, the pipeline shows the result — the changed document, the passing check, the running
page, whatever the decision sheet named — and closes the checkpoint in the same step. It never
leaves a row open to wait for the human to look at what was already shown and bless it: a row's
own definition of done that names his eye as the check is describing one of the three cases
base rule 12/27 already reserve for him — a taste call, a trade-off no artifact settles, or a change
to the definition of correct that is still an open fork — never an ordinary buildable result a
command, a test, or a plain read already confirms was delivered. A redefinition he ordered
himself is not that third case: he settled the fork when he ordered it, and carrying out his
decision is executing it, not making it. The converse holds too: where a delivered change reaches
past what he ordered and redefines behaviour he never named, that wider half is the third case, and
an artifact describing the old behaviour is what the change is weighed against rather than a
decision to change it. If he disagrees with a shown result afterward, that
disagreement is a new fact, not a reopening of the one that shipped: it becomes its own task
carrying his correction, and the closed row stays closed. This changes nothing about rule 12's
own ground — an action that is genuinely irreversible outside git still stops for his word
before it runs, never only after it is shown.

**For the taste calls rule 12/27 reserve for him, his verdict — approval or rejection — is
itself the movement end for the judged artifact, written into the task's board row or project
charter in the same minute it lands, before the conversation the
verdict triggers continues.** A verdict arriving mid-conversation does not feel like a movement
end, because the conversation carries on past it — but for the artifact judged, the movement
ended the instant the verdict was heard, and chat does not survive a context wipe, only files do.
On 2026-08-08, in the tlvphotos project, a rejection on a shown prototype arrived mid-conversation;
the session spent two hours on the design dialogue the rejection triggered while the task state
still read "awaits his walk" the whole time. An adversarial reviewer caught the gap — not the
session, and not him. The corollary is amend, not append: a new verdict replaces the superseded
board state in place, and the old text moves to history; appending an addendum over a line
the verdict has already made stale is the failure that produced that incident.

## The trusted closure kernel

**An estimate's basis is either comparable rows or a plain admission.** The basis names the closed rows whose recorded durations the range rests on, or it says the range is the author's reading of the plan with no history behind it. A sentence shaped like a derivation ("read off the plan's steps") in front of a number nobody derived is refused by the reader of the statement, since three rows with the same sentence and unrelated numbers were found on 2026-09-06.

**Nothing is spawned before admission.** A worker or a subagent starts only from the brief the
pipeline hands it (`brief <id>`), and the brief is refused without an admitted row on the one
board carrying a definition of done and an acceptance command. A report or a row written after
the work was done is not admission; the gate refuses without a task id, mechanically (the
tlvphotos defect, 2026-09-06).

The rule sits on the spawn itself, not on the caller's willingness to consult it: the guard the
body names and the brief run the same three legs through the same function, `pre_spawn_check`, so
they cannot judge a row differently. Until that guard existed the legs lived only inside `brief`,
a command an orchestrator was free never to call. What the guard costs, said plainly: every spawn
from a session opened on this project names a row, read-only errands included. What it cannot
reach: a spawn from a session that does not load this repository's settings, and a worker that
names a real row and then does something else — it reads the board, never the worker's conduct.


The skill body carries the rule in short. These are the ten clauses it defers here, and the
commands that run them.

- The definition of done (DOD) is fixed at admission and cannot be silently changed after work
  starts.
- Changing the DOD is a separate explicit T3 operation: keep the previous text/hash, the source and
  the reason of the change.
- The executor may provide evidence but may not issue the final acceptance verdict itself.
- The verifier receives the frozen DOD, the real diff/artifact, the check commands, and the exact
  commit/tree hash.
- Any change after verification voids the evidence.
- The presence of a test, a field or a report is not success: the command must actually pass.
- A task cannot close while its accepted scope still holds todo/target/not-built, a missing
  artifact, or a red check.
- No numeric threshold may be invented after start that was not in the admitted DOD.
- `blocked` is allowed only for a real external dependency; needing the owner's choice is not
  blocked.
- close is a controlled state transition, never a textual claim by an agent.

A done mark typed straight onto `PLAN.md` skips every one of those. `guardrails/check-close-receipt.py`
(push gate u, and a step in the CI gates workflow) refuses to let such a row out: a row that became
done in what is about to be published must carry a checkpoint, and any done row that has a
checkpoint must carry a passed receipt whose verified done is the one the row and its anchor both
still read. The anchor is read here as well as at `verify`, because `verify` never runs again on a
closed row — without that, deleting the hash line one step later published the same contract swap.
The published board reads the same receipt: `scripts/render-board.sh` draws a done over a FAILED
receipt as reopened, which holds on the Pages runner, where no acceptance command runs at all and
every mark is otherwise taken at its word.

**What none of this holds, said rather than left to be discovered.** Whether a recorded acceptance
is a meaningful check: a key reading `true` clears every gate here, and the only reader of that is
a person looking at the diff. And a receipt is plain text in the checkpoint, which the tree hash
deliberately leaves out of the tree it pins, so a hand-written RECEIPT line satisfies both `close`
and the gate. What the kernel buys is that forging a done now takes a forged receipt naming a
verifier, a verdict and the admitted done's own digest, sitting in the diff — instead of one typed
character.

`admit` writes the DOD's own sha256 onto the row beside the text it hashes. `correct <id> --done
"<new>" --source "<who asked>" --reason "<why>"` is the only door through it: it records the
previous text and the previous hash on the row, and a `--done` without both of those flags is
refused. The close recomputes the hash from the row and refuses a mismatch, so a done edited by
hand between admission and closing stops the close rather than passing under it.

`verify <id> --by <name> [--command "<extra>" ...] [--surface <path-or-url>]` writes the
acceptance receipt into the checkpoint's `DONE` section: who accepted, when, the tree hash `git
write-tree` computes over a temporary index of the working tree, the HEAD commit, the frozen DOD's
hash, the acceptance it ran, the surfaces given, and every command with the exit code it actually
returned.

**The verifier runs the acceptance the row already recorded** — the body carries the mechanic and
the command shape. Why it is so: until 2026-09-06 the receipt was made of whatever the command
line handed it, so `verify --by anybody --command true` produced a passed verdict having run
nothing about the work, and the row's own check — the one that would have failed — never ran. The
name in `--by` proves nothing on its own; the acceptance running is what the receipt is for. The
key is run in the tree that holds the plan, because a key names that project's files relative to
its root. `close` then compares the acceptance the receipt ran against the one the tree records
now, so rewriting the check after the evidence was written voids it.

`--by` is refused when it names the row's own holder, because the holder is the producer. A receipt carrying
any non-zero exit code is a failed verdict, which is what "the presence of a test is not success"
means in code. Where the DOD names a rendered or published surface — the words `page`, `board.html`,
`link`, `published`, `rendered`, `url` — a receipt with no `--surface` is refused, because a fixture
passing is not the surface rendering.

`close` reads that receipt rather than any agent's sentence, whatever the checkpoint's own status
— a checkpoint closed by some other route carries no receipt, and closing over it would be the
textual claim this kernel exists to refuse. It refuses when there is none, when
its verdict failed, when the DOD's hash has moved since it was written, or when the tree hash no
longer matches the tree as it stands — a change after verification voids the evidence and the work
is verified again. It also refuses a row whose checkpoint is gone, because no checkpoint means no
receipt to read, and a row closed once re-enters through `reopen` rather than through a missing
file. Every refusal prints one plain reason, exits 2, and leaves the row's mark exactly
as it was.

**The done's digest is anchored on the checkpoint at admission, which makes the row's own copy
tamper-evident** — the body carries where the two copies live. Why it is so: deleting the row's
hash line used to make the row read as one predating the kernel, so the next `verify` minted a
fresh hash over whatever the done then said and `close` compared that new contract against itself
— a contract swap in one deleted line. The verifier now refuses a row whose anchor stands and
whose hash line is gone, and refuses one whose hash and anchor disagree, which is the shape of a
done and its hash rewritten together. `correct --done` moves the anchor with the done it anchors;
nothing else writes it. The anchor is evidence, never a second home for the done: it is a digest,
and a hand that reaches the checkpoint as well leaves both copies to disagree with the receipt
`close` reads out of that same file.

A row admitted before this kernel existed carries its frozen scope under `**Acceptance:**` and no
hash at all. That acceptance IS its done, read as one; its first `verify` records the hash on the
row and the anchor on the checkpoint, dated and marked as predating the kernel, so every
comparison after that is real and that arm is walked once per row; and `close`
refuses such a row until one is recorded. `reopen` on a row that predates checkpoints opens the
minimal one it never had, headed with the day it was opened, so the row has a door back into the
kernel at all.

**Landing a change owes its own law, regardless of which specialist performed the work.** See
[the landing law](landing-law.md) for the bug-door tripwire, the
removal-accounting pointer, the restructure/migration merge gate, the docs-layout vehicle,
compaction's every-push cadence, the adversarial-review freshness rule, the release-tier
judgment, and the skill-review gate.

## The specialist brief

A specialist gets a brief naming the goal and the primary sources to read — never a pasted copy of
what the pipeline already read. A brief to a lead also says that the lead watches its own spawns by
the rule above and never lets a cascade run to a fourth round. What comes back is a short answer
with pointers. The pipeline re-reads only the lines a decision rests on.

## Reporting a closed piece of work

For accepted work the sentence names what actually changed — which document, which check, which
artifact — not merely that work began. A sentence that only restates intent after the fact reads as
more work than it reports, and the checkpoint's DONE section is where the detail lives for anyone
who needs it.

A change to a document owes three more short lines beside the document's name: what that part said
before, what it says now, and what was added. The person can then disagree with the edit while
undoing it is still cheap, which is what turns "I understood you" into something they can check.
