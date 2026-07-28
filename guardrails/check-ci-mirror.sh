#!/usr/bin/env bash
# check-ci-mirror.sh — the CI mirror carries every local gate (SPEC INV-210, gate u).
#
# The push gate lives twice: guardrails/pre-push runs it on this machine, and
# .github/workflows/gates.yml re-runs it in CI as the second, any-machine net (SPEC M-5).
# gates.yml is hand-maintained, so it drifts the moment a gate is added locally and the CI
# file is not touched — the worked instance: gates h, k, and n were missing from CI on
# 2026-07-18, so a push a green CI would wave through could still fail the local gate.
#
# This check reads the gate letters pre-push invokes (the "-- gate X:" markers) and the gate
# letters gates.yml invokes (the "gate X" tokens in its step names), subtracts the declared CI
# carve-outs (guardrails/ci-mirror.json — the gates a CI checkout legitimately cannot or need
# not re-run, each with its reason), and reds on any local gate letter missing from CI, naming
# the gate and the one fix. It is the kin of config-health (gate m): that proves the installed
# hook matches its source, this proves the CI mirror matches the source too.

set -euo pipefail

# Resolve the repo root from the script's own location, not git, so the check runs the same in
# a scratch copy the suite makes (the scratch tree drops .git by design) as on the real tree.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PREPUSH="${CI_MIRROR_PREPUSH:-$REPO_ROOT/guardrails/pre-push}"
GATES_YML="${CI_MIRROR_GATES_YML:-$REPO_ROOT/.github/workflows/gates.yml}"
CARVE_JSON="${CI_MIRROR_JSON:-$REPO_ROOT/guardrails/ci-mirror.json}"

for f in "$PREPUSH" "$GATES_YML" "$CARVE_JSON"; do
  if [ ! -f "$f" ]; then
    echo "ci-mirror: cannot read $f — the gate stands on all three files."
    exit 1
  fi
done

fail=0

# Local gate letters: the "-- gate X:" markers pre-push echoes before each gate.
local_letters="$(grep -oE -- '-- gate [a-z]{1,2}:' "$PREPUSH" | grep -oE '[a-z]{1,2}:' | tr -d ':' | sort -u || true)"

# CI gate letters: the "gate X" tokens inside gates.yml step names (a "name:" line).
ci_letters="$(grep -E 'name:.*gate [a-z]' "$GATES_YML" | grep -oE 'gate [a-z]{1,2}' | grep -oE '[a-z]{1,2}$' | sort -u || true)"

# Declared carve-outs: gates a CI checkout does not re-run, each with its reason.
carve="$(jq -r '.ci_excluded | keys[]' "$CARVE_JSON" | sort -u || true)"

in_set() {  # in_set <letter> <newline-separated set>
  printf '%s\n' $2 | grep -qx "$1"
}

# A carve-out must name a real local gate — a stale carve-out is itself drift.
for c in $carve; do
  if ! in_set "$c" "$local_letters"; then
    echo "ci-mirror: carve-out '$c' in ci-mirror.json names no local pre-push gate — remove the stale carve-out."
    fail=1
  fi
done

# Every local gate letter must be mirrored in CI, or declared a carve-out with its reason.
for g in $local_letters; do
  if in_set "$g" "$ci_letters"; then
    continue
  fi
  if in_set "$g" "$carve"; then
    continue
  fi
  echo "ci-mirror: gate $g runs in guardrails/pre-push but is absent from .github/workflows/gates.yml — add its step to gates.yml, or declare it in guardrails/ci-mirror.json with the reason it stays out of CI."
  fail=1
done

if [ "$fail" -eq 0 ]; then
  echo "ci-mirror: OK (every local pre-push gate is mirrored in CI or a declared carve-out)."
fi
exit "$fail"
