#!/usr/bin/env bash
# check-plan-delta.sh — a commit that changes the campaign plan must carry a delta page
# rooting every changed hunk (his word 2026-08-10, evening: a guard against plan edits
# nobody asked for). Local pre-commit step by design — the campaign's rule 2 freezes the
# gate roster, and his word granted this one exception as a LOCAL step only; it enters
# the roster solely by his closing ruling (plan v3, D9).
set -euo pipefail

PLAN=".live-spec/culling-plan-v3-2026-08-10.md"
cd "$(git rev-parse --show-toplevel)"

git diff --cached --name-only | grep -qx "$PLAN" || exit 0

# The plan's first landing has no prior committed version to deviate from.
git cat-file -e "HEAD:$PLAN" 2>/dev/null || { echo "OK (plan delta): initial landing of the plan file."; exit 0; }

DELTA="$(git diff --cached --name-only | grep -E '^\.live-spec/plan-v3-delta-[0-9]{4}-[0-9]{2}-[0-9]{2}[A-Za-z0-9-]*\.md$' | head -1 || true)"
if [ -z "$DELTA" ]; then
  echo "FAIL (plan delta): the commit changes $PLAN and stages no .live-spec/plan-v3-delta-<date>.md page. Every plan change lands with a delta page naming each changed hunk and its root (his request, a review finding, or his standing instruction — dated)." >&2
  exit 1
fi

HUNKS="$(git diff --cached -U0 -- "$PLAN" | grep -c '^@@' || true)"
ROOTS="$(grep -c '^- ' "$DELTA" || true)"
if [ "$ROOTS" -lt "$HUNKS" ]; then
  echo "FAIL (plan delta): $HUNKS changed hunks in the plan, but $DELTA roots only $ROOTS of them (one '- ' line per hunk: what changed, and whose word or which finding forced it)." >&2
  exit 1
fi

echo "OK (plan delta): $HUNKS hunks, $ROOTS rooted lines in $DELTA."
