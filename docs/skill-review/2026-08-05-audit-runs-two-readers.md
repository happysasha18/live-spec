# Skill review — the audit's reading step runs two readers

SKILL-REVIEW

Skills: text-audit.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds a second reader to the reading step, adds a merge step, and states
what the pair costs. It removes no instruction, and it offers no reduced form of the step.

## What changed

The reading step now runs two cold readers over the same text, and both run on every audit. One works
under the printed rule list at `skills/text-audit/references/reader-prompt.md`. One works under a new
brief at `skills/text-audit/references/unprompted-reader-brief.md`, which prints no rules. That brief
hands over three things: the text, the reader the text is written for, and the task. It tells its
reader to leave the page, open what a claim cites, run the steps, and check a number against its
source. Neither reader sees the other's output.

The loop runs in five steps now, and the new step 3 is the merge. The auditor merges, and the skill
names the auditor as the session running the skill. The merge is written as these steps:

- read both lists whole before matching anything;
- match the stops by the passage each one quotes;
- mark the passages both readers stopped on, and lead the list with them;
- keep every stop one reader found alone, with that reader recorded beside it;
- carry every stop into one ordered list.

The skill says plainly that the two readers label one passage differently, so the match is made on
the passage.

The closing condition still asks for two clean readings. A reading is now a round of two readers. The
loop closes when both readers of a round return zero blocking findings, twice in a row. The
build-test paragraph was pointing at step 4 and now points at step 5.

## Why it was worth a change

Two measurements ran on 2026-08-05. Over three documents, the prompted reader reported 227 stops, of
which 135 survived refutation and 36 blocked. The unprompted reader reported 128, of which 87
survived and 21 blocked. Neither set contains the other.

The prompted reader alone caught sentence mechanics. It found a pronoun with no antecedent, one word
carrying two meanings, a sentence with no actor, and an image with no referent.

The unprompted reader alone caught whether the document can be used. It found these:

- prerequisites the page never states;
- an install section that installs nothing the page promises;
- a link pointing at another repository;
- a rule its own evidence contradicts;
- an arithmetic error in a worked example.

Those readers left the page and checked claims against the tree, and no prompted reader did.

About thirty passages came back from both readers, and every one of them survived refutation. A
second measurement over a publish candidate reproduced the split.

## What the review looked at

**Does the summary line still trigger correctly?** The description is untouched. The change sits in
the body and in one new reference file.

**Is the new instruction stated as an action a reader can take?** Yes. The merge is six ordered
steps, each one an act. The brief prints a pasteable block in the same shape as the existing prompt,
with two slots to fill before pasting.

**Does the body still fit the progressive-disclosure pattern?** Yes. The pasteable block sits in
`references/`, beside the prompt it pairs with. It loads for the task that needs it. The body grew
from 366 lines to 445, which stays under the 500-line guidance. The two paragraphs of measurement
numbers are the part most easily moved to a reference file if the body grows again.

**Could the change be read as permission to run one reader?** The body says both passes run on every
audit, whatever the budget allows. The by-hand section says that one reader alone leaves the round
incomplete and the audit open. It also says that the reading record names the brief that went unread.

**Does it state the cost honestly?** Yes. The body prints the thrown-out shares, 40.5% and 32.0%. It
says that between a third and two fifths of what comes back leads to no repair. It says that one
reading brings back about 26 stops per document and that the pair brings back about 71.

**Does anything now carry two names?** No. The two readers are named once each: the prompted reader
and the unprompted reader. The roles list defines both. The heading "The cold reader" stays as it
was, because the generated prompt file points at that heading by name.

## Findings

None blocking.

Two observations for a later pass. The measurement paragraphs state numbers from two runs on one
project's documents, and a run on another author's prose may return different shares. The skill says
where the numbers came from and leaves that limit unstated.

The full skill-creator eval loop did not run for this change. That loop compares a skill against a
baseline over test prompts and asks the person to review the outputs. Judging this change that way
means running two audits end to end and refuting every stop, which is the measurement the two reports
already carry. This review is the reading pass alone, and the record says so rather than implying a
benchmark that never ran.

## Checks run

`python3 scripts/preshow-register-lint.py` over `skills/text-audit/SKILL.md`, over
`skills/text-audit/references/unprompted-reader-brief.md`, and over this record — clean on each.

`python3 scripts/rule-census.py` — `skills/text-audit/SKILL.md` measures 0 findings with its longest
sentence at 25 words, holding the zero ceiling its record carries.
`skills/text-audit/references/unprompted-reader-brief.md` measures 0 findings with its longest
sentence at 24 words.

`python3 -m pytest tests/test_config_health.py tests/test_reader_prompt_shape.py
tests/test_text_audit_fixtures.py -q` — 50 passed. The repository copy and the installed copy under
`~/.claude/skills/text-audit/` hold the same bytes.

`sh guardrails/check-skill-loadability.sh` — 11 skills load, named, versioned, negative-scoped.

## Owed before the push

`guardrails/rule-census.json` carries no entry for
`skills/text-audit/references/unprompted-reader-brief.md`, and a live document missing from that
record reds `guardrails/check-doc-findings-bound.py`. The file measures 0 findings. Another process
holds `guardrails/` while this change lands, so whoever pushes seeds that entry at 0 first.
