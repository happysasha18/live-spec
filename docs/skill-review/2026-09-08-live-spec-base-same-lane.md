# Skill review — live-spec-base (rule 5 gains the same-lane sub-bullet)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-08
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/scripts/quick_validate.py`,
plus the skill-creator Skill Writing Guide applied by hand. The eval-and-iterate loop the skill
prescribes does not fit a prose rulebook — the same carve-out the earlier records for this skill
state. The reviewer is the session that made the edit; nothing here is an independent read.

Verdict: PASS (`quick_validate.py`, quoted below). Three findings, two folded before this record
was written, one left standing and named.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
(exit 0)
```

## What changed

Rule 5 gained a second sub-bullet: the lane that finds a cause repairs it in the same lane, with
the design reviewer's no-landing named as the one deliberate exception and the reason it is one.
Ten lines, no rule renumbered, no other rule touched.

## Findings

- **Folded before this record: the reason travels with the exception.** A first draft named the
  design reviewer as an exception and stopped there. The guide's "explain the why" line is the
  whole point of the rule — a session that reads only which skill is exempt learns a name, and a
  session that reads why learns the test it can apply to the next case. The bullet now carries the
  reason (a grouping the reviewer surfaces is not a defect anybody meets until a person accepts a
  declaration, so there is nothing for the lane to build).
- **Folded before this record: no imperative stack.** The draft's shape was a rule sentence
  followed by three prohibitions. It now states the rule once, gives the incident that produced it,
  and names the exception — the guide's preference for reasoning over stacked MUSTs.
- **Left standing: the body is 483 lines against the guide's 500-line ideal, and this edit spends
  ten of the remaining seventeen.** The guide's answer at that limit is another layer of
  hierarchy, and this file already has one: `references/rule-origins.md`, where each rule's
  citation, history and worked example live. The rule's incident is stated inline in one clause
  here and has no entry in that reference, which is the same gap the rule-40, rule-41 and rule-43
  records each flagged for their own rules and left unfixed. It stays unfixed here too, for the
  same reason: this record holds no edit authority over `skills/live-spec-base/`, and the gap is
  now on its fourth record rather than its first.
