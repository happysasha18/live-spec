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
# THE CASE-OR-SPACE CARVE-OUT. A per-file check ahead of the stamp scan: a changed file whose two
# sides are identical once whitespace is stripped and letter case is folded (see
# guardrails/case_or_space_only.py) contributes nothing to substantive_skills either — a change in
# case or whitespace changes no instruction the model reads differently, so it owes no review.
#
# THE BYTE-IDENTICAL CARVE-OUT (a host's own vendor-sync, PLAN q-814). A host that refreshes its
# skills from the pack byte-for-byte (sync-skills.sh) can land content that is new to the HOST's own
# last commit but not new to this repo's history — the exact same bytes, at the exact same path,
# were committed once before and already carry a covering review record. Re-landing reviewed content
# verbatim is not a fresh edit, so it owes no fresh review. Checked per changed file, after the
# ordinary record search above finds nothing: for each substantively-changed file under the skill,
# the gate walks that file's own commit history (`git log -- <path>`) for an EARLIER commit whose
# blob hash equals the file's current blob hash, and asks whether THAT commit already had a covering
# record (the same name+marker+verdict+freshness match, freshness measured against that earlier
# commit). The skill is satisfied only when EVERY one of its changed files clears this — one
# genuinely new file among them still owes the review, exactly as today.
#
# THE RECORD. For each substantively-changed skill <name>, the gate requires a COMMITTED record
# under <review-dir> that (1) names the skill, (2) carries the SKILL-REVIEW marker and a Verdict:
# line, and (3) is FRESH — THAT RECORD'S OWN commit is at least as new as the skill's own last
# change (equal, or an ancestor of the record's commit — the record may ship in the same commit as
# the skill change it covers). A stale record from an earlier review does not cover a later
# change, mirroring check-prover-record.sh's freshness rule, and a fresh but unrelated commit
# elsewhere under <review-dir> does not launder a stale match for THIS skill either — each
# candidate record is checked on its own commit, not the directory's.
#
# Exit 0 = every substantively-changed skill carries a fresh review record (or none changed).
# Exit 1 = at least one substantively-changed skill has no matching record.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

# Where this script itself lives (never the judged repo's root, which a scratch/fixture run can
# point elsewhere) — the classifier module it calls (case_or_space_only.py) always ships beside it.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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
  # case-or-space carve-out: a file whose whole change is only a change in letter case and/or
  # whitespace changes no instruction a model reads differently, so it contributes nothing to
  # substantive_skills either — the same boundary the prover-record gate stands down for.
  if python3 "$SCRIPT_DIR/case_or_space_only.py" "$DIFF_BASE" HEAD "$f"; then
    continue
  fi
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
  echo "OK (skill review): the push changes no skill body — every changed line under skills/ is"
  echo "  either a machine-stamped version copy or only a change in letter case and/or whitespace,"
  echo "  so the skill-creator-review gate stands down by name (SPEC INV-208)."
  exit 0
fi

# Find a COMMITTED record that names $2, carries the marker, carries a verdict, AND is itself fresh
# enough — its own commit is at or after $1 (the commit whose change it must cover). Checking the
# whole review dir's newest commit here (an earlier shape of this gate) let an unrelated same-day
# record elsewhere under docs/skill-review/ wave through a match on a different, stale record for
# THIS skill: the loop below took the first name+marker+verdict hit in `git ls-files` order
# (oldest-dated file first, since filenames sort lexically), and the directory-wide freshness check
# then compared against a commit that record never carried. Two records for 'live-spec-base' —
# 2026-07-17 and a same-day-as-the-skill-change 2026-08-09 one — reproduced exactly this: the gate
# matched the 2026-07-17 record and called it fresh off the directory's unrelated last commit
# (finding 7, docs/prover/2026-08-09-the-culling-first-day.md). Each candidate's OWN commit is
# checked, and the loop keeps looking past a stale match instead of stopping on the first name hit.
# Echoes the matched record's path and returns 0 when found; returns 1 with no output otherwise.
find_covering_record() {
  local covers_commit="$1" name="$2" rec body rec_commit
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

    rec_commit="$(git log -1 --format=%H -- "$rec" 2>/dev/null || true)"
    if [ -n "$covers_commit" ] && [ -n "$rec_commit" ] && [ "$rec_commit" != "$covers_commit" ] && \
       ! git merge-base --is-ancestor "$covers_commit" "$rec_commit" 2>/dev/null; then
      continue   # this record predates the commit it would need to cover — keep looking
    fi
    printf '%s\n' "$rec"
    return 0
  done < <(git ls-files "$REVIEW_DIR" 2>/dev/null)
  return 1
}

fail=0
for name in $substantive_skills; do
  skill_commit="$(git log -1 --format=%H -- "skills/$name" 2>/dev/null || true)"

  matched="$(find_covering_record "$skill_commit" "$name" || true)"

  if [ -z "$matched" ]; then
    # THE BYTE-IDENTICAL CARVE-OUT (see the header comment). No direct record covers today's
    # change — before failing, ask whether every changed file's CONTENT was already reviewed once,
    # earlier in this repo's own history, at the same path.
    carveout_ok=1
    changed_under_skill="$(git diff --name-only "$DIFF_BASE" HEAD -- "skills/$name" || true)"
    if [ -z "$changed_under_skill" ]; then
      carveout_ok=0   # nothing to carve out over ($name only entered $substantive_skills with a
    fi                # real changed file, but stay honest rather than assume that here)
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      cur_blob="$(git rev-parse "HEAD:$f" 2>/dev/null || true)"
      if [ -z "$cur_blob" ]; then
        carveout_ok=0; break   # deleted at HEAD, or unreadable — no content to match
      fi
      file_covered=0
      while IFS= read -r old_commit; do
        [ -z "$old_commit" ] && continue
        [ "$old_commit" = "$skill_commit" ] && continue   # this change itself, not an earlier state
        old_blob="$(git rev-parse "${old_commit}:$f" 2>/dev/null || true)"
        [ -n "$old_blob" ] && [ "$old_blob" = "$cur_blob" ] || continue
        if find_covering_record "$old_commit" "$name" >/dev/null; then
          file_covered=1
          break
        fi
      done < <(git log --format=%H -- "$f" 2>/dev/null)
      if [ "$file_covered" -eq 0 ]; then
        carveout_ok=0; break
      fi
    done <<< "$changed_under_skill"

    if [ "$carveout_ok" -eq 1 ]; then
      echo "OK (skill review): skill '$name' changed, but every changed file's content is byte-"
      echo "  identical to an earlier commit whose content already carries a covering review record"
      echo "  — a vendor re-sync of already-reviewed content, not a new edit, owes no fresh record."
      continue
    fi

    echo "FAIL (skill review): the skill '$name' changed in a real way in this push, but nobody has"
    echo "  reviewed it since — the newest record under $REVIEW_DIR/ is older than the skill's own"
    echo "  last change, so it doesn't cover what's being pushed now (SPEC INV-208)."
    echo "  skill '$name' last changed in ${skill_commit:-unknown}."
    fail=1
    continue
  fi

  echo "OK (skill review): skill '$name' carries a fresh review record ($matched)."
done

if [ "$fail" -ne 0 ]; then
  echo "  Fix: ask your agent to run the skill-creator review over the changed skill and commit its"
  echo "  verdict as $REVIEW_DIR/$(date +%Y-%m-%d)-<skill>.md before pushing (a version-number-only"
  echo "  bump is exempt and needs no review)."
  exit 1
fi

exit 0
