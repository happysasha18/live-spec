"""tests/test_install_session_hooks.py — the setup walk installs every hook the pack declares
(ROADMAP row 506).

guardrails/judge-hooks.json declares ten wired session hooks, each with its event, its plain command
form, and the shipped data files it reads. scripts/install-session-hooks.sh is the ONE command a human
runs (the harness classifier blocks an agent's own hand in its configuration, so this is the only lever
that reaches a real machine's settings.json). This suite drives that REAL script against an isolated
fake $HOME — never the real one — and proves the installer's coverage against the declaration in both
directions: every declared wired hook ends up wired under its declared event with its declared command,
every declared data file lands beside the hook that reads it, nothing undeclared gets copied, a personal
overlay already on the machine is never touched, a hook this host already wired by hand in ANY form
(including wrapped in the personal ~/.claude/hooks/hook-meter.py counter) is recognized as already
present rather than duplicated, and a second run changes nothing.

RED PROOF (captured 2026-07-27, before this row's fix): scripts/install-session-hooks.sh copied only
clock-hook.sh and chat-law-hook.sh and wired only those two UserPromptSubmit entries. Against that tree,
test_every_declared_hook_ends_up_wired failed naming the eight still-missing stems (answer-first-scan,
scissors-scan, hedge-scan, affirmation-scan, code-anchor-scan, register-judge-collect,
register-judge-report was ALSO covered already so only pipe seven were absent beyond the two already
wired — see the delivery report for the exact captured stdout), test_every_declared_data_file_is_installed
failed on turn_reader.py/chat-calques.json/register_judge_core.py/register-judge.py never landing, and
test_rerun_changes_nothing could not even be reached meaningfully since the first run itself under-covered.
Fixed by teaching the installer to read the declaration for its own two hooks (clock-hook, chat-law-hook)
and chain to the existing scripts/install-pack-hooks.sh for the other eight (that script already carried
its own tests pinned to its literal source, so it is chained rather than rewritten), reaching all ten
from the one command a human actually runs.
"""
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLER = os.path.join(REPO_ROOT, "scripts", "install-session-hooks.sh")
DECL_PATH = os.path.join(REPO_ROOT, "guardrails", "judge-hooks.json")


def _load_decl():
    with open(DECL_PATH, encoding="utf-8") as f:
        return json.load(f)


def _run_installer(home):
    env = dict(os.environ)
    env["HOME"] = home
    return subprocess.run(["sh", INSTALLER], capture_output=True, text=True, timeout=60, env=env)


def _settings(home):
    path = os.path.join(home, ".claude", "settings.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _commands_for(settings, event):
    out = []
    for group in settings.get("hooks", {}).get(event, []):
        for h in group.get("hooks", []):
            cmd = h.get("command", "")
            if cmd:
                out.append(cmd)
    return out


def test_every_declared_hook_ends_up_wired(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    decl = _load_decl()
    wired = decl["wired"]
    files = decl["file"]
    settings = _settings(home)

    missing = []
    for stem, event in sorted(wired.items()):
        cmds = _commands_for(settings, event)
        fname = files[stem]
        if not any(fname in c for c in cmds):
            missing.append((stem, event))
    assert not missing, "not wired after a fresh install: %r\nstdout:\n%s" % (missing, proc.stdout)


def test_every_declared_hook_command_matches_the_declaration(tmp_path):
    """Not just present — wired with the EXACT command string the declaration states, so a fresh
    install reproduces the command form (interpreter + path) rather than some other invocation."""
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    decl = _load_decl()
    settings = _settings(home)
    mismatched = []
    for stem, event in sorted(decl["wired"].items()):
        cmds = _commands_for(settings, event)
        want = decl["command"][stem]
        if want not in cmds:
            mismatched.append((stem, want, cmds))
    assert not mismatched, "declared command form not found verbatim: %r" % (mismatched,)


def test_every_declared_data_file_is_installed_beside_its_hook(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    decl = _load_decl()
    installed_dir = os.path.join(home, ".claude", "hooks")
    missing = []
    for stem, datafiles in decl["data"].items():
        for df in datafiles:
            if not os.path.isfile(os.path.join(installed_dir, df)):
                missing.append((stem, df))
    assert not missing, "data files missing after install: %r" % (missing,)


def test_no_undeclared_file_is_installed(tmp_path):
    """Direction two: nothing lands in the installed hooks dir beyond a declared hook file or a
    declared data file — an installer that copies a stray file is as much a drift as one that misses
    a declared one."""
    home = str(tmp_path / "home")
    os.makedirs(home)
    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    decl = _load_decl()
    allowed = set(decl["file"].values())
    for datafiles in decl["data"].values():
        allowed.update(datafiles)

    installed_dir = os.path.join(home, ".claude", "hooks")
    present = {f for f in os.listdir(installed_dir) if os.path.isfile(os.path.join(installed_dir, f))}
    stray = present - allowed
    assert not stray, "installer put undeclared file(s) in place: %r" % (stray,)


def test_rerun_changes_nothing(tmp_path):
    home = str(tmp_path / "home")
    os.makedirs(home)
    first = _run_installer(home)
    assert first.returncode == 0, first.stdout + first.stderr
    settings_after_first = _settings(home)

    second = _run_installer(home)
    assert second.returncode == 0, second.stdout + second.stderr
    settings_after_second = _settings(home)

    assert settings_after_first == settings_after_second, "a re-run changed settings.json"
    assert "installed:" not in second.stdout, (
        "a re-run should report every hook already present, never a fresh install: %s" % second.stdout
    )


def test_a_personal_overlay_already_present_is_left_untouched(tmp_path):
    home = str(tmp_path / "home")
    hooks_dir = os.path.join(home, ".claude", "hooks")
    os.makedirs(hooks_dir)
    sentinel = "SENTINEL — a host's own pattern, never the pack's\n"
    with open(os.path.join(hooks_dir, "scissors-personal.json"), "w", encoding="utf-8") as f:
        f.write(sentinel)

    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    with open(os.path.join(hooks_dir, "scissors-personal.json"), encoding="utf-8") as f:
        assert f.read() == sentinel, "the installer touched a personal overlay file"
    assert "scissors-personal.json" in proc.stdout, (
        "the installer should name the personal overlay it left alone: %s" % proc.stdout
    )


def test_a_meter_wrapped_existing_entry_is_recognized_not_duplicated(tmp_path):
    """A host may already wrap a hook in the personal ~/.claude/hooks/hook-meter.py counter (this
    machine wraps seven of the ten today). The installer must recognize that hook as already wired by
    its filename appearing in the existing command — whatever form that command takes — and never add
    a second, plain-form entry beside it."""
    home = str(tmp_path / "home")
    claude_dir = os.path.join(home, ".claude")
    os.makedirs(claude_dir)
    settings_path = os.path.join(claude_dir, "settings.json")
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump({
            "hooks": {
                "Stop": [
                    {"hooks": [{"type": "command",
                                "command": "python3 ~/.claude/hooks/hook-meter.py ~/.claude/hooks/scissors-scan.py"}]}
                ]
            }
        }, f)

    proc = _run_installer(home)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    settings = _settings(home)
    cmds = _commands_for(settings, "Stop")
    scissors_cmds = [c for c in cmds if "scissors-scan.py" in c]
    assert len(scissors_cmds) == 1, "the meter-wrapped entry was duplicated rather than recognized: %r" % cmds
    assert "hook-meter.py" in scissors_cmds[0], "the installer rewrote the host's own meter-wrapped form"
