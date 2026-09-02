# Next steps — live-spec

A digest with no redundancy (SPEC INV-48) — one live-state block, nothing removable without losing
information. One status block stands here at a time, and every update replaces it. Dated history
lives in `JOURNAL.md`.

## LIVE STATE (2026-09-02, 01:25)

Written for a session starting with clean context, covering the whole overnight run in
`534cb16b..49b4813f` — from the prompt-authoring session's own closing commit through this note.
Heals landing b5914865 (q-436), landing beaf953d (q-501), landing d0bbc72b (q-803) — three commits
in that range closed rows without touching this file
(`tests/test_landing_next_steps.py::test_real_repo_range_refreshes_next_steps` red on exactly those
three), the same shape this file's own prior entries already record for seven earlier commits; the
overnight prompt itself asked for exactly this: one honest pass at the end, covering the whole night.

**Scope and outcome, against the prompt's own eight rows.** `.live-spec/overnight-prompt-2026-09-01.md`
named `q-803`, `q-54`, `q-163`, `q-48`, `q-385`, `q-804`, `q-436`, `q-501`. Six actually moved
tonight; two stayed correctly untouched.

- **`q-436` (`b5914865`) — closed ✅.** The value-space in-between forcing step lands beside q-437's
  already-built two-poles duty in `skills/spec-author/references/facet-sweep.md`, and
  `skills/product-prover-pack/SKILL.md` reads an unnamed co-occurrence value as the same
  blank-answer class q-437's own sweep already reports. Requirement 265 criterion 15 rewritten to
  describe the built step; `TARGET_ROW_OWNERS["INV-244"]` entry dropped with its tag, same commit.
  Proof: `tests/test_composition_axes.py`'s new `TestCooccurrenceValueForcingStep`.
- **`q-501` (`beaf953d`) — closed, `Checked by reading on 02.09.`** The eleven historical
  corrections were mostly moot — README had already been rewritten once since the 08-05 draft they
  were written against — so each surviving claim was re-derived fresh against the live repo instead
  of trusted from the old draft. Tonight's narrowing (his word, 2026-09-01 23:15) dropped the
  project-count claim from the page entirely; `tests/test_host_count_agrees.py` rewritten to lock
  that. The July gap resolved for him as a verified fact (the 10 July hole, fixed 07-11, still armed —
  proven by planting a real unregistered surface). First-time-reader pass: six
  independent fresh-context cold reads, converged.
- **`q-803` (`d0bbc72b`) — closed ✅.** The row's own text cited 31 hits from the owner's original
  13:15 sweep; by the time work actually ran the real count had moved to 20 (11+7+2 below), which is
  what got processed — 11
  removed as citations (4 needed a fresh `JOURNAL.md` entry first, since the fact lived nowhere
  else; 7 already had one), 7 left as genuine behavioural-actor sense (no date attached, describing
  a live rule rather than citing a source), 2 exempted (`communicator/references/rule-histories.md`
  is itself the document built to hold this skill's dated citations — stripping there would just
  delete the fact instead of moving it), 1 stripped with no citation possible (no date was ever
  attached to it).
  `tests/test_no_inline_provenance_citation.py` is the new lock.
- **`q-48` (`68539f6e`) — honest partial, stays ⬜.** The pack-side automatic-fetch success-measure
  contract is real: `spec/success-measure-feed.md` (Requirement 318, `INV-324`) plus
  `scripts/check-success-measure-feed.py` and 12 fixture cases. `INV-21`'s `[target]` tag stays live
  on purpose — a host's own fetch tooling and status-view wiring (clauses 9–10) are `~/tlvphotos`'s
  own job, out of this window's reach, named plainly in the row.
- **`q-804` (`f69f0340`, `1c1d0800`) — honest partial, stays 🔄.** Two of the three lane-net arms
  ship for real and red-proven by deed: the config-health primary-tree-holds-main arm (`INV-198`)
  and the adoption-gate vendored-worktree-line arm (`INV-201`) — both `[target]` tags dropped with
  their map entries. The third (`INV-199`'s stale-lane half — a `lane/*` branch or worktree with no
  open queue row) stays unbuilt; the merge-base half of `INV-199` did ship. **This row's first
  worker process died mid-task, silently** — no crash report, just gone from the agent list with
  real, correct, uncommitted work sitting in its worktree. A second worker recovered it: verified
  the dead worker's scripts by hand (fresh scratch repos, planted each violating condition against
  each script directly, watched it red then green) rather than trusting them, then committed as-is.
  A real row-id collision surfaced at merge (`q-804` and the already-landed `q-48` had independently
  picked matrix row `M-621`) — renumbered `q-804`'s three rows to `M-624`/`M-625`/`M-626`.
