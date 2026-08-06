# Eval — build-pipeline (SPEC E-19)

## Scenario

Both arms get the same task; the with-skill arm first reads `skills/build-pipeline/SKILL.md` and works
by it. Prompt (verbatim):

> You maintain a small CLI project; the repo contains PRODUCT_SPEC.md, ARCHITECTURE.md, TEST_MATRIX.md, a pytest
> suite in tests/, and the tool's source. A user reports: "mytool --export out/report.csv silently
> writes an EMPTY file when the out/ directory doesn't exist."
> Describe EXACTLY what you would do to handle this report — step by step, in order, from the moment you
> read it to the moment you consider it done.

## Criteria

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| The door named aloud BEFORE any file touch (T-12; bug → matrix → test → code entry, not the full walk) | RED — no door step; plan opened with reproduce-then-code framing | GREEN — step 1 names door=bug · kind=product · priority · size, enters at the bug door |
| The work-kind named at intake (T-16) | RED — absent | GREEN — kind called (product: the CSV is the user's artifact) |
| Fix the class, sweep look-alikes (base rule 14) | MET BARE — loader-fed run swept sibling write paths | GREEN |
| Red-on-bug test BEFORE code (step 6) | MET BARE | GREEN |
| A pending human question never parks the lane (INV-4): recommend + batch + proceed | FLOOR ROSE 2026-07-12 (row 268/N1) to MET BARE — the loader-fed bare arm now proceeds on a stated default ("I'd default to auto-creating the dir") and does not park; the original 2026-07-05 red was "I'd stop and ask rather than guess", the 2026-07-10 red "decides silently, no report". The skill's marginal value now sits in the structural layer (door/kind/guardrails), not this floor. | GREEN — question batched with class findings, decided once, `[default]`-tagged, told at landing, never asked |
| Guardrails run named before done (pipeline teeth) | RED — absent | GREEN — pre-push check named as a step |
| Verify by deed on the real artifact (step 8) | MET BARE (manual re-run present) | GREEN |
| Plain-language report to the owner before push (step 9 / T-7) | MET BARE — floor rose 2026-07-12 (row 268/N1): the bare arm now closes the loop with a plain report to the reporter (previously partial). | GREEN — report step names files + verified output |
| The capture echo at intake: the report is echoed back in one sentence — heard · door · name · row (step zero; SPEC INV-27, added 2026-07-06) | — (criterion added later) | scored from the 2026-07-06 re-run |
| Verify in the medium's own form (step 8; SPEC INV-30, added 2026-07-06): a CLI verifies by the command round-trip on the real artifact, not "tests pass" alone | PARTIAL (2026-07-06 push re-run) — manual re-run present | GREEN (same re-run) — real command run AND real file read, sibling flags included |
| A taken default is TOLD at landing, never confirmed (step 9; SPEC INV-31, added 2026-07-06): the report names the choice with an example and a tweakable mark, asks nothing | RED (2026-07-06 push re-run) — would ask before committing | GREEN (same re-run) — "named as a tweakable default rather than asked-and-blocked-on" |
| A delegation brief carries the ledger walk + the clock (ACT-3; added 2026-07-06 batch 2) | — (bare plans no delegation) | PARTIAL (2026-07-06 batch-2 re-run) — brief sketch names exact edits + checkpoint path, neither clock nor ledger line; the scenario only brushes delegation |
| Steps worked in their craft's head (INV-33; added 2026-07-06 batch 2) | — | PARTIAL (same re-run) — substance craft-true (matrix derivation reads QA, verify reads the user's own eyes), no hat named |

## The red

The bare run (bare run: 2026-07-05, Sonnet worker, zero tool uses — record
`docs/evals/2026-07-05-first-run/bare-build-pipeline.md`) produced a strong loader-fed plan (class
sweep, red-first, spec sync all present — the honest boundary in evals/README.md at work) but never
NAMED the door or the kind, planned to PARK on the design question ("stop and ask rather than guess" —
the exact anti-pattern of INV-4), and never ran the guardrails. The with-skill run (same day, record
`with-skill-build-pipeline.md`) opened with the intake line (door · kind · priority · size), entered at
the bug door, batched the question and kept the lane moving, and put the guardrails and the
report-before-push where the law puts them.

