# The verifier in detail

Referenced from `SKILL.md`'s Execution section. Extracted from
`skills/build-pipeline/references/verify-step-detail.md` and `skills/build-pipeline/SKILL.md`'s own
verify step (SPEC INV-46/INV-298/INV-299) — the mechanics are unchanged from the pipeline this pack
replaces; only the caller changed, from a fixed pipeline stage to a step the Director calls by
decision.

## When a fresh checker is required (SPEC INV-46)

Not every landing earns one. It fires when the change is high-stakes AND its only review so far is
the author's own.

**High-stakes means one of two things.** The delta is surface-sized — a new surface, or a multi-file
behaviour change. Or the change edits the method itself — a rule whose meaning changed, a new or
re-scoped invariant. A wording-only edit that changes no rule's meaning is not a method edit.

**The author's own review means no independent read has happened.** A differently-contexted head,
briefed from the primary sources on the "goal missed" hypothesis, is independent. A prover pass run
in the author's own context never counts as one. Delegation never makes the review independent either
— the same head that briefed the worker reading the worker's result is still the author's own review.

Below the bar, the Director's own re-check against the decision sheet's observable outcome is enough.
Above it, call a fresh checker.

## The worker-restore gate at verify (SPEC INV-298; the gate INV-299)

Keep the transcript path for every worker result. Before accepting that result, run `python3
guardrails/check-worker-restore.py --run <exact-agent-jsonl>` and read its verdict. The exact path is
the `agent-*.jsonl` file for that worker run, not the session root and not whichever file is newest.
This mode has no clock window, counting start, or project-owner downgrade: it judges the result being
accepted wherever and whenever it ran.

A red names the run, command, paths, and shell outcome. Reject that result. Recover the named file
from the last committed stage, give the worker a fresh brief carrying the file's current bytes, and
check the fresh run by its own path. Never make the original run green: it remains a real finding.
`python3 guardrails/check-worker-restore.py --all` reads the full census when an investigation needs
it; it never decides whether a later result is acceptable on its own. A missing or empty exact run is
red because it proves nothing.

## The audit protocol, once it has fired

One fresh checker per landing batch covers every claim in the batch — its scope grows with the batch,
its freshness never shrinks. Brief the checker with the primary sources the landing claims to satisfy
(spec sentences, requirement codes, the decision sheet's observable outcome) and the artifact paths —
never the worker's summary, never the Director's own plan. Its opening hypothesis is "tasks completed,
goal missed." It walks each claimed fact up the ladder exists → substantive → wired → flows, and greps
for stubs: TODO · FIXME · placeholder · lorem · hardcoded sample · empty function body.

Findings become blocking or a recorded pass, never a nod, resolved before the landing closes. The
checker is itself a worker under the same brief contract as any other (a self-contained brief, a named
write-set, no silent restore) — see the checkpoint-mechanism pattern this pack's own recent history
used: the fix a checker rejects goes back to the original author, and the SAME checker re-verifies the
fix rather than a different one taking its word.
