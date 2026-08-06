# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-06, 15:08)

Three landings finished their code and tests today, and their shared documents were written in one
pass by a single writer. Nothing is pushed yet.

Four numbers on the two front pages were wrong. They were the gate count, two line counts under
`skills/`, and a worker-run count that moves between readings minutes apart. Every count this repository publishes
about its own tree now has a declared measurement and a home on its page. Gate ad re-measures each of
them on every push. Queue row 555.

The audit skill told an agent to run two checks that judge this pack's own document set. In a host
project those two would read nothing and print green. `scripts/check-registry.json` is the record of
what each runnable file is, and gate ae holds it. That landing's own files were still being written
while these documents were landed. So matrix rows M-505 to M-511 read *todo* and name their test file
as the future owner. Queue row 556.

Saying "attach live-spec to this project" now reaches a walk. The entry sits on one skill
description, a routing card resolves the pack's own tree, and `adopt/START.md` is the founding walk
for an empty directory. It was proven by a founding run against a throwaway tree to a green scaffold
suite. Queue row 557.

The public edition of the prover skill published a finding count from two runs that no longer
reproduces. Two fresh runs measured twenty-nine and twenty-five kinded findings, and the page now says
what those runs support.

## Forward queue

1. Push the three landings. Each of rows 555, 556 and 557 closes at the push, and the freeze baseline
   for the spec, the architecture and the matrix is owed before it.
2. When the check-registry landing's own files arrive, flip matrix rows M-505 to M-511 to *built* and
   pin the two files under the guardrails node in `ARCHITECTURE.md`.
3. The rule census refuses to write its record while `editions/product-prover/README.md` (14 recorded,
   18 measured) and `editions/product-prover/SKILL.md` (24 recorded, 27 measured) stand above their
   ceilings. Gate aa stays red until those two come down. Two new live files, `adopt/START.md` and
   `skills/build-pipeline/references/project-setup.md`, get their first entry in the same run.
4. Row 558: give the opening read an artifact and make the handover gate refuse a push from a session
   that wrote none. The newest handover under `docs/handovers/` is dated 2026-07-29.
5. Row 559: put a machine over the reading panel — a gate that reds a round whose two readers came
   from one brief, and a stated test for what counts as a stop that blocks.
6. Row 560 waits on your word: the surface registry a new project copies carries two names, and the
   rename has been offered twice with no answer.
7. Row 561: give the settings ladder a `pack.tree` line, which the setup walk's routing card needs
   and nothing reads yet.
8. Run the next reading round on the audit skill, with one prompted reader and one unprompted reader.
9. Take rows 532 to 546 through the pipeline. Rows 537 and 538 open with a freshness re-check, since
   the reds they cite no longer reproduce.

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. It gives the hours each file still owes. Each column carries a note saying what it counts
and what it aims at. Build it with `python3 scripts/measurements-table.py`. Every number stated to
the person who decides what ships carries five things. It names what it counts and in what unit. It
names the decision it informs, and what changes when it moves. It names the command that produced
it and the value it aims at. A bare number is a defect of the same kind as an undefined term.

`guardrails/tree-counts.json` is the home for every count this repository publishes about its own
tree. It carries the measurement that produces each count and every page that states it, and gate ad
re-measures them on every push. Four surfaces stay outside it, each with its own later row. A number
a session writes into chat. A number in a rendered artifact. A count inside a skill body. A count on
an undeclared page.

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When the commit it names differs from the one you recorded at the
start of your session, read what changed and run `bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs `git checkout -- <path>`,
`git checkout .`, or `git restore` outside `--staged`. The same holds for `git stash` in every
form. It holds for `git reset` with `--hard`, `--merge` or `--keep`, and for `git clean` with `-f`
or `-x`. To put a file back, write back the bytes you read before you changed it.

Never give two workers the same file. Two workers held one file on 2026-07-29, and the second read
the first one's edits as an intrusion and reverted them. A test result is the printed count of
passes and failures. Run `python3 -m pytest -q > <scratch>/suite.log 2>&1` and read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py
--freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

`bash guardrails/pre-push` runs the whole push gate set, listed in `guardrails/README.md`. New
requirements, invariants and queue rows take the next identifier above the highest one in use in
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md`. Read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask. Publish
once the suite passes. Write documents in plain English. Before you ask the person who decides what
ships anything, check whether a document already answers it. If it does, act on that answer and
cite it. Say aloud whether a request is one-time or standing before acting.
