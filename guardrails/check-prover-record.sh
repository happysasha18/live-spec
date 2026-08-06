#!/usr/bin/env bash
# check-prover-record.sh — gate (a) of the push gate: a fresh, committed prover record
# dated today must exist before a push, and that record must be fresh for BOTH guarded
# documents — PRODUCT_SPEC.md and ARCHITECTURE.md (SPEC M-6, INV-116: every live-spec push
# is preceded by a fresh re-check recorded in docs/prover/, covering the spec and the
# architecture alike).
#
# Usage: check-prover-record.sh [prover-dir] [YYYY-MM-DD]
#   prover-dir  defaults to docs/prover (relative to the repo root)
#   date        defaults to today
#
# "Present and committed" means: at least one file matching <prover-dir>/<date>*.md
# both exists on disk AND is tracked by git (git ls-files sees it) — not just an
# untracked scratch file sitting in the working tree.
#
# Freshness rule (row 61, SPEC M-6; extended row 271, INV-116): a record dated-today-and-
# committed is not enough on its own — it can be a record for a STALE state if PRODUCT_SPEC.md
# or ARCHITECTURE.md changed again after it landed. So after the tracked-record check above
# passes, also require that the newest commit touching <prover-dir> is at least as new as the
# newest commit touching PRODUCT_SPEC.md, and separately at least as new as the newest commit
# touching ARCHITECTURE.md (equal, or the document's commit is an ancestor of the record's
# commit — a record may ship in the very same commit as the document change it covers).

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

# Two roads (row 571, the cost audit's repair b). The PUSH road (--push; pre-push and CI pass
# it) keeps the original demand: a record dated today. The default WORK road serves an ordinary
# suite run: a clean tree after midnight is not a defect, so it also accepts the newest committed
# record of any date — the freshness checks below still refuse it the moment PRODUCT_SPEC.md or
# ARCHITECTURE.md changed after it.
PUSH_ROAD=0
if [ "${1:-}" = "--push" ]; then
  PUSH_ROAD=1
  shift
fi

PROVER_DIR="${1:-docs/prover}"
TODAY="${2:-$(date +%Y-%m-%d)}"

# Carve-out (row 269, SPEC M-6/INV-112): a push whose diff is exactly one NEW file under
# inbox/ — the remote-deposit shape — changes no spec-backed content, so it owes no fresh
# prover record. This mirrors the spec-level carve-out into the gate script, so an inbox
# deposit on a day with no committed record does not red the CI. A diff carrying anything
# more (a second file, an edit, a delete) rides the full gate below.
#   The diff is measured against a BASE ref: LIVE_SPEC_DIFF_BASE if set (CI passes
#   github.event.before, a planted test passes the base commit), else origin/main, else
#   HEAD~1. If no base resolves, the carve-out cannot be judged and the full gate runs.
DIFF_BASE=""
if [ -n "${LIVE_SPEC_DIFF_BASE:-}" ] && \
   [ "${LIVE_SPEC_DIFF_BASE}" != "0000000000000000000000000000000000000000" ] && \
   git rev-parse --verify --quiet "${LIVE_SPEC_DIFF_BASE}^{commit}" >/dev/null 2>&1; then
  DIFF_BASE="${LIVE_SPEC_DIFF_BASE}"
elif git rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
  DIFF_BASE="origin/main"
elif git rev-parse --verify --quiet "HEAD~1" >/dev/null 2>&1; then
  DIFF_BASE="HEAD~1"
fi

if [ -n "$DIFF_BASE" ]; then
  changed="$(git diff --name-status "$DIFF_BASE" HEAD)"
  # exactly one line, status A (added), path under inbox/
  if [ "$(printf '%s' "$changed" | grep -c '')" -eq 1 ] && \
     printf '%s\n' "$changed" | grep -qE '^A[[:space:]]+inbox/'; then
    echo "OK (prover record): carve-out — the pushed diff is exactly one new inbox/ file"
    echo "  (the remote-deposit shape, SPEC M-6/INV-112); no fresh prover record is owed."
    exit 0
  fi
fi

shopt -s nullglob
candidates=("$PROVER_DIR"/"$TODAY"*.md)
shopt -u nullglob

