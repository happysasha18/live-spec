"""Request-layer classifier at the pipeline's door — the closed door set + entry-layer criterion
+ the one-plain-question fallback (INV-151), the deferral-must-justify-itself clause (INV-152), and
the unification stated once (INV-153).

Design settled by the Fable audit (scratchpad fable-prover-vs-designreview-audit.md, sections 6-10),
the companion of the property->review routing that landed the same session (INV-150). String rows on
the shipped homes: the spec clauses, the build-pipeline door step, and the base rulebook.

Every check here declares the input set it reads and reds by name when that set is empty, so a check
whose subject has been reworded away reports the absence (ROADMAP row 384, the vacuous-pass class;
the sibling of the unexpected-skip law, SPEC INV-155). Each home is found by an anchor the prose
cannot reword away — the invariant code itself — since a needle drawn from the prose under test
would travel with the very edit the check exists to catch.
"""

import os
import re
import sys
import unittest

from conftest import ROOT, read, read_flat, read_all, read_all_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


# --- reading a count out of prose ------------------------------------------------------------

_ONES = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen")
_TENS = (None, None, "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")


def _spell(n):
    """The English word for a count from 0 to 99: `4` reads "four", `31` reads "thirty-one"."""
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    if ones == 0:
        return _TENS[tens]
    return "%s-%s" % (_TENS[tens], _ONES[ones])


_WORD_VALUE = {_spell(i): i for i in range(100)}


def _as_number(token):
    """The integer a token names, or None when the token names no number.

    A numeral ("31") and an English number word ("thirty-one") both read; the docs are prose, so
    either spelling is a true statement of the count.
    """
    t = token.strip().lower()
    if t.isdigit():
        return int(t)
    return _WORD_VALUE.get(t)


def _counts_before(word, text):
    """Every number stated immediately before `word` in `text`, as integers.

    A token that names no number is passed over, so "the rules every pack skill works by" yields
    nothing while "thirty-one rules" yields 31. An empty result means the text states no count,
    which each caller reds on by name.
    """
    found = []
    for token in re.findall(r"([A-Za-z0-9-]+)\s+%s\b" % re.escape(word), text):
        n = _as_number(token)
        if n is not None:
            found.append(n)
    return found


def _frontmatter_description(rel):
    """The `description:` field of a skill's YAML frontmatter, whitespace collapsed.

    Returns an empty string when the file carries no frontmatter description, which the caller
    reds on by name.
    """
    text = read(rel)
    block = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not block:
        return ""
    field = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_][A-Za-z0-9_]*:|\Z)",
                      block.group(1), re.S | re.M)
    if not field:
        return ""
    return " ".join(field.group(1).split())


