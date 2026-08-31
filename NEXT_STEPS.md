# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-31, 21:35)

Written for a session starting with clean context. Heals landing 16b1a300, heals landing
6d0257ac, heals landing 8da47015.

**A hostile read of the remaining board found five rows to archive, one already done, and
eleven real ones overbuilt or vaguely sourced — asked for by the owner directly** ("из этих
20 в очереди точно все нужны?"). Full findings, bucket by bucket, are in
`.live-spec/checkpoints/night-run-2026-08-28.md` under "THE HOSTILE REVIEW OF THE REMAINING
BOARD". The method it set: narrow a row's acceptance in `PLAN.md` before dispatching a
worker on it, never hand the original wording to a fresh agent and hope it self-narrows —
learned from `q-55`, whose original justification cited five spec requirements that turned
out not to exist, caught only because the review ran before the worker finished.

**Three landed since the last note**: the Director/`q-497`/`q-527` merge (`16b1a300`,
pushed, CI green — a fresh-context read refused the first build of that merge and found
nine real defects, all repaired before it went out); then `q-531`, `q-801`, and a narrowed
`q-55` (locally at `8da47015`, **not yet pushed** — see below).

**`q-531` (critical) — a document split now proves it lost nothing.**
`scripts/nothing-lost.py` compares a document's before-state against its after-files at
block granularity (heading, paragraph, list item, table row, code fence, thematic break),
normalized for whitespace, as a multiset — so reordering across files is fine, a dropped
block is caught and printed with its content. Proven against two real splits in this
repo's own history (`ARCHITECTURE.md`'s and `PRODUCT_SPEC.md`'s, the second correctly
distinguishing an intentionally deleted reference table from a real loss). A `q-531` key
in `scripts/plan_checks.py` computes the mark. tlvphotos's own conversion has not started
(`~/tlvphotos/SPEC.md` is still one file) — read-only, not run against it for real yet.

**`q-801` — release 6.1.0, a new project starts on one list.** Two decisions executed: a
project founded from now on gets the one-list shape (no legacy queue file); an existing
host with a separate queue is asked to change nothing. Eleven-plus files repointed,
`templates/ROADMAP.template.md` retired to `attic/`, `templates/PLAN.template.md` takes
its place. `VERSION` 6.0.0 → 6.1.0, skill stamps followed, `MIGRATION.md` carries the
6.1.0 chapter. Gate (s)'s skill-review record and gate (a)'s prover record are both
written for the range.

