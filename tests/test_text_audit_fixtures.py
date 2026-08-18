"""The planted-defect texts under `evals/fixtures/text-audit/` still carry their defects.

WHY THIS TEST EXISTS. A check is worth nothing until a text with a known defect proves the check
reports it. On 2026-08-04 a rewrite of eleven skill files dropped phrases the suite required, and no
one put the old and the new version side by side. The repair was a checklist,
`skills/text-audit/references/rewrite-meaning-check.md`. A checklist nobody can fail is a page of
good intentions, so three short texts came in beside it, each carrying one defect on purpose:

  - `ambiguous-explanation.md` — three criteria use a relational word and leave its slot empty. A
    reader cannot say how long "some time" runs, how long an "appropriate stretch" lasts, or how soon
    "quickly" is. `guardrails/check-weak-words.py` reports all three.
  - `rewrite-weakens-the-rule.md` — a paragraph and the rewrite offered in its place. The rewrite
    changes the actor (administrator becomes user), softens the force (must becomes should), and
    drops the legal-hold exception. No shipped check reports any of it.
  - `clean-prose-wrong-command.md` — prose that reads clean and teaches a command that fails. It
    names an output file this tree does not build and omits the flag the builder needs. No shipped
    check reports it.

WHAT THIS HOLDS. For the first text, that the weak-word gate still names all three unfilled slots,
and that the other two spec-format gates stay green there, so the red is the planted defect alone.
For the other two texts, that the planted defect still stands in the words, and that every prose
lint this project ships passes the text. Those two texts are covered by a reading rather than by a
script: step 1 of `skills/text-audit/references/rewrite-meaning-check.md` for the weakened rewrite,
and step 2 for the wrong command. Their passing lints are the evidence that the gap is real. A
future check that closes either gap turns the matching test red, which is the moment to move that
fixture into the caught column.

A fixture added to the directory without a row in FIXTURES below fails here, so no planted text sits
in the tree with nobody saying what catches it.

Reach: this test reads the three files under `evals/fixtures/text-audit/`, and it runs
`guardrails/check-weak-words.py`, `guardrails/check-vocabulary.py`,
`guardrails/check-requirement-shape.py`, `scripts/preshow-register-lint.py`, and
`scripts/spec-style-lint.py` over them. It reads the usage block of `scripts/build-index.py` and
asks the filesystem whether two index paths exist. It writes nothing and edits no check.
"""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(ROOT, "evals", "fixtures", "text-audit")

# Every fixture in the directory, with the check that reports its planted defect. A value of None
# says no shipped script reports it and a reading carries it instead.
FIXTURES = {
    "ambiguous-explanation.md": "guardrails/check-weak-words.py",
    "rewrite-weakens-the-rule.md": None,
    "clean-prose-wrong-command.md": None,
}

# The lints this project ships for plain human-facing prose. Both take the file as their last
# argument and exit 0 on a clean read.
PROSE_LINTS = (
    ("scripts/preshow-register-lint.py", ()),
    ("scripts/spec-style-lint.py", ("--tier", "full")),
)


