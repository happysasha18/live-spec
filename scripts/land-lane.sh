#!/usr/bin/env bash
# land-lane.sh — the lane-landing act (SPEC INV-199, T-23; PLAN q-804).
#
# scripts/open-lane.sh performs the lane-OPEN act rather than narrating it. This is its counterpart
# at the other end of the lane's life, and it exists for the same reason: the walk Requirement 86
# names — the lane takes the pen, rebases its branch onto main's tip, the landing gate runs on the
# rebased tree, main advances by fast-forward, and the branch and worktree come down — was written
# down in three places and performed by none, so the check that stands ahead of that gate
# (guardrails/check-merge-base.sh) had no caller anywhere in the tree. Here is that caller.
#
# The rebase itself is deliberately NOT done here: a textual conflict is the lane's own work,
# resolved in the lane's own worktree (Requirement 87 criterion 1). So this act opens with the
# predicate Requirement 86 criterion 2 names — the branch's merge-base with main equals main's tip
# — which reds a lane that has not rebased, so the landing gate never reads a stale tree.
#
# Usage:
#   1. In the lane's own worktree: `git rebase main`, resolving any conflict there.
#   2. From the PRIMARY worktree on main: scripts/land-lane.sh <row-id> <slug>
#      e.g. land-lane.sh q-804 wire-lane-net-arms   (the pair open-lane.sh was given)
#
# The four steps it performs, each a red that stops the act:
#   - run from the PRIMARY worktree on main, because moving main is the pen's sole right (INV-198);
#   - the merge-base check ahead of the gate (INV-199, Requirement 86 criterion 2);
#   - the landing gate on the rebased tree — the tree's own guardrails/pre-push chain, where the
#     tree carries one; a tree with no chain says so by name rather than passing silently;
#   - the fast-forward, with no merge commit, so main stays linear (INV-39, INV-2).
#
# Teardown (Requirement 86 criterion 3) closes the act and uses git's NON-forcing forms only:
# `git worktree remove` refuses a worktree holding uncommitted work and `git branch -d` refuses an
# unmerged branch, and each refusal is reported as a finding rather than forced past — no landing
# discards work a lane has not committed.
set -euo pipefail

die() { echo "land-lane: $*" >&2; exit 1; }

# The checks this act runs are the PACK's, resolved beside this script — never against the tree
# being landed, which is the host and carries only what adoption vendored into it.
PACK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MERGE_BASE_CHECK="$PACK_ROOT/guardrails/check-merge-base.sh"
[ -x "$MERGE_BASE_CHECK" ] || die "the merge-base check is missing from the pack at $MERGE_BASE_CHECK — this act will not land a lane it could not check (SPEC INV-199)"

[ $# -eq 2 ] || die "usage: land-lane.sh <row-id> <slug>"
ROW="$1"; SLUG="$2"
[[ "$ROW" =~ ^[a-z][a-z0-9]*-[0-9]+$ ]] || die "row must be a task id from PLAN.md such as plan-11 or q-166, got '$ROW'"
[[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "slug must be kebab-case [a-z0-9-], got '$SLUG'"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
cd "$ROOT"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[ "$BRANCH" = "main" ] || die "run from the primary tree on main; HEAD is '$BRANCH' (holding the pen is the sole right to move main, INV-198)"

LANE="lane/${ROW}-${SLUG}"
git rev-parse --verify --quiet "refs/heads/$LANE" >/dev/null || die "no such lane branch: $LANE"

# The lane's worktree, read off git's shared worktree metadata rather than guessed from the base
# directory — a lane whose worktree was opened elsewhere still lands.
WT="$(git worktree list --porcelain | awk -v b="refs/heads/$LANE" '
  $1 == "worktree" { p = $2 }
  $1 == "branch" && $2 == b { print p; exit }')"

# --- the check ahead of the gate (INV-199, Requirement 86 criterion 2) ---
echo "-- the merge-base check, ahead of the landing gate (SPEC INV-199) --"
"$MERGE_BASE_CHECK" "${WT:-$LANE}" \
  || die "$LANE has not rebased onto main's tip — rebase it in its own worktree, then land again"

# --- the landing gate on the rebased tree ---
GATE_TREE="${WT:-$ROOT}"
echo ""
echo "-- the landing gate, on the rebased tree ($GATE_TREE) --"
if [ -x "$GATE_TREE/guardrails/pre-push" ]; then
  # </dev/null: the chain reads its ref-update lines from stdin, and a hand invocation must never
  # block on a read (guardrails/pre-push's own deletion-only stand-down).
  ( cd "$GATE_TREE" && ./guardrails/pre-push </dev/null ) \
    || die "the landing gate reds on the rebased tree — fix it in the lane and land again"
else
  echo "   this tree carries no gate chain at guardrails/pre-push — the landing gate stands down by name"
fi

# --- the fast-forward: main advances onto the lane, no merge commit (INV-39, INV-2) ---
echo ""
git merge --ff-only --quiet "$LANE" || die "main could not fast-forward onto $LANE"
echo "main advanced to $(git rev-parse HEAD) by fast-forward"

# --- teardown (Requirement 86 criterion 3), non-forcing: a refusal is a finding ---
if [ -n "$WT" ]; then
  if git worktree remove "$WT"; then
    echo "worktree removed: $WT"
  else
    echo "finding: $WT was not removed — git refused it, which on a landing means the worktree holds"
    echo "  uncommitted work. Read the refusal, then remove the worktree by hand (INV-199, INV-150)."
  fi
fi
if git branch -d "$LANE"; then
  echo "branch removed: $LANE"
else
  echo "finding: $LANE was not removed — git refused it. Read the refusal before removing it by hand."
fi

echo ""
echo "Lane landed: $LANE → main. Flip the row's mark on the list and close it out."