**`q-55` — narrowed, then landed.** The hostile review found its stated justification
false (E-6, E-7, E-10, A-6, INV-17 don't say what the row claimed). Cut to the one real
case: a project joining with no git history gets one commit of its files as found, before
any pack file lands; a project with existing history is untouched, and the step is
idempotent. `adopt/record-starting-state.sh`, wired into `adopt/ADOPT.md` Phase 0 step 2.

**`q-386` was proposed for closing on tonight's own merge history as proof, and stays
open.** Three of its four legs hold (the lane cap is enforced and tested; the landing
sequence is stated identically in the law and the script; independent work running side by
side and merging with no hand repair happened a dozen times tonight). The fourth does not:
nothing checks that the lane-opening script and the written law describe the act the same
way, so the two could drift apart today and nothing would catch it. The row keeps that one
leg; do not re-propose closing it without building that check.

**Not yet pushed, and two real gate failures are open right now** — this is the first
thing the next session does:
1. `tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` — this
   very LIVE STATE update is the fix; re-run it after this file is committed in the same
   commit range and it should clear.
2. `tests/test_traceability.py::TestTargetOwnership::test_targets_owned_by_open_rows` —
   **not fixed, and here is real diagnosis, not just the failure.** `q-55` is marked done,
   but five spec `[target]` anchors (E-6, E-7, E-10, A-6, INV-17) still name it as their
   owning task. Read `TARGET_ROW_OWNERS` in `tests/test_traceability.py` (~line 1454) and
   `target_marker_anchors()` beside it: the anchors live in the *assembled* body
   `conftest.read("PRODUCT_SPEC.md")` returns (8,357 lines), built from `spec/*.md` parts —
   **not** the 315-line file you see with a plain `cat`, which is only a glossary/index.
   Checking the raw file directly, the way this session's own hostile-review pass did
   earlier tonight, makes the anchors look absent when they are not — that pass's claim
   ("E-6/E-7/E-10/A-6 appear nowhere in PRODUCT_SPEC.md") is itself wrong, caught only now.
   Use the assembled read, or `bash scripts/plan-step.sh` sibling tooling, never `cat`.

   What each anchor actually is, checked directly: **`A-6`** (`spec/adopt-existing-project.md:25`,
   "save a first baseline snapshot of the host's artifacts as found, git-tracked, as the
   diff baseline the snapshot machinery guards") is a real, close match to what `q-55`'s
   landed work (`adopt/record-starting-state.sh`) actually does — re-owning it to `q-55` and
   dropping its `[target]` tag as satisfied looks right, but confirm the "diff baseline the
   snapshot machinery guards" clause isn't citing a *different* baseline system (see next)
   before doing that. **`E-7`** co-occurs with `A-6` at that same line but its fuller
   definition (`spec/doc-order-generated.md:301-307`) is about a *different* baseline: a
   rendered-surface snapshot folder (`.live-spec/snapshot/`) for the design-sync machine,
   with its own manifest and heavy-byte handling — this looks unrelated to project
   onboarding and may have been mis-cited onto `q-55` from the start, not something today
   broke. **`E-10`** (`spec/doc-order-generated.md:360-365`, `spec/work-board.md:24`,
   `spec/design-spec-review.md:211`) is the surface-registry completeness gate
   (`SURFACES.md`) — also design-sync territory, not onboarding. **`E-6`**
   (`spec/design-spec-review.md:560-561`) is the prototype-into-prod fence turning red —
   also unrelated. **`INV-17`** appears across `spec/draft-sandbox.md`,
   `spec/design-spec-review.md`, `spec/roles-and-agents.md` as a general
   spec-claims-only-what's-built invariant, cited too broadly to belong to any one row.

   So the honest read: `A-6` probably is `q-55`'s to close (verify the snapshot-machinery
   clause first); `E-6`, `E-7`, `E-10` were very likely mis-mapped to `q-55` in
   `TARGET_ROW_OWNERS` before tonight and belong to whatever row (if any) owns design-sync
   and the surface registry — check `plan-14`/`q-54` territory; `INV-17` may need to stay
   generic or get dropped as too broad to own. This is real spec work, not a rubber stamp —
   read each cited spec line yourself before touching the map. Once resolved:
   `python3 -m pytest -q` clean, `bash guardrails/pre-push`, push.

**Still owed, unwritten, carried forward from an earlier note:** a `JOURNAL.md` entry for
the prover-description-test movement (`85b659d1`, from 31.08 morning).

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. Build it with `python3 scripts/measurements-table.py`. A number stated to the person who decides
what ships names four things. They are what it counts, the decision it informs, the command
that produced it, and the value it aims at.

## Rules you must not break

Several sessions share this repository. Stage files by name, and never run `git add -A`. Read
`git log -1` before you write. When the commit it names differs from the one you recorded at the
start of your session, read what changed and run `bash guardrails/fence-refresh.sh`.

Never discard uncommitted work. No session and no worker runs `git checkout -- <path>`,
`git checkout .`, or `git restore` outside `--staged`. The same holds for `git stash` in every
form, for `git reset` with `--hard`, `--merge` or `--keep`, and for `git clean` with `-f` or
`-x`. To put a file back, write back the bytes you read before you changed it.

Never give two workers the same file. A test result is the printed count of passes and failures.
Run `python3 -m pytest -q > <scratch>/suite.log 2>&1` and read the last line.

`PRODUCT_SPEC.md`, `ARCHITECTURE.md` and `TEST_MATRIX.md` are frozen against silent drift. After a
commit that changes one on purpose, record the new baseline: `python3 scripts/spec-freeze.py
--freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`.

`bash guardrails/pre-push` runs the whole push gate set, listed in `guardrails/README.md`. New
requirements, invariants and queue rows take the next identifier above the highest one in use in
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `PLAN.md`. Read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask.
Publish once the suite passes. Write documents in plain English. Speak of every task by its board
echo-name in every communication. Before you ask the person who decides what ships anything,
check whether a document already answers it. If it does, act on that answer and cite it. Say
aloud whether a request is one-time or standing before acting. Guard Fable tokens hard (his word
2026-08-11 14:52, standing). A Fable seat spends its own turns only on decisions and acceptance.
Reads, drafts and sweeps go to workers on cheaper tiers, and replies stay short. The campaign
plan itself always carries execution statuses, kept current by point edits with delta pages (his
word 2026-08-11).

Keep the session's task list visible for the whole of a pass, one item per step. Word each item as
the plan document words that step. Give every spawned worker a label carrying the same number and
title in the chat language (his word 2026-08-12 08:40, standing). Three surfaces then say one
thing: the agents panel, the task list, and the plan. The plan file stays the one source, and the
list holds the current pass alone. This line owes a copy in the personal profile, which lives in
another repository and waits for a session that owns it.

A worker never runs the full suite. This environment moves a foreground command past 600 seconds
into the background, and the suite runs 18 to 21 minutes. A worker that starts it stalls and then
returns an unfinished report as final. A brief names the exact test files that finish in seconds.
The orchestrator runs one clean full suite at the end of a pass with no worker active. A run taken
while workers write the tree reds on files being written, and its reds carry no verdict.

## Prompt for the next session

**Everything below this line was written 31.08 21:35 for a session resuming after a context
reset mid-way through the 28.08 night run. Read `bash scripts/state-probe.sh` and this
file's own LIVE STATE section above first — this prompt only tells you what to do with
what they show you.**

Do not ask Alexander anything before doing the two fixes below. His standing word for this
run (28.08 00:53, repeated 31.08 12:12 and 18:32): carry the plan to the end, do not ask
him, push and deploy are pre-authorized on green. Nothing here overrides that.

**Step 1 — clear the two real gate failures blocking tonight's unpushed work.**
1. `tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` should
   already be clear, since this file's own edit is the fix (INV-242: a landing commit
   needs a NEXT_STEPS.md refresh somewhere in its range, and this section is that refresh
   for commits `16b1a300`/`6d0257ac`/`8da47015`). Confirm it passes; if it doesn't, the fix
   didn't land in the pushed range and needs redoing.
