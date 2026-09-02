#!/usr/bin/env bash
# adopt/install-style-gates.sh — the turnkey style-gate adoption kit (SPEC INV-172).
#
# Run from a HOST repo root. Vendors the pack's style lint, near-duplicate reading, freeze tool and
# their shared library into the host, pins each vendored copy's source in scripts/ratchet-manifest.json
# so the update check can tell a current copy from a stale one, and wires the style gate into the
# host's push gate.
#
# WHAT THIS INSTALLER DOES NOT DO, and why. Until 2026-09-02 this script also measured the host's
# documents at adoption time, wrote those two counts into scripts/spec-debt-cap.json as caps, and
# generated tests/test_ratchet_lock.py to pin them — a ceiling seeded from whatever the host's
# documents happened to measure that day. A bound of that shape reds a delivery that improves the
# document: the pack's own copy reddened on 2026-08-19 for cutting two whole requirements out of its
# specification, because the criteria removed ran shorter than the rest and the average rose while
# the document shrank (docs/prover/2026-08-19-invented-numbers-out.md, finding 9). The whole class
# was cut on the owner's word. What ships instead is the style gate at zero: every finding it reds
# names one construction at one line, and a host that wants to carry a specific finding for now
# writes it into scripts/spec-waivers.json by rule, file and text, with an expiry date, so the debt
# is named rather than hidden inside an aggregate.
#
# Usage: adopt/install-style-gates.sh [--force] [--tier universal|full] [DOC ...]
#   DOC...     gated doc paths (relative to the host root). If omitted: read
#              guardrails.config.json's spec_path (+ extra_gated_docs) if present in the host root,
#              else default to PRODUCT_SPEC.md if that file exists, else fail.
#   --force    overwrite an already-vendored file (default: skip an existing file and note it).
#   --tier     tier the vendored style lint runs at, in the wired gate (default: universal).
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
  echo '{"severity":"error","code":"style-gates-install","message":"no gated docs found","fix":"pass doc paths as arguments"}'
  exit 1
fi

# A doc named by config or default may still not exist yet — the ordinary state of a fresh project
# before step 2 (or a by-hand doc write) has created it. That is not breakage, so refuse cleanly here,
# before step b vendors anything: a clean early exit means a re-run after the doc exists starts from
# nothing rather than picking up a half-vendored tree.
MISSING_DOCS=()
for doc in "${DOCS[@]}"; do
  if [ ! -f "$HOST_ROOT/$doc" ]; then
    MISSING_DOCS+=("$doc")
  fi
done
if [ ${#MISSING_DOCS[@]} -gt 0 ]; then
  python3 - "${MISSING_DOCS[@]}" << 'PYEOF'
import json, sys

missing = sys.argv[1:]
print(json.dumps({
    "severity": "error",
    "code": "style-gates-install",
    "message": "gated doc(s) not found yet: %s" % ", ".join(missing),
    "fix": "write the doc first (step 2 does this for you), then re-run adopt/install-style-gates.sh — "
           "a fresh project has no gated docs until then, so this is expected, not a failure",
}))
PYEOF
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

# --- step c: write or merge the source-pin manifest ----------------------------------------------
python3 - "$HOST_ROOT" "$PACK_ROOT" "$TIER" "${DOCS[@]}" << 'PYEOF'
import hashlib
import json
import os
import sys

host_root, pack_root, tier = sys.argv[1], sys.argv[2], sys.argv[3]
docs = sys.argv[4:]

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
os.makedirs(scripts_dir, exist_ok=True)

# The manifest is MERGED, never rebuilt from scratch: a scaffold install (adopt/install-scaffold.sh)
# may already have pinned its checks here, and a fresh run must not drop those keys (the 2026-07-16
# defect — a from-scratch rebuild silently dropped a prior scaffold install's keys). Read whatever
# manifest exists, update only this installer's own entries, and leave every other prior entry —
# scaffold's pack-relative keys included — exactly as found.
#
# The filename stays scripts/ratchet-manifest.json through the 2026-09-02 rename of this installer.
# It is a source-pin record, not a ratchet, and every already-adopted host's update check reads it
# by that name: renaming it would break their update road to fix nothing.
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
manifest["tier"] = tier
manifest["gated_docs"] = list(docs)
# A prior install of the retired ratchet kit left its seeded counts here. They record a size, and
# nothing reads them any more; drop them so no later reader mistakes them for a live bound.
manifest.pop("seeded", None)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
print("wrote scripts/ratchet-manifest.json")
PYEOF

# --- step d: wire (repair, or recommend) the pre-push gate -----------------------------------------
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
  GATE_R_STATUS="$(python3 - "$PRE_PUSH" "$TIER" "${DOCS[@]}" << 'PYEOF'
import re
import sys

path, tier = sys.argv[1], sys.argv[2]
docs = sys.argv[3:]
MARKER = "# live-spec:gate-r"
LABEL_RE = re.compile(r"gate\s*r\W{0,3}(ratchet caps|style gate)", re.IGNORECASE)
FAIL_CHECK_RE = re.compile(r'^if\s*\[\s*"\$fail"\s*-ne\s*0\s*\]\s*;\s*then\b')
TOPLEVEL_EXIT_RE = re.compile(r'^exit\s+\d+\s*;?\s*(#.*)?$')

BLOCK_LINES = [
    "",
    MARKER,
    'echo ""',
    'echo "-- gate r — style gate --"',
    "for doc in %s; do" % " ".join(docs),
    '  if ! python3 scripts/spec-style-lint.py --tier %s "$doc"; then' % tier,
    "    fail=1",
    "  fi",
    "done",
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
        # A block installed by the retired ratchet kit runs a lock test this installer no longer
        # writes. It is replaced wherever it stands, live position or dead, so no host is left
        # pushing against a test file that is not there.
        stale = any("test_ratchet_lock" in lines[i] for i in range(start, end))
        dead = any(TOPLEVEL_EXIT_RE.match(lines[i]) for i in range(start))
        if not dead and not stale:
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
      echo "wired: guardrails/pre-push gate r — style gate"
      ;;
    already-wired)
      echo "already wired: guardrails/pre-push gate r — style gate"
      ;;
    repaired)
      echo "repaired: guardrails/pre-push gate r — style gate (was dead past a terminating exit, or ran the retired lock test; moved to a safe anchor)"
      ;;
    manual|*)
      echo "guardrails/pre-push has no safe wiring point (an unclear tail) — add this recipe by hand:"
      echo "  echo \"-- gate r — style gate --\""
      echo "  python3 scripts/spec-style-lint.py --tier $TIER <doc> || fail=1"
      ;;
  esac
