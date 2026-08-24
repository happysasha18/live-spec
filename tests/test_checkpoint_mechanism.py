"""Deterministic parsing/validation for `.live-spec/checkpoints/*.md` (scripts/checkpoint.py).

Checkpoints used to be pure convention: nothing on disk validated Status/DONE/IN
PROGRESS/NEXT, they were just habits an agent followed when it remembered to. This suite
locks the mechanical replacement: scripts/checkpoint.py's read_checkpoint (structural
parse), validate_checkpoint (semantic rules), new_checkpoint (fresh-file writer),
update_checkpoint (in-place section rewrite of an existing open checkpoint — the fix for
the adversarial-review finding that new_checkpoint was the only writer and silently
overwrote existing content back to a blank template), close_checkpoint (the mechanical
enforcement of "a landing that ships a checkpoint's items flips that checkpoint to its
closed state"), and the CLI wrapper around all five.

Every fixture file here is written under a tempfile.TemporaryDirectory() — never into this
worktree's real (gitignored, ephemeral) .live-spec/checkpoints/.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import checkpoint  # noqa: E402

CHECKPOINT_PY = os.path.join(SCRIPTS, "checkpoint.py")


# ---------------------------------------------------------------------------
# Fixture bodies
# ---------------------------------------------------------------------------

VALID_OPEN_NON_DIRECTOR = """\
# A worker's plain checkpoint
Status: open
Owner: some-worker

## DONE

Wrote the parser.

## IN PROGRESS

Wiring the CLI.

## NEXT

Add tests.
"""

VALID_CLOSED = """\
# A finished checkpoint
Status: closed
Owner: some-worker

## DONE

Shipped the feature end to end.

## IN PROGRESS

(nothing)

## NEXT

none
"""

CLOSED_WITH_OPEN_IN_PROGRESS = """\
# A wrongly-closed checkpoint
Status: closed
Owner: some-worker

## DONE

Shipped most of it.

## IN PROGRESS

Still wiring the retry path.

## NEXT

-
"""

MISSING_STATUS = """\
# No status here
Owner: some-worker

## DONE

Something.

## IN PROGRESS

(nothing)

## NEXT

(nothing)
"""

BAD_STATUS_VALUE = """\
# Weird status value
Status: in-progress
Owner: some-worker

## DONE

(nothing)

## IN PROGRESS

(nothing)

## NEXT

(nothing)
"""

DUPLICATE_STATUS_KEY = """\
# Duplicate Status line
Status: open
Owner: some-worker
Status: closed

## DONE

(nothing)

## IN PROGRESS

(nothing)

## NEXT

(nothing)
"""

DUPLICATE_OWNER_KEY = """\
# Duplicate Owner line
Status: open
Owner: some-worker
Owner: someone-else

## DONE

(nothing)

## IN PROGRESS

(nothing)

## NEXT

(nothing)
"""

MISSING_NEXT_SECTION = """\
# Missing the NEXT section
Status: open
Owner: some-worker

## DONE

Did some things.

## IN PROGRESS

Doing more things.
"""

DIRECTOR_MISSING_DECISION_SHEET = """\
# Director's checkpoint
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

(nothing yet)

## NEXT

(nothing yet)
"""


def _worker_variant_of_director_fixture():
    """Same content as DIRECTOR_MISSING_DECISION_SHEET, just a non-director Owner:."""
    return DIRECTOR_MISSING_DECISION_SHEET.replace("Owner: director", "Owner: some-worker")


# Regression fixture for the adversarial-review finding on commit 6ce6fca0: an unrecognized
# `## ` heading used to be silently accepted by read_checkpoint and completely unchecked by
# validate_checkpoint, so real unfinished-work text could hide inside it and close_checkpoint
# would succeed anyway. ALLOWED_SECTIONS closes that hole — this header is not in the set, so
# read_checkpoint itself must now raise ValueError before validate/close ever see the file.
UNRECOGNIZED_SECTION_HIDES_OPEN_WORK = """\
# A checkpoint smuggling open work
Status: open
Owner: some-worker

## DONE

Shipped the easy part.

## IN PROGRESS

(nothing)

## some ad hoc subheading

Still wiring the retry path — do not close yet!

## NEXT

