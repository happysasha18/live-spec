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
[ "$AHEAD" != "0" ] && warn "не запушено коммитов: $AHEAD"
[ "$BEHIND" = "0" ] && [ "$AHEAD" = "0" ] && ok "совпадает с origin/main"

# ---------------------------------------------------------------- план
b "ПЛАН"
if [ -f PLAN.md ]; then
  awk '/^### \[/ {
    line=$0
    sub(/^### /,"",line)
    if (line ~ /^\[x\]/) { printf "  \033[0;32m%s\033[0m\n", line }
    else if (line ~ /^\[~\]/) { printf "  \033[1;33m%s  <-- СЕЙЧАС\033[0m\n", line }
    else if (line ~ /^\[!\]/) { printf "  \033[0;31m%s  <-- БЛОКЕР\033[0m\n", line }
    else { if (!shown) { printf "  \033[1m%s  <-- ДАЛЬШЕ\033[0m\n", line; shown=1 }
           else printf "  %s\n", line }
  }' PLAN.md
else
  bad "PLAN.md отсутствует"
fi

# ---------------------------------------------------------------- факты
b "ФАКТЫ"
echo "  версия пака: $(cat VERSION 2>/dev/null || echo '?')"

if [ -f evals/director/check.py ]; then
  SCORE=$(python3 evals/director/check.py --all 2>/dev/null | tail -1)
  case "$SCORE" in
    *"of"*) echo "  Director по сценариям: $SCORE" ;;
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
  NS_AGE=$(( ($(date +%s) - NS_D) / 86400 ))
  [ "$NS_AGE" -gt 7 ] && { warn "NEXT_STEPS.md не правился $NS_AGE дней"; ALARM=1; }
fi

# рабочее дерево вне дома — /private/tmp стирается при перезагрузке
git worktree list 2>/dev/null | grep -q "/private/tmp" && { warn "есть рабочее дерево в /private/tmp — стирается при перезагрузке"; ALARM=1; }

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

printf '\n'
