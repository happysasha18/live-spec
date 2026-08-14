# Push review — main be4e4f0..b2fc1af — 2026-08-14

PUSH-REVIEW

Range: be4e4f0..b2fc1af (base be4e4f0, 33 commits, head b2fc1af)
Files read: full diffs of b2fc1af, 4e8df4c, acf0e3c, a3e54fb, 9d36c16, f03b425, 0b77c09, a388fc2 and 2718c69, each by an independent reviewer; the candidate segment via docs/prover/2026-08-14-candidate-repair.md and its in-mission adversarial review; the suite logs and mission digests those records name.
Checks run: clone-present full suite at b2fc1af, node set 2,552 identical to the 4e8df4c baseline; 16 red-first guard proofs for the settings-ladder split; protected-path scan over be4e4f0..b2fc1af, empty; check-doc-findings-bound.py, OK; merge, upstream and reflog verification of both branches.
Findings: ten non-blocking notes across the range, held in the review reports; one blocking finding on 2718c69, listed under Blocking.
Blocking: one standing finding, listed below.
- 2718c69 adds a gate-a stand-down for prose-only and scoped verdicts. The spec's R226 criterion 6 names deletion-only as the one exception; the commit amends no spec text; the verdict it adds exempts its own infra-only commit class — stands: the owner read the review and ordered this push on 2026-08-14 12:24. Today's push takes the full record road. The repair, an R226 amendment or a revert of the stand-down, is the first queued unit after this push.

## Coverage by segment

**b2fc1af — the settings-ladder split.** Independent review today: ALLOW-WITH-NOTES. Wording preserved byte for byte; 16 guards proven red on the moved state and green after; the measurement re-computed exact; node-id sets identical.

**4e8df4c — gate b's scratch-copy repair.** Independent review today: ALLOW. The defect reproduced red at the parent and green after; the copy rule uses the probe install.sh already carries.

**12f6f8b, 5d84040, 5e845cd, 450ee24 — the green-candidate repairs.** In-mission independent review: ALLOW-WITH-NOTES. Scope 3 files; no guard weakened.

**cd6ef7b, f09a876, c1139b0, 35f3977, db6c0d9, 1ebc6e8, f100c73, 5e214b2, 9e46503, 057c87b, 76d926b, c2a147d, 4bb6e65, 6b1f0c4, 6e9bfb3, 0d2082a, a1a43f6, 5724da7, 54f61fd, 08acf23 — the candidate.** Covered by docs/prover/2026-08-14-candidate-repair.md. The in-mission adversarial review returned REFUSE with three blocking findings; all three were closed before landing (35f3977, db6c0d9, 1ebc6e8). Four complete suites with complete node-id comparison: none introduced, 66 closed tracked-only, 61 clone-present.

**acf0e3c — the row-602 landing.** Adversarial read today: ALLOW-WITH-NOTES. Protected paths clean; the message matches the diff; the NEXT_STEPS miss it carried was healed by 5e845cd on the checker's documented road. Two non-blocking test-looseness notes, queue-row material.

**a3e54fb, 9d36c16, f03b425, 0b77c09, a388fc2, 2718c69 — the pre-campaign segment.** Adversarial read today: one ALLOW, four ALLOW-WITH-NOTES, one REFUSE (2718c69, under Blocking). The non-blocking notes are queue-row material after this push.

## Execution note

The merge of acf0e3c..b2fc1af ran in the judging seat's window on the owner's direct word of 2026-08-14 12:04. This record and the push were executed by a worker on the owner's word of 12:24. The day is recorded as a one-time deviation from the seat split and sets no precedent. The standing rule: the judging seat judges; merge and push run in an executor window.

## The commits

```
b2fc1af The settings ladder leaves the rulebook body and loads on demand
4e8df4c Gate b copies the pack's tree, not the repository installed inside it
12f6f8b The installer run stands down where no index names the skills
5d84040 The heal paragraph comes back under the human-prose cap
5e845cd The resume file records the 5.0.0 chapter's landing — heals landing acf0e3c1
450ee24 Gate f's known-red proof points at the file the split moved it to
cd6ef7b The record closes its own range: the four complete suites, and the two commits it was missing
f09a876 Row M-253 names the tests that now carry its law, not the three it used to have
c1139b0 The candidate-repair range gets its record: no prover mode ran, and the law that says so is cited
35f3977 The architecture stops promising line numbers inside another repository
db6c0d9 The published skills line count stops counting another repository's lines
1ebc6e8 Two checks of the CI authority model could pass over nothing; both now bite
f100c73 CI installs the external canon, pinned to a commit and verified — the fork is closed
5e214b2 The pack's skill count stops counting another repository as one of its skills
9e46503 Tracked documents are matched as written again; only the external canon reads flat
057c87b The tracked halves of the restructure-merge law stop hiding behind the clone guard
76d926b Eleven tracked-adapter anchors now hold on a bare checkout, ahead of the clone guard
c2a147d The CI failure names its remedies instead of a queue row no branch here carries
4bb6e65 The bare-checkout skip refuses to become CI's silent blind spot
6b1f0c4 Every tracked version home carries VERSION 5.0.0, and only the tracked ones
6e9bfb3 The version stamper learns the external-skill fence: another repo's release number is not ours to write
0d2082a The document census stops walking the external clone and records the adapter the pack actually ships
a1a43f6 tests: skip, never crash, on a bare checkout with no prover clone
5724da7 tests: re-pin prover content needles to the externalized canon's real homes
54f61fd tests+adapter: re-home pack anchors on the product-prover-pack adapter
08acf23 The dev-machine sync and the config-health arm learn the external-skill fence the installer already carries
acf0e3c MIGRATION gains the owed 5.0.0 chapter; the stale rule-30 pointer is dated; row 602 lands and rotates
2718c69 Gate a stands down on prose-only and scoped reach verdicts (P2-lite)
a388fc2 Traceability holds the external prover by its tracked contract on a bare checkout
0b77c09 The eleven prover-body assertions find their tracked homes
f03b425 skills/product-prover-pack enters the pack's seven rosters
9d36c16 The guardrail tests split into a fast unit lane and the sandboxed half
a3e54fb The external prover's adapter contract gets its first live fence
```

## Environment reds known at push time

The full suite at b2fc1af fails four host-local checks on the review machine. A fresh-HOME probe with the CI variables set passes all three underlying checks. Expected CI result on this push: green. CI itself runs after the push.

## Post-record commits

- c73c6e4 — this record itself; it touches the prover directory alone.
- 26f6850 — gate repairs on the gates' own remedies: six SKILL-REVIEW records and the README tree-count block rebuilt by its generator. The freeze baseline was re-blessed locally after the reviewed pin moves.
- c06af27 — the six records rewritten to name every substantive commit of the range per skill, with the verdict line where the gate reads it.
