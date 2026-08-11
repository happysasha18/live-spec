# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-10, 21:40)

Written for a session starting with clean context.

**One plan — the standing order, his word 2026-08-10 21:26.** The only plan is the cutting campaign.
Base: `.live-spec/culling-plan-2026-08-08.md`, frozen, the record of what was ordered. Executing
revision awaiting his «принято»: `.live-spec/culling-plan-v3-2026-08-10.md` (Russian, his word of
21:12; its line-by-line provenance sweep is `.live-spec/plan-v3-sweep-2026-08-10.md`). Every
live-spec session works on this plan until it is accepted and executed. An interrupted session
changes nothing: the next one resumes the same plan at the same step. Every status line is phrased
in the plan's own step codes (U/R/D/S/C). If Alexander himself asks for work outside the plan, the
session answers with one line naming the unfinished plan. It then asks whether to fold the request
in or set the plan aside by his word. The page he reads is the claude.ai artifact rendering
the v3 file; regenerate it from the committed file only.

**Where it stands.** Phase 0 of v3 is closed. The missing architecture review record landed
(`docs/prover/2026-08-10-architecture-wall-time-row.md`), and commit `2121b91` went green: 2,490
passed, 0 failed. The adversarial range review found no blocker
(`docs/push-review/2026-08-10-the-repaired-range.md`). The push landed at 21:35 — 31 commits,
`ba479b6..e82da27`, every gate green. Rules cut: 0 of 88. Checks removed and still gone: 1 of 31.

**What waits on him.** The nine rulings D1–D9 on the v3 plan page, each carrying a recommendation,
one sitting. Phase R of v3 — six items his written word already covers, listed there — runs without
waiting.

**Debts recorded by the 2026-08-10 push review.** Findings 6, 7, 9 and 10 of the 2026-08-09
push-review record still stand. They cover 219 vs 218, gate s greening on a 2026-07-17 record, and a
retired R303.19 citation. Two more: "ten skill folders" vs 11, and ROADMAP row 522's gate ab
citation. The
push-review house format in `docs/push-review/README.md` differs from what gate ac's in-push arms
actually parse — worth a queue row. The post-push hook warns that `editions/product-prover/` is
older than `skills/product-prover/`: carry the newer work into the edition and commit it. Mirror
sync did not complete; run `scripts/sync-mirrors.sh` by hand.

**Three habits that cost 2026-08-09, named so the next session skips them.**
1. His instruction and the tree's record disagreed. The session picked the record and worked on.
   Stop there, state the difference in one line, and wait. This is the one case that blocks.
2. His spoken settings landed in a state page nobody governs by. A standing setting belongs in the
   profile. A task belongs in `ROADMAP.md`. `scripts/session-extract.py` already pulls his own turns
   for a fresh reader, and what it finds has to land in one of those two homes.
3. A page was rewritten whole where three lines needed changing. Change what needs changing.

**Right now.** A fresh review of the push range refused it on three findings. All three arrived with
the repair pass. Its record is `docs/push-review/2026-08-09-the-culling-first-day.md`. One of the
three is structural. An `ARCHITECTURE.md` edit demands a fresh record under `docs/prover/` that
descends from it, and a push-review record leaves that gate unsatisfied.

## Where the numbers live

`docs/MEASUREMENTS.md` holds one row per file and one column per indicator, in the reading queue's
order. Build it with `python3 scripts/measurements-table.py`. A number stated to the person who decides
what ships names four things. They are what it counts, the decision it informs, the command
that produced it, and the value it aims at. `guardrails/tree-counts.json` is the home for every count this
repository publishes about its own tree, re-measured by gate ad on every push.

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
`PRODUCT_SPEC.md`, `TEST_MATRIX.md` and `ROADMAP.md`. Read it before you claim a number.

## Standing instructions

Carry one change from its first edit to a passing suite and a push without stopping to ask.
Publish once the suite passes. Write documents in plain English. Speak of every task by its board
echo-name in every communication. Before you ask the person who decides what ships anything,
check whether a document already answers it. If it does, act on that answer and cite it. Say
aloud whether a request is one-time or standing before acting.
