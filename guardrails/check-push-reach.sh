#!/usr/bin/env bash
# check-push-reach.sh — the reach map's deciding script (SPEC INV-45, ROADMAP row 147;
# scoped middle road ROADMAP row 362, SPEC M-344).
# Answers ONE question for the push gate: can this push's diff reach the python suite?
#   exit 0 = prose-only diff — every changed file matches the explicit prose class below;
#            the suite's checks read none of these files, gate b may stand the suite down BY NAME.
#   exit 2 = SCOPED — every changed file is PROSE or INFRA, and at least one is INFRA: the diff is
#            confined to the guardrail scripts, the scaffold checks, the shipped templates, the
#            helper scripts, the hooks, the guardrails config, or the suite's own test files. The
#            scoped test set is printed as `SCOPED <path>` lines (sorted, unique) plus one reason
#            line; gate b runs exactly that set instead of the whole suite.
#   exit 1 = full reach — at least one changed file is outside PROSE ∪ INFRA (code, spec, matrix,
#            queue, skills, scripts the map never met — or anything NEW), or an INFRA file names no
#            test (directly or via one referrer level), or the diff/base cannot be established.
#            Conservative by construction.
#
# The prose class is EXPLICIT and narrow — "just .md" is NOT a class: PRODUCT_SPEC.md, TEST_MATRIX.md,
# ARCHITECTURE.md, PLAN.md, JOURNAL.md, NEXT_STEPS.md and every SKILL.md are TESTED documents
# (string rows read them) and must never be added below.
#
# The infra class is EXPLICIT too: guardrails/, scaffold/guardrails/, templates/, scripts/, hooks/,
# adopt/, the file guardrails.config.json, and tests/test_*.py files. A changed infra file's owning
# tests are found mechanically by filename — grep for the changed file's basename over tests/test_*.py
# — plus ONE referrer level: a file under one of the infra dirs that names the changed file's basename
# adds the tests that name THAT referrer's own basename. tests/test_traceability.py (the traceability
# net) always rides along — pinned as the first permanent member of ALWAYS_SCOPED below, an integrity
# rider. A changed infra file that no test names (directly or via a referrer) is not
# safely scopable, so the whole diff falls back to FULL — the conservative teeth this road keeps.
#
# Usage: check-push-reach.sh [base-ref]      (default base: origin/main)
#   REACH_FILES (tests only): newline-separated file list replaces the git diff.

set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

BASE="${1:-origin/main}"

# --- reach classes as host config (SPEC INV-224, ROADMAP row 380) ---------------------------
# The infra directories, prose files, and referrer directories the classifier sorts a changed
# file into are the HOST's to declare, not this script's to hold as constants: they are read
# from guardrails.config.json under `reach_classes`, the pack's own values shipped there as the
# default. A host whose layout differs — a product engine kept under scripts/, not helper tools
# — declares its own classes there once (the same knowledge project.layers carries, SPEC
# INV-135) and this vendored script needs no edit. REACH_CONFIG overrides the path (tests only).
# The conservative floor holds by construction: a config that names no classes leaves every
# changed file unclassified, so matches_prose/matches_infra both return false and the whole diff
# falls to FULL — never a false-green scope on a missing or empty config.
CONFIG="${REACH_CONFIG:-$REPO_ROOT/guardrails.config.json}"

reach_class() {
  # $1 = key under reach_classes; prints its values newline-separated, empty when the config or
  # the key is absent or unreadable (which lands on the conservative floor above).
  python3 - "$CONFIG" "$1" <<'PY' 2>/dev/null || true
import json, sys
try:
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
except Exception:
    sys.exit(0)
for v in cfg.get("reach_classes", {}).get(sys.argv[2], []):
    print(v)
PY
}

