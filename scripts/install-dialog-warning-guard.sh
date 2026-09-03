#!/bin/sh
# Places the dialog-warning PreToolUse(Bash) guard on this machine (PLAN q-581).
#
# Copy-only, like the six opt-in judges install-pack-hooks.sh ships: the file lands in
# ~/.claude/hooks/ so guardrails/check-config-health.sh's source-vs-installed diff stays green, and
# this script wires NOTHING into settings.json. A host that wants the warning live adds one
# PreToolUse(Bash) entry naming `python3 ~/.claude/hooks/dialog-warning-guard.py`, the same shape
# scripts/install-worker-restore-guard.sh already wires for its neighbour — that script is the
# pattern to copy once the wiring question itself is the human's own call, not this one's.
#
# Usage: install-dialog-warning-guard.sh [--dry-run]
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/hooks/dialog-warning-guard.py"
DEST_DIR="$HOME/.claude/hooks"
DEST="$DEST_DIR/dialog-warning-guard.py"
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) echo "usage: install-dialog-warning-guard.sh [--dry-run]"; exit 2 ;;
  esac
done

if [ "$DRY_RUN" = 1 ]; then
  if [ -f "$DEST" ] && cmp -s "$SOURCE" "$DEST"; then
    echo "DRY-RUN: already present: $DEST"
  else
    echo "DRY-RUN: would copy $SOURCE -> $DEST"
  fi
  echo "DRY-RUN: would wire nothing into settings.json — opt-in until a host adds the entry by hand."
  exit 0
fi

mkdir -p "$DEST_DIR"
if [ -f "$DEST" ] && cmp -s "$SOURCE" "$DEST"; then
  echo "already present: $DEST"
else
  cp "$SOURCE" "$DEST"
  chmod +x "$DEST"
  echo "installed: $DEST"
fi

warned=$(printf '%s' '{"tool_name":"Bash","tool_input":{"command":"security find-generic-password -w"}}' \
         | python3 "$DEST")
quiet=$(printf '%s' '{"tool_name":"Bash","tool_input":{"command":"git status"}}' | python3 "$DEST")
case "$warned" in *permissionDecision*ask*|*ask*permissionDecision*) : ;; *)
  echo "self-test FAILED: a keychain read passed with no warning"; exit 1;; esac
[ -z "$quiet" ] || { echo "self-test FAILED: an ordinary command was warned about"; exit 1; }
echo "self-tests OK: a keychain read is warned about; an ordinary command passes silently"
