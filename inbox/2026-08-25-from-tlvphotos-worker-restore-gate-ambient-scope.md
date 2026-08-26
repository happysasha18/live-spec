# Push gate blocked by an unrelated project's transcript — 2026-08-25

Lived: pushing `wip/2026-08-06-darkroom` from `~/tlvphotos` (seven ready commits, clean tree) was
blocked twice tonight and again this morning by `check-worker-restore.py`. Both times the block
cited EXECUTED discarding git commands (`git stash` and forms of it) in
`/private/tmp/ls-director/wt` — a live-spec pack development worktree that has never shared a
repository with tlvphotos and was touched by sessions this project never spawned.

tlvphotos's own copy of the gate (`tlvphotos/guardrails/check-worker-restore.py`) imports the pack
script at `~/live-spec/guardrails/check-worker-restore.py` unchanged and inherits its
`DEFAULT_ROOT = ~/.claude/projects` with `DEFAULT_SINCE_HOURS = 24.0` — every project's transcripts
on the machine, last 24 hours, when no `--root`/`--run` narrows it. `build-pipeline/SKILL.md` names
this its "ambient root scan," documented there as serving "forensic census work," distinct from the
scoped `--run <exact-agent-jsonl>` check the same doc says to run before accepting one worker's
result. Whatever calls the gate at push time in this host's wiring is using the wide, undirected
census as a hard blocking check rather than the scoped one — so any session's mistake anywhere on
the machine, in a project tlvphotos has no relationship to, can stall a tlvphotos push indefinitely.

Not something this session can fix from inside tlvphotos: the gate script is a live-spec pack file,
read-only to a session assigned elsewhere.

Need-by: none — worked around by waiting; naming it so the block doesn't keep recurring silently.
Id: tlvphotos-2026-08-25-worker-restore-scope
