# Next steps — live-spec

A digest, at or under 100 lines (SPEC INV-48). One status block stands here at a time, and every
update replaces it. Dated history lives in `JOURNAL.md`.

## LIVE STATE (2026-08-06, 22:02)

The work board movement (row 166, Live work board) ran the whole evening with Alexander in the
chat. It stands in inception by the stage ladder he set at ~21:34. Its specification is
Requirement 309: 99 criteria after three drafted passes and two folded review rounds, ids
INV-308..313, feature F-work-board, the whole scenario [target]. The queue's status vocabulary
gained *ready* across its five homes. The approved page form is frozen at
`docs/norms/work-board.html`. It is variant 8, his 20:47 "looks good" plus every later
amendment, and the dated history sits in the provenance file beside it. The architecture carries the work-board node
owning the six new rules; the matrix carries rows M-519..M-544, all todo. His nine widenings of
the evening are each in `DECISIONS.md` with their times, and the journal's 22:01 chapter tells the
whole arc. Estimate discipline started this evening: every estimated step of the movement closed
under its estimate.

## Forward queue

1. Row 166 continues — inception's remaining products, in order:
   a. The FULL adversarial review of Requirement 309 by a fresh seat with none of this evening's
      context (his ask ~21:49). Brief from primary sources only.
   b. The stage-ladder re-map (his ~21:34 word): columns become backlog · inception · ready ·
      in work · done. Validation is inception's exit, and exploration is inception's product. This
      is spec pass 4, and it opens with the round-3 scoped re-read the review loop still owes.
   c. The task-graph criteria (his ~21:35 word): every new wish is placed into the maintained web
      of tasks — relations, dependencies, parallelism — at arrival. The seat plans the path off it.
   d. The mid-flight-updates and history-fold criteria check (~21:49): widening count on the card,
      dated word-history behind it — partly folded already, verify at the re-read.
   Then the statement re-validates and the task turns *ready*. The build opens: the entry check,
   the board source file and generator, the page checked against the frozen norm.
2. The page's next revision reads `~/live-spec-carry/2026-08-06/kanban-tools-study.md` (card-face
   and history patterns from Linear/Jira/GitHub; lane header counts; the widened/edited marker).
   Collapsible per-deliverable folds are already owed (his ~21:34 word).
3. Row 567 (bug): the session rules name `scripts/preshow-register-lint.py`, and no host tree
   holds it. Ship the checker at adopt and catch-up, or re-word the law. From the tlvphotos
   report, atticked with the manifest naming this row.
4. Row 566: board-ready statements for the whole queue. Every open row gets an authored
   echo-name, description, plan and estimate through the entry check, in batches.
5. Rows 558, 559, 560 (waiting on Alexander: the two-name screens list), 561, 562-565, and rows
   532-546 stand as before; see the queue.

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
