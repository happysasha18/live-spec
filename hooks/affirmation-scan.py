#!/usr/bin/env python3
"""Stop-hook: catch empty affirmation / validation aimed at the user in outgoing chat.

A reply carries no line telling the human he is right, praising his question or his intuition, or
framing the agent's own work as superior ("measured, not guessed"; "honest, not on the eye"). Empty
validation costs the reader attention and returns nothing; the reply owes the finding or the action,
and nothing else leads. The exchange that set this standing is dated in JOURNAL.md. This is the machine
behind the personal profile's no-affirmation rule, a sibling of the scissors scan.

Two tiers. The UNIVERSAL tier holds the language-neutral English validation phrases. A host's own extra
patterns — another language, a narrower personal phrase — load from an optional overlay file
`~/.claude/hooks/affirmation-personal.json` (a JSON list of regex strings), owned by the personal layer;
this file never creates or edits that overlay. Missing or malformed overlay falls back to universal-only,
silently.

Reads every assistant message shown since the last human turn (hooks/turn_reader.py), so an affirmation
in an early narration line reds like one in the final reply — the reach its siblings took at the row-482
fix and this arm had missed until 2026-07-27. A phrase demonstrated inside «guillemets», "double
quotes", or `backticks`, and any line inside a fenced ``` code block, is stripped before matching — so
quoting a banned phrase to talk ABOUT it is not itself a live instance. A surviving match BLOCKS the stop
with a rewrite instruction.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turn_reader  # noqa: E402

# UNIVERSAL tier — English validation aimed at the user or the exchange.
PATTERNS = [
    r"\byou'?re\s+(absolutely\s+|totally\s+|completely\s+|so\s+|quite\s+)?right\b",
    r"\byou\s+are\s+(absolutely\s+|totally\s+|completely\s+|quite\s+)?right\b",
    r"\byou'?re\s+not\s+wrong\b",
    r"\byou'?re\s+onto\s+something\b",
    r"\b(great|good|excellent|fair|sharp|nice)\s+(question|point|catch|call|instinct)\b",
    r"\bgood\s+catch\b",
    r"\bspot[\s-]on\b",
    r"\bwell\s+spotted\b",
    r"\b(exactly|absolutely|precisely)\s+right\b",
    r"\byour\s+(intuition|instinct)\s+(is|was)\b",
]


def _load_personal_patterns():
    path = os.path.expanduser("~/.claude/hooks/affirmation-personal.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    patterns = []
    for p in data:
        if not isinstance(p, str):
            continue
        try:
            re.compile(p)
        except re.error:
            continue
        patterns.append(p)
    return patterns


def _compiled_patterns():
    return [re.compile(p, re.IGNORECASE) for p in PATTERNS + _load_personal_patterns()]


def _strip_quoted_demos(line):
    s = re.sub(r"«[^»]*»", " ", line)
    s = re.sub(r'"[^"]*"', " ", s)
    s = re.sub(r"“[^”]*”", " ", s)
    s = re.sub(r"‘[^’]*’", " ", s)
    s = re.sub(r"`[^`]*`", " ", s)
    return s


def find_hits(text, patterns):
    hits = []
    in_fence = False
    for raw_line in text.splitlines():
        if raw_line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        scrubbed = _strip_quoted_demos(raw_line)
        for rx in patterns:
            if rx.search(scrubbed):
                hits.append(raw_line.strip()[:160])
                break
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
    hits = find_hits(text, _compiled_patterns())
    if not hits:
        sys.exit(0)
    quoted = "\n".join("  · " + h for h in hits[:5])
    reason = (
        "AFFIRMATION CHECK — the reply validates the user or praises the exchange:\n"
        + quoted
        + "\n\nEmpty affirmation and validation are banned. Do not tell the user he is right, praise his "
        "question or intuition, or frame your own work as superior. Delete the validating clause and open "
        "with the substance — the finding or the action. Send the corrected reply now."
    )
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
