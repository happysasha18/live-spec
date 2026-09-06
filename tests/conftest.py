"""Suite hygiene: the run leaves the machine as it found it (SPEC INV-100, M-236, row 222).

Every temp artifact the run makes is born under one temp root of the run's own, and the
session-end check reads that root, filtered to the suite's own artifact prefixes — an
artifact of this run's surviving to session end is a leak and fails the run.
"""

import atexit
import glob
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Git exports these while it runs a hook, and every `git` a test starts inherits them.
# An inherited GIT_DIR outranks `-C tmp`, so a fixture that builds its own little
# repository commits into the repository being pushed instead — the suite run inside the
# pre-push guard fabricated hundreds of commits this way. They are stripped once, here,
# before any test collects: nothing in this suite may act on a repository it did not name.
INHERITED_GIT_ENV = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_QUARANTINE_PATH",
    "GIT_PREFIX",
    "GIT_NAMESPACE",
)

for _inherited in INHERITED_GIT_ENV:
    os.environ.pop(_inherited, None)

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import specformat as _sf  # noqa: E402

# The spec may be written as a core file plus part files; the core's `## Parts map` names them and
# their order. Every test that reads the spec reads it through read()/read_flat() here, so this one
# node is where the parts are joined back into the one document those ~140 tests expect. An empty
# map (the state today) makes the core the whole document and the text byte-identical to the file.
SPEC = "PRODUCT_SPEC.md"
SPEC_INDEX = "PRODUCT_SPEC.index.md"

# The generated code-to-location table used to be embedded a SECOND time under the spec's own
# trailing `## Reference` heading — byte-identical to the committed PRODUCT_SPEC.index.md, the
# same generated artifact in two places (a pure duplicate, confirmed by diff). The spec split
# deleted that inline copy (ROADMAP row 621): PRODUCT_SPEC.index.md is now the table's one home on
# disk. A large family of tests still reads the spec as one document carrying its own closing
# table, so `read()` re-synthesizes the section below rather than sending every one of them to
# learn a second file exists — the same one-node fix the parts map itself rests on: storage may
# change shape; the read the node hands back does not, for a caller written before it did.
_REFERENCE_INTRO = (
    "## Reference\n\n\n\n\n"
    "The code-to-location table below is generated output, built from the body criteria by "
    "`scripts/build-index.py`; no one edits it by hand. Feature codes (`F-...`) live on their "
    "scenario headings and carry no table row.\n\n"
)

# The matrix is written the same way: a core file plus part files, the core's `## Parts map`
# naming them and their order (the state today — TEST_MATRIX.md's rows live in matrix/*.md, and the
# core carries no inline `## Reference` section of its own any more). So `read()` always does real
# work here: it joins the core and every named part, then appends the committed `TEST_MATRIX.index.md`
# under a synthesized `## Reference` heading, the same way the spec's own read() does.
MATRIX = "TEST_MATRIX.md"
MATRIX_INDEX = "TEST_MATRIX.index.md"

_MATRIX_REFERENCE_INTRO = (
    "## Reference\n\n\n\n\n"
    "The anchor-to-row table below is generated output, built from the body rows by "
    "`scripts/build-matrix-reference.py`; no one edits it by hand. Each spec anchor a body row "
    "carries maps to the matrix rows that cover it, ranges and compound anchors expanded.\n\n"
)

# The architecture is written the same way: a core file plus part files under architecture/*.md,
# the core's `## Parts map` naming them and their order. Unlike the spec and the matrix, its
# generated index (ARCHITECTURE.index.md, the gate-z anchor table and the node/part router table)
# is its own separate file rather than an inline `## Reference` section synthesized at read time —
# so read() here does the core+parts join and nothing more.
ARCHITECTURE = "ARCHITECTURE.md"
ARCHITECTURE_INDEX = "ARCHITECTURE.index.md"


def spec_paths():
    """The files the spec is written across: the core first, then the parts its map names."""
    return _sf.spec_paths([os.path.join(ROOT, SPEC)])


def matrix_paths():
    """The files the matrix is written across: the core first, then the parts its map names."""
    return _sf.spec_paths([os.path.join(ROOT, MATRIX)])


def architecture_paths():
    """The files the architecture is written across: the core first, then the parts its map names."""
    return _sf.spec_paths([os.path.join(ROOT, ARCHITECTURE)])


