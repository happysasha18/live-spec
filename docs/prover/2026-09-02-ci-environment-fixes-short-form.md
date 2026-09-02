# Prover short-form — the two CI-only environment fixes (2026-09-02 ~04:50)

Short-form per the cadence for a small, well-verified delta: commit `34f41718` fixes exactly the
two root causes CI's own real run (`https://github.com/happysasha18/live-spec/actions/runs/33578188215`,
`effa3ecc`, 24 failed) traced to — no new ground beyond what that failure log itself showed.

The config-health `INV-198` arm's new scoping (only a repo holding more than one worktree) was
verified live in both directions, not just read: a scratch single-worktree repo on branch `master`
(`git init -q -b master`, matching what the failure log's own `"holds 'master' instead of main"`
message named) now passes the check clean; a real two-worktree repo with a lane and a deliberately
drifted primary branch still reds with the same message shape the arm always gave. `python3 -m
pytest -q tests/test_lane_net_arms.py tests/test_routing_preamble_hook.py tests/test_config_health.py`
— 54 passed, the exact three files the CI log's failures concentrated in.

`test_wind_down.py`'s explicit git identity was verified by running the whole file under
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` — the closest local reproduction of a
runner carrying no `~/.gitconfig` of its own, which is exactly the condition CI's own "Please tell
me who you are" error names. 6 passed under that isolation, matching the fix's own reasoning rather
than assuming it from the diff alone.

Full local suite re-run once more after both fixes, alone: `2737 passed, 4 skipped`. The one
`error` that run showed was `test_worker_restore_run_scope.py` correctly flagging this commit's own
changes as still sitting uncommitted at the time it ran — an accurate flag, resolved the moment
`34f41718` lands, since the check reads the working tree's own status.

This record's own job is proving the two new fixes actually hold, which the commands above do; the
full push range's own already-reviewed ground stays exactly where
`docs/prover/2026-09-02-full-push-range.md` and its own short-form follow-up already put it.
