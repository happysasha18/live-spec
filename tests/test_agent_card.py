"""The card's "How a session speaks to the owner" section points at the owner's format and states
none of it.

Until 2026-08-31 this section wrote the format out in full — five numbered parts, a ten-line cap,
the "leaves unread" consequence, the попугаи word — and this test pinned all of that here. Two
other homes carried the same format in different words (the owner's boot file and his personal
profile), and this copy had already drifted from the profile on what counts as a real-world unit.
plan-16 converged them: the format's one home is `~/.claude/playbook/CLAUDE.md`, section "How a
reply to him looks", which lives in the owner's personal layer and outside this repository, so
the suite can check that the card points there and repeats nothing — which is what it now does.

The card's standing rules are untouched: rule 1 is load-bearing for a gate, and its checks below
stand as they were.

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

# The home the card must name, and the words that would mean it had started stating the format
# again instead of pointing at it.
FORMAT_HOME = "~/.claude/playbook/CLAUDE.md"
FORMAT_HOME_SECTION = "How a reply to him looks"
RESTATEMENT_PHRASES = (
    "recommendation and its reason",
    "external review's verdict",
    "leaves unread",
    "ten lines at most",
    "10 lines",
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


def test_section_names_the_one_home():
    body = _section(read(CARD))
    assert FORMAT_HOME in body, (
        "the section does not name %r, so a reader has nowhere to go for the format"
        % FORMAT_HOME)
    assert FORMAT_HOME_SECTION in body, (
        "the section names the file but not the section %r inside it" % FORMAT_HOME_SECTION)


def test_section_states_no_second_copy_of_the_format():
    body = _section(read(CARD)).lower()
    for phrase in RESTATEMENT_PHRASES:
        assert phrase not in body, (
            "the section states the format again (%r) instead of pointing at its one home" % phrase)
    assert not re.search(r"^\d\.", _section(read(CARD)), re.M), (
        "the section carries a numbered list again — the format's parts belong to its one home")


def test_section_says_what_to_do_when_the_home_cannot_be_read():
    body = _section(read(CARD)).lower()
    assert "cannot read" in body, (
        "the section does not say what a session does when the home is unreadable, so a session "
        "with no access to it would invent a format of its own")
