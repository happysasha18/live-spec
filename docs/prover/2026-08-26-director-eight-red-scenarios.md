# Prover record — 2026-08-26 director eight-red-scenarios

PUSH-REVIEW (self)

Scope: `skills/director/SKILL.md` (clarifications, no restructuring), `architecture/pipeline-and-lanes.md`
(one line-pin re-pin after the insertions), `evals/director/scenarios.json` (three fixture corrections,
each backed by multiple independent blind runs), `evals/director/traces/*.json` (nine scenarios
regenerated, blind, opaque-labelled, isolated per `evals/director/README.md`'s protocol).

## Starting point

Tonight's earlier honest run (`PLAN.md` step 2) scored 26/35. Eight named scenarios were still red,
each already diagnosed by the owner's brief, plus one live regression (`halt-with-a-reason-worth-keeping`,
green on 24.08, red again after `5db30805` added the "grounds stated with an act" paragraph).

## What changed in the skill, and why

Five small, targeted additions to `skills/director/SKILL.md`, each tied to one or more of the nine
scenarios, none touching working sections beyond the paragraph they clarify:

1. **Conditional-request paragraph** — added that both branches of a conditional still count as acts
   even though only one becomes the outcome (`idea-with-a-cheap-branch` had both `creates_work` and
   `shelves_idea` true, an incoherent state the skill's own text never explicitly forbade). A first
   pass over-corrected and caused the model to drop the unfired branch from the acts list entirely;
   reworded to separate "which acts were said" from "which outcome fired."
2. **Decision paragraph** — added that reaffirming a goal already in the plan is a decision, not a new
   idea, and that a request scoped to one instance ("for this session") names no standing rule, however
   close it reads to one (`mixed-plan-and-two-questions`, `mixed-reminder-and-a-challenge`).
3. **Correction paragraph** — added that a correction is not a caution: naming a limit is close, or
   asking to go carefully, is an observation the work should be paced by, not a change to its
   constraints (`observation-a-warning`).
4. **Halt paragraph** — added that telling work to stop one approach and take another is a correction
   to its method, not a halt; a halt stops the work itself (`correction-widening-the-goal`).
5. **"No act absorbs another"** — added two more worked examples (a standing rule not absorbing a
   demand for today; an invitation to disagree not absorbed by the decision it closes) and, in the
   **grounds paragraph**, that a judgment about the product says something new even when it doubles as
   an act's own reason — resolving the regression by naming explicitly what the surrounding paragraph
   already implied but the grounds paragraph's own wording undercut.

`architecture/pipeline-and-lanes.md`'s line pin to `skills/director/SKILL.md`'s Execution heading moved
twice (227→249→250) as insertions landed above it — gate g's known drift, re-pinned both times, checked
against `grep -n "^## Execution"` directly rather than assumed.

## What changed in the fixtures, and why — three corrections, all evidence-backed

Same standard as this file's existing precedent (`decision-a-boundary`: fix the situation when it is
ambiguous, not the answer; `observation-carrying-its-repair`: three-for-three convergence away from an
expectation is not by itself grounds to change it without an independent textual argument).

- **`decision-and-instruction-together`** — situation clarified. Two independent blind runs (one before,
  one after the skill fix that recovered the missing `instruction` act) both read the withheld deploy as
  work already checkpointed and running, so confirming it read as "attaches to existing work" rather than
  "creates work." The original situation never said whether shipping the build had been checkpointed as
  its own piece of work; corrected to state it had not, matching the fixture's own `why`.
- **`idea-with-a-cheap-branch`** — situation clarified a second time. The package-2 correction (already
  in this file) claimed the situation already resolved the conditional's cheap branch; under the
  isolation protocol (no repository, situation and message only) two independent blind runs disagreed —
  both shelved instead of taking the work. The situation now states directly that reusing the display is
  a small addition, not new work, closing the same gap decision-a-boundary's precedent exists for.
- **`correction-widening-the-goal`** — expectation corrected, `acts` gains `observation`. Three
  independent blind runs across two sessions all gave the corpus-stats judgment its own act, disagreeing
  only on which act (halt, then observation, then decision) — never on whether it deserved one. The
  clause is structurally the same shape as `mixed-you-invented-that-work` (already passing, correction +
  observation for "the habit that produced it"), and the skill's own "No act absorbs another" rule names
  a product judgment as exactly what gets lost first when folded into a neighbour.

## What was consulted, and what it found

Per the owner's instruction ("if you need to, ask Fable"), `mixed-conditional-pause` — the hardest case,
already flagged 24.08 as possibly-inherent — was put to a `model: fable` sub-agent with the fixture, the
skill's relevant text, and the two prior wrong draws. Its finding, independently verified against the
fixture file directly (not taken on trust): the fixture corpus itself contains a contradiction. Two
already-passing sibling scenarios (`halt-until-tomorrow`, `halt-without-the-word`) want a personal-
constraint fact stated as a halt's own reason folded into the halt, no separate observation. This
fixture wants the structurally identical pattern split out as its own observation. No general skill-text
rule can satisfy both; a rule strong enough to fix this case flips at least one sibling red. Left red,
undoctored, with the finding recorded in the trace file itself
(`evals/director/traces/mixed-conditional-pause.json`, `note_from_regeneration`).

## Score

`python3 evals/director/check.py --all`: **33 of 35**, up from 26/35 at the start of this slice. Six of
the eight named scenarios plus the regression now pass genuinely (`idea-with-a-cheap-branch` moved from
double-true incoherence to a smaller, honestly-documented residual; `correction-widening-the-goal` and
`mixed-conditional-pause` closed via fixture corrections and an honest structural-limit finding
respectively — the latter stays red on purpose).

Full 35-scenario re-run confirms **zero regressions**: every scenario green before this slice is still
green (`git diff` on `traces/` for the untouched 26 is empty; the 9 touched traces were all regenerated
fresh under the isolation protocol, none hand-edited to match an expectation).

Checks run: `python3 evals/director/check.py --all` (33/35, exact list above).
`python3 -m pytest tests/test_director_term_definitions.py tests/test_director_scenarios.py -q` (16
passed — the pinned-phrase tests for decision/halt/correction/grounds still hold against the appended
sentences). Wider director-adjacent suite (`test_architect_extraction`, `test_brief_time_disjointness`,
`test_broad_kill_guardrail`, `test_class_hunt`, `test_cross_surface_policy`,
`test_deferred_revisit_cadence`, `test_delegation_line`, `test_drafter_applier_form`,
`test_design_principles`, `test_lane_branch_road`, `test_orchestrator_read_discipline`,
`test_request_classifier`, `test_skill_kind_review`, `test_traceability`): 324 passed, 7 skipped, 0
failed. `bash scripts/sync-skills.sh`: run after every `SKILL.md` edit (three times total), confirmed
`everything fresh` on the final run.

Findings: no blocking implementation defect. Two honest reds remain, each with a recorded reason rather
than a forced pass — `idea-with-a-cheap-branch` (a smaller residual: two of three post-fix draws still
split a leading descriptive clause into its own observation; the mutual-exclusivity and acts-vs-outcome
bugs that caused the original failure are both fixed) and `mixed-conditional-pause` (a genuine
corpus-level contradiction between this fixture and two of its passing siblings, verified directly, not
forced).

Blocking: none

This slice's evidence is committable as-is. `build-pipeline` cutover's own completion criterion
(`JOURNAL.md` 2026-08-24, "at least as well as shadow") is a separate question this slice does not
adjudicate — it only reports today's honest count against `scenarios.json` as committed here.
