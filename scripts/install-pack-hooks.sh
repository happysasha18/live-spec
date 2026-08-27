#!/bin/sh
# Installs the canonical pack hooks (SPEC INV-173) on this machine, universal tier only. Idempotent:
# re-running changes nothing once installed. It COPIES the files below and wires none of them: all six
# stood down from the default wiring on the owner's word of 2026-08-17 (JOURNAL.md; PRODUCT_SPEC.md
# Requirement 311), so each is opt-in and a host turns one on in its own settings.json. These
# mechanisms ship here:
#   - the scissors-scan Stop hook (the literal contrast-frame scan);
#   - the hedge-scan Stop hook (the literal offering-hedge scan, SPEC INV-238);
#   - the affirmation-scan Stop hook (validation and praise of the human);
#   - the code-anchor Stop hook (a queue row number left standing where plain words belong);
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
    # An unrecognized argument stops the run. Without this arm a near miss — `--dryrun`,
    # `--dry_run`, a typo — fell through the case silently and the script installed for real
    # against the caller's actual home, which is the one outcome --dry-run exists to prevent.
    *)
      echo "install-pack-hooks: I don't know the option '$arg', so I stopped before touching" >&2
      echo "  anything. The only option is --dry-run, which shows what would happen and" >&2
      echo "  changes nothing. Run it with no options to install for real." >&2
      exit 2
      ;;
  esac
done

DEST_DIR="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"

# The universal files this script ships: the scissors scan, the hedge scan, and the register-judge
# mechanism + arms.
JUDGE_FILES="scissors-scan.py hedge-scan.py affirmation-scan.py code-anchor-scan.py language-laws.json turn_reader.py register_judge_core.py register-judge.py register-judge-collect.sh register-judge-report.sh"

if [ "$DRY_RUN" = "1" ]; then
  for f in $JUDGE_FILES; do
    if [ -f "$DEST_DIR/$f" ] && cmp -s "$DIR/hooks/$f" "$DEST_DIR/$f"; then
      echo "DRY-RUN: already present: $DEST_DIR/$f"
    else
      echo "DRY-RUN: would copy $DIR/hooks/$f -> $DEST_DIR/$f"
    fi
  done
  echo "DRY-RUN: would wire nothing into $SETTINGS — these six checks are opt-in since 2026-08-17."
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

echo "note: these six checks are opt-in since 2026-08-17 (JOURNAL.md). Their files stand in $DEST_DIR and"
echo "      this script wires none of them into $SETTINGS. A host that wants one adds its command there"
echo "      by hand, reading the surface and the command form from guardrails/judge-hooks.json."

echo "note: ~/.claude/hooks/scissors-personal.json, hedge-personal.json, and register-judge-personal.md are owned by the personal layer — never created or modified here."
