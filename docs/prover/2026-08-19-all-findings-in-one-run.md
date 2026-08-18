# Prover record — 2026-08-19 all-findings-in-one-run

PUSH-REVIEW

Range: ed8e1da0..3b14d744
- c43b700e Merge origin/main: two hand-kept lists catch up with yesterday's two culls
- 6f33bc27 The record carries the pin's red canon and the floor decision
- abd4246d Move the external product-prover pin off a canon that was red since Aug 13
- 2fefd844 The record names the pushed range by its hash
- 59da3681 The record carries the CI gate fix that stops turnarounds at the first red
- beeb46e5 CI runs every gate in one pass instead of stopping at the first failure
Files read: .github/workflows/gates.yml, guardrails/check-ci-mirror.sh, tests/test_ci_mirror.py, guardrails/pre-push, skills/product-prover-pack/SKILL.md
Checks run: python3 -m pytest tests/test_ci_mirror.py -q — 13 passed; guardrails/check-ci-mirror.sh — OK (every local pre-push gate is mirrored in CI or a declared carve-out); python3 -m pytest tests/test_prover_adapter_contract.py -q — 18 passed, 1 skipped; python3 -m pytest tests/test_config_health.py -q — 33 passed; python3 -m pytest tests/test_readme_stance.py -q — 5 passed; gh api repos/happysasha18/product-prover/commits/main and .../git/refs/tags/v1.3.1, read live, not taken on say-so
Findings: gates.yml stopped at the first red gate, so one CI run told the owner about one problem at a time, and each round trip cost about nine minutes; the external product-prover pin also named a commit that had been red on its own CI since 2026-08-13, so gate b's proof rested on a canon that could not prove itself; both are set out below
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

A second finding, direct consequence of the first: the "install the external product-prover
canon" step that gate b's proof depends on was pinned, both `--ref` and `--expect-commit`, to
`94d36454d55438951311d302fc86adba33123868` — a commit of happysasha18/product-prover that had
been red on its own CI since 2026-08-13 (a stale `-standalone` version-format check in
`scripts/validate.py`, left behind when 1.3.0 dropped the `-standalone` suffix and the check was
never updated). Gate b's proof rested on a canon that could not prove itself. The coordinator
named a replacement hash, `540914da05f77ec1ec98a75d3d9ba61ee5cfd3ab`, and asked that it be
verified rather than trusted; verifying it (`gh api repos/happysasha18/product-prover/commits/main
--jq '.sha'` and `gh api repos/happysasha18/product-prover/git/refs/tags/v1.3.1 --jq
'.object.sha'`, cross-checked against the tag's own commit field) turned up a different hash,
`540914d740e4f6178d1a69f324c43a0ae871e066` — the two strings diverge at the 8th character. Both
`main` HEAD and the `v1.3.1` tag agree on `540914d740e4f6178d1a69f324c43a0ae871e066` live from
the API, so that is the hash both `--ref` and `--expect-commit` now carry, not the one named in
the message. `grep -rln "94d36454"` over the tree found the pin named nowhere else — one spot,
now moved.

Whether `skills/product-prover-pack/SKILL.md`'s `requires: product-prover >= 1.3.0` floor should
rise to `>= 1.3.1`: no. Release 1.3.1's own log (`gh api
repos/happysasha18/product-prover/compare/v1.3.0...v1.3.1`) shows it fixed the external
repository's own CI — `scripts/validate.py` accepting a plain semantic version instead of
demanding the retired `-standalone` suffix, `evals/sample-spec-rubric.json`'s key rename, and
README/CHANGELOG housekeeping. None of that touches what the pack binding page depends on: the
mode-name table, the pack paths, the record home and shape, or anything else
`product-prover-pack/SKILL.md` reads from the prover's own SKILL.md. The floor stays at 1.3.0
because nothing the pack binds to changed; raising it on the version number alone, with no
functional reason, would be exactly the mistake the owner warned against.
