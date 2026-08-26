"""The waiting list keeps what waits for his eyes, and nothing on it is ever lost
(SPEC INV-206, ROADMAP 408).

Chat is a display and it scrolls, so a question parked for the person and an answer he never saw both
evaporate. The board — `WAITING.md` at the host root — holds them, and chat renders it. An item clears
on his acknowledgement alone (never auto-expired, which would lose an unread item — his 2026-07-17 ~15:57
correction). The bound governs only the shown set (cap 12); the list and the attic are unbounded. When
the shown set is full and a new item arrives, the oldest shown item demotes into the list whole and
alive, and a superseded or cleared item moves to the attic with a manifest line (base rule 10).

The gate `guardrails/check-board.py` reds three violations: a closing report that omits a still-open
item; a demotion with no matching line (a silent loss); an over-cap shown set. A genuine board passes
quiet.
"""
import os
import subprocess

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "check-board.py")
FIXTURES = os.path.join(ROOT, "guardrails", "board-fixtures")
BOARD = os.path.join(ROOT, "WAITING.md")


def _gate(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def _fix(name):
    return os.path.join(FIXTURES, name)


# --- the board file ships and declares its touchpoint ---

def test_board_declares_its_touchpoint():
    text = read("WAITING.md")
    assert "TOUCHPOINT-KIND: waiting-list" in text, "the board does not declare its touchpoint kind"


def test_board_has_the_four_regions():
    text = read("WAITING.md")
    for marker in ("board:shown", "board:list", "board:attic", "board:demotions"):
        assert marker in text, "the board is missing region marker %r" % marker


# --- the gate ships and is wired in ---

def test_gate_wired_into_pre_push():
    pre_push = read("guardrails/pre-push")
    assert "check-board.py" in pre_push, "pre-push does not wire the board gate"


# --- the three red conditions ---

def test_gate_reds_a_demotion_with_no_matching_line():
    # RED-FIRST: an item recorded as demoted that is accounted for nowhere on the board = a silent loss.
    r = _gate("--board", _fix("board-demoted-absent.md"))
    assert r.returncode != 0, "gate passed a demotion with no matching list line"
    assert "INV-206" in (r.stdout + r.stderr)
    assert "w-002" in (r.stdout + r.stderr)


def test_gate_reds_an_over_cap_shown_set():
    # RED-FIRST: thirteen items shown at once, when the design demotes the oldest instead.
    r = _gate("--board", _fix("board-over-cap.md"))
    assert r.returncode != 0, "gate passed an over-cap shown set"
    assert "INV-206" in (r.stdout + r.stderr)
    assert "cap" in (r.stdout + r.stderr).lower()


def test_gate_reds_a_closing_report_that_omits_an_open_item():
    # RED-FIRST: a closing note omitting an item still open on the board.
    r = _gate("--board", _fix("board-genuine.md"), "--report", _fix("closing-note-omits-open.md"))
    assert r.returncode != 0, "gate passed a closing report that omits an open item"
    assert "INV-206" in (r.stdout + r.stderr)
    assert "w-002" in (r.stdout + r.stderr)


# --- the parked-question arm: a parked question carries a default, or the work stalls (INV-229, ROADMAP 409) ---

def test_gate_reds_a_parked_question_with_no_default():
    # RED-FIRST: a board item marked as a parked question ([[park]]) that records no default is a
    # stalled question wearing a parked question's clothes (INV-4 — the lane never parks on a proposal).
    r = _gate("--board", _fix("board-parked-no-default.md"))
    assert r.returncode != 0, "gate passed a parked question carrying no default"
    assert "INV-229" in (r.stdout + r.stderr)
    assert "w-101" in (r.stdout + r.stderr)


def test_gate_passes_a_parked_question_naming_its_default():
    r = _gate("--board", _fix("board-parked-with-default.md"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_spec_states_the_parked_default_law():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-229" in spec
    assert "default" in spec.lower()


def test_formal_index_row_for_parked_default():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-229 |" in spec


def test_architecture_owns_the_parked_default_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-229" in arch


def test_matrix_row_covers_the_parked_default_law():
    matrix = read("TEST_MATRIX.md")
    assert "INV-229" in matrix
    assert "M-410" in matrix


# --- the quiet-pass cases ---

def test_gate_passes_a_genuine_board():
    r = _gate("--board", _fix("board-genuine.md"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_a_closing_note_that_names_every_open_item():
    r = _gate("--board", _fix("board-genuine.md"), "--report", _fix("closing-note-names-all.md"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_the_real_board():
    # push mode: the repo's real WAITING.md is well-formed and loses nothing.
    r = _gate()
    assert r.returncode == 0, r.stdout + r.stderr


# --- the frame in the spec, the index, the architecture, the matrix ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-206" in spec
    assert "acknowledg" in spec.lower()  # an item clears on his acknowledgement alone


def test_formal_index_row():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-206 |" in spec


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-206" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "INV-206" in matrix
