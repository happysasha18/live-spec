#!/usr/bin/env python3
"""skill_review_verdict.py — the tool-verification arm of guardrails/check-skill-review.sh (q-817,
SPEC INV-208). A record can quote the validator's output by hand; only running the validator right
now and diffing its real verdict against that quote proves the quote is not itself invented — the
same class of closing check-prover-record.sh and case_or_space_only.py already apply to their own
gates, read the thing rather than the words about the thing.

Usage: python3 skill_review_verdict.py <record-path> <skill-name> <repo-root> <validator-path>

<record-path> may be relative to <repo-root> (as `git ls-files` returns it) or absolute. Reads the
record's fenced block whose first line names quick_validate.py and this skill's own directory, and
whose last line reads "(exit N)" — the shape docs/skill-review/README.md states. Runs
`python3 <validator-path> skills/<skill-name>` from <repo-root> and compares its real stdout and
exit code against what the record quotes.

Exit 0, silent: the quote matches what the validator says right now.
Exit 2, a FAIL line on stdout: the quote and the real verdict disagree.
Exit 3, a FAIL line on stdout: the record carries no such quoted block at all.
Exit 4, a FAIL line on stdout: the validator itself reports this skill invalid, whatever the
  record quotes — a currently-broken skill never passes on an old, honest quote.
Exit 1: bad usage.
"""
import os
import re
import subprocess
import sys

FENCE_RE = re.compile(r"```\n(.*?)\n```", re.DOTALL)
EXIT_LINE_RE = re.compile(r"^\(exit\s+(-?\d+)\)\s*$")


def find_quoted_block(text, skill_name):
    """The first fenced block whose opening line runs the validator against this skill: its
    printed stdout and the exit code it closes on, or None if no such block exists."""
    for match in FENCE_RE.finditer(text):
        body_lines = match.group(1).split("\n")
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        if not body_lines:
            continue
        head = body_lines[0].strip()
        if not head.startswith("$") or "quick_validate.py" not in head:
            continue
        if not re.search(r"\bskills/" + re.escape(skill_name) + r"/?\s*$", head):
            continue
        tail_lines = body_lines[1:]
        while tail_lines and not tail_lines[-1].strip():
            tail_lines.pop()
        if not tail_lines:
            continue
        exit_match = EXIT_LINE_RE.match(tail_lines[-1].strip())
        if not exit_match:
            continue
        return "\n".join(tail_lines[:-1]).strip(), int(exit_match.group(1))
    return None


def _print_block(label, text, exit_code):
    print(f"  {label}:")
    for line in text.splitlines() or [""]:
        print(f"    {line}")
    print(f"  (exit {exit_code})")


def main(argv):
    if len(argv) != 5:
        print("usage: skill_review_verdict.py <record-path> <skill-name> <repo-root> <validator-path>")
        return 1
    record_path, skill_name, repo_root, validator_path = argv[1:5]
    record_full = record_path if os.path.isabs(record_path) else os.path.join(repo_root, record_path)

    with open(record_full, encoding="utf-8") as f:
        record_text = f.read()

    quoted = find_quoted_block(record_text, skill_name)
    if quoted is None:
        print(f"FAIL (skill review): skill '{skill_name}' has a covering record ({record_path}), "
              f"but no quoted block in it names quick_validate.py against skills/{skill_name}.")
        return 3
    quoted_stdout, quoted_exit = quoted

    result = subprocess.run(
        ["python3", validator_path, f"skills/{skill_name}"],
        cwd=repo_root, capture_output=True, text=True,
    )
    real_stdout = result.stdout.strip()
    real_exit = result.returncode

    if real_exit != 0:
        print(f"FAIL (skill review): skill '{skill_name}' fails Anthropic's own quick_validate.py "
              f"right now — a currently-invalid skill cannot pass regardless of what its record "
              f"quotes.")
        _print_block("validator says, right now", real_stdout, real_exit)
        return 4

    if quoted_stdout != real_stdout or quoted_exit != real_exit:
        print(f"FAIL (skill review): skill '{skill_name}' quotes a verdict the validator disagrees "
              f"with.")
        _print_block("record quotes", quoted_stdout, quoted_exit)
        _print_block("quick_validate.py just now said", real_stdout, real_exit)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
