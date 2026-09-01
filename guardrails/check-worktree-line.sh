#!/usr/bin/env bash
# check-worktree-line.sh — the adoption gate for a host's vendored worktree line (SPEC INV-201;
# PLAN q-804).
#
# The isolation law fires on a machine-readable condition — two lanes' write-sets overlap — while
# the worktree tool fires only on a human's word or a project instruction (spec/parallel-lanes.md
# Requirement 88's Context). Adoption vendors one line into the host's own project instructions
# that cites the isolation law's write-set condition (INV-105) rather than restating it, so the two
# agree with no second home for the condition. Requirement 88 criterion 4 names the gate this
# script performs: red a host whose project instructions carry no worktree line.
#
# What counts as "carrying the line": a line in the host's project instructions (CLAUDE.md at the
# host tree's root — the file every project-instructions convention in this pack reads) that names
# both a worktree and its citation, INV-105 — the isolation law's write-set condition (Requirement
# 88 criterion 1's own citation target). This is a minimal, mechanical reading, not a style check:
# it does not police the line's exact wording, since criteria 1-3 (what the line says, where it is
# scoped, when it is written) are their own still-open promise, not this gate's.
#
# This gate is the adoption/catch-up walk's own step (attach's job, per the seam
# "isolation default -> the host's instructions"), not a standing arm of guardrails/pre-push: this
# pack's own tree is itself an adopted host and carries no such line yet, since Requirement 88
# criterion 3 leaves that write "shut until the pack's own owner gives the word for the pack's
# line" — wiring this gate into every push would red this repo's own push chain ahead of that word,
# which is not this row's call to make. A host's setup/catch-up walk invokes it directly.
#
# Usage: check-worktree-line.sh [<host-tree-path>]     (default: this repo's own toplevel)
set -euo pipefail

die() { echo "check-worktree-line: $*" >&2; exit 1; }

HOST="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$HOST" ] || die "no host tree given and not inside a git repo"
[ -d "$HOST" ] || die "host tree not found: $HOST"

INSTRUCTIONS="$HOST/CLAUDE.md"

if [ ! -f "$INSTRUCTIONS" ]; then
  echo "{\"severity\":\"error\",\"code\":\"worktree-line\",\"message\":\"$HOST carries no CLAUDE.md at all, so no vendored worktree line either\",\"fix\":\"vendor the worktree isolation line into $INSTRUCTIONS (SPEC INV-201)\"}"
  exit 1
fi

if grep -q "worktree" "$INSTRUCTIONS" && grep -q "INV-105" "$INSTRUCTIONS"; then
  echo "worktree-line: OK ($INSTRUCTIONS carries a vendored worktree line citing INV-105)"
  exit 0
fi

echo "{\"severity\":\"error\",\"code\":\"worktree-line\",\"message\":\"$INSTRUCTIONS carries no vendored worktree line citing the isolation law's write-set condition (INV-105)\",\"fix\":\"vendor one line into $INSTRUCTIONS that cites INV-105 rather than restating it (SPEC INV-201)\"}"
exit 1
