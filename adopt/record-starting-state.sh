#!/usr/bin/env bash
# adopt/record-starting-state.sh — a project joining live-spec keeps its files as they were found.
#
# Run from the HOST project root, or pass that root as the one argument. This is Phase 0 of the
# attach walk (adopt/ADOPT.md) and of the founding walk (adopt/START.md). It runs before any pack
# file lands in the tree, because a commit that already carries pack scaffolding is not the project
# as it was found.
#
# A project with no git history becomes a repository and its files are committed exactly as found.
# That first commit is the point every later change is diffed against.
#
# A project that already carries git history keeps it: the history it has is already a starting
# point, so this makes no commit and touches nothing. That case is reported and skipped, which is
# also what makes a second run safe.
#
# Usage: adopt/record-starting-state.sh [HOST_ROOT]
set -euo pipefail

HOST_ROOT="${1:-$(pwd)}"
if [ ! -d "$HOST_ROOT" ]; then
  echo "record-starting-state: no such directory: $HOST_ROOT" >&2
  exit 2
fi
HOST_ROOT="$(cd "$HOST_ROOT" && pwd)"

emit() {  # action commit
  python3 - "$1" "$2" << 'PYEOF'
import json, sys
print(json.dumps({
    "severity": "ok",
    "code": "starting-state",
    "action": sys.argv[1],
    "starting_commit": sys.argv[2],
}))
PYEOF
}

# --- history already stands: leave it alone -------------------------------------------------------
if git -C "$HOST_ROOT" rev-parse --verify HEAD > /dev/null 2>&1; then
  first="$(git -C "$HOST_ROOT" rev-list --max-parents=0 HEAD | tail -n 1)"
  echo "skip (already tracked): this project's history starts at $first"
  emit already-tracked "$first"
  exit 0
fi

# --- no history: initialise where needed, then commit the files as found --------------------------
if ! git -C "$HOST_ROOT" rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  git -C "$HOST_ROOT" -c init.defaultBranch=main init -q
fi

# Commit with the machine's own git identity where it has one, and with the pack's fallback where it
# does not — a project joining on a fresh machine must not fail on an unset identity.
ident=()
if ! git -C "$HOST_ROOT" config user.email > /dev/null 2>&1; then
  ident=(-c "user.name=live-spec" -c "user.email=live-spec@localhost")
fi

git -C "$HOST_ROOT" add -A
git -C "$HOST_ROOT" ${ident[@]+"${ident[@]}"} commit -q --allow-empty \
  -m "Starting state, as found when live-spec joined"

STARTING="$(git -C "$HOST_ROOT" rev-parse HEAD)"
echo "committed the files as found: $STARTING"
echo "to see what has changed since, run this from the project root:"
echo "    git diff $STARTING --stat"
emit committed "$STARTING"
