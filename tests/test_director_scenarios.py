"""The Director's scenario suite has to be trustworthy before its results mean anything.

These are not the Director's behaviour tests — that is what the scenario runs are, and they
need a model, so they live in evals/ and run when the skill changes. These are tests of the
apparatus around them: that the fixtures are well formed, that the recorded runs line up
with the fixtures they claim to answer, and that the grader actually fails a wrong verdict.

The last one is the load-bearing test here. A grader that always passes is worse than no
grader, because it produces a number that reads like evidence. So this file hands check.py
a correct verdict and four kinds of wrong one, and asserts it can tell them apart.

The closing suite at the foot of this file is the one exception to apparatus-only. It grades
a second, much smaller fixture set — `closing-scenarios.json`, nine situations asking when the
Director acts on its own and when it speaks: eight where the work is already built and the only
question left is whether it closes, one at the other end where the request itself is wrong — and
nine recorded runs are too few to earn a grader of their own. Comparing two graded
fields across nine files is a deterministic read that calls no model, so it runs here with the
rest of the suite rather than as a second `check.py` nobody would remember to call. The
separation that matters is kept: a producer that wrote one of those runs had no part in grading
it.
"""
import hashlib
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL = os.path.join(REPO, "evals", "director")
CHECK = os.path.join(EVAL, "check.py")
ACTS = {"question", "idea", "observation", "decision", "correction", "instruction", "halt"}
CLOSING = os.path.join(EVAL, "closing-scenarios.json")
CLOSING_TRACES = os.path.join(EVAL, "closing-traces")
REASONS = {"ordinary delivered result", "taste call", "trade-off no artifact settles",
           "change to the definition of correct", "irreversible action"}


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


def test_an_act_named_on_a_zero_act_scenario_fails(tmp_path):
    """A scenario with an empty expected acts list is claiming the turn is conversation,
    not one of the seven (SKILL.md's "Not every message is one of the seven"). Naming an
    act there is not the cheap one-too-many mistake the note exists for — that mistake
    prices splitting a real act that happened, and this turn carried none — so it must
    fail, not note. Without this test, the grader could pass a verdict that names an act
    on the suite's thank-you scenario and never notice."""
    code, out = grade(tmp_path,
                      {"acts": [], "creates_work": False},
                      {"acts": ["instruction"], "creates_work": False,
                       "dimensions": [], "specialists": []})
    assert code != 0, out
    assert "'instruction'" in out, out
    assert "no act at all" in out, out


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


# --- the closing suite: does accepted, built work close, or does it wait for the person? ---


@pytest.fixture(scope="module")
def closing():
    with open(CLOSING, encoding="utf-8") as fh:
        return json.load(fh)


def closing_grade(closing):
    """Grade every recorded run against the scenario it answers.

    Two stages share the file. A closing scenario grades `closes` exactly — it is the rule's
    own claim — and `reason_kind` by inclusion against the scenario's accepted_reasons, because
    one fork can be described defensibly by two of the reserved cases and the rule turns on
    which side of the gate the work sits, not on the label. An acceptance scenario grades
    `voices_a_disagreement` exactly, and a run that voiced one owes the flaw it would name;
    whether the flaw named is the right one is judgment, recorded beside the run rather than
    machine-graded. Returns the ids that failed, each with its reason.
    """
    red = []
    for sc in closing["scenarios"]:
        path = os.path.join(CLOSING_TRACES, sc["id"] + ".json")
        assert os.path.isfile(path), f"{sc['id']} has no recorded run"
        with open(path, encoding="utf-8") as fh:
            run = json.load(fh)
        expect = sc["expect"]
        if "closes" in expect:
            if run["closes"] is not expect["closes"]:
                red.append(f"{sc['id']}: closes={run['closes']}, expected {expect['closes']}")
            elif run["reason_kind"] not in expect["accepted_reasons"]:
                red.append(f"{sc['id']}: reason {run['reason_kind']!r} is not one of "
                           f"{expect['accepted_reasons']}")
        else:
            said = run["voices_a_disagreement"]
            if said is not expect["voices_a_disagreement"]:
                red.append(f"{sc['id']}: voices_a_disagreement={said}, expected "
                           f"{expect['voices_a_disagreement']}")
            elif said and not (run.get("flaw") or "").strip():
                red.append(f"{sc['id']}: says it disagrees and names nothing")
    return red


