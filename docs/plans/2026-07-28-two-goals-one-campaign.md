# Two goals, one campaign — the process this project runs from 2026-07-28

## The two goals

**A document a reader understands.** A specification or a skill that a reader cannot follow makes
every conversation about it fail. The reader asks what a word means, the answer takes context, and
the context fills with repair work while the work itself waits.

**A document that stops growing.** The specification grew because one fact was stated in several
places in several shapes. Nothing merged those statements, so each new requirement added its own
wording of an old idea.

Both goals hold the same priority. The work so far has served the first goal alone.

## What the earlier attempt produced, and what it missed

Eighteen readings ran across chunks of the specification over one week. The reports carried counts of
readings and counts of findings. The specification is still hard to read.

Three reasons stand behind that outcome, and each one gets a rule below.

A document is the unit a reader meets. A reading of 250 lines proves that those lines read well, and
it proves nothing about the file around them.

A state is what a person can act on. The sentence "nine readings ran" leaves a person with nothing to
do. The sentence "the audit skill is done, the roadmap is next" hands them the next move.

A class lives in every file that carries it. A stop names one place and stands for the class.
Repairing that one place leaves the class standing everywhere else.

## The two states a document can reach

**Measured clean** means the census counts zero findings in the document: no sentence past the
twenty-five-word cap, no style finding, no register finding.

**Read clean** means two consecutive rounds returned zero stops that block the reader. A round is two
readers given the same document.

A place counts as a blocking stop when both readers of one round stopped there. A place one reader of
the round found alone is recorded as residue, and it blocks nothing. The session settled this on
2026-07-29 and recorded it in `DECISIONS.md`.

Three rounds ran on one document. Each round handed two readers the whole file and the reader prompt
from `skills/text-audit`. The rounds returned fifteen and ten blocking stops, then five and eight,
then nine and four. No single reader's list repeated. Agreement between the two readers of one round
is what lets the loop close.

**Finished** means the document is measured clean and read clean. A document holding one of the two
is named by the state it reached and by the state it still owes.

## The rules this campaign runs by

These rules bind the session that runs the campaign. Each rule is written so two readers give it the
same verdict.

**Rule 1 — one document at a time.** One document is picked and carried to finished before the next
document opens.

**Rule 3 — the unit of reading is the whole file.** A reader is given the entire document. A document
that a single reader cannot hold is too long, and the repair is to shorten that document or to split
it into two.

**Rule 4 — every reader holds nothing.** A reading runs in a fresh session with no package loaded, no
repository history, and no earlier draft. The reader is given the file's text and the reading prompt.

**Rule 5 — every stop is repaired everywhere it occurs.** A blocking stop names one place and stands
for a class of defect. That class is looked up in `guardrails/language-rules.json`, and a class with
no rule there gets a new rule. Every file is then searched for the same class, and the repair covers
every place found.

**Rule 6 — the checks are reviewed after every document.** One question follows every finished
document: which of its stops could a script have caught? A class a script can catch gets that
script. A class no script can catch gets a line saying why.

**Rule 7 — the report names states.** A report says which documents are finished, which document is
in hand, and what stands in the way. Counts of readings, findings, and workers appear under a state
as its evidence.

**Rule 8 — the lead reads reports.** Workers read the documents and repair them. The session leading
the campaign reads what the workers report and verifies the result. The leading session then holds
enough room to carry the campaign.

**Rule 9 — three things go to the owner.** They are taste, policy, and an act outside git that
cannot be undone. Every other question is settled from the document that answers it, and that
document is named.

## The order of documents

The owner stated the ordering principle on 2026-07-28 and recorded it in `DECISIONS.md`: the queue is
ordered by what enters a working context earliest. A document that fills an agent's context on every
turn costs the most, so it is repaired first.

The list below derives from that principle. It is the one order this campaign runs by, and it replaces
the two other lists written on 2026-07-28, in `docs/reports/2026-07-28-document-state-and-plan.md` and
in `docs/handovers/2026-07-28-readability-campaign-handover.md`.

1. The text that enters every turn: `hooks/chat-law-hook.sh`.
2. The text that enters every session at its start: `~/.claude/CLAUDE.md` and the personal profile at
   `~/.claude/live-spec/profile.md`. Both sit outside the measured set today, and joining that set is
   the first step of this group.
3. The file every session reads first: `NEXT_STEPS.md`.
4. `skills/text-audit/SKILL.md` and the four documents it points at: `docs/language-rules.md`,
   `docs/spec-style.md`, `docs/spec-format.md`, `docs/language-worked-example.md`. Every other
   document is checked through this skill.
5. The three skills loaded in every task run by the method: `live-spec-base`, `build-pipeline`,
   `communicator`.
6. `ROADMAP.md`, read whenever a session picks up work.
7. The remaining seven skills.
8. The specification family: `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`.
9. The documents a stranger meets on arrival: `README.md`, `OVERVIEW.md`, `adopt/ADOPT.md`. These
   enter no agent's working context, so they stand behind every document that does.
10. Every remaining live document, worst first.

The queue carries on past this list, and it runs to every live document in the tree.

## The growing specification has no measure today

The size of the specification is measured by nothing. The census counts defects of writing, and it
counts nothing about one fact stated twice.

The first step is a measurement, and it runs before any design. One pass reads `PRODUCT_SPEC.md` and
answers three questions.

- How many requirements state a fact another requirement already states?
- How many requirements share a shape that one requirement could carry with a parameter?
- How many glossary entries name the same thing twice under two words?

That measurement decides what the mechanism against growth has to do. `check-size-ratchet.py` and
`docs/spec-compaction-protocol.md` already exist, and the measurement says whether they reach.

## Which model does which job

Three jobs run under this campaign, and each one names its tier.

**The mechanical repair** takes a stop list and applies it: capitals, whitespace, a phrase swapped
across files. A cheap tier carries it, and the result is checked by a script.

**The reading** decides whether a stranger understands the text. Its quality decides the campaign's
quality.

**The class work** writes a rule, sweeps the repository, and judges what a machine can catch.

The reading tier is settled by one measurement, taken on the first document. The same document is
read by a cheap reader and by a strong reader, and the two stop lists are compared. The tier that
finds what the other finds is the tier the campaign uses.

## Which documents get read — settled on 2026-07-28

Every live document gets readings. Measuring a document with the census costs seconds, and a reading
costs one worker per reader. The rounds repeat until two of them come back with nothing blocking.

A document that has had no reading is unfinished, whatever the census measures it at.
