"""INV-168 — every stated transition triggers the prover's standing transition-payload lens.

For every transition the spec states, the parameters a person perceives across it must be enumerated:
where focus and selection land, what scroll or playback position holds, whether sound continues,
whether a timer keeps running, whether a shown value is fresh or stale. A parameter the spec leaves
blank is answered by the platform default alone, and a default that silently becomes the behaviour
leaves the topology lenses no written text to read. The motion-parity lens [INV-165] and the
entry-state lens [INV-167] are instances this parent lens generalizes.

These tests assert the spec states the lens and the product-prover skill carries it, so the standing
lens is real text a reviewer runs by construction rather than a note in a journal.
"""
from conftest import external_clone_or_skip, read, read_all


def test_spec_states_the_transition_payload_lens():
    spec = read("PRODUCT_SPEC.md")
    assert "carries a payload lens" in spec


def test_prover_skill_carries_the_lens():
    # whole-surface read: the canon carries this lens in reference/stress-lenses.md
    external_clone_or_skip()
    skill = read_all("skills/product-prover/SKILL.md")
    assert "**Transition payload**" in skill
    assert "answered by the platform default" in skill


def test_spec_names_the_instances():
    spec = read("PRODUCT_SPEC.md")
    assert "instances this parent generalizes" in spec
    assert "INV-165" in spec
    assert "INV-167" in spec


def test_index_row_present():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-168 |" in spec
