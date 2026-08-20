# The verify step in detail

The two long passages of `SKILL.md`'s verify step, referenced from the step itself: the worker-restore
gate's own reading, and the audit protocol. Every line below reads exactly as it read in the body.

## The worker-restore gate at verify (SPEC INV-298; the gate INV-299)

**Keep the transcript path for every worker result. Before accepting that result, run `python3
guardrails/check-worker-restore.py --run <exact-agent-jsonl>` and read its verdict (SPEC INV-298; the
gate INV-299).** The exact path is the `agent-*.jsonl` file for that worker run, not the session root
and not whichever file is newest. This mode has no clock window, counting start, or project-owner
downgrade: it judges the result being accepted wherever and whenever it ran.

A red names the run, command, paths, and shell outcome. Reject that result. Recover the named file
from the last committed stage, give the worker a fresh brief carrying the file's current bytes, and
check the fresh run by its own path. Never make the original run green: it remains a real finding in
the forensic census. `python3 guardrails/check-worker-restore.py --all` reads that census when an
investigation needs it; its time window and counting start describe history and never decide whether
a later worker result is acceptable. A missing or empty exact run is red because it proves nothing.

## The audit protocol (SPEC INV-46)

**The audit — a second pair of FRESH eyes, REQUIRED where the stakes are high and only the
author has judged the work (SPEC INV-46).** An audit is adversarial by nature: a whole-read that sets
out to break the work, refute its claims, and find its holes. When the audit FIRES — what high-stakes
means and what counts as the author's own review — stands in `SKILL.md` at the verify step: that is the
gate's firing condition and belongs where the step is walked. What follows is how the audit is run once
it has fired. One fresh checker per landing
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
