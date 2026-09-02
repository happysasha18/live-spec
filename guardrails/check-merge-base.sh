#!/usr/bin/env bash
# check-merge-base.sh — the merge-base check ahead of the landing gate (SPEC INV-199; PLAN q-804).
#
# At integration a lane takes the pen, rebases its branch onto main's tip, then runs the landing
# gate on the rebased tree (spec/parallel-lanes.md Requirement 86 criterion 1). Criterion 2 names
# the check that stands ahead of that gate: the branch's merge-base with main must equal main's own
# tip, so a lane that has not rebased reds BEFORE the gate runs rather than the gate reading a stale
# tree. This script is that check, performable rather than only narrated.
#
# It runs ahead of the landing gate, not inside the general push chain: a lane's own branch is
# penless traffic that never pushes (the base-rulebook worker contract), and outside a landing this
# predicate answers a question nobody is asking, so nothing wires it into guardrails/pre-push.
#
# Its caller is scripts/land-lane.sh, the landing act — it runs this check first, and refuses to
# reach the gate or move main when it reds. That caller is the whole point: this script passed its
# own fixture tests for a night while a full-tree grep found nothing invoking it, which is a check
# that exists rather than a promise that is kept (docs/prover/2026-09-02-overnight-run-hostile-review.md,
# finding 2). It stays runnable by hand on whichever tree is about to integrate.
#
# Usage:
#   check-merge-base.sh                 # HEAD of the current worktree, against local 'main'
#   check-merge-base.sh <branch-or-sha>  # that ref, against local 'main'
#   check-merge-base.sh <worktree-path>  # that worktree's HEAD, against local 'main'
#
# Exit 0 and a plain OK line when the branch's merge-base with main equals main's own tip (the lane
# is rebased). Exit 1 and one JSON error line, matching this pack's guardrail convention, when it
# does not — the exact condition Requirement 86 criterion 2 names.
set -euo pipefail

die() { echo "check-merge-base: $*" >&2; exit 1; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
cd "$ROOT"

TARGET="${1:-HEAD}"

if [ "$TARGET" != "HEAD" ] && [ -d "$TARGET" ]; then
  TARGET_SHA="$(git -C "$TARGET" rev-parse HEAD 2>/dev/null)" || die "cannot resolve worktree '$TARGET'"
  TARGET_LABEL="$TARGET"
else
  TARGET_SHA="$(git rev-parse "$TARGET" 2>/dev/null)" || die "cannot resolve '$TARGET' to a commit"
  TARGET_LABEL="$TARGET"
fi

MAIN_SHA="$(git rev-parse main 2>/dev/null)" || die "no local 'main' branch to check against"
BASE_SHA="$(git merge-base "$MAIN_SHA" "$TARGET_SHA" 2>/dev/null)" || die "git merge-base found no common ancestor between '$TARGET_LABEL' ($TARGET_SHA) and main ($MAIN_SHA)"

if [ "$BASE_SHA" != "$MAIN_SHA" ]; then
  echo "{\"severity\":\"error\",\"code\":\"merge-base\",\"message\":\"'$TARGET_LABEL' has not rebased onto main's tip — merge-base $BASE_SHA does not equal main $MAIN_SHA — the landing gate must not run on a stale tree\",\"fix\":\"rebase the lane branch onto main, then re-run this check before the landing gate (SPEC INV-199, Requirement 86 criterion 2)\"}"
  exit 1
fi

echo "merge-base: OK ('$TARGET_LABEL' is rebased onto main's tip $MAIN_SHA)"
