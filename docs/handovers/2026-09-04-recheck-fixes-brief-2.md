# 17:2x — finish the prover re-check's remaining findings

You work in `/Users/sashaabramovich/live-spec`, on the branch **`lane/recheck-fixes`**, already
checked out. No suite is running there. **Do not commit. Do not push. Do not run the whole pytest
suite.** Run only the individual test files you touch. No background jobs — every command runs in
the foreground.

R1 and R2/R3 are already done on this branch and their tests pass. What is left is below.

Read first, in full:
- `docs/handovers/2026-09-04-recheck-fixes-brief.md` — the original brief, for R6, R9, R12's own
  statements.
- `skills/live-spec-base/SKILL.md` rules 36 to 41.

## 1. R5 — the root cause is the parser, not the template (blocking)

`tests/test_priority_order.py::test_the_templates_seeded_statement_parses_and_names_every_word_its_own_examples_use`
is red. The template already names `critical`, `quick win`, `normal` in its seeded "Words used
here" list, in that order, and its worked wish row uses `priority: quick win`. The list is correct.

The defect is in `scripts/plan_checks_core.py`: `_PRIORITY_WORD_RE` is
`r"^\s+\d+\.\s+`([a-z][a-z0-9-]*)`"` — it accepts no space, so a backticked two-word priority name
never parses and the word its own statement declares silently ranks last. Requirement 320 criterion
1a says the priority words are "the backticked names of its indented numbered sub-items" and puts
no single-token limit on them, so the parser is narrower than the law it implements. **Widen the
regex to accept a multi-word backticked name** (inner single spaces, no leading or trailing space),
and say in the comment above it why, in one line.

Then check every other reader of that word for the same narrowness: the priority field parser that
reads `priority:` out of an intake note, and `priority_rank`. If either splits on whitespace or
matches a single token, fix it the same way. Grep for the callers before you edit.

Prove it: a case in `tests/test_priority_order.py` where a plan names a two-word priority word and
a row carrying it ranks by it rather than last. Red before green, pasted.

If `scaffold/status-view/` vendors a copy of `plan_checks_core.py` or of that regex, the copy
changes with it and stays byte-identical.

## 2. The two director-route fixtures (blocking)

`tests/test_director_route_end_to_end.py::TestTheRecordedStateNamesOneNextAction` has two red cases.
Both expect the old rule, where a row already in hand won the next move. Rule 38 says the next move
is the topmost row nobody is working yet, and the renderer now follows rule 38. Bring the two
fixtures to rule 38 — the assertion changes, not the renderer. Read the fixture's plan rows to see
which row rule 38 actually names, and make the test say that with the reason in a comment.

Do not touch the renderer to make these pass.

## 3. R6 — the installer tells an adopting host what it seeded nothing for (fold in)

Per the original brief's R6. `adopt/install-status-view.sh`, when it seeds nothing for a host that
carries no priority statement, prints one line naming the statement's form and
`templates/PLAN.template.md` as the thing that carries it. Prove the line appears.

## 4. R12 — the recorded pack root (fold in). **The decision is made, do not re-open it.**

`adopt/install-status-view.sh` line ~129 records `manifest["pack_root"]` as an absolute path into a
file the host commits, so a second clone, a second machine or CI reads a path that is not theirs.

Record it **relative to the host root when the two trees resolve under a shared parent** (the
ordinary `~/live-spec` beside `~/my-project` layout — `os.path.relpath(pack_root, host_root)`),
and absolute only when they do not. `guardrails/check-status-view-drift.py` resolves a relative
recorded value against the host root before using it; an absolute one it uses as it stands.

Say both halves in Requirement 319 criterion 9a in `spec/live-status-reporting.md`: the record is
relative where the trees sit under one parent so a second checkout reads its own pack, and an
absolute record is a convenience for one machine which, where it does not resolve, stands the arm
down rather than comparing against an unintended checkout.

Prove: an installer case recording a relative value for a sibling layout, and a check case reading
that relative value and finding the drift.

## 5. R1's own leftover — the same wrong question, one line down

`guardrails/check-status-view-drift.py` line ~196 still validates the resolved pack root by asking
whether it carries a `VERSION` file. That is the question R1 threw out: an ordinary host project
carries one, so a recorded root pointing at the wrong checkout passes as the pack. Use the
`_is_pack_root` helper the same file already defines. Adjust the stand-down message's words if they
name the VERSION file. The existing stand-down test must stay green; add one for a resolved root
that is not the pack.

## 6. R9 — the architecture and the matrix still describe the one-pole gate (fold in)

Per the original brief's R9: `architecture/guardrails.md`'s INV-325 entry and `matrix/guardrails.md`
row M-634. Keep the architecture entry a pointer rather than a restatement of the spec's law, and
put no date or history in a node field — `tests/test_architecture_format.py` reds on both.

## What this work must NOT touch

`PLAN.md`, `README.md`, `skills/`, `evals/`, `docs/prover/`, `docs/skill-review/`, `NEXT_STEPS.md`,
`spec/design-spec-review.md`, `tests/test_traceability.py`'s TARGET_ROW_OWNERS map. Nothing outside
this repository.

## After each spec change

`spec/live-status-reporting.md` is a part of `PRODUCT_SPEC.md`. After editing it:
`python3 scripts/build-index.py PRODUCT_SPEC.md spec/*.md -o PRODUCT_SPEC.index.md`, then
`python3 -m pytest -q tests/test_index_generated.py tests/test_requirement_shape.py`.

After editing the architecture or the matrix:
`python3 scripts/build-index.py ARCHITECTURE.md architecture/*.md -o ARCHITECTURE.index.md`,
`python3 scripts/build-architecture-reference.py ARCHITECTURE.md -o ARCHITECTURE.index.md`,
`python3 scripts/build-index.py TEST_MATRIX.md matrix/*.md -o TEST_MATRIX.index.md`,
`python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o TEST_MATRIX.index.md`,
then `python3 -m pytest -q tests/test_traceability.py tests/test_architecture_reference.py tests/test_matrix_reference.py tests/test_architecture_format.py`.

## Report back

Name each of the six items and what you did about it. Paste the red-before-green output for every
new case and the final run of every test file you touched. Name anything you decided that this
brief did not settle. If an item turns out to rest on a premise that is false, say so and stop on
that item rather than inventing a repair.
