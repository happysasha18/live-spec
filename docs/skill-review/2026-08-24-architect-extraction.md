# Skill review — architect

SKILL-REVIEW

Skill: architect

Date: 2026-08-24
Reviewer: skill-creator (Anthropic)

Verdict: ALLOW — two blocking findings from an independent adversarial review, both fixed in this
same push and verified below; one secondary finding (this record's own absence) closed by writing
it; one further stale-count instance in `communicator`'s own README, caught by a second
independent review pass, folded below; a fifth finding (CI-only, caught by the full suite rather
than the fast local gate) adds `architect` to four more working skills' own closing "pack, whole"
rosters, folded below and also serving as the INV-208 review for `communicator`, `design-reviewer`,
`feedback-intake`, and `test-author`.

## What changed

`skills/architect/SKILL.md` is new: the architecture step of `skills/build-pipeline/SKILL.md`
(step 3, `references/architecture-step-detail.md`) extracted into a standalone,
directly-invocable skill, per Row 21 of `docs/director/capability-map.md` — kept in-repo,
mirroring `test-author`, rather than moved to an external repository (that pattern stays
reserved for capabilities proven reusable standalone, like `product-prover` and `text-audit`).
`skills/director/SKILL.md`'s specialist table now points to it directly (`skills/architect`, was
"inside `skills/build-pipeline`, pending this package's own architect-step decision"), and
`docs/director/capability-map.md` records Row 21 as resolved. `skills/build-pipeline/SKILL.md`
itself, its step 3, and `references/architecture-step-detail.md` are untouched — build-pipeline's
own cutover to calling this skill is a separate future slice, not part of this one; no partial
migration.

## Findings

An agent that did not write the file, given the file and the package's own requirements, reviewed
it adversarially rather than to approve it. Two findings blocked; both are fixed in this same
push, verified below.

1. **Blocking — stale skill count.** Adding `skills/architect/` brought the pack to 13 folders
   under `skills/` (12 working skills plus the `live-spec-base` rulebook), but every "how many
   working skills" statement still said eleven: `README.md:3`, `OVERVIEW.md`'s roster heading and
   list, `ARCHITECTURE.md:35`, `skills/live-spec-base/SKILL.md` (frontmatter `description`, lines
   8 and 12, and the closing "pack, whole" roster), and `PRODUCT_SPEC.md`'s glossary definition of
   "working skill." Caught live by the guardrail test `tests/test_skill_count_agrees.py`, which
   read 3 failed / 10 passed before the fix. **Folded**: all six homes updated from eleven to
   twelve, `architect` added to every roster/enumeration in its pipeline-order position (after
   `design-reviewer`, before `build-pipeline`), matching `docs/director/capability-map.md`'s row
   order and `skills/build-pipeline/SKILL.md`'s own step order — architecture is step 3, right
   after the prove/design-review step and before the test-derivation step. Verified: `python3 -m
   pytest tests/test_skill_count_agrees.py -q` — 13 passed, 0 failed.

