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

Every scenario's expected verdict now also carries an `operation` beside its `acts`, naming
the state transitions T1–T9 the turn runs on the plan's own tickets, or `none` when it runs
none. The grader compares it only when the recorded run carries the field too, so the
thirty-six runs recorded on 2026-09-06 stay valid unchanged — they predate the field and are
skipped on it rather than failed. The field is required of the next recording: a producer
writing a verdict from here on names the operation the turn runs, or `none`.

## The former closing eval moved to build-pipeline

Execution left Director on 2026-09-05. The closing fixtures and their historical traces now live in
`../build-pipeline/`; its README marks them stale until fresh producers run against the new pipeline.

`scenarios.json` and its thirty-six traces test the first stage only: a message arrives and the
Director decides which of the seven acts it carries. `../build-pipeline/closing-scenarios.json` tests what happens
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
`tests/test_director_scenarios.py` and runs with the suite. Recorded runs are in `../build-pipeline/closing-traces/`,
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

## What a run reports, and what it does not

A run reports which scenarios failed and what shape those failures share. The count of passes is a
byproduct of that, and it is never quoted as the result of a change.

The reason is on record in this file already. Three full re-records of this set, on a skill whose
text moved a little between them, read 31, then 34, then 30; the 2026-09-02 control pair watched a
single run's own partial score walk 32, 31, 30 as its last producers landed, on a grader that is
deterministic. So one run's score carries about two scenarios of producer variance, and a line drawn
through one number is drawn through noise.

So a scenario counts as failing when it fails on two separate recordings. A single red on a single
run is a draw: it is named in that run's own notes and left there. A shape that repeats across
recordings — several scenarios failing the same way, as the correction shape did on 2026-09-04 — is
what a run can carry, and it is what a run is read for.

