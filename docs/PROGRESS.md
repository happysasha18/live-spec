# Progress — the two promises

Generated 2026-08-19 by `python3 scripts/progress-report.py`, reading the tree as it stands today.

## Where the two promises stand

Promise one, a reader gets through a document without stopping, measures 4,213 open writing findings across the live set today.

Promise two, the specification stops growing, measures PRODUCT_SPEC.md at 49,381 bytes today.

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
| 5 | `skills/text-audit/SKILL.md` | not measured | not measured | no | waiting |
| 6 | `docs/language-rules.md` | 33 | no | no | waiting |
| 7 | `docs/spec-style.md` | 65 | no | no | waiting |
| 8 | `docs/spec-format.md` | 13 | no | no | waiting |
| 9 | `docs/language-worked-example.md` | 8 | no | no | waiting |

### 5. The three skills loaded in every task run by the method

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 10 | `skills/live-spec-base/SKILL.md` | 20 | no | no | waiting |
| 11 | `skills/build-pipeline/SKILL.md` | 37 | no | no | waiting |
| 12 | `skills/communicator/SKILL.md` | 17 | no | no | waiting |

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
| 19 | `skills/spec-author/SKILL.md` | 46 | no | no | waiting |
| 20 | `skills/test-author/SKILL.md` | 54 | no | no | waiting |

### 8. The specification family

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 21 | `PRODUCT_SPEC.md` | 130 | no | no | waiting |
| 22 | `ARCHITECTURE.md` | 0 | yes | no | waiting |
| 23 | `TEST_MATRIX.md` | 76 | no | no | waiting |

### 9. The documents a stranger meets on arrival

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 24 | `README.md` | 4 | no | no | waiting |
| 25 | `OVERVIEW.md` | 8 | no | no | waiting |
| 26 | `adopt/ADOPT.md` | 46 | no | no | waiting |

