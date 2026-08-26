"""INV-179 — the upstream note is anonymized before it leaves the draft.

A host's real entities (names, company, internal repos, paths, customer data) become neutral
role words IN the draft the user reads at consent — so what they approve is exactly what would
travel; a note masked after the yes is a different note from the approved one. Enterprise hosts
are why this is law rather than taste.
"""
from conftest import read


def test_collector_masks_host_entities():
    s = read("skills/feedback-collector/SKILL.md")
    assert "anonymized" in s
    assert "masked before the note leaves the draft" in s


def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-179 |" in spec
