#!/bin/sh
# The judge's asynchronous half (ROADMAP row 416; the owner's word 2026-07-17 ~16:39, choosing the
# asynchronous road over a 33-second wait per reply).
#
# The judge reads meaning, so it costs a model call, and the call costs ~33s — almost all of it the
# harness's own process start rather than the model's thinking (probed: the flag that skips the start
# breaks the login). Waiting for it at the end of every turn would tax the human 33 seconds per reply
# to fix a sentence he has already read, and a tax that size gets a guard torn out.
#
# So the cost is moved off the waiting path entirely. This script is the Stop arm: it hands the turn's
# text to the judge in the BACKGROUND and returns at once, blocking nothing. The verdict lands
# in a file. The UserPromptSubmit arm (register-judge-report.sh) reads that file at the human's next
# message and puts the finding in front of the model, which sends the correction then.
#
# The trade this makes, stated plainly because the human asked and it is his to know: the offending
# message reaches him uncorrected, and the correction follows one turn later. A sent message cannot be
# recalled or edited — the harness offers no such act — so one turn is the floor for any judge that
# reads meaning.
#
# Repo home: hooks/register-judge-collect.sh; installed copy: ~/.claude/hooks/.
PAYLOAD=$(cat)
VERDICT_DIR="${HOME}/.claude/hooks/.judge"
mkdir -p "$VERDICT_DIR"

# One verdict slot per session: a second turn's judgment replaces an unread first, since the newer
# message is the one the human is reading and a queue of stale verdicts would report the wrong text.
SESSION=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys;print((json.load(sys.stdin) or {}).get("session_id","unknown"))' 2>/dev/null || echo unknown)

PART="${VERDICT_DIR}/${SESSION}.json.part"
JSON="${VERDICT_DIR}/${SESSION}.json"
ERR="${VERDICT_DIR}/${SESSION}.err"

# One subshell owns BOTH the write and the rename, so the rename can never race ahead of a write it does
# not own. The earlier form backgrounded the judge and then ran `wait $!` in a SIBLING subshell; the
# judge was not that subshell's child, so wait returned instantly, the still-empty .part was removed, and
# the judge finished writing into an unlinked inode — no verdict ever landed (~/.claude/hooks/.judge held
# only .err files, corrected 2026-07-17). Here the judge runs to completion first (the pipe blocks the
# subshell until it exits), THEN the same subshell renames a non-empty verdict into place or clears an
# empty one. nohup wraps the whole subshell so both the judge and the rename survive the hook's return.
# The run below sets no REGISTER_JUDGE_TIMEOUT: 120s is now the judge default in
# hooks/register_judge_core.py, derived there from the ~33s measured above. Restating it here gave one
# deadline two homes that could drift apart.
RJ_PAYLOAD="$PAYLOAD" RJ_JUDGE="${HOME}/.claude/hooks/register-judge.py" \
RJ_PART="$PART" RJ_JSON="$JSON" RJ_ERR="$ERR" \
    nohup sh -c '
        printf "%s" "$RJ_PAYLOAD" | python3 "$RJ_JUDGE" > "$RJ_PART" 2> "$RJ_ERR"
        if [ -s "$RJ_PART" ]; then
            mv "$RJ_PART" "$RJ_JSON"
        else
            rm -f "$RJ_PART"
        fi
    ' > /dev/null 2>&1 &

exit 0
