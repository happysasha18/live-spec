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

Thirty-six messages. Thirty-two are real, taken verbatim from this project's own
transcripts and anonymised: typos, shouting and swearing intact, because a Director that
only works on tidy sentences does not work. Four are written, covering classes the
transcripts held no single example of — a thank-you, an answer to a question the Director
itself asked, a pasted stack trace with no words around it, and the shaping turn added
2026-09-03 for `PLAN.md`'s q-812, where the person invites ideas, names four possibilities
and settles one of them in the same breath.

Each fixture carries a `situation`. This is not padding. The skill's central claim is that
the same sentence is an idea, a correction or part of an instruction depending on what was
happening when it arrived, so a fixture without its situation would be testing the one
thing the skill says cannot be read: the wording alone.

Twenty-two of the thirty-six must produce no work at all. That ratio is the point. A
system that treats most messages as work is the system being replaced.

### What the expected verdicts grade, and how

Exactly: whether work is created, whether an idea is shelved, whether the turn attaches to
work already running, and how many separate pieces of work the turn produces. These are the
mandate's claims, and they are either met or not. Every act a scenario expects is graded
exactly the same way — each one has to show up, or the scenario is red.

By inclusion: dimensions and specialists. A scenario names what must be present and what
must be absent and leaves the rest to judgment, because there is a defensible range there
and a grader that demanded one exact answer would be measuring conformity, not competence.

