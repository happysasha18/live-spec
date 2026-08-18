"""INV-144 — when the product and the spec diverge, the spec is the definition of correct,
and changing it is a decision. Enshrines the reconciliation triage + the ratification bar +
the forbidden move across its homes so none can silently drift out. Landed 2026-07-14."""

# _read IS the suite's one reading node: for PRODUCT_SPEC.md it returns the core and every part
# the map names, and for any other file the file itself. A local reader would have shadowed it and
# gone blind to the parts.
from conftest import external_clone_or_skip, read as _read, read_all_flat


def test_spec_states_the_definition_of_correct():
    spec = _read("PRODUCT_SPEC.md")
    assert "the spec is the definition of correct" in spec
    # the triage default: a divergence is presumed a product error, checked against the spec
    assert "defaults to a possible error in the product" in spec
    # the silent-spec path is completed and pinned
    assert "complete the spec to state the guarantee" in spec
    # the forbidden move
    assert "never silently rewritten to match the product" in spec
    assert "INV-144" in spec
    # Formal-index row
    assert "| INV-144 |" in spec


def test_prover_carries_the_divergence_pointer():
    # The divergence rule itself lives in the externalized canon (three-source disagreement,
    # closing paragraph); the INV-144 anchor is a pack fact and lives on the pack adapter's
    # pin map. The whole-surface read follows the canon wherever its reference files move.
    pack = _read("skills/product-prover-pack/SKILL.md")
    assert "INV-144" in pack
    # The tracked-adapter anchor above holds on a bare checkout; only the canon read below needs the clone.
    external_clone_or_skip()
    prover = read_all_flat("skills/product-prover/SKILL.md")
    assert "the document is the definition of correct" in prover


def test_architecture_owns_144():
    arch = _read("ARCHITECTURE.md")
    assert "INV-144" in arch


def test_matrix_row_for_144():
    matrix = _read("TEST_MATRIX.md")
    assert "INV-144" in matrix
