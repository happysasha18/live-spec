# Skill review — live-spec-base, rule 13's instruction-authority arm

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-31
Reviewer: skill-creator quality lens, run in a clean context over the committed diff (Anthropic's
skill-creator writing guide — Progressive Disclosure, Anatomy of a Skill, frontmatter accuracy —
plus this pack's own register bars in `skills/communicator/references/writing-register.md`)

Verdict: PASS after one blocking correction, applied before this record was written.

## What changed

`skills/live-spec-base/SKILL.md`, rule 13 only. Two edits, both for q-497:

1. **A new paragraph, the rule's second half.** Rule 13 already said where a recorded decision's
   authority comes from. It said nothing about an instruction the seat is acting under, which is what
   the row's founding incident was. The paragraph names the sources a session's instructions arrive
   from — the person's messages and standing profile, the tooling's defaults, a wrapper's injected
   lines, a project file — states that only the first two carry the person's authority, and states how
   a conflict is spoken: the reply names both lines and the person's standing word decides.
2. **One clause updated** where rule 13 describes the mechanical check, since
   `guardrails/check-authority-anchor.py` gained a tree-wide arm in the same range.

## The blocking finding, and the correction

**The dated incident sentence contradicted its source.** The first draft read "a window read another
window's claim of a direct instruction against launching workers". The source
(`docs/queue-archive/rotated-ROADMAP-2026-08-27-merged-into-plan.md:113`, row 497) says the person was
the one reading another window's line, and the window itself had taken a line from its own session
instructions and handed it back as the person's word. `PLAN.md:308` agrees: one window, one false
attribution, no window-to-window hop. As drafted the example described a chat-relay error between two
agents, which is the one case the paragraph's own four sources do not cover — so the example failed to
instantiate the rule standing above it. It also dropped "without his ask", the detail that made the
injected line read as the person's word.

Corrected: the sentence now says the window told the person that a direct instruction in its session
forbade launching workers without their ask, that the line had come from the session's own
instructions, and that the person's standing word was the opposite.

## Non-blocking findings, all applied

- **The gate clause overstated its reach.** It said the check hard-blocks "anywhere else in the tree",
  while the gate spares `docs/`, `attic/`, `inbox/`, `.live-spec/`, `tests/`, `evals/`, `prototype/`,
  `JOURNAL.md`, `MIGRATION.md`, every declared `DECISION-RECORD` surface, and every file that is not a
  tracked `.md` or `.txt`. The clause now says "every other text page the project tracks" and sends the
  reader to the gate's own opening for what it leaves out.
- **"the roster" was ungrounded and collided with an existing use** — the file's other roster is the
  roster of twelve skills at line 12. The clause now names the file, `guardrails/authority-anchor.json`.
- **A short wrapped line mid-paragraph** was rewrapped.

## Checks that passed

- **Rule count.** `grep -cE '^[0-9]+\. \*\*' skills/live-spec-base/SKILL.md` returns 22, matching the
  frontmatter's "twenty-two rules in the body". The edit adds no rule number.
- **One home, proven two ways.** No statement about instruction sources, a tooling-injected line, or a
  conflict with the person's standing word stands anywhere else in the surfaces that tell a session how
  to work (`skills/`, `scripts/`, `guardrails/`, `hooks/`, `templates/`, `adopt/`, `scaffold/`,
  `evals/`, `README.md`, `OVERVIEW.md`, `CLAUDE.md`, `.live-spec/agent.md`).
  `python3 tests/test_one_home_per_rule.py` exits 0 with `instruction-authority` as its fourth rule,
  and reds on a planted second copy. The pointer at the home already stood at
  `skills/communicator/SKILL.md:352`.
- **Placement.** Rule 13 is the right rule: it already holds the attribution half of the same law. The
  body is the right level — the law is short and every seat needs it every turn, so a reference module
  would hide it. A dated incident in a rule's own text is this file's house style (lines 83, 180, 243).
- **Register.** No contrast frame, no coined name, no empty intensifier, no personification outside the
  glossary's own `seat`.

## Carried forward, not this change's

The frontmatter's line 3 claims "three on-demand reference modules under `references/`"; the directory
holds five and the body links four. Pre-existing, untouched here, and named so it is not lost.
