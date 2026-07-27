# Tier refusals — the record a free routing check is learned from

Opened 2026-07-28 for the routing experiment in queue row 507. A dispatch to the expensive tier opens
with one instruction: read the task, and stop when a cheaper tier does it as briefed, naming that tier.
Every stop lands here as one row. The rows are the whole evidence the experiment is judged on, and they
are the only source the learned patterns in `guardrails/tier-refusal.json` grow from.

**How a row is written.** One row per refusal, appended when the refusal arrives, left alone afterwards.
`Id` is the label a pattern cites, running TR-001, TR-002, and on. `Date` is the day of the refusal,
written YYYY-MM-DD. `Task` is the brief's own words, trimmed to the sentence saying what the work is and
copied word for word, since a phrase is later read out of it. `Named tier` is the tier the run named,
drawn from the ladder in `guardrails/tier-refusal.json`. `Reason` is one sentence
saying what makes the work fit that tier.

**What happens after a row lands.** The orchestrator re-runs the same brief a tier down. When the
re-run comes back needing the expensive tier after all, that row gets a second line in its `Reason`
cell saying so, which is the cost of a wrong refusal the experiment measures.

**How a row becomes a free check.** When three rows name the same tier and their task texts share a run
of words, that run of words is added to `patterns` in `guardrails/tier-refusal.json` with the three Ids
beside it. From then on `guardrails/check-tier-refusal.py --brief` turns a matching task away before any
model call. The gate re-reads the three rows on every run, so a pattern whose evidence was edited away
reds.

**Where the numbers go.** The experiment's own record is `docs/measure/2026-07-28-tier-routing-experiment.md`:
the hypothesis, the measures, the baselines, and the decision rule. This file holds the raw rows it counts.

| Id | Date | Task | Named tier | Reason |
|---|---|---|---|---|
