"""The front door has three owners: Director reads, pipeline executes, PLAN holds tasks."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_director_stops_at_a_route_and_pipeline_owns_execution():
    director = read("skills/director/SKILL.md")
    pipeline = read("skills/build-pipeline/SKILL.md")
    execution = read("skills/build-pipeline/references/accepted-work-execution.md")

    assert "## Route contract" in director
    assert "## Execution" not in director
    assert "scripts/checkpoint.py" not in director

    assert "## Accepted-work pipeline" in pipeline
    assert "scripts/checkpoint.py" in execution
    assert "## Execution" in execution


def test_a_quiet_turn_loads_no_pipeline():
    """A question, musing or conversation is answered where it is read, not routed onward."""
    director = read("skills/director/SKILL.md")
    assert "A question, musing or conversation is answered without loading a pipeline." in director


def test_next_steps_is_not_a_second_task_surface():
    plan = read("PLAN.md")
    assert "`NEXT_STEPS.md` is not an exception" in plan

    for path in ("NEXT_STEPS.md", "templates/NEXT_STEPS.template.md"):
        text = read(path)
        assert not re.search(r"^##\s+(?:Tasks|Forward queue)\b", text, re.MULTILINE), path
        assert not re.search(r"\b(?:q|plan)-\d+\b", text), path
        assert "one terse line per open leg" not in text, path


def test_resume_state_points_to_the_board_instead_of_repeating_it():
    for path in ("NEXT_STEPS.md", "templates/NEXT_STEPS.template.md"):
        text = read(path)
        assert "PLAN.md" in text, path
        assert "transient execution state" in text.lower(), path
