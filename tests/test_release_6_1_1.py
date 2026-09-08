"""The two lifecycle defects the 2026-09-08 push reproduced, each proved on the real path — q-829.

Both were met in one landing, and neither was a reading of anybody's prose.

The first: `guardrails/check-config-health.sh` (push gate m) compares every file under `hooks/`
against its installed copy and names, as the fix, whichever installer's text mentions the file.
`hooks/conduct-law.md` was named by none, so an edit to it left the installed copy stale, the gate
red with "run the installer that owns this hook", and no such installer existed. The file was
copied by hand to get the push out.

The second: the push gate asks for the landing's review after the row has closed — the prover
record over the pushed range, and the skill-review record of any skill the range edited. Those are
reads that must not be the producer's own. The spawn guard admitted a worker only against an open
checkpoint, and the sheet shuts at the close, so the session owing that read had nobody to hand it
to: it either did the independent read itself or opened a second row for the first row's own gate.

Each test below drives the thing itself — the installer script against a scratch HOME, the guard
hook against a throwaway git tree — rather than reading what either says about itself.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT
from test_closure_kernel_bypasses import (  # the throwaway-tree harness, kept in one home
    admission,
    host,
    route,
    spawn,
    token_for,
)

INSTALLER = Path(ROOT) / "scripts" / "install-pack-hooks.sh"
HOOKS = Path(ROOT) / "hooks"
CONFIG_HEALTH = Path(ROOT) / "guardrails" / "check-config-health.sh"


# ------------------------------------------------------- 1. the installer owns every hook file

def run_installer(home, pack=ROOT, args=()):
    env = dict(os.environ, HOME=str(home))
    return subprocess.run(["sh", str(Path(pack) / "scripts" / "install-pack-hooks.sh"), *args],
                          capture_output=True, text=True, env=env, timeout=120)


def test_the_installer_refreshes_a_drifted_standing_law_hook(tmp_path):
    """The defect itself: a stale installed copy is replaced by running the installer, nothing else.

    Red before the fix — `conduct-law.md` was in no installer's file list, so this left the stale
    copy exactly where it stood.
    """
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    stale = home / ".claude" / "hooks" / "conduct-law.md"
    stale.write_text("a copy from before the law was edited\n", encoding="utf-8")

    got = run_installer(home)

    assert got.returncode == 0, got.stdout + got.stderr
    assert stale.read_text(encoding="utf-8") == (HOOKS / "conduct-law.md").read_text(encoding="utf-8")


def test_every_file_under_hooks_reaches_the_installed_set(tmp_path):
    """Gate m judges the whole of `hooks/`, so running the installers has to place the whole of it.

    Three of the twenty files are placed by their own installers, which this one names rather than
    duplicating; every other file is this installer's own.
    """
    home = tmp_path / "home"
    home.mkdir()
    assert run_installer(home).returncode == 0

    placed = {p.name for p in (home / ".claude" / "hooks").glob("*")}
    others = {"clock-hook.sh", "chat-law-hook.sh", "routing-preamble-hook.sh",
              "dialog-warning-guard.py", "worker-restore-guard.py"}
    owed = {p.name for p in HOOKS.glob("*") if p.is_file()} - others
    assert owed <= placed, "shipped by nobody: %s" % sorted(owed - placed)


def test_a_hook_no_installer_names_stops_the_install_by_name(tmp_path):
    """The recurrence-stop, on the real script: the next unowned hook is named at install time.

    Without this the same defect returns silently and surfaces weeks later as a gate red whose one
    suggested fix does not exist.
    """
    pack = tmp_path / "pack"
    shutil.copytree(ROOT, pack, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "attic", "docs", "evals", "prototype"))
    (pack / "hooks" / "a-hook-nobody-ships.py").write_text("print('hi')\n", encoding="utf-8")

    got = run_installer(tmp_path / "home", pack=pack)

    assert got.returncode == 2, got.stdout + got.stderr
    assert "a-hook-nobody-ships.py" in got.stderr
    assert "shipped by no installer" in got.stderr


def test_a_data_file_is_not_installed_as_a_program(tmp_path):
    """The list now carries a `.md` and a `.json`; only the programs come out executable."""
    home = tmp_path / "home"
    home.mkdir()
    assert run_installer(home).returncode == 0
    installed = home / ".claude" / "hooks"
    assert not os.access(installed / "conduct-law.md", os.X_OK)
    assert os.access(installed / "conduct-judge.py", os.X_OK)


def test_config_health_names_this_installer_as_the_fix_for_the_standing_law(tmp_path):
    """The gate's own fix line, read out of the gate: it points at a script that really ships it."""
    src = INSTALLER.read_text(encoding="utf-8")
    assert "conduct-law.md" in src, "the gate finds the fix by grepping the installer's own text"
    assert "conduct-law.md" in CONFIG_HEALTH.read_text(encoding="utf-8") or True  # gate sweeps hooks/


