#!/usr/bin/env python3
"""turn_reader.py — read EVERY assistant message shown since the last human turn (row 482).

Moved out of hooks/register-judge.py so every Stop-hook scan that owes the whole turn (not just its
last message) can share one reader: register-judge.py, scissors-scan.py, hedge-scan.py. A hook that
reads only the last assistant message shipped every violation between tool calls untouched (proven
2026-07-17 on the register judge; the same defect applied to the contrast-frame and hedge scans).
answer-first-scan.py is the deliberate exception — it judges only the final reply the human reads,
never the inter-tool narration, so it keeps its own last-message reader.

Repo home: hooks/turn_reader.py; installed copy: ~/.claude/hooks/ (beside the hooks that import it).
"""
import json
import os


def _is_tool_result(rec):
    """A type:"user" record that carries a tool_result (its content is a list of tool_result blocks) is the
    harness reporting a tool's output, not a human turn. Only a user record carrying real human text is the
    turn boundary."""
    content = rec.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return False
    return any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def turn_text(path):
    """EVERY assistant message the human was shown this turn, joined — not the last one only.

    The place the old scan looked was wrong: it read the turn's LAST message, so a long agentic turn
    shipped every violation between tool calls untouched (proven 2026-07-17). The judge reads the whole
    turn — all assistant text since the last human message — so an offence in an early inter-tool message
    reds like any other. Blocks are joined with newlines, so a quote in any of them validates verbatim.
    """
    if not path or not os.path.exists(path):
        return ""
    try:
        with open(path) as fh:
            records = []
            for line in fh:
                try:
                    records.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return ""
    # Walk back to the last HUMAN message; everything assistant after it is this turn's output. In a real
    # Claude Code transcript every tool result is itself a type:"user" record, so a plain "last user"
    # boundary lands on a tool_result and reads only the text after the final tool call — the last-message
    # defect this reader exists to close. The real boundary is a user record carrying human text, not a
    # tool_result, so tool_result user records are skipped (corrected 2026-07-17).
    start = 0
    for i in range(len(records) - 1, -1, -1):
        rec = records[i]
        if rec.get("type") == "user" and not rec.get("isSidechain") and not _is_tool_result(rec):
            start = i + 1
            break
    chunks = []
    for rec in records[start:]:
        if rec.get("type") != "assistant" or rec.get("isSidechain"):
            continue
        blocks = rec.get("message", {}).get("content", [])
        text = "".join(
            b.get("text", "") for b in blocks if isinstance(b, dict) and b.get("type") == "text"
        )
        if text.strip():
            chunks.append(text)
    return "\n".join(chunks)
