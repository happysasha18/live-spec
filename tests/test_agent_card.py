"""The card's "How a session speaks to the owner" section carries the owner's dictated format
(agent card, 2026-08-15): five numbered parts, a ten-line cap, a "leaves unread" consequence for
breaking the format, and the попугаи word bound to that same format rather than to a looser
"say it again" reading.

The section once read as a plain four-item bullet list (see the parent commit 39e393c) with no
numbered parts, no recommendation, no irreversibility line, no external-review line, and a
попугаи line that only asked for a rewording, not a reformulation to this format. This test
reds against that shape and passes against the current card.

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest tests/test_agent_card.py -q
"""
import os
import re

from conftest import ROOT, read

CARD = os.path.join(ROOT, ".live-spec", "agent.md")
HEADING = "## How a session speaks to the owner"

STABLE_PHRASES = (
    "what it changes",
    "recommendation and its reason",
    "irreversible",
    "external review's verdict",
    "real world",
)


def _section(text):
    """The body of the "How a session speaks to the owner" section: from its heading to the
    next `## ` heading, or end of file."""
    m = re.search(r"^## How a session speaks to the owner\s*$", text, re.M)
    assert m, "the card carries no 'How a session speaks to the owner' heading"
    start = m.end()
    rest = text[start:]
    nxt = re.search(r"^## ", rest, re.M)
    body = rest[:nxt.start()] if nxt else rest
    return body


def test_card_ships():
    assert os.path.isfile(CARD), ".live-spec/agent.md missing"


def test_section_carries_the_five_numbered_parts():
    body = _section(read(CARD))
    for n in range(1, 6):
        assert re.search(r"^%d\." % n, body, re.M), (
            "the section carries no numbered part %d" % n)


def test_section_carries_the_stable_phrases():
    body = _section(read(CARD)).lower()
    for phrase in STABLE_PHRASES:
        assert phrase in body, (
            "the section drops the stable phrase %r" % phrase)


def test_section_carries_the_ten_line_cap():
    body = _section(read(CARD))
    assert "Ten lines at most." in body, (
        "the section drops the ten-line cap sentence")


def test_section_carries_the_leaves_unread_sentence():
    body = _section(read(CARD))
    assert "leaves unread" in body, (
        "the section drops the sentence binding a format break to going unread")


def test_section_binds_the_word_to_the_format():
    body = _section(read(CARD))
    assert "попугаи" in body, "the section drops the попугаи word"
    assert "reformulate it to this format" in body, (
        "the попугаи line no longer binds the word to this format")