2. **Blocking — a real mechanic dropped in extraction.** `skills/build-pipeline/SKILL.md:391`
   ties architecture quality budgets to enforcement: "Each budget is asserted by a matrix-row
   acceptance, never a hope in prose." The extracted `skills/architect/SKILL.md`'s Quality
   budgets section named the instrumentation home and the watcher but never said a budget is
   actually enforced by a `TEST_MATRIX.md` row `test-author` derives from it — leaving budgets as
   unenforced prose, the exact failure mode the dropped sentence exists to prevent. **Folded**:
   added an equivalent sentence to the Quality budgets section, adapted to the standalone-skill
   framing ("A budget written here is not yet enforced by writing it here. It becomes real only
   once `test-author` derives a `TEST_MATRIX.md` row from it that asserts the stated number —
   never a hope left standing in this document's prose."), preserving the substance: enforcement
   runs through a matrix-row assertion, never prose alone.

3. **Secondary, not blocking on its own but a hard push-gate fail otherwise — no skill-review
   record.** Per INV-208 (`skills/build-pipeline/SKILL.md:701-705`,
   `guardrails/check-skill-review.sh`), a new or substantively-changed skill needs a committed
   review record here before push. None existed for `skills/architect/SKILL.md`. **Folded**: this
   record.

4. **Blocking — a fifth stale-count home missed by finding 1's fix.** `skills/communicator/
   README.md:10` also stated "the live-spec pack, which ships eleven skills" — a live, current-facing
   doc, not a dated historical record, so it falls in the same class as finding 1's five homes but
   sits outside `tests/test_skill_count_agrees.py`'s `HOMES` list, so nothing red-flagged it
   mechanically. Caught by a second, independent adversarial review pass over the full committed
   diff. **Folded**: `eleven` → `twelve` at that line. This edit substantively changes the
   `communicator` skill (a non-stamp content line), so this record also serves as `communicator`'s
   own INV-208 review: the only change to `skills/communicator/` in this push is this one-word
   factual correction to its own stated skill count, nothing else in the skill's body/instructions
   changed.

5. **Blocking, CI-only — four more closing rosters missed by finding 1's fix.** Finding 1 updated
   `live-spec-base`'s own closing "pack, whole" roster to name `architect`, but the same closing
   block quote is independently carried by each other working skill's own `SKILL.md`
   (`tests/test_traceability.py::TestPackListParity`'s `footer_bodies()` reads every skill whose
   `SKILL.md` carries either roster heading, not just `live-spec-base`'s). `skills/communicator/
   SKILL.md`, `skills/feedback-intake/SKILL.md`, and `skills/test-author/SKILL.md`'s closing
   rosters still omitted `architect` between `design-reviewer` and `build-pipeline`, and
   `skills/design-reviewer/SKILL.md`'s bulleted roster form still omitted the matching bullet in
   the same slot — all four missed because this test lives in `tests/test_traceability.py`'s full
   run, which CI's `pytest -q` covers and the fast local push gate does not (this project's own
   documented rule: the full suite hangs in this local environment). Caught by CI on
   `origin/main`'s `12d82f74`, not by an adversarial read here. **Folded**: the same closing-roster
   line `architect` already carries in `live-spec-base` and in `architect`'s own file, added to
   each of the four skills in the identical pipeline-order slot; `skills/build-pipeline/`
   deliberately left untouched (no partial migration). Verified: `python3 -m pytest
   tests/test_traceability.py -q` — 181 passed, and `tests/test_architect_extraction.py` gained a
   pinned regression test per skill so a later edit that drops the line from just one of them reds
   by name (`python3 -m pytest tests/test_architect_extraction.py -q` — 10 passed). Each of the
   four skills' only change in this push is this one-line factual addition to its own closing
   roster — nothing else in any of their bodies/instructions changed (`git show b31fc42f --stat`:
   4 files changed, 4 insertions(+), 3 deletions(-)) — so this finding also serves as each of
   their own INV-208 review.

Other checks run, none of which found anything to fold: frontmatter (`name`, `description`,
`metadata.version: 5.0.0`) matches sibling skills' shape, and the description states a
standalone-invocable task in its own first sentence ("'Here's a proven spec, produce or update
the architecture' is a complete task on its own — invoke this skill directly, not only as a step
inside a larger pipeline"), matching the convention `skills/director/SKILL.md` states in this
same push for a `skills/…` specialist-table cell. INV numbers cited in the body (INV-36, INV-41,
INV-74, INV-75, INV-113, INV-122) were grepped against `PRODUCT_SPEC.md` and each resolves to the
invariant the skill cites it for. `skills/build-pipeline/` carries no changes in this diff —
confirmed no partial migration. `guardrails/check-skill-loadability.sh skills` passes with
`skills/architect/` present.
