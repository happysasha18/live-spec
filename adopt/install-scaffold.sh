#!/usr/bin/env bash
# adopt/install-scaffold.sh — the turnkey scaffold-adoption kit (SPEC INV-97).
#
# Run from a HOST repo root. Vendors the pack's four project-side checks — completeness,
# tests-present, behaviour-traces-to-spec, conflicts — plus their shared library and README into the
# host tree, and seeds the host's guardrails config from the example (only when the host has none — a
# filled config is never clobbered). It writes or MERGES the ratchet manifest (scripts/ratchet-manifest.json):
# a source pin per vendored check (pack version + content hash) so the daily update check can tell a
# current copy from a stale one (SPEC INV-177). A host that already ran the ratchet installer keeps its
# ratchet entries untouched — the two installers share the one manifest.
#
# The manifest keys are the pack-relative source paths (scaffold/guardrails/<name>): the update watcher
# resolves each key against the pack checkout to read the current source and diff its hash, and the
# pack's own copy of these checks lives only under scaffold/guardrails/.
#
# Usage: adopt/install-scaffold.sh [--force]
#   --force    overwrite an already-vendored check file (default: skip an existing file and note it).
#              Never overwrites the host's own guardrails.config.json — that carries the host's paths.
set -euo pipefail

PACK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_ROOT="$(pwd)"

FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    *) echo "install-scaffold: unknown flag $1" >&2; exit 2 ;;
  esac
done

# --- step a: vendor the four checks + shared lib + README into the host's guardrails/ --------------
# Host layout follows the attach walk (scaffold/guardrails/README.md): the checks run from guardrails/,
# where the pre-push hook and config-health check expect them.
VENDOR_CODE=(
  "check_completeness.py"
  "check_tests_present.py"
  "check_traces_to_spec.py"
  "check_conflicts.py"
  "gate_lib.py"
)

for name in "${VENDOR_CODE[@]}" "README.md"; do
  src="$PACK_ROOT/scaffold/guardrails/$name"
  dest="$HOST_ROOT/guardrails/$name"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "skip (exists, use --force to overwrite): guardrails/$name"
  else
    cp "$src" "$dest"
    echo "vendored: guardrails/$name"
  fi
done

# --- step b: seed the host's guardrails config from the example (never clobber a filled one) --------
CONFIG_SEEDED=0
if [ -f "$HOST_ROOT/guardrails.config.json" ]; then
  echo "skip (exists, keep your paths): guardrails.config.json"
else
  cp "$PACK_ROOT/scaffold/guardrails/guardrails.config.example.json" "$HOST_ROOT/guardrails.config.json"
  echo "seeded: guardrails.config.json (fill your paths before the checks pass)"
  CONFIG_SEEDED=1
fi

# --- step c: write or MERGE the one manifest, pinning the vendored checks against the pack ----------
python3 - "$HOST_ROOT" "$PACK_ROOT" "${VENDOR_CODE[@]}" << 'PYEOF'
import hashlib
import json
import os
import sys

host_root, pack_root = sys.argv[1], sys.argv[2]
vendor_code = sys.argv[3:]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


pack_version = open(os.path.join(pack_root, "VERSION"), encoding="utf-8").read().strip()

scripts_dir = os.path.join(host_root, "scripts")
os.makedirs(scripts_dir, exist_ok=True)
manifest_path = os.path.join(scripts_dir, "ratchet-manifest.json")

# Merge into an existing manifest — a host that ran the ratchet installer keeps its ratchet entries.
manifest = {"pack_version": pack_version, "vendored": {}}
if os.path.isfile(manifest_path):
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {"pack_version": pack_version, "vendored": {}}
manifest["pack_version"] = pack_version
vendored = manifest.setdefault("vendored", {})

# Scaffold entries are ours to own: drop any prior scaffold-check key (either the pack-relative form we
# write, or the host-relative guardrails/<name> form the ratchet installer opportunistically pinned),
# then re-pin under the pack-relative source path so the watcher resolves it against the pack checkout.
# Ratchet's own kit basenames are disjoint from these, so no ratchet entry is ever touched.
for key in list(vendored):
    base = os.path.basename(key)
    d = os.path.dirname(key)
    if base in vendor_code and d in ("guardrails", "scaffold/guardrails"):
        del vendored[key]

for name in vendor_code:
    host_file = os.path.join(host_root, "guardrails", name)
    vendored["scaffold/guardrails/%s" % name] = sha256_of(host_file)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
print("wrote scripts/ratchet-manifest.json (%d scaffold checks pinned, pack %s)"
      % (len(vendor_code), pack_version))
PYEOF

# --- step d: the walk's remaining manual steps + final summary ------------------------------------
echo ""
echo "next — the attach walk's manual steps (scaffold/guardrails/README.md):"
if [ "$CONFIG_SEEDED" -eq 1 ]; then
  echo "  1. fill your paths in guardrails.config.json (spec, matrix, tests dir, user-facing globs, registry)"
fi
echo "  2. run each check once from the host root:"
echo "       python3 guardrails/check_completeness.py"
echo "       python3 guardrails/check_tests_present.py --base origin/main"
echo "       python3 guardrails/check_traces_to_spec.py"
echo "       python3 guardrails/check_conflicts.py"
echo "  3. prove one red-first: plant a fake registry row, watch check_completeness.py red, remove it"
echo "  4. add the four check lines to your pre-push hook (guardrails/README.md, step 5 — the copy just vendored)"

# --- step e: the adoption gate — the host's vendored worktree line (SPEC INV-201) ----------------
# Requirement 88 criterion 4 names a mechanical gate "read at the adoption/catch-up walk rather than
# wired into every push", and this walk is where it is read: this command is the adoption walk's own
# gate-installing step (adopt/ADOPT.md, "Installing the gates"), and the catch-up walk re-runs it
# with --force as the re-install road check-pack-update.sh names. So the gate reds HERE, once, at
# the walk — not on the host's every push, and never in this pack's own push chain, where
# criterion 3 leaves the pack's own line shut until the pack's owner gives the word.
#
# It runs last, after everything is vendored, so a red costs the host the line and not the install.
echo ""
echo "-- the adoption gate: the host's vendored worktree line (SPEC INV-201) --"
if ! "$PACK_ROOT/guardrails/check-worktree-line.sh" "$HOST_ROOT"; then
  echo ""
  echo "adoption gate red: the scaffold is vendored, but this host's project instructions carry no"
  echo "  worktree line. Vendor one line into CLAUDE.md that CITES the isolation law's write-set"
  echo "  condition (INV-105) rather than restating it, then run this installer again."
  exit 1
fi

python3 - "${#VENDOR_CODE[@]}" "$CONFIG_SEEDED" << 'PYEOF'
import json, sys
print(json.dumps({
    "severity": "ok",
    "code": "scaffold-install",
    "checks_vendored": int(sys.argv[1]),
    "config_seeded": bool(int(sys.argv[2])),
}))
PYEOF
