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


def test_integration_refuses_a_target_this_tree_never_named():
    """This tree's own contract carries an empty `targets` list, so every integration run here is
    refused until somebody writes down what the run covers. That is the state the key is meant to
    be in between changes: named before the run, empty otherwise."""
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("integration", ["t1"])
    message = str(exc.value)
    assert "integration" in message
    assert "targets" in message


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
# `max_targets`, and `adopt/install-scaffold.sh` seeds `row` with none — so on every host the pack
# installs, a `row` run admitted forty targets without a word. Criterion 2 pins a row run to one
# target, and that is the pack's law rather than a host's budget (criterion 20).
#
# The same day the second figure came out. `integration` had carried "at most five", borrowed from
# `MOST_DELIVERABLES` — a figure about how many deliverables one plan holds. A count admitted any
# five targets and refused a sixth for no stateable reason, so criterion 3 now names a composition
# recorded before the run, and the other two modes read the same way (owner's word, 2026-09-08).


def test_a_row_run_carrying_no_cap_falls_to_the_packs_own_law():
    seeded = {"row": {"decides_verdict": True}}
    with pytest.raises(run_modes.ModeCapExceeded) as exc:
        run_modes.admit_targets("row", ["a", "b"], run_modes=seeded)
    assert "row" in str(exc.value) and "1 target" in str(exc.value)
    assert run_modes.admit_targets("row", ["a"], run_modes=seeded) == ["a"]


def test_no_mode_but_row_is_judged_by_a_number():
    """The whole of the pack's numeric law, read out of the module: one entry, and it is `row`."""
    assert run_modes.MODE_LAW == {"row": 1}


def test_an_integration_run_needs_its_targets_named_before_it_starts():
    seeded = {"integration": {"decides_verdict": True, "layer_map": {}}}
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("integration", list("abcdef"), run_modes=seeded)
    assert "written down before it started" in str(exc.value)

    named = {"integration": {"targets": ["tests/test_a.py", "tests/test_b.py"]}}
    assert run_modes.admit_targets("integration", ["tests/test_a.py"], run_modes=named) == [
        "tests/test_a.py"]
    # a named composition admits six as readily as two: the naming is the law, never the count
    six = {"integration": {"targets": list("abcdef")}}
    assert len(run_modes.admit_targets("integration", list("abcdef"), run_modes=six)) == 6
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("integration", ["tests/test_c.py"], run_modes=named)
    assert "does not name" in str(exc.value)


def test_a_release_run_needs_a_versioned_core():
    with pytest.raises(run_modes.ModeCompositionUnnamed):
        run_modes.admit_targets("release", ["b"], run_modes={"release": {"decides_verdict": True}})
    unversioned = {"release": {"core": ["b", "a"]}}
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("release", ["b"], run_modes=unversioned)
    assert "core_version" in str(exc.value)
    versioned = {"release": {"core": ["b", "a"], "core_version": "6.1.1"}}
    assert run_modes.admit_targets("release", ["b", "a"], run_modes=versioned) == ["b", "a"]


def test_a_manual_run_needs_a_purpose_and_a_finite_sample():
    bare = {"manual": {"in_ci": False, "decides_verdict": False}}
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("manual", list("abc"), run_modes=bare)
    assert "purpose" in str(exc.value)
    endless = {"manual": {"records_before_start": ["purpose", "limit"],
                          "purpose": "read the new page by hand", "limit": "as many as it takes"}}
    with pytest.raises(run_modes.ModeCompositionUnnamed) as exc:
        run_modes.admit_targets("manual", list("abc"), run_modes=endless)
    assert "nobody can count" in str(exc.value)
    recorded = {"manual": {"records_before_start": ["purpose", "limit"],
                           "purpose": "read the new page by hand", "limit": 3}}
    assert len(run_modes.admit_targets("manual", list("abc"), run_modes=recorded)) == 3


def test_the_host_seed_carries_the_one_cap_the_law_names_and_no_other():
    """The seed adopt/install-scaffold.sh writes into a host names the row cap outright, and gives
    every other mode an empty composition for the host to fill — so a host reading its own config
    sees what it runs under, and an unfilled mode refuses rather than admitting a count."""
    text = (ROOT_PATH / "adopt" / "install-scaffold.sh").read_text(encoding="utf-8")
    seed = text[text.index('cfg["run_modes"] = {'):text.index('with open(cfg_path, "w"')]
    assert '"max_targets": 1' in seed
    assert '"max_targets": 5' not in seed
    assert '"targets": []' in seed
    assert '"core": []' in seed
    assert '"records_before_start": ["purpose", "limit"]' in seed


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
