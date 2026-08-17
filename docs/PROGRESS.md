# Progress — the two promises

Generated 2026-08-17 by `python3 scripts/progress-report.py`, reading the tree as it stands today.

## Where the two promises stand

Promise one, a reader gets through a document without stopping, measures 4,950 open writing findings across the live set today.

Promise two, the specification stops growing, measures PRODUCT_SPEC.md at 702,954 bytes against its 840,000-byte ceiling today.

## The queue, in the plan's order

The order below comes from `docs/plans/2026-07-28-two-goals-one-campaign.md`, the section "The order of documents".

Three members carry no entry in the findings record: `hooks/chat-law-hook.sh` and two files outside this repository, `~/.claude/CLAUDE.md` and `~/.claude/live-spec/profile.md`. Their findings column reads not measured.

### 1. The text that enters every turn

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 1 | `hooks/chat-law-hook.sh` | not measured | not measured | no | in hand |

### 2. The text that enters every session at its start

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 2 | `~/.claude/CLAUDE.md` | not measured | not measured | no | waiting |
| 3 | `~/.claude/live-spec/profile.md` | not measured | not measured | no | waiting |

### 3. The file every session reads first

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 4 | `NEXT_STEPS.md` | 0 | yes | no | waiting |

### 4. The text-audit skill and the four documents it points at

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 5 | `skills/text-audit/SKILL.md` | 0 | yes | no | waiting |
| 6 | `docs/language-rules.md` | 37 | no | no | waiting |
| 7 | `docs/spec-style.md` | 65 | no | no | waiting |
| 8 | `docs/spec-format.md` | 16 | no | no | waiting |
| 9 | `docs/language-worked-example.md` | 8 | no | no | waiting |

### 5. The three skills loaded in every task run by the method

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 10 | `skills/live-spec-base/SKILL.md` | 68 | no | no | waiting |
| 11 | `skills/build-pipeline/SKILL.md` | 255 | no | no | waiting |
| 12 | `skills/communicator/SKILL.md` | 176 | no | no | waiting |

### 6. ROADMAP.md, read whenever a session picks up work

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 13 | `ROADMAP.md` | 215 | no | no | waiting |

### 7. The remaining seven skills

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 14 | `skills/design-reviewer/SKILL.md` | 0 | yes | no | waiting |
| 15 | `skills/feedback-collector/SKILL.md` | 14 | no | no | waiting |
| 16 | `skills/feedback-intake/SKILL.md` | 23 | no | no | waiting |
| 17 | `skills/product-prover/SKILL.md` | not measured | not measured | no | waiting |
| 18 | `skills/publish/SKILL.md` | 61 | no | no | waiting |
| 19 | `skills/spec-author/SKILL.md` | 112 | no | no | waiting |
| 20 | `skills/test-author/SKILL.md` | 54 | no | no | waiting |

### 8. The specification family

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 21 | `PRODUCT_SPEC.md` | 1,862 | no | no | waiting |
| 22 | `ARCHITECTURE.md` | 0 | yes | no | waiting |
| 23 | `TEST_MATRIX.md` | 76 | no | no | waiting |

### 9. The documents a stranger meets on arrival

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 24 | `README.md` | 13 | no | no | waiting |
| 25 | `OVERVIEW.md` | 8 | no | no | waiting |
| 26 | `adopt/ADOPT.md` | 46 | no | no | waiting |

