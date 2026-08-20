# Worker-restore incident record — 2026-08-20

This is a forensic record, not a PUSH-REVIEW record. It preserves the historical result of a real
worker command and records the repair that prevents a later worker from repeating it. No transcript
was changed, removed, or reclassified to make this record green.

## The observed command

`guardrails/check-worker-restore.py --all` reads a command in
`~/.claude/projects/-private-tmp-live-spec-roadmap-wave/279a25e4-6919-4347-965a-f49848119223/subagents/agent-afc7daf29f1501c3e.jsonl`:

- session: `279a25e4-6919-4347-965a-f49848119223`
- worker: `afc7daf29f1501c3e`
- timestamp: `2026-08-19T11:01:06.707Z`
- working directory: `/private/tmp/live-spec-man/wt`
- command: `git checkout -- TEST_MATRIX.md`
- transcript outcome: `RAN`

The worker had first added two matrix rows, then made a mistaken rebuild that removed a heading and
intro. Immediately before checkout, the tracked delta was four insertions and six deletions in the
worker's scratch change; the checkout made the tree clean. The command is a real violation whether
or not its effect was later reconstructed.

## What the evidence can and cannot establish

The exact preimage is deterministically reconstructible from the transcript and history: 475,325
bytes, SHA-256 `062a89a00fea0f36e27e447f3487484250ad6edf5edde4d56d20cc584c98bfc5`. It is not present
as a Git blob, index entry, or stash. There was no additional tracked delta at the time of the
checkout. That does not prove an invisible concurrent writer did not exist; it only records that the
available evidence contains none.

The worker did not halt after the command. It continued and rebuilt its useful intended rows as
`M-547` and `M-548`; commit `de5158b8` carries that later useful content and is an ancestor of
`origin/main`.

The strengthened classifier also surfaces two additional historical path-checkout forms in a
separate worker run (`git checkout -q .` and `git checkout HEAD file.txt`). They remain forensic
findings too. They are not folded into the TEST_MATRIX incident or used to excuse it.

## Repair and acceptance rule

The new acceptance command is `check-worker-restore.py --run <exact-agent-jsonl>`. It reads exactly
the result being accepted, with no time threshold, retry, recovery record, or project/neighbour
downgrade. A red original run stays red. Recovery means a fresh brief and a fresh worker run; only
that fresh exact run may pass acceptance.

`hooks/worker-restore-guard.py` denies the same destructive forms before Bash runs them. A worker
that lacks its own saved bytes halts and reports the file; only the orchestrator may recover from a
committed stage. The hook's installer is dry-run capable and idempotent; its host installation is
backed up before modification.
