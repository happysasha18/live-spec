#!/usr/bin/env bash
# fence-refresh.sh — (re-)arms the concurrent-edit fence (SPEC INV-11) at the current
# HEAD. Run this to opt in to the fence, or after reviewing what another writer
# changed so the fence tracks the repo again.
#
# Also records this session's token on line 2 of .live-spec-fence (ROADMAP row 572)
# — from $LIVE_SPEC_SESSION_ID if set, else $CLAUDE_CODE_SESSION_ID, else empty. The
# post-commit hook uses this token to re-arm the fence on THIS session's own
# successful commits (so a second commit in the same session never needs a manual
# refresh) while leaving the fence stale after a commit from a session carrying a
# different token (or no token), so the next commit — by anyone — still blocks.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
sha="$(git -C "$REPO_ROOT" rev-parse HEAD)"
session_token="${LIVE_SPEC_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}"
{
  echo "$sha"
  echo "$session_token"
} > "$REPO_ROOT/.live-spec-fence"
echo "Fence armed: recorded HEAD $sha into $REPO_ROOT/.live-spec-fence"
