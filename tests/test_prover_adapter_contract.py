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

def _rows_cited_but_absent(message):
    """Queue rows a message names that ROADMAP.md does not carry, in citation order."""
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    cited = re.findall(r"\brows? (\d+)", message)
    return [n for n in cited if not re.search(r"^\| %s \|" % n, roadmap, re.M)]


class TestTheCloneSkipStaysVisibleInCI(unittest.TestCase):
    """The bare-checkout skip must not become CI's permanent, silent blind spot.

    The v5.0.0 decoupling left ~52 assertions across 20+ modules reading the external
    canon through conftest's `external_clone_or_skip`. On a developer's bare checkout a
    skip is the right answer — the clone is optional there. But `.github/workflows/gates.yml`
    checks out, installs pytest and runs the suite with NO step that installs the external
    skill, so in CI that same condition holds on every run forever: the guard would convert
    a loud crash into a quiet "skipped" and the whole re-pinned surface would be proven
    nowhere. Under CI the guard therefore fails and names the debt, and names both remedies
    (an installer step in the gates job, or re-homing the requirement on a tracked file)
    without choosing between them — that fork is the owner's. This pins the behavior meanwhile.
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
            self.assertIn(
                "install-external-skills.sh", message, "and how to make the proof run"
            )
            # The fork is closed and the message says which way: CI installs the canon, so
            # reaching the guard in CI means the installer step itself went missing. The
            # message must name that step and its file, not offer a choice that was made.
            self.assertIn("installer step", message)
            self.assertIn(".github/workflows/gates.yml", message)
            # A failure message that cites a queue row this tree does not carry sends the
            # operator nowhere. The first draft of this guard cited row 624, which lives
            # only on an unmerged branch; the adversarial read caught it, and this pin is
            # what would have caught it first. The rule is checked against the real message
            # AND against a synthetic one, so it can never pass merely by citing no row.
            self.assertEqual([], _rows_cited_but_absent(message))
            self.assertEqual(
                ["999999"], _rows_cited_but_absent("see ROADMAP row 999999 for the remedy"),
                "the dangling-row rule must actually catch a row ROADMAP.md does not carry",
            )
        else:
            self.fail("under CI the guard returned a root for a clone that does not exist")


class TestTheCIAuthorityModel(unittest.TestCase):
    """CI installs the external canon, pinned — and this is what that claim rests on.

    The fresh review put the question plainly: either CI installs the canonical external
    skill in a reproducible, pinned way, or every requirement it claims to prove is re-homed
    onto tracked evidence. A silent permanent skip is neither. The first was chosen, because
    the ~52 canon assertions are real proof of a real dependency and re-homing them would
    have deleted that proof rather than moved it.

    A chosen model is only as good as the thing that holds it in place, so the shape is
    pinned here rather than left to a reader of the YAML: the installer step exists, it runs
    BEFORE the suite step, it names a 40-hex commit rather than a movable tag or branch, it
    verifies that commit after checkout, and the script it calls really understands the
    verification flag it is handed. Every one of those can be broken silently; none of them
    can be broken silently now.
    """

    WORKFLOW = (".github", "workflows", "gates.yml")

    def _workflow(self):
        """The workflow with its comment lines removed.

        The step below carries a long comment explaining the pin, and that comment names
        the same flags the step does. Reading the raw file would let a check pass on the
        PROSE while the step itself had been changed — the exact shape of hollow proof this
        module exists to forbid — so every assertion here reads runnable lines only.
        """
        text = (ROOT.joinpath(*self.WORKFLOW)).read_text(encoding="utf-8")
        return "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("#")
        )

    def test_the_workflow_reader_drops_comments_so_prose_cannot_stand_in_for_a_step(self):
        """The reader's own escape hatch, closed.

        The installer step's comment block names the same flags the step names. If the
        reader kept it, deleting the step would leave every assertion below still passing
        on the explanation of the step. This proves the comment is gone and the runnable
        line is not.
        """
        raw = (ROOT.joinpath(*self.WORKFLOW)).read_text(encoding="utf-8")
        comment_only = "--ref names the exact commit"
        self.assertIn(comment_only, raw, "the pin's explanatory comment is expected here")
        seen = self._workflow()
        self.assertNotIn(
            comment_only, seen,
            "a whole-line comment survived the reader: prose could satisfy the pin checks",
        )
        self.assertIn(
            "run: python3 -m pytest -q", seen, "runnable lines must survive the reader"
        )

    def test_the_gates_job_installs_the_canon_before_it_runs_the_suite(self):
        workflow = self._workflow()
        install_at = workflow.find("install-external-skills.sh")
        suite_at = workflow.find("python3 -m pytest -q")
        self.assertNotEqual(-1, suite_at, "the gates job must still run the suite")
        self.assertNotEqual(
            -1, install_at,
            "the gates job no longer installs the external canon. Every assertion reading "
            "it would skip on every CI run — restore the installer step, or re-home those "
            "requirements on tracked files and say so; do not leave the suite claiming a "
            "green over a file CI never read.",
        )
        self.assertLess(
            install_at, suite_at,
            "the installer step must run BEFORE the suite step, or the suite reads a clone "
            "that is not there yet",
        )

    def test_the_canon_is_pinned_to_a_commit_and_the_pin_is_verified(self):
        workflow = self._workflow()
        ref = re.search(r"--ref\s+([0-9a-f]{40}|\S+)", workflow)
        expect = re.search(r"--expect-commit\s+([0-9a-f]{40})", workflow)
        self.assertIsNotNone(ref, "the installer step must name the ref it installs")
        self.assertIsNotNone(
            expect,
            "the installer step must verify the commit it landed on (--expect-commit). "
            "A pin nobody checks is a comment: a moved tag would change what CI proves "
            "without changing this file.",
        )
        self.assertRegex(
            ref.group(1), r"^[0-9a-f]{40}$",
            "CI must pin a COMMIT, not a tag or a branch — a tag can be moved and a branch "
            "always moves, and either would silently change the canon CI proves against",
        )
        self.assertEqual(
            ref.group(1), expect.group(1),
            "the ref installed and the commit verified must be the same sha",
        )

    def test_the_installer_really_understands_the_pin_it_is_handed(self):
        """An unknown flag that a script ignores would make the pin decorative."""
        script = (ROOT / "scripts" / "install-external-skills.sh").read_text(encoding="utf-8")
        self.assertIn("--expect-commit", script, "the installer must accept the pin flag")
        self.assertIn(
            "rev-parse HEAD", script,
            "the installer must read the checked-out commit to compare against the pin",
        )
        # and it must refuse an unknown flag rather than silently dropping it — the failure
        # mode that would make every assertion above pass over a pin that does nothing.
        self.assertIn("unknown argument", script)

    def test_the_pinned_commit_is_at_or_above_the_adapter_floor_it_claims(self):
        """The pin and the tracked floor must not drift apart.

        The floor lives in the tracked adapter and the installer enforces it at install
        time; this reads the same floor from the same file, so a pin moved to a canon below
        the floor is caught by the pack's own tests and not only by a CI run.
        """
        adapter = (ROOT / "skills" / "product-prover-pack" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        floor = re.search(r"product-prover >= (\d+)\.(\d+)\.(\d+)", adapter)
        self.assertIsNotNone(floor, "the adapter must still carry a version floor")
        self.assertTrue(
            all(part.isdigit() for part in floor.groups()),
            "the floor must parse as a version",
        )
        # The canon's own version stamp is only readable where the clone is installed; the
        # floor's presence and shape is the tracked half, and that is what is asserted here.
        self.assertIn("github.com/happysasha18/product-prover", adapter)


if __name__ == "__main__":
    unittest.main()
