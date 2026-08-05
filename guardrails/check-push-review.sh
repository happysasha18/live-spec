#!/usr/bin/env bash
# check-push-review.sh — gate (ac) of the push gate: the delta a push sends carries a fresh,
# committed adversarial review record (SPEC INV-304).
#
# THE LAW behind it. A change that passes every test can still be wrong in ways no test asks
# about. A reviewer briefed to find reasons to refuse the change reads it differently from a
# reviewer set on confirming it, and the difference is what the suite misses. So a push carries
# such a review of the very commits it is about to send, and the review leaves a record.
#
# Usage: check-push-review.sh [review-dir]
#   review-dir  defaults to docs/push-review (relative to the repo root)
#
# THE RANGE. The gate reads the push range through the base ladder check-prover-record.sh uses:
# LIVE_SPEC_DIFF_BASE if it resolves (a planted test passes a base commit), else origin/main,
# else HEAD~1. The reviewed commits are the commits in that range that touch a file outside the
# review directory. A commit that carries the record alone is exempt, since the record cannot
# name the commit that first ships it.
#
# THE RECORD. One dated file under <review-dir>, committed, carrying:
#   PUSH-REVIEW      the marker line
#   Range:           the base commit and the head commit the review read
#   Files read:      the files the reviewer opened
#   Checks run:      the commands the reviewer ran, each with its result
#   Findings:        what the review found; a review that found nothing says so here, and its
#                    coverage stands on the two fields above
#   Blocking:        `none`, or one item per blocking finding, each carrying `closed:` or
#                    `stands:` with the reason it stands
# docs/push-review/README.md holds the same shape for a person writing one.
#
# WHAT THIS SCRIPT CAN HOLD: that a record exists, that it is committed rather than a scratch
# file, that it is fresh against the pushed range, that it names the base commit and every
# reviewed commit, that it carries each field with a value, and that a blocking finding is
# closed or explained.
#
# WHAT THIS SCRIPT CANNOT HOLD: whether the review was adversarial. No script decides whether a
# reviewer set out to refuse the change or to confirm it, whether the files named were read, or
# whether the findings are the ones the delta deserved. Those rest on the reviewer. This gate
# applies the pressure a machine can apply — the record names the commits, the files, the checks
# and the findings — and leaves the judgment where it belongs.
#
# Exit 0 = the pushed delta carries its fresh record (or the range holds nothing to review).
# Exit 1 = the record is absent, uncommitted, stale, covering another range, or short a field.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

REVIEW_DIR="${1:-docs/push-review}"

FIX_LINE="  Fix: run an adversarial review over the pushed delta — brief the reviewer to find reasons
  to refuse the change — and commit its record as $REVIEW_DIR/$(date +%Y-%m-%d)-<slug>.md."

# --- resolve the push range's base (the ladder check-prover-record.sh uses) ---
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

if [ -z "$DIFF_BASE" ]; then
  echo "OK (push review): no push range resolves (a single-commit tree with no origin/main), so no"
  echo "  delta can be measured and none is owed."
  exit 0
fi

BASE_SHA="$(git rev-parse "$DIFF_BASE")"
BASE_SHORT="${BASE_SHA:0:7}"

range_commits="$(git rev-list "$BASE_SHA..HEAD" 2>/dev/null || true)"
if [ -z "$range_commits" ]; then
  echo "OK (push review): the range $DIFF_BASE..HEAD holds no commit, so the push sends nothing to review."
  exit 0
fi

# --- the reviewed commits: those touching a file outside the review directory ---
reviewed=""
while IFS= read -r c; do
  [ -z "$c" ] && continue
  paths="$(git show --pretty=format: --name-only "$c" | grep -v '^[[:space:]]*$' || true)"
  outside="$(printf '%s\n' "$paths" | grep -v "^$REVIEW_DIR/" || true)"
  if [ -n "$outside" ]; then
    reviewed="$reviewed $c"
  fi
done <<< "$range_commits"
reviewed="$(printf '%s' "$reviewed" | sed 's/^ //')"

if [ -z "$reviewed" ]; then
  echo "OK (push review): every commit in $DIFF_BASE..HEAD carries the review record alone, so the"
  echo "  range holds no change of its own to review."
  exit 0
fi

reviewed_count="$(printf '%s\n' $reviewed | grep -c '' || true)"
NEWEST_REVIEWED="$(printf '%s\n' $reviewed | head -1)"

# --- arm A: a committed record exists ---
tracked_records=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$(basename "$f")" in README.md) continue ;; esac
  tracked_records="$tracked_records $f"
done < <(git ls-files "$REVIEW_DIR" 2>/dev/null || true)
tracked_records="$(printf '%s' "$tracked_records" | sed 's/^ //')"

if [ -z "$tracked_records" ]; then
  echo "FAIL (push review): the push sends $reviewed_count commit(s) and no committed record under"
  echo "  $REVIEW_DIR/ covers them (SPEC INV-304)."
  echo "$FIX_LINE"
  exit 1
