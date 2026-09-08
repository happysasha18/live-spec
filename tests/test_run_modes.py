"""The run-mode contract (SPEC rule 43): a budget's composition is named in advance and
finite, and a runtime timeout never settles a verdict. Proves guardrails/run_modes.py's
resolution order and the four modes' own composition in guardrails.config.json."""

import json
import os

import pytest

from conftest import ROOT
from pathlib import Path as _Path

ROOT_PATH = _Path(ROOT)

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


# ------------------------------------------------- the pack's own law about composition
# The adversarial read of 2026-09-08: `admit_targets` refused only where the config named a
# `max_targets`, and `adopt/install-scaffold.sh` seeds `row` and `integration` with none — so on
# every host the pack installs, a `row` run admitted forty targets without a word. Criterion 2
# pins a row run to one target and criterion 3 pins an integration run to five, and both are the
# pack's law rather than a host's budget (criterion 20).


def test_a_mode_carrying_no_cap_falls_to_the_packs_own_law():
    seeded = {
        "row": {"decides_verdict": True},
        "integration": {"decides_verdict": True, "layer_map": {}},
        "release": {"decides_verdict": True},
        "manual": {"in_ci": False, "decides_verdict": False},
    }
    with pytest.raises(run_modes.ModeCapExceeded) as exc:
        run_modes.admit_targets("row", ["a", "b"], run_modes=seeded)
    assert "row" in str(exc.value) and "1 target" in str(exc.value)
    with pytest.raises(run_modes.ModeCapExceeded):
        run_modes.admit_targets("integration", list("abcdef"), run_modes=seeded)
    # the two that carry no law here take what they are given: a release run's composition is its
    # own versioned core list, and a manual run decides no verdict at all
    assert len(run_modes.admit_targets("release", list("abcdefghij"), run_modes=seeded)) == 10
    assert len(run_modes.admit_targets("manual", list("abcdefghij"), run_modes=seeded)) == 10


def test_the_host_seed_carries_the_two_caps_the_law_names():
    """The seed adopt/install-scaffold.sh writes into a host names both caps outright, so a
    host reading its own config sees what it runs under."""
    text = (ROOT_PATH / "adopt" / "install-scaffold.sh").read_text(encoding="utf-8")
    seed = text[text.index('cfg["run_modes"] = {'):text.index('"manual": {')]
    assert '"max_targets": 1' in seed
    assert '"max_targets": 5' in seed


def test_named_mode_answers_none_where_nothing_named_one():
    assert run_modes.named_mode(env={}) is None
    # an empty string names nothing, and used to take the "a mode was named" branch
    assert run_modes.named_mode(env={"LIVE_SPEC_RUN_MODE": ""}) is None
    # pre-push treats its own switch as set-or-not, so anything set names release
    assert run_modes.named_mode(env={"LIVE_SPEC_PUSH_FULL": "yes"}) == "release"
    assert run_modes.named_mode(env={"LIVE_SPEC_RUN_MODE": "manual"}) == "manual"
    assert run_modes.resolve_mode(env={}) == "row"


def test_only_manual_is_barred_from_standing_as_a_gate():
    assert run_modes.stands_as_a_gate("manual") is False
    for name in ("row", "integration", "release"):
        assert run_modes.stands_as_a_gate(name) is True


# ------------------------------------------------- the release core is the CI chain, kept in step
# Criterion 5 and M-659: a release run covers a FIXED, VERSIONED list of core gates. The list in
# guardrails.config.json was 23 letters copied out of .github/workflows/gates.yml with nothing
# holding the two together (the adversarial read of 2026-09-08, F7): a gate added, dropped or
# renamed in CI left this file green, and a release core that has quietly stopped naming a gate
# still reads as a fixed versioned list. The owner's own reading of it, 2026-09-08 21:08: a row
# promising a fixed composition stays open until the composition is proved finite and the same.


def _ci_gate_letters():
    """Every gate letter the CI chain actually runs, read off its own step names. Two shapes
    appear there: `gate x — …` and `… (gate b, full — …)`."""
    import re
    text = (ROOT_PATH / ".github" / "workflows" / "gates.yml").read_text(encoding="utf-8")
    # Step NAMES only. Read across the whole file, the word "gate" inside a comment's prose
    # ("the gate falls back to origin/main") reads as a gate letter and the check turns noisy.
    names = re.findall(r'^\s*-?\s*name:\s*"([^"]+)"', text, re.M)
    letters = set()
    for name in names:
        letters.update(re.findall(r"gate ([a-z]+)[ ,]", name))
    return letters


def test_the_release_core_names_exactly_the_gates_ci_runs():
    core = set(_config()["release"]["core"])
    ci = _ci_gate_letters()
    assert core - ci == set(), "named in the release core and run by no CI step: %s" % sorted(core - ci)
    assert ci - core == set(), "run by CI and absent from the release core: %s" % sorted(ci - core)


def test_the_release_cores_version_is_the_packs_own():
    version = (ROOT_PATH / "VERSION").read_text(encoding="utf-8").strip()
    assert _config()["release"]["core_version"] == version
