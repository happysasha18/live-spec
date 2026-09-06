"""A push that changes a skill reds until its skill-creator review is on record
(SPEC INV-208, ROADMAP 419).

Alexander asked for this on 2026-07-17 ~18:26: he leans on the session to remember to run
Anthropic's skill-creator review whenever a skill is modified, and the session forgets, so a
reminder does not hold — he wants a blocking gate. When a diff about to be pushed changes a
skill's body, the push reds unless a skill-creator review record for that change is committed.

The gate mirrors the shape of guardrails/check-prover-record.sh: it reads the push range
(LIVE_SPEC_DIFF_BASE / origin/main / HEAD~1), finds substantive changes under skills/, and
requires a fresh committed record under docs/skill-review/ that names each changed skill and
carries the review's verdict.

The one carve-out that must NOT red: a pure version-frontmatter stamp. scripts/stamp-versions.py
writes `  version: X.Y.Z` into every skill's frontmatter and the `live-spec-base (vX.Y.Z)`
base-reference at each version bump — that is a machine-stamped copy of one fact, not a change to
the skill's instructions, so it owes no skill-creator review.
"""
import os
import subprocess
import tempfile

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "check-skill-review.sh")
REVIEW_DIR = os.path.join(ROOT, "docs", "skill-review")


def _run(args, cwd=None, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, env=env)


# --- a scratch repo, so the behavioural proofs never depend on the real repo's HEAD ---

def _init_repo(tmp):
    _run(["git", "init", "-q"], cwd=tmp)
    _run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
    _run(["git", "config", "user.name", "a"], cwd=tmp)


