"""The Director's scenario suite has to be trustworthy before its results mean anything.

These are not the Director's behaviour tests — that is what the scenario runs are, and they
need a model, so they live in evals/ and run when the skill changes. These are tests of the
apparatus around them: that the fixtures are well formed, that the recorded runs line up
with the fixtures they claim to answer, and that the grader actually fails a wrong verdict.

The last one is the load-bearing test here. A grader that always passes is worse than no
grader, because it produces a number that reads like evidence. So this file hands check.py
a correct verdict and four kinds of wrong one, and asserts it can tell them apart.
"""
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL = os.path.join(REPO, "evals", "director")
CHECK = os.path.join(EVAL, "check.py")
ACTS = {"question", "idea", "observation", "decision", "correction", "instruction", "halt"}


@pytest.fixture(scope="module")
def book():
    with open(os.path.join(EVAL, "scenarios.json"), encoding="utf-8") as fh:
        return json.load(fh)


def grade(tmp_path, expect, actual):
    """Run the grader on one made-up pair and return (exit code, output)."""
    s = tmp_path / "s.json"
    a = tmp_path / "a.json"
    s.write_text(json.dumps({"id": "t", "expect": expect}), encoding="utf-8")
    a.write_text(json.dumps(actual), encoding="utf-8")
    p = subprocess.run([sys.executable, CHECK, "--scenario", str(s), "--actual", str(a)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def test_every_scenario_is_well_formed(book):
    seen = set()
    for sc in book["scenarios"]:
        for field in ("id", "origin", "situation", "message", "expect", "why"):
            assert sc.get(field), f"{sc.get('id')} has no {field}"
        assert sc["id"] not in seen, f"duplicate scenario id {sc['id']}"
        seen.add(sc["id"])
        bad = set(sc["expect"]["acts"]) - ACTS
        assert not bad, f"{sc['id']} expects things that are not speech acts: {bad}"


def test_most_scenarios_expect_no_work(book):
    """The design's whole claim is that most messages are not work. If the suite ever drifts
    to mostly-work fixtures, it has stopped testing the claim."""
    quiet = [s for s in book["scenarios"] if not s["expect"].get("creates_work")]
    assert len(quiet) > len(book["scenarios"]) / 2


def test_the_corpus_is_mostly_real(book):
    """Made-up messages are tidier than real ones in exactly the way that hides the defect."""
    real = [s for s in book["scenarios"] if s["origin"].startswith("real")]
    assert len(real) >= len(book["scenarios"]) * 0.8


def test_every_trace_answers_a_scenario(book):
    ids = {s["id"] for s in book["scenarios"]}
    traces = os.path.join(EVAL, "traces")
    for name in os.listdir(traces):
        if not name.endswith(".json"):
            continue
        assert name[:-5] in ids, f"trace {name} answers no scenario"
        with open(os.path.join(traces, name), encoding="utf-8") as fh:
            v = json.load(fh)
        assert set(v.get("acts") or []) <= ACTS, f"{name} records things that are not acts"


def test_a_correct_verdict_passes(tmp_path):
    code, out = grade(tmp_path, {"acts": ["question"], "creates_work": False},
                      {"acts": ["question"], "creates_work": False,
                       "dimensions": [], "specialists": []})
    assert code == 0, out


@pytest.mark.parametrize("actual,expected_words", [
    ({"acts": ["instruction"], "creates_work": False}, "acts"),
    ({"acts": ["question"], "creates_work": True}, "creates_work"),
    ({"acts": ["question"], "creates_work": False, "dimensions": ["quality, safety, regressions"]},
     "never accepted"),
    ({"acts": ["not-a-real-act"], "creates_work": False}, "not speech acts"),
])
def test_the_grader_fails_a_wrong_verdict(tmp_path, actual, expected_words):
    """Four ways to be wrong. A grader that passes any of them is producing a number that
    looks like evidence and is not."""
    code, out = grade(tmp_path, {"acts": ["question"], "creates_work": False}, actual)
    assert code != 0, f"the grader passed a wrong verdict: {actual}"
    assert expected_words in out, out


def test_one_act_too_many_is_reported_and_does_not_fail(tmp_path):
    """The skill states the cost itself: naming one act too many costs a sentence, naming
    one too few loses what somebody said. The grader used to charge both the same, which
    reddened scenarios whose every material field was right."""
    code, out = grade(tmp_path,
                      {"acts": ["question"], "creates_work": False},
                      {"acts": ["question", "observation"], "creates_work": False,
                       "dimensions": [], "specialists": []})
    assert code == 0, out
    assert "extra act" in out, out
    assert "'observation'" in out, out


def test_one_act_too_few_still_fails_even_beside_an_extra_one(tmp_path):
    """The cheap half is only cheap on its own. A run that loses an act the person made
    is red whatever else it named."""
    code, out = grade(tmp_path,
                      {"acts": ["question", "idea"], "creates_work": False},
                      {"acts": ["question", "observation"], "creates_work": False,
                       "dimensions": [], "specialists": []})
    assert code != 0, out
    assert "idea" in out, out


def test_a_wrong_material_field_still_fails_beside_an_extra_act(tmp_path):
    """An extra act carries nothing across to the booleans: they are graded exactly."""
    code, out = grade(tmp_path,
                      {"acts": ["question"], "creates_work": False},
                      {"acts": ["question", "observation"], "creates_work": True,
                       "work_items": 1, "dimensions": [], "specialists": []})
    assert code != 0, out
    assert "creates_work" in out, out


def test_a_correction_may_name_what_the_running_work_touches(tmp_path):
    """The grader used to forbid any routing when no new work was created, which was wrong:
    a correction creates nothing and still changes work whose dimensions are worth naming."""
    code, out = grade(tmp_path,
                      {"acts": ["correction"], "creates_work": False,
                       "attaches_to_existing_work": True},
                      {"acts": ["correction"], "creates_work": False,
                       "attaches_to_existing_work": True,
                       "dimensions": ["product value and behaviour"], "specialists": ["Developer"]})
    assert code == 0, out


def test_fixtures_changed_after_grading_are_declared(book):
    """A fixture edited after it graded a run is worth less than one written blind. The suite
    keeps that admission next to the fixtures rather than in a commit message nobody reads."""
    for c in book.get("corrections", []):
        assert c.get("scenario") and c.get("why")
        assert any(s["id"] == c["scenario"] for s in book["scenarios"])
