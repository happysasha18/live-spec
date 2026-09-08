"""A push review runs in one of two named modes — id: q-827 (the owner's word, 2026-09-08 21:25
and 21:26).

Closure is the default and reads the accepted row alone: its definition of done, its recorded
acceptance command, the diff of the pushed range, and the paths that diff touches. It blocks on
material failure alone, and anything true it notices outside that reach becomes one deposit under
`inbox/` rather than a second list or a new row. Global is owed rather than chosen — on the owner's
own request naming a critical scope, and on a row that itself changes a critical cross-cutting
surface (the base pack, the installer, CI or admission, or the shared release path) — and it names
that scope on the record before it reads.

Both modes are proved HERE THROUGH THE GATE: each test plants a record of one mode in a throwaway
tree and runs `guardrails/check-prover-record.sh` against it, so what is held is the record the gate
actually accepts. The prose describing the modes is checked only where a mode's own contract has no
other home — the reach and the blocking set — and never in place of a run.
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path

from conftest import ROOT

GATE = Path(ROOT) / "guardrails" / "check-prover-record.sh"
BINDING = Path(ROOT) / "skills" / "product-prover-pack" / "SKILL.md"
RECORD_README = Path(ROOT) / "docs" / "prover" / "README.md"


def _git(tree, *args):
    return subprocess.run(["git", *args], cwd=str(tree), capture_output=True, text=True)


def _tree(tmp):
    """A throwaway repository with one commit past its own base, so a record has a range to name."""
    _git(tmp, "init", "-q")
    _git(tmp, "config", "user.email", "t@example.invalid")
    _git(tmp, "config", "user.name", "t")
    (tmp / "PRODUCT_SPEC.md").write_text("# spec\n", encoding="utf-8")
    (tmp / "ARCHITECTURE.md").write_text("# architecture\n", encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "base")
    base = _git(tmp, "rev-parse", "HEAD").stdout.strip()
    (tmp / "shipped.txt").write_text("the change this push sends\n", encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "the change")
    head = _git(tmp, "rev-parse", "HEAD").stdout.strip()
    return base, head


def _record(tmp, body, slug):
    path = tmp / "docs" / "prover" / ("2026-09-08-%s.md" % slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "the record")
    return path


def _run_gate(tmp, base):
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base, TZ="Asia/Jerusalem")
    env.pop("LIVE_SPEC_EVALUATING", None)
    return subprocess.run([str(GATE), "--push", "docs/prover", "2026-09-08"],
                          cwd=str(tmp), env=env, capture_output=True, text=True, timeout=60)


CLOSURE = """# Prover record — 2026-09-08 the closure read of one row

PUSH-REVIEW

Mode: closure
Range: {base}..{head}
- {head} the change
Files read: the row's definition of done, its acceptance command, shipped.txt
Checks run: the row's own acceptance command — passed
Findings: one, outside this read's reach and deposited under inbox/ rather than opened as work.
Blocking: none
"""

GLOBAL = """# Prover record — 2026-09-08 the global read of one surface

PUSH-REVIEW

Mode: global
Scope: the installer, which this row changes
Range: {base}..{head}
- {head} the change
Files read: the installer and every path it writes
Checks run: the installer against a planted host — passed
Findings: one reproducible failure of the named surface, with its affected path.
Blocking: one.
- the installer leaves a host without the key it seeds — closed: the seed writes it, proved on a
  planted host of that shape.
