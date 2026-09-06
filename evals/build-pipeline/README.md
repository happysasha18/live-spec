# Accepted-work pipeline eval

This suite owns the decisions made after Director has returned a work route: whether verified work
closes now or waits for a genuinely human-only judgment, and whether the pipeline voices a conflict
before it admits a request.

`closing-scenarios.json` and `closing-traces/` moved here on 2026-09-05 when execution moved out of
Director. The traces on file were re-recorded on 2026-09-06 against
`skills/build-pipeline/SKILL.md` plus `references/accepted-work-execution.md`; the older ones,
produced from the monolithic `skills/director/SKILL.md`, are gone from the directory rather than
kept as a second answer to the same question. The hash must never be repinned without new
producer runs.

To refresh them, give one fresh producer exactly one opaque-labelled scenario plus the current
pipeline skill and accepted-work execution reference. Do not show the expected verdict or another
producer's run. Save the returned JSON under `closing-traces/<scenario-id>.json`, repeat the whole
set with separate producers, and update `recorded_run` only after both recordings. The deterministic
grader remains in `tests/test_director_scenarios.py` until it is extracted without changing its
judgment.

## Runs

### 2026-09-06 — four recordings, one skill edit between the pairs

Nine scenarios, one fresh `opus` producer each, opaque two-letter labels reissued for every
recording. A producer held the pipeline skill and the accepted-work execution reference and one
scenario's situation and delivered state, and saw neither the expectation, nor the scenario's own
name, nor the repository, nor another producer's answer. Each set was graded by the suite's own
`closing_grade`, pointed at that set's directory.

| recording | text | score | red |
|---|---|---|---|
| 1 | as it stood, `3101d3fa…` | 7 of 9 | `close-a-redefinition-the-person-himself-ordered` (closes=False, expected True); `ask-when-the-change-reaches-past-what-was-ordered` (closes=True, expected False) |
| 2 | as it stood, `3101d3fa…` | 8 of 9 | `close-a-redefinition-the-person-himself-ordered` |
| 3 | after the edit, `18329981…` | 9 of 9 | — |
| 4 | after the edit, `18329981…` | 8 of 9 | `ask-when-the-change-reaches-past-what-was-ordered` |

Recordings 1 and 2 intersect on `close-a-redefinition-the-person-himself-ordered` and differ on
`ask-when-the-change-reaches-past-what-was-ordered`. Recordings 3 and 4 intersect on nothing and
differ on `ask-when-the-change-reaches-past-what-was-ordered`. The runs on file are recording 4,
the second of the pair made against the text as it now stands.

**The finding.** A scenario counts as failing only when it fails on two separate recordings, and
`close-a-redefinition-the-person-himself-ordered` did: both producers read a redefinition of what
counts as correct — one the person himself ordered, in the very instruction the work carries out —
as still the third of the three cases rule 12/27 reserve for him, and held the row open for a fork
he had already settled. The closing paragraph named that third case without saying whether an
already-settled one still counts, so both readings were available to a producer reading carefully.
The reference gained the missing qualifier (`references/accepted-work-execution.md`, the closing
paragraph: 12,485 → 12,672 bytes) and both recordings were made again from the edited text. Both
producers then closed it, quoting the new clause.

**Shapes below the fix threshold, worth naming.**

- *Curing the overreach instead of voicing it* — `ask-when-the-change-reaches-past-what-was-ordered`,
  red in recording 1 and again in recording 4. The run sees that the delivered change reaches past
  the narrow instruction, decides the collateral case is settled by the eval's own written cost
  model, splits the shared branch itself, re-grades, and closes. It never defers to a stale gate;
  it decides the wider case by repairing it. Green in the other two recordings, where the same
  producer material read the wider case as still open.
- *The disagreement scenario is stable.* All four producers voiced the conflict, named the
  standing decision as the flaw, and had the pipeline proceed on the person's word rather than
  refuse — no run treated the request's size or reversibility as an excuse to build it silently.
- *Reason labels stayed inside the fixture's accepted set on every graded run.* No recording lost
  a scenario on `reason_kind` alone; every red was a disagreement on the boolean itself.

**Method note.** The two documents were concatenated verbatim into one scratch file and each
producer was told to read that file and nothing else, rather than having 18 KB of skill text
retyped into eighteen prompts. The producer then reads the same bytes the recorded hash pins.
Retyping is where a producer's copy quietly stops being the skill under test.

### 2026-09-06 (later) — one clause in the skill, one more pair

`scripts/task-admission.py` had gained a refusal for a ticket carrying no context pointers (q-823),
but the skill's own sentence about what the write door validates did not name them, so a route
written to the skill's instruction would be refused at the door it names. The skill gained one
clause — "source, outcome, DOD, verification, project, **scope, context pointers** and duplicate
title" (`skills/build-pipeline/SKILL.md`, the admission paragraph: 6,281 → 6,299 bytes; the
paragraph was rewrapped, nothing else in the file changed). The set was recorded twice more under
the same protocol, opaque labels reissued again.

