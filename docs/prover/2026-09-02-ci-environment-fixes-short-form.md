# Prover record — 2026-09-02 ci-environment-fixes

PUSH-REVIEW

Range: effa3ecc..df5ff7d3
- df5ff7d3 docs/prover: short-form record for the CI-environment fixes, extend the full-push-range record's Range to include them
- 34f41718 Fix two CI-only environment defects gate b's server-side run surfaced
Files read: guardrails/check-config-health.sh (the whole INV-198 arm and its new scoping),
tests/test_lane_net_arms.py, tests/test_routing_preamble_hook.py, tests/test_config_health.py,
tests/test_wind_down.py, spec/parallel-lanes.md Requirement 85 criterion 5, the CI failure log
itself (https://github.com/happysasha18/live-spec/actions/runs/33578188215)
Checks run: `python3 -m pytest -q tests/test_lane_net_arms.py tests/test_routing_preamble_hook.py tests/test_config_health.py` — 54 passed. `python3 -m pytest -q tests/test_wind_down.py` under `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (the closest local reproduction of a runner with no git identity of its own) — 6 passed. A live scratch repo built with `git init -q -b master` (single worktree) against `guardrails/check-config-health.sh` directly — passes clean, matching the CI failure log's own "holds 'master' instead of main" case. A second scratch repo with a real second worktree and a deliberately drifted primary branch against the same script — still reds with the same message shape. Full local suite once more after both fixes: `python3 -m pytest -q` — 2737 passed, 4 skipped, 0 failed (the one `error` that run showed was this commit's own changes reading as still uncommitted at the time it ran, resolved by this commit landing).
Findings: `effa3ecc` passed every local gate and a full local suite run, then failed CI's gate b
(24 failed) on two root causes invisible on a machine whose own ambient git config happened to
already answer both gaps. (1) `q-804`'s new config-health INV-198 arm checked any git repo the
script ran inside, not only one with an actual lane to protect, so any unrelated test's own scratch
repo — built with a bare `git init` and no branch pinned — reddened once its default branch read
whatever the host machine's own git config produced: "main" locally, "master" on the CI runner.
Eighteen of the twenty-four CI failures trace to this one gap. (2) `tests/test_wind_down.py`'s own
`git()` fixture helper committed with no explicit author identity, inheriting whatever the running
machine's global `~/.gitconfig` happened to hold — real on a dev machine, absent on a fresh CI
runner, where `git commit` fails outright (exit 128). Six direct failures plus one cascading
`test_worker_restore_run_scope.py` leaked-temp-dir error from the aborted `setUp()`. Both fixed:
the INV-198 arm now only checks a repository actually holding more than one worktree (the only
shape where a lane could move main out from under the primary, the entire concern INV-198 exists
for); the wind-down fixture now sets an explicit `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL`/
`GIT_COMMITTER_NAME`/`GIT_COMMITTER_EMAIL`, the same pattern this project's other hermetic git
fixtures already use (`tests/test_lane_branch_road.py`'s `_git()`).
Blocking: none