class DocHomeCase(unittest.TestCase):
    """Locators for the homes a code lives in. Each one asserts it found its subject, so a home
    that has been reworded or removed reds by name (ROADMAP row 384)."""

    def declaration(self, path, code):
        """The prose that DECLARES `code` — the whole body of the one requirement section whose
        own acceptance criteria name `code` as the FIRST code in their trailing bracket.

        The new requirements-format spec states one law across a whole requirement (a Context
        paragraph plus several numbered criteria) rather than in one paragraph, and a criterion's
        trailing bracket lists the code it defines first, then any supporting cites — a
        consistent convention confirmed across R45/R56/R212. A neighbouring requirement that only
        CITES this code (never as the first code in its own bracket) is passed over, keeping the
        same anti-vacuous-pass guarantee the old one-paragraph lookup gave: reading only the
        section that actually declares this code, not any place it is merely mentioned.
        """
        import re as _re
        lines = read(path).splitlines()
        owning_starts = set()
        for i, line in enumerate(lines):
            s = line.strip()
            m = _re.match(r"^\d+\.\s.*\[([^\]]+)\]\s*$", s)
            if not m:
                continue
            codes = [c.strip() for c in m.group(1).split(",")]
            if codes and codes[0] == code:
                for j in range(i, -1, -1):
                    if lines[j].startswith("## Requirement "):
                        owning_starts.add(j)
                        break
        self.assertEqual(len(owning_starts), 1,
                         "%s: %d requirement sections declare %s as their own code (first in a "
                         "criterion's bracket); the home is the one section that declares it"
                         % (path, len(owning_starts), code))
        start = owning_starts.pop()
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].strip() == "---" or lines[j].startswith("## Requirement "):
                end = j
                break
        return " ".join(" ".join(lines[start:end]).split())

    def index_row(self, path, code):
        """The one Formal-index row for `code`, with whitespace collapsed."""
        marker = "| %s |" % code
        found = [l for l in read(path).splitlines() if l.startswith(marker)]
        self.assertEqual(len(found), 1,
                         "%s holds %d Formal-index rows for %s; the index carries one row per "
                         "code" % (path, len(found), code))
        return " ".join(found[0].split())

    def code_prose(self, path, code):
        """Every paragraph of a skill's whole surface that cites `code`, joined and collapsed."""
        pattern = re.compile(r"\b%s\b" % re.escape(code))
        found = [l for l in read_all(path).splitlines() if pattern.search(l)]
        self.assertTrue(found, "%s cites %s nowhere on its surface; the home is absent"
                               % (path, code))
        return " ".join(" ".join(found).split())

    def architecture_owner(self, code):
        """The node whose `owns` field (guardrails/archformat.py) lists `code`.

        Anchors are read from the owns field only, ranges expanded to their members. A code that
        appears only in loose prose has no owner and reds here."""
        owners = [n.name for n in archformat.parse_nodes(read("ARCHITECTURE.md"))
                  if code in n.anchors_expanded]
        self.assertEqual(len(owners), 1,
                         "ARCHITECTURE.md gives %s %d owning nodes %s; a code is owned by "
                         "one node's owns field" % (code, len(owners), owners))
        return owners[0]


class TestRequestClassifierEntryLayer(DocHomeCase):
    """INV-151 — a request enters at the highest document its change reaches; the door set is
    closed; a request matching no kind is one plain question."""

    def test_entry_layer_criterion_stands(self):
        """Read inside INV-151's own declaration paragraph. Both phrases live elsewhere in the
        spec as well — in the Formal-index row, and in neighbouring clauses that cite the rule —
        so a whole-file read would stay green with the home clause deleted."""
        clause = self.declaration("PRODUCT_SPEC.md", "INV-151")
        self.assertIn("highest document in the derivation chain", clause)
        self.assertIn("closed on purpose", clause)

    def test_one_plain_question_fallback(self):
        """Read inside INV-151's own declaration paragraph. "one plain question" is stated in
        six places across the spec, so a whole-file read passes off any of them."""
        clause = self.declaration("PRODUCT_SPEC.md", "INV-151")
        self.assertIn("matches no kind", clause)
        self.assertIn("one plain question", clause)

    def test_closed_set_at_the_door(self):
        rk = read_all_flat("skills/director/references/request-kind-table.md")
        self.assertIn("The door set is CLOSED", rk)
        self.assertIn("highest document in the derivation chain", rk)
        self.assertIn("one plain question", rk)
        kinds = [row[0] for row in self._request_kind_rows()]
        for kind in ("product behaviour", "docs-only", "settings", "inbox wish",
                     "method", "sketch", "research", "feedback"):
            self.assertTrue(any(kind in k for k in kinds),
                            "closed-set entry missing at the door: %r; the door names %s"
                            % (kind, kinds))

    def _request_kind_rows(self):
        """The rows of the request-kind table — the home of the closed door set.

        request-kind-table.md moved from build-pipeline/references/ to director/references/ in
        the build-pipeline cutover, so its rows are read via director's surface now.

        Each named kind is checked against the table's kind column. A bare word like "method" or
        "feedback" matches unrelated prose across a large skill surface, so a whole-surface read
        reports the door set complete while the door names none of it. An absent table reds here
        by name."""
        rows = []
        in_table = False
        for line in read_all("skills/director/SKILL.md").splitlines():
            s = line.strip()
            if s.startswith("| Request kind |"):
                in_table = True
                continue
            if not in_table:
                continue
            if not s.startswith("|"):
                break
            if set(s) <= set("|-: "):
                continue
            rows.append([c.strip() for c in s.strip("|").split("|")])
        self.assertTrue(rows, "director states no request-kind table; the closed door set "
                              "has no rows to read")
        return rows

    def test_intake_moment_back_check(self):
        # spec-motion tripwire text lives in request-kind-table.md, moved to director/ in the
        # build-pipeline cutover.
        director = read_all_flat("skills/director/SKILL.md")
        # A phrase unique to the new door-step wiring, so this test is genuinely red
        # before the classifier lands (the bare "at intake" already existed elsewhere).
        self.assertIn("spec-motion tripwire fires", director)
        self.assertIn("lifts it to the spec at the door", director)

    def test_inv151_index_and_ownership(self):
        self.index_row("PRODUCT_SPEC.md", "INV-151")
        self.assertEqual(self.architecture_owner("INV-151"), "build-pipeline")


