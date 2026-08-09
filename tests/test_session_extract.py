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


def run(root, out, extra=(), repo=REPO):
    return subprocess.run(["python3", SCRIPT, "--root", root, "--repo", repo, "--out", out] + list(extra),
                          capture_output=True, text=True)


def two_transcripts(tmp):
    """Two transcripts naming one repository, the second written a minute after the first."""
    root, mine = seed(tmp, [human("the turn of my own session")], name="s-mine.jsonl")
    root, other = seed(tmp, [human("the turn of the other lane")], name="s-other.jsonl")
    os.utime(mine, (1000, 1000))
    os.utime(other, (2000, 2000))
    return root, mine, other


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


class TestWhichTranscriptIsRead(unittest.TestCase):
    """M-488, M-489 — the run reads the transcript named for one session identity (R303.27..R303.31)."""

    def test_a_named_session_reads_its_own_transcript(self):
        """RED-FIRST: two lanes are live, and the named session gets its own file, never the newest."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _, _ = two_transcripts(tmp)
            out = os.path.join(tmp, "extract.md")
            r = run(root, out, ["--session", "s-mine"])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("the turn of my own session", text)
            self.assertNotIn("the turn of the other lane", text)

    def test_a_leading_part_of_an_identity_names_one_transcript(self):
        """An operator typing the head of an identity is served while one file answers to it."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = seed(tmp, [human("the turn of my own session")],
                           name="176e927f-4e67-4fa6-887e-86d1d6e5d1e4.jsonl")
            seed(tmp, [human("the turn of the other lane")], name="0014d5ce-16b2-4ae1-ba25-7a83b98d.jsonl")
            out = os.path.join(tmp, "extract.md")
            r = run(root, out, ["--session", "176e927f"])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("the turn of my own session", text)
            self.assertNotIn("the turn of the other lane", text)

    def test_an_unnamed_run_takes_the_newest_and_says_how_many(self):
        """An operator running by hand keeps the newest file, and the run says what it chose among."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _, other = two_transcripts(tmp)
            out = os.path.join(tmp, "extract.md")
            r = run(root, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                self.assertIn("the turn of the other lane", f.read())
            self.assertIn("no session named", r.stdout)
            self.assertIn("2", r.stdout)
            self.assertIn(os.path.basename(other), r.stdout)

    def test_an_identity_matching_no_transcript_refuses_by_name(self):
        """An identity nothing answers to reds, names the identity, and writes no extract."""
        with tempfile.TemporaryDirectory() as tmp:
            root, _, _ = two_transcripts(tmp)
            out = os.path.join(tmp, "extract.md")
            r = run(root, out, ["--session", "s-nobody"])
            self.assertEqual(r.returncode, 1, "an unmatched identity passed:\n%s" % r.stdout)
            self.assertIn("s-nobody", r.stdout)
            self.assertIn(root, r.stdout)
            self.assertFalse(os.path.exists(out))

    def test_an_identity_matching_several_refuses_and_names_them(self):
        """An identity two files answer to reds and prints both paths, so the caller can choose."""
        with tempfile.TemporaryDirectory() as tmp:
            root, first = seed(tmp, [human("the first lane")], name="s-1a.jsonl")
            root, second = seed(tmp, [human("the second lane")], name="s-1b.jsonl")
            out = os.path.join(tmp, "extract.md")
            r = run(root, out, ["--session", "s-1"])
            self.assertEqual(r.returncode, 1, "an undecided identity passed:\n%s" % r.stdout)
            self.assertIn(os.path.basename(first), r.stdout)
            self.assertIn(os.path.basename(second), r.stdout)
            self.assertFalse(os.path.exists(out))


class TestWhereTheExtractLands(unittest.TestCase):
    """M-490 — an output path landing inside the repository is refused (R303.8, R303.32, R303.33)."""

    def seed_repo(self, tmp):
        """A scratch repository, one transcript naming it, and its handover directory."""
        repo = os.path.join(tmp, "repo")
        os.makedirs(os.path.join(repo, "docs", "handovers"))
        root, _ = seed(tmp, [human("a decision I made", cwd=repo)])
        return repo, root

    def test_an_output_path_inside_the_repository_is_refused(self):
        """A closing agent pointing the extract at the tree is refused, and nothing is written."""
        with tempfile.TemporaryDirectory() as tmp:
            repo, root = self.seed_repo(tmp)
            out = os.path.join(repo, "docs", "handovers", "2026-07-29-extract.md")
            r = run(root, out, repo=repo)
            self.assertEqual(r.returncode, 1, "an in-tree output path passed:\n%s" % r.stdout)
            self.assertIn(out, r.stdout)
            self.assertIn("repository", r.stdout)
            self.assertFalse(os.path.exists(out))

    def test_a_path_holding_dot_dot_is_judged_by_where_it_lands(self):
        """A path walking out and back in lands in the tree, so it is refused."""
        with tempfile.TemporaryDirectory() as tmp:
            repo, root = self.seed_repo(tmp)
            os.makedirs(os.path.join(tmp, "outside"))
            out = os.path.join(tmp, "outside", "..", "repo", "docs", "extract.md")
            r = run(root, out, repo=repo)
            self.assertEqual(r.returncode, 1, "a path holding .. passed:\n%s" % r.stdout)
            self.assertFalse(os.path.exists(os.path.join(repo, "docs", "extract.md")))

    def test_a_symbolic_link_into_the_repository_is_refused(self):
        """A link pointing at the tree is judged by what it points at."""
        with tempfile.TemporaryDirectory() as tmp:
            repo, root = self.seed_repo(tmp)
            link = os.path.join(tmp, "link")
            os.symlink(repo, link)
            out = os.path.join(link, "docs", "extract.md")
            r = run(root, out, repo=repo)
            self.assertEqual(r.returncode, 1, "a link into the tree passed:\n%s" % r.stdout)
            self.assertFalse(os.path.exists(os.path.join(repo, "docs", "extract.md")))

    def test_an_output_path_outside_the_repository_is_written(self):
        """The scratch directory the law asks for keeps working, so the refusal reaches it never."""
        with tempfile.TemporaryDirectory() as tmp:
            repo, root = self.seed_repo(tmp)
            out = os.path.join(tmp, "scratch", "extract.md")
            os.makedirs(os.path.dirname(out))
            r = run(root, out, repo=repo)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as f:
                self.assertIn("a decision I made", f.read())


if __name__ == "__main__":
    unittest.main()
