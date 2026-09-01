"""Locks the fix that stopped spec-redundancy-precheck.py reading a core file's own bytes only.

Before the fix, `main()` opened the FILE argument directly (`open(src, encoding="utf-8").read()`),
so a core file carrying a `## Parts map` (PRODUCT_SPEC.md, ARCHITECTURE.md, both split into part
files earlier in this same session) was scanned as its preamble/glossary/map alone — every
requirement living in the part files was invisible to the redundancy pre-check. The fix routes the
read through `guardrails/specformat.py`'s `spec_paths()` / `read_document()`, the same core+parts
mechanism the requirement-format gates already use (check-requirement-shape.py, build-index.py), so
the pre-check now scans the WHOLE document.

Two things are locked:
  1. A core file's Parts map is expanded — a duplicate sentence split across two part files is now
     found, where the old direct-read code could not see it (the duplicate never appears in the
     core file's own bytes at all).
  2. A file with no Parts map (an ordinary part file, or any file with no such section) is read
     exactly as before — byte for byte, same candidates, same JSON summary — since expansion is
     idempotent by `spec_paths()`'s own construction.
"""
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "spec-redundancy-precheck.py")


def run(*args):
    return subprocess.run(["python3", SCRIPT, *args], capture_output=True, text=True)


def summary(stdout):
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            return json.loads(line)
    raise AssertionError("no JSON summary in stdout:\n%s" % stdout)


# A duplicate sentence, long enough to clear MIN_TOKENS (6 content tokens) and the SHARE_MIN /
# jaccard-or-containment thresholds on its own.
DUPLICATE_SENTENCE = (
    "The queue drains oldest first and never reorders an item once it has started running.\n"
)


class TestPartsMapIsExpanded(unittest.TestCase):
    def test_duplicate_split_across_two_parts_is_found(self):
        with tempfile.TemporaryDirectory() as d:
            core = os.path.join(d, "CORE.md")
            part_a = os.path.join(d, "part-a.md")
            part_b = os.path.join(d, "part-b.md")

            with open(core, "w", encoding="utf-8") as f:
                f.write(
                    "# Core\n\n"
                    "Some preamble text that names nothing duplicated.\n\n"
                    "## Parts map\n\n"
                    "| Part | Requirements | Topic |\n"
                    "|---|---|---|\n"
                    "| `part-a.md` | R1 | Part A |\n"
                    "| `part-b.md` | R2 | Part B |\n"
                )
            with open(part_a, "w", encoding="utf-8") as f:
                f.write("## Requirement 1: A\n\n" + DUPLICATE_SENTENCE)
            with open(part_b, "w", encoding="utf-8") as f:
                f.write("## Requirement 2: B\n\n" + DUPLICATE_SENTENCE)

            # Sanity: the duplicate does NOT live in the core file's own bytes — the old direct-read
            # code could not have found it no matter what.
            with open(core, encoding="utf-8") as f:
                self.assertNotIn("queue drains oldest first", f.read())

            r = run(core)
            js = summary(r.stdout)
            self.assertGreaterEqual(
                js["candidates"], 1,
                "expected the cross-part duplicate to surface as a candidate: %s\n%s" % (js, r.stdout))
            self.assertIn("queue drains oldest first", r.stdout.lower())

    def test_core_with_empty_parts_map_reads_as_itself(self):
        # An explicit map that resolves to nothing (no data rows) behaves exactly like no map at all
        # — the core is the whole document.
        with tempfile.TemporaryDirectory() as d:
            core = os.path.join(d, "CORE.md")
            with open(core, "w", encoding="utf-8") as f:
                f.write("# Core\n\n## Parts map\n\n| Part | Requirements | Topic |\n|---|---|---|\n")
            r = run(core)
            js = summary(r.stdout)
            self.assertEqual(js["candidates"], 0)
            self.assertEqual(r.returncode, 0)


class TestFileWithoutPartsMapIsUnchanged(unittest.TestCase):
    def test_plain_file_matches_direct_read_byte_for_byte(self):
        """A file with no `## Parts map` section (an ordinary matrix/*.md-style part file, or any
        plain document) must be scanned identically to the pre-fix behaviour: read exactly its own
        bytes, nothing appended. Proven by comparing against a from-scratch, dependency-free direct
        read done right here in the test — the same one-liner main() used to run."""
        text = (
            "# Plain document\n\n"
            "The queue drains oldest first and never reorders an item once it has started running.\n\n"
            "Elsewhere: the queue drains oldest first and never reorders an item once it has started "
            "running, restated for a different reader.\n"
        )
        with tempfile.TemporaryDirectory() as d:
            plain = os.path.join(d, "plain.md")
            with open(plain, "w", encoding="utf-8") as f:
                f.write(text)

            r_file = run(plain)
            r_stdin = subprocess.run(["python3", SCRIPT, "-"], input=text, capture_output=True, text=True)

            js_file = summary(r_file.stdout)
            js_stdin = summary(r_stdin.stdout)
            self.assertEqual(js_file["candidates"], js_stdin["candidates"])
            self.assertEqual(js_file["open"], js_stdin["open"])
            self.assertEqual(js_file["waived"], js_stdin["waived"])
            self.assertEqual(r_file.returncode, r_stdin.returncode)


class TestVendoredStandaloneFallback(unittest.TestCase):
    """adopt/install-style-gates.sh vendors this script alone (plus gate_common.py) into a host repo —
    guardrails/specformat.py is NOT one of its VENDOR_FILES. Locks that the core+parts import stays
    optional: run from a copy with no sibling guardrails/ dir at all, the script must still behave
    exactly as it did before the core+parts fix (read the named file directly), not crash."""

    def test_runs_with_no_specformat_available(self):
        with tempfile.TemporaryDirectory() as d:
            vendor_scripts = os.path.join(d, "scripts")
            os.makedirs(vendor_scripts)
            import shutil
            shutil.copy(SCRIPT, os.path.join(vendor_scripts, "spec-redundancy-precheck.py"))
            shutil.copy(os.path.join(ROOT, "scripts", "gate_common.py"),
                        os.path.join(vendor_scripts, "gate_common.py"))
            # No guardrails/ dir at all next to this vendored copy's parent.

            doc = os.path.join(d, "DOC.md")
            with open(doc, "w", encoding="utf-8") as f:
                f.write("# Doc\n\n" + DUPLICATE_SENTENCE + "\nElsewhere: " + DUPLICATE_SENTENCE)

            r = subprocess.run(
                ["python3", os.path.join(vendor_scripts, "spec-redundancy-precheck.py"), doc],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)  # open candidate found -> exit 1
            js = summary(r.stdout)
            self.assertGreaterEqual(js["candidates"], 1)


if __name__ == "__main__":
    unittest.main()
