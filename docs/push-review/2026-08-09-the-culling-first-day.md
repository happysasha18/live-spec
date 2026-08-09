# Push review — 2026-08-09 the culling's first day

PUSH-REVIEW

Range: ba479b6..9c929a0, plus the two commits that will carry the repairs this record names and this
record itself.

The base is `origin/main` at ba479b6, the remote tip pushed 2026-08-07 at 15:24, carrying the
push-review record that named the wall-time commit. The brief named ba479b6 as the base and
`origin/main` resolves to the same commit, so the two agree and the range is the whole unpushed
delta. The head is 9c929a0, the state page that reads the git log back at the two executed rows.

The range holds 26 commits at the time of the first pass. Every one is named below with what it does.

- ee118f6 — the 08-08 hostile re-audit verdict lands in the resume file.
- b2c8186 — the culling plan and its hostile review land in the resume file.
- 992c356 — the third-edition culling plan and its four review rounds land in the resume file.
- 36e0518 — the frozen culling plan, its review record and the audit land in the workshop area.
- b52d355 — the plan freeze and the restart protocol land in the resume file.
- fb1e9d7 — day 1 preparation: the two red tests go green, two feedback files enter the record, the
  resume file returns to zero findings.
- 4efa029 — day 1 preparation: the four starting measures and the rule census land.
- 63db23c — day 1 preparation: the delivery census lands and fills the first starting measure.
- daf953d — day 1 preparation: the queue page for his pen lands.
- ab72d75 — the queue page states each row in its own positive sentence.
- cef83d5 — day 1 preparation: the check census lands, and the restore incident takes queue row 586.
- 73840dc — day 1 preparation closes: the resume file carries the day's results.
- e68b8c3 — day 2 trial cut: the verdict list commits first.
- 1b32d8f — day 2 row 2.1: the architecture-pin drift gate goes with its whole tail.
- 0ef204e — day 2 row 2.2: the handover-provenance gate goes with its tail, its two reviews and the
  day's journal entry.
- 94dfd02 — day 2 closes: the measured price and the recounted calendar.
- 3b9bdd6 — day 2: the three rule verdicts are withdrawn, and the reason is recorded.
- ab8031c — day 3 opens: the install defect is narrower than stated, and its repair is named.
- 17429cc — the rule verdicts are redrawn with the reach column, and the lever moves to shortening.
- 75cb327 — the redrawn verdicts are reviewed before execution, and five rows are withdrawn.
- d80a7e0 — the rulebook measure counts the reference pages beside the body.
- 49f246c — the culling is recompiled against the cost of a change, on his word.
- d58c903 — the architecture-pointer check comes back on his word, with its own repair row.
- 1f7fca7 — the recompiled plan gets its adversarial review before any of it executes.
- 9cfc5c8 — one page carries the whole state for the next session, and the resume points at it.
- 9c929a0 — the state page states what the git log shows about the two executed rows.

Two more commits will follow: one carrying the repairs this record's second pass judges, one carrying
this record. Both are covered here.

Files read: the full diff of the range; the uncommitted repair diff over `NEXT_STEPS.md`,
`ARCHITECTURE.md`, `.live-spec/handover-2026-08-09.md`, `.live-spec/day2-price-2026-08-09.md` and
`.live-spec/day3-opening-2026-08-09.md`; `PRODUCT_SPEC.md` (Requirement 303 and both generated code
tables), `PRODUCT_SPEC.index.md`, `TEST_MATRIX.md` (M-082, M-154, M-483 to M-490 and the anchor
table), `ROADMAP.md` (rows 522, 541, 558, 586, 587),
`docs/queue-archive/rotated-ROADMAP-2026-08.md`, `JOURNAL.md` (the three entries this range adds),
`guardrails/pre-push`, `guardrails/check-prover-record.sh`, `guardrails/check-tests.sh`,
`.github/workflows/gates.yml`, `guardrails/gate-red-proofs.json`, `guardrails/README.md`,
`guardrails/tree-counts.json`, `tests/conftest.py`, `scripts/check-registry.json`,
`scripts/spec-freeze.py`, `install.sh`, `skills/live-spec-base/SKILL.md` rule 35,
`tests/test_opening_decision_sweep.py`, `tests/test_session_extract.py`,
`scripts/session-extract.py`, `attic/MANIFEST.md`,
`docs/prover/2026-08-09-culling-day2-cuts.md`, `docs/prover/2026-08-09-redrawn-rule-verdicts.md`,
`docs/prover/2026-08-09-culling-plan-v2.md`, `docs/skill-review/2026-08-09-live-spec-base.md`,
`.live-spec/day1-measures-2026-08-09.md`, `.live-spec/day1-census-delivery.md`,
`.live-spec/day1-census-checks.md`, `.live-spec/day1-queue-for-striking.md`,
`.live-spec/day2-verdicts-2026-08-09.md`, and
`docs/push-review/2026-08-07-the-night-order-and-the-morning-orders.md` for form.

