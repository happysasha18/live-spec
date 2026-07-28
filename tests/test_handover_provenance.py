"""Gate ab — a session handover names where it was read from (SPEC INV-302, M-484, R303.10..R303.18).

On 2026-07-28 a session wrote its own handover from memory and named a question as waiting for the
owner, though the owner had answered it earlier that day. The repair is that a fresh agent writes the
handover from a session extract. A handover is a committed artifact, so the shape of that provenance
is held by a push gate, and whether the writing agent was truly fresh stays with the session.

The red-first proof is `test_a_handover_with_no_provenance_reds`: a handover dated after the counting
start, carrying none of the three lines, drives `guardrails/check-handover-provenance.py` to a
non-zero exit.
"""
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-handover-provenance.py")

FULL = """# Handover, 2026-08-01 — a movement

## How this handover was written

transcript: ~/.claude/projects/-Users-somebody/abc.jsonl
extract: /tmp/scratch/session-extract-abc.md
written by: a fresh agent session that did not live the work

## What runs right now

Nothing.
"""

NONE = """# Handover, 2026-08-01 — a movement

## What runs right now

Nothing.
"""

PARTIAL = """# Handover, 2026-08-01 — a movement

## How this handover was written

transcript: ~/.claude/projects/-Users-somebody/abc.jsonl

## What runs right now

Nothing.
"""


def write(tmp, name, body):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def run(directory, extra=()):
    return subprocess.run(["python3", GATE, "--dir", directory] + list(extra),
                          capture_output=True, text=True)


class TestHandoverProvenance(unittest.TestCase):

    def test_a_handover_with_no_provenance_reds(self):
        """RED-FIRST: a handover naming none of the three turns the gate red."""
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-a-movement-handover.md", NONE)
            r = run(tmp)
            self.assertEqual(r.returncode, 1, "a handover with no provenance passed:\n%s" % r.stdout)
            self.assertIn("2026-08-01-a-movement-handover.md", r.stdout)

    def test_a_handover_naming_all_three_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-a-movement-handover.md", FULL)
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_a_partial_provenance_reds_and_names_what_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-a-movement-handover.md", PARTIAL)
            r = run(tmp)
            self.assertEqual(r.returncode, 1, "a half-named provenance passed:\n%s" % r.stdout)
            self.assertIn("extract", r.stdout)
            self.assertIn("written by", r.stdout)

    def test_a_handover_before_the_counting_start_is_passed_over(self):
        """A record written before the law reds nothing: the gate carries a counting start."""
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-07-28-readability-campaign-handover.md", NONE)
            write(tmp, "2026-08-01-a-movement-handover.md", FULL)
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_an_empty_directory_reds_rather_than_passing_over_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(tmp)
            self.assertEqual(r.returncode, 1, "a gate over no files passed:\n%s" % r.stdout)
            self.assertIn("no session handover at all", r.stdout)

    def test_a_directory_of_drafts_alone_reds_over_no_subject(self):
        """The emptiness is read over the declared handovers, never the directory's whole contents."""
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-readme-replacement-draft.md", NONE)
            write(tmp, "2026-08-01-row-notes.md", NONE)
            r = run(tmp)
            self.assertEqual(r.returncode, 1, "a directory of drafts alone passed:\n%s" % r.stdout)
            self.assertIn("no session handover at all", r.stdout)

    def test_a_directory_of_only_pre_law_handovers_stands_down_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-07-28-readability-campaign-handover.md", NONE)
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("stands down", r.stdout)

    def test_a_file_that_is_no_handover_is_left_alone(self):
        """The directory also holds drafts and notes, and the gate reads the declared handover name."""
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-readme-replacement-draft.md", NONE)
            write(tmp, "2026-08-01-a-movement-handover.md", FULL)
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertNotIn("readme-replacement-draft", r.stdout)

    def test_the_real_repository_passes(self):
        r = subprocess.run(["python3", GATE], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_the_green_run_states_its_reach(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, "2026-08-01-a-movement-handover.md", FULL)
            r = run(tmp)
            self.assertIn("reach:", r.stdout)
            self.assertIn("check-handover-provenance", r.stdout)


if __name__ == "__main__":
    unittest.main()