| recording | text | score | red |
|---|---|---|---|
| 5 | after the clause, `64a6a393…` | 8 of 9 | `ask-when-the-change-reaches-past-what-was-ordered` (closes=True, expected False) |
| 6 | after the clause, `64a6a393…` | 9 of 9 | — |

Intersection: empty. Symmetric difference: `ask-when-the-change-reaches-past-what-was-ordered`.
No scenario is red on both, so this pair holds no finding and the skill was not edited again. The
runs on file are recording 6.

Across all six recordings of the day, one shape keeps surfacing without ever reddening both runs of
a pair: three producers of six resolved `ask-when-the-change-reaches-past-what-was-ordered` by
repairing the overreach themselves — split the shared branch, restore the documented cost model,
re-grade to 30 — and closing, rather than putting the unsettled wider case to the person. A run that
cures the overreach and closes is not deferring to a stale gate; it decides the wider case by fixing
it. Half the producers read the cost model as settling that case and half read it as still open,
which is where the fixture and the skill disagree about what "no artifact settles it" means. Worth
a fixture reading before it is worth a skill edit.

### 2026-09-06 (night) — one false sentence repaired, one more pair

A cold reviewer found the reference claiming that `references/delegation-protocol.md`'s content
"does not survive the cut into this skill", while that file is carried in the same directory,
`tests/test_delegation_line.py` requires its content and `guardrails/README.md` names it as a live
wording source. The sentence was false about the pack it describes. It was rewritten to say what is
true — the file is kept as the wording source for the delegation line and the worker-brief shape,
and it is the tier ladders, escrow law and reporting bureaucracy it also carries that are no part of
this procedure (`references/accepted-work-execution.md`, the specialist-brief paragraph: 12,672 →
12,756 bytes). Nothing else in either document changed. The set was recorded twice more under the
same protocol.

| recording | text | score | red |
|---|---|---|---|
| 7 | after the repair, `8655c0d1…` | 9 of 9 | — |
| 8 | after the repair, `8655c0d1…` | 9 of 9 | — |

Intersection: empty. Symmetric difference: empty. The first pair on record where both recordings are
clean, so nothing here is a finding and the skill was not edited again. The runs on file are
recording 8.

The one shape that has recurred all day — a producer repairing the delivered overreach itself and
closing on `ask-when-the-change-reaches-past-what-was-ordered` — did not appear in this pair, and
across eight recordings it has never reddened both runs of the same pair. Three producers of eight
took it. It stays a fixture question rather than a skill defect: the fixture holds that the wider
case is unsettled, and those three read the eval's own written cost model as settling it.

### 2026-09-06 (statement half) — the pipeline gains a validated statement, one more pair

Requirement 309's statement half landed in `scripts/task-admission.py`: admission derives the
task's statement, `validate` puts it through a mechanical floor and a clean-context reader before
any take-up, `hold` freezes the wording and records the lane decision against the plan's own
expectation, and the close carries the estimate beside the actual. Both documents changed, so both
were re-recorded. The skill gained one paragraph naming what admission derives and what `validate`
runs (`skills/build-pipeline/SKILL.md`: 6,299 → 6,974 bytes). The reference gained the procedure
behind it — who writes the reader's file, what take-up freezes, what the close carries — and one
sentence putting the closing check on the product as it renders rather than on the producer's own
test (`references/accepted-work-execution.md`: 12,756 → 14,069 bytes).

| recording | text | score | red |
|---|---|---|---|
| 9 | after the statement half, `c1b65a2e…` | 8 of 9 | `ask-when-the-change-reaches-past-what-was-ordered` (closes=True, expected False) |
| 10 | after the statement half, `c1b65a2e…` | 9 of 9 | — |

Intersection: empty. Symmetric difference: `ask-when-the-change-reaches-past-what-was-ordered`.
No scenario is red on both, so this pair holds no finding. Both recordings are kept whole under
`recordings/2026-09-06-pair-5/` and `recordings/2026-09-06-pair-5-second/` — a pair is kept now
rather than the first half being thrown away once graded — because the documents changed again
before these runs could be the ones on file, for a reason the pair itself did not raise.

The one shape that has recurred all day appeared again in recording 9 and not in recording 10:
four producers of ten now resolve `ask-when-the-change-reaches-past-what-was-ordered` by repairing
the delivered overreach themselves and closing. It has still never reddened both runs of a pair.
Recording 10's producer read the same case as a change to the definition of correct nobody ordered
and held the row open, which is the fixture's own reading.

### 2026-09-06 (statement half, after the skill-creator fold) — one more pair