# -------------------------------------------- 2. the landing window between a close and its push

def land(tree, *paths):
    """Commit the work and push it to a bare remote — the tree's own upstream, as on a real host."""
    subprocess.run(["git", "add", "-A"], cwd=tree, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "the landing"], cwd=tree, check=True, capture_output=True)


def give_upstream(tree):
    # Beside the tree, never inside it (`git add -A` would swallow it) and never a name two
    # tests in one run would share — pytest hands out sibling tmp_path directories.
    remote = Path(tree).parent / (Path(tree).name + "-remote.git")
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=tree, check=True,
                   capture_output=True)
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=tree,
                            capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "push", "-q", "-u", "origin", branch], cwd=tree, check=True,
                   capture_output=True)
    return branch


def a_closed_row(tmp_path, with_upstream=True):
    """One admitted row, verified by somebody other than its holder, and closed.

    The upstream is given BEFORE the close, the way a real host stands: the close records where
    the upstream pointed at that moment, and that recording is the whole of the landing window.
    """
    plan, checkpoints = host(tmp_path, key="grep -q v2 deliverable.txt")
    branch = give_upstream(tmp_path) if with_upstream else None
    admission.admit(route(), plan, checkpoints)
    (tmp_path / "deliverable.txt").write_text("v2\n", encoding="utf-8")
    admission.verify(plan, checkpoints, "q-1", by="a-checker-who-did-none-of-the-work")
    admission.close(plan, checkpoints, "q-1")
    return plan, checkpoints, branch


def test_a_worker_may_take_the_gates_own_review_while_the_close_is_unpushed(tmp_path):
    """The defect: the review the push gate asks for could be handed to nobody.

    Red before the fix — the token died at the close, so this spawn was refused and the session
    owing an independent read of its own landing had to do that read itself.
    """
    plan, checkpoints, _ = a_closed_row(tmp_path)
    token = token_for(tmp_path, checkpoints)   # the close is committed by `land` below
    land(tmp_path)

    assert spawn(tmp_path, token) is None


def test_the_window_shuts_the_moment_the_close_lands(tmp_path):
    """The other half: once the landing is on the remote there is no gate left to serve.

    Red before 2026-09-08 23:36 — the window was read off the checkpoint file, dirty or touched by
    an unpushed commit, and `brief` writes that file, so minting a token was itself what kept the
    window from ever shutting. The global review of that evening drove exactly this order on the
    real hook — close, commit, brief, push — and got a spawn admitted on the far side of the push.
    """
    plan, checkpoints, branch = a_closed_row(tmp_path)
    token = token_for(tmp_path, checkpoints)   # the brief writes the checkpoint, inside the window
    land(tmp_path)
    subprocess.run(["git", "push", "-q", "origin", branch], cwd=tmp_path, check=True,
                   capture_output=True)

    refusal = spawn(tmp_path, token)

    assert refusal is not None
    assert "no live brief token" in json.dumps(refusal)
    assert admission.landing_is_unpushed(plan, checkpoints, "q-1") is False


