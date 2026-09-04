# 15:50 — the prover's re-check found four blocking defects in today's own repairs

Work in the git worktree **/private/tmp/ls-wt/recheck** (branch `lane/recheck-fixes`). Never touch
`/Users/sashaabramovich/live-spec` — a full test suite is running there. Do not commit, do not push,
do not run the whole pytest suite. Run only the individual test files you touch.

Read first, in the main tree, both records in full:
`/Users/sashaabramovich/live-spec/docs/prover/2026-09-04-status-renderer-priority-and-feed-delta.md`
and `/Users/sashaabramovich/live-spec/docs/prover/2026-09-04-repairs-recheck.md`. The second is the
review these fixes answer and it states each finding with its reproduction. Then read
`skills/live-spec-base/SKILL.md` rules 36 to 40, rule 39 hardest.

Six items. The first four block a push; the last two ride in the same landing.

## R1 — a check that asserts a pass having compared nothing (blocking)

`guardrails/check-status-view-drift.py` decides which pole it is on by asking whether the checked
repo carries a `VERSION` file. Ordinary host repositories carry `VERSION` files. A host with one,
with a recorded `pack_root`, and with a genuinely drifted `scripts/state-probe.sh` prints
`0 vendored file(s) checked … no drift` and exits 0 — it never opens the manifest. The honest
silence this gate had before became a false green, which is worse.

Fix both halves:

1. **Decide the pole by something that actually names the pack.** A repo is the pack when it is the
   tree the pack itself ships from — the shipped source `scaffold/status-view/state-probe.sh` is
   present in it. A host carries the vendored copy and no `scaffold/` kit of its own. Use that, and
   say in the script's header why the `VERSION` file was the wrong question.
2. **A comparison that compared nothing never prints a pass.** When the check reaches its end having
   opened zero pairs, it says so in those words and reds, or stands down by name with the reason.
   A zero count must never read as clean. This is the finding's own general form and it matters more
   than the discriminator.

Prove both in `tests/test_status_view_drift.py`: a host fixture carrying a `VERSION` file, a
recorded pack root and a drifted copy must red; and a case where nothing resolves must not print a
clean pass. Each red shown before its green.

## R2 — the board prints a false reason (blocking)

The next move is picked from the queued rows alone, so a reopened row (`🔁`) can never win it. Rule
38 in `skills/live-spec-base/SKILL.md` gives the group order — closed since the last push, in hand,
blocked, reopened, queued — and says the next move is the topmost row nobody is working yet. A
reopened row is nobody's work in progress, so it belongs in the candidate set, ahead of the queued
ones.

**The decision is made: the candidate set is the reopened rows first, then the queued ones, and a
blocked row never wins.** Change `scaffold/status-view/state-probe.sh` accordingly and copy it byte
for byte to `scripts/state-probe.sh`. Update Requirement 320 criterion 6 in
`spec/live-status-reporting.md` to name that candidate set in the rule's own words.

The reproduction to turn into a test: a reopened row of the higher-ranking priority beside a queued
row of the lower one. Today the queued row wins and the reason line reads "nothing of higher
priority is free", which is false with the higher row printed one line above.

## R3 — the whole next-move block vanishes silently (blocking, fold with R2)

With no candidate row at all, the block prints nothing and a person cannot tell whether the reader
broke or the work ran out. Print one line saying every row is either finished or in hand, or
blocked, whichever is true. Prove it.

## R5 — the template shipped to fix a defect contradicts itself (blocking)

`templates/PLAN.template.md` names `quick win` as a priority mark ten lines above the priority
statement seeded into it, and that statement names only `critical` and `normal`. The template's own
worked row carries `priority: quick win`, which the reader then ranks last. Make the template
consistent with itself: one vocabulary, stated once, used by its own examples. Prove that the
template's seeded statement parses and that every priority word the template's own examples use is
one the statement names.

## R6 — an adopting host still gets the demand with nothing shipped (fold)

`adopt/install-status-view.sh` never touches a host's `PLAN.md` and never copies the template, so a
host still has no shipped thing naming the statement's form. The lightest honest answer: when the
installer seeds nothing for a host that has no statement, it prints one line naming the form and the
template that carries it, so the person running the installer is told. Do that, and prove the line
appears.

## R12 — an absolute machine-local path recorded into a committed file (fold)

Requirement 319 criterion 9a has the installer record the pack root it installed from, and the
manifest is a file the host commits. A second clone, a second machine or CI then reads a path that
is not theirs. Record it in a form that survives that: relative to the host root where the two trees
sit under one parent, and otherwise say in the criterion that an absolute record is a convenience
for one machine and that a root which does not resolve stands the arm down. Choose the lighter of
the two that actually holds, state it in the criterion, and prove the not-resolving case stands
down rather than comparing against an unintended checkout.

## R9 — the architecture and the matrix still describe the one-pole gate (fold)

`architecture/guardrails.md`'s INV-325 entry and `matrix/guardrails.md`'s row M-634 describe the
gate as it was before today's repairs. Bring both up to what it does now, in each file's own house
style. Keep the architecture entry a pointer rather than a restatement of the spec's law — the
format gate `tests/test_architecture_format.py` reds on a restated law and on any date or history in
a node field.

## What this work must NOT touch

- `PLAN.md`, `README.md`, `skills/`, `evals/`, `docs/prover/`, `docs/skill-review/`, `NEXT_STEPS.md`.
- `spec/design-spec-review.md` and `tests/test_traceability.py`'s TARGET_ROW_OWNERS map — the
  `[target]` finding is the seat's own and is being handled beside you.
- Anything outside this worktree.

## After each spec change

`spec/live-status-reporting.md` is a part of `PRODUCT_SPEC.md`. After editing it, rebuild the index:
`python3 scripts/build-index.py PRODUCT_SPEC.md spec/*.md -o PRODUCT_SPEC.index.md`, then
`python3 -m pytest -q tests/test_index_generated.py tests/test_requirement_shape.py`.
After editing the architecture or the matrix, rebuild with
`python3 scripts/build-index.py ARCHITECTURE.md architecture/*.md -o ARCHITECTURE.index.md`,
`python3 scripts/build-architecture-reference.py ARCHITECTURE.md -o ARCHITECTURE.index.md`,
`python3 scripts/build-index.py TEST_MATRIX.md matrix/*.md -o TEST_MATRIX.index.md`,
`python3 scripts/build-matrix-reference.py TEST_MATRIX.md -o TEST_MATRIX.index.md`,
and run `python3 -m pytest -q tests/test_traceability.py tests/test_architecture_reference.py tests/test_matrix_reference.py tests/test_architecture_format.py`.

## How to wait for a long command

Poll in a loop that sleeps under the shell's foreground limit and checks the run's own output for a
line that only appears at its end. Never end your turn waiting on a background job.

## Report back

Name each item and what you did about it. Paste the red-before-green output for every new case, and
the final run of every test file you touched. Name anything you decided that this brief did not
settle.
