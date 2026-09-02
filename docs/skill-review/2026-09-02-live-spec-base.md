# Skill review — live-spec-base (the register-compression landing, 40,443 → 22,688 bytes)

SKILL-REVIEW

Skill: live-spec-base
Date: 2026-09-02
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand
against the compressed body and its new `references/rule-origins.md` split; the tool's own
eval/iterate loop is disproportionate for a wording-only compression that changes no rule's
meaning, number, or SPEC anchors)

Verdict: three findings below, none folded — this record holds no edit authority over
`skills/live-spec-base/SKILL.md` or its `references/` tree.

## What changed

`skills/live-spec-base/SKILL.md` went from 40,443 bytes (482 lines) to 22,688 bytes (314 lines).
Every one of the twenty-two shared rules kept its number and now reads as one imperative sentence
carrying its SPEC codes and the check that reads it; the sub-laws under rules 6, 7, 13 and 31
compressed to one line each. Each rule's dated citation, history, justification and worked example
moved out to the new `skills/live-spec-base/references/rule-origins.md` (6,539 bytes), pointed at
once from the body ("Each rule's background... lives in references/rule-origins.md, opened only to
dispute or amend a rule"). `references/` now holds six modules: `glossary.md`, `worked-examples.md`,
`settings-ladder.md`, `worker-restore.md`, `session-handover.md`, `rule-origins.md`. The frontmatter
`description` was rewritten to enumerate all six by name, where the pre-compression description
named only three (`glossary`, `worked examples`, `settings ladder`).

## Findings

**F1 — `references/session-handover.md` carries a live, SPEC-backed rule with no pointer anywhere
in the body.** The module states the session-open and session-close protocol behind SPEC INV-302
(read the previous session's extract, cross-check `DECISIONS.md` and `NEXT_STEPS.md`, write the
closing handover) and is read by `tests/test_opening_decision_sweep.py`, an active test. That test
passes today only because it reads the skill's flattened normative surface (`SKILL.md` plus every
file under `references/`, per its own `read_all_flat` helper and its docstring's note that the rule
"was never in the cut rule's body anyway; it always lived in the on-demand reference module the
rule pointed to") — it does not require the `SKILL.md` body itself to name the module. A session
that reads only the body, which is the reading path the file's own progressive-disclosure design
sets up ("Open that module when..." sentences beside every other reference), has no way to learn
`session-handover.md` exists or when its question arises. The rewritten frontmatter description now
states plainly that this module is one of six "opened only when its own kind of question needs
resolving" — the description promises a trigger the body does not supply. Checked history: as of
the 2026-08-25 review (`docs/skill-review/2026-08-25-batch-2b-slice-3-and-a5.md`), a body sentence
under the numbered rule 35 did point to this file; that pointer went with rule 35 itself when the
2026-08-26 cut moved the rule to `attic/live-spec-base-unbacked-rules-2026-08-26.md` and no
replacement pointer was added anywhere in the body. No skill-review record since 2026-08-26
mentions `session-handover.md`, so the gap has stood unexamined for a week and survives unchanged
through today's landing.

**F2 — `references/worked-examples.md`'s rule-24 section lost its only pointer in this
compression, and a different worked example for the same rule now lives in `rule-origins.md`
instead.** Before this landing, the body's rule 24 carried both an inline "three footprints"
example (presentation-only / single-module / cross-cutting) and an explicit line, "See
references/worked-examples.md for the per-kind illustration of both" — pointing at that file's own
"Rule 24 — the per-kind layers and proofs" section, which illustrates the same rule with a
different example (a codebase's frontend/backend/store split, a photo site's content/rendering
engine/deployment split, a promotion campaign's message/channels/assets split, and three matching
proof examples). The compression moved the inline "three footprints" text into `rule-origins.md`'s
new rule-24 entry, and dropped rule 24's line pointing at `worked-examples.md` — but left that
file's "Rule 24" section in place, untouched and now unreachable: nothing in the current body or in
`rule-origins.md` names it. The result is two separate worked examples for one rule split across
two reference files, only one of which (`rule-origins.md`, reached through the body's single
blanket sentence covering all twenty-two rules) is still reachable — the shape rule 4 ("one
canonical home per fact") and SPEC INV-13 forbid for an instruction, here landed on an example
instead of an instruction proper. `worked-examples.md` carries four further sections explicitly
marked "(its rule number retired to attic 2026-08-26)" — the routing rule, the release-tier 2.0.0
boundary case, the no-self-certification rule, and the session-handover rule's worked failure —
each already unreachable from any live rule before this landing, for the same reason as F1. Of the
file's six sections, one ("The rule of thinking") is pointed at from the body today.

**F3 — rule 4 carries a verbatim self-duplicate, introduced by this compression.** The rule reads:
"**One canonical home per fact.** One canonical home per fact; repoint every reference the same
session a doc moves or is superseded." The bold lead-in and the sentence that follows it open with
the identical six words. The pre-compression body did not repeat itself here — rule 4's lead-in was
followed by different text ("Everything else that mentions the fact is a pointer, and pointers are
kept live..."). No other rule in the body repeats its own bold lead-in verbatim; this is the one
instance, and it lands on the rule that itself names one-fact-one-home as the law.

## Checked clean

- The frontmatter `description`'s counts match the body as it stands: "twelve working skills"
  (title and intro) and the description's own list both name exactly twelve, and the closing
  roster's two additional entries (`product-prover-pack`, `text-audit-pack`) are named there as
  bindings to external skills, not as a thirteenth and fourteenth working skill — no contradiction
  of the kind the 2026-07-23 review's B1 found (title vs. footer skill-count mismatch). "Twenty-two
  rules in the body" is accurate: rules 1–10, 12, 13, 16, 17, 22, 24–27, 29, 31, 36 are the
  twenty-two live numbers, matching the retirement list's own arithmetic (36 minus the fourteen
  retired numbers).
- All twenty-two rules are actionable from the body alone. Each carries its instruction, its SPEC
  anchor(s), and the check or script that reads it in the same numbered item; none requires opening
  `rule-origins.md` to know what to do. `rule-origins.md` itself holds only citation, history,
  justification, and worked example, exactly as its own opening paragraph promises ("never a rule
  restated in words of its own") — read in full, no entry restates an instruction the body doesn't
  already carry standalone.
- `glossary.md`, `settings-ladder.md`, and `worker-restore.md` each still have a reason to be
  separate and each is pointed at from the body at the place a session would need it: glossary
  before any term or code needs resolving (two pointers), settings-ladder before any setting is
  resolved, proposed, or recorded (one pointer), worker-restore from rule 7's own sub-bullet (one
  pointer).
