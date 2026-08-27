#!/usr/bin/env bash
# check-cleanup-notice.sh — SPEC INV-204 (ROADMAP 417): a cleanup says what it ended. Every cleanup
# path that ENDS a process must emit the notice — WHAT it ended and WHY the run owned it — so an ending
# nobody expected is visible the moment it happens rather than at the next unexplained loss. This gate
# reds a tracked script that ends a process but carries no notice anywhere in its code. It ships ahead
# of INV-162's stricter owned-identity check and makes it safe to land, showing what the strict form
# would have refused before the strict form starts refusing.
#
# Usage: check-cleanup-notice.sh [path]
#   no arg  — scan the repo's tracked executable surfaces (default, the push gate)
#   path    — scan one file or directory (used by the guardrail's own test)
#
# What it flags: a FILE (not a line — an emit and the ending it announces rarely share a line) whose
# comment-stripped code ENDS A PROCESS but carries the cleanup-notice marker NOWHERE in that code. A
# file ENDS a process when its code reaps a process group (`killpg`), name-kills (`pkill` / `killall`),
# terminates a spawned child (`proc.terminate()` / `proc.kill()` on a `subprocess`/`Popen` handle), or
# sends a real terminating signal to another process (a shell `kill -<sig>` other than `-0`, or an
# `os.kill(..., signal.SIG...)` / `os.kill(..., <nonzero>)`). A liveness probe (`os.kill(pid, 0)`,
# `kill -0`) and a signal-handler self-raise (`os.kill(os.getpid(), ...)`, whose signal is a variable,
# not a literal) end no spawned resource and never trip the gate. A file that emits the notice —
# carrying the `CLEANUP-NOTICE` marker, or a call to the shared `cleanup_notice` helper — passes.
# Portable across GNU and BSD grep. Honest boundary: this is a structural scan, kin of
# check-muted-launch.sh; an ending built through an indirection the patterns above cannot read stays the
# forker's own to announce. Prose surfaces, this checker, its tests, and the probe corpus are excluded.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

ends_a_process() {
  # print "ENDS" if the file's comment-stripped code ends a process by any recognised means.
  awk '
    BEGIN {
      NAMEKILL = "(^|[^/a-zA-Z._])(pkill|killall)([^a-zA-Z]|$)"
      KILLPG   = "killpg"
      SHKILL   = "(^|[^a-zA-Z._])kill[ \t]+-(SIG[A-Z]+|[A-Z]+|[1-9][0-9]*)"   # kill -9 / -TERM, not -0
      OSKILL_SIG = "os\\.kill\\([^)]*signal\\.SIG"
      OSKILL_NUM = "os\\.kill\\([^)]*,[ \t]*[1-9]"                            # os.kill(pid, 9), not , 0
      PROC_END = "\\.(terminate|kill)\\([ \t]*\\)"      # proc.terminate()/proc.kill(): Popen endings
    }
    {
      l = $0; sub(/#.*/, "", l)
      if (l ~ NAMEKILL || l ~ KILLPG || l ~ SHKILL || l ~ OSKILL_SIG || l ~ OSKILL_NUM || l ~ PROC_END) {
        print "ENDS"; exit
      }
    }' "$1" 2>/dev/null || true
}

emits_notice() {
  # print "EMITS" if the file's comment-stripped code carries the marker or a helper call.
  awk '
    { l = $0; sub(/#.*/, "", l)
      if (l ~ /CLEANUP-NOTICE/ || l ~ /cleanup_notice/) { print "EMITS"; exit } }' "$1" 2>/dev/null || true
}

scan_file() {
  local f="$1"
  [ "$(ends_a_process "$f")" = "ENDS" ] || return 0
  [ "$(emits_notice "$f")" = "EMITS" ] && return 0
  echo "$f"
}

hits=""
target="${1:-}"

if [ -n "$target" ]; then
  if [ -d "$target" ]; then
    while IFS= read -r f; do
      hit="$(scan_file "$f")"; [ -n "$hit" ] && hits="$hits$hit"$'\n'
    done < <(find "$target" -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' \
          -o -name '*.ts' -o -name '*.mjs' -o -name '*.cjs' \))
  else
    hit="$(scan_file "$target")"; [ -n "$hit" ] && hits="$hit"
  fi
else
  cd "$REPO_ROOT"
  while IFS= read -r f; do
    case "$f" in
      tests/*) continue ;;
      guardrails/check-cleanup-notice.sh) continue ;;
      guardrails/check-broad-kill.sh) continue ;;   # names the kill verbs to forbid, ends nothing
      *.md) continue ;;
    esac
    hit="$(scan_file "$f")"; [ -n "$hit" ] && hits="$hits$hit"$'\n'
  done < <(git ls-files '*.sh' '*.py' '*.js' '*.ts' '*.mjs' '*.cjs' 'scripts/*' 2>/dev/null)
fi

hits="$(printf '%s' "$hits" | grep -vE '^[[:space:]]*$' || true)"

if [ -n "$hits" ]; then
  echo "FAIL (cleanup-notice): part of this change ends a process during cleanup but never says what it"
  echo "  ended (SPEC INV-204) — with no record, nobody can check afterward whether it ended the right thing:"
  printf '%s\n' "$hits" | sed 's/^/  /'
  echo "  Fix: ask your agent to print what was ended and the proof it owned it (a process id, a process"
  echo "  group, or a path inside its own run), using the shared helper guardrails/cleanup_notice.py."
  exit 1
fi

echo "OK (cleanup-notice): every cleanup path that ends a process says what it ended (INV-204)."
exit 0
