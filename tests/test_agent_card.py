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

# Rule 1 of the owner's standing rules is load-bearing code, not just prose: gate a's
# stand-down in guardrails/check-prover-record.sh cites "agent card rule 1" as its authority,
# and tests/test_deletion_only_push.py resolves R226 criterion 6's recordless exception to this
# very file. The card and the gate must state the same class, so the class is pinned here.
# The adversarial refusal of 2026-08-15 23:41 (F1–F3) narrowed it to the record directories:
# the wider class had let a range rewrite the strict test and this card while owing no record.
RECORD_DIRS = ("docs/prover/", "docs/skill-review/", "docs/language-reads/")
OUT_OF_CLASS_DIRS = (".live-spec/", "tests/", "guardrails/", ".github/workflows/")

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


def _standing_rule_1(text):
    """Rule 1's own text: from the numbered `1.` under the standing-rules heading to `2.`."""
    m = re.search(r"^## The owner's standing rules.*$", text, re.M)
    assert m, "the card carries no standing-rules heading"
    rest = text[m.end():]
    one = re.search(r"^1\. (.*?)(?=^2\. )", rest, re.M | re.S)
    assert one, "the standing-rules section carries no rule 1"
    return " ".join(one.group(1).split())


def test_rule_1_names_the_three_record_directories():
    rule = _standing_rule_1(read(CARD))
    for d in RECORD_DIRS:
        assert d in rule, (
            "the card's rule 1 does not name the record directory %r, so the card and gate a's "
            "stand-down no longer state the same class" % d)


def test_rule_1_exempts_nothing_beyond_the_record_directories():
    """The teeth: enforcement machinery never rides its own exemption. Rule 1 naming any of
    these would put the rules card, the suite or the gates back inside the recordless class the
    refusal of 2026-08-15 23:41 took them out of."""
    rule = _standing_rule_1(read(CARD))
    for d in OUT_OF_CLASS_DIRS:
        assert d not in rule, (
            "the card's rule 1 names %r, which left the recordless class: a range touching it "
            "would owe no record while changing what a record must hold" % d)


def test_rule_1_carries_the_phrase_the_spec_test_resolves():
    """tests/test_deletion_only_push.py resolves criterion 6's `recordless` exception by finding
    `earns no record` in this card. The phrase is the join between the two documents."""
    assert "earns no record" in _standing_rule_1(read(CARD)), (
        "rule 1 drops the phrase R226 criterion 6's mechanism map resolves against")


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


def test_section_carries_the_leaves_unread_sentence():
    body = _section(read(CARD))
    assert "leaves unread" in body, (
        "the section drops the sentence binding a format break to going unread")


def test_section_binds_the_word_to_the_format():
    body = _section(read(CARD))
    assert "попугаи" in body, "the section drops the попугаи word"
    assert "reformulate it to this format" in body, (
        "the попугаи line no longer binds the word to this format")
