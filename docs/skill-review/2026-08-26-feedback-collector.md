# Skill review — feedback-collector

SKILL-REVIEW

Skill: feedback-collector

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over twelve skills, PLAN.md step 8)

Verdict: clean — no blocking findings.

## What changed

This is not a review of a specific edit. It is the plan-mandated pack-wide skill-creator pass over
every live-spec working skill ahead of PLAN.md step 8 ("Релиз наружу") and its push gate s, which
otherwise reds a substantive skill change with no matching record. `feedback-collector` is reviewed
fresh here as part of that full set.

## Findings

None blocking. Checked against the skill-creator checklist:

- **Frontmatter description** — states what (offer, on consent, to draft a private upstream note) and
  the precise trigger condition (a rare, strong reaction), and states the two properties most load-
  bearing for correct triggering up front: "only if enabled" and "the skill never sends the note —
  delivery is the human's own step." An agent skimming only the description would not mistake this for
  an always-on or auto-sending skill — good triggering hygiene.
- **Anatomy of a Skill** — a single 142-line `SKILL.md`, no `references/` directory. Appropriate: the
  skill is one short, linear procedure (flag check → strong-signal read → consent ask → distilled note →
  deposit → ledger line), with nothing that reads as needing offload.
- **Progressive Disclosure** — 142 lines, well under the guideline.
- **Principle of Lack of Surprise** — this skill handles a genuinely sensitive action (drafting a note
  that leaves the host and travels to a third party) and its description and body both read as
  unusually careful about that: off by default, positive consent required every time (explicitly
  overriding the pack's usual silence-is-consent default), anonymization required before the draft is
  even shown for consent, and no network call ever made by the skill itself. Nothing misleading; if
  anything the skill is stricter than a casual reading of its one-line description would suggest, which
  is the safe direction for a trust-sensitive action.
- **Writing style** — imperative, explains why at each guard (why consent must be positive here and not
  silence-as-consent like elsewhere in the pack; why the masking must be part of what the user approves,
  not applied after).
- **Reference-file consistency** — no `references/` directory exists; not applicable.
