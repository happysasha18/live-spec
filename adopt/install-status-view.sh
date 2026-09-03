#!/usr/bin/env bash
# adopt/install-status-view.sh — the turnkey status-view adoption kit.
#
# Run from a HOST repo root. Vendors the plan reader (probe · board · one-row reader) and its shared
# core into the host's scripts/, seeds the host's own acceptance-command file where it has none (a
# filled one is never clobbered), and pins each vendored copy's source in scripts/ratchet-manifest.json
# so the daily update check can tell a current copy from a stale one.
#
# WHAT THE HOST GETS, and what it does not. It gets the three readers and the parser: `state-probe.sh`
# prints where the project stands at the start of a session, `render-board.sh` draws the same state as
# a page, `plan-step.sh` prints one row on its own, and `plan_checks_core.py` is the one home for how a
# plan is parsed, how a mark is spelled and how a row's state is computed from the command that proves
# it. It does NOT get one command of this pack's own: those name this pack's files and belong to it
# alone. The host's `scripts/plan_checks.py` arrives with an empty map and is the host's to fill, row
# by row, exactly the way the pack filled its own.
#
# The manifest keys are the pack-relative source paths, so the update watcher resolves each key against
# the pack checkout to read the current source and diff its hash. The host's own `plan_checks.py` is
# deliberately NOT pinned: it is the host's content from the first minute, like guardrails.config.json.
#
# Usage: adopt/install-status-view.sh [--force]
#   --force    overwrite an already-vendored reader (default: skip an existing file and note it).
#              Never overwrites the host's own scripts/plan_checks.py — that carries the host's commands.
set -euo pipefail

PACK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_ROOT="$(pwd)"

FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    *) echo "install-status-view: unknown flag $1" >&2; exit 2 ;;
  esac
done

# --- step a: vendor the readers + the shared parser into the host's scripts/ ----------------------
# Each entry is "<pack-relative source>|<host-relative destination>". The two readers the pack runs
# on itself travel from the pack's own scripts/ — they are already project-generic and there is one
# copy of each, so a fix reaches every host. The probe has a host copy of its own under
# scaffold/status-view/: the pack's own probe also measures things only the pack has.
VENDOR=(
  "scaffold/status-view/state-probe.sh|scripts/state-probe.sh"
  "scripts/render-board.sh|scripts/render-board.sh"
  "scripts/plan-step.sh|scripts/plan-step.sh"
  "scripts/plan_checks_core.py|scripts/plan_checks_core.py"
)

for pair in "${VENDOR[@]}"; do
  src="$PACK_ROOT/${pair%%|*}"
  rel="${pair##*|}"
  dest="$HOST_ROOT/$rel"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "skip (exists, use --force to overwrite): $rel"
  else
    cp "$src" "$dest"
    chmod +x "$dest" 2>/dev/null || true
    echo "vendored: $rel"
  fi
done

# --- step b: seed the host's own acceptance commands (never clobber a filled one) ------------------
# Same rule install-scaffold.sh gives guardrails.config.json: the file carries the host's own content
# from the moment it is edited, so a re-run — including a --force re-run of the readers above — leaves
# it exactly as found. A host that loses this file loses every command it ever wrote.
CHECKS_SEEDED=0
if [ -f "$HOST_ROOT/scripts/plan_checks.py" ]; then
  echo "skip (exists, keep your commands): scripts/plan_checks.py"
else
  cp "$PACK_ROOT/scaffold/status-view/plan_checks.py" "$HOST_ROOT/scripts/plan_checks.py"
  echo "seeded: scripts/plan_checks.py (an empty command map — every row reads DECLARED until you fill it)"
  CHECKS_SEEDED=1
fi

# --- step c: write or MERGE the one manifest, pinning the vendored readers against the pack --------
python3 - "$HOST_ROOT" "$PACK_ROOT" "${VENDOR[@]}" << 'PYEOF'
import hashlib
import json
import os
import sys

host_root, pack_root = sys.argv[1], sys.argv[2]
pairs = [p.split("|", 1) for p in sys.argv[3:]]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


pack_version = open(os.path.join(pack_root, "VERSION"), encoding="utf-8").read().strip()

scripts_dir = os.path.join(host_root, "scripts")
os.makedirs(scripts_dir, exist_ok=True)
manifest_path = os.path.join(scripts_dir, "ratchet-manifest.json")

# MERGED, never rebuilt: a host that ran the scaffold or style-gate installer keeps every key those
# wrote. Only this kit's own entries are touched.
manifest = {"pack_version": pack_version, "vendored": {}}
if os.path.isfile(manifest_path):
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {"pack_version": pack_version, "vendored": {}}
manifest["pack_version"] = pack_version
vendored = manifest.setdefault("vendored", {})

for src_rel, host_rel in pairs:
    vendored[src_rel] = sha256_of(os.path.join(host_root, host_rel))

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
print("wrote scripts/ratchet-manifest.json (%d status-view files pinned, pack %s)"
      % (len(pairs), pack_version))
PYEOF

# --- step d: read this host's plan once, and say what stands --------------------------------------
# A reading, not a seed. Nothing is written down: the person adopting sees what the probe will say
# before their next session, and a plan the reader cannot see says so here rather than at their desk.
echo ""
echo "-- your plan, as the probe now reads it --"
bash "$HOST_ROOT/scripts/state-probe.sh" || true

# --- step e: the remaining manual steps ------------------------------------------------------------
echo ""
echo "next — by hand:"
echo "  1. run it as your session's first act:  bash scripts/state-probe.sh"
if [ "$CHECKS_SEEDED" -eq 1 ]; then
  echo "  2. add your own commands to scripts/plan_checks.py's CHECKS map as your rows earn them —"
  echo "     one entry per row id, each reading what that row actually promised (a grep, a test, one"
  echo "     fast script), never just that a file exists. Until a row has one it prints DECLARED,"
  echo "     which is the honest state and not a gap."
else
  echo "  2. your scripts/plan_checks.py was left as found — its commands are yours"
fi
echo "  3. prove one red-first: point a row's command at something untrue, watch its mark flip to 🔁"
echo "     in the probe, then put it back"
echo "  4. draw the page once:  bash scripts/render-board.sh   (writes board.html)"
echo "  5. name scripts/state-probe.sh as the session's first action in your CLAUDE.md"

python3 - "${#VENDOR[@]}" "$CHECKS_SEEDED" << 'PYEOF'
import json, sys
print(json.dumps({
    "severity": "ok",
    "code": "status-view-install",
    "files_vendored": int(sys.argv[1]),
    "checks_seeded": bool(int(sys.argv[2])),
}))
PYEOF
