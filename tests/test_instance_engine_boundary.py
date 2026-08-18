"""Crossing the instance->engine boundary -- provenance and naming (SPEC INV-119, row 276).

A feature usually proves itself first on a live instance and then generalizes into the
engine. When that history goes into the engine's spec, it must read as the engine's own
record: a reconciliation log citing the engine's own public commits, never a private
instance's commit or the instance's own locale label standing as a mechanism name.
"""

import unittest

from conftest import open_spec, read_flat


class TestInstanceEngineBoundary(unittest.TestCase):
    def test_reconciliation_phrase_in_spec(self):
        # PRODUCT_SPEC.md generalized the reconciliation-log's concrete worked example (the exact
        # quoted header text) to the class-level rule; the precise wording the skill teaches an
        # author to use still lives in skills/spec-author and skills/publish (unaffected, still
        # passing) since that FORMAT is their job, not the spec's.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "cite only the engine's own public commits for provenance", spec
        )

    def test_reconciliation_phrase_in_spec_author(self):
        body = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("how each behaviour landed in code", body)

    def test_reconciliation_phrase_in_publish(self):
        body = read_flat("skills/publish/SKILL.md")
        self.assertIn("how each behaviour landed in code", body)

    def test_engine_commit_phrase_in_spec(self):
        # the exact quoted citation format ("landed in engine commit `<hash>`") is now the skill's
        # authoring detail (spec-author/publish, unaffected); the spec states the same provenance
        # rule at the class level.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "cite only the engine's own public commits for provenance", spec
        )

    def test_engine_commit_phrase_in_spec_author(self):
        body = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("landed in engine commit", body)

    def test_engine_commit_phrase_in_publish(self):
        body = read_flat("skills/publish/SKILL.md")
        self.assertIn("landed in engine commit", body)

    def test_proven_first_phrase_in_spec(self):
        # The requirements-format spec states the engine/instance boundary law (INV-119) with its own
        # wording; "proven first on a live instance" is the skills' phrasing (asserted in the two
        # sibling tests below). The spec states the same law as the engine proven independent of its
        # first user.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("proven independent of its first user", spec)

    def test_proven_first_phrase_in_spec_author(self):
        body = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("proven first on a live instance", body)

    def test_proven_first_phrase_in_publish(self):
        body = read_flat("skills/publish/SKILL.md")
        self.assertIn("proven first on a live instance", body)

    def test_spec_anchor(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-119]", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "engine", spec.lower(),
            "INV-119's body criterion doesn't carry the 'engine' phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-119 |"):
                    return
        self.fail("INV-119 index row missing")


if __name__ == "__main__":
    unittest.main()
