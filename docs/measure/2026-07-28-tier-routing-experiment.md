# The tier-routing experiment — a dispatch to the expensive tier proves its own need

Opened 2026-07-28 from queue row 507, stated here before any data arrived. The build it measures spends
money only on its middle step:

1. Patterns learned from past refusals turn a task away before any model call
   (`guardrails/check-tier-refusal.py --brief`). The list starts empty and grows from the record.
2. A dispatch to the expensive tier opens with one instruction, held as data in
   `guardrails/tier-refusal.json`: read the task, and stop when a cheaper tier does it as briefed,
   naming that tier. A refusal costs the brief plus one short line, and the orchestrator re-runs the
   same brief a tier down.
3. The full run proceeds when the first two let it through.

Every refusal lands in `docs/measure/tier-refusals.md` with its task text, its named tier, its reason,
and its date. A phrase that predicted a refusal three times is promoted to a pattern in step one.

## Hypothesis

A run that answers for its own need turns itself away often enough to move the tier mix, and the
refusals it leaves behind teach a check that costs nothing.

## The stated weakness

A run judging its own need leans toward yes. The instruction answers that by stating the cheap tier as
the default assumption, and the record makes the lean visible: refusals near zero over fifty expensive
dispatches means the instruction failed.

## Measures

All four are read from records that already exist.

- **Tier mix.** The share of helper runs on each tier per day, counted from the worker-run transcripts
  under the harness transcript root (the method is stated below).
- **Refusal rate.** The count of rows in `docs/measure/tier-refusals.md` against the count of expensive
  dispatches over the same days.
- **Spend.** The weekly spend from the usage report.
- **The cost of a wrong refusal.** The count of tasks re-run a tier down that came back needing the
  expensive tier after all. Such a task gets a second line in its record row's reason cell saying so.

## Baseline, first point: the evening of 2026-07-27, as row 507 recorded it

Twelve helper runs, six of them on the expensive tier, about two million output units across that
evening, and zero refusals — no instruction asked for one.

## Baseline, second point: this session, measured 2026-07-27 21:44Z

The session that built this experiment, read from its own transcripts while it was still running. The
numbers are a floor: work continued after the reading.

| Quantity | Measured |
|---|---|
| Worker runs on disk for the session | 29 |
| Dispatched by the seat | 25 — 15 on `claude-opus-5`, 10 on `claude-sonnet-5` |
| Dispatched by a worker inside its own run | 4, all on `claude-opus-5` |
| Expensive share of the seat's dispatches | 15 of 25 |
| Output units, the session and its workers together | 1,335,608 — 1,037,514 on `claude-opus-5`, 298,094 on `claude-sonnet-5` |
| Refusals | 0 — no instruction asked for one |

**How the runs were found.** The locator is the one `guardrails/check-worker-restore.py` reads: under
the harness transcript root (`~/.claude/projects`), every file matching
`<project-dir>/<session-id>/subagents/agent-*.jsonl` is one worker run. This session's runs sit under
the project directory `-Users-sashaabramovich` beside the session's own transcript
`14f2fe20-40cb-4760-b709-ef591b5eb05c.jsonl`, and its worker runs are the 29 files in the `subagents`
directory next to it.

**How the tiers were told apart.** Every assistant record in a run's transcript carries `message.model`.
Each of the 29 runs carried one model name throughout its records — `claude-opus-5` or
`claude-sonnet-5` — so no run's tier had to be guessed. The sidecar `agent-*.meta.json` beside each
transcript carries `agentType`, `description`, and `spawnDepth`, and it carries a `model` field on only
two of the 29 runs, so the transcript's own records are what the tier was read from. `spawnDepth` is
what separates the seat's own dispatches (depth 1) from the ones a worker made inside its run
(depth 2).

**Output units** were summed from `message.usage.output_tokens` over the same transcripts plus the
session's own, and split by the `message.model` on the same record.

## Decision rule, stated before the run

- The expensive share falls by a third or more and wrong refusals stay under one in ten: the
  instruction stays.
- The expensive share holds and refusals sit near zero: the instruction is judged inert, and the paid
  whole-record reading is tried instead.
- Wrong refusals pass one in ten: the instruction is rewritten toward caution.

## Duration

One week from the day it ships. Shipped 2026-07-28; the week ends **2026-08-04**, and the reading is
written under this heading on that day.

## Results

Empty until 2026-08-04. The rows counted are whatever `docs/measure/tier-refusals.md` holds then.
