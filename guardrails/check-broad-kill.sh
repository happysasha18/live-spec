#!/usr/bin/env bash
# check-broad-kill.sh — SPEC INV-162 (ROADMAP 334, inverted 417): a cleanup ends only what THIS RUN
# provably owns, identified by a recorded PID, a shell variable holding one, or the process group the
# run itself holds. When several sessions share one machine, a kill by a shared install path reaches the
# other sessions' live browsers too, so the recorded process group is the sole safe target there (the
# owner's 2026-07-17 correction on ROADMAP 335). A guard that recognised a cleanup by a process NAME
# could never tell this run's
# copy of a program from the person's copy — that is the defect that once closed the owner's REAL
# browser mid-session (a broad `pkill chrome` / `pkill chrome_crashpad_handler`), destroying work state
# outside git, the effect base rule 17 forbids. So this gate DENIES every ending that names a NAME, and
# accepts an ending that proves what it owns. The four browser words that used to BE the check are now
# only this comment's example — the check itself never asks which programs matter, it asks whether the
# command can prove what it is ending.
#
# Usage: check-broad-kill.sh [path]
#   no arg  — scan the repo's tracked executable surfaces (default, the push gate)
#   path    — scan one file or directory (used by the guardrail's own test)
#
# What it flags: a line whose comment-stripped code ENDS a process by NAME —
#   * `pkill` or `killall`, which target a process by name/pattern by construction, including a
#     full-path invocation like `/usr/bin/pkill chrome`; or
#   * `kill` fed by a name-to-pid resolver — `pgrep` / `pidof`, or a `ps ... | grep <name>` pipeline —
#     the same danger wearing kill's clothes (`kill $(pgrep chrome)`, `pgrep chrome | xargs kill`,
#     `ps aux | grep chrome | awk '{print $2}' | xargs kill`); or
#   * a two-line form of that: a variable assigned from a resolver (`PIDS=$(pgrep -f chrome)`) and then
#     fed to `kill` on a later line — the taint is tracked across the file so the split cannot hide it.
# An ending that PROVES what it owns passes quiet: `kill $pid` / `kill 48213` / `os.killpg($pgid,...)`
# name a PID or a process group directly and are never name-based. The safe targets per SPEC INV-162
# are a recorded PID, a shell variable holding one passed to `kill`, or a process group the run owns
# (`os.killpg`). A kill by an INSTALL PATH is NOT exempt: a shared install such as `~/.cache/puppeteer`
# reaches every session that drives its browser from that path (the owner's 2026-07-17 correction on
# ROADMAP 335), so the recorded process group is the sole target that always stays inside this run, and
# a `pkill -f user-data-dir` reaches every process carrying that flag. This says nothing about which
# programs matter — Safari, Slack, node, and chrome all red the same when ended by name, because none of
# them proves ownership. Portable across GNU and BSD grep. Prose surfaces (spec, ROADMAP, inbox, this
# checker, its own tests, the probe corpus) legitimately NAME the patterns to forbid or exercise them
# and are excluded from the repo scan.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

