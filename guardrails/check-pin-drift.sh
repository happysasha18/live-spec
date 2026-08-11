#!/usr/bin/env bash
# check-pin-drift.sh — gate (g): architecture pins must not rot (row 90, the
# track-coach lesson: 7 of 17 pins drifted in ONE session, silently; row 541, the
# 2026-08-05 prover pass that found 29 stale pins standing green under this gate).
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

TOL=2            # the line-pin tolerance, in lines either side of the pinned line
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
  # A machine-local pin (~/ or absolute, outside the repo) exists only on the author's
  # machine; in CI (the second net, SPEC M-5) it is noted and skipped, never a false red.
  # It is skipped BEFORE the count, so the green line's arithmetic closes over the pins
  # this run actually read; the note above names what stood outside it.
  case "$path" in
    "~/"*|/*)
      if [ ! -f "$full" ] && [ "${CI:-}" = "true" ]; then
        echo "note (pin drift): $path:$line — machine-local pin, absent in CI; skipped."
        continue
      fi ;;
  esac
  checked=$((checked+1))
  if [ ! -f "$full" ]; then
    echo "FAIL (pin drift): $path:$line — pinned file missing"; fail=1; continue
  fi
  read_files="$read_files$path"$'\n'
  total=$(wc -l < "$full")
  if [ "$line" -gt "$total" ]; then
    echo "FAIL (pin drift): $path:$line — beyond end of file ($total lines)"; fail=1; continue
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
    echo "FAIL (pin drift): $path:$line ($label) — no ${kind} of the label stands in $where; looked for [$looked]."
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
  echo "  Fix: re-run the pin's grep and update the path/line, or re-label the pin to name what the line carries (SPEC E-14)."
  exit 1
fi

reach="$(printf '%s' "$read_files" | sed '/^$/d' | sort -u | paste -sd, - | sed 's/,/, /g')"
echo "OK (pin drift): $checked pin(s) checked — $line_pins line pin(s) proved against their own line (tolerance ±$TOL lines), $file_pins file-level :1 pin(s) proved against the whole file, $bare_pins unlabelled pin(s) proved by the file's existence alone: ${bare_names%, }."
echo "  reach: files=[$(basename "$ARCH"), $reach]"
exit 0
