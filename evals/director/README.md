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

## What the first run caught

The first run was thrown away. The batches handed each agent the scenario's `id`, and the
ids were descriptive — one of them read `halt-with-a-reason-worth-keeping`. An agent said
so plainly in its report: the name told it what to answer. The question contained its own
answer.

Nothing in the harness detected this. An agent's honest account of its reasoning did. The
run was re-done with opaque labels, and the discarded run is recorded here because a
result that is thrown away is still a result.
