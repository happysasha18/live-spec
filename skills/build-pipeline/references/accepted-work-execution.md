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
claim against them directly.

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
rule 12/27 already reserve for him — a taste call, a trade-off no artifact settles, or a change
to the definition of correct that is still an open fork — never an ordinary buildable result a
command, a test, or a plain read already confirms was delivered. A redefinition he ordered
himself is not that third case: he settled the fork when he ordered it, and carrying out his
decision is executing it, not making it. If he disagrees with a shown result afterward, that
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

**Landing a change owes its own law, regardless of which specialist performed the work.** See
[the landing law](landing-law.md) for the bug-door tripwire, the
removal-accounting pointer, the restructure/migration merge gate, the docs-layout vehicle,
compaction's every-push cadence, the adversarial-review freshness rule, the release-tier
judgment, and the skill-review gate.

## The specialist brief

A specialist gets a brief naming the goal and the primary sources to read — never a pasted copy of
what the pipeline already read. What comes back is a short answer with pointers. The pipeline
re-reads only the lines a decision rests on.

## Reporting a closed piece of work

For accepted work the sentence names what actually changed — which document, which check, which
artifact — not merely that work began. A sentence that only restates intent after the fact reads as
more work than it reports, and the checkpoint's DONE section is where the detail lives for anyone
who needs it.

A change to a document owes three more short lines beside the document's name: what that part said
before, what it says now, and what was added. The person can then disagree with the edit while
undoing it is still cheap, which is what turns "I understood you" into something they can check.
