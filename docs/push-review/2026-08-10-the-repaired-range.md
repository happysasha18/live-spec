# Push review — 2026-08-10 the repaired range

PUSH-REVIEW

Range: `origin/main..HEAD`, that is ba479b6..2121b91, plus this record itself.

The base is `origin/main` at ba479b6, the remote tip pushed 2026-08-07 at 15:24. `git rev-list
--count ba479b6..HEAD` returns 28. The head is 2121b91, tonight's commit carrying a prover record
and the day's progress regeneration.

Twenty-six of the twenty-eight commits were reviewed on 2026-08-09 in
`docs/push-review/2026-08-09-the-culling-first-day.md`, which refused the delta on three findings.
This pass covers the whole range again, and it spends its attention on the two commits written since
that refusal and on whether the three findings are truly closed in the tree.

- 740dc0f — four published numbers come back to what the tree holds, and the resume is rewritten for
  a clean start. It carries the 08-09 review record itself.
- 2121b91 — the architecture's wall-time row earns its re-check under `docs/prover/`, and
  `docs/PROGRESS.md` with its baseline take the day's regeneration.

Root: the pre-push run's own printed remedy at gate ac (SPEC INV-304), and Alexander's word of
2026-08-10 20:30 to land the previous seat's finished work.

## Files read

The full diff of the range, by file and by added line. `NEXT_STEPS.md` whole, and its diff in
740dc0f. `docs/prover/2026-08-10-architecture-wall-time-row.md` whole. The wall-time row at
`ARCHITECTURE.md:878`. `guardrails/pre-push` whole, `guardrails/check-pin-drift.sh`,
`guardrails/check-doc-findings-bound.py` at its live-document arm, `scripts/progress-report.py` at
its continuity sentence and its baseline write. `guardrails/rule-census.json`'s whole diff.
`skills/live-spec-base/SKILL.md` rule 9. `PRODUCT_SPEC.md` at the INV-302 clause list,
`TEST_MATRIX.md` at M-484, M-485, M-346 and M-514, `ROADMAP.md` at row 522,
`JOURNAL.md` at its last entry and at lines 2466 to 2472,
`.live-spec/handover-2026-08-09.md` at its correction table,
`.live-spec/day1-census-delivery.md` at its headline and method,
`.live-spec/day1-queue-for-striking.md` at row 553, `tests/test_opening_decision_sweep.py`,
`tests/test_guardrails.py` at its skip guards, `docs/plans/2026-08-07-recovery-plan.md` and
`docs/prover/2026-08-07-recovery-plan-adversarial.md` at the passage each gives
`docs/plans/current-order.md`, `attic/MANIFEST.md`, `inbox/2026-08-08-verdict-lands-same-minute.md`,
and `docs/push-review/2026-08-09-the-culling-first-day.md` whole, for its verdict and for form.

## Checks run

Every result below is the printed line, taken after the last commit in the range.

- `bash guardrails/pre-push` — one gate red out of thirty, gate ac, the push-review gate this record
  answers. Every other gate printed OK. The log's last line reads "PUSH BLOCKED — one or more gates
  above failed."
- `python3 -m pytest -q` — `2490 passed, 2 skipped in 173.84s (0:02:53)`, exit 0.
- `python3 -m pytest -q --collect-only` — `2492 tests collected in 0.39s`.
- The two skips are named guards inside `tests/test_guardrails.py`: the suite-in-suite meta-test
  stands itself down while the gate machinery's digest is unchanged since its last green (row 573).
  That accounts for the gap between tonight's 173.84 s and the 463.51 s the prover record measured
  with the meta-test firing.
