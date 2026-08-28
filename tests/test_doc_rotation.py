"""Document rotation — the pack's append-only working docs are split and rotated, and nothing
rotated is lost (SPEC INV-209, ROADMAP rows 390 + 392, the growth/grooming family).

ROADMAP.md, JOURNAL.md, PRODUCT_SPEC.md, and TEST_MATRIX.md grow with every landing until a guard's
scan and a grep run slow (the owner's word, 2026-07-17 ~18:25). So a fully-closed portion of a growable
document rotates out of the live file into a dated archive with a manifest line (base rule 10), the live
file keeping only live material and the archive keeping everything, grepable, so a rotated row stays
findable by its number.

One machine holds the invariant: guardrails/check-doc-rotation.py (gate t), the net. It reds a
rotation that DROPS content (a manifested row found in neither the live file nor its archive), a
rotation with NO manifest (a rotated-* archive no manifest points to), a row findable both live and
archived, a row resting in an archive whose status is not terminal, and a terminal row in a
referenced archive that no manifest line names.

The mechanism that used to stand beside it, scripts/rotate-doc.py, retired to the attic on
2026-08-28: it understood one document's table shape and that document is retired, so it could no
longer be run on anything in the live tree. Rows move by hand now, and the gate is what proves the
hand lost nothing. Its own tests retired with it — they exercised a tool that is gone.

This file is red-first: run it against the pre-delta tree and the gate is absent, the
spec/index/architecture/matrix carry no INV-209, and the push chain is unwired.
"""
import os
import re
import subprocess
import sys
import unittest

# The suite's one reading node: for the spec it returns the core and every part the map
# names, and for any other file the file itself. A local reader would have shadowed it.
from conftest import read

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-doc-rotation.py")


def run_gate(base, docs, extra=None):
    """Run the gate over a fixture base dir; return (exit_code, combined_output)."""
    cmd = [sys.executable, GATE, "--base", base]
    for d in docs:
        cmd += ["--doc", d]
    cmd += ["--archive-glob", "rotated-*.md"]
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ---- fixtures ---------------------------------------------------------------

MANIFEST = (
    "<!-- rotated-manifest -->\n"
    "Rotated closed rows (base rule 10 — nothing lost; the archive keeps everything):\n"
    "- rows 14, 27 → rotated-ROADMAP-2026-07-18.md\n"
    "<!-- /rotated-manifest -->\n"
)


def _live_doc(manifest):
    return (
        "# live-spec Roadmap (dated version: 2026-07-18)\n\n"
        "The wish queue.\n\n"
        + manifest +
        "\n| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
        "|---|---|---|---|---|\n"
        "| 42 | a live open wish | surface | queued 2026-07-18 | Done when: x |\n"
    )


def _archive(rows):
    head = "> ARCHIVED 2026-07-18 by scripts/rotate-doc.py from ROADMAP.md — nothing lost (base rule 10).\n\n"
    body = "".join(
        "| %d | closed wish %d | small | **landed 2026-07-05** | Done when: met |\n" % (n, n)
        for n in rows
    )
    return head + "| # | Wish | Class | Status | Decision |\n|---|---|---|---|---|\n" + body


def _write(base, name, text):
    with open(os.path.join(base, name), "w", encoding="utf-8") as f:
        f.write(text)