class TestDeferralJustifiesItself(DocHomeCase):
    """INV-152 — a held work item is re-tested by derivability; a marker that cannot name its
    human-only fact defaults to the seat. Base rulebook home + spec clause."""

    def test_deferral_clause_stands(self):
        """Read inside INV-152's own declaration paragraph; a neighbouring clause states the
        rule again in its own words, so a whole-file read passes off the neighbour."""
        clause = self.declaration("PRODUCT_SPEC.md", "INV-152")
        self.assertIn("A deferral must justify itself", clause)
        self.assertIn("re-tested for derivability every time it is touched", clause)
        self.assertIn("default a marker that cannot name its human-only fact to the seat's own",
                      clause)

    def test_lives_in_the_base_rulebook(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("SPEC INV-152", base)
        self.assertIn("needs-the-human's-word marker", base)

    def test_base_description_counts_the_rule(self):
        """The body is the authority on how many rules it holds, and the frontmatter description
        agrees with it.

        The count is derived from the shape the file gives its rules: a top-level numbered bold
        head, `N. **`, matched at column zero so an indented sub-point is passed over. The heads
        are required to number strictly upward from one; a cut rule leaves its number standing as
        a hole (rule 30, cut by his D2 word 2026-08-11), because every citation keeps pointing at
        the number it names, and the count derives from the heads present.

        Accepted description shape: the count stated immediately before the word "rules", either
        as an English number word ("thirty-one") or as a numeral ("31"); the rest of the sentence
        is free prose. A word before "rules" that names no number is passed over, so "the rules
        every pack skill works by" is never read as a count. A description that states no count
        at all reds by name.

        A rule added to the body without the description following it reds here.
        """
        rel = "skills/live-spec-base/SKILL.md"
        heads = [int(n) for n in re.findall(r"^([0-9]+)\. \*\*", read(rel), re.M)]
        self.assertTrue(heads, "%s states no numbered rule heads (`N. **`), so the rule count "
                               "has nothing to derive from" % rel)
        self.assertEqual(heads[0], 1,
                         "%s opens its rule heads at %d; the body numbers its rules from one"
                         % (rel, heads[0]))
        self.assertEqual(heads, sorted(set(heads)),
                         "%s numbers its rule heads %s; the numbers climb strictly, a cut rule's "
                         "number stays a hole and is never reused" % (rel, heads))
        holes = set(range(1, max(heads) + 1)) - set(heads)
        self.assertLessEqual(holes, {30},
                             "%s skips rule numbers %s; the only recorded cut is rule 30 "
                             "(his D2 word 2026-08-11) — an unrecorded hole is a lost rule"
                             % (rel, sorted(holes)))
        rules = len(heads)

        desc = _frontmatter_description(rel)
        self.assertTrue(desc, "%s carries no frontmatter description to read a rule count from"
                              % rel)
        claimed = _counts_before("rules", desc)
        self.assertTrue(claimed,
                        "the description of %s states no rule count; the body holds %s rules "
                        "(%d) and the description says how many" % (rel, _spell(rules), rules))
        for c in claimed:
            self.assertEqual(c, rules,
                             "the description of %s says %s rules; the body holds %s (%d)"
                             % (rel, _spell(c), _spell(rules), rules))

    def test_inv152_index_and_ownership(self):
        self.index_row("PRODUCT_SPEC.md", "INV-152")
        self.assertEqual(self.architecture_owner("INV-152"), "base-rulebook")


class TestUnificationStatedOnce(DocHomeCase):
    """INV-153 — request, property, work item, and the earned message are one routing principle:
    every incoming thing routes to the home whose declared sentence governs it, and a thing that
    pins to no home is itself the finding."""

    #: The controls the principle unifies: the request classifier, the property net, the deferral
    #: test, and the earned message. The count is a spec-backed literal (SPEC INV-104), so it
    #: travels with every control added to the set.
    CONTROLS = 4

    def test_unification_clause_stands(self):
        clause = self.declaration("PRODUCT_SPEC.md", "INV-153")
        self.assertIn("routes to the home whose declared sentence governs it", clause)
        self.assertIn("pins to no home is itself the finding", clause)

    def test_names_all_four_controls(self):
        clause = self.declaration("PRODUCT_SPEC.md", "INV-153")
        for anchor in ("INV-150", "INV-151", "INV-152", "INV-189", "INV-191"):
            self.assertIn(anchor, clause,
                          "the unification clause does not cite %s" % anchor)

    def test_count_word_tracks_the_control_set(self):
        """The spec's unification clause says how many times the principle is stated; the number
        is a spec-backed literal, so it travels with every control added to the set (SPEC
        INV-104).

        Read inside INV-153's own declaration paragraph. The whole-file read this replaces was
        satisfied by the Formal-index row's copy of the sentence, so the clause could lose its
        count and stay green. The count is read as any count word standing before "times", so the
        check survives a rewording of the sentence around it.
        """
        clause = self.declaration("PRODUCT_SPEC.md", "INV-153")
        stated = _counts_before("times", clause)
        self.assertTrue(stated,
                        "the unification clause states no count of the controls; the set holds "
                        "%s (%d)" % (_spell(self.CONTROLS), self.CONTROLS))
        for n in stated:
            self.assertEqual(n, self.CONTROLS,
                             "the unification clause says the principle is stated %s times; the "
                             "control set holds %s (%d)"
                             % (_spell(n), _spell(self.CONTROLS), self.CONTROLS))

    def test_the_count_agrees_across_its_homes(self):
        """The count of controls lives in two prose homes, and both say the same number.

        Each home is found by the code INV-153, which the prose cannot reword away; the earlier
        shape of this guard keyed on the phrase "routing principle stated", so rewording that
        phrase stopped the guard from running while it went on reporting green.

        A home that carries the code and states no count reds by name, and a home whose count
        differs from the control set reds by name. The number is read as any count word standing
        before "times", so restating "stated four times" as "told four times" leaves the guard
        running.

        The Formal-index row is checked for presence only: the new-format index carries
        locations only (SPEC INV-271), so it no longer duplicates the prose count.
        """
        self.index_row("PRODUCT_SPEC.md", "INV-153")
        homes = {
            "the spec's unification clause": self.declaration("PRODUCT_SPEC.md", "INV-153"),
            "director's request-kind prose": self.code_prose(
                "skills/director/references/request-kind-table.md", "INV-153"),
        }
        for name, text in sorted(homes.items()):
            stated = _counts_before("times", text)
            self.assertTrue(stated,
                            "%s carries INV-153 and states no count of the controls; the set "
                            "holds %s (%d)" % (name, _spell(self.CONTROLS), self.CONTROLS))
            for n in stated:
                self.assertEqual(n, self.CONTROLS,
                                 "%s says the principle is stated %s times; the control set "
                                 "holds %s (%d)"
                                 % (name, _spell(n), _spell(self.CONTROLS), self.CONTROLS))

    def test_inv153_index_and_ownership(self):
        self.index_row("PRODUCT_SPEC.md", "INV-153")
        self.assertEqual(self.architecture_owner("INV-153"), "build-pipeline")


if __name__ == "__main__":
    unittest.main()
