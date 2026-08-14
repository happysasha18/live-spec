"""feedback-collector (ROADMAP 321) — the pack's outbound feedback arm, E-30 / T-21 / INV-161.

On a rare, genuinely strong reaction the pack OFFERS (positive consent every time) to draft a short
private "upstream note" to the pack's authors, deposits it into a gitignored ``outbox/``, and never
sends — delivery is the human's own step. Off by default. Distinct from feedback-intake (the inverse
arrow) and from the measurement family (no scoring).

String-level assertions on the shipped files. Landed 2026-07-15."""
import re

from conftest import ROOT, read, read_all

SKILL = "skills/feedback-collector/SKILL.md"


def _skill():
    return read(SKILL)


def test_feedback_collector_ships():
    # SKILL.md loads with frontmatter name + version, and states the arm's shape: a rare strong-moment
    # offer that drafts an upstream note. Never a skill file missing the offer or the off-by-default flag.
    s = _skill()
    assert "name: feedback-collector" in s
    version = open("VERSION", encoding="utf-8").read().strip()
    assert "version: %s" % version in s  # stamped from the one VERSION fact (INV-178)
    assert "upstream note" in s.lower()
    assert "feedback-upstream" in s                      # the off-by-default flag is named
    # README + LICENSE ship too
    assert read("skills/feedback-collector/README.md").strip()
    assert read("skills/feedback-collector/LICENSE").strip()


def test_off_by_default_and_positive_consent():
    # Off by default (feedback-upstream: off), and consent is POSITIVE word — the deliberate opposite of
    # silence-is-consent [INV-31]. Never a silent send, never firing on a host that has not opted in.
    s = _skill().lower()
    assert "off by default" in s
    assert "feedback-upstream: on" in s                  # a host opts in by a recorded line
    assert "explicit yes" in s or "positive" in s        # positive consent, not silence
    assert "inv-31" in s                                 # names the deliberate opposite


def test_never_sends_only_deposits():
    # It DEPOSITS to a gitignored outbox/ and never opens a network connection or public request — the
    # outward act is the human's gate. Never a raw transcript/script, never a tracked/pushed note.
    s = _skill()
    low = s.lower()
    assert "outbox/" in s
    assert "gitignored" in low
    assert "never send" in low or "no network" in low or "never sends" in low
    assert "transcript" in low                           # the no-raw-material fence is stated
    # outbox/ is gitignored so a private note never rides a push
    assert "outbox/" in read(".gitignore")


def test_distinct_from_intake_and_measurement():
    # Fenced against feedback-intake (the inverse arrow — this IS the agent's own observation T-20 leaves
    # open) and against the measurement family (reads one moment, never scores/aggregates). Never an
    # analytics machine, never competing with intake for a handed-in item.
    low = _skill().lower()
    assert "feedback-intake" in low
    assert "t-20" in low                                 # the seam it occupies
    assert "measurement" in low
    assert "aggregate" in low or "score" in low          # the no-scoring fence


def test_spec_states_the_third_arrow():
    # The spec carries the third arm (register rewrite renamed "arrow" to "arm") with its three
    # anchors, and names the upstream note distinct from the two existing "digest" meanings.
    # Never an unanchored behaviour.
    spec = read("PRODUCT_SPEC.md")
    for anchor in ("E-30", "T-21", "INV-161"):
        assert re.search(r"\[[^\]\n]*\b%s\b[^\]\n]*\]" % re.escape(anchor), spec), anchor
    assert "third arm" in spec.lower()
    assert "upstream note" in spec.lower()


def test_flag_in_settings_catalog():
    # INV-87: every setting is a marked row in the package-defaults catalog. feedback-upstream lives
    # there, off by default. Never a setting named only in prose with no catalog row.
    base = read_all("skills/live-spec-base/SKILL.md")
    assert "`feedback-upstream`" in base
