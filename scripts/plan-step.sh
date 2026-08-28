#!/usr/bin/env bash
# Print exactly one PLAN.md task by id — the state-probe output plus this file's
# section is what a session reads to take a step, instead of the whole plan (plan-17).
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $(basename "$0") <task-id>   e.g. plan-step.sh plan-17" >&2
  exit 2
fi

ID="$1"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLAN="$DIR/PLAN.md"

START=$(grep -n "^### .*— id: $ID\$" "$PLAN" | head -1 | cut -d: -f1)
if [ -z "$START" ]; then
  echo "no task with id: $ID" >&2
  exit 1
fi

# A step ends at the next task heading OR at the next section heading. Stopping only at `^### `
# meant the last task in `## Tasks` ran on into `## Blockers` and everything after it: asking for
# one step printed 533 of the plan's lines, which is the whole of what this reader exists to
# avoid (adversarial review, 28.08).
END=$(awk -v start="$START" 'NR>start && (/^### / || /^## /){print NR; exit}' "$PLAN")
if [ -z "$END" ]; then
  END=$(wc -l < "$PLAN")
  sed -n "${START},${END}p" "$PLAN"
else
  sed -n "${START},$((END-1))p" "$PLAN"
fi
