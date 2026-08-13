"""INV-138 — a gated behaviour names every side of its gate.
Both ends of a threshold-gated transition + the three states of an async slot.
Enshrines the law across its six homes. Landed 2026-07-13."""
from conftest import external_clone_or_skip, read, read_all_flat


def _flat(rel):
    # the conftest whole-surface flat read: a skill's reference/*.md offload is part of its
    # surface, and a needle that wraps a source line still matches.
    return read_all_flat(rel)


def test_spec_clause_stands():
    spec = _flat("PRODUCT_SPEC.md")
    assert "A gated behaviour names both ends of its range" in spec
    assert "[INV-138]" in spec


def test_spec_names_both_faces():
    spec = _flat("PRODUCT_SPEC.md")
    assert "below the low end" in spec
    assert "above the high end" in spec
    assert "pending, arrived, and failed" in spec
    assert "visible pending" in spec


def test_formal_index_row():
    # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
    # The "gate" subject is asserted against the spec body in test_spec_clause_stands.
    for line in read("PRODUCT_SPEC.md").splitlines():
        if line.startswith("| INV-138 |"):
            assert "R52.1" in line
            return
    raise AssertionError("no Formal-index row for INV-138")


def test_spec_author_carries_the_facet():
    sa = _flat("skills/spec-author/SKILL.md")
    assert "Edge completeness" in sa
    assert "the three faces of a wait" in sa


def test_prover_carries_the_edge_completeness_lens():
    external_clone_or_skip()
    pp = _flat("skills/product-prover/SKILL.md")
    assert "Edge-condition completeness" in pp
    assert "both ends of the range" in pp
    # the INV-138 anchor is a pack fact: the pack adapter's pin map carries it against the lens
    pack = read("skills/product-prover-pack/SKILL.md")
    assert "INV-138" in pack


def test_matrix_row_covers_edge_completeness():
    for line in read("TEST_MATRIX.md").splitlines():
        if line.startswith("| M-") and "INV-138" in line:
            return
    raise AssertionError("no matrix row cites INV-138")
