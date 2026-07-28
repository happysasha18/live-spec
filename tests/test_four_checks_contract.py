"""The four host checks' shipping contract — matrix row M-226 (SPEC INV-97, row 241).

The web session's curator read, 2026-07-10: the pipeline's four teeth (completeness,
tests-present, behaviour-traces-to-spec, conflicts) ship as generic runnable code a host
attaches by ONE config file — honest failure modes, adopt-walk attachment, the pack repo
as the first host. This test pins the CONTRACT's presence; the checks' own function-level
rows land with their code (the row 241 build).
"""

import json
import os
import re
import subprocess
import unittest

from conftest import ROOT, read, read_flat


class TestFourChecksContract(unittest.TestCase):
    def test_contract_in_the_spec(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "the four project-side checks configured rather than re-implemented", spec
        )
        self.assertIn("parametrized by one host config file", spec)
        self.assertIn(
            "shall* red with an attach-me line rather than pass silently", spec
        )

    def test_waivers_are_declared(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("an undeclared gap never passes quietly", spec)

    def test_acceptance_is_measured(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("each check proves itself red-first on one planted defect", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-97]", spec)
        self.assertIn("| INV-97 |", spec)

    def test_own_attach_arms_the_discovery_pattern(self):
        """The external gate check (2026-07-10, docs/prover/2026-07-10-external-gate-check.md)
        planted an unregistered rendered surface and the completeness gate stayed green: this
        repo's own config left surface_discovery_pattern null, so the self-closing
        DOM-to-registry direction never ran on the one host that is the pack itself. Armed
        2026-07-11 and locked here: the pattern stays set and keeps catching the planted class."""
        config = json.loads(read("guardrails.config.json"))
        pattern = config.get("surface_discovery_pattern")
        self.assertTrue(pattern,
                        "surface_discovery_pattern is null again — the rendered-but-unregistered "
                        "branch of the completeness check is disarmed on the pack's own repo "
                        "(the external gate-check hole, 2026-07-10)")
        planted = '<section id="phantom-surface">planted, registered nowhere</section>'
        self.assertEqual(re.findall(pattern, planted), ["phantom-surface"],
                         "the armed pattern no longer catches the planted break class")


if __name__ == "__main__":
    unittest.main()
