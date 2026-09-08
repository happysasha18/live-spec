# Skill review — design-reviewer (the no-landing bullet names itself an exception)

SKILL-REVIEW

Skill: design-reviewer

Date: 2026-09-08
Reviewer: skill-creator (Anthropic), `~/.claude/skills/skill-creator/scripts/quick_validate.py`,
plus the skill-creator Skill Writing Guide applied by hand. The reviewer is the session that made
the edit; nothing here is an independent read.

Verdict: PASS (`quick_validate.py`, quoted below). Two findings, one folded, one considered and
rejected with its reason.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/design-reviewer
Skill is valid!
(exit 0)
```

## What changed

The closing "Never file a defect, never hold a landing" bullet gained four lines: it is the one
deliberate exception to `live-spec-base` rule 5, the reason it is one, and a sentence saying to
read it as this pass's own exception and never as the shape of an ordinary brief. Four lines, no
other section touched, the body at 435 lines.

## Findings

- **Folded before this record: the closing sentence is the one that does the work.** Without it a
  reader takes the exception and generalizes it, which is the exact failure the incident of
  2026-09-08 recorded — four briefs written that day in the reviewer's shape. Naming the exception
  without saying what not to do with it would have left the sentence pointing at nothing.
- **Considered and rejected: the frontmatter description still says only "It holds no landing;
  every finding is a recommendation or a question."** The description's job is triggering, and a
  clause about why the rule is an exception adds no trigger and costs the always-in-context budget
  the guide's first loading level is about. A reader who reaches the exception has already loaded
  the body, where the reason stands.
