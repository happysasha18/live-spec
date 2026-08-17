# The verify step in detail

The two long passages of `SKILL.md`'s verify step, referenced from the step itself: the worker-restore
gate's own reading, and the audit protocol. Every line below reads exactly as it read in the body.

## The worker-restore gate at verify (SPEC INV-298; the gate INV-299)

**A session that spawned a worker runs `python3 guardrails/check-worker-restore.py` here, and reads
its verdict before it accepts the worker's result (SPEC INV-298; the gate INV-299).** The gate reads
the worker runs' own transcripts for a command that discards uncommitted work, which is the one
signal that separates a worker that wrote a file's bytes back from a worker that discarded a lane's
uncommitted work — the `git status` both paste afterwards reads "clean". The gate reads the last 24
hours; a session whose worker ran earlier than that passes `--since-hours` wide enough to cover the
run it is accepting. A red names the run, the command and the paths. Where the run is this
project's, the session recovers the named files from the last committed stage before anything else,
and the worker's result waits on that. Where the paths belong to another project's tree, the session
writes what it read into that project's intake folder and touches no file there, since a repo it was
not assigned to stays read-only (base rule 7). The gate stands down by name on a host that keeps no
transcripts where it looks, and it carries a counting start so a machine's pre-clause history reds
nothing. A red naming an empty transcript root says the layout the gate reads has moved: no worker
discarded anything, and the gate's reach is what the session repairs.

## The audit protocol (SPEC INV-46)

**The audit — a second pair of FRESH eyes, REQUIRED where the stakes are high and only the
author has judged the work (SPEC INV-46).** An audit is adversarial by nature: a whole-read that sets
out to break the work, refute its claims, and find its holes. Verify runs a fresh-context checker when the change is
HIGH-STAKES and its only review is the author's own. High-stakes means one of two things: the delta is
surface-sized (a new surface or a multi-file behaviour change), or the change edits the method itself — a
rule whose MEANING changed, a new or re-scoped invariant (a wording-only edit that changes no rule's
meaning is not a method edit). The author's own review means no independent read has happened, where an
independent read is a differently-contexted head briefed from the primary sources on the "goal missed"
hypothesis; a prover pass in the author's own context never counts as one, and delegation never makes the
review independent — the same head that briefed the worker reads the result. One fresh checker per landing
batch covers every law in the batch (SPEC INV-61 scales the audit's form, never its freshness). Brief the
checker with the SPEC sentences the landing claims (the anchors) and the artifact paths — primary sources
only: never the worker's summary, never the senior's own plan. Its opening
hypothesis is "tasks completed, goal missed". It walks each claimed fact up the ladder exists →
substantive → wired → flows, and greps for stubs: TODO · FIXME · placeholder · lorem · hardcoded sample ·
empty function body.

Findings become rows or red, never a nod, folded before the landing commits. The checker is a worker
under the full contract (checkpoint, ledger, clock), and its verdict rides the delivery report. Anywhere
else the checker is the senior's option. A skill or prose landing walks the ladder in its kind's form:
the checker re-reads the SHIPPED text against the spec sentences.
