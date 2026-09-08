#!/usr/bin/env bash
# check-prover-record.sh — gate (a) of the push gate: a fresh, committed prover record
# covering the pushed range must exist before a push, and that record must be fresh for BOTH guarded
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
# THE STAND-DOWN MARKER CONVENTION (the REFUSE of 2026-08-15 23:41, finding F2). Every arm in
# this chain that can let a push past the record demand — an arm that exits 0 without a record
# on file — carries, immediately above it, one line of the exact shape:
#
#   # STAND-DOWN: <name>
#
# <name> is a single token, and PRODUCT_SPEC.md R226 criterion 6 must carry that same token in
# the exception it names. guardrails/pre-push carries the same marker over the deletion-only
# stand-down, which stands the whole chain down ahead of gate a. The convention exists so a
# test can enumerate the stand-downs THE CODE IMPLEMENTS rather than the ones a person
# remembered to list: tests/test_deletion_only_push.py greps these markers and holds both
# directions — every marker is named by criterion 6, and every exception criterion 6 names has
# a marker. An arm added here without its marker, or a marker whose name criterion 6 does not
# carry, reds that test. The two must be edited together.
#
# Usage: check-prover-record.sh [--push] [prover-dir] [YYYY-MM-DD]
#   prover-dir  defaults to docs/prover (relative to the repo root)
#   date        defaults to today, and is used for one thing: the filename this script SUGGESTS
#               when it refuses. No arm below reads it.
#
# "Present and committed" means: at least one file under <prover-dir> named YYYY-MM-DD*.md is
# tracked by git (git ls-files sees it). Every such file is a candidate whatever date its name
# carries; a scratch file sitting untracked in the working tree is refused by name. This script
# matched <prover-dir>/<date>*.md until 2026-09-09, when the owner retired the arm: a landing
# reviewed at 23:50 and pushed at 00:05 was told it carried no review at all.
#
# Freshness rule (row 61, SPEC M-6; extended row 271, INV-116): a committed record is not enough
# on its own — it can be a record for a STALE state if PRODUCT_SPEC.md or ARCHITECTURE.md changed
# again after it landed. So the newest commit touching <prover-dir> has to be at least as new as
# the newest commit touching PRODUCT_SPEC.md, and separately at least as new as the newest commit
# touching ARCHITECTURE.md (equal, or the document's commit is an ancestor of the record's
# commit — a record may ship in the very same commit as the document change it covers).
#
# On the push road one more arm follows: a record has to name the base commit and every commit
# being pushed. Those two arms are the whole of what decides here.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

# Where this script itself lives (never the judged repo's root, which a scratch/fixture run can
# point elsewhere) — the classifier module it calls (case_or_space_only.py) always ships beside it.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Two roads (row 571, the cost audit's repair b), and neither reads a calendar. Both take every
# committed record as a candidate. The PUSH road (--push; pre-push and CI pass it) keeps the one
# that covers the pushed range; the default WORK road serves an ordinary suite run and asks only
# that the newest be fresh. What decides in both is the same pair of arms below: the record is no
# older than PRODUCT_SPEC.md or ARCHITECTURE.md, and — on the push road — it names the base commit
# and every commit being pushed.
#
# The push road demanded a record whose FILENAME began with today's date until 2026-09-09, when
# that arm was retired: a minute before midnight and a minute after change nothing, and the demand
# was machinery serving itself. A landing reviewed at 23:50 and pushed at 00:05 had been told it
# carried no review at all, and what cleared it was a second record written to satisfy the clock.
# The date settles nothing the two arms do not settle. This script's own work road had carried the
# same reasoning for months — "a clean tree after midnight is not a defect" — on the road where
# nothing enforced it. JOURNAL.md's entry for that day holds the exchange.
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

# STAND-DOWN: inbox-deposit
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

