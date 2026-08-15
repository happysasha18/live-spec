#!/usr/bin/env bash
# check-prover-record.sh — gate (a) of the push gate: a fresh, committed prover record
# dated today must exist before a push, and that record must be fresh for BOTH guarded
# documents — PRODUCT_SPEC.md and ARCHITECTURE.md (SPEC M-6, INV-116: every live-spec push
# is preceded by a fresh re-check recorded in docs/prover/, covering the spec and the
# architecture alike).
#
# ONE RECORD PER PUSH (SPEC INV-304). A push once owed two review records to two separate
# gates: this one, and a second adversarial read of the pushed delta kept in its own home.
# The two are one pass, so they are one record. On the PUSH road this gate therefore also
# holds what the second gate held: the record names the pushed range, carries the fields
# that say what the review covered, and leaves no blocking finding open.
#
# THE LAW behind that half. A change that passes every test can still be wrong in ways no
# test asks about. A reviewer briefed to find reasons to refuse the change reads it
# differently from a reviewer set on confirming it, and the difference is what the suite
# misses. So the record a push carries is an adversarial read of the very commits it sends.
#
# THE RECORD. One dated file under <prover-dir>, committed, carrying:
#   PUSH-REVIEW      the marker line
#   Range:           the base commit and the head commit the review read, with the commits
#                    between them listed under it
#   Files read:      the files the reviewer opened
#   Checks run:      the commands the reviewer ran, each with its result
#   Findings:        what the review found; a review that found nothing says so here, and its
#                    coverage stands on the two fields above
#   Blocking:        `none`, or one item per blocking finding, each carrying `closed:` or
#                    `stands:` with the reason it stands
# docs/prover/README.md holds the same shape for a person writing one, and holds no field
# this script leaves unread.
#
# WHAT THIS SCRIPT CAN HOLD: that a record exists, that it is committed rather than a scratch
# file, that it is fresh against the guarded documents and against the pushed range, that it
# names the base commit and every reviewed commit, that it carries each field with a value,
# and that a blocking finding is closed or explained.
#
# WHAT THIS SCRIPT CANNOT HOLD: whether the review was adversarial. No script decides whether
# a reviewer set out to refuse the change or to confirm it, whether the files named were read,
# or whether the findings are the ones the delta deserved. Those rest on the reviewer. This
# gate applies the pressure a machine can apply — the record names the commits, the files, the
# checks and the findings — and leaves the judgment where it belongs.
#
# Usage: check-prover-record.sh [--push] [prover-dir] [YYYY-MM-DD]
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
# DIFF_BASE_LAST_RESORT marks the HEAD~1 fallback: a single-commit-tree-with-no-remote
# expedient for local/synthetic runs, never the base a real push (CI's explicit
# LIVE_SPEC_DIFF_BASE, or a hook's real origin/main) resolves. The recordless-class arm below
# reads it so that arm never fires off a base no real push would ever measure against.
DIFF_BASE_LAST_RESORT=0
if [ -n "${LIVE_SPEC_DIFF_BASE:-}" ] && \
   [ "${LIVE_SPEC_DIFF_BASE}" != "0000000000000000000000000000000000000000" ] && \
   git rev-parse --verify --quiet "${LIVE_SPEC_DIFF_BASE}^{commit}" >/dev/null 2>&1; then
  DIFF_BASE="${LIVE_SPEC_DIFF_BASE}"
elif git rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
  DIFF_BASE="origin/main"
