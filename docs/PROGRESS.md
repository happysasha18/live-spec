# Progress — the two promises

Generated 2026-09-02 by `python3 scripts/progress-report.py`, reading the tree as it stands today.

## Where the two promises stand

Promise one, a reader gets through a document without stopping, measures not stated open writing findings across the live set today.

Promise two, the specification stops growing, measures PRODUCT_SPEC.md at 51,094 bytes today.

## The queue, in the plan's order

The order below comes from `docs/plans/2026-07-28-two-goals-one-campaign.md`, the section "The order of documents".

Every member's findings column reads not measured: the per-file census (`guardrails/rule-census.json`, written by `scripts/rule-census.py`) that used to fill it was retired 2026-08-21 along with gate aa (`guardrails/check-doc-findings-bound.py`). Group ten — every live document the nine named groups leave out, worst first — is empty for the same reason: the census was also this page's only source for which documents are live and how they rank, and no other source stands in for it here.

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
| 4 | `NEXT_STEPS.md` | not measured | not measured | no | waiting |

### 4. The four documents behind the language rules (text-audit itself moved to its own repository, 2026-08-18 — skills/text-audit-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 5 | `docs/language-rules.md` | not measured | not measured | no | waiting |
| 6 | `docs/spec-style.md` | not measured | not measured | no | waiting |
| 7 | `docs/spec-format.md` | not measured | not measured | no | waiting |
| 8 | `docs/language-worked-example.md` | not measured | not measured | no | waiting |

### 5. The three skills loaded in every task run by the method

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 9 | `skills/live-spec-base/SKILL.md` | not measured | not measured | no | waiting |
| 10 | `skills/build-pipeline/SKILL.md` | not measured | not measured | no | waiting |
| 11 | `skills/communicator/SKILL.md` | not measured | not measured | no | waiting |

### 6. PLAN.md, read whenever a session picks up work

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 12 | `PLAN.md` | not measured | not measured | no | waiting |

### 7. The remaining six skills (product-prover moved to its own repository, 2026-08-13 — skills/product-prover-pack/SKILL.md is the thin adapter left behind, measured below among the remaining live documents)

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 13 | `skills/design-reviewer/SKILL.md` | not measured | not measured | no | waiting |
| 14 | `skills/feedback-collector/SKILL.md` | not measured | not measured | no | waiting |
| 15 | `skills/feedback-intake/SKILL.md` | not measured | not measured | no | waiting |
| 16 | `skills/publish/SKILL.md` | not measured | not measured | no | waiting |
| 17 | `skills/spec-author/SKILL.md` | not measured | not measured | no | waiting |
| 18 | `skills/test-author/SKILL.md` | not measured | not measured | no | waiting |

### 8. The specification family

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 19 | `PRODUCT_SPEC.md` | not measured | not measured | no | waiting |
| 20 | `ARCHITECTURE.md` | not measured | not measured | no | waiting |
| 21 | `TEST_MATRIX.md` | not measured | not measured | no | waiting |

### 9. The documents a stranger meets on arrival

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|
| 22 | `README.md` | not measured | not measured | no | waiting |
| 23 | `OVERVIEW.md` | not measured | not measured | no | waiting |
| 24 | `adopt/ADOPT.md` | not measured | not measured | no | waiting |

### 10. Every remaining live document, worst first

| # | document | findings today | measured clean | read clean | state |
|---|---|---|---|---|---|

## Promise one — a reader gets through a document without stopping

The counts below once came from the record `guardrails/rule-census.json`, written by `scripts/rule-census.py`. Both were retired 2026-08-21 along with gate aa (`guardrails/check-doc-findings-bound.py`); every measure that came from them now reads "not stated" until a live source replaces the retired record.

| measure | today | recorded before | target |
|---|---|---|---|
| live documents measured | not stated | 108 | all of them |
| writing findings across all documents | not stated | 4,810 | 0 |
| documents at zero findings | not stated | 16 | all |
| documents that passed two consecutive readings with nothing blocking | 0 | not stated | all |

The fifteen documents carrying the most findings: none — the source record was retired 2026-08-21 (see above).

| document | findings | of which long sentences | style | longest sentence | readings run | passed |
|---|---|---|---|---|---|---|

## Promise two — the specification stops growing

| measure | today | at the format change, 2026-07-23 | target |
|---|---|---|---|
| bytes | 51,094 | 590,695 | under the ceiling |
| lines | 316 | not stated | set by the subdivision plan |
| words | 8,548 | not stated | set by the subdivision plan |
| requirements | 0 | 282 | set by the subdivision plan |
| acceptance criteria | 0 | 1,372 | set by the subdivision plan |
| bytes per criterion | not stated | not stated | no target |
| pairs stating one fact twice | 115 | 116 | no target |

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
