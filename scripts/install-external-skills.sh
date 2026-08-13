#!/usr/bin/env bash
# install-external-skills.sh — fetch external skills the live-spec pack depends on.
#
# Today that is one skill: product-prover (github.com/happysasha18/product-prover).
# The pack keeps no copy of it. This script clones or updates it into
# skills/product-prover/ and refuses a version below the floor read from
# skills/product-prover-pack/SKILL.md (the `requires:` line).
#
# Usage: scripts/install-external-skills.sh [--ref <tag-or-branch>]
#   default ref: the repository's default branch (latest release state)
#
# The installed copy is ignored by git (.gitignore: skills/product-prover/).
# Re-run this script to update; it is idempotent.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

PROVER_URL="https://github.com/happysasha18/product-prover.git"
DEST="skills/product-prover"
ADAPTER="skills/product-prover-pack/SKILL.md"

REF=""
if [ "${1:-}" = "--ref" ]; then
  REF="${2:?--ref needs a value}"
fi

# --- the version floor, read from the adapter's metadata ---
FLOOR="$(grep -m1 -oE 'product-prover >= [0-9]+\.[0-9]+\.[0-9]+' "$ADAPTER" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
if [ -z "$FLOOR" ]; then
  echo "FAIL (external skills): no version floor found in $ADAPTER (requires: line)."
  exit 1
fi

# --- clone or update ---
if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin
  if [ -n "$REF" ]; then git -C "$DEST" checkout -q "$REF"; fi
  git -C "$DEST" pull -q --ff-only 2>/dev/null || true
else
  rm -rf "$DEST"
  if [ -n "$REF" ]; then
    git clone -q --branch "$REF" "$PROVER_URL" "$DEST"
  else
    git clone -q "$PROVER_URL" "$DEST"
  fi
fi

# --- hold the floor ---
GOT="$(grep -m1 -oE 'version: *[0-9]+\.[0-9]+\.[0-9]+' "$DEST/SKILL.md" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
if [ -z "$GOT" ]; then
  echo "FAIL (external skills): $DEST/SKILL.md carries no readable version stamp."
  exit 1
fi

lowest="$(printf '%s\n%s\n' "$FLOOR" "$GOT" | sort -V | head -1)"
if [ "$lowest" != "$FLOOR" ]; then
  echo "FAIL (external skills): product-prover $GOT is below the pack's floor $FLOOR."
  echo "  Fix: update the clone (re-run without --ref), or raise/lower the floor in $ADAPTER as a pack change."
  exit 1
fi

echo "OK (external skills): product-prover $GOT installed at $DEST (floor $FLOOR)."