"""


class TestBothModesPassTheGate(unittest.TestCase):
    """The gate reads a record of either mode. Neither shape is a special case to it: it holds
    presence, commit, freshness, range and fields, and the mode line rides with them."""

    def _plant_and_run(self, template, slug):
        import tempfile
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, head = _tree(tmp)
            _record(tmp, template.format(base=base[:7], head=head[:7]), slug)
            return self, _run_gate(tmp, base)

    def test_a_closure_record_passes_the_push_gate(self):
        _, got = self._plant_and_run(CLOSURE, "closure")
        self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
        self.assertIn("covers the pushed range", got.stdout)

    def test_a_global_record_carrying_its_scope_passes_the_push_gate(self):
        _, got = self._plant_and_run(GLOBAL, "global")
        self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
        self.assertIn("covers the pushed range", got.stdout)

    def test_a_blocking_finding_still_holds_the_push_in_either_mode(self):
        """The modes narrow what a review READS. What a blocking finding does is unchanged: it
        holds the push until the record says closed or stands."""
        open_finding = GLOBAL[:GLOBAL.index("Blocking:")] + (
            "Blocking: one.\n"
            "- the installer leaves a host without the key it seeds.\n")
        _, got = self._plant_and_run(open_finding, "global-open")
        self.assertEqual(got.returncode, 1, got.stdout)
        self.assertIn("neither closed nor explained", got.stdout)


class TestEachModeStatesItsOwnReach(unittest.TestCase):
    """A mode's reach and its blocking set have no home outside the words that state them, so
    these read those words. Everything a run can prove is proved by a run above."""

    def setUp(self):
        # Read with line wrapping collapsed: these documents are wrapped for a reader, and a
        # sentence's meaning does not change with where a line broke.
        raw = BINDING.read_text(encoding="utf-8")
        self.binding = raw
        self.flat = " ".join(raw.split())

    def test_the_binding_names_exactly_two_push_review_modes(self):
        self.assertIn("\n## Closure review\n", self.binding)
        self.assertIn("\n## Global review\n", self.binding)
        self.assertIn("runs as CLOSURE or", self.binding)

    def test_closure_reaches_the_row_and_blocks_on_material_failure_alone(self):
        closure = " ".join(self.binding[self.binding.index("## Closure review"):
                                        self.binding.index("## Global review")].split())
        for owed in ("definition of done", "acceptance command", "diff of the row",
                     "paths that diff touches"):
            self.assertIn(owed, closure)
        self.assertIn("blocks on material failure alone", closure.lower())
        self.assertIn("one inbox deposit", closure.lower())
        self.assertIn("opens no row", closure)

    def test_global_runs_on_its_two_triggers_and_names_its_scope(self):
        section = " ".join(self.binding[self.binding.index("## Global review"):].split())
        self.assertIn("the owner asks for one", section)
        for surface in ("base pack", "installer", "CI or admission", "shared release path"):
            self.assertIn(surface, section)
        self.assertIn("the scope is named outright", section)
        self.assertIn("never a licence to audit the repository", section)

    def test_the_record_shape_carries_the_mode_and_a_global_scope(self):
        readme = RECORD_README.read_text(encoding="utf-8")
        flat = " ".join(readme.split())
        self.assertIn("\nMode: closure\n", readme)
        self.assertIn("`Mode:` reads `closure` or `global`", flat)
        self.assertIn("`Scope:`", readme)


if __name__ == "__main__":
    unittest.main()


class TestTheGateReadsTheModeLine(unittest.TestCase):
    """The mode is a field the gate holds, rather than a line a record carries for a reader. A
    record that names no mode says nothing about its own reach, and a global one naming no scope is
    the unbounded read this whole contract ends — so the gate refuses both."""

    def _plant_and_run(self, body, slug):
        import tempfile
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, head = _tree(tmp)
            _record(tmp, body.format(base=base[:7], head=head[:7]), slug)
            return _run_gate(tmp, base)

    def test_a_record_naming_no_mode_is_refused(self):
        got = self._plant_and_run(CLOSURE.replace("Mode: closure\n", ""), "no-mode")
        self.assertEqual(got.returncode, 1, got.stdout)
        self.assertIn("missing its `Mode:` line", got.stdout)

    def test_a_global_record_naming_no_scope_is_refused(self):
        body = GLOBAL.replace("Scope: the installer, which this row changes\n", "")
        got = self._plant_and_run(body, "global-no-scope")
        self.assertEqual(got.returncode, 1, got.stdout)
        self.assertIn("names no `Scope:`", got.stdout)

    def test_a_mode_that_is_not_one_of_the_two_is_refused(self):
        got = self._plant_and_run(CLOSURE.replace("Mode: closure", "Mode: quick"), "bad-mode")
        self.assertEqual(got.returncode, 1, got.stdout)
        self.assertIn("is not a mode a review runs in", got.stdout)