Checks run: seventeen, each with its result. The suite figure that counts is the third run, taken
after the last edit to the tree.

- `python3 -m pytest -q > <scratch>/push-review-suite-3.log 2>&1` — last line of the log:
  `1 failed, 2489 passed, 2 skipped in 182.17s (0:03:02)`. The one failure is
  `tests/test_doc_findings_bound.py::TestDocFindingsBound::test_the_real_repository_passes`. See
  finding 1.
- The two earlier runs, for the record: `2490 passed, 2 skipped in 169.48s` before any repair, and
  `2490 passed, 2 skipped in 173.96s` after the four repairs and before the 15:25 rewrite of
  `NEXT_STEPS.md`.
- `python3 -m pytest -q --collect-only | tail -3` — `2492 tests collected in 0.38s`.
- `python3 guardrails/check-doc-findings-bound.py` — FAIL on `NEXT_STEPS.md`. See finding 1.
- `python3 scripts/rule-census.py NEXT_STEPS.md` — 5 long, longest 35 words, 1 style, 6 in all. The
  same command over the committed copy of the file returns 0 in all.
- `python3 scripts/spec-style-lint.py NEXT_STEPS.md --tier full` — 1 error, `line 18 [scissors]`.
- `bash guardrails/check-freeze.sh` — GREEN over the three guarded documents, after the re-freeze.
- `bash guardrails/check-prover-record.sh` — OK today, and see finding 2 for what happens when the
  repair commit lands.
- `python3 guardrails/check-tree-counts.py` — OK, 3 of 3 rows matched.
- `grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push | sort -u | wc -l` — 30.
- `cat skills/*/SKILL.md skills/*/references/*.md | wc -l` — 6412.
- `cat skills/*/SKILL.md | wc -l` — 5177.
- `ls scaffold/guardrails/check_*.py | wc -l` — 4.
- `python3 guardrails/check-every-gate-can-fail.py` — OK, 30 gates checked, each with a proof.
- `bash guardrails/check-ci-mirror.sh` — OK.
- `bash guardrails/check-config-health.sh` — OK, installed hooks match their sources.
- `python3 guardrails/check-landing-next-steps.py` — OK.
- `bash guardrails/check-skill-review.sh` — OK, but the OK names a record from 2026-07-17, not this
  range's own. See finding 7.
- `bash guardrails/check-push-review.sh` — FAIL, as it must until this record commits.

## What the range did to the two checks

The handover-provenance check is gone for good, and its removal is complete in the tree. The script
moved to `attic/check-handover-provenance.py` with a dated manifest line. Gate ab left
`guardrails/pre-push`, `.github/workflows/gates.yml` and `guardrails/gate-red-proofs.json`; the
roster block on `guardrails/README.md` lost its line and its count fell to 30. `check-ci-mirror`,
`check-every-gate-can-fail` and `check-named-checks` all pass over the result, and the script was
never in `scripts/check-registry.json`. `tests/test_handover_provenance.py` is deleted, its 140
lines tested that gate alone, and `TEST_MATRIX.md:200` marks M-484 `*retired*` with no owning test.
Requirement 303 renumbered from 38 clauses to 33, and both generated code tables agree with the
body. No live file sends a reader to `guardrails/check-handover-provenance.py`.

What the removal took with it is real and only half-recorded. `PRODUCT_SPEC.md` R303.19 still stands
as a *shall*: a session handover names the transcript it was read from, the extract file, and the
agent that wrote it. Nothing now reads that shape. `ARCHITECTURE.md:69` records the loss —
"Both steps stay a discipline the seat holds" — and rule 35 of the shipped rulebook records it too,
naming the withdrawn script and the day. The spec itself does not: R303.26 says why no machine holds
the *opening* step, and no clause says the same about R303.19. The queue holds row 587 for the
adjacent failure, sessions closing with no handover at all, and no row for the provenance shape. So
the behaviour is unguarded, two documents say so and the third does not, and the queue records the
neighbouring gap rather than this one.

