#!/usr/bin/env bash
# adopt/install-ratchet.sh — the turnkey ratchet-adoption kit (SPEC INV-172).
#
# Run from a HOST repo root. Vendors the pack's style/redundancy/freeze gates into the host, seeds a
# debt cap at the host's CURRENT size (an adoption run never blocks on pre-existing debt — only on
# growth beyond it), and generates a lock test that only ever tightens: doc growth beyond the seeded
# cap reds the suite, and raising the cap itself means editing the generated test (deliberate,
# visible, reviewed — never a silent raise).
#
# Usage: adopt/install-ratchet.sh [--force] [--tier universal|full] [DOC ...]
#   DOC...     gated doc paths (relative to the host root). If omitted: read
#              guardrails.config.json's spec_path (+ extra_gated_docs) if present in the host root,
#              else default to PRODUCT_SPEC.md if that file exists, else fail.
#   --force    overwrite an already-vendored file (default: skip an existing file and note it).
#   --tier     tier passed to the vendored style lint when seeding + locking (default: universal).
set -euo pipefail

PACK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_ROOT="$(pwd)"

FORCE=0
TIER="universal"
DOCS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --tier) TIER="$2"; shift 2 ;;
    --tier=*) TIER="${1#--tier=}"; shift ;;
    *) DOCS+=("$1"); shift ;;
  esac
done

