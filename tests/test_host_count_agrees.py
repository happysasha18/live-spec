"""The public page's host count agrees with the architecture's own (ROADMAP 501, his word 2026-07-27).

The README told a stranger that two projects run under the pack while ARCHITECTURE.md named three real
hosts, and the contradiction stood on the page's own honesty claim, where it costs most. The number moved
by hand in both files, so nothing would have caught the next drift either. This reads the architecture's
count as the authority and asserts the front page states the same one.
"""
import os
import re

from conftest import read as _read

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
ARCH_COUNT = re.compile(r"[Tt]he (one|two|three|four|five|six) real hosts?\b")
README_COUNT = re.compile(r"(?m)^(One|Two|Three|Four|Five|Six) projects?\b")


def test_the_architecture_states_its_host_count():
    hits = {WORDS[m.group(1).lower()] for m in ARCH_COUNT.finditer(_read("ARCHITECTURE.md"))}
    assert hits, "ARCHITECTURE.md states no real-host count for the front page to agree with"
    assert len(hits) == 1, (
        "ARCHITECTURE.md states more than one real-host count: %s — the count has one home" % sorted(hits))


def test_the_front_page_states_the_architecture_count():
    arch = {WORDS[m.group(1).lower()] for m in ARCH_COUNT.finditer(_read("ARCHITECTURE.md"))}
    readme = _read("README.md")
    sentences = README_COUNT.findall(readme)
    assert sentences, "README.md opens no sentence with a project count; the honesty paragraph states one"
    stated = {WORDS[w.lower()] for w in sentences}
    assert stated == arch, (
        "the front page says %s project(s) run under the pack and the architecture names %s real host(s): "
        "the two numbers move together, and the architecture is the authority "
        "(README.md, ARCHITECTURE.md, ROADMAP 501)" % (sorted(stated), sorted(arch)))
