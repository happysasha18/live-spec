"""scripts/measurements-table.py builds docs/MEASUREMENTS.html only when asked (SPEC INV-286).

The generator used to write docs/MEASUREMENTS.md and docs/MEASUREMENTS.html together on every run,
whether or not a person was about to read the page. Most runs are a plain remeasure with no reading
exchange behind them, so the page stood in the tree far more often than it was read: this one page
alone carries five separate sweep entries in attic/MANIFEST.md (2026-08-04 through 2026-08-19,
commits 063a55df and 33a983be among them), every other rendered page in the project's history
carrying at most two. Each leftover trips `guardrails/check-rendered-sweep.py`, which rides the test
suite (gate b), so an ordinary remeasure could fail the next push.

The fix moves the HTML build behind an explicit `--html` flag: a bare run writes only the `.md`, the
source of truth, and the reading page is built (and, per SPEC INV-286, later swept) only when someone
actually means to read it.

This test runs the real script against the real tree — a remeasure is exactly the case that broke —
and proves the tree stays clean afterward: no `--html` leaves no rendered page and a green sweep gate;
`--html` does produce the page, the sweep gate correctly reds while it stands (proving the page really
is read as transient, not just absent by accident), and `scripts/sweep-rendered.py` clears it back to
green. `docs/MEASUREMENTS.md`, `docs/MEASUREMENTS.html`, and `attic/MANIFEST.md` are restored to their
pre-test bytes in every case, run or fail, so the suite leaves the tree exactly as it found it.

Red proven 2026-08-19: reverting scripts/measurements-table.py's `main` to write the HTML page
unconditionally (dropping the `--html` gate) makes `test_a_bare_remeasure_leaves_no_rendered_page`
fail, reporting `docs/MEASUREMENTS.html` standing after a bare run; restoring the gate passes it
again.
"""
import os
import shutil
import subprocess
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "measurements-table.py")
GATE = os.path.join(ROOT, "guardrails", "check-rendered-sweep.py")
SWEEP = os.path.join(ROOT, "scripts", "sweep-rendered.py")
MD = os.path.join(ROOT, "docs", "MEASUREMENTS.md")
HTML = os.path.join(ROOT, "docs", "MEASUREMENTS.html")
MANIFEST = os.path.join(ROOT, "attic", "MANIFEST.md")
ATTIC_COPY = os.path.join(ROOT, "attic", "docs-MEASUREMENTS.html")


def _run(*args):
    return subprocess.run(["python3", *args], capture_output=True, text=True, cwd=ROOT)


class TestMeasurementsHTMLOptIn(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.isfile(MD), "docs/MEASUREMENTS.md must exist before this test runs")
        with open(MD, encoding="utf-8") as f:
            self._md_before = f.read()
        with open(MANIFEST, encoding="utf-8") as f:
            self._manifest_before = f.read()
        self._html_existed = os.path.isfile(HTML)
        if self._html_existed:
            with open(HTML, encoding="utf-8") as f:
                self._html_before = f.read()
        self._attic_copy_existed = os.path.exists(ATTIC_COPY)

    def tearDown(self):
        # Every file this test's real runs may have touched goes back to its pre-test bytes,
        # whether the test passed or raised — the suite leaves the tree as it found it.
        with open(MD, "w", encoding="utf-8") as f:
            f.write(self._md_before)
        with open(MANIFEST, "w", encoding="utf-8") as f:
            f.write(self._manifest_before)
        if self._html_existed:
            with open(HTML, "w", encoding="utf-8") as f:
                f.write(self._html_before)
        elif os.path.exists(HTML):
            os.remove(HTML)
        if not self._attic_copy_existed and os.path.exists(ATTIC_COPY):
            os.remove(ATTIC_COPY)

    def test_a_bare_remeasure_leaves_no_rendered_page(self):
        if os.path.exists(HTML):
            os.remove(HTML)
        r = _run(SCRIPT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse(
            os.path.exists(HTML),
            "a bare `measurements-table.py` run built docs/MEASUREMENTS.html — every plain "
            "remeasure now leaves a transient page standing, the exact mine this fix removes")
        gate = _run(GATE)
        self.assertEqual(gate.returncode, 0, "the sweep gate reds after a bare remeasure:\n"
                         + gate.stdout + gate.stderr)

    def test_html_flag_builds_a_page_the_gate_reds_on_and_the_sweep_clears(self):
        if os.path.exists(HTML):
            os.remove(HTML)
        r = _run(SCRIPT, "--html")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(HTML), "--html did not build docs/MEASUREMENTS.html")

        gate = _run(GATE)
        self.assertEqual(
            gate.returncode, 1,
            "the sweep gate stayed green with docs/MEASUREMENTS.html standing — it is not being "
            "read as the transient page it is")
        self.assertIn("MEASUREMENTS.html", gate.stdout)

        swept = _run(SWEEP)
        self.assertEqual(swept.returncode, 0, swept.stdout + swept.stderr)
        self.assertFalse(os.path.exists(HTML), "the sweep did not clear the page")
        self.assertTrue(os.path.exists(ATTIC_COPY), "the sweep did not land the page in the attic")

        gate_after = _run(GATE)
        self.assertEqual(gate_after.returncode, 0, "the gate still reds after the sweep:\n"
                         + gate_after.stdout + gate_after.stderr)


if __name__ == "__main__":
    unittest.main()
