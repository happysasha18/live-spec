#!/usr/bin/env bash
# check-skill-review.sh — gate (s) of the push gate: a push that substantively changes a skill
# reds unless a skill-creator review record for that change is committed (SPEC INV-208, ROADMAP 419).
#
# THE LAW (the owner's word, 2026-07-17 ~18:26): the session is leaned on to remember to run Anthropic's
# skill-creator review whenever a skill is modified, and the session forgets — a reminder does not
# hold. So the habit becomes a machine: when a diff about to be pushed changes a skill's body, the
# push reds until a matching review record exists. This is the same shape as check-prover-record.sh,
# which reds a push whose spec/architecture delta carries no fresh prover record.
#
# Usage: check-skill-review.sh [review-dir]
#   review-dir  defaults to docs/skill-review (relative to the repo root)
#
# WHAT COUNTS AS A CHANGED SKILL. The gate reads the push range (the same base ladder as
# check-prover-record.sh: LIVE_SPEC_DIFF_BASE if set — CI passes github.event.before, a planted
# test passes the base commit — else origin/main, else HEAD~1) and looks at every changed file
# under skills/. A skill is SUBSTANTIVELY changed when a changed file under it carries at least one
# added or removed content line that is NOT a version stamp.
#
# THE VERSION-STAMP CARVE-OUT (crucial). scripts/stamp-versions.py rewrites two things in a skill's
# SKILL.md at every version bump: the frontmatter `  version: X.Y.Z` line, and the in-text
# `live-spec-base (vX.Y.Z)` base-reference. That is a machine-stamped copy of one fact (the pack
# version), not a change to the skill's instructions, so it owes NO skill-creator review. A changed
# line is EXEMPT when it is exactly the frontmatter version line, or when it carries the
# base-reference token — so a file whose ONLY changed lines are stamps is not a substantive change.
# A change to the skill's body / instructions / logic leaves a non-stamp changed line, and that is
# what requires the review.
#
# THE RECORD. For each substantively-changed skill <name>, the gate requires a COMMITTED record
# under <review-dir> that (1) names the skill, (2) carries the SKILL-REVIEW marker and a Verdict:
# line, and (3) is FRESH — the newest commit touching <review-dir> is at least as new as the newest
# commit touching that skill (equal, or an ancestor of the record's commit — the record may ship in
# the same commit as the skill change it covers). A stale record from an earlier review does not
# cover a later change, mirroring check-prover-record.sh's freshness rule.
#
# Exit 0 = every substantively-changed skill carries a fresh review record (or none changed).
# Exit 1 = at least one substantively-changed skill has no matching record.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

REVIEW_DIR="${1:-docs/skill-review}"

# The frontmatter stamp: `  version: X.Y.Z` on its own. The base-reference stamp: any line carrying
# the `live-spec-base` (vX.Y.Z) token. A changed line matching either is a pure stamp.
STAMP_VERSION_RE='^  version: [0-9]+\.[0-9]+\.[0-9]+[[:space:]]*$'
STAMP_BASEREF_RE='`live-spec-base` \(v[0-9]+\.[0-9]+\.[0-9]+\)'

# --- resolve the push range's base (same ladder as check-prover-record.sh) ---
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
  echo "OK (skill review): no push range resolves (single-commit tree, no origin/main) — no skill"
  echo "  change can be measured, so none is required."
  exit 0
fi

# --- which skills changed substantively in the range? ---
changed_files="$(git diff --name-only "$DIFF_BASE" HEAD -- 'skills/' || true)"

substantive_skills=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  # the changed content lines for this file (added or removed), minus the +++/--- headers
  diff_body="$(git diff -U0 "$DIFF_BASE" HEAD -- "$f" | grep -E '^[+-]' | grep -Ev '^(\+\+\+|---)' || true)"
  # drop the leading +/-, then strip out stamp lines and blank lines; whatever remains is substance
  remainder="$(printf '%s\n' "$diff_body" \
      | sed -E 's/^[+-]//' \
      | grep -Ev "$STAMP_VERSION_RE" \
      | grep -Ev "$STAMP_BASEREF_RE" \
      | grep -vE '^[[:space:]]*$' || true)"
  if [ -n "$remainder" ]; then
    # skills/<name>/... -> <name>
    name="$(printf '%s' "$f" | sed -E 's#^skills/([^/]+)/.*#\1#')"
    case " $substantive_skills " in
      *" $name "*) : ;;
      *) substantive_skills="$substantive_skills $name" ;;
    esac
  fi
done <<< "$changed_files"

substantive_skills="$(printf '%s' "$substantive_skills" | tr -s ' ' | sed 's/^ //;s/ $//')"

if [ -z "$substantive_skills" ]; then
  echo "OK (skill review): the push changes no skill body (a pure version-stamp diff owes no review),"
  echo "  so the skill-creator-review gate stands down by name (SPEC INV-208)."
  exit 0
fi

# --- the freshest committed record file under the review dir ---
RECORD_COMMIT="$(git log -1 --format=%H -- "$REVIEW_DIR" 2>/dev/null || true)"

fail=0
for name in $substantive_skills; do
  skill_commit="$(git log -1 --format=%H -- "skills/$name" 2>/dev/null || true)"

  # find a COMMITTED record that names this skill, carries the marker, and carries a verdict
  matched=""
  while IFS= read -r rec; do
    [ -z "$rec" ] && continue
    case "$(basename "$rec")" in README.md) continue ;; esac   # the home doc is not a record
    git ls-files --error-unmatch "$rec" >/dev/null 2>&1 || continue   # committed only
    body="$(cat "$rec")"
    # A here-string reads the whole body. A pipe into `grep -q` loses the race once a record
    # outgrows the pipe buffer: grep leaves at the first hit and the writer takes SIGPIPE.
    grep -q "SKILL-REVIEW" <<<"$body" || continue
    grep -qiE '^Verdict:' <<<"$body" || continue
    grep -qw "$name" <<<"$body" || continue
    matched="$rec"
    break
  done < <(git ls-files "$REVIEW_DIR" 2>/dev/null)

  if [ -z "$matched" ]; then
    echo "FAIL (skill review): skill '$name' is substantively changed in this push but no committed"
    echo "  skill-creator review record under $REVIEW_DIR/ names it with a verdict (SPEC INV-208)."
    fail=1
    continue
  fi

  # freshness: the review dir's newest commit must be at least as new as the skill's
  if [ -n "$RECORD_COMMIT" ] && [ -n "$skill_commit" ]; then
    if [ "$RECORD_COMMIT" != "$skill_commit" ] && \
       ! git merge-base --is-ancestor "$skill_commit" "$RECORD_COMMIT" 2>/dev/null; then
      echo "FAIL (skill review): the review record for '$name' predates the skill's last change —"
      echo "  a stale earlier review does not cover a later change (SPEC INV-208)."
      echo "  skill '$name' last changed in $skill_commit; newest $REVIEW_DIR/ commit is $RECORD_COMMIT."
      fail=1
      continue
    fi
  fi

  echo "OK (skill review): skill '$name' carries a fresh review record ($matched)."
done

if [ "$fail" -ne 0 ]; then
  echo "  Fix: run Anthropic's skill-creator review over the changed skill, then save its verdict as"
  echo "  $REVIEW_DIR/$(date +%Y-%m-%d)-<skill>.md (a SKILL-REVIEW record naming the skill and its"
  echo "  verdict) and commit it before pushing. A pure version-stamp bump is exempt by construction."
  exit 1
fi

exit 0