(nothing)
"""

# WATCHED stays on the allowlist: a pre-existing "workshop noise" ledger convention already
# used by worker checkpoints in this project. Ignored by validate_checkpoint, same as before —
# it just now has to be spelled exactly "WATCHED" rather than being any-old-unrecognized-header.
VALID_WITH_WATCHED_SECTION = """\
# A checkpoint with a workshop-noise ledger
Status: open
Owner: some-worker

## DONE

Wrote the parser.

## IN PROGRESS

(nothing)

## NEXT

(nothing)

## WATCHED

2026-08-24: noticed the CLI --all glob needs a stable sort; not blocking, just logging it.
"""


class TestReadCheckpoint(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)

    def _write(self, name, content):
        p = self.tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    # 1. valid open, non-director checkpoint
    def test_valid_open_non_director_parses_and_validates_clean(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        data = checkpoint.read_checkpoint(p)
        self.assertEqual(data["title"], "A worker's plain checkpoint")
        self.assertEqual(data["status"], "open")
        self.assertEqual(data["owner"], "some-worker")
        self.assertFalse(data["is_director_owned"])
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 2. valid closed checkpoint (placeholders in IN PROGRESS / NEXT)
    def test_valid_closed_checkpoint_validates_clean(self):
        p = self._write("closed.md", VALID_CLOSED)
        data = checkpoint.read_checkpoint(p)
        self.assertEqual(data["status"], "closed")
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 3. closed checkpoint with real content in IN PROGRESS fails
    def test_closed_checkpoint_with_open_in_progress_fails(self):
        p = self._write("bad_closed.md", CLOSED_WITH_OPEN_IN_PROGRESS)
        issues = checkpoint.validate_checkpoint(p)
        self.assertTrue(issues, "expected at least one issue")
        joined = " ".join(issues)
        self.assertIn("IN PROGRESS", joined)
        self.assertIn("closed", joined)

    # 4. missing Status: raises ValueError
    def test_missing_status_raises(self):
        p = self._write("missing_status.md", MISSING_STATUS)
        with self.assertRaises(ValueError):
            checkpoint.read_checkpoint(p)

    # 5. Status: value not open/closed raises ValueError
    def test_bad_status_value_raises(self):
        p = self._write("bad_status.md", BAD_STATUS_VALUE)
        with self.assertRaises(ValueError):
            checkpoint.read_checkpoint(p)

    # 6. missing ## NEXT parses fine, fails validate_checkpoint naming ## NEXT
    def test_missing_next_section_parses_but_fails_validation(self):
        p = self._write("missing_next.md", MISSING_NEXT_SECTION)
        data = checkpoint.read_checkpoint(p)  # must not raise
        self.assertNotIn("NEXT", data["sections"])
        issues = checkpoint.validate_checkpoint(p)
        self.assertTrue(any("## NEXT" in issue for issue in issues), issues)

    # 7. director-owned missing DECISION SHEET fails; same content, non-director owner is fine
    def test_decision_sheet_required_only_for_director_owner(self):
        director_path = self._write("director.md", DIRECTOR_MISSING_DECISION_SHEET)
        worker_path = self._write("worker.md", _worker_variant_of_director_fixture())

        director_data = checkpoint.read_checkpoint(director_path)
        self.assertTrue(director_data["is_director_owned"])
        director_issues = checkpoint.validate_checkpoint(director_path)
        self.assertTrue(
            any("DECISION SHEET" in issue for issue in director_issues), director_issues
        )

        worker_data = checkpoint.read_checkpoint(worker_path)
        self.assertFalse(worker_data["is_director_owned"])
        self.assertEqual(checkpoint.validate_checkpoint(worker_path), [])

    # Regression (adversarial review of 6ce6fca0): an unrecognized ## header must not be able
    # to hide real unfinished-work text from validation. read_checkpoint rejects it outright,
    # at parse time — before validate_checkpoint or close_checkpoint ever get a look at the file.
    def test_unrecognized_section_header_raises_at_parse_time(self):
        p = self._write("smuggled.md", UNRECOGNIZED_SECTION_HIDES_OPEN_WORK)
        with self.assertRaises(ValueError) as ctx:
            checkpoint.read_checkpoint(p)
        self.assertIn("some ad hoc subheading", str(ctx.exception))

    # WATCHED is the one non-required, non-director header that stays allowed — a pre-existing
    # "workshop noise" ledger convention. It parses fine and doesn't block validity.
    def test_watched_section_remains_allowed(self):
        p = self._write("watched.md", VALID_WITH_WATCHED_SECTION)
        data = checkpoint.read_checkpoint(p)  # must not raise
        self.assertIn("WATCHED", data["sections"])
        self.assertIn("workshop-noise", data["title"])
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 31. A duplicate "Status:" line in the metadata block (written directly, bypassing
    # new_checkpoint, since this is read_checkpoint's own defense-in-depth) must raise,
    # naming the duplicate key — not silently let the second line override the first.
    def test_duplicate_status_key_raises(self):
        p = self._write("dup_status.md", DUPLICATE_STATUS_KEY)
        with self.assertRaises(ValueError) as ctx:
            checkpoint.read_checkpoint(p)
        self.assertIn("Status", str(ctx.exception))

    # 32. Same, for a duplicate "Owner:" line.
    def test_duplicate_owner_key_raises(self):
        p = self._write("dup_owner.md", DUPLICATE_OWNER_KEY)
        with self.assertRaises(ValueError) as ctx:
            checkpoint.read_checkpoint(p)
        self.assertIn("Owner", str(ctx.exception))


class TestNewCheckpoint(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)

    # 8. new_checkpoint, non-director, no decision_sheet: round-trips clean
    def test_new_checkpoint_non_director_round_trips(self):
        p = self.tmp_path / "sub" / "new.md"
        checkpoint.new_checkpoint(p, title="A fresh checkpoint", owner="some-worker")
        self.assertTrue(p.is_file())
        data = checkpoint.read_checkpoint(p)
        self.assertEqual(data["title"], "A fresh checkpoint")
        self.assertEqual(data["status"], "open")
        self.assertEqual(data["owner"], "some-worker")
        self.assertFalse(data["is_director_owned"])
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 9. director owner requires decision_sheet
    def test_new_checkpoint_director_requires_decision_sheet(self):
        p = self.tmp_path / "director.md"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(p, title="Director's checkpoint", owner="director")
        self.assertFalse(p.exists())

        checkpoint.new_checkpoint(
            p,
            title="Director's checkpoint",
            owner="director",
            decision_sheet="We decided to ship plan B.",
        )
        self.assertTrue(p.is_file())
        self.assertEqual(checkpoint.validate_checkpoint(p), [])
        data = checkpoint.read_checkpoint(p)
        self.assertIn("We decided to ship plan B.", data["sections"]["DECISION SHEET"])

    def test_new_checkpoint_non_director_rejects_decision_sheet(self):
        p = self.tmp_path / "worker_with_sheet.md"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(
                p, title="Worker", owner="some-worker", decision_sheet="not allowed"
            )

    # 20. decision_sheet containing a "## "-prefixed line (anywhere, not just as the first
    # line) raises ValueError and the file is not created at all — the write must never
    # happen, since a written copy would be permanently unreadable by every other function.
    def test_new_checkpoint_rejects_embedded_header_in_decision_sheet(self):
        p = self.tmp_path / "director_bricked.md"
        bad_sheet = "Goal: ship the fix.\n## Blocked on\n- waiting on the retry-path answer"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(
                p, title="Director's checkpoint", owner="director", decision_sheet=bad_sheet
            )
        self.assertFalse(p.exists())

    # 27. title containing "\n" raises ValueError, file not created.
    def test_new_checkpoint_rejects_multiline_title(self):
        p = self.tmp_path / "bad_title.md"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(
                p, title="Bad\ntitle with embedded newline", owner="worker"
            )
        self.assertFalse(p.exists())

    # 28. owner containing "\n" raises ValueError, file not created.
    def test_new_checkpoint_rejects_multiline_owner(self):
        p = self.tmp_path / "bad_owner.md"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(
                p, title="T", owner="worker\nwith embedded newline"
            )
        self.assertFalse(p.exists())

    # 29. The reviewer's exact gap-2 regression: an embedded newline in `owner` that injects
    # a bogus second "Status:" line must raise at the new_checkpoint call itself, rather than
    # silently succeeding and later reading back with a corrupted status.
    def test_new_checkpoint_rejects_status_injection_via_owner(self):
        p = self.tmp_path / "t3.md"
        with self.assertRaises(ValueError):
            checkpoint.new_checkpoint(p, title="T3", owner="worker\nStatus: closed")
        self.assertFalse(p.exists())

    # 30. Negative control: an ordinary single-line title/owner with unicode and punctuation
    # (no embedded line break) still works fine.
    def test_new_checkpoint_accepts_ordinary_unicode_title_and_owner(self):
        p = self.tmp_path / "unicode.md"
        checkpoint.new_checkpoint(
            p, title="Ship the fix — café’s retry path (v2)", owner="worker-☂️-42"
        )
        self.assertTrue(p.is_file())
        data = checkpoint.read_checkpoint(p)
        self.assertEqual(data["title"], "Ship the fix — café’s retry path (v2)")
        self.assertEqual(data["owner"], "worker-☂️-42")
        self.assertEqual(checkpoint.validate_checkpoint(p), [])


class TestCloseCheckpoint(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)

    def _write(self, name, content):
        p = self.tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    # 10. close_checkpoint with non-empty NEXT raises, and does not modify the file
    def test_close_with_open_next_raises_and_does_not_modify(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        before = p.read_bytes()
        with self.assertRaises(ValueError):
            checkpoint.close_checkpoint(p)
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 11. close_checkpoint success path, then double-close raises
    def test_close_succeeds_then_double_close_raises(self):
        p = self._write("closeable.md", VALID_CLOSED.replace("Status: closed", "Status: open"))
        data_before = checkpoint.read_checkpoint(p)
        self.assertEqual(data_before["status"], "open")

        checkpoint.close_checkpoint(p)

        data_after = checkpoint.read_checkpoint(p)
        self.assertEqual(data_after["status"], "closed")
        # everything else preserved
        self.assertEqual(data_after["title"], data_before["title"])
        self.assertEqual(data_after["owner"], data_before["owner"])
        self.assertEqual(data_after["sections"], data_before["sections"])

        with self.assertRaises(ValueError):
            checkpoint.close_checkpoint(p)


class TestUpdateCheckpoint(unittest.TestCase):
    """update_checkpoint: the regression lock for the adversarial-review finding that
    new_checkpoint was the ONLY writer, and a second call against a path already holding
    real content silently overwrote it back to a blank template — no error, no exists-check,
    exit 0. update_checkpoint must be able to rewrite one or more sections of an existing
    open checkpoint in place without ever reproducing that silent-clobber behaviour.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)

    def _write(self, name, content):
        p = self.tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    # 13. update NEXT only: DONE/IN PROGRESS bodies byte-identical before/after, NEXT changed,
    # result validates clean.
    def test_update_next_only_leaves_other_sections_untouched(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        before = checkpoint.read_checkpoint(p)

        checkpoint.update_checkpoint(p, next="Ship the retry logic next.")

        after = checkpoint.read_checkpoint(p)
        self.assertEqual(after["sections"]["DONE"], before["sections"]["DONE"])
        self.assertEqual(after["sections"]["IN PROGRESS"], before["sections"]["IN PROGRESS"])
        self.assertEqual(after["sections"]["NEXT"], "Ship the retry logic next.")
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 14. update DECISION SHEET on a director-owned checkpoint: succeeds, new text lands,
    # everything else (including the DONE/IN PROGRESS/NEXT placeholders) unchanged.
    def test_update_decision_sheet_on_director_owned(self):
        p = self.tmp_path / "director.md"
        checkpoint.new_checkpoint(
            p, title="Director's checkpoint", owner="director",
            decision_sheet="Original decision.",
        )
        before = checkpoint.read_checkpoint(p)

        checkpoint.update_checkpoint(p, decision_sheet="Revised decision after correction.")

        after = checkpoint.read_checkpoint(p)
        self.assertEqual(
            after["sections"]["DECISION SHEET"], "Revised decision after correction."
        )
        self.assertEqual(after["sections"]["DONE"], before["sections"]["DONE"])
        self.assertEqual(after["sections"]["IN PROGRESS"], before["sections"]["IN PROGRESS"])
        self.assertEqual(after["sections"]["NEXT"], before["sections"]["NEXT"])
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 15. decision_sheet on a NON-director-owned checkpoint raises ValueError.
    def test_update_decision_sheet_on_non_director_raises(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, decision_sheet="not allowed here")

    # 16. all four params None (the defaults) raises ValueError.
    def test_update_with_nothing_to_update_raises(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p)

    # 17. update on a closed checkpoint raises, and does not modify the file.
    def test_update_on_closed_checkpoint_raises_and_does_not_modify(self):
        p = self._write("closed.md", VALID_CLOSED)
        before = p.read_bytes()
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, next="trying to reopen via the back door")
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 18. The exact scenario the reviewer found: a checkpoint with real DONE content must
    # keep that content after an unrelated section is updated — update must never look like
    # new_checkpoint's silent full-file overwrite.
    def test_update_never_clobbers_unrelated_completed_work(self):
        p = self.tmp_path / "worker.md"
        checkpoint.new_checkpoint(p, title="Worker's checkpoint", owner="some-worker")
        checkpoint.update_checkpoint(p, done="Finished the hard, easy-to-lose part.")
        seeded = checkpoint.read_checkpoint(p)
        self.assertEqual(seeded["sections"]["DONE"], "Finished the hard, easy-to-lose part.")

        checkpoint.update_checkpoint(p, next="revised next")

        after = checkpoint.read_checkpoint(p)
        self.assertEqual(
            after["sections"]["DONE"], "Finished the hard, easy-to-lose part."
        )
        self.assertEqual(after["sections"]["NEXT"], "revised next")
        self.assertEqual(checkpoint.validate_checkpoint(p), [])

    # 21. `next` containing a "## "-prefixed line raises ValueError, file left byte-identical.
    def test_update_rejects_embedded_header_in_next(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        before = p.read_bytes()
        bad_next = "Still to do:\n## Blocked on\n- waiting on the retry-path answer"
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, next=bad_next)
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 22. same, for `done`.
    def test_update_rejects_embedded_header_in_done(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        before = p.read_bytes()
        bad_done = "Finished most of it.\n## Caveat\n- one edge case left"
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, done=bad_done)
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 23. same, for `in_progress`.
    def test_update_rejects_embedded_header_in_in_progress(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        before = p.read_bytes()
        bad_in_progress = "Wiring retries.\n## Note\n- flaky under load"
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, in_progress=bad_in_progress)
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 24. same, for `decision_sheet` on a director-owned checkpoint.
    def test_update_rejects_embedded_header_in_decision_sheet(self):
        p = self.tmp_path / "director.md"
        checkpoint.new_checkpoint(
            p, title="Director's checkpoint", owner="director",
            decision_sheet="Original decision.",
        )
        before = p.read_bytes()
        bad_sheet = "Revised: ship plan C.\n## Risk\n- untested rollback"
        with self.assertRaises(ValueError):
            checkpoint.update_checkpoint(p, decision_sheet=bad_sheet)
        after = p.read_bytes()
        self.assertEqual(before, after)

    # 25. Negative control: a body value that merely CONTAINS "## " mid-line (not at the
    # start of a line) must NOT be rejected — only a line that itself starts with "## " is
    # the problem, matching read_checkpoint's own per-line startswith("## ") test exactly.
    def test_update_accepts_mid_line_hash_hash_substring(self):
        p = self._write("open.md", VALID_OPEN_NON_DIRECTOR)
        next_value = "see the ## DONE section above for context"
        checkpoint.update_checkpoint(p, next=next_value)
        data = checkpoint.read_checkpoint(p)
        self.assertEqual(data["sections"]["NEXT"], next_value)
        self.assertEqual(checkpoint.validate_checkpoint(p), [])