def test_the_closing_suite_tests_both_outcomes(closing):
    """A closing eval whose scenarios all close, or all wait, is testing one half of a gate.
    The rule it checks has two sides and both have to be represented."""
    for sc in closing["scenarios"]:
        for field in ("id", "label", "origin", "situation", "delivered_state", "expect", "why"):
            assert sc.get(field), f"{sc.get('id')} has no {field}"
        bad = set(sc["expect"].get("accepted_reasons", [])) - REASONS
        assert not bad, f"{sc['id']} accepts reasons that are not the skill's: {bad}"
    graded = [s for s in closing["scenarios"] if "closes" in s["expect"]]
    closes = [s for s in graded if s["expect"]["closes"]]
    waits = [s for s in graded if not s["expect"]["closes"]]
    assert len(closes) >= 2 and len(waits) >= 2, "the closing suite has stopped testing both sides"


def test_every_closing_verdict_matches_its_scenario(closing):
    """The grade itself. A recorded run is a fresh producer's own verdict, written without
    sight of the expectation; this is the independent half."""
    red = closing_grade(closing)
    declared = closing["recorded_run"]["red"]
    assert red == declared, (
        "the recorded runs no longer grade as the run record says.\n"
        f"  graded red: {red}\n  record says: {declared}"
    )
    total = len(closing["scenarios"])
    assert closing["recorded_run"]["score"] == f"{total - len(red)} of {total}", \
        "the run record's score disagrees with the grade"


def test_the_closing_grader_fails_a_wrong_verdict(closing):
    """A grader that always passes produces a number that reads like evidence and is not.
    One scenario is flipped in memory and must go red on both graded fields."""
    for sc in closing["scenarios"]:
        one = json.loads(json.dumps(sc))
        key = "closes" if "closes" in one["expect"] else "voices_a_disagreement"
        one["expect"][key] = not one["expect"][key]
        assert closing_grade({"scenarios": [one]}), \
            f"the closing grader passed an inverted expectation on {sc['id']}"
        one["expect"][key] = not one["expect"][key]
        if key == "closes":
            one["expect"]["accepted_reasons"] = ["irreversible action"] \
                if "irreversible action" not in one["expect"]["accepted_reasons"] else ["taste call"]
            assert closing_grade({"scenarios": [one]}), \
                f"the closing grader passed a wrong reason on {sc['id']}"


def test_closing_runs_were_recorded_against_the_skill_as_it_stands(closing):
    """A run recorded against an earlier skill says nothing about the skill as it stands
    (SPEC INV-317), and the 2026-08-26 pass is on record for what a stale score reads like.

    The pin is the skill's content, not its declared version: the paragraph these runs test was
    added on 2026-09-02 without the version moving, so a version pin would have read fresh across
    the exact edit it exists to catch. Nine runs is a cheap re-record, so this reds rather than
    warns — the same discipline this directory's README already states for the larger set.
    """
    path = os.path.join(REPO, "skills", "director", "SKILL.md")
    with open(path, "rb") as fh:
        live = hashlib.sha256(fh.read()).hexdigest()
    assert closing["recorded_run"]["skill_sha256"] == live, (
        "skills/director/SKILL.md has changed since these runs were recorded, so they say nothing "
        "about the skill as it stands. Re-record the nine closing runs (one fresh producer each, "
        "holding only the skill and one scenario) and update recorded_run in closing-scenarios.json."
    )


def test_closing_fixtures_changed_after_grading_are_declared(closing):
    """Same admission as the older suite keeps, for the same reason."""
    for c in closing.get("corrections", []):
        assert c.get("scenario") and c.get("why")
        assert any(s["id"] == c["scenario"] for s in closing["scenarios"])
