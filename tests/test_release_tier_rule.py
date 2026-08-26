"""A release's number reports what taking it costs a host, and the minor-versus-major-versus-patch
call is a stated judgment held by no gate (SPEC INV-217, ROADMAP 407).

The owner asked for this guidance on 2026-07-17 ~15:45: he wanted to know when a release earns a
minor bump and when a major one, saying it would be useful, since every release so far had picked
its number by the session's feel with the rule written nowhere. The minor-versus-major call reads
meaning a machine cannot, so the rule stays a stated guidance rather than a blocking gate — a
judgment is never a gate. This is a traceability test that the guidance stands in each of its
homes: the base rulebook a host reads, the spec's formal clause and index, the architecture's
owning node, build-pipeline's release step, and the matrix. Red-proven against the pre-delta tree
(2026-07-18): none of these homes carried the release-tier rule before this landing.
"""
from conftest import read, read_flat


def test_base_rulebook_states_the_release_tier_rule():
    # base rule 32, which restated this three-tier clause, was cut 2026-08-26 (PLAN.md
    # step 7, commit 0ae778bc, moved to attic/live-spec-base-unbacked-rules-2026-08-26.md):
    # no eval fixture or executable script enforced its exact wording. TEST_MATRIX.md row
    # M-398 still cites this function as part of INV-217's owning-test set, so the check
    # stays under this name, repointed at the SPEC's own three-tier criteria (Requirement
    # 274) — the fact the base rulebook restatement is now the sole home for, in the wake
    # of that cut, per the SPEC's own criterion 7 (which still names the base rulebook as
    # a home, a pointer the rulebook itself no longer answers — see report).
    spec = read_flat("PRODUCT_SPEC.md")
    assert "[INV-217]" in spec
    for tier_fact in ("which the host takes by doing nothing",
                       "which the host takes by re-running its catch-up walk",
                       "ship its dated migration chapter"):
        assert tier_fact in spec


def test_base_rule_says_it_is_a_judgment_not_a_gate():
    # base rule 32 also restated this judgment-not-a-gate clause; see the note above.
    # TEST_MATRIX.md row M-398 still cites this function, so the check stays under this
    # name, repointed at the SPEC's own statement (Requirement 274, criterion 6).
    spec = read_flat("PRODUCT_SPEC.md")
    assert "held by no gate" in spec
    assert "the releasing session applies and names" in spec


def test_spec_states_the_law():
    spec = read_flat("PRODUCT_SPEC.md")
    assert "[INV-217]" in spec
    assert "what taking it costs a host" in spec
    # the clause names its homes
    assert "in the base rulebook" in spec


def test_formal_index_row():
    assert "| INV-217 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-217" in arch


def test_build_pipeline_release_step_points_to_the_rule():
    # the commit & show step's release-tier pointer moved to director's landing-law
    # reference, alongside the other facts build-pipeline's fixed steps used to carry.
    law = read("skills/director/references/landing-law.md")
    assert "INV-217" in law


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "| M-398 |" in matrix
    assert "INV-217" in matrix
