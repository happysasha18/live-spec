# Prover record — 2026-08-07, the night order and the morning's two orders
Record filed by the orchestrator seat at 10:25 from the fresh reviewer's report, verbatim below.
(The filing first carried an invented 10:37 stamp; corrected against the filing commit's own clock.)
Addendum, 10:48: the push gate re-measured the full suite at 473 s over 2,502 tests; the
architecture's wall-time row re-set to the fresh figure per its own law, in this record's commit.
Reviewer: a clean-context seat on the strongest tier, distinct from the authoring seat (base rule 33).
Range: 7c3858a..HEAD. Verdict as returned: 6 defects, 8 recommendations. Disposition at filing:
all six defects fixed and landed (D1 e8921e8, D2 f6048da, D3 f6048da, D4 removed with its journal
line, D5 and D6 40c3c95); recommendations R5 and R11 stand as queue rows 578 and 579, R4 landed
with D1, R6 with 40c3c95, R7 rides row 570, R8 and R9 landed on the two pages, R10 rides row 576.

# Adversarial review of the night and morning work — 2026-08-07

Reviewer: fresh seat, clean context, per the owner's 01:06 order. Range reviewed: 7c3858a..HEAD
(15 commits, 537c6ae through 3dedba7). Sources read: docs/plans/2026-08-07-night-plan.md,
per-commit diffs, ROADMAP.md rows 166/496/568/569/570/572/574/575/576/577, DECISIONS.md On
record, .live-spec/checkpoints/2026-08-07-night-order.md, docs/audits/2026-08-07-cost-map.md,
-number-rulings.md, -number-census.md, the guardrail scripts and tests each fix touched, and the
old rulebook texts in the scratchpad. Three delegated attack lanes (rulebook spot-check, fence,
leak) ran with fresh context; their raw evidence is cited inline. No repository file was changed;
the only writes are this report and scratch experiments in clones under the scratchpad.

Full-suite state at review time: 1 known red (DEFECT 2 below); the suite log is
scratchpad/adversarial-suite.log (result line appended at the end of this file).

---

## 1. DEVIATION — plan vs commits

Checked: every block of the night plan against the commit list and diffs; every morning commit
against a dated word or a found defect.

- Block 1 (row 572) → b74444b at 01:54. Delivered as planned. Ledger entry flipped SOLVED
  (.live-spec/PROBLEMS.md, fence row, "SOLVED 2026-08-07 01:54").
- Block 2 (row 574) → 4dafeb8 at 02:59. Delivered; three byte-identical runs claimed and the
  leak check armed (verified by the leak lane).
- Block 3 (row 568) → 02f97ac at 01:58. Clean-written page, register lint claimed; repairs each
  hold a queue row (571, 572, 573, 574, 575, 570 — 571/573 landed pre-range at 00:30–01:34 and
  sit in docs/queue-archive/rotated-ROADMAP-2026-08.md, so the page's "landed the same night" is
  true).
- Block 4 (row 569) → d245b7b at 01:58. Requirement 310/INV-314 in PRODUCT_SPEC.md, pipeline
  report shape carries the accounting line, string test in tests/test_traceability.py:3329.
- Block 5 (row 570) → f7d4548 (prover) + b1560a4 (base), with the declared "as far as it goes"
  stop. The clause covers the fewer-files-than-worst-first outcome. BUT the plan's own proof
  clause — "before and after numbers on the row" / "What remains stays on the row with its
  measurements" — is not met by the row (see finding D6).
- Block 6 → this review.
- Unplanned night step c8a0d59 (prose-cap repairs): roots in the standing r08 sentence law; the
  checkpoint's 03:01 update declares it. Acceptable under the plan's own out-of-plan-announce
  rule — but it shipped a stale cross-reference table (finding D3).
- Morning additions all trace: efc7d74 → his 09:11 word (DECISIONS.md:53); c57b7c4 + 2d34616 →
  his 09:16 word (row 576 cites the Russian quote); 416f4c1 + 5da174d → a defect found 09:47 at
  the seat's own acceptance run; 3dedba7 + b1560a4 → the night plan's own tail. Nothing found
  that traces to neither a dated word nor a found defect.
- Plan close says "The full suite runs at each landing." From 2d34616 (09:50) onward the suite
  has one red (D2), so the last three landings (2d34616, 5da174d, 3dedba7) did not hold that
  clause. Counted under D2.

Findings here: D2 (partial), D6 (partial). Everything else holds.

## 2. HIS DECISIONS — the three ~01:10 answers

Checked: the cost page verdict column, tonight's new texts, the removal commits.

- No numeric caps: the cost page's verdicts (docs/audits/2026-08-07-cost-map.md:17,18,20,22)
  carry his standard verbatim; no cap survives on the page. The struck 360-second budget is
  named dropped (line 38) and the page keeps measured numbers.
- Test-plan timing: restated as the settled rule (line 20, and question 4 at line 68). Matches
  DECISIONS.md:70.
- No self-invented standards in the night's own new texts: Requirement 310 carries no numbers;
  the heal road's 7-hex minimum is git's own short-sha convention (derived); the fence and leak
  fixes introduce no numbers.
- RECOMMENDATION R9: the cost page's step-8 price "roughly 40–60 minutes" (line 23) names no
  source while the page vows "Every number below names its source" (line 4); and the repair
  list still tells the morning reader rows 574 and 570 are "in work tonight" (lines 52, 55)
  though 574 landed at 02:59 and 570 reads queued. His read is the row's last open box; the
  page should read true at that read.

## 3. THE FENCE FIX (row 572, b74444b)

Mechanism verified in scratch clones: state in the untracked `.live-spec-fence` (sha + arming
session's token, guardrails/fence-refresh.sh:15-20); pre-commit blocks on sha mismatch, knowing
nothing of tokens (guardrails/pre-commit:61-72); post-commit re-arms to current HEAD when the
committer's token matches line 2 (guardrails/post-commit:34-50).

- Two honest windows racing: HOLDS. Same-clone commits serialize on .git/index.lock; partial
  fence reads fail closed.
- **DEFECT D1 — post-commit re-arms past commits the session never verified.** Reproduced step
  by step: A arms and commits; B (foreign token) commits first-through (fence goes stale at A's
  sha); A commits with `--no-verify` — pre-commit's block is skipped but post-commit still runs,
  token matches, and guardrails/post-commit:46 re-arms to a HEAD that contains B's commit. A's
  next normal commit exits 0. The block for B's move never fires for anyone. Before this fix the
  stale fence still caught B at the next honest commit — the fix regresses that guarantee. The
  same root (re-arm never checks that the new HEAD extends the armed tip) also lets a background
  child that inherited the session's token (CLAUDE_CODE_SESSION_ID rides the env — verified
  live) absorb its own commits on a shared tree unseen; the workers-use-worktrees rule mitigates
  but no hook enforces it. Class fix: re-arm only when `git rev-parse HEAD^` equals the recorded
  line-1 sha (amend carve-out), which also closes the commit-vs-post-commit timing window. A
  test pinning the --no-verify-after-foreign sequence rides the fix.
- Tests: the demanded foreign-blocks pin EXISTS — tests/test_guardrails.py:677
  (test_foreign_session_commit_still_blocks), plus own-two-commits (:652), no-token no-re-arm
  (:707), install ships the hook (:725).
- RECOMMENDATION R4: no test exercises the CLAUDE_CODE_SESSION_ID fallback branch, the
  empty-recorded-token case, or fence-file corruption (fails closed today, unpinned); after a
  session restart the old token makes every second commit block again with no hint in the
  message that the token is the cause — the row-572 pain returns on every /clear with a mute
  diagnosis.

## 4. THE LEAK FIX (row 574, 4dafeb8)

Root cause confirmed from the diff: test_deletion_only_push.py's bounded pre-push runs SIGKILL a
process group at 3s; the nested full pytest run inside bare check-tests.sh was mid-
test_agent_channels (mkdtemp in setUp, teardown skipped by SIGKILL); a second nested instance
opened a detached group killpg cannot reach. Fix: sweep by the shared SUITE_TEMP_PREFIXES
(tests/conftest.py:121) + NESTED_MARKER skip (test_deletion_only_push.py:66,249). The nested-
marker mechanic held under attack; 14 tests pass with temp-dir count unchanged.

- **DEFECT D4 — a pre-fix leaked folder still sits on disk and the check grandfathers it.**
  /tmp/livespec-test-agent-inbox-g60jly0r (mtime Aug 7 00:00) exists now, while row 574's text
  says the old folders were removed 2026-08-07 with their names in the journal. The session leak
  check (tests/conftest.py:129-136) diffs against a before-snapshot, so a pre-existing leak is
  invisible forever: "three consecutive runs unchanged" is true while the temp dir is not clean.
  Fix: remove the folder, journal the removal.
- RECOMMENDATION R5 — the sibling class the sweep cannot see: non-prefixed temp artifacts.
  NamedTemporaryFile(delete=False) with default tmp* names at tests/test_build_index.py:49,65
  and tests/test_ci_mirror.py:61,84 (plus test_every_gate_can_fail.py:50, test_net_meter.py:111)
  sit alphabetically adjacent to the proven kill point; the same kill window orphans them and
  both the per-test sweep and the session check filter on suite prefixes, so that leak would be
  silent. Nothing enforces prefix use (tests/test_suite_hygiene.py:39-43 only string-checks the
  fixture exists). Root fix: a hygiene gate forcing suite temp artifacts onto the prefix list,
  or pytest tmp_path. Also: the third bounded call (test_deletion_only_push.py:258, 15s kill)
  has no _before/_clean_new pair — a stand-down regression would kill deeper with no sweep.

## 5. THE GROUNDING LAW (row 569, d245b7b + c8a0d59)

Requirement 310 (PRODUCT_SPEC.md:7808-7837, eleven criteria) covers everything the row's three
dated words demand: root named with stage, rule, estimate (1); root definition (2); no rootless
block (3); machinery never a root, the carried instruction named instead (4, 5); report lines
open with the root, missing = defect (6); out-of-plan stop and announce (7, 8); the plan home
and the accounting line (9-11). The string test (tests/test_traceability.py:3335) reds when
either home drops the law's core: six spec needles including the full root definition, three
pipeline needles including the accounting line, plus the M-545 matrix pin. Judged real, not
comment-anchored.

- **DEFECT D3 — the spec's own invariant table was left at the pre-resplit numbering and now
  contradicts the generated index.** c8a0d59 resplit Requirement 310 from 7 to 11 criteria and
  its message says "index regenerated" — true for PRODUCT_SPEC.index.md (lines 87, 162, 367,
  373 carry R310.6 / R310.11 / R310.9-10 / eleven codes), false for PRODUCT_SPEC.md's own
  table: line 7933 still maps INV-28 → R310.4 (the report-line criterion is 6), line 8213 maps
  INV-308 → R310.6 (the plan-home criteria are 9 and 10), line 8008 maps INV-103 → R310.7 (the
  accounting criterion is 11), and line 8219 gives INV-314 seven codes where eleven exist. Two
  published tables in one tree now disagree; no gate reads them against the inline tags. Same
  class as the recorded matrix-drift-at-landing lesson. Fix: correct the four PRODUCT_SPEC.md
  rows (the index already has the right values); queue a consistency check inline-tags ↔ both
  tables.
- RECOMMENDATION R6: the spec-side needles pin criteria 1-4 only; dropping the out-of-plan stop
  (7, 8) or the accounting criterion (11) from the spec alone leaves the test green (the
  accounting is pinned only through the pipeline home). Add one needle for each.

## 6. THE RULEBOOK CUT (row 570, f7d4548 + b1560a4)

Second-verifier spot-check, twenty rules chosen differently from the first verifier (their
picks read from row570-prover-verify.md / row570-base-verify.md first): ten per file, favoring
rules with numbers, exceptions, and paths. Result: **20 KEPT, 0 WEAKENED, 0 LOST** — including
the delta-scoped defect exception (prover new:177-180), the quantifier re-verify sweep
(new:294-302), the declared-laws sweep with its three enforcers (new:536-564), the ledger rule's
full state machine (base new:324-343), the four lock mechanisms (base new:366-378), and the
earned-message ban with its two justifying situations (base new:517-526). Both first-verifier
findings are confirmed repaired in the committed text (prover worked instance at new:641-643;
base rule-21 disjunct at new:363-364).

- Census: product-prover at 0 (ceiling 0 held). live-spec-base at 74, down from the old text's
  92, ratchet recorded and honored (guardrails/rule-census.json) — no record claims zero for the
  base, so no claim is broken; stated here so nobody reads "cut finished" as "census zero".
- Needle tests: 56 files referencing the two skills ran — 768 passed, 1 failed, and the one red
  is NOT a rulebook needle (it is D2, collateral of 2d34616).
- Installed copies ~/.claude/skills/{product-prover,live-spec-base}: byte-identical to the repo
  (diff -r clean). The base body carries exactly 35 numbered rules, matching its own claim.
- RECOMMENDATION R7: editions/product-prover/ still holds the pre-cut text. scripts/
  sync-mirrors.sh will refuse it by name at the next mirror publish (edition older than skill —
  the guard is loud, not silent), but the mirror stays on old text until the edition is rebuilt.

## 7. THE CLASS QUESTION — one sibling hunt per repair

- Row 572 claims "the fence charges the session for its own work": instance fixed, but the fix
  opened the sibling described in D1 (re-arm past unverified commits).
- Row 574 claims "the suite leaks a temp folder": the named class (prefixed suite artifacts) is
  genuinely closed — sweep generalized to the shared prefix list, nested recursion cut at its
  root. The wider class "artifact a timed kill can orphan" has the living sibling R5
  (non-prefixed tmp* files) and the on-disk instance D4.
- Row 569: no sibling found — law 7 (session rules), Requirement 310, and the pipeline report
  shape state the same law in all three homes.
- Row 576 first batch: the cap removals swept all cells (spec, skill, guardrail, tests, docs
  — checked for the 500-byte and 100-line families; no residual mention greps out), except the
  editions/ copies (R7) and the broken matrix cell (D2).
- Row 577: the heal road covers all three of the night's misses; the checker output shows
  exactly three warns and OK.

## 8. THE QUEUE — statuses vs true state

- Rows 166 and 496: *queued* 2026-08-07 — true (nothing runs on them; re-queue commit 6999523
  names the lane cap as the reason).
- Row 575: *queued*, class small — matches the mint and the correction.
- Rows 569/572/574/577: *landed* — each has its landing commit and its Done-when satisfied
  (577's fixtures prove heal-passes / wrong-sha-reds / backdated-heal-counts-nothing in
  tests/test_landing_next_steps.py, +110 lines).
- Rows 568/576: *in-work* — true; both wait on his read.
- **DEFECT D6 — row 570's published state hides landed progress and drifts from its frozen
  statement.** The row reads bare *queued* with no mention that two files landed (f7d4548,
  b1560a4), no per-file before/after numbers, and no remainder list — while the night plan's
  Block-5 proof clause promises "before and after numbers on the row" and NEXT_STEPS.md:22-24
  asserts the remaining files "stay on the row with the before-measurements" (the row carries
  only the original coarse sentence). The checkpoint's frozen statement adds "State: two files
  done overnight; the shared rulebook finishing" — stale since 09:45 (the shared rulebook is
  landed, not finishing), and at its own validation time (09:20) only ONE file's cut had landed.
  A statement spoken letter for letter must not carry a mutable State line. Fix: record the two
  landed files with their before/after byte counts and the remainder list on row 570; move the
  State sentence out of the frozen statement.

