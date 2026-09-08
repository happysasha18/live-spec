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

# The four-mode contract's own runtime (row q-826, 2026-09-07 22:00): the run-mode reader, the
# repo-local spawn guard, the push-time acceptance re-run (owned by another worker right now —
# vendored by path, never opened here), and the minimal runtime admission the four modes rest on.
# These five live outside scaffold/guardrails/, so they get their own "<pack-rel>|<host-rel>"
# pairs, the same shape adopt/install-status-view.sh already uses for files whose pack source and
# host destination differ.
VENDOR_MODES=(
  "guardrails/run_modes.py|guardrails/run_modes.py"
  "guardrails/check-acceptance-rerun.py|guardrails/check-acceptance-rerun.py"
  "guardrails/worker-admission-guard.py|guardrails/worker-admission-guard.py"
  "scripts/task-admission.py|scripts/task-admission.py"
  "scripts/checkpoint.py|scripts/checkpoint.py"
)

for pair in "${VENDOR_MODES[@]}"; do
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
# The run-mode contract's own files (VENDOR_MODES above) are pinned in this same pass, by their own
# pack-relative source path — the generic shape guardrails/check-status-view-drift.py and
# scripts/check-pack-update.sh already read. One manifest write keeps key order stable across reruns;
# a second, later write of the same file would re-append the scaffold keys the loop below deletes and
# re-inserts every run, moving them after whatever this pass wrote and breaking the idempotent-rerun
# byte-equality the sibling installer already proves.
python3 - "$HOST_ROOT" "$PACK_ROOT" "${#VENDOR_CODE[@]}" "${VENDOR_CODE[@]}" "${VENDOR_MODES[@]}" << 'PYEOF'
import hashlib
import json
import os
import sys

host_root, pack_root, n_code = sys.argv[1], sys.argv[2], int(sys.argv[3])
rest = sys.argv[4:]
vendor_code = rest[:n_code]
vendor_modes_pairs = [p.split("|", 1) for p in rest[n_code:]]


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

# Pinned first, so a rerun's key order is stable: an existing key just gets its value refreshed in
# place, at the position it already holds. The scaffold loop below deletes-then-reinserts its own
# keys on every run (to dedupe a stale host-relative pin), which would otherwise reorder these keys
# behind it every single rerun if they were pinned after.
for src_rel, host_rel in vendor_modes_pairs:
    vendored[src_rel] = sha256_of(os.path.join(host_root, host_rel))

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
print("wrote scripts/ratchet-manifest.json (%d scaffold checks + %d run-mode files pinned, pack %s)"
      % (len(vendor_code), len(vendor_modes_pairs), pack_version))
PYEOF

# The four-mode contract's names, seeded into the host's own guardrails.config.json only when the
# host carries no "run_modes" key of its own. The host owns every budget under it — max_targets,
# the release core list, the layer map, timeouts — this seeds only the mechanism: the four names and
# whether a mode decides a verdict. A host's own tuning, once written, is never touched again.
#
# Gated on CONFIG_SEEDED (step b just created this file from the example, which carries no
# run_modes key of its own): a host's PRE-EXISTING config is never opened here, the same
# never-clobber promise step b already gives the whole file — the run_modes key rides that file's
# own seed rather than becoming a second, independent way this installer can touch a filled config.
if [ "$CONFIG_SEEDED" -eq 1 ]; then
  python3 - "$HOST_ROOT/guardrails.config.json" << 'PYEOF'
import json
import sys

cfg_path = sys.argv[1]
with open(cfg_path, encoding="utf-8") as f:
    cfg = json.load(f)

if "run_modes" in cfg:
    print("skip (exists, keep your tuning): guardrails.config.json run_modes")
else:
    cfg["run_modes"] = {
        # max_targets rides the seed because it is the PACK's law rather than a host's budget
        # (Requirement 322 criteria 2 and 3): a row run covers one target, an integration run at
        # most five. guardrails/run_modes.py carries the same two figures as its floor, so a host
        # that edits these keys away still gets them; seeding them keeps the host's own config
        # honest about what it is running under.
        "row": {"max_targets": 1, "decides_verdict": True, "emergency_timeout_seconds": None,
                "timeout_is_never_a_verdict": True},
        "integration": {"max_targets": 5, "decides_verdict": True,
                         "emergency_timeout_seconds": None,
                         "timeout_is_never_a_verdict": True, "layer_map": {}},
        "release": {"decides_verdict": True, "emergency_timeout_seconds": None,
                     "timeout_is_never_a_verdict": True},
        "manual": {"in_ci": False, "decides_verdict": False, "emergency_timeout_seconds": None,
                   "timeout_is_never_a_verdict": True},
    }
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    print("seeded: guardrails.config.json run_modes (the four names; fill your budgets, "
          "release core and layer map)")
PYEOF
else
  echo "skip (guardrails.config.json pre-dates this install, keep your tuning): run_modes"
fi

# The repo-local spawn guard's own wiring: a PreToolUse hook on Task|Agent in the HOST's own
# .claude/settings.json, beside the tree it guards — never under the user's home, no global hook.
# A host that already carries the hook (its own, or from an earlier install) is left alone.
mkdir -p "$HOST_ROOT/.claude"
python3 - "$HOST_ROOT/.claude/settings.json" << 'PYEOF'
import json
import os
import sys

path = sys.argv[1]
HOOK_CMD = 'python3 "$CLAUDE_PROJECT_DIR/guardrails/worker-admission-guard.py"'

settings = {}
if os.path.isfile(path):
    try:
        settings = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        settings = {}

pre_tool_use = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
already = any(
    "worker-admission-guard.py" in (h.get("command") or "")
    for group in pre_tool_use
    for h in group.get("hooks", [])
)
if already:
    print("skip (exists, keep your host's hook): .claude/settings.json PreToolUse "
          "worker-admission-guard")
else:
    pre_tool_use.append({
        "matcher": "Task|Agent",
        "hooks": [{"type": "command", "command": HOOK_CMD}],
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    print("wired: .claude/settings.json PreToolUse Task|Agent -> "
          "guardrails/worker-admission-guard.py")
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
