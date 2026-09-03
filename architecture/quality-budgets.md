## Quality budgets

What quality means for a skill pack, in numbers [INV-41]. Numbers proposed by the agent, tunable on
the human's word [INV-70]. Each is asserted by a matrix row, and its instrumentation home is where the
real number is read.

| Budget | Number | Instrumentation home | Watcher |
|---|---|---|---|
| full suite wall-time | ≤ 1780 s on the dev machine [default] — what it counts: the serial wall-time of one full `python3 -m pytest -q` run; the decision it informed: a push may proceed. Its mechanical watcher retired, so the figure below stands as a historical snapshot. Last derived 2026-08-13 from the seven full runs of the 2026-08-12 evening pass: 1,221.81 s, 1,281.39 s, 1,304.65 s, 1,605.37 s, 1,559.15 s, 1,387.88 s and 1,451.77 s. Read the spread before the number: the same suite on trees differing by a handful of documents swung 31% between runs, a load signal more than a code signal | the pytest tail line in the suite run's log | retired: `guardrails/check-suite-budget.sh` and its call site in `guardrails/check-tests.sh` are gone; nothing reds past this budget today, and it is read by eye if at all |
| skill evals | every per-skill scenario green at each milestone | dated run records in `docs/evals/` | the eval suite reds any red scenario at each milestone run (INV-99) |
| resume-file form | `NEXT_STEPS.md` is a digest with no redundancy, one live-state block (INV-48; the numeric cap struck on the owner's ~01:10 word, row 576) | the suite's own check | `test_template_states_the_law` holds the template's statement of the law (INV-48) |
| spec prose register | style lint: 0 errors on PRODUCT_SPEC.md | `scripts/spec-style-lint.py` JSON tail | the style-lint gate reds on any error at the pre-show and push gates (INV-83) |
| work board update [target] | no stage delayed by its own board update [default] — the periodic ≤5 s auto-refresh heartbeat this budget once also carried retired 2026-09-03 on the owner's 2026-09-02 12:46 word (`.live-spec/turnkey-contract-composed.md:304`) | the page's own build stamp — the time the generator last wrote the page, read off the rendered board | the generator's own suite timing assertion at its landing (q-816); until that landing the budget stands unwatched [target] |
| settings card render | ≤ 1 s on a pack-sized catalog [default] | the render script's own run, asserted by its matrix row | its matrix-row test (M-206) reds past the 1 s budget, read from the render script's own instrumentation |

A skill's judgment quality beyond the evals has no honest number. It is said by name here and judged
by the human's eye on real landings, never given a vanity metric.
