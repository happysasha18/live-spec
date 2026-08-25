# Prover record — 2026-08-25 director-scenario-gate-resample

PUSH-REVIEW

Range: 10a7bfe3..32ffe10b (1 commit: `32ffe10b` "director scenarios: fix
observation-carrying-its-repair's fixture to traced ground truth"). One file changed,
`evals/director/scenarios.json` (27 insertions, 6 deletions). Nothing else touched.

## What this closes

`docs/prover/2026-08-24-director-scenario-runs.md` left package 3's cutover gate open on
one-shot evidence: NEW (5.0.0) 19/35 against a FROZEN shadow (0.3.0) snapshot at `23f83047`
23/35, same `scenarios.json`, and flagged that shadow itself was never resampled, so the
gap could be single-draw noise rather than a real regression. This record supplies the
missing bilateral resample and a ground-truth fix to one fixture, and reports what the gate
actually shows now.

## observation-carrying-its-repair — fixture correction, not an answer-matching edit

The fixture's message ("вроде пуш не прошел уже, мне пришел мейл") is a verbatim, anonymised
transcript line. Traced independently to its real source: `~/.claude/projects/-private-tmp-live-spec-roadmap-wave/270e2224-42cb-4817-ace0-cd02b86f69b7.jsonl`,
line 2411, `2026-08-18T18:19:39.680Z`. The surrounding transcript (lines 2376-2488) shows the
assistant had already diagnosed two prior red CI runs as one stale-pin cause and pushed a fix
3m17s earlier (line 2381, `18:16:22`); CI run `32169552541` was still `in_progress` when the
message landed (confirmed `in_progress` both immediately before, line 2406, and immediately
after, line 2419); the assistant's reply at `18:19:56` (line 2422) told the human the email
was stale and the fix was already running. Nothing about the incident was checkpointed or
accepted at message time. The fixture's `situation` field omitted all of this, so its
`expect` (`creates_work: true`) assumed a closed, standalone failure the real transcript
does not show. `situation` is corrected to state the missing facts; `expect` is corrected to
`creates_work: false, attaches_to_existing_work: true, work_items: 0`, matching the shape of
this scenario corpus's five other `attaches_to_existing_work: true` siblings exactly (no
stray `dimensions_required` key). A `corrections` entry is appended citing the source
verbatim, same precedent as the existing `decision-a-boundary` entry: an under-specified
situation is corrected, not the answer.

An adversarial reviewer (different agent) rejected the first version of this edit as
unverifiable — the corrections entry asserted a "traced ground truth" without a checkable
citation, indistinguishable from the exact anti-pattern the original 2026-08-24 record
warned against (editing the answer to match the run). Reviewer re-ran on the citation-bearing
version, independently opened the transcript file itself and confirmed all four factual
claims against the raw JSONL (not against this record's paraphrase), confirmed the kept
5.0.0 trace's `reasoning` never mentions any of the added facts (so the correction adds
information the trace could not have supplied backward), and confirmed the corrections
entry's own claim that "three independent blind acting-mode runs converged 3-for-3" refers
to the original 2026-08-24 investigation's three runs (a real, already-documented fact in
that file), not to this session's later resample. Verdict: CONFIRMED-SAFE-TO-COMMIT, one
cosmetic citation line-number fixed (2410 → 2411).

## Bilateral resample — is the 19-vs-23 gap real

Five fresh independent blind samples collected, 35 scenarios each, same protocol as the
original 2026-08-24 run (blind to `expect`/`why`/descriptive id, shown only `situation` +
`message`, opaque `case-NN` labels): two more of the NEW (5.0.0) skill (the original
committed `evals/director/traces/` counts as the first), three of the SHADOW (0.3.0) skill
text (`git show ad851b7d~1:skills/director/SKILL.md`, since the frozen `23f83047` snapshot
was never itself resampled). All 175 verdict files kept at
`/private/tmp/ls-director/runs/{new-2,new-3,shadow-1,shadow-2,shadow-3}/case-NN.json`
(outside the repo, this session's working evidence — not committed, to avoid shipping 150
raw fixture-eval files for a comparison whose conclusion is reported here in full).

`observation-carrying-its-repair` is excluded from all six runs for this comparison: the
five later runs were all generated from a `blind-input.json` snapshot frozen from the
pre-correction fixture text, so grading them against the corrected `expect` tests the old,
known-ambiguous situation, not the fix. (First pass at this arithmetic asymmetrically
included it only for the `traces/` run, since that one happens to pass against the corrected
`expect` — an independent reviewer caught the inconsistency; corrected below by excluding it
from all six runs alike.)