elif git rev-parse --verify --quiet "HEAD~1" >/dev/null 2>&1; then
  DIFF_BASE="HEAD~1"
  DIFF_BASE_LAST_RESORT=1
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
  # Recordless class (the owner's word, agent card rule 1; narrowed by his ruling of
  # 2026-08-15 22:07, grounded in his north star of honest conservative proof): a pushed range
  # whose every commit touches only records, reviews, rules and test machinery earns no prover
  # record of its own, and this gate stands down for it by name, ahead of the record-missing
  # FAIL below. The class is exact:
  #   docs/prover/  docs/skill-review/  docs/language-reads/  .live-spec/  tests/  TEST_MATRIX.md
  # guardrails/ and .github/workflows/ left this class by that ruling: a push touching gate
  # machinery itself demands its record again, since gate machinery is exactly the code this
  # push chain trusts to hold the line — a change to it earns no free pass from the record it
  # enforces on everything else.
  # A range where any commit touches one file outside this class keeps the full record demand.
  # This arm runs on the PUSH road only, using the range already derived above, and only where
  # no record was found — a range with a record on file keeps every existing behavior below —
  # and only against a base a real push would resolve (never the HEAD~1 last resort).
  if [ "$PUSH_ROAD" -eq 1 ] && [ -n "$DIFF_BASE" ] && [ "$DIFF_BASE_LAST_RESORT" -ne 1 ]; then
    rc_range_commits="$(git rev-list "$DIFF_BASE..HEAD" 2>/dev/null || true)"
    if [ -n "$rc_range_commits" ]; then
      rc_all_in_class=1
      while IFS= read -r c; do
        [ -z "$c" ] && continue
        rc_paths="$(git show --pretty=format: --name-only "$c" | grep -v '^[[:space:]]*$' || true)"
        while IFS= read -r p; do
          [ -z "$p" ] && continue
          case "$p" in
            docs/prover/*|docs/skill-review/*|docs/language-reads/*|.live-spec/*|tests/*|TEST_MATRIX.md) ;;
            *) rc_all_in_class=0 ;;
          esac
        done <<< "$rc_paths"
      done <<< "$rc_range_commits"
      if [ "$rc_all_in_class" -eq 1 ]; then
        echo "OK (prover record): stand-down — every commit in $DIFF_BASE..HEAD touches only the"
        echo "  owner's recordless class (records, reviews, rules and test machinery), agent card rule 1,"
        echo "  narrowed by the 2026-08-15 22:07 ruling; no fresh prover record is owed for this push."
        exit 0
      fi
    fi
  fi

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

# ---------------------------------------------------------------------------
# The push half (SPEC INV-304): the same record is the adversarial read of the pushed range.
# These arms ran as their own gate over their own record home until the two records merged
# into one. They run on the PUSH road only — an ordinary suite run measures no push range.
# ---------------------------------------------------------------------------

if [ "$PUSH_ROAD" -ne 1 ]; then
  exit 0
fi

if [ -z "$DIFF_BASE" ]; then
  echo "OK (push range): no push range resolves (a single-commit tree with no origin/main), so no"
  echo "  delta can be measured and none is owed."
  exit 0
fi

BASE_SHA="$(git rev-parse "$DIFF_BASE")"
BASE_SHORT="${BASE_SHA:0:7}"

range_commits="$(git rev-list "$BASE_SHA..HEAD" 2>/dev/null || true)"
if [ -z "$range_commits" ]; then
  echo "OK (push range): the range $DIFF_BASE..HEAD holds no commit, so the push sends nothing to review."
  exit 0
fi

# The reviewed commits: those touching a file outside the record directory. A commit that
# carries the record alone is exempt, since the record cannot name the commit that first ships it.
reviewed=""
while IFS= read -r c; do
  [ -z "$c" ] && continue
  paths="$(git show --pretty=format: --name-only "$c" | grep -v '^[[:space:]]*$' || true)"
  outside="$(printf '%s\n' "$paths" | grep -v "^$PROVER_DIR/" || true)"
  if [ -n "$outside" ]; then
    reviewed="$reviewed $c"
  fi
done <<< "$range_commits"
reviewed="$(printf '%s' "$reviewed" | sed 's/^ //')"

if [ -z "$reviewed" ]; then
  echo "OK (push range): every commit in $DIFF_BASE..HEAD carries the review record alone, so the"
  echo "  range holds no change of its own to review."
  exit 0
fi

reviewed_count="$(printf '%s\n' $reviewed | grep -c '' || true)"
NEWEST_REVIEWED="$(head -1 <<<"$(printf '%s\n' $reviewed)")"

FIX_LINE="  Fix: run an adversarial review over the pushed delta — brief the reviewer to find reasons
  to refuse the change — and carry its findings in the same record, $PROVER_DIR/$TODAY-<slug>.md."

# --- arm: the record is at least as new as the newest commit it must cover ---
range_fresh=0
if [ -n "$RECORD_COMMIT" ]; then
  if [ "$RECORD_COMMIT" = "$NEWEST_REVIEWED" ]; then
    range_fresh=1
  elif git merge-base --is-ancestor "$NEWEST_REVIEWED" "$RECORD_COMMIT" 2>/dev/null; then
    range_fresh=1
  fi
fi

if [ "$range_fresh" -ne 1 ]; then
  echo "FAIL (prover record): the newest committed record under $PROVER_DIR/ predates the newest commit"
  echo "  in the pushed range, so it covers a state this push has already left behind (SPEC INV-304)."
  echo "  newest reviewed commit: $NEWEST_REVIEWED; newest $PROVER_DIR/ commit: ${RECORD_COMMIT:-none}."
  echo "$FIX_LINE"
  exit 1
fi

# --- arm: a record names the base commit and every reviewed commit ---
matched=""
missing_report=""
for rec in "${tracked[@]}"; do
  body="$(cat "$rec")"
  misses=""
  # A shell pattern match reads the whole body in this process. A pipe into `grep -q` reads it
  # wrong: grep exits at the first hit, printf takes SIGPIPE, and `set -o pipefail` then reports
  # the found hash as missing. The longer the record, the more reliably that happens.
  case "$body" in *"$BASE_SHORT"*) ;; *) misses="$misses $BASE_SHORT(base)" ;; esac
  for c in $reviewed; do
    short="${c:0:7}"
    case "$body" in *"$short"*) ;; *) misses="$misses $short" ;; esac
  done
  if [ -z "$misses" ]; then
    matched="$rec"
    break
  fi
  missing_report="$missing_report
  $rec names none of:$misses"
done

if [ -z "$matched" ]; then
  echo "FAIL (prover record): no committed record under $PROVER_DIR/ names the pushed range, so every"
  echo "  record on file covers some other change (SPEC INV-304)."
  echo "  the pushed range is $BASE_SHORT..$(git rev-parse --short=7 HEAD), $reviewed_count commit(s) reviewed.$missing_report"
  echo "$FIX_LINE"
  exit 1
fi

# --- arm: the record carries the marker and each field with a value ---
body="$(cat "$matched")"
shape_fail=0

# The same whole-body read the hash match uses: a pipe into `grep -q` reports a marker the record
# carries as absent once the body outgrows the pipe buffer.
case "$body" in
  *"PUSH-REVIEW"*) ;;
  *)
    echo "FAIL (prover record): $matched carries no PUSH-REVIEW marker (SPEC INV-304)."
    shape_fail=1
    ;;
esac

for field in "Range" "Files read" "Checks run" "Findings" "Blocking"; do
  line="$(grep -m1 -E "^${field}:" <<<"$body" || true)"
  if [ -z "$line" ]; then
    echo "FAIL (prover record): $matched carries no \`${field}:\` field, so the record leaves unsaid what"
    echo "  the review covered (SPEC INV-304)."
    shape_fail=1
    continue
  fi
  value="$(printf '%s' "$line" | sed -E "s/^${field}:[[:space:]]*//")"
  if [ -z "$value" ]; then
    echo "FAIL (prover record): $matched carries \`${field}:\` with no value (SPEC INV-304)."
    shape_fail=1
  fi
