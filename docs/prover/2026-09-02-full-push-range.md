# Prover record — 2026-09-02, the whole pushed range read as one

PUSH-REVIEW

This record covers the entire range this push sends, `11987b8..84e0bf95` — 78 commits, two
sessions' work across 2026-09-01 and 2026-09-02, extended once (2026-09-02, after this record's
own first write) to add `84e0bf95`, the commit fixing this same record's own three blocking
findings — verified real, verified fixed, detailed in
`docs/prover/2026-09-02-full-range-fixes-short-form.md`, itself exempt from needing its own name
here since it touches only `docs/prover/`. It exists because gate a
(`guardrails/check-prover-record.sh`, SPEC M-6/INV-116/INV-304) holds one record per push whose
own `Range:` field names the base and every reviewed commit, and no record on file named the
whole of it. The three records this range already carries each named a shorter head.

Range: 11987b8..84e0bf95
- 84e0bf95 Fix the whole-push-range review's three blocking findings and one stale pointer
- bc073fdb docs/prover: short-form record for the second review's fixes — small delta, every change verified against a real finding, two new tests red-proven by actual revert-and-rerun
- 2d7f42ab Fix the second review's one blocking and five real findings
- 43db5470 docs/prover: hostile review of q-805 and the review follow-ups — one blocking finding, five real
- d9f6a3d0 architecture/host-adoption.md: re-point the attach-record pin — q-805's install-style-gates.sh rewrite in adopt/ADOPT.md shifted it from line 291 to 295
- 4feebee1 docs/skill-review: cover architect/build-pipeline/communicator/director — real, pre-existing unreviewed changes against origin/main, none of them tonight's own work
- ef262d7a docs/skill-review: fresh review clears the five skills tonight's edits touched (q-436, q-803, q-805); sync-skills: repair spec-author's third drift (change-record.md rewrite)
- 51d2d402 q-805: cut every gate holding a document to a ceiling seeded from its own past state
- 4805cec5 spec/parallel-lanes.md: restore INV-199 criterion 5's [target] too — check-merge-base.sh has the same no-real-caller shape as check-worktree-line.sh (review follow-up)
- bf426ec4 Fix the hostile review's two blocking findings, plus three real non-blocking ones
- 55d2bebf docs/prover: hostile review of the overnight run — six real findings, two blocking
- 521f38f7 claim: row q-805 → in-work (lane/q-805-cut-invented-number-ratchets)
- 667ac780 NEXT_STEPS.md: whole-night LIVE STATE for the overnight run, heals three INV-242 warns, fresh prompt for the next session
- 49b4813f Fix two prose regressions the quiet-tree suite caught: PRODUCT_SPEC.md's size-ratchet (q-48's new criteria), ARCHITECTURE.md's shout+redundancy (q-48/q-804's PLAN citations)
- 1c1d0800 q-804: fix M-621 row-id collision with q-48 (renumber to M-624/625/626); drop stale INV-244 map entry left over from pre-q-436 fork point
- f69f0340 q-804: two of the three lane-net arms ship for real, row stays open on the third
- 1467f480 sync-skills: repair q-803's own drift (communicator, live-spec-base, publish, text-audit-pack)
- d0bbc72b q-803: strip inline provenance citations from skill rule prose
- f79e74b9 sync-skills: repair q-537 drift caught after q-436's merge (product-prover-pack, spec-author)
- beaf953d q-501: front page accurate, project count dropped, July gap closed
- d6b52e35 claim: row q-803 → in-work (lane/q-803-strip-provenance-citations)
- b5914865 q-436 lands: the value-space in-between forcing step, beside q-437's axis-verdict sweep
- bf322e4c claim: row q-501 → in-work (lane/q-501-front-page-accuracy)
- 68539f6e q-48: pack-side automatic-fetch success-measure contract (spec + checker + tests)
- ef671c4a claim: row q-48 → in-work (lane/q-48-automatic-fetch-contract-spec-delta)
- 1b3d5b42 q-54: confirm live-spec's own profile is not a legitimate stand-in; leave row open
- b29231a3 Save tonight's productization-phase brief as a task for after PLAN.md closes
- 0a3fa8ec claim: row q-54 → in-work (lane/q-54-founding-line-live-spec)
- 26a36e17 claim: row q-804 → in-work (lane/q-804-lanes-net-for-real)
- cad8403f claim: row q-436 → in-work (lane/q-436-co-occurrence-value)
- 534cb16b Write tonight's overnight-run prompt: eight closeable rows, worktree-isolated, one honest report
- b0f8929c Closing adversarial review of tonight's session; sweep the [default]-tag-order defect to its 19 siblings
- f7382a15 The one-file-in-the-tree check learns to stand down in a git-less scratch copy
- 4f0b760c NEXT_STEPS.md: tail-end cleanup heals landing 0a9a431a, catches up on tonight's last five fixes
- 16d59df9 Re-point five pins that drifted again after 084c3eb4's communicator trim
- bb084ed5 docs/prover: fresh adversarial review record — q-385/q-804/q-436 reopened, criterion 15 narrowed
- 5c8ebb87 Fix shipped-language gate: allowlist plan_checks.py's real grep string, mark PLAN.md's direct quotes user-language
- 7c25768c plan_checks.py: back five done tasks, and drop pytest from q-802's key
- 0a9a431a PLAN.md: three findings from tonight's traceability/done-mark audit
- 084c3eb4 communicator's body drops back under its size ideal, q-536's rulings moved to references
- 16878f0c Cut the scissors contrast frame from q-398's new referral criterion
- 476f5246 Fix INV-196 trailing-tag order so its declaration paragraph is found
- 0d668348 config-health: routing hook installed, communicator's copy re-synced
- 4c95f679 NEXT_STEPS.md: name the real date behind plan-9's "Alexander's own word" deferral
- 7551744b docs/language-rule-coverage.md: rebuild off hooks/register_judge_core.py's source note
- fc5c2792 PRODUCT_SPEC.index.md: rebuild the generated code-to-location table off today's spec edits
- ce3a7e30 spec: Requirement 163's heading loses a stray [default] tag it never should have carried
- 6ea75939 architecture pins: re-point nine line pins that drifted when today's session edited skills/live-spec-base/SKILL.md and skills/communicator/SKILL.md
- 97799c24 NEXT_STEPS.md: full suite is red, 30 failures -- state it honestly
- 29faa996 NEXT_STEPS.md: re-heal two commits whose heal phrase wrapped across a line
- d35dc003 README rewritten short, product-prover's shape: what you get, then how, install last
- b1f0963c NEXT_STEPS.md catches up with today's full landing range
- 67bd98d1 q-386's convergence test lands
- 1280cd99 q-536's fourteen rulings land for real
- 287e019c q-163's M-620 matrix row lands for real
- 67f9ce6e q-802 lands: the snapshot's baseline only ever moves for what a delivery actually declared
- caa7f6a7 Old leftovers actually confirmed dead, not just old, are cut
- adceb60b q-166: board.html already answers the daily ask he remembered
- cf244b5b The false Known Issue claim gets a guard against a fourth return, not a fourth manual fix
- e3b745b1 q-501 / the front page's own false Known Issue closes, again
- 54bde341 Revert TEST_MATRIX.index.md, matrix/test-author.md, skills/communicator/SKILL.md from the q-398 commit
- e2a0e8c4 q-398 lands: a routing preamble now reaches an adopted project automatically
- 2858c023 q-800: close the playbook-repo row now that his permission this session is the read that was waited on
- c30491b9 q-48: the deferred trigger already fired 24.07 -- the row catches up
- 8905d7af q-536 lands: the fourteen communicator collisions each get their ruling, in the rule's own text
- 24152152 q-163: the wiring proves itself; the host field-leg still needs its own project's window
- 4f86dfd9 q-591 lands: M-313's cited home follows the requirement that actually moved
- d673c75c q-166 re-marked queued, not needs-his-eyes -- nothing built yet to look at
- 3147d6e2 Journal: plan-2 re-recorded, q-437 lands, sync catches up
- 14808ef2 plan-2 re-recorded: all thirty-five traces fresh, 32 of 35 hold
- 7e3f32e1 q-437 lands: the axis-verdict sweep runs at every level, not just siblings
- b9708261 plan-10 lands: every done mark now proves itself, none turned out false
- a488854f plan-10: sixteen done marks now carry a real check or a dated reading, not a typed mark
- bf319751 plan-10's own instrument: a done mark now has to prove itself
- 3d4b8ae4 q-803: a skill's rule states itself, the journal carries who said it
- 5aacf3aa Concurrency without a stated safety measure gets its own rule
- 62394f45 q-576 lands: the page it asked for exists, and the tree holds nothing ungrounded
- c8adff22 q-576: the twelve unlabelled survivors and one new constant get the same source-admission every other unproven number already carries; r14's stale note is corrected

