"""Row 313: the status-report format Alexander asked for, captured in the communicator skill.

He wants one unified emoji legend across every done/remaining report. A 2026-08-27 review found
that legend living in three homes with three different mark sets — the exact drift behind his
repeated "отчет должен быть всегда последовательным" complaint. Commit 0a00fb18 converged it:
communicator's rule 9 no longer restates its own six-mark legend, it points at the one canonical
home, `~/.claude/playbook/CLAUDE.md`'s "How a reply to him looks" section, and says plainly that
the vocabulary is not repeated here. Rule 9 keeps only what stays genuinely its own job — when to
show a report, and the pipeline-step vocabulary a report's in-work lines name. This test pins the
pointer and the no-second-legend statement, plus the surviving pipeline-step vocabulary. And when a
PLAN is reported, each step names whether it can run in PARALLEL and, when known, which MODEL tier
does the work (opus/sonnet/haiku/Fable) — pinned by the sibling test below.
"""

import os
import unittest

from conftest import ROOT, read_flat

SKILL_REL = os.path.join("skills", "communicator", "SKILL.md")


class TestUnifiedReportFormat(unittest.TestCase):
    def test_unified_emoji_legend_present(self):
        flat = read_flat(SKILL_REL)
        for needle in (
            # Points at the one canonical home for the mark vocabulary, rather than restating it.
            "lives in one home",
            "~/.claude/playbook/CLAUDE.md",
            "How a reply to him looks",
            "It is not repeated here",
            # Rule 9 still names its own genuinely-owned vocabulary: the pipeline steps a
            # reported in-work line names.
            "names its pipeline step",
            "spec → prove → architecture",
        ):
            self.assertIn(
                needle, flat,
                "communicator SKILL.md missing a piece of the report-legend pointer or its "
                "surviving pipeline-step vocabulary: %r" % needle,
            )
        # The six-mark legend itself moved out; communicator must not carry a second, competing
        # definition of what the marks mean (the exact drift the 2026-08-27 review closed).
        self.assertNotIn(
            "✅ done · 🔄 in progress", flat,
            "communicator SKILL.md restates the mark legend inline — it should only point at "
            "the one canonical home",
        )

    def test_plan_step_parallel_and_model_annotation_present(self):
        flat = read_flat(SKILL_REL)
        for needle in (
            "reported PLAN",
            "runs in PARALLEL",
            "MODEL tier",
            "opus for judgment",
            "sonnet for mechanical work",
            "haiku for a one-shot",
            "Fable only for the hard passes",
        ):
            self.assertIn(
                needle, flat,
                "communicator SKILL.md missing the plan-step parallel/model annotation rule: %r" % needle,
            )


if __name__ == "__main__":
    unittest.main()