## 9. THE NUMBER RULINGS (row 576 pages)

Checked: every group of docs/audits/2026-08-07-number-rulings.md against the census and the
tree.

- **DEFECT D5 — group 6's claim about the rewritten files is false.** The page says of the
  rulebook micro-numbers: "The ones already rewritten tonight kept only what a suite test pins"
  (line 86). The rewritten prover keeps "scans in 30 seconds / reads carefully in 5 minutes"
  (skills/product-prover/SKILL.md:116), "10–15 seconds" (:120), and the "5–8 sentences" opening
  cap (:459) — and no test pins any of those phrases (grep across tests/ returns nothing; the
  only match, tests/test_delegation_trigger_no_size.py:78, treats "30 seconds" as benign prose
  it must NOT flag). The page goes to his eyes this morning; the sentence must be corrected or
  the numbers cut.
- RECOMMENDATION R8 — the "derived" rulings his read should be pointed at, since the census's
  own closing section contradicts them: the census (2026-08-07-number-census.md, closing) calls
  the four doc-bounds byte ceilings "squarely the size-cap class his ~01:10 word rejected" and
  lists spec-ratchet's 207.2 bytes-per-criterion beside them, while the rulings page files both
  under "Derived, kept" (lines 25, 30). The ratchet's defense (measured, may only fall) is real
  but it remains a numeric bound on spec prose per criterion — the same substance as the struck
  500-byte cap, differing in mechanism; and inside the "derived" doc-bounds ruling hides an
  underived convention, the "roughly a hundred kilobytes" of headroom (doc-bounds.json comment)
  whose own provenance the rulings never state. Both pages ship to him together; the rulings
  page should name the tension instead of ruling past it.
