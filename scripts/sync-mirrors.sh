#!/usr/bin/env bash
# sync-mirrors.sh
#
# What this does, in plain English:
#
# The live-spec pack (this repo) is the single source of truth for every skill
# under skills/<name>/. Some of those skills ALSO exist as their own separate
# public GitHub repos (e.g. happysasha18/product-prover), kept around so people
# who only want one skill don't have to clone the whole pack. Those standalone
# repos are READ-ONLY MIRRORS — nobody should edit them directly, and this
# script is the one thing that updates them.
#
# For every skill folder in skills/:
#   1. Look for a GitHub repo named happysasha18/<skill-name>.
#      - If it doesn't exist, we do NOT create one (that's a deliberate,
#        separate decision the project owner makes) — we just print that we
#        skipped it and move on.
#   2. If it exists, clone it into a scratch directory, replace its contents
#      with the current skills/<skill-name>/ folder from the pack (keeping the
#      mirror's own .git history), make sure its README.md opens with a banner
#      explaining it's a read-only mirror, stamp the "made with live-spec" line
#      (current pack version) on its README.md and SKILL.md, and if anything
#      actually changed, commit and push that to the mirror repo.
#   3. If nothing changed, we say "up to date" and don't make an empty commit.
#
# This script only ever pushes to the STANDALONE MIRROR repos, never to the
# pack repo itself — the pack's own push is a separate, human-gated step.
#
# Usage:
#   ./scripts/sync-mirrors.sh
#   ./scripts/sync-mirrors.sh --print-release-history   # print the generated section, touch nothing
#
# Requires: git, rsync, and the GitHub CLI (`gh`), already authenticated.

set -euo pipefail

# The release-history generator below does byte-oriented string work (cutting/stripping
# around the multibyte em-dash "—" and the "·" separator). Under the C locale those bytes
# get split mid-character, producing mojibake — and CI defaults to LC_ALL=C. Pin a UTF-8
# locale here, before any of that computation runs, regardless of what the caller's own
# environment set; prefer en_US.UTF-8, fall back to C.UTF-8, else leave the inherited
# locale alone rather than erroring on a host with neither installed.
# The locale list is captured into a variable first, not piped straight into grep: under
# `set -o pipefail`, `grep -q`'s early exit on the first match sends SIGPIPE back to a
# still-writing `locale -a`, which then reports a non-zero (141) exit that pipefail promotes
# to the whole pipeline's status — silently defeating this very `if`, even though grep DID match.
available_locales="$(locale -a 2>/dev/null || true)"
if grep -qi '^en_US\.utf-\{0,1\}8$' <<< "$available_locales"; then
  export LC_ALL=en_US.UTF-8
elif grep -qi '^C\.utf-\{0,1\}8$' <<< "$available_locales"; then
  export LC_ALL=C.UTF-8
fi

# Resolve the pack root (this script lives in <pack>/scripts/).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PACK_ROOT/skills"
GITHUB_OWNER="happysasha18"

# A skill's copy in skills/ is written for a session that has already loaded this pack: it cites
# internal codes as its authority and points at scripts and tests that travel with the pack. Read
# by a stranger those codes resolve to nothing, so the mirror was publishing a document its own
# audience could not follow (caught 2026-08-05, when the public prover mirror was found shipping
# the internal 62 KB copy).
#
# A skill may therefore ship a PUBLIC EDITION under editions/<skill>/: the same method with every
# internal code resolved into the plain rule it stands for, carrying whatever it points at. Where
# an edition exists it is what the mirror publishes, and skills/<skill>/ stays the copy this
# project loads. The pack remains the single source of truth for both, so a hand edit made
# directly on a mirror is still overwritten by the next sync.
# An edition is only a publish source when it actually holds a skill. The copy step runs
# `rsync --delete`, so a directory that exists and holds no SKILL.md would empty the public
# repository and leave it shipping nothing, and both the attribution stamp and the language scan
# return 0 on a missing file, so nothing downstream would notice. A directory standing there
# without a SKILL.md is a half-made edition, and this refuses it by name rather than publishing
# over a working mirror.
publish_source_for() {
  local name="$1"
  local edition="$PACK_ROOT/editions/$name"
  if [ -d "$edition" ]; then
    if [ -f "$edition/SKILL.md" ]; then
      printf '%s\n' "$edition"
      return 0
    fi
    echo "${name}: editions/${name}/ holds no SKILL.md, so it publishes nothing." >&2
    echo "  Add the edition's SKILL.md, or remove the directory to publish skills/${name}/ again." >&2
    return 3
  fi
  printf '%s\n' "$PACK_ROOT/skills/$name"
}