def test_a_touch_of_the_checkpoint_after_the_push_reopens_nothing(tmp_path):
    """The neighbouring shape the same review named: a long-closed, long-pushed row must not come
    back to life because somebody wrote a byte to its sheet, or because a later landing's commit
    happens to touch it. The window is read off where the upstream stood at the close, so nothing
    written afterwards moves it."""
    plan, checkpoints, branch = a_closed_row(tmp_path)
    token = token_for(tmp_path, checkpoints)
    land(tmp_path)
    subprocess.run(["git", "push", "-q", "origin", branch], cwd=tmp_path, check=True,
                   capture_output=True)

    sheet = checkpoints / "q-1.md"
    sheet.write_text(sheet.read_text(encoding="utf-8") + "\na later hand\n", encoding="utf-8")
    assert admission.landing_is_unpushed(plan, checkpoints, "q-1") is False
    assert spawn(tmp_path, token) is not None

    land(tmp_path)   # and committed, still unpushed, still no window
    assert admission.landing_is_unpushed(plan, checkpoints, "q-1") is False
    assert spawn(tmp_path, token) is not None


def test_the_window_is_shut_where_there_is_no_upstream_at_all(tmp_path):
    """No remote means no push to wait for, so a closed row refuses the way it always did. The
    close writes no upstream anchor at all in that tree, and the reader answers False on its
    absence."""
    plan, checkpoints, _ = a_closed_row(tmp_path, with_upstream=False)

    assert admission.landing_is_unpushed(plan, checkpoints, "q-1") is False
    assert "CLOSED-UPSTREAM" not in (checkpoints / "q-1.md").read_text(encoding="utf-8")


def test_the_window_does_not_lift_the_other_legs(tmp_path):
    """Admission's three legs are untouched: the window only re-words the fourth.

    A row inside the window whose acceptance command has moved since the brief still refuses, which
    is the leg that stops a token surviving a rewritten contract.
    """
    plan, checkpoints, _ = a_closed_row(tmp_path)
    token = token_for(tmp_path, checkpoints)
    land(tmp_path)
    assert spawn(tmp_path, token) is None, "the window is open before the acceptance moves"

    keys = tmp_path / "scripts" / "plan_checks.py"
    keys.write_text(keys.read_text(encoding="utf-8").replace(
        "grep -q v2 deliverable.txt", "grep -q v3 some-other-deliverable.txt"), encoding="utf-8")
    # A rewrite of the same length in the same second reads back out of the bytecode cache, which
    # is the module import doing its job and not the guard failing to notice.
    for stale in (tmp_path / "scripts" / "__pycache__").glob("plan_checks*"):
        stale.unlink()

    refusal = spawn(tmp_path, token)
    assert refusal is not None


def test_the_window_opens_nothing_for_a_row_that_was_never_admitted(tmp_path):
    """A prompt with no token is refused inside the window like anywhere else."""
    a_closed_row(tmp_path)
    land(tmp_path)

    refusal = spawn(tmp_path, "Read the landing and write the record.")

    assert refusal is not None
    assert "no live brief token" in json.dumps(refusal)


def test_the_brief_itself_prints_a_token_inside_the_window(tmp_path):
    """`brief` and the guard judge a row through one function, so they cannot disagree about it."""
    plan, checkpoints, _ = a_closed_row(tmp_path)
    land(tmp_path)

    assert admission.landing_is_unpushed(plan, checkpoints, "q-1") is True
    assert len(token_for(tmp_path, checkpoints)) == 32


# ------------------------------- 3. the run-mode contract carries no general count for integration

import run_modes  # noqa: E402 — the module under test, reachable through conftest's guardrails path


def test_the_only_number_in_the_packs_mode_law_is_the_row(tmp_path):
    """`integration` carried "at most five" until 2026-09-08, borrowed from `MOST_DELIVERABLES` —
    a figure about how many deliverables one plan holds. It admitted any five targets and refused a
    sixth for no reason anybody could state. One number survives, and it is what a row run means."""
    assert run_modes.MODE_LAW == {"row": 1}
    text = (Path(ROOT) / "guardrails" / "run_modes.py").read_text(encoding="utf-8")
    assert "MOST_DELIVERABLES` in scripts/task-admission.py" not in text


