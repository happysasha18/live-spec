"""INV-167 — a re-enterable surface triggers the prover's standing entry-state lens.

A surface a visitor can leave and re-enter must declare, in the spec, the state that re-entry OPENS IN:
where it lands focused/positioned, and whether entering resets its internal state or resumes the state a
prior visit left. Entry symmetry [INV-50] tests that a re-entry PATH exists; this tests the STATE that
path opens in. Born of a shipped bug: a series side-room reopened on the last picture a prior visit had
scrolled its lane to, instead of the first member, because no line stated the entry state (2026-07-16).

These tests assert the spec states the lens and the product-prover skill carries it, so the standing lens
is real text a reviewer runs by construction rather than a note in a journal."""
from conftest import external_clone_or_skip, read, read_all


def test_spec_states_the_entry_state_lens():
    spec = read("PRODUCT_SPEC.md")
    assert "prover's entry-state lens" in spec
    assert "resets its internal state or resumes" in spec


def test_spec_distinguishes_it_from_entry_symmetry():
    # the lens is the complement of INV-50: path-existence vs the state that path opens in. Stating the
    # distinction is what keeps it from reading as a duplicate of the entry-symmetry lens.
    spec = read("PRODUCT_SPEC.md")
    assert "entry-symmetry lens tests that a re-entry path exists" in spec


def test_prover_skill_carries_the_lens():
    # whole-surface read: the canon carries this lens in reference/stress-lenses.md
    external_clone_or_skip()
    skill = read_all("skills/product-prover/SKILL.md")
    assert "**Entry state**" in skill
    assert "reset-or-resume semantics" in skill
    # it must name what entry symmetry does NOT ask, so a reviewer applies it as a distinct lens
    assert "tests the state that path opens in" in skill


def test_index_row_present():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-167 |" in spec
