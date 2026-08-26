"""INV-141 / INV-142 — the design-review pass (similarity discovery + the echo channel).
Enshrines the pass across its homes: the design-reviewer skill, the two spec clauses and
their index rows, the ARCHITECTURE node and seams, and these matrix rows. Landed 2026-07-14.
String level against the SHIPPED files on disk (matrix M-283, M-284)."""
import os
import sys

from conftest import ROOT, read, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)

SKILL = "skills/design-reviewer/SKILL.md"


# --- the shipped skill (INV-141) ---

def test_skill_ships():
    head = "\n".join(read(SKILL).splitlines()[:10])
    assert "name: design-reviewer" in head, "frontmatter lost its name"
    assert "version:" in head, "frontmatter lost its version"
    flat = read_flat(SKILL)
    # the description carves the trigger from the prover's: design-rightness, not spec-verification
    assert "same-kind" in flat, "skill lost the same-kind grouping headline"
    assert "judge the design" in flat or "judges the design" in flat, \
        "skill lost the judge-the-design mandate"


def test_similarity_lens_ships():
    flat = read_flat(SKILL)
    for step in ("Enumerate", "Describe by role", "Propose", "parity", "the tight ask"):
        assert step in flat, "similarity lens lost the step: %s" % step
    # role sentence uses the person's action words, not the author's class names
    assert "action words" in flat, "lens lost the person's-action-words rule"


def test_inventory_never_a_rival_registry():
    flat = read_flat(SKILL)
    assert "transient" in flat, "skill lost the transient-inventory word"
    assert "never written into the surface registry" in flat, \
        "skill lost the never-a-rival-registry boundary [E-10, INV-97]"


def test_never_blocks():
    flat = read_flat(SKILL)
    assert "never hold a landing" in flat, "skill lost the never-holds-a-landing property"
    assert "no blocking defects" in flat or "produces no defects" in flat, \
        "skill lost the no-defects derivation [INV-140]"


def test_record_discipline():
    flat = read_flat(SKILL)
    assert "docs/design-review/" in flat, "skill lost the dated-record home"
    assert "per-finding outcome" in flat, "skill lost the per-finding outcome column"


# --- the confidence read and the echo channel (INV-142) ---

def test_confidence_read_two_values():
    flat = read_flat(SKILL)
    assert "confident" in flat and "likely" in flat, "skill lost the two confidence values"
    assert "spec text alone" in flat, "skill lost the confident definition (text alone)"
    assert "human's intent" in flat, "skill lost the likely definition (intent)"


def test_echo_bar_and_cap():
    flat = read_flat(SKILL).lower()
    for cond in ("one plain sentence", "whole behaviour", "no spec sentence already decides"):
        assert cond in flat, "strong-signal bar lost the condition: %s" % cond
    assert "at most three" in flat, "echo channel lost the cap of three"
    assert "strongest first" in flat, "echo channel lost the strongest-first ordering"
    assert "recommended default" in flat, "echo channel lost the recommended default"


def test_unanswered_held():
    flat = read_flat(SKILL)
    assert "unanswered" in flat, "skill lost the unanswered-ask path"
    assert "not raised again" in flat or "not re-raised" in flat, \
        "skill lost the do-not-re-fire rule [INV-130]"


def test_cross_sibling_routing_split():
    """Cross-sibling propagation routes by declaration status: a declared class (or a class-
    general sentence homed on one member) is the prover's defect [INV-125]; a genuinely
    undeclared grouping is the design review's own discovery [INV-141]. Neither pass both-claims
    it nor drops it. (Born of the tlvphotos openable-face miss, 2026-07-14.)"""
    flat = read_flat(SKILL)
    assert "routes by declaration status" in flat, \
        "skill lost the declaration-status routing split"
    assert "INV-125" in flat and "INV-141" in flat, "routing split lost its two homes"


# --- the spec clauses and index rows ---