def _with_reference_tail(text):
    """`text` plus its generated index table under a trailing `## Reference`, unless `text`
    already carries that heading itself (the pre-split shape, read straight off disk)."""
    if "\n## Reference" in text or text.startswith("## Reference"):
        return text
    with open(os.path.join(ROOT, SPEC_INDEX), encoding="utf-8") as f:
        table = f.read()
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return text + sep + _REFERENCE_INTRO + table


def _with_matrix_reference_tail(text):
    """`text` plus its generated Reference table under a trailing `## Reference`, unless `text`
    already carries that heading itself (the pre-split shape, read straight off disk)."""
    if "\n## Reference" in text or text.startswith("## Reference"):
        return text
    with open(os.path.join(ROOT, MATRIX_INDEX), encoding="utf-8") as f:
        table = f.read()
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return text + sep + _MATRIX_REFERENCE_INTRO + table


def read(rel):
    if rel == SPEC:
        return _with_reference_tail(_sf.read_document(spec_paths(), expand=False)[1])
    if rel == MATRIX:
        return _with_matrix_reference_tail(_sf.read_document(matrix_paths(), expand=False)[1])
    if rel == ARCHITECTURE:
        # No Reference tail is synthesized here: ARCHITECTURE.index.md is its own committed
        # file (gate z's output), never an inline section of ARCHITECTURE.md itself.
        return _sf.read_document(architecture_paths(), expand=False)[1]
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def read_flat(rel):
    """The file's text with whitespace collapsed, so wrapped lines match needles."""
    return " ".join(read(rel).split())


def open_spec():
    """The whole spec as a readable text stream, for a test that walks it line by line.

    `with open_spec() as f: for line in f:` reads exactly what `open(PRODUCT_SPEC.md)` used to —
    each line with its ending — and reads it through read() above, so a test that iterates the spec
    sees the core AND the parts its map names. A test that opens the path itself would see the core
    alone the moment a part exists, and would pass while reading a fraction of the document; that is
    why the path is not spelled out in ~40 test files any more.
    """
    return io.StringIO(read(SPEC))


_BULLET = re.compile(r"^\s{2,}[-*]\s")
_TRAILING_CODES = re.compile(r"\[([^\[\]]*)\]\s*$")


def criterion_units(text):
    """Every line of a requirements-format document, paired with the whole criterion it heads.

    The format moves an in-place definition out of its criterion line into indented bullets
    beneath it, so one criterion's fact and its trailing code bracket now sit on different
    physical lines. A unit is `(head, whole)`: the head line as written, and the head joined
    with the bullets under it, whitespace collapsed. A check that wants the fact reads `whole`;
    a check that wants the trailing bracket reads `head`.
    """
    units, head, body = [], None, []
    for line in text.splitlines():
        if head is not None and _BULLET.match(line):
            body.append(line)
            continue
        if head is not None:
            units.append((head, " ".join(" ".join([head] + body).split())))
        head, body = line, []
    if head is not None:
        units.append((head, " ".join(" ".join([head] + body).split())))
    return units


def criterion_with_bullets(text, phrase):
    """The one criterion carrying a distinctive phrase, read with the bullets under it.

    None when no criterion carries the phrase, so a caller asserts the home is there before
    reading a fact out of it.
    """
    for _head, whole in criterion_units(text):
        if phrase in whole:
            return whole
    return None


def criteria_citing(text, anchor):
    """Every criterion whose trailing code bracket names this anchor, each read with its bullets.

    Membership in the bracket — not sole occupancy of it — is what makes a line the anchor's
    declaration, and the bracket rides the head line, so it is matched there while the bullets
    come along in the returned text. Table lines are passed over: an index row is a lookup into
    the home, never the home itself.
    """
    found = []
    for head, whole in criterion_units(text):
        s = head.rstrip()
        if s.lstrip().startswith("|"):
            continue
        m = _TRAILING_CODES.search(s)
        if m and anchor in [c.strip() for c in m.group(1).split(",")]:
            found.append(whole)
    return " ".join(found)


def _skill_surface(rel):
    """The files that make up a skill's whole normative surface.

    A skill may offload set-piece material (large tables, worked examples) from its
    SKILL.md into a sibling references/ directory to stay within the length budget —
    build-pipeline does, and the external product-prover clone uses the singular
    reference/ for the same offload. A content-presence check reads the skill as ONE
    home, so its surface is SKILL.md plus its reference(s)/*.md: the anchor is found
    wherever inside the skill it lives. A size check keeps reading SKILL.md alone via
    read(), because the body-thinness ideal is about the SKILL.md body itself.
    """
    m = re.match(r"(skills/[^/]+)/SKILL\.md$", rel)
    if not m:
        return [rel]
    refs = sorted(
        glob.glob(os.path.join(ROOT, m.group(1), "references", "*.md"))
        + glob.glob(os.path.join(ROOT, m.group(1), "reference", "*.md"))
    )
    return [rel] + [os.path.relpath(p, ROOT) for p in refs]


