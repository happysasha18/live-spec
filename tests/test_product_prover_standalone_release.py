"""The public prover edition has a release identity, compact output, and its own CI floor."""

import json
import shutil
import subprocess
from pathlib import Path

from conftest import ROOT


EDITION = Path(ROOT) / "editions" / "product-prover"
VALIDATOR = EDITION / "scripts" / "validate.py"


def run_validator(*args, cwd=EDITION):
    return subprocess.run(
        ["python3", str(VALIDATOR), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=30,
    )


def git(cwd, *args):
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, timeout=30,
        env={
            "PATH": __import__("os").environ["PATH"],
            "GIT_AUTHOR_NAME": "test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        },
    )


def test_the_real_standalone_package_validates():
    result = run_validator()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1.1.0-standalone" in result.stdout


def test_the_short_response_and_eval_rubric_hold_each_other():
    response = (EDITION / "examples" / "sample-response.md").read_text(encoding="utf-8")
    rubric = json.loads((EDITION / "evals" / "sample-spec-rubric.json").read_text())
    assert len(response.split()) <= rubric["acceptance"]["max_conversation_words"]
    assert rubric["acceptance"]["readiness"] in " ".join(response.split()).replace("**", "")
    top = response[response.index("## Top findings"):response.index("## Remaining finding index")]
    critical_terms = ("Expired", "Deposit", "authorization")
    assert sum(term in top for term in critical_terms) >= 2


def test_runtime_change_without_version_bump_is_refused(tmp_path):
    package = tmp_path / "product-prover"
    shutil.copytree(EDITION, package)
    assert git(package, "init", "-q").returncode == 0
    assert git(package, "add", ".").returncode == 0
    assert git(package, "commit", "-q", "-m", "baseline").returncode == 0
    baseline = git(package, "rev-parse", "HEAD").stdout.strip()

    skill = package / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\nA runtime change.\n", encoding="utf-8")
    assert git(package, "add", "SKILL.md").returncode == 0
    assert git(package, "commit", "-q", "-m", "runtime change").returncode == 0

    validator = package / "scripts" / "validate.py"
    result = subprocess.run(
        ["python3", str(validator), "--base", baseline],
        cwd=package,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "without a standalone version bump" in result.stderr


def test_generated_pack_attribution_does_not_demand_an_edition_bump(tmp_path):
    package = tmp_path / "product-prover"
    shutil.copytree(EDITION, package)
    assert git(package, "init", "-q").returncode == 0
    skill = package / "SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8") + "\nmade with [live-spec](https://example.test) v4.3.0\n",
        encoding="utf-8",
    )
    assert git(package, "add", ".").returncode == 0
    assert git(package, "commit", "-q", "-m", "baseline").returncode == 0
    baseline = git(package, "rev-parse", "HEAD").stdout.strip()
    skill.write_text(
        skill.read_text(encoding="utf-8").replace("v4.3.0", "v4.4.0"), encoding="utf-8"
    )
    assert git(package, "add", "SKILL.md").returncode == 0
    assert git(package, "commit", "-q", "-m", "generated attribution").returncode == 0

    validator = package / "scripts" / "validate.py"
    result = subprocess.run(
        ["python3", str(validator), "--base", baseline],
        cwd=package,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_public_mirror_will_receive_its_own_workflow():
    workflow = EDITION / ".github" / "workflows" / "validate.yml"
    assert workflow.is_file()
    body = workflow.read_text(encoding="utf-8")
    assert "fetch-depth: 0" in body
    assert "scripts/validate.py --base" in body


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
