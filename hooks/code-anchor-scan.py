#!/usr/bin/env python3
"""Stop-hook: an internal code may only trail a sentence as a quiet anchor (SPEC INV-28, base rule 2).

The law says every human-facing sentence stands on its own in the product's words, and internal handles
— a queue row number, an INV/M/E/T code — trail in parentheses for anyone who wants to follow them. A
sentence that leads with a handle hands the reader a number he has no way to resolve.

It decayed for want of a machine. On 2026-07-27 the human was handed "rows 386 and 412, hanging since 18
July" and answered plainly: he does not remember row numbers, the sentence tells him nothing, put a hook
on it. This is that hook.

WHAT IT READS. Every assistant message shown since the last human turn (hooks/turn_reader.py), so a
naked code in an early narration line reds like one in the final reply.

WHAT PASSES, by construction:
  - a code inside parentheses or square brackets — the lawful trailing anchor;
  - a table row (a line starting with `|`), where the neighbouring cell carries the plain words;
  - a fenced code block, an inline `backtick` span, and a «quoted» or "quoted" span — text ABOUT a code
    rather than a code addressed to the reader;
  - a bare number with no code word in front of it, since this net reads the naming, not arithmetic.

HONEST BOUNDARY. This arm sees whether a code was left standing outside an anchor. It cannot see whether
the plain words that replace it are the RIGHT words: "the thing from yesterday (row 386)" passes the
machine and still fails the reader. It is a Stop-hook notice, so the reply is already sent when it fires;
it asks for the naming to be repeated in plain words in the next message, which is the most a chat
surface allows.

Repo home: hooks/code-anchor-scan.py; installed copy: ~/.claude/hooks/ (beside scissors-scan.py).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turn_reader  # noqa: E402

# The naming patterns: a code word followed by its number, in either working language, plus the bare
# letter-dash-number handles the documents use.
PATTERNS = [
    r"(?<![\w-])строк[аиуеойы]?\s+\d+",
    r"(?<![\w-])строки\s+\d+",
    r"(?<![\w-])rows?\s+\d+",
    r"(?<![\w-])(?:INV|ROW|M|E|T|S|D|A|B|C|F|R|ACT)-\d+",
]
COMPILED = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
QUOTED = re.compile(r"«[^»\n]*»|\"[^\"\n]*\"|“[^”\n]*”")
BRACKETED = re.compile(r"\([^()\n]*\)|\[[^\[\]\n]*\]")


def _strippable(text):
    """Remove every span where a code is lawful or is being quoted, leaving live prose behind."""
    text = FENCE.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    text = QUOTED.sub(" ", text)
    # Table rows carry their describing cell beside the number.
    lines = [ln for ln in text.split("\n") if not ln.lstrip().startswith("|")]
    text = "\n".join(lines)
    # Parenthesised and bracketed spans are the lawful anchor position. Two passes so a nested pair
    # collapses too.
    for _ in range(2):
        text = BRACKETED.sub(" ", text)
    return text


def find_hits(text):
    live = _strippable(text)
    hits = []
    for rx in COMPILED:
        for m in rx.finditer(live):
            start = max(0, m.start() - 60)
            end = min(len(live), m.end() + 60)
            hits.append(live[start:end].replace("\n", " ").strip())
    return hits


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    if payload.get("stop_hook_active"):
        sys.exit(0)
    text = turn_reader.turn_text(payload.get("transcript_path", ""))
    if not text:
        sys.exit(0)
    hits = find_hits(text)
    if not hits:
        sys.exit(0)
    quoted = "\n".join("  · " + h for h in hits[:5])
    reason = (
        "CODE-ANCHOR CHECK — the reply leaves an internal code standing where plain words belong:\n"
        + quoted
        + "\n\nA queue row number or an INV/M/E/T code names nothing to the reader on its own. Name the "
        "wish in the product's words and let the code trail in parentheses: 'branches and working copies "
        "for parallel lanes have been open since 18 July (row 386)'. Send the naming now, in one line "
        "per code, so what was asked of him is legible."
    )
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
