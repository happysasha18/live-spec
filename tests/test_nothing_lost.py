"""Trimming a long document never loses what moved (PLAN.md q-531).

`scripts/nothing-lost.py` takes the document as it stood and the files it became, and prints the
blocks of the old document that none of the new files account for. Empty output and exit 0 mean
every word and every mark survived somewhere; a block that did not survive is printed whole and the
exit code is 1.

The proofs below run it both ways, so the red is proved rather than assumed:

  - a legitimate split -- sections reordered into two files, paragraphs rewrapped, list indentation
    changed, a table reflowed, new part titles added -- prints nothing and exits 0;
  - and one dropped thing at a time -- a paragraph, a sentence off the end of a paragraph, a table
    row, a footnote, a citation, an inline code span, a line inside a code fence, a list item, a
    heading -- each prints the thing and exits 1.

The last two proofs run the command over real splits this repository already performed, at the size
the photo site's spec is about to be converted at:

  - b344d33c cut ARCHITECTURE.md (93 KB) into a core and 15 architecture/*.md parts. The command
    reads its 594 blocks and prints an empty difference: a real split, really lossless.
  - d79fc334 moved 310 requirements out of PRODUCT_SPEC.md (703 KB) into 30 spec/*.md parts and
    deleted the trailing `## Reference` table on purpose. The command prints the deleted table and
    nothing else -- every block of the document that sits above that heading survived the move.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from conftest import ROOT

COMMAND = os.path.join(ROOT, "scripts", "nothing-lost.py")

# Two real splits this repository performed, both of a document large enough to be unreadable by
# hand: one that lost nothing, one that deleted a section on purpose.
ARCHITECTURE_SPLIT = "b344d33c"   # ARCHITECTURE.md -> core + 15 architecture/*.md parts
SPEC_SPLIT = "d79fc334"           # PRODUCT_SPEC.md -> core + 30 spec/*.md parts


def run(before, after, stdin=None):
    """Run the command; return (exit_code, stdout, stderr)."""
    cmd = [sys.executable, COMMAND, "--before", before, "--after"] + list(after)
    p = subprocess.run(cmd, capture_output=True, text=True, input=stdin)
    return p.returncode, p.stdout, p.stderr


# ---- fixtures ---------------------------------------------------------------

BEFORE = """\
# The long document

This document stood as one file before the split. It carries a preamble, two sections, a table,
a list, a fenced example, and a footnote, so that every kind of mark has somewhere to hide.

## The first section

The first section states the rule and then qualifies it. A restructure is free to rewrap this
paragraph across different line lengths; that is not loss. What it may not do is drop a sentence
off the end and call the move complete.

- the first item of the list
- the second item, which runs long enough to wrap onto a continuation line
  when the file it lands in is narrower than the one it came from
- the third item, carrying an `inline code span` that has to survive

| Mark | Where it lives | Kept |
|---|---|---|
| heading | the `#` prefix | yes |
| bullet | the `-` prefix | yes |
| footnote | the `[^1]` marker | yes |

## The second section

The second section carries the example, which is a fenced block whose inner whitespace means
something, and a citation nobody may quietly drop.[^1]

```python
def keep(text):
    if not text:
        return None
    return text.strip()
```

See also the Rossum citation, 1991, page 14, which the second section rests on.

[^1]: The footnote itself, which is a block of the document like any other.
"""

# The legitimate split: the SECOND section moves into its own file and lands first in the argument
# list, paragraphs are rewrapped at different widths, the list is indented under a new parent, the
# table's cell padding is reflowed, and each part gains a title of its own.
AFTER_PART_TWO = """\
# Part two -- the second section

## The second section

The second section carries the example,
which is a fenced block whose inner whitespace
means something, and a citation nobody may quietly drop.[^1]

  ```python
  def keep(text):
      if not text:
          return None
      return text.strip()
  ```

See also the Rossum citation, 1991, page 14, which the second section rests on.

[^1]: The footnote itself, which is a block of the document like any other.
"""

AFTER_PART_ONE = """\
# Part one -- the preamble and the first section

# The long document

This document stood as one file before the split. It carries a preamble, two sections,
a table, a list, a fenced example, and a footnote, so that every kind of mark has
somewhere to hide.

## The first section