- RECOMMENDATION R10 — no per-number verdict exists. The rulings page claims "Each of the 144
  was judged" yet gives groups with representative homes only, and the census's columns carry
  provenance leads, "not the ruling itself" (its own words). Sample: census #1 (the 12-item
  waiting-board demotion cap, check-board.py:51) fits no group — it is not machinery (it shapes
  what he sees), not a listed design constant, not struck. Row 576 is in-work, so incomplete is
  legal — but the rulings page's "each was judged" sentence overstates until a number→group
  mapping exists.
- Census miss found: the same prose targets ruled in group 6 live also in
  editions/product-prover/SKILL.md:117,121 — editions/ is absent from the census's swept
  families (its count section lists guardrails/tests/scripts/hooks/templates/skills/spec/docs
  only). One more miss candidate checked and cleared: adopt/install-ratchet.sh's max_waivers=0
  is census #52's zero-waiver cap. Folded into R7/R10.

## 10. THE HEAL ROAD (row 577, 5da174d)

Mechanism: a later commit in BASE..HEAD that touches NEXT_STEPS.md and says "heals landing
<shortsha>" (≥7 hex, prefix-matching the missed landing) with committer time not earlier than
the landing's, converts the red to a named warning (guardrails/check-landing-next-steps.py:
210-232, 281-300).

