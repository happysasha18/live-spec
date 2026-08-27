#!/bin/bash
# state-probe.sh — prints the project's MEASURED state, not something written down by hand.
#
# Why: resuming work between sessions used to rest on prose that had to be written correctly at
# the end of a session and read correctly at the start of the next. It broke on both ends. Here
# the state is computed by commands, so it cannot go stale.
#
# Run: bash scripts/state-probe.sh    (the first action of every session)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
REPO=$(pwd)

b() { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok() { printf '  \033[0;32m%s\033[0m\n' "$1"; }
warn() { printf '  \033[0;33m! %s\033[0m\n' "$1"; }
bad() { printf '  \033[0;31mX %s\033[0m\n' "$1"; }

printf '\033[1m[%s] live-spec\033[0m  %s\n' "$(date '+%H:%M, %d.%m.%Y')" "$REPO"

# ---------------------------------------------------------------- where we stand
b "WHERE WE STAND"
git fetch origin --quiet 2>/dev/null
HEAD_SHA=$(git log -1 --format=%h)
echo "  branch $(git branch --show-current) · $HEAD_SHA · $(git log -1 --format=%s | cut -c1-60)"
DIRTY=$(git status --porcelain | wc -l | tr -d ' ')
[ "$DIRTY" = "0" ] && ok "tree clean" || warn "uncommitted files: $DIRTY"
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
[ "$BEHIND" != "0" ] && warn "behind origin/main by $BEHIND commits"
[ "$AHEAD" != "0" ] && warn "commits not pushed: $AHEAD (push is blocked by gates — see §Blockers)"
[ "$BEHIND" = "0" ] && [ "$AHEAD" = "0" ] && ok "matches origin/main"

# ---------------------------------------------------------------- plan
# A task's status comes from its acceptance command, not from a hand-set mark, wherever a
# command exists (scripts/plan_checks.py). A task with no command prints as DECLARED — the
# reader can see where the fact ends and someone's word begins; that is existing, correct
# behaviour, not a gap to fill.
#
# PLAN.md's `## Tasks` section (commit bc6f862b) can hold well over a hundred tasks — this
# printout is what CLAUDE.md's Canon report carries into chat verbatim, and that report is
# capped at seven to ten lines (the owner's own repeated words; see ~/.claude/CLAUDE.md). So
# this prints the top of the list, not all of it: full detail always stays one command away,
# `bash scripts/render-board.sh`, or PLAN.md itself.
b "PLAN"
rm -f /tmp/probe-next.txt
if [ -f PLAN.md ]; then
  python3 - <<'PYEOF'
import subprocess, sys

G, Y, R, D, B, X = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[2m", "\033[1m", "\033[0m"

# The parser and the acceptance commands live in one home, scripts/plan_checks.py: a status
# board a person edits by hand must not also be an execution surface, and two copies of either
# would let this reader and scripts/render-board.sh disagree about what a task is.
# Both readers cd to the repository root before this block runs, so "scripts" resolves.
sys.path.insert(0, "scripts")
from plan_checks import parse_tasks

text = open("PLAN.md", encoding="utf-8").read()
tasks = parse_tasks(text)

for t in tasks:
    if t["check"]:
        ok = subprocess.run(t["check"], shell=True, capture_output=True).returncode == 0
        # A checked task's real state can outrun or lag the mark a person typed — the command
        # is the fact. Falling back to the task's own mark rather than a flat "⬜" on failure
        # (unlike the old x/~/!/space vocabulary) keeps a real distinction: q-... items have no
        # checks at all, but a checked task like plan-9 can be marked in hand (🔄) and still
        # fail its command, which is exactly what plan-9's own note in PLAN.md says is true
        # today.
        t["icon"] = "✅" if ok else t["mark"]
        t["verified"] = True
    else:
        ok = t["mark"] == "✅"
        t["icon"] = t["mark"]
        t["verified"] = False
    t["ok"] = ok

ICON_COLOUR = {"✅": G, "🔄": Y, "⛔": R, "👁️": Y, "⬜": D}

# Priority order for the budget below: needs-his-eyes (only he can move it), then in hand
# (already running work), then blocked (worth knowing about), then queued (what's next) —
# filled round-robin, one category at a time, so a single large category (31 blocked today)
# cannot eat the whole budget and crowd the others out.
TASK_LINE_BUDGET = 9  # 9 task lines + 1 summary line = 10, the Canon cap's own top end.
CATEGORY_ORDER = ["👁️", "🔄", "⛔", "⬜"]

buckets = {icon: [t for t in tasks if t["icon"] == icon] for icon in CATEGORY_ORDER}
for icon in CATEGORY_ORDER:
    # Critical priority first; ties keep the file's own order. PLAN.md's "## Tasks" preamble
    # already lists critical tasks first, so this is a safety net, not the source of the order
    # (a stable sort changes nothing when the input is already in that order).
    buckets[icon].sort(key=lambda t: 0 if (t["priority"] or "").strip().lower() == "critical" else 1)

shown = []
idx = {icon: 0 for icon in CATEGORY_ORDER}
budget = TASK_LINE_BUDGET

# Critical first, across every category. A task marked critical was judged to matter now — that
# judgment outranks which bucket it happens to sit in, so a critical queued task beats a normal
# blocked one. Within critical, the file's own order stands. Only once every critical is shown
# does the round-robin below fill what's left, so no single large category crowds the others out.
for icon in CATEGORY_ORDER:
    while budget > 0 and idx[icon] < len(buckets[icon]) and \
            (buckets[icon][idx[icon]]["priority"] or "").strip().lower() == "critical":
        shown.append(buckets[icon][idx[icon]])
        idx[icon] += 1
        budget -= 1

progressed = True
while budget > 0 and progressed:
    progressed = False
    for icon in CATEGORY_ORDER:
        if budget <= 0:
            break
        i = idx[icon]
        if i < len(buckets[icon]):
            shown.append(buckets[icon][i])
            idx[icon] += 1
            budget -= 1
            progressed = True

# NEXT: the first task actually in hand — a task waiting on his eyes can't be advanced without
# him either, so (like the old rule skipping blocked steps) it doesn't win NEXT.
next_task = buckets["🔄"][0] if buckets["🔄"] else (buckets["⬜"][0] if buckets["⬜"] else None)

next_title = ""
for t in shown:
    tag = ""
    if next_task is not None and t["id"] == next_task["id"]:
        tag = f"  {B}<-- NEXT{X}"
        next_title = t["title"]
    verified = f"{D}verified{X}" if t["verified"] else f"{D}declared{X}"
    colour = ICON_COLOUR.get(t["icon"], D)
    print(f"  {t['icon']} {colour}{t['title']}{X}  {D}({t['id']}){X} {verified}{tag}")

shown_ids = {t["id"] for t in shown}
done_count = sum(1 for t in tasks if t["icon"] == "✅")
more_below = sum(1 for t in tasks if t["id"] not in shown_ids and t["icon"] != "✅")
print(f"  {D}… {more_below} more below · {done_count} done · full list in PLAN.md / board.html{X}")

if next_title:
    open("/tmp/probe-next.txt", "w", encoding="utf-8").write(next_title)
PYEOF
else
  bad "PLAN.md is missing"
fi

# ---------------------------------------------------------------- facts
b "FACTS"
echo "  pack version: $(cat VERSION 2>/dev/null || echo '?')"

if [ -f evals/director/check.py ]; then
  SCORE=$(python3 evals/director/check.py --all 2>/dev/null | tail -1)
  case "$SCORE" in
    *"of"*)
      SD=$(git log -1 --format=%ct -- skills/director/SKILL.md 2>/dev/null || echo 0)
      ED=$(git log -1 --format=%ct -- evals/director/traces 2>/dev/null || echo 0)
      if [ "$SD" -gt "$ED" ] 2>/dev/null; then
        echo "  Director by scenario: $SCORE — REPLAY OF OLD TRACES, says nothing about today's skill"
      else
        echo "  Director by scenario: $SCORE"
      fi ;;
    *) warn "Director eval isn't responding" ;;
  esac
fi

# required context: what loads on every session start
CTX_BYTES=$(cat skills/live-spec-base/SKILL.md skills/director/SKILL.md 2>/dev/null | wc -c | tr -d ' ')
CTX_TOK=$(python3 - <<'EOF' 2>/dev/null
import sys
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    t = 0
    for p in ("skills/live-spec-base/SKILL.md", "skills/director/SKILL.md"):
        t += len(enc.encode(open(p, encoding="utf-8").read()))
    print(t)
except Exception:
    print("")
EOF
)
if [ -n "$CTX_TOK" ]; then
  echo "  required context: $CTX_TOK tokens (base + director, $CTX_BYTES bytes)"
else
  echo "  required context: $CTX_BYTES bytes (tiktoken unavailable)"
fi

CANON=$(cat PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md ROADMAP.md spec/* architecture/* matrix/* 2>/dev/null | wc -c | tr -d ' ')
echo "  full canon: $CANON bytes"
echo "  ROADMAP queue: $(grep -c '^| [0-9]' ROADMAP.md 2>/dev/null || echo '?') rows"

# ---------------------------------------------------------------- alarm
b "ALARM"
ALARM=0

# the skill changed after the last eval run — the score is stale
SKILL_D=$(git log -1 --format=%ct -- skills/director/SKILL.md 2>/dev/null || echo 0)
EVAL_D=$(git log -1 --format=%ct -- evals/director/traces 2>/dev/null || echo 0)
if [ "$SKILL_D" -gt "$EVAL_D" ] 2>/dev/null; then
  warn "director skill changed $(date -r "$SKILL_D" '+%d.%m') — eval last ran $(date -r "$EVAL_D" '+%d.%m'). The score is stale."
  ALARM=1
fi

# one fact, one home
[ -f evals/director.md ] && { warn "evals/director.md exists and conflicts with evals/director/ — two homes for one fact"; ALARM=1; }

# live state has gone stale
if [ -f NEXT_STEPS.md ]; then
  NS_D=$(git log -1 --format=%ct -- NEXT_STEPS.md 2>/dev/null || echo 0)
  LAST=$(git log -1 --format=%ct)
  [ "$NS_D" -lt "$LAST" ] && { warn "NEXT_STEPS.md is $(( (LAST - NS_D) / 86400 )) days older than the tree's last commit"; ALARM=1; }
fi

# work outside its home — /private/tmp is wiped on reboot.
# Catches both a working tree there and a leftover directory: the alarm used to miss the second case.
git worktree list 2>/dev/null | grep -q "/private/tmp" && { warn "working tree in /private/tmp — wiped on reboot"; ALARM=1; }
[ -d /private/tmp/ls-director ] && { warn "directory /private/tmp/ls-director still exists ($(ls /private/tmp/ls-director 2>/dev/null | wc -l | tr -d ' ') files) — wiped on reboot"; ALARM=1; }

# other worktrees carrying unmerged work
git worktree list 2>/dev/null | tail -n +2 | grep -v "/private/tmp" | while read -r wt _ br; do
  br=$(echo "$br" | tr -d '[]')
  [ -z "$br" ] && continue
  n=$(git rev-list --count "main..$br" 2>/dev/null || echo 0)
  [ "$n" != "0" ] && warn "tree $(basename "$wt") on branch $br: $n commit(s) not in main"
done
git worktree list 2>/dev/null | tail -n +2 | grep -qv "/private/tmp" && ALARM=1

# host drift
for h in ~/tlvphotos ~/exhibition-engine ~/promoter ~/promoter-alexander ~/tc-cloud-validate; do
  [ -d "$h/.claude/skills/live-spec-base" ] || continue
  HV=$(grep -m1 'version:' "$h/.claude/skills/live-spec-base/SKILL.md" 2>/dev/null | tr -d ' ' | cut -d: -f2)
  PV=$(cat VERSION 2>/dev/null)
  [ "$HV" != "$PV" ] && { warn "$(basename "$h"): pack $HV vs $PV in the pack"; ALARM=1; }
done

[ "$ALARM" = "0" ] && ok "no alarms"

# ---------------------------------------------------------------- blockers
b "BLOCKERS"
if [ -f PLAN.md ]; then
  awk '/^## Blockers/{f=1;next} /^## /{f=0} f && /^- /' PLAN.md | head -20 | sed 's/^/  /'
fi

# ---------------------------------------------------------------- next move
# Taken from the same run that printed the list above. It used to be read from the checkbox
# in PLAN.md, and the two sources disagreed on the same screen.
NEXT_TITLE=$(cat /tmp/probe-next.txt 2>/dev/null)
[ -n "$NEXT_TITLE" ] && printf '\n\033[1mNEXT\033[0m\n  %s\n  (details — in PLAN.md)\n' "$NEXT_TITLE"

printf '\n'
