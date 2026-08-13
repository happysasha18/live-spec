#!/usr/bin/env bash
# install-external-skills.sh — fetch external skills the live-spec pack depends on.
#
# Today that is one skill: product-prover (github.com/happysasha18/product-prover).
# The pack keeps no copy of it. This script clones or updates it into
# skills/product-prover/ and refuses a version below the floor read from
# skills/product-prover-pack/SKILL.md (the `requires:` line).
#
# Usage: scripts/install-external-skills.sh [--ref <tag|branch|commit>] [--expect-commit <sha>]
#   default ref: the repository's default branch (latest release state)
#
# --ref takes a COMMIT SHA as well as a tag or branch, because a developer wants "the
# latest release" while a machine that gates a push wants the one state the pack's
# assertions were written against. A tag can be moved and a branch always moves;
# a commit cannot.
#
# --expect-commit is the verification half of that pin: after the install, the checked-out
# HEAD must equal the named sha or this script fails and says both shas. A pin nobody
# verifies is a comment. CI passes both (see .github/workflows/gates.yml, gate b's
# installer step) so a silently-moved tag cannot change what CI proves.
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
EXPECT=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --ref) REF="${2:?--ref needs a value}"; shift 2 ;;
    --expect-commit) EXPECT="${2:?--expect-commit needs a value}"; shift 2 ;;
    *) echo "FAIL (external skills): unknown argument '$1'." >&2; exit 1 ;;
  esac
done

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
  # A full clone first, then the ref: `clone --branch` resolves a tag or a branch and
  # nothing else, and the pin CI carries is a commit sha.
  git clone -q "$PROVER_URL" "$DEST"
  if [ -n "$REF" ]; then git -C "$DEST" checkout -q "$REF"; fi
fi

# --- hold the pin ---
if [ -n "$EXPECT" ]; then
  HEAD_SHA="$(git -C "$DEST" rev-parse HEAD)"
  if [ "$HEAD_SHA" != "$EXPECT" ]; then
    echo "FAIL (external skills): $DEST is at $HEAD_SHA, and the pin names $EXPECT."
    echo "  The canon moved under a ref that was expected to stand still, or the pin is stale."
    echo "  Fix: re-read what the pack's assertions are written against, then move the pin"
    echo "  deliberately in .github/workflows/gates.yml — do not widen this check."
    exit 1
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

if [ -n "$EXPECT" ]; then
  echo "OK (external skills): product-prover $GOT installed at $DEST (floor $FLOOR, pinned $EXPECT)."
else
  echo "OK (external skills): product-prover $GOT installed at $DEST (floor $FLOOR)."
fi
