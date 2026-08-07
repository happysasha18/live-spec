# Every numeric standard in the tree, and the ruling on each

On 2026-08-07 at 09:16 you asked to find the numbers the process invented and root them out (row 576).
A read-only sweep of the tree found 144 numeric standards. Your answer at about 01:10 set the rule for
the whole class. A standard is yours, or it is derived and justified, or it is absent. Each of the 144
was placed in one of the eight groups below. The per-number mapping table is the task's next
artifact; the census page holds every number's home meanwhile.

Strike anything here that does not match what you said.

## 1. Yours

Two numbers stand on your word alone.

- A text ships after two consecutive clean cold reads. Your word, 2026-08-05. Homes:
  `guardrails/language-rules.json`, `scripts/measurements-table.py`, `docs/language-rules.md`.
- At most three build lanes run in parallel without asking. Your word, 2026-07-06. Homes:
  `scripts/open-lane.sh`, `PRODUCT_SPEC.md`, `skills/build-pipeline/SKILL.md`, `docs/roadmap-format.md`.

## 2. Derived, kept

Each of these is a measurement. The derivation is written where the number lives.

- The measured-baseline ratchets that may only fall. The readability defect baselines sit in
  `guardrails/criterion-readability.json` and `guardrails/language-rules.json`.
- The specification's bytes-per-criterion bound, in `guardrails/spec-ratchet.json`.
- The debt caps that stand at zero waivers, in `scripts/spec-debt-cap.json` and
  `scripts/spec-done-gate.py`.
- The suite's wall-time bound in `ARCHITECTURE.md`, re-measured at every landing.
  `guardrails/check-suite-budget.sh` reads it against the fresh run.
- The byte ceilings for the four large documents, in `guardrails/doc-bounds.json`. They trigger
  rotation of closed material. Content is never cut. Each is seeded as measured size plus headroom,
  with the reason recorded in the file.
- The node-per-file caps in `guardrails/node-file-cap.json`, seeded from the tree's measured state.

These embody the same logic as your no-redundancy standard. The number is measured, and the only
allowed motion is improvement.

One tension in this group is yours to judge. The census's own closing calls the four byte
ceilings and the bytes-per-criterion bound kin of the size-cap class you struck. The ruling
keeps them because each is seeded from measurement, moves only by rotation or downward, and
writes its reason in its file. The headroom convention inside the ceilings (roughly a hundred
kilobytes) has no stated ground of its own. Strike the ruling if the distinction does not
convince you.

## 3. Machinery tuning, kept and marked

Timeouts on subprocesses and network calls, scan windows, truncation bounds, retry caps, staleness
windows, and detector thresholds. Representative homes: `scripts/gen-tree-counts.py`,
`scripts/check-pack-update.sh`, `scripts/sweep-rendered.py`, `hooks/register_judge_core.py`,
`hooks/conduct-judge-collect.sh`, `templates/headless_harness.py`,
`guardrails/check-runaway-child.py`, `guardrails/reap_owned_group.py`.

These judge no work. They bound tools. They stay retunable defaults. Any that lacks its retunable
mark gets one.

## 4. Design constants, kept where the reason is written

For these rules the number is the design itself.

- A problem's second occurrence earns an owner. Homes:
  `skills/build-pipeline/references/minor-bump-gate.md`, `skills/live-spec-base/SKILL.md`,
  `PRODUCT_SPEC.md`.
- A question crosses between the same two agents at most twice before it reaches you. Home:
  `PRODUCT_SPEC.md`.
- A behavioral rule that breaks twice mid-turn earns a live channel. Home: `PRODUCT_SPEC.md`.
- A confirmed bug's class hunt has four moves. Home: `skills/build-pipeline/SKILL.md`.

Each stands with its reason beside it. One lacking a written reason gets the reason written.

## 5. Rooted out

Your answer at about 01:10 already struck this size-cap family.

- The 500-byte cap on one new specification criterion. Homes:
  `guardrails/check-delta-record.py`, `skills/spec-author/SKILL.md`, `PRODUCT_SPEC.md`,
  `tests/test_delta_classifier.py`.
- The 250-line target for a subdivided specification part. Homes:
  `scripts/measurements-table.py`, `docs/MEASUREMENTS.md`.
- The 100-line cap on the resume digest. Homes: `tests/test_resume_digest.py`,
  `templates/NEXT_STEPS.template.md`, `docs/worker-liveness.md`, `PRODUCT_SPEC.md`. Its qualitative
  law takes over: one live-state block, and no redundancy.

Removal is landing today as its own batch.

## 6. Rides the rulebook cut

The micro-numbers inside the rulebook files. These are the scan-in-30-seconds targets, the
sentence-count caps for report sections, and the question-count checklists. Homes:
`skills/product-prover/SKILL.md`, `skills/build-pipeline/SKILL.md`, `skills/spec-author/SKILL.md`,
`skills/communicator/SKILL.md`, `skills/test-author/SKILL.md`, `skills/text-audit/SKILL.md`.

Each rewrite under the rulebook cut replaces them with the qualitative form. The two files
already rewritten tonight still carry some of these numbers — the reviewer's scan-time targets
among them, none pinned by a test. They go in the same task's next pass.

## 7. External derivations, citation written in

- The sentence-length caps of 25 and 35 words follow plain-language readability practice. Homes:
  `guardrails/language-rules.json`, `guardrails/criterion-readability.json`,
  `docs/language-rules.md`, `skills/text-audit/SKILL.md`.
- The contrast and font-size floors follow the public accessibility standard (`WCAG AA`). Homes:
  `scripts/preshow-legibility-lint.py`, `PRODUCT_SPEC.md`.
- The roughly 500-line skill-file ideal follows the published skill-authoring guidance. Home:
  `tests/test_communicator_body_thinned.py`.

Each citation is being written where the number lives.

## 8. Two plain bugs, fixed today

- One test asserts an older floor of 17 while the live record holds 23. Homes:
  `tests/test_convergence_locks.py`, `scripts/register-lint-floor.json`.
- Another asserts an older redundancy ceiling of 121 while the live record holds 119. Homes:
  `tests/test_convergence_locks.py`, `scripts/spec-debt-cap.json`.

Both tests now read the live record itself, so the copied number cannot go stale again.

## The full table

Every one of the 144 standards, with each home and its provenance lead, is at
`docs/audits/2026-08-07-number-census.md`.