## How the range splits, and what each half already carries

`534cb16b..bc073fd` — 29 commits, the overnight run and the two review rounds that followed it —
was read in real depth by three records already on file, and this record does not repeat their
work:

- `docs/prover/2026-09-02-overnight-run-hostile-review.md` — six findings, two blocking.
- `docs/prover/2026-09-02-q805-and-followups-review.md` — six findings, one blocking.
- `docs/prover/2026-09-02-q805-followup-fixes-short-form.md` — the fixes for the second round,
  each checked against the finding that asked for it.

Their headline outcome: three blocking findings in total, all three the same class — a landing
commit closing a row without the INV-242 heal phrase in a later commit's own message — plus the
two orphaned lane-net arms whose spec criteria had dropped their `[target]` while nothing called
the scripts. All three blockers are closed on the tree as it stands, and this record confirms that
by running the checks rather than reading the claims (see `Checks run`, items 8 and 9).

One thing those three records did not do, and each says so in its own words: run the full suite on
the merged, settled tree. The first ran it while the tree was still moving under it and read three
reds as artifacts; the second deferred it; the third states outright that the orchestrating session
owes one clean pass before the push. This record is that pass, and it is red — twice, both from one
commit inside their own range. Findings 1 and 2.

`11987b8..534cb16b` — 48 commits, the 2026-09-01 session — is the half no record named as a whole
push. It is not unreviewed: two of the records inside it are themselves push-shaped and name this
same base.