# --- step a: resolve the host's gated doc set --------------------------------------------------
if [ ${#DOCS[@]} -eq 0 ]; then
  if [ -f "$HOST_ROOT/guardrails.config.json" ]; then
    while IFS= read -r d; do
      [ -n "$d" ] && DOCS+=("$d")
    done < <(python3 - "$HOST_ROOT/guardrails.config.json" << 'PYEOF'
import json, sys
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
docs = []
if cfg.get("spec_path"):
    docs.append(cfg["spec_path"])
docs.extend(cfg.get("extra_gated_docs") or [])
for d in docs:
    print(d)
PYEOF
)
  elif [ -f "$HOST_ROOT/PRODUCT_SPEC.md" ]; then
    DOCS=("PRODUCT_SPEC.md")
  fi
fi

if [ ${#DOCS[@]} -eq 0 ]; then
  echo '{"severity":"error","code":"ratchet-install","message":"no gated docs found","fix":"pass doc paths as arguments"}'
  exit 1
fi

# --- step b: vendor the pack's gate files into the host ------------------------------------------
VENDOR_FILES=(
  "scripts/spec-style-lint.py"
  "scripts/spec-style-lint.json"
  "scripts/spec-redundancy-precheck.py"
  "scripts/spec-freeze.py"
  "scripts/spec-freeze.json"
  "scripts/gate_common.py"
  "guardrails/check-freeze.sh"
  "guardrails/spec-coinages.json"
)

for rel in "${VENDOR_FILES[@]}"; do
  src="$PACK_ROOT/$rel"
  dest="$HOST_ROOT/$rel"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "skip (exists, use --force to overwrite): $rel"
  else
    cp "$src" "$dest"
    echo "vendored: $rel"
  fi
done

# --- step d: seed caps at the host's CURRENT size -----------------------------------------------
STYLE_ERRORS=0
REDUNDANCY_OPEN=0
for doc in "${DOCS[@]}"; do
  style_out="$(python3 "$HOST_ROOT/scripts/spec-style-lint.py" --tier "$TIER" "$HOST_ROOT/$doc" 2>&1 || true)"
  style_json="$(printf '%s\n' "$style_out" | tail -n1)"
  n="$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['errors'])" "$style_json")"
  STYLE_ERRORS=$((STYLE_ERRORS + n))

  redundancy_out="$(python3 "$HOST_ROOT/scripts/spec-redundancy-precheck.py" "$HOST_ROOT/$doc" 2>&1 || true)"
  redundancy_json="$(printf '%s\n' "$redundancy_out" | tail -n1)"
  m="$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['open'])" "$redundancy_json")"
  REDUNDANCY_OPEN=$((REDUNDANCY_OPEN + m))
done

# --- step c + d: write the manifest, the debt cap, and the generated lock test -------------------
python3 - "$HOST_ROOT" "$PACK_ROOT" "$TIER" "$STYLE_ERRORS" "$REDUNDANCY_OPEN" "${DOCS[@]}" << 'PYEOF'
import hashlib
import json
import os
import sys

host_root, pack_root, tier = sys.argv[1], sys.argv[2], sys.argv[3]
style_errors, redundancy_open = int(sys.argv[4]), int(sys.argv[5])
docs = sys.argv[6:]

# Kept in step with the VENDOR_FILES shell array above by hand: this list is what the update
# watcher pins, so a file vendored there and missing here changes in the pack without the host
# hearing of it. A data file counts as much as its script — a lint whose word list moved is a
# different lint.
VENDOR_FILES = [
    "scripts/spec-style-lint.py",
    "scripts/spec-style-lint.json",
    "scripts/spec-redundancy-precheck.py",
    "scripts/spec-freeze.py",
    "scripts/spec-freeze.json",
    "scripts/gate_common.py",
    "guardrails/check-freeze.sh",
    "guardrails/spec-coinages.json",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


pack_version = open(os.path.join(pack_root, "VERSION"), encoding="utf-8").read().strip()

scripts_dir = os.path.join(host_root, "scripts")
tests_dir = os.path.join(host_root, "tests")
os.makedirs(scripts_dir, exist_ok=True)
os.makedirs(tests_dir, exist_ok=True)

# The manifest is MERGED, never rebuilt from scratch: a scaffold install (adopt/install-scaffold.sh)
# may already have pinned its checks here, and a fresh ratchet run must not drop those keys (the
# 2026-07-16 defect — a from-scratch rebuild silently dropped a prior scaffold install's keys). Read
# whatever manifest exists, update only this installer's own entries, and leave every other prior
# entry — scaffold's pack-relative keys included — exactly as found.
manifest_path = os.path.join(scripts_dir, "ratchet-manifest.json")
manifest = {"pack_version": pack_version, "vendored": {}}
if os.path.isfile(manifest_path):
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {"pack_version": pack_version, "vendored": {}}
vendored = manifest.setdefault("vendored", {})

# The scaffold kit's files, where the host carries them, join the manifest (the design-review
# recommendation of 2026-07-16: one source-pin mechanism covers both installable kits, so the
# update watcher reads one file). Informational pins; this installer never vendors them.
SCAFFOLD_NAMES = ("check_completeness.py", "check_tests_present.py",
                  "check_traces_to_spec.py", "check_conflicts.py", "gate_lib.py")

# Dedupe first: a host-relative guardrails/<name> pin never resolves against the pack (only the
# pack-relative scaffold/guardrails/<name> form does) — drop either dir form of a prior scaffold-check
# key before re-pinning, mirroring install-scaffold.sh's own dedupe, so a host that hit the old
# opportunistic host-relative pin gets it cleaned up here too.
for key in list(vendored):
    base = os.path.basename(key)
    d = os.path.dirname(key)
    if base in SCAFFOLD_NAMES and d in ("guardrails", "scaffold/guardrails"):
        del vendored[key]

# This installer's own vendored set is always current.
for rel in VENDOR_FILES:
    vendored[rel] = sha256_of(os.path.join(host_root, rel))

# Re-derive scaffold pins from whatever the host actually carries, always under the pack-relative
# key so the watcher resolves it against the pack checkout, never a host path.
for name in SCAFFOLD_NAMES:
    for d in ("scaffold/guardrails", "guardrails"):
        p = os.path.join(host_root, d, name)
        if os.path.isfile(p):
            vendored["scaffold/guardrails/%s" % name] = sha256_of(p)
            break

manifest["pack_version"] = pack_version
manifest["seeded"] = {"style_errors": style_errors, "redundancy_open": redundancy_open}
manifest["tier"] = tier

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
print("wrote scripts/ratchet-manifest.json")

cap = {"max_waivers": 0, "max_redundancy_open": redundancy_open, "max_style_errors": style_errors}
with open(os.path.join(scripts_dir, "spec-debt-cap.json"), "w", encoding="utf-8") as f:
    json.dump(cap, f, indent=2)
    f.write("\n")
print("wrote scripts/spec-debt-cap.json (max_style_errors=%d max_redundancy_open=%d)"
      % (style_errors, redundancy_open))

LOCK_TEST_TEMPLATE = '''"""tests/test_ratchet_lock.py — generated by adopt/install-ratchet.sh (SPEC INV-172). Do not hand-edit
the SEEDED_* constants; they are the size measured at adoption time. The ratchet only ever tightens:
the suite reds when a gated doc grows past the seeded size, and reds when scripts/spec-debt-cap.json
is raised past what was seeded here — raising a cap for real means editing this file, on purpose,
reviewed.
"""
import json
import os
import subprocess

SEEDED_STYLE_ERRORS = {seeded_style_errors}
SEEDED_REDUNDANCY_OPEN = {seeded_redundancy_open}
GATED_DOCS = {gated_docs!r}
TIER = {tier!r}


def _host_root():
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
    )
    return out.stdout.strip()


def _cap():
    root = _host_root()
    with open(os.path.join(root, "scripts", "spec-debt-cap.json"), encoding="utf-8") as f:
        return json.load(f)


def test_caps_never_raised_past_seed():
    cap = _cap()
    assert cap["max_style_errors"] <= SEEDED_STYLE_ERRORS, (
        "max_style_errors raised above the seeded %d — raising the cap for real means editing "
        "this generated test" % SEEDED_STYLE_ERRORS)
    assert cap["max_redundancy_open"] <= SEEDED_REDUNDANCY_OPEN, (
        "max_redundancy_open raised above the seeded %d — raising the cap for real means editing "
        "this generated test" % SEEDED_REDUNDANCY_OPEN)
    assert cap["max_waivers"] <= 0


def test_style_errors_within_cap():
    root = _host_root()
    cap = _cap()
    total = 0
    for doc in GATED_DOCS:
        out = subprocess.run(
            ["python3", os.path.join(root, "scripts", "spec-style-lint.py"), "--tier", TIER,
             os.path.join(root, doc)],
            capture_output=True, text=True,
        )
        last_line = out.stdout.strip().splitlines()[-1]
        total += json.loads(last_line)["errors"]
    assert total <= cap["max_style_errors"], (
        "style errors grew to %d, above the cap %d" % (total, cap["max_style_errors"]))


def test_redundancy_open_within_cap():
    root = _host_root()
    cap = _cap()
    total = 0
    for doc in GATED_DOCS:
        out = subprocess.run(
            ["python3", os.path.join(root, "scripts", "spec-redundancy-precheck.py"),
             os.path.join(root, doc)],
            capture_output=True, text=True,
        )
        last_line = out.stdout.strip().splitlines()[-1]
        total += json.loads(last_line)["open"]
    assert total <= cap["max_redundancy_open"], (
        "redundancy-open grew to %d, above the cap %d" % (total, cap["max_redundancy_open"]))
'''

lock_test = LOCK_TEST_TEMPLATE.format(
    seeded_style_errors=style_errors,
    seeded_redundancy_open=redundancy_open,
    gated_docs=list(docs),
    tier=tier,
)
with open(os.path.join(tests_dir, "test_ratchet_lock.py"), "w", encoding="utf-8") as f:
    f.write(lock_test)
print("wrote tests/test_ratchet_lock.py")
PYEOF

# --- step f: wire (repair, or recommend) the pre-push gate -----------------------------------------
# Never blind-append: a host pre-push commonly ends in a terminating `exit` (a bare `exit N`, or a
# final `if [ "$fail" ... ]; then ... exit 1; fi` fail-check) and appending past that point is dead
# code — the installer reports "wired" while the gate never runs (2026-07-16 track-coach report,
# inbox/2026-07-16-from-track-coach-install-ratchet-appends-past-exit.md). The insertion ladder:
# before a trailing fail-check if one is found; else above a trailing bare exit; else append (the
# plain-EOF case). When neither anchor is safe, print the manual recipe instead of guessing.
# Idempotency keys off a stable marker comment, tolerant of the human label's wording drift; a
# marker (or drifted label) found in a dead position — past a top-level exit — is REPAIRED: moved
# to the safe anchor, not left dead.
PRE_PUSH="$HOST_ROOT/guardrails/pre-push"
if [ -f "$PRE_PUSH" ]; then
  GATE_R_STATUS="$(python3 - "$PRE_PUSH" << 'PYEOF'
import re
import sys

path = sys.argv[1]
MARKER = "# live-spec:gate-r"
LABEL_RE = re.compile(r"gate\s*r\W{0,3}ratchet caps", re.IGNORECASE)
FAIL_CHECK_RE = re.compile(r'^if\s*\[\s*"\$fail"\s*-ne\s*0\s*\]\s*;\s*then\b')
TOPLEVEL_EXIT_RE = re.compile(r'^exit\s+\d+\s*;?\s*(#.*)?$')

BLOCK_LINES = [
    "",
    MARKER,
    'echo ""',
    'echo "-- gate r — ratchet caps --"',
    "if ! python3 -m pytest -q tests/test_ratchet_lock.py; then",
    "  fail=1",
    "fi",
]


def read_lines(p):
    with open(p, encoding="utf-8") as f:
        return f.read().splitlines()


def write_lines(p, lines):
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def find_existing(lines):
    """Index of any line naming the marker or the human label — tolerant of label wording drift."""
    for i, line in enumerate(lines):
        if line.strip() == MARKER or LABEL_RE.search(line):
            return i
    return None


def block_bounds(lines, idx):
    """Expand to the whole contiguous non-blank run containing idx — the installed block's shape,
    old label-only style or new marker style alike, is one paragraph with blank lines around it."""
    start = idx
    while start > 0 and lines[start - 1].strip() != "":
        start -= 1
    end = idx + 1
    while end < len(lines) and lines[end].strip() != "":
        end += 1
    return start, end


def find_anchor(lines):
    """Return (kind, index): index to insert BEFORE ('fail_check'/'trailing_exit'), 'append' means
    at end (index == len(lines)), 'ambiguous' means no safe anchor was found (index is None)."""
    fail_idx = None
    for i, line in enumerate(lines):
        if FAIL_CHECK_RE.match(line.strip()):
            fail_idx = i  # keep the LAST match
    if fail_idx is not None:
        return ("fail_check", fail_idx)

    last_i = len(lines) - 1
    while last_i >= 0 and lines[last_i].strip() == "":
        last_i -= 1
    if last_i >= 0 and TOPLEVEL_EXIT_RE.match(lines[last_i]):
        return ("trailing_exit", last_i)

    for line in lines:
        if TOPLEVEL_EXIT_RE.match(line):
            return ("ambiguous", None)

    return ("append", len(lines))


def insert_at(lines, kind, idx):
    if kind == "append":
        return lines + BLOCK_LINES
    return lines[:idx] + BLOCK_LINES + lines[idx:]


try:
    lines = read_lines(path)
    existing = find_existing(lines)

    if existing is not None:
        start, end = block_bounds(lines, existing)
        dead = any(TOPLEVEL_EXIT_RE.match(lines[i]) for i in range(start))
        if not dead:
            print("already-wired")
            sys.exit(0)
        stripped = lines[:start] + lines[end:]
        kind, idx = find_anchor(stripped)
        if kind == "ambiguous":
            print("manual")
            sys.exit(0)
        write_lines(path, insert_at(stripped, kind, idx))
        print("repaired")
        sys.exit(0)

    kind, idx = find_anchor(lines)
    if kind == "ambiguous":
        print("manual")
        sys.exit(0)
    write_lines(path, insert_at(lines, kind, idx))
    print("wired")
except Exception:
    print("manual")
PYEOF
)"
  case "$GATE_R_STATUS" in
    wired)
      echo "wired: guardrails/pre-push gate r — ratchet caps"
      ;;
    already-wired)
      echo "already wired: guardrails/pre-push gate r — ratchet caps"
      ;;
    repaired)
      echo "repaired: guardrails/pre-push gate r — ratchet caps (was past a terminating exit, dead; moved to a safe anchor)"
      ;;
    manual|*)
      echo "guardrails/pre-push has no safe wiring point (an unclear tail) — add this recipe by hand:"
      echo "  echo \"-- gate r — ratchet caps --\""
      echo "  python3 -m pytest -q tests/test_ratchet_lock.py || fail=1"
      ;;
  esac
else
  echo "no guardrails/pre-push found — add this recipe to your own push gate:"
  echo "  echo \"-- gate r — ratchet caps --\""
  echo "  python3 -m pytest -q tests/test_ratchet_lock.py || fail=1"
fi

# --- step g: final summary -------------------------------------------------------------------------
python3 - "$STYLE_ERRORS" "$REDUNDANCY_OPEN" "${#VENDOR_FILES[@]}" "${DOCS[@]}" << 'PYEOF'
import json, sys

style_errors, redundancy_open, vendored = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
docs = sys.argv[4:]
print(json.dumps({
    "severity": "ok",
    "code": "ratchet-install",
    "docs": docs,
    "style_errors": style_errors,
    "redundancy_open": redundancy_open,
    "vendored": vendored,
}))
PYEOF
