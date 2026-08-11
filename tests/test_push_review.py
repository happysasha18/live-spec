"""A push reds until the one record it carries reads the delta it sends (SPEC INV-304).

Twice in two days an adversarial review of a whole change was run before a push, each time
because the owner asked for it in that moment. Both times it found real defects the suite
missed: on 2026-08-04 it found four red push gates and one measurement error in the session's
own work. The practice lived nowhere — no requirement named it, no gate demanded it — so the
next session pushes without one and nothing notices.

The duty it earned was first written as a second review record with a second gate over a second
home. One push then owed two records for one and the same change. The two are one pass, so they
are one record: the dated record under docs/prover/ that a push already owed carries the
adversarial read as well, and guardrails/check-prover-record.sh holds it on the push road. It
reads the push range (LIVE_SPEC_DIFF_BASE / origin/main / HEAD~1), takes the commits in that
range that touch a file outside docs/prover/, and requires the committed record to name the base
commit and every one of them, to be at least as new as the newest of them, and to carry its
fields.

What the tests below hold is the mechanical half: a record exists, is committed, is fresh, names
the pushed range, and carries its fields with values. Whether the review was adversarial is the
reviewer's own, and no test here claims otherwise.

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest tests/test_push_review.py -q
"""
import json
import os
import re
import subprocess
import tempfile

from conftest import ROOT, read, read_flat

GATE = os.path.join(ROOT, "guardrails", "check-prover-record.sh")
RECORD_DIR = os.path.join(ROOT, "docs", "prover")

# The fixtures date their records, so the gate is called for that same day rather than today's.
FIXTURE_DAY = "2026-08-05"
PUSH_ROAD = ["--push", "docs/prover", FIXTURE_DAY]


def _run(args, cwd=None, extra_env=None):
    env = dict(os.environ)
    env.pop("LIVE_SPEC_DIFF_BASE", None)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, env=env)


def _gate(tmp, base=None):
    extra = {"LIVE_SPEC_DIFF_BASE": base} if base else None
    return _run([GATE] + PUSH_ROAD, cwd=tmp, extra_env=extra)


# --- a scratch repo, so every behavioural proof stands apart from this repo's own HEAD ---

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
    return _head(tmp)


def _head(tmp):
    return _run(["git", "rev-parse", "HEAD"], cwd=tmp).stdout.strip()


def _record(shas, findings="the delta was read for a refusal; two soft spots noted below.",
            blocking="none", drop_field=None, extra=""):
    """A record body naming the given commits, in the shape docs/prover/README.md states."""
    fields = [
        ("Range", "%s..%s" % (shas[0], shas[-1])),
        ("Files read", "PRODUCT_SPEC.md, guardrails/pre-push"),
        ("Checks run", "python3 -m pytest -q — 12 passed"),
        ("Findings", findings),
        ("Blocking", blocking),
    ]
    lines = ["# Prover record — %s scratch" % FIXTURE_DAY, "", "PUSH-REVIEW", ""]
    for name, value in fields:
        if name == drop_field:
            continue
        lines.append("%s: %s" % (name, value))
        if name == "Range":
            lines.extend("- %s a commit the review read" % s for s in shas)
        if name == "Blocking" and extra:
            lines.append(extra)
    return "\n".join(lines) + "\n"


def _short(sha):
    return sha[:7]


# --- the gate and its record home ship ---

def test_gate_ships():
    assert os.path.isfile(GATE), "guardrails/check-prover-record.sh missing"
    assert os.access(GATE, os.X_OK), "guardrails/check-prover-record.sh is not executable"


def test_record_home_ships():
    assert os.path.isdir(RECORD_DIR), "docs/prover/ home missing"
    assert os.path.isfile(os.path.join(RECORD_DIR, "README.md")), \
        "docs/prover/README.md, which states the record's shape, is missing"


# --- red first: the four states the requirement names ---

def test_range_with_no_record_reds():
    """A push carrying commits and no record under docs/prover/ reds — the case the practice
    lived in before the requirement existed."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        _commit_all(tmp, "a v2")
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "FAIL (prover record)" in r.stdout
        assert "no file matching" in r.stdout


def test_stale_record_does_not_cover_a_later_commit():
    """A record committed before the newest commit in the range covers a state the push has
    already left behind."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY, _record([_short(base)]))
        _commit_all(tmp, "a review record")
        _write(tmp, "a.txt", "two — changed after the review\n")
        _commit_all(tmp, "a v2")
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "predates the newest commit" in r.stdout