def fixture(name):
    return os.path.join(FIXTURE_DIR, name)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def run(script_rel, *args):
    """A shipped check's exit code and its whole printed output, run from the repository root."""
    proc = subprocess.run([sys.executable, os.path.join(ROOT, script_rel)] + list(args),
                          cwd=ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


class TestTheFixtureSetShips(unittest.TestCase):
    def test_every_fixture_named_here_is_on_disk(self):
        for name in FIXTURES:
            self.assertTrue(os.path.isfile(fixture(name)),
                            "%s names a fixture that is not in %s" % (name, FIXTURE_DIR))

    def test_every_fixture_on_disk_says_what_catches_it(self):
        found = sorted(n for n in os.listdir(FIXTURE_DIR) if n.endswith(".md"))
        self.assertEqual(sorted(FIXTURES), found,
                         "a fixture in %s carries no row in this test's FIXTURES table, so nothing "
                         "says which check reports its planted defect" % FIXTURE_DIR)


class TestAmbiguousExplanation(unittest.TestCase):
    """The unfilled relational slots, which a shipped script does report."""

    NAME = "ambiguous-explanation.md"

    def test_the_weak_word_gate_names_all_three_unfilled_slots(self):
        code, out = run("guardrails/check-weak-words.py", fixture(self.NAME))
        self.assertEqual(1, code,
                         "guardrails/check-weak-words.py passed %s, whose three criteria each leave "
                         "a relational word's slot empty:\n%s" % (self.NAME, out))
        self.assertIn("3 weak-word violation(s)", out,
                      "the gate reported a different number of unfilled slots:\n%s" % out)
        for word in ("some", "appropriate", "quickly"):
            self.assertIn(word, out,
                          "the gate no longer names the weak word %r planted in %s:\n%s"
                          % (word, self.NAME, out))

    def test_the_fixture_s_other_spec_gates_stay_green(self):
        # The fixture carries ONE planted defect. A second red here would mean the weak-word result
        # above rides on a malformed document rather than on the planted words.
        for script in ("guardrails/check-requirement-shape.py", "guardrails/check-vocabulary.py"):
            code, out = run(script, fixture(self.NAME))
            self.assertEqual(0, code,
                             "%s reds on %s, so the fixture carries a second defect:\n%s"
                             % (script, self.NAME, out))


class TestRewriteWeakensTheRule(unittest.TestCase):
    """The actor, the force, and the exception a rewrite dropped. Covered by a reading."""

    NAME = "rewrite-weakens-the-rule.md"

    def test_the_three_planted_changes_still_stand_in_the_words(self):
        body = read(fixture(self.NAME))
        self.assertIn("When an administrator closes a workspace", body,
                      "the first version no longer names the administrator, so the actor change is gone")
        self.assertIn("the service must keep", body,
                      "the first version no longer says must, so the force change is gone")
        self.assertIn("When a user closes a workspace", body,
                      "the rewrite no longer names the user, so the actor change is gone")
        self.assertIn("the service should keep", body,
                      "the rewrite no longer says should, so the force change is gone")
        self.assertEqual(1, body.count("legal hold"),
                         "the legal-hold exception stands in exactly one of the two versions; the "
                         "dropped exception is the third planted change")

    def test_no_shipped_prose_lint_reports_the_weakening(self):
        # This is the finding the fixture exists to record: the pack ships no script that reads two
        # versions of a rule together. Step 1 of skills/text-audit/references/rewrite-meaning-check.md
        # is what covers it, and a person or a reading session performs it.
        for script, extra in PROSE_LINTS:
            code, out = run(script, *(list(extra) + [fixture(self.NAME)]))
            self.assertEqual(0, code,
                             "%s now reports something on %s. Read the output: if it names the "
                             "changed actor, the softened force, or the dropped exception, this "
                             "fixture is now caught by a script and its row moves:\n%s"
                             % (script, self.NAME, out))


class TestCleanProseWrongCommand(unittest.TestCase):
    """Prose that reads clean and teaches a command that fails. Covered by a reading."""

    NAME = "clean-prose-wrong-command.md"

    def test_the_output_file_the_text_teaches_does_not_exist(self):
        body = read(fixture(self.NAME))
        self.assertIn("PRODUCT_SPEC.index.json", body,
                      "the fixture no longer names the wrong output file, so the defect is gone")
        self.assertFalse(os.path.exists(os.path.join(ROOT, "PRODUCT_SPEC.index.json")),
                         "PRODUCT_SPEC.index.json now exists, so the fixture's command is no longer "
                         "wrong; plant a different defect or retire the fixture")
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "PRODUCT_SPEC.index.md")),
                        "the table this tree really builds, PRODUCT_SPEC.index.md, is gone")

    def test_the_taught_command_omits_the_flag_the_builder_needs(self):
        builder = read(os.path.join(ROOT, "scripts", "build-index.py"))
        self.assertIn("build-index.py <document.md> [<part.md> ...] -o <file>", builder,
                      "scripts/build-index.py changed the way it takes an output file; re-read the "
                      "fixture's command against the new usage")
        body = read(fixture(self.NAME))
        self.assertIn("python3 scripts/build-index.py PRODUCT_SPEC.md PRODUCT_SPEC.index.json", body,
                      "the fixture no longer teaches the flagless command, so the defect is gone")

    def test_no_shipped_prose_lint_reports_the_wrong_command(self):
        # The second half of the plant: the paragraph reads clean, so a readability pass returns
        # nothing. Step 2 of skills/text-audit/references/rewrite-meaning-check.md is what covers it —
        # resolve every path the text names and run every command it teaches.
        for script, extra in PROSE_LINTS:
            code, out = run(script, *(list(extra) + [fixture(self.NAME)]))
            self.assertEqual(0, code,
                             "%s now reports something on %s. If it names the wrong output file or "
                             "the missing flag, this fixture is now caught by a script:\n%s"
                             % (script, self.NAME, out))


if __name__ == "__main__":
    unittest.main()
