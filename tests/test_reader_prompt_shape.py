"""The standing reader-prompt and the pages that describe it state one shape (ROADMAP row 516).

WHY THIS TEST EXISTS. The prompt handed to a reader who meets a text with no context lives in
`skills/text-audit/SKILL.md`. Two other places describe that same prompt: the skill's own prose,
which tells a maintainer what the reader does, and `docs/language-defects.md`, which records how a
reading is run. On 2026-07-28 those three drifted: the prompt asked for four parts per stop and said
"Do not guess the missing answer", while the record page said a reading carries the guess the reader
made, and the class-into-rule procedure needed that guess. A blind reader caught the contradiction
after it had stood for two repair rounds. Bringing the prompt into step then left two sentences in
the skill and its README still saying the reader guesses nothing, which the craft review caught.

WHAT THIS HOLDS. The prompt asks for five parts, the fourth being the reader's guess. The skill's own
prose and its README agree that the reader records that guess. The record page names the same five
parts. Any future edit that changes one of the four homes without the others reds here.

Reach: this test opens `skills/text-audit/SKILL.md`, `skills/text-audit/README.md`, and
`docs/language-defects.md`, and reads their prose. It runs no script and reads no other file.
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "text-audit", "SKILL.md")
README = os.path.join(ROOT, "skills", "text-audit", "README.md")
RECORD = os.path.join(ROOT, "docs", "language-defects.md")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class TestReaderPromptShape(unittest.TestCase):
    def test_the_prompt_asks_for_five_parts(self):
        body = read(SKILL)
        self.assertIn("write one entry with five parts", body,
                      "the reader-prompt in %s no longer states five parts" % SKILL)

    def test_the_fourth_part_is_the_reader_s_guess(self):
        body = read(SKILL)
        self.assertRegex(body, r"4\.\s+the guess you made in place of the missing answer",
                         "the prompt's fourth part no longer asks for the reader's guess")

    def test_the_prompt_asks_for_no_repair(self):
        body = read(SKILL)
        self.assertIn("Do not fix anything.", body,
                      "the prompt stopped telling the reader to fix nothing")

    def test_no_home_still_says_the_reader_guesses_nothing(self):
        # The sentence the settlement retired. It stood in the skill and in its README after the
        # prompt already asked for the guess, which is the drift this test exists to catch.
        stale = re.compile(r"guess(es)? no answers")
        for path in (SKILL, README):
            self.assertIsNone(stale.search(read(path)),
                              "%s still says the reader guesses no answers" % path)

    def test_the_skill_prose_says_the_reader_records_the_guess(self):
        for path in (SKILL, README):
            body = read(path)
            self.assertIn("writes down the guess it made in place of a missing answer", body,
                          "%s does not say the reader records its guess" % path)

    def test_the_record_page_names_the_same_five_parts(self):
        body = read(RECORD)
        for part in ("the phrase", "the guess"):
            self.assertIn(part, body,
                          "%s no longer names the reading entry's %s" % (RECORD, part))
        self.assertIn("skills/text-audit/SKILL.md", body,
                      "%s no longer names where the standing prompt lives" % RECORD)


if __name__ == "__main__":
    unittest.main()
