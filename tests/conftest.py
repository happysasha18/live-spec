"""Suite hygiene: the run leaves the machine as it found it (SPEC INV-100, M-236, row 222).

A session-scoped before/after diff of the system temp home, filtered to the suite's own
artifact prefixes — a new file surviving to session end is a leak and fails the run.
"""

import glob
import os
import re
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def read_flat(rel):
    """The file's text with whitespace collapsed, so wrapped lines match needles."""
    return " ".join(read(rel).split())


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
    build-pipeline does. A content-presence check reads the skill as ONE home, so its
    surface is SKILL.md plus its references/*.md: the anchor is found wherever inside
    the skill it lives. A size check keeps reading SKILL.md alone via read(), because
    the body-thinness ideal is about the SKILL.md body itself.
    """
    m = re.match(r"(skills/[^/]+)/SKILL\.md$", rel)
    if not m:
        return [rel]
    refs = sorted(glob.glob(os.path.join(ROOT, m.group(1), "references", "*.md")))
    return [rel] + [os.path.relpath(p, ROOT) for p in refs]


def read_all(rel):
    """A skill's whole normative surface (SKILL.md + references/*.md) as one text."""
    texts = []
    for r in _skill_surface(rel):
        with open(os.path.join(ROOT, r), encoding="utf-8") as f:
            texts.append(f.read())
    return "\n".join(texts)


def read_all_flat(rel):
    """The whole-surface text with whitespace collapsed, so wrapped lines match needles."""
    return " ".join(read_all(rel).split())


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