Measuring the spread itself is refused on purpose. Learning how far a score moves on its own means
running the set repeatedly to find out, which buys a number that changes nothing about what to fix.
Reading the shape costs nothing and answers the same question.

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
(`recorded_run.skill_sha256` in `../build-pipeline/closing-scenarios.json` re-pinned to today's file): 7 of 9 pass. Two
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

bare run pair: 2026-09-04 (afternoon) — two full re-records of both sets, one after the other, made
for `PLAN.md`'s q-820. The skill's own text was edited first: the correction rule now says in the
numbers a verdict carries that replanning work already running produces zero new pieces of work and
opens no row; it names the two clauses that ride inside a correction (the repair stated aloud, and
the part of the goal being withdrawn) as belonging to it; a new paragraph splits a standing clause
by which half of it is new, so a judgment about the product stays an observation and a rule for
what happens from here on is a decision; and the dimensions section says a turn that accepted no
work names no dimension and calls no specialist. One apparatus repair went with it, declared in
`scenarios.json`'s own corrections list: the `shelves_idea` field's description named the idea shelf,
a mechanism the skill retired on 2026-09-03, so a producer reading the skill correctly had to answer
false to a question about a shelf that does not exist. Its description now asks which road the idea
took. No fixture's expected value moved.

Skill as it stands: `skill_version: 6.1.0`, `skill_sha256`
`99a79b438a2d83f2419f593766135ceea3c6444fbac447c62c1f051acf593bcd`. One fresh producer per scenario
under the isolation protocol above, opaque two-letter labels drawn fresh for each of the two
recordings, no producer given another's fixture or the expected verdict.

| set | first recording | second recording |
|---|---|---|
| the thirty-six | 34 of 36 | 32 of 36 |
| the closing nine | 8 of 9 | 8 of 9 |

The runs on file are the second recording of the pair. Read by the rule this file now states — a
scenario counts as failing when it fails on two separate recordings — three scenarios are red and
two are draws.

Red on both recordings:

- `idea-for-another-project` — the run takes the note as work to write now and routes a dimension
  for it, against a fixture that expects it raised as a question and nothing accepted.
- `decision-how-to-report` — "с этого момента веди план… и показывай мне всегда «где мы находимся»"
  read as one standing decision, missing that it also asks for a plan that does not exist yet. This
  is the oldest disagreement on file: it is red in every recording this directory has kept.
- `close-a-redefinition-the-person-himself-ordered` — a redefinition the person himself ordered read
  as one of the three cases the closing rule reserves, rather than as the fork his own word already
  settled.

Draws, carried and left alone: `mixed-reminder-and-a-challenge` and `mixed-conditional-pause`, each
red on the second recording and green on the first.

What the pair was made to check: the four scenarios where a person corrects work already running —
`correction-stop-counting-pairs`, `correction-shouted-constraint`, `correction-widening-the-goal`,
`mixed-you-invented-that-work`. All four pass on both recordings. On the recording before the skill
was edited, three of the four failed the same way: the run read the correction as work of its own,
returned one new work item, and in one case set `creates_work` true, which is the second row opening
beside the one that should have been replanned.

## What the first run caught

The first run was thrown away. The batches handed each agent the scenario's `id`, and the
ids were descriptive — one of them read `halt-with-a-reason-worth-keeping`. An agent said
so plainly in its report: the name told it what to answer. The question contained its own
answer.

Nothing in the harness detected this. An agent's honest account of its reasoning did. The
run was re-done with opaque labels, and the discarded run is recorded here because a
result that is thrown away is still a result.

bare run pair: 2026-09-06 — two full re-records before a change to `skills/director/SKILL.md`, the
edit, and two more after it. Made for `PLAN.md`'s q-822. The Director's text had moved since the last
recording, so all thirty-six were re-run, never a subset. One fresh producer per scenario under the
isolation protocol above: it held the skill's full text, one scenario's situation and message, the
required JSON shape and an opaque two-letter label drawn fresh for each of the four recordings, and it
saw no repository, no fixture, no expected verdict and no other producer's answer. Producer model:
Opus, the tier that runs the Director in real sessions, for all one hundred and forty-four runs.

Before the edit, `skill_sha256` `e0e922c67863dd3124dc90c814fadfda2d292071149239baac84a1d25bca3ed0`
(21,439 bytes):

| recording | score | extra acts |
|---|---|---|
| first | 32 of 36 | 6 |
| second | 32 of 36 | 7 |

Both recordings failed on the same four scenarios, with the same failure lines on each — no scenario
was red in one recording only, so the pair reports no producer variance at all this time, against the
roughly two scenarios of spread the 2026-09-02 control pair put on record.

The shapes, which is what the pair was run to read:

- **A standing rule swallows the thing it asks for.** `decision-how-to-report` and
  `mixed-reminder-and-a-challenge`, red on both recordings. Both runs named the standing decision,
  quoted this file's own "always deploy without asking, and deploy this one" passage back, and
  concluded there was no second half asking for anything today — so `creates_work` false and zero
  work items, where the person had asked for a plan that does not exist and for status lines that are
  not in the plan file yet. The rule as it stood only recognised the demand when it arrived as its own
  separate clause. This is the oldest disagreement in this directory: `decision-how-to-report` is red
  in every recording kept here.
- **An idea aimed at another project becomes work here.** `idea-for-another-project`, red on both.
  The imperative inside the idea — send live-spec the note — reads as a result wanted now, so one new
  piece of work and a dimension routed for it, against a fixture that expects the idea half handled as
  an idea and nothing accepted. Red on all four recordings on 2026-09-04 and 2026-09-06.
- **An observation about work in flight does not attach to it.** `observation-carrying-its-repair`,
  red on both. Both runs reasoned that the report changes neither the goal nor the constraints of the
  open checkpoint, so nothing attaches — reading `attaches_to_existing_work` as "changes that work"
  where the fixture reads it as "lands on it".

**The edit.** One sentence added to *No act absorbs another*, `skills/director/SKILL.md:148`, beside
the deploy example that names the same rule: the demand does not need a clause of its own — a rule
about how something is kept, reported or shown also asks for that thing, and where it does not exist
yet, making it is what the person wants today. Classification only; it adds no execution rule. The
file went from 21,439 to 21,691 bytes, and the paragraph was re-wrapped to the file's own width.
After the edit, `skill_sha256` `0852e4f0557e4b337548c3aea0c47f5d0150dc3d3115f3a2fb35542b91579473`.

The whole set was then recorded twice more against the edited text, fresh producers and fresh labels
again:

| recording | score | extra acts |
|---|---|---|
| third (first after the edit) | 35 of 36 | 5 |
| fourth (second after the edit) | 35 of 36 | 7 |

`decision-how-to-report` and `mixed-reminder-and-a-challenge` pass on both post-edit recordings, which
is the shape the edit was made for. `observation-carrying-its-repair` also passes on both, and the
edit does not touch the rule that scenario exercises, so that one reads as the producer variance this
file already warns about clearing on this draw rather than as anything the sentence fixed.

`idea-for-another-project` stayed red on both of those recordings, and the second edit below is what
closed it.

**The second edit, and the third pair.** The first reading of that red called it a fixture problem,
because the fixture's own reason named shelving — "'Кинь идею' asks for the idea to be recorded,
which is what shelving is" — and the shelf is a mechanism the skill retired on 2026-09-03. That
reading was wrong about which file was at fault. "Кинь лайвспеку идею" asks for a note to be handed
to another project, and the pack's boot file already sanctions exactly that one cross-project act: a
session may drop one new wish file into a project's `inbox/`. Handing a note over is done in the same
turn as an answer. It has no goal of its own, no definition of done, no decision sheet, and it opens
no row on this board — which is what the fixture's `expect` fields say, in today's vocabulary, whatever
word its prose used. The expectation stands; only the reason needed rewording, and `scenarios.json`'s
`why` for that fixture now reads "'Кинь идею' asks for the idea to be handed on, which is done in the
turn; handing on an idea is not doing it." No `expect` value moved, and nothing else in the fixture
file changed.

The skill gained one more classification sentence, in *An idea is not an instruction*
(`skills/director/SKILL.md:61`): where the ask is to hand the idea itself to someone — tell another
project, drop it in their inbox — that is passing a message, done in the turn like an answer, no row
and no work item; an ask that makes something exist is an instruction as usual. The first draft of it
left off that last clause and generalised to any handover, and the recordings caught it immediately:
`instruction-one-goal-two-steps` went red on both, both producers quoting the new sentence back to
justify returning zero work items for "скинь отчет в файл… дай путь к файлу" — a file that does not
exist yet. That draft is on record here rather than quietly dropped, because it is the same failure
this directory keeps finding: a rule stated one clause too wide. The pair recorded against it scored
34 and 32 of 36. The clause was added, and the whole set recorded twice more.

Skill as it stands: `skill_version: 6.1.0`, `skill_sha256`
`94986245598fc5b3a97b7548e49a2e7cf58c3cd5dfa2f9c24aecac9232a3d79b`, 21,977 bytes, against 21,439 at
the start of the day.

| recording | score | extra acts |
|---|---|---|
| fifth (first after the narrowed sentence) | 36 of 36 | 6 |
| sixth (second after it) | 34 of 36 | 6 |

The fifth is the first clean sweep this set has on record. The sixth is red on
`observation-carrying-its-repair` and `mixed-check-now-improve-later`, and the intersection of the two
recordings is empty, so by this file's own rule both are draws and neither is a defect. All four
scenarios the day's two edits were aimed at — `decision-how-to-report`, `mixed-reminder-and-a-challenge`,
`idea-for-another-project` and the `instruction-one-goal-two-steps` regression — pass on both.

`observation-carrying-its-repair` is worth a line on its own, as an instance of the variance this file
warns about rather than as a finding. Across the day's four pairs it read red, red / green, green /
red, red / green, red, on a fixture nothing in either edit touches. A score quoted to the scenario
would have told three different stories about it.

The runs on file are the sixth recording, following the precedent of the 2026-09-04 pair — the second
of the pair, not the better of the two. The fifth is kept outside the tree for comparison, in this
session's scratchpad (`.../scratchpad/director-run7/`), together with the four earlier recordings of
the day. Only traces produced from the final skill text are in `traces/`; no trace was hand-edited,
and every hash on file was pinned by the run behind it. Final grading:
`python3 evals/director/check.py --all` prints
`34 of 36 recorded runs pass; 6 named an act the scenario did not ask for`.

Eight full recordings went into this entry — two hundred and eighty-eight producers, all Opus, one per
scenario, none of them seeing the repository, the fixture, the expected verdict, or another producer's
answer.

bare run pair: 2026-09-06 (evening) — a third pair the same day, recorded because the traces had no
`operation` field. q-823 closed on the arm "the grader reads that field", and it was firing on none of
the thirty-six: every scenario's `expect` names an operation, but the runs on file predated the field,
so `check.py` skipped it on all thirty-six and the arm was vacuous. A gate that skips every case it
was built for passes for the same reason a phrase search passes — the failure this whole directory
exists to catch, one level up.

The Director's own text did not move: `skill_sha256`
`94986245598fc5b3a97b7548e49a2e7cf58c3cd5dfa2f9c24aecac9232a3d79b`, 21,977 bytes, the same file the
day's third pair was recorded against. This pair changes nothing about the Director and measures one
field that was never measured before.

Two apparatus changes went with it, both outside the skill. `scenarios.json`'s `verdict_shape` entry
for `operation` now spells the closed set out in the producer's own terms — what T1 through T9 each
are, and when the answer is `["none"]` — taken from the contract's section 7A and its transition
table. The old wording named "the closed set T1..T9 of the product contract's state machine", which a
producer holding only the skill and one message cannot resolve: it had the vocabulary's name and not
its content. No fixture's `expect` moved. And `check.py` now requires the field on any run recorded on
or after `OPERATION_REQUIRED_FROM` (2026-09-06) — a missing `operation` on such a run fails its
scenario, the same as a missing act — while older recordings stay skipped on that one field, because
the field did not exist when their producers answered and no re-reading can invent it.

| recording | score | extra acts |
|---|---|---|
| seventh (first of this pair) | 23 of 36 | 6 |
| eighth (second of this pair) | 23 of 36 | 6 |

Both recordings score 23, and the drop from 34 is almost entirely one field. Read apart:

- **Act and boolean reds.** `observation-carrying-its-repair` on both (`attaches_to_existing_work`
  again), and `mixed-check-now-improve-later` on the first only (`work_items` 2 for 1). The same two
  scenarios, and the same oscillation, the day's earlier pairs already recorded.
- **Operation reds.** Thirteen on each recording, twelve of them shared. This is not spread: it is
  one shape with a long tail.

The shape, on eight scenarios in the first recording and seven in the second: **a run answers
`["T1","T2"]` where the fixture wants `["T1"]` alone** — `instruction-one-pass`,
`instruction-a-procedure`, `instruction-one-goal-two-steps`, `decision-how-to-report`,
`decision-and-instruction-together`, `idea-shaping-then-one-decided`, `mixed-plan-and-two-questions`,
`mixed-four-at-once`, `mixed-check-now-improve-later`, `not-an-act-a-bare-trace`. The producers are
reading the contract's own sentence — an instruction accepted right now runs T1 and T2 as one
operation — and answering with both, where every fixture in the set records the admission alone. That
sentence reached the producers through the `verdict_shape` text this pair introduced, so the run
cannot separate a Director that over-names T2 from a shape description that invited it. Either the
fixtures mean T1 to stand for admission-and-take-up together, or the shape must stop naming T2 at
all; this is a question for whoever owns the fixtures, and it is not answered by re-running.

Three smaller operation forms, each on both recordings: `decision-a-boundary` answers `["T1"]` where
the fixture wants `["none"]` (a boundary rule read as a ticket); `mixed-conditional-pause` answers
`["T6"]` where the fixture wants `["none"]`; `halt-with-a-reason-worth-keeping` answers `["T9"]`
where the fixture wants `["T6"]` — abandon read for park. `observation-carrying-its-repair` answers
`["none"]` against `["T3"]`, which is the operation-side face of the same disagreement its boolean
red has carried all day.

The runs on file are the second recording of the pair, by the standing precedent. The first is in
this session's scratchpad (`.../scratchpad/director-run9/`). All thirty-six carry `operation`, and
`grep -l '"operation"' evals/director/traces/*.json | wc -l` prints 36. The score of 23 is kept as it
came: a real number on a field measured for the first time is the point of the exercise, and a score
recovered by loosening the fixture it is measured against would be worth nothing.

bare run pair: 2026-09-06 (late) — the fourth pair of the day, after the fixtures' `operation` values
were corrected against the contract. The pair before this one read 23 of 36 on both recordings, and
almost all of the loss was one form: a run answering `["T1","T2"]` where the fixture wanted `["T1"]`.
That was resolved against the fixtures, not the Director. The `expect.operation` values were written
by an agent earlier the same night; `.live-spec/turnkey-contract-composed.md` is the owner-proven
document, and it says an instruction accepted right now runs T1 and T2 as one operation, an idea the
person explicitly wants kept runs T1 alone. `scripts/task-admission.py` writes the row and the
checkpoint in one call — the two transitions are fused in the built code. So the producers quoting
the contract were right and the fixtures were wrong, and fourteen fixtures moved to `["T1","T2"]`:
`idea-with-a-cheap-branch`, `idea-shaping-then-one-decided`, `observation-a-verdict-on-delivered-work`,
`decision-how-to-report`, `decision-and-instruction-together`, `instruction-one-pass`,
`instruction-one-goal-two-steps`, `instruction-a-procedure`, `mixed-plan-and-two-questions`,
`mixed-reminder-and-a-challenge`, `mixed-check-now-improve-later`, `mixed-four-at-once`,
`not-an-act-answering-the-director`, `not-an-act-a-bare-trace` — every scenario whose
`creates_work` is true, and no other `expect` field on any of them.

`verdict_shape.operation` was rewritten again, this time as a derivation rather than a glossary: the
producer is told to read the field off the rest of its own verdict, taking the first line that fits —
work accepted now is `["T1","T2"]`; a correction or a decision applied to running work is `["T3"]`; a
halt that clears the holder and leaves the work to resume is `["T6"]`; a halt that drops it for good
is `["T9"]`; a blocker verifiably gone is `["T5"]`; a newly named blocker is `["T4"]`; a done that
turned out false is `["T8"]`; everything else is `["none"]`. A glossary asks the producer to classify
twice and lets the two answers drift; a derivation ties the field to the verdict it sits in.

Skill unchanged throughout: `skill_sha256`
`94986245598fc5b3a97b7548e49a2e7cf58c3cd5dfa2f9c24aecac9232a3d79b`, 21,977 bytes.

| recording | score | extra acts | operation-only reds |
|---|---|---|---|
| ninth (first of this pair) | 30 of 36 | 7 | 4 |
| tenth (second of this pair) | 33 of 36 | 7 | 3 |

Against 23 and 23 on the pair before. The `["T1","T2"]` form is gone from both recordings — not one
occurrence — which is what a correct fixture looks like from the outside. `check.py` now prints
`operation-only reds: N` on its own line just above the score line, counting scenarios red on that field and nothing else,
so the field's share of a score is visible instead of inferred.

Red on both recordings, all three on the operation field alone:

- `halt-with-a-reason-worth-keeping` — the runs answer `["T9"]`, the fixture wants `["T6"]`. "Стоп,
  ты тупо жжешь токены обслуживая ненужную машинерию выдуманного параметра" reads to every producer
  as dropping the machinery for good, not parking it to resume. Four recordings now agree on T9.
  Park and abandon are not distinguishable from this fixture's own `expect` fields, so it was left
  alone rather than corrected on one reading of the message.
- `idea-plus-a-fact` — the runs answer `["T1"]`, the fixture wants `["none"]`. The derivation's own
  exception says an idea the person explicitly asks to keep is queued as T1, and the person's
  "дальний бэклог" reads as exactly that request. The fixture's `shelves_idea: true` means, in
  today's vocabulary, raised as a question or answered and let go — not stored — so the two are
  answering different questions. The exception clause is what makes this ambiguous, and it is the one
  place the new derivation can still be read two ways.
- `observation-carrying-its-repair` — the runs answer `["T4"]`, the fixture wants `["T3"]`. This
  scenario has now disagreed with its fixture on every recording today, and on three different
  fields: `attaches_to_existing_work`, then `operation: none`, now `operation: T4`. Producers read a
  failed CI run as a newly named blocker; the fixture reads it as a correction in place. It is the
  set's most contested fixture and wants an owner's word, not another recording.

The first recording carries three more, none of them shared: `observation-neutral` answering `["T5"]`
for a plain report, and act-or-boolean disagreements on `observation-a-verdict-on-delivered-work` and
`mixed-check-now-improve-later`. By this file's rule those are draws.

The runs on file are the tenth recording, the second of the pair, by the standing precedent. The
ninth is in this session's scratchpad (`.../scratchpad/director-run11/`). All thirty-six carry
`operation`.

bare run pair: 2026-09-06 (night) — the fifth pair of the day, and the one q-823 was reopened
against. The pair before it read 30 and 33 of 36 and shared three reds, all on the `operation`
field: `halt-with-a-reason-worth-keeping`, `idea-plus-a-fact` and `observation-carrying-its-repair`.
By this file's own rule three reds on both recordings are three defects, so the row that had closed
on "the grader reads that field" was closed on a failing eval. It was reopened through
`scripts/task-admission.py reopen q-823` against that false condition, and this pair is what closed
it again.

The owner settled each of the three, and the settlements went to different files.

- **`halt-with-a-reason-worth-keeping` — the fixture was wrong.** Four recordings had answered
  `["T9"]` against a fixture wanting `["T6"]`. "Ты тупо жжешь токены обслуживая ненужную машинерию
  выдуманного параметра" orders needless machinery stopped, not parked for later, so the producers
  were right: `expect.operation` is now `["T9"]`, and the fixture's `why` says why the abandon and
  not the park. No other field of that fixture moved, and no other fixture changed.
- **`idea-plus-a-fact` — the Director was unclear.** The fixture keeps its strict `["none"]`: "может
  имеет смысл", "просто как идея", "дальний бэклог" with no commitment to do it is neither a task
  nor a kept ticket. Producers had been reading "дальний бэклог" as the explicit ask-to-keep that the
  operation derivation's own exception admits as `["T1"]`. Two sentences were added to *An idea is not
  an instruction* (`skills/director/SKILL.md:59`): saying where an idea belongs is not asking for it
  to be kept — that wording commissions nothing, so no ticket opens for it, not even a queued one,
  and only a direct ask to record it opens one.
- **`observation-carrying-its-repair` — the Director was unclear.** Producers read a mail about an
  old CI failure as a newly named blocker (`["T4"]`) where the fixture reads it as a correction in
  place (`["T3"]`, attaching). One sentence was added to *Some observations carry their repair with
  them* (`skills/director/SKILL.md:127`): a failure already diagnosed whose repair is in flight — the
  fix sent, the work still open, a fresh run under way — is no new problem when it is reported again;
  it stays an observation and lands on that running work as a correction, opening no second row and
  naming nothing newly blocked.

Both edits are classification only; neither adds an execution rule. The file went from 21,977 to
22,548 bytes, and `skill_sha256` from
`94986245598fc5b3a97b7548e49a2e7cf58c3cd5dfa2f9c24aecac9232a3d79b` to
`25918077595e51533c96de018652426dbc9758c70a6c0961dea8a747e2373943`.

All thirty-six were then recorded twice against the edited text, under the isolation protocol above:
one fresh Opus producer per scenario, holding the skill's full text, one situation and message, the
required JSON shape including `operation`, and an opaque two-letter label drawn fresh for each of the
two recordings — no repository, no fixture, no expected verdict, no other producer's answer.

| recording | score | extra acts | reds |
|---|---|---|---|
| eleventh (first of the pair) | 33 of 36 | 7 | `observation-a-verdict-on-delivered-work`, `instruction-one-goal-two-steps`, `not-an-act-a-bare-trace` |
| twelfth (second of the pair) | 34 of 36 | 6 | `observation-neutral`, `mixed-plan-and-two-questions` |

**The intersection is empty.** `python3 evals/director/check.py --pair evals/director/traces
evals/director/recordings/2026-09-06-pair-6` prints `shared reds: 0` as its last line. All three
scenarios the day's settlements were aimed at pass on both recordings, and every red above is a
draw by this file's own rule. The first recording's three are one shape — a producer declining to
accept work the fixture expects accepted, so `creates_work` false and `operation` `["none"]` or
`["T4"]` — and the second recording answers all three the fixture's way, which is the variance this
file has warned about since 2026-09-02 rather than a finding.

Both recordings of this pair are kept in the tree, not only in a scratchpad. The twelfth is in
`traces/`, the recording the probe and the grader's `--all` read, by the standing precedent that the
runs on file are the second of the pair. The eleventh is in
`recordings/2026-09-06-pair-6/` — thirty-six JSON files of the same shape, each carrying its own
scenario, label, `skill_sha256`, `recorded`, `skill_version`, `producer_model` and `operation`. A pair
whose second half alone survives cannot be re-checked by anyone, and the intersection is the whole
verdict here, so both halves stay.

`check.py` gained `--pair DIR_A DIR_B` for this: it grades two recording directories, prints each
one's score and reds, and prints `shared reds: N` followed by the ids as its last line. The
acceptance keys for q-822 and q-823 read that clause and no score at all.

**The grader's own exit follows the same rule.** A defect in this directory is a red both
independent recordings agree on; a red in one recording only is producer variance, on record here
since 2026-09-02 and never a reason to fail the eval. So `--all` grades the recording named by
`recorded_pair` in `scenarios.json` beside `traces/`, prints `variance reds (one recording only):`
and `shared reds:` above its score line, and exits 0 when the intersection is empty — as it does
today, at 34 of 36 with five variance reds and none shared. Until 2026-09-06 it exited 1 on anything
short of 36 of 36, which is a clean-sweep floor nobody declared and which moves with the draw. The
score line itself keeps its exact shape, because `scripts/state-probe.sh` and
`scripts/plan_checks.py` read it with `tail -1`, and the variance reds stay printed rather than
swallowed: a scenario that oscillates is worth seeing even when it is not a defect. With no
`recorded_pair` on file the exit falls back to the clean sweep and says so on its own line.

## When a recording is owed (rule from 2026-09-06 15:34)

A recording pair is owed once per push, after the last edit to the skill under test, never per
edit. On 2026-09-06 the pack re-recorded after every one-sentence fold — eight full Director
recordings and twenty of the closing set in one day, about 550 producers — and the method gained
nothing from the intermediate pairs: the verdict that matters is the pair against the text that
ships. So: edit, review, edit again if the review says so, and record the pair last, against the
final bytes; the hash pin proves which text it was. An intermediate pair is run only when a
change is suspected of moving behaviour and the answer decides the next edit.
