"""Row 313: the status-report format Alexander asked for, captured in the communicator skill.

He wants one unified emoji legend across every done/remaining report — ✅ done · 🔄 in progress
(naming the pipeline step) · ⏳ remaining/queued · ⚠️ needs the human's word · ⏱ time/estimate ·
📖 docs — so the emoji carry the state and plain words carry the content. And when a PLAN is
reported, each step names whether it can run in PARALLEL and, when known, which MODEL tier does the
work (opus/sonnet/haiku/Fable). This test pins both additions in the shipped communicator SKILL.md.
"""

import os
import unittest

from conftest import ROOT, read_flat

SKILL_REL = os.path.join("skills", "communicator", "SKILL.md")


class TestUnifiedReportFormat(unittest.TestCase):
    def test_unified_emoji_legend_present(self):
        flat = read_flat(SKILL_REL)
        for needle in (
            "✅ done",
            "🔄 in progress",
            # The plain word carries this. "pipeline station" was the coined form, and the register
            # lint bans a coinage in text a reader meets, which a skill body is (2026-08-05).
            "name the pipeline step",
            "⏳",
            "remaining/queued",
            "⚠️ needs the human's word",
            "⏱ time/estimate",
            "📖 docs",
        ):
            self.assertIn(
                needle, flat,
                "communicator SKILL.md missing a piece of the unified report legend: %r" % needle,
            )

    def test_legend_states_emoji_carry_state_words_carry_content(self):
        flat = read_flat(SKILL_REL)
        self.assertIn(
            "the emoji carry the state, plain words carry the content", flat,
            "communicator SKILL.md dropped the emoji-vs-words split for the unified legend",
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
