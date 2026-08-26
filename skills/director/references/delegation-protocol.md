# Junior delegation protocol

The full protocol referenced from `SKILL.md`'s "Gates worth remembering" section — decided from the
request, BEFORE the first tool call (SPEC INV-69).

**Junior delegation (decided from the request, BEFORE the first tool call):** the trigger is judgment
against mechanical — work whose steps can be written precisely (known edit strings, a known command,
fan-out fact-gathering, a report or list or dump to produce) routes to a worker, while anything carrying
judgment or design stays senior. Size is a weak hint only, never the decider. The trigger, the tier
ladder, and the raw-output law all live in the base skill's rule 5 and the routing rule — this passage is
their reference; it is not a second home (live-spec-base rule 5, SPEC INV-69).

**The routing rule (SPEC INV-69) picks the tier — propose the cheapest tier that can pass the brief, the
seat may overrule it aloud:** the proposal reads the STEP and kind of the work, beyond the row's size
alone — a judgment step (spec, prove, architecture, matrix-level calls, findings triage, any taste call)
proposes the seat and is never routed down, a mechanical step proposes a worker at the tier above. The
economy rung moves the threshold (at `lean` an airtight brief rides one tier cheaper, at `tight` the
cheapest sufficient tier is always the proposal). And the proposal is ADVISORY — the seat may override
per wish, the override logged as one line on the checkpoint and the delivery report, proposed tier → chosen
tier → why.

**The brief is self-contained (the BMAD story-file lesson):** delegated work ships as one document
embedding the EXACT spec sentences it serves, the exact edit strings or commands, the checks to run, and
the checkpoint path — the worker never hunts context, never interprets the spec, never decides. If writing
the brief means deciding something first, that decision is the seat's and happens BEFORE delegation —
"explaining it would take longer than doing it" is how delegation silently dies.

