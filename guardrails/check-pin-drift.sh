#!/usr/bin/env bash
# check-pin-drift.sh — gate (g): architecture pins must not rot (row 90, the
# track-coach lesson: 7 of 17 pins drifted in ONE session, silently; row 541, the
# 2026-08-05 prover pass that found 29 stale pins standing green under this gate;
# row 588, where 48 of the r5 rule-price page's 53 range pins rotted unseen because
# this gate read ARCHITECTURE.md alone — the r5 leg near the bottom of this file
# closed that gap without touching the ARCHITECTURE.md check above it).
#
# A pin looks like `path/to/file:123` (label words) in a node section of
# ARCHITECTURE.md, read through the one node reader guardrails/archformat.py
# (--pins), never by slicing the node body here (SPEC INV-280). The NORMATIVE
# pin is the named thing; the :line is a cache (SPEC E-14).
#
# THE MATCHING RULE (row 541, the prover record's own prescription in F4): a pin is
# proved against its OWN line, by the words that NAME something.
#   * A LINE pin (`file:N`, N > 1) — the label must be carried by line N itself,
#     with a tolerance of ±2 lines, the width of one wrapped sentence and no more:
#     one NAMING word of the label, four characters or more, must stand in that
#     five-line window.
#   * A NAMING word is any label word that is not document furniture. The furniture
#     words — rule, step, gate, line, table, check, node, file, home, section, part,
#     item, row, list, name, page, doc, entry — recur in every window of every
#     rulebook, and matching on them is how the old gate read clean: a pin labelled
#     "rule 20" sitting on rule 19's opening line matched the bare word "rule", and
#     the 2026-08-05 pass found 29 stale pins that way. A furniture word counts only
#     when the label carries no other word of four characters or more ("gates",
#     "the rules"), so a label that names nothing else is still judged by what it has.
#   * A FILE-LEVEL pin (`file:1`) names the file, not a line — line 1 of a script
#     is a shebang and of a JSON file a brace — so its label is proved against the
#     whole file, by the same naming words.
#   * A pin carrying no label at all is proved by the file's existence, and the
#     green line names those pins so the reader sees what went unproved.
#
# Every miss is named — the pin, the label, and what the target line actually
# reads — and every miss is RED. The old gate reported a label miss as advisory
# DRIFT unless --strict was passed, and the push chain passed no --strict, so the
# 29 stale pins crossed a green gate. --strict is now the default; the flag is
# still accepted so an installed host's wiring keeps working.
#
# RED — pinned file missing, :line beyond end of file, or the label not carried.
#
# Usage: check-pin-drift.sh [architecture-file] [--strict]

set -euo pipefail

# the one node reader sits beside this script (both in guardrails/), found by the script's own path so a
# gate run against an ARCHITECTURE.md anywhere (a test fixture in a temp dir) still resolves the reader.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCH="${1:-$(git rev-parse --show-toplevel)/ARCHITECTURE.md}"
[ "${2:-}" = "--strict" ] && echo "note (pin drift): --strict is the default since row 541; the flag changes nothing."
ROOT="$(cd "$(dirname "$ARCH")" && pwd)"

# The line-pin tolerance, in lines either side of the pinned line. This one IS a bar — a pin further
# off than TOL reds the gate — and it has no incident or source behind it (the 2026-08-07 census, row
# 9, found no trace; the introducing commit 3915e95 carries a subject line and no body). An
# engineering default, not a policy decision: it names how much a pinned line may shift before the
# pin counts as stale, and the direction of a wrong value is a noisier gate, not a missed drift.
TOL=2
fail=0
checked=0
line_pins=0
file_pins=0
bare_pins=0
bare_names=""
read_files=""

# Document furniture — the words every window of a rulebook holds. Singular forms; a
# trailing "s" is stripped before the comparison.
FURNITURE=" rule step gate line table check node file home section part item row list name page doc entry "

# The label's words of four characters or more, whole and split at hyphens and
# underscores, printed one per line: the naming words first, then the furniture
# words, separated by a line reading `--`.
#
# The four-character floor is a stop-word heuristic — it drops "the", "a", "of", "and" and the like so
# a label matches on its naming words. Kin of check-vocabulary.py's own significant-word floor. No
# source behind the exact 4 (2026-08-07 census, row 10); an engineering default. It cannot hide drift
# on its own: the FURNITURE list below is what decides which surviving words count as naming.
label_words() {
  local label="$1" w part naming="" furniture="" bare seen=" "
  for w in $label; do
    w="$(printf '%s' "$w" | tr -cd '[:alnum:]_-')"
    for part in "$w" ${w//[-_]/ }; do
      [ ${#part} -lt 4 ] && continue
      bare="$(printf '%s' "$part" | tr '[:upper:]' '[:lower:]')"
      case "$seen" in *" $bare "*) continue ;; esac
      seen="$seen$bare "
      bare="${bare%s}"
      case "$FURNITURE" in
        *" $bare "*) furniture="$furniture$part"$'\n' ;;
        *)           naming="$naming$part"$'\n' ;;
      esac
    done
  done
  printf '%s--\n%s' "$naming" "$furniture"
}

