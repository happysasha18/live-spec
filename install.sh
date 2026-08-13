#!/usr/bin/env bash
# install.sh — copies live-spec skills into ~/.claude/skills/
# Idempotent: backs up any existing skill with a timestamp before overwriting.
# Usage: ./install.sh

set -euo pipefail

SKILLS_SRC="$(cd "$(dirname "$0")/skills" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$SKILLS_DEST"  # a fresh machine has no skills home yet (E-21's fresh-install promise)

echo "live-spec install — copying skills to $SKILLS_DEST"
echo "Timestamp for backups: $TIMESTAMP"
echo ""

for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name="$(basename "$skill_dir")"
  if [ -e "$skill_dir/.git" ]; then
    echo "  $skill_name — SKIPPED (external skill's canonical clone; scripts/install-external-skills.sh owns it)"
    continue
  fi
  dest="$SKILLS_DEST/$skill_name"

  if [ -d "$dest" ]; then
    backup_home="$SKILLS_DEST-attic"
    mkdir -p "$backup_home"
    backup="$backup_home/$skill_name.bak_$TIMESTAMP"
    echo "  $skill_name — backing up existing to $backup"
    cp -r "$dest" "$backup"
  else
    echo "  $skill_name — new install"
  fi

  cp -r "$skill_dir" "$dest"
  echo "  $skill_name — installed"
done

echo ""
echo "Done. Skills available in ~/.claude/skills/:"
ls "$SKILLS_DEST"
