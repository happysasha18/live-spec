#!/usr/bin/env bash
# check-deletion-only-push.sh — is every ref line this push carries a pure deletion?
# (SPEC INV-290, ROADMAP row 502)
#
# git feeds a pre-push hook one line per ref update on stdin, of the form:
#   <local ref> SP <local sha> SP <remote ref> SP <remote sha>
# (githooks(5)). Verified against a real `git push --delete` run (2026-07-27, scratch repo): a ref
# DELETION reports the all-zero object id as its LOCAL sha; the local ref field reads the literal
# string "(delete)", which this script does not rely on — the sha alone is the reliable signal. A
# push that only deletes references carries no content: nothing changed in the tree for any
# downstream gate to read.
#
# Exit 0 = deletion-only: at least one line was read and EVERY line's local sha is all-zero.
# Exit 1 = not deletion-only: a mixed push (some lines carry real content), an all-content push, or
#          no lines read at all. Zero lines is CONSERVATIVE, never read as "safe to skip" — a real
#          push always feeds at least one line, so an empty read means this script was not handed
#          the hook's real input.
#
# Usage: check-deletion-only-push.sh          # reads ref lines from stdin
#   PUSH_REF_LINES (tests only, and the caller's own drained-stdin relay): newline-separated
#   ref-update lines, replaces stdin. Set (even to "") to skip the stdin read entirely.

set -euo pipefail

ZERO_SHA="0000000000000000000000000000000000000000"

if [ -n "${PUSH_REF_LINES+x}" ]; then
  lines="$PUSH_REF_LINES"
else
  lines="$(cat)"
fi

seen=0
all_deleted=1
while IFS= read -r line; do
  [ -z "$line" ] && continue
  seen=$((seen + 1))
  local_sha="$(printf '%s\n' "$line" | awk '{print $2}')"
  if [ "$local_sha" != "$ZERO_SHA" ]; then
    echo "deletion-check: ref line carries a real object id — not deletion-only: $line"
    all_deleted=0
  fi
done <<< "$lines"

if [ "$seen" -eq 0 ]; then
  echo "deletion-check: no ref-update lines read — not deletion-only (conservative)."
  exit 1
fi

if [ "$all_deleted" -eq 1 ]; then
  echo "deletion-check: all $seen ref line(s) carry the all-zero local object id — deletion-only."
  exit 0
fi

exit 1