WORK_ROAD_FALLBACK=0
if [ ${#candidates[@]} -eq 0 ] && [ "$PUSH_ROAD" -ne 1 ]; then
  # WORK road fallback: the newest committed record of any date stands in, and the
  # freshness checks below still refuse it if a guarded document changed after it.
  newest=""
  for f in $(git ls-files "$PROVER_DIR" | grep -E '/[0-9]{4}-[0-9]{2}-[0-9]{2}.*\.md$' | sort); do
    newest="$f"
  done
  if [ -n "$newest" ]; then
    candidates=("$newest")
    WORK_ROAD_FALLBACK=1
    echo "NOTE (prover record): no record dated $TODAY; work-run road (row 571) — the newest"
    echo "  committed record stands in while it stays fresh for the guarded documents: $newest"
  fi
fi

if [ ${#candidates[@]} -eq 0 ]; then
  echo "FAIL (prover record): no file matching $PROVER_DIR/$TODAY*.md exists."
  echo "  A fresh whole-spec prover re-check must be recorded before every push (SPEC M-6)."
  echo "  Fix: run the product-prover pass and save its record as $PROVER_DIR/$TODAY-<slug>.md, then commit it."
  exit 1
fi

tracked=()
untracked=()
for f in "${candidates[@]}"; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
    tracked+=("$f")
  else
    untracked+=("$f")
  fi
done

if [ ${#tracked[@]} -eq 0 ]; then
  echo "FAIL (prover record): found today's prover record(s) but none are committed to git:"
  printf '  %s\n' "${untracked[@]}"
  echo "  Fix: git add the file(s) and commit before pushing."
  exit 1
fi

if [ "$WORK_ROAD_FALLBACK" -eq 1 ]; then
  echo "OK (prover record): committed record accepted on the work-run road:"
else
  echo "OK (prover record): committed record(s) for $TODAY found:"
fi
printf '  %s\n' "${tracked[@]}"

SPEC_COMMIT=$(git log -1 --format=%H -- PRODUCT_SPEC.md)
RECORD_COMMIT=$(git log -1 --format=%H -- "$PROVER_DIR")

if [ -z "$SPEC_COMMIT" ]; then
  echo "OK (freshness): no PRODUCT_SPEC.md in git history — spec freshness check skipped."
else
  fresh=0
  if [ "$SPEC_COMMIT" = "$RECORD_COMMIT" ]; then
    fresh=1
  elif git merge-base --is-ancestor "$SPEC_COMMIT" "$RECORD_COMMIT"; then
    fresh=1
  fi

  if [ "$fresh" -ne 1 ]; then
    echo "FAIL (prover record): the newest committed prover record predates the last PRODUCT_SPEC.md change."
    echo "  PRODUCT_SPEC.md last changed in commit $SPEC_COMMIT; newest docs/prover/ commit is $RECORD_COMMIT."
    echo "  SPEC M-6 wants a re-check record for the PUSHED STATE — re-run the prover pass and commit its record after the SPEC change."
    exit 1
  fi

  echo "OK (freshness): record commit is not older than the last PRODUCT_SPEC.md commit."
fi

ARCH_COMMIT=$(git log -1 --format=%H -- ARCHITECTURE.md)
if [ -n "$ARCH_COMMIT" ]; then
  arch_fresh=0
  if [ "$ARCH_COMMIT" = "$RECORD_COMMIT" ]; then
    arch_fresh=1
  elif git merge-base --is-ancestor "$ARCH_COMMIT" "$RECORD_COMMIT"; then
    arch_fresh=1
  fi
  if [ "$arch_fresh" -ne 1 ]; then
    echo "FAIL (prover record): the newest committed prover record predates the last ARCHITECTURE.md change."
    echo "  ARCHITECTURE.md last changed in commit $ARCH_COMMIT; newest docs/prover/ commit is $RECORD_COMMIT."
    echo "  SPEC M-6/INV-116 wants the prover pass to cover ARCHITECTURE.md too — re-run the prover over the architecture and commit its record."
    exit 1
  fi
  echo "OK (freshness): record commit is not older than the last ARCHITECTURE.md commit."
fi

exit 0
