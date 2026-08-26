"""Every request enters through a three-source impact read, the footprint decides the route — INV-128 (row 259).

Beside the door and the work-kind, a third dimension is read at intake: the FOOTPRINT, read from the spec
(what behaviour changes), the architecture (which module owns it), and the code (what gets touched). One
named footprint — presentation-only / single-module / cross-cutting — spoken in the capture echo, written in
the row's footprint note. The footprint decides the route (light road / matrix step / full pipeline). Source
disagreement is a finding routed to its owner. It is the verdict derive-before-fork (INV-121) rests on. It
re-classifies mid-work. The station carries the boundary-health law. The entry station (P1-P6) of the
fourteen-principle architect draft. Homes: the intake clause, build-pipeline step zero, ARCHITECTURE's
boundary-health law, product-prover's three-source lens, communicator's capture echo. (Alexander live
2026-07-12.)
"""

import unittest

from conftest import external_clone_or_skip, open_spec, read, read_all_flat, read_flat


class TestImpactAnalysisEntry(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "Every request enters through a three-source impact read, and the footprint decides the route",
            spec,
        )
        self.assertIn("[INV-128]", spec)

    def test_spec_names_three_footprints_and_the_route(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in ("presentation-only", "single-module", "cross-cutting",
                       "the footprint decide how far each step reaches",
                       "never let the footprint promote a feature past the spec step"):
            self.assertIn(needle, spec, needle)

    def test_spec_cites_derive_before_fork(self):
        # the coined label "derive-before-fork" is gone from the register rewrite (no coined names,
        # plain mechanisms); the same rule stands as R43.6's plain-language statement.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "the three-source read tell whether a proven artifact already settles a question",
            spec,
        )
        self.assertIn("[INV-128, INV-121]", spec)

    def test_spec_carries_boundary_health(self):
        # the spec's own restatement of the boundary-health definition was compacted out (the fact
        # now lives once, in ARCHITECTURE.md's "Boundary health" law — see
        # test_architecture_states_boundary_health); the spec still states the same law as its
        # diagnostic signal (a repeatedly cross-cut boundary is a misplaced one).
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "read repeated cross-cuts on the same module pair as the signal to move a boundary",
            spec,
        )

    def test_formal_index_row(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "footprint", spec.lower(),
            "INV-128's body criterion doesn't carry the footprint phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-128 |"):
                    return
        self.fail("INV-128 Formal-index row missing")

    def test_build_pipeline_reads_the_footprint(self):
        bp = read_flat("skills/director/references/footprint-read.md")
        self.assertIn("The same line reads the footprint", bp)
        self.assertIn("three-source impact read that decides the route (SPEC INV-128)", bp)

    def test_architecture_states_boundary_health(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("Boundary health — a typical request lands in one node (SPEC INV-128)", arch)

    def test_prover_carries_three_source_lens(self):
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Three-source disagreement", pv)

    def test_communicator_echo_carries_footprint(self):
        cm = read_flat("skills/communicator/SKILL.md")
        self.assertIn("the footprint the three-source read named", cm)

    def test_matrix_row_covers_the_entry_station(self):
        for line in read("TEST_MATRIX.md").splitlines():
            if line.startswith("| M-269 |"):
                self.assertIn("INV-128", line)
                return
        self.fail("M-269 matrix row missing")


if __name__ == "__main__":
    unittest.main()
