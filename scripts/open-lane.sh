#!/usr/bin/env bash
# open-lane.sh — the lane-open act (SPEC INV-214, T-23, E-34).
#
# Opening a parallel build lane is a step the session PERFORMS, not narration it
# emits. This script is that step's performable form. It runs the concrete git
# ceremony the branch road specifies: the row→in-work claim commit on main under
# the pen, the lane branch cut from that commit into its own worktree, and the
# worker brief stub that names the branch the lane rides.
#
# Usage:
#   1. Edit the queue (ROADMAP.md): flip the row's status cell to in-work, and
#      STAGE only that file  (git add ROADMAP.md).
#   2. scripts/open-lane.sh <row-number> <slug>
#   3. Delegate the lane to a worker with the Agent tool's isolation: "worktree"
#      option (it carries no gate), the brief naming the printed branch.
#
# Preconditions it enforces — each a red that stops the act:
#   - run from the PRIMARY worktree on main, so the claim commit lands where INV-2's
#     ancestry order can read it (a claim on a lane's own branch sits outside it);
#   - the row→in-work flip staged, and ONLY the queue file staged, so the claim
#     commit carries one row's delta (INV-39);
#   - the profile cap not exceeded: open lanes + 1 <= lanes.cap (default 3, INV-214/T-18);
#   - the fence unbroken where it is armed (INV-11);
#   - the lane branch not already present.
#
# Env overrides (for tests and non-default hosts):
#   LIVE_SPEC_QUEUE       the queue file the claim commit carries      (default ROADMAP.md)
#   LIVE_SPEC_PROFILE     the profile the cap is read from             (default ~/.claude/live-spec/profile.md)
#   LIVE_SPEC_WORKTREES   the base dir the lane worktree is created in (default .claude/worktrees)
set -euo pipefail

die() { echo "open-lane: $*" >&2; exit 1; }

[ $# -eq 2 ] || die "usage: open-lane.sh <row-number> <slug>"
ROW="$1"; SLUG="$2"
[[ "$ROW" =~ ^[0-9]+$ ]] || die "row must be a number, got '$ROW'"
[[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "slug must be kebab-case [a-z0-9-], got '$SLUG'"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
cd "$ROOT"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[ "$BRANCH" = "main" ] || die "run from the primary tree on main; HEAD is '$BRANCH' (the claim commits to main so INV-2 can order it)"

LANE="lane/${ROW}-${SLUG}"
if git rev-parse --verify --quiet "refs/heads/$LANE" >/dev/null; then
  die "branch $LANE already exists"
fi

# --- cap: open lanes + this one must fit the profile-declared cap (INV-214) ---
PROFILE="${LIVE_SPEC_PROFILE:-$HOME/.claude/live-spec/profile.md}"
CAP=3
if [ -f "$PROFILE" ]; then
  v="$(grep -oE 'lanes\.cap:[[:space:]]*[0-9]+' "$PROFILE" | head -1 | grep -oE '[0-9]+' || true)"
  [ -n "$v" ] && CAP="$v"
fi
OPEN="$(git branch --list 'lane/*' | grep -c . || true)"
if [ "$((OPEN + 1))" -gt "$CAP" ]; then
  die "cap reached: $OPEN lane(s) already open, cap is $CAP (lanes.cap) — a further lane needs the human's word (INV-214, T-18)"
fi

# --- the staged claim: exactly the queue file, and something staged (INV-39) ---
QUEUE_FILE="${LIVE_SPEC_QUEUE:-ROADMAP.md}"
STAGED="$(git diff --cached --name-only)"
[ -n "$STAGED" ] || die "stage the row→in-work flip in $QUEUE_FILE first, then run open-lane"
if [ "$STAGED" != "$QUEUE_FILE" ]; then
  die "the claim commit carries one row's delta (INV-39): stage only $QUEUE_FILE, got: $(echo "$STAGED" | tr '\n' ' ')"
fi

# --- the fence, where it is armed (INV-11) ---
if [ -f "$ROOT/.live-spec-fence" ]; then
  armed="$(cat "$ROOT/.live-spec-fence")"
  head="$(git rev-parse HEAD)"
  [ "$armed" = "$head" ] || die "fence tripped: HEAD $head moved since the fence was armed at $armed — review and run guardrails/fence-refresh.sh (INV-11)"
fi

# --- the claim commit on main under the pen ---
git commit -q -m "claim: row ${ROW} → in-work (${LANE})"
CLAIM="$(git rev-parse HEAD)"

# --- cut the lane branch into its own worktree from the claim commit (E-34) ---
WT_BASE="${LIVE_SPEC_WORKTREES:-.claude/worktrees}"
WT="${WT_BASE}/lane-${ROW}-${SLUG}"
git worktree add -q -b "$LANE" "$WT" "$CLAIM"

cat <<EOF
Lane opened: $LANE
  claim commit : $CLAIM (on main)
  worktree     : $WT
  open lanes   : $((OPEN + 1)) of $CAP

Worker brief stub — the lane rides its own branch:
  branch   : $LANE
  worktree : $WT
  row      : $ROW
Copy this clause into the brief verbatim (ROADMAP row 479):
EOF

cat <<'CLAUSE'
  A worker never restores a working tree with a git command. Before a worker mutates a file
  it means to put back, it reads that file and holds its bytes. A worker puts a file back by
  WRITING ITS OWN SAVED BYTES. A worker runs no command that discards uncommitted work, in
  any tree: `git checkout -- <path>`, `git checkout .`, `git restore` outside `--staged`,
  `git stash` and its `push`, `save`, `create` and `store` forms, `git reset` with `--hard`,
  `--merge` or `--keep`, and `git clean` with `-f` or `-x`. Such a command's blast radius is
  a PATH, so its damage lands on files the worker never wrote and its brief never named.
  This rule binds a worker in every tree, including its own isolated worktree, since a
  worktree shares one repository with the lanes beside it and a worker cannot read off its
  brief what else that repository holds. A worker that holds no saved bytes for a file it
  mutated, or that believes a file needs a git-level restore, HALTS and reports the file and
  the mutation it made, and it writes no further file and runs no further command. The
  orchestrator owns recovery: it restores the named file from the last committed stage, hands
  the worker a fresh brief carrying that file's current bytes, and records the halt in the
  row's delivery report, and the halted work resumes under that new brief.
The orchestrator's own half: a finished build stage is committed before the next worker
touches its files. `guardrails/check-worker-restore.py` reads the worker runs' transcripts
for the command and runs at the verify step.
CLAUSE

cat <<EOF

Delegate with the Agent tool's isolation: "worktree" option (no gate), or point a
worker at $WT. The brief must name the branch $LANE. The lane's delta reaches main
only through integration under the pen: rebase onto main's tip, gate on the rebased
tree, fast-forward (T-23, INV-199).
EOF