The pin-drift check came back whole. `guardrails/check-pin-drift.sh` does not appear in the range's
diff at all, which means it is byte-identical to the base. Neither do `tests/test_guardrails.py`,
`tests/test_traceability.py`, `tests/test_architecture_pins.py`, `adopt/ADOPT.md`, or the M-082 and
M-154 rows of `TEST_MATRIX.md`. The wiring is live: gate g announces at `guardrails/pre-push:89`
and runs the script at line 90, `.github/workflows/gates.yml:37` mirrors it, the red proof stands in
`guardrails/gate-red-proofs.json:26`, and the roster line stands at `guardrails/README.md:34`.
`TEST_MATRIX.md:555` reads M-082 `*built*` with its three tests. Queue row 541, the check's own
defect, is live again in `ROADMAP.md:217`. The restoration is complete; I found nothing left behind.

## The four blocking findings of the first pass, verified against the tree

All four are truly fixed. Each is stated with what I checked rather than what the repair claimed.

**Original finding 1, the resume file's commit count — fixed.** `NEXT_STEPS.md:15` now reads
"Commits since the last push of 2026-08-07: 26, all local." `git rev-list --count ba479b6..HEAD`
returns 26. The date holds too: `git log -1 --date=iso ba479b6` returns 2026-08-07 15:24:15. The
repair also corrects this record's own first pass, which called the base a push of 2026-08-08; the
header above is amended. The number is now stated against a fixed landmark rather than a count that
goes stale on the next commit, which is the right shape. What the repair broke is in findings 1, 3
and 4 below: the sentence landed inside a whole-page rewrite that reds two gates.

**Original finding 2, the handover's commit count and false range — fixed.**
`.live-spec/handover-2026-08-09.md:22` now reads "Every commit since `ba479b6`, the last push of
2026-08-07, is local, `fb1e9d7` onward." The false count and the false range
`fb1e9d7` through `1f7fca7` are both gone, and the page no longer excludes the five commits below
`fb1e9d7`. The surviving "`fb1e9d7` onward" is decorative now that `ba479b6` sets the boundary, and
it is not wrong. Nothing else on the page moved.

**Original finding 3, the architecture's test count — fixed.** `ARCHITECTURE.md:878` now reads "one
full `python3 -m pytest -q` run at 2,492 tests", matching `pytest -q --collect-only`. The two later
figures in the same row are correctly left alone: "the row it replaces read 474 s at 2,502 tests on
the morning of 2026-08-07" and "before it, 470 s at 2,404 tests on 2026-08-06" are labelled as
earlier measurements and are true as history. The re-freeze was really run —
`bash guardrails/check-freeze.sh` returns GREEN over all three guarded documents, and it redded
before it. One thing the re-freeze does not do: `.spec-freeze/` is ignored at `.gitignore:24`, so the
baseline is a local artifact and does not travel with the push. That is how the freeze has always
worked here and is not this delta's business.

**Original finding 4, the install measure — fixed, and the arithmetic checks out independently.**
`.live-spec/day2-price-2026-08-09.md:23` now reads "219 | 218 | row 2.2 took one counted reference
with it", and `.live-spec/day3-opening-2026-08-09.md:67` carries the same correction with the reason
named. I verified 218 rather than taking it: the rule-35 edit deleted exactly one path,
`guardrails/check-handover-provenance.py`, which
`.live-spec/day1-census-delivery.md:80` lists among the 123 missing targets; no other installed file
named it, and the census's separate bare-filename class holds no twin of it. The rest of the
rewritten rule 35 names `DECISIONS.md` and `NEXT_STEPS.md`, both of which survive the edit, and
`docs/handovers/`, which the census excludes as a directory-only mention. So the movement is exactly
one, and 218 is right.

## The four numbers swept across the tracked tree

Every hit ruled on. The attic is excluded by rule.

**"2,502" — ten hits, all correct.** `ARCHITECTURE.md:878` keeps one, as the row it replaces.
`JOURNAL.md:2420`, `docs/plans/2026-08-07-recovery-plan.md:32`,
`docs/prover/2026-08-07-night-order-adversarial.md:4`,
`docs/prover/2026-08-07-pushgate-intake-sweep.md:21`,
`docs/prover/2026-08-07-recovery-plan-adversarial.md:92` and four lines of
`docs/push-review/2026-08-07-the-night-order-and-the-morning-orders.md` are all dated 08-07 records
of a run that really returned 2,502. Records of something that happened are out of scope by the
census's own rule.