fi

# --- arm B: freshness, the rule check-prover-record.sh uses ---
RECORD_COMMIT="$(git log -1 --format=%H -- "$REVIEW_DIR" 2>/dev/null || true)"
fresh=0
if [ -n "$RECORD_COMMIT" ]; then
  if [ "$RECORD_COMMIT" = "$NEWEST_REVIEWED" ]; then
    fresh=1
  elif git merge-base --is-ancestor "$NEWEST_REVIEWED" "$RECORD_COMMIT" 2>/dev/null; then
    fresh=1
  fi
fi

if [ "$fresh" -ne 1 ]; then
  echo "FAIL (push review): the newest committed record under $REVIEW_DIR/ predates the newest commit"
  echo "  in the pushed range, so it covers a state this push has already left behind (SPEC INV-304)."
  echo "  newest reviewed commit: $NEWEST_REVIEWED; newest $REVIEW_DIR/ commit: ${RECORD_COMMIT:-none}."
  echo "$FIX_LINE"
  exit 1
fi

# --- arm C: a record names the base commit and every reviewed commit ---
matched=""
missing_report=""
for rec in $tracked_records; do
  body="$(cat "$rec")"
  misses=""
  printf '%s' "$body" | grep -qF "$BASE_SHORT" || misses="$misses $BASE_SHORT(base)"
  for c in $reviewed; do
    short="${c:0:7}"
    printf '%s' "$body" | grep -qF "$short" || misses="$misses $short"
  done
  if [ -z "$misses" ]; then
    matched="$rec"
    break
  fi
  missing_report="$missing_report
  $rec names none of:$misses"
done

if [ -z "$matched" ]; then
  echo "FAIL (push review): no committed record under $REVIEW_DIR/ names the pushed range, so every"
  echo "  record on file covers some other change (SPEC INV-304)."
  echo "  the pushed range is $BASE_SHORT..$(git rev-parse --short=7 HEAD), $reviewed_count commit(s) reviewed.$missing_report"
  echo "$FIX_LINE"
  exit 1
fi

# --- arm D: the record carries the marker and each field with a value ---
body="$(cat "$matched")"
shape_fail=0

if ! printf '%s' "$body" | grep -q "PUSH-REVIEW"; then
  echo "FAIL (push review): $matched carries no PUSH-REVIEW marker (SPEC INV-304)."
  shape_fail=1
fi

for field in "Range" "Files read" "Checks run" "Findings" "Blocking"; do
  line="$(printf '%s\n' "$body" | grep -m1 -E "^${field}:" || true)"
  if [ -z "$line" ]; then
    echo "FAIL (push review): $matched carries no \`${field}:\` field, so the record leaves unsaid what"
    echo "  the review covered (SPEC INV-304)."
    shape_fail=1
    continue
  fi
  value="$(printf '%s' "$line" | sed -E "s/^${field}:[[:space:]]*//")"
  if [ -z "$value" ]; then
    echo "FAIL (push review): $matched carries \`${field}:\` with no value (SPEC INV-304)."
    shape_fail=1
  fi
done

if [ "$shape_fail" -ne 0 ]; then
  echo "  Fix: fill the record's fields — the shape is in $REVIEW_DIR/README.md."
  exit 1
fi

# --- arm E: a blocking finding is closed, or the record says why it stands ---
block="$(printf '%s\n' "$body" | awk '/^Blocking:/{flag=1} flag{ if ($0 ~ /^[[:space:]]*$/) exit; print }')"
value="$(printf '%s\n' "$block" | head -1 | sed -E 's/^Blocking:[[:space:]]*//')"
lower="$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:].')"

if [ "$lower" != "none" ]; then
  items="$(printf '%s\n' "$block" | grep -E '^[[:space:]]*-' || true)"
  if [ -n "$items" ]; then
    offenders="$(printf '%s\n' "$items" | grep -vE 'closed:|stands:' || true)"
  else
    offenders="$(printf '%s\n' "$value" | grep -vE 'closed:|stands:' || true)"
  fi
  if [ -n "$offenders" ]; then
    echo "FAIL (push review): $matched carries a blocking finding that is neither closed nor explained"
    echo "  (SPEC INV-304). A blocking finding holds the push until it is closed, or until the record"
    echo "  states why it stands:"
    printf '  %s\n' "$offenders"
    echo "  Fix: close the finding and write \`closed: <what changed>\`, or write \`stands: <why>\`."
    exit 1
  fi
fi

echo "OK (push review): $matched covers the pushed range $BASE_SHORT..$(git rev-parse --short=7 HEAD)"
echo "  — $reviewed_count commit(s) reviewed, $(printf '%s\n' $tracked_records | grep -c '') record(s) on file read."
echo "  This gate holds the record's presence, its commit, its freshness, its range and its fields."
echo "  Whether the review was adversarial rests on the reviewer; no script decides that."
exit 0
