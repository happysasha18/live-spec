#!/bin/bash
# check-pack-update.sh — once a day, ask the public repo whether the pack moved past this machine (SPEC E-25).
# PROPOSES only — never installs (the human's gate, ACT-1). Offline or unreadable remote = one honest
# skip line naming the address, exit 0, stamp left unwritten so the next session retries.
# Forward only: a machine ahead of the public repo reads as up to date, never a downgrade proposal.
# Test/override flags: --remote-file <path> (bypass network) · --installed-file <path> · --stamp-file <path> · --force (ignore today's stamp)
set -u

REMOTE_URL="https://raw.githubusercontent.com/happysasha18/live-spec/main/VERSION"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALLED_FILE="$ROOT/VERSION"
STAMP_FILE="$HOME/.claude/live-spec/update-check-stamp"
REMOTE_FILE=""
FORCE=0
MANIFEST=""
PACK_ROOT=
FOUNDING_MANIFEST=""
HOST_PROFILE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --remote-file)    REMOTE_FILE="$2";    shift 2 ;;
    --installed-file) INSTALLED_FILE="$2"; shift 2 ;;
    --stamp-file)     STAMP_FILE="$2";     shift 2 ;;
    --force)          FORCE=1;             shift ;;
    --manifest)       MANIFEST="$2";       shift 2 ;;
    --pack-root)      PACK_ROOT="$2";      shift 2 ;;
    --founding-manifest) FOUNDING_MANIFEST="$2"; shift 2 ;;
    --host-profile)   HOST_PROFILE="$2";   shift 2 ;;
    *) echo "check-pack-update: unknown flag $1" >&2; exit 2 ;;
  esac
done

today="$(date +%Y-%m-%d)"
if [ "$FORCE" -eq 0 ] && [ -f "$STAMP_FILE" ] && [ "$(cat "$STAMP_FILE" 2>/dev/null)" = "$today" ]; then
  echo "pack update check: already ran today ($today) — skipped"
  exit 0
fi

if [ -n "$REMOTE_FILE" ]; then
  src="$REMOTE_FILE"
  remote="$(cat "$REMOTE_FILE" 2>/dev/null)"
else
  src="$REMOTE_URL"
  # --max-time bounds one network read of a VERSION file; a slow or dead remote falls through to the
  # "skipped — offline or unreachable" road below and never blocks. Machinery tuning, kept and marked
  # under the owner-ruled class (docs/audits/2026-08-07-number-rulings.md §3, which names this file).
  # No incident or source behind the 10; it is an ordinary engineering default for a one-line fetch.
  remote="$(curl -fsS --max-time 10 "$REMOTE_URL" 2>/dev/null)"
fi

if ! printf '%s' "$remote" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "pack update check: skipped — offline or unreadable remote ($src)"
  exit 0
fi

installed="$(cat "$INSTALLED_FILE" 2>/dev/null)"
if ! printf '%s' "$installed" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "pack update check: skipped — no readable installed version at $INSTALLED_FILE"
  exit 0
fi

mkdir -p "$(dirname "$STAMP_FILE")" && printf '%s' "$today" > "$STAMP_FILE"

check_manifest() {
  # Vendored-copy staleness (SPEC INV-177): runs on EVERY check, not only when the pack itself moved —
  # the standing state is a current pack and a lagging host, and a watcher silent exactly there would
  # re-open the hole it was built to close (batch audit 2026-07-16, F1). The pin compares against the
  # LOCAL pack VERSION: the newest truth this machine can act on.
  local pack_now="$1"
  [ -z "$MANIFEST" ] && [ -f "scripts/ratchet-manifest.json" ] && MANIFEST="scripts/ratchet-manifest.json"
  [ -z "$PACK_ROOT" ] && PACK_ROOT="$ROOT"
  if [ -n "$MANIFEST" ] && [ -f "$MANIFEST" ]; then
    python3 - "$MANIFEST" "$PACK_ROOT" "$pack_now" <<'PYEOF'
import hashlib, json, os, sys
manifest_path, pack_root, pack_now = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    man = json.load(open(manifest_path))
except (OSError, ValueError):
    sys.exit(0)
def _v(t):
    try:
        return tuple(int(x) for x in t.split("."))
    except ValueError:
        return ()
pinned = str(man.get("pack_version", ""))
if pinned and _v(pinned) and _v(pack_now) and _v(pinned) < _v(pack_now):
    stale = []
    for rel, sha in (man.get("vendored") or {}).items():
        src = os.path.join(pack_root, rel)
        if os.path.isfile(src):
            cur = hashlib.sha256(open(src, "rb").read()).hexdigest()
            if cur != sha:
                stale.append(rel)
    print("  VENDORED GATES PINNED TO %s — the pack moved past the pin (now %s):" % (pinned, pack_now))
    for rel in stale:
        print("    stale vs current pack: %s" % rel)
    if not stale:
        print("    (no vendored file differs from the local pack copy — the pin alone is old)")
    # Name the road per stale kit (2026-07-16 fix): a scaffold-only host was pointed at the
    # style-gate installer, which doesn't touch scaffold/guardrails/ at all. Manifest keys tell the kits apart —
    # install-scaffold.sh always pins under the pack-relative scaffold/guardrails/<name> prefix;
    # install-style-gates.sh's own vendor set never uses that prefix.
    scaffold_stale = [rel for rel in stale if rel.startswith("scaffold/guardrails/")]
    style_gate_stale = [rel for rel in stale if not rel.startswith("scaffold/guardrails/")]
    if scaffold_stale:
        print("  re-install road: bash <pack>/adopt/install-scaffold.sh --force  (re-vendoring the scaffold checks)")
    if style_gate_stale or not stale:
        print("  re-install road: bash <pack>/adopt/install-style-gates.sh --force  (a re-vendor is explicit, never silent)")
PYEOF
  fi
}

