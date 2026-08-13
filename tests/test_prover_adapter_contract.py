"""The adapter contract for the external product-prover skill (v5.0.0 decoupling).

Every assertion here reads TRACKED files only — the adapter page, the installer
script, and the mirror-sync guard — so the module is green on a bare checkout,
with or without the installed external clone. It is the first live fence on the
decoupling debt: the vendored prover body left the tree in v5.0.0, and what the
pack still promises about the external skill is pinned here instead of in tests
that read the departed body.
"""

import os
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


class TestTheCloneSkipStaysVisibleInCI(unittest.TestCase):
    """The bare-checkout skip must not become CI's permanent, silent blind spot.

    The v5.0.0 decoupling left ~52 assertions across 20+ modules reading the external
    canon through conftest's `external_clone_or_skip`. On a developer's bare checkout a
    skip is the right answer — the clone is optional there. But `.github/workflows/gates.yml`
    checks out, installs pytest and runs the suite with NO step that installs the external
    skill, so in CI that same condition holds on every run forever: the guard would convert
    a loud crash into a quiet "skipped" and the whole re-pinned surface would be proven
    nowhere. Under CI the guard therefore fails and names the debt. ROADMAP row 624 holds
    the owner's choice of remedy; this pins the behavior meanwhile.
    """

    def _call_with_ci(self, value):
        from conftest import external_clone_or_skip as guard

        prior = os.environ.get("CI")
        if value is None:
            os.environ.pop("CI", None)
        else:
            os.environ["CI"] = value
        try:
            # A name that cannot exist stands in for the missing clone, so the assertion
            # holds identically on a machine that HAS the real clone installed.
            return guard("no-such-external-skill-fixture")
        finally:
            if prior is None:
                os.environ.pop("CI", None)
            else:
                os.environ["CI"] = prior

    def test_a_local_bare_checkout_still_skips_with_the_reason(self):
        with self.assertRaises(unittest.SkipTest) as caught:
            self._call_with_ci(None)
        self.assertIn("install-external-skills.sh", str(caught.exception))

    def test_ci_fails_instead_of_skipping_and_says_what_went_unproven(self):
        # SkipTest is caught by name, never by assertRaises: a bare
        # `assertRaises(AssertionError)` lets SkipTest escape and pytest scores the whole
        # test "skipped" — this proof would then go silent in exactly the way it exists to
        # forbid (observed while proving it red, 2026-08-13).
        try:
            self._call_with_ci("true")
        except unittest.SkipTest as skipped:
            self.fail("under CI the guard skipped instead of failing: %s" % skipped)
        except AssertionError as failed:
            message = str(failed)
            self.assertIn("did not run", message)
            self.assertIn("row 624", message, "the failure must name where the remedy is held")
            self.assertIn(
                "install-external-skills.sh", message, "and how to make the proof run"
            )
        else:
            self.fail("under CI the guard returned a root for a clone that does not exist")

    def test_ci_workflow_still_has_no_installer_step_so_the_guard_is_load_bearing(self):
        # If a later change gives the gates job an installer step, the clone is present in
        # CI and this guard stops firing — that is the fix, and this assertion is the thing
        # that must then be re-read rather than the guard quietly outliving its reason.
        workflow = (ROOT / ".github" / "workflows" / "gates.yml").read_text(encoding="utf-8")
        self.assertIn("python3 -m pytest -q", workflow, "the gates job runs the suite")
        self.assertNotIn(
            "install-external-skills", workflow,
            "CI now installs the external clone: re-read the guard in tests/conftest.py, "
            "the CI arm may have become dead code (ROADMAP row 624)",
        )