2. `tests/test_traceability.py::TestTargetOwnership::test_targets_owned_by_open_rows` is
   **not fixed** and needs a real look, not a guess: five spec `[target]` anchors (E-6, E-7,
   E-10, A-6, INV-17) still name the now-done `q-55` as their owner, and the narrowed work
   that actually landed doesn't address any of them. Read what each anchor promises in
   `PRODUCT_SPEC.md` (or wherever `grep -rn "\[target\]"` finds them), decide per anchor
   whether something else already covers it (re-own the tag) or the promise is genuinely
   dead (drop the tag with a one-line note saying why), and make the test pass honestly —
   not by weakening it.

Then: `python3 -m pytest -q` clean (check `ps ax | grep pytest` first — nothing else should
be running), `bash guardrails/pre-push < /dev/null` reading its verdict line, push, confirm
CI green.

**Step 2 — walk the hostile review's remaining list, one row at a time.** The full findings
are in `.live-spec/checkpoints/night-run-2026-08-28.md` under "THE HOSTILE REVIEW OF THE
REMAINING BOARD" (31.08 18:34, run because Alexander asked directly whether the board's
remaining rows were all real or partly junk/unneeded machinery). Its buckets, already
decided, not to be re-litigated:
- **Archive now, no work:** `plan-15`, `q-453`, `q-48`, `q-751` — each with its reason
  already written in the checkpoint.
- **Solid, build as written:** `plan-10`, `q-591`, `plan-9` (already correctly deferred on
  his word — do not start it).
- **Real but overbuilt — narrow the row's acceptance in `PLAN.md` before dispatching a
  worker on it, every time, no exceptions:** `q-581`, `q-576`, `q-437`, `plan-14`, `q-163`,
  `q-489`, `q-536`, `q-54`, `q-235`, `q-398`. The checkpoint names exactly how to narrow
  each. This rule exists because `q-55`'s original wording was handed to a worker before
  being narrowed and had to be corrected mid-flight — don't repeat that.

Work lanes the same way the whole run did: up to three parallel worktree lanes
(`Agent` tool, `isolation: "worktree"`), each briefed with the row's own (narrowed)
acceptance as the definition of done, each running its own full suite before reporting,
merged by a dedicated merge pass that reads both sides on conflict and runs an adversarial
re-read of its own merge before pushing — that pattern caught real defects every single
time it ran tonight and should not be skipped as a shortcut.

Three rows wait on Alexander's own read and take no further work: `q-800`, `q-166`,
`q-501`. Do not build anything for these; they close only when he reads them.

Report to him in the Канон format his own boot file (`~/.claude/CLAUDE.md`) specifies —
`bash scripts/state-probe.sh`'s own printed plan, never a hand-typed summary — after every
row that lands, not only at the end.