class TestRotationGate(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-fixture-")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_gate_reds_a_rotation_that_loses_a_row(self):
        # the manifest claims rows 14 and 27 rotated, but the archive holds only 14 — row 27 is
        # present in neither the live file nor the archive: the nothing-lost violation.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "a rotation that drops row 27 must red")
        self.assertIn("27", out)

    def test_gate_reds_a_rotation_with_no_manifest(self):
        # a rotated-* archive exists but no manifest line in any live doc points to it: the
        # base-rule-10 violation (a superseded portion moved with no manifest line).
        _write(self.tmp, "ROADMAP.md", _live_doc(""))  # no manifest block at all
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "an orphan archive with no manifest line must red")
        self.assertIn("rotated-ROADMAP-2026-07-18.md", out)

    def test_gate_reds_a_row_that_is_both_live_and_rotated(self):
        # row 14 is declared rotated yet still present as a live table row — ambiguous, findable
        # twice, the canonical copy unclear.
        live = _live_doc(MANIFEST) + "| 14 | still here | small | **landed 2026-07-05** | Done: met |\n"
        _write(self.tmp, "ROADMAP.md", live)
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "a row both live and rotated must red")
        self.assertIn("14", out)

    def test_gate_passes_a_clean_rotation(self):
        # the live file shrank, the archive holds every rotated row, the manifest names them, and no
        # rotated row is still live: a clean rotation passes.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertEqual(code, 0, "a clean rotation must pass:\n" + out)

    def test_rotated_row_is_findable_by_number_in_the_archive(self):
        # findability: a reader who greps the archive for the row's own `| n |` line finds it.
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        arch = open(os.path.join(self.tmp, "rotated-ROADMAP-2026-07-18.md"), encoding="utf-8").read()
        self.assertRegex(arch, r"(?m)^\| 27 \|", "a rotated row must keep its `| n |` line so a grep finds it")

    def test_gate_passes_the_real_tree(self):
        # the repo's own ROADMAP.md after the first rotation must be clean under the gate.
        p = subprocess.run([sys.executable, GATE], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 0, "the real tree fails the rotation gate:\n" + p.stdout + p.stderr)


class TestArchiveRowUnclaimed(unittest.TestCase):
    """Arm (e): a terminal row inside a referenced archive that no manifest line names.

    The gate held one direction only — every row the manifest NAMES is present in its archive — and
    never the mirror, that every row PRESENT in an archive is named. A row can therefore be moved out
    of the live list and left out of the manifest line, and nothing says so: it is not live, it is not
    manifested, and the archive it rests in is referenced, so the orphan-archive arm stays quiet too.
    The findability promise the whole gate exists to keep is per row, so this is the same nothing-lost
    violation seen from the archive side.

    RED-PROOF, from the tree itself: docs/queue-archive/rotated-ROADMAP-2026-08.md carried row 558
    (`declined 2026-08-09`) while the manifest line for that archive named seventeen other rows and
    never 558, and gate t passed the tree. The fixtures below are the permanent minimal shape of that
    red.
    """

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-unclaimed-")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_a_terminal_row_no_manifest_line_names_reds(self):
        # the manifest names 14 and 27; the archive also holds 33, closed and named nowhere.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        archive = _archive([14, 27]) + \
            "| 33 | a closed wish nobody wrote down | small | **declined 2026-08-09** | Done: n/a |\n"
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", archive)
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "an archived row no manifest line names must red:\n" + out)
        self.assertIn("33", out)
        self.assertIn("unclaimed", out)

    def test_an_archive_whose_every_terminal_row_is_named_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertEqual(code, 0, "an archive whose rows are all named must pass:\n" + out)

    def test_an_unnamed_row_that_is_not_terminal_reds_as_the_non_terminal_violation(self):
        # boundary: a row still open in an archive belongs to arm (d) and is named as such. Arm (e)
        # must not double-report it, since a row that never closed has no business being named on a
        # manifest line in the first place.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        archive = _archive([14, 27]) + \
            "| 33 | a wish still open | small | queued 2026-08-09 | Done: x |\n"
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", archive)
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "a non-terminal archived row must red:\n" + out)
        self.assertIn("live queue body", out)
        self.assertNotIn("unclaimed", out)

    def test_rows_in_an_archive_no_manifest_points_at_red_as_no_manifest_only(self):
        # boundary: an archive nothing points at is arm (b)'s whole-file violation. Naming each of
        # its rows unclaimed on top of that would bury the one finding that matters under a row list.
        _write(self.tmp, "ROADMAP.md", _live_doc(""))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "an orphan archive must red")
        self.assertIn("no manifest", out)
        self.assertNotIn("unclaimed", out)


MONTH_MANIFEST = (
    "<!-- rotated-manifest -->\n"
    "Rotated closed rows (base rule 10 — nothing lost; the archive keeps everything):\n"
    "- rows 480 → docs/queue-archive/rotated-ROADMAP-2026-07.md\n"
    "<!-- /rotated-manifest -->\n"
)
MONTH_MANIFEST_TWO = MONTH_MANIFEST.replace("- rows 480 →", "- rows 480, 483 →")