**"2502" — four hits, all correct.** `.live-spec/day1-census-checks.md:121` and
`.live-spec/day1-measures-2026-08-09.md:13` are day-1 starting measures, taken before the ten tests
went, and their whole purpose is to be the baseline day 14 measures against.
`docs/prover/2026-08-07-pushgate-intake-sweep.md:8` is a dated record.
`docs/audit/2026-07-28-rule-census.md:107` is the byte count 25028 and no hit at all.

**"Seventeen commits" — zero hits, in either case.** Both sites are cleared.

**"219" — correct everywhere it means the install measure, with one row half-done.** The day-1
baseline keeps it and should: `.live-spec/day1-census-delivery.md:7`, `:52` and `:94`, and
`.live-spec/day1-measures-2026-08-09.md:11` and `:38`. The two repaired sites now read 218.
`.live-spec/day3-opening-2026-08-09.md:11` keeps 219 under the heading "What the census counted",
which scopes it to day 1, and line 67 of the same page names the day explicitly, so the page is
consistent with itself. `.live-spec/handover-2026-08-09.md:43` and `JOURNAL.md:2471` still say 219
with no day beside them; see finding 6. Every other hit is the invariant code INV-219, a requirement
code R219.x, matrix row M-219, a line number in a census list, or a byte count, in
`.github/workflows/gates.yml`, `ARCHITECTURE.md`, `JOURNAL.md`, `MIGRATION.md`,
`PRODUCT_SPEC.md`, `PRODUCT_SPEC.index.md`, `.live-spec/day1-census-rules.md` and
`.live-spec/checkpoints/pending-draft-rows239-240.md`. None of those is the install measure.

## Findings

Ten findings stand. Three block. Findings 1 to 3 are new, raised by the repairs. Findings 4 to 10
are the first pass's non-blocking findings, unchanged except where a repair touched them.

### 1. Blocking — the resume file was rewritten whole, and it reds gate aa and the suite with it

`python3 guardrails/check-doc-findings-bound.py` fails: "NEXT_STEPS.md was repaired to zero and now
carries 6 finding(s). A cleared document stays cleared." That check is gate aa on
`guardrails/pre-push`, and its meta-test fails with it, so the suite is red at
`1 failed, 2489 passed, 2 skipped`. The single failure is
`tests/test_doc_findings_bound.py::TestDocFindingsBound::test_the_real_repository_passes`. Two push
gates refuse this state, gate aa directly and gate b through the suite.

The six findings are concrete. `scripts/spec-style-lint.py` reports one error at `NEXT_STEPS.md:18`,
code `[scissors]`, on "the list was drawn from summary tables instead of each rule's own text". Five
prose sentences run past the 25-word cap, the longest at 35 words: the ones opening
"**The campaign.**" (26), "So a verdict row is invalid" (29), "A worker brief that allows" (26),
"**The finding that decides the rest of the campaign.**" (30), "The number the plan was written
against" (31), "**What waits on him.**" (35) and "Repairing the install" (37) by my own count, of
which the census counts five as prose.

The cause is not the repair I was asked to verify. The commit-count sentence is one line. At 15:25,
six minutes after the other four repairs landed at 15:19, the whole live-state block was replaced —
1,602 bytes added, every paragraph rewritten, and the `## Forward queue` section deleted. The
committed copy of the file measures 0 findings under the same command. The rewrite is what reds the
gates.

The page's own line 52 reads "A page was rewritten whole where three lines needed changing. Change
what needs changing." It is the third of three habits the page names so the next session skips them,
and the page carrying it was rewritten whole in the act of writing it.

### 2. Blocking — the repair commit will red gate a the moment it lands

`guardrails/check-prover-record.sh` is gate a. Its third arm reads
`ARCH_COMMIT=$(git log -1 --format=%H -- ARCHITECTURE.md)` and refuses unless the newest commit under
`docs/prover/` is that same commit or a descendant of it. Today `ARCH_COMMIT` is 0ef204e and the
newest prover commit is 1f7fca7, which is a descendant, so the gate passes.

The repair commit changes `ARCHITECTURE.md`. `ARCH_COMMIT` becomes that commit, the newest prover
commit stays 1f7fca7, and 1f7fca7 is its ancestor rather than its descendant. Gate a reds and the
push is refused. The second planned commit does not help: this record goes to `docs/push-review/`,
which gate a does not read.

This is the 08-07 record's finding 1 recurring by the same mechanism. It is fixed by committing a
`docs/prover/` record — a fresh pass, or an addendum to one of today's three — in the repair commit
itself or in a commit after it. Note the standing objection at finding 8 of the 08-07 record: an
addendum re-arms the gate without a pass, which is a dodge the gate cannot tell from the real thing.

