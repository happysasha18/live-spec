"""Every document that states how many skills this pack holds says what it counts (2026-08-05).

Four documents once stated the number four ways: ten, nine, eleven, and ten working skills. Two of
the four were defensible, because one folder under skills/ is the shared rulebook the other ten load,
and none of them said which thing was being counted. A reader had no way to tell a typo from a
different unit. The overview's heading claimed nine while its own eleven entries stood below it.

The number is now read off disk, and each document states the count together with its unit. This test
holds both halves: the number every document states, and the rulebook named in the same sentence, so
a reader can check the arithmetic on the page. Adding a skill reds here until every document that
names the count has been brought along.
"""
import os
import re
import unittest

from conftest import ROOT

SKILLS_DIR = os.path.join(ROOT, "skills")

# The one folder under skills/ that is the shared rulebook rather than a working skill.
RULEBOOK = "live-spec-base"

# Every document that states the count. A document added here is covered from then on.
HOMES = [
    "README.md",
    "OVERVIEW.md",
    "ARCHITECTURE.md",
    os.path.join("skills", RULEBOOK, "SKILL.md"),
]

NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
    8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
    14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
    19: "nineteen", 20: "twenty",
}

# A markdown link between the number and its noun leaves the phrase whole for a reader and broken
# for a plain substring search, so the link markup comes off before anything is matched.
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")

# A product name may stand between the unit and its noun — "ten working Claude Code skills" — so the
# phrase is matched with a short gap. The gap admits CAPITALISED words alone, so an ordinary phrase
# that happens to run the same shape ("one working copy of the skills") is left to its own sentence.
_GAP = r"(?:[A-Z][\w-]*\s+){0,3}"


def plain(text):
    return _LINK.sub(r"\1", text)


def working_skill_count():
    """How many working skills stand on disk: every folder under skills/ except the rulebook."""
    names = [n for n in os.listdir(SKILLS_DIR)
             if os.path.isdir(os.path.join(SKILLS_DIR, n)) and not n.startswith(".")]
    assert RULEBOOK in names, "the shared rulebook must stand among the skill folders"
    return len(names) - 1


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return plain(fh.read())


# Only a NUMBER standing before the unit is a count. An ordinary word there — "per working skill" —
# belongs to a different sentence and is left alone. A count written in DIGITS counts too: the first
# version of this test read words alone, and "10 working skills" walked straight past it.
# The gap stays CASE-SENSITIVE while the words around it do not, so the whole pattern is compiled
# without the ignore-case flag and the case-blind parts carry their own inline group. Compiling the
# lot with that flag folded the gap's uppercase requirement away, and "one working copy of the
# skills" read as a count of one (caught 2026-08-05 by a probe written against this test).
_WORDS = "|".join(NUMBER_WORDS.values())
_COUNT_PHRASE = re.compile(
    r"\b((?i:%s)|\d{1,3})\s+(?i:working)\s+%s(?i:skills?)\b" % (_WORDS, _GAP))

_BY_WORD = {v: k for k, v in NUMBER_WORDS.items()}


def as_number(token):
    """A count written either way, as an integer. Returns None for anything else."""
    token = token.lower()
    if token.isdigit():
        return int(token)
    return _BY_WORD.get(token)


def count_phrases(text):
    """Every '<number> working skill(s)' the text carries, as integers."""
    return [as_number(m.group(1)) for m in _COUNT_PHRASE.finditer(text)]


class TestTheMatcherItself(unittest.TestCase):
    """A test that reads a document is only as good as the phrase it looks for. Both misses below
    were found by probing this matcher rather than by any document failing, so they are pinned here.
    """

    def test_a_count_written_in_digits_is_read(self):
        self.assertEqual(count_phrases("10 working skills, plus the shared rulebook."), [10])

    def test_a_count_written_in_words_is_read(self):
        self.assertEqual(
            count_phrases("Ten working Claude Code skills, plus the shared rulebook."), [10])

    def test_a_wrong_count_is_read_rather_than_skipped(self):
        """A pattern that only matched the right answer would pass on every wrong one."""
        self.assertEqual(count_phrases("Nine working skills, plus the shared rulebook."), [9])
        self.assertEqual(count_phrases("9 working skills, plus the shared rulebook."), [9])

    def test_ordinary_prose_running_the_same_shape_is_left_alone(self):
        """The gap admits a capitalised product name. Lower-case prose between the words belongs to
        its own sentence, and reading it as a count would red a lawful document."""
        self.assertEqual(count_phrases("A session loads one working copy of the skills."), [])

    def test_a_word_that_is_no_number_is_left_alone(self):
        self.assertEqual(count_phrases("The cost is measured per working skill."), [])


class TestSkillCountAgrees(unittest.TestCase):
    def test_the_rulebook_is_one_of_the_folders(self):
        """The count is a subtraction off disk, so the thing subtracted has to be there."""
        self.assertTrue(os.path.isdir(os.path.join(SKILLS_DIR, RULEBOOK)))

    def test_every_home_states_the_count_that_stands_on_disk(self):
        n = working_skill_count()
        for home in HOMES:
            found = count_phrases(read(home))
            self.assertTrue(found, "%s states no working-skill count at all" % home)
            for stated in found:
                self.assertEqual(
                    stated, n,
                    "%s says %r working skills; disk holds %d folders under skills/, which is %d "
                    "once the rulebook is set aside" % (home, stated, n + 1, n))

    def test_every_home_names_the_rulebook_beside_the_count(self):
        """A bare number drifts unnoticed. Each home says what it set aside, in the same sentence."""
        word = NUMBER_WORDS[working_skill_count()]
        pattern = re.compile(
            r"[^.\n]*\b%s\s+working\s+%sskills?\b[^.\n]*" % (word, _GAP), re.I)
        for home in HOMES:
            sentence = pattern.search(read(home))
            self.assertIsNotNone(sentence, "%s states no working-skill count" % home)
            self.assertIn(
                "rulebook", sentence.group(0).lower(),
                "%s states the count without naming the rulebook it sets aside, so a reader "
                "cannot check it: %r" % (home, sentence.group(0)[:160]))

    def test_a_heading_never_disagrees_with_the_entries_under_it(self):
        """The overview's heading claimed nine while eleven entries stood below it."""
        text = read("OVERVIEW.md")
        heading = re.search(
            r"^##\s+([A-Za-z]+)\s+working\s+%sskills?\b.*$" % _GAP, text, re.M)
        self.assertIsNotNone(heading, "OVERVIEW.md lost the section that states the count")
        body = text[heading.end():]
        nxt = re.search(r"^##\s", body, re.M)
        entries = re.findall(r"^-\s+\*\*([a-z-]+)\*\*", body[:nxt.start() if nxt else len(body)], re.M)
        self.assertEqual(
            len(entries), working_skill_count() + 1,
            "the section lists %d skills while disk holds %d folders under skills/"
            % (len(entries), working_skill_count() + 1))
        self.assertEqual(heading.group(1).lower(), NUMBER_WORDS[working_skill_count()],
                         "the heading disagrees with the entries standing under it")


if __name__ == "__main__":
    unittest.main()