def test_record_naming_another_range_covers_nothing():
    """A record that names some other range covers nothing here: it is fresh by its commit
    and still fails, because coverage is read off the commits the record names."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record(["0ddba11", "c0ffee1"]))
        _commit_all(tmp, "a record for some other change")
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "names the pushed range" in r.stdout


def test_a_fresh_record_naming_the_range_passes():
    """The green direction: a committed record naming the base commit and every reviewed
    commit, carrying its fields, lets the push through."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        change = _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record([_short(base), _short(change)]))
        _commit_all(tmp, "the review of that change")
        r = _gate(tmp, base)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "OK (push range)" in r.stdout


# --- the record is committed, whole, and honest about its blocking findings ---

def test_untracked_record_does_not_count():
    """A record sitting untracked in the working tree is a scratch file."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        change = _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record([_short(base), _short(change)]))  # written, never committed
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "none are committed to git" in r.stdout


def test_record_short_a_field_reds():
    """A record naming the right range and leaving out what it ran states nothing about its
    coverage, so it reds by the missing field's name."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        change = _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record([_short(base), _short(change)], drop_field="Checks run"))
        _commit_all(tmp, "a record with no checks named")
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "Checks run" in r.stdout


def test_open_blocking_finding_reds():
    """A blocking finding holds the push while it stands open."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        change = _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record([_short(base), _short(change)], blocking="1",
                       extra="- the new gate never runs on a fresh checkout"))
        _commit_all(tmp, "a record carrying an open blocking finding")
        r = _gate(tmp, base)
        assert r.returncode == 1, r.stdout + r.stderr
        assert "neither closed nor explained" in r.stdout


def test_closed_blocking_finding_passes():
    """A blocking finding that is closed, or that carries the reason it stands, lets the
    push through — the record is what settles it."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "a.txt", "two\n")
        change = _commit_all(tmp, "a v2")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY,
               _record([_short(base), _short(change)], blocking="1",
                       extra="- the new gate never runs on a fresh checkout — closed: the "
                             "base ladder falls back to the previous commit"))
        _commit_all(tmp, "a record whose blocking finding is closed")
        r = _gate(tmp, base)
        assert r.returncode == 0, r.stdout + r.stderr


# --- the ranges that owe nothing ---

