"""Every landed feature-or-refactor row carries its footprint note, and a suite check reads the queue — M-275 (SPEC INV-134, row 291).

INV-128 (row 259) states the three-source footprint read and defers the mechanical enforcement to the
follow-on rows. This is that enforcement — the mechanical floor under the footprint read, built to the
same shape the delegation-accounting check (INV-103) gives the routing rule. Beyond the string needles on
the law's homes, the ROADMAP scan is the check itself: a feature-or-refactor row landed once the
impact-analysis station was law (2026-07-12 ~17:01, when INV-128 landed) must carry a `footprint:` note.
Rows that landed before the read was law stay as they landed.
"""

import glob
import os
import re
import unittest

from conftest import ROOT, open_spec, read_flat


def _queue_lines():
    """Every line of the live queue AND its archives — the union scanned so a landed feature/refactor
    row holds in both eras: pre-conversion in the queue's own body, now attic/ROADMAP.md, post-conversion moved to
    docs/queue-archive/*.md under the live-body law (SPEC INV-276, ROADMAP row 480)."""
    files = [os.path.join(ROOT, "attic", "ROADMAP.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "docs", "queue-archive", "*.md")))
    for path in files:
        with open(path, encoding="utf-8") as f:
            for line in f:
                yield line

# Capture the landed date and, when present, the ~HH:MM time-of-day of the stamp.
LANDED = re.compile(r"\*\*landed (20\d\d-\d\d-\d\d)(?:[^|]*?~(\d\d):(\d\d))?", re.IGNORECASE)
DOOR = re.compile(r"door:\s*([a-z-]+)", re.IGNORECASE)
# The note itself — `footprint: <value>` — not the bare word, which prose uses freely.
FOOTPRINT_NOTE = re.compile(r"footprint:\s*(presentation-only|single-module|cross-cutting)", re.IGNORECASE)
BINDS_FROM_DATE = "2026-07-12"      # the day the footprint read became law
BINDS_FROM_TIME = (17, 1)          # INV-128 (row 259) landed ~17:01 that day
ENFORCED_DOORS = ("feature", "refactor")

# The cutoff-day feature/refactor rows that landed BEFORE the impact-analysis station
# became law (INV-128, commit d1bb6c4, 2026-07-12 17:07) and so carry no footprint note by
# right. Each carries no ~HH:MM stamp, so a bare timestamp cannot place it before or after the
# law — its landing ORDER does, read from the commit that added its landed status, every one
# earlier than d1bb6c4:
#   row 242 — 270edb6 (2026-07-12 02:20)   ·   row 274 — 0692931 (2026-07-12 10:39)
#   row 275 — 48204a8 (2026-07-12 11:00)   ·   row 276 — 0cfa0d7 (2026-07-12 10:48)
# A cutoff-day feature/refactor row with no time that is NOT in this pinned pre-law set is
# treated as REQUIRED (fail-closed), so a forward no-time row can no longer silently escape.
PRE_LAW_NO_TIME_ROWS = frozenset({"242", "274", "275", "276"})


def _required(date, hm, rownum=None):
    """A feature-or-refactor row owes a footprint note once the impact-analysis station was
    law. Later dates always owe it; on the cutoff day a stamped row owes it iff stamped at or
    after INV-128's landing time. A cutoff-day row with NO parseable time no longer escapes on
    the missing time alone: it is placed by its landing ORDER — exempt only when it is one of
    the pinned genuinely-pre-law rows, otherwise required (fail-closed)."""
    if date > BINDS_FROM_DATE:
        return True
    if date == BINDS_FROM_DATE:
        if hm is not None:
            return hm >= BINDS_FROM_TIME
        # No parseable time: place the row by its landing ORDER, not the absent stamp — exempt
        # only when it is one of the pinned genuinely-pre-law rows, otherwise required.
        return rownum not in PRE_LAW_NO_TIME_ROWS
    return False


class TestFootprintNoteLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md",)

    def test_law_in_the_spec(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "A landed feature-or-refactor row carries its footprint note, held by a suite check",
            "reddens a landed feature-or-refactor row that carries no footprint note",
            "the mechanical floor under the footprint read",
            "INV-134",
        ):
            self.assertIn(needle, spec, "SPEC INV-134 lost the enforcement clause: %s" % needle)

    def test_spec_index_row(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
        # "footprint" prose is asserted against the spec body in test_law_in_the_spec.
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-134 |"):
                    self.assertIn("R44.1", line)
                    return
        self.fail("INV-134 Formal-index row missing")

    def test_plan_template_carries_the_footprint_field(self):
        tmpl = read_flat("templates/PLAN.template.md")
        self.assertIn("footprint", tmpl.lower(),
                      "the PLAN row template does not name the footprint field")
        for fp in ("presentation-only", "single-module", "cross-cutting"):
            self.assertIn(fp, tmpl, "template lost the footprint value: %s" % fp)

    def test_capture_echo_carries_the_footprint_field(self):
        cm = read_flat("skills/communicator/SKILL.md")
        self.assertIn("the footprint the three-source read named", cm,
                      "communicator's capture echo (rule 12) lost the footprint field")

    def test_every_forward_landed_feature_row_carries_the_note(self):
        checked = 0
        for line in _queue_lines():
            m = LANDED.search(line)
            if not m:
                continue
            date = m.group(1)
            hm = (int(m.group(2)), int(m.group(3))) if m.group(2) else None
            cells = line.split("|")
            rownum = cells[1].strip() if len(cells) > 1 else ""
            status = next((c for c in cells if re.search("landed", c, re.IGNORECASE)), "")
            d = DOOR.search(status)
            door = d.group(1).lower() if d else ""
            if door not in ENFORCED_DOORS:
                continue
            if not _required(date, hm, rownum):
                continue
            self.assertRegex(
                status,
                FOOTPRINT_NOTE,
                "landed-forward feature/refactor row missing its footprint note: " + line[:70],
            )
            checked += 1
        self.assertGreater(checked, 0, "no forward-landed feature/refactor rows found to scan (body or archive)")

    def test_missing_time_cutoff_day_row_does_not_escape(self):
        """A cutoff-day feature/refactor row with no ~HH:MM stamp no longer escapes the footprint
        requirement on the missing time alone. A forward (not-pre-law) no-time row is REQUIRED
        (fail-closed); the pinned genuinely-pre-law rows stay exempt; after the cutoff day every
        row is required regardless of time (SPEC INV-134's mechanism, hardened)."""
        # a forward cutoff-day no-time row (not in the pre-law set) is required — the escape closed
        self.assertTrue(_required(BINDS_FROM_DATE, None, "999"),
                        "a forward no-time cutoff-day feature/refactor row must not silently escape")
        # each pinned genuinely-pre-law row stays exempt (landed before INV-128's commit)
        for pre_law in sorted(PRE_LAW_NO_TIME_ROWS):
            self.assertFalse(_required(BINDS_FROM_DATE, None, pre_law),
                             "a genuinely-pre-law no-time row (%s) must stay exempt" % pre_law)
        # a stamped cutoff-day row still keys off its time; after the day, always required
        self.assertTrue(_required(BINDS_FROM_DATE, (17, 1), "999"), "17:01 cutoff-day row is required")
        self.assertFalse(_required(BINDS_FROM_DATE, (2, 20), "999"), "an early stamped row is exempt")
        self.assertTrue(_required("2026-07-13", None, "999"), "after the cutoff day, always required")


if __name__ == "__main__":
    unittest.main()
