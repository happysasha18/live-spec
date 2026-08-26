# Skill review — feedback-intake

SKILL-REVIEW

Skill: feedback-intake

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over twelve skills, PLAN.md step 8)

Verdict: one non-blocking finding (frontmatter names a trigger the body never describes); everything
else checked clean.

## What changed

This is not a review of a specific edit. It is the plan-mandated pack-wide skill-creator pass over
every live-spec working skill ahead of PLAN.md step 8 ("Релиз наружу") and its push gate s, which
otherwise reds a substantive skill change with no matching record. `feedback-intake` is reviewed fresh
here as part of that full set.

## Findings

None blocking. Checked against the skill-creator checklist:

- **Frontmatter description — one real, non-blocking gap.** The description names four trigger
  surfaces: "a comment, answer, file, or reaction from a person, a file appearing in inbox/... an
  inbox sweep, or an append to the feedback ledger FEEDBACK.md." The fourth clause reads as if a
  `FEEDBACK.md` append is itself a thing this skill watches for and fires on. The body's own `##
  When it fires` section (lines 29–34) describes only two firing conditions — a handed-in item
  arriving in any session, and an inbox sweep — and never mentions `FEEDBACK.md` as a trigger.
  Every other place `FEEDBACK.md` appears in the body (the routing table, `## The feedback ledger
  (FEEDBACK.md)`) treats it strictly as a write destination this skill appends to, never as
  something it reads from or reacts to. So the description overclaims one trigger the body doesn't
  carry — a small, real gap between what a reader is told to expect and what the skill actually
  does. Non-blocking: the other three trigger clauses are accurate and the overclaim doesn't point
  a reader anywhere actively wrong, just to a firing condition that isn't really there.
- **Anatomy of a Skill** — a single 104-line `SKILL.md`, no `references/` directory. Appropriate for a
  skill whose whole job is one routing table plus the receipt discipline around it — nothing here reads
  as needing offload.
- **Progressive Disclosure** — 104 lines, well under the guideline.
- **Principle of Lack of Surprise** — nothing misleading; "Work that belongs elsewhere" and "What this
  skill deliberately leaves alone" both draw the boundary precisely (never on the agent's own output,
  never opens a queue row on its own judgment — the door owns that verdict).
- **Writing style** — imperative, and the five-row routing table is a clean instance of skill-creator's
  own "defining output formats" pattern — a fixed, scannable table mapping input shape to route to home.
- **Reference-file consistency** — no `references/` directory exists; not applicable.
