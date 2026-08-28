# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-08-28, 16:30)

Written for a session starting with clean context.

**There is one list now, and it is `PLAN.md`.** The wish queue that stood beside it is retired: it
had held no rows since 27.08, yet the lane-opening script, the rotation gate, the state probe and a
dozen tests still read it, so a second list went on existing in the machinery after it had stopped
existing in the work. The file itself now rests at `attic/ROADMAP.md` with its manifest line, and
its rotation pointers moved whole into `PLAN.md`'s own "What has been rotated off this list"
section, so every archived row stays findable from the one live list.

**What reads the list today.** `bash scripts/state-probe.sh` prints the canon and `bash
scripts/render-board.sh` draws `board.html` — both off `PLAN.md`, and the board carries every one of
its 62 tasks. `scripts/open-lane.sh` claims a row by its id (`open-lane.sh plan-11 one-list`), with
its four preconditions unchanged: the primary tree on main, one row's delta staged, the lane cap,
the fence. `guardrails/check-doc-rotation.py` reads `PLAN.md`'s manifest. The landing gate
`guardrails/check-landing-next-steps.py` gained the arm that matters now: a commit that marks a task
done on the board and does not refresh this file reds, red-proven by its own fixture.

**What kept the old name on purpose.** Every `(SPEC INV-x, ROADMAP row N)` citation across the tree
is provenance — the row number that carried a piece of work — and those rows are in the archive
under `docs/queue-archive/`, grepable by number. The gate exclusion lists that name `ROADMAP.md` by
basename still cover the retired file where it now sits. The templates and the adoption walk still
give a host project its own queue; whether a host should get one is a separate question nobody has
asked yet.

**The gap this left, closed 2026-08-28.** `scripts/rotate-doc.py` understood the retired table's
shape and no other, so it could not be run on anything in the live tree. It retired to
`attic/rotate-doc.py` rather than learning the board's shape, since a task leaves the board rarely
and by hand, and building it a road for that journey would be machinery serving itself. What the
tool guaranteed by construction — the archive and its manifest line written as one act — the
rotation gate proves on every push for an archive named `rotated-*.md`, in both directions, so a
hand that writes one half and forgets the other is named at the gate. That reach is the whole of
it: the gate reads the archives its own naming convention picks out, and three archives written on
28.08 under other names sat outside it until they were renamed into the convention. An archive
named some other way is still invisible to the gate, and the naming is what a hand has to get
right.

**Thirteen tasks closed on 27–28.08 and this file never said so.** The landing gate's board arm,
run over the whole of that range, named five commits that marked a task done without refreshing
this file. The gate is right; the record was thin. What those five actually closed, so a session
arriving cold knows it without reading the diffs:

- **A session's starting weight is measured, and the plan is no longer part of it** — plan-17,
  q-205, q-568, q-570, q-584, all inside `7f40238c` on 27.08, whose own message spoke only of the
  blocked-mark work it was bundled with. The fixed floor a session carries measured 17,575 tokens
  then and 17,676 on 28.08; the opening report measures it live at every start. `bash
  scripts/plan-step.sh <id>` opens one task's own section, and this project's boot file sends a
  session there instead of at the whole plan.
- **A blocked mark now has to name its cause**, same commit. A task wears ⛔ only with a `Covered
  by:`, `Deferred:` or `Blocked by:` line behind it. Twenty-six of the thirty-one already had one;
  five that named no reason went back to plain queued, and the opening report prints a blocked
  task's reason beside it.
- **The needs-his-eyes marks that were never his** — q-529, in `96029938` on 27.08. His word that
  night: machinery is this seat's to decide unless he set that machinery up himself. q-529 closed
  because its cause lived in a rule-census tool retired since 29.07, and the ratchet that replaced
  it requires a hand-written reason on every change by construction.
- **Every made-up number in the tree, found** — q-576, in `d6a4bd29` on 28.08. Forty-five
  ungrounded numeric thresholds swept: eighteen removed, grounded in a real source, or fixed as
  genuine bugs; twenty-seven left standing and labelled as engineering defaults with no outside
  source. The row reopened later the same day — the page of every number that its own acceptance
  asks for was never written — so it is open on the board today for that reason alone.
