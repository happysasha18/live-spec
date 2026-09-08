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
#     law ships in the mechanism; its personal laws ride ~/.claude/hooks/register-judge-personal.md;
#   - the conduct-judge arms with the standing orchestration law they read (conduct-law.md), and the
#     lean-orchestrator net. These five were shipped by nothing until 2026-09-08, though gate m held
#     each of them to match its installed copy — see the note above JUDGE_FILES.
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

# Every file this script ships. It is the whole of hooks/ minus the files another installer already
# owns, because config-health (gate m) compares EVERY file under hooks/ against its installed copy
# and names the installer whose text mentions the file as the fix. A file under hooks/ that no
# installer names has no fix to offer: on 2026-09-08 an edit to conduct-law.md left the installed
# copy stale, gate m red with "run the installer that owns this hook", and no such installer
# existed — the file was copied by hand to get the push out. The list below therefore holds the six
# opt-in checks it always shipped (the scissors, hedge, affirmation and code-anchor scans, and the
# register-judge mechanism with its arms), and beside them the conduct-judge arms with the standing
# law they read and the lean-orchestrator net, which nothing installed before today.
JUDGE_FILES="scissors-scan.py hedge-scan.py affirmation-scan.py code-anchor-scan.py language-laws.json turn_reader.py register_judge_core.py register-judge.py register-judge-collect.sh register-judge-report.sh conduct-judge.py conduct-judge-collect.sh conduct-judge-report.sh conduct-law.md lean-orchestrator-scan.py"

# The names another installer owns, so the sweep below can tell "somebody ships it" from "nobody
# does". scripts/install-session-hooks.sh generates the three wired hooks from the declaration and
# then chains here; scripts/install-dialog-warning-guard.sh and scripts/install-worker-restore-guard.sh
# each own one file.
OWNED_ELSEWHERE="clock-hook.sh chat-law-hook.sh routing-preamble-hook.sh dialog-warning-guard.py worker-restore-guard.py"

# The recurrence-stop for the defect above: a file added to hooks/ and to no installer is named
# here, at install time, instead of surfacing weeks later as a gate red with no fix behind it.
for src_hook in "$DIR"/hooks/*; do
  hname="$(basename "$src_hook")"
  case " $JUDGE_FILES $OWNED_ELSEWHERE " in
    *" $hname "*) ;;
    *)
      echo "install-pack-hooks: hooks/$hname is shipped by no installer, so config-health has no" >&2
      echo "  fix to name when its installed copy drifts. Add it to JUDGE_FILES here, or to the" >&2
      echo "  installer that owns it, then run this again." >&2
      exit 2
      ;;
  esac
done

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
    case "$f" in *.py|*.sh) chmod +x "$DEST_DIR/$f" ;; esac
    echo "installed: $DEST_DIR/$f"
  fi
done

echo "note: these six checks are opt-in since 2026-08-17 (JOURNAL.md). Their files stand in $DEST_DIR and"
echo "      this script wires none of them into $SETTINGS. A host that wants one adds its command there"
echo "      by hand, reading the surface and the command form from guardrails/judge-hooks.json."

echo "note: ~/.claude/hooks/scissors-personal.json, hedge-personal.json, and register-judge-personal.md are owned by the personal layer — never created or modified here."
