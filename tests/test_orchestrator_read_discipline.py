"""INV-137 / base rule 25 — the orchestrator reads to decide; discovery reads go to workers.
Enshrines the read-discipline law across its homes so it cannot silently drift out.
Landed 2026-07-13."""

from conftest import read as _read, read_all


def test_base_rule_states_read_discipline():
    text = _read("skills/live-spec-base/SKILL.md")
    assert "reads to decide; discovery reads go to workers" in text
    # promoted to its own numbered rule, not a buried clause
    assert "25. **The seat reads to decide; discovery reads go to workers" in text
    assert "SPEC INV-137" in text


def test_spec_invariant_137_present_and_indexed():
    spec = _read("PRODUCT_SPEC.md")
    # prose clause (Requirement 210's own heading carries the same meaning)
    assert "reads to decide and dispatches the discovery reads" in spec
    assert "INV-137" in spec
    # Formal-index row (a table row starting with the code)
    assert "| INV-137 |" in spec


def test_delegation_accounting_names_reads():
    # the discipline is made visible in the landing report's delegation accounting
    # delegation-protocol.md now lives in skills/build-pipeline/references/: the landing report is
    # written at close, which the q-822 classifier/pipeline split moved out of Director.
    bp = read_all("skills/build-pipeline/SKILL.md")
    assert "reads dispatched" in bp
    assert "INV-137" in bp


def test_architecture_owns_137():
    arch = _read("ARCHITECTURE.md")
    assert "INV-137" in arch


def test_matrix_row_for_137():
    matrix = _read("TEST_MATRIX.md")
    assert "INV-137" in matrix
