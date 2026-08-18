"""Suite hygiene: the run leaves the machine as it found it (SPEC INV-100, M-236, row 222).

A session-scoped before/after diff of the system temp home, filtered to the suite's own
artifact prefixes — a new file surviving to session end is a leak and fails the run.
"""

import glob
import io
import os
import re
import sys
import tempfile
import unittest

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def spec_paths():
    """The files the spec is written across: the core first, then the parts its map names."""
    return _sf.spec_paths([os.path.join(ROOT, SPEC)])


def _with_reference_tail(text):
    """`text` plus its generated index table under a trailing `## Reference`, unless `text`
    already carries that heading itself (the pre-split shape, read straight off disk)."""
    if "\n## Reference" in text or text.startswith("## Reference"):
        return text
    with open(os.path.join(ROOT, SPEC_INDEX), encoding="utf-8") as f:
        table = f.read()
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return text + sep + _REFERENCE_INTRO + table


def read(rel):
    if rel == SPEC:
        return _with_reference_tail(_sf.read_document(spec_paths(), expand=False)[1])
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


@pytest.fixture(autouse=True, scope="session")
def suite_leaves_no_trace():
    tmp = tempfile.gettempdir()
    before = _ours(set(os.listdir(tmp)))
    yield
    after = _ours(set(os.listdir(tmp)))
    leaked = sorted(after - before)
    assert not leaked, "the suite leaked temp artifacts (SPEC INV-100): %s" % leaked
