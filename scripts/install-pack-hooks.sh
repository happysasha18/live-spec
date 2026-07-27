#!/bin/sh
# Installs the canonical pack hooks (SPEC INV-173) on this machine, universal tier only. Idempotent:
# re-running changes nothing once installed. These mechanisms ship here:
#   - the scissors-scan Stop hook (the literal contrast-frame scan);
#   - the answer-first arm (a lead-less wall notice, SPEC INV-220);
#   - the hedge-scan Stop hook (the literal offering-hedge scan, SPEC INV-238);
#   - the affirmation-scan Stop hook (validation and praise of the human);
#   - the code-anchor Stop hook (a queue row number left standing where plain words belong);
#   - the mid-turn chat scan (PreToolUse), which judges the seat's own narration at the first tool
#     call after it is written, so a correction reaches the human inside the same turn; it reads the
#     calque list shipped beside it as chat-calques.json;
#   - the register judge (register_judge_core.py + register-judge.py + the async collect/report arms),
#     the class-reading model judge that holds what a literal list cannot (SPEC INV-203). Its universal
#     law ships in the mechanism; its personal laws ride ~/.claude/hooks/register-judge-personal.md.
# The personal overlays (scissors-personal.json, hedge-personal.json, register-judge-personal.md) are
# owned entirely by the personal layer — this script never creates or edits them.
#
# Usage: install-pack-hooks.sh [--dry-run]
#   --dry-run   print what would be done, touch nothing. Honors $HOME as-is (no hardcoded path),
#               so a test can point it at a scratch HOME without ever touching the real one.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"   # pack root (this script lives in <pack>/scripts/)

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
  esac
done

DEST_DIR="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"

# The universal files this script ships: the scissors scan, the answer-first arm, the hedge scan, and
# the register-judge mechanism + arms.
JUDGE_FILES="scissors-scan.py answer-first-scan.py hedge-scan.py affirmation-scan.py code-anchor-scan.py midturn-chat-scan.py chat-calques.json answer-first-scan.json language-laws.json turn_reader.py register_judge_core.py register-judge.py register-judge-collect.sh register-judge-report.sh"

if [ "$DRY_RUN" = "1" ]; then
  for f in $JUDGE_FILES; do
    if [ -f "$DEST_DIR/$f" ] && cmp -s "$DIR/hooks/$f" "$DEST_DIR/$f"; then
      echo "DRY-RUN: already present: $DEST_DIR/$f"
    else
      echo "DRY-RUN: would copy $DIR/hooks/$f -> $DEST_DIR/$f"
    fi
  done
  echo "DRY-RUN: would wire Stop hooks 'scissors-scan.py' + 'answer-first-scan.py' + 'hedge-scan.py' + 'register-judge-collect.sh' into $SETTINGS (if absent)."
  echo "DRY-RUN: would wire PreToolUse hook 'midturn-chat-scan.py' into $SETTINGS (if absent)."
  echo "DRY-RUN: would wire UserPromptSubmit hook 'register-judge-report.sh' into $SETTINGS (if absent)."
  echo "DRY-RUN: scissors-personal.json, hedge-personal.json, and register-judge-personal.md are never touched by this script."
  exit 0
fi

mkdir -p "$DEST_DIR"
for f in $JUDGE_FILES; do
  if [ -f "$DEST_DIR/$f" ] && cmp -s "$DIR/hooks/$f" "$DEST_DIR/$f"; then
    echo "already present: $DEST_DIR/$f"
  else
    cp "$DIR/hooks/$f" "$DEST_DIR/$f"
    chmod +x "$DEST_DIR/$f"
    echo "installed: $DEST_DIR/$f"
  fi
done

python3 - "$SETTINGS" << 'PYEOF'
import json, os, sys

p = sys.argv[1]
s = json.load(open(p)) if os.path.exists(p) else {}
hooks = s.setdefault("hooks", {})

def wire(event, needle, cmd):
    arr = hooks.setdefault(event, [])
    have = [hk.get("command", "") for e in arr for hk in e.get("hooks", [])]
    if any(needle in c for c in have):
        print("already present: %s hook %s wired" % (event, needle))
    else:
        arr.append({"hooks": [{"type": "command", "command": cmd}]})
        print("installed: %s hook %s wired" % (event, needle))

wire("Stop", "scissors-scan.py", "python3 ~/.claude/hooks/scissors-scan.py")
wire("Stop", "answer-first-scan.py", "python3 ~/.claude/hooks/answer-first-scan.py")
wire("Stop", "hedge-scan.py", "python3 ~/.claude/hooks/hedge-scan.py")
wire("Stop", "affirmation-scan.py", "python3 ~/.claude/hooks/affirmation-scan.py")
wire("Stop", "code-anchor-scan.py", "python3 ~/.claude/hooks/code-anchor-scan.py")
wire("Stop", "register-judge-collect.sh", "sh ~/.claude/hooks/register-judge-collect.sh")
wire("PreToolUse", "midturn-chat-scan.py", "python3 ~/.claude/hooks/midturn-chat-scan.py")
wire("UserPromptSubmit", "register-judge-report.sh", "sh ~/.claude/hooks/register-judge-report.sh")

os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(s, open(p, "w"), indent=2, ensure_ascii=False)
PYEOF

echo "note: ~/.claude/hooks/scissors-personal.json, hedge-personal.json, and register-judge-personal.md are owned by the personal layer — never created or modified here."
