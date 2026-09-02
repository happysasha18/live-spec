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
# printout is what the Canon report carries into chat verbatim, and that report's length, its
# marks and its shape have one home: ~/.claude/playbook/CLAUDE.md, "How a reply to him looks".
# Nothing here restates that law; TASK_LINE_BUDGET below is this script's reading of it. So
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
from plan_checks import key_failure_note, parse_tasks

text = open("PLAN.md", encoding="utf-8").read()
tasks = parse_tasks(text)

for t in tasks:
    if t["check"]:
        r = subprocess.run(t["check"], shell=True, capture_output=True)
        ok = r.returncode == 0
        # A checked task's real state can outrun or lag the mark a person typed — the command
        # is the fact. Falling back to the task's own mark rather than a flat "⬜" on failure
        # (unlike the old x/~/!/space vocabulary) keeps a real distinction: q-... items have no
        # checks at all, but a checked task like plan-9 can be marked in hand (🔄) and still
        # fail its command, which is exactly what plan-9's own note in PLAN.md says is true
        # today.
        #
        # A done mark is the one exception, and it is why the keys were written at all: a ✅
        # whose command fails printed itself back as ✅ and was counted among the done, so the
        # key could never contradict the mark it was there to test (found by the adversarial
        # review of 28.08). Such a row drops out of the done count. It wore ⛔ until 02.09, when
        # he named the confusion: a task that turns out not to be done is back in work, and
        # blocked is a different state — a real outside cause, held in blocked_by. It then wore
        # ⬜ (queued) for the rest of that same day, until he named a third confusion: queued
        # means never started, and this row was done and is done no longer — reopened, its own
        # state, marked 🔁.
        t["failing_key"] = t["mark"] == "✅" and not ok
        t["icon"] = "🔁" if t["failing_key"] else ("✅" if ok else t["mark"])
        t["note"] = key_failure_note(t["check"], r) if t["failing_key"] else ""
        t["verified"] = True
    else:
        ok = t["mark"] == "✅"
        t["icon"] = t["mark"]
        t["failing_key"] = False
        t["note"] = ""
        t["verified"] = False
    t["ok"] = ok

ICON_COLOUR = {"✅": G, "🔄": Y, "🔁": Y, "⛔": R, "👁️": Y, "⬜": D}

# Ranking eligibility (27.08, his word). "Blocked" only means a real, understood cause —
# a flag, like Jira's, not a feeling. That leaves two things that wore the ⛔/⬜ marks without
# being either "in progress" or "genuinely blocked": a row folded into the task that actually
# carries the work (covered_by, with no independent reason of its own), and a row he postponed
# by his own decision (deferred) — neither is blocked, so neither competes for the board's top
# slots; they drop out of the current set rather than sitting on it under the wrong label. A ⛔
# with no blocked_by and no covered_by/deferred either is a mislabel, not a fourth state: it
# ranks where it actually competes (⬜) so the drift is visible, not asserted away. None of this
# touches 🔄 or 👁️ — a task already in hand or needing his own decision is live regardless of
# any fold bookkeeping (all three of today's 🔄 tasks carry a covered_by pointer and are still
# genuinely being worked).
for t in tasks:
    t["rank_icon"] = t["icon"]
    t["excluded"] = False
    if t["icon"] not in ("⛔", "⬜"):
        continue
    if t["deferred"]:
        t["excluded"] = True
    elif t["covered_by"] and not t["blocked_by"]:
        t["excluded"] = True
    elif t["icon"] == "⛔" and not t["blocked_by"]:
        t["rank_icon"] = "⬜"

eligible = [t for t in tasks if not t["excluded"]]

# Priority order for the budget below: needs-his-eyes (only he can move it), then in hand
# (already running work), then reopened (was done and is done no longer — outranked by work
# already running, but ahead of a real outside blocker and of work never started, added
# 02.09 on his word), then blocked (worth knowing about), then queued (what's next) —
# filled round-robin, one category at a time, so a single large category cannot eat the whole
# budget and crowd the others out. Category order is the one ranking; critical only breaks ties
# inside its own category (below) and never crosses into a higher one — a cross-category
# "critical drains first" pass used to sit here and let a critical but unworkable queued task
# outrank a task the owner already needed to look at. Removed 27.08 on his word: urgency must
# never outrank whether a task is actually workable now.
# 9 task lines + 1 summary line = 10, the top end of the cap set at the report format's one home
# (~/.claude/playbook/CLAUDE.md, "How a reply to him looks"). Change it there first.
TASK_LINE_BUDGET = 9
CATEGORY_ORDER = ["👁️", "🔄", "🔁", "⛔", "⬜"]