PROSE_FILES=(); while IFS= read -r x; do [ -n "$x" ] && PROSE_FILES+=("$x"); done < <(reach_class prose_files)
PROSE_DIRS=();  while IFS= read -r x; do [ -n "$x" ] && PROSE_DIRS+=("$x");  done < <(reach_class prose_dirs)
INFRA_DIRS=();  while IFS= read -r x; do [ -n "$x" ] && INFRA_DIRS+=("$x");  done < <(reach_class infra_dirs)
INFRA_FILES=(); while IFS= read -r x; do [ -n "$x" ] && INFRA_FILES+=("$x"); done < <(reach_class infra_files)
INFRA_GLOBS=(); while IFS= read -r x; do [ -n "$x" ] && INFRA_GLOBS+=("$x"); done < <(reach_class infra_globs)

if [ -n "${REACH_FILES:-}" ]; then
  files="$REACH_FILES"
else
  if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
    echo "reach: base ref '$BASE' not found — conservative fall-through to FULL."
    exit 1
  fi
  files="$(git diff --name-only "$BASE"..HEAD)"
fi

matches_prose() {
  local f="$1" p
  for p in "${PROSE_FILES[@]:-}"; do [ -z "$p" ] && continue; [ "$f" = "$p" ] && return 0; done
  for p in "${PROSE_DIRS[@]:-}"; do [ -z "$p" ] && continue; case "$f" in "$p"/*) return 0 ;; esac; done
  return 1
}

matches_infra() {
  local f="$1" p
  for p in "${INFRA_FILES[@]:-}"; do [ -z "$p" ] && continue; [ "$f" = "$p" ] && return 0; done
  for p in "${INFRA_DIRS[@]:-}"; do [ -z "$p" ] && continue; case "$f" in "$p"/*) return 0 ;; esac; done
  for p in "${INFRA_GLOBS[@]:-}"; do [ -z "$p" ] && continue; case "$f" in $p) return 0 ;; esac; done
  return 1
}

seen=0
full=0
infra_files=()
while IFS= read -r f; do
  [ -z "$f" ] && continue
  seen=$((seen + 1))
  if matches_prose "$f"; then
    continue
  elif matches_infra "$f"; then
    infra_files+=("$f")
  else
    echo "reach: '$f' is outside the prose/infra classes — FULL suite."
    full=1
  fi
done <<< "$files"

if [ "$seen" -eq 0 ]; then
  echo "reach: empty diff — conservative fall-through to FULL."
  exit 1
fi

if [ "$full" -ne 0 ]; then
  exit 1
fi

if [ "${#infra_files[@]}" -eq 0 ]; then
  echo "OK (reach): prose-only diff — the suite's checks read none of the changed files."
  exit 0
fi

# SCOPED middle road: every changed file is PROSE or INFRA, and at least one is INFRA.
# The referrer directories are host config too (SPEC INV-224); loaded above, joined to a
# space-separated list here for the word-split grep below.
REFERRER_DIRS="$(reach_class referrer_dirs | tr '\n' ' ')"

# --- ALWAYS_SCOPED (permanent scoped-run riders) BEGIN ---
# Tests pinned to ride EVERY scoped run, whatever the diff touched. Two kinds live here:
#   - an integrity rider: a test that must ride for the suite's own integrity whether or not it
#     enumerates infra dirs. tests/test_traceability.py is the first permanent member — the
#     traceability net rides every scoped verdict so a scoped run can never skip it.
#   - an enumerating-infra test: one that reads an infra directory by walk/glob rather than naming
#     basenames, invisible to the by-name discovery below, pinned here so it rides too.
# One home: the suite-hygiene net (tests/test_guardrails.py::TestScopedReachHygiene) reads THIS block
# [ROADMAP 366].
ALWAYS_SCOPED=(
  "tests/test_traceability.py"      # integrity rider — rides every scoped run for suite integrity
  "tests/test_setup_entry.py"       # enumerating-infra test — globs skills/*/SKILL.md, invisible to by-name discovery
  "tests/test_guardrails_unit.py"   # the guardrail unit half: fast, sandbox-free, rides every scoped run
  "tests/test_work_board.py"        # enumerating-infra test — walks scripts/ to prove the craft set has one home
)
# SCOPED_EXCLUDED — test files the by-name discovery must NOT pull into a scoped run. One member:
# the guardrail integration half, whose classes copy the repository, build git sandboxes and run
# the suite inside the suite. It runs on explicit ask and in the full suite; a scoped run takes the
# unit half above instead. A changed infra file whose ONLY owning test sits in an excluded file
# counts as unowned and the diff falls to FULL — the conservative floor keeps its teeth.
SCOPED_EXCLUDED=(
  "tests/test_guardrails.py"
)
# --- ALWAYS_SCOPED (permanent scoped-run riders) END ---

