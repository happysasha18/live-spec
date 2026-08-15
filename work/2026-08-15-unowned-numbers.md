# The unowned numbers, refreshed against tonight's tree — read-only, 2026-08-15

The 2026-08-14 ownership inventory
(`/private/tmp/live-spec-night/defaults-and-thresholds.md`, taken against `main` at `acf0e3c`)
marked **42** numbers "unowned AI-invented candidate" — the night brief called it ~38. Every one
of the 42 was re-resolved tonight against `39e393c`: each named home still exists and still
carries its number. **Nothing has been struck since the inventory was taken**, and the one home
outside the repository (`~/.claude/hooks/lean-orchestrator-scan.py`) is untouchable from here by
the night's boundaries.

No repair, no deletion, no ruling is made below. This is the list the owner rules on.

## The five priority rows

Each verified at its path tonight, with the line the value sits on.

| # | number | value | home tonight | what a wrong value does |
|---|---|---|---|---|
| 1 | `DEFAULT_SINCE_HOURS` | `24.0` | `guardrails/check-worker-restore.py:175` | the destructive-git scan window. Too small and a destructive act older than a day is never surfaced; too large and every run pays to re-read a week of transcripts. |
| 2 | `MAX_WAIVER_DAYS` | `30` | `scripts/gate_common.py:119` (enforced by `tests/test_prose_gate.py:222`) | how long a lint exemption stands before CI hard-fails. Too small and honest work is interrupted; too large and a waiver becomes permanent silently. |
| 3 | `JAC` / `CON` / `MIN_TOKENS` | `0.60` / `0.85` / `6` | `scripts/spec-redundancy-precheck.py:32-34`, hand-mirrored in `guardrails/language-rules.json` | the definition of "redundant" across the spec. These decide which pairs a person is asked to merge; the hand-mirroring means two homes can drift apart. |
| 4 | `CPU_THRESHOLD` / `IDLE_THRESHOLD` | `50.0%` / `120.0s` | `guardrails/check-runaway-child.py:52`, `guardrails/reap_owned_group.py:39` | the auto-termination of worker processes. The known incident: a suite SIGKILLed mid-run on 2026-08-13/14. Too aggressive and honest compute dies; too lax and a runaway burns the machine. |
| 5 | `rounds_expected` / `working_hours_per_day` / `parallel_lanes` | `5` / `6` / `4` | `guardrails/progress-baseline.json:261,264,265` | the estimate inputs behind every projected finish date. The file's own comment admits `rounds_expected` rests on one measured file and is "the weakest input here". |

Note on the fifth: the parallel dossier brief names this file as `progress-baseline.json` at the
tree root. It lives at `guardrails/progress-baseline.json`; there is no root copy.

## The other thirty-seven

All verified present tonight at the homes named.

**Pack rules and skill bodies.**

- far-tier surfacing cadence, 14 days — `skills/live-spec-base/SKILL.md`
- full-audit cadence, every 10 landings — same file
- design↔prover loop cap, 3 rounds — `skills/build-pipeline/SKILL.md`, `skills/design-reviewer/SKILL.md`
- design-review question cap, 3 per pass — `skills/design-reviewer/SKILL.md`
- brief size bound, ~300 lines / ~8 files — `PRODUCT_SPEC.md`, `skills/build-pipeline/references/delegation-protocol.md`
- cross-agent question routing, 2 crossings — `PRODUCT_SPEC.md`
- worker stall detection, ~2 min — `PRODUCT_SPEC.md`
- inline-read threshold, 50 KiB — its second home sits outside this repository

**Registry ratchets and detector thresholds.**

- `guardrails/tier-refusal.json` — 3 refusals; 2–8 word phrases
- `guardrails/criterion-readability.json` — 35 words, 25 chars, 4 words, 3 codes/3 spans, 60 words
- `guardrails/tree-counts.json` — expected_seconds 10
- `scripts/spec-debt-cap.json` — the zero-bars
- `guardrails/crosscut_counter.py` — 3
- `guardrails/check-deposit-description.py`, `check-description-field.py` — MIN_WORDS 2
- `guardrails/check-landing-next-steps.py` — freshness window 2 days
- `guardrails/check-tree-counts.py` — OPENING_CHARS 160
- `scripts/spec-style-lint.py` — NEG_OPENER_WORDS 12
- `scripts/rule-census.py` — roster shape 4 / 4
- `scripts/rank-criterion-defects.py` — top_n 40

**Machinery timeouts.**

- `guardrails/check-hooks-can-fire.py` — 30 s
- `scripts/stranger-wish-monitor.py` — LOCK_STALE_SECONDS 3600
- `scripts/sweep-rendered.py` — HEAD_BYTES 4096
- `scripts/gen-tree-counts.py` — STAGE_SECONDS 120
- `scripts/check-pack-update.sh` — curl max-time 10 s

**CI.**

- the stranger-monitor cron, `17 6 * * *`
- its push retry count, 3
- the absent `timeout-minutes` key in both workflows; the platform default stands unstated

**Floors asserted inside tests.**

- ARCHITECTURE.md node-count floor, ≥20 — `tests/test_architecture_format.py`
- hedge-fixture floors, ≥8 / ≥2 — `tests/test_hedge_arm.py`
- mid-turn scan budget, <0.1 s — `tests/test_midturn_chat_scan.py`
- INV-286 anchor/index floors, ≥8 — `tests/test_rendered_sweep.py`
- register-judge kept-quote floor, ≥40 chars — `tests/test_register_judge.py`
- worker-command-check window, 24 h — `ROADMAP.md`
- redundancy-pair flag threshold, 3 — `ARCHITECTURE.md`

## The one number that matters

42 numbers still await his word. None moved since the inventory was written; the list does
not shrink on its own.
