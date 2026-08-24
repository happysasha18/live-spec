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
import tempfile
import unittest

from conftest import ROOT, ARCHITECTURE, read as _conftest_read

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


# An adapter page declares the external skill it stands in for on its metadata `requires:`
# line — the same tracked sentence tests/test_traceability.py's external_skill_roots() and
# scripts/install-external-skills.sh both read. That roster is the AUTHORITY here, because it
# is tracked: it reads the same on a bare checkout, on a developer's machine with the clone
# installed, and in CI. The structural `.git` probe below is the second net, for a checkout
# nobody declared.
_REQUIRES = re.compile(r"^\s*requires:\s*([\w-]+)\s*>=\s*[\d.]+\s*\(([^()\s]+)\)", re.M)


def declared_external_skills(skills_dir=SKILLS_DIR):
    """Every external skill name the pack's tracked adapter pages declare."""
    names = set()
    if not os.path.isdir(skills_dir):
        return names
    for name in sorted(os.listdir(skills_dir)):
        page = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(page):
            continue
        with open(page, encoding="utf-8") as fh:
            found = _REQUIRES.search(fh.read(4000))
        if found:
            names.add(found.group(1))
    return names


def is_external_skill(skills_dir, name):
    """Is this folder another repository, installed here rather than shipped by the pack?

    The same structural probe install.sh, scripts/sync-skills.sh and scripts/stamp-versions.py
    already use: a skill folder carrying its own `.git` is an EXTERNAL skill that some
    installer put here — product-prover today — and belongs to a repository this one does
    not own. `os.path.exists` rather than `isdir`, because a worktree checkout writes `.git`
    as a FILE, and install.sh's `[ -e ... ]` covers both spellings for the same reason.

    The probe is structural, not a name list, so it holds for the next external skill as
    well as this one and cannot be fooled by a rename.
    """
    return os.path.exists(os.path.join(skills_dir, name, ".git"))


def working_skill_count(skills_dir=SKILLS_DIR):
    """How many working skills stand on disk: every folder under skills/ except the rulebook.

    And except any external skill installed into the same folder. The count answers "how
    many skills does this pack hold", so a clone of another repository sitting under
    skills/ is not one of them — the same boundary the version stamper and the two sync
    scripts already hold. Before this fence the number was
    a property of the READER's machine rather than of the pack: a developer who ran
    scripts/install-external-skills.sh counted eleven where every document says ten, and
    the three checks below reddened on their own machine while staying green in a CI that
    installed nothing. Now that CI installs the pinned canon, the unfenced count would have
    reddened there too, on every run.
    """
    declared = declared_external_skills(skills_dir)
    names = [n for n in os.listdir(skills_dir)
             if os.path.isdir(os.path.join(skills_dir, n)) and not n.startswith(".")
             and n not in declared and not is_external_skill(skills_dir, n)]
    assert RULEBOOK in names, "the shared rulebook must stand among the skill folders"
    return len(names) - 1


def pack_skill_folders(skills_dir=SKILLS_DIR):
    """The pack's own skill folders, rulebook included, external skills excluded."""
    declared = declared_external_skills(skills_dir)
    return {n for n in os.listdir(skills_dir)
            if os.path.isdir(os.path.join(skills_dir, n)) and not n.startswith(".")
            and n not in declared and not is_external_skill(skills_dir, n)}


def read(rel):
    # ARCHITECTURE.md is a core plus parts (its own `## Parts map`) — reading it through
    # conftest's shared reader joins them, the way every other document-aware test does, so a
    # count sentence living in a part is not silently unseen once it moves off the core.
    if rel == ARCHITECTURE:
        text = _conftest_read(rel)
    else:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            text = fh.read()
    return plain(text)


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


