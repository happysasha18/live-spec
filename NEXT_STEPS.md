# Next steps — live-spec

## LIVE STATE (2026-07-28) — start here

The one task is to make this project's documents readable enough that an agent can build from them
without asking a question.

Read `docs/reports/2026-07-28-document-state-and-plan.md` first. It carries every live document with
its count, the worst sections, and the mechanics this page states in short.

Then repair the prose fields inside `guardrails/language-rules.json`: `name`, `rule`, `reader_test`,
`notes`, and the `examples` pairs. Every other field is machine input. Five files are built from that
one: `docs/language-rules.md`, `docs/language-rule-coverage.md`, `hooks/language-laws.json`, and a
marked block inside each of `docs/language-defects.md` and `skills/text-audit/SKILL.md`. Rebuild with
`python3 scripts/gen-language-consumers.py`.

## The two bars

**The cheap floor** is a count from `python3 scripts/rule-census.py`: sentences past the 25-word cap,
style findings, register findings. The record of counts is `guardrails/rule-census.json`, and gate aa
refuses a push where a document stands above its recorded count. A document recorded at zero reds on
its first finding.

**The reader bar** is two readings in a row that stop nobody. Each reading is one fresh agent session
holding no context on this project, reading the one document alone, under the prompt inside
`skills/text-audit/SKILL.md`. A stop blocks when the reader could not act, or would have acted wrongly.

Passing the floor is no quality claim. This page stood at zero on the floor and stopped two fresh
readers 13 and 12 times. No document has passed the reader bar yet.

## The order of work

Every step below stands today. The reading question was settled on 2026-07-28, so no step waits on it.

1. The prose inside `guardrails/language-rules.json`.
2. The three files a stranger meets first: `README.md`, `OVERVIEW.md`, `adopt/ADOPT.md`.
3. The three skill files loaded in every session: `skills/live-spec-base/SKILL.md` at 229 findings,
   `skills/build-pipeline/SKILL.md` at 262, `skills/communicator/SKILL.md` at 182.
4. `ROADMAP.md`, at 215 findings. Its rows are how this project states the work it will do, so a row
   phrased loosely sends the next session at the wrong thing.
5. The requirements of `PRODUCT_SPEC.md` those documents point a reader at.
6. The rest of `PRODUCT_SPEC.md`, highest count first.

## Three things block this work

**A test pins a phrase inside one line.** 79 test files assert an exact phrase, and 68 of their helpers
return the file unflattened. A repaired sentence that re-wraps fails a passing test; twelve did today.

**The reader bar carries no gate.** The floor is held by gate aa, and nothing holds a reading. The
repair is a record per document carrying the text's fingerprint, and a gate reading it at a minor
version bump.

**The task's baseline has no record.** No file names which six requirements were handed to the fresh
agent, or what it produced.

## The reader bar reaches every live document

Settled on 2026-07-28. The reader bar runs over every live document in this tree. The queue puts
first what enters a working context earliest, which is the entry documents and the pack skills.

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When HEAD has moved, read what changed, then run
`bash guardrails/fence-refresh.sh`. It records the commit you started from, and a commit refuses while
that record and HEAD disagree.

Never discard uncommitted work. No session and no worker runs any of these:

- `git checkout -- <path>` or `git checkout .`;
- `git restore`, outside `--staged`;
- any form of `git stash`;
- `git reset` with `--hard`, `--merge`, or `--keep`;
- `git clean` with `-f` or `-x`.

To put a file back, write back the bytes you read before you changed it. This rule was broken four
times, and two of those breaks destroyed work.

A test result is the printed count of passes and failures. Write the output to a file:
`python3 -m pytest -q > <scratch>/suite.log 2>&1`, then read the last line. A run that dies before a
test starts can still exit zero.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py --freeze
PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

These numbers are free, so two lines of work do not collide: requirement 304, INV-303, E-36, T-25,
M-491, queue row 529. A number is taken by writing it into its document, and the free number here is
raised in the same commit.

## The owner's standing instructions

Run a whole movement alone: one wish carried from its first edit to a green suite and a push. Save and
publish on green without asking, which means commit the work and push it to this project's remote on
GitHub. Write documents in plain English. Run every gate: the checks in `guardrails/`, which the
`pre-push` hook runs as one chain, each holding the push until its fault is repaired.

Before you ask the owner anything, check whether an existing document already answers it. If it does,
act on that answer and cite the document. Name every request as one-time or standing before you act on
it, and say which it is.