The first section states the rule and then qualifies it.
A restructure is free to rewrap this paragraph across different line lengths;
that is not loss. What it may not do is drop a sentence off the end and call the move complete.

  - the first item of the list
  - the second item, which runs long enough to wrap onto a continuation line when the file it lands in is narrower than the one it came from
  - the third item, carrying an `inline code span` that has to survive

|   Mark   |    Where it lives     | Kept |
| --- | --- | --- |
|  heading  |  the `#` prefix  |  yes  |
|  bullet  |  the `-` prefix  |  yes  |
|  footnote  |  the `[^1]` marker  |  yes  |
"""


class NothingLostCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="nothing-lost-fixture-")
        self.before = self.write("before.md", BEFORE)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def split(self, part_one=AFTER_PART_ONE, part_two=AFTER_PART_TWO):
        """The files the document became, in the order a shell glob would hand them over."""
        return [self.write("part_one.md", part_one), self.write("part_two.md", part_two)]

    def assertLost(self, after, needle):
        code, out, _err = run(self.before, after)
        self.assertEqual(code, 1, "a split that drops content must exit non-zero:\n" + out)
        self.assertIn(needle, out, "the command must print what it could not account for")
        return out


class TestALegitimateSplitPrintsNothing(NothingLostCase):
    def test_reordered_rewrapped_reindented_split_is_green(self):
        code, out, err = run(self.before, self.split())
        self.assertEqual(out, "", "a split that lost nothing prints an empty difference")
        self.assertEqual(code, 0, "a split that lost nothing exits 0:\n" + err)

    def test_the_summary_names_what_the_restructure_added(self):
        # The two new part titles are additions, not loss: they are counted, and they do not red.
        _code, _out, err = run(self.before, self.split())
        self.assertIn("2 added by the restructure", err)

    def test_a_document_read_from_stdin_is_the_same_document(self):
        # `git show REV:doc.md | nothing-lost.py --before - --after ...` is how a split already
        # committed gets checked, so the pipe has to read as the file does.
        code, out, _err = run("-", self.split(), stdin=BEFORE)
        self.assertEqual((code, out), (0, ""))

    def test_the_same_files_read_twice_are_not_double_credit(self):
        # A multiset, not a set: handing the same part twice does not excuse a missing one.
        parts = self.split()
        code, out, _err = run(self.before, [parts[0], parts[0]])
        self.assertEqual(code, 1, "the second section is gone; a repeated part one cannot cover it")
        self.assertIn("The second section carries the example", out)


class TestADroppedThingReds(NothingLostCase):
    def test_a_dropped_paragraph_is_printed(self):
        gone = "The first section states the rule and then qualifies it."
        part_one = AFTER_PART_ONE.replace(
            "The first section states the rule and then qualifies it.\n"
            "A restructure is free to rewrap this paragraph across different line lengths;\n"
            "that is not loss. What it may not do is drop a sentence off the end and call the move complete.\n",
            "")
        self.assertNotIn(gone, part_one, "the fixture must actually drop the paragraph")
        out = self.assertLost(self.split(part_one=part_one), gone)
        # printed whole, not as a fragment: the reader can put it back from what they are shown.
        self.assertIn("drop a sentence off the end and call the move complete.", out)
        self.assertIn("paragraph", out)

    def test_a_paragraph_silently_truncated_reds(self):
        # The words that remain are all present; the sentence that went is what the check is for.
        # A bag of words would pass this and a bag of lines would red on the rewrap above.
        part_one = AFTER_PART_ONE.replace(
            "that is not loss. What it may not do is drop a sentence off the end and call the move complete.",
            "that is not loss.")
        self.assertLost(self.split(part_one=part_one), "drop a sentence off the end")

    def test_a_dropped_table_row_reds(self):
        part_one = AFTER_PART_ONE.replace("|  footnote  |  the `[^1]` marker  |  yes  |\n", "")
        out = self.assertLost(self.split(part_one=part_one), "the `[^1]` marker")
        self.assertIn("table row", out)

    def test_a_dropped_footnote_reds(self):
        part_two = AFTER_PART_TWO.replace(
            "[^1]: The footnote itself, which is a block of the document like any other.\n", "")
        self.assertLost(self.split(part_two=part_two), "The footnote itself")

    def test_a_dropped_citation_reds(self):
        part_two = AFTER_PART_TWO.replace(
            "See also the Rossum citation, 1991, page 14, which the second section rests on.\n", "")
        self.assertLost(self.split(part_two=part_two), "Rossum citation, 1991, page 14")

    def test_a_dropped_inline_code_span_reds(self):
        part_one = AFTER_PART_ONE.replace(
            "carrying an `inline code span` that has to survive",
            "carrying an inline code span that has to survive")
        out = self.assertLost(self.split(part_one=part_one), "`inline code span`")
        self.assertIn("list item", out)

    def test_a_dropped_line_inside_a_code_fence_reds(self):
        part_two = AFTER_PART_TWO.replace("          return None\n", "")
        out = self.assertLost(self.split(part_two=part_two), "return text.strip()")
        self.assertIn("code block", out)

    def test_a_dropped_list_item_reds(self):
        part_one = AFTER_PART_ONE.replace("  - the first item of the list\n", "")
        self.assertLost(self.split(part_one=part_one), "the first item of the list")

    def test_a_dropped_heading_reds(self):
        part_one = AFTER_PART_ONE.replace("## The first section\n", "")
        out = self.assertLost(self.split(part_one=part_one), "## The first section")
        self.assertIn("heading", out)

    def test_a_whole_part_left_out_of_the_after_list_reds(self):
        parts = self.split()
        out = self.assertLost([parts[0]], "The second section carries the example")
        self.assertIn("def keep(text):", out)


class RealSplitCase(unittest.TestCase):
    """The live proofs: real documents of the size this exists for, really split, checked after."""

    COMMIT = None

    def setUp(self):
        if _git("cat-file", "-e", self.COMMIT + "^{commit}") is None:
            raise unittest.SkipTest(
                "the split commit %s is not in this checkout (a shallow clone); the live proof "
                "needs its history" % self.COMMIT)
        self.tmp = tempfile.mkdtemp(prefix="nothing-lost-real-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def extract(self, rev, path, tag):
        blob = _git("show", "%s:%s" % (rev, path))
        self.assertIsNotNone(blob, "%s:%s is not readable" % (rev, path))
        local = os.path.join(self.tmp, tag + "_" + path.replace("/", "_"))
        with open(local, "w", encoding="utf-8") as f:
            f.write(blob)
        return local

    def before_and_after(self, core, part_dir):
        """The document as it stood one commit earlier, and the files it became."""
        before = self.extract(self.COMMIT + "^", core, "before")
        listing = _git("ls-tree", "--name-only", self.COMMIT, part_dir)
        parts = [p for p in listing.splitlines() if p.endswith(".md")]
        self.assertGreater(len(parts), 10, "the split produced a part file per section")
        after = [self.extract(self.COMMIT, p, "after") for p in [core] + parts]
        return before, after


class TestARealSplitThatLostNothing(RealSplitCase):
    COMMIT = ARCHITECTURE_SPLIT

    def test_the_architecture_split_prints_an_empty_difference(self):
        # 93 KB of architecture, cut into a core and 15 parts, checked after the fact: the command
        # accounts for all 594 of its blocks and prints nothing.
        before, after = self.before_and_after("ARCHITECTURE.md", "architecture/")
        code, out, err = run(before, after)
        self.assertEqual(out, "", "a real lossless split must print an empty difference")
        self.assertEqual(code, 0, err)
        self.assertIn("0 missing", err)


class TestARealSplitThatDeletedASectionOnPurpose(RealSplitCase):
    COMMIT = SPEC_SPLIT

    def test_only_the_deleted_reference_tail_is_reported(self):
        # 703 KB of spec, 310 requirements moved into 30 parts, and one trailing `## Reference`
        # table deleted on purpose in the same commit. The command names that table and nothing
        # else: every block above its heading survived the move.
        before, after = self.before_and_after("PRODUCT_SPEC.md", "spec/")
        code, out, _err = run(before, after)
        self.assertEqual(code, 1, "the commit deleted the trailing `## Reference` table")

        with open(before, encoding="utf-8") as f:
            before_lines = f.read().splitlines()
        tail_at = 1 + before_lines.index("## Reference")

        reported = [int(line.rsplit(":", 1)[1].split()[0])
                    for line in out.splitlines()
                    if line.startswith("  " + before) and ":" in line]
        self.assertGreater(len(reported), 100, "the deleted table carried 400 rows")
        self.assertEqual(min(reported), tail_at,
                         "the deleted section's own heading is the first thing reported")
        self.assertTrue(all(n >= tail_at for n in reported),
                        "nothing above the deleted section went missing, and the report says so")


def _git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


if __name__ == "__main__":
    unittest.main()