# Carve-out (SPEC M-6, R226 criterion 6): a push whose ENTIRE diff is only a change in letter
# case and/or whitespace changes nothing a reader reads for meaning, so it owes no fresh prover
# record either. Judged over the same DIFF_BASE this gate already resolved, and — like the
# recordless-class arm below — never against the HEAD~1 last-resort base, so a multi-commit push
# can never be waved through on the shape of its last commit alone.
# STAND-DOWN: case-or-space
if [ -n "$DIFF_BASE" ] && [ "$DIFF_BASE_LAST_RESORT" -ne 1 ] && \
   python3 "$SCRIPT_DIR/case_or_space_only.py" "$DIFF_BASE" HEAD; then
  echo "OK (prover record): stand-down — the pushed diff is only a change in letter case and/or"
  echo "  whitespace (the case-or-space carve-out); no fresh prover record is owed."
  exit 0
fi

# Every committed record is a candidate on both roads, newest filename first, and the arms below
# pick: the freshness arms refuse one older than a guarded document, and the push road's range arm
# keeps the one naming the base and every pushed commit. A record's own filename date orders this
# list and decides nothing in it.
candidates=()
while IFS= read -r f; do
  [ -n "$f" ] && candidates+=("$f")
done <<< "$(git ls-files "$PROVER_DIR" | grep -E '/[0-9]{4}-[0-9]{2}-[0-9]{2}.*\.md$' | sort -r || true)"