The pair above held no finding, but the Anthropic skill-creator review run beside it did, and both
cold readers found it separately: the execution reference restated the four statement fields, the
person-never-writes-them fact and the `validate` command the skill body already owns, instead of
stating only what the body defers to it. That is the two-homes-for-one-fact shape this pack forbids
and the same file already refuses one paragraph over ("rule 7 carries the lane law in full and is
not repeated here"). It was folded, along with a verify sentence that repeated its own paragraph's
thesis and illustrated it with one project's nouns
(`references/accepted-work-execution.md`: 14,069 → 14,027 bytes; `SKILL.md` unchanged at 6,974).
The full review is at `docs/skill-review/2026-09-05-build-pipeline-admission.md`, third section.

| recording | text | score | red |
|---|---|---|---|
| 11 | after the fold, `37a14789…` | 8 of 9 | `ask-when-the-change-reaches-past-what-was-ordered` (`closes` right, `reason_kind` "ordinary delivered result" outside the accepted set) |
| 12 | after the fold, `37a14789…` | 9 of 9 | — |

Intersection: empty. No scenario is red on both, so this pair holds no finding and neither document
was edited again. The runs on file are recording 12; recording 11 is kept whole under
`recordings/2026-09-06-pair-6/`.

Recording 11 is the same recurring scenario reddening in a new way. The producer held the row open,
which the fixture expects, but labelled its reason "ordinary delivered result" — reading the work as
simply undelivered rather than as a fork the person owns, and then repairing the overreach itself
before closing. Across twelve recordings that scenario has now gone red five times and never on
both runs of a pair. What the day's runs actually disagree about is whether the eval's own written
cost model settles the wider case; the fixture holds it open and half the producers read it as
settled. That is a fixture question, and it is now old enough to be worth answering rather than
recording again.

### 2026-09-06 (the trusted closure kernel) — two pairs, one fold between them

The closure rule landed in code and in both documents. The skill gained one short section: the
definition of done is fixed at admission, changing it is its own operation that keeps the previous
text and hash, the executor hands over evidence and never issues the acceptance verdict itself, and
close is a state transition against a receipt rather than a sentence an agent writes
(`skills/build-pipeline/SKILL.md`: 6,974 → 8,077 bytes). The reference gained the ten clauses in
full and the commands behind them — `correct --done --source --reason`, `verify --by --command
--surface`, and what `close` refuses (`references/accepted-work-execution.md`: 14,027 → 16,850
bytes). Both documents moved, so both were re-recorded under the same protocol, opaque labels
reissued for every recording.

| recording | text | score | red |
|---|---|---|---|
| 13 | after the kernel, `6a1821bd…` | 9 of 9 | — |
| 14 | after the kernel, `6a1821bd…` | 9 of 9 | — |

Intersection: empty. Symmetric difference: empty. The pair held no finding.

**The finding came from the review beside it, and both cold readers found it separately.** The
body's new section did not summarize the reference's ten clauses — it restated four of them almost
word for word, the exact command and its flags included ("The definition of done is fixed when the
row is admitted" against "The definition of done (DOD) is fixed at admission"; "The executor hands
over evidence and never issues the acceptance verdict itself" against "The executor may provide
evidence but may not issue the final acceptance verdict itself"). That is the two-homes-for-one-fact
shape this pack forbids, and the same shape the pair-five review folded. The body was cut back to
the law plus the three commands a body-only session must be able to run — `correct`, `verify`,
`close` — with the clauses' one home named as the reference (`SKILL.md`: 8,077 → 8,002 bytes; the
reference unchanged at 16,850).

| recording | text | score | red |
|---|---|---|---|
| 15 | after the fold, `b7dec6d7…` | 9 of 9 | — |
| 16 | after the fold, `b7dec6d7…` | 8 of 9 | `ask-when-the-change-reaches-past-what-was-ordered` (closes=True, expected False) |

Intersection: empty. Symmetric difference: `ask-when-the-change-reaches-past-what-was-ordered`. No
scenario is red on both, so this pair holds no finding and neither document was edited again. The
runs on file are recording 16; recordings 13 and 15 are kept whole under
`recordings/2026-09-06-pair-7/` and `recordings/2026-09-06-pair-8/`.

Recording 16's one red is the shape that has recurred all day, in its usual form: the producer read
the eval's own written cost model as settling the wider case, split the shared branch itself,
re-verified and closed. Across sixteen recordings that scenario has gone red six times and never on
both runs of a pair. Recording 15's producer read the same case the fixture's way and reached for
the new kernel to say why — no threshold or scoring rule invented after start that was not in the
admitted done. Half the producers read the cost model as settling the wider case and half as leaving
it open; that is a fixture question, and it is now well past the age where recording it again adds
anything.