def read_all(rel):
    """A skill's whole normative surface (SKILL.md + references/*.md) as one text."""
    return "\n".join(read(r) for r in _skill_surface(rel))


def read_all_flat(rel):
    """The whole-surface text with whitespace collapsed, so wrapped lines match needles."""
    return " ".join(read_all(rel).split())


def external_clone_or_skip(name="product-prover"):
    """The installed external skill clone's root, or a clean skip on a bare checkout.

    skills/product-prover/ is an untracked clone that scripts/install-external-skills.sh
    installs; the tracked contract for it lives in skills/product-prover-pack/SKILL.md.
    A test that reads the clone's CONTENT calls this before reading, so a checkout with
    no installed clone skips with the reason instead of crashing on FileNotFoundError.

    In CI the same skip would once have been permanent and silent: the gates job checked
    out, installed pytest and ran the suite with no step that installs the external skill,
    so every call here would skip on every run forever and the whole re-pinned prover
    surface would be proven nowhere. That fork is now closed, and closed one way: CI
    INSTALLS the canon. `.github/workflows/gates.yml` runs
    `scripts/install-external-skills.sh` with a commit pin and a verification of that pin
    before the suite step, so the ~52 canon assertions actually run in the environment that
    gates a push. The pack proves the canon it depends on instead of claiming a green over
    a file it never read.

    The CI arm below therefore stays, changed in meaning: it is no longer a debt marker but
    the tripwire on the installer step. If that step is ever removed, renamed or fails, this
    fails loudly and names the step, instead of the suite quietly reporting ~52 skips.

    The same fork was reached from the other side by the adversarial read on branch
    `prover-decoupling-emergency-2026-08-13` (its `docs/prover/2026-08-13-push-range-4.md`,
    finding 4, and the ROADMAP row it opened there); that branch's disposition remains the
    owner's, and nothing here depends on it.
    """
    root = os.path.join(ROOT, "skills", name)
    if not os.path.isfile(os.path.join(root, "SKILL.md")):
        reason = (
            "external clone skills/%s/ not installed (tracked contract: "
            "skills/product-prover-pack/SKILL.md; install: "
            "scripts/install-external-skills.sh)" % name
        )
        if os.environ.get("CI"):
            raise AssertionError(
                "this proof did not run and CI has no other net for it — " + reason +
                "; CI is supposed to carry the canon, so reaching this line means the "
                "pinned installer step in .github/workflows/gates.yml was removed, renamed "
                "or failed. Restore that step rather than widening this guard. A silent "
                "permanent skip is not a pass."
            )
        raise unittest.SkipTest(reason)
    return root


# The suite's own temp-artifact prefixes — the single source of truth for "this name is ours".
# Exported (no leading underscore) so any test that deliberately kills a process which may be
# mid-way through creating one of these artifacts (SIGKILL, uncatchable, skips every tearDown)
# can sweep by the same rule this session-end check uses, rather than guessing at one hardcoded
# pattern of its own (ROADMAP row 574: a guess at one pattern left every OTHER suite artifact,
# such as an agent-inbox test's temp dir, free to leak past a kill it never anticipated).
SUITE_TEMP_PREFIXES = ("livespec-test-", "row241-host-")
_PREFIXES = SUITE_TEMP_PREFIXES  # back-compat alias for any in-file reference


def _ours(names):
    return {n for n in names if n.startswith(SUITE_TEMP_PREFIXES)}


# This run's own temp home, and the one place the leak check below looks.
#
# The check used to list the machine's SHARED temp home at session start and fail on any
# suite-prefixed name that had appeared by session end. That judges a machine-global
# namespace, not the files this process made — so a SECOND run of this suite anywhere on
# the machine reddened the first one, and `guardrails/check-tests.sh` mktemps a
# `livespec-test-suite-log.*` the instant it starts, which is enough on its own. Parallel
# lanes in one tree are this pack's own working mode, so the collision was routine: several
# sessions on 2026-08-27 read that red as another session's droppings and moved past it
# (2026-08-28 adversarial review, finding 1).
#
# So the run takes a root of its own and the check ranges over what landed inside it. The
# root is exported through TMPDIR as well as tempfile's own module state, so a subprocess the
# suite starts — a nested pytest, check-tests.sh, git — writes its temp files inside this
# run's root too. Its name carries a suite prefix, so a sibling that sweeps by
# SUITE_TEMP_PREFIXES (tests/test_deletion_only_push.py after a kill it throws on purpose)
# still recognises it as suite property.
RUN_TEMP_ROOT = tempfile.mkdtemp(prefix="livespec-test-run-", dir=tempfile.gettempdir())
tempfile.tempdir = RUN_TEMP_ROOT
os.environ["TMPDIR"] = RUN_TEMP_ROOT