### 10. Every remaining live document, worst first

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 27 | `spec/design-spec-review.md` | 233 | no | no | waiting |
| 28 | `spec/guardrails-freshness.md` | 209 | no | no | waiting |
| 29 | `spec/queue-intake-priority.md` | 185 | no | no | waiting |
| 30 | `spec/doc-order-generated.md` | 178 | no | no | waiting |
| 31 | `spec/roles-and-agents.md` | 145 | no | no | waiting |
| 32 | `docs/prior-art-frameworks.md` | 112 | no | no | waiting |
| 33 | `spec/live-status-reporting.md` | 105 | no | no | waiting |
| 34 | `docs/language-rule-coverage.md` | 98 | no | no | waiting |
| 35 | `spec/push-gate-milestone-audit.md` | 84 | no | no | waiting |
| 36 | `docs/restyle-repoint-log.md` | 83 | no | no | waiting |
| 37 | `spec/parallel-lanes.md` | 82 | no | no | waiting |
| 38 | `spec/project-setup-tuning.md` | 82 | no | no | waiting |
| 39 | `docs/prior-art-longtail.md` | 78 | no | no | waiting |
| 40 | `spec/test-honesty.md` | 74 | no | no | waiting |
| 41 | `MIGRATION.md` | 62 | no | no | waiting |
| 42 | `docs/plans/2026-08-07-recovery-plan.md` | 61 | no | no | waiting |
| 43 | `skills/build-pipeline/references/delegation-protocol.md` | 53 | no | no | waiting |
| 44 | `spec/owner-questions-drafts.md` | 49 | no | no | waiting |
| 45 | `guardrails/README.md` | 48 | no | no | waiting |
| 46 | `docs/wishes/2026-07-09-project-onboarding-what-can-i-customize.md` | 41 | no | no | waiting |
| 47 | `spec/customer-feedback.md` | 40 | no | no | waiting |
| 48 | `docs/lenses.md` | 39 | no | no | waiting |
| 49 | `docs/decisions/2026-07-07-morning-round3.md` | 38 | no | no | waiting |
| 50 | `hooks/conduct-law.md` | 38 | no | no | waiting |
| 51 | `docs/language-defects.md` | 37 | no | no | waiting |
| 52 | `docs/spec-compaction-protocol.md` | 36 | no | no | waiting |
| 53 | `spec/work-board.md` | 36 | no | no | waiting |
| 54 | `docs/roadmap-format.md` | 33 | no | no | waiting |
| 55 | `docs/test-matrix-format.md` | 33 | no | no | waiting |
| 56 | `docs/prose-quality-gate-design.md` | 32 | no | no | waiting |
| 57 | `spec/internal-failure-log.md` | 32 | no | no | waiting |
| 58 | `spec/public-text-rules.md` | 32 | no | no | waiting |
| 59 | `docs/decisions/2026-07-06-overnight-decisions.md` | 31 | no | no | waiting |
| 60 | `inbox/README.md` | 31 | no | no | waiting |
| 61 | `spec/settings-layers.md` | 26 | no | no | waiting |
| 62 | `skills/spec-author/references/facet-sweep.md` | 25 | no | no | waiting |
| 63 | `docs/audits/2026-08-07-number-census.md` | 22 | no | no | waiting |
| 64 | `skills/communicator/references/field-examples.md` | 21 | no | no | waiting |
| 65 | `docs/wishes/2026-07-09-test-method-lessons-tlvphoto-week.md` | 19 | no | no | waiting |
| 66 | `skills/build-pipeline/references/lanes-and-pen.md` | 19 | no | no | waiting |
| 67 | `docs/wishes/2026-07-09-prover-unwritten-seams.md` | 18 | no | no | waiting |
| 68 | `docs/wishes/2026-07-10-from-tlvphoto-red-first-slips-on-small-voiced-fixes.md` | 18 | no | no | waiting |
| 69 | `docs/worker-liveness.md` | 17 | no | no | waiting |
| 70 | `skills/spec-author/references/how-it-reads.md` | 17 | no | no | waiting |
| 71 | `spec/bug-priority-queue.md` | 17 | no | no | waiting |
| 72 | `templates/agent.template.md` | 17 | no | no | waiting |
| 73 | `docs/architecture-format.md` | 16 | no | no | waiting |
| 74 | `docs/migration-sample/2026-07-20-backdescribe-sample.md` | 16 | no | no | waiting |
| 75 | `skills/design-reviewer/README.md` | 16 | no | no | waiting |
| 76 | `docs/test-method.md` | 15 | no | no | waiting |
| 77 | `docs/wishes/2026-07-09-architecture-runtime-placement-views.md` | 14 | no | no | waiting |
| 78 | `scripts/judge-rubric.md` | 13 | no | no | waiting |
| 79 | `skills/build-pipeline/references/verify-step-detail.md` | 13 | no | no | waiting |
| 80 | `skills/build-pipeline/references/work-kind-table.md` | 13 | no | no | waiting |
| 81 | `docs/architecture-method.md` | 12 | no | no | waiting |
| 82 | `skills/build-pipeline/references/footprint-read.md` | 12 | no | no | waiting |
| 83 | `spec/agent-request.md` | 12 | no | no | waiting |
| 84 | `spec/engine-instance-pair.md` | 12 | no | no | waiting |
| 85 | `skills/build-pipeline/references/architecture-step-detail.md` | 11 | no | no | waiting |
| 86 | `skills/build-pipeline/references/guardrails-catalog.md` | 11 | no | no | waiting |
| 87 | `skills/communicator/references/page-lifecycle.md` | 11 | no | no | waiting |
| 88 | `skills/spec-author/README.md` | 11 | no | no | waiting |
| 89 | `spec/public-contract.md` | 11 | no | no | waiting |
| 90 | `spec/settings-card.md` | 11 | no | no | waiting |
| 91 | `docs/plans/2026-07-28-top-level-readability.md` | 10 | no | no | waiting |
| 92 | `skills/build-pipeline/README.md` | 10 | no | no | waiting |
| 93 | `spec/agent-identity.md` | 10 | no | no | waiting |
| 94 | `spec/pack-upgrade.md` | 10 | no | no | waiting |
| 95 | `docs/onboarding-and-settings.md` | 9 | no | no | waiting |
| 96 | `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md` | 9 | no | no | waiting |
| 97 | `skills/spec-author/references/primary-unit.md` | 9 | no | no | waiting |
| 98 | `spec/adopt-existing-project.md` | 9 | no | no | waiting |
| 99 | `spec/product-map.md` | 9 | no | no | waiting |
| 100 | `docs/pipeline.md` | 8 | no | no | waiting |
| 101 | `docs/spec-format-by-project-type.md` | 8 | no | no | waiting |
| 102 | `inbox/2026-08-08-verdict-lands-same-minute.md` | 8 | no | no | waiting |
| 103 | `skills/communicator/references/writing-register.md` | 8 | no | no | waiting |
| 104 | `skills/spec-author/references/the-spine.md` | 8 | no | no | waiting |
| 105 | `skills/test-author/README.md` | 8 | no | no | waiting |
| 106 | `docs/pair-adoption.md` | 7 | no | no | waiting |
| 107 | `inbox/2026-08-12-tlvphotos-reply-worker-restore-finding.md` | 7 | no | no | waiting |
| 108 | `scripts/read-grant-ask.md` | 7 | no | no | waiting |
| 109 | `skills/build-pipeline/references/drafter-applier-example.md` | 7 | no | no | waiting |
| 110 | `skills/communicator/references/rule-histories.md` | 7 | no | no | waiting |
| 111 | `skills/product-prover-pack/SKILL.md` | 7 | no | no | waiting |
| 112 | `spec/agent-birth.md` | 7 | no | no | waiting |
| 113 | `docs/push-law.md` | 6 | no | no | waiting |
| 114 | `skills/feedback-intake/README.md` | 6 | no | no | waiting |
| 115 | `skills/publish/README.md` | 6 | no | no | waiting |
| 116 | `skills/text-audit-pack/SKILL.md` | 6 | no | no | waiting |
| 117 | `docs/adoption.md` | 5 | no | no | waiting |
| 118 | `docs/norms/work-board.provenance.md` | 5 | no | no | waiting |
| 119 | `skills/spec-author/references/composition-sweep.md` | 5 | no | no | waiting |
| 120 | `spec/draft-sandbox.md` | 5 | no | no | waiting |
| 121 | `templates/DECISIONS.template.md` | 5 | no | no | waiting |
| 122 | `templates/JOURNAL.template.md` | 5 | no | no | waiting |
| 123 | `templates/NEXT_STEPS.template.md` | 5 | no | no | waiting |
| 124 | `templates/PROBLEMS.template.md` | 5 | no | no | waiting |
| 125 | `docs/matrix-notes/guardrails.md` | 4 | no | no | waiting |
| 126 | `skills/build-pipeline/references/minor-bump-gate.md` | 4 | no | no | waiting |
| 127 | `skills/communicator/references/words.md` | 4 | no | no | waiting |
| 128 | `spec/external-publish.md` | 4 | no | no | waiting |
| 129 | `templates/KILL_LIST.template.md` | 4 | no | no | waiting |
| 130 | `templates/profile.template.md` | 4 | no | no | waiting |
| 131 | `work/ladder-measurement.md` | 4 | no | no | waiting |
| 132 | `SURFACES.md` | 3 | no | no | waiting |
| 133 | `docs/MEASUREMENTS.md` | 3 | no | no | waiting |
| 134 | `docs/audits/2026-08-07-cost-map.md` | 3 | no | no | waiting |
| 135 | `docs/norms/onboarding-card-2026-07-10.provenance.md` | 3 | no | no | waiting |
| 136 | `inbox/2026-08-08-profile-briefed-worker-ab-result.md` | 3 | no | no | waiting |
| 137 | `inbox/2026-08-12-preshow-lint-script-missing.md` | 3 | no | no | waiting |
| 138 | `scripts/grant-ask.md` | 3 | no | no | waiting |
| 139 | `skills/build-pipeline/references/request-kind-table.md` | 3 | no | no | waiting |
| 140 | `skills/communicator/README.md` | 3 | no | no | waiting |
| 141 | `skills/feedback-collector/README.md` | 3 | no | no | waiting |
| 142 | `spec/wish-intake.md` | 3 | no | no | waiting |
| 143 | `skills/build-pipeline/references/excuses-table.md` | 2 | no | no | waiting |
| 144 | `skills/build-pipeline/references/mockup-first-entry.md` | 2 | no | no | waiting |
| 145 | `skills/live-spec-base/references/settings-ladder.md` | 2 | no | no | waiting |
| 146 | `skills/spec-author/references/anti-patterns.md` | 2 | no | no | waiting |
| 147 | `skills/spec-author/references/change-record.md` | 2 | no | no | waiting |
| 148 | `spec/fresh-start.md` | 2 | no | no | waiting |
| 149 | `templates/skill-review.template.md` | 2 | no | no | waiting |
| 150 | `docs/plans/2026-07-29-specification-subdivision.md` | 1 | no | no | waiting |
| 151 | `docs/prior-art.md` | 1 | no | no | waiting |
| 152 | `skills/live-spec-base/README.md` | 1 | no | no | waiting |
| 153 | `skills/spec-author/references/completeness-pass.md` | 1 | no | no | waiting |
| 154 | `skills/spec-author/references/glossary.md` | 1 | no | no | waiting |
| 155 | `templates/ARCHITECTURE.template.md` | 1 | no | no | waiting |
| 156 | `PRODUCT_SPEC.index.md` | 0 | yes | no | waiting |
| 157 | `adopt/START.md` | 0 | yes | no | waiting |
| 158 | `docs/PROGRESS.md` | 0 | yes | no | waiting |
| 159 | `docs/audits/2026-08-07-number-rulings.md` | 0 | yes | no | waiting |
| 160 | `docs/plans/2026-07-28-two-goals-one-campaign.md` | 0 | yes | no | waiting |
| 161 | `docs/plans/2026-08-07-night-plan.md` | 0 | yes | no | waiting |
| 162 | `skills/build-pipeline/references/project-setup.md` | 0 | yes | no | waiting |
| 163 | `skills/live-spec-base/references/glossary.md` | 0 | yes | no | waiting |
| 164 | `skills/live-spec-base/references/worked-examples.md` | 0 | yes | no | waiting |
| 165 | `templates/PRODUCT_SPEC.template.md` | 0 | yes | no | waiting |
| 166 | `templates/ROADMAP.template.md` | 0 | yes | no | waiting |
| 167 | `templates/TEST_MATRIX.template.md` | 0 | yes | no | waiting |
| 168 | `work/2026-08-15-branch-table.md` | 0 | yes | no | waiting |
| 169 | `work/2026-08-15-unowned-numbers.md` | 0 | yes | no | waiting |

