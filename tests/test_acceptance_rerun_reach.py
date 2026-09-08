"""Which done rows `check-acceptance-rerun.py` actually re-runs on a push — id: q-826 (the reach
half of it; the mode contract and the config key it reads live elsewhere).

The owner's word, 2026-09-07 22:00: CI runs a fixed release core AND a limited set of
actually-affected obligations. The release core is a list of GATES (`run_modes.release.core` in
`guardrails.config.json`) — this script is one entry in it — and the obligations are PLAN.md rows.
The two never belonged in one selection: an earlier version of this gate read that gate-list and
treated its entries as row ids too, a category error corrected 2026-09-08. This gate now selects
only the AFFECTED rows: a done row whose own contract (`Done when` / `DOD hash.` in PLAN.md) or
own files (its recorded acceptance command in `scripts/plan_checks.py`, or a file that command
names) moved in the pushed range. A done row that is not affected is closed history, and this file
proves it is never walked — including a row the release-core config happens to name, which this
gate does not read at all for its own row selection.

Each scenario below plants a two-commit fixture tree (BASE, then HEAD — the pushed range) with
done rows, one per reason a row can or cannot be selected, and reads `LIVE_SPEC_DIFF_BASE` as the
base commit — the same variable `check-prover-record.sh` reads first, before `origin/main` and
`HEAD~1`. Every row's acceptance command is a sentinel write: the row ran if, and only if, its
file appears.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

RERUN = Path(ROOT) / "guardrails" / "check-acceptance-rerun.py"

PLAN_HEAD = """# Fixture plan

## Tasks

### ✅ Untouched control row — id: q-ctrl
**Done when:** nothing about this row moves across the push
**DOD hash.** deadbeef0

### ✅ Row whose contract text moves — id: q-contract
**Done when:** the new wording nobody had at the base commit
**DOD hash.** deadbeef1

### ✅ Row whose acceptance command moves — id: q-accept
**Done when:** stays fixed across the push
**DOD hash.** deadbeef2

### ✅ Row naming a file that moves — id: q-file
**Done when:** stays fixed across the push
**DOD hash.** deadbeef3

### ✅ Row untouched by the push but named in the release-core config — id: q-core
**Done when:** stays fixed across the push
**DOD hash.** deadbeef4

## Blockers

