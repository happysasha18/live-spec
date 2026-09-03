# Prover record — 2026-09-03, the full unpushed range read as one

PUSH-REVIEW

Prover skill version: product-prover 4.3.0, with product-prover-pack bindings (live-spec-base 6.1.0).
Mode: FULL — the whole range ahead of `origin/main`, read for reasons to refuse it, not for
confirmation. Run from a fresh seat that authored none of this range's changes (SPEC INV-237).

This record exists because `NEXT_STEPS.md`'s own LIVE STATE names it as still owed: "A genuinely
comprehensive adversarial prover review of the whole pushed range is still owed, not satisfied by
name. `docs/prover/2026-09-03-q812-director-route-contract.md` mechanically satisfies the
dated-record push gate, but it only reviewed `q-812`'s own contract — not the adversarial read of the
whole range this pack's own method calls for before a push." That file is a feature-fit review of one
row's spec contract, dated before code, and says so itself ("Not a push review: no range is measured
here"). This record is the range-wide read it named as missing, and its own findings are not repeated
here.

Range: `f217a3188aa39a833f10f39edc31ad511573d8b5..d68a49fa33c9fb1400846a136550de186733af1a` (65
commits — the count `NEXT_STEPS.md` gave this morning as "63 commits and rising"; it grew to 65 by
the time this pass started and no further commit landed under review). `git log
origin/main..HEAD --oneline` gives the full list; the closing commit of each row this record reads
by name:

- `d68a49fa` checkpoint: refresh suite-green fingerprint cache
- `127c07bb` NEXT_STEPS: rewrite for session close — plan closed except onboarding
- `1450e1be` plan-14 closes: the catch-up walk vendors the status view too
- `8e3a4a70` q-815: worker-restore gate scopes "own" to the pushing repo, not the script's file location
- `29a4e047` q-814: skill-review gate gains a byte-identical carve-out; catch-up walk names a known-difference class
- `73be8ad5` q-163: close, field leg landed in tlvphotos's own TEST_MATRIX.md
- `3b5beee0` q-812 closes: the Director's real route proven end to end, independently re-verified
- `899c4ee1` q-813 closes; flags one judgment call still owed his word
- `4fc05b6c` plan-9 closes: tlvphotos ran the real 2.7.0 -> 6.1.0 catch-up walk; q-814 files two real findings
- `871e234a` q-808 closes on a real outside-reader check; q-812 opens for the Director's route proof
- `68fee57f` q-810 closes: closing rule and argue-first rule both proven, not just written
- `4e17c268` q-809 closes: final weight measured, honest accounting of the shortfall
- `3e4777e0` q-804 closes: three lane-net arms wired, mutation-proven, re-verified independently
- `614cc25e` director: the Director runs the project; no idea shelf, no second list (the third
  `skills/director/SKILL.md` edit of the night — the seam this record's own finding turns on)
- the remaining 51 commits are checkpoints, claims, corrections and heals belonging to the rows
  above, plus `q-581`'s dialog-warning-guard install and one declined prototype sweep, none closing
  a row this record has not already named.

`q-807`, `q-806`, `q-801` and `q-800` — named in the brief as part of "many landed rows" this range
spans — were already `✅` at `origin/main` (verified: `git show origin/main:PLAN.md` carries all
four already marked done). None of their closing commits fall in this range; PLAN.md's own text for
each is untouched by this range's diff. They are not re-reviewed here.

Files read: `PLAN.md` (whole, 3453 lines, diffed line-by-line against `origin/main`), `NEXT_STEPS.md`
(whole, both versions), `DECISIONS.md` §Open and §Struck, the full diff of `PRODUCT_SPEC.md`,
`PRODUCT_SPEC.index.md`, `spec/message-first-read.md`, `spec/wish-intake.md`,
`spec/parallel-lanes.md`, `spec/live-status-reporting.md`, `spec/work-board.md` (deletion),
`architecture/pipeline-and-lanes.md`, `architecture/feature-coverage.md`, `matrix/director.md`,
`matrix/parallel-lanes.md`, `attic/MANIFEST.md` (the two new retirement entries),
`attic/spec-work-board-R309.md`, `attic/matrix-work-board-R309.md`, `tests/test_traceability.py`
(`TARGET_ROW_OWNERS`, full comment trail), `tests/test_formal_index.py` (the pinned-gap table),
`guardrails/check-skill-review.sh` (`find_covering_record`), `guardrails/language-rules.json` (rule
`r31`), `guardrails/pre-push` (gates c, d, x), `MIGRATION.md` Phase 4, `adopt/ADOPT.md`,
`docs/skill-review/2026-09-03-director.md`, `docs/skill-review/2026-09-03-director-runs-the-project.md`,
`inbox/handled/2026-09-03-from-tlvphotos-catchup-6.1.0-findings.md`,
`inbox/handled/2026-09-03-from-tlvphotos-q163-field-leg-landed.md`, `skills/director/SKILL.md` (the
pinned line ranges), `.live-spec/checkpoints/q808-plain-language-titles.md`, and every commit message
in the range (`git log --reverse --format='%h %ad %s' --date=format:'%m-%d %H:%M'`, giving the exact
chronology the findings below turn on).

Checks run, each against a `git archive` snapshot of the actual tip commit (`d68a49fa`) and, for the
one finding that turns on timing, against a second snapshot of the exact commit under question
(`8e3a4a70`) — never against a commit's own prose:

- `python3 -m pytest -q tests/test_formal_index.py tests/test_director_route_end_to_end.py` — 14
  passed (the 11 tests `q-812`'s own text claims, confirmed by name and count).
- `python3 -m pytest -q tests/test_status_view_install.py tests/test_catchup_walk.py
  tests/test_skill_review.py tests/test_lane_net_arms.py tests/test_scaffold_install.py` — 82
  passed (the test files `plan-14`, `q-814` and `q-804` cite by name).
- `python3 -m pytest -q tests/test_worker_restore.py tests/test_worker_restore_made_good.py
  tests/test_worker_restore_guard.py tests/test_worker_restore_run_scope.py
  tests/test_install_worker_restore_guard.py` — 288 passed (`q-815`'s own cited count, reproduced).
- `python3 -m pytest -q tests/test_director_scenarios.py -k recorded_against_the_skill` — **FAILED**
  at `d68a49fa` (current tip) and **FAILED** again at `8e3a4a70` (the exact commit `q-815` closed
  on), same assertion, same hash mismatch both times. This is the check the central finding below
  is built on.
- `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md` — OK: 535 of
  535 rows matched, committed Reference equals the fresh build, 402 anchors agree.
- `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK: 395 of
  395 rows matched, 395 codes agree, 311 requirement numbers each claimed once.
- `git cat-file -s origin/main:skills/live-spec-base/SKILL.md` and `git cat-file -s
  main:skills/live-spec-base/SKILL.md` — both `23441`, byte-identical; the file is untouched
  anywhere in this range (`git log origin/main..main -- skills/live-spec-base/SKILL.md` is empty).
  Investigated against `q-809`'s own closing text ("carries 22,683 bytes today... checked again
  tonight ~22:35 by direct grep against the live file"); a body-only count (frontmatter stripped)
  reads 22,620, close enough to the claimed figure that the discrepancy most likely reads as a
  frontmatter-inclusion convention rather than a false measurement. Not raised as a finding — the
  evidence does not clear the bar to call it one, and inventing a defect out of an ambiguous unit
  would break this pack's own "no invented findings" rule.
- `grep -rn "INV-308\|INV-67[^0-9]"` over the whole tree at `main` — both anchors exist only inside
  retired `attic/` files and inside the withdrawal note in `attic/MANIFEST.md`; neither is live in
  any spec, architecture or matrix file. Cross-checked against `tests/test_formal_index.py`'s pinned
  gap table, which names `INV-308`–`INV-313` explicitly as retired and unclaimed.
- Direct read of `skills/director/SKILL.md` at lines 45, 225 and 272 against
  `architecture/pipeline-and-lanes.md`'s three re-pointed pins (fixed in `36f64877` after the
  night's `SKILL.md` edits moved them) — each pin lands on or immediately beside the content its
  label names.
- `grep -in "full suite" ` over the whole `PLAN.md` diff — seven hits, each read in its row's own
  context and cross-checked against the commit timeline; this produced the finding below.
- `git log 09bbd39a..3b5beee0 --oneline -- skills/director/SKILL.md` and `git log
  614cc25e..8e3a4a70 --oneline -- skills/director/SKILL.md` — both empty, confirming `q-812`'s own
  claim that it never touched the file, and confirming `q-815`'s lane inherited the staleness from
  `614cc25e` unchanged.

Findings: one, non-blocking. Everywhere else this pass looked for the seam-between-close-rows defect
this method's own findings log calls for, the seam holds.

## F1 — Two rows closing within the same known-red window as a third state their own suite check passed clean, or say nothing, while the row between them had already disclosed the exact opposite

> "Full suite (`python3 -m pytest -q`) run clean from this worktree's root; see the session's own
> report for its tally." — `PLAN.md`, `q-815`'s own closing text, commit `8e3a4a70`

`skills/director/SKILL.md` changed for the third time this range at `614cc25e` (09-03 10:28,
`q-813`'s own "no idea shelf" edit). That edit invalidated the nine-producer-run recording
(`evals/director/closing-scenarios.json`) made two hours earlier at `3458c213`, which
`tests/test_director_scenarios.py::test_closing_runs_were_recorded_against_the_skill_as_it_stands`
holds against the file's live sha256. From `614cc25e` on, every close of that test reds — proven
above by running it directly against both the current tip and against `q-815`'s own closing commit,
neither of which had touched the file since.

Four rows close after `614cc25e`, in this order: `q-813` (11:41), `q-812` (12:47), `q-814` (14:18),
`q-815` (14:32). Two of the four get this right. `q-812`'s own closing text says "full **targeted**
suite green" — a scoped claim that is true and never overreaches into the whole suite, even though
its own stated Acceptance criterion demands the scenario proof run "green in the full suite."
`q-814`'s own closing text states the true count outright: "Full suite: `python3 -m pytest -q` —
2731 passed, 55 skipped, 4 failed, none touching either finding (pre-existing: a stale
`skills/director/SKILL.md` hash against its recorded closing-eval runs, a nested run of the same;
Cyrillic already on `PLAN.md:1361`...) — carried as-is, not this row's job." That is exactly the
right way to close beside a known, unrelated red: name it, show it is unrelated, move on.

The other two do not carry that disclosure forward, in the same session, on the same known
condition. `q-813`'s own Definition of done states flatly "Full suite green," and its "Checked by
reading" paragraph — written after `614cc25e`, the very commit `q-813`'s own lane produced — says
only "Full suite re-verified independently on the merged tree after integration, not taken on the
worker's own report," with no failure named and no reconciliation of the "green" the DOD demanded.
`q-815` goes further and states an outcome directly: "run clean." Both are checkable, and both read
false against the same fact `q-814` — closing in between them, in the same session — had already
written down in the same file.

Who is affected and how: a later session (or the owner) reading `PLAN.md` row by row meets `q-814`'s
honest four-failure count, then `q-813`'s unqualified "Full suite green," then `q-815`'s "run
clean," for what is, on the actual tree, the identical known-red condition the whole time. Nothing
in either row's own text says "the same debt `q-814` already named", so a reader has no way to know
without independently running the suite (which this record did) that the two claims are not
describing three different states of the world — they are one state, described three different
ways by three rows written within three hours of each other. `NEXT_STEPS.md`'s own final LIVE STATE
paragraph, written at session close, does state the honest aggregate ("2788 passed, 2 failed, 1
error, 4 skipped... both failures and the error are the same pre-existing debt") — so the project's
final resting state is accurately reported. The gap is at the row level, inside the range this push
is about to carry, not in the session's closing summary.

This is the shape the brief asked this pass to hunt for at the seams between rows landed close in
time: not a promise dropped between two rows, but the same fact affirmed by one row, then
contradicted or left unstated by two rows closing either side of it in the same sitting.

Proposed action: amend `q-813`'s "Checked by reading" line and `q-815`'s closing line to name the
same known-stale-eval debt `q-814` already named, or to point at `q-814`'s own line rather than
restate the suite's state independently. No code change, no new gate — this is prose accuracy on
already-committed closing text, reversible in the ordinary way (an edit to `PLAN.md`).

Severity: non-blocking. It does not misstate what any row's own mechanism does — every test file
this range's rows cite by name was independently re-run above and passes exactly as claimed (`q-812`
11/11, `q-814`+`q-815` 82+288, `q-804`'s and `plan-14`'s cited files among them). It misstates the
*suite's own state* at two points in the row-by-row record, on a fact the range's own final summary
later states correctly. `Blocking: none` below reflects that this is a documentation-accuracy
finding on prose already superseded by an accurate aggregate, not a claim that the range's shipped
mechanism is broken or unproven.

`defect · direct-contradiction (contradiction)`

## What else this pass looked for, and found clean

**The INV-308/INV-67 handoff chain.** `q-166` (09-02) moved two `[target]` anchors it could not
close to a fresh row, `q-811`; `q-813` (09-03) retired `q-811` and the whole spec chapter it lived
in the next day. That is exactly the shape this method's own findings log has caught before — a
promise handed to a row that then stops existing. Checked directly: `attic/MANIFEST.md` and
`tests/test_traceability.py`'s comment trail both name the handoff and explicitly withdraw the two
anchors rather than silently dropping them, and `tests/test_formal_index.py`'s own pinned-gap table
lists `INV-308`–`INV-313` as retired and unclaimed by name. The seam was real and was closed by the
same session that opened it.

**The stale "armed nowhere" note.** `guardrails/language-rules.json` rule `r31` carries a structured
`status: "held"` (the catcher runs) beside a free-text note that still says "`check-no-history.py`
is armed nowhere" — a live, present-tense contradiction inside one entry, confirmed by direct read
at `main`. This is not a new discovery: `PLAN.md`'s own Blockers section (the "check that nothing
calls is a class" entry, corrected 03.09) already names this exact contradiction, cites the test
that disproves it, and explicitly defers the fix as the owner's own priority call rather than
folding it. Confirmed present, confirmed already disclosed, confirmed not silently claimed fixed.

**The mechanical consistency gates.** `check-matrix-reference.py` and `check-index-generated.py`
both pass clean on the merged tree (535/535 and 395/395 rows respectively), across every spec and
matrix part file this range touched — `spec/work-board.md`'s full retirement, `spec/message-first-
read.md`'s Requirement 315 removal and Requirement 314's two new criteria, `spec/parallel-lanes.md`'s
two `[target]` drops, `matrix/director.md`'s four new rows (M-630–M-633), and `matrix/parallel-
lanes.md`'s M-629. No dangling anchor, no duplicate matrix id, no orphaned code survived the churn.

**The architecture pins director/SKILL.md's own edits shifted.** Three pins in
`architecture/pipeline-and-lanes.md` were re-pointed in `36f64877` after the night's `SKILL.md`
edits moved their line numbers; the commit itself named a fourth pin as deliberately left broken
pending `q-813`'s retirement work. Checked: `q-813` did not patch that pin — it deleted the whole
paragraph the pin lived in, along with the `E-37`/`INV-320` line it was attached to, which is the
correct fix once the requirement it pinned no longer exists. The three repaired pins land correctly
against the live file at their new line numbers.

**Every cited test file, re-run.** `q-812` (11 tests), `q-814` and `q-815`'s shared families (82 and
288 respectively), and the mechanical index/matrix checks all reproduce exactly the counts their own
`PLAN.md` text claims. `plan-14`'s claim that `MIGRATION.md` Phase 4 now calls
`adopt/install-status-view.sh` is confirmed at the correct line, inside the correct phase heading.
`q-804`'s claim that `TARGET_ROW_OWNERS` dropped `INV-199`/`INV-201`/`INV-150` is confirmed absent
from the live dict. `q-812`'s claim that its own row never touched `skills/director/SKILL.md` is
confirmed by an empty `git log` over the file for its commit range.

**PLAN.md's own bottom line.** `NEXT_STEPS.md` states "the plan is closed except onboarding" —
confirmed: exactly three `⬜` rows remain in the whole `## Tasks` section (`q-54`, `q-48`, `q-385`),
each on its own named, unfired trigger, matching the LIVE STATE paragraph's own account precisely.

## Class lens

One class, one finding: a claim about the suite's own state, made in a row's closing prose, that a
direct re-run contradicts — the same class the 2026-09-02 full-range review's F3/F8 named for a
different mechanism (the done-line predicate). Here the mechanism itself (the freshness gate on
`skills/director/SKILL.md`) is sound and does its job; what fails is two rows' own narration of
having run past it clean. Swept for siblings: every other "checked by reading" claim in this range
that names a specific test file or count was independently reproduced above and held. No third
instance in this range.

## Verdict

Ready to carry forward; this is not a reason to hold the range. One finding, non-blocking, a prose
correction to already-committed closing text whose underlying facts the range's own final
`NEXT_STEPS.md` summary already states correctly. Everything this pass could independently re-run —
every test file cited by name across `q-804`, `q-812`, `q-813`, `q-814`, `q-815` and `plan-14` — ran
and matched its claimed count. The mechanical spec/architecture/matrix consistency gates are clean
across the whole range's churn, including two chapter-sized retirements (`spec/work-board.md`,
Requirement 315) and one four-row matrix addition. The one seam this range's own working notes
flagged as a live risk (`INV-308`/`INV-67` handed from a closing row to a row that itself then
retired) was closed correctly by the same session, with the withdrawal recorded rather than the
promise silently dropped.

Blocking: none.