**The brief's birth has three laws (SPEC INV-53/54/55):** a brief that edits existing files is born from
READING them in full — three recorded lines per file (current state · what changes · what must survive),
every step back-referencing its spec sentence, every technical claim citing a source (a file:line, a
command's output), never memory of a file. The brief carries the closed HALT list — ambiguous requirement
· two consecutive unexplained failures of one command · missing config/dependency · acceptance impossible
as briefed — stop WITH evidence, otherwise run to completion (the seat's escalation ladder is a separate
move, after a failed acceptance). And the brief is SIZED — its text within ~300 lines, at most ~8 files to
edit [default], the work splitting above either — passing PATHS, never inlined file bodies. See the private
playbook repo's PLAYBOOK.md.

**The worker contract (SPEC ACT-3):** the brief NAMES the files the worker may write — its session's
write-ownership narrowed to exactly those, reads free, writes fenced. Same-session sibling-worker files
are fence-benign (the concurrent-edit fence alarms on foreign sessions, staying quiet on your own briefed
workers — the seat who briefed both owns the seams between briefs). Owning those seams is a brief-time
act: before spawning another concurrent writer, the seat confirms its brief's write-set is disjoint
from every already-running writer's brief, or gives it an isolated worktree (SPEC INV-105) — because
the fence stays silent between same-session siblings, this disjointness is settled when the briefs are
written, ahead of the new worker's first write. The session's live setting lines ride
into the brief verbatim — a worker never resolves the settings ladder itself, it cannot hear the human's
spoken word.

**A worker never restores a working tree with a git command (SPEC INV-298; the gate INV-299).** Before a worker
mutates a file it means to put back, it reads that file and holds its bytes. A worker puts a file
back by WRITING ITS OWN SAVED BYTES. A worker runs no command that discards uncommitted work, in any
tree: `git checkout -- <path>`, `git checkout .`, `git restore` outside `--staged`, `git stash` and
its `push`, `save`, `create` and `store` forms, `git reset` with `--hard`, `--merge` or `--keep`, and
`git clean` with `-f` or `-x`. Such a command's blast radius is a PATH, so its damage lands on files
the worker never wrote and its brief never named. This rule binds a worker in every tree, including
its own isolated worktree, since a worktree shares one repository with the lanes beside it and a
worker cannot read off its brief what else that repository holds. A worker that holds no saved bytes
for a file it mutated, or that believes a file needs a git-level restore, HALTS and reports the file
and the mutation it made, and it writes no further file and runs no further command. The
orchestrator owns recovery: it restores the named file from the last committed stage, hands the
worker a fresh brief carrying that file's current bytes, and records the halt in the row's delivery
report, and the halted work resumes under that new brief. The orchestrator's own half: a finished
build stage is committed before the next worker touches its files, so a worker that hits a broken
file has a commit to be recovered from. `guardrails/check-worker-restore.py` reads the worker runs'
transcripts for the command and runs at the verify step. The write-set disjointness above fences
EDITS and gives no cover here, which is why the clause stands on its own: the two destructions of
uncommitted work on 2026-07-23 and the near miss of 2026-07-27 all came from a worker running
correct-looking work, and the `git status` it pasted afterwards read "clean" in the safe case and the
destructive one alike. The clause rides every brief this protocol composes.

**The brief carries the register laws, so the worker's own text obeys them (SPEC INV-221, INV-173).** The
brief states the register laws the worker's report and any agent-to-agent message must hold — the
no-scissors law (no naming a thing by denying its neighbour, SPEC INV-173) and the no-dramatization law
(grading the size of a change, up or down, is the reader's act, SPEC INV-221). A worker writes text a
human reads, and the chat and document judges [INV-203] never read its report, so the brief is where the
laws reach it. The worked instance: workers reporting to this pack opened "Excellent work" and named a
premise wrong "in an important way", both graded-size sentences the worker had no brief telling it to
drop (the owner's count, 2026-07-17).

The brief ARMS the worker for the workshop — it carries the host's problem-ledger path
(`.live-spec/PROBLEMS.md`) with the WATCHED-line duty: workshop noise the worker hits (a flaky harness, a
missing dependency, a tool misbehaving) goes into its checkpoint as a ledger line — signature, date, one
line of context, logged every time — and the seat carries the lines into the ledger at verify (SPEC
INV-23). And it carries the CLOCK — the date and time read at briefing — so the worker stamps its
checkpoint and any dated output from the brief's clock, never an invented hour (SPEC INV-24; a worker WITH
a shell re-reads the machine clock itself — the brief's line is the floor for one without, and elapsed
time is never guessed). And a result failing its brief's acceptance escalates exactly ONE tier every time,
with a logged line covering the move — one rung up, in order, always logged.

**Every delegation reports its saving:** the
delivery report carries one line — what went to the worker and roughly how much senior work it saved.
The line is what keeps the habit alive; a session that never writes it is a session that quietly
stopped delegating. The line lives in the row's delivery report, which the closing commit moves to the archive with the
row, and a suite check reads it from the archive: a delivered row without the line goes red
(SPEC INV-103, INV-276, forward from 2026-07-12).
 The same accounting also names the reads dispatched beside the work delegated, so a session that filled its own context with a read it should have dispatched shows that in the report (SPEC INV-137). Each work block in the report opens by naming its root, and the report accounts the block against its announced plan line (SPEC INV-314). The duty binds the
orchestrator seat regardless of model, whatever tier leads the seat.

## The cleanup-safety constraint, and the grounding law's canonical wording

Two things the body's "Junior delegation" bullet carried and this file did not. The brief's birth laws,
the worker contract, write-set disjointness and the reporting duty are stated above and are not
restated here.

The brief carries the cleanup-safety constraint: a cleanup acts only on what the run provably owns,
targeted by a recorded process group or an owned install path (SPEC INV-162, base rule 17).

Each work block in the report opens by naming its root. The root is the person's dated request, a
standing instruction, or a stated reason, and machinery is never a root. The report accounts each
block against its announced plan line (SPEC INV-314).
