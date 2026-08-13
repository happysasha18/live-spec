"""INV-140 — the prover labels each finding a defect or a recommendation.
Enshrines the finding-kind reporting rule across its homes. Landed 2026-07-13."""
from conftest import external_clone_or_skip, read, read_all_flat


def _flat(rel):
    # the conftest whole-surface flat read: a skill's reference/*.md offload is part of its
    # surface, and a needle that wraps a source line still matches.
    return read_all_flat(rel)


def test_prover_tag_carries_kind():
    external_clone_or_skip()
    pp = _flat("skills/product-prover/SKILL.md")
    assert "kind · plain-label (formal-term)" in pp
    # the canon's worked example changed with the parcel-locker rewrite; the tag shape holds
    assert "defect · partial-success-risk (atomicity)" in pp


def test_severity_axis_retired_from_prover():
    """kind is the sole verdict axis: the old three-level severity vocabulary
    is gone from the prover's tag and rule surface (INV-140 collapse)."""
    external_clone_or_skip()
    pp = _flat("skills/product-prover/SKILL.md")
    for token in ("must-fix", "should-clarify", "worth-considering"):
        assert token not in pp, f"retired severity token {token!r} still in prover SKILL"


def test_severity_axis_retired_from_spec_and_readme_case_insensitive():
    """The retired three-level severity vocabulary is gone from the two most
    visible normative surfaces — case-insensitively, so a capital 'Must-fix'
    cannot survive again (D1/D2 defect class, INV-140 single-axis collapse)."""
    import re
    tokens = ("must-fix", "should-clarify", "should-fix", "nice-to-have", "worth-considering")
    pat = re.compile("|".join(re.escape(t) for t in tokens), re.IGNORECASE)
    for rel in ("PRODUCT_SPEC.md", "README.md"):
        hits = [m.group(0) for m in pat.finditer(_flat(rel))]
        assert hits == [], f"retired severity token(s) still in {rel}: {hits}"


def test_push_gate_folds_on_kind():
    """M-6 folds on kind, not on a separate severity level."""
    spec = _flat("PRODUCT_SPEC.md")
    assert "fold every defect and queue every recommendation" in spec
    # the externalized canon says "pre-merge check" where the pack says "push gate" (the pack
    # adapter's own description keeps the push-gate name); the kind-folding semantics hold.
    external_clone_or_skip()
    pp = _flat("skills/product-prover/SKILL.md")
    assert "A defect blocks. It is applied to the document at the pre-merge check" in pp


def test_prover_defines_defect_and_recommendation():
    external_clone_or_skip()
    pp = _flat("skills/product-prover/SKILL.md")
    assert "a stated invariant is violated" in pp
    # "taste call" became "judgment call" in the canon's rewrite; the queue semantics hold
    assert "queues for a judgment call" in pp
    assert "`defect`" in pp and "`recommendation`" in pp


def test_spec_clause_stands():
    spec = _flat("PRODUCT_SPEC.md")
    assert "The prover labels each finding a defect or a recommendation" in spec
    assert "[INV-140]" in spec


def test_formal_index_row():
    text = read("PRODUCT_SPEC.md")
    for line in text.splitlines():
        if line.startswith("| INV-140 |"):
            # the index row is location-only (SPEC INV-271); the "defect" prose lives on the body
            assert "label a finding a defect" in text
            return
    raise AssertionError("no Formal-index row for INV-140")


def test_matrix_row_covers_finding_kind():
    for line in read("TEST_MATRIX.md").splitlines():
        if line.startswith("| M-") and "INV-140" in line:
            return
    raise AssertionError("no matrix row cites INV-140")


def test_architecture_owns_140():
    assert "INV-140" in _flat("ARCHITECTURE.md")
