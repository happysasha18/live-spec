"""scripts/director-wire-report.py — standalone, read-only, informational report on how far a
Director decision sheet already covers the commits gate (a) (check-prover-record.sh) would
demand a fresh prover record for. It never gates anything; these tests prove the report
content and the "reports, never gates" exit-code contract, against temp git repos rather than
this repository's own real, ever-changing state.
"""

import os
import subprocess
import sys
import tempfile
import shutil
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "director-wire-report.py")
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

sys.path.insert(0, SCRIPTS_DIR)
import checkpoint as checkpoint_mod  # noqa: E402


def _git(args, cwd, env=None):
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, env=full_env
    )
    assert result.returncode == 0, "git %s failed: %s" % (args, result.stderr)
    return result.stdout.strip()


def _run_report(cwd, diff_base=None):
    env = dict(os.environ)
    if diff_base is not None:
        env["LIVE_SPEC_DIFF_BASE"] = diff_base
    else:
        env.pop("LIVE_SPEC_DIFF_BASE", None)
    return subprocess.run(
        [sys.executable, SCRIPT], cwd=cwd, capture_output=True, text=True, env=env
    )


class DirectorWireReportBase(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="director-wire-report-test-")
        _git(["init", "-q"], self.repo)
        _git(["config", "user.email", "test@example.com"], self.repo)
        _git(["config", "user.name", "Test"], self.repo)
        with open(os.path.join(self.repo, "README.md"), "w") as f:
            f.write("initial\n")
        _git(["add", "README.md"], self.repo)
        _git(["commit", "-q", "-m", "initial"], self.repo)
        self.base_sha = _git(["rev-parse", "HEAD"], self.repo)
        os.makedirs(os.path.join(self.repo, ".live-spec", "checkpoints"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def _write_closed_checkpoint(self, name, documents_body):
        path = os.path.join(self.repo, ".live-spec", "checkpoints", name)
        checkpoint_mod.new_checkpoint(
            path,
            title="Test checkpoint",
            owner="Director",
            decision_sheet=(
                "- **Goal** — a test goal\n"
                "- **Documents that must change** — %s" % documents_body
            ),
        )
        checkpoint_mod.close_checkpoint(path)
        return path

    def _write_closed_checkpoint_raw(self, name, decision_sheet):
        """Like _write_closed_checkpoint, but takes the full DECISION SHEET body verbatim
        (for shapes _write_closed_checkpoint can't express: multi-line fields, alternate
        field labels)."""
        path = os.path.join(self.repo, ".live-spec", "checkpoints", name)
        checkpoint_mod.new_checkpoint(
            path, title="Test checkpoint", owner="Director", decision_sheet=decision_sheet
        )
        checkpoint_mod.close_checkpoint(path)
        return path

    def _commit_all(self, message):
        _git(["add", "-A"], self.repo)
        _git(["commit", "-q", "-m", message], self.repo)
        return _git(["rev-parse", "HEAD"], self.repo)


class TestEmptyDocumentsFieldCovers(DirectorWireReportBase):
    def test_covers_the_commit_that_touched_it(self):
        self._write_closed_checkpoint("covering.md", "none")
        commit_sha = self._commit_all("add covering checkpoint")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(commit_sha[:12], result.stdout)
        # It must land in the Covered section, not Uncovered.
        covered_section = result.stdout.split("Covered commits")[1].split("Uncovered commits")[0]
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertIn(commit_sha[:12], covered_section)
        self.assertNotIn(commit_sha[:12], uncovered_section)


class TestNonEmptyDocumentsFieldDoesNotCover(DirectorWireReportBase):
    def test_still_requires_the_record(self):
        self._write_closed_checkpoint(
            "noncover.md", "PRODUCT_SPEC.md gains a new criterion"
        )
        commit_sha = self._commit_all("add non-covering checkpoint")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        covered_section = result.stdout.split("Covered commits")[1].split("Uncovered commits")[0]
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertNotIn(commit_sha[:12], covered_section)
        self.assertIn(commit_sha[:12], uncovered_section)


class TestCommitWithNoCheckpointIsUncovered(DirectorWireReportBase):
    def test_uncovered_when_no_checkpoint_matches(self):
        with open(os.path.join(self.repo, "some_file.py"), "w") as f:
            f.write("x = 1\n")
        commit_sha = self._commit_all("plain commit, no checkpoint at all")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertIn(commit_sha[:12], uncovered_section)


class TestDisclaimerAlwaysPresent(DirectorWireReportBase):
    DISCLAIMER = (
        "INFORMATIONAL ONLY — this does not affect any gate. Wiring this into gate (a) "
        "needs a new STAND-DOWN class and a PRODUCT_SPEC.md R226 criterion, which needs "
        "the owner's word, not this script."
    )

    def test_disclaimer_present_with_checkpoints(self):
        self._write_closed_checkpoint("covering.md", "-")
        self._commit_all("add checkpoint")
        result = _run_report(self.repo, diff_base=self.base_sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.DISCLAIMER, result.stdout)

    def test_disclaimer_present_with_no_checkpoints_at_all(self):
        with open(os.path.join(self.repo, "plain.txt"), "w") as f:
            f.write("hello\n")
        self._commit_all("plain commit")
        result = _run_report(self.repo, diff_base=self.base_sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.DISCLAIMER, result.stdout)

    def test_disclaimer_present_when_no_range_resolves(self):
        # A repo with no origin/main and only one commit: with no LIVE_SPEC_DIFF_BASE, and
        # HEAD~1 unresolvable (only one commit exists), no range resolves at all.
        result = _run_report(self.repo, diff_base=None)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.DISCLAIMER, result.stdout)


class TestExitCodeZeroWhenNothingQualifies(DirectorWireReportBase):
    def test_exit_zero_with_no_checkpoints_directory_content(self):
        # checkpoints dir exists (created in setUp) but holds no files at all.
        with open(os.path.join(self.repo, "unrelated.txt"), "w") as f:
            f.write("no checkpoint touches this\n")
        commit_sha = self._commit_all("no checkpoints ever written")
        result = _run_report(self.repo, diff_base=self.base_sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertIn(commit_sha[:12], uncovered_section)

    def test_exit_zero_with_open_checkpoint_only(self):
        # An open (not closed) checkpoint touching the range never covers anything, but the
        # script still reports cleanly rather than erroring.
        path = os.path.join(self.repo, ".live-spec", "checkpoints", "open.md")
        checkpoint_mod.new_checkpoint(
            path, title="Open checkpoint", owner="Director",
            decision_sheet="- **Documents that must change** — none",
        )
        commit_sha = self._commit_all("add open checkpoint")
        result = _run_report(self.repo, diff_base=self.base_sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertIn(commit_sha[:12], uncovered_section)


class TestMultiLineDocumentsFieldDoesNotFalselyCover(DirectorWireReportBase):
    """Finding 4: a realistic decision sheet often puts the label alone on its line and the
    real document list on the lines below it. The old single-line capture saw an empty tail
    after the em dash and wrongly reported the commit as "covered" — the dangerous direction,
    since two real documents are actually listed."""

    def test_list_on_following_lines_is_not_treated_as_empty(self):
        self._write_closed_checkpoint_raw(
            "multiline.md",
            "- **Goal** — a test goal\n"
            "- **Documents that must change** —\n"
            "  - PRODUCT_SPEC.md\n"
            "  - ARCHITECTURE.md\n"
            "- **Evidence** — a passing test",
        )
        commit_sha = self._commit_all("add multi-line documents checkpoint")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        covered_section = result.stdout.split("Covered commits")[1].split("Uncovered commits")[0]
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertNotIn(commit_sha[:12], covered_section)
        self.assertIn(commit_sha[:12], uncovered_section)


class TestShortFormDocumentsLabelRecognized(DirectorWireReportBase):
    """Finding 5: skills/director/SKILL.md's own worked example writes the field as the short
    "**Documents**" label, not the long "**Documents that must change**" form the field is
    defined with elsewhere in the same file. The regex must recognize both as the same
    field."""

    def test_short_form_label_with_empty_body_covers(self):
        self._write_closed_checkpoint_raw(
            "shortform.md", "- **Goal** — a test goal\n- **Documents** — none"
        )
        commit_sha = self._commit_all("add short-form documents checkpoint")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        covered_section = result.stdout.split("Covered commits")[1].split("Uncovered commits")[0]
        # Before the fix the regex required the literal "Documents that must change" text and
        # never matched "**Documents**" at all -- the checkpoint would show as carrying no
        # such line, and the commit would stay uncovered even though the field plainly says
        # nothing needs to change.
        self.assertIn(commit_sha[:12], covered_section)

    def test_skill_worked_example_wording_stays_uncovered_known_limitation(self):
        # The skill's own worked-example body ("none. The spec already says what should
        # happen") is now correctly RECOGNIZED as the Documents field by the finding-5 fix,
        # but that exact text does not match _is_empty_body()'s recognized empty forms
        # ("", "none", "-", "(nothing...)"), so it still reports "uncovered" here -- a known,
        # separate limitation of _is_empty_body() itself, not something this script owns.
        self._write_closed_checkpoint_raw(
            "worked_example.md",
            "- **Goal** — a test goal\n"
            "- **Documents** — none. The spec already says what should happen",
        )
        commit_sha = self._commit_all("add skill worked-example checkpoint")

        result = _run_report(self.repo, diff_base=self.base_sha)

        self.assertEqual(result.returncode, 0, result.stderr)
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertIn(commit_sha[:12], uncovered_section)


class TestLastResortBaseNeverReportsCovered(DirectorWireReportBase):
    """Finding 8: gate (a) (guardrails/check-prover-record.sh) itself treats the HEAD~1
    last-resort base as "a base no real push would ever measure against" and never runs any
    stand-down reasoning against it. This report must hold itself to the same rule."""

    def test_last_resort_treats_covering_checkpoint_as_uncovered(self):
        self._write_closed_checkpoint("covering.md", "none")
        commit_sha = self._commit_all("add covering checkpoint")

        # No LIVE_SPEC_DIFF_BASE, and this temp repo has no origin/main remote, so
        # resolve_diff_base falls back to HEAD~1 -- the last-resort base. HEAD~1 here equals
        # self.base_sha, the same range TestEmptyDocumentsFieldCovers uses explicitly (and
        # where the very same checkpoint body DOES cover the commit).
        result = _run_report(self.repo, diff_base=None)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[last-resort]", result.stdout)
        covered_section = result.stdout.split("Covered commits")[1].split("Uncovered commits")[0]
        uncovered_section = result.stdout.split("Uncovered commits")[1]
        self.assertNotIn(commit_sha[:12], covered_section)
        self.assertIn(commit_sha[:12], uncovered_section)
        self.assertIn("base resolved via HEAD~1 (last resort)", result.stdout)


class TestNeverWiredIntoPrePushOrCI(unittest.TestCase):
    """Finding 6: make the "never wired in" claim in this script's own docstring a checked
    command, following the same pattern as tests/test_no_history.py's
    test_gate_not_wired_into_pre_push_or_ci."""

    def test_script_not_wired_into_pre_push_install_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("director-wire-report", f.read())
        with open(os.path.join(ROOT, "guardrails", "install.sh"), encoding="utf-8") as f:
            self.assertNotIn("director-wire-report", f.read())
        workflows_dir = os.path.join(ROOT, ".github", "workflows")
        workflow_files = [
            os.path.join(workflows_dir, name)
            for name in os.listdir(workflows_dir)
            if name.endswith(".yml")
        ]
        self.assertTrue(workflow_files, "no .github/workflows/*.yml files found to check")
        for wf in workflow_files:
            with open(wf, encoding="utf-8") as f:
                self.assertNotIn("director-wire-report", f.read())


class TestScriptErrorExitCode(unittest.TestCase):
    def test_bad_args_exit_nonzero(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "--not-a-real-flag"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_outside_git_repo_exit_nonzero(self):
        outside = tempfile.mkdtemp(prefix="director-wire-report-outside-")
        try:
            env = dict(os.environ)
            env.pop("LIVE_SPEC_DIFF_BASE", None)
            result = subprocess.run(
                [sys.executable, SCRIPT], cwd=outside, capture_output=True, text=True, env=env
            )
            self.assertNotEqual(result.returncode, 0)
        finally:
            shutil.rmtree(outside, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
