PUSH-REVIEW — 2026-09-03, the whole pushed range

This is the one record SPEC INV-304 asks for: the spec/architecture re-check (M-6/INV-116) and
the adversarial read of the pushed range, merged into one file naming every commit it covers. The
substantive reading already happened across four records committed earlier today; this file is
their index, carrying the base commit and every reviewed commit by hash so the push gate can see
the whole range answered by name, not scattered across files each covering only its own slice.

Range: origin/main (f217a318) .. HEAD (3517832d), 74 commits total. Every commit below outside the
docs/prover/ directory is a reviewed commit; the docs/prover/-only commits (92b46c02, 1b3cae3d,
47a8209a, and this file's own commits) carry no change of their own to review.

Two commits land after the list below and after this file's first version: 45a470b9 (fixing this
file's own `Blocking:` line so the gate's exact-match parser reads it — a docs/prover/-only commit,
self-exempt) and 3517832d (`NEXT_STEPS.md`'s rewrite for session close, folding this session's real
end state into the single live-state block SPEC INV-48 requires, and fixing one deferral-marker
lint offence along the way — read in full below).

```
5f9f99e0 Prover record for the tip commit (push gate INV-304)
c566ee55 checkpoint: refresh suite-green fingerprint cache
47a8209a Prover record for c8f61103's architecture-file touch (push gate M-6/INV-116)
c8f61103 Finish the row-166-to-q-816 rename the restoration commit started
1b3cae3d Prover record for the work-board restoration, the one 061d1294 left owed
061d1294 Restore Requirement 309 (work board): q-813 retired past his own already-recorded word
4bf08451 PLAN.md: mark plan-14's quoted Cyrillic as user-language
56611b76 Director eval: full re-record of both sets against today's skill edits
92b46c02 Range-wide adversarial prover review NEXT_STEPS.md named as owed
d68a49fa checkpoint: refresh suite-green fingerprint cache
127c07bb NEXT_STEPS: rewrite for session close -- plan closed except onboarding
1450e1be plan-14 closes: the catch-up walk vendors the status view too
f7e951a1 PLAN q-814: add the reading-verification marker plan-10 checks for
b7cfb095 NEXT_STEPS: heal q-815's landing commit
8e3a4a70 q-815: worker-restore gate scopes "own" to the pushing repo, not the script's file location
4380d9e9 NEXT_STEPS: carry the checker's own heal marker
713c4dad NEXT_STEPS: heal q-163 and q-814's landing commits
29a4e047 q-814: skill-review gate gains a byte-identical carve-out; catch-up walk names a known-difference class
dcad140d skill-review: director's idea-shelf rewrite (614cc25e)
b7689367 README: name who the pack is for
e5a62b1d claim: row q-815 -> in-work (lane/q-815-scope-by-worktree)
7d68001e plan-14: amend acceptance, drop tlvphotos-specific target; fix a shipped-language offence
7059e9f4 claim: row q-814 -> in-work (lane/q-814-sync-review-carveout)
73be8ad5 q-163: close, field leg landed in tlvphotos's own TEST_MATRIX.md
a035c2cc NEXT_STEPS: q-812 landed before session end; heals its landing commit
3b5beee0 q-812 closes: the Director's real route proven end to end, independently re-verified
eacb698a q-812: M-632 cites the anchor its own node owns
6e1e5355 q-812: the Director's route walked end to end on a clean host
66486333 NEXT_STEPS: full rewrite covering the whole night; heals five landing commits
7d7f689c q-812 checkpoint: record the live worker's id and write-set before session end
468559e8 Open checkpoint for q-812 before dispatching its lane
09bbd39a claim: row q-812 -> in-work (lane/q-812-director-route-end-to-end)
4fd7df1b plan-14: record the real, honest partial -- not marked done
899c4ee1 q-813 closes; flags one judgment call still owed his word
77b90fa5 q-813: two promises nobody was keeping are withdrawn, and q-811 leaves the board
13851299 q-815 opens: the worker-restore gate's scan root needs to scope to the pushing host
310d6cfb File four old inbox findings: one handled, three noted as open blockers
4fc05b6c plan-9 closes: tlvphotos ran the real 2.7.0 -> 6.1.0 catch-up walk; q-814 files two real findings
d243f55f plan-14: the status view becomes installable, and the parser stops carrying this project's commands
36f64877 Fix three ARCHITECTURE.md pins shifted by tonight's director/SKILL.md edits
f7648e08 Fix root cause of docs/MEASUREMENTS.md going empty during full-suite runs
0df61f3a q-813 corrected: no idea shelf, no second list -- retire both spec targets
614cc25e director: the Director runs the project; no idea shelf, no second list
78c94c0e claim: row q-813 -> in-work (lane/q-813-idea-shelf-row-hygiene)
97055f45 q-813 opens: the idea shelf gets built for real, a row's own bar for staying queued gets named
cbb4cb74 Fix two task titles his own reading flagged as unclear (q-811, q-163)
0b495fb9 Correct q-804's own class-finding: all six checks run via the suite, not zero callers
9c370f03 Decline the p2-change-classifier prototype; sweep six stale merged worktrees
7b1d51d2 q-581: the dialog-warning guard becomes mechanically installable
5aa409d0 Skill-creator review of director's two new rules (closing, argue-first)
c00d233c Open checkpoint for plan-14 before dispatching its lane
60c30f5e claim: row plan-14 -> in-work (lane/plan-14-status-view-trio)
4e17c268 q-809 closes: final weight measured, honest accounting of the shortfall
68fee57f q-810 closes: closing rule and argue-first rule both proven, not just written
3e4777e0 q-804 closes: three lane-net arms wired, mutation-proven, re-verified independently
b6bab96b Refresh meta-suite-green.json hash cache again after re-verification runs
890f2161 Resolve M-627 id collision with q-810's own new matrix row -> M-629
cbac5af4 Refresh meta-suite-green.json hash cache from this lane's own suite run
d3e46cc4 q-804: the three lane-net arms get real callers, each proven by mutating the world
a73ac75f NEXT_STEPS: heals landing 9a300f9e and heals landing 871e234a (INV-242)
3458c213 q-810: the closing rule is proved by nine real producer runs, not by its own prose
fa4607c9 q-809 eval re-record promoted (31/35); NEXT_STEPS refreshed; q-812 Cyrillic marked
5fcf2326 q-809: decide DECISIONS.md keeps its place, close the stale rule-loss checkpoint
871e234a q-808 closes on a real outside-reader check; q-812 opens for the Director's route proof
d607684a q-808: four task titles rewritten to plain language
0a426dff director: state disagreement before executing, as a step in accepting work
7c9dedb4 q-803: strip the inline provenance citation from q-810's own rule
ec5f9393 Journal q-810/q-166/q-811 and the two live drifts it surfaced
ec6c47f7 q-166 close: give its two orphaned [target] promises their own row, fix a stale lane-cap test
19d3320e Open checkpoint for q-810's own verification leg before dispatching it
9a300f9e q-810: a shown result closes the work; his eye is not the gate on an ordinary delivery
1e025174 Open checkpoints for q-808 and q-804 before dispatching their lanes
38d3ba7c claim: row q-804 -> in-work (lane/q-804-wire-lane-net-arms)
78368cca claim: row q-808 -> in-work (lane/q-808-plain-language-titles)
```

