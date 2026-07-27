"""tests/test_check_hooks_can_fire.py — the hook red-proof runner proves it can red itself.

guardrails/check-hooks-can-fire.py is the hook-side sibling of check-every-gate-can-fail.py (gate w):
it runs every classified session hook against a fixture built to trigger it and fails when a hook
stays silent. A runner that can only ever pass is itself a hollow check, so this file proves the
runner REDS on a hook that never fires and on a fixture carrying no trigger, before it proves the
runner stays green against the real, shipped fixtures.
"""
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = os.path.join(REPO_ROOT, "guardrails", "check-hooks-can-fire.py")
REAL_FIXTURES_DIR = os.path.join(REPO_ROOT, "guardrails", "hook-red-fixtures")
REAL_HOOKS_DIR = os.path.join(REPO_ROOT, "hooks")
REAL_INSTALLED_DIR = os.path.expanduser("~/.claude/hooks")


def _run(env_overrides):
    env = dict(os.environ)
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, RUNNER], capture_output=True, text=True, timeout=60, env=env,
    )


def test_runner_reds_on_a_hook_that_never_fires(tmp_path):
    """Point the runner at a stub hook that always exits 0 with empty stdout — a hook that can never
    fire — and assert the runner's own exit is non-zero and names the silent hook."""
    stub_hooks_dir = tmp_path / "hooks"
    stub_hooks_dir.mkdir()
    (stub_hooks_dir / "scissors-scan.py").write_text(
        "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"
    )

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "scissors-scan.py": {"fixture": "hook-red-fixtures/scissors-scan", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    empty_installed_dir = tmp_path / "no-installed-hooks"
    empty_installed_dir.mkdir()

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_REPO_DIR": str(stub_hooks_dir),
        "HOOKS_INSTALLED_DIR": str(empty_installed_dir),
        "HOOKS_FIXTURES_DIR": REAL_FIXTURES_DIR,
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "SILENT scissors-scan.py" in proc.stdout, proc.stdout


def test_runner_reds_on_a_fixture_that_carries_no_trigger(tmp_path):
    """Break the FIXTURE instead of the hook: a transcript with no offending text must not make the
    real hook fire, so the runner reds exactly as it would for a genuinely blind hook."""
    fixtures_root = tmp_path / "fixtures"
    fixture_dir = fixtures_root / "scissors-scan"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "payload.json").write_text(json.dumps({
        "transcript_path": "transcript.jsonl", "session_id": "broken", "stop_hook_active": False,
    }))
    (fixture_dir / "transcript.jsonl").write_text(
        json.dumps({"type": "user", "message": {"role": "user",
                    "content": [{"type": "text", "text": "hi"}]}}) + "\n"
        + json.dumps({"type": "assistant", "message": {"role": "assistant",
                      "content": [{"type": "text", "text": "All is well, nothing notable here."}]}}) + "\n"
    )

    proofs_json = tmp_path / "proofs.json"
    proofs_json.write_text(json.dumps({
        "proofs": {
            "scissors-scan.py": {"fixture": "hook-red-fixtures/scissors-scan", "detect": "json-block"}
        },
        "cannot_red": {},
    }))

    proc = _run({
        "HOOKS_PROOFS_JSON": str(proofs_json),
        "HOOKS_REPO_DIR": REAL_HOOKS_DIR,
        "HOOKS_INSTALLED_DIR": REAL_INSTALLED_DIR,
        "HOOKS_FIXTURES_DIR": str(fixtures_root),
    })

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "SILENT scissors-scan.py" in proc.stdout, proc.stdout


def test_runner_is_green_on_the_real_shipped_fixtures():
    """The actual census: every hook classified in guardrails/hook-red-proofs.json fires against its
    real, shipped fixture under guardrails/hook-red-fixtures/."""
    proc = _run({})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FAIL" not in proc.stdout
