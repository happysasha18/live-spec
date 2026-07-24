#!/usr/bin/env python3
"""register-judge.py — the CHAT surface's register judge (ROADMAP row 416, SPEC INV-203).

The chat arm of the one judge (the mechanism lives in register_judge_core.py). It reads the outgoing
text and hands it, with the chat law, to the cheapest tier, taking back the sentences that carry no
information. The literal overlay beside this file (scissors-personal.json) covers the phrases someone
thought of; a list cannot cover a class, so four empty intensifiers passed the 22-pattern list untouched
when probed 2026-07-17. This judge holds the class the list cannot.

The law it reads is SPLIT (SPEC INV-173): the UNIVERSAL law (naming a thing by denying its neighbour —
the scissors frame) ships with the pack in register_judge_core.py; the PERSONAL laws (empty intensifier,
grading the reader's remark) ride an overlay the personal layer owns
(~/.claude/hooks/register-judge-personal.md), so the pack ships nobody's personal rules. A missing
overlay falls back to universal-only, silently.

Contract: reads a Stop-hook payload on stdin, writes a Stop-hook JSON decision on stdout, exits 0. It
NEVER blocks on its own failure — a judge that cannot reach a model, or answers slowly, or answers in a
shape this script cannot read, stands down and says so on stderr, never blocking on its own breakage.

Repo home: hooks/register-judge.py; installed copy: ~/.claude/hooks/.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import register_judge_core as core  # noqa: E402
from turn_reader import turn_text  # noqa: E402

MIN_CHARS = 120


def chat_law():
    """The chat law body: the universal frame law plus the personal overlay laws, numbered in sequence."""
    universal = core.UNIVERSAL_CHAT_LAW
    personal = core.load_personal_law()
    combined = universal + "\n\n" + personal if personal else universal
    return core.renumber_laws(combined)


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        sys.exit(0)
    if payload.get("stop_hook_active"):  # never loop
        sys.exit(0)
    text = turn_text(payload.get("transcript_path", ""))
    if len(text.strip()) < MIN_CHARS:
        sys.exit(0)
    offences, error = core.judge(text, chat_law(), surface="one person's working chat")
    if error:
        # Stand down loudly enough that a silent net is read rather than trusted [SPEC INV-202].
        sys.stderr.write("register-judge stood down: %s\n" % error)
        sys.exit(0)
    if not offences:
        sys.exit(0)
    reason = core.block_reason(offences, header="REGISTER JUDGE")
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