As a note, not a failure, but only when the scenario expects a real act: an extra act beside
one or more expected ones. The skill sets this price itself, in *One turn, several acts* —
"Naming one act too many costs a sentence. Naming one too few loses what somebody said."
That passage prices splitting one real act that happened into two, and a grader charging
that the same as a missed act was grading against a cost model the skill does not hold, and
it was: two of the nine reds in the 2026-08-26 run were scenarios whose every material field
was right and whose only defect was one act too many beside a real one (re-derived directly
against that commit's traces). So an extra act beside an expected one is printed beside its
scenario and counted in the closing summary, where a producer drifting toward
over-segmentation stays visible, and it does not redden a scenario on its own.

When a scenario expects no act at all, an extra one is a different mistake, priced in the
skill's own *Not every message is one of the seven* — "Reaching for one of the seven acts
here is how a thank-you becomes a roadmap row." That is not a real act split in two; it is
an act invented where none happened, and it fails.

Everything else still fails, an extra act beside a real one or not: a missing act, a wrong
boolean, a wrong `work_items`, a missing or forbidden dimension or specialist, an act named
where the scenario expects none, and a name that is not a speech act at all.

## The second, smaller eval in this directory

`scenarios.json` and its thirty-six traces test the first stage only: a message arrives and the
Director decides which of the seven acts it carries. `closing-scenarios.json` tests what happens
after that, and the two must not be read as one score. Eight of its nine fixtures start where the
other set stops — work was accepted, built and verified — and ask the one question left: does the
Director close it now, or hold it and put a question to the person first. The rule they test landed
2026-09-02 with `PLAN.md`'s q-810: a shown, ordinary delivered result closes the checkpoint in the
same step, and the wait for the person is reserved for a taste call, a trade-off no artifact
settles, a change to the definition of correct, or an action irreversible outside git, which stops
before it runs. The ninth fixture sits at the opposite end of the same skill, the moment the
decision sheet is written: a request that contradicts a decision already on record, where the rule
landed the same night has the Director say so before the checkpoint opens rather than build it
silently, and proceed on the person's word once they have heard it. Both are the same question
asked twice — when does the Director act on its own, and when does it speak. Same
method as the larger set and the same three parts kept apart — fixtures here, one fresh producer
per scenario holding the skill and nothing else, opaque two-letter labels, and a grader that had no
part in producing the verdicts. What differs is where the grading lives: nine recorded runs and two
graded fields do not earn a second `check.py`, so the comparison sits in
`tests/test_director_scenarios.py` and runs with the suite. Recorded runs are in `closing-traces/`,
the run record and its score are in the fixture file itself, and the suite reds when the Director's
own text has changed since the runs were recorded. That last pin reads the skill's content rather
than its declared version: the Director's text moved three times on the day these fixtures were
written and its declared version moved none of them, so a version pin would have read fresh across
every edit it exists to catch — and a stale score that reads as a fresh one is the failure this
directory already has on record. The first recording of the closing runs was thrown out under that
same pin when the skill changed an hour later, and the whole set was recorded again.

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

Any change to `skills/director/SKILL.md` re-records all thirty-six scenarios, never a
subset, because a partial re-record leaves the untouched scenarios certified against a
skill version that no longer exists. The 2026-08-26 pass re-recorded only the nine reds of
the day and carried a score of 33 of 35 for days that a full re-record put at 26 of 35.

A scenario added while the skill's own text stands still is the one case that takes a single
run: its run is the only one missing, and the thirty-five already on file were recorded
against the same bytes the new one was. The rule above binds a change to the skill, and this
is a change to the fixtures.

## Bare run

bare run: 2026-08-26 — all 35 traces regenerated against the skill as it stood that day
(`skill_version: 5.0.0`, commit `70a3d360`), graded with `python3 evals/director/check.py --all`:
26 of 35 pass. The full per-scenario breakdown, including the nine still-red and their
individual reasons, is carried in `PLAN.md`'s own record of that run rather than duplicated here —
one home per fact.

bare run: 2026-08-31 — all 35 re-recorded against `skill_version: 6.0.0`, one fresh producer
per scenario under the isolation protocol above, graded once: 34 of 35 pass. Five runs in
total named an act the scenario did not ask for — four of the 34 passing runs, plus the one
red run below, whose own failure is a material field rather than the extra act. The single
red is `idea-for-another-project`, where the run read the message's imperative clause as a
request to deliver the note now, against a fixture that expects it shelved — a disagreement
on all three material fields, with the extra acts a consequence of it rather than the cause.
The skill's text was not touched for this run; what changed under it was the grader's cost
model for an extra act and `observation-carrying-its-repair`'s situation, both described
above.

bare run: 2026-09-02 — two full re-records on the same afternoon, one producer per scenario under
the isolation protocol above, opaque labels. The pair was run as a control, because a change to
`skills/director/SKILL.md` had cut it from 25,613 to 21,900 bytes and the question was whether the
cut cost anything. Same producers, same hour, the only difference the skill text:

| skill text | score |
|---|---|
| the skill as it stands (25,613 bytes) | 30 of 35, 2 extra acts |
| the same skill cut to 21,900 bytes | 29 of 35, 4 extra acts |

The cut was withdrawn before it was committed, so no change to the skill reaches git from this
pair: the traces below are recorded against the skill as it already stood. One scenario is inside
what this method can see, so the run does not certify the cut either way, and 3.7 KB is a small
saving to take on an unresolved question at the pack's front door.

The 34-of-35 line above and the 30-of-35 line here read the same skill text and are not comparable
with each other: they were produced on different days by different producers, which is the whole
point of the paragraph below.

**What the pair established about the method itself.** While the second run was still finishing,
its partial trace set graded 32, then 31, then 30 as the last producers landed. Nothing about the
grader changed between those readings — the grader is deterministic on a fixed trace set, and was
re-checked to be so. What moved was the trace set. So a single bare run's score carries about two
scenarios of producer variance, and a score quoted to the scenario reads more precisely than the
method can support. Two scores from separate runs are comparable when they differ by more than
that, and a change worth a re-record should be large enough to clear it. Grade only a complete
trace set: a partial one reports a number that is still moving.

single-scenario run: 2026-09-03 — `idea-shaping-then-one-decided`, the shaping turn `PLAN.md`'s
q-812 asked for, recorded by one fresh producer under the isolation protocol above: it held the
skill's text and the scenario's situation and message, was handed the opaque label TK, read no other
file, and never saw the expected verdict. The run passes its fixture. The set grades 32 of 36,
against 31 of 35 before it, so the one added pass is the whole of the difference — and that number
is a mixed reading rather than a score for today's skill: `skills/director/SKILL.md` changed at
10:28 the same morning, the idea shelf coming out of it, so the other thirty-five runs are stale
under this directory's own freshness pin and the probe already prints them as a replay. The full
re-record is held on purpose, so one pass covers the whole night's edits to that file. This run is
the only one on file recorded against the text as it stands.

The producer's verdict disagreed with the fixture author's expectation on one field: it read the
three unchosen possibilities as answered and let go rather than shelved, quoting the skill's rewritten
idea rule back. The fixture grades neither answer. Where the shelf stood that morning and stands no
longer, a fixture forcing one of the two would be grading the version of the rule its author happened
to read.

bare run: 2026-09-03 (afternoon) — a full re-record of both sets, triggered by today's changes to
`skills/director/SKILL.md`: the idea-shelf mechanism added then retired, "the Director runs the
project" rule, and the disagreement-before-executing rule carried further than the single-scenario
run above had seen. Skill as it stands: `skill_version: 6.1.0`, commit `614cc25e`, `skill_sha256`
`44b427838c14701ce04098a20a0425239c2e4becf253d57bbd07f34a76ea995b`. One fresh producer per scenario
under the isolation protocol above — opaque two-letter labels, no producer given another's fixture
or the expected verdict, all forty-five run in one afternoon.

The thirty-six-scenario set, graded with `python3 evals/director/check.py --all`: 31 of 36 pass,
against 30 of 35 in the last full re-record before it (2026-09-02, the skill as it stood that
afternoon). Three runs named an act the scenario did not ask for, against two in that prior run.
The five reds: `idea-plus-a-fact` (wanted `shelves_idea: true`, got `false` — the run read the
person's own "дальний бэклог" hedge as too unspecified to keep rather than as the reason that keeps
it); `decision-how-to-report` (missing the secondary `instruction` act — "веди план и показывай мне
где мы находимся" read as a standing decision alone, not decision-plus-today's-own-request);
`mixed-reminder-and-a-challenge` (the same miss — the reminder to monitor two goals read as decision
alone, not decision-plus-instruction); `mixed-conditional-pause` (missing the `observation` act —
"надо этот комп отключить ненадолго" folded into the halt's own grounds instead of standing as its
own fact); `not-an-act-answering-the-director` ("yeah go ahead" graded as a decision reaffirming the
open choice rather than the instruction the skill's own rule says it becomes — "the idea just became
the instruction it was waiting to become" — so the primary act itself disagrees with the fixture,
with an extra `decision` beside the miss).

The nine-scenario closing set, graded with `python3 -m pytest -q tests/test_director_scenarios.py`
(`recorded_run.skill_sha256` in `closing-scenarios.json` re-pinned to today's file): 7 of 9 pass. Two
reds, both a disagreement on the boolean itself rather than a wording gap: `close-a-row-whose-own-
line-names-his-eye` (the run reads the row's own stale "his own eye is the check" acceptance line as
still binding, not as exactly the wording the closing rule refuses, and holds the checkpoint open
where the fixture expects it closed); `close-a-redefinition-the-person-himself-ordered` (the run
treats a person-ordered redefinition of what correct means as itself one of the three reserved cases,
not as the fork the rule closes over once the person, not an open question, made the call).

bare run: 2026-09-03 (night) — a full re-record of both sets, triggered by the same night's follow-on
commit `85ddbda0` ("Adopt: a verdict on shown work is a movement end for its artifact"), which added a
paragraph on top of the afternoon's already-recorded text: for the three taste-call cases rule 12/27
reserve for him, his verdict on the shown artifact is itself that artifact's movement end, and belongs
in the resume files in the same minute rather than after the conversation it triggers runs on. Skill as
it stands: `skill_version: 6.1.0`, commit `85ddbda0`, `skill_sha256`
`55806109032985f9b7bb00a94242e7c6c112c67039fcfa7f58e6f9c2aee2d684`. One fresh producer per scenario
under the isolation protocol above — opaque two-letter labels, no producer given another's fixture or
the expected verdict, all forty-five run in one pass.

**Re-recorded 2026-09-04 against the skill as it stands after that night's edits, `skill_sha256` `b9e49a8a92cfc7352dd82617ed414b93fbfbb7a07f8a11fc8966690b26ee6a72`: 30 of 36 on the main set and 7 of 9 on the closing set.** Six main-set reds, and four of them are one shape: a correction read as new work, opening a row where the scenario asks for the running work to be replanned. Two closing-set reds flipped back to deferring to a row's own stale gate. Read the three recorded runs together before drawing a line through them — 31 of 36, then 34, then 30, on a skill whose text moved a little between each — the spread is wider than most of the differences anyone reads into a single run. What the number can carry is a shape that repeats across runs, and the correction shape is one.

The thirty-six-scenario set, graded with `python3 evals/director/check.py --all`, on the 2026-09-03 night run: 34 of 36 pass,
against 31 of 36 in the last full re-record before it (2026-09-03 afternoon, commit `614cc25e`). Two
runs named an act the scenario did not ask for (`idea-with-a-cheap-branch`, `correction-stop-counting-
pairs`), both notes rather than fails under the extra-act cost model. The two reds: `decision-how-to-
report` (missing the secondary `instruction` act — "с этого момента веди план (краткий, без умных слов)
и показывай мне всегда «где мы находимся»" read as one standing decision alone, not decision-plus-a-plan
that does not yet exist and was asked for); `mixed-plan-and-two-questions` (missing the secondary
`observation` act — "я ему все скопировал и запустил" read as grounds for the question that follows
rather than as its own reported fact).

The nine-scenario closing set, graded with `python3 -m pytest -q tests/test_director_scenarios.py`
(`recorded_run.skill_sha256` re-pinned to tonight's file): 9 of 9 pass — the first clean pass this set
has on record. Both scenarios red in the afternoon run (`close-a-row-whose-own-line-names-his-eye`,
`close-a-redefinition-the-person-himself-ordered`) passed this time: the added paragraph does not touch
the closing rule or the disagreement rule those two scenarios exercise, so this reads as the producer
variance the 2026-09-02 control pair already put on record clearing on this draw, not as the new
paragraph fixing anything.

## What the first run caught

The first run was thrown away. The batches handed each agent the scenario's `id`, and the
ids were descriptive — one of them read `halt-with-a-reason-worth-keeping`. An agent said
so plainly in its report: the name told it what to answer. The question contained its own
answer.

Nothing in the harness detected this. An agent's honest account of its reasoning did. The
run was re-done with opaque labels, and the discarded run is recorded here because a
result that is thrown away is still a result.
