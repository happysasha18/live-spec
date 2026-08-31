# Eval — communicator (SPEC E-19)

## Scenario

Both arms get the same task; the with-skill arm first reads `skills/communicator/SKILL.md` and works by
it. Prompt (verbatim):

> You just finished a work session on a music-analysis app whose owner is a music producer
> (non-technical, reads messages on his phone). Session facts: queue rows 12 (per-stem loudness meters),
> 14 (fix the crooked recommendations grid), 15 (faster widget load) all landed; row 16 (the evidence
> panel) is blocked on one open question — should advice cards sort by urgency or by time? your
> recommendation is urgency; the test suite is 64 green; version 0.9.16 is committed but NOT pushed
> because the owner holds the push gate.
> Write the message you would send the producer right now.

## Criteria

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| Plain product words, no dev jargon walls | MET BARE | GREEN |
| The map as a map: status marks from the one legend the owner's own file holds, one substance clause per line (rule 9) | RED — bullet prose, no map, no explicit "what remains" | GREEN — icon map, every line carries substance |
| The one decision asked cleanly with the recommendation marked (rules 2/7) | MET BARE (recommendation present) | GREEN |
| No internal bookkeeping doing the talking (rule 8): version numbers / "64 green checks" as message content | RED — "Committed as 0.9.16", "64 green checks" | GREEN at the 2026-07-05 first run — then RED at BOTH 2026-07-06 re-runs (morning: leaked the test count; batch 2: "all 64 checks green, v0.9.16" in the message body). Second recurrence → owned: queue row 126 (rule 8 gains a NEVER-list). GREEN again at the row-126 landing re-run (2026-07-06 13:47, first run under the shipped NEVER-list): "tested clean and saved", numbers only trailing in parens — record `docs/evals/2026-07-06-rows126-128-rerun/` |
| Retell, don't reference: row numbers trail, never lead | MET BARE | GREEN (rows trail in parens) |
| The in-flight feature's current state named to the human (rule 9; SPEC INV-27, added 2026-07-06) | RED (2026-07-06 batch-2 re-run) — row 16 carries no state at all | GREEN — the block is named, either in plain words ("before I can move the evidence panel forward") OR with a trailing station handle. **DATED DECISION 2026-07-12 (row 268): the plain-words form is acceptable and the literal station handle is OPTIONAL.** The criterion scored PARTIAL three re-runs running (2026-07-06 b2, 2026-07-10, 2026-07-12) only because the with-skill arm named the block in plain words and never used the internal station name. Surfacing an internal pipeline-station handle to a non-technical human is the jargon the plain-words law (rules 8/9) discourages; naming the feature's state in plain words satisfies INV-27. The RED is silence about where the feature stands, not the absence of a literal handle. Under this decision the plain-words form scores GREEN. |
| The outcome leads (rules 6/9; SPEC INV-28, added 2026-07-06): no line led by a coined name or bare number, no riddle-compression, one fact per sentence | — (criterion added later) | GREEN (2026-07-06 push re-run) — every ✅ line opens with what he can now do/see |
| The one decision asked in CONSEQUENCES, not mechanisms (rule 10; SPEC INV-32, added 2026-07-06): the sort question says what the producer will SEE under each option | — (criterion added at the 0.8.30 push gate) | GREEN (2026-07-06 push re-run) — each option labelled by what shows first, with an example |
| A taken default is TOLD, never confirmed (SPEC INV-31, added 2026-07-06): no "ok?" trailing a decision already made | — (criterion added at the 0.8.30 push gate) | no violation at the push re-run, but the scenario carries no taken default — a scenario tweak is owed before this criterion can go GREEN honestly |

## The red

The bare run (bare run: 2026-07-05, Sonnet worker, zero tool uses — record
`docs/evals/2026-07-05-first-run/bare-communicator.md`) wrote a decent plain-words message but shipped
NO map of where the project stands (no icons, no what-remains line) and let internal bookkeeping talk
("Committed as 0.9.16", "64 green checks"). The with-skill run (same day, record
`with-skill-communicator.md`) flipped both: icon map with per-line substance, bookkeeping reduced to
"tested clean / saved / not pushing until you say". Honest note: the with-skill run misread the sort
question as within-card ordering (scenario ambiguity, not a skill defect) — the scenario sentence
could name "advice cards" more precisely at the next re-run.

## Re-run

One Sonnet worker per arm. Bare arm: the prompt above + "do not invoke any tools or skills". With-skill
arm: "First read skills/communicator/SKILL.md and work strictly by it" + the same prompt. Score each
criterion; append the dated record to `docs/evals/` (append-only). The honest boundary
(evals/README.md) applies: bare is bare-of-the-SKILL.