### 3. Blocking — the resume file sends the next session to a directory that dies with this session

`NEXT_STEPS.md:42-44` says the install repair "was written today, failed its own review on seven
findings, and its eight files sit set aside at
`/private/tmp/claude-501/-Users-sashaabramovich/0dc19ee5-4c7f-46c4-b792-e57a2390b08f/scratchpad/day3-work-set-aside/`".

The directory exists and holds exactly eight modified skill bodies, 252 KB in all. The path is a
scratchpad keyed to a session identity, and that identity is this reviewing session's own. It is
removed when the session ends. A tracked document, pushed to a remote, would tell every later reader
that eight files of finished work are recoverable at an address that no longer resolves — and the
work described is a change across eight shipped skill bodies, which is not cheap to redo.

This is queue row 586's class wearing different clothes: work held outside the tree, with only a
pointer standing between it and loss. Row 586 covers a worker discarding uncommitted work; nothing
covers a document publishing a dying address as the home of real work. Either the eight files come
into the tree, or the sentence names what was written and stops promising a location.

### 4. Major — the price page's other two measures were undone and only the install row was corrected

`.live-spec/day2-price-2026-08-09.md:20` reads "checks before a publish | 31 | 29 | yes" and line 21
reads "full test run | 447 s | 410 s | yes". Both rest on both cuts standing, and the pin-drift
restore of 11:22 put one back: thirty gate letters stand, and the suite carries its pin tests again.
The install row on line 23 was corrected in this repair pass; these two were not, and the page now
carries one corrected row beside two stale ones, which reads as though the other two were checked.

The handover names the restore and `JOURNAL.md:2518` records "The gate roster stands at 30". The
measured-price page, which is the artifact day 14 reads, still does not.

### 5. Major — the four headline numbers carry no command, in a file whose next section demands one

`NEXT_STEPS.md:13-15` opens with "Where it actually stands, in four numbers" and gives four, and
`NEXT_STEPS.md:24-26` gives three more. `NEXT_STEPS.md:60-64`, the section immediately below,
states that a number given to the person who decides what ships names four things, one of them the
command that produced it. None of these carries one.

Three I could verify and they hold: `cat skills/*/SKILL.md | wc -c` returns 410457, which is the
figure given for the eleven skill files; `wc -c skills/live-spec-base/SKILL.md` returns 66435; and
the 26 commits check out. Two I could not: "about 346 000 bytes" of text the campaign wrote about
itself names no file set — my own reading of the campaign's pages returns 376,759 bytes, which is
near enough to be the same measure taken over a different list, and there is no way to tell. "3.7 per
cent" depends on which nine rules the criterion leaves unprotected and on whether the denominator is
rule bytes or file bytes; the census holds per-rule sizes, so the figure is derivable, and the page
does not say from what.

The new block also fixes a miscount the first pass raised: it says "the eleven skill files", where the
day-3 page said ten. That is right — `skills/` holds eleven folders and `install.sh` copies every one.

### 6. Major — the correction table promises the next session will not inherit the mistakes, and two still stand

`.live-spec/handover-2026-08-09.md:34-46` lists seven claims this session got wrong beside their
corrected values, under "The next session must not inherit these mistakes." Two still stand
uncorrected in `JOURNAL.md`, which is the durable record and outlives the handover.
`JOURNAL.md:2468` reads "Thirty-five rules hold 48 387 bytes", against the table's 88 rules.
`JOURNAL.md:2471` reads "33 of the 66 installed files carry 219 references".

The repair pass makes the second worse rather than better. The table's own row at
`.live-spec/handover-2026-08-09.md:43` still reads "the install leaves 219 references pointing at
nothing", and its "what is true" column answers only the scope, not the value. The value moved to
218 in this same pass, in two other files. So the page that exists to hold the corrected numbers now
holds a stale one.

### 7. Major — the skill-review gate greens this range on a record three weeks old

`bash guardrails/check-skill-review.sh` prints "skill 'live-spec-base' carries a fresh review record
(docs/skill-review/2026-07-17-live-spec-base-build-pipeline.md)". This range changed
`skills/live-spec-base/SKILL.md` and filed `docs/skill-review/2026-08-09-live-spec-base.md` for it.
The gate matched neither the change nor the record written for it.