None.
"""

PLAN_BASE = PLAN_HEAD.replace(
    "**Done when:** the new wording nobody had at the base commit",
    "**Done when:** the old wording, before the push",
)

CHECKS_HEAD = {
    "q-ctrl": "touch sentinel-ctrl.txt",
    "q-contract": "touch sentinel-contract.txt",
    "q-accept": "touch sentinel-accept.txt",
    "q-file": "test -f watched-file.txt && touch sentinel-file.txt",
    "q-core": "touch sentinel-core.txt",
}
CHECKS_BASE = {**CHECKS_HEAD, "q-accept": "true"}

# Names q-core as a release-core GATE-list entry — irrelevant to this script's own row
# selection, and the regression this file exists to prevent is exactly this config being read
# as if it named a row.
CONFIG = {"run_modes": {"release": {"core": ["q-core"]}}}


def _checks_text(table):
    return "CHECKS = %r\n" % table


def _git(tree, *args, check=True):
    return subprocess.run(["git", *args], cwd=str(tree), check=check, capture_output=True, text=True)


def build_fixture(tmp_path):
    """A throwaway tree with two commits: BASE, then HEAD (the pushed range). Returns
    (plan_path, checkpoints_dir, base_sha)."""
    plan = tmp_path / "PLAN.md"
    (tmp_path / "scripts").mkdir()
    checks = tmp_path / "scripts" / "plan_checks.py"
    config = tmp_path / "guardrails.config.json"
    watched = tmp_path / "watched-file.txt"

    plan.write_text(PLAN_BASE, encoding="utf-8")
    checks.write_text(_checks_text(CHECKS_BASE), encoding="utf-8")
    config.write_text(json.dumps(CONFIG), encoding="utf-8")
    watched.write_text("before\n", encoding="utf-8")

    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.invalid")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "base")
    base_sha = _git(tmp_path, "rev-parse", "HEAD").stdout.strip()

    plan.write_text(PLAN_HEAD, encoding="utf-8")
    checks.write_text(_checks_text(CHECKS_HEAD), encoding="utf-8")
    watched.write_text("after\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "the push")

    checkpoints = tmp_path / ".live-spec" / "checkpoints"
    return plan, checkpoints, base_sha


def run_rerun(tmp_path, plan, checkpoints, base_sha, mode="release"):
    """Run the gate the way CI runs it. The mode is named on every call because the gate refuses
    a run that named none (Requirement 322 criterion 1); `mode=None` is how a test asks for that
    refusal itself."""
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base_sha)
    env.pop("LIVE_SPEC_EVALUATING", None)
    env.pop("LIVE_SPEC_PUSH_FULL", None)
    # The CI markers are cleared, so a fixture run is a fixture run wherever the suite itself is
    # running. Inherited through `dict(os.environ, ...)`, they made the gate's own CI refusal fire
    # inside the manual scenario below — green on a laptop and red on the server, which is the
    # one direction a test must never differ in. The test that wants those markers sets them.
    env.pop("GITHUB_ACTIONS", None)
    env.pop("CI", None)
    if mode is None:
        env.pop("LIVE_SPEC_RUN_MODE", None)
    else:
        env["LIVE_SPEC_RUN_MODE"] = mode
    return subprocess.run(
        [sys.executable, str(RERUN), "--plan", str(plan), "--checkpoints", str(checkpoints)],
        cwd=str(tmp_path), env=env, capture_output=True, text=True, timeout=60,
    )


def sentinel(tmp_path, name):
    return (tmp_path / ("sentinel-%s.txt" % name)).exists()


def test_an_untouched_row_is_never_run(tmp_path):
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base)
    assert not sentinel(tmp_path, "ctrl"), "closed history got walked: " + got.stdout


def test_a_row_whose_done_when_text_moved_in_the_range_is_run(tmp_path):
    plan, checkpoints, base = build_fixture(tmp_path)
    run_rerun(tmp_path, plan, checkpoints, base)
    assert sentinel(tmp_path, "contract")


def test_a_row_whose_recorded_acceptance_command_moved_in_the_range_is_run(tmp_path):
    plan, checkpoints, base = build_fixture(tmp_path)
    run_rerun(tmp_path, plan, checkpoints, base)
    assert sentinel(tmp_path, "accept")


def test_a_row_naming_a_file_that_changed_in_the_range_is_run(tmp_path):
    plan, checkpoints, base = build_fixture(tmp_path)
    run_rerun(tmp_path, plan, checkpoints, base)
    assert sentinel(tmp_path, "file")


def test_a_row_untouched_by_the_range_never_runs_even_when_the_release_core_config_names_it(tmp_path):
    """The regression this correction exists to prevent: `run_modes.release.core` naming a row's
    id must not make this gate run it. That config is a GATE list; this gate is one entry in it,
    and it selects rows off the pushed range alone, never off that list."""
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base)
    assert not sentinel(tmp_path, "core"), "the release-core config leaked into row selection: " + got.stdout


def _load_rerun_module():
    """A fresh import of the gate module, so a test can shrink its EMERGENCY_STOP_SECONDS without
    touching the constant every other test relies on (300s, unshrunk, everywhere else)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_acceptance_rerun_under_test", str(RERUN))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_a_stopped_command_is_unjudged_and_never_a_failed_verdict(tmp_path, monkeypatch):
    """Criterion 11: a runtime timeout takes no part in the verdict. A selected row whose own
    acceptance command outlives the emergency stop must be reported UNJUDGED, never as a failed
    acceptance, and must never be the thing that turns the gate red."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checks = tmp_path / "scripts" / "plan_checks.py"
    slow_checks = {**CHECKS_HEAD, "q-contract": "sleep 5"}
    checks.write_text(_checks_text(slow_checks), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "the slow check")

    monkeypatch.setenv("LIVE_SPEC_DIFF_BASE", base)
    monkeypatch.delenv("LIVE_SPEC_EVALUATING", raising=False)

    mod = _load_rerun_module()
    monkeypatch.setattr(mod, "EMERGENCY_STOP_SECONDS", 1)

    ran, faults, unanchored, keyless, offmachine, unjudged, total, total_done, reasons = mod.judge(
        str(plan), str(checkpoints), 1, "release")

    assert any(line.startswith("q-contract: ") for line in unjudged), unjudged
    assert not any("q-contract" in line for line in faults), faults
    assert not faults, "a stopped command must never turn the gate red on its own: %r" % faults


def test_the_summary_never_claims_a_pass_over_an_unjudged_row(tmp_path, monkeypatch, capsys):
    """docs/prover F2 residual: 'every selected row's acceptance passes here' used to print even
    when the emergency stop left a row UNJUDGED, overstating by exactly the row it had just named.
    A clean gate with an unjudged row must say so, never claim the blanket pass line."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checks = tmp_path / "scripts" / "plan_checks.py"
    slow_checks = {**CHECKS_HEAD, "q-contract": "sleep 5"}
    checks.write_text(_checks_text(slow_checks), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "the slow check")

    monkeypatch.setenv("LIVE_SPEC_DIFF_BASE", base)
    # The run names its kind, the way the gates workflow's own step does. A run that names none is
    # refused before it selects anything (Requirement 322 criterion 1), which has its own test.
    monkeypatch.setenv("LIVE_SPEC_RUN_MODE", "release")
    monkeypatch.delenv("LIVE_SPEC_EVALUATING", raising=False)
    monkeypatch.setattr(
        sys, "argv",
        ["check-acceptance-rerun.py", "--plan", str(plan), "--checkpoints", str(checkpoints)])

    mod = _load_rerun_module()
    monkeypatch.setattr(mod, "EMERGENCY_STOP_SECONDS", 1)

    code = mod.main()
    out = capsys.readouterr().out

    assert code == 0, out
    assert "UNJUDGED" in out, out
    assert "every selected row's acceptance passes here." not in out, out