def test_a_range_of_record_commits_alone_stands_down():
    """A range whose every commit carries the record alone holds no change of its own to
    review, so the gate stands down by name instead of asking for a record of a record."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        base = _commit_all(tmp, "a v1")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY, _record([_short(base)]))
        _commit_all(tmp, "a record, and nothing else")
        r = _gate(tmp, base)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "carries the review record alone" in r.stdout


def test_a_tree_with_no_range_stands_down():
    """A single-commit tree with no remote resolves no range, so no delta can be measured
    and none is owed — the honest stand-down, never a silent pass."""
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "a.txt", "one\n")
        _write(tmp, "docs/prover/%s-scratch.md" % FIXTURE_DAY, _record(["0ddba11"]))
        _commit_all(tmp, "the first commit, record and all")
        r = _gate(tmp)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "no push range resolves" in r.stdout


# --- one record, one gate: the second of each is gone ---

def test_one_record_and_one_gate_carry_the_push_review():
    """The merge itself: the push chain runs one review-record gate over one record home. The
    second gate, its record home and its registry entry are gone, and the retired script rests
    in the attic under its manifest line."""
    prepush = read("guardrails/pre-push")
    assert "check-prover-record.sh" in prepush, "pre-push does not wire the review-record gate"
    assert "-- gate a:" in prepush, "the review-record gate carries no gate letter in pre-push"
    assert "check-push-review" not in prepush, "the second review gate is still wired into pre-push"

    assert not os.path.exists(os.path.join(ROOT, "guardrails", "check-push-review.sh")), \
        "the retired second gate still ships under guardrails/"
    assert os.path.isfile(os.path.join(ROOT, "attic", "check-push-review.sh")), \
        "the retired second gate does not rest in the attic"
    assert "check-push-review.sh" in read("attic/MANIFEST.md"), \
        "the retired second gate carries no attic manifest line"

    assert not os.path.isdir(os.path.join(ROOT, "docs", "push-review")), \
        "the second record home still stands"

    with open(os.path.join(ROOT, "guardrails", "gate-red-proofs.json"), encoding="utf-8") as f:
        reg = json.load(f)
    assert "ac" not in reg["proofs"], "the retired gate still holds a known-red proof entry"


# --- the four documents agree ---

def test_spec_states_the_law():
    spec = read_flat("PRODUCT_SPEC.md")
    assert "[INV-304]" in spec
    assert "require one review record per push and no second one" in spec
    assert "the reviewer is briefed to find reasons the change should be refused" in spec
    assert "`docs/prover/`" in spec
    assert "docs/push-review" not in spec, "the retired record home is still named in the spec"


def test_matrix_rows_cover_the_law():
    matrix = read("TEST_MATRIX.md")
    for row in ("M-494", "M-495", "M-496"):
        assert row in matrix, "matrix row %s missing" % row
    assert "INV-304" in matrix


def test_the_limit_is_stated_in_every_home():
    """What a script cannot hold is said in three places, so no reader takes the green line
    for a judgment that the review was adversarial."""
    for home in ("guardrails/check-prover-record.sh", "docs/prover/README.md",
                 "PRODUCT_SPEC.md"):
        text = read_flat(home).lower()
        assert "no script decides" in text or "adversarial" in text, home
    script = read_flat("guardrails/check-prover-record.sh").lower()
    assert "cannot hold" in script, "the script does not state its own limit"
    spec = read_flat("PRODUCT_SPEC.md")
    assert "no script decides whether a reviewer set out to refuse the change" in spec


def test_the_house_format_names_only_fields_the_gate_reads():
    """One format, and the surviving gate parses all of it. The house format once carried a
    `Commits:` field no arm ever read, so a person writing a record could not tell which lines
    the machine held. Every field the README's shape block names is now a field the gate's own
    field list reads."""
    script = read("guardrails/check-prover-record.sh")
    m = re.search(r'for field in ((?:"[^"]+" ?)+); do', script)
    assert m, "the gate's field list is no longer readable from the script"
    parsed = set(re.findall(r'"([^"]+)"', m.group(1)))

    readme = read("docs/prover/README.md")
    block = re.search(r"```\n(# Prover record.*?)```", readme, re.S)
    assert block, "docs/prover/README.md carries no record shape block"
    documented = set(re.findall(r"^([A-Z][A-Za-z ]*):", block.group(1), re.M))
    assert documented == parsed, (
        "the house format and the gate's field list disagree: documented=%s parsed=%s"
        % (sorted(documented), sorted(parsed)))
    assert "PUSH-REVIEW" in block.group(1), "the shape block drops the marker the gate reads"


def test_a_long_record_still_matches_the_hashes_it_names(tmp_path):
    """A record of real size passes. The gate once read the body through a pipe into `grep -q`:
    grep left at the first hit, the writer took SIGPIPE, and `set -o pipefail` turned a hash the
    record plainly named into a miss. The longer the record, the more reliably that happens
    (found 2026-08-06, the record stood at 57 kilobytes)."""
    tmp = tmp_path
    _init_repo(tmp)
    _write(tmp, "a.txt", "one\n")
    _commit_all(tmp, "base")
    base = _head(tmp)
    _run(["git", "branch", "-f", "origin-main", base], cwd=tmp)
    _write(tmp, "a.txt", "two\n")
    _commit_all(tmp, "work")
    work = _head(tmp)
    shas = [_short(base), _short(work)]
    padding = "\n".join(
        "Finding %d: a paragraph of ordinary review prose that carries no hash at all." % i
        for i in range(1, 1200))
    _write(tmp, "docs/prover/%s-long.md" % FIXTURE_DAY, _record(shas, extra=padding))
    _commit_all(tmp, "the record")
    body = (tmp / ("docs/prover/%s-long.md" % FIXTURE_DAY)).read_text()
    assert len(body) > 60000, "the fixture record must be long enough to fill a pipe buffer"
    res = _gate(str(tmp), base)
    assert res.returncode == 0, (
        "the gate red a record that names every reviewed commit:\n%s" % (res.stdout + res.stderr))


def test_a_long_record_with_a_blank_line_after_its_fields_still_reads(tmp_path):
    """The blocking-field reader once died silently on a long record. It walked the body with awk
    and left at the first blank line after the fields, which is the record's ordinary shape; the
    writer took SIGPIPE and the gate exited 141 printing nothing at all. A record padded BELOW its
    fields drives that reader, which the hash test above never reaches (found 2026-08-06)."""
    tmp = tmp_path
    _init_repo(tmp)
    _write(tmp, "a.txt", "one\n")
    _commit_all(tmp, "base")
    base = _head(tmp)
    _write(tmp, "a.txt", "two\n")
    _commit_all(tmp, "work")
    work = _head(tmp)
    shas = [_short(base), _short(work)]
    padding = "\n".join(
        "Note %d: review prose standing below the fields, after a blank line." % i
        for i in range(1, 1600))
    body = _record(shas) + "\n" + padding + "\n"
    _write(tmp, "docs/prover/%s-tail.md" % FIXTURE_DAY, body)
    _commit_all(tmp, "the record")
    assert len(body) > 90000, "the fixture must outgrow the pipe buffer below its fields"
    res = _gate(str(tmp), base)
    assert res.returncode == 0, (
        "the gate failed on a record whose prose sits below its fields:\n%s"
        % (res.stdout + res.stderr))
    assert res.stdout.strip(), "the gate exited without printing a verdict"
