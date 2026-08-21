# PUSH-REVIEW — the Director in shadow mode

Range: 18d87c5c..1eed2797 — two commits reviewed, `36eb8fd0` (capability map) and
`1eed2797` (the Director, its scenario suite and its recorded runs). Base `18d87c5c`.

Files read: the two commits' full diffs; `skills/director/SKILL.md` cold, three times, once
per version; `evals/director/scenarios.json` and every file under `evals/director/traces/`;
`guardrails/check-skill-loadability.sh`, `check-skill-review.sh` and `check-prover-record.sh`
to establish what each gate actually requires rather than what it is said to require.
`PRODUCT_SPEC.md` and `ARCHITECTURE.md` were **not** re-read: this range changes neither,
adds no requirement and no architecture node, and reading them would have been a ritual
rather than a check. Said plainly here so the record is not mistaken for one that did.

Checks run: `guardrails/check-skill-loadability.sh` — green, 12 skills. Three full scenario
runs of 35 messages each, 21 subagents, graded by `evals/director/check.py`. The grader was
itself checked against a correct verdict, three kinds of wrong verdict and a verdict that
routed work it had not accepted, before any result from it was believed. The full local
pytest suite was **not** run: it kills itself reproducibly in this environment (a known
finding), and CI runs it authoritatively on this push.

Findings: eight, listed below. Two are defects in the reviewer's own harness rather than in
the work, and are recorded with the rest because a test that lies is worse than no test.

**F1 — the first run was invalid, and a gate did not catch it.** The blind batches carried
each scenario's identifier, and the identifiers were descriptive: one read
`halt-with-a-reason-worth-keeping`. An agent said in its own report that the name told it
what to answer. The question contained its answer. The run was discarded and redone with
opaque labels. Nothing mechanical detected this — an agent's honest account of its own
reasoning did. Recorded in `evals/director/README.md` as well, where a future reader of the
suite will meet it.

**F2 — the skill's own escape hatch, found only by running it.** The file's closing section
points wording questions at `skills/communicator`. Three separate agents cited that line to
answer a plain request — "давай план, замеры по времени, все пиши" — by creating nothing.
Two rounds of adversarial reading had not found it; using the file did. The line now says
that a plan, a status or a report asked for is work like any other, and that routing it to
the communicator is how a plain request disappears.

**F3 — the Director dissolved multi-act turns.** In the second run, every one of the six
mixed scenarios failed on the set of acts, while single-act turns passed nearly cleanly —
four questions of four, three instructions of three. One trace shows the failure exactly:
the agent listed every instruction in the message in its own reasoning and then recorded
that no work had been requested. It saw them and dissolved them. "One turn, several acts"
was a paragraph; it is now a step, with an explicit rule that no act absorbs another and a
tie-break that names one act too many rather than too few.

**F4 — the fix bought a compensating error, and the headline number did not move.** After
F2 and F3 were fixed, exact agreement on the act set went from 25 of 35 to 25 of 35. What
changed was the composition: acts the person performed and the Director lost fell from 12
to 7, and acts it invented rose from 5 to 7. It now attaches an observation to a plain
halt. That is the cheaper error by the file's own reasoning — naming one act too many costs
a sentence, naming one too few loses what somebody said — but it is an error, and the
trade was not free.

**F5 — exact-set grading of acts measures agreement, not competence.** This is the
reviewer's own defect. The seven acts are not a partition: "мораторий на мне остальное на
тебе" is defensibly a decision, defensibly a decision and a halt, and grading one reading
as truth turns a suite into a conformity test. Three runs converged on nothing because
there was nothing to converge on. Acts lost against acts invented is the measure that
tracks what the mandate actually asks for, and it is the number to read above. The scenario
suite keeps both.

**F6 — two fixtures were wrong, and were corrected after they had been graded.** Both are
recorded inside `evals/director/scenarios.json` under `corrections`, with what they said
before, what they say now and why. `decision-how-to-report` expected a standing rule and
nothing else, where two independent runs read a request for a plan that does not yet exist,
and were right. `decision-a-boundary` never said what the moratorium was on, so two
readings were equally defensible; its expectation is unchanged and its situation now states
itself. A fixture edited after seeing the result it graded is worth less than one written
blind, which is why both are named rather than quietly amended.

**F7 — the verdict shape was under-defined in two places, and runs disagreed because of
it.** `work_items` was read by some agents as pieces of work involved and by others as new
pieces created; it now says new. `creates_work` is still undefined for a correction — one
run answered false across the board and the next answered true, both with reasons. Not
fixed. It costs three of the remaining failures and it is a wording problem in the harness,
not a defect in the Director.

**F8 — the residual loss is concentrated, and is not being fixed here.** Four of the seven
acts still lost are the same one: **decision**. The Director under-reads standing rules —
"с этого момента", "запиши себе всегда", "всегда давай ссылку". These are exactly the
utterances the mandate says must not be lost, since a rule dropped is re-litigated. It is
named here as the first thing package 3 should take, and it is not being chased now: the
package closes when behaviour is checked by scenarios, not when every scenario is green.

Blocking: none. Nothing in this range changes product behaviour, and the Director acts on
nothing — it writes a decision sheet into its reply and touches no file. F8 is real and
open, and is recorded rather than fixed by decision, not by oversight.
