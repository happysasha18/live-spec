"""The run-mode contract (SPEC rule 43): a budget's composition is named in advance and
finite, and a runtime timeout never settles a verdict. Proves guardrails/run_modes.py's
resolution order and the four modes' own composition in guardrails.config.json."""

import json
import os

import pytest

from conftest import ROOT

import run_modes  # noqa: E402 — guardrails/ is on sys.path via conftest


def _config():
    with open(os.path.join(ROOT, "guardrails.config.json"), encoding="utf-8") as f:
        return json.load(f)["run_modes"]


def test_the_four_names_are_exactly_the_four():
    assert run_modes.MODES == ("row", "integration", "release", "manual")
    assert set(_config().keys()) >= set(run_modes.MODES)


def test_run_modes_holds_the_four_modes_and_nothing_else():
    assert set(_config().keys()) == {"row", "integration", "release", "manual"}


def test_an_unknown_mode_name_is_refused_naming_the_four():
    with pytest.raises(ValueError) as exc:
        run_modes.resolve_mode(env={"LIVE_SPEC_RUN_MODE": "nightly"})
    message = str(exc.value)
    assert "nightly" in message
    for name in run_modes.MODES:
        assert name in message


def test_push_full_with_no_run_mode_resolves_to_release():
    assert run_modes.resolve_mode(env={"LIVE_SPEC_PUSH_FULL": "1"}) == "release"


def test_neither_set_resolves_to_row():
    assert run_modes.resolve_mode(env={}) == "row"


def test_row_admits_one_target_and_refuses_two_naming_the_cap():
    assert run_modes.admit_targets("row", ["scripts/plan_checks.py::q-1"]) == [
        "scripts/plan_checks.py::q-1"
    ]
    with pytest.raises(ValueError) as exc:
        run_modes.admit_targets("row", ["target-a", "target-b"])
    message = str(exc.value)
    assert "row" in message
    assert "1" in message
    assert "2" in message


def test_integration_refuses_a_sixth_named_target():
    run_modes.admit_targets("integration", ["t1", "t2", "t3", "t4", "t5"])
    with pytest.raises(ValueError) as exc:
        run_modes.admit_targets("integration", ["t1", "t2", "t3", "t4", "t5", "t6"])
    message = str(exc.value)
    assert "integration" in message
    assert "5" in message
    assert "6" in message


def test_manual_decides_no_verdict_release_and_row_do():
    assert run_modes.decides_verdict("manual") is False
    assert run_modes.decides_verdict("release") is True
    assert run_modes.decides_verdict("row") is True


def test_every_mode_ships_emergency_timeout_seconds_as_null():
    config = _config()
    for name in run_modes.MODES:
        assert config[name]["emergency_timeout_seconds"] is None
        assert config[name]["timeout_is_never_a_verdict"] is True


def test_release_core_list_is_non_empty_and_never_grows_with_named_things():
    release = _config()["release"]
    assert len(release["core"]) > 0
    for word in ("samples", "seeds", "roles", "combinations"):
        assert any(word in item for item in release["never_grows_with"])