def test_the_summary_line_names_the_count_selected_and_the_reason_for_each(tmp_path):
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base)
    assert "5 row(s) in the plan, 5 marked done, 3 selected here" in got.stdout, got.stdout
    assert "q-contract — its Done-when text or DOD hash moved in the pushed range" in got.stdout
    assert "q-accept — its recorded acceptance command moved in the pushed range" in got.stdout
    assert "q-file — a file its acceptance command names changed in the pushed range" in got.stdout
    # neither untouched row names a reason, because neither was selected
    assert "q-ctrl —" not in got.stdout
    assert "q-core —" not in got.stdout


# ------------------------------------------------- the run names its mode, and the mode binds it
# Requirement 322 (INV-328): a run states which of four kinds it is BEFORE it selects a target,
# and fixes its composition to that kind's own. This script is the acceptance run itself — gate v
# of the release core — so it is where a mode and a composition are actually known: which rows the
# run may take, how many, and whether what it returns is a verdict at all. The record of
# 2026-09-08 (docs/prover/2026-09-08-four-named-modes-and-the-runner-that-never-arrived.md, F6/F8)
# found `guardrails/run_modes.py` with no caller outside its own test; these four are that caller's
# proof, each driving the real script rather than the reader beneath it.


def test_a_run_that_names_no_mode_is_refused_before_it_selects_anything(tmp_path):
    """M-661: an automatic run with no mode named is refused, rather than resolved to `row` and
    judged under a budget nobody asked for. Nothing runs: no sentinel appears."""
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base, mode=None)
    assert got.returncode == 1, got.stdout + got.stderr
    assert "named no mode" in got.stdout, got.stdout
    for name in ("row", "integration", "release", "manual"):
        assert name in got.stdout, got.stdout
    for name in ("ctrl", "contract", "accept", "file", "core"):
        assert not sentinel(tmp_path, name), "%s ran under a run that named no mode" % name


def test_a_row_run_is_refused_by_its_own_cap_when_more_than_one_row_is_affected(tmp_path):
    """M-661: the mode's fixed composition binds what the run may take. Three rows are affected
    here, and `row` admits one target — so the run is refused, naming the mode, the cap and the
    count, and it judges none of them."""
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base, mode="row")
    assert got.returncode == 1, got.stdout + got.stderr
    assert "row" in got.stdout and "1 target" in got.stdout and "3 were asked for" in got.stdout
    for name in ("contract", "accept", "file"):
        assert not sentinel(tmp_path, name), "%s ran past the mode's own cap" % name


