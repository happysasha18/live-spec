# Push review — 2026-08-07 the night order and the morning orders

PUSH-REVIEW

Range: 05a2ab9..0e1ccf5

The base is `origin/main` at 05a2ab9, the remote tip pushed 2026-08-06 19:26. The head is 0e1ccf5.
The range holds 47 commits. The brief named 7c3858a as the base; that commit sits inside the range,
not under it.

Reviewed commits: 47, listed below in three groups by who read them.

My own fresh read covered the nine commits after 3dedba7. Each is named with what it does.

- f6048da — suite repairs after the morning removals; M-146 repointed, spec table rebuilt, two previews atticked.
- 40c3c95 — adversarial defects D5 and D6 fixed; rows 578 and 579 minted; the leaked temp folder removed.
- e8921e8 — adversarial defect D1 fixed; the fence re-arms only when the new commit's parent is the recorded tip.
- d62ef94 — the fresh adversarial review's record filed for the push gate.
- 113c22a — the night's journal chapter; the resume file rewritten at the order's tail.
- 52cb0af — the review record's filing stamp corrected against its own commit's clock.
- f19b47f — session close: handover filed, two decisions brought on record, census re-measured.
- c150c1d — the wall-time row re-measured; the two rulebook-cut skill-review records filed.
- 0e1ccf5 — two more skill-review records filed; their findings fixed; the review gate's loose match rowed as 580.

The fifteen commits 537c6ae through 3dedba7 were already read by a fresh adversarial seat. That
record is committed at `docs/prover/2026-08-07-night-order-adversarial.md`. I did not re-review them.
I verified instead that its six defects were truly fixed, and by the commits it names.

Those fifteen: 3dedba7 5da174d 416f4c1 2d34616 c57b7c4 efc7d74 b1560a4 4dafeb8 c8a0d59 f7d4548
02f97ac d245b7b 6999523 b74444b 537c6ae.

Twenty-three further commits sit between the base and 7c3858a. They are in the push. Neither the
filed adversarial record nor this review read them. Finding 5 states that gap plainly.

Those twenty-three: 7c3858a df261c5 a58e424 3b3b65b b12b144 291db2a 4f6cf08 486b229 bedcb83
4afec74 68c00c7 98aa8f2 e2ea404 5c89a69 54dac6e 61789f6 16c575c 563d267 a718f9e 9457199 b06373c
9e0de7d 86a39fe.

Files read: docs/prover/2026-08-07-night-order-adversarial.md, docs/push-review/README.md,
guardrails/check-push-review.sh, guardrails/check-skill-review.sh, guardrails/post-commit,
guardrails/pre-commit, guardrails/rule-census.json, PRODUCT_SPEC.md (INV-48, R310 tables, glossary),
PRODUCT_SPEC.index.md (R310 rows), ARCHITECTURE.md (the budget table), TEST_MATRIX.md (M-146),
ROADMAP.md (rows 524, 570, 577, 578, 579, 580), DECISIONS.md, JOURNAL.md, docs/PROGRESS.md,
docs/handovers/2026-08-07-night-order-handover.md, docs/audits/2026-08-07-cost-map.md,
docs/audits/2026-08-07-number-rulings.md, docs/skill-review/2026-08-07-{build-pipeline,
live-spec-base,product-prover,spec-author}.md, tests/test_resume_digest.py,
tests/test_traceability.py, .live-spec/checkpoints/2026-08-07-night-order.md, and the nine
post-3dedba7 diffs in full.

Checks run: six, each with its result.

- `python3 guardrails/check-doc-findings-bound.py` — exit 0.
- `bash guardrails/check-skill-review.sh 2>&1 | tail -2` — OK for product-prover and spec-author. The full output greens four skills. Each OK names a record from 2026-07-17 or 07-18, not today's four. See finding 7.
- `python3 guardrails/check-landing-next-steps.py 2>&1 | tail -1` — OK: every landing commit in origin/main..HEAD refreshes NEXT_STEPS.md (INV-242).
- `python3 -m pytest -q tests/test_traceability.py tests/test_guardrails.py -x -q` — last line: `!!! stopping after 1 failures !!!`. The failure is `TestGateA_ProverRecord::test_real_repo_passes`. Re-run without `-x`: 1 failed, 270 passed, 2 skipped in 58.45s.
- `grep -rnE '100 lines|500-byte|six thousand'` over md, py, sh and json, excluding archives, attic, queue-archive and JOURNAL.md — three live hits. ARCHITECTURE.md:882, ROADMAP.md:200, and the prototype tree. See finding 2.
- `python3 -m pytest -q --collect-only | tail -3` — 2,502 tests collected. This matches the re-measured wall-time row exactly.

Findings: nine of my own, three of them blocking, plus the filed record's six defects all verified closed.

The six defects the filed adversarial record raised are all genuinely closed. I checked each against
the tree rather than against its commit message.