def _write(tmp, relpath, content):
    path = os.path.join(tmp, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _commit_all(tmp, msg):
    _run(["git", "add", "-A"], cwd=tmp)
    _run(["git", "commit", "-q", "-m", msg], cwd=tmp)


def _head(tmp):
    return _run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()


SKILL_V1 = "---\nname: demo\nmetadata:\n  version: 1.0.0\n---\n\n# demo\n\nStep one: do the thing.\n"
# a body change (a new instruction line) — substantive
SKILL_BODY_CHANGED = (
    "---\nname: demo\nmetadata:\n  version: 1.0.0\n---\n\n# demo\n\nStep one: do the thing.\n"
    "Step two: do the other thing.\n"
)
# only the frontmatter version line moved (and the base reference) — the stamp diff, NOT substantive
SKILL_STAMP_ONLY = (
    "---\nname: demo\nmetadata:\n  version: 2.0.0\n---\n\n# demo\n\nStep one: do the thing.\n"
)
SKILL_V1_WITH_BASEREF = (
    "---\nname: demo\nmetadata:\n  version: 1.0.0\n---\n\n# demo (`live-spec-base` (v1.0.0))\n\n"
    "Step one: do the thing.\n"
)
SKILL_STAMP_ONLY_BASEREF = (
    "---\nname: demo\nmetadata:\n  version: 2.0.0\n---\n\n# demo (`live-spec-base` (v2.0.0))\n\n"
    "Step one: do the thing.\n"
)
# SKILL_V1's body, purely re-cased and re-spaced — no word added, removed, or reordered
SKILL_CASE_ONLY = (
    "---\nname: demo\nmetadata:\n  version: 1.0.0\n---\n\n# DEMO\n\nSTEP ONE:   do THE thing.\n"
)
# the same case/space change, but with a genuine new instruction line added alongside it
SKILL_CASE_PLUS_SUBSTANCE = (
    "---\nname: demo\nmetadata:\n  version: 1.0.0\n---\n\n# DEMO\n\nSTEP ONE:   do THE thing.\n"
    "Step two: do the other thing.\n"
)

RECORD = (
    "# Skill review — demo\n\nSKILL-REVIEW\n\nSkill: demo\n\n"
    "Reviewer: skill-creator (Anthropic)\n\nVerdict: passes — description and body reviewed.\n"
)

# RECORD plus the quoted-tool-output block a directly-matched covering record must now carry
# (q-817): a command line naming quick_validate.py against this skill, its printed stdout, and the
# "(exit N)" line closing it — the shape docs/skill-review/README.md states and
# docs/skill-review/2026-09-04-build-pipeline.md already uses.
RECORD_WITH_QUOTE = RECORD + (
    "\n## The tool's own verdict\n\n"
    "```\n$ python3 /opt/skill-creator/scripts/quick_validate.py skills/demo\n"
    "Skill is valid!\n(exit 0)\n```\n"
)

# Forces the tool-verification arm to stand down (q-817): a value that names no real file, so the
# gate never falls back to a machine default and the real ~/.claude is never consulted by a test.
NO_VALIDATOR_ENV = {"LIVE_SPEC_SKILL_VALIDATOR": "/nonexistent/quick_validate.py"}


# --- the gate ships ---

def test_review_dir_ships():
    assert os.path.isdir(REVIEW_DIR), "docs/skill-review/ home missing"


def test_template_ships():
    tmpl = os.path.join(ROOT, "templates", "skill-review.template.md")
    assert os.path.isfile(tmpl), "templates/skill-review.template.md missing"
    text = read("templates/skill-review.template.md")
    assert "SKILL-REVIEW" in text and "Verdict:" in text and "Skill:" in text


# --- behaviour: the three red-proofs the row names ---

def test_body_change_without_record_reds(self=None):
    """A skill BODY changed but no review record exists → the push reds."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "skill body changed, no review")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (skill review)" in r.stdout
        assert "demo" in r.stdout


def test_version_stamp_only_does_not_red():
    """A pure version-frontmatter stamp (and its base-reference) is not a substantive change,
    so it owes no skill-creator review — the gate passes even with no record."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_STAMP_ONLY)
        _commit_all(tmp, "version bump stamp only")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 0, r.stdout + r.stderr


def test_version_stamp_with_baseref_does_not_red():
    """The bump also rewrites the `live-spec-base (vX.Y.Z)` base reference; that line change is
    still a pure stamp and owes no review."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1_WITH_BASEREF)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_STAMP_ONLY_BASEREF)
        _commit_all(tmp, "version bump stamp + baseref")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 0, r.stdout + r.stderr


def test_case_only_change_does_not_red():
    """A skill body change that is only a change in letter case and/or whitespace — no word
    added, removed, or reordered — is not a substantive change either (the case-or-space
    carve-out): the gate passes even with no review record on file."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_CASE_ONLY)
        _commit_all(tmp, "case and whitespace change only")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 0, r.stdout + r.stderr


def test_case_change_with_real_edit_still_reds():
    """The boundary holds: a case/whitespace change riding ALONGSIDE a genuine new instruction
    line is a substantive change, and owes the review same as any other body change."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_CASE_PLUS_SUBSTANCE)
        _commit_all(tmp, "case change plus a real new instruction, no review")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (skill review)" in r.stdout
        assert "demo" in r.stdout


def test_body_change_with_matching_record_passes():
    """A substantive skill change WITH a committed, matching review record — one that also quotes
    the tool's own output (q-817) — passes quiet. The validator is forced absent here so the
    tool-verification arm stands down; that arm gets its own dedicated tests below."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD_WITH_QUOTE)
        _commit_all(tmp, "skill body changed + its review, same commit")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base, **NO_VALIDATOR_ENV})
        assert r.returncode == 0, r.stdout + r.stderr


def test_vendor_sync_of_previously_reviewed_content_needs_no_new_record():
    """THE BYTE-IDENTICAL CARVE-OUT (PLAN q-814, from tlvphotos' 2.7.0 -> 6.1.0 catch-up finding):
    a host's vendor sync (sync-skills.sh) can land content the pack already reviewed once, at an
    earlier commit in this repo's own history — the exact same bytes, at the exact same path,
    reintroduced verbatim by an unedited sync, not a fresh edit. Reproduced here: SKILL_V1 is
    reviewed, the skill then diverges (a hand-edit, unreviewed), and a sync restores SKILL_V1's
    exact bytes with no new record — the gate passes, since SKILL_V1's content was already
    reviewed. Confirmed red against the pre-carve-out gate (2026-09-03, same fixture, no such
    path existed): the push failed with no way to satisfy it short of a fresh, redundant record."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)
        _commit_all(tmp, "skill v1 + its review")
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "hand edit, diverged, no review")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "vendor sync restores the reviewed v1 content byte-for-byte")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 0, r.stdout + r.stderr
        assert "byte-" in r.stdout and "identical" in r.stdout


def test_hand_edit_to_never_reviewed_content_still_reds_with_carveout_present():
    """The carve-out's boundary (the regression guard the row demands): a hand-edit that lands
    content NEVER reviewed anywhere in this repo's history still demands a fresh record, even
    though the skill DOES carry an earlier review — for different content. The carve-out matches
    on exact byte content only, never on 'this skill was reviewed once, so anything goes'."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)
        _commit_all(tmp, "skill v1 + its review")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "hand edit to brand-new content, no review")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (skill review)" in r.stdout


