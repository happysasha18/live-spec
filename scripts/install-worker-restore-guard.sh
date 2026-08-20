#!/bin/sh
# Install and wire the worker-restore PreToolUse(Bash) guard. Idempotent. A dry run prints the exact
# file and settings changes and writes nothing. Back up an existing global hook and settings file
# before the real run; the migration workflow owns that host-level backup.
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="$ROOT/hooks/worker-restore-guard.py"
DEST_DIR="$HOME/.claude/hooks"
DEST="$DEST_DIR/worker-restore-guard.py"
SETTINGS="$HOME/.claude/settings.json"
COMMAND="python3 ~/.claude/hooks/worker-restore-guard.py"
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) echo "usage: install-worker-restore-guard.sh [--dry-run]"; exit 2 ;;
  esac
done

# Validate every settings shape before copying the hook. A malformed personal settings file must leave
# both the existing hook and the settings bytes untouched; the real write below has no failing parse
# left to perform.
python3 - "$SETTINGS" <<'PY'
import json, os, sys
path = sys.argv[1]
if not os.path.isfile(path):
    raise SystemExit(0)
try:
    data = json.load(open(path, encoding="utf-8"))
except Exception as exc:
    raise SystemExit("worker-restore installer: cannot parse %s: %s" % (path, exc))
if not isinstance(data, dict):
    raise SystemExit("worker-restore installer: settings root must be an object")
hooks = data.get("hooks", {})
if not isinstance(hooks, dict):
    raise SystemExit("worker-restore installer: settings hooks must be an object")
pre = hooks.get("PreToolUse", [])
if not isinstance(pre, list) or any(not isinstance(entry, dict) or
                                   not isinstance(entry.get("hooks", []), list) for entry in pre):
    raise SystemExit("worker-restore installer: settings hooks.PreToolUse must be a list of hook groups")
PY

if [ "$DRY_RUN" = 1 ]; then
  if [ -f "$DEST" ] && cmp -s "$SOURCE" "$DEST"; then
    echo "DRY-RUN: already present: $DEST"
  else
    echo "DRY-RUN: would copy $SOURCE -> $DEST"
  fi
  python3 - "$SETTINGS" "$COMMAND" <<'PY'
import json, os, sys
path, command = sys.argv[1:]
data = json.load(open(path)) if os.path.isfile(path) else {}
pre = data.get("hooks", {}).get("PreToolUse", [])
commands = [hook.get("command", "") for entry in pre for hook in entry.get("hooks", [])]
print("DRY-RUN: %s" % ("already wired: " + command if any(
    "worker-restore-guard.py" in item for item in commands) else "would wire: " + command))
PY
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

python3 - "$SETTINGS" "$COMMAND" <<'PY'
import json, os, sys
path, command = sys.argv[1:]
data = json.load(open(path)) if os.path.isfile(path) else {}
pre = data.setdefault("hooks", {}).setdefault("PreToolUse", [])
commands = [hook.get("command", "") for entry in pre for hook in entry.get("hooks", [])]
if any("worker-restore-guard.py" in item for item in commands):
    print("already wired: %s" % command)
else:
    pre.append({"matcher": "Bash", "hooks": [{"type": "command", "command": command}]})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wired: %s" % command)
PY

deny=$(printf '%s' '{"tool_name":"Bash","tool_input":{"command":"git checkout -- x"}}' \
       | python3 "$DEST")
quiet=$(printf '%s' '{"tool_name":"Bash","tool_input":{"command":"git restore --staged x"}}' \
        | python3 "$DEST")
case "$deny" in *deny*) : ;; *) echo "self-test FAILED: destructive checkout passed"; exit 1;; esac
[ -z "$quiet" ] || { echo "self-test FAILED: staged-only restore was denied"; exit 1; }
echo "self-tests OK: destructive checkout denied; staged-only restore passed"