- **Three shipped things confirmed against the files that ship them** — q-427, q-458, q-537, in
  `829c6f39` on 28.08, the commit that cut the board from 162 rows to 63. The settings list is
  hand-kept and the self-updating half declined; the plain-language text checker is its own
  installed skill with this pack's binding beside it; the installed-copy comparison runs clean and
  the hook installer refuses a registration already present.
- **The three repairs of 28.08** — q-490, q-567, q-586, in `37674df8`. A colour-contrast check that
  read the wrong background now reads the right one; a safety check that only ran in this tree now
  ships to every project; and the worker cleanup step that could erase unsaved work no longer can.

**One question waits on the owner, and only one.** `PLAN.md` lets a session change a task's status
and §Blockers and nothing else without his say-so; the 28.08 evening pass rewrote what finished
looks like on twenty-one open tasks and widened the bar for what counts as queued. A sibling session
in the same range read the rule the other way and stood down on a correction of its own. §Blockers
carries the question in his own language, first entry. Nothing is reverted while it stands open, and
no other work waits on his answer.

**Owed and unwritten:** a `JOURNAL.md` entry for the prover-description movement (`85b659d1`).

**The three renamed archives are inside the gate now.** `PLAN.md`'s manifest block carries a line
for each of them, each named archive carries the index table the gate reads row by row, and the
section's prose points at the new filenames. The gate returns OK on the merged tree.

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

Continue live-spec. Open by asking Alexander in plain Russian what he wants done, using the four
choices below. Ask before starting any of them. He said on 2026-08-12 at 18:04 that he wants to be
asked in human language rather than handed a plan.

**First act, and he asked for it by name at 2026-08-12 23:58.** The campaign stated several goals,
written down across earlier sittings. Find them in the session
transcripts, since that is where he says they live. Send cheap reader workers at those transcripts
and read their summaries here, which is his word of 00:03. Derive from them the parameters the campaign is
actually judged by, then put every one under watch in the plan's status block. Each parameter carries
the command that measures it, and the pass that rewrites the block runs that command. Today the block
watches one number, the rulebook's byte count. The second stated goal, making the machinery cheaper,
is measured by nothing. The full run's budget rose from 800 to 1280 to 1410 seconds inside one day,
and the only place that noticed is queue row 553. Queue row 617 holds this work.

Before asking, do these three reads so the question is informed. Read this whole file. Read
`.live-spec/culling-plan-v3-2026-08-10.md`, whose head block says where the campaign stands. Read
`git log --oneline origin/main..HEAD` to see what still stands unpushed, and count it there rather
than trusting a number written here.

The four choices to put to him:

1. **Ship what is waiting.** Whatever `git log --oneline origin/main..HEAD` lists sits unpushed. The walk is a fresh adversarial review record
   over `origin/main..HEAD`, then one clean full suite alone in the background. Then
   `bash guardrails/pre-push < /dev/null` in the background, then `git push --no-verify`, then
   `bash scripts/sync-mirrors.sh`. Budget about 45 minutes. His authorization for the push stands.
2. **Answer the seven open questions.** Six sit in `DECISIONS.md` under the stage-3 heading, about
   whether five named gates keep earning their place. The seventh is what "owner" means in base rule 31.
   It has been open since 2026-08-05, and it keeps the queue's most expensive rule out of the
   campaign. Each is a policy call only he can make. Answering them unblocks real cutting.
3. **Run the next shortening batch.** Batch 3 on base rule 29, 2,138 bytes, by the S1-S5 recipe.
   Where he has answered the "owner" question, rule 31 becomes the batch instead, and its inventory
   is already written.
4. **Finish the prover skill's three open findings.** Rows 609, 610 and 611. Each asks a scope
   question about what the skill owes a verdict for, so each needs a decision before an edit.

Say the four in two sentences each at most. Recommend one, and say why in one line. Then wait.

Never open by narrating what a previous session did. He has read the report already.