buckets = {icon: [t for t in eligible if t["rank_icon"] == icon] for icon in CATEGORY_ORDER}
for icon in CATEGORY_ORDER:
    # Critical priority first; ties keep the file's own order. PLAN.md's "## Tasks" preamble
    # already lists critical tasks first, so this is a safety net, not the source of the order
    # (a stable sort changes nothing when the input is already in that order).
    buckets[icon].sort(key=lambda t: 0 if (t["priority"] or "").strip().lower() == "critical" else 1)

shown = []
idx = {icon: 0 for icon in CATEGORY_ORDER}
budget = TASK_LINE_BUDGET

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

# His word, 02.09: the row's own id leads its printed line, ahead of the mark and the title —
# it used to trail at the end in parentheses. Padded to the widest id PLAN.md declares, so the
# mark that follows still lands in one column down the printed list.
id_width = max((len(t["id"]) for t in tasks), default=0)

next_title = ""
for t in shown:
    tag = ""
    if next_task is not None and t["id"] == next_task["id"]:
        tag = f"  {B}<-- NEXT{X}"
        next_title = t["title"]
    # A row whose key failed is neither verified nor declared: it is a done mark the command
    # contradicts. Saying "verified" beside the ⛔ was the last of the three things the failing-key
    # work set out to stop, and it stayed behind when the other two were fixed (2026-08-28).
    if t["failing_key"]:
        verified = f"{D}marked done{X}"
    else:
        verified = f"{D}verified{X}" if t["verified"] else f"{D}declared{X}"
    colour = ICON_COLOUR.get(t["icon"], D)
    reason = ""
    if t["failing_key"]:
        reason = f" {D}— {t['note']}{X}"
    elif t["icon"] == "⛔" and t["blocked_by"]:
        r = t["blocked_by"].strip()
        reason = f" {D}— {r[:39].rstrip() + '…' if len(r) > 40 else r}{X}"
    print(f"  {D}{t['id'].ljust(id_width)}{X} {t['icon']} {colour}{t['title']}{X}  {verified}{reason}{tag}")

shown_ids = {t["id"] for t in shown}
done_count = sum(1 for t in tasks if t["icon"] == "✅")
open_count = len(tasks) - done_count
more_below = sum(1 for t in tasks if t["id"] not in shown_ids and t["icon"] != "✅")
# He does not count done tasks by default (his word, 02.09) — a done total told him nothing
# about what is left. The open count leads; done trails, kept only as the secondary figure.
print(f"  {D}… {open_count} open · {more_below} more below · {done_count} done · full list in PLAN.md / board.html{X}")

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

# required context: what actually loads before a session takes its first step —
# the boot file and profile every session reads, plus base + director (plan-17,
# q-570/q-584/q-205: the old number counted only the last two and missed the rest).
CTX_FILES="$HOME/.claude/CLAUDE.md $HOME/.claude/live-spec/profile.md skills/live-spec-base/SKILL.md skills/director/SKILL.md"
CTX_BYTES=$(cat $CTX_FILES 2>/dev/null | wc -c | tr -d ' ')
CTX_TOK=$(python3 - "$CTX_FILES" <<'EOF' 2>/dev/null
import sys
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    t = 0
    for p in sys.argv[1].split():
        t += len(enc.encode(open(p, encoding="utf-8").read()))
    print(t)
except Exception:
    print("")
EOF
)
PLAN_TOK=$(python3 - <<'EOF' 2>/dev/null
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    print(len(enc.encode(open("PLAN.md", encoding="utf-8").read())))
except Exception:
    print("")
EOF
)
if [ -n "$CTX_TOK" ]; then
  echo "  required context (boot + profile + base + director): $CTX_TOK tokens ($CTX_BYTES bytes)"
  if [ -n "$PLAN_TOK" ]; then
    echo "  + PLAN.md whole: $PLAN_TOK tokens — take a step with scripts/plan-step.sh <id> instead"
  fi
else
  echo "  required context: $CTX_BYTES bytes (tiktoken unavailable)"
fi

SPEC_CORPUS=$(cat PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md spec/* architecture/* matrix/* 2>/dev/null | wc -c | tr -d ' ')
echo "  full spec/architecture/matrix corpus: $SPEC_CORPUS bytes"

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
