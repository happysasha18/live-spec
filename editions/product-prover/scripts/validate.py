#!/usr/bin/env python3
"""Validate the standalone product-prover package with only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+-standalone)\s*$", re.M)


def fail(message: str) -> None:
    raise AssertionError(message)


def read(relative: Path | str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def version_from(text: str, source: str) -> str:
    match = VERSION_RE.search(text)
    if not match:
        fail(f"{source} carries no semantic standalone version")
    return match.group(1)


def semantic_skill(text: str) -> str:
    """Drop the pack-version attribution that mirror sync generates after publication."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.startswith("made with [live-spec]")
    )


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def validate_package() -> str:
    skill = read("SKILL.md")
    lenses = read("reference/stress-lenses.md")
    readme = read("README.md")
    response = read("examples/sample-response.md")
    rubric = json.loads(read("evals/sample-spec-rubric.json"))

    version = version_from(skill, "SKILL.md")
    if version not in readme:
        fail("README.md and SKILL.md disagree on the standalone version")
    if rubric.get("edition") != version:
        fail("the sample rubric does not name the current standalone version")

    flat_skill = " ".join(skill.split())
    flat_lenses = " ".join(lenses.split())
    for needle in (
        "under 1,500 words",
        "read-only by default",
        "highest-impact findings",
        "one-line index of every remaining finding",
    ):
        if needle not in flat_skill:
            fail(f"SKILL.md lost the compact response contract: {needle}")

    if "derive a working surface inventory" not in flat_skill or "label it review-derived" not in flat_skill:
        fail("SKILL.md no longer derives a surface inventory when the registry is absent")
    if "missing maintained registry never turns" not in flat_lenses:
        fail("the policy sweep can silently become N/A when a registry is absent")

    for forbidden in ("SPEC INV-", "[INV-", "base rule "):
        if forbidden in skill or forbidden in lenses:
            fail(f"public runtime files leaked an internal rule code: {forbidden}")

    max_words = rubric["acceptance"]["max_conversation_words"]
    response_words = len(response.split())
    if response_words > max_words:
        fail(f"sample response has {response_words} words; budget is {max_words}")
    if len(rubric.get("critical_findings", [])) < 6:
        fail("sample rubric needs at least six critical finding classes")
    if len(rubric.get("must_not_claim", [])) < 2:
        fail("sample rubric needs negative controls against invented claims")

    workflow = read(".github/workflows/validate.yml")
    if "scripts/validate.py" not in workflow or "fetch-depth: 0" not in workflow:
        fail("standalone CI does not run this validator with history available")
    return version


def validate_version_bump(base: str) -> None:
    if not base or set(base) == {"0"}:
        return
    prefix_result = git("rev-parse", "--show-prefix")
    if prefix_result.returncode:
        fail(prefix_result.stderr.strip() or "cannot resolve git path prefix")
    prefix = prefix_result.stdout.strip()
    skill_path = f"{prefix}SKILL.md"
    reference_path = f"{prefix}reference"
    diff = git("diff", "--name-only", f"{base}..HEAD", "--", skill_path, reference_path)
    if diff.returncode:
        fail(diff.stderr.strip() or f"cannot compare runtime files with {base}")
    changed = set(diff.stdout.splitlines())
    if not changed:
        return

    old_skill = git("show", f"{base}:{skill_path}")
    if old_skill.returncode:
        return  # The edition did not exist at the comparison point.
    reference_changed = any(path.startswith(reference_path + "/") for path in changed)
    skill_changed = skill_path in changed and semantic_skill(old_skill.stdout) != semantic_skill(read("SKILL.md"))
    if not reference_changed and not skill_changed:
        return
    old_version = version_from(old_skill.stdout, f"{base}:SKILL.md")
    new_version = version_from(read("SKILL.md"), "SKILL.md")
    if old_version == new_version:
        fail(
            "SKILL.md or reference/stress-lenses.md changed without a standalone "
            f"version bump ({new_version})"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="git ref before this release")
    args = parser.parse_args()
    try:
        version = validate_package()
        if args.base:
            validate_version_bump(args.base)
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"product-prover standalone: FAIL — {exc}", file=sys.stderr)
        return 1
    print(f"product-prover standalone: OK — {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
