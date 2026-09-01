"""A skill's rule states itself; the journal carries who said it and when (q-803).

Alexander, 2026-09-01 13:15: "какая нафиг разница? ты видел что в спеках пишут 'его слова' или 'не
его слова'? это может где-то в журнале если надо, это бред... это мусор в самой спеке!" A sweep
found the pattern pack-wide: a `SKILL.md` or `references/*.md` rule citing "his word, DATE" or
"owner's word, DATE" as its own source duplicates a job `JOURNAL.md` and `DECISIONS.md` already do,
in documents meant to be read purely operationally.

NOT EVERY HIT IS THE SAME DEFECT. "blocked on his word alone" (communicator/SKILL.md) is not a
citation of where a rule came from — it names a live piece of runtime behaviour, the rule itself.
Only a hit that pairs the phrase with a date is the inline-provenance-citation defect this check
reds on; a bare "his word" with no date beside it is read as the behavioural-actor sense and left
alone, matching this row's own acceptance line: "none of it citing a date as the rule's own
source."

ONE NAMED EXEMPTION: `skills/communicator/references/rule-histories.md`. Its own opening line
states its purpose — "this file is read when a rule's ORIGIN is wanted... and not before" — it is
already the document built to hold this pack's dated citations, scoped to one skill the way
JOURNAL.md is scoped to the whole project. Stripping "his word, DATE" out of a file whose entire
job is recording "his word, DATE" would not move the fact anywhere; it would delete it. No other
file in the reach carries that same self-declared purpose.
"""

import glob
import os
import re
import unittest

from conftest import ROOT

PHRASE = re.compile(r"\bhis word\b|\bhis words\b|owner[’']s word\b", re.IGNORECASE)
DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")

EXEMPT_FILES = {
    os.path.join(ROOT, "skills", "communicator", "references", "rule-histories.md"),
}


def _reach():
    files = sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")))
    files += sorted(glob.glob(os.path.join(ROOT, "skills", "*", "references", "*.md")))
    return [f for f in files if f not in EXEMPT_FILES]


class TestNoInlineProvenanceCitation(unittest.TestCase):
    def test_no_skill_rule_cites_a_date_as_its_own_his_word_or_owners_word_source(self):
        violations = []
        for path in _reach():
            with open(path, encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    if PHRASE.search(line) and DATE.search(line):
                        violations.append(f"{os.path.relpath(path, ROOT)}:{lineno}: {line.strip()}")
        self.assertEqual(
            [],
            violations,
            "inline provenance citation still in skill rule prose (move the fact to "
            "JOURNAL.md or DECISIONS.md, then strip the citation): " + "; ".join(violations),
        )

    def test_the_exemption_still_exists_and_still_declares_its_own_purpose(self):
        # A guard against the exemption quietly outliving its own justification: if this file
        # stops naming itself as the origin record, the exemption above stops being warranted.
        for path in EXEMPT_FILES:
            self.assertTrue(os.path.isfile(path), path)
            with open(path, encoding="utf-8") as f:
                body = f.read()
            self.assertIn("this file is read when a rule's ORIGIN is wanted", body)


if __name__ == "__main__":
    unittest.main()
