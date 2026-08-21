# -*- coding: utf-8 -*-
"""An expensive decision earns an adversarial read before it lands (ROADMAP row 395, SPEC INV-235).

Agent birth [T-22] says the owner ratifies a new agent, and says nothing about what he ratifies ON:
the proposal names the capability, the zone, and the contracts, and it carries no adversarial read.
The class of EXPENSIVE decisions — the ones whose reversal costs more than the decision itself — has no
stated way to be decided at all. Row 395 names that class, sweeps its members, states the road from
pieces the pack already owns, and has agent birth carry it (the owner's word, 2026-07-17, continuing the
multi-agent thread).

An expensive decision cannot be told from an ordinary one by a machine — no gate reads a decision's
reversal cost — so this is a STATED DUTY at the named decision points, and this module is the
traceability proof that those points name the read. No new pre-push gate letter: the duty rides the
suite here, the way several suite-riding checks mint no push-gate letter.

Red-first: against HEAD 35069ba the spec carries no INV-235, the road pieces are cited nowhere as a
class, and T-22 names no adversarial read, so every assertion below fails — the red recorded in
docs/prover/2026-07-18-row395-expensive-decision.md.

Re-pinned for the requirements-format PRODUCT_SPEC.md (row 445 stage 3): the law used to live as one
prose paragraph per invariant, so a single `line_with()` match sufficed. The new format spreads a law
across a Context paragraph and several numbered acceptance criteria under one `## Requirement N:`
heading, so the needles below match anywhere within that whole requirement's body (heading through
the next `## Requirement` or `## Reference`), and per-code anchors are checked as bare codes since
criteria now share one combined `[..]` tag list rather than one bracket per code.
"""
import os
import sys
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(REPO, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


def line_with(text, phrase):
    """The single line carrying a distinctive phrase (an invariant is one line per paragraph)."""
    for line in text.splitlines():
        if phrase in line:
            return line
    return None


def req_body(spec, req_num):
    """The whole body of one `## Requirement N: ...` section — heading, Context, User Story, and
    every numbered acceptance criterion — up to the next `## Requirement` or `## Reference`."""
    marker = "## Requirement %d:" % req_num
    start = spec.index(marker)
    end = spec.find("\n## Requirement", start + 1)
    if end == -1:
        end = spec.find("\n## Reference", start + 1)
    return spec[start:end] if end != -1 else spec[start:]


CLASS_OPENER = "An expensive decision earns an adversarial read before it lands"


class TestExpensiveDecisionLawStands(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = read("PRODUCT_SPEC.md")
        body = req_body(spec, 214)
        self.assertIn(CLASS_OPENER, body, "the INV-235 clause is absent from the spec")
        self.assertIn("[INV-235]", body, "the clause carries no [INV-235] tag")
        low = body.lower()
        # the class is named by its defining property: reversal costs more than the decision
        self.assertIn("unwinding it costs more than making it", low)

    def test_members_swept_enumerated(self):
        """The class is closed and enumerable, so every member is named in the clause [INV-226]."""
        spec = read("PRODUCT_SPEC.md")
        body = req_body(spec, 214)
        low = body.lower()
        self.assertIn("closed", low)
        self.assertIn("enumerable", low)
        self.assertIn("INV-226", body, "the clause does not key on the enumerate-versus-ride family")
        # the swept members, each by its bare anchor code (agent birth, node carve/merge, pinned
        # contract, project kind, the engine/instance split, a repo going public) — R214.1 now
        # tags them all on one shared combined bracket rather than one bracket per code.
        for anchor in ("T-22", "INV-113", "INV-122", "INV-187", "INV-36", "INV-85", "INV-44"):
            self.assertIn(anchor, body, "member %s is not enumerated in the class clause" % anchor)

    def test_road_states_owned_pieces(self):
        """The road is assembled from pack-owned pieces, cited by anchor rather than invented."""
        spec = read("PRODUCT_SPEC.md")
        body = req_body(spec, 214)
        low = body.lower()
        self.assertIn("adversarial", low)
        self.assertIn("recommendation", low)
        # the audit, the periodic-audit stance, the design-review grouping read, and the human's taste
        # call (surfaced by the orchestrator [INV-143] because it needs a fact only he holds [INV-152])
        for anchor in ("INV-46", "INV-145", "INV-141", "INV-142", "INV-143", "INV-152"):
            self.assertIn(anchor, body, "road piece %s is not cited in the class clause" % anchor)

    def test_stated_duty_no_detector(self):
        """The clause is honest that no machine tells an expensive decision from an ordinary one."""
        spec = read("PRODUCT_SPEC.md")
        body = req_body(spec, 214)
        low = body.lower()
        self.assertIn("no machine tells an expensive decision from an ordinary one", low)
        self.assertIn("traceability test", low)


class TestAgentBirthCarriesTheRead(unittest.TestCase):
    """T-22's ratification now names the adversarial read the owner ratifies on (SPEC INV-235)."""

    def test_proposal_carries_the_read(self):
        spec = read("PRODUCT_SPEC.md")
        body = req_body(spec, 197)
        # R197.1 names what the proposal carries (capability, zone, contracts); R197.2 is the
        # separate criterion stating that same proposal carries the adversarial read — one
        # sentence split into two criteria by the requirements-format rewrite.
        self.assertIn("naming the capability, the zone the new agent would own", body,
                      "the T-22 proposal clause is absent")
        self.assertIn("carry the adversarial read", body,
                      "the birth proposal does not carry the adversarial read")
        self.assertIn("INV-235", body, "the birth proposal does not cite INV-235")

    def test_owner_ratifies_on_the_read(self):
        spec = read("PRODUCT_SPEC.md")
        body197 = req_body(spec, 197)
        # R197.4: "ratify on" replaces the old "ratifies on" (subjunctive *shall* form).
        self.assertIn("ratify on the adversarial read", body197,
                      "T-22 does not say the owner ratifies ON the read")
        self.assertIn("INV-235", body197, "the T-22 ratifies-on sentence does not cite INV-235")
        # the old "first member of the expensive-decision class" summary sentence is gone; the
        # same tie now lives in R214.2, which names agent birth as the traceable member carrying
        # this exact duty.
        body214 = req_body(spec, 214)
        self.assertIn("agent birth carries it", body214,
                      "R214 does not name agent birth as a member of the expensive-decision class")


class TestTraceability(unittest.TestCase):
    def test_formal_index_row(self):
        spec = read("PRODUCT_SPEC.md")
        # the generated index lived a second time under the spec's own trailing "## Reference"
        # heading until the spec split removed that inline duplicate (ROADMAP row 621);
        # PRODUCT_SPEC.index.md is its one home now.
        row = line_with(read("PRODUCT_SPEC.index.md"), "| INV-235 |")
        self.assertIsNotNone(row, "no Formal-index row for INV-235")
        # index now carries locations only (SPEC INV-271) — move the prose check onto the body
        # requirement heading that carries INV-235.
        self.assertIn(CLASS_OPENER, spec)

    def test_architecture_owns_the_invariant(self):
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        build_pipeline = next((n for n in nodes if n.name == "build-pipeline"), None)
        self.assertIsNotNone(build_pipeline, "ARCHITECTURE.md carries no build-pipeline node")
        self.assertIn("INV-235", build_pipeline.anchors_expanded,
                      "build-pipeline does not own INV-235 in the architecture owns-list")

    def test_matrix_row_covers_the_law(self):
        mat = read("TEST_MATRIX.md")
        self.assertIn("| M-416 |", mat)
        row = line_with(mat, "| M-416 |")
        self.assertIn("INV-235", row, "M-416 does not cite INV-235")

    def test_duty_rides_the_suite_not_the_push_chain(self):
        """Stated duty rather than a mechanical gate: no INV-235 push-gate letter is wired.

        An expensive decision cannot be detected mechanically, so the duty is held by this traceability
        test riding the suite, and the gate chain is untouched. This test is the honesty check on that.
        """
        self.assertNotIn("INV-235", read("guardrails/pre-push"),
                         "INV-235 appears in pre-push — a push gate was wired where a stated duty "
                         "was intended")


if __name__ == "__main__":
    unittest.main(verbosity=2)