## Scenario B — delegation-forcing (added 2026-07-12, row 268 / S2)

The export-bug scenario above only brushes delegation, so the delegation-brief criterion (ACT-3) and the
craft-hat criterion (INV-33) could never score past PARTIAL — a one-file bug plans no worker. This variant
forces a delegation brief by hitting the delegation tripwires (>3 files touched, a known long-running
suite), so those two criteria can score cleanly. Prompt (verbatim):

> Same repo as above. A user asks you to rename the internal function `parse_row` to `parse_record`
> everywhere — it appears in 11 source files and 6 test files, and the full pytest suite takes about 90
> seconds to run. Describe EXACTLY what you would do, step by step, from reading the request to
> considering it done.

Criteria scored against Scenario B (the with-skill arm should now score GREEN where Scenario A left PARTIAL):

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| A delegation brief carries the ledger walk + the clock (ACT-3) | — (bare plans no worker) | GREEN target — the >3-files-and-90s-suite tripwire forces a worker; the brief must carry the exact edit strings, the checkpoint path, the problem-ledger WATCHED-line duty, AND the clock read at briefing |
| Steps worked in their craft's head (INV-33) | — | GREEN target — the mechanical rename routes to a worker (senior briefs), the judgment (naming, matrix, verify) stays senior, the hats named at each step |

## Scenario C — the spoken setup entry loads the skill (added 2026-08-06, row 557)

Scenarios A and B measure what the skill does once it is loaded. This one measures whether it loads
at all. The pack's front page promises that a person who has installed it says one sentence and the
setup walk runs, and that promise rests on the description field alone: a matcher reads the field and
picks the skill, so a sentence nobody's field covers reaches nothing. The arm this scenario scores
was added to `skills/build-pipeline/SKILL.md`'s description on 2026-08-06 (SPEC Requirement 308).

**How it is scored.** One fresh session per phrase, each given the phrase as its whole first message
and nothing else. Score which skills load. A phrase in the first list that loads no build-pipeline is
a red; a phrase in the second list that loads build-pipeline is a red. `evals/README.md` states the
standing boundary: a machine carrying the pack has no truly bare session, so this scenario measures
the marginal value of the field's wording over what the machine already teaches.

Eight phrases *shall* load build-pipeline:

| # | Phrase | Loads build-pipeline |
|---|---|---|
| 1 | attach live-spec to this project | to be scored |
| 2 | adopt live-spec here | to be scored |
| 3 | set live-spec up on this repo | to be scored |
| 4 | add live-spec to this codebase | to be scored |
| 5 | found a new project on live-spec | to be scored |
| 6 | start a new project with live-spec | to be scored |
| 7 | I just installed live-spec, what now | to be scored |
| 8 | update live-spec here | to be scored |

Two phrases *shall* miss it:

| # | Phrase | Loads build-pipeline |
|---|---|---|
| 9 | install the requests library | to be scored — a miss is the pass |
| 10 | start a new project | to be scored — a miss is the pass |

Phrase 6 is the contested one: `spec-author`'s own field opens on starting a new spec, and phrase 10
is the same sentence with the pack's name taken out. The two together measure whether the pack's name
is what does the picking. Phrase 9 measures the same thing from the other side, on the word install.

**When it re-scores.** The description field runs 493 characters, and the other ten fields range
from 122 to 383 characters, so this one is the longest in the pack today (measured 2026-08-06). No gate caps the
field, and dilution would show here first. Re-score this scenario after any later growth of the
field.

## Re-run

One Sonnet worker per arm. Bare arm: the prompt above + "do not invoke any tools or skills". With-skill
arm: "First read skills/build-pipeline/SKILL.md and work strictly by it" + the same prompt. Score each
criterion; append the dated record to `docs/evals/`. Run BOTH scenarios (A: the export bug; B: the
delegation-forcing rename); the delegation-brief and craft-hat criteria score against Scenario B.
