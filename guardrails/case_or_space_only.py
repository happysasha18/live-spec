#!/usr/bin/env python3
"""case_or_space_only.py — judges whether a diff consists ENTIRELY of changes in letter case
and/or whitespace: the case-or-space carve-out that lets gate a (the prover record) and gate s
(the skill review) stand down without paying the full price those gates otherwise charge.

The boundary is drawn exactly there, and nowhere wider. A change that only re-cases letters or
re-spaces the same words changes nothing a reader, or a model reading a skill's body, would read
differently — it is the same words in the same order. Anything else — a reworded line, an added or
removed word, a reordered sentence, a changed punctuation mark that is not whitespace — is an
ordinary edit and owes the review it would otherwise owe. There is no "small diff" or "one-liner"
or "docs-only" allowance here: only these two exact categories are exempt, judged by literal
comparison, never by guessing at a change's importance.

Three boundaries this judge holds, each one found by an adversarial read of its first draft and
each one narrowing the carve-out rather than widening it:

  Word boundaries survive. Whitespace runs collapse to ONE space rather than vanishing, so a
  re-wrapped paragraph or a re-indented block still reads as the same words, while `foo bar`
  turned into `foobar` does not — deleting the space between two words changes the words.

  The file mode must not move. A change from 100644 to 100755 leaves a file's bytes untouched
  while making it executable; that is not a change in case or whitespace, and it is not exempt.

  Only regular files are judged. A symlink's blob holds its target path, which would otherwise
  read as ordinary text and let a re-cased target pass as cosmetic on a case-sensitive
  filesystem. Symlinks, submodule links, and anything else that is not a regular file stop the
  carve-out cold.

Usage: python3 guardrails/case_or_space_only.py <base> <head> [path ...]
  no paths given  -> judges the whole base..head diff
  paths given     -> judges only those paths within that diff

Exit 0: the diff is non-empty AND every changed entry is a same-path edit (git status `M`) of a
        regular file whose mode did not move and whose two sides, once whitespace is collapsed
        and case is folded, are identical.
Exit 1: everything else — an empty diff (nothing changed is not "only case/space", since there is
        nothing to carve out for), any add/delete/rename/copy/type-change, any mode change, any
        entry that is not a regular file, any side that fails to decode as UTF-8 (a binary is
        never judged), or any entry whose normalized sides differ.

Silent on both exits: this is a predicate other scripts call, not a report meant for a person.
"""
import subprocess
import sys

# The two modes a regular file carries in a git tree. A symlink (120000), a submodule link
# (160000), or anything else is not a regular file and is never judged cosmetic.
REGULAR_FILE_MODES = ("100644", "100755")


def _changed_entries(base, head, paths):
    """Every changed entry as (old_mode, new_mode, old_sha, new_sha, status).

    Reads `git diff --raw`, which carries both sides' modes and blob ids — the modes are what
    catch a chmod and a symlink, and the blob ids let the content be read without ever quoting a
    path. Returns None if git could not run the diff at all.
    """
    cmd = ["git", "diff", "--raw", base, head]
    if paths:
        cmd += ["--"] + list(paths)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    entries = []
    for line in result.stdout.splitlines():
        if not line.startswith(":"):
            continue
        left = line[1:].split("\t")[0]
        fields = left.split()
        if len(fields) < 5:
            return None
        entries.append(tuple(fields[:5]))
    return entries


def _blob(sha):
    """The raw bytes of a blob, or None if git could not read it."""
    result = subprocess.run(["git", "cat-file", "blob", sha], capture_output=True)
    if result.returncode != 0:
        return None
    return result.stdout


def _normalize(data):
    """None in, None out (unreadable side). Bytes that fail UTF-8 decoding are a binary and also
    normalize to None. Otherwise: every whitespace run collapsed to a single space, the ends
    trimmed, and letters lower-cased — so re-wrapping and re-indenting read the same, and joining
    two words into one does not."""
    if data is None:
        return None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return " ".join(text.split()).lower()


def is_case_or_space_only(base, head, paths):
    entries = _changed_entries(base, head, paths)
    if not entries:
        return False

    for old_mode, new_mode, old_sha, new_sha, status in entries:
        if not status.startswith("M"):
            return False
        if old_mode != new_mode:
            return False
        if old_mode not in REGULAR_FILE_MODES:
            return False
        before = _normalize(_blob(old_sha))
        after = _normalize(_blob(new_sha))
        if before is None or after is None:
            return False
        if before != after:
            return False

    return True


def main(argv):
    if len(argv) < 3:
        return 1
    base, head = argv[1], argv[2]
    paths = argv[3:]
    return 0 if is_case_or_space_only(base, head, paths) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