def test_a_release_run_decides_the_verdict_and_a_manual_run_decides_none(tmp_path):
    """Criterion 8: a manual run never stands as a gate and decides no verdict. The same failing
    row reds the release run and is reported without a verdict by the manual one."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checks = tmp_path / "scripts" / "plan_checks.py"
    checks.write_text(_checks_text({**CHECKS_HEAD, "q-contract": "false"}), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "a row whose acceptance fails")

    red = run_rerun(tmp_path, plan, checkpoints, base, mode="release")
    assert red.returncode == 1, red.stdout
    assert "BLOCKED" in red.stdout, red.stdout

    audit = run_rerun(tmp_path, plan, checkpoints, base, mode="manual")
    assert audit.returncode == 0, audit.stdout
    assert "q-contract" in audit.stdout, audit.stdout
    assert "decides no verdict" in audit.stdout, audit.stdout


def test_the_gate_judges_no_program_name(tmp_path):
    """M-662: no registry of forbidden verifier commands, and criterion 13 — the name of the
    program carrying a check decides nothing. A key that names a test runner and a key that merely
    MENTIONS one in its text are both run like any other key.

    This one is a STANDING GUARD rather than a proof of the change beside it: it passes against the
    gate as it stood before, which is correct, because that gate judged no program name either. It
    exists because a program-name rule was written into this pack twice — deleted in 5ca8697c, and
    written again at the admission door on 2026-09-08 before a review caught it — and the row it
    answers, M-662, is the one that would have caught the second time and did not exist."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checks = tmp_path / "scripts" / "plan_checks.py"
    checks.write_text(_checks_text({
        **CHECKS_HEAD,
        # one names a test runner, one names none, one merely mentions the runner's name in text
        "q-contract": "python3 -m pytest --version >/dev/null && touch sentinel-contract.txt",
        "q-accept": "grep -q pytest scripts/plan_checks.py && touch sentinel-accept.txt",
    }), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "keys that name a runner and merely mention one")

    got = run_rerun(tmp_path, plan, checkpoints, base, mode="release")
    assert got.returncode == 0, got.stdout + got.stderr
    assert sentinel(tmp_path, "contract"), got.stdout
    assert sentinel(tmp_path, "accept"), got.stdout


def test_a_manual_run_may_not_stand_as_a_gate_in_ci(tmp_path):
    """Criterion 8's first half: a manual run never STANDS as a CI or release gate. `in_ci: false`
    sat in the config with no reader, so naming manual on a CI step turned this gate into a
    one-word green — the faults printed and the step passed (the adversarial read of 2026-09-08).
    In CI the run is refused outright; off CI the same mode is the audit it is meant to be."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checks = tmp_path / "scripts" / "plan_checks.py"
    checks.write_text(_checks_text({**CHECKS_HEAD, "q-contract": "false"}), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "a row whose acceptance fails")

    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base, LIVE_SPEC_RUN_MODE="manual",
               GITHUB_ACTIONS="true")
    env.pop("LIVE_SPEC_EVALUATING", None)
    env.pop("LIVE_SPEC_PUSH_FULL", None)
    in_ci = subprocess.run(
        [sys.executable, str(RERUN), "--plan", str(plan), "--checkpoints", str(checkpoints)],
        cwd=str(tmp_path), env=env, capture_output=True, text=True, timeout=60)
    assert in_ci.returncode == 1, in_ci.stdout
    assert "may never stand as a CI or release gate" in in_ci.stdout, in_ci.stdout
    assert "GITHUB_ACTIONS" in in_ci.stdout, in_ci.stdout


def test_an_integration_run_is_refused_until_its_targets_are_named(tmp_path):
    """Criterion 3 as it now reads: an integration run covers a composition somebody wrote down
    before it started, and no count stands in for that naming.

    Until 2026-09-08 this same run was admitted because three affected rows sat inside a cap of
    five — a figure borrowed from how many deliverables one plan holds, which said nothing about
    which targets a run covers. This tree's own contract names no integration targets, which is
    the state that key is meant to be in between changes, so the run is refused here and the
    refusal names the key to fill. Nothing runs: the sentinels stay untouched."""
    plan, checkpoints, base = build_fixture(tmp_path)
    got = run_rerun(tmp_path, plan, checkpoints, base, mode="integration")
    assert got.returncode == 1, got.stdout + got.stderr
    assert "'targets' names none" in got.stdout, got.stdout
    for name in ("contract", "accept", "file"):
        assert not sentinel(tmp_path, name), got.stdout


def test_an_unreadable_checkpoint_reds_its_row_instead_of_killing_the_run(tmp_path):
    """A selected row whose own checkpoint will not parse used to take the whole gate down with a
    traceback and no verdict at all — found 2026-09-08 when the gate's own fixture proof was
    called for the first time. Unknown admission is a fault on that row, never a pass and never a
    dead run."""
    plan, checkpoints, base = build_fixture(tmp_path)
    checkpoints.mkdir(parents=True, exist_ok=True)
    (checkpoints / "q-contract.md").write_text("# no metadata block at all\n", encoding="utf-8")
    got = run_rerun(tmp_path, plan, checkpoints, base, mode="release")
    assert got.returncode == 1, got.stdout + got.stderr
    assert "Traceback" not in got.stderr, got.stderr
    assert "its own checkpoint does not load" in got.stdout, got.stdout
    # the other selected rows still ran: one unreadable checkpoint reds its own row alone
    assert sentinel(tmp_path, "accept"), got.stdout


def test_a_row_run_takes_its_one_target_and_decides_on_it(tmp_path):
    """M-661 and criterion 12's row half: a targeted run is ADMITTED in a `row` run, rather than
    only refused past a cap. One affected row sits inside row's cap of one, so the run takes it,
    runs that row's own named command and decides the verdict on what it returned."""
    plan, checkpoints, base = build_fixture(tmp_path)
    # narrow the push to one affected row: only q-file's watched file moved
    plan.write_text(PLAN_BASE, encoding="utf-8")
    checks = tmp_path / "scripts" / "plan_checks.py"
    checks.write_text(_checks_text(CHECKS_BASE), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "put the contract and the key back")
    narrow_base = _git(tmp_path, "rev-parse", "HEAD").stdout.strip()
    (tmp_path / "watched-file.txt").write_text("moved again\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "one affected row")

    got = run_rerun(tmp_path, plan, checkpoints, narrow_base, mode="row")
    assert got.returncode == 0, got.stdout + got.stderr
    assert "1 selected here" in got.stdout, got.stdout
    assert "run mode: row — it decides the verdict below" in got.stdout, got.stdout
    assert sentinel(tmp_path, "file"), got.stdout
    assert not sentinel(tmp_path, "ctrl"), got.stdout


def _vendored_host(tmp_path, config):
    """A host as adopt/install-scaffold.sh leaves one: the gate and the run-mode reader vendored
    into its own guardrails/, reading that host's own config. The pack's copy reads the pack's
    config, so a host's shape can only be judged by running the host's own copy."""
    import shutil
    (tmp_path / "guardrails").mkdir(exist_ok=True)
    for name in ("check-acceptance-rerun.py", "run_modes.py"):
        shutil.copy2(Path(ROOT) / "guardrails" / name, tmp_path / "guardrails" / name)
    (tmp_path / "scripts" / "plan_checks_core.py").write_bytes(
        (Path(ROOT) / "scripts" / "plan_checks_core.py").read_bytes())
    (tmp_path / "scripts" / "checkpoint.py").write_bytes(
        (Path(ROOT) / "scripts" / "checkpoint.py").read_bytes())
    (tmp_path / "guardrails.config.json").write_text(json.dumps(config), encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "a host carrying its own copy of the gate")
    return tmp_path / "guardrails" / "check-acceptance-rerun.py"


def _run_host_gate(tmp_path, gate, plan, checkpoints, base_sha, mode="release"):
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base_sha, LIVE_SPEC_RUN_MODE=mode)
    for name in ("LIVE_SPEC_EVALUATING", "LIVE_SPEC_PUSH_FULL", "GITHUB_ACTIONS", "CI"):
        env.pop(name, None)
    return subprocess.run(
        [sys.executable, str(gate), "--plan", str(plan), "--checkpoints", str(checkpoints)],
        cwd=str(tmp_path), env=env, capture_output=True, text=True, timeout=60)