class TestTheExternalSkillFence(unittest.TestCase):
    """The fence is proven on a planted layout, not on this machine's install state.

    A check that only ran where the clone happens to be installed would prove nothing on a
    machine without it, and nothing at all about the NEXT external skill. The layout below
    is built in a temp directory under one of the suite's own artifact prefixes, so the
    session hygiene fixture in conftest.py covers it, and it is torn down either way.
    """

    def _plant(self, tmp):
        for name in (RULEBOOK, "alpha", "beta"):
            os.makedirs(os.path.join(tmp, name))

    def test_a_folder_that_is_its_own_checkout_is_not_one_of_the_packs_skills(self):
        with tempfile.TemporaryDirectory(prefix="livespec-test-skillcount-") as tmp:
            self._plant(tmp)
            os.makedirs(os.path.join(tmp, "external-canon", ".git"))
            unfenced = len([n for n in os.listdir(tmp)
                            if os.path.isdir(os.path.join(tmp, n))]) - 1
            self.assertEqual(
                3, unfenced,
                "the layout must be one the fence actually changes, or this proves nothing",
            )
            self.assertEqual(2, working_skill_count(tmp))

    def test_the_worktree_spelling_of_a_checkout_is_fenced_too(self):
        """A worktree writes `.git` as a FILE; install.sh's `[ -e ]` covers both spellings."""
        with tempfile.TemporaryDirectory(prefix="livespec-test-skillcount-") as tmp:
            self._plant(tmp)
            os.makedirs(os.path.join(tmp, "external-worktree"))
            with open(os.path.join(tmp, "external-worktree", ".git"), "w") as fh:
                fh.write("gitdir: /elsewhere/.git/worktrees/external\n")
            self.assertEqual(2, working_skill_count(tmp))

    def test_an_ordinary_skill_folder_is_still_counted(self):
        """The fence must not empty the count — a rule that excludes everything is no rule."""
        with tempfile.TemporaryDirectory(prefix="livespec-test-skillcount-") as tmp:
            self._plant(tmp)
            self.assertEqual(2, working_skill_count(tmp))
            self.assertFalse(is_external_skill(tmp, "alpha"))

    def test_the_real_tree_reads_the_same_number_either_way(self):
        """On this repository the fence changes the answer only when a clone is installed.

        Stated as an identity rather than a fixed number so the check survives the pack
        gaining or losing a skill: the fenced count equals the raw folder count minus the
        rulebook minus however many external checkouts are actually present.
        """
        folders = [n for n in os.listdir(SKILLS_DIR)
                   if os.path.isdir(os.path.join(SKILLS_DIR, n)) and not n.startswith(".")]
        external = [n for n in folders if is_external_skill(SKILLS_DIR, n)]
        self.assertEqual(len(folders) - 1 - len(external), working_skill_count())


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
        # The section also introduces the external canon, because a reader needs to know it
        # exists — but it is another repository's skill and not one of the pack's. Which
        # entries those are is read from the tracked adapter roster, so this arithmetic is
        # the same on a bare checkout, on a machine with the clone installed, and in CI.
        # Before this, the check silently measured whether the reader had run the installer.
        external = declared_external_skills()
        pack_entries = [e for e in entries if e not in external]
        self.assertEqual(
            len(pack_entries), working_skill_count() + 1,
            "the section lists %d of the pack's own skills (%d entries, %d of them external) "
            "while disk holds %d pack folders under skills/"
            % (len(pack_entries), len(entries), len(entries) - len(pack_entries),
               working_skill_count() + 1))
        # …and it is the SAME set, not merely the same size: an entry renamed, or a skill
        # shipped without an entry, is exactly the drift this section is here to prevent and
        # a count alone would let both through as long as they cancelled out.
        self.assertEqual(
            pack_skill_folders(), set(pack_entries),
            "the section's entries and the pack's skill folders name different sets",
        )
        self.assertEqual(heading.group(1).lower(), NUMBER_WORDS[working_skill_count()],
                         "the heading disagrees with the entries standing under it")


if __name__ == "__main__":
    unittest.main()