# Recordless class (the owner's word, agent card rule 1; narrowed to records alone by the
# adversarial REFUSE of 2026-08-15 23:41, findings F1–F3, grounded in his north star of
# honest conservative proof): a pushed range whose every commit touches only the RECORD
# DIRECTORIES earns no prover record of its own, and this gate stands down for it by name,
# ahead of the record-missing FAIL below. The class is exact, and it is only these three:
#   docs/prover/  docs/skill-review/  docs/language-reads/
# Every other path rides the full record demand. .live-spec/, tests/, TEST_MATRIX.md,
# guardrails/ and .github/workflows/ are all OUT. The earlier, wider class let a reviewer
# build a live range that gutted the strict test and rewrote the rules card recordlessly —
# the exempted range changed the very rules and tests that decide what a record must hold.
# Enforcement machinery must never exempt itself: rules, tests and gates are exactly the
# code this push chain trusts to hold the line, so a change to any of them earns no free
# pass from the record it enforces on everything else. What stays in the class is what
# carries no behaviour of its own: the written records of reviews and reads.
# A range where any commit touches one file outside this class keeps the full record demand.
# This arm runs on the PUSH road only, using the range already derived above, and only where
# no record was found — a range with a record on file keeps every existing behavior below —
# and only against a base a real push would resolve (never the HEAD~1 last resort).
# STAND-DOWN: recordless
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
          docs/prover/*|docs/skill-review/*|docs/language-reads/*) ;;
          *) rc_all_in_class=0 ;;
        esac
      done <<< "$rc_paths"
    done <<< "$rc_range_commits"
    if [ "$rc_all_in_class" -eq 1 ]; then
      echo "OK (prover record): stand-down — every commit in $DIFF_BASE..HEAD touches only the"
      echo "  owner's recordless class, the record directories alone (docs/prover/, docs/skill-review/,"
      echo "  docs/language-reads/), agent card rule 1, narrowed by the REFUSE of 2026-08-15 23:41;"
      echo "  no fresh prover record is owed for this push."
      exit 0
    fi
  fi
fi

if [ ${#candidates[@]} -eq 0 ]; then

  # A scratch file in the working tree is the near miss worth naming: the record was written and
  # never committed, and the candidate list is built from git, so nothing above would have seen it.
  shopt -s nullglob
  on_disk=("$PROVER_DIR"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*.md)
  shopt -u nullglob
  if [ ${#on_disk[@]} -gt 0 ]; then
    echo "FAIL (prover record): a review record exists on disk and none are committed to git:"
    printf '  %s\n' "${on_disk[@]}"
    echo "  A scratch file in the working tree is not the evidence a push stands on."
    echo "  Fix: ask your agent to add and commit the file(s) above before pushing."
    exit 1
  fi
  echo "FAIL (prover record): $PROVER_DIR/ holds no committed record at all — this push carries no"
  echo "  written review of the spec and the architecture. Every push needs one, covering the range"
  echo "  it pushes and committed (SPEC M-6). Its filename's date orders the directory and settles"
  echo "  nothing: a record written before midnight covers the push that follows it."
  echo "  Fix: ask your agent to run the review (the product-prover pass) and commit its record as $PROVER_DIR/$TODAY-<slug>.md."
  exit 1
fi

# Every candidate came out of `git ls-files`, so the tracked/untracked split the list used to walk
# has nothing left to decide: an uncommitted record is refused above, by name, before this.
tracked=("${candidates[@]}")

# Listing every committed record would bury the verdict, so the count and the newest stand for the
# set; on the push road the range arm below names the one that actually covers this push.
echo "OK (prover record): ${#tracked[@]} committed record(s) to pick from; the newest is ${tracked[0]}."

# The spec is ONE document written across the core and, once its parts map names them, the files
# under spec/. Freshness reads the newest commit touching any of them, so a change landing in a part
# is not invisible here; naming a path with no commits yet simply contributes nothing.
SPEC_COMMIT=$(git log -1 --format=%H -- PRODUCT_SPEC.md spec/)
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
    echo "  The spec changed after that record was written, so the record no longer covers what's being pushed."
    echo "  PRODUCT_SPEC.md last changed in commit $SPEC_COMMIT; newest docs/prover/ commit is $RECORD_COMMIT."
    echo "  Fix: ask your agent to re-run the review over the current spec and commit a fresh record (SPEC M-6)."
    exit 1
  fi

  echo "OK (freshness): record commit is not older than the last PRODUCT_SPEC.md commit."
fi

# The architecture is the same shape as the spec: ONE document written across the core and, once
# its own Parts map names them, the files under architecture/. Freshness reads the newest commit
# touching either, the same reasoning as SPEC_COMMIT above.
ARCH_COMMIT=$(git log -1 --format=%H -- ARCHITECTURE.md architecture/)
if [ -n "$ARCH_COMMIT" ]; then
  arch_fresh=0
  if [ "$ARCH_COMMIT" = "$RECORD_COMMIT" ]; then
    arch_fresh=1
  elif git merge-base --is-ancestor "$ARCH_COMMIT" "$RECORD_COMMIT"; then
    arch_fresh=1
  fi
  if [ "$arch_fresh" -ne 1 ]; then
    echo "FAIL (prover record): the newest committed prover record predates the last ARCHITECTURE.md change."
    echo "  The architecture changed after that record was written, so the record no longer covers what's being pushed."
    echo "  ARCHITECTURE.md last changed in commit $ARCH_COMMIT; newest docs/prover/ commit is $RECORD_COMMIT."
    echo "  Fix: ask your agent to re-run the review over the current architecture and commit a fresh record (SPEC M-6/INV-116)."
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

FIX_LINE="  Fix: ask your agent to read through the actual pushed changes looking for reasons to
  refuse them, then record what it found in $PROVER_DIR/$TODAY-<slug>.md."

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
  echo "FAIL (prover record): this change hasn't been reviewed since it was last edited — the newest"
  echo "  record under $PROVER_DIR/ predates the newest commit in the pushed range, so it covers a"
  echo "  version already left behind (SPEC INV-304)."
  echo "  newest reviewed commit: $NEWEST_REVIEWED; newest $PROVER_DIR/ commit: ${RECORD_COMMIT:-none}."
  echo "$FIX_LINE"
  exit 1
fi

# --- arm: a record names the base commit and every reviewed commit ---
matched=""
missing_report=""
# The report names the three newest records it walked and counts the rest. Every record on file is
# a candidate now, so a loop that printed one line each put 44.9 KB inside a pre-push hook and left
# the FAIL on line 4 of it — the same reasoning the passing message above already carried, withheld
# from the message a person actually needs to read (the closure review of q-830).
reported=0
considered=0
for rec in "${tracked[@]}"; do
  # The committed bytes, never the working tree's: a record edited in place and left uncommitted is
  # a scratch file however old its commit is, and the retired date filter used to refuse it by name
  # (the closure review of q-830).
  body="$(git show "HEAD:$rec" 2>/dev/null || true)"
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
  if [ "$reported" -lt 3 ]; then
    missing_report="$missing_report
  $rec names none of:$misses"
    reported=$((reported + 1))
  fi
  considered=$((considered + 1))
done

if [ -z "$matched" ]; then
  echo "FAIL (prover record): no committed record under $PROVER_DIR/ names the pushed range — every"
  echo "  record on file was written about some other change, not this one (SPEC INV-304)."
  echo "  the pushed range is $BASE_SHORT..$(git rev-parse --short=7 HEAD), $reviewed_count commit(s) reviewed."
  echo "  $considered committed record(s) were read; the newest few and what each one misses:$missing_report"
  echo "$FIX_LINE"
  exit 1
fi

# --- arm: the record carries the marker and each field with a value ---
body="$(git show "HEAD:$matched" 2>/dev/null || true)"
shape_fail=0

# The same whole-body read the hash match uses: a pipe into `grep -q` reports a marker the record
# carries as absent once the body outgrows the pipe buffer.
case "$body" in
  *"PUSH-REVIEW"*) ;;
  *)
    echo "FAIL (prover record): the record isn't written in the shape this gate expects (SPEC INV-304)."
    shape_fail=1
    ;;
esac

for field in "Mode" "Range" "Files read" "Checks run" "Findings" "Blocking"; do
  line="$(grep -m1 -E "^${field}:" <<<"$body" || true)"
  if [ -z "$line" ]; then
    echo "FAIL (prover record): the review record is missing its \`${field}:\` line, so it doesn't say"
    echo "  what the review covered there (SPEC INV-304)."
    shape_fail=1
    continue
  fi
  value="$(printf '%s' "$line" | sed -E "s/^${field}:[[:space:]]*//")"
  if [ -z "$value" ]; then
    echo "FAIL (prover record): the record's \`${field}:\` line is empty — it names the field but says"
    echo "  nothing under it (SPEC INV-304)."
    shape_fail=1
  fi