The day-2 review's blocking finding 3 predicted this gate would red once the rulebook edit committed,
and prescribed committing today's record. The record was committed and the gate never tested it. This
is the vacuous match `docs/push-review/2026-08-07-...:85` already named and rowed as 580. The
substance holds — the review exists, ran, and refused two drafts — but the gate proves nothing here.

### 8. Major — a blocking finding was closed by removing the symptom, and the cause is untouched

The day-2 review's finding 2 blocked on the suite redding over a leaked temporary log. Its cause is
`guardrails/check-tests.sh:32`, which makes its log with `mktemp
"${TMPDIR:-/tmp}/livespec-test-suite-log.XXXXXX"` — inside the suite's own leak-sweep prefix at
`tests/conftest.py:121`. A pre-push run killed mid-flight leaves the log behind and the next suite
run reds on it. The record's stated repair was a log name outside the swept prefix or a trap on any
exit. `guardrails/check-tests.sh` is unchanged. The red was cleared by deleting the stale files.

`JOURNAL.md:472` shows the same failure on 2026-07-18, filed then as an intermittent to handle
separately, and `.live-spec/day1-queue-for-striking.md:118` shows queue row 574 open on the class.
Third occurrence, still no reproduction. Nothing in this range records that the blocking finding was
closed by symptom removal rather than by its own repair, so the committed verdict "not fit to push
today" travels with one of its four repairs unlanded and unexplained.

### 9. Major — the renumbering swept every citation but the one that mattered, and the rewrite dropped the forward queue

`tests/test_opening_decision_sweep.py:1` still reads "(SPEC INV-302, R303.19..R303.23)". Requirement
303 renumbered in this range, and M-485 now claims R303.20 to R303.26. R303.19 is the handover's
provenance clause, the one the withdrawn gate held. So the file documenting the surviving half of
INV-302 sends its reader to five clauses, the first of which belongs to the half that went.
`scripts/session-extract.py` and `tests/test_session_extract.py` were both repointed in the same
commits. This one was missed. The day-2 review named it at its line 198 and called it cheap to fold;
it was not folded.

Beside it, the 15:25 rewrite deleted the `## Forward queue` heading and its six numbered items from
`NEXT_STEPS.md`, which pointed at rows 576, 166, 567, 566, 581 to 585, 558 to 565 and 532 to 546. The
four items under "Work needing nobody's word" replace some of them and not those. The rows themselves
survive in `ROADMAP.md`, so nothing is lost from the tree, but the resume file's forward pointer is
gone and the repair was described as a one-sentence change.

### 10. Minor — one skill miscount survives, and a stale queue row

`.live-spec/day3-opening-2026-08-09.md:9` and `.live-spec/day1-census-delivery.md:7` both read that a
person running `./install.sh` "gets the ten skill folders". `install.sh` copies every folder under
`skills/` and there are eleven. The 219 figure itself is unaffected — the census simulated the
install into a throwaway home rather than counting folders by hand — but the stated scope of the
measure is wrong in the page that declares it. `NEXT_STEPS.md:25` now says eleven, so the tree
disagrees with itself across two live pages.

`ROADMAP.md:198`, row 522, still reads "gate ab reds a handover that names no transcript, no extract
and no writer", and its Done-when still reads "rows M-483, M-484 and M-485 carry them with their
tests — MET". M-484 carries no test and gate ab does not exist. The row is landed and reads as
history, which is why this sits last.

`.live-spec/handover-2026-08-09.md:18` says "five decisions only he can make" and its own section at
line 111 lists six.

## Verdict

This delta may not be pushed.

The four findings that blocked the first pass are all genuinely closed, and I verified each against
the tree rather than against the repair's own account: the commit count, the handover's count and
range, the architecture's test figure, and the install measure. The number sweep is clean — every
surviving "2,502", "2502" and "219" is a dated measurement in a record of something that happened,
and "Seventeen commits" is gone from the tree.

Three findings block now, and all three arrived with the repair pass rather than with the range it
was repairing. The resume file was rewritten whole where one sentence was owed, and the rewrite reds
gate aa and the suite. The repair commit will red gate a, because it touches `ARCHITECTURE.md` and no
`docs/prover/` record follows it. And the rewritten resume file publishes a scratchpad path, keyed to
a session identity that dies with the session, as the home of eight files of real work.

None of the three is expensive. Restore the live-state block to a form the census reads at zero and
keep the corrected commit-count sentence; commit a prover record at or after the `ARCHITECTURE.md`
change; and either bring the eight set-aside files into the tree or stop the page promising an
address. Then re-run the suite and the push gate, and the delta is fit to push on their printed
result.
