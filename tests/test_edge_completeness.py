"""INV-138 — a gated behaviour names every side of its gate.
Both ends of a threshold-gated transition + the three states of an async slot.
Enshrines the law across its six homes. Landed 2026-07-13."""
from conftest import external_clone_or_skip, read, read_all_flat

# Two readers, and which one a check gets is decided by WHO OWNS THE LINE BREAKS.
#
# `tracked` is the raw bytes. A document this repository owns is matched exactly as it is
# written, so a needle only counts when it stands whole on the page — the locality the
# check was written to have. Flattening a tracked document lets a phrase match across an
# arbitrary line break and across any indentation, which quietly widens every assertion in
# the file; the re-pinning packet had swapped these reads to the flat one and this restores
# them (fresh review finding 2).
#
# `canon` is the flat whole-surface read, and it is used for exactly one home: the
# externalized product-prover canon. That is another repository's file. This pack does not
# own its wrapping and must not red because the canon re-flowed a paragraph, so a
# cross-line match is the correct bar there and nowhere else. The boundary is ownership,
# not convenience.
tracked = read
canon = read_all_flat


def test_the_tracked_reader_stays_locality_sensitive():
    """The flattening cannot come back by accident.

    `read_all_flat` collapses every whitespace run, so its result can never contain a
    newline. Asserting that the tracked reader's output does contain one pins the raw
    read mechanically, rather than trusting the name at the top of the file.
    """
    assert "\n" in tracked("PRODUCT_SPEC.md"), (
        "the tracked reader returned no newline: a flattened read has been wired back in "
        "and every needle in this file now matches across line breaks"
    )
    assert "\n" not in canon("skills/product-prover-pack/SKILL.md"), (
        "the canon reader must be the flat one — this assertion also proves the two "
        "readers above are genuinely different functions, not the same one twice"
    )


def test_spec_clause_stands():
    spec = tracked("PRODUCT_SPEC.md")
    assert "A gated behaviour names both ends of its range" in spec
    assert "[INV-138]" in spec


def test_spec_names_both_faces():
    spec = tracked("PRODUCT_SPEC.md")
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
    sa = tracked("skills/spec-author/SKILL.md")
    assert "Edge completeness" in sa
    assert "the three faces of a wait" in sa


def test_prover_carries_the_edge_completeness_lens():
    # the INV-138 anchor is a pack fact: the pack adapter's pin map carries it against the lens
    pack = read("skills/product-prover-pack/SKILL.md")
    assert "INV-138" in pack
    # The tracked-adapter anchor above holds on a bare checkout; only the canon read below needs the clone.
    external_clone_or_skip()
    pp = canon("skills/product-prover/SKILL.md")
    assert "Edge-condition completeness" in pp
    assert "both ends of the range" in pp


def test_matrix_row_covers_edge_completeness():
    for line in read("TEST_MATRIX.md").splitlines():
        if line.startswith("| M-") and "INV-138" in line:
            return
    raise AssertionError("no matrix row cites INV-138")
