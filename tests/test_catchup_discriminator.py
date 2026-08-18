"""The catch-up routing carries its version-delta discriminator — M-248 (SPEC INV-110, row 239).

The track-coach audit (2026-07-10 ~14:19) found the trigger wordings would justify the heavy
catch-up walk where a host queue row is the truth: a pure docs-layout pass with no pack-version
delta fell into the gap. The routing states the discriminator in one sentence — the walk fires
only when the host's recorded package version is behind the current package VERSION — carried in
both homes: the spec's skill-behaviour paragraph and the guide's "When to run this".
"""

import unittest

from conftest import open_spec, read_flat


class TestCatchupDiscriminator(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "MIGRATION.md")

    def test_discriminator_in_both_homes(self):
        # The two homes carry the same rule in each document's own current wording
        # (MIGRATION.md: "package"/"VERSION"; PRODUCT_SPEC.md's rewrite: "pack version").
        needles = {
            "PRODUCT_SPEC.md": (
                "the host's recorded pack version is behind the current pack version",
                "route it as the host's own queue row through its pipeline",
            ),
            "MIGRATION.md": (
                "fires only when the host's recorded package version is behind the current package VERSION",
                "no version delta is the host's own queue row through its pipeline",
            ),
        }
        for home in self.HOMES:
            body = read_flat(home)
            version_needle, no_delta_needle = needles[home]
            self.assertIn(version_needle, body, home)
            self.assertIn(no_delta_needle, body, home)

    def test_trigger_wordings_read_as_examples(self):
        needles = {
            "PRODUCT_SPEC.md": (
                "The owner's wording is an example, never the decider",
                "whatever wording the ask used",
            ),
            "MIGRATION.md": (
                "The trigger wordings are examples under this test",
                "A wording never decides the routing",
            ),
        }
        for home in self.HOMES:
            body = read_flat(home)
            example_needle, wording_needle = needles[home]
            self.assertIn(example_needle, body, home)
            self.assertIn(wording_needle, body, home)

    def test_spec_anchor_and_index(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only
        # ("| INV-110 | R115.1, R183.1, R185.1, ... |"), no prose. The row's PRESENCE
        # is checked here; the "version" prose lives on the body criterion (R185.1)
        # that carries the code, asserted below against the flattened spec body.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-110]", spec)
        self.assertIn(
            "the host's recorded pack version is behind the current pack version",
            spec,
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-110 |"):
                    self.assertIn("R185.1", line)
                    return
        self.fail("INV-110 index row missing")


if __name__ == "__main__":
    unittest.main()