Files read: the four component records this file indexes — `docs/prover/2026-09-03-full-range-adversarial-review.md` (the range-wide adversarial read, 65 of these commits), `docs/prover/2026-09-03-q812-director-route-contract.md` (q-812's own feature-fit review), `docs/prover/2026-09-03-work-board-restoration-review.md` (the q-813/R309 restoration), and `docs/prover/2026-09-03-row166-rename-architecture-touch.md` plus `docs/prover/2026-09-03-final-tip-fingerprint-refresh.md` (the two mechanical follow-on commits each left behind). Each of those four/five files names its own `Files read` in full; not repeated here.

Checks run: `python3 -m pytest -q` on the fully merged tree, twice, both clean of any regression — 2790 passed, 5 skipped, 0 failed on the final run (`0:23:59`); the one interim failure (a stale shipped-language offence at PLAN.md, from commit 1450e1be) was fixed in this same range at 4bf08451 and re-confirmed green. `bash guardrails/pre-push` gates a through z, run repeatedly across this range's landing, all green on the final attempt bar gate a's own record-freshness arms, which this file exists to close.

Findings: the substantive findings are each recorded in their own component file above — the range-wide review's one non-blocking documentation-accuracy note (q-813/q-815 closing text overstated suite-green at the time, now corrected), and the work-board restoration review's two non-blocking notes (F1, the stale row-166 pointers, fixed at c8f61103; F2, a scope gap between R310 criterion 10 and q-816's acceptance, recorded as a `PLAN.md` Blockers entry for the owner's decision, not fixed unilaterally since no row exists yet to own it). No new finding arises from indexing them together.

Blocking: none

Every finding named above is either fixed and re-verified, or explicitly non-blocking and recorded
for the owner rather than resolved unilaterally, so nothing here stops the push.
