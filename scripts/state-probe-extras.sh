# state-probe-extras.sh — this project's own facts, printed by scripts/state-probe.sh's extras
# hook under this file's own heading. The pack's renderer stays generic; whatever names this pack's
# own files or measures its own machinery lives here instead, verbatim, so a fix to it never has to
# touch the shared renderer.
#
# Sourced, not run: it inherits REPO and the b/ok/warn/bad printers from state-probe.sh.

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

if grep -q '"status": "stale after' evals/build-pipeline/closing-scenarios.json 2>/dev/null; then
  warn "Pipeline closing eval: STALE after the Director split — fresh producer runs are owed"
elif [ -f evals/build-pipeline/closing-scenarios.json ]; then
  CLOSING=$(python3 -c "import json;r=json.load(open('evals/build-pipeline/closing-scenarios.json'))['recorded_run'];print(r['score'], 'recorded', r['recorded'])" 2>/dev/null)
  [ -n "$CLOSING" ] && echo "  Pipeline closing by scenario: $CLOSING"
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
