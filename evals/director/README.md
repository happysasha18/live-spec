# Checking the Director by behaviour

The mandate closes package 1 when the Director's behaviour is checked by scenarios rather
than by searching its own skill file for required phrases. A phrase search passes on a
skill that says the right words and does the wrong thing, which is the failure mode this
whole rebuild exists to correct.

So the evidence here is a verdict the Director actually produced, from a real message,
graded by a program that had no part in producing it.

## The three parts, and why they are apart

| Part | What it is | Where |
|---|---|---|
| Fixtures | the messages and the expected verdicts | `scenarios.json` |
| Producer | a fresh agent holding only the skill and one message, returning a verdict | not in this directory — it is a run, not a file |
| Grader | deterministic comparison | `check.py` |

A grader that also produces the answer grades itself. A producer that can see the expected
verdict is not being tested. Both separations are load-bearing, and the second one was
learned the hard way — see *What the first run caught*, below.

## The fixtures

Thirty-five messages. Thirty-two are real, taken verbatim from this project's own
transcripts and anonymised: typos, shouting and swearing intact, because a Director that
only works on tidy sentences does not work. Three are written, covering classes the
transcripts held no example of — a thank-you, an answer to a question the Director itself
asked, and a pasted stack trace with no words around it.

Each fixture carries a `situation`. This is not padding. The skill's central claim is that
the same sentence is an idea, a correction or part of an instruction depending on what was
happening when it arrived, so a fixture without its situation would be testing the one
thing the skill says cannot be read: the wording alone.

Twenty-two of the thirty-five must produce no work at all. That ratio is the point. A
system that treats most messages as work is the system being replaced.

### What the expected verdicts grade, and how

Exactly: the acts, whether work is created, whether an idea is shelved, whether the turn
attaches to work already running, and how many separate pieces of work the turn produces.
These are the mandate's claims, and they are either met or not.

By inclusion: dimensions and specialists. A scenario names what must be present and what
must be absent and leaves the rest to judgment, because there is a defensible range there
and a grader that demanded one exact answer would be measuring conformity, not competence.

As a note, not a failure: an act the scenario did not ask for. The skill sets this price
itself, in *One turn, several acts* — "Naming one act too many costs a sentence. Naming one
too few loses what somebody said." A grader charging both the same is grading against a
cost model the skill does not hold, and it was: six of the nine reds in the 2026-08-26 run
were scenarios whose every material field was right and whose only defect was one act too
many. So an extra act is printed beside its scenario and counted in the closing summary,
where a producer drifting toward over-segmentation stays visible, and it does not redden a
scenario on its own. Everything else still does, an extra act beside it or not: a missing
act, a wrong boolean, a wrong `work_items`, a missing or forbidden dimension or specialist,
and a name that is not a speech act at all.

## Running it

Produce a verdict per scenario with a fresh agent that holds `skills/director/SKILL.md`
and one message — and nothing else, no repository, no other skills. Have it return the
shape `scenarios.json` describes under `verdict_shape`. Save each verdict as
`traces/<scenario id>.json`. Then:

```
python3 evals/director/check.py --all
python3 evals/director/check.py --scenario ONE.json --actual RUN.json
```

This costs a model call per scenario, so it is not on the push path and must not be put
there. It is a professional action, run when the skill changes, the way a review is.

Any change to `skills/director/SKILL.md` re-records all thirty-five scenarios, never a
subset, because a partial re-record leaves the untouched scenarios certified against a
skill version that no longer exists. The 2026-08-26 pass re-recorded only the nine reds of
the day and carried a score of 33 of 35 for days that a full re-record put at 26 of 35.

## Bare run

bare run: 2026-08-26 — all 35 traces regenerated against the skill as it stood that day
(`skill_version: 5.0.0`, commit `70a3d360`), graded with `python3 evals/director/check.py --all`:
26 of 35 pass. The full per-scenario breakdown, including the eight still-red and their
individual reasons, is carried in `PLAN.md`'s own record of that run rather than duplicated here —
one home per fact.

bare run: 2026-08-31 — all 35 re-recorded against `skill_version: 6.0.0`, one fresh producer
per scenario under the isolation protocol above, graded once: 34 of 35 pass, and five of those
named an act the scenario did not ask for. The single red is `idea-for-another-project`, where
the run read the message's imperative clause as a request to deliver the note now, against a
fixture that expects it shelved — a disagreement on all three material fields, with the extra
acts a consequence of it rather than the cause. The skill's text was
not touched for this run; what changed under it was the grader's cost model for an extra act and
`observation-carrying-its-repair`'s situation, both described above.

## What the first run caught

The first run was thrown away. The batches handed each agent the scenario's `id`, and the
ids were descriptive — one of them read `halt-with-a-reason-worth-keeping`. An agent said
so plainly in its report: the name told it what to answer. The question contained its own
answer.

Nothing in the harness detected this. An agent's honest account of its reasoning did. The
run was re-done with opaque labels, and the discarded run is recorded here because a
result that is thrown away is still a result.