# pins: `path:line` optionally followed by (label)
while IFS=$'\t' read -r path line label; do
  [ -z "$path" ] && continue
  case "$path" in
    "~/"*) full="$HOME/${path#\~/}" ;;
    /*)    full="$path" ;;
    *)     full="$ROOT/$path" ;;
  esac
  # A machine-local pin (~/ or absolute, outside the repo) exists only on the machine that
  # carries it. Where the HOME running this gate holds no such file — CI, a fresh machine, a
  # run under a clean HOME — it is noted and skipped, never a false red (the second net,
  # SPEC M-5). The stand-down reads the file, not the CI variable: the variable said "absent"
  # only where CI happened to be the sole clean HOME, which stopped being true. A pin whose
  # file IS present is checked wherever it stands, so a drifted home file still reds locally.
  # It is skipped BEFORE the count, so the green line's arithmetic closes over the pins
  # this run actually read; the note above names what stood outside it.
  case "$path" in
    "~/"*|/*)
      if [ ! -f "$full" ]; then
        echo "note (pin drift): $path:$line — machine-local pin, absent under this HOME; skipped."
        continue
      fi ;;
  esac
  checked=$((checked+1))
  if [ ! -f "$full" ]; then
    echo "FAIL (pin drift): $path:$line — pinned file missing (the architecture points at a file"
    echo "  that isn't there anymore)."; fail=1; continue
  fi
  read_files="$read_files$path"$'\n'
  total=$(wc -l < "$full")
  if [ "$line" -gt "$total" ]; then
    echo "FAIL (pin drift): $path:$line — beyond end of file ($total lines; the reference points"
    echo "  past where the file now ends)."; fail=1; continue
  fi
  if [ -z "$label" ]; then
    bare_pins=$((bare_pins+1))
    bare_names="$bare_names$path:$line, "
    continue
  fi

  if [ "$line" -le 1 ]; then
    file_pins=$((file_pins+1))
    window="$(cat "$full")"
    where="the file"
  else
    line_pins=$((line_pins+1))
    lo=$(( line > TOL ? line - TOL : 1 ))
    hi=$(( line + TOL ))
    window="$(sed -n "${lo},${hi}p" "$full")"
    where="lines $lo-$hi"
  fi

  # The words the pin is judged by: its naming words, or — when it has none — its
  # furniture words. A hyphenated or underscored word is tried whole and in its parts,
  # so `workshop-noise` matches "workshop noise" and `render_widget` its own halves.
  words="$(label_words "$label")"
  naming="$(awk 'BEGIN{before=1} /^--$/{before=0;next} before && NF' <<<"$words")"
  if [ -n "$naming" ]; then
    judged_by="$naming"
    kind="naming word"
  else
    judged_by="$(awk 'BEGIN{after=0} /^--$/{after=1;next} after && NF' <<<"$words")"
    kind="word"
  fi

  found=0
  while IFS= read -r part; do
    [ -z "$part" ] && continue
    if grep -qiF -- "$part" <<<"$window"; then found=1; break; fi
    if grep -qiF -- "${part%s}" <<<"$window"; then found=1; break; fi
  done <<<"$judged_by"

  if [ "$found" -eq 0 ]; then
    looked="$(printf '%s' "$judged_by" | paste -sd, - | sed 's/,/, /g')"
    echo "FAIL (pin drift): $path:$line ($label) — the code has moved on: no ${kind} of the label"
    echo "  stands in $where anymore; looked for [$looked]."
    if [ "$line" -gt 1 ]; then
      echo "    line $line reads: $(sed -n "${line}p" "$full" | cut -c1-100)"
    fi
    fail=1
  fi
done < <(python3 "$SCRIPT_DIR/archformat.py" --pins "$ARCH")

if [ "$checked" -eq 0 ]; then
  echo "FAIL (pin drift): no pins parsed from $ARCH"; exit 1
fi

if [ "$fail" -ne 0 ]; then
  echo "  Fix: ask your agent to find where this description now lives in the code and re-point"
  echo "  the reference, or reword the description to match what the code actually does (SPEC E-14)."
fi

reach="$(printf '%s' "$read_files" | sed '/^$/d' | sort -u | paste -sd, - | sed 's/,/, /g')"
# The word OK stands only over a leg that passed. The r5 leg below runs either way, so this
# leg's verdict is decided here, before that leg can add findings of its own (row 588).
arch_fail="$fail"
if [ "$arch_fail" -eq 0 ]; then
  echo "OK (pin drift): $checked pin(s) checked — $line_pins line pin(s) proved against their own line (tolerance ±$TOL lines), $file_pins file-level :1 pin(s) proved against the whole file, $bare_pins unlabelled pin(s) proved by the file's existence alone: ${bare_names%, }."
else
  echo "FAILED (pin drift): $checked pin(s) checked in $(basename "$ARCH"), and the findings above stand."
fi
echo "  reach: files=[$(basename "$ARCH"), $reach]"

# --- the .live-spec range-pin leg (ROADMAP row 588) ---------------------------------------
# ARCHITECTURE.md is not the only page that pins a line — the r5 rule-price page pins 53 skill
# rules by `path:start-end`, a RANGE rather than a single line, and it rotted unseen because
# this gate read ARCHITECTURE.md alone. This leg widens the reach to that page, by the same
# naming-word rule as above: the pinned range must carry the label somewhere in its own span
# (the whole range, not a ±2-line window — a range pin names more than one line on purpose).
# The ARCHITECTURE.md check above is untouched by this leg; it still runs, reports, and reds on
# its own terms.
GITROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
R5="$GITROOT/.live-spec/r5-rule-prices-2026-08-11.md"
if [ -n "$GITROOT" ] && [ -f "$R5" ]; then
  r5_checked=0
  fail_before_r5="$fail"
  while IFS=$'\t' read -r rpath rstart rend rlabel; do
    [ -z "$rpath" ] && continue
    r5_checked=$((r5_checked+1))
    rfull="$GITROOT/$rpath"
    if [ ! -f "$rfull" ]; then
      echo "FAIL (pin drift, r5): $rpath:$rstart-$rend — pinned file missing"; fail=1; continue
    fi
    rtotal=$(wc -l < "$rfull")
    if [ "$rend" -gt "$rtotal" ]; then
      echo "FAIL (pin drift, r5): $rpath:$rstart-$rend — end beyond file end ($rtotal lines)"; fail=1; continue
    fi
    rwindow="$(sed -n "${rstart},${rend}p" "$rfull")"
    rwords="$(label_words "$rlabel")"
    rnaming="$(awk 'BEGIN{before=1} /^--$/{before=0;next} before && NF' <<<"$rwords")"
    if [ -n "$rnaming" ]; then rjudged="$rnaming"; rkind="naming word"
    else rjudged="$(awk 'BEGIN{after=0} /^--$/{after=1;next} after && NF' <<<"$rwords")"; rkind="word"
    fi
    rfound=0
    while IFS= read -r rpart; do
      [ -z "$rpart" ] && continue
      if grep -qiF -- "$rpart" <<<"$rwindow"; then rfound=1; break; fi
      if grep -qiF -- "${rpart%s}" <<<"$rwindow"; then rfound=1; break; fi
    done <<<"$rjudged"
    if [ "$rfound" -eq 0 ]; then
      echo "FAIL (pin drift, r5): $rpath:$rstart-$rend — no $rkind of the label stands in lines $rstart-$rend"
      fail=1
    fi
  done < <(python3 - "$R5" <<'PYEOF'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
homes = list(re.finditer(r'Home: `([^`]+):(\d+)-(\d+)`\.', text))
opens = list(re.finditer(r'Opening line, quoted in full: "(.+?)"\n', text, re.S))
for hm, om in zip(homes, opens):
    print("%s\t%s\t%s\t%s" % (hm.group(1), hm.group(2), hm.group(3), om.group(1).replace("\t", " ")))
PYEOF
)
  if [ "$fail" -eq "$fail_before_r5" ]; then
    echo "OK (pin drift, r5): $r5_checked range pin(s) checked against $(basename "$R5") — each proved against its own line range, by the label's naming words."
  else
    echo "FAILED (pin drift, r5): $r5_checked range pin(s) checked against $(basename "$R5"), and the findings above stand."
  fi
else
  echo "note (pin drift): no .live-spec/r5-rule-prices-2026-08-11.md found under this tree; that leg skipped."
fi

[ "$fail" -ne 0 ] && exit 1
exit 0
