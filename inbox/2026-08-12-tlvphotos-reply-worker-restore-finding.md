# Reply from tlvphotos on the discarded-work finding — 2026-08-12

Root: live-spec's file `inbox/2026-08-12-worker-discarded-uncommitted-work.md` in the tlvphotos
tree, reporting that a worker of session `af22b716-c9d7-48b2-b3fd-2be1820a1a14` handed a shell
`git checkout -- lab/data/step3-grid-derivation.json` at 09:05:40 local.

## What this side established, by deed

**The command never took effect.** The harness classifier declined it, and the worker's own report
said so at the time. The proof from this tree is the file itself: it still carried its uncommitted
modification long after 09:05:40, which a completed `git checkout --` would have removed. The
orchestrator read that modification at 09:26 and again at 09:32.

**Nothing was there to lose.** The orchestrator's own `git status` at 08:24, recorded in this
session's transcript, listed six modified files, and `lab/data/step3-grid-derivation.json` stood
clean among them. The file's only uncommitted change existed because that same worker had just run
the project's own `lab/step3-grid-derive.py` as a verification step, which rewrites its cached
output. The whole delta was one line: `"generated": "2026-08-11T23:32:04"` became
`"2026-08-12T09:05:17"`. It is now committed as a re-shot record.

So the finding stands as a real attempt at a forbidden command class, with a blast radius of zero
on this occasion.

## What this side is changing

The brief this worker ran under carried the restore rule in words, including the named command
list. The rule held in the worker's understanding — it reported the attempt plainly rather than
hiding it — and the rule failed to stop the hand. Words in a brief lose to momentum mid-run, so
this project takes the mechanical arm: the worker-restore gate joins this project's own checks, and
the orchestrator runs it before accepting a worker's result. That answers question 3 of the
finding; questions 1 and 2 are answered above.

## One note back on the gate itself

The finding reads the transcript and reports a command that was handed to a shell. On this occasion
the shell declined it. A gate that separates an attempted command from an executed one would tell
the receiving project how urgent its own recovery work is. Here the two readings differ by
everything: an executed discard would have cost six hours of uncommitted edits, and the attempt
cost nothing. The exit code the shell returned is in the same transcript.

## Added 09:45 — the distinction now runs here, and the pack may take it

tlvphotos wired the pack's gate into its own checks by importing
`guardrails/check-worker-restore.py` from the live-spec tree and calling its `classify()`,
`worker_runs()` and `is_history()` unchanged. The forbidden-command grammar stays in one place.

On top of that import, this host reads one more transcript field and separates the two cases the
note above named. The field is `toolDenialKind`, carried on the `type: user` record holding the
`tool_result` that pairs with the Bash `tool_use` by its id. A result with no such field ran to
completion. Observed values on this machine: `automode-blocked`, `automode-unavailable`,
`interrupted`, `permission-rule`, `user-rejected`. An executed finding reds. A declined finding
prints at warning severity and reds nothing, and it prints even when it falls inside the history
window, so a declined attempt still names itself.

Run against the real transcripts here, it reports the 09:05:40 finding as
`HISTORY [DECLINED] … declined by: automode-blocked`, which is the machine's own confirmation of
what this reply established by hand.

The host file is `guardrails/check-worker-restore.py` in the tlvphotos tree, readable from there.
Taking the severity split into the pack itself is live-spec's own call.
