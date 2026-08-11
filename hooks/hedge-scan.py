#!/usr/bin/env python3
"""Stop-hook: catch the offering-hedge frame in outgoing chat (SPEC INV-238).

An offering-hedge is a sentence that offers to do a thing the seat could already derive and could
already reverse through git, holding the offer open for a cue — "just say the word", "let me know
if you want me to" — instead of doing the thing and reporting it done. This is the machine for the
standing no-only-say-hedge behaviour and its deferral chat-hedge sibling [profile
proactivity.no-only-say-hedge, base rule 29, INV-152].

Modeled exactly on the scissors scan (hooks/scissors-scan.py, SPEC INV-173): canonical pack copy,
universal tier only, ships an inline English pattern list. A host's own extra patterns (another
language, a narrower personal rule) never live here — they load from an optional overlay file
`~/.claude/hooks/hedge-personal.json` (a JSON list of regex strings), owned by the personal layer;
this file never creates or edits that overlay. Missing or malformed overlay falls back to
universal-only, silently.

Reads every assistant message shown since the last human turn (hooks/turn_reader.py) and scans it for
the hedge markers, so an offence in an early inter-tool narration line reds like one in the final
reply. A line
demonstrated inside «guillemets», "double quotes", or `backticks`, and any line inside a fenced
``` code block, is stripped before matching — quoting the banned frame to talk ABOUT it is not
itself a live instance of it. A surviving match BLOCKS the stop with a rewrite instruction.

The gate stands clear of a genuine taste, policy, or irreversible question that names its
human-only fact [INV-152]: that question is the seat's honest admission that the call is not its
own, a shape distinct from an offer to do a call that already is its own.

This net is a FIRST cheap filter on common high-confidence hedge frames, not the whole class. A
paraphrase it does not list slips through, the way the scissors scan's literal list trails one
escape behind the next word [INV-173, INV-203]. The class itself — a hedge in any phrasing, judged
against whether the act was actually derivable — is held by the bucket-1 conduct judge that reads
the turn's action trace, not by this literal net. And this is a Stop-hook notice: the reply is
already emitted when it fires, so it flags the previous reply and asks for a rewrite that reaches
the human one message later, the same one-turn floor the retired answer-first arm carried [INV-220].
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turn_reader  # noqa: E402

# UNIVERSAL tier — the English offering-hedge frame (SPEC INV-238's pack law). A FIRST cheap filter
# on high-confidence frames, never the whole class [INV-173, INV-203]. The `(?!['’]t)` after "i can"
# keeps a limitation ("if you want, I can't force it") off the net — that states a boundary rather
# than offering an act. The last entry catches the reversed order ("I can rename it if you'd like").
PATTERNS = [
    r"just say the word",
    r"say the word and i",
    r"just give me (the word|a nod|a shout|the go[- ]?ahead)",
    r"let me know if you want me to",
    r"let me know if you'?d like me to",
    r"let me know if you would like me to",
    r"let me know and i'?ll",
    r"if you want,? i can\b(?!['’]t)",
    r"if you'?d like,? i can\b(?!['’]t)",
    r"if you would like,? i can\b(?!['’]t)",
    r"\bi can\b(?!['’]t)[^.?!\n]{0,40}\bif you(?:['’]?d like| want)\b",
]


def _load_personal_patterns():
    """PERSONAL overlay: ~/.claude/hooks/hedge-personal.json, a JSON list of regex strings,
    owned by the personal layer. Missing or malformed -> silently proceed with universal only."""
    path = os.path.expanduser("~/.claude/hooks/hedge-personal.json")
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
    """Strip spans inside «guillemets», "double quotes", and `backticks` (non-greedy, per line)."""
    s = re.sub(r"«[^»]*»", " ", line)
    s = re.sub(r'"[^"]*"', " ", s)
    s = re.sub(r"“[^”]*”", " ", s)  # typographic double quotes
    s = re.sub(r"‘[^’]*’", " ", s)  # typographic single quotes (ASCII ' kept: apostrophes)
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
        "HEDGE CHECK — the reply carries an offering-hedge frame:\n"
        + quoted
        + "\n\nAn offer to do a derivable, git-reversible act only once the human gives a cue "
        "('just say the word' / 'let me know if you want me to' / a personal-layer pattern) is "
        "banned. For each line above: if the act is already derivable and already reversible, do "
        "it now and rewrite the reply to report it done, not offered. If the call genuinely is the "
        "human's own — a taste, policy, or irreversible fact only he can name — say so in one line "
        "and continue; that is not a hedge."
    )
    # suppressOutput keeps the machine's complaint off the human's screen: the hook talks to the
    # model, and what the human is owed is the correction the model then sends (as scissors-scan does).
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
