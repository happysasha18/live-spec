"""INV-155 — a test is green only when it passes deterministically, and a flaky
test whose root is in OWNED code is a defect fixed at that root. This guard
proves the law is carried in all three text homes: the spec's green-means-
deterministic clause with its removable-in-owned-code seam question, the
build-pipeline step-8 green definition, and the test-author determinism rule.
Landed 2026-07-15."""
from pathlib import Path

# _read IS the suite's one reading node: for the spec it returns the core and every part
# the map names, and for any other file the file itself.
from conftest import read as _read

ROOT = Path(__file__).resolve().parent.parent


def test_flaky_test_is_a_defect_spec_states_the_seam():
    spec = _read("PRODUCT_SPEC.md")
    assert "removable in owned code" in spec
    assert "green means deterministic" in spec


def test_flaky_test_is_a_defect_build_pipeline_green_definition():
    bp = _read("skills/build-pipeline/SKILL.md")
    assert "deterministic" in bp
    assert "INV-155" in bp


def test_flaky_test_is_a_defect_test_author_determinism_rule():
    ta = _read("skills/test-author/SKILL.md")
    assert "deterministic" in ta
    assert "INV-155" in ta
