#!/usr/bin/env bash
# check-skill-loadability.sh — gate (f) of the push gate: every shipped skill LOADS
# (row 80, the Trail-of-Bits lesson). A skill that ships with broken frontmatter, a
# name that doesn't match its folder, no description, no version, or a "when NOT to
# use" section missing, is RED at push — a skill the harness can't index or a reader
# can't scope is a broken artifact however good its prose.
#
# Usage: check-skill-loadability.sh [skills-dir]
#   skills-dir defaults to "<repo-root>/skills"

set -euo pipefail

SKILLS_DIR="${1:-$(git rev-parse --show-toplevel)/skills}"

fail=0
count=0
for skill_md in "$SKILLS_DIR"/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  count=$((count+1))
  dir_name="$(basename "$(dirname "$skill_md")")"

  # frontmatter block: first line ---, a closing --- within the first 40 lines
  if [ "$(head -1 "$skill_md")" != "---" ] || ! sed -n '2,40p' "$skill_md" | grep -q '^---$'; then
    echo "FAIL (loadability): $dir_name — no frontmatter block"; fail=1; continue
  fi
  fm="$(awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$skill_md")"

  name="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -1)"
  if [ -z "$name" ]; then
    echo "FAIL (loadability): $dir_name — frontmatter has no name:"; fail=1
  elif [ "$name" != "$dir_name" ]; then
    echo "FAIL (loadability): $dir_name — name '$name' does not match its folder"; fail=1
  fi

  if ! printf '%s\n' "$fm" | grep -q '^description:'; then
    echo "FAIL (loadability): $dir_name — frontmatter has no description:"; fail=1
  fi

  if ! printf '%s\n' "$fm" | grep -Eq '^[[:space:]]+version:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+'; then
    echo "FAIL (loadability): $dir_name — no metadata version (M-7)"; fail=1
  fi

  if ! grep -qi 'work that belongs elsewhere' "$skill_md"; then
    echo "FAIL (loadability): $dir_name — no 'Work that belongs elsewhere' section (row 80)"; fail=1
  fi
done

if [ "$count" -eq 0 ]; then
  echo "FAIL (loadability): no skills found under $SKILLS_DIR"; exit 1
fi

if [ "$fail" -ne 0 ]; then
  echo "  Fix: repair the skill's frontmatter/section; a skill that can't load or scope itself must not ship."
  exit 1
fi

echo "OK (loadability): $count skill(s) load, named, versioned, negative-scoped."
exit 0
