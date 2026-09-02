# Prover record — 2026-09-02 ci-environment-fixes

PUSH-REVIEW

Range: effa3ecc..9b06b553
- 9b06b553 Fix third CI-only defect: INV-198's worktree read reds loudly instead of standing down
- 323dc6a3 docs/prover: extend the CI-fixes record to cover 10b2a208, name the open hypothesis honestly
- 10b2a208 Ignore __pycache__/*.pyc; add safe.directory to INV-198's worktree reads
- df5ff7d3 docs/prover: short-form record for the CI-environment fixes, extend the full-push-range record's Range to include them
- 34f41718 Fix two CI-only environment defects gate b's server-side run surfaced
Files read: guardrails/check-config-health.sh (the whole INV-198 arm, its scoping, its
`safe.directory` reads, and now its `mktemp`-captured error path), tests/test_lane_net_arms.py,
tests/test_routing_preamble_hook.py, tests/test_config_health.py, tests/test_wind_down.py,
.gitignore, tests/test_dialog_warning_guard.py, spec/parallel-lanes.md Requirement 85 criterion 5,
matrix/parallel-lanes.md row M-624, both CI failure logs
(https://github.com/happysasha18/live-spec/actions/runs/33578188215,
https://github.com/happysasha18/live-spec/actions/runs/33581346738)
Checks run: `python3 -m pytest -q tests/test_lane_net_arms.py tests/test_routing_preamble_hook.py tests/test_config_health.py` — 54 passed. `python3 -m pytest -q tests/test_wind_down.py` under `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (the closest local reproduction of a runner with no git identity of its own) — 6 passed. A live scratch repo built with `git init -q -b master` (single worktree) against `guardrails/check-config-health.sh` directly — passes clean, matching the CI failure log's own "holds 'master' instead of main" case. A second scratch repo with a real second worktree and a deliberately drifted primary branch against the same script — still reds with the same message shape. `bash -n guardrails/check-config-health.sh` after the `safe.directory` addition. A manual reproduction of a stray `.pyc` colliding with `tests/test_dialog_warning_guard.py`'s own one-file-in-the-tree proof, cleared by the new `.gitignore` line. Mutation proof of the loud-failure fix in `9b06b553`: a fake `git` wrapper on `PATH` that fails only the `worktree list` subcommand with git's own "detected dubious ownership" message, run against `check-config-health.sh` — with `9b06b553` reverted (the prior `2>/dev/null`, silent-stand-down shape) the new test reds; with the fix applied, it passes and the arm's JSON names `worktree list failed` and quotes git's stderr. Full local suite three times across this range (before 10b2a208, after it, after 9b06b553): `python3 -m pytest -q` — 2737 passed, 4 skipped, 0 failed; then 2736 passed, 6 skipped, 0 failed twice more (the skip count shift is an unrelated environment-dependent skip elsewhere in the suite, not this range's own tests).
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

The second CI run (33581346738, on `e567c5f9`) confirmed both fixes above worked — neither failure
signature recurred — but 3 of `test_lane_net_arms.py::TestConfigHealthPrimaryTreeArm`'s own tests
(`test_a_detached_primary_tree_reds`, `test_primary_tree_drifted_off_main_reds`,
`test_the_read_is_of_the_primary_tree_not_the_invoking_one`) still failed, all with the same shape:
the arm read zero worktrees and stood itself down instead of reddening a deliberately drifted or
detached primary tree. Checked against the FIRST CI run's own log and confirmed these 3 failures
were present there too, before this range's scoping fix ever landed — a separate, pre-existing gap
in `q-804`'s original INV-198 arm that simply had no CI run to surface it until tonight.
`10b2a208` adds `-c safe.directory='*'` to both `git worktree list --porcelain` reads in this arm:
git's own "detected dubious ownership" refusal empties that command's stdout on a container/CI
runner where the process's detected user differs from the scratch repo's owner, and this arm's own
`2>/dev/null` would swallow that refusal's message and read as "no second worktree" — matching the
failure shape exactly. This is not confirmed against the actual CI runner (no shell access to it);
it is the best-supported hypothesis after ruling out pytest ordering, git-version `--porcelain`
format differences, and fixture-state leakage, and it is a narrow, well-understood mitigation for
exactly this failure class rather than a guess pulled from nowhere. The next CI run is the real
proof; if the 3 failures persist, this hypothesis is wrong and needs to be dropped, not patched
further.

Neither `10b2a208` nor `323dc6a3` has been pushed or run on CI yet — both land in this same range,
alongside a third fix (`9b06b553`) found while re-reading the arm before that push: the same
`git worktree list` read the `safe.directory` hypothesis targets was also swallowing ANY read
failure through its `2>/dev/null`, not only the dubious-ownership case, and reading the resulting
empty output as "no second worktree" — standing the whole INV-198 arm down silently instead of
reddening. This is exactly the shape the 3 still-failing tests need to distinguish from a genuine
"only one worktree" state: if `safe.directory` does not fully clear the dubious-ownership refusal
on the actual CI runner (untested — no shell access to it), the arm would previously have kept
standing down silently and the 3 tests would keep failing with no diagnostic. `9b06b553` makes that
read fail loudly by name instead, captured via `mktemp` rather than `2>/dev/null`, so the next CI
run either passes clean or, if it still fails, names the real git error instead of leaving the
prior "stood down with no clue why" shape. Proven locally by mutation only (see Checks run above);
this is not yet confirmed against the actual CI runner, and this push is that confirmation.
Blocking: none
