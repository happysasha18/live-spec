#!/bin/bash
# state-probe.sh — печатает СЧИТАННОЕ состояние проекта, а не записанное кем-то.
#
# Зачем: возобновление работы между сессиями держалось на прозе, которую надо было правильно
# записать в конце сессии и правильно прочитать в начале. Ломалось на обоих концах. Здесь
# состояние вычисляется командами, поэтому оно не может протухнуть.
#
# Запуск: bash scripts/state-probe.sh    (первое действие каждой сессии)

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
REPO=$(pwd)

b() { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok() { printf '  \033[0;32m%s\033[0m\n' "$1"; }
warn() { printf '  \033[0;33m! %s\033[0m\n' "$1"; }
bad() { printf '  \033[0;31mX %s\033[0m\n' "$1"; }

printf '\033[1m[%s] live-spec\033[0m  %s\n' "$(date '+%H:%M, %d.%m.%Y')" "$REPO"

# ---------------------------------------------------------------- где мы
b "ГДЕ МЫ"
git fetch origin --quiet 2>/dev/null
HEAD_SHA=$(git log -1 --format=%h)
echo "  ветка $(git branch --show-current) · $HEAD_SHA · $(git log -1 --format=%s | cut -c1-60)"
DIRTY=$(git status --porcelain | wc -l | tr -d ' ')
[ "$DIRTY" = "0" ] && ok "дерево чистое" || warn "незакоммиченных файлов: $DIRTY"
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
[ "$BEHIND" != "0" ] && warn "отстаём от origin/main на $BEHIND коммитов"
[ "$AHEAD" != "0" ] && warn "не запушено коммитов: $AHEAD (пуш блокируют ворота — см. §Блокеры)"
[ "$BEHIND" = "0" ] && [ "$AHEAD" = "0" ] && ok "совпадает с origin/main"

# ---------------------------------------------------------------- план
# Статус шага берётся из его команды приёмки, а не из галочки, которую поставила рука.
# Шаг без команды печатается как ЗАЯВЛЕНО — читателю видно, где факт, а где чьё-то слово.
b "ПЛАН"
if [ -f PLAN.md ]; then
  python3 - <<'PYEOF'
import re, subprocess, sys

G, Y, R, D, B, X = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[2m", "\033[1m", "\033[0m"
steps, cur = [], None
for line in open("PLAN.md", encoding="utf-8"):
    m = re.match(r"^### \[(.)\] (.+)$", line.rstrip())
    if m:
        cur = {"mark": m.group(1), "title": m.group(2), "check": None}
        steps.append(cur)
        continue
    m = re.match(r"^<!-- check: (.+) -->$", line.strip())
    if m and cur:
        cur["check"] = m.group(1)

next_shown = False
for s in steps:
    if s["check"]:
        ok = subprocess.run(s["check"], shell=True, capture_output=True).returncode == 0
        icon, colour = ("✅", G) if ok else ("⬜", D)
        verified = f"{D}проверено{X}"
    else:
        ok = s["mark"] == "x"
        icon = {"x": "✅", "~": "🔄", "!": "⛔"}.get(s["mark"], "⬜")
        colour = G if s["mark"] == "x" else (Y if s["mark"] == "~" else (R if s["mark"] == "!" else D))
        verified = f"{D}заявлено{X}"
    tail = ""
    if not ok and not next_shown and s["mark"] != "!":
        icon, colour, tail, next_shown = "🔄" if s["mark"] == "~" else "⬜", Y, f"  {B}<-- ДАЛЬШЕ{X}", True
    print(f"  {icon} {colour}{s['title']}{X} {verified}{tail}")
PYEOF
else
  bad "PLAN.md отсутствует"
fi

# ---------------------------------------------------------------- факты
b "ФАКТЫ"
echo "  версия пака: $(cat VERSION 2>/dev/null || echo '?')"

if [ -f evals/director/check.py ]; then
  SCORE=$(python3 evals/director/check.py --all 2>/dev/null | tail -1)
  case "$SCORE" in
    *"of"*)
      SD=$(git log -1 --format=%ct -- skills/director/SKILL.md 2>/dev/null || echo 0)
      ED=$(git log -1 --format=%ct -- evals/director/traces 2>/dev/null || echo 0)
      if [ "$SD" -gt "$ED" ] 2>/dev/null; then
        echo "  Director по сценариям: $SCORE — ПЕРЕИГРОВКА СТАРЫХ ТРЕЙСОВ, про сегодняшний скилл не говорит"
      else
        echo "  Director по сценариям: $SCORE"
      fi ;;
    *) warn "эвал Director не отвечает" ;;
  esac
fi

# обязательный контекст: то, что грузится на каждый заход
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
  echo "  обязательный контекст: $CTX_TOK токенов (base + director, $CTX_BYTES байт)"
else
  echo "  обязательный контекст: $CTX_BYTES байт (tiktoken недоступен)"
fi

CANON=$(cat PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md ROADMAP.md spec/* architecture/* matrix/* 2>/dev/null | wc -c | tr -d ' ')
echo "  канон целиком: $CANON байт"
echo "  очередь ROADMAP: $(grep -c '^| [0-9]' ROADMAP.md 2>/dev/null || echo '?') строк"

# ---------------------------------------------------------------- тревога
b "ТРЕВОГА"
ALARM=0

# скилл менялся после последнего прогона эвала — счёт устарел
SKILL_D=$(git log -1 --format=%ct -- skills/director/SKILL.md 2>/dev/null || echo 0)
EVAL_D=$(git log -1 --format=%ct -- evals/director/traces 2>/dev/null || echo 0)
if [ "$SKILL_D" -gt "$EVAL_D" ] 2>/dev/null; then
  warn "скилл director менялся $(date -r "$SKILL_D" '+%d.%m') — эвал гонялся $(date -r "$EVAL_D" '+%d.%m'). Счёт устарел."
  ALARM=1
fi

# один факт — один дом
[ -f evals/director.md ] && { warn "evals/director.md существует и противоречит evals/director/ — два дома у одного факта"; ALARM=1; }

# живое состояние протухло
if [ -f NEXT_STEPS.md ]; then
  NS_D=$(git log -1 --format=%ct -- NEXT_STEPS.md 2>/dev/null || echo 0)
  LAST=$(git log -1 --format=%ct)
  [ "$NS_D" -lt "$LAST" ] && { warn "NEXT_STEPS.md старше последнего коммита дерева на $(( (LAST - NS_D) / 86400 )) дней"; ALARM=1; }
fi

# работа вне дома — /private/tmp стирается при перезагрузке.
# Ловим и рабочее дерево, и просто оставленный каталог: второе тревога проглядела.
git worktree list 2>/dev/null | grep -q "/private/tmp" && { warn "рабочее дерево в /private/tmp — стирается при перезагрузке"; ALARM=1; }
[ -d /private/tmp/ls-director ] && { warn "каталог /private/tmp/ls-director ещё стоит ($(ls /private/tmp/ls-director 2>/dev/null | wc -l | tr -d ' ') файлов) — стирается при перезагрузке"; ALARM=1; }

# чужие рабочие деревья с несмёрженной работой
git worktree list 2>/dev/null | tail -n +2 | grep -v "/private/tmp" | while read -r wt _ br; do
  br=$(echo "$br" | tr -d '[]')
  [ -z "$br" ] && continue
  n=$(git rev-list --count "main..$br" 2>/dev/null || echo 0)
  [ "$n" != "0" ] && warn "дерево $(basename "$wt") на ветке $br: $n коммит(ов) не в main"
done
git worktree list 2>/dev/null | tail -n +2 | grep -qv "/private/tmp" && ALARM=1

# дрейф хостов
for h in ~/tlvphotos ~/exhibition-engine ~/promoter ~/promoter-alexander ~/tc-cloud-validate; do
  [ -d "$h/.claude/skills/live-spec-base" ] || continue
  HV=$(grep -m1 'version:' "$h/.claude/skills/live-spec-base/SKILL.md" 2>/dev/null | tr -d ' ' | cut -d: -f2)
  PV=$(cat VERSION 2>/dev/null)
  [ "$HV" != "$PV" ] && { warn "$(basename "$h"): пак $HV против $PV в паке"; ALARM=1; }
done

[ "$ALARM" = "0" ] && ok "тревог нет"

# ---------------------------------------------------------------- блокеры
b "БЛОКЕРЫ"
if [ -f PLAN.md ]; then
  awk '/^## Блокеры/{f=1;next} /^## /{f=0} f && /^- /' PLAN.md | head -20 | sed 's/^/  /'
fi

# ---------------------------------------------------------------- следующий ход
NEXT=$(grep -E "^### \[[ ~]\]" PLAN.md 2>/dev/null | head -1 | sed 's/^### \[.\] //')
[ -n "$NEXT" ] && printf '\n\033[1mДАЛЬШЕ\033[0m\n  %s\n  (шаг целиком — в PLAN.md)\n' "$NEXT"

printf '\n'