# --print-publish-source NAME: print the directory this script would publish for one skill and
# exit, touching no repo — the same testability the release-history flag gives. It stands above
# the release-history computation so a scratch tree with no commit history can still run it.
if [ "${1:-}" = "--print-publish-source" ]; then
  if [ -z "${2:-}" ]; then
    echo "usage: sync-mirrors.sh --print-publish-source SKILL-NAME" >&2
    exit 2
  fi
  publish_source_for "$2"
  exit 0
fi

PACK_VERSION="$(cat "$PACK_ROOT/VERSION" 2>/dev/null || echo "unknown")"
PACK_SHA="$(git -C "$PACK_ROOT" rev-parse --short HEAD)"

# The banner leads with WHAT THIS IS (a stranger from a directory reads that first),
# then the read-only notice (promoter inbox wish, 2026-07-05).
banner_for() {
  local skill_name="$1"
  echo "**${skill_name}** — one skill from the [live-spec pack](https://github.com/${GITHUB_OWNER}/live-spec), installable on its own. Read-only mirror: do not open PRs here; changes land in the pack and are synced by scripts/sync-mirrors.sh."
}

# Every publication built with the pack carries the "made with live-spec" line (SPEC INV-96).
# A mirror is rebuilt from the pack folder on every sync, so the line is stamped HERE, from the
# live VERSION file — never hand-written on a mirror, where it would go stale and be wiped by
# the next rsync anyway. Stamped on the two landing files a skill owes: README.md and SKILL.md.
# Wording home: skills/publish/SKILL.md (the publish floor) — this is a reproduction, kept in
# lockstep by test_script_wording_locksteps_with_the_publish_floor.
ATTRIBUTION_LINE="made with [live-spec](https://github.com/${GITHUB_OWNER}/live-spec) v${PACK_VERSION}"

stamp_attribution() {
  local file="$1"
  [ -f "$file" ] || return 0
  if grep -q '^made with \[live-spec\]' "$file"; then
    # dead in normal operation (rsync rebuilds from the pack, which carries no line) —
    # guards a future where a pack source file ships the line itself; refresh its version
    local tmp_stamp
    tmp_stamp="$(mktemp)"
    sed "s|^made with \[live-spec\].*|${ATTRIBUTION_LINE}|" "$file" > "$tmp_stamp"
    mv "$tmp_stamp" "$file"
  else
    printf '\n---\n\n%s\n' "$ATTRIBUTION_LINE" >> "$file"
  fi
}

# A mirror also carries a generated "## Release history" section on its README.md — one line
# per pack release, so a reader who only cloned the standalone skill still sees the pack's own
# version story, without cloning the whole pack. Computed ONCE from the PACK's own git log
# (never hand-written on a mirror, where it would go stale), before the mirror loop even starts.
#
# A release commit's subject reads (in this repo's real log): an optional "live-spec " or "v"
# prefix, a semver X.Y.Z, then a separator (space, colon, em-dash, or hyphen), then the story —
# e.g. "v2.1.1 — the day-after sweep: the register floor widens... (rows 354/356/357/358)" or
# "live-spec 1.10.1 — the launch sweep clears stale temp litter by age, safely (ROADMAP 333, PATCH)".
# `git log` lists newest-first, so per distinct version we keep OVERWRITING as we scan down —
# the LAST write for a version is its OLDEST matching commit (the bump commit itself; a newer
# follow-up commit for the same version, e.g. "2.0.0: prover record covers the pushed state",
# is seen earlier in the scan and loses). The ORDER a version first appears in, though, is kept
# (that's already newest-release-first — exactly the order we want to print in).

