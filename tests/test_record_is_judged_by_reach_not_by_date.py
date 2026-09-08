"""A push review record is picked by what it covers — id: q-830 (the owner's word, 2026-09-09 00:03).

Gate a demanded a record whose FILENAME began with today's date. On the night of 2026-09-08 a
landing was reviewed at 23:50 and pushed at 00:05, and the gate told it that it carried no written
review at all; what cleared the push was a second record written to satisfy the clock and nothing
else. His word on it: «одна минута до полночи или после ничего не меняют. это лишняя машинерия».

Two arms already decided everything the date pretended to. A record is refused when it is older
than `PRODUCT_SPEC.md` or `ARCHITECTURE.md`, and refused when it does not name the base commit and
every commit being pushed. Both still refuse exactly what they refused before, and each test here
proves that by driving `guardrails/check-prover-record.sh` itself over a throwaway repository,
rather than by reading what the script says about itself.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from conftest import ROOT

GATE = Path(ROOT) / "guardrails" / "check-prover-record.sh"
SCRIPT = GATE.read_text(encoding="utf-8")
README = (Path(ROOT) / "docs" / "prover" / "README.md").read_text(encoding="utf-8")

RECORD = """# Prover record — {slug}

PUSH-REVIEW

Mode: closure
Range: {base}..{head}
- {head} the change
Files read: shipped.txt
Checks run: the row's own acceptance command — passed
Findings: none material.
Blocking: none
"""


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
    return base, _git(tmp, "rev-parse", "HEAD").stdout.strip()


def _plant(tmp, name, body):
    path = tmp / "docs" / "prover" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    _git(tmp, "add", "-A")
    _git(tmp, "commit", "-qm", "the record")
    return path


def _run(tmp, base, today="2026-09-09"):
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base, TZ="Asia/Jerusalem")
    env.pop("LIVE_SPEC_EVALUATING", None)
    return subprocess.run([str(GATE), "--push", "docs/prover", today],
                          cwd=str(tmp), env=env, capture_output=True, text=True, timeout=60)


class TestTheDateDecidesNothing(unittest.TestCase):

    def test_a_record_written_before_midnight_carries_the_push_after_it(self):
        """The defect itself, in the shape it arrived in: reviewed on the 8th, pushed on the 9th.

        Red before this row — the gate looked for `docs/prover/2026-09-09*.md`, found the record
        named for the 8th and refused the push as carrying no review.
        """
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, head = _tree(tmp)
            _plant(tmp, "2026-09-08-reviewed-before-midnight.md",
                   RECORD.format(slug="reviewed before midnight", base=base[:7], head=head[:7]))

            got = _run(tmp, base, today="2026-09-09")

            self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
            self.assertIn("2026-09-08-reviewed-before-midnight.md covers the pushed range",
                          got.stdout)

class TestTheArmsThatDecideStillRefuse(unittest.TestCase):
    """The two arms the date was standing in front of, each red-proven on the real gate."""

    def test_a_record_naming_another_range_is_refused_however_it_is_dated(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, head = _tree(tmp)
            _plant(tmp, "2026-09-09-today-and-about-something-else.md",
                   RECORD.format(slug="about something else",
                                 base="0000000", head="1111111"))

            got = _run(tmp, base, today="2026-09-09")

            self.assertEqual(got.returncode, 1, got.stdout + got.stderr)
            self.assertIn("names none of", got.stdout)

    def test_a_record_older_than_the_spec_it_re_checked_is_refused(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, head = _tree(tmp)
            _plant(tmp, "2026-09-09-today-but-stale.md",
                   RECORD.format(slug="today but stale", base=base[:7], head=head[:7]))
            (tmp / "PRODUCT_SPEC.md").write_text("# spec, changed after the record\n",
                                                 encoding="utf-8")
            _git(tmp, "add", "-A")
            _git(tmp, "commit", "-qm", "the spec moves after its review")

            got = _run(tmp, base, today="2026-09-09")

            self.assertEqual(got.returncode, 1, got.stdout + got.stderr)
            self.assertIn("predates the last PRODUCT_SPEC.md change", got.stdout)

    def test_a_tree_with_no_committed_record_at_all_is_refused(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            base, _head = _tree(tmp)

            got = _run(tmp, base, today="2026-09-09")

            self.assertEqual(got.returncode, 1, got.stdout + got.stderr)
            self.assertIn("no committed record at all", got.stdout)

class TestTheWordingSaysWhatTheGateDoes(unittest.TestCase):
    """One rule, one home: what a push prints, and the two documents that describe this gate."""

    def test_the_push_road_reads_no_date(self):
        self.assertNotIn('"$TODAY"*.md', SCRIPT)

    def test_the_wording_a_push_prints_and_the_two_documents_say_what_the_gate_does(self):
        """The banner `guardrails/pre-push` prints on every push, the gate roster copied out of it,
        the CI step name, the record README and the matrix row. A reader meets one of these before
        they meet the script, and each stated the retired rule as current fact."""
        for path, forbidden in (
            (Path(ROOT) / "guardrails" / "pre-push", ("record for today",)),
            (Path(ROOT) / "guardrails" / "README.md", ("record for today", "record dated today")),
            (Path(ROOT) / ".github" / "workflows" / "gates.yml", ("record for today",)),
            (Path(ROOT) / "docs" / "prover" / "README.md", ("a record dated today exists",)),
            (Path(ROOT) / "matrix" / "product-prover.md", ("today-dated-but-stale",)),
        ):
            body = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                self.assertNotIn(phrase, body, "%s still asks for a dated record" % path.name)
        self.assertIn("covers the pushed range", README)


if __name__ == "__main__":
    unittest.main()
