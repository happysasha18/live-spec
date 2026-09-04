# Skill review — build-pipeline

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-09-04
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/build-pipeline/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop (spawn with-skill vs. baseline subagents, grade assertions against a
gradeable file output, benchmark) does not fit here: build-pipeline is a setup-walk-and-gate-
procedure skill with no file artifact it produces that a grader could check — the structural review
below is what skill-creator actually supports for a skill of this shape.

Verdict: PASS (`quick_validate.py`, quoted below) — one open, non-blocking frontmatter finding,
pre-existing since 2026-08-26 and not folded here (this record holds no edit authority over
`skills/build-pipeline/SKILL.md`). No leftover August-cutover material found.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/build-pipeline
Skill is valid!
(exit 0)
```

`quick_validate.py` is Anthropic's own packaging validator (the same check `package_skill.py` runs
before producing a `.skill` file): frontmatter YAML parses, only allowed keys are present, `name` is
kebab-case, `description` is ≤1024 characters with no angle brackets. All pass; no scriptable defect
found.

## Sizes

- `skills/build-pipeline/SKILL.md`: 4,099 bytes, 67 lines.
- `skills/build-pipeline/` (whole directory, `wc -c` summed over all five files —
  `SKILL.md`, `README.md`, `LICENSE`, `references/minor-bump-gate.md`,
  `references/project-setup.md`): 14,187 bytes.

## Checked against the August cutover (q-817's own question)

This skill was cut back from a 728-line fixed pipeline orchestrator to a ~65-line adapter on
2026-08-25 (`docs/skill-review/2026-08-25-build-pipeline-cutover-adapter.md`), keeping only the
craft ladder, the setup-walk pointer, and the MINOR-bump-gate pointer — everything else (the door,
work-kind table, footprint scale, request-kind table, the old nine-step sequence) moved to
`director`. Read the current body end to end against that cut: nothing here reads like debris the
cut should have carried away. The "Work that belongs elsewhere" section is itself the boundary
statement, naming `director` as the sole destination for any accepted change. The single open
finding below is not about leftover material — it is a stale *description* line pointing at
material that correctly stayed.

## Findings

1. **Frontmatter `description:` still does not name the craft-ladder section.** The body's first
   substantive section, "## The craft ladder — which craft's standards judge each step," is real,
   load-bearing content (which craft's own standards judge spec/prove/architecture/matrix/test/
   code/verify/commit) — but the `description:` line only speaks to the setup walk and the
   MINOR-bump gate. A reader deciding whether to open this skill from the description alone would
   not learn the craft ladder lives here. **Not fixed here — pre-existing, already tracked.** First
   raised in `docs/skill-review/2026-08-26-build-pipeline.md` and reconfirmed still open and
   unaffected by later wording fixes in `docs/skill-review/2026-08-27-build-pipeline.md`; this
   record's write-set is `docs/skill-review/` only, and the fix belongs with whichever future real
   edit to `SKILL.md` next touches this file, per the standing rule against re-touching a skill body
   with no other need.
2. **Progressive Disclosure and Anatomy check out clean.** 67-line `SKILL.md`, well under the
   ~500-line ideal; two reference files (`minor-bump-gate.md`, 25 lines; `project-setup.md`, 72
   lines), both under the 300-line threshold that would call for a table of contents; no `scripts/`
   or `assets/` needed and none present. No finding.
3. **Writing Style.** The body explains why it keeps only two pieces ("the two pieces of real,
   still-needed craft that have nowhere else to live yet") rather than issuing bare imperatives; no
   heavy-handed all-caps MUSTs found. No finding.
