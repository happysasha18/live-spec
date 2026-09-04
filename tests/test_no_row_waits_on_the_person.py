"""A row's own done-when never names the person as the check.

The pack's rule is that what needs the person's judgement is asked as a question in the reply: it
is never a task, and never a row's definition of done (rulebook rule 36). That ban had no reader —
it was prose, and prose is what rotted the last time. This is the reader.

It looks only at the part of a row that says when the row is finished, so a row may still record in
its Source line that the person asked for it, and may still quote him in its body. What it refuses
is a row whose finish condition is somebody looking at it.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from plan_checks import parse_tasks  # noqa: E402

# The finish condition goes by two names in this tree; both are read.
_DONE_HEAD = re.compile(r"^\*\*(Done when|Acceptance)[:*]", re.I)
# A person as the check. Deliberately narrow: a pronoun or "the owner" standing next to a word for
# looking or approving. "The owner asked for this" is not a match; "his own eye is the check" is.
_PERSON_IS_THE_CHECK = re.compile(
    r"\b(his|her|their|the owner'?s?|the human'?s?)\s+"
    r"(own\s+)?(word|eye|eyes|read|look|verdict|approval|sign-?off|blessing|judgement|judgment)\b"
    r"|\bawait(s|ing)?\s+(his|her|their|the owner|the human)\b"
    r"|\bneeds?\s+(his|her|their|the owner'?s?|the human'?s?)\s+(word|eye|eyes|approval)\b",
    re.I,
)


# A citation is not a finish condition. "His word, 2026-09-03: one row, not two" records who decided
# a scope question; "his own eye is the check" makes a person the finish condition. The two read alike
# to a pattern and mean opposite things, so a match that a date follows is provenance and is passed
# over. Found by a worker on 2026-09-04, when restoring a row's own text tripped this reader.
_PROVENANCE_AFTER = re.compile(r"^[,:]?\s*(of\s+)?\d{1,4}[-.]\d{1,2}([-.]\d{1,4})?", re.I)


def _is_provenance(line, match):
    return bool(_PROVENANCE_AFTER.match(line[match.end():]))


def _finish_lines(body):
    """The lines under the row's finish heading, up to the next bold heading."""
    out, inside = [], False
    for line in body:
        if _DONE_HEAD.match(line.strip()):
            inside = True
            out.append(line)
            continue
        if inside:
            if line.strip().startswith("**") or line.strip().startswith("### "):
                inside = False
                continue
            out.append(line)
    return out


class TestNoRowWaitsOnThePerson(unittest.TestCase):
    def test_no_open_row_makes_a_person_its_finish_condition(self):
        text = (ROOT / "PLAN.md").read_text(encoding="utf-8")
        offenders = []
        for task in parse_tasks(text):
            if task["mark"] == "✅":
                continue
            for line in _finish_lines(task["body"]):
                m = _PERSON_IS_THE_CHECK.search(line)
                if m and not _is_provenance(line, m):
                    offenders.append("%s: %s" % (task["id"], line.strip()[:120]))
        self.assertFalse(
            offenders,
            "a row's finish condition names a person looking at it. What needs their judgement is "
            "asked as a question in the reply; it is never what makes a row done (rulebook rule "
            "36). Rewrite the finish condition as something a command or a reader can settle, or "
            "drop the row: %s" % offenders,
        )

    def test_the_reader_catches_the_shape_it_is_written_for(self):
        """The pattern fires on the real phrasings this tree used to carry, and stays quiet on a
        Source line naming the same person.

        Red-proven against the tree's own history rather than by assertion: run over `PLAN.md` at
        `ead4a705`, this reader catches q-166, whose acceptance read "No command decides this one;
        his own eye is the check." That row is closed today, which is why the live check is green.
        An earlier, blunter version of this pattern also caught two rows there whose lines were
        notes about who had ruled on something; passing over provenance dropped both, which is the
        narrowing working rather than coverage lost."""
        fires = [
            "**Done when:** his own eye is the check on the rendered page.",
            "**Acceptance:** awaiting his word on which sketch to build.",
            "**Done when:** the page ships and needs his approval.",
        ]
        quiet = [
            "**Source:** owner 2026-09-04 — he asked for the pass over every skill.",
            "**Acceptance:** one row, not two. His word, 2026-09-03: splitting it helps nobody.",
            "**Done when:** the suite is green and the record names a different seat.",
            "**Done when:** a reader who did not build it can tell finished from unfinished.",
        ]
        for line in fires:
            self.assertTrue(_PERSON_IS_THE_CHECK.search(line), line)
        for line in quiet:
            m = _PERSON_IS_THE_CHECK.search(line)
            self.assertTrue(m is None or _is_provenance(line, m), line)


if __name__ == "__main__":
    unittest.main()
