# Handover, 2026-07-28 21:40 — the readability campaign

## Read these two files first

`docs/plans/2026-07-28-two-goals-one-campaign.md` carries the whole campaign: two goals, ten rules,
the order of documents, and the open question. Read it before anything else.

`NEXT_STEPS.md` carries the older plan and the repository's working rules. The campaign plan replaces
its order of work.

## The order of documents, by how often each one enters an agent's context

| | file | how often | measured |
|---|---|---|---|
| 1 | `hooks/chat-law-hook.sh` | every turn | in hand now |
| 2 | `~/.claude/CLAUDE.md` | every session start | outside the live set |
| 3 | `~/.claude/live-spec/profile.md`, 217 lines | every session start | outside the live set |
| 4 | `NEXT_STEPS.md` | every session start | zero |
| 5 | `skills/live-spec-base/SKILL.md` | every task run by the method | 229 |
| 6 | `skills/text-audit/SKILL.md` | every check | zero, one owner reading |
| 7 | `skills/build-pipeline/SKILL.md` | every non-trivial change | 261 |
| 8 | `ROADMAP.md` | picking work | 215 |
| 9 | `PRODUCT_SPEC.md` | building | 1831 |

Rows two and three sit outside the measured set of 109 documents. Adding them is queued work.

## What runs right now

A lead worker carries `hooks/chat-law-hook.sh` to finished. It measures, repairs, spawns readers,
repairs each blocking stop, and repeats until two readings return nothing blocking. It writes its
record to `docs/language-reads/2026-07-28-read16-chat-law-hook.md`. Its report is owed to the next
session.

The installed copy at `~/.claude/hooks/chat-law-hook.sh` is untouched. Installing the repaired file
is a separate step after the run.

## What sits uncommitted in the tree

- `tests/` — 18 files, every quoted phrase from a document now compared with whitespace collapsed.
  Suite before and after: 1 failed, 2223 passed. The single failure is the prover-record gate.
- `tests/test_rule_census_prose_units.py` — new, three tests, proved red before green.
- `scripts/rule-census.py` — a list of short names written with the interpunct stops counting as a
  sentence. Three counts fell because of it.
- `guardrails/language-rules.json` — four rules added (r65 plain vocabulary, r66 the register of a
  request, r67 a term with no path to its definition, r68 a placeholder word), r14's reader test
  sharpened, examples added to r02 and r14. Five generated files rebuilt.
- `guardrails/rule-census.json` — re-seeded four times today. Every re-seed was checked, and no
  count rose.
- `docs/prover/2026-07-28-requirement-302-findings-ratchet.md` — the prover pass the push gate owes.
  Eight defects to fix, listed in the record.
- `docs/language-reads/2026-07-28-read14-text-audit-skill.md` and `-read15-campaign-plan.md` — two
  readings by the owner.
- `docs/briefs/reader-prompt.md`, `repairer-prompt.md`, `consistency-prompt.md` — the three worker
  prompts, each measuring zero.
- `docs/plans/2026-07-28-two-goals-one-campaign.md` — the campaign, measuring zero.
- `inbox/2026-07-28-from-tlvphotos-a-parked-question-stays-in-the-list-after-its-answer-arrives.md`
  — a finding handed in from another project, unanswered.

Nothing is committed. Nothing is pushed. The push gate refuses until the prover record is committed.

## The eight defects the prover found in the counting gate

The first one is the one the owner settled tonight: a document's recorded count may only fall. The
command the gate prints as its remedy rewrites every count, growth included. The record at
`docs/prover/2026-07-28-requirement-302-findings-ratchet.md` lists all eight with their proofs.

## What the owner settled today

- A document's count moves down alone. The command that writes the record must refuse a higher
  number.
- A document with no reading is unfinished, whatever it measures.
- Every place the owner stops becomes a class, and the class is swept across the repository.
- A document is written to the rules of its surface, whatever register the request carried.
- A sentence earns its place by changing what the reader does.
- Every worker prompt is written by a worker holding an empty context.
- The word list behind the plain-vocabulary rule is never kept by hand.
- Every live document gets a reading by a fresh reader (settled 2026-07-28).
- The queue is ordered by what enters a working context earliest, and the entry documents and the
  pack skills stand at its front (settled 2026-07-28).

## What waits for the owner

Nothing waits on the owner today. The reading question was settled on 2026-07-28, and the measurement
below is this session's to run.

The measurement of the growing specification: 302 requirements, 7697 lines, 248 glossary entries. The
campaign plan already commits to running it. The size of the first sample is a cost call, with no
taste, policy, or irreversible act behind it. The proposal on record is a sample of 30 requirements.

## The next three moves

1. Take the lead worker's report on `hooks/chat-law-hook.sh`, install the repaired file, and run the
   suite.
2. Fix the counting gate so a recorded count refuses to rise.
3. Commit the prover record, then commit the rest by name, then push on a green suite.