def test_a_host_whose_config_pre_dates_the_run_modes_key_is_refused_by_name(tmp_path):
    """A host that adopted the pack before `run_modes` existed carries a config without it — the
    installer's never-clobber promise means it is never added later. Every reader used to end in
    a bare KeyError traceback with no verdict at all (the adversarial read of 2026-09-08). It is
    a named refusal now, saying what the tree lacks and who writes it."""
    plan, checkpoints, base = build_fixture(tmp_path)
    gate = _vendored_host(tmp_path, {"some_other_key": {}})
    got = _run_host_gate(tmp_path, gate, plan, checkpoints, base)
    assert got.returncode == 1, got.stdout + got.stderr
    assert "Traceback" not in got.stderr, got.stderr
    assert 'no "run_modes" key' in got.stdout, got.stdout


def test_a_mode_the_host_config_does_not_carry_is_refused_by_name(tmp_path):
    """The partial shape the pack's own installer test plants: a host holding some of the four and
    not the rest. The run names one the config lacks, and says so instead of dying on it."""
    plan, checkpoints, base = build_fixture(tmp_path)
    gate = _vendored_host(tmp_path, {"run_modes": {"row": {"decides_verdict": True}}})
    got = _run_host_gate(tmp_path, gate, plan, checkpoints, base)
    assert got.returncode == 1, got.stdout + got.stderr
    assert "Traceback" not in got.stderr, got.stderr
    assert "nothing for 'release'" in got.stdout, got.stdout