done

# --- arm: the mode this review ran in, and the scope a global one names ---
# A push review runs as closure or as global (skills/product-prover-pack/SKILL.md). Closure reads
# the accepted row alone and blocks on material failure; global is owed by the owner's own request
# or by a row touching a critical cross-cutting surface, and it names that surface before it reads.
# The mode decides what the review was allowed to cover, so a record that does not name it says
# nothing about its own reach, and a global one that names no scope is the unbounded read this
# whole contract exists to end.
mode_line="$(grep -m1 -E '^Mode:' <<<"$body" || true)"
mode_value="$(printf '%s' "$mode_line" | sed -E 's/^Mode:[[:space:]]*//' | tr '[:upper:]' '[:lower:]')"
case "$mode_value" in
  closure) ;;
  global)
    scope="$(grep -m1 -E '^Scope:' <<<"$body" | sed -E 's/^Scope:[[:space:]]*//' || true)"
    if [ -z "$scope" ]; then
      echo "FAIL (prover record): the record says its mode is global and names no \`Scope:\`. A global"
      echo "  review is owed for one critical surface and reads that surface; a global read with no"
      echo "  scope on the record is the unbounded review this contract ends (SPEC INV-304)."
      shape_fail=1
    fi
    ;;
  "") ;;  # the missing-field arm above has already said so
  *)
    echo "FAIL (prover record): \`Mode: $mode_value\` is not a mode a review runs in. The two are"
    echo "  closure and global (skills/product-prover-pack/SKILL.md)."
    shape_fail=1
    ;;
esac

if [ "$shape_fail" -ne 0 ]; then
  echo "  Fix: ask your agent to fill in the record's fields — the shape they should follow is"
  echo "  written out in $PROVER_DIR/README.md."
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
    echo "FAIL (prover record): the review found a real problem that is neither closed nor explained yet:"
    printf '  %s\n' "$offenders"
    echo "  A blocking finding has to be fixed, or the record has to say why it's being left as-is (SPEC INV-304)."
    echo "  Fix: ask your agent to either fix the problem and write \`closed: <what changed>\`, or write"
    echo "  \`stands: <why>\` if it is staying as-is for now."
    exit 1
  fi
fi

echo "OK (push range): $matched covers the pushed range $BASE_SHORT..$(git rev-parse --short=7 HEAD)"
echo "  — $reviewed_count commit(s) reviewed."
echo "  This gate holds the record's presence, its commit, its freshness, its range and its fields."
echo "  Whether the review was adversarial rests on the reviewer; no script decides that."
exit 0