- **`q-54` — stays ⬜, correctly, and now says why in its own text.** Its remaining field leg needs
  a line added to `~/tlvphotos/.live-spec/profile.md`, which this window cannot write (audit-only on
  other projects). A wish naming exactly this has sat unhandled in that project's own inbox since
  31.08 (`2026-08-31-from-livespec-q54-founding-line.md`) — checked live tonight, still there,
  nothing has changed. live-spec's own profile was considered as a stand-in and rejected: it's the
  pack's own birthplace, never onboarded through the joining walk this row is actually about.
- **`q-163`, `q-385` — deliberately untouched, both correctly.** `q-163`'s host-side leg has the
  same shape as `q-48`'s and `q-54`'s — out of this window's reach, already honestly partial from
  01.09. `q-385` carries its own unfired revisit trigger in its own text ("the first host declaring
  a contract in its card. No host has declared one yet, so this stays queued rather than in hand")
  — building its three arms tonight would have been exactly the un-triggered machinery this pack's
  own standing rule forbids inventing. Flagged to Alexander as a real disagreement with the prompt's
  own scoping before starting; held.

**A real, unrelated side effect caught mid-run.** `q-537`'s own gate (installed skill copies vs.
source) went ⛔ twice tonight — once after `q-436`'s skill edits landed, once after `q-803`'s. Not a
bug in either row: any skill-file edit drifts the installed mirror at `~/.claude/skills` until
`scripts/sync-skills.sh` runs. Ran twice (`f79e74b9`, `1467f480`); `guardrails/check-config-health.sh`
clean after each.

**The quiet-tree suite, run once, alone, after all six rows merged.** First pass: `python3 -m
pytest -q` — 5 failed, 2735 passed, 4 skipped. Three were the `INV-242` warn-then-heal pattern this
note already closes above. The other two were real, both from tonight's own prose, both fixed and
re-verified (`49b4813f`):
- `PRODUCT_SPEC.md`'s bytes-per-criterion hit 185.9 against the recorded 185.8 ratchet bound
  (`INV-264`/`265`) — `q-48`'s new Requirement 318 added criteria whose average byte length pulled
  the whole document's ratio up. Six of its ten criteria tightened, no clause lost; re-measured
  exactly at 185.8.
- `ARCHITECTURE.md` re-grew a register defect the convergence lock (`M-217`) exists to catch: `q-48`
  and `q-804`'s new prose cited the plan by a bare, capitalized word `spec-style-lint.py` reads as a
  shout. Reworded to cite `PLAN.md`'s own row by number, matching every other citation
  on the page. Fixing that surfaced a second, real finding: `q-804`'s own new prose at one line
  restated a phrase its own pin list two lines away already carried verbatim — one redundant pair
  over the page's 15-pair floor, confirmed against the pre-session baseline commit (`534cb16b`, via
  a scratch worktree: 15 open there, 16 after tonight, 15 again once the restatement pointed at the
  pin instead of repeating it).
- Both `PRODUCT_SPEC.index.md` and `ARCHITECTURE.index.md` regenerated after each fix; both came
  back byte-identical to what was already committed — neither trim touched a requirement or node id.

**A second full-suite run is still owed after this commit lands**, to confirm the fixes above hold
together on a genuinely quiet tree with nothing else mid-flight. Not run yet as this note is
written; whoever reads this next should confirm `python3 -m pytest -q` is clean before trusting the
range green, per this project's own rule against reporting a red suite as basically done.

**No new queue row opened for anything found tonight.** Every real finding (the size-ratchet trim,
the shout/redundancy fix, the `q-537` syncs, the `M-621` renumber) was a direct repair of tonight's
own work, already folded into the row it belongs to above.

**Saved for a later session:** `.live-spec/next-phase-prompt-turnkey-productization.md`
(`b29231a3`) — his own words, the next LiveSpec phase (a product contract for a Director-led turnkey
workflow, reviewed by product-prover before any code). Explicitly deferred: work through it only
after this note's own suite is confirmed green and either a fresh session picks it up on his word, or
morning arrives with everything green and no further word from him.

**Update, same night, 02:30–03:10 — his live word to cut every invented-number ceiling, and what
that took.** Said live in chat, filed as a queued row after the fact: "все цифры с потолка уходят. все
инструменты их обслуживающие тоже уходят... больше не значит хуже. больше значит надо измерить и
поговорить и решить это ок или нет." Filed as `q-805` and closed ✅ (`51d2d402`) — full detail in
`JOURNAL.md`'s matching entry. Two rounds of fresh-context hostile review followed, since the push
gate demands a review no older than the spec's own last change and `q-805` changed it twice more
after the first overnight review:

- Round 1 (`docs/prover/2026-09-02-overnight-run-hostile-review.md`) found two blocking defects in
  the original 8-row range (a heal-phrase format miss, a prematurely-dropped `[target]` tag) and
  three smaller ones — all fixed (`bf426ec4`, `4805cec5`).
- `q-805` landed, plus two skill-review records covering nine skills' worth of accumulated
  unreviewed changes — the gate checks against `origin/main`, the last real push, so it covered
  weeks of debt from before this session as well as tonight's own work. A pin-drift fix and a
  compaction-freeze re-lock followed.
