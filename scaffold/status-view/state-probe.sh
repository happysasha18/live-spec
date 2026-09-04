#!/bin/bash
# state-probe.sh — prints this project's MEASURED state, not something written down by hand.
#
# Why: resuming work between sessions used to rest on prose that had to be written correctly at
# the end of a session and read correctly at the start of the next. It broke on both ends. Here
# the state is computed by commands, so it cannot go stale.
#
# What it reads, and nothing else: git, PLAN.md, the acceptance commands in scripts/plan_checks.py,
# and inbox/. It carries no knowledge of any other project.
#
# Run: bash scripts/state-probe.sh    (the first action of every session)
#
# Installed by live-spec's adopt/install-status-view.sh. Its source is the pack's own
# scaffold/status-view/state-probe.sh, pinned in scripts/ratchet-manifest.json — local edits are
# reported as drift by the update check, so grow this file by growing the pack's copy.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
REPO=$(pwd)

b() { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok() { printf '  \033[0;32m%s\033[0m\n' "$1"; }
warn() { printf '  \033[0;33m! %s\033[0m\n' "$1"; }
bad() { printf '  \033[0;31mX %s\033[0m\n' "$1"; }

printf '\033[1m[%s] %s\033[0m  %s\n' "$(date '+%H:%M, %d.%m.%Y')" "$(basename "$REPO")" "$REPO"

# ---------------------------------------------------------------- where we stand
b "WHERE WE STAND"
git fetch --quiet 2>/dev/null
echo "  branch $(git branch --show-current) · $(git log -1 --format=%h) · $(git log -1 --format=%s | cut -c1-60)"
DIRTY=$(git status --porcelain | wc -l | tr -d ' ')
[ "$DIRTY" = "0" ] && ok "tree clean" || warn "uncommitted files: $DIRTY"
# Against the branch's OWN upstream, whatever it is — a project need not call its trunk `main`, and
# a lane branch reads against its own remote rather than against somebody else's trunk.
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)
if [ -n "$UPSTREAM" ]; then
  BEHIND=$(git rev-list --count "HEAD..$UPSTREAM" 2>/dev/null || echo 0)
  AHEAD=$(git rev-list --count "$UPSTREAM..HEAD" 2>/dev/null || echo 0)
  [ "$BEHIND" != "0" ] && warn "behind $UPSTREAM by $BEHIND commits"
  [ "$AHEAD" != "0" ] && warn "commits not pushed: $AHEAD"
  [ "$BEHIND" = "0" ] && [ "$AHEAD" = "0" ] && ok "matches $UPSTREAM"
else
  warn "this branch tracks no remote branch"
fi

# ---------------------------------------------------------------- plan
# A row's status comes from its acceptance command, not from a hand-set mark, wherever a command
# exists (scripts/plan_checks.py). A row with no command prints as DECLARED — the reader can see
# where the fact ends and someone's word begins.
b "PLAN"
if [ -f PLAN.md ]; then
  python3 - <<'PYEOF'
import sys

G, Y, R, D, B, X = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[2m", "\033[1m", "\033[0m"

# The parser, the marks and the state computation live in one home, scripts/plan_checks_core.py,
# reached through scripts/plan_checks.py so this project's own commands ride along. The board
# (scripts/render-board.sh) reads the same home, so the two cannot disagree about a row.
sys.path.insert(0, "scripts")
from plan_checks import evaluate, parse_tasks

tasks = evaluate(parse_tasks(open("PLAN.md", encoding="utf-8").read()))
if not tasks:
    print("  %sPLAN.md holds no rows this reader can see — it needs either a `## Tasks` section of"
          "\n  `### <mark> <title> — id: <id>` rows, or the `## The body` table the pack's own"
          "\n  PLAN.template.md lands.%s" % (D, X))
    sys.exit(0)

ICON_COLOUR = {"✅": G, "🔄": Y, "🔁": Y, "⛔": R, "⬜": D}

# Every row still open, plus every row whose done mark its own command contradicts. Finished work
# stays off: the plan itself holds it, and a list of everything ever done answers nothing.
open_rows = [t for t in tasks if t["icon"] != "✅"]
next_task = next((t for t in open_rows if t["icon"] == "🔄"),
                 next((t for t in open_rows if t["icon"] == "⬜"), None))
id_width = max((len(t["id"]) for t in tasks), default=0)

for t in open_rows:
    if t["failing_key"]:
        state = "%smarked done%s" % (D, X)
    else:
        state = "%s%s%s" % (D, "verified" if t["verified"] else "declared", X)
    reason = ""
    if t["blocked_by"]:
        r = t["blocked_by"].strip()
        reason = " %s— %s%s" % (D, r[:39].rstrip() + "…" if len(r) > 40 else r, X)
    if t["note"]:
        reason += " %s— %s%s" % (D, t["note"], X)
    tag = "  %s<-- NEXT%s" % (B, X) if next_task is not None and t["id"] == next_task["id"] else ""
    print("  %s%s%s %s %s%s%s  %s%s%s"
          % (D, t["id"].ljust(id_width), X, t["icon"],
             ICON_COLOUR.get(t["icon"], D), t["title"], X, state, reason, tag))

print("  %s… %d open of %d rows · full list in PLAN.md / board.html%s"
      % (D, len(open_rows), len(tasks), X))
PYEOF
else
  bad "PLAN.md is missing"
fi

# ---------------------------------------------------------------- inbox
# What came in through the door and nobody has taken yet. The sweep REMOVES a file when it harvests
# it, so a file still standing here is an unhandled item — no second ledger to keep in step.
# A name ending `.draft` is a deposit mid-write and is passed over, exactly as the sweep passes over
# it; README.md is the folder's own instructions rather than an item.
if [ -d inbox ]; then
  b "INBOX"
  INBOX_N=0
  for f in inbox/*; do
    base=$(basename "$f")
    case "$base" in *.draft|README.md|'*') continue ;; esac
    [ -f "$f" ] || continue
    warn "$base"
    INBOX_N=$((INBOX_N + 1))
  done
  [ "$INBOX_N" = "0" ] && ok "nothing unhandled"
fi

# ---------------------------------------------------------------- blockers
if [ -f PLAN.md ] && grep -q '^## Blockers' PLAN.md; then
  b "BLOCKERS"
  awk '/^## Blockers/{f=1;next} /^## /{f=0} f && /^- /' PLAN.md | head -20 | sed 's/^/  /'
fi

printf '\n'
