# Background workers: spawning, liveness, resume

This page explains how the pack runs background workers. A background worker is a delegated sub-agent that a session starts to carry out a well-scoped piece of work while the session continues. The normative rules live in the product spec (`PRODUCT_SPEC.md`: the "Delegation and workers" section, plus INV-76 and INV-80) and in the shared rulebook (`skills/live-spec-base/SKILL.md`, rules 6 and 7). This page explains those rules in plain words and points at their homes; it adds no rule of its own.

## Spawning a worker

A session delegates mechanical work and keeps judgment for itself (ACT-2, ACT-3). A delegation starts with a brief: one self-contained document carrying the exact spec sentences the work serves, the exact edits or commands, the checks to run, and the checkpoint path. The brief names the files the worker may write. Outside those files the worker reads and never writes (ACT-3).

Four brief duties matter most for liveness and resume:

- The worker keeps a persistent checkpoint file in the host's `.live-spec/checkpoints/` directory (gitignored, inside the repo tree). It records done / in-progress / next and is updated as the work runs, so a cut-off run resumes from disk (live-spec-base rule 6).
- The worker touches that same checkpoint file on a fixed interval (~60 s [default]) as a bare heartbeat, whatever else its work writes. A compute-bound run — a long render, a large test pass — can write no product file for minutes; the heartbeat is what proves it still alive to the resume protocol's death check (INV-76).
- The brief carries the clock: the date and time read at briefing, so the worker stamps its checkpoint from a real clock (INV-24).
- The brief carries a closed halt list: an ambiguous requirement, two consecutive unexplained failures of one command, a missing config or dependency, or acceptance impossible as briefed. On any of these the worker stops with evidence; otherwise it runs to completion (INV-54).

The full delegation contract — tier routing, brief sizing, escalation — lives in the spec's "Delegation and workers" section, elaborated in `skills/build-pipeline/SKILL.md`.

## Liveness: check before spawning a second worker

A background worker survives a context wipe. After a `/clear` or a handoff, a worker spawned earlier may still be running and still writing the shared tree. The operating system's process list and the harness task list show nothing for it, so an empty list proves nothing about its death (INV-76).

The checkpoint or handoff note that records a live worker states three things (live-spec-base rule 6):

- the worker's recorded id, pointing at the worker's own checkpoint file;
- the exact files its brief lets it write (the write-set);
- the three liveness checks a resuming session runs before touching those files or spawning a sibling.

The three checks:

1. Watch the write-set's file modification times over a short window (~30 s [default]). Any change means a live writer.
2. Read the worker's heartbeat on its checkpoint file: a worker touches that file on a fixed interval (~60 s [default]) whatever its work writes, so a heartbeat moved within the last ~2 min [default] means a live writer even when no product file has — the case of a compute-bound run mid-computation.
3. Send one message to the recorded id. A live worker answers; allow ~2 min [default].

Life on any one check means reconnect and treat the worker's files as claimed. A dead verdict requires all three quiet together — a still write-set, a stale heartbeat, and an unanswered probe — declared in one written line, then proceed. Until that verdict the worker's output is never framed as finished. A worker from a prior context counts as a foreign writer until verified; the same-session courtesy of the concurrent-edit fence ends at the wipe. No second worker goes onto a shared tree until the first has confirmed halted by its own reply or has been declared dead by all three checks (INV-11, INV-76).

Before a wipe, prefer halting the workers or letting them finish, so the next session starts single-writer. A handoff also says plainly when a worker dies with a closed window or a sleeping machine, so nobody is told the worker will simply be recognized. The rule was born from a real two-writer race: a resuming session declared a worker dead off the empty process list and spawned a second worker onto the same files (2026-07-09; wish: `docs/wishes/2026-07-09-tlvphoto-worker-liveness-across-clear.md`, landed as queue row 181).

## Verifying a worker's result

A worker's report is a lead. Evidence is raw output: the command, its exit code, and the failing lines, pasted into the checkpoint as the work runs (live-spec-base rule 5). The senior spot-checks by re-running.

For a delegated or background test run, the verdict lives in the suite log itself. The gate reads the suite log's own tail line, the "N/N green" verdict. A wrapper's exit code reports only that the wrapper finished, and for a background or delegated run it never stands as the verdict (INV-80). A foreground gate reading its own child's exit stays legal. This law was landed the same evening one commit slipped through on a red suite because a command chain read a wrapper's exit code and never read the log (JOURNAL.md, session 30).

When the code step was delegated and the delta is surface-sized, verify also runs a fresh-context checker. It is briefed with the spec sentences the landing claims and the artifact paths, opens on the hypothesis "tasks completed, goal missed", and walks each claimed fact up the ladder exists → substantive → wired → flows (INV-46).

## Git discipline on a shared tree

- Write-ownership stays narrow. A worker writes only the files its brief names; a same-session sibling's briefed files are fence-benign, and the senior who briefed both owns the seams (ACT-3).
- The concurrent-edit fence runs before every write and every commit: re-check `git status` and `HEAD` against what was last read. If `HEAD` moved, or the tree holds changes the session did not make, stop, re-read, then proceed surgically or back off (live-spec-base rule 7, INV-11).
- A landing commit carries exactly one row's delta, and its gate runs on a tree clean of any other lane's unfinished work, so a stray file from a parallel worker never rides a commit (INV-39).
- A brief may instead name an isolated copy of the tree (a git worktree). The worker builds and tests there, and its delta reaches the shared tree only through the senior's integration, under the pen (T-18, ACT-3). The pack's first double-lane run built one lane entirely this way (queue rows 135 and 137).

## Resume after a pause or wipe

Every movement ends the same way: replace the NEXT_STEPS live state, add a dated journal entry, and commit. After that, session memory can be wiped with zero loss (M-2). NEXT_STEPS may be gitignored, so the journal entry is the durable net.

The resume file is a digest with no redundancy: the whole NEXT_STEPS file holds one live-state block and nothing removable without losing information, and a suite check owns that shape. An open leg restates as one terse line — its name, what stays open, and where the detail lives — while the detail itself flows to the journal or the queue row (INV-48, INV-26).

A cold session reads NEXT_STEPS first. If the pause left a red test, the failing test name plus a hypothesis stands as the top item; the checkpoint is the red test, and red is never committed (live-spec-base rule 6). If the note records a live worker, the session runs the three liveness checks above before touching that worker's files or spawning any sibling (INV-76). On the way back it also re-checks skill freshness (A-7).