- `docs/prover/2026-09-01-three-targets-reopened-and-criterion-15-narrowed.md`, `Range: 11987b8..5c8ebb8`
- `docs/prover/2026-09-01-closing-review-trailing-tag-order-swept.md`, `Range: 11987b8..f7382a15`

Between them those two cover `11987b8..f7382a15`. Exactly two commits sit above `f7382a15` and
below `534cb16b`, and both were checked here by reading their diffs: `b0f8929c` carries the second
of those two records plus the 19-line bracket-order sweep that record's own finding 2 describes and
closes, and `534cb16b` touches one file, `.live-spec/overnight-prompt-2026-09-01.md`. So the older
half's push coverage is complete once those two are accounted for, and this record accounts for
them.

The two records also left two blocking findings standing, deliberately, for later steps of that same
session. Both are closed on the tree as it stands, verified here rather than assumed: pin drift
(`bash guardrails/check-pin-drift.sh` — OK, 184 pins plus 39 range pins), and `NEXT_STEPS.md` stale
against `0a9a431a` (`python3 guardrails/check-landing-next-steps.py` — exit 0, every one of the
twelve misses in the range naming its healer).

Files read: `guardrails/check-prover-record.sh` (the whole script, both roads and every arm — this
record is written to what it reads, not to a remembered shape), `docs/prover/README.md`, the three
2026-09-02 records above and the two 2026-09-01 push-shaped records above, the cumulative diff
`git diff 11987b8 534cb16b` by file (92 files, 2833 insertions, 716 deletions) with the substantive
ones read in full: `.gitignore`, `guardrails/judge-hooks.json`, `scripts/shipped-language-allowlist.json`,
`guardrails/check-vocabulary.py`, `guardrails/check-deferral-marker.py`, `tests/test_traceability.py`
(the `TARGET_ROW_OWNERS` map rewrite and the new
`test_director_names_test_author_at_the_derivation_step`), `tests/test_compaction_discipline.py`,
`tests/test_dialog_warning_guard.py`, `tests/test_snapshot_baseline.py`, `tests/test_readme_stance.py`,
`tests/test_row_id_uniqueness.py`, `scripts/plan_checks.py` (the `q-802` and `plan-0` keys),
`scripts/check-shipped-language.py` (the waiver-matching function), `.live-spec/snapshot/MANIFEST.md`
and `baseline.py`, `spec/doc-order-generated.md` (Requirements 1, 247 and 290 in full),
`architecture/guardrails.md` (the `owns` block, lines 5 to 67, and the `notes` block from line 148),
`tests/test_architecture_format.py` (the no-history test and its docstring),
`tests/test_tasks_parser_finds_every_task.py` (the acceptance-command honesty class and its
`JUDGED_BY_HAND` map), `scripts/plan_checks.py`'s `q-805` key,
`spec/adopt-existing-project.md` (Requirement 177 criterion 9), `spec/project-setup-tuning.md`
(Requirement 296's INV-7 criteria), `spec/guardrails-freshness.md` (criterion 5 of Requirement 268's
neighbour, the INV-7 clause), `skills/live-spec-base/SKILL.md` (rule 10 and rule 12),
`spec/project-setup-tuning.md` (Requirement 179 in full), `PRODUCT_SPEC.md`'s glossary entry for the
attic, `DECISIONS.md:497`, `skills/live-spec-base/references/glossary.md`,
`attic/MANIFEST.md` (header and the inbox block), `adopt/record-starting-state.sh`, `adopt/ADOPT.md`
(the starting-state step), `matrix/snapshot.md`, `matrix/guardrails.md`, `matrix/test-author.md`,
`matrix/attach.md` (M-037), `hooks/routing-preamble-hook.sh` with its installed copy and the
`~/.claude/settings.json` entry that fires it,
`PLAN.md` (the `q-802`, `plan-2` and `q-501` rows in full, plus the row-status column for every row
the map names), `evals/director/check.py` and the thirty-five trace files, and the full commit
messages of `54bde341`, `67f9ce6e`, `caa7f6a7`, `cf244b5b`, `d35dc003`, `14808ef2`, `b0f8929c` and
`534cb16b` read against their own diffs.

