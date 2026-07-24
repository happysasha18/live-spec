#!/usr/bin/env python3
"""Stop-hook: catch the scissors / empty-contrast frame in outgoing chat (SPEC INV-173).

Canonical pack copy, universal tier only: the English contrast-by-denial frame ("X, not Y",
"X — not Y") is a pack law every host inherits. A host's own extra patterns (another language, a
narrower personal rule) never live here — they load from an optional overlay file
`~/.claude/hooks/scissors-personal.json` (a JSON list of regex strings), owned by the personal
layer; this file never creates or edits that overlay. Missing or malformed overlay falls back to
universal-only, silently.

Reads every assistant message shown since the last human turn (hooks/turn_reader.py) and scans it for
the scissors markers, so an offence in an early inter-tool narration line reds like one in the final
reply. A line
demonstrated inside «guillemets», "double quotes", or `backticks`, and any line inside a fenced
``` code block, is stripped before matching — quoting the banned frame to talk ABOUT it is not
itself a live instance of it. A surviving match BLOCKS the stop with a rewrite instruction.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turn_reader  # noqa: E402

# UNIVERSAL tier — the English contrast frame (SPEC INV-173's pack law).
PATTERNS = [
    r",\s+not\s+\S",       # "X, not Y"
    r"\s+—\s+not\s+\S",    # "X — not Y" (em-dash negation)
]


def _load_personal_patterns():
    """PERSONAL overlay: ~/.claude/hooks/scissors-personal.json, a JSON list of regex strings,
    owned by the personal layer. Missing or malformed -> silently proceed with universal only."""
    path = os.path.expanduser("~/.claude/hooks/scissors-personal.json")
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
    return [re.compile(p) for p in PATTERNS + _load_personal_patterns()]


def _strip_quoted_demos(line):
    """Strip spans inside «guillemets», "double quotes", and `backticks` (non-greedy, per line)."""
    s = re.sub(r"«[^»]*»", " ", line)
    s = re.sub(r'"[^"]*"', " ", s)
    s = re.sub(r"\u201c[^\u201d]*\u201d", " ", s)  # typographic double quotes
    s = re.sub(r"\u2018[^\u2019]*\u2019", " ", s)  # typographic single quotes (ASCII ' kept: apostrophes)
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
    # never loop: if a prior stop-hook already fired this turn, stand down.
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
        "SCISSORS CHECK — the reply carries a contrast/negation frame:\n"
        + quoted
        + "\n\nThe contrast-by-denial frame is banned ('X, not Y' / 'X — not Y', or a personal-layer "
        "pattern). For each line above: if the denied half adds no new information, restate it as a "
        "plain positive sentence and send that correction now. If the contrast genuinely informs (a "
        "real alternative the reader would assume), say so in one line and continue."
    )
    # suppressOutput keeps the machine's complaint off the human's screen: the hook talks to the
    # model, and what the human is owed is the correction the model then sends. Added 2026-07-17
    # on the owner's word, asking why the raw block text was being shown to him at all.
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
