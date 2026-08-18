# Prover record — 2026-08-19 all-findings-in-one-run

PUSH-REVIEW

Range: 942b8cd2..59da3681
- beeb46e5 CI runs every gate in one pass instead of stopping at the first failure
Files read: .github/workflows/gates.yml, guardrails/check-ci-mirror.sh, tests/test_ci_mirror.py, guardrails/pre-push
Checks run: python3 -m pytest tests/test_ci_mirror.py -q — 13 passed; guardrails/check-ci-mirror.sh — OK (every local pre-push gate is mirrored in CI or a declared carve-out)
Findings: gates.yml stopped at the first red gate, so one CI run told the owner about one problem at a time, and each round trip cost about nine minutes; the fix and its two risks are set out below
Blocking: none

The owner's word: a red gate on GitHub should surface every finding in one run, not the first
one only, so fewer nine-minute round trips are spent finding out what else is wrong.

Root: gates.yml's `gates` job runs about twenty-five steps in a straight line. GitHub Actions
skips every step after a failing one by default, so the job stopped at the first red gate and
the rest went unrun and unreported.

What changed: every gate step (from "test suite (gate b, full ...)" through "gate ae — named
checks") now carries `if: ${{ !cancelled() }}`, so it runs even when an earlier step in the same
job failed — it only stands down if the whole workflow run itself was cancelled. The four setup
steps that come before the gates (checkout, setup-python, install pytest, install the external
product-prover canon) keep their default fail-fast behavior on purpose: without them the gates
run against no code, no pytest, and no external canon, and their being green would be a lie. The
sync-mirrors job's own step was left untouched — it depends on `needs: gates` at the job level,
and giving its single step `!cancelled()` would have let it attempt a mirror sync even after its
own checkout step failed, which is not what the owner asked for.

Two risks were checked and closed rather than assumed:

1. `continue-on-error` would have hidden the red steps behind a green job, so it was never used.
   No step in the diff carries it (`grep -n continue-on-error .github/workflows/gates.yml` finds
   nothing). GitHub Actions marks a job failed on any step failure unless that step has
   `continue-on-error: true`; `if: !cancelled()` only lets *later* steps keep running, it does not
   erase an earlier failure — the job stays red exactly as required.
2. gate u (`guardrails/check-ci-mirror.sh`, INV-210) reads gate letters out of gates.yml by
   matching `name:.*gate [a-z]` on each step's `name:` line alone; it never looks at `if:` or
   `run:` lines. Read before editing, along with tests/test_ci_mirror.py. The new `if:` lines sit
   on their own line under each step and do not touch any `name:` line, so the parser is
   unaffected. Verified after the edit: `python3 -m pytest tests/test_ci_mirror.py -q` (13 passed)
   and `guardrails/check-ci-mirror.sh` (OK) both still pass, and `python3 -c "import yaml; ...` was
   used to confirm gates.yml still parses and that exactly the 24 gate steps (not the 4 setup
   steps, not the sync-mirrors step) carry the new `if:`.

guardrails/pre-push was also read end to end for the same disease. It does not have it: every
gate call in the fast local chain is already wrapped `if ! "$GUARDRAILS/check-X.sh"; then
fail=1; fi` (or the python3 equivalent), under `set -euo pipefail` — a failing command inside an
`if` condition does not trigger `-e`, so the hook already runs every gate and only prints
"PUSH BLOCKED" once, after the whole chain, listing every gate that failed rather than stopping
at the first one. No change was made to guardrails/pre-push; it already does what the owner
asked for.

What was not done: no CI run against the real GitHub Actions runner was observed (no push was
made from this working copy; the coordinator pushes). The claim that the job still turns red on
a gate failure rests on GitHub Actions' documented step/job-conclusion semantics (a step failure
without `continue-on-error` fails the job regardless of `if:` conditions on later steps), not on
an observed red run in this repository's Actions tab.
