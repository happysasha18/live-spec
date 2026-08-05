# Skill review — the audit skill says which of its lints only read a spec

SKILL-REVIEW

Skills: text-audit.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds one paragraph that states an existing behaviour of three shipped
scripts. It removes no instruction and adds no new step.

## What changed

The section that lists the mechanical lints opens by telling the reader to run them all before any
reader sees the text. Three of those scripts read a spec section alone. `check-vocabulary.py` reads
the glossary. `check-weak-words.py` and `check-requirement-shape.py` read the acceptance criteria.

A README, an article, or a piece of copy carries neither, so each script exits 1 and names its input
set as empty. The skill now says so, and it says what to do: record the refusal and carry the class
on the grep fallback and the cold reader.

One entry already carried a skip note of its own, for the requirement-shape script. The other two
carried none, so a reader met a refusal the document had not prepared them for.

## Why it was worth a change

A run over ten documents on 2026-08-05 met four such refusals and recorded them as coverage. A
refusal read as coverage is worse than a red, because the class it was meant to hold then belongs to
nobody. The largest class in that run, a term left undefined at its first use, is exactly the class
`check-vocabulary.py` would have held on a spec section.

## What the review looked at

**Does the summary line still trigger correctly?** The line is untouched. The change sits in the
body.

**Does the body still hold together?** Yes. The new paragraph agrees with the requirement-shape
entry below it, which already said to skip that script for a README, an article, or copy. Nothing
now states a rule twice: the earlier entry names its own surface, and the new paragraph names the
three scripts as a group and the reason they share.

**Could the change be read as permission to skip a check?** The paragraph closes the reading that
would allow it. Editing a script or a document to make one of the three pass is named out of bounds,
so a reader meeting a refusal has one lawful move.

**Does it instruct anything new?** One instruction is added: record the refusal in the reading
record. That instruction already stood in the skill's by-hand section for a missing cold reader, so
the shape is the skill's own.

## Findings

None blocking.

One observation for a later pass. The three scripts announce their empty input set in the same
wording, taken from the shared guard at `guardrails/nonempty_input.py`. A reader who meets that
message for the first time reads it as a fault in their own file. A line in the message naming the
surface the script expects would answer them at the point they stop.

## Checks run

`python3 -m pytest tests/test_config_health.py -q` — 32 passed, so the repository copy and the
installed copy hold the same bytes.

`python3 scripts/rule-census.py` — `skills/text-audit/SKILL.md` measures 0 findings with its longest
sentence at 25 words, holding the zero ceiling the record already carried for it.