scan_file() {
  # Read the comment-stripped code and print `file:line: code` for each line that ends a process by
  # NAME. `pkill`/`killall` are name-based by construction; `kill` becomes name-based when a resolver
  # on the same line (`pgrep`/`pidof`, or a `ps ... | grep` pipe) supplies its target, or when it kills
  # a variable earlier assigned from a resolver. A `kill`/`killpg` fed a PID or a process group directly
  # is not name-based and never reaches the flag. The whole classification runs in awk so the
  # kill-plus-resolver case (tokens on one line, or a taint carried across lines) is judged as one unit.
  awk -v F="$1" '
    BEGIN {
      # regexes held as strings so a "/" inside a character class does not close an awk /literal/. The
      # NAMEKILL class no longer excludes a leading "/", so a full-path `/usr/bin/pkill` is caught too.
      NAMEKILL = "(^|[^a-zA-Z._])(pkill|killall)([^a-zA-Z]|$)"    # pkill/killall: name-based by design
      RESOLVER = "(^|[^a-zA-Z._])(pgrep|pidof)([^a-zA-Z]|$)"      # a name-to-pid lookup
      PS       = "(^|[^a-zA-Z._])ps([^a-zA-Z]|$)"                 # a `ps` listing, the other resolver
      GREP     = "(^|[^a-zA-Z._])grep([^a-zA-Z]|$)"               # ... piped through grep by a name
      KILL     = "(^|[^a-zA-Z._])kill([^a-zA-Z]|$)"              # the kill verb as a word (not killpg)
      ASSIGN   = "^[ \t]*[A-Za-z_][A-Za-z0-9_]*="                # a VAR=... assignment head
    }
    {
      l = $0; sub(/#.*/, "", l)                      # strip a trailing comment, judge the code only
      ps_grep = ((l ~ PS) && (l ~ GREP))             # a `ps ... | grep <name>` resolver pipeline
      # a variable assigned from a name resolver is tainted; a later `kill` of it is a name-based ending
      # split across two lines. Track the taint across the file so the split cannot slip past.
      if ((l ~ RESOLVER || ps_grep) && match(l, ASSIGN)) {
        v = substr(l, RSTART, RLENGTH); sub(/^[ \t]*/, "", v); sub(/=.*/, "", v)
        tainted[v] = 1
      }
      name_kill = (l ~ NAMEKILL)
      kill_by_lookup = ((l ~ RESOLVER || ps_grep) && ((l ~ KILL) || name_kill))
      kill_of_tainted = 0
      if ((l ~ KILL) || name_kill)
        for (v in tainted) if (l ~ ("[$]{?" v "([^A-Za-z0-9_]|$)")) { kill_of_tainted = 1; break }
      if (!(name_kill || kill_by_lookup || kill_of_tainted)) next  # an owned PID/pgroup kill, not a name
      printf "%s:%d: %s\n", F, NR, l
    }' "$1" 2>/dev/null || true
}

hits=""
target="${1:-}"

if [ -n "$target" ]; then
  if [ -d "$target" ]; then
    while IFS= read -r f; do hits="$hits$(scan_file "$f")"$'\n'; done \
      < <(find "$target" -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' \
            -o -name '*.ts' -o -name '*.mjs' -o -name '*.cjs' -o -name '*.txt' -o -name '*.md' \))
  else
    hits="$(scan_file "$target")"
  fi
else
  cd "$REPO_ROOT"
  # `guardrails/*` and `hooks/*` pull in the extensionless executables (`pre-push`, `pre-commit`) the
  # extension globs miss; the case below drops the non-code surfaces those globs also pull in (fixtures,
  # JSON data, prose). A tracked shell/python script without an extension is a cleanup surface too.
  while IFS= read -r f; do
    # tests and the checker itself legitimately NAME / exercise the patterns; prose (.md) is not code.
    case "$f" in
      tests/*) continue ;;
      guardrails/check-broad-kill.sh) continue ;;
      guardrails/check-cleanup-notice.sh) continue ;;  # names the kill verbs to detect an ending
      guardrails/touchpoint-fixtures/*) continue ;;    # fixture text, not executable code
      *.md|*.json|*.txt) continue ;;
    esac
    hits="$hits$(scan_file "$f")"$'\n'
  done < <(git ls-files '*.sh' '*.py' '*.js' '*.ts' '*.mjs' '*.cjs' 'scripts/*' 'guardrails/*' 'hooks/*' 2>/dev/null)
fi

hits="$(printf '%s' "$hits" | grep -vE '^[[:space:]]*$' || true)"

if [ -n "$hits" ]; then
  echo "FAIL (broad-kill): part of this change shuts down a program by matching its NAME, with no proof"
  echo "  it ends only the copy this run started (SPEC INV-162):"
  printf '%s\n' "$hits" | sed 's/^/  /'
  echo "  A name match can hit someone else's real, running copy of the same program by mistake — that"
  echo "  already happened once and closed the person's own browser (row 334, base rule 17)."
  echo "  Fix: ask your agent to make the cleanup track and end only the exact process it started (its"
  echo "  own recorded process id or process group), never a name pattern."
  exit 1
fi

echo "OK (broad-kill): no cleanup ends a process by a bare name pattern (INV-162)."
exit 0