def _month_archive(rows):
    head = ("# Rotated ROADMAP rows — 2026-07\n\n"
            "> ARCHIVED 2026-07 by scripts/rotate-doc.py from ROADMAP.md at the closing commit — nothing lost.\n\n")
    body = "".join(
        "| %d | closed wish %d | small | *landed 2026-07-23* | Done: met |\n" % (n, n) for n in rows)
    return head + "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n|---|---|---|---|---|\n" + body


class TestMonthlyClosingCommitGate(unittest.TestCase):
    """Piece 2 (SPEC INV-276): the doc-rotation gate accepts the monthly-growing manifest shape — one
    line per month archive whose row-set grows across commits, a monthly-named archive as legal as the
    day-named legacy ones — and the three reds stay live on it."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-month-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, docs=("ROADMAP.md",)):
        return run_gate(self.tmp, list(docs),
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    def test_a_row_moved_into_a_month_file_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertEqual(code, 0, "a clean monthly close must pass:\n" + out)

    def test_a_second_row_appended_with_the_line_grown_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST_TWO))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480, 483]))
        code, out = self._run()
        self.assertEqual(code, 0, "a grown month manifest line must pass:\n" + out)

    def test_a_moved_row_missing_from_the_archive_reds(self):
        # RED-PROOF: manifest names 480 and 483 but the month archive holds only 480.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST_TWO))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "a row lost from the month archive must red")
        self.assertIn("483", out)

    def test_a_row_in_both_body_and_archive_reds(self):
        # RED-PROOF: row 480 is declared moved yet still stands as a live body row — ambiguous.
        live = _live_doc(MONTH_MANIFEST) + "| 480 | still here | small | *queued 2026-07-23* | Done: x |\n"
        _write(self.tmp, "ROADMAP.md", live)
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "a row both live and archived must red")
        self.assertIn("480", out)

    def test_an_orphan_month_archive_reds(self):
        # RED-PROOF: a month archive with no manifest line pointing to it (base-rule-10 violation).
        _write(self.tmp, "ROADMAP.md", _live_doc(""))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "an orphan month archive must red")
        self.assertIn("rotated-ROADMAP-2026-07.md", out)


class TestNonTerminalArchiveRow(unittest.TestCase):
    """Arm (d) (docs/prover/2026-07-27-push-gate-addendum.md finding A4): a row inside an archive
    whose Status cell carries none of the terminal words (landed / decided / declined / superseded) reds — a
    row like this is reachable from no live answer, no cap count and no gate. Red-first proof: HEAD's
    docs/queue-archive/rotated-ROADMAP-2026-07.md row 482 carried `*queued* 2026-07-23` with no
    terminal word; this fixture is the permanent, minimal shape of that same red."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-nonterminal-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        return run_gate(self.tmp, ["ROADMAP.md"],
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    def test_a_queued_row_in_the_archive_reds(self):
        # RED-PROOF: the row-482 shape — a bug row moved to the archive still reading *queued*, no
        # terminal word standing anywhere in its Status cell.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (
            "# Rotated ROADMAP rows — 2026-07\n\n"
            "> ARCHIVED 2026-07 — a row's terminal exit is certified by the landed, declined, or "
            "superseded word standing somewhere in the cell.\n\n"
            "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n|---|---|---|---|---|\n"
            "| 480 | mid-turn chat lines reach the human ungated | bug | *queued* 2026-07-23 | Done "
            "when: x |\n"
        )
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertNotEqual(code, 0, "a non-terminal row sitting in the archive must red:\n" + out)
        self.assertIn("480", out)
        self.assertIn("live queue body", out)

    def test_terminal_word_bolded_and_dated_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace(
            "*landed 2026-07-23*", "**LANDED 2026-07-07 ~11:47**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a bolded, dated terminal word must pass:\n" + out)

    def test_terminal_word_declined_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "declined 2026-07-23")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a declined row must pass:\n" + out)

    def test_terminal_word_decided_passes(self):
        # A row that exists to settle a question exits as decided, the fourth word of the vocabulary
        # docs/roadmap-format.md states in one home; the pre-format archives carry it on their
        # decision rows.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "**decided 2026-07-05**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a decided row must pass:\n" + out)

    def test_terminal_word_superseded_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "superseded 2026-07-23")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a superseded row must pass:\n" + out)

    def test_stale_leading_narration_word_still_passes_when_terminal_word_stands_later(self):
        # the archive preamble's own caveat: the leading word can be a stale narration opener (queued
        # or in-work) on a row that later landed, so the check reads the whole cell, never the leading
        # word alone.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace(
            "*landed 2026-07-23*",
            "*queued* 2026-07-20, then **landed 2026-07-23**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a terminal word standing anywhere in the cell must pass:\n" + out)


