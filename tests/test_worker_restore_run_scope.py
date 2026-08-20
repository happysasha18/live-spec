"""The verify step judges the exact worker run being accepted, never an ambient time window."""
import os

from conftest import ROOT
from test_worker_restore import _gate, _transcript_root


GATE = os.path.join(ROOT, "guardrails", "check-worker-restore.py")


def test_an_exact_bad_run_reds_even_when_its_timestamp_is_old(tmp_path):
    root, run = _transcript_root(
        tmp_path, ["git checkout -- TEST_MATRIX.md"], answers=["ran"])
    result = _gate("--run", run, counting_from=None)
    assert result.returncode == 1, result.stdout
    assert "TEST_MATRIX.md" in result.stdout
    assert "exact worker run" in result.stdout
    assert "history" not in result.stdout.lower()


def test_an_exact_clean_run_passes_while_an_older_bad_run_remains_beside_it(tmp_path):
    root, bad_run = _transcript_root(
        tmp_path / "bad", ["git checkout -- TEST_MATRIX.md"], answers=["ran"],
        session="s-bad", agent="bad0000000000000")
    _, clean_run = _transcript_root(
        tmp_path / "clean", ["git status"], answers=["ran"],
        session="s-clean", agent="clean00000000000")

    clean = _gate("--run", clean_run, counting_from=None)
    assert clean.returncode == 0, clean.stdout
    assert "exact worker run" in clean.stdout

    forensic = _gate("--root", root, "--all")
    assert forensic.returncode == 1, forensic.stdout
    assert bad_run in forensic.stdout


def test_an_explicit_run_in_another_repository_still_reds(tmp_path):
    neighbour = tmp_path / "neighbour"
    neighbour.mkdir()
    (neighbour / ".git").mkdir()
    _, run = _transcript_root(
        tmp_path / "transcripts", ["git stash push -- PRODUCT_SPEC.md"], answers=["ran"],
        cwd=str(neighbour))
    result = _gate("--run", run, counting_from=None)
    assert result.returncode == 1, result.stdout
    assert "ANOTHER PROJECT'S SESSIONS" not in result.stdout


def test_a_missing_exact_run_reds_by_name(tmp_path):
    missing = tmp_path / "agent-missing.jsonl"
    result = _gate("--run", str(missing), counting_from=None)
    assert result.returncode == 1
    assert "cannot read exact worker run" in result.stdout


def test_run_scope_refuses_ambient_window_options(tmp_path):
    _, run = _transcript_root(tmp_path, ["git status"], answers=["ran"])
    result = _gate("--run", run, "--all", counting_from=None)
    assert result.returncode != 0
    assert "not allowed with argument" in result.stderr


def test_run_scope_refuses_equals_spelled_ambient_options(tmp_path):
    _, run = _transcript_root(tmp_path, ["git status"], answers=["ran"])
    for option in ("--since-hours=1", "--counting-from=2026-08-20"):
        result = _gate("--run", run, option, counting_from=None)
        assert result.returncode != 0
        assert "not allowed with argument" in result.stderr


def test_packet_a_does_not_move_the_counting_start_or_add_a_resume_threshold():
    source = open(GATE, encoding="utf-8").read()
    assert "COUNTING_FROM = \"2026-08-18T21:48:00Z\"" in source
    assert "RESUME_THRESHOLD" not in source
    assert "session_started_at" not in source
