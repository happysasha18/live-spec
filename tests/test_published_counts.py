"""The second net over the counts this repository publishes in a hand-written sentence (SPEC R306,
INV-305).

`guardrails/check-tree-counts.py` (gate ad) holds every count in `guardrails/tree-counts.json` at the
push. This file holds the sentence homes a second time, from inside the suite, so a page statement is
caught on the next test run, before anybody pushes.

It measures the tree itself, with its own reader and its own table of cardinals, so a defect in the
gate's renderer cannot hide a defect on the page. A sentence carrying a word is checked against the
word this file spells; a sentence carrying a floor is checked against the floor it publishes.

Red-first: each case was written and run against the pages before the registry existed.
"""
import glob
import os
import re

from conftest import ROOT, read

# One through twenty, in the two forms a sentence uses. This table is this file's own, deliberately
# apart from the generator's, so both would have to be wrong the same way for a page to pass wrongly.
CARDINALS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
             "fifteen sixteen seventeen eighteen nineteen twenty").split()


def word(number):
    assert 0 <= number < len(CARDINALS), "%d falls outside the cardinals this file spells" % number
    return CARDINALS[number]


def flat(text):
    """The text with whitespace runs collapsed, so a sentence wrapped across lines still matches."""
    return " ".join(text.split())


def count_files(pattern):
    """The files one pattern matches under the repository root, sorted and non-empty."""
    hits = sorted(glob.glob(os.path.join(ROOT, pattern)))
    assert hits, "the pattern %s matches no file, so a count off it would be a count of nothing" % (
        pattern,)
    return len(hits)


def test_the_scaffold_check_count_is_stated_as_the_tree_holds_it():
    """`scaffold/guardrails/check_*.py` is the whole set a host installs, and three sentences on two
    pages state its size in words."""
    measured = count_files("scaffold/guardrails/check_*.py")
    spelled = word(measured)
    readme = flat(read("README.md"))
    guardrails_readme = flat(read("guardrails/README.md"))

    assert "%s checks decide whether a push in your project is allowed." % spelled.capitalize() \
        in readme, "README.md states a scaffold-check count the tree does not carry (%d checks)" % (
            measured,)
    assert "The %s are Python on the pre-push hook" % spelled in readme, (
        "README.md's second statement of the scaffold-check count disagrees with the tree "
        "(%d checks)" % measured)
    assert "The %s scaffold checks" % spelled in guardrails_readme, (
        "guardrails/README.md states a scaffold-check count the tree does not carry (%d checks)"
        % measured)


def test_the_gate_roster_count_agrees_with_the_push_hook():
    """`guardrails/README.md` publishes how many distinct gate letters the push hook runs."""
    letters = sorted(set(re.findall(r"-- gate ([a-z]{1,2}):", read("guardrails/pre-push"))))
    assert letters, "guardrails/pre-push carries no gate markers, so the roster would be empty"
    page = flat(read("guardrails/README.md"))
    assert "%d distinct gate letters" % len(letters) in page, (
        "guardrails/README.md states a gate count the push hook does not carry (%d letters: %s)"
        % (len(letters), ", ".join(letters)))
    for letter in letters:
        assert "-- gate %s:" % letter in read("guardrails/README.md"), (
            "the published roster misses gate %s" % letter)


def test_no_page_still_publishes_a_worker_run_count():
    """The worker-run figure left `guardrails/README.md` on 2026-08-06: the command that produced it
    reads a transcript root outside this repository, and the reading moves between two runs minutes
    apart, so no push can hold the number to anything."""
    page = flat(read("guardrails/README.md"))
    assert "80 worker runs" not in page
    assert "check-worker-restore.py --counting-from 2000-01-01 --all" in page, (
        "the counting-start paragraph names no command a reader can run for the figure")