scoped=()
scoped_has() {
  local needle="$1" x
  for x in "${scoped[@]:-}"; do
    [ "$x" = "$needle" ] && return 0
  done
  return 1
}
add_scoped() {
  # returns 1 (and adds nothing) for an excluded file, so a caller counting owners
  # never counts an excluded owner — the file then falls to FULL if nothing else owns it
  local ex
  for ex in "${SCOPED_EXCLUDED[@]:-}"; do
    [ -n "$ex" ] && [ "$1" = "$ex" ] && return 1
  done
  scoped_has "$1" || scoped+=("$1")
  return 0
}

conservative_full=0
for f in "${infra_files[@]}"; do
  case "$f" in
    tests/test_*.py)
      # a changed test file adds itself to the scoped set — it is its own owning test. A DELETED
      # test file must never be handed to pytest (a nonexistent path reds collection, a false red);
      # it falls through to by-name discovery and, unowned, to FULL [2.3.0 audit, finding 6].
      if [ -f "$f" ]; then
        if add_scoped "$f"; then
          continue
        fi
        # an excluded test file that itself changed falls through to by-name discovery
        # and, unowned there, to FULL
      fi
      ;;
  esac

  base="$(basename "$f")"
  owning=0

  while IFS= read -r t; do
    [ -z "$t" ] && continue
    if add_scoped "$t"; then
      owning=1
    fi
  done < <(grep -l -F -- "$base" tests/test_*.py 2>/dev/null || true)

  while IFS= read -r r; do
    [ -z "$r" ] && continue
    [ "$r" = "$f" ] && continue
    rbase="$(basename "$r")"
    while IFS= read -r t; do
      [ -z "$t" ] && continue
      if add_scoped "$t"; then
        owning=1
      fi
    done < <(grep -l -F -- "$rbase" tests/test_*.py 2>/dev/null || true)
  done < <(grep -rl -F -- "$base" $REFERRER_DIRS 2>/dev/null || true)

  if [ "$owning" -eq 0 ]; then
    echo "reach: '$f' names no test file (directly or via one referrer level) — conservative fall-through to FULL."
    conservative_full=1
  fi
done

if [ "$conservative_full" -ne 0 ]; then
  exit 1
fi

for t in "${ALWAYS_SCOPED[@]:-}"; do
  [ -z "$t" ] && continue
  if [ ! -f "$t" ]; then
    # a stale pin must red loudly under its own name here, never as a bare pytest collection error
    echo "BLOCK (reach): ALWAYS_SCOPED pins a missing file: $t — fix the pin before pushing." >&2
    exit 1
  fi
  add_scoped "$t" || true
done

sorted_scoped="$(printf '%s\n' "${scoped[@]}" | sort -u)"
printf '%s\n' "$sorted_scoped" | while IFS= read -r t; do
  [ -z "$t" ] && continue
  echo "SCOPED $t"
done
count="$(printf '%s\n' "$sorted_scoped" | grep -c .)"
echo "OK (reach): infra-class diff — scoped to $count test files (each names a changed file; + the traceability net), SPEC INV-45"
exit 2