def test_stale_record_does_not_cover_a_later_change():
    """A review committed BEFORE the last skill change is stale — it does not cover a change
    made after it, exactly as the prover-record gate refuses a record older than its spec."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)
        _commit_all(tmp, "skill v1 + its review")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "skill body changed again, review not refreshed")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (skill review)" in r.stdout


def test_an_earlier_stale_record_does_not_mask_a_later_change_when_a_fresher_one_also_exists():
    """Two records name the same skill: one committed before the skill's last change (and sorting
    first in `git ls-files`, since filenames are dated and sort lexically), one committed with —
    or after — that change. The gate must not stop at the first name+marker+verdict hit and call
    it fresh off some OTHER file's commit; it must find and accept the record that itself covers
    the change. Reproduces the live bug (2026-08-11 debts, finding 7 of
    docs/prover/2026-08-09-the-culling-first-day.md): two 'live-spec-base' records existed, the
    gate matched the older one, and an unrelated commit touching a third file under
    docs/skill-review/ made the whole directory read as fresh regardless."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)  # sorts first, but stale
        _commit_all(tmp, "skill v1 + an early review")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        # sorts later, covers the change, and carries the quoted-tool block the matched record
        # now owes (q-817) — the stale 2026-07-17 one above never needs it, since it is never matched.
        _write(tmp, "docs/skill-review/2026-08-09-demo.md", RECORD_WITH_QUOTE)
        _commit_all(tmp, "skill body changed again, with a fresh review this time")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base, **NO_VALIDATOR_ENV})
        assert r.returncode == 0, r.stdout + r.stderr
        assert "2026-08-09-demo.md" in r.stdout, r.stdout + r.stderr


