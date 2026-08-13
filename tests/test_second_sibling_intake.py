"""INV-169 — a feature delta that adds a second member of an existing kind draws the scoped
design review at intake.

The moment an undeclared same-kind grouping comes into existence is the intake of its SECOND
member — and that was exactly where the design review stood down (FEATURE-FIT drew none), so a
second sibling could enter, ship, and diverge, findable only at the next FULL pass after the
divergence was live. FEATURE-FIT now asks the second-sibling question by construction; a yes
draws the scoped design review over the delta.

These tests assert the spec states the law and both skills carry it, so the intake window is
closed in real text rather than a journal note.
"""
from conftest import read


def test_spec_states_the_second_sibling_law():
    spec = read("PRODUCT_SPEC.md")
    assert "second member of a kind an existing surface already has" in spec


def test_spec_scopes_the_stand_down():
    spec = read("PRODUCT_SPEC.md")
    # the old single paragraph fused two facts ("it stands down at the push gate" [INV-141] and
    # "at feature intake it stands down only when..." [INV-169]) into one sentence run; the
    # requirements-format rewrite splits them into R61 (general: never blocks a landing) and R63
    # (intake-specific: the second-sibling question). This needle re-pins to R61's own phrasing
    # of the same "stands down at the push gate" fact.
    assert "Its findings are recommendations or questions and never block a landing" in spec


def test_prover_skill_asks_the_question_at_intake():
    skill = read("skills/product-prover/SKILL.md")
    assert "second member of a kind an existing surface already has" in skill
    # the INV-169 anchor is a pack fact: the externalized canon carries no project codes,
    # so the pack adapter's pin map binds the code to the second-sibling question.
    pack = read("skills/product-prover-pack/SKILL.md")
    assert "INV-169" in pack


def test_design_reviewer_carries_the_exception():
    skill = read("skills/design-reviewer/SKILL.md")
    assert "second member" in skill
    assert "INV-169" in skill


def test_index_row_present():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-169 |" in spec
