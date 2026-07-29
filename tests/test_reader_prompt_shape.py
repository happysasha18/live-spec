"""The standing reader-prompt and the pages that describe it state one shape (ROADMAP row 516).

WHY THIS TEST EXISTS. The prompt handed to a reader who meets a text with no context lives in
`skills/text-audit/references/reader-prompt.md`, where the skill's 2026-07-29 split moved it from the
skill body. Two other places describe that same prompt: the skill's own prose,
which tells a maintainer what the reader does, and `docs/language-defects.md`, which records how a
reading is run. On 2026-07-28 those three drifted: the prompt asked for four parts per stop and said
"Do not guess the missing answer", while the record page said a reading carries the guess the reader
made, and the class-into-rule procedure needed that guess. A blind reader caught the contradiction
after it had stood for two repair rounds. Bringing the prompt into step then left two sentences in
the skill and its README still saying the reader guesses nothing, which the craft review caught.

The settlement on 2026-07-28 was to stop restating the shape in a fourth place. `docs/language-defects.md`
now points at the skill and states no parts of its own, so the shape has one home and cannot drift into
a second reading of itself. That page still relies on the guess, in the step where a stop becomes a
rule, so the test holds the pointer and holds the restatement gone.

WHAT THIS HOLDS. The prompt asks for five parts, the fourth being the reader's guess. The skill's own
prose and its README agree that the reader records that guess. The record page names the skill as the
prompt's home and restates none of the five parts. Any future edit that changes one of these homes
without the others fails here.

Reach: this test opens `skills/text-audit/SKILL.md`, `skills/text-audit/references/reader-prompt.md`,
`skills/text-audit/README.md`, and `docs/language-defects.md`, and reads their prose. It runs no script
and reads no other file.
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "text-audit", "SKILL.md")
PROMPT = os.path.join(ROOT, "skills", "text-audit", "references", "reader-prompt.md")
README = os.path.join(ROOT, "skills", "text-audit", "README.md")
RECORD = os.path.join(ROOT, "docs", "language-defects.md")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class TestReaderPromptShape(unittest.TestCase):
    def test_the_prompt_asks_for_five_parts(self):
        body = read(PROMPT)
        self.assertIn("write one entry with five parts", body,
                      "the reader-prompt in %s no longer states five parts" % PROMPT)

    def test_the_fourth_part_is_the_reader_s_guess(self):
        body = read(PROMPT)
        self.assertRegex(body, r"4\.\s+the guess you made in place of the missing answer",
                         "the prompt's fourth part no longer asks for the reader's guess")

    def test_the_prompt_asks_for_no_repair(self):
        body = read(PROMPT)
        self.assertIn("Do not fix anything.", body,
                      "the prompt stopped telling the reader to fix nothing")

    def test_the_skill_body_points_at_the_prompt_s_file(self):
        # The split left the body as the reader's way in, so the body names the file the prompt
        # moved to. A body that stops naming it strands the loop's second step.
        self.assertIn("references/reader-prompt.md", read(SKILL),
                      "%s no longer points at the file holding the reader-prompt" % SKILL)

    def test_no_home_still_says_the_reader_guesses_nothing(self):
        # The sentence the settlement retired. It stood in the skill and in its README after the
        # prompt already asked for the guess, which is the drift this test exists to catch.
        stale = re.compile(r"guess(es)? no answers")
        for path in (SKILL, PROMPT, README):
            self.assertIsNone(stale.search(read(path)),
                              "%s still says the reader guesses no answers" % path)

    def test_the_skill_prose_says_the_reader_records_the_guess(self):
        for path in (SKILL, README):
            body = read(path)
            self.assertIn("writes down the guess it made in place of a missing answer", body,
                          "%s does not say the reader records its guess" % path)

    def test_the_record_page_points_at_the_prompt_s_one_home(self):
        body = read(RECORD)
        self.assertIn("skills/text-audit/SKILL.md", body,
                      "%s no longer names where the standing prompt lives" % RECORD)

    def test_the_record_page_restates_none_of_the_five_parts(self):
        # A second statement of the shape is what drifted before. The page may use the guess; it may
        # not list the parts again.
        body = read(RECORD)
        for restatement in ("five things", "the phrase the reader stopped on",
                            "whether the stop blocked"):
            self.assertNotIn(restatement, body,
                             "%s restates the reading entry's shape (%r); the shape's one home is %s"
                             % (RECORD, restatement, SKILL))

    def test_the_record_page_still_relies_on_the_guess(self):
        self.assertIn("including the guess the reader made", read(RECORD),
                      "%s no longer carries the guess into the step that opens a rule" % RECORD)


if __name__ == "__main__":
    unittest.main()
