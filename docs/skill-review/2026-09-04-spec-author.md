# Skill review — spec-author

SKILL-REVIEW

Skill: spec-author

Date: 2026-09-04

Reviewer: skill-creator quality lens. The `skill-creator` skill was invoked directly (via the Skill
tool, args: "Review the skill at skills/spec-author for quality (structure, progressive disclosure,
frontmatter description accuracy, writing style). This is a prose/methodology skill with no gradeable
eval output — if the standard eval/benchmark loop needs a gradeable file output this skill doesn't
produce, skip that loop and run the structural/quality review instead."). The tool's own reply
confirmed its full workflow is a draft → spawn with-skill/baseline subagents on test prompts → grade
with assertions → `generate_review.py` benchmark viewer → iterate loop, built for skills with a
*gradeable file output*. `spec-author` produces prose judgment (a grown `PRODUCT_SPEC.md` section) —
there is no fixed right answer a grader script can diff against, and this task's write-set is scoped
to `docs/skill-review/` only, with no room for a `spec-author-workspace/` sibling directory the eval
loop would need. So this record runs the structural/quality review the tool's own guide supports
without the benchmark loop: "Anatomy of a Skill", "Progressive Disclosure", frontmatter-description
accuracy, and "Writing Style", applied by hand against `skills/spec-author/`.

Verdict: holds up structurally — one low-priority cross-file consistency finding, not folded.

## The tool's own verdict

```
$ python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skills/spec-author
Skill is valid!
(exit 0)
```

## Size

`skills/spec-author/SKILL.md`: 20,324 bytes (274 lines).
Whole `skills/spec-author/` directory: 74,482 bytes (`SKILL.md`, `LICENSE`, `README.md`, and eight
reference files under `references/` totaling 593 lines: `anti-patterns.md` 28, `change-record.md` 31,
`completeness-pass.md` 35, `composition-sweep.md` 38, `facet-sweep.md` 144, `glossary.md` 53,
`how-it-reads.md` 130, `primary-unit.md` 48, `the-spine.md` 50).

## The tool's own guide, quoted

> Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of
> hierarchy along with clear pointers about where the model using the skill should go next to follow
> up.
> ...
> Reference files clearly from SKILL.md with guidance on when to read them
> ...
> For large reference files (>300 lines), include a table of contents
> ...
> **description**: When to trigger, what it does. ... All "when to use" info goes here, not in the
> body.

## Findings

1. **Length and progressive disclosure — the strongest example among the four skills reviewed
   today.** 274 lines in `SKILL.md`, with eight reference files (the largest, `facet-sweep.md`, is 144
   lines — well under the tool's 300-line table-of-contents threshold). Every reference is pointed at
   from the body with a one-line summary of what it holds and a "See [references/x.md] for..."
   pointer, matching the guide's "Reference files clearly from SKILL.md with guidance on when to read
   them" almost to the letter. **No fix needed.**
2. **Frontmatter description accuracy.** The description ("Use to start a new product spec, add a
   feature to an existing spec, or keep a spec in sync with behavior changes... Documenting
   already-built code after the fact and a prototype sketch that carries no spec stay outside it")
   matches the body's own "Work that belongs elsewhere" section fact for fact: retro-documenting,
   prototypes, the skip-boundary edit, and the product-prover redirect are all named there too.
   **No fix needed.**
3. **Writing style.** Zero hits for caps `ALWAYS`/`MUST`/`NEVER` in the body — obligations are stated
   in lowercase prose with reasons attached ("A fence is not new law and earns no new matrix row — the
   cited clause's row already carries its never-side"). **No fix needed.**
4. **Missing the pack-directory footer three of the other four reviewed skills carry.** `architect`,
   `test-author`, and `design-reviewer` (this session's other three reviews) each close with a "> The
   pack, whole:" block listing every skill in the pack and its one-line job. `spec-author` has no such
   block — it closes on the "Pairing with product-prover" table instead. Checked against the wider
   pack: this footer is not universal (`director`, `build-pipeline`, `product-prover`, and `publish`
   also lack it), so this is not `spec-author` uniquely falling out of a house norm — it is a
   pack-wide inconsistency spec-author happens to sit on the missing side of. **Not folded**: an
   editorial-only addition to a file already at a healthy 274/500 lines is exactly the kind of
   unrequested-machinery diff this task is scoped to record, not to write; worth a session's attention
   only alongside the wider "does every skill need this block" question across the whole pack, not as
   a spec-author-only patch.

Findings: 4 raised, 3 already clean (no fix), 1 real but low-priority and left open by design (a
pack-wide question, not a spec-author defect).