- Round 2 (`docs/prover/2026-09-02-q805-and-followups-review.md`) reviewed everything since round 1.
  One blocking finding (this same heal-phrase class, third time — `q-805`'s own landing commit) and
  five real, smaller ones: the host kit repaired the push-gate wiring but left an adopted host's
  leftover ratchet-lock test and seeded cap file in place (fixed, with two new red-proven tests);
  the kept `check-language-rules.py` reasonless-rule cap had drifted stale by one and was re-seeded
  from a live count (4→3); one dangling reference to the renamed installer in a worked-example doc;
  two skill-review records with real coverage-claim errors (a missed third file, a wrong
  cross-reference) corrected in place; and `M-327`'s own matrix row claimed a repair behavior no
  spec criterion actually carried — widened (`Requirement 268` gained criterion 7).

This commit's own message carries the third heal phrase. A third full-suite run is still owed
before this range can be trusted green.

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
into the background, and the suite runs 18 to 24 minutes. A worker that starts it stalls and then
returns an unfinished report as final, or worse, reports a stale background run against a worktree
the orchestrator has already reclaimed — happened twice tonight, both self-diagnosed correctly by
the worker rather than acted on. A brief names the exact test files that finish in seconds. The
orchestrator runs one clean full suite at the end of a pass with no worker active. A run taken
while workers write the tree reds on files being written, and its reds carry no verdict.

**Tonight's addition: a worker process can die silently, mid-task, with no crash report** — just
gone from the agent list, its real uncommitted work still sitting safe on disk in its own worktree.
Happened once tonight (`q-804`). The recovery is not to redo the work: inspect `git status`/`git
diff` in the worktree, verify what's there for real (don't trust it because it looks done), finish
whatever's missing, and commit. Never run a destructive git command on a dead worker's worktree to
"clean up" — that would destroy real, unrecovered work.

## Prompt for the next session

**Everything below this line was written 2026-09-02 01:25, right after tonight's overnight run
(`534cb16b..49b4813f`) moved six of the prompt's own eight rows (three closed, two honest partials,
one returned to the queue) and fixed the two prose regressions the quiet-tree suite caught. A second
full-suite run and the push are still owed as this is written — check `bash scripts/state-probe.sh`
and this file's own LIVE STATE section above first; if both already show green and pushed, this
prompt is stale and you're likely looking at a later state than the one this was written against.**

Do not ask Alexander anything before doing the work below unless it's genuinely his — a taste call,
a policy question, or an act irreversible outside git. His standing word already covers pushing
tonight's range once the suite is confirmed green.

**If the suite and push aren't done yet:** finish that first — `python3 -m pytest -q` alone on a
quiet tree, `0 failed, 0 errors`, then push, per the LIVE STATE section above.

**If everything above is already green and pushed**, the next real work is the saved productization
phase: `.live-spec/next-phase-prompt-turnkey-productization.md`. Read it whole before starting — it
carries its own precondition (verify the current PLAN.md's state against the real repo, nothing
taken on faith) and its own five serial CI-green packages. Do not start it opportunistically; it
was deliberately deferred to either his own word or a morning check with nothing further from him.

**Still open on the board, each correctly left that way — do not start any of these without a real
reason to revisit:**
- `q-166` — a taste call: its own acceptance names his eye over one real stretch of work as the
  check, no command decides it.
- `plan-14` — real install-infrastructure work spanning the pack's install/adopt walk; a wrong
  wiring choice here is hard to unwind once every future adoption depends on it.
- `plan-9` — held by his own prior word.
- `q-163`, `q-48`, `q-54` — each has a real remaining leg that only a `~/tlvphotos` session can
  close (this window is read-only there beyond one inbox wish).
- `q-385` — its own revisit trigger (a host declaring its first real contract) hasn't fired.

**Method, proven again tonight, unchanged:** up to three parallel worktree lanes (`Agent` tool),
each briefed with the row's own `PLAN.md` text pasted verbatim, the worker-restore rule copied
verbatim, and told explicitly not to rebase/merge/push — the orchestrator integrates. Merge one row
at a time, rebase onto main's tip first, re-verify from the merged tree, then clean up the lane.
Watch for two real collision classes that showed up tonight even with worktree isolation: two lanes
independently picking the same next-free matrix row id (check `grep -rhoE "^\| M-[0-9]+"
matrix/*.md` before trusting a new row number), and a lane forked before an earlier lane's own
landing carrying a now-stale copy of a shared map entry (`tests/test_traceability.py`'s
`TARGET_ROW_OWNERS`, most often) through its own rebase.

Report in the Канон format his own boot file (`~/.claude/CLAUDE.md`) specifies —
`bash scripts/state-probe.sh`'s own printed plan, never a hand-typed summary — after every row
that lands, not only at the end.
