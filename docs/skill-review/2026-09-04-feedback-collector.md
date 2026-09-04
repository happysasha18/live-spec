# Skill review — feedback-collector

SKILL-REVIEW

Skill: feedback-collector

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/feedback-collector/`, plus the skill-creator SKILL.md's own Skill Writing Guide
(Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style)
applied by hand. The eval/iterate loop needs a gradeable file output to compare with-skill vs.
baseline runs against; feedback-collector's own output is a drafted note plus a human consent step,
not a fixed artifact this review can score, so that loop does not apply — the structural review
below is what skill-creator actually supports for a skill of this shape.

Verdict: no findings — the skill passes the tool's own validation cleanly.

## The tool's own verdict

```
$ python3 scripts/quick_validate.py skills/feedback-collector
Skill is valid!
(exit 0)
```

## Sizes

- `skills/feedback-collector/SKILL.md`: 7509 bytes, 139 lines.
- `skills/feedback-collector/` (whole directory, `wc -c` summed over all files): 11487 bytes.

## Findings

1. **Frontmatter is valid YAML, name is kebab-case, description under the 1024-char cap** —
   confirmed by the tool's own pass above. No fix needed.
2. **139 lines**, well under the guide's "<500 lines ideal" ceiling, and the skill carries no
   `references/` directory. No fix needed.
3. **No `MUST`/`NEVER`/`ALWAYS` in all-caps** anywhere in the file — no yellow flag to raise.
4. **Frontmatter description matches the body.** The description ("only if enabled... offer
   drafting a private note... the skill never sends the note") lines up with the "Before anything:
   the flag" section, which gates the whole skill behind an explicit off-by-default host setting.
   No finding.