**34 scenarios × 3 runs each, graded with the current `evals/director/check.py`:**

| | run 1 | run 2 | run 3 | total |
|---|---|---|---|---|
| NEW (5.0.0) | 19/34 | 19/34 | 17/34 | **55/102 (53.9%)** |
| SHADOW (0.3.0) | 20/34 | 19/34 | 19/34 | **58/102 (56.9%)** |

Gap: 3 checks out of 102 — within single-draw noise on a corpus this size, not a
statistically supportable regression. Two of thirty-four scenarios show a persistent
(≥2-of-3) hit-rate difference, and they point in opposite directions:
`correction-widening-the-goal` (new 0/3, shadow 2/3 — shadow better, an "acts" set mismatch
where NEW co-tags an extra `observation` alongside `correction`) and
`halt-with-a-reason-worth-keeping` (new 3/3, shadow 1/3 — new better). They cancel; no
scenario shows a one-sided, uncompensated regression. Eight of the ten scenarios that fail
in every one of the six runs also failed in the ORIGINAL frozen `traces/`
(`evals/director/traces/`) and frozen-shadow (`23f83047`) snapshots checked independently —
confirming these are corpus-inherent grading strictness (mostly exact `acts`-set mismatches
on multi-act turns), not new-skill-specific defects, and not an artifact of this session's
producer prompt.

Independently recomputed by an adversarial reviewer from scratch (own script, no shared
code): first pass reproduced my headline 56/105 vs 58/105 exactly but caught that it
included `observation-carrying-its-repair` inconsistently (only in the `traces/` run);
recomputing with the scenario excluded from all six runs gives 55/102 vs 58/102, confirmed
identical to the number reported above. The 2-scenario, opposite-direction persistent
divergence replicated independently. Producer methodology sanity-checked: reasoning fields
read as genuinely case-specific across a sample, no templating found.

## What this means for the package-3 gate

`JOURNAL.md`'s cutover gate asks whether the acting Director behaves "at least as well as"
shadow. On this fairly-resampled evidence — both sides drawn three times, not one frozen
snapshot against three fresh draws — the answer is yes, within noise: 53.9% vs 56.9%, zero
net one-sided regression across 34 scenarios. The original 19/35-vs-23/35 finding was not
wrong as a single measurement, but comparing it to a never-resampled frozen shadow snapshot
overstated the gap; two of shadow's four apparent advantages (`mixed-conditional-pause`,
`mixed-plan-and-two-questions`) do not survive shadow's own resampling — shadow fails them
in 2 of 3 and 3 of 3 fresh draws respectively, despite having passed them in the one frozen
draw used for the original comparison.

This record does not itself perform the `build-pipeline` cutover (package 3, step 5) — that
is deliberately a separate slice per the mandate's ban on partial extraction, and per this
project's own one-slice-one-push discipline.

Files read: `evals/director/scenarios.json` (full, current and diffed against `HEAD`),
`evals/director/check.py` (full, `grade()` read directly and imported programmatically, not
trusted from CLI text), `docs/prover/2026-08-24-director-scenario-runs.md` and
`-review-round-2.md` (full, prior record and its own adversarial review), the source
transcript cited above (lines 2376-2488), all 175 files under
`/private/tmp/ls-director/runs/`, `evals/director/traces/` (all 35, current), the frozen
`23f83047:evals/director/traces/` snapshot (all 35, via `git show`), `JOURNAL.md`'s
2026-08-24 cutover-gate entry.

Checks run: `python3 -m pytest tests/test_director_scenarios.py -q` — 11 passed, run fresh
after the `scenarios.json` edit. `python3 -c "import json; ..."` — 35 scenarios, 3
corrections, valid JSON, confirmed both before and after the citation-typo fix. Grading
script (`evals/director/check.py`'s `grade()`, imported directly) run against all 6
run-directories × 34 scenarios = 204 grade calls, aggregated as above; independently
reproduced by an adversarial reviewer's own from-scratch script, exact match after the
case-30-exclusion-consistency fix. `git diff --stat -- evals/director/scenarios.json`:
1 file, 27 insertions, 6 deletions, confirmed no other file touched.

Findings: one fixture correction (ground-truth-traced, adversarially confirmed, cited
above), and one measurement result — the package-3 "at least as well as shadow" gate is met
within noise on a fair bilateral resample. No implementation defect in `skills/director/SKILL.md`
itself; that file is untouched by this slice (`git diff origin/main -- skills/director/SKILL.md`
empty).

Blocking: none
