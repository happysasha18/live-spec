"""tests/test_architecture_pins.py — a hand-kept count in an architecture pin proves itself against
the tree it describes (SPEC INV-281, S9 of docs/prover/2026-07-27-push-gate-fold.md).

ARCHITECTURE.md's `hooks/turn_reader.py:1` pin names the hooks that import the shared full-turn
reader — the contrast-frame scan, the hedge scan, the register judge, the code-anchor scan, and the
empty-validation scan. That list moved from three to five to six inside one day, each time by a hand
edit against a `grep` somebody remembered to run, and back to five when the tool-boundary scan was
retired on 2026-08-17. This file is the net:
it reads the actual importers of hooks/turn_reader.py under hooks/ and asserts the pin's own
parenthetical names every one of them, by its own descriptive name, so a sixth importer arriving
with no matching pin edit reds here instead of waiting for the next person who remembers to grep.
"""
import os
import re

from conftest import read as _read, ARCHITECTURE as _ARCHITECTURE

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = os.path.join(REPO_ROOT, "hooks")
# ARCHITECTURE.md is a core plus parts (its own `## Parts map`); the `hooks/turn_reader.py:1`
# pin now lives in the guardrails node's part, architecture/guardrails.md. Reading it through
# conftest.read() (the shared reader every test uses) joins the core and its parts the same
# way as any other consumer, so this test sees the pin whether the doc is one file or sixteen.
ARCHITECTURE_MD = _ARCHITECTURE

# Every hook file that imports turn_reader is named in the pin's own prose by a fixed descriptive
# name — the same names PRODUCT_SPEC.md's R281 sentence uses for the same five scans plus the
# register judge. A file added here without a matching pin edit is exactly the drift this test
# exists to catch; a file that imports turn_reader but has no entry here reds too (see the
# "unrecognized" assertion below), rather than passing silently on a name this test does not know.
IMPORTER_NAMES = {
    "scissors-scan.py": "contrast-frame scan",
    "hedge-scan.py": "hedge scan",
    "register-judge.py": "register judge",
    "code-anchor-scan.py": "code-anchor scan",
    "affirmation-scan.py": "empty-validation scan",
}

IMPORT_RE = re.compile(r"^\s*(?:import\s+turn_reader\b|from\s+turn_reader\s+import\b)", re.MULTILINE)


def _actual_importers():
    """Every hooks/*.py file, other than turn_reader.py itself, whose source imports it — read fresh
    from the tree each run, never from a remembered count."""
    importers = []
    for name in sorted(os.listdir(HOOKS_DIR)):
        if not name.endswith(".py") or name == "turn_reader.py":
            continue
        with open(os.path.join(HOOKS_DIR, name), encoding="utf-8") as f:
            source = f.read()
        if IMPORT_RE.search(source):
            importers.append(name)
    return importers


def _turn_reader_pin_parenthetical(architecture_path=ARCHITECTURE_MD):
    """The parenthetical text ARCHITECTURE.md's pins field carries for `hooks/turn_reader.py:1`,
    tolerant of the prose around it: the pins field is one long list for every node, so this walks
    the balanced parentheses that follow that one path rather than matching a fixed line shape."""
    body = _read(architecture_path)
    marker = "`hooks/turn_reader.py:1` ("
    start = body.find(marker)
    assert start != -1, (
        "%s carries no `hooks/turn_reader.py:1` pin to read (tests/test_architecture_pins.py)"
        % architecture_path
    )
    open_paren = start + len(marker) - 1
    depth = 0
    for j in range(open_paren, len(body)):
        if body[j] == "(":
            depth += 1
        elif body[j] == ")":
            depth -= 1
            if depth == 0:
                return body[open_paren + 1:j]
    raise AssertionError(
        "%s: hooks/turn_reader.py:1's pin parenthetical never closes (tests/test_architecture_pins.py)"
        % architecture_path
    )


def test_turn_reader_pin_names_every_actual_importer():
    """S9: the pin's parenthetical names, by its own descriptive name, exactly the hook files that
    actually import hooks/turn_reader.py — no fewer (a real importer missing from the prose) and no
    more (a name left in the prose after its file stopped importing it)."""
    importers = _actual_importers()
    parenthetical = _turn_reader_pin_parenthetical()

    unrecognized = [name for name in importers if name not in IMPORTER_NAMES]
    assert not unrecognized, (
        "hooks/%s imports turn_reader.py but tests/test_architecture_pins.py's IMPORTER_NAMES has no "
        "entry for it — add its descriptive name to IMPORTER_NAMES here and to ARCHITECTURE.md's "
        "hooks/turn_reader.py:1 pin" % ", hooks/".join(unrecognized)
    )

    missing_from_pin = [name for name in importers if IMPORTER_NAMES[name] not in parenthetical]
    assert not missing_from_pin, (
        "ARCHITECTURE.md's hooks/turn_reader.py:1 pin omits %s — hooks/%s imports turn_reader.py and "
        "the pin's parenthetical must name it (fix: add its descriptive name to the pin's list in "
        "ARCHITECTURE.md, hooks/turn_reader.py:1)"
        % (
            ", ".join(IMPORTER_NAMES[name] for name in missing_from_pin),
            ", hooks/".join(missing_from_pin),
        )
    )

    stale_in_pin = [
        name for name, desc in IMPORTER_NAMES.items()
        if name not in importers and desc in parenthetical
    ]
    assert not stale_in_pin, (
        "ARCHITECTURE.md's hooks/turn_reader.py:1 pin still names %s but hooks/%s no longer imports "
        "turn_reader.py — remove its descriptive name from the pin in ARCHITECTURE.md"
        % (
            ", ".join(IMPORTER_NAMES[name] for name in stale_in_pin),
            ", hooks/".join(stale_in_pin),
        )
    )

NUMBER_WORDS = {
    2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
}


def test_turn_reader_pin_count_word_matches_the_tree():
    """The pin opens with a count in words, and that word drifted from its own list on 2026-08-17: the
    parenthetical was edited down to five scans while the opening still read `six checks`. The name list
    passed, since it is the only thing the sibling test reads. This reads the number itself."""
    actual = _actual_importers()
    parenthetical = _turn_reader_pin_parenthetical()
    expected = NUMBER_WORDS[len(actual)]
    head = parenthetical.split(".", 1)[0]
    assert "%s checks read through" % expected in head, (
        "ARCHITECTURE.md's turn_reader pin opens with %r while %d hooks import it (%s) — "
        "tests/test_architecture_pins.py"
        % (head, len(actual), ", ".join(actual))
    )