done

if [ "$shape_fail" -ne 0 ]; then
  echo "  Fix: fill the record's fields — the shape is in $PROVER_DIR/README.md."
  exit 1
fi

# --- arm: a blocking finding is closed, or the record says why it stands ---
block="$(awk '/^Blocking:/{flag=1} flag{ if ($0 ~ /^[[:space:]]*$/) exit; print }' <<<"$body")"
value="$(sed -E 's/^Blocking:[[:space:]]*//' <<<"$(head -1 <<<"$block")")"
lower="$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:].')"

if [ "$lower" != "none" ]; then
  items="$(printf '%s\n' "$block" | grep -E '^[[:space:]]*-' || true)"
  if [ -n "$items" ]; then
    offenders="$(printf '%s\n' "$items" | grep -vE 'closed:|stands:' || true)"
  else
    offenders="$(printf '%s\n' "$value" | grep -vE 'closed:|stands:' || true)"
  fi
  if [ -n "$offenders" ]; then
    echo "FAIL (prover record): $matched carries a blocking finding that is neither closed nor explained"
    echo "  (SPEC INV-304). A blocking finding holds the push until it is closed, or until the record"
    echo "  states why it stands:"
    printf '  %s\n' "$offenders"
    echo "  Fix: close the finding and write \`closed: <what changed>\`, or write \`stands: <why>\`."
    exit 1
  fi
fi

echo "OK (push range): $matched covers the pushed range $BASE_SHORT..$(git rev-parse --short=7 HEAD)"
echo "  — $reviewed_count commit(s) reviewed."
echo "  This gate holds the record's presence, its commit, its freshness, its range and its fields."
echo "  Whether the review was adversarial rests on the reviewer; no script decides that."
exit 0
