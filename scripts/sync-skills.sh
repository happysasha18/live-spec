#!/usr/bin/env bash
# sync-skills.sh — the pack developer's freshness tool (SPEC E-23).
# Copies each repo skill over its installed copy and REPORTS every version change old -> new,
# so the A-7 re-read has its trigger line. The repo is the source (D-4); the installed copy
# is a mirror that must never run stale through a working session.
# Usage: scripts/sync-skills.sh [dest]   (default: ~/.claude/skills)

set -euo pipefail

REPO_SKILLS="$(cd "$(dirname "$0")/../skills" && pwd)"
DEST="${1:-$HOME/.claude/skills}"

mkdir -p "$DEST"

version_of() {
  # frontmatter form:  metadata:\n  version: X.Y.Z
  awk '/^  version: / { print $2; exit }' "$1" 2>/dev/null || true
}

changed=0
for skill_dir in "$REPO_SKILLS"/*/; do
  name="$(basename "$skill_dir")"
  # External-skill fence — the shared policy install.sh already carries: a skill dir holding
  # its own .git is the external canonical clone; never copy it (or its .git).
  if [ -e "$skill_dir/.git" ]; then
    echo "  $name — SKIPPED (external skill's canonical clone; scripts/install-external-skills.sh owns it)"
    continue
  fi
  src_v="$(version_of "$skill_dir/SKILL.md")"
  dst_v="$(version_of "$DEST/$name/SKILL.md")"
  # Skip only when the installed tree is byte-identical to the source — the SAME whole-tree compare
  # the config-health skill-copy arm reds on (INV-243). Gating the skip on the SKILL.md version or
  # mtime alone let a drift confined to a non-SKILL.md file (a reference edited with no version bump)
  # red the gate while re-running this fix skipped it as "unchanged" — a red with no working escape.
  if [ -d "$DEST/$name" ] && diff -rq "$skill_dir" "$DEST/$name" >/dev/null 2>&1; then
    echo "  $name — unchanged ($src_v)"
    continue
  fi
  # A full remove-then-copy, not an overlay: cp -r alone never removes a file that left the
  # source (2026-08-25 — 4 reference files moved out of build-pipeline left stale copies
  # behind, and diff -rq never reached equality, so gate m reds "drifted" right after a sync).
  rm -rf "$DEST/$name"
  mkdir -p "$DEST/$name"
  cp -r "$skill_dir"/. "$DEST/$name/"
  echo "  $name — synced: ${dst_v:-absent} -> $src_v   (A-7: RE-READ this skill before continuing)"
  changed=$((changed + 1))
done

if [ "$changed" -eq 0 ]; then
  echo "sync-skills: everything fresh."
else
  echo "sync-skills: $changed skill(s) updated — journal the old -> new line (A-7)."
fi
