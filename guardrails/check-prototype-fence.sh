#!/usr/bin/env bash
# check-prototype-fence.sh — gate (e) of the push gate: the prototype fence
# (SPEC INV-17 / E-17). A prototype lives in a fenced home (a `prototype/` folder);
# a PROD file referencing anything inside that home is RED at push.
#
# This gate catches STRUCTURAL wiring — a prod file naming/loading a fenced file
# (e.g. a <script src="prototype/sketch.html">, an import path, a link target) —
# not narrative mentions. Narrative homes are excluded by list: docs/, attic/,
# inbox/, JOURNAL.md, ROADMAP.md, NEXT_STEPS.md, and any README.md under
# guardrails/, plus .live-spec/ (this pack's own working state) — a project can
# talk ABOUT a prototype in its journal or docs without that being a wiring fault.
#
# Usage: check-prototype-fence.sh [repo-root] [fence-dir-name]
#   repo-root       defaults to `git rev-parse --show-toplevel`
#   fence-dir-name  defaults to "prototype" — a host renames its fence home by
#                   passing this argument (e.g. "sketches", "labs")
#
# If no fence directory exists (or it exists but is empty), there is nothing to
# fence yet: OK. Otherwise every file under the fence dir is grepped for, by its
# repo-relative path, across all git-tracked files outside the exclusion list;
# any hit is a structural reference into the fenced home and fails the gate.

# contract: BLOCKING gate (SPEC INV-47) — on red, one typed failure line beside the human lines.

set -euo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel)}"
FENCE_NAME="${2:-prototype}"
cd "$REPO_ROOT"

FENCE_DIR="$REPO_ROOT/$FENCE_NAME"

if [ ! -d "$FENCE_DIR" ]; then
  echo "OK (prototype fence): no prototype home present."
  exit 0
fi

fenced_files=()
while IFS= read -r -d '' f; do
  fenced_files+=("${f#"$REPO_ROOT"/}")
done < <(find "$FENCE_DIR" -type f -print0)

if [ ${#fenced_files[@]} -eq 0 ]; then
  echo "OK (prototype fence): prototype home present but empty."
  exit 0
fi

scan_files="$(git ls-files | grep -Ev \
  -e "^${FENCE_NAME}/" \
  -e "^docs/" \
  -e "^attic/" \
  -e "^inbox/" \
  -e "^\.live-spec/" \
  -e "(^|/)JOURNAL\.md\$" \
  -e "(^|/)ROADMAP\.md\$" \
  -e "(^|/)NEXT_STEPS\.md\$" \
  -e "^guardrails/.*README\.md\$" \
  || true)"

# One pass rather than a grep per (fenced path, scanned file) pair: the fixed-string patterns go
# into one file and every scanned file is read once. The pair-wise walk cost minutes on a tree with
# a few hundred fenced files, which is a quarter of the suite's whole wall time for one gate.
hits=()
if [ -n "$scan_files" ]; then
  pattern_file="$(mktemp)"
  printf '%s\n' "${fenced_files[@]}" > "$pattern_file"
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    f="${line%%:*}"
    rel="${line#*:}"
    hits+=("$f references $rel")
  done < <(printf '%s\n' "$scan_files" \
    | tr '\n' '\0' \
    | xargs -0 grep -oHF -f "$pattern_file" -- 2>/dev/null \
    | sort -u || true)
  rm -f "$pattern_file"
fi

if [ ${#hits[@]} -gt 0 ]; then
  for h in "${hits[@]}"; do
    echo "FAIL (prototype fence): $h"
  done
  echo "  Fix: a prod file must not reference into a prototype home (SPEC INV-17); promote through the pipeline or remove the reference."
  echo '{"severity":"error","code":"prototype-fence","message":"a prod file references into a prototype home","fix":"promote through the pipeline or remove the reference (SPEC INV-17)"}'
  exit 1
fi

echo "OK (prototype fence): ${#fenced_files[@]} fenced file(s), no prod references."
exit 0
