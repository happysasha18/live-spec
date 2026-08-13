#!/usr/bin/env bash
# check-config-health.sh — the installed gate is the source gate (SPEC INV-175).
#
# A gate lives twice: its source in guardrails/ travels with the repo; its installed copy in
# .git/hooks/ actually runs. They drift the moment an install is skipped — the worked instance
# (2026-07-16): the installed pre-push was missing gates k and l that the source carried.
# This check reds when an expected hook is missing from .git/hooks/ or differs byte-for-byte
# from its guardrails/ source, and names the one fix. A checkout with no installed hooks by
# design (CI) skips by name. Runs inside the suite, so even a stale pre-push that still runs
# the tests surfaces the drift — the self-healing shape.

set -euo pipefail

if [ "${GITHUB_ACTIONS:-}" = "true" ] || [ "${CI:-}" = "true" ]; then
  echo "config-health: skip (CI checkout installs no local hooks by design)"
  exit 0
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$(git -C "$REPO_ROOT" rev-parse --git-path hooks)"
case "$HOOKS_DIR" in
  /*) : ;;
  *) HOOKS_DIR="$REPO_ROOT/$HOOKS_DIR" ;;
esac

fail=0
for name in pre-commit pre-push; do
  src="$REPO_ROOT/guardrails/$name"
  [ -f "$src" ] || continue
  inst="$HOOKS_DIR/$name"
  if [ ! -f "$inst" ]; then
    echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed hook missing: .git/hooks/$name\",\"fix\":\"run guardrails/install.sh\"}"
    fail=1
  elif ! cmp -s "$src" "$inst"; then
    echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed hook drifted from source: $name\",\"fix\":\"run guardrails/install.sh\"}"
    fail=1
  fi
done

# INV-173 x INV-175 (batch audit 2026-07-16, F3; inverted ROADMAP 417): the pack's session hooks are
# gates living twice too. Rather than a hardcoded basename list — which goes blind to every hook added
# after it was written (it was blind to hook-meter.py and the register-judge arms installed 2026-07-17)
# — DIFF the whole hook SOURCE directory (hooks/) against the installed set. Every file in hooks/ is
# covered automatically: when an installed copy exists it must match its source byte-for-byte; when a
# source hook has NO installed copy that is drift and it reds (source exists, install missing = the
# config is unhealthy, and a missing installed judge goes dark while every other gate stays green —
# corrected 2026-07-17, the earlier form skipped a missing install green). A file living only in the
# installed set (a personal-layer overlay the pack never ships) has no source here and is correctly left
# alone. RESIDUAL for row 420's gate audit: this arm proves the installed FILE exists and matches; it
# does not yet prove settings.json still LISTS the Stop/UserPromptSubmit judge entries — that check is
# harder because settings.json is personal-layer, and it is left for the row 420 gate audit.
HOOK_SRC_DIR="$REPO_ROOT/hooks"
if [ -d "$HOOK_SRC_DIR" ]; then
  for src_hook in "$HOOK_SRC_DIR"/*; do
    [ -f "$src_hook" ] || continue
    hname="$(basename "$src_hook")"
    inst_hook="$HOME/.claude/hooks/$hname"
    if [ ! -f "$inst_hook" ]; then
      echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed hook missing: ~/.claude/hooks/$hname (source exists, install missing)\",\"fix\":\"run scripts/install-pack-hooks.sh or scripts/install-session-hooks.sh\"}"
      fail=1
    elif ! cmp -s "$src_hook" "$inst_hook"; then
      # A machine may deliberately run a changed copy of a hook — a check switched off for a stated
      # span while the documents it reads are rewritten, say. The repository stays the version
      # everyone gets, and the difference is declared as DATA in guardrails/local-overrides.json
      # rather than by editing this script. An entry pins the fingerprint of the installed file it
      # covers, so it buys silence for exactly that copy: change the installed file again and the
      # entry stops matching and this arm reds. An undeclared difference still reds (2026-08-04).
      inst_sha="$(shasum -a 256 "$inst_hook" | awk '{print $1}')"
      if [ -f "$REPO_ROOT/guardrails/local-overrides.json" ] && python3 - "$REPO_ROOT/guardrails/local-overrides.json" "$hname" "$inst_sha" <<'PYCHECK'
import json, sys
path, hook, sha = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    entries = json.load(open(path, encoding="utf-8")).get("hook_overrides", [])
except Exception:
    sys.exit(1)
for e in entries:
    if e.get("hook") == hook and e.get("installed_sha256") == sha and e.get("reason"):
        sys.exit(0)
sys.exit(1)
PYCHECK
      then
        echo "config-health: declared local override, installed hook differs from source by design: $hname (guardrails/local-overrides.json)"
      else
        echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed hook drifted from source: $hname\",\"fix\":\"run scripts/install-pack-hooks.sh or scripts/install-session-hooks.sh, or declare the difference in guardrails/local-overrides.json with its reason and the installed file's fingerprint\"}"
        fail=1
      fi
    fi
  done
fi

# INV-243: a skill is a gate living twice too — source in skills/ travels with the repo, the
# installed copy under ~/.claude/skills/<name> is what a pack skill actually loads from. Same
# shape as the session-hook directory-diff arm above, but the unit is a whole DIRECTORY TREE (a
# skill carries SKILL.md plus references/, scripts/...), so the compare is a recursive tree diff
# rather than a single-file cmp. A WHOLE skill installed under ~/.claude/skills with no pack source
# (a personal-layer skill the pack never ships) is never iterated here and is correctly left alone —
# the same TOP-LEVEL asymmetry the hook arm holds. A shipped skill's installed copy is held
# byte-pristine, though: because the compare is a recursive tree diff, an extra file dropped INSIDE a
# shipped skill's directory counts as drift and reds. That is stricter than the hook arm's flat-file
# tolerance, and intended — a shipped skill should match its source tree exactly.
SKILL_SRC_DIR="$REPO_ROOT/skills"
if [ -d "$SKILL_SRC_DIR" ]; then
  for src_skill in "$SKILL_SRC_DIR"/*/; do
    [ -d "$src_skill" ] || continue
    sname="$(basename "$src_skill")"
    # External-skill fence (shared policy; siblings: install.sh, scripts/sync-skills.sh,
    # scripts/sync-mirrors.sh): a skill dir holding its own .git is the external canonical clone —
    # scripts/install-external-skills.sh owns its installed copy, not the sync; INV-243 holds
    # pack-owned skills only.
    if [ -e "$src_skill/.git" ]; then
      continue
    fi
    inst_skill="$HOME/.claude/skills/$sname"
    if [ ! -d "$inst_skill" ]; then
      echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed skill missing: ~/.claude/skills/$sname (source exists, install missing)\",\"fix\":\"run scripts/sync-skills.sh\"}"
      fail=1
    elif ! diff -rq "$src_skill" "$inst_skill" >/dev/null 2>&1; then
      echo "{\"severity\":\"error\",\"code\":\"config-health\",\"message\":\"installed skill drifted from source: $sname\",\"fix\":\"run scripts/sync-skills.sh\"}"
      fail=1
    fi
  done
fi

# INV-216: a permission rule that points at nothing is a dead rule. This arm reads every permission
# rule that names a filesystem path in the personal ~/.claude/settings.json and the host's project
# settings and reds a rule whose path is absent — the ~/tlvphoto→~/tlvphotos rename (2026-07-10) sat
# a week failing silently into prompts. Personal-layer: it stands down by name where the settings
# cannot be read and never falsely passes. Rides gate m's existing CI carve-out (a CI checkout skips
# this whole script) and gate m's red proof; it adds no gate letter.
PERMS="$(dirname "${BASH_SOURCE[0]}")/check-config-health-perms.py"
if [ -f "$PERMS" ]; then
  if ! python3 "$PERMS"; then
    fail=1
  fi
fi

if [ "$fail" -eq 0 ]; then
  echo "config-health: OK (installed hooks match their sources)"
fi
exit "$fail"
