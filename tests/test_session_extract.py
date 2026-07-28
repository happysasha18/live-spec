"""M-483 — the person's own turns become one compact session extract (SPEC INV-302, R303.1..R303.9).

A session transcript is a JSON Lines file where most `user` lines are machines: one live transcript
held 8 human turns against 34 machine lines of the same type. So the extract's whole worth rests on
telling a human turn from a machine one, and on the four traps the 2026-07-28 survey found in the
real files: the sibling directory that holds no human turns, the working directory that changes
mid-file, the machine writing in the human's slot, and the harness wrapper written as human text.

The red-first proof is `test_a_machine_user_line_is_not_a_human_turn`: run against a tree with no
`scripts/session-extract.py`, every test here fails on the missing script.
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "session-extract.py")

REPO = "/Users/somebody/a-project"


def line(**kw):
    """One transcript line, carrying the keys the real files carry."""
    base = {"timestamp": "2026-07-28T18:55:00.000Z", "type": "user", "cwd": REPO,
            "sessionId": "s-1", "isSidechain": False}
    base.update(kw)
    return json.dumps(base)


def human(text, ts="2026-07-28T18:55:00.000Z", cwd=REPO):
    return line(timestamp=ts, cwd=cwd, message={"role": "user", "content": text})


def machine_tool_result():
    return line(toolUseResult={"stdout": "ok"},
                message={"role": "user",
                         "content": [{"type": "tool_result", "content": "ok", "tool_use_id": "t1"}]})


def machine_content_only():
    return line(message={"role": "user",
                         "content": [{"type": "tool_result", "content": "ok", "tool_use_id": "t2"}]})


def assistant_line():
    return line(type="assistant", message={"role": "assistant",
                                           "content": [{"type": "text", "text": "working on it"}]})


def seed(tmp, lines, name="session.jsonl"):
    root = os.path.join(tmp, "projects")
    os.makedirs(root, exist_ok=True)
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return root, path


def run(root, out, extra=()):
    return subprocess.run(["python3", SCRIPT, "--root", root, "--repo", REPO, "--out", out] + list(extra),
                          capture_output=True, text=True)


class TestSessionExtract(unittest.TestCase):

    def test_a_machine_user_line_is_not_a_human_turn(self):
        """RED-FIRST: a user line carrying a tool result is a machine, and it never reaches the extract."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("build the thing"), machine_tool_result(),
                                 machine_content_only(), assistant_line()])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("build the thing", text)
            self.assertNotIn("tool_result", text)
            self.assertNotIn("working on it", text)

    def test_a_wrapper_only_turn_is_dropped(self):
        """A turn whose whole text is a harness wrapper carries none of the person's words."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("<system-reminder>the memory file says X</system-reminder>"),
                                 human("real words here")])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("real words here", text)
            self.assertNotIn("the memory file says X", text)

    def test_a_wrapper_is_stripped_from_a_turn_with_real_words(self):
        """A wrapper riding beside the person's own words is stripped, and the words are kept."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("<command-name>/loop</command-name>keep this sentence")])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("keep this sentence", text)
            self.assertNotIn("/loop", text)

    def test_a_file_naming_the_repository_path_is_taken_whole(self):
        """The opening turns of a session carry the home directory, so the file is picked, not the line."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("the opening turn", cwd="/Users/somebody"),
                                 human("a later turn", cwd=REPO)])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("the opening turn", text)
            self.assertIn("a later turn", text)

    def test_a_turn_carries_its_timestamp_and_its_text(self):
        """Each written turn states when it was said."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("a decision I made", ts="2026-07-28T16:55:00.000Z")])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("2026-07-28", text)
            self.assertIn("a decision I made", text)

    def test_the_run_states_its_reach(self):
        """The green line names the transcript it read, the turns it found, and both file sizes."""
        with tempfile.TemporaryDirectory() as tmp:
            root, path = seed(tmp, [human("one"), human("two"), machine_tool_result()])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("reach:", r.stdout)
            self.assertIn(os.path.basename(path), r.stdout)
            self.assertIn("2", r.stdout)
            self.assertIn("bytes", r.stdout)

    def test_an_extract_is_smaller_than_its_transcript(self):
        """The point of the file is size: a cheap reader takes the extract, never the raw transcript."""
        with tempfile.TemporaryDirectory() as tmp:
            noise = [machine_tool_result() for _ in range(40)]
            root, path = seed(tmp, [human("the one thing I said")] + noise)
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertLess(os.path.getsize(out), os.path.getsize(path))

    def test_no_matching_transcript_reds_by_name(self):
        """A run that matched nothing reds and says what it read nothing of, never writing an empty extract."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("a turn from another project", cwd="/Users/somebody/elsewhere")
                                 .replace(REPO, "/Users/somebody/elsewhere")])
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 1, "a run over no matching transcript passed:\n%s" % r.stdout)
            self.assertIn("session-extract", r.stdout)
            self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