else
  echo "no guardrails/pre-push found — add this recipe to your own push gate:"
  echo "  echo \"-- gate r — style gate --\""
  echo "  python3 scripts/spec-style-lint.py --tier $TIER <doc> || fail=1"
fi

# --- step d2: remove the retired ratchet's own leftover files ---------------------------------------
# Repairing the pre-push block above (step d) stops CALLING the retired lock test, but a host that
# ran the old ratchet kit before 2026-09-02 still HOLDS the generated test file and its seeded caps —
# both still collected by the host's own pytest, still enforcing the ceiling this kit no longer seeds.
# Deleting the generated test is safe: it is this installer's own past output, never hand-edited law.
# Stripping just the `max_redundancy_open` key from spec-debt-cap.json (not the whole file, which may
# carry other, unrelated fields) avoids the KeyError a host hits deleting the key by hand while the
# generated test still reads it (found in review, docs/prover/2026-09-02-q805-and-followups-review.md).
if [ -f "$HOST_ROOT/tests/test_ratchet_lock.py" ]; then
  rm -f "$HOST_ROOT/tests/test_ratchet_lock.py"
  echo "removed: tests/test_ratchet_lock.py (this installer's own past output, retired 2026-09-02)"
fi
if [ -f "$HOST_ROOT/scripts/spec-debt-cap.json" ]; then
  python3 - "$HOST_ROOT/scripts/spec-debt-cap.json" << 'PYEOF'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
if "max_redundancy_open" in data:
    del data["max_redundancy_open"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    print("stripped max_redundancy_open from scripts/spec-debt-cap.json")
PYEOF
fi

# --- step e: read the host's documents once, and say what stands -----------------------------------
# A reading, not a seed. Nothing is written down and nothing is held against these numbers; they are
# printed so the person adopting sees what the gate will say before their next push, and can clear a
# finding or waive it by name in scripts/spec-waivers.json.
for doc in "${DOCS[@]}"; do
  python3 "$HOST_ROOT/scripts/spec-style-lint.py" --tier "$TIER" "$HOST_ROOT/$doc" || true
  python3 "$HOST_ROOT/scripts/spec-redundancy-precheck.py" "$HOST_ROOT/$doc" || true
done

# --- step f: final summary -------------------------------------------------------------------------
python3 - "${#VENDOR_FILES[@]}" "$TIER" "${DOCS[@]}" << 'PYEOF'
import json, sys

vendored, tier = int(sys.argv[1]), sys.argv[2]
docs = sys.argv[3:]
print(json.dumps({
    "severity": "ok",
    "code": "style-gates-install",
    "docs": docs,
    "tier": tier,
    "vendored": vendored,
}))
PYEOF
