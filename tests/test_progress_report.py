"""scripts/progress-report.py writes docs/PROGRESS.md in one fixed shape every run, so a person
comparing two days compares numbers rather than layouts. This pins: the script runs and writes the
page; the page carries its five sections in the stated order; every table carries its stated
columns; and a number no source provides prints "not stated" rather than a fabricated zero.

The suite never runs the script against its real output path. docs/PROGRESS.md is a PROTECTED
file: a real run regenerates it deliberately, not as a side effect of the test suite. Every
invocation below passes --out at a scratch path under a temp dir this test owns, so a full suite
run reads the tree (cwd stays ROOT, since the script's inputs are ROOT-relative) but writes
nowhere the working tree can see it, and leaves docs/PROGRESS.md untouched.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "progress-report.py")
BASELINE = os.path.join(ROOT, "guardrails", "progress-baseline.json")


def load_progress_report():
    spec = importlib.util.spec_from_file_location("progress_report", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(out_path):
    """Runs the generator with cwd at ROOT (its inputs are ROOT-relative) but --out redirected
    to `out_path`, so nothing under the repository's own tree is written."""
    return subprocess.run([sys.executable, SCRIPT, "--out", out_path], cwd=ROOT,
                          capture_output=True, text=True, timeout=180)


def run_script_and_read(out_path):
    proc = run_script(out_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    with open(out_path, encoding="utf-8") as f:
        return f.read()


def table_after(text, heading, table_caption=None):
    """The markdown table immediately after `heading` (and, when given, after the first line
    containing `table_caption` past that heading) — the header row and every data row, as lists
    of cells."""
    idx = text.index(heading)
    chunk = text[idx:]
    if table_caption:
        chunk = chunk[chunk.index(table_caption):]
    lines = chunk.splitlines()
    # first line starting with "| " is the header row; the next is the "|---|" rule; data follows
    start = next(i for i, ln in enumerate(lines) if ln.startswith("| "))
    rows = []
    for ln in lines[start:]:
        if not ln.startswith("|"):
            break
        if re.match(r"^\|[\s:|-]+\|$", ln):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
    return rows


def priority_section_text(text):
    start = text.index("## The queue, in the plan's order")
    end = text.index("## Promise one")
    return text[start:end]


def priority_groups(text):
    """One `(number, title, rows)` tuple per "### N. Title" block in the queue section, `rows`
    holding each group's table as lists of cells, header row included."""
    sec = priority_section_text(text)
    groups = []
    for chunk in sec.split("### ")[1:]:
        header_line, _, rest = chunk.partition("\n")
        num_str, _, title = header_line.partition(". ")
        lines = rest.strip("\n").splitlines()
        start = next(i for i, ln in enumerate(lines) if ln.startswith("| "))
        rows = []
        for ln in lines[start:]:
            if not ln.startswith("|"):
                break
            if re.match(r"^\|[\s:|-]+\|$", ln):
                continue
            rows.append([c.strip() for c in ln.strip("|").split("|")])
        groups.append((int(num_str), title.strip(), rows))
    return groups


class TestProgressReportRuns(unittest.TestCase):
    def test_script_runs_and_writes_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "PROGRESS.md")
            proc = run_script(out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(os.path.isfile(out), "the script did not write its --out path")
            with open(out, encoding="utf-8") as f:
                text = f.read()
        self.assertTrue(text.startswith("# Progress — the two promises"))


class TestProgressReportShape(unittest.TestCase):
    """Runs once for the class, so every shape assertion reads one fresh page."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.text = run_script_and_read(os.path.join(cls.tmp, "PROGRESS.md"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_six_sections_present_in_order(self):
        headings = [
            "# Progress — the two promises",
            "## Where the two promises stand",
            "## The queue, in the plan's order",
            "## Promise one — a reader gets through a document without stopping",
            "## Promise two — the specification stops growing",
            "## Readings run so far",
            "## What no measure covers",
        ]
        positions = []
        for h in headings:
            self.assertIn(h, self.text, "missing heading: %r" % h)
            positions.append(self.text.index(h))
        self.assertEqual(positions, sorted(positions),
                          "the sections are not in the stated fixed order")

    def test_where_the_two_promises_stand_carries_exactly_two_sentences(self):
        start = self.text.index("## Where the two promises stand")
        end = self.text.index("## The queue, in the plan's order")
        body = self.text[start:end].split("\n\n")
        sentences = [p.strip() for p in body if p.strip() and not p.strip().startswith("#")]
        self.assertEqual(len(sentences), 2, sentences)

    def test_table_a_has_its_stated_columns(self):
        rows = table_after(self.text, "## Promise one", "| measure |")
        self.assertEqual(rows[0], ["measure", "today", "recorded before", "target"])
        measures = [r[0] for r in rows[1:]]
        self.assertEqual(measures, [
            "live documents measured",
            "writing findings across all documents",
            "documents at zero findings",
            "documents that passed two consecutive readings with nothing blocking",
        ])

    def test_table_b_has_its_stated_columns(self):
        rows = table_after(self.text, "## Promise one", "| document |")
        self.assertEqual(rows[0], ["document", "findings", "of which long sentences", "style",
                                    "longest sentence", "readings run", "passed"])
        self.assertLessEqual(len(rows) - 1, 15)

    def test_table_c_has_its_stated_columns(self):
        rows = table_after(self.text, "## Promise two", "| measure |")
        # The "ceiling" column between the format-change reading and the target went with the two
        # bounds that filled it — the size ratchet's recorded bytes-per-criterion and the redundancy
        # cap — cut 2026-09-02. Every other cell in it already read "not stated".
        self.assertEqual(rows[0], ["measure", "today", "at the format change, 2026-07-23",
                                    "target"])
        measures = [r[0] for r in rows[1:]]
        self.assertEqual(measures, [
            "bytes", "lines", "words", "requirements", "acceptance criteria",
            "bytes per criterion", "pairs stating one fact twice",
        ])

    def test_readings_table_has_its_stated_columns(self):
        rows = table_after(self.text, "## Readings run so far", "| date |")
        self.assertEqual(rows[0], ["date", "document read", "reading number",
                                    "blocking stops left"])

    def test_readings_table_sorted_by_date_then_number(self):
        rows = table_after(self.text, "## Readings run so far", "| date |")[1:]
        keys = [(r[0], int(r[2])) for r in rows]
        self.assertEqual(keys, sorted(keys))


class TestQueueSection(unittest.TestCase):
    """The queue, in the plan's order — the ten priority groups, and the states derived from
    them (SPEC row: docs/plans/2026-07-28-two-goals-one-campaign.md, "The order of documents")."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.text = run_script_and_read(os.path.join(cls.tmp, "PROGRESS.md"))
        with open(BASELINE, encoding="utf-8") as f:
            cls.baseline = json.load(f)
        cls.groups = priority_groups(cls.text)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_ten_groups_in_the_plans_order(self):
        self.assertEqual(len(self.groups), 10)
        numbers = [g[0] for g in self.groups]
        self.assertEqual(numbers, list(range(1, 11)))
        baseline_titles = {g["number"]: g["title"] for g in self.baseline["priority"]["groups"]}
        for num, title, _ in self.groups:
            self.assertEqual(title, baseline_titles[num])

    def test_group_tables_carry_their_stated_columns(self):
        for _, _, rows in self.groups:
            self.assertEqual(rows[0], ["#", "document", "findings today", "measured clean",
                                        "read clean", "state"])

    def test_exactly_one_row_reads_in_hand(self):
        states = [row[5] for _, _, rows in self.groups for row in rows[1:]]
        self.assertEqual(states.count("in hand"), 1, states)

    def test_a_file_with_no_record_entry_prints_not_measured_not_zero(self):
        _, _, rows = self.groups[0]
        row = rows[1]
        self.assertEqual(row[1], "`hooks/chat-law-hook.sh`")
        self.assertEqual(row[2], "not measured")
        self.assertNotEqual(row[2], "0")


class TestTargetsAndNoComparison(unittest.TestCase):
    """Table A's and Table C's target columns read the baseline file. The page states what the
    tree holds today only — no sentence anywhere on it may compare this run against a previous
    one."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.text = run_script_and_read(os.path.join(cls.tmp, "PROGRESS.md"))
        with open(BASELINE, encoding="utf-8") as f:
            cls.baseline = json.load(f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_target_column_prints_a_baseline_value(self):
        targets = self.baseline["targets"]
        for heading in ("## Promise one", "## Promise two"):
            rows = table_after(self.text, heading, "| measure |")
            for row in rows[1:]:
                expected = targets.get(row[0], {}).get("value", "not stated")
                self.assertEqual(row[-1], expected, row)

    def test_the_page_never_carries_a_run_to_run_comparison(self):
        """A generated page states the tree as it stands today, never what moved since a prior
        run. This fails the moment "Since the last run" or a "changed by" delta returns."""
        self.assertNotIn("Since the last run", self.text)
        self.assertNotIn("changed by", self.text)
        self.assertNotRegex(self.text, r"[Cc]ompared to (the )?(last|previous) run")


class TestNotStatedNotZero(unittest.TestCase):
    """A number no source provides prints "not stated", never a fabricated zero."""

    def test_fmt_of_none_is_not_stated(self):
        m = load_progress_report()
        self.assertEqual(m.fmt(None), "not stated")
        self.assertNotEqual(m.fmt(None), "0")

    def test_fmt_pct_of_none_is_not_stated(self):
        m = load_progress_report()
        self.assertEqual(m.fmt_pct(None), "not stated")

    def test_a_read_record_with_no_stated_blocking_count_parses_as_none(self):
        m = load_progress_report()
        text = ("# Blind read, 2026-01-01 — a document with no blocking count stated\n\n"
                "Text read: `PRODUCT_SPEC.md`, a paragraph.\n\n"
                "This record states no blocking count anywhere in its body.\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "2026-01-01-read99-no-count.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            record = m.parse_read_record(path)
        self.assertIsNone(record["blocking"])

    def test_the_live_page_prints_not_stated_for_an_unsourced_cell(self):
        """Table C's "lines" row carries no baseline entry for the format-change column (the
        seed file only records bytes, requirements, and acceptance criteria at that date), so
        the live page must print "not stated" there rather than 0."""
        with tempfile.TemporaryDirectory() as tmp:
            text = run_script_and_read(os.path.join(tmp, "PROGRESS.md"))
        rows = table_after(text, "## Promise two", "| measure |")
        by_measure = {r[0]: r for r in rows[1:]}
        self.assertEqual(by_measure["lines"][2], "not stated")
        self.assertNotEqual(by_measure["lines"][2], "0")


if __name__ == "__main__":
    unittest.main()