check_founding_questions() {
  # The founding-question arm (SPEC INV-227): the founding-question set is versioned, a host records
  # which set version it answered on a `founding.set-version` profile line, and this arm names each
  # founding question the host has never answered — beside the vendored files the manifest arm names.
  # Runs on EVERY check, like the manifest arm: the standing state is a grown set and a host founded
  # before it. A never-answered question is SURFACED for the owner to answer at catch-up, never
  # answered here (proposal only, the duty binds forward, INV-159).
  [ -z "$FOUNDING_MANIFEST" ] && [ -f "$ROOT/scripts/founding-questions.json" ] && FOUNDING_MANIFEST="$ROOT/scripts/founding-questions.json"
  [ -z "$HOST_PROFILE" ] && HOST_PROFILE="$ROOT/.live-spec/profile.md"
  if [ -n "$FOUNDING_MANIFEST" ] && [ -f "$FOUNDING_MANIFEST" ]; then
    python3 - "$FOUNDING_MANIFEST" "$HOST_PROFILE" <<'PYEOF'
import json, os, re, sys
man_path, profile_path = sys.argv[1], sys.argv[2]
try:
    man = json.load(open(man_path))
except (OSError, ValueError):
    sys.exit(0)
current = man.get("set_version")
if not isinstance(current, int):
    sys.exit(0)
answered = None
if profile_path and os.path.isfile(profile_path):
    txt = open(profile_path, encoding="utf-8", errors="replace").read()
    m = re.search(r"founding\.set-version:\s*(\d+)", txt)
    if m:
        answered = int(m.group(1))
# A host with no readable founding.set-version founded before the set was versioned, so every
# question is potentially owed: base at -1 names them all (the versionless-record rule, INV-91 kin).
base = answered if answered is not None else -1
newer = [q for q in (man.get("questions") or []) if isinstance(q.get("since"), int) and q["since"] > base]
if newer:
    if answered is None:
        print("  FOUNDING QUESTIONS — this host records no founding.set-version (founded before the set was versioned):")
    else:
        print("  FOUNDING QUESTIONS NEWER THAN THIS HOST'S SET (answered version %d, current %d):" % (answered, current))
    for q in newer:
        print("    never answered: %s  [%s, records %s]" % (q.get("question", ""), q.get("anchor", ""), q.get("key", "")))
    print("  PROPOSAL ONLY — a never-answered founding question is surfaced for the owner at catch-up; nothing is answered here.")
PYEOF
  fi
}

newest="$(printf '%s\n%s\n' "$installed" "$remote" | sort -V | tail -1)"
if [ "$remote" = "$installed" ] || [ "$newest" = "$installed" ]; then
  echo "pack update check: up to date ($installed)"
  arm_out="$(check_manifest "$installed")"
  founding_out="$(check_founding_questions)"
  if [ -n "$arm_out" ] || [ -n "$founding_out" ]; then
    [ -n "$arm_out" ] && printf '%s\n' "$arm_out"
    [ -n "$founding_out" ] && printf '%s\n' "$founding_out"
    echo "  PROPOSAL ONLY — nothing installed; updating is the human's word."
  fi
  exit 0
fi

echo "PACK UPDATE AVAILABLE: $remote (this machine runs $installed)"
echo "  what changed: https://github.com/happysasha18/live-spec/blob/main/JOURNAL.md"
echo "  update road: install.sh (attic-backed) — or a plain 'git pull' where the repo itself runs the pack"

check_manifest "$installed"
check_founding_questions

echo "  PROPOSAL ONLY — nothing installed; updating is the human's word."
exit 0
