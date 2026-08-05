# Skill review — live-spec-base (a budget moves the pace, and never the standard)

`SKILL-REVIEW`

Skill: live-spec-base
Date: 2026-08-05
Reviewer: the authoring worker session that made the change. It is not a clean-context review, and
base rule 33 owes one before the release that carries this change.

Verdict: landed with the checks below green. One finding stands open for the seat — the law is
stated as a settings-ladder subsection rather than as numbered rule 36, and the reason is recorded
under "Where the rule went" so the seat can take the numbered form later as its own row.

## What changed

The owner's word, 2026-08-05 ~23:00: on the smallest plan the quality never suffers. We cannot
afford bad work. Slower is allowed, cheaper is allowed, worse is never allowed. He asked that this
live in the skill, and that a fresh clean-context agent be raised whenever the method needs one.

`skills/live-spec-base/SKILL.md` gained a subsection under "The settings ladder", after the
package-defaults table and its two trailing paragraphs:

> ### A budget moves the pace, and never the standard
>
> A rung of the economy ladder sets how fast and how cheaply the work runs. The standard the work is
> held to stands outside every rung. A check the method calls for runs at whatever the plan costs. A
> fresh clean-context agent is raised every time the method asks for one. Four such asks are an
> adversarial review, a cold reading, a release re-prove, and a deep spec-and-architecture audit.
> Economy is bought from pace, from batching, and from a cheaper tier on mechanical work. It is
> bought from no check. The full never-bend list this rule joins lives in the economy-ladder section
> of `PRODUCT_SPEC.md` (SPEC INV-40, R220). The owner's word, 2026-08-05 ~23:00: on the smallest
> plan the work may run slower and may cost less, and its quality never drops.

The `budget.pressure` row of the same table now ends its Default cell with a pointer at that
subsection: "a rung moves the pace and never the standard, stated under this table".

`PRODUCT_SPEC.md` carries the canonical never-bend list at Requirement 220, so the fact's one home
(base rule 4) is there. Its Context gained two sentences, and a fourth case joined its acceptance
criteria:

- **Case: a rung moves the pace alone**
- R220.6 — hold at every rung the standard the work is held to, moving the project's pace alone.
- R220.7 — run a check the method calls for at whatever the plan costs.
- R220.8 — raise a fresh clean-context agent for an adversarial review, a cold reading, a release
  re-prove, and a deep spec-and-architecture audit.
- R220.9 — buy economy from pace, from batching, and from a cheaper tier on mechanical work, and
  buy it from no check.

The criteria ride the codes the ladder already owns — INV-40 the never-bend list, T-19 the ladder,
INV-46 the fresh-context checker, INV-69 the tier routing. No new invariant number was minted,
because a new code needs an owning architecture node and a matrix row, and both files sat outside
this worker's write-set.

## Where the rule went, and why not rule 36

The brief left the placement to this session, offering a new shared rule 36, the `budget.pressure`
row, or both. The settings-ladder subsection was taken for two reasons.

The law governs one named setting, and that setting's home is the settings ladder. A reader who
meets `budget.pressure` meets its reach in the same section, with no jump.

The numbered form would have cost a sweep this worker's write-set could not reach. The skill's
frontmatter claims "thirty-five rules in the body", and that claim is asserted as a literal string by
`tests/test_clean_context_review.py` and `tests/test_resume_rederive.py`, restated in `README.md`,
`skills/build-pipeline/SKILL.md`, `skills/communicator/SKILL.md`, and
`skills/communicator/references/words.md`. Landing rule 36 means moving all six plus the two tests in
one change (base rule 14 sweeps the class). That is a lane of its own, and half of it would have been
a red suite. The subsection states the same law today with no stale count anywhere.

## Derived files this change carried

Two generated artifacts were rebuilt because the spec body moved, and both are output of
`PRODUCT_SPEC.md` rather than authored files:

- `PRODUCT_SPEC.index.md` and the `## Reference` table inside `PRODUCT_SPEC.md` — rebuilt with
  `python3 scripts/build-index.py`, four rows changed (INV-40, INV-46, INV-69, T-19).
- `docs/PROGRESS.md` — rewritten by `guardrails/check-doc-findings-bound.py` when it ran, recording
  the spec's new byte count and criterion count.

## Checks

- `python3 scripts/rule-census.py skills/live-spec-base/SKILL.md PRODUCT_SPEC.md` — SKILL.md 92
  findings (record 92), PRODUCT_SPEC.md 1830 (record 1830).
- `python3 guardrails/check-doc-findings-bound.py` — OK, 110 live documents, none above its record.
- `python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md` — OK.
- `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK, 388 of
  388 rows matched.
- `check-requirement-shape`, `check-criterion-readability`, `check-vocabulary`, `check-weak-words`,
  `check-no-history`, `check-one-name` on `PRODUCT_SPEC.md` — all OK.
- `python3 -m pytest -q tests` — the suite log is named in the delivery report.
- `python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md
  --compaction` — output in the delivery report.

One check caught a real defect while it ran. The first draft anchored the owner's word inside the
spec's Context with its date, and `check-no-history.py` red it: the spec states today's behaviour,
and a date belongs in the journal or the skill (INV-253). The attribution now sits in the skill's
subsection, which is where the pack's other owner-anchored rules keep theirs.
