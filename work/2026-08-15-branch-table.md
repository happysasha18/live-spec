# The branch table — read-only, 2026-08-15 night

Every branch in `/Users/sashaabramovich/live-spec`, its tip, whether `main` already contains it,
the worktree holding it, and one recommendation. Nothing here was deleted, moved or merged: this
is a table for the owner's ruling.

`main` is `39e393c` and did not move tonight. Seventeen branches stand. The night brief
expected thirteen; four arrived after that count was taken, two of them tonight's own work.

## Contained in `main` — the work has landed

| branch | tip | worktree pinning it | recommendation |
|---|---|---|---|
| `fix/2026-08-14-ci-home-and-templates` | `0956d93` | `/private/tmp/live-spec-fix2/wt-fix2` | delete, with its worktree |
| `fix/2026-08-14-scratch-keeps-canon` | `d4e0e2f` | `/private/tmp/live-spec-fix/wt-fix` | delete, with its worktree |
| `fix/2026-08-15-gate-a-recordless` | `39e393c` | `/private/tmp/live-spec-gate-a/wt` | delete — it holds no commit of its own; the gate-a work lives on the `-2` branch below |
| `green/2026-08-14-claude` | `4e8df4c` | `/private/tmp/live-spec-green-candidate/wt-green` | delete, with its worktree |
| `ladder/2026-08-14-settings-split` | `b2fc1af` | `/private/tmp/live-spec-ladder/wt-ladder` | delete, with its worktree |
| `night/2026-08-14-candidate` | `cd6ef7b` | `/private/tmp/live-spec-roadmap-wave/wt-candidate` | delete, with its worktree |
| `relay` | `b3373ac` | none | delete — landed 2026-08-06 |

## Carrying unique commits — the owner's ruling

| branch | tip | unique commits | worktree | recommendation |
|---|---|---|---|---|
| `night/2026-08-15-batch` | `3ab6c1c` | 4 — tonight's units 1, 2, 3 and its skill-review record | `/private/tmp/live-spec-night2/wt-batch` | **his push word**: this is the night's work, unpushed by the night's own law |
| `fix/2026-08-15-gate-a-recordless-2` | `a0060d2` | 1 — "Gate a learns the owner's recordless class; the agent card carries his full speak-to-owner format" | `/private/tmp/live-spec-gate-a2/wt` | **his push word**: the parallel gate-a mission's landing, authorized in its own brief |
| `night/2026-08-13-integration` | `5ea60dd` | 12 — the external-prover decoupling (anchors re-homed, bare-checkout skips, version-stamp fence, census stops walking the external clone) | `/private/tmp/live-spec-night-integration/wt-integration` | **his ruling**: twelve commits of real work never merged; either land the range or record why it is abandoned |
| `prover-decoupling-emergency-2026-08-13` | `7d8d947` | 5 — the emergency decoupling and its three adversarial reads | none | **his ruling**: same subject as the row above; the two need reading together before either is deleted |
| `night/2026-08-13-ck2-neutral` | `6915ef5` | 4 — gate t's archive-to-manifest direction, row 558's citation, two table-splitter repairs | `/private/tmp/live-spec-night-integration/wt-ck2` | **his ruling**: small, self-contained, still unlanded |
| `backup-2026-08-06-before-relay` | `28791f7` | 4 — the pre-relay backup point | none | keep until the relay work is settled, then delete |
| `codex-2026-08-14-first-bounded-mission` | `d2387a5` | 2 — Gate B scratch-proof fidelity, a stale Gate F proof path | `/private/tmp/live-spec-first-bounded-mission-wt` | **his ruling**: two repairs that look landable; read and land or drop |
| `p2-change-classifier` | `23a1fb6` | 1: the P2 change-classifier prototype | `/Users/sashaabramovich/live-spec-p2` | keep while P2 is live; it stays a prototype |
| `wip/comms-naming-424` | `55597bc` | 1: a work-in-progress checkpoint, "comms/naming build, proven spec delta, still unlandable" | none | **his ruling**: 2026-07-19, the oldest unique branch here; land the spec delta or delete the checkpoint |

## Detached worktrees holding no branch

`/private/tmp/live-spec-night-integration/wt-baseline` and
`/private/tmp/live-spec-roadmap-wave/wt-baseline` sit detached at `acf0e3c`; a scratchpad
worktree sits detached at `2718c69`. All three are baselines for comparison runs and can be
pruned with `git worktree prune` once their missions close.

## The one number that matters

Seventeen branches. Seven sit fully inside `main` and can go today. Two await his push word.
Six await his ruling on work that never landed; two are prototypes or backups.
