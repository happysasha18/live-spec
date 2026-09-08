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


def run_rerun(tmp_path, plan, checkpoints, base_sha):
    env = dict(os.environ, LIVE_SPEC_DIFF_BASE=base_sha)
    env.pop("LIVE_SPEC_EVALUATING", None)
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
        str(plan), str(checkpoints), 1)

    assert any(line.startswith("q-contract: ") for line in unjudged), unjudged
    assert not any("q-contract" in line for line in faults), faults
    assert not faults, "a stopped command must never turn the gate red on its own: %r" % faults


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