def test_spec_clauses_stand():
    spec = read("PRODUCT_SPEC.md")
    assert "A design review reads a proven spec and judges the design behind it" in spec, \
        "SPEC lost the INV-141 clause headline"
    assert "Every design review finding carries a confidence read" in spec, \
        "SPEC lost the INV-142 clause headline"
    assert "INV-141" in spec and "INV-142" in spec, "SPEC lost the clause anchors"


def test_formal_index_rows():
    # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only, no
    # prose. Assert each row's presence and its first location; assert the "design
    # review" subject against the flattened spec body instead (both requirement
    # headlines name it — R61's and R69's — already checked in test_spec_clauses_stand).
    lines = read("PRODUCT_SPEC.md").splitlines()
    spec_flat = read_flat("PRODUCT_SPEC.md")
    first_loc = {"INV-141": "R55.4", "INV-142": "R68.2"}
    for anchor in ("INV-141", "INV-142"):
        row = next((l for l in lines if l.startswith("| %s |" % anchor)), None)
        assert row is not None, "no Formal-index row for %s" % anchor
        assert first_loc[anchor] in row, "%s index row lost its expected location" % anchor
    assert "design review" in spec_flat, "spec body lost the design-review subject"


# --- the architecture node and seams ---

def test_architecture_node_and_seams():
    arch = read("ARCHITECTURE.md")
    nodes = archformat.parse_nodes(arch)
    node = next((n for n in nodes if n.name == "design-reviewer"), None)
    assert node is not None, "ARCHITECTURE lost the design-reviewer node"
    assert "INV-141" in node.anchors_expanded and "INV-142" in node.anchors_expanded, \
        "design-reviewer node lost its owned anchors"
    flat = read_flat("ARCHITECTURE.md")
    for seam in ("spec → design review", "design review → record", "design-review ask → human"):
        assert seam in flat, "ARCHITECTURE lost the seam: %s" % seam


# --- the matrix rows sit under the node ---

def test_matrix_rows_cite_the_node():
    mat = read("TEST_MATRIX.md")
    assert "### [node: design-reviewer]" in mat, "TEST_MATRIX lost the design-reviewer block"
    rows = [l for l in mat.splitlines() if l.startswith("| M-283 |") or l.startswith("| M-284 |")]
    assert len(rows) == 2, "TEST_MATRIX lost a design-review row (want M-283, M-284)"
    assert any("INV-141" in r for r in rows) and any("INV-142" in r for r in rows), \
        "design-review matrix rows lost their anchors"


# --- the bounded prover/design-review loop (INV-154) ---

def test_fixed_point_loop_bounded_and_nonblocking():
    """INV-154 — the prover/design-review fixed-point loop is bounded and never holds a
    landing. Enshrined across its homes: the spec clause, build-pipeline's step-2 re-entry,
    the ARCHITECTURE loop seam, and matrix row M-299."""
    spec = read("PRODUCT_SPEC.md")
    assert "three progressing rounds" in spec, "SPEC lost the three-progressing-rounds cap"
    assert "without holding the landing" in spec, "SPEC lost the never-holds-a-landing property"
    assert "it converges when the design review left no open question and no new grouping" in spec \
        and "it waits when a question stands unanswered" in spec, \
        "SPEC lost the two named resting states"
    assert "it stands down when no element a person acts on exists" in spec, \
        "SPEC lost the third (stand-down) resting state"
    assert "since neither re-reads the spec on its own" in spec, \
        "SPEC lost the standing-recommendation-does-not-advance-the-loop property"
    assert "A round is one prover re-read" in spec, "SPEC lost the round definition"

    arch = read("ARCHITECTURE.md")
    assert "re-prove (the loop)" in arch, "ARCHITECTURE lost the design-review re-prove loop seam"

    mat = read("TEST_MATRIX.md")
    assert "M-299" in mat and "INV-154" in mat, "TEST_MATRIX lost the M-299/INV-154 row"
