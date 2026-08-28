#!/usr/bin/env bash
# guardrails/install.sh — installs this folder's git hooks into a repo's .git/hooks/,
# together with the check scripts those hooks call. Idempotent: re-running just
# overwrites with whatever is currently in guardrails/, no duplication and no error
# if already installed.
#
# The checks travel with the hooks (q-567). Until 2026-08-28 this script copied three
# hook files and none of the scripts they invoke, so a repo that installed them got
# pre-commit's two content gates as no-ops — both are guarded by a file test, and an
# absent script skipped in silence, leaving the repo believing it was checked. The
# gates now ship beside the hook and the hook stops rather than skipping.
#
# SOURCE is the guardrails folder this script lives in. DESTINATION is the repo the
# caller is standing in: run from the pack's own root — the documented
# `./guardrails/install.sh` — the two are one tree and nothing is copied sideways.
#
# What travels, and what does not:
#   pre-commit  — the concurrent-edit fence plus two host-agnostic content gates
#                 (a future-stamped line, an unjustified parked item). Both read the
#                 staged diff and the pack's ordinary documents, so they hold in any
#                 repo. Installed everywhere, with its two checks and with
#                 fence-refresh.sh, the script its own refusal tells a person to run.
#   post-commit — pure git, no checks of its own. Installed everywhere.
#   pre-push    — the live-spec push gate. Every one of its gates reads a document of
#                 this repository's own (PRODUCT_SPEC.md, ARCHITECTURE.md,
#                 TEST_MATRIX.md, docs/prover, skills/, scaffold/), so it cannot be
#                 shipped to a host as it stands. guardrails/README.md, "How a host
#                 project adapts the pattern", is where a host takes the gate shape by
#                 hand. Installed only inside the repository that holds it.
#
# post-commit (ROADMAP row 572) carries no gate of its own — it only re-arms the
# concurrent-edit fence on the session's own successful commit, when the fence is
# already armed. Installing it does NOT arm the fence itself — that stays opt-in
# (see guardrails/fence-refresh.sh and guardrails/README.md).

set -euo pipefail

GUARDRAILS_DIR="$(cd "$(dirname "$0")" && pwd)"

# The repo the caller stands in, falling back to the one this script belongs to when the
# caller is nowhere in particular.
if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  REPO_ROOT="$(git -C "$GUARDRAILS_DIR" rev-parse --show-toplevel)"
fi

# Worktree-aware: a linked worktree's hooks live in the MAIN checkout's common git dir, not in a
# per-worktree .git/hooks (a worktree's .git is a file, not a directory, pointing at the common
# one) — `git rev-parse --git-path hooks` resolves the real, shared hooks directory either way,
# the same resolver guardrails/check-config-health.sh already uses for the same reason.
HOOKS_DIR="$(git -C "$REPO_ROOT" rev-parse --git-path hooks)"
case "$HOOKS_DIR" in
  /*) : ;;
  *) HOOKS_DIR="$REPO_ROOT/$HOOKS_DIR" ;;
esac

if [ ! -d "$HOOKS_DIR" ]; then
  echo "No .git/hooks directory found at $HOOKS_DIR — is $REPO_ROOT a git repo?"
  exit 1
fi

DEST_GUARDRAILS="$REPO_ROOT/guardrails"
# `-ef` compares device and inode, so a symlinked path (on macOS git reports /private/var where
# the caller said /var) still reads as the one directory it is.
if [ -d "$DEST_GUARDRAILS" ] && [ "$DEST_GUARDRAILS" -ef "$GUARDRAILS_DIR" ]; then
  SAME_TREE=1
else
  SAME_TREE=0
fi

# What the two portable hooks need beside them. The first two are the scripts pre-commit
# invokes. The third is the one both this script's closing line and pre-commit's own refusal
# tell a person to run, and a named script that is not there is the same defect one step
# further on. All three are host-agnostic: they read the staged diff, the ordinary documents,
# and git.
PORTABLE_SUPPORT="check-future-times.sh check-deferral-marker.py fence-refresh.sh"

for check in $PORTABLE_SUPPORT; do
  if [ ! -f "$GUARDRAILS_DIR/$check" ]; then
    echo "Stopping without installing anything: $GUARDRAILS_DIR/$check is missing, and the hooks"
    echo "would be installed naming a script nobody has. Restore the file, then run this again."
    exit 1
  fi
done

HOOKS="pre-commit post-commit pre-push"
if [ "$SAME_TREE" -eq 0 ]; then
  HOOKS="pre-commit post-commit"
fi

if [ "$SAME_TREE" -eq 0 ]; then
  mkdir -p "$DEST_GUARDRAILS"
  for check in $PORTABLE_SUPPORT; do
    cp "$GUARDRAILS_DIR/$check" "$DEST_GUARDRAILS/$check"
    chmod +x "$DEST_GUARDRAILS/$check"
    echo "Installed guardrails/$check -> $DEST_GUARDRAILS/$check"
  done
fi

for hook in $HOOKS; do
  cp "$GUARDRAILS_DIR/$hook" "$HOOKS_DIR/$hook"
  chmod +x "$HOOKS_DIR/$hook"
  echo "Installed $hook -> $HOOKS_DIR/$hook"
done

if [ "$SAME_TREE" -eq 0 ]; then
  echo "Left the push gate alone: it reads this repository's own spec, architecture, matrix and"
  echo "prover records, so a copy of it here would block every push over documents $REPO_ROOT"
  echo "does not have. Take its shape by hand — guardrails/README.md, \"How a host project adapts"
  echo "the pattern\"."
fi

echo "Done. The fence (pre-commit) stays OFF until a session runs guardrails/fence-refresh.sh."