# The headline/detail split has to be paren-aware: a subject like "...pack version (his word:
# the line doubles as the adoption tracker): made with..." has its FIRST ": " sitting INSIDE
# the parenthetical (a plain string cut would leave a dangling "(his word" fragment). Scan
# character by character, tracking paren depth, and cut at the first ": " or ". " seen at
# depth 0 — everything from there on is detail, dropped. If none is found outside parens, the
# whole story is kept (and any trailing parenthetical is still stripped below).
cut_at_outside_paren_break() {
  local s="$1"
  local depth=0 i len c c2
  len=${#s}
  for ((i = 0; i < len; i++)); do
    c="${s:$i:1}"
    if [ "$c" = "(" ]; then
      depth=$((depth + 1))
    elif [ "$c" = ")" ]; then
      [ "$depth" -gt 0 ] && depth=$((depth - 1))
    elif [ "$depth" -eq 0 ] && { [ "$c" = ":" ] || [ "$c" = "." ]; }; then
      c2="${s:$((i + 1)):1}"
      if [ "$c2" = " " ]; then
        printf '%s' "${s:0:$i}"
        return 0
      fi
    fi
  done
  printf '%s' "$s"
}

# Strip trailing parenthetical groups REPEATEDLY (not just one): a headline can carry more than
# one, e.g. "...folded (3 passes + skill eval...)" is itself the whole remaining story after the
# cut above, and other subjects stack a code-pointer group after a plain one. Each pass removes
# the LAST balanced "(...)" group anchored at the very end of the string (walking backward,
# tracking paren depth, to find its matching open paren — so a nested group inside is kept
# intact and only the outermost trailing group peels off), then trims the trailing space left
# behind. Stops as soon as the string no longer ends with ")", or a ")" is unbalanced (defensive:
# never loops forever on a malformed subject).
strip_trailing_parens() {
  local s="$1"
  local depth i c open_idx
  while [[ "$s" == *")" ]]; do
    depth=0
    open_idx=-1
    for ((i = ${#s} - 1; i >= 0; i--)); do
      c="${s:$i:1}"
      if [ "$c" = ")" ]; then
        depth=$((depth + 1))
      elif [ "$c" = "(" ]; then
        depth=$((depth - 1))
        if [ "$depth" -eq 0 ]; then
          open_idx=$i
          break
        fi
      fi
    done
    if [ "$open_idx" -ge 0 ]; then
      s="${s:0:$open_idx}"
      s="$(printf '%s' "$s" | sed -e 's/[[:space:]]*$//')"
    else
      break
    fi
  done
  printf '%s' "$s"
}

# True if $1 (X.Y.Z) is numerically greater than $2 (X.Y.Z), comparing major/minor/patch
# as integers (never lexically — "10.0.0" must beat "9.0.0"). Used to reject a commit
# subject that names a version ahead of what VERSION actually ships (a follow-up commit
# naming a future bump, e.g. "2.2.0 gate folds, first batch: ..." while VERSION still
# reads 2.1.1) — oldest-wins dedupe would otherwise let that phantom line survive a real
# bump forever.
version_gt() {
  local -a av bv
  IFS='.' read -r -a av <<< "$1"
  IFS='.' read -r -a bv <<< "$2"
  local i
  for i in 0 1 2; do
    local x="${av[$i]:-0}" y="${bv[$i]:-0}"
    if [ "$x" -gt "$y" ]; then return 0; fi
    if [ "$x" -lt "$y" ]; then return 1; fi
  done
  return 1
}

compute_release_history() {
  local -a hist_versions=()
  local -a hist_dates=()
  local -a hist_stories=()
  # Parallel flag per version: 1 once that version's stored entry came from a dash-form
  # commit (see below), so a later loose match for the same version can never demote it.
  local -a hist_is_dash=()
  local date subject version sep story is_dash found idx i

  while IFS=$'\t' read -r date subject; do
    [ -n "$date" ] || continue
    if [[ "$subject" =~ ^(live-spec\ |v)?([0-9]+\.[0-9]+\.[0-9]+)[[:space:]]*([:—-]?)[[:space:]]*(.*)$ ]]; then
      version="${BASH_REMATCH[2]}"
      sep="${BASH_REMATCH[3]}"
      story="${BASH_REMATCH[4]}"

      # Never emit a version ahead of what VERSION actually ships — such a subject names
      # follow-up work for a future bump, not a shipped release.
      if [ "$PACK_VERSION" != "unknown" ] && version_gt "$version" "$PACK_VERSION"; then
        continue
      fi

      # Cut at the first paren-outside ": " or ". " (the headline/detail split), then peel
      # off any trailing parenthetical group(s), e.g. " (ROADMAP 333, PATCH)".
      story="$(cut_at_outside_paren_break "$story")"
      story="$(strip_trailing_parens "$story")"
      # Collapse whitespace and trim the ends (printf, not echo, so no trailing newline
      # sneaks into the whitespace class tr squeezes down to a stray trailing space).
      story="$(printf '%s' "$story" | tr -s '[:space:]' ' ' | sed -e 's/^ *//' -e 's/ *$//')"

      # The bump-commit convention writes the separator directly after the version token
      # as an em-dash ("v2.1.1 — …", "live-spec 1.10.1 — …"). A dash-form commit's story
      # always wins over a "loose" match (version followed by other words, no punctuation
      # directly after it, e.g. a pre-bump audit commit) or a colon-form aside — once a
      # version has a dash-form entry stored, only another dash-form match may replace it.
      is_dash=0
      [ "$sep" = "—" ] && is_dash=1

      found=0
      idx=0
      for ((i=0; i<${#hist_versions[@]}; i++)); do
        if [ "${hist_versions[$i]}" = "$version" ]; then
          found=1
          idx=$i
          break
        fi
      done
      if [ "$found" -eq 0 ]; then
        hist_versions+=("$version")
        hist_dates+=("$date")
        hist_stories+=("$story")
        hist_is_dash+=("$is_dash")
      elif [ "${hist_is_dash[$idx]}" -eq 1 ] && [ "$is_dash" -eq 0 ]; then
        : # an existing dash-form entry outranks this loose/colon match — keep it
      else
        hist_dates[$idx]="$date"
        hist_stories[$idx]="$story"
        hist_is_dash[$idx]="$is_dash"
      fi
    fi
  done < <(git -C "$PACK_ROOT" log --date=short --pretty=format:'%ad%x09%s')

  {
    echo "---"
    echo
    echo "## Release history"
    echo
    echo "One line per release, generated from the pack's own history at every sync; the full story per release lives in the pack's [JOURNAL.md](https://github.com/${GITHUB_OWNER}/live-spec/blob/main/JOURNAL.md)."
    echo
    # ${arr[@]+"${arr[@]}"}-style guard not needed for length/indexed access (safe under
    # bash 3.2's set -u even when empty), but a repo with zero release-shaped commits must
    # still print the header above with no lines below and exit 0 — the loop below simply
    # never executes in that case.
    for ((i=0; i<${#hist_versions[@]}; i++)); do
      echo "- ${hist_versions[$i]} · ${hist_dates[$i]} — ${hist_stories[$i]}"
    done
  }
}

# Computed once, up front, and reused for every mirror (and for --print-release-history).
RELEASE_HISTORY="$(compute_release_history)"

stamp_release_history() {
  local file="$1"
  [ -f "$file" ] || return 0
  printf '\n%s\n' "$RELEASE_HISTORY" >> "$file"
}

# --print-release-history: print the generated section and exit, touching no repo at all —
# lets the generation logic be tested without cloning a mirror or reaching GitHub.
if [ "${1:-}" = "--print-release-history" ]; then
  printf '%s\n' "$RELEASE_HISTORY"
  exit 0
fi

# The shipped-language machine's reach onto a mirror (SPEC INV-120): the assembled README
# carries generated text harvested from commit subjects, so before anything is committed the
# file is scanned for stray Cyrillic and a bare owner name; a hit aborts this mirror's sync
# loudly instead of publishing it. The license line's "© Alexander Abramovich" stays legal.
check_mirror_language() {
  local file="$1"
  [ -f "$file" ] || return 0
  python3 - "$file" <<'PY'
import re, sys
bad = []
for n, ln in enumerate(open(sys.argv[1], encoding="utf-8").read().splitlines(), 1):
    if re.search("[\u0400-\u04FF]", ln):
        bad.append("%d: %s" % (n, ln.strip()))
    elif "Alexander" in ln and "©" not in ln:
        bad.append("%d: %s" % (n, ln.strip()))
if bad:
    sys.stderr.write("sync-mirrors: FAIL (shipped-language) — stray Cyrillic or an owner name in %s:\n  %s\n"
                     % (sys.argv[1], "\n  ".join(bad[:5])))
    sys.exit(1)
PY
}

# One status line per skill, collected here and printed again at the end as a summary.
declare -a SUMMARY_LINES=()
# A skill this run refused to publish. The summary alone left the run exiting zero, so a half-made
# edition read as a clean sync (caught 2026-08-05 by the review of the change that added the refusal).
declare -a REFUSED=()

# Pull a short description out of a SKILL.md's YAML frontmatter "description:" field.
# Used only as a fallback when a mirror has no README.md of its own.
extract_skill_description() {
  local skill_md="$1"
  awk '
    /^---[[:space:]]*$/ { fence++; next }
    fence == 1 && /^description:[[:space:]]*/ {
      sub(/^description:[[:space:]]*/, "");
      gsub(/^"|"$/, "");
      print;
      exit
    }
  ' "$skill_md"
}

for skill_path in "$SKILLS_DIR"/*/; do
  [ -d "$skill_path" ] || continue
  skill_name="$(basename "$skill_path")"
  repo="${GITHUB_OWNER}/${skill_name}"

  echo "== ${skill_name} =="

  # Does a standalone mirror repo exist for this skill? We never create one here.
  # Two auth paths. Locally we use gh + HTTPS (the developer's own gh login). In CI we set
  # MIRROR_SSH=1 and clone over SSH with a per-mirror deploy key; that key is registered on
  # exactly one mirror repo, so every OTHER skill's would-be mirror fails to authenticate and
  # naturally reads as "no mirror yet" — the correct outcome, no allow-list to maintain.
  if [ -n "${MIRROR_SSH:-}" ]; then
    if ! git ls-remote "git@github.com:${repo}.git" >/dev/null 2>&1; then
      echo "${skill_name}: skipped (no mirror repo reachable with the deploy key)"
      SUMMARY_LINES+=("${skill_name}: skipped (no mirror repo yet)")
      continue
    fi
  else
    if ! gh repo view "$repo" >/dev/null 2>&1; then
      echo "${skill_name}: skipped (no mirror repo yet)"
      SUMMARY_LINES+=("${skill_name}: skipped (no mirror repo yet)")
      continue
    fi
  fi

  work_dir="$(mktemp -d)"
  trap 'rm -rf "$work_dir"' EXIT

  echo "cloning ${repo} into scratch dir..."
  if [ -n "${MIRROR_SSH:-}" ]; then
    git clone --quiet "git@github.com:${repo}.git" "$work_dir/mirror"
  else
    gh repo clone "$repo" "$work_dir/mirror" -- -q
  fi

  mirror_dir="$work_dir/mirror"

  # Replace the mirror's content with the pack's copy of this skill, but keep
  # the mirror's own .git history (that's how it stays a real, pushable repo).
  # Where the skill ships a public edition, that edition is what goes out.
  # A half-made edition stops this one mirror and leaves every other mirror to run.
  if ! publish_src="$(publish_source_for "$skill_name")"; then
    SUMMARY_LINES+=("${skill_name}: skipped (editions/${skill_name}/ holds no SKILL.md)")
    REFUSED+=("$skill_name")
    continue
  fi
  if [ "$publish_src" != "$skill_path" ] && [ "$publish_src/" != "$skill_path" ]; then
    echo "${skill_name}: publishing the public edition from editions/${skill_name}/"
  fi
  rsync -a --delete --exclude='.git' "$publish_src/" "$mirror_dir/"

  # Make sure README.md starts with the what-this-is + read-only banner.
  BANNER="$(banner_for "$skill_name")"
  readme="$mirror_dir/README.md"
  if [ -f "$readme" ] && head -1 "$readme" | grep -q "Read-only mirror"; then
    # a banner (old or new wording) is there — rewrite line 1 to the current wording
    tmp_readme="$(mktemp)"
    { echo "$BANNER"; tail -n +2 "$readme"; } > "$tmp_readme"
    mv "$tmp_readme" "$readme"
  elif [ -f "$readme" ]; then
    # Skill has its own README — keep it, just prepend the banner above it.
    tmp_readme="$(mktemp)"
    {
      echo "$BANNER"
      echo
      cat "$readme"
    } > "$tmp_readme"
    mv "$tmp_readme" "$readme"
  else
    # No README shipped with the skill — write banner + a short description
    # pulled from the SKILL.md frontmatter.
    desc="$(extract_skill_description "$mirror_dir/SKILL.md" 2>/dev/null || true)"
    {
      echo "$BANNER"
      echo
      if [ -n "$desc" ]; then
        echo "# ${skill_name}"
        echo
        echo "$desc"
      else
        echo "# ${skill_name}"
      fi
    } > "$readme"
  fi

  # The generated release-history section, README.md only (SKILL.md stays clean) — stamped
  # before the attribution line so the attribution line stays the last thing in the file.
  stamp_release_history "$mirror_dir/README.md"

  # The attribution line, stamped from the live pack version (SPEC INV-96).
  stamp_attribution "$mirror_dir/README.md"
  stamp_attribution "$mirror_dir/SKILL.md"

  # The assembled README is scanned before anything is committed (SPEC INV-120).
  check_mirror_language "$mirror_dir/README.md"

  # Anything to commit?
  ( cd "$mirror_dir" && git add -A )
  if ( cd "$mirror_dir" && git diff --cached --quiet ); then
    echo "${skill_name}: up to date"
    SUMMARY_LINES+=("${skill_name}: up to date")
  else
    commit_msg="sync from live-spec pack ${PACK_VERSION} (${PACK_SHA})"
    ( cd "$mirror_dir" && git commit -q -m "$commit_msg" )
    ( cd "$mirror_dir" && git push -q )
    echo "${skill_name}: updated"
    SUMMARY_LINES+=("${skill_name}: updated")
  fi

  rm -rf "$work_dir"
  trap - EXIT
done

echo
echo "== summary =="
for line in "${SUMMARY_LINES[@]}"; do
  echo "$line"
done

# A refusal ends the run non-zero. Every other mirror has already synced by here, so the exit code
# reports what was left behind rather than undoing the work that succeeded.
if [ "${#REFUSED[@]}" -gt 0 ]; then
  echo
  echo "sync-mirrors: ${#REFUSED[@]} skill(s) published nothing: ${REFUSED[*]}"
  echo "  Each has an editions/<skill>/ directory holding no SKILL.md."
  echo "  Add the edition's SKILL.md, or remove the directory to publish skills/<skill>/ again."
  exit 1
fi
