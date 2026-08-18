"""INV-145 — a periodic full audit catches the drift no lint names.
Two layers (continuous lints on every push + a full audit on a landing-count
cadence beside the milestone gate) across the rule's homes, so none can drift
back out. Landed 2026-07-14."""
from pathlib import Path

from conftest import read as _read, read_all

ROOT = Path(__file__).resolve().parent.parent


def test_base_rule_states_periodic_full_audit():
    base = _read("skills/live-spec-base/SKILL.md")
    assert "28. **A periodic full audit catches the drift no lint names" in base
    # the two layers
    assert "continuous lints" in base
    assert "every ten landings since the last full" in base
    # host-settable cadence
    assert "a host may set its own count on its word" in base
    # an audit is adversarial by nature
    assert "adversarial by" in base and "sets out to break the work, refute its claims, and find its holes" in base


def test_spec_invariant_145_present_and_indexed():
    spec = _read("PRODUCT_SPEC.md")
    # the rhythm clause
    assert "A periodic full audit catches the drift no lint names" in spec
    # the tag now always rides grouped with sibling codes, never solo
    assert "INV-145" in spec
    # the cadence and the reset
    assert "every ten landings since the last full audit" in spec
    assert "reset the counter at a milestone gate" in spec
    # index row (location-only, SPEC INV-271); the "Rhythm" home lived in the old
    # Formal-index homes column, now gone — the row's existence is what's checked,
    # the class's own heading (already asserted above) carries the prose.
    for line in spec.splitlines():
        if line.startswith("| INV-145 |"):
            return
    raise AssertionError("no index row for INV-145")


def test_architecture_owns_145():
    arch = _read("ARCHITECTURE.md")
    assert "INV-145" in arch
    # owned by the base-rulebook node with a rule-28 pin
    assert "rule 28, INV-145" in arch


def test_matrix_row_for_145():
    for line in _read("TEST_MATRIX.md").splitlines():
        if line.startswith("| M-") and "INV-145" in line:
            return
    raise AssertionError("no matrix row cites INV-145")


def test_audit_is_defined_adversarial_by_nature_once():
    """C8: 'audit' is defined once as adversarial by nature (INV-46 clause),
    and the redundant 'adversarial audit' qualifier is gone from build-pipeline."""
    spec = _read("PRODUCT_SPEC.md")
    assert "carries an audit — a whole-read that sets out to break the work" in spec
    pipe = read_all("skills/build-pipeline/SKILL.md")
    assert "adversarial audit" not in pipe
    assert "An audit is adversarial by nature" in pipe