### 10. Every remaining live document, worst first

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 27 | `editions/product-prover/examples/sample-review-run-2.md` | 186 | no | no | waiting |
| 28 | `editions/product-prover/examples/sample-review-run-1.md` | 157 | no | no | waiting |
| 29 | `docs/prior-art-frameworks.md` | 112 | no | no | waiting |
| 30 | `docs/language-rule-coverage.md` | 99 | no | no | waiting |
| 31 | `docs/restyle-repoint-log.md` | 83 | no | no | waiting |
| 32 | `docs/prior-art-longtail.md` | 78 | no | no | waiting |
| 33 | `MIGRATION.md` | 62 | no | no | waiting |
| 34 | `docs/plans/2026-08-07-recovery-plan.md` | 61 | no | no | waiting |
| 35 | `skills/build-pipeline/references/delegation-protocol.md` | 52 | no | no | waiting |
| 36 | `guardrails/README.md` | 48 | no | no | waiting |
| 37 | `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | 41 | no | no | waiting |
| 38 | `docs/lenses.md` | 39 | no | no | waiting |
| 39 | `docs/decisions/2026-07-07-morning-round3.md` | 38 | no | no | waiting |
| 40 | `hooks/conduct-law.md` | 38 | no | no | waiting |
| 41 | `docs/language-defects.md` | 37 | no | no | waiting |
| 42 | `docs/spec-compaction-protocol.md` | 36 | no | no | waiting |
| 43 | `docs/roadmap-format.md` | 33 | no | no | waiting |
| 44 | `docs/test-matrix-format.md` | 33 | no | no | waiting |
| 45 | `docs/prose-quality-gate-design.md` | 32 | no | no | waiting |
| 46 | `docs/decisions/2026-07-06-overnight-decisions.md` | 31 | no | no | waiting |
| 47 | `inbox/README.md` | 31 | no | no | waiting |
| 48 | `docs/audits/2026-08-07-number-census.md` | 22 | no | no | waiting |
| 49 | `skills/communicator/references/field-examples.md` | 21 | no | no | waiting |
| 50 | `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | 19 | no | no | waiting |
| 51 | `docs/wishes/2026-07-09-prover-unwritten-seams.md` | 18 | no | no | waiting |
| 52 | `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | 18 | no | no | waiting |
| 53 | `docs/worker-liveness.md` | 17 | no | no | waiting |
| 54 | `templates/agent.template.md` | 17 | no | no | waiting |
| 55 | `docs/architecture-format.md` | 16 | no | no | waiting |
| 56 | `docs/migration-sample/2026-07-20-backdescribe-sample.md` | 16 | no | no | waiting |
| 57 | `skills/design-reviewer/README.md` | 16 | no | no | waiting |
| 58 | `docs/test-method.md` | 15 | no | no | waiting |
| 59 | `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | 14 | no | no | waiting |
| 60 | `scripts/judge-rubric.md` | 13 | no | no | waiting |
| 61 | `skills/build-pipeline/references/work-kind-table.md` | 13 | no | no | waiting |
| 62 | `docs/architecture-method.md` | 12 | no | no | waiting |
| 63 | `skills/build-pipeline/references/guardrails-catalog.md` | 11 | no | no | waiting |
| 64 | `skills/communicator/references/page-lifecycle.md` | 11 | no | no | waiting |
| 65 | `skills/spec-author/README.md` | 11 | no | no | waiting |
| 66 | `docs/onboarding-and-settings.md` | 10 | no | no | waiting |
| 67 | `docs/plans/2026-07-28-top-level-readability.md` | 10 | no | no | waiting |
| 68 | `skills/build-pipeline/README.md` | 10 | no | no | waiting |
| 69 | `skills/communicator/references/writing-register.md` | 10 | no | no | waiting |
| 70 | `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | 9 | no | no | waiting |
| 71 | `docs/pipeline.md` | 8 | no | no | waiting |
| 72 | `docs/spec-format-by-project-type.md` | 8 | no | no | waiting |
| 73 | `inbox/2026-08-08-verdict-lands-same-minute.md` | 8 | no | no | waiting |
| 74 | `skills/test-author/README.md` | 8 | no | no | waiting |
| 75 | `docs/pair-adoption.md` | 7 | no | no | waiting |
| 76 | `inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md` | 7 | no | no | waiting |
| 77 | `scripts/read-grant-ask.md` | 7 | no | no | waiting |
| 78 | `skills/build-pipeline/references/drafter-applier-example.md` | 7 | no | no | waiting |
| 79 | `skills/product-prover-pack/SKILL.md` | 7 | no | no | waiting |
| 80 | `docs/adoption.md` | 6 | no | no | waiting |
| 81 | `docs/push-law.md` | 6 | no | no | waiting |
| 82 | `editions/product-prover/examples/sample-spec.md` | 6 | no | no | waiting |
| 83 | `skills/feedback-intake/README.md` | 6 | no | no | waiting |
| 84 | `skills/publish/README.md` | 6 | no | no | waiting |
| 85 | `docs/norms/work-board.provenance.md` | 5 | no | no | waiting |
| 86 | `templates/DECISIONS.template.md` | 5 | no | no | waiting |
| 87 | `templates/JOURNAL.template.md` | 5 | no | no | waiting |
| 88 | `templates/NEXT_STEPS.template.md` | 5 | no | no | waiting |
| 89 | `templates/PROBLEMS.template.md` | 5 | no | no | waiting |
| 90 | `skills/build-pipeline/references/minor-bump-gate.md` | 4 | no | no | waiting |
| 91 | `skills/communicator/references/words.md` | 4 | no | no | waiting |
| 92 | `templates/KILL_LIST.template.md` | 4 | no | no | waiting |
| 93 | `templates/profile.template.md` | 4 | no | no | waiting |
| 94 | `work/ladder-measurement.md` | 4 | no | no | waiting |
| 95 | `SURFACES.md` | 3 | no | no | waiting |
| 96 | `docs/MEASUREMENTS.md` | 3 | no | no | waiting |
| 97 | `docs/audits/2026-08-07-cost-map.md` | 3 | no | no | waiting |
| 98 | `docs/norms/onboarding-card-2026-07-10.provenance.md` | 3 | no | no | waiting |
| 99 | `inbox/2026-08-08-profile-briefed-worker-ab-result.md` | 3 | no | no | waiting |
| 100 | `inbox/2026-08-12-preshow-lint-script-missing.md` | 3 | no | no | waiting |
| 101 | `scripts/grant-ask.md` | 3 | no | no | waiting |
| 102 | `skills/build-pipeline/references/request-kind-table.md` | 3 | no | no | waiting |
| 103 | `skills/communicator/README.md` | 3 | no | no | waiting |
| 104 | `skills/feedback-collector/README.md` | 3 | no | no | waiting |
| 105 | `editions/product-prover/PROVENANCE.md` | 2 | no | no | waiting |
| 106 | `skills/build-pipeline/references/excuses-table.md` | 2 | no | no | waiting |
| 107 | `skills/live-spec-base/references/settings-ladder.md` | 2 | no | no | waiting |
| 108 | `templates/skill-review.template.md` | 2 | no | no | waiting |
| 109 | `docs/plans/2026-07-29-specification-subdivision.md` | 1 | no | no | waiting |
| 110 | `docs/prior-art.md` | 1 | no | no | waiting |
| 111 | `editions/product-prover/SKILL.md` | 1 | no | no | waiting |
| 112 | `skills/live-spec-base/README.md` | 1 | no | no | waiting |
| 113 | `templates/ARCHITECTURE.template.md` | 1 | no | no | waiting |
| 114 | `PRODUCT_SPEC.index.md` | 0 | yes | no | waiting |
| 115 | `adopt/START.md` | 0 | yes | no | waiting |
| 116 | `docs/PROGRESS.md` | 0 | yes | no | waiting |
| 117 | `docs/audits/2026-08-07-number-rulings.md` | 0 | yes | no | waiting |
| 118 | `docs/plans/2026-07-28-two-goals-one-campaign.md` | 0 | yes | no | waiting |
| 119 | `docs/plans/2026-08-07-night-plan.md` | 0 | yes | no | waiting |
| 120 | `editions/product-prover/README.md` | 0 | yes | no | waiting |
| 121 | `editions/product-prover/examples/sample-response.md` | 0 | yes | no | waiting |
| 122 | `editions/product-prover/reference/stress-lenses.md` | 0 | yes | no | waiting |
| 123 | `skills/build-pipeline/references/project-setup.md` | 0 | yes | no | waiting |
| 124 | `skills/text-audit/README.md` | 0 | yes | no | waiting |
| 125 | `skills/text-audit/references/human-prose-rules.md` | 0 | yes | no | waiting |
| 126 | `skills/text-audit/references/reader-prompt.md` | 0 | yes | no | waiting |
| 127 | `skills/text-audit/references/rewrite-meaning-check.md` | 0 | yes | no | waiting |
| 128 | `skills/text-audit/references/unprompted-reader-brief.md` | 0 | yes | no | waiting |
| 129 | `templates/PRODUCT_SPEC.template.md` | 0 | yes | no | waiting |
| 130 | `templates/ROADMAP.template.md` | 0 | yes | no | waiting |
| 131 | `templates/TEST_MATRIX.template.md` | 0 | yes | no | waiting |
| 132 | `work/2026-08-15-branch-table.md` | 0 | yes | no | waiting |
| 133 | `work/2026-08-15-unowned-numbers.md` | 0 | yes | no | waiting |

## Promise one — a reader gets through a document without stopping

The counts below come from the record `guardrails/rule-census.json`. It states when each document was last measured.

| measure | today | recorded before | target |
|---|---|---|---|
| live documents measured | 129 | 108 | all of them |
| writing findings across all documents | 4,950 | 4,810 | 0 |
| documents at zero findings | 24 | 16 | all |
| documents that passed two consecutive readings with nothing blocking | 0 | not stated | all |

The fifteen documents carrying the most findings:

| document | findings | of which long sentences | style | longest sentence | readings run | passed |
|---|---|---|---|---|---|---|
| `PRODUCT_SPEC.md` | 1,862 | 1,862 | 0 | 90 | 0 | no |
| `skills/build-pipeline/SKILL.md` | 255 | 135 | 120 | 198 | 0 | no |
| `ROADMAP.md` | 215 | 8 | 207 | 242 | 0 | no |
| `editions/product-prover/examples/sample-review-run-2.md` | 186 | 140 | 46 | 68 | 0 | no |
| `skills/communicator/SKILL.md` | 176 | 85 | 91 | 97 | 0 | no |
| `editions/product-prover/examples/sample-review-run-1.md` | 157 | 114 | 43 | 63 | 0 | no |
| `docs/prior-art-frameworks.md` | 112 | 7 | 105 | 42 | 0 | no |
| `skills/spec-author/SKILL.md` | 112 | 112 | 0 | 99 | 0 | no |
| `docs/language-rule-coverage.md` | 99 | 77 | 22 | 64 | 0 | no |
| `docs/restyle-repoint-log.md` | 83 | 20 | 63 | 78 | 0 | no |
| `docs/prior-art-longtail.md` | 78 | 15 | 63 | 53 | 0 | no |
| `TEST_MATRIX.md` | 76 | 8 | 68 | 46 | 0 | no |
| `skills/live-spec-base/SKILL.md` | 68 | 54 | 14 | 48 | 0 | no |
| `docs/spec-style.md` | 65 | 32 | 33 | 64 | 0 | no |
| `MIGRATION.md` | 62 | 62 | 0 | 65 | 0 | no |

## Promise two — the specification stops growing

| measure | today | at the format change, 2026-07-23 | ceiling | target |
|---|---|---|---|---|
| bytes | 702,954 | 590,695 | 840,000 | under the ceiling |
| lines | 8,211 | not stated | not stated | set by the subdivision plan |
| words | 117,839 | not stated | not stated | set by the subdivision plan |
| requirements | 310 | 282 | not stated | set by the subdivision plan |
| acceptance criteria | 1,771 | 1,372 | not stated | set by the subdivision plan |
| bytes per criterion | 185.4 | not stated | 207.2 | falls or holds |
| pairs stating one fact twice | 117 | 116 | 119 | falls or holds |
| share of the byte ceiling used | 83.7% | 70.3% | not stated | not stated |

## Readings run so far

| date | document read | reading number | blocking stops left |
|---|---|---|---|
| 2026-07-27 | language defects | 5 | 11 |
| 2026-07-28 | language rules reference | 1 | not stated |
| 2026-07-28 | language rules reference | 2 | not stated |
| 2026-07-28 | language defects | 6 | 8 |
| 2026-07-28 | language defects | 7 | 12 |
| 2026-07-28 | language defects | 8 | 6 |
| 2026-07-28 | language defects | 9 | 5 |
| 2026-07-28 | language defects | 10 | 5 |
| 2026-07-28 | language defects | 11 | 6 |
| 2026-07-28 | language defects | 12 | 5 |
| 2026-07-28 | language defects | 13 | 8 |
| 2026-07-28 | text audit skill | 14 | 6 |
| 2026-07-28 | campaign plan | 15 | 7 |
| 2026-07-28 | chat law hook | 16 | 3 |
| 2026-07-29 | text audit skill | 17 | 15 |
| 2026-07-29 | text audit skill | 18 | 10 |
| 2026-07-29 | text audit skill | 19 | 5 |
| 2026-07-29 | text audit skill | 20 | 8 |
| 2026-07-29 | text audit skill | 21 | 9 |
| 2026-07-29 | text audit skill | 22 | 4 |
| 2026-07-29 | text audit skill | 23 | 7 |
| 2026-07-29 | text audit skill | 24 | 6 |
| 2026-07-29 | text audit skill | 25 | 8 |
| 2026-07-29 | text audit skill | 26 | 5 |
| 2026-07-29 | text audit skill | 27 | 6 |
| 2026-07-29 | text audit skill | 28 | 8 |
| 2026-07-29 | text audit skill | 29 | 3 |
| 2026-08-05 | text audit skill | 30 | 8 |
| 2026-08-05 | text audit skill | 31 | 8 |
| 2026-08-15 | readme | 32 | not stated |

## What no measure covers

The register lint prints no count field for a caught leak. A cold read once found a real finding scored as zero because of that gap.

A near-duplicate pair with disjoint vocabulary needs a language-model judge, spec-judge.py, which this report does not run.

A document at zero recorded findings has not necessarily cleared a cold read. The mechanical census and the reader bar measure two different things.

Table B's readings-run count only finds a reading record when that record states a real repository path near its top. An informal read leaves no trace here.

A document with no entry under docs/language-reads/ carries no reading history in this page, whether or not anyone has read it informally.