def test_the_retired_mechanism_is_gone_and_its_line_is_in_the_attic():
    """scripts/rotate-doc.py retired 2026-08-28, and nothing silently deleted (base rule 10).

    The tool read one document's table shape and refused every other document by name. That
    document left the tree, so every invocation it could still be given either names a file that
    is not there or is refused as out of scope — it cannot be run on the live tree at all. Its
    behaviour tests retired with it: a test of a tool that is gone proves nothing about the tree.
    What it promised — that a move writes the archive and the manifest line together — is now
    promised by the gate instead, which reds either half missing on every push whatever hand made
    the move.
    """
    assert not os.path.exists(os.path.join(ROOT, "scripts", "rotate-doc.py")), \
        "the retired mechanism is back in scripts/ with no tests covering it"
    assert os.path.exists(os.path.join(ROOT, "attic", "rotate-doc.py")), \
        "the retired mechanism is not in the attic — base rule 10 deletes nothing silently"
    assert "attic/rotate-doc.py" in read("attic/MANIFEST.md"), \
        "the attic manifest carries no line for the retired mechanism"


# --- wired into the push chain, both nets ---

def test_gate_wired_into_pre_push():
    assert "check-doc-rotation.py" in read("guardrails/pre-push"), \
        "pre-push does not wire the rotation gate (gate t)"


def test_gate_mirrored_in_ci():
    assert "check-doc-rotation.py" in read(".github/workflows/gates.yml"), \
        "the CI mirror does not run the rotation gate"


# --- traceability across the four documents ---

def test_spec_states_the_law():
    # PRODUCT_SPEC.md states this law in plain behaviour, not by script filename — the literal
    # rotate-doc.py / check-doc-rotation.py names moved to ARCHITECTURE.md's ownership row (see
    # test_architecture_owns_the_invariant), the rewrite's document-boundary convention (spec =
    # behaviour, architecture = implementation file). Re-pinned to the plain-language equivalents.
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-209]" in spec
    assert "move the closed rows into a dated archive" in spec
    assert "nothing-lost violation" in spec


def test_formal_index_row():
    assert "| INV-209 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-209" in arch
    assert "check-doc-rotation.py" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "M-390" in matrix
    assert "INV-209" in matrix


if __name__ == "__main__":
    unittest.main()


class TestStatusColumnReadFromHeader(unittest.TestCase):
    """The Status cell is located by the archive table's own header (the record's S8), so an archive
    whose columns sit in another order is still read at the right cell."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-header-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        return run_gate(self.tmp, ["ROADMAP.md"],
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    ARCHIVE_HEAD = ("# Rotated ROADMAP rows — 2026-07\n\n> ARCHIVED 2026-07 — terminal words: landed, "
                    "decided, declined, superseded.\n\n")

    def test_a_reordered_header_still_finds_the_status_cell(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (self.ARCHIVE_HEAD +
                   "| # | Status | Wish | Class | Decision |\n|---|---|---|---|---|\n"
                   "| 480 | *queued* 2026-07-23 | a wish | bug | Done when: x |\n")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertNotEqual(code, 0, "the non-terminal row must red at its real column:\n" + out)
        self.assertIn("480", out)

    def test_a_reordered_header_passes_a_terminal_row(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (self.ARCHIVE_HEAD +
                   "| # | Status | Wish | Class | Decision |\n|---|---|---|---|---|\n"
                   "| 480 | **landed 2026-07-23** | a wish | bug | Done when: x |\n")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a terminal row at a moved column must pass:\n" + out)