- Whitewash attempts: a heal cannot predate its landing honestly — the landing's sha is
  unpredictable before the landing exists, so the backdate road is closed by arithmetic, not
  just by the timestamp check. A heal commit that touches NEXT_STEPS.md trivially while naming
  every sha would still leave the misses on record as warnings — the law's visibility survives.
  The three healed shas in 5da174d's title prefix-match the three true misses exactly
  (b74444b5…, 69995232…, 4dafeb8c…), and the checker run shows three warns + OK; d245b7b and
  02f97ac needed no heal (their rows' NEXT_STEPS discharge came in-range).
- RECOMMENDATION R11 — the norm has no counter. Nothing bounds heals per push range, so a
  session could stop refreshing at landings entirely and bulk-heal before every push; the
  strict same-commit law would quietly become a same-push law enforced only by unratcheted
  warnings. Cheap teeth: the checker warns-and-counts, and a range where every landing healed
  (none same-commit) reds, or the count lands in the push report.

## 11. FROZEN STATEMENTS vs QUEUE ROWS

- "what a feature costs" (row 568): statement and row agree (page, demanded-by, verdicts,
  repairs as rows, his read open). The page's title still reads "Where the time goes…" — the
  name the first validation round rejected lives on as the page's headline; harmless to the
  row, worth aligning when he reads it (folded into R9).
- "the rulebook cut" (row 570): drift found — see D6.

---

## Verdict roll-up

DEFECTS (must fix before push):
- D1. Fence post-commit re-arms past unverified commits — reproduced: a --no-verify commit after
  a foreign first-through absorbs the foreign move; regression vs the pre-fix fence
  (guardrails/post-commit:46). Fix: parent-sha check before re-arm + pin the sequence.
- D2. Suite is red now: 2d34616 deleted test_resume_digest_cap while TEST_MATRIX.md M-146 still
  cites it (test_matrix_built_rows_name_real_tests fails, reproduced); the last three landings
  carried the red against the plan's suite-green-at-each-landing clause. Fix: repoint M-146.
- D3. PRODUCT_SPEC.md's invariant table still holds pre-resplit R310 numbering and contradicts
  PRODUCT_SPEC.index.md (lines 7933, 8008, 8213, 8219 vs index 87, 162, 367, 373).
- D4. /tmp/livespec-test-agent-inbox-g60jly0r still on disk against row 574's removal claim;
  the diff-based leak check grandfathers it forever.
- D5. Rulings page group 6 falsely claims the rewritten skills kept only suite-pinned numbers;
  the rewritten prover keeps three unpinned micro-number families.
- D6. Row 570's row/frozen-statement/NEXT_STEPS triple drifts from the true state: landed
  progress invisible, promised before/after numbers absent, "State:" line stale.

RECOMMENDATIONS (queued): R4 fence test gaps + restart-staleness diagnosis; R5 non-prefixed
temp-artifact sibling class + unswept 15s kill; R6 grounding-law needles for criteria 7-11;
R7 stale editions/product-prover rebuild; R8 point his read at ratchet/doc-bounds vs census
contradiction + headroom provenance; R9 cost-page staleness at his read + unsourced 40-60min +
page title; R10 per-number verdict mapping; R11 heal-road counter.

VERDICT: 6 DEFECTS