- D1 is fixed in e8921e8. `guardrails/post-commit` now reads line 1 of the fence file. It re-arms only when `git rev-parse HEAD^` equals that sha. The amend cost is stated in the hook's own header.
- D2 is fixed in f6048da. M-146 no longer cites the deleted `test_resume_digest_cap`. It names `test_template_states_the_law`, which exists.
- D3 is fixed in f6048da. PRODUCT_SPEC.md rows 7932, 8007, 8212 and 8218 now match PRODUCT_SPEC.index.md rows 87, 162, 367 and 373 character for character.
- D4 is fixed. No `/tmp/livespec-test-agent-inbox-*` folder survives, and JOURNAL.md:2385 records the removal.
- D5 is fixed in 40c3c95. The false sentence about the rewritten rulebooks is replaced by an accurate one naming the unpinned numbers.
- D6 is fixed in 40c3c95. Row 570 carries before and after bytes for both files and the nine-file remainder. The checkpoint holds no `State:` line.

Nine findings of my own follow. Three block.

1. The tip commit leaves the push gate's own first gate red. 0e1ccf5 changed PRODUCT_SPEC.md and committed no prover record after it. `check-prover-record.sh` reds, and the suite reds with it. The preceding commit c150c1d was green on this gate. The last commit broke it. Blocking.

2. A stale cross-reference survives the cap removals. ARCHITECTURE.md:882 still reads `NEXT_STEPS.md ≤ 100 lines (INV-48, already asserted)`. Its watcher column names a line-count test that reds past 100 lines. 2d34616 struck that cap from INV-48 and deleted the test. `tests/test_resume_digest.py` now holds one test, and it counts no lines. So the architecture asserts a struck number and names a watcher that does not exist. This also falsifies the filed record's section 7, which says no residual mention greps out. Blocking.

3. A regeneration the range's claims depend on sits uncommitted. `docs/PROGRESS.md` is modified but unstaged. The committed page publishes PRODUCT_SPEC.md at 704,495 bytes. The pushed spec measures 704,455. The gap is exactly the 40 bytes 0e1ccf5 removed from the glossary. The push would send a progress page whose headline number its own spec contradicts. Blocking.

4. ROADMAP row 580 carries an eighth cell. Every neighbour carries seven. The extra cell is row 577's Done-when, about the heal road, sitting on a row about the skill-review gate. Row 577 itself now carries six cells and no Done-when at all. It reads `landed` with nothing stating what landing meant. 40c3c95 moved the text off row 577 onto the freshly minted 579. 0e1ccf5 then moved it onto 580 instead of returning it home. Two commits touched the defect and neither saw it. No gate reads the table's column count.

5. The review's coverage is narrower than the push. The gate resolves the base to `origin/main`, which is 05a2ab9. Twenty-three commits sit between that base and 7c3858a. The filed adversarial record's range starts at 7c3858a, so it never read them. My brief scoped me after 3dedba7, so neither did I. They are named above so the gate can match. Their adversarial coverage rests on nothing.

6. One gate was cleared by an addendum rather than a pass. c150c1d changed ARCHITECTURE.md's wall-time row. `check-prover-record.sh` reads only the newest commit touching `docs/prover`. Appending two lines to the existing record re-armed the gate for that change. The change is a measured-number refresh the row's own law demands, and 2,502 tests confirms the figure. So the substance holds. The mechanism is still a freshness dodge available to any change.

7. The skill-review gate passes vacuously over this range. Its four OK lines name records from 2026-07-17 and 07-18. Four skills changed today and four records were filed today. None of the four filed records is what the gate matched. The gate matches any committed record containing the skill's name as a word. This is disclosed, not hidden: 0e1ccf5's message names it and mints row 580 for it.

8. The handover miscounts the rulebook cut. Line 53 reads `Two of ten are done`. The tree holds eleven skills. The handover's own following list names nine remaining, which makes eleven. Row 570 and the cost page both say eleven.

9. Struck-cap wording survives in two more live places, the same class as finding 2. PRODUCT_SPEC.md:2858 still asks for the resume file `capped` and `a short, capped current picture`. Its Context paragraph directly above was rewritten to the qualitative law. ROADMAP.md:200, row 524, still states the resume file carries a hard cap of 100 lines as present fact. Neither blocks alone. Both belong to row 576's unfinished sweep.

Blocking: three, each closed by the seat in the closing commit that ships this record.
- Finding 1, the tip commit reds the prover-record gate and the suite. closed: the review
  record's freshness addendum lands in the closing commit, on top of every spec change.
- Finding 2, ARCHITECTURE.md:882 asserts the struck 100-line cap and names a deleted test.
  closed: the row now states the digest law with its living watchers, and the two same-class
  sites the review named beside it (the spec's user story, queue row 524) are swept in the
  same commit.
- Finding 3, the regeneration of docs/PROGRESS.md is uncommitted and its published byte count
  is wrong. closed: the regeneration lands in the closing commit off the settled tree.
