"""INV-170 — a surface add re-verifies the document's quantified claims against the grown set.

A new surface falsifies EXISTING document-level sentences without touching them: a class clause's
member enumeration now silently excludes the newcomer, an "every"/"only"/"all"/"exactly" sentence
ranges over a set that grew, a previously terminal scenario's decided edge may no longer be
terminal. None of these are seams the new surface composes across, so the seam-scoped CROSS-LINK
mode missed them and the whole-doc property sweep it skips is where they would have been caught.
CROSS-LINK now carries the quantifier re-verify as its one mandatory whole-doc step.

These tests assert the spec states the law and the prover skill's CROSS-LINK mode carries it.
"""
from conftest import external_clone_or_skip, read


def test_spec_states_the_quantifier_reverify():
    spec = read("PRODUCT_SPEC.md")
    assert "re-verifies the document's quantified claims" in spec


def test_spec_names_the_staleness_vector():
    spec = read("PRODUCT_SPEC.md")
    # R66 Context: the old summarizing sentence ("a clause that names its members must grow with
    # them") is gone from the compact rewrite; the same staleness vector — an enumeration clause
    # left behind by a set that just grew — is stated in the Context's own description of the fault.
    assert "member enumeration excludes the newcomer" in spec
    assert "ranges over a set that just grew" in spec


def test_prover_skill_crosslink_carries_the_step():
    external_clone_or_skip()
    skill = read("skills/product-prover/SKILL.md")
    assert "quantifier re-verify" in skill
    # the INV-170 anchor is a pack fact: the externalized canon carries no project codes,
    # so the pack adapter's pin map binds the code to the quantifier re-verify.
    pack = read("skills/product-prover-pack/SKILL.md")
    assert "INV-170" in pack


def test_index_row_present():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-170 |" in spec
