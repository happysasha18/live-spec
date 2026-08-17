"""A release note may offer the reader appealing next steps for their own choice
(SPEC INV-228, ROADMAP 402).

A GitHub changelog / release note may offer the reader next-step CHOICES — appealing things the
reader may do next, phrased as choices and never instructions. The publish skill's release-note
shape carries the offers section as OPTIONAL, and the publish walk RECORDS the offer-or-none
decision: a release-note record that neither offers a next step nor records "no offer" reds, and one
that offers or records "none" passes.

The touchpoint frame [INV-205] already classifies this surface: the release note is the human-audience,
no-answer-needed kind — an asynchronous, person-opened point (he reads it when he opens the release
notes himself), so an offer (a teaching-adjacent line) is afforded and an interruption is not. This
movement consumes that classification; it does not re-open the frame.

The checker `guardrails/attic/check-release-note.py` reds a record that leaves the offer-or-none
decision unrecorded and passes one that offers or records "none". It rides the suite and NOT the push
chain: the release note the walk produces is a process artifact the walk records at runtime, and no
committed release-note file exists in the tree for a push gate to scan (the sibling of the far-tier
report-shape check, SPEC INV-83). It was parked in the attic on 2026-08-18 with its fixtures beside
it, having only ever read those fixtures; this suite still drives it there, and the test below still
holds it out of the push chain.
"""
import os
import subprocess

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "attic", "check-release-note.py")
FIXTURES = os.path.join(ROOT, "guardrails", "attic", "release-note-fixtures")


def _gate(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def _fix(name):
    return os.path.join(FIXTURES, name)


# --- the checker ships ---

def test_gate_ships():
    assert os.path.isfile(GATE), "guardrails/attic/check-release-note.py missing"


# --- the red condition: the offer-or-none decision left unrecorded ---

def test_gate_reds_a_note_recording_neither():
    # RED-FIRST: a release note that neither offers a next step nor records "no offer".
    r = _gate("--note", _fix("note-neither.md"))
    assert r.returncode != 0, "gate passed a note that records neither an offer nor 'no offer'"
    assert "INV-228" in (r.stdout + r.stderr)


# --- the quiet-pass cases ---

def test_gate_passes_a_note_that_offers():
    r = _gate("--note", _fix("note-offers.md"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_a_note_that_records_no_offer():
    r = _gate("--note", _fix("note-no-offer.md"))
    assert r.returncode == 0, r.stdout + r.stderr


# --- it rides the suite, not the push chain ---

def test_checker_not_wired_into_pre_push():
    pre_push = read("guardrails/pre-push")
    assert "check-release-note.py" not in pre_push, (
        "the release-note check must ride the suite, not the push chain — no committed release-note "
        "file exists for a push gate to scan (INV-83)")


# --- the publish skill's release-note shape carries the optional offers section ---

def test_publish_skill_carries_the_offers_section():
    pub = read("skills/publish/SKILL.md")
    assert "offers section" in pub.lower(), "the publish release-note shape names no offers section"
    assert "INV-228" in pub, "the publish release-note shape does not cite INV-228"


def test_publish_skill_records_offer_or_none():
    pub = read("skills/publish/SKILL.md").lower()
    # the walk records the offer-or-none decision (offer, or a recorded 'none').
    assert "offer-or-none" in pub or ("offer" in pub and "no offer" in pub)


# --- the touchpoint frame already classifies the surface (consumed, not re-opened) ---

def test_touchpoint_manifest_classifies_the_release_note():
    import json
    with open(os.path.join(ROOT, "guardrails", "touchpoints.json")) as f:
        data = json.load(f)
    entry = next(t for t in data["touchpoints"] if t["name"] == "release-note")
    assert entry["kind"] == "asynchronous"
    assert entry["opened_by"] == "person"
    assert entry.get("row") == "402"


# --- the frame in the spec, the index, the architecture, the matrix ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-228" in spec
    assert "offers section" in spec.lower()


def test_formal_index_row():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-228 |" in spec


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-228" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "INV-228" in matrix
    assert "M-409" in matrix
