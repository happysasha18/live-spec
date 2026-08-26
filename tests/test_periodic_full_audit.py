"""INV-145 — a periodic full audit catches the drift no lint names.
Two layers (continuous lints on every push + a full audit on a landing-count
cadence beside the milestone gate) across the rule's homes, so none can drift
back out. Landed 2026-07-14."""

import os
import sys

from conftest import ROOT, read as _read, read_all

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


def test_base_rule_states_periodic_full_audit():
    # base rule 28, which restated this two-layer clause, was cut 2026-08-26 (PLAN.md
    # step 7, commit 0ae778bc, moved to attic): no eval fixture or executable script
    # enforced its exact wording. TEST_MATRIX.md row M-287 still cites this function as
    # part of INV-145's owning-test set, so the check stays under this name, repointed at
    # the SPEC's own declaration of the same two-layer clause (Requirement 131).
    spec = _read("PRODUCT_SPEC.md")
    # the two layers
    assert "The continuous lints run on every push" in spec
    assert "every ten landings since the last full audit" in spec
    # host-settable cadence
    assert "host-settable default" in spec
    # an audit is adversarial by nature
    assert "set on breaking the work, refuting its claims and finding its holes" in spec


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
    # owned by the base-rulebook node (its rule-28 pin retired with the base rule itself,
    # 2026-08-26; ownership is checked structurally now, not by a citation of that number)
    owners = [n.name for n in archformat.parse_nodes(arch) if "INV-145" in n.anchors_expanded]
    assert owners == ["base-rulebook"], "INV-145 owning node(s): %r" % owners


def test_matrix_row_for_145():
    for line in _read("TEST_MATRIX.md").splitlines():
        if line.startswith("| M-") and "INV-145" in line:
            return
    raise AssertionError("no matrix row cites INV-145")


def test_audit_is_defined_adversarial_by_nature_once():
    """C8: 'audit' is defined once as adversarial by nature (INV-46 clause),
    and the redundant 'adversarial audit' qualifier is gone from director's verify step
    (moved there from build-pipeline in the build-pipeline cutover)."""
    spec = _read("PRODUCT_SPEC.md")
    assert "carries an audit — a whole-read that sets out to break the work" in spec
    detail = read_all("skills/director/references/verify-step-detail.md")
    assert "adversarial audit" not in detail
