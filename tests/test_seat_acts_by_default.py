"""INV-143 / base rule 27 — the orchestrator decides what it can decide, and surfaces
only what it cannot. Enshrines the default-action posture across its homes so it cannot
silently drift out. Landed 2026-07-14."""

# _read IS the suite's one reading node: for the spec it returns the core and every part
# the map names, and for any other file the file itself.
from conftest import read as _read


def test_base_rule_states_the_default_action_posture():
    text = _read("skills/live-spec-base/SKILL.md")
    # promoted to its own numbered rule, not a buried clause
    assert "27. **The orchestrator decides what it can decide" in text
    assert "SPEC INV-143" in text
    # the anti-stall clause is load-bearing
    assert "never parks derivable work" in text
    # survives-a-wipe scope
    assert "after a memory wipe" in text


def test_spec_invariant_143_present_and_indexed():
    spec = _read("PRODUCT_SPEC.md")
    assert "decides what it can decide" in spec
    assert "surfaces only what it cannot" in spec
    assert "never park derivable work on the human's queue" in spec
    assert "INV-143, INV-4]" in spec
    # Formal-index row (a table row starting with the code)
    assert "| INV-143 |" in spec


def test_architecture_owns_143():
    arch = _read("ARCHITECTURE.md")
    assert "INV-143" in arch


def test_matrix_row_for_143():
    matrix = _read("TEST_MATRIX.md")
    assert "INV-143" in matrix
