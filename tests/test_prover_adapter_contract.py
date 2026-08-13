"""The adapter contract for the external product-prover skill (v5.0.0 decoupling).

Every assertion here reads TRACKED files only — the adapter page, the installer
script, and the mirror-sync guard — so the module is green on a bare checkout,
with or without the installed external clone. It is the first live fence on the
decoupling debt: the vendored prover body left the tree in v5.0.0, and what the
pack still promises about the external skill is pinned here instead of in tests
that read the departed body.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAPTER = ROOT / "skills" / "product-prover-pack" / "SKILL.md"
INSTALLER = ROOT / "scripts" / "install-external-skills.sh"
SYNC = ROOT / "scripts" / "sync-mirrors.sh"

# The one pattern the installer greps the adapter with (install-external-skills.sh,
# "the version floor, read from the adapter's metadata").
FLOOR_PATTERN = r"product-prover >= ([0-9]+\.[0-9]+\.[0-9]+)"


class TestAdapterPage(unittest.TestCase):
    def setUp(self):
        self.text = ADAPTER.read_text(encoding="utf-8")

    def test_adapter_page_is_tracked_and_named(self):
        self.assertTrue(ADAPTER.is_file(), f"adapter page missing: {ADAPTER}")
        self.assertIn("name: product-prover-pack", self.text)

    def test_requires_line_names_floor_and_canon(self):
        m = re.search(FLOOR_PATTERN, self.text)
        self.assertIsNotNone(m, "adapter carries no 'product-prover >= X.Y.Z' floor")
        floor = tuple(int(p) for p in m.group(1).split("."))
        self.assertGreaterEqual(floor, (1, 3, 0), f"floor {m.group(1)} is below 1.3.0")
        self.assertIn(
            "github.com/happysasha18/product-prover",
            self.text,
            "adapter names no canonical repository beside the floor",
        )

    def test_mode_names_bind_all_three_pipeline_modes(self):
        for mode in ("`FULL`", "`CROSS-LINK`", "`FEATURE-FIT`"):
            self.assertIn(mode, self.text, f"mode table misses {mode}")

    def test_pack_paths_name_the_reviewed_documents(self):
        for doc in ("PRODUCT_SPEC.md", "ARCHITECTURE.md"):
            self.assertIn(doc, self.text, f"pack paths misses {doc}")


class TestInstallerReadsTheAdapterFloor(unittest.TestCase):
    def setUp(self):
        self.text = INSTALLER.read_text(encoding="utf-8")

    def test_installer_extracts_the_floor_from_the_adapter(self):
        self.assertIn(
            "product-prover >= [0-9]+\\.[0-9]+\\.[0-9]+",
            self.text,
            "installer no longer greps the adapter's floor pattern",
        )

    def test_installer_refuses_when_the_floor_is_absent(self):
        self.assertIn(
            "no version floor found",
            self.text,
            "installer's missing-floor refusal branch is gone",
        )

    def test_the_adapter_floor_parses_with_the_installer_pattern(self):
        # The two files agree mechanically: the same regex the installer runs
        # finds exactly one floor in the adapter.
        found = re.findall(FLOOR_PATTERN, ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(
            len(found), 1, f"installer's pattern finds {len(found)} floors in the adapter"
        )


class TestMirrorSyncGuard(unittest.TestCase):
    def test_sync_skips_the_external_skill_always(self):
        text = SYNC.read_text(encoding="utf-8")
        guard = re.search(
            r"case \"\$skill_name\" in\s*\n\s*product-prover\)(.*?)continue", text, re.S
        )
        self.assertIsNotNone(guard, "sync-mirrors carries no product-prover skip guard")
        self.assertIn("SKIPPED", guard.group(1), "the guard skips without saying so")


if __name__ == "__main__":
    unittest.main()