def test_an_unrelated_fresher_record_does_not_launder_a_stale_match():
    """The mirror case: only a stale record names this skill, but a THIRD, unrelated file under
    docs/skill-review/ was committed after the skill's last change (for some other skill
    entirely). The gate must still red — the directory's newest commit is not a stand-in for
    this skill's own matched record being fresh."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)
        _commit_all(tmp, "skill v1 + its review")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "skill body changed again, review not refreshed")
        _write(tmp, "docs/skill-review/2026-08-10-other-skill.md",
               RECORD.replace("demo", "other-skill"))
        _commit_all(tmp, "an unrelated record, for a different skill, lands later")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (skill review)" in r.stdout


def test_a_sibling_records_prose_naming_this_skill_is_not_its_covering_record():
    """A record for one skill sometimes names ANOTHER skill in its own prose — citing a sibling
    review, comparing findings, and so on (docs/skill-review/2026-09-04-architect.md names
    "director" this way in this repo's real history, and the real gate matched it as director's
    own covering record). Matching the whole body for the changed skill's name, rather than its
    `Skill:` field, lets that prose mention stand in for a real review. The gate must still red
    on the changed skill with no record of its own, not silently accept the other skill's."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _write(tmp, "skills/other-skill/SKILL.md", SKILL_V1.replace("demo", "other-skill"))
        _commit_all(tmp, "both skills at v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "demo's body changed, no record of its own")
        # other-skill's own record lands AFTER demo's change (so it is fresh enough to pass the
        # gate's freshness check too) and, in its own prose, names demo in passing.
        _write(tmp, "docs/skill-review/2026-09-04-other-skill.md",
               RECORD.replace("Skill: demo", "Skill: other-skill")
               + "\nThe same disproportion the demo skill's own review already found.\n")
        _commit_all(tmp, "other-skill reviewed, its record mentions demo in passing")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr
        # The honest "nobody has reviewed it" message, not "has a covering record (...)" — the
        # latter would mean other-skill's record wrongly stood in for demo's own.
        assert "nobody has" in r.stdout, r.stdout + r.stderr
        assert "has a covering record" not in r.stdout, r.stdout + r.stderr


def test_record_must_be_committed_not_untracked():
    """A review record sitting untracked in the working tree does not count — it must be
    committed, mirroring the prover-record gate's tracked-file rule."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _commit_all(tmp, "skill body changed, no review committed")
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)  # written, never committed
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr


def test_no_skill_change_passes():
    """A push that touches no skill owes nothing — the gate stands down by name."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "PRODUCT_SPEC.md", "spec v1\n")
        _commit_all(tmp, "spec v1")
        base = _head(tmp)
        _write(tmp, "PRODUCT_SPEC.md", "spec v2 — a non-skill change\n")
        _commit_all(tmp, "spec v2")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 0, r.stdout + r.stderr


def test_record_missing_verdict_reds():
    """The record's minimal shape includes a Verdict line; a record naming the skill but
    carrying no verdict does not satisfy the gate."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md",
               "# Skill review — demo\n\nSKILL-REVIEW\n\nSkill: demo\n\n(no verdict yet)\n")
        _commit_all(tmp, "skill body changed + a record with no verdict")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base})
        assert r.returncode == 1, r.stdout + r.stderr


# --- the tool-verification arm (q-817): the gate runs quick_validate.py itself and compares its
# real verdict against what the covering record quotes, rather than trusting the quote on its own.

def _write_fixture_validator(tmp, stdout_line, exit_code):
    """A tiny stand-in for Anthropic's quick_validate.py: the gate always calls it as
    `python3 <path> skills/<name>` — one argument, the skill directory, which this fixture
    ignores — so the canned line and exit code the test wants are baked into the script's own
    source rather than read from argv. Lets a test control the 'real' verdict the gate sees
    without ever touching ~/.claude."""
    script = (
        "#!/usr/bin/env python3\n"
        f"print({stdout_line!r})\n"
        f"raise SystemExit({exit_code!r})\n"
    )
    path = _write(tmp, "fixture/quick_validate.py", script)
    os.chmod(path, 0o755)
    return path, stdout_line, exit_code


def _run_gate_with_validator(tmp, base, validator_path, extra_argv=()):
    args = [GATE] + list(extra_argv)
    return _run(args, cwd=tmp, extra_env={
        "LIVE_SPEC_DIFF_BASE": base,
        "LIVE_SPEC_SKILL_VALIDATOR": validator_path,
    })


def _quoted_record(stdout_line, exit_code):
    return RECORD + (
        "\n## The tool's own verdict\n\n"
        "```\n$ python3 /wherever/quick_validate.py skills/demo\n"
        f"{stdout_line}\n(exit {exit_code})\n```\n"
    )


def test_record_with_no_quoted_tool_output_reds():
    """A covering record that carries a marker, a Skill: line, and a Verdict:, but no quoted
    command-and-output block at all, still reds — the shape the record must carry now includes
    the quote (q-817), whether or not the validator is even on the machine."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD)  # no quote at all
        _commit_all(tmp, "skill body changed + a record with no quoted tool output")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base, **NO_VALIDATOR_ENV})
        assert r.returncode == 1, r.stdout + r.stderr
        assert "quotes no" in r.stdout, r.stdout + r.stderr


def test_quoted_verdict_disagreeing_with_the_validator_reds():
    """The record quotes a PASS, but the validator, run right now, disagrees — the gate reds and
    names both verdicts, rather than trusting the quote."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        record = _quoted_record("Skill is valid!", 0)  # quotes a pass
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", record)
        _commit_all(tmp, "skill body changed + a record quoting a pass")
        validator, _, _ = _write_fixture_validator(tmp, "not what was quoted", 0)
        r = _run_gate_with_validator(tmp, base, validator)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "disagrees" in r.stdout, r.stdout + r.stderr
        assert "Skill is valid!" in r.stdout and "not what was quoted" in r.stdout, r.stdout


def test_quoted_verdict_matching_the_validator_passes():
    """The record quotes exactly what the validator prints right now, at the exit code it
    returns — the gate runs the tool and passes quiet."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        record = _quoted_record("Skill is valid!", 0)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", record)
        _commit_all(tmp, "skill body changed + a record whose quote matches")
        validator, _, _ = _write_fixture_validator(tmp, "Skill is valid!", 0)
        r = _run_gate_with_validator(tmp, base, validator)
        assert r.returncode == 0, r.stdout + r.stderr