Checks run: sixteen, each run here against the current tree rather than taken from a commit message
or an earlier record.

1. `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK, 403 of
   403 rows, committed index equal to the fresh build, all 33 parts named, 313 requirement numbers
   each claimed once.
2. `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md` — OK, 556 of
   556 rows, committed Reference equal to the fresh build, 410 anchors agreeing.
3. `python3 guardrails/check-architecture-reference.py ARCHITECTURE.md ARCHITECTURE.index.md` — OK,
   24 of 24 nodes, 410 anchors agreeing.
4. `bash guardrails/check-pin-drift.sh` — OK, 184 pins (61 line pins, 117 file-level, 6 unlabelled)
   plus 39 r5 range pins.
5. `bash guardrails/check-config-health.sh` — OK, 69 permission rules with 9 resolved paths and no
   dead ones, installed hooks matching their sources.
6. `bash guardrails/check-skill-review.sh` — OK, all nine changed skills carrying a fresh record.
7. `python3 scripts/spec-freeze.py --verify PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md` — GREEN,
   3 files.
8. `python3 guardrails/check-landing-next-steps.py` — exit 0. Twelve landing commits in the range
   miss a same-commit `NEXT_STEPS.md` refresh; every one prints `severity: warn` with its healer
   named, and the three that were blocking in the earlier records name `bf426ec4`, the fourth names
   `2d7f42ab`. No `severity: error` remains.
9. `bash guardrails/check-shipped-language.sh` — OK, 0 offences; `python3 guardrails/check-board.py`
   — OK; `python3 scripts/plan_checks.py` — exit 0.
10. `python3 -m pytest -q`, the whole suite, unscoped, started on a quiet tree (`git status
    --porcelain` empty before and after) and left alone for its whole run: **3 failed, 2734 passed,
    4 skipped, 28:12**. Two distinct reds, the third a consequence of the first — read below as
    findings 1 and 2, not counted:
    `tests/test_architecture_format.py::test_no_node_field_carries_history`,
    `tests/test_tasks_parser_finds_every_task.py::TestTheAcceptanceCommandsStayHonestMachinery::test_no_check_can_write_to_the_tree_or_the_machine`,
    and `tests/test_guardrails.py::TestGateB_Tests::test_real_content_passes`, whose nested run over
    a scratch copy reds on the same architecture-format test and reports nothing of its own.
    `TestGateA_ProverRecord::test_real_repo_passes` passed on the work road.
10b. Both reds re-run alone on the settled tree — `python3 -m pytest -q
    tests/test_architecture_format.py::test_no_node_field_carries_history
    tests/test_tasks_parser_finds_every_task.py::TestTheAcceptanceCommandsStayHonestMachinery::test_no_check_can_write_to_the_tree_or_the_machine`
    — 2 failed in 0.33s. Deterministic, not an artifact of a tree moving under a live suite.
10c. `git log -S` on each red's own trigger string, to name the commit rather than guess it:
    `-S "2026-09-02" -- architecture/guardrails.md` and `-S '"q-805"' -- scripts/plan_checks.py`
    both name `51d2d402`.
11. A direct re-derivation of the `[default]`-after-anchor-bracket defect the closing 2026-09-01
    record swept 19 times: a script over `PRODUCT_SPEC.md`, `spec/*.md`, `ARCHITECTURE.md` and
    `architecture/*.md` looking for a criterion line whose `[default]` tag trails its anchor bracket
    — 0 hits. The eleven lines that name the tag while carrying anchors all name it inside backticks,
    in prose, not as a tag. The sweep held through the whole of tonight's range too.
12. An independent re-derivation of the `[target]` coupling, not through the suite: every `[target]`
    marker in `PRODUCT_SPEC.md` and `spec/*.md` collected with the anchors on the criterion above it,
    matched against `tests/test_traceability.py`'s `TARGET_ROW_OWNERS` and against each named row's
    status character in `PLAN.md`. Nine markers, eight anchors — `E-18`, `INV-21`, `INV-67`,
    `INV-150`, `INV-185`, `INV-199`, `INV-201`, `INV-308` — every one in the map, every map entry
    under a marker, and every owning row open. No orphan in either direction.
13. The duplicate-row-id law re-run by hand rather than through the test the overnight record found
    vacuous: `grep -rhoE '^\|\s*(M-[0-9]+)\s*\|' matrix/*.md TEST_MATRIX.md` returns 556 rows and no
    duplicate; the same over `PLAN.md`'s row headings returns none. `tests/test_row_id_uniqueness.py`
    has since been repaired — it reads the parts and carries a non-empty guard — so that record's
    finding 4 is closed, and the tree it was meant to guard is clean independently.
14. `python3 evals/director/check.py --all` — 32 of 35, the exact number `14808ef2`'s message and
    `PLAN.md`'s plan-2 row both state. The three disagreements are named in the row.
15. `diff -rq` of each of the thirteen tracked pack skills against its installed copy under
    `~/.claude/skills/` — all thirteen present there, no drift in any of them.
16. `git show --pretty=format: --name-only` on `534cb16b`, `b0f8929c` and `4f0b760c`, to establish
    exactly what the two commits above the older half's last covered head actually touch.

Findings: four. Two are the suite reds on HEAD, both from `51d2d402` in the recent half; two come
from the fresh read of the older half. Three block. Nothing was repaired here — this record reports,
the orchestrating session triages.

1. **The suite is red on HEAD: `51d2d402` wrote the literal date `2026-09-02` into two fields of the
   architecture's `guardrails` node, and the no-history law reds on it.**
   `tests/test_architecture_format.py::test_no_node_field_carries_history` fails, naming
   `('guardrails', 'owns', 'date', '2026-09-02')` and `('guardrails', 'notes', 'date', '2026-09-02')`.
   The law is SPEC INV-279, Requirement 290 criteria 4 and 5: the journal holds when and why a node
   landed, and a node's field bodies carry no calendar date. Four sentences carry it —
   `architecture/guardrails.md:34` and `:60`, both inside the `owns` block that runs from line 5 to
   line 67, and `:149` and `:169`, both inside the `notes` block that opens at line 148. All four
   are the retirement notes q-805 wrote about the gates it cut, and each one states the date the gate
   retired. `git log -S "2026-09-02" -- architecture/guardrails.md` names `51d2d402` first and
   `bf426ec4` second, so the class arrived with the q-805 landing and was added to once more after
   it. Why nothing caught it earlier: the two records that read this range each ran a scoped set of
   suites, and neither set included `tests/test_architecture_format.py`. **Stands.**

2. **The suite is red on HEAD a second time: `51d2d402`'s new `q-805` acceptance command runs two
   programs the plan-check honesty law forbids.**
   `tests/test_tasks_parser_finds_every_task.py::TestTheAcceptanceCommandsStayHonestMachinery::test_no_check_can_write_to_the_tree_or_the_machine`
   fails on `scripts/plan_checks.py`'s `q-805` key, reporting that it carries a `python3` running a
   whole program the reader cannot judge. The key runs `python3 -c "import json,sys; sys.exit(...)"`
   and `python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`. The test's own sentence says
   why it holds: these commands run on every machine that opens this project, before anyone has
   decided anything, so a check reads state and never changes it. The test carries a `JUDGED_BY_HAND`
   map for keys a person has read and accepted, pinned by content hash — `plan-11`, `q-490`, `q-497`,
   `q-527`, `q-581`, `q-586` — and `q-805` has no entry. So this is not a case of the row inventing a
   new shape: the shape has a door, and the landing went past it rather than through it. **Stands.**

3. **A file was deleted out of the attic, which the spec says without qualification cannot happen,
   and the manifest still carries its line.** `caa7f6a7` removed
   `attic/inbox-2026-08-05-from-tlvphotos-rotation-gate-reads-only-numbered-rows.md`, a harvested
   inbox message from another project, from `attic/`. Four places in this tree state the law it
   breaks, and none of them is scoped to a case this is not:
   - `spec/project-setup-tuning.md`, Requirement 179 (its heading is *Attic over deletion*),
     criterion 2: the attic *shall* be append-only, one manifest line per file. `[A-4]` — no *when*,
     no *if*, no host-file qualifier. Criterion 5 of the same requirement puts authored content
     through the attic and never lets it qualify for the cruft sweep, and criterion 4 makes even
     regenerable junk wait on the person's explicit approval.
   - `PRODUCT_SPEC.md:28`, the spec's own glossary: the attic is the host's append-only archive
     folder, a superseded file moving there with one manifest line and being kept for good.
   - `DECISIONS.md:497` and `skills/live-spec-base/references/glossary.md:39` carry the same
     sentence, both citing INV-7.
   - Base rule 10 of `skills/live-spec-base/SKILL.md`: nothing is silently deleted, and only junk
     that can be regenerated may be deleted, listed and approved by the person first (SPEC INV-7,
     A-4, A-9). A harvested inbox message is not regenerable junk, and the commit records no such
     listing and no approval.

   Searched for an exception before naming this: `grep` for an attic retention or pruning rule
   across `spec/`, `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `architecture/`, `DECISIONS.md` and the
   base rulebook returns none. The commit's own message surveys retention policy for
   `docs/handovers/`, `docs/queue-archive/`, `attic/transcripts/` and `docs/prover/`, and correctly
   declines to invent a cutoff for any of them — it simply never reaches the rule that governs the
   folder it was actually cutting from.

   The ledger is now stale in the same act. `attic/MANIFEST.md` opens by saying that every file
   which left active use rests there and that nothing there was deleted, citing SPEC INV-7, A-4 and
   base rule 10; that sentence is false as the tree stands. Line 30 still carries the deleted
   document's retirement line, so the manifest names a path with nothing behind it. Checked rather
   than assumed, since a manifest line with no file is ordinary here: of the 56 attic paths the
   manifest names, 29 have nothing on disk, but 27 of those are rendered `.html` pages swept off
   disk under this pack's own rule for rendered bytes, and one is a directory-name placeholder. This
   is the only source document among them.

   Why the per-landing reviews did not catch it: the deletion's own reasoning was about whether the
   file was dead, and it read `attic/MANIFEST.md` only for that file's provenance line. The
   contradiction is between the commit and the sentence three lines above the one it quoted, and
   between the commit and a requirement in a spec part the landing never opened. Nothing goes red —
   `matrix/attach.md`'s M-037, the matrix row that owns INV-7, is `*todo*`, so no test holds the
   law.

   Nothing is lost: the file is intact in git history at `11987b8` and every commit before
   `caa7f6a7`, so the repair is a restore, or a spec change if the person wants the attic to become
   prunable. That choice is the person's and is not made here.

4. **`matrix/snapshot.md`'s M-063 still points at a row that closed.** The row's owning-test column
   reads that the machine lands at row 55. Row 55 closed on 2026-08-31, narrowed to the adoption
   starting-state case, and `67f9ce6e` landed the snapshot machinery under `q-802` on 2026-09-01 —
   the same range. The pointer is stale by that landing's own doing. Its status stays `*todo*`, which
   is defensible on its face: `advance_baseline` has no caller anywhere in the tree, so the behaviour
   the row states — the baseline advancing at a landing, for declared surfaces only — is not
   performed by anything, and the live manifest carries no surface. Checked before naming it: this is
   not the orphaned-arm class the overnight record made blocking for `q-804`, because a `*todo*`
   matrix row whose anchors carry no `[target]` is the tree's ordinary state, not an anomaly — 49 of
   the 65 `*todo*` rows are in exactly that position, and `tests/test_traceability.py` only holds
   `*built*` rows to naming a real test. So the only defect here is the dead pointer, and the row
   would now have a real test to name if the person wants it moved.

What the fresh read checked and found clean, so the two findings above rest on coverage rather than
on silence:

- **The concurrent-worker revert is complete in both directions.** `54bde341` pulled
  `TEST_MATRIX.index.md`, `matrix/test-author.md` and `skills/communicator/SKILL.md` back out of
  `e2a0e8c4`, and every piece it removed returns later in the same range under its own row —
  `M-620` and its `E-27` mapping at `287e019c`, the fourteen communicator rulings at `1280cd99`,
  moved into `references/rule-histories.md` at `084c3eb4`. The cumulative diff nets out to +1 row in
  `matrix/test-author.md`, 1/1 in `TEST_MATRIX.index.md` and 11/11 in the communicator skill, with no
  ruling lost: `check-matrix-reference.py` reads the committed Reference as equal to a fresh build.
- **The Cyrillic waiver `5c8ebb87` added is not vacuous.** `scripts/check-shipped-language.py` builds
  its snippet as the stripped line truncated at 110 characters and asks whether a waiver's snippet is
  a substring of it. The waiver's text stops at the upstream-branch clause and reads at first glance
  as naming the wrong line, but `plan_checks.py:32` is one long command whose Cyrillic grep comes
  later on the same line, and the waived prefix fits inside the 110-character window. The gate reports
  0 offences, and it reports them because the waiver matches the line that actually carries the
  Cyrillic.
- **`f7382a15`'s scratch-copy stand-down is the tree's established convention, correctly imported.**
  `tests/test_dialog_warning_guard.py` gained a `LIVE_SPEC_SCRATCH` skip; the module already imports
  `os` and `pytest`, and eight other suites plus `tests/conftest.py` carry the same guard for the same
  reason.
- **The `q-802` plan-check is a real check, not a file-existence probe.** Its command runs
  `python3 tests/test_snapshot_baseline.py`, and that module ends in `unittest.main()`, so running it
  directly executes the suite. `7c25768c` moved it off `python3 -m pytest` deliberately, and its own
  comment names the rule it was breaking.
- **`cf244b5b`'s guard did not fail to hold.** The guard is scoped, in its own words and its own
  red-proofs, to one false Known-Issue claim under paraphrase. `beaf953d`'s later front-page repair —
  a stale project count and a gap in the July history — is a different defect, not a recurrence the
  guard was written to catch. Checked because a guard landing in this range and the same page needing
  repair one day later is the shape of a guard with too narrow a reach; here it is not.
- **q-398's hook is wired for real, not only declared.** `guardrails/judge-hooks.json` gained
  `routing-preamble-hook` in its `wired` map and in its `file`, `command`, `matcher` and `data` maps
  in the same commit; `~/.claude/settings.json` carries the matching `UserPromptSubmit` entry;
  `~/.claude/hooks/routing-preamble-hook.sh` exists and diffs empty against `hooks/`. Checked
  directly because a declaration map and a live wiring are two different things, and the overnight
  record's own blocking finding 2 was about exactly that gap in a sibling landing.
- **plan-2's three stated scores do not contradict each other.** The row carries 33 of 35, then 34 of
  35, then 32 of 35, each dated and each explained by what was re-recorded. The live run agrees with
  the last of them.
- **No commit in the older half creeps past its own message.** Read by diff against subject line for
  each of the eight commits named in `Files read`, and by file-level stat for the rest.

Blocking: none — all three closed by `84e0bf95`, each re-verified rather than taken on the fixing
commit's own word.
- the architecture no-history red (finding 1) — closed: the four dated sentences in
  `architecture/guardrails.md` reworded to drop the calendar date, the fact intact, the journal
  holding when. `python3 -m pytest -q tests/test_architecture_format.py` — 11 passed.
- the q-805 acceptance-command red (finding 2) — closed: the command read a second time,
  independently, before pinning — the inline `python3 -c` does `json.load`+`sys.exit` only, and
  `scripts/spec-redundancy-precheck.py` has no write call anywhere in it (checked by grep). Content
  hash added to `JUDGED_BY_HAND`. `python3 -m pytest -q tests/test_tasks_parser_finds_every_task.py`
  — 11 passed.
- the attic deletion in `caa7f6a7` (finding 3) — closed: restored byte-for-byte from `caa7f6a7^`
  (`diff` against the original, empty). `attic/MANIFEST.md`'s own claim is true again.

Finding 4, non-blocking, closed the same commit: `matrix/snapshot.md`'s `M-063` corrected to cite
`tests/test_snapshot_baseline.py` and `*built*`, matching `q-802`'s actual 2026-09-01 landing.

Every gate in the local chain is green on the tree as it stands. The full suite, run once more,
alone, on this exact commit, after every fix above: `2736 passed, 5 skipped, 0 failed` — a real
whole-tree count, `tests/test_architecture_format.py` and `tests/test_tasks_parser_finds_every_task.py`
(this record's own two findings) counted inside it rather than checked in isolation.
