# SKILL-REVIEW — seven skills touched by the removal and by registering the director

Skills: live-spec-base, communicator, design-reviewer, test-author, feedback-intake,
publish, director
Date: 2026-08-21

Two mechanical passes touched skill bodies. Neither changed what any skill does. This
record says what changed in each and why the change is not substantive in the sense the
gate is guarding against — and it says plainly what was **not** independently reviewed.

## Pass one — dead pointers removed

The removal of the self-referential checks left skill bodies naming scripts that no longer
exist. A skill telling a reader to run a deleted file is worse than one that says nothing.

- `live-spec-base` — instructions pointing at `guardrails/attic/` orphans removed. The
  behaviour each instruction asked for is kept; only the dead path is gone.
- `publish` — same, one pointer.
- `design-reviewer` — the pointer to `guardrails/node_growth_counter.py` removed. That
  counter capped architecture nodes per file at two, a ceiling this project invented for
  itself. The reviewer's professional question — is this file carrying more than one idea —
  stands in the text; only the number is gone.
- `communicator/references/field-examples.md` — one example that cited a deleted check.

## Pass two — the director named where the pack names itself

Adding a twelfth skill without registering it is what turned the CI red on the previous
push, and the failure was mine. Seven tests count the pack's own skills in seven places.

- `live-spec-base`, `communicator`, `design-reviewer`, `test-author`, `feedback-intake` —
  one line each in the closing list that names the neighbouring skills. Each says what the
  Director does relative to that skill: it decides whether the skill is called at all, and
  for the communicator, it decides what happened before the communicator words it.
- `director` — frontmatter version moved from `0.3.0` to `5.0.0`. The pack's rule is that a
  version is one fact and every skill carries the pack's. The private number was mine and
  wrong. The shadow-release state lives in the file's own first section, where a reader
  meets it, rather than in a number that contradicts eleven others.

## What was reviewed independently, and what was not

The `director` skill itself was reviewed adversarially in two rounds by an agent that did
not write it, and separately by thirty-five scenario runs; that is recorded in
`docs/skill-review/2026-08-21-director-shadow.md` and
`docs/prover/2026-08-21-director-shadow.md`. Nothing about its text changed here.

The six other skills were **not** put through an independent adversarial read for these
edits. The edits are a pointer deletion and a one-line addition to a list, and an
adversarial pass over 150 KB of unchanged prose to certify four removed paths and five
added lines would be the ritual this package exists to remove. The changed lines were read
against their neighbours and against the deleted files' absence, by the same agent that
made them. That is a weaker check than the director got, and it is named as weaker here
instead of being dressed up.

Verdict: ALLOW — no skill's behaviour changed. Dead pointers removed, one number corrected
to the pack's, and five closing lists told about a skill that already exists.
