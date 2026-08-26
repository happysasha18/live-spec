# Skill review — build-pipeline

SKILL-REVIEW

Skill: build-pipeline

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is out of scope for a pack-wide pass over 12 skills)

Verdict: no blocking findings; one non-blocking finding on frontmatter-description completeness.

## What changed

This is not a review of one edit — it is a plan-mandated pack-wide skill-creator pass over every
working skill ahead of a release step and its push gate. `build-pipeline` is read fresh here, at
its current size: it was cut down sharply during today's cutover, from roughly 728 lines to about
66, and this review reads the file as it now stands (67 lines with trailing newline), with no
assumption carried in from its earlier, much larger shape or from prior reviews of that cut.

## Findings

**1. Non-blocking — the frontmatter description, and the body's own framing, both omit the craft
ladder as a reason to use this skill.**

The body carries three distinct sections: `## The craft ladder` (which craft's standards judge
each pipeline step — spec as a product manager, prove as a formal-methods reviewer, architecture
as a software architect, matrix and test as QA, code as a senior developer, verify as the
visitor's own eyes, commit & show as a release hand), `## Setting a project up on the pack` (the
setup walk), and `## Gates worth remembering` (the MINOR-bump gate). But the frontmatter
`description` names only the setup walk and its five spoken trigger phrases ("attach live-spec to
this project," "adopt or install live-spec here," and so on) plus a passing mention that the skill
is "retained ... for the setup walk and the MINOR-bump gate procedure" — it says nothing about the
craft ladder. The body's own intro sentence, right before the craft-ladder section, reads "This
page keeps only the two pieces of real, still-needed craft that have nowhere else to live yet,"
and the closing "Work that belongs elsewhere" section repeats "This skill runs only at two
moments." Both undercount: three H2 sections carry real content, not two. The skill's own README
(`skills/build-pipeline/README.md`) repeats the same "two things" framing and likewise never
mentions the craft ladder.

This is not orphaned or leftover content — it is real and load-bearing. `architecture/
pipeline-and-lanes.md` pins "the craft ladder — step→craft one home" directly to
`skills/build-pipeline/SKILL.md:21`, citing Requirement 51; `matrix/build-pipeline.md`'s M-120 (SPEC
INV-33) requires that "the step→craft ladder ... lives in one home, build-pipeline's step list ...
never a second full ladder statement elsewhere." So the craft ladder's presence here is correct and
intentional — the gap is only in how the skill describes itself. A session that needs "which
craft's standards judge the code step" has no phrase in the frontmatter description pointing it to
this skill; in practice the pack's other skills reach this content by direct file:line pin (as
`architecture/pipeline-and-lanes.md` and `product-prover-pack/SKILL.md` both do for the
MINOR-bump-gate reference), not by a natural-language skill trigger, which contains the practical
risk. It is still a real gap against skill-creator's own standard that a description name
everything a skill does: worth a one-clause fix to the description (naming the craft ladder
alongside the setup walk and the gate) and either correcting "two pieces"/"two moments" to three or
explaining why the craft ladder is not counted as one of the "moments" the skill runs.

Everything else checked clean:

- **Anatomy of a Skill** — `SKILL.md` (67 lines) plus two reference files,
  `references/minor-bump-gate.md` (24 lines) and `references/project-setup.md` (72 lines), both
  well short of needing a table of contents. No scripts/assets, none needed for what this skill
  does.
- **Progressive Disclosure** — 67 lines is unusually short for the pack, but it reads as a
  coherent, deliberately narrowed adapter rather than an underspecified stub: the opening
  paragraph states plainly that this skill is no longer the pipeline's entry point, names what
  moved to `director`, and the banner explicitly disclaims restating `live-spec-base`'s shared
  rules while noting "loaded alone, every section below still runs" — an honest, self-aware
  boundary, not a silent gap.
- **Lack of Surprise** — aside from finding 1, description and body agree; the skill is candid
  about being transitional ("until Packages 5 and 6 give each its own home").
- **Writing style** — imperative and explains WHY (e.g., the cross-cut counter's threshold "is a
  signal, never a push-blocking red, and a boundary still moves only through the architecture step
  and its re-prove" — the reasoning is stated alongside the rule). No bare ALL-CAPS MUST/NEVER.
- **Reference-file consistency** — both reference files exist and are each linked exactly once from
  `SKILL.md` ("Read [references/project-setup.md](references/project-setup.md)" and "see
  [references/minor-bump-gate.md](references/minor-bump-gate.md)"). No dead links, no orphan file
  under `skills/build-pipeline/references/`.