def test_validator_itself_failing_reds_even_if_the_record_quotes_it_honestly():
    """The record honestly quotes the validator's own failing verdict — a currently-invalid skill
    must never pass just because its record is honest about the failure."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        record = _quoted_record("Skill is invalid: missing frontmatter key", 1)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", record)
        _commit_all(tmp, "skill body changed + a record honestly quoting a fail")
        validator, _, _ = _write_fixture_validator(tmp, "Skill is invalid: missing frontmatter key", 1)
        r = _run_gate_with_validator(tmp, base, validator)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "fails Anthropic's own quick_validate.py" in r.stdout, r.stdout + r.stderr


def test_validator_missing_from_the_machine_stands_down_and_record_checks_still_run():
    """No validator resolves anywhere (the override names a file that does not exist) — the gate
    stands down on the tool-verification arm alone, naming what it looked for, and the record's
    other checks (which a record carrying the quoted block still satisfies) still decide the
    outcome: green here, since nothing else is wrong with the record."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_V1)
        _commit_all(tmp, "skill v1")
        base = _head(tmp)
        _write(tmp, "skills/demo/SKILL.md", SKILL_BODY_CHANGED)
        _write(tmp, "docs/skill-review/2026-07-17-demo.md", RECORD_WITH_QUOTE)
        _commit_all(tmp, "skill body changed + a complete record, validator absent")
        r = _run([GATE], cwd=tmp, extra_env={"LIVE_SPEC_DIFF_BASE": base, **NO_VALIDATOR_ENV})
        assert r.returncode == 0, r.stdout + r.stderr
        assert "standing down" in r.stdout, r.stdout + r.stderr


# --- wired into the push chain, both nets ---

def test_gate_wired_into_pre_push():
    assert "check-skill-review.sh" in read("guardrails/pre-push"), \
        "pre-push does not wire the skill-review gate"


def test_gate_mirrored_in_ci():
    assert "check-skill-review.sh" in read(".github/workflows/gates.yml"), \
        "the CI mirror does not run the skill-review gate"


# --- traceability across the four documents ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-208]" in spec
    # The requirements-format spec states the law behaviourally; the concrete gate script and record
    # directory consolidated into ARCHITECTURE.md's guardrails node (one-home-per-fact).
    assert "require a committed review naming the skill" in " ".join(spec.split())
    arch = read("ARCHITECTURE.md")
    assert "check-skill-review.sh" in arch
    assert "docs/skill-review" in arch


def test_formal_index_row():
    assert "| INV-208 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-208" in arch
    assert "check-skill-review.sh" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "M-389" in matrix
    assert "INV-208" in matrix


def test_build_pipeline_names_the_skill_review_step():
    """The pipeline's own step list names the skill-creator review by its gate, not just its
    mechanism (gap found 2026-08-19): a reader walking the pipeline's steps met the check
    nowhere on that list, only in the separate guardrails machinery. Since the build-pipeline
    cutover this fact's home is director's landing-law reference, pointed to from SKILL.md's
    Execution section, so a reader following director's own walk still meets the gate named
    beside its INV-208 anchor."""
    landing_law = read("skills/build-pipeline/references/landing-law.md")
    assert "check-skill-review.sh" in landing_law
    assert "SPEC INV-208" in landing_law


def test_publish_kind_checklist_names_the_skill_review():
    """The publish skill's kind checklist owes the same naming for kind = skill (2026-08-19)."""
    publish = read("skills/publish/SKILL.md")
    assert "| skill |" in publish
    skill_row = next(l for l in publish.splitlines() if l.startswith("| skill |"))
    assert "SPEC INV-208" in skill_row
