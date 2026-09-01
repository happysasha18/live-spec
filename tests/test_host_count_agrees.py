"""The architecture's own host count stays internally consistent; the front page states none (q-501,
his word 2026-09-01 23:15).

Born 2026-07-27 (ROADMAP 501, his word that day) as a check that the README's project count agreed
with ARCHITECTURE.md's own "real hosts" count, after the two drifted by hand (README said two,
architecture said three). That coupling assumed the front page would keep stating a count at all.

His later word, 2026-09-01 23:15, dropped that assumption: the front page names no project count,
full stop — not because a count could not be backed, but because the question of how many projects
may be claimed is retired entirely, not answered. The README-side half of this test (matching a
`README.md` sentence's number against `ARCHITECTURE.md`'s) is retired with it. What remains real:
`ARCHITECTURE.md` still states its own "real hosts" count for its own purposes (the project-kind
founding-check fixtures, unrelated to front-page marketing), and that count must still have exactly
one internally-consistent value. And the front page must not regenerate the retired claim — the same
shape of guard this pack already uses elsewhere (see `test_readme_stance.py`'s known-issues lock):
pin the content that must NOT be present, so a rewrite that reintroduces it is caught here rather than
needing another manual read.
"""
import os
import re

from conftest import read as _read

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
ARCH_COUNT = re.compile(r"[Tt]he (one|two|three|four|five|six) real hosts?\b")
# The same shape the retired README-side check looked for: a sentence opening with a bare
# "<Number> project(s)" count. Kept here as a lock against reintroduction, not an expectation.
README_PROJECT_COUNT = re.compile(r"(?m)^(One|Two|Three|Four|Five|Six) projects?\b")


def test_the_architecture_states_its_host_count():
    hits = {WORDS[m.group(1).lower()] for m in ARCH_COUNT.finditer(_read("ARCHITECTURE.md"))}
    assert hits, "ARCHITECTURE.md states no real-host count"
    assert len(hits) == 1, (
        "ARCHITECTURE.md states more than one real-host count: %s — the count has one home" % sorted(hits))


def test_the_front_page_states_no_project_count():
    readme = _read("README.md")
    hit = README_PROJECT_COUNT.search(readme)
    assert hit is None, (
        "README.md opens a sentence with a project count (%r) — his word 2026-09-01 23:15 retired "
        "that claim entirely; the page should name no count of projects it runs under, backed or "
        "not" % hit.group(0) if hit else None)
