#!/bin/sh
# Installs every session hook guardrails/judge-hooks.json declares "wired" (ROADMAP row 506).
#
# Before this fix this script only ever installed two of the ten (clock-hook.sh, chat-law-hook.sh —
# rows 134/141); the other eight (the register judge's two arms, the four literal Stop scans, and the
# mid-turn PreToolUse scan) reached a real machine only by a human copying them and editing
# settings.json by hand over several weeks. That left the shipped setup a fifth of the machinery the
# declaration itself already named ten of, with no signal a fresh machine — or any host adopting the
# pack — was short seven of them (found 2026-07-27 verifying row 495's setup-walk leg).
#
# The fix: this script now GENERATES its own two hooks' installation from guardrails/judge-hooks.json
# (command form + data files, so the declaration stays the one home for what is wired — never a second
# hand-kept list here), then CHAINS to scripts/install-pack-hooks.sh for the other eight. That script
# already carries its own tests pinned to its literal source (tests/test_register_judge.py,
# tests/test_hedge_arm.py, tests/test_affirmation_arm.py,
# tests/test_midturn_chat_scan.py), so it is chained rather than rewritten — the ONE command below
# still reaches all ten.
#
# Run BY THE HUMAN (`sh ~/live-spec/scripts/install-session-hooks.sh`) — the harness classifier blocks
# an agent's own hand in its configuration, deliberately. Idempotent: re-running changes nothing and
# says so — a hook already wired in ANY form (including wrapped in a host's own personal
# ~/.claude/hooks/hook-meter.py counter) is recognized by its filename appearing in the existing
# command and is left exactly as it stands, never duplicated or rewritten to the plain form below. A
# personal overlay file (a `*-personal.json`/`*-personal.md` a hook reads when present) is never
# created, edited, or overwritten by either script — this script only reports the ones it finds.
#
# Repo home: scripts/install-session-hooks.sh.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_SRC="$ROOT/hooks"
DECL="$ROOT/guardrails/judge-hooks.json"
DEST_DIR="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"

mkdir -p "$DEST_DIR"

# This script's own two hooks (rows 134/141), generated from the declaration.
python3 - "$DECL" "$HOOKS_SRC" "$DEST_DIR" "$SETTINGS" << 'PYEOF'
import json, os, sys

decl_path, hooks_src, dest_dir, settings_path = sys.argv[1:5]
with open(decl_path, encoding="utf-8") as f:
    decl = json.load(f)

OWN = ["clock-hook", "chat-law-hook"]  # this script's own two; the other eight chain to install-pack-hooks.sh


def _same(a, b):
    return os.path.isfile(b) and open(a, encoding="utf-8").read() == open(b, encoding="utf-8").read()


def _install(src, dst, exe=False):
    if _same(src, dst):
        print("already present: %s" % dst)
        return
    with open(src, encoding="utf-8") as sf:
        body = sf.read()
    with open(dst, "w", encoding="utf-8") as df:
        df.write(body)
    if exe:
        os.chmod(dst, 0o755)
    print("installed: %s" % dst)


for stem in OWN:
    fname = decl["file"][stem]
    _install(os.path.join(hooks_src, fname), os.path.join(dest_dir, fname), exe=True)
    for df_name in decl["data"].get(stem, []):
        _install(os.path.join(hooks_src, df_name), os.path.join(dest_dir, df_name))

s = json.load(open(settings_path)) if os.path.exists(settings_path) else {}
hooks = s.setdefault("hooks", {})
for stem in OWN:
    event = decl["wired"][stem]
    fname = decl["file"][stem]
    cmd = decl["command"][stem]
    arr = hooks.setdefault(event, [])
    have = [hk.get("command", "") for e in arr for hk in e.get("hooks", [])]
    if any(fname in c for c in have):
        print("already wired: %s hook %s" % (event, fname))
    else:
        arr.append({"hooks": [{"type": "command", "command": cmd}]})
        print("wired: %s hook %s" % (event, fname))

os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
PYEOF

# The other eight already have their own installer — chained here rather than duplicated.
sh "$ROOT/scripts/install-pack-hooks.sh"

# Coverage summary + personal-overlay report, read back from settings.json + the declaration so
# neither list is hand-kept a second time.
python3 - "$DECL" "$DEST_DIR" "$SETTINGS" << 'PYEOF'
import json, os, sys

decl_path, dest_dir, settings_path = sys.argv[1:4]
with open(decl_path, encoding="utf-8") as f:
    decl = json.load(f)

s = json.load(open(settings_path)) if os.path.exists(settings_path) else {}
hooks = s.get("hooks", {})


def commands_for(event):
    out = []
    for group in hooks.get(event, []):
        for h in group.get("hooks", []):
            c = h.get("command", "")
            if c:
                out.append(c)
    return out


missing = []
for stem, event in sorted(decl["wired"].items()):
    fname = decl["file"][stem]
    if not any(fname in c for c in commands_for(event)):
        missing.append(stem)

total = len(decl["wired"])
covered = total - len(missing)
print("session hooks: %d/%d of the pack's declared wired hooks are live in %s" % (covered, total, settings_path))
if missing:
    print("session hooks: STILL MISSING: %s" % ", ".join(missing))

overlays_found = []
for stem, names in decl.get("personal_overlay", {}).items():
    for name in names:
        p = os.path.join(dest_dir, name)
        if os.path.isfile(p):
            overlays_found.append(name)
if overlays_found:
    print("session hooks: personal overlay(s) present and left untouched: %s" % ", ".join(sorted(set(overlays_found))))

hook_meter = os.path.join(dest_dir, "hook-meter.py")
if os.path.isfile(hook_meter):
    print("session hooks: hook-meter.py present (the personal layer's own counter wrapper, never "
          "shipped or installed by the pack) — left untouched; any hook this host already wraps in "
          "it stays wrapped, since a hook already wired in any form is left exactly as it stands.")
PYEOF

echo "Installed. Every window's next prompt and turn carry the pack's declared session hooks."
