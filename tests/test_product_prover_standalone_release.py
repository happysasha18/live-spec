"""The public prover edition has a release identity, compact output, and its own CI floor."""

import json
import subprocess
from pathlib import Path

from conftest import ROOT


EDITION = Path(ROOT) / "editions" / "product-prover"
VALIDATOR = EDITION / "scripts" / "validate.py"


def run_validator():
    return subprocess.run(
        ["python3", str(VALIDATOR)],
        cwd=EDITION,
        text=True,
        capture_output=True,
        timeout=30,
    )


def test_the_real_standalone_package_validates():
    result = run_validator()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1.2.0-standalone" in result.stdout


def test_the_short_response_and_eval_rubric_hold_each_other():
    response = (EDITION / "examples" / "sample-response.md").read_text(encoding="utf-8")
    rubric = json.loads((EDITION / "evals" / "sample-spec-rubric.json").read_text())
    assert len(response.split()) <= rubric["acceptance"]["max_conversation_words"]
    assert rubric["acceptance"]["readiness"] in " ".join(response.split()).replace("**", "")
    top = response[response.index("## Top findings"):response.index("## Remaining finding index")]
    critical_terms = ("Expired", "Deposit", "authorization")
    assert sum(term in top for term in critical_terms) >= 2


def test_the_public_mirror_will_receive_its_own_workflow():
    workflow = EDITION / ".github" / "workflows" / "validate.yml"
    assert workflow.is_file()
    body = workflow.read_text(encoding="utf-8")
    assert "scripts/validate.py" in body
    assert "--base" not in body


def test_internal_and_public_copies_share_the_user_facing_contract():
    internal = (Path(ROOT) / "skills" / "product-prover" / "SKILL.md").read_text(encoding="utf-8")
    public = (EDITION / "SKILL.md").read_text(encoding="utf-8")
    for needle in (
        "under 1,500 words",
        "one-line index of every remaining finding",
        "read-only",
        "review-derived",
    ):
        assert needle in " ".join(internal.split())
        assert needle in " ".join(public.split())