class TestCli(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = Path(self._tmpdir.name)

    def _write(self, name, content):
        p = self.tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    # 12. CLI smoke test: good fixture -> exit 0; bad fixture -> non-zero + ISSUE/ERROR
    def test_cli_validate_good_and_bad(self):
        good = self._write("good.md", VALID_OPEN_NON_DIRECTOR)
        bad = self._write("bad.md", CLOSED_WITH_OPEN_IN_PROGRESS)

        good_result = subprocess.run(
            [sys.executable, CHECKPOINT_PY, "validate", str(good)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(good_result.returncode, 0, good_result.stdout + good_result.stderr)
        self.assertIn("OK:", good_result.stdout)

        bad_result = subprocess.run(
            [sys.executable, CHECKPOINT_PY, "validate", str(bad)],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(bad_result.returncode, 0)
        self.assertTrue(
            "ISSUE:" in bad_result.stdout or "ERROR:" in bad_result.stdout,
            bad_result.stdout,
        )

    def test_cli_new_and_close(self):
        target = self.tmp_path / "cli_new.md"
        new_result = subprocess.run(
            [
                sys.executable,
                CHECKPOINT_PY,
                "new",
                str(target),
                "--title",
                "CLI-made checkpoint",
                "--owner",
                "some-worker",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(new_result.returncode, 0, new_result.stdout + new_result.stderr)
        self.assertTrue(target.is_file())
        self.assertEqual(checkpoint.validate_checkpoint(target), [])

        # its DONE/IN PROGRESS/NEXT are all placeholders, so it's immediately closeable
        close_result = subprocess.run(
            [sys.executable, CHECKPOINT_PY, "close", str(target)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(close_result.returncode, 0, close_result.stdout + close_result.stderr)
        self.assertEqual(checkpoint.read_checkpoint(target)["status"], "closed")

    # 19. CLI smoke test for `update`: write a fixture, update a couple of sections via
    # subprocess, assert exit 0 and "updated:" in stdout, then confirm the change landed.
    def test_cli_update(self):
        target = self._write("cli_update.md", VALID_OPEN_NON_DIRECTOR)

        update_result = subprocess.run(
            [
                sys.executable,
                CHECKPOINT_PY,
                "update",
                str(target),
                "--next",
                "Ship the retry logic next.",
                "--in-progress",
                "Still wiring the retry path.",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            update_result.returncode, 0, update_result.stdout + update_result.stderr
        )
        self.assertIn("updated:", update_result.stdout)

        data = checkpoint.read_checkpoint(target)
        self.assertEqual(data["sections"]["NEXT"], "Ship the retry logic next.")
        self.assertEqual(data["sections"]["IN PROGRESS"], "Still wiring the retry path.")
        # DONE, untouched by the call, must survive
        self.assertEqual(data["sections"]["DONE"], "Wrote the parser.")
        self.assertEqual(checkpoint.validate_checkpoint(target), [])

    # 26. Reviewer's exact repro, end to end via the CLI: `new` a checkpoint, then attempt
    # an `update` whose --next carries an embedded "## " line. The CLI call must fail loudly
    # (non-zero exit, ERROR: in stdout) — and, the actual point of the fix, the file on disk
    # must still parse cleanly afterward and be completely unchanged, i.e. the fix prevents
    # the brick, not just makes the failing CLI call itself noisy.
    def test_cli_update_rejects_embedded_header_and_does_not_brick_file(self):
        target = self.tmp_path / "cli_bad_next.md"
        new_result = subprocess.run(
            [
                sys.executable,
                CHECKPOINT_PY,
                "new",
                str(target),
                "--title",
                "t",
                "--owner",
                "director",
                "--decision-sheet",
                "Goal: ship the fix.",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(new_result.returncode, 0, new_result.stdout + new_result.stderr)
        before_data = checkpoint.read_checkpoint(target)
        before_bytes = target.read_bytes()

        bad_next = "Still to do:\n## Blocked on\n- waiting on the retry-path answer"
        update_result = subprocess.run(
            [sys.executable, CHECKPOINT_PY, "update", str(target), "--next", bad_next],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(update_result.returncode, 0)
        self.assertIn("ERROR:", update_result.stdout)

        # the fix: the file must still parse cleanly (read_checkpoint called directly, not
        # via the CLI) and be byte-for-byte unchanged from before the failed CLI call.
        after_data = checkpoint.read_checkpoint(target)
        self.assertEqual(after_data, before_data)
        self.assertEqual(target.read_bytes(), before_bytes)
        self.assertEqual(checkpoint.validate_checkpoint(target), [])


if __name__ == "__main__":
    unittest.main()
