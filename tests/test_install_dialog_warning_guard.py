"""tests/test_install_dialog_warning_guard.py — the dialog-warning guard installs mechanically.

Found 2026-09-03: `hooks/dialog-warning-guard.py` (PLAN q-581) shipped and closed, but no installer
made it reach a fresh machine — it was present on the dev machine only because a prior session
copied it by hand. This drove the row's own promise — `guardrails/check-config-health.sh`'s
source-vs-installed diff stays green — accidentally rather than by mechanism. This suite drives the
real installer against an isolated fake $HOME, never the real one.
"""
import os
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLER = os.path.join(REPO_ROOT, "scripts", "install-dialog-warning-guard.sh")


def _run(home, *args):
    env = dict(os.environ)
    env["HOME"] = home
    return subprocess.run(["sh", INSTALLER, *args], capture_output=True, text=True,
                           timeout=30, env=env)


def test_dry_run_copies_nothing(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run(home, "--dry-run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    dest = os.path.join(home, ".claude", "hooks", "dialog-warning-guard.py")
    assert not os.path.exists(dest), "a dry run must copy nothing"
    assert "would copy" in proc.stdout


def test_real_run_installs_and_self_tests(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    dest = os.path.join(home, ".claude", "hooks", "dialog-warning-guard.py")
    assert os.path.isfile(dest), "the hook file did not land"
    assert "self-tests OK" in proc.stdout


def test_wires_nothing_into_settings(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    settings = os.path.join(home, ".claude", "settings.json")
    assert not os.path.exists(settings), "this installer must not create or edit settings.json"


def test_rerun_reports_already_present(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    first = _run(home)
    assert first.returncode == 0, first.stdout + first.stderr
    second = _run(home)
    assert second.returncode == 0, second.stdout + second.stderr
    assert "already present" in second.stdout
    assert "installed:" not in second.stdout
