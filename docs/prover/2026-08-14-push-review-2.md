# Push review — main 9c4cd0b..d4e0e2f — 2026-08-14, second range of the day

PUSH-REVIEW

Range: 9c4cd0b..HEAD (base 9c4cd0b; one reviewed commit, d4e0e2f; this record's own commit follows it and touches the prover directory alone)
Files read: the full diff of d4e0e2f, read by an independent adversarial reviewer running its own reproductions; the mission digest at /private/tmp/live-spec-night/ci-fix-digest.md; the red-first and full-suite logs under /private/tmp/live-spec-fix/.
Checks run: red-first reproduction of CI run 31801225761's failure mode — 8 failed in an old-way scratch copy under the CI variables, 28 passed in a new-way copy; the realpath edges for a linked worktree and the /tmp symlink, held in all tested layouts; the clone-absence teeth re-proven in a copy carrying no clone — 8 failed, so no guard widened; the 4e8df4c fence pair and the 12f6f8b installer stand-down, each under its own guard; one clone-present full suite — 4 failed, 2,547 passed, 1 skipped, 19m 55s.
Findings: three non-blocking reviewer notes, held in the review report; the one skip is tests/test_guardrails.py::TestGateB_Tests::test_broken_suite_fails, lawful under the row-573 content digest — the stored value equals the digest at d4e0e2f, the store is gitignored, so CI re-fires that test on every run; the four failures are the known machine-local checks.
Blocking: none

## What this record covers

Commit d4e0e2f teaches gate b's scratch copy to carry any nested repository whole, its .git included, excluding only __pycache__ and the pack's own root .git, identified by realpath. This closes CI run 31801225761's failure mode: clone-dependent tests inside the scratch copy failed under the CI variables because the copy carried no clone. Independent review verdict: ALLOW-WITH-NOTES, every check reproduced by the reviewer's own commands. The four tolerated machine-local failures and the certification road are unchanged from docs/prover/2026-08-14-push-review.md.

## Execution note

The push runs in an executor window; the owner's pasting of the executor brief is the order. The judging seat wrote the brief and this record on 2026-08-14 after the review verdict.