## Promise one — a reader gets through a document without stopping

The counts below come from the record `guardrails/rule-census.json`. It states when each document was last measured.

| measure | today | recorded before | target |
|---|---|---|---|
| live documents measured | 164 | 108 | all of them |
| writing findings across all documents | 4,213 | 4,810 | 0 |
| documents at zero findings | 17 | 16 | all |
| documents that passed two consecutive readings with nothing blocking | 0 | not stated | all |

The fifteen documents carrying the most findings:

| document | findings | of which long sentences | style | longest sentence | readings run | passed |
|---|---|---|---|---|---|---|
| `spec/design-spec-review.md` | 233 | 233 | 0 | 69 | 0 | no |
| `ROADMAP.md` | 215 | 8 | 207 | 242 | 0 | no |
| `spec/guardrails-freshness.md` | 209 | 209 | 0 | 78 | 0 | no |
| `spec/queue-intake-priority.md` | 185 | 185 | 0 | 60 | 0 | no |
| `spec/doc-order-generated.md` | 178 | 178 | 0 | 53 | 0 | no |
| `spec/roles-and-agents.md` | 145 | 145 | 0 | 76 | 0 | no |
| `PRODUCT_SPEC.md` | 130 | 130 | 0 | 103 | 1 | no |
| `docs/prior-art-frameworks.md` | 112 | 7 | 105 | 42 | 0 | no |
| `spec/live-status-reporting.md` | 105 | 105 | 0 | 63 | 0 | no |
| `docs/language-rule-coverage.md` | 98 | 76 | 22 | 64 | 0 | no |
| `spec/push-gate-milestone-audit.md` | 84 | 84 | 0 | 52 | 0 | no |
| `docs/restyle-repoint-log.md` | 83 | 20 | 63 | 78 | 0 | no |
| `spec/parallel-lanes.md` | 82 | 82 | 0 | 69 | 0 | no |
| `spec/project-setup-tuning.md` | 82 | 82 | 0 | 56 | 0 | no |
| `docs/prior-art-longtail.md` | 78 | 15 | 63 | 53 | 0 | no |

## Promise two — the specification stops growing

| measure | today | at the format change, 2026-07-23 | ceiling | target |
|---|---|---|---|---|
| bytes | 49,381 | 590,695 | not stated | under the ceiling |
| lines | 307 | not stated | not stated | set by the subdivision plan |
| words | 8,258 | not stated | not stated | set by the subdivision plan |
| requirements | 0 | 282 | not stated | set by the subdivision plan |
| acceptance criteria | 0 | 1,372 | not stated | set by the subdivision plan |
| bytes per criterion | not stated | not stated | 185.6 | falls or holds |
| pairs stating one fact twice | 0 | 116 | 119 | falls or holds |

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
