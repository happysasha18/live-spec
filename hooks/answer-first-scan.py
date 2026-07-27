#!/usr/bin/env python3
"""Stop-hook: flag a chat reply that opens with a wall instead of a short lead (SPEC INV-220).

The answer-first law (the personal profile's `language.answer-first`, PERMANENT) says every reply OPENS
with its answer — the outcome, the decision, or the finding — in a few lines the reader may stop at, with
reasoning and evidence underneath. A stated law with no machine is a wish (live-spec base rule 30), so
this arm is the machine that HOLDS it, the sibling of the scissors scan (scissors-scan.py) on the same
Stop event.

Whether a text "opens with the answer" is undecidable, so this arm reds a MEASURABLE PROXY of the shape
the law names: a reply OVER a length threshold whose OPENING BLOCK (its first paragraph, up to the first
blank line) is a long wall carrying no short lead. A reply that opens with a short paragraph, a heading,
or a scannable list — anything the reader can stop at in seconds — passes.

HONEST BOUNDARY. This arm is a net for the WALL, and it is honest about what it cannot see:
  - It measures whether an opening lead is PRESENT, never whether the lead is the RIGHT answer. A short
    lead that answers the wrong question passes it — a human still reads meaning.
  - It judges the FINAL reply the human reads (the last assistant message of the turn), not the short
    inter-tool narration lines, which are not a "reply" that owes a lead.
  - It is a Stop-hook NOTICE, never a pre-push gate: a chat reply is already emitted when this fires, so
    it cannot be blocked the way a shown document is [INV-83]. It flags the previous reply and asks for a
    one-line lead-first correction, which is the most a chat surface allows — the correction reaches the
    human one message later, the reply itself already sent.

A surviving wall prints a Stop-hook block decision naming the fault; the net-meter [INV-202] reads its
runs and fires. It never blocks on its own breakage — an unreadable payload or transcript stands it down
silently. Repo home: hooks/answer-first-scan.py; installed copy: ~/.claude/hooks/ (beside scissors-scan.py).
"""
import json
import os
import re
import sys

# The length floor and the three lead signals are NOT written here. They live in
# answer-first-scan.json beside this file, which docs/language-rules.md also reads at build time, so
# the rule a writer reads and the shape this hook measures are one list and cannot drift apart. The
# installed copy sits at ~/.claude/hooks/ (declared under `data` for this hook in
# guardrails/judge-hooks.json). A missing or unreadable home stands the hook down silently, the way
# every other breakage of its own machinery does — this arm never blocks on itself.
SIGNALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "answer-first-scan.json")


def load_signals(path=None):
    """The floor and the three signals, or (None, None) when the home cannot be read."""
    try:
        with open(path or SIGNALS_PATH, encoding="utf-8") as fh:
            cfg = json.load(fh)
        floor = int(cfg["reply_chars_above_which_a_lead_is_required"])
        signals = {s["id"]: s for s in cfg["lead_signals"]}
        return floor, (int(signals["opening_sentence"]["max_chars"]),
                       int(signals["opening_block"]["max_chars"]),
                       re.compile(signals["structure"]["pattern"]))
    except (OSError, ValueError, KeyError, TypeError, re.error):
        return None, None


LENGTH_THRESHOLD, _SIGNALS = load_signals()
FIRST_SENTENCE_MAX, LEAD_MAX, _STRUCTURAL = _SIGNALS if _SIGNALS else (None, None, None)

# The first sentence ends at the first '.', '!', '?', or ':' followed by whitespace or end-of-text (so a
# decimal like "2.1" or "18%." mid-number does not end it), or at the first newline, whichever comes first.
_SENTENCE_END = re.compile(r"[.!?:](?=\s|$)|\n")

# A leading [HH:MM] timestamp (the profile's chat.timestamp habit) is part of the lead line and never
# counts against it.
_TIMESTAMP = re.compile(r"^\s*\[\d{1,2}:\d{2}\]\s*")


def last_assistant_text(transcript_path):
    """The LAST assistant message of the turn — the reply the human reads for the answer.

    One reply can arrive as several transcript events sharing one message id; every chunk of that last
    message is joined, so a lead split across chunks is measured whole (the same join scissors-scan uses).
    """
    text = ""
    last_id = None
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") != "assistant":
                    continue
                msg = ev.get("message", {})
                parts = msg.get("content", [])
                if isinstance(parts, str):
                    chunk = parts
                    mid = msg.get("id")
                else:
                    chunk = "".join(
                        p.get("text", "") for p in parts
                        if isinstance(p, dict) and p.get("type") == "text"
                    )
                    mid = msg.get("id")
                if not chunk.strip():
                    continue
                if mid and mid == last_id:
                    text += chunk
                else:
                    text = chunk
                    last_id = mid
    except OSError:
        return ""
    return text


def _strip_timestamp(text):
    return _TIMESTAMP.sub("", text.lstrip("\n"), count=1)


def opening_block(text):
    """The first paragraph: the run of non-blank lines up to the first blank line, leading blanks skipped."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    block = []
    while i < len(lines) and lines[i].strip():
        block.append(lines[i])
        i += 1
    return "\n".join(block).strip()


def _is_structural_lead(block):
    """Every non-blank line of the block opens with a structural marker — a scannable list/heading answer."""
    lines = [ln for ln in block.split("\n") if ln.strip()]
    return bool(lines) and all(_STRUCTURAL.match(ln) for ln in lines)


def first_sentence(body):
    """The opening sentence: text up to the first sentence terminator or newline, whichever comes first."""
    m = _SENTENCE_END.search(body)
    return body[: m.start() + 1].strip() if m else body.strip()


def has_lead(text):
    """True when the reply carries a short lead the reader can stop at (or is short enough to owe none).

    Fires only when a reply over the length floor fails ALL THREE lead signals — a long opening sentence,
    a long opening paragraph, and no scannable structure. Any one signal passing means a lead is present.
    """
    if LENGTH_THRESHOLD is None:
        return True  # the signal home is unreadable; the arm stands down rather than firing blind
    body = _strip_timestamp(text).strip()
    if len(body) < LENGTH_THRESHOLD:
        return True
    if len(first_sentence(body)) <= FIRST_SENTENCE_MAX:
        return True
    block = opening_block(body)
    if len(block) <= LEAD_MAX:
        return True
    if _is_structural_lead(block):
        return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    # never loop: if a prior stop-hook already fired this turn, stand down.
    if payload.get("stop_hook_active"):
        sys.exit(0)
    text = last_assistant_text(payload.get("transcript_path", ""))
    if not text or has_lead(text):
        sys.exit(0)
    reason = (
        "ANSWER-FIRST CHECK — the previous reply ran long and opened with a wall, carrying no short lead:\n"
        "  · its opening paragraph runs past the lead threshold with no early stop point.\n\n"
        "The answer-first law asks every reply to OPEN with its answer — the outcome, the decision, or the "
        "finding — in a few lines the reader may stop at, with reasoning underneath. Send a one-line lead "
        "now that states the answer up front. (This net measures only whether an opening lead is PRESENT, "
        "never whether it is the right answer; if the reply already led with its answer and this misread "
        "the shape, say so in one line and continue.)"
    )
    # suppressOutput keeps the machine's complaint off the human's screen: the hook talks to the model,
    # and what the human is owed is the lead-first correction the model then sends (as scissors-scan does).
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
