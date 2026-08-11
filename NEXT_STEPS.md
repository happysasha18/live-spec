# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-11, 16:41)

Written for a session starting with clean context.

**One plan — the standing order, his word 2026-08-10 21:26.** The only plan is the cutting campaign.
Base: `.live-spec/culling-plan-2026-08-08.md`, frozen, the record of what was ordered. Executing
revision awaiting his «принято»: `.live-spec/culling-plan-v3-2026-08-10.md` (Russian, his word of
21:12; its line-by-line provenance sweep is `.live-spec/plan-v3-sweep-2026-08-10.md`). Every
live-spec session works on this plan until it is accepted and executed. An interrupted session
changes nothing: the next one resumes the same plan at the same step. Every status line is phrased
in the plan's own step codes (U/R/D/S/C). The plan file itself carries execution statuses — done /
in work / waiting. Point edits with delta pages keep it current (his word 2026-08-11 ~14:55). If
Alexander himself asks for work outside the plan, the session answers with one line naming the
unfinished plan. It then asks whether to fold the request in or set the plan aside by his word.
The page he reads is the claude.ai artifact rendering the v3 file; regenerate it from the
committed file only. One more order of his, 2026-08-11 10:23. Once the plan is submitted for his
review, the session executes nothing from it until the review happens. The exception is what he
ordered directly. His 11:08 «давай все по некст степс» was that direct word for D4, D8 and R7.

**Where it stands, 16:41.** Phases 0 and R are closed, R7 included. The R7 escort inventory sits
at `.live-spec/escort-inventory-R7-2026-08-11.md` (`fa6d6a9`): 41 mandated escorts — 21 from his
dated word, 11 derived, 9 invented. Prior R-step numbers live in the plan's stamped steps and the journal. They are R2 6,363 bytes /
37 groups, R5 46,100 bytes / 307 tests, R3 51-of-88 unenforced. The
sitting's rulings, after his second and third passes (`DECISIONS.md`): D1 yes. D3 keep. D4
executed — one review record per push, read by one gate; gate ac and Requirement 305 retired
(`06cf3ae`). D5 yes and executed — verification after each real change, no schedule, the
two-hour session alarm removed. D8 executed (`a829e8b`, suite then 2,484/0). D6 struck; D7
scheduled with him at the keyboard, later. D10 and D11 stay parked as policy calls. D2 waits his
«делай»; the rule-23 broadening that makes it whole is a campaign-close post-action in the plan.
D9 is explained in chat; its word comes at the campaign close. Suite now: 2,486 passed, 0 failed
(16:37 log).

**Debts closed this afternoon (`391ba41`, `c9a4088`).** The 219-vs-218 figure, the retired
R303.19 citation and ROADMAP row 522's gate-ab clause are fixed. The "ten skill folders" debt was
already closed. Gate s now checks freshness per candidate record, pinned by two red-then-green
tests on the bug lane. Its honest new red — the 2026-08-11 skill-review record lacks a
`Verdict:` line — is in repair with a worker. The prover edition carried the newer skill work.
The problem ledger holds a new WATCHED line: parallel pytest runs share /tmp and red the
leaked-temp gates on a neighbour's files.

**Runnable next.** The verdict-line repair commit lands. Then a fresh clean-context agent writes
the one range review record in the merged form, covering every unpushed commit
(`git rev-list --count origin/main..HEAD`). On green: push, then `scripts/sync-mirrors.sh` and
the edition publish — both were held back so no unreviewed content leaves the machine. The
rule-30 removal waits his «делай». Phase 2 batches wait the plan's «принято»; phase 3 opens on
D2 plus the already-given D3.

**Three habits that cost 2026-08-09, named so the next session skips them.**
1. His instruction and the tree's record disagreed. The session picked the record and worked on.
   Stop there, state the difference in one line, and wait. This is the one case that blocks.
2. His spoken settings landed in a state page nobody governs by. A standing setting belongs in the
   profile. A task belongs in `ROADMAP.md`. `scripts/session-extract.py` already pulls his own turns
   for a fresh reader, and what it finds has to land in one of those two homes.
3. A page was rewritten whole where three lines needed changing. Change what needs changing.

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
aloud whether a request is one-time or standing before acting. Guard Fable tokens hard (his word
2026-08-11 14:52, standing). A Fable seat spends its own turns only on decisions and acceptance.
Reads, drafts and sweeps go to workers on cheaper tiers, and replies stay short. The campaign
plan itself always carries execution statuses, kept current by point edits with delta pages (his
word 2026-08-11).