- `guardrails/check-suite-budget.sh` over that run's log — `OK (suite budget): measured 173.84 s
  within the stated 605 s`. Inside the gate chain's own run it read 170.72 s.
- `python3 guardrails/check-doc-findings-bound.py` — `OK: 122 live documents, 22 held at zero, none
  above its record (cap 25, rule r08)`. `NEXT_STEPS.md` is among the documents held clean.
- `bash guardrails/check-prover-record.sh --push` — OK, naming
  `docs/prover/2026-08-10-architecture-wall-time-row.md`, and OK on both freshness arms.
- `bash guardrails/check-push-review.sh` — FAIL, as it must until this record commits.
- `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md` — OK, 544 of 544 rows, 405 anchors.
- `bash guardrails/check-freeze.sh` — GREEN over the three guarded documents.
- `python3 guardrails/check-tree-counts.py` — OK, 3 of 3 rows.
- `python3 guardrails/check-every-gate-can-fail.py` — OK, 30 gates, each with a proof.
- `bash guardrails/check-ci-mirror.sh` — OK. `bash guardrails/check-config-health.sh` — OK.
- `python3 guardrails/check-landing-next-steps.py` — OK over the whole range.
- `bash guardrails/check-pin-drift.sh` — OK with four drifts reported under the non-strict rule.
- `git rev-list --count ba479b6..HEAD` — 28. `git rev-parse --short origin/main` — ba479b6.
- `wc -c skills/live-spec-base/SKILL.md` — 66435. `cat skills/*/SKILL.md | wc -c` — 410457.
  `ls -d skills/*/ | wc -l` — 11. `grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push | sort -u |
  wc -l` — 30.
- A path sweep over every backtick-quoted file path on a line this range adds, resolved against the
  tree. Results below.
- A credential-shaped-string sweep over the whole range diff, since the remote is a public
  repository. Nothing matched.

## The three findings that refused this delta on 2026-08-09

All three are closed. I checked each one against the tree, reading the files the repair touched.

**Blocking finding 1, the resume file redding gate aa and the suite — closed.**
`python3 guardrails/check-doc-findings-bound.py` returns OK and names `NEXT_STEPS.md` among the
documents held clean. The suite is green at 2490 passed, and
`tests/test_doc_findings_bound.py::TestDocFindingsBound::test_the_real_repository_passes`, the case
that failed then, is inside that green run. The census entry for `NEXT_STEPS.md` in
`guardrails/rule-census.json` moved from 4854 bytes to 4822 with its recorded finding counts left at
zero, which is the shape a repaired page takes.

**Blocking finding 2, the prover-record gate redding on the architecture edit — closed by a real
pass.** 740dc0f moved `ARCHITECTURE.md:878`, and 2121b91 commits
`docs/prover/2026-08-10-architecture-wall-time-row.md` after it, so gate a's third arm finds a
descendant record and prints OK. The 08-07 record's standing objection asks whether a record filed
to re-arm a gate does any work, so I re-derived the record's own claims. The row's figure of 2,492
tests matches `--collect-only` tonight. The bound of 605 s is what the check's own parse pulls out of
the row, and the measured run sits under it. `guardrails/check-suite-budget.sh`,
`guardrails/doc-bounds.json`, M-346 at `TEST_MATRIX.md:571`, queue row 553 at
`.live-spec/day1-queue-for-striking.md:104`, and the pytest line in `.github/workflows/gates.yml` all
exist and say what the record says they say. The one claim I could not reproduce is the meta-test's
292.0 s, since those two cases stood themselves down tonight under their digest guard; the record
names the two cases and its own command, so a later seat can re-measure it.

**Blocking finding 3, the resume publishing a dying scratchpad address — closed.**
`NEXT_STEPS.md:46-47` now reads "Its eight files sit at `~/live-spec-carry/2026-08-09/`".
`ls ~/live-spec-carry/2026-08-09/` returns eight files, 252 kilobytes of modified skill bodies,
sitting under the home directory, which outlives every session. The 2026-08-06 carry directory
beside it shows the same home is already the habit for work held outside the tree. No
tracked file in the range names a `claude-501` scratch path as the home of live work; the ten
remaining scratch paths in the tree are dated records naming the file a past pass read.

## What else I attacked

**The path pointers.** Every backtick-quoted path on a line this range adds was resolved against the
tree. Twelve files hold a path that does not resolve, and every one of them is correct as written.
Nine name `guardrails/check-handover-provenance.py` or `tests/test_handover_provenance.py`, which are
records of the removal that took them, and the script's new home is
`attic/check-handover-provenance.py` with its manifest line. `docs/plans/current-order.md` appears in
the recovery plan as a file that plan proposes, and in the adversarial review that rejects the
proposal. `.live-spec/day1-census-delivery.md` names `docs/deltas/2026-07-22-row445.json` in the
list of illustrative examples it excludes from its own count. `docs/prover/2026-08-09-culling-plan-v2.md`
names `attic/check-pin-drift.sh` while reading a staged rename, which the restore of 11:22 undid.

**The ratchet.** No recorded finding count rises anywhere in `guardrails/rule-census.json`. The diff
moves byte counts and adds three documents at their measured values, the largest being
`docs/plans/2026-08-07-recovery-plan.md` at 61 findings with a longest sentence of 99 words. Gate aa
reads the recorded value as the ceiling, so the entrant is bounded from here on.

**The removals.** The gate roster stands at 30, `check-every-gate-can-fail` finds a red proof for each
of the thirty, `check-ci-mirror` finds each mirrored in CI or carved out by name, and
`check-named-checks` reads 32 registry entries against 11 skill bodies without an offence. The
architecture-pointer check that was cut and restored is byte-identical to the base and wired at
`guardrails/pre-push:89`.

**The public remote.** `github.com/happysasha18/live-spec` is public, so the range was swept for
credential-shaped strings and found none. Cyrillic appears on lines this range adds in nine files,
and every one of them belongs to a class the published tree already carries, including `JOURNAL.md`,
`ROADMAP.md`, `TEST_MATRIX.md` and `.live-spec/`. Gate i finds no owner name and no Cyrillic inside
the shipped set, which is the boundary the owner set for this repository.

## Findings

Five findings stand. None blocks. Findings 1 and 2 are new. Finding 3 carries forward the 08-09
record's unrepaired majors. Findings 4 and 5 are minor and predate this range.

### 1. Major — the resume's live-state block sits two steps behind the tree

`NEXT_STEPS.md:57-60` opens "**Right now.**" and says a fresh review refused the push range on three
findings, then names the structural one: an `ARCHITECTURE.md` edit demands a fresh record under
`docs/prover/` that descends from it. Commit 2121b91 filed that record, gate a prints OK, and the
other two findings are closed as shown above. A session starting on this page would set out to repair
what the tree already holds repaired.

`NEXT_STEPS.md:17` reads "Commits since the last push of 2026-08-07: 26, all local" while
`git rev-list --count ba479b6..HEAD` returns 28. The line went one behind the moment it landed, and
tonight's commit put it two behind. The prover record raised this at its minor finding and named the
repair as the next seat's.

Rule 9 of the shipped rulebook asks the prose of `NEXT_STEPS.md` for current truth. Both sentences sit
under a block stamped 2026-08-09, 15:35, and both were true under that stamp. No gate reads either
one. The repair is two sentences and belongs to whoever next writes the live-state block, which is the
same seat that lands this record's verdict. My write set for this pass is this record alone, so the
repair is named here and passed on rather than made.

### 2. Major — the day's movements after 11:35 carry no journal entry

`JOURNAL.md`'s newest heading is "## 2026-08-09, 11:22-11:35 — the architecture-pointer check comes
back on his word". Rule 9 of the shipped rulebook asks that the dated reason behind every movement go
to `JOURNAL.md` the same session. Three movements since that entry have none: the push review that
refused the delta, the repair pass that answered its four numbers, and tonight's prover pass with the
progress regeneration.

What the journal would carry is written down and dated elsewhere, in
`docs/push-review/2026-08-09-the-culling-first-day.md` and
`docs/prover/2026-08-10-architecture-wall-time-row.md`, so no reason is lost from the tree. What a
reader of the journal alone sees is a day that stops at 11:35 on 2026-08-09. The entries are owed and
cheap, and they belong with the resume repair in finding 1.

### 3. Major — four findings from the 08-09 record stand exactly as that record left them

Each was ruled non-blocking then, and nothing since has moved any of them. I re-checked all four.

`.live-spec/handover-2026-08-09.md:43` still reads "the install leaves 219 references pointing at
nothing" in the table whose purpose is to hold corrected values, and its answer column speaks to the
scope rather than to the value of 218 that two other pages now carry. `JOURNAL.md:2471` still reads
219 and `JOURNAL.md:2468` still reads "Thirty-five rules hold 48 387 bytes" against the same table's
88 rules.

Gate s greens on `docs/skill-review/2026-07-17-live-spec-base-build-pipeline.md` while this range
changes `skills/live-spec-base/SKILL.md` and files
`docs/skill-review/2026-08-09-live-spec-base.md` for that change. The review exists and did its work;
the gate matched neither the change nor the record, and queue row 580 holds the repair.

`tests/test_opening_decision_sweep.py:1` still reads "(SPEC INV-302, R303.19..R303.23)" while
`TEST_MATRIX.md:201` reads R303.20 to R303.26 for M-485, and R303.19 is the retired provenance clause
whose matrix row M-484 now reads "retired, no owning test". Beside it, `PRODUCT_SPEC.md` keeps R303.19
as a *shall* with no machine reading it; `ARCHITECTURE.md:69` and rule 35 of the rulebook say so and
the spec itself stays silent.

`.live-spec/day3-opening-2026-08-09.md:9` and `.live-spec/day1-census-delivery.md:7` still say a
stranger gets the ten skill folders, where `ls -d skills/*/ | wc -l` returns 11 and `NEXT_STEPS.md:26`
says eleven. `ROADMAP.md:198`, row 522, still gives its Done-when as "rows M-483, M-484 and M-485
carry them with their tests — MET" and still describes gate ab, which no longer exists.

### 4. Minor — the progress page's continuity sentence names its own generation date

`docs/PROGRESS.md:5` reads "Since the last run on 2026-08-10, total findings changed by 0 and
documents at zero changed by 0", and the page above it says it was generated on 2026-08-10. The
previous run was 2026-08-09. `scripts/progress-report.py` builds that sentence from the baseline at
line 463 and rewrites the baseline at line 565, so a second run on the same day reads the date it
just wrote. `origin/main` carries the same shape with 2026-08-07 on both lines, so this predates the
range. The delta the sentence reports is true against the 08-09 baseline as well: total findings
stand at 4876 and documents at zero at 22 on both sides of the commit.

### 5. Minor — four pin labels drift, and the gate reports without redding

`bash guardrails/check-pin-drift.sh` names `scripts/install-pack-hooks.sh:1`,
`guardrails/rule-census.json:1`, `skills/design-reviewer/SKILL.md:1` and `skills/text-audit/SKILL.md:1`,
then prints OK under the non-strict rule the script states in its own header. Three of the four sit in
files this range never touches. The fourth is a pin into a JSON data file, where the label's words have
nowhere to appear. Queue row 541 already holds this check's own defect.

## Verdict

This delta is fit to push.

The three findings that refused it on 2026-08-09 are closed, and I verified each against the tree.
The resume no longer sends a reader to a session-keyed scratch path, and the eight skill bodies it
names really sit at `~/live-spec-carry/2026-08-09/`. The findings-bound gate reads `NEXT_STEPS.md`
clean and the suite is green at 2490 passed with 2 named skips. The architecture edit carries a prover
record that re-derives its numbers instead of reading them back, and every pointer that record names
resolves.

Twenty-nine of the thirty push gates pass. The one red is gate ac, the push-review gate, and it is
red because this record had not been committed when the chain ran. It turns green with this commit.

Five findings stand and none of them blocks. Two of them, the stale live-state block and the missing
journal entries, are the same debt in two places: the day's verdict has not yet been written into the
documents a next session reads first. Both repairs belong to the seat that lands this record, and
both are short.

## Reach

Read whole: `NEXT_STEPS.md`, `docs/prover/2026-08-10-architecture-wall-time-row.md`,
`docs/push-review/2026-08-09-the-culling-first-day.md`, `guardrails/pre-push`,
`guardrails/check-pin-drift.sh`, the diff of `guardrails/rule-census.json`, and the range's diff by
added line.

Read in part: `ARCHITECTURE.md` at line 878 and line 293, `PRODUCT_SPEC.md` at the INV-302 clause
list, `TEST_MATRIX.md` at M-346, M-484, M-485 and M-514, `ROADMAP.md` at row 522, `JOURNAL.md` at its
tail and at lines 2466 to 2472, `scripts/progress-report.py` at lines 455 to 475 and 555 to 570,
`guardrails/check-doc-findings-bound.py` at its live-document arm, `tests/test_guardrails.py` at its
skip guards, `skills/live-spec-base/SKILL.md` at rules 8 and 9, and the `.live-spec/` day pages at the
lines named above.

Not verified: the meta-test figure of 292.0 s, which stood down tonight under its digest guard; the
install measure of 218, which counts an installed tree outside this repository; and the three
historical wall-time readings the architecture row keeps as records of past runs.

Files written by this pass: this record alone. The working tree held no uncommitted change when the
pass began and holds none beside this file.
