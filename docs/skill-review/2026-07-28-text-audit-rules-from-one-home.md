# Skill review — text-audit (its rules now print from the one rule file)

`SKILL-REVIEW`

Skill: text-audit
Date: 2026-07-28
Reviewer: this session. Agents are barred in this window by its own instruction, so the review was
run by the seat against the skill-creator criteria rather than by a fresh reviewer. A fresh reviewer
should re-run it when agents are available; this record names what was checked and what was found.

Verdict: passes with one finding. The finding names a second full statement of the same rules still
shipping inside another skill, and it is recorded as a queue row rather than fixed here.

## What changed

The section headed "The register it holds a text to" carried seven rules written out in the skill's
own words: one idea per sentence, plain words, every term defined at first use, positive framing, no
significance inflation, native short-SVO English, and answer-first ordering. Those same seven rules
already stood in `guardrails/language-rules.json`, which is the one file every rule is edited in.

That section is replaced by a block between `generated:human-prose-rules` markers. The block carries
all 41 rules binding human-prose, each with its rule sentence, the question to ask of a sentence, and
its identifier, printed by `scripts/gen-language-consumers.py` out of the rule file.

## Why the restatement was not simply deleted

Adoption installs four checks and no rule file (`scaffold/guardrails/`). A host that installs this
skill therefore never receives `guardrails/language-rules.json`. Deleting the restatement would have
left such a host with a skill that audits against rules it cannot read. Printing the rules into the
skill keeps one home for editing and ships the skill complete.

## What was checked

- **The block matches a fresh build.** `guardrails/check-language-rules.py` compares what stands
  between the markers with a fresh build and refuses a difference. Proven by hand both ways: one
  edited bullet inside the block is refused by name; the restored block passes.
- **The description still holds.** It promises that the skill "states the register it holds a text to
  and the reader-prompt it hands the cold reader, ready to paste". The block is that register, and the
  reader-prompt is untouched.
- **Size.** 268 lines, inside the ~500-line ideal for a skill body.
- **Nothing else in the skill moved.** The loop, the mechanical lints, the cold reader, the
  reader-prompt, and the closing sections stand as they were.
- **The pointer that closed the old section is replaced.** It named
  `skills/communicator/references/writing-register.md` as the register's full home. The text after the
  block now names the rule file, the writer's page, and the worked example.

## The finding: a second full statement still ships

`skills/communicator/references/writing-register.md` is 136 lines carrying 26 rules written out in
prose. `guardrails/language-rules.json` lists that file among the places that stated its rules before
it existed, so the duplication is known and recorded. It still ships inside the communicator skill,
and a rule edited in the rule file does not reach it.

The repair is the same mechanism this review is about: print the rules into that file from the rule
home between markers, and let the gate refuse a drift. Recorded as a queue row rather than done here,
because this session's task is the audit skill.

## What a fresh reviewer should look at

Whether 41 bullets sitting in the middle of the skill break the reader's path through the procedure.
The seat cannot judge its own text as a stranger would, and this is exactly the kind of question a
cold reader answers and the author does not.
