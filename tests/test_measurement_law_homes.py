# -*- coding: utf-8 -*-
"""A number handed to the human carries its method — the law's written homes.

The owner's instruction of 2026-07-29 12:08: a number stated to him, or written into a document,
carries four things — why it is measured, what changes when it moves, its unit, and the method that
produced it. A number stated without those four is a defect.

This rule's one machine was the measurement arm of the PreToolUse scan, retired on 2026-08-17 (the arm
could not prove whose tool call it stopped, JOURNAL.md and PRODUCT_SPEC.md Requirement 295). Its own
tests went with it. These did not: they hold the law's PROSE homes, and those homes are what the rule
now rests on entirely. A retirement that took them too would have left the law with no machine and no
net at once, which is the finding the retirement's review named.
"""
from conftest import read_flat


def test_the_writing_register_states_the_rule():
    body = read_flat("skills/communicator/references/writing-register.md")
    assert "(rule 17)" in body
    assert "A number carries four things" in body
    assert "Its method" in body
    assert "Eighteen rules" in body


def test_the_communicator_body_carries_the_chat_face():
    body = read_flat("skills/communicator/SKILL.md")
    assert "A number is a fact with four parts" in body


def test_the_communicator_body_names_no_machine_for_the_rule():
    """The retirement's own assertion: the chat face must not promise a scan that no longer runs."""
    body = read_flat("skills/communicator/SKILL.md")
    assert "midturn-chat-scan" not in body
    body = read_flat("skills/communicator/references/writing-register.md")
    assert "midturn-chat-scan" not in body


def test_the_decision_record_carries_the_instruction():
    body = read_flat("DECISIONS.md")
    assert "2026-07-29 12:08" in body
    assert "a number is never handed to you on its own" in body
    assert "every decision about how the work runs is written down" in body


def test_the_campaign_plan_carries_the_two_reader_rule():
    body = read_flat("docs/plans/2026-07-28-two-goals-one-campaign.md")
    assert "A place counts as a blocking stop when both readers of one round stopped there" in body