@atexit.register
def _drop_empty_run_temp_root():
    """A process that imports this file and never reaches the session fixture — a
    collect-only pass, an interpreter that only imports the helpers — leaves the root
    behind otherwise. Only an EMPTY root goes: anything inside it is evidence, and
    rmdir refuses a directory that holds any."""
    try:
        os.rmdir(RUN_TEMP_ROOT)
    except OSError:
        pass


@pytest.fixture(autouse=True, scope="session")
def suite_leaves_no_trace():
    yield
    leaked = sorted(_ours(set(os.listdir(RUN_TEMP_ROOT))))
    assert not leaked, (
        "the suite leaked temp artifacts (SPEC INV-100): %s — left in this run's own temp "
        "root %s" % (leaked, RUN_TEMP_ROOT)
    )
    # Nothing of ours survives, so the root itself goes; pytest's own tmp_path bookkeeping
    # (`pytest-of-<user>/`) lives inside it and goes with it. On a leak the assert above fires
    # first and the whole root stays put, named and findable, for whoever reads the failure.
    shutil.rmtree(RUN_TEMP_ROOT, ignore_errors=True)


def _git(*args):
    """A read-only git call against ROOT, the judged tree itself — never a fixture's scratch
    copy. Returns None on any git error (e.g. ROOT is not a git checkout at all, a LIVE_SPEC_SCRATCH
    run), which the caller below treats as "nothing to compare"."""
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _judged_status():
    """ROOT's status with the interpreter's own droppings filtered out.

    Running the suite compiles the tree it imports from, so `__pycache__` directories appear
    under paths the run merely read. They are not the suite writing to the judged tree, and on a
    fresh CI checkout they appear during the run every time. Everything else — a tracked file
    changed, a file deleted, any other untracked path — still counts."""
    status = _git("status", "--porcelain")
    if status is None:
        return None
    keep = []
    for line in status.splitlines():
        path = line[3:].strip().strip('"')
        if line.startswith("??") and (path.endswith("__pycache__/") or path.endswith(".pyc")):
            continue
        # Gate B records the suite's own green in this one checkpoint by design (the meta
        # suite-green checkpoint); the guard reads it as the suite's record, not as a mutation.
        if path == ".live-spec/checkpoints/meta-suite-green.json":
            continue
        keep.append(line)
    return "\n".join(keep)


@pytest.fixture(autouse=True, scope="session")
def judged_tree_gains_no_commits():
    """The suite reads the judged tree; it does not write to it (2026-08-18 polluter incident:
    hundreds of scratch commits with messages lifted from fixture builders — "fixture", "base",
    "a v1", "skill v1" — landed on a real, pushed branch, and tracked fixture files vanished from
    the working tree, because a script under test inherited the judged tree as its own ambient cwd
    instead of an isolated one of its own).

    A session-scoped before/after snapshot of ROOT's HEAD and working-tree status: whatever the
    run does to its own scratch copies, ROOT's HEAD must not move and its tracked files must not
    change. This catches the class, not one script — it reds no matter which call site regresses
    next."""
    if os.environ.get("LIVE_SPEC_SCRATCH"):
        yield
        return
    head_before = _git("rev-parse", "HEAD")
    if head_before is None:
        yield  # ROOT is not a git checkout (e.g. an installed copy) — nothing to compare.
        return
    status_before = _judged_status()
    yield
    head_after = _git("rev-parse", "HEAD")
    status_after = _judged_status()
    assert head_before == head_after, (
        "the suite left new commits on the judged tree's checked-out branch: HEAD moved from "
        "%s to %s — a script under test wrote to ROOT instead of a directory of its own"
        % (head_before, head_after)
    )
    assert status_before == status_after, (
        "the suite changed the judged tree's working-copy state (SPEC INV-100, one layer down):\n"
        "before:\n%s\nafter:\n%s" % (status_before, status_after)
    )
