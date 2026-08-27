#!/bin/sh
# The conduct judge's asynchronous half — the Stop arm (SPEC INV-241). Mirrors register-judge-collect.sh
# exactly, but writes a DISTINCT per-session verdict slot (<session>.conduct.json) so a turn that trips
# BOTH judges never has one verdict overwrite the other.
#
# The judge reads meaning, so it costs a model call (~33s, almost all of it the harness's own process
# start). Waiting for it at the end of every turn would tax the human that long per reply to correct acts
# already committed, and a tax that size gets a guard torn out. So the cost is moved off the waiting path:
# this arm hands the turn's ACTION TRACE to the judge in the BACKGROUND and returns at once, blocking
# nothing. The verdict lands in the .conduct.json slot; the UserPromptSubmit arm (conduct-judge-report.sh)
# reads it at the human's next message and puts the finding in front of the model then. A finished turn
# cannot be recalled, so the behavioural correction arrives one turn later by design.
#
# Opt-in and OFF by default: a host turns the conduct judge on by adding this arm (and the report arm) to
# their OWN settings.json. It is a library hook, not wired by the pack.
#
# Repo home: hooks/conduct-judge-collect.sh; installed copy: ~/.claude/hooks/.
PAYLOAD=$(cat)

# Never loop: on a stop that the hook itself provoked, stand aside.
STOP_ACTIVE=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys;print("1" if (json.load(sys.stdin) or {}).get("stop_hook_active") else "")' 2>/dev/null || echo "")
[ -n "$STOP_ACTIVE" ] && exit 0

VERDICT_DIR="${HOME}/.claude/hooks/.judge"
mkdir -p "$VERDICT_DIR"

# One verdict slot per session: a second turn's judgment replaces an unread first, since the newer turn is
# the one the human is reading and a queue of stale verdicts would report the wrong trace.
SESSION=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys;print((json.load(sys.stdin) or {}).get("session_id","unknown"))' 2>/dev/null || echo unknown)

# DISTINCT slot: <session>.conduct.json, never the register judge's <session>.json.
PART="${VERDICT_DIR}/${SESSION}.conduct.json.part"
JSON="${VERDICT_DIR}/${SESSION}.conduct.json"
ERR="${VERDICT_DIR}/${SESSION}.conduct.err"

# One subshell owns BOTH the write and the rename, so the rename can never race ahead of a write it does
# not own (the register arm's corrected shape). The judge runs to completion first (the pipe blocks the
# subshell until it exits), THEN the same subshell renames a non-empty verdict into place or clears an
# empty one. nohup wraps the whole subshell so both the judge and the rename survive the hook's return.
# The run below sets no REGISTER_JUDGE_TIMEOUT: 120s is now the judge default in
# hooks/register_judge_core.py, derived there from the ~33s measured above. Restating it here gave one
# deadline two homes that could drift apart.
CJ_PAYLOAD="$PAYLOAD" CJ_JUDGE="${HOME}/.claude/hooks/conduct-judge.py" \
CJ_PART="$PART" CJ_JSON="$JSON" CJ_ERR="$ERR" \
    nohup sh -c '
        printf "%s" "$CJ_PAYLOAD" | python3 "$CJ_JUDGE" > "$CJ_PART" 2> "$CJ_ERR"
        if [ -s "$CJ_PART" ]; then
            mv "$CJ_PART" "$CJ_JSON"
        else
            rm -f "$CJ_PART"
        fi
    ' > /dev/null 2>&1 &

exit 0
