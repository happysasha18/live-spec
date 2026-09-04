# Skill review — architect

SKILL-REVIEW

Skill: architect

Date: 2026-09-04

Reviewer: skill-creator quality lens. The `skill-creator` skill was invoked directly (via the Skill
tool, args: "Review the skill at skills/architect for quality (structure, progressive disclosure,
frontmatter description accuracy, writing style). This is a prose/methodology skill with no gradeable
eval output — if the standard eval/benchmark loop needs a gradeable file output this skill doesn't
produce, skip that loop and run the structural/quality review instead."). The tool's own reply
confirmed the same disproportion the 2026-09-03 director review already found: its full workflow is a
draft → spawn with-skill/baseline subagents on test prompts → grade with assertions →
`generate_review.py` benchmark viewer → iterate loop, built for skills that produce a *gradeable file
output* (a .docx, a chart, a code transform). `architect` produces prose judgment on a proven spec —
there is no fixed right answer a grader script can diff against, and no `docs/skill-review/`-scoped
subagent workspace to run that loop in under this task's write-set. So this record runs the
structural/quality review the tool's own guide supports without the benchmark loop: its "Anatomy of a
Skill", "Progressive Disclosure", frontmatter-description-accuracy, and "Writing Style" sections,
applied by hand against `skills/architect/`.

Verdict: holds up — no findings that call for a fix.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/architect
Skill is valid!
(exit 0)
```

## Size

`skills/architect/SKILL.md`: 14,675 bytes (201 lines).
Whole `skills/architect/` directory: 17,023 bytes (`SKILL.md` plus one reference file,
`references/architecture-step-detail.md`, 36 lines).

## The tool's own guide, quoted

> Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of
> hierarchy along with clear pointers about where the model using the skill should go next to follow
> up.
> ...
> **description**: When to trigger, what it does. This is the primary triggering mechanism - include
> both what the skill does AND specific contexts for when to use it. All "when to use" info goes here,
> not in the body.
> ...
> Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory
> of mind and try to make the skill general and not super-narrow to specific examples.

## Findings

1. **Length and progressive disclosure.** 201 lines is well clear of the tool's 500-line ceiling, so
   no hierarchy pressure exists yet. The one reference file it does carry
   (`references/architecture-step-detail.md`, 36 lines) is pointed at from the body three times, each
   time naming what it holds ("in the words the step first used") rather than a bare link — matches
   the guide's "Reference files clearly from SKILL.md with guidance on when to read them." **No fix
   needed.**
2. **Frontmatter description accuracy.** The description ("Use to write or update ARCHITECTURE.md
   from a proven spec... invoke this skill directly, not only as a step inside a larger pipeline")
   matches the body's own closing "Work that belongs elsewhere" section verbatim in intent: "Use this
   skill directly whenever a proven spec is in hand and the task is producing or updating the
   structure that carries it." No drift between what the frontmatter promises and what the body does.
   **No fix needed.**
3. **Writing style.** A search for the tool's flagged anti-pattern (`ALWAYS`/`MUST`/`NEVER` in caps,
   the "heavy-handed musty MUSTs" the guide warns against) returns zero hits in the body — the file
   already writes obligations in lowercase prose with the reason stated alongside ("never from the
   document's own prose, memory, or a worker's summary; those are leads to verify, not facts"),
   matching the guide's preferred register. **No fix needed.**
4. **Where the paths point.** The skill opens with an explicit note that `templates/`, `guardrails/`,
   and `scripts/` belong to the external pack repo rather than a bundled `scripts/`/`assets/` folder —
   this is the skill's own documented design (an installed skill sits beside the pack checkout), not
   an omission against the tool's "Anatomy of a Skill" layout; the guide lists bundled resources as
   optional. **No fix needed.**

No findings against this skill required a fix; none were folded because none were raised.