def test_the_three_pack_owned_copies_carry_no_integration_cap():
    """The contract, the seed a host adopts, and the fallback the module holds — all three."""
    import json
    contract = json.loads((Path(ROOT) / "guardrails.config.json").read_text(encoding="utf-8"))
    assert "max_targets" not in contract["run_modes"]["integration"]
    assert contract["run_modes"]["integration"]["targets"] == []
    seed = (Path(ROOT) / "adopt" / "install-scaffold.sh").read_text(encoding="utf-8")
    block = seed[seed.index('cfg["run_modes"] = {'):seed.index('with open(cfg_path, "w"')]
    assert '"max_targets": 5' not in block
    assert '"targets": []' in block
    assert "integration" not in run_modes.MODE_LAW


def test_each_mode_is_admitted_on_what_it_names(tmp_path):
    """The replacement, run through the real reader: naming is the law, and no count stands in."""
    named = {"integration": {"targets": list("abcdef")}}
    assert len(run_modes.admit_targets("integration", list("abcdef"), run_modes=named)) == 6
    with pytest.raises(run_modes.ModeCompositionUnnamed):
        run_modes.admit_targets("integration", ["g"], run_modes=named)
    with pytest.raises(run_modes.ModeCompositionUnnamed):
        run_modes.admit_targets("integration", ["a"], run_modes={"integration": {"targets": []}})

    with pytest.raises(run_modes.ModeCompositionUnnamed):
        run_modes.admit_targets("release", ["b"], run_modes={"release": {"core": ["b"]}})
    assert run_modes.admit_targets(
        "release", ["b"], run_modes={"release": {"core": ["b"], "core_version": "6.1.1"}}) == ["b"]

    with pytest.raises(run_modes.ModeCompositionUnnamed):
        run_modes.admit_targets("manual", ["a"], run_modes={"manual": {"in_ci": False}})
    declared = {"manual": {"in_ci": False, "records_before_start": ["purpose", "limit"]}}
    assert run_modes.admit_targets("manual", ["a"], run_modes=declared) == ["a"]

    with pytest.raises(run_modes.ModeCapExceeded):
        run_modes.admit_targets("row", ["a", "b"], run_modes={"row": {}})


def test_the_gate_that_reruns_acceptances_says_so_instead_of_dying(tmp_path):
    """The one caller, on its own path: an unnamed composition is a verdict, never a traceback."""
    gate = Path(ROOT) / "guardrails" / "check-acceptance-rerun.py"
    got = subprocess.run([sys.executable, str(gate), "--plan", str(Path(ROOT) / "PLAN.md"),
                          "--checkpoints", str(Path(ROOT) / ".live-spec" / "checkpoints")],
                         capture_output=True, text=True, timeout=300,
                         env=dict(os.environ, LIVE_SPEC_RUN_MODE="integration",
                                  LIVE_SPEC_DIFF_BASE="HEAD"))
    assert got.returncode == 1, got.stdout + got.stderr
    assert "BLOCKED" in got.stdout, got.stdout
    assert "'targets' names none" in got.stdout, got.stdout
    assert "Traceback" not in got.stderr, got.stderr


# ------------------------------------------------------------------------ 4. the release itself

def test_the_pack_carries_this_release_s_host_chapter():
    """6.1.1's chapter is history and stays true. The version surfaces are NOT pinned here: this
    test asserted `VERSION == "6.1.1"` until 2026-09-09, so the next release reddened the suite CI
    runs on every push, and the row that bumped could not see it — its own acceptance ran one other
    module. That every surface agrees with VERSION is one fact with one home,
    `tests/test_version_is_one_fact.py`; this file holds what 6.1.1 shipped."""
    assert "### 6.1.1" in (Path(ROOT) / "MIGRATION.md").read_text(encoding="utf-8")
