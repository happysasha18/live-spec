# -*- coding: utf-8 -*-
"""A number handed to the human carries its method — the measurement arm of hooks/midturn-chat-scan.py.

The owner's instruction of 2026-07-29 12:08: a number stated to him, or written into a document,
carries four things — why it is measured, what changes when it moves, its unit, and the method that
produced it. A number stated without those four is a defect, and whatever a gate can hold, a gate holds.

The recorded case is the session's own sentence. It reported that a reader returned a count of stops,
and it named neither what a stop is, nor what the count decides, nor how the count was produced. That
sentence is the red fixture below; the same count carrying its four parts is the green one.

Red-first: written against the arm before the arm judged anything, so every judging case here failed on
a hook that returned no finding.
"""
import importlib.util
import json
import os
import subprocess

from conftest import ROOT, read_flat

SCRIPT = os.path.join(ROOT, "hooks", "midturn-chat-scan.py")
FIXTURES = os.path.join(ROOT, "guardrails", "measured-number-fixtures")
BARE = os.path.join(FIXTURES, "bare-number.md")
MEASURED = os.path.join(FIXTURES, "measured-number.md")


def _module():
    spec = importlib.util.spec_from_file_location("midturn_chat_scan", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---- the hook run end to end -----------------------------------------------------------------------

def _write_transcript(path, texts):
    records = [{"type": "user", "message": {"role": "user", "content": "статус"}}]
    for i, text in enumerate(texts):
        records.append({
            "type": "assistant",
            "message": {"role": "assistant", "id": "a%d" % i,
                        "content": [{"type": "text", "text": text}]},
        })
    with open(path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(path)


def _run(tmp_path, text, session_id="measure-test", transcript_name="transcript.jsonl"):
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    tp = _write_transcript(tmp_path / transcript_name, [text])
    payload = {
        "session_id": session_id,
        "transcript_path": tp,
        "cwd": ROOT,
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "ls"},
    }
    env = dict(os.environ)
    env["HOME"] = str(home)
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True, env=env)


def _denied(res):
    out = res.stdout.strip()
    if not out:
        return False
    return json.loads(out).get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def _reason(res):
    return json.loads(res.stdout).get("hookSpecificOutput", {}).get("permissionDecisionReason", "")


# ---- the two proofs --------------------------------------------------------------------------------

def test_the_bare_count_denies_the_tool_call(tmp_path):
    """The red proof: the recorded sentence, run through the real hook."""
    res = _run(tmp_path, _fixture(BARE))
    assert _denied(res), res.stdout + res.stderr


def test_the_same_count_with_its_four_parts_passes(tmp_path):
    """The green proof: the same number, carrying why, what changes, its unit and its method."""
    res = _run(tmp_path, _fixture(MEASURED))
    assert not _denied(res), res.stdout


def test_both_fixtures_ship_beside_the_guardrails(tmp_path):
    assert os.path.isfile(BARE)
    assert os.path.isfile(MEASURED)
    assert "15 стопов" in _fixture(BARE)
    assert "15 стопов" in _fixture(MEASURED)


def test_the_deny_quotes_the_count_and_asks_for_the_four_parts(tmp_path):
    reason = _reason(_run(tmp_path, _fixture(BARE)))
    assert "15 стопов" in reason, reason
    assert "four things" in reason, reason
    assert "method that produced it" in reason, reason
    assert "next message" in reason, reason


# ---- what the arm reads ----------------------------------------------------------------------------

def test_the_arm_is_wired_into_the_hook_s_own_judgment():
    """A finding the hook's judge() never returns is a check nobody runs."""
    module = _module()
    kinds = [f["kind"] for f in module.judge(_fixture(BARE))]
    assert "measure" in kinds, kinds


def test_a_command_in_the_same_paragraph_satisfies_the_method():
    module = _module()
    text = "Перечёт дал 112 документов, команда `python3 scripts/rule-census.py`."
    assert module.judge_measurements(text) == []


def test_a_command_in_another_paragraph_leaves_the_count_bare():
    """The window is the paragraph: a count here and a command three paragraphs on are two statements."""
    module = _module()
    text = "Перечёт дал 112 документов.\n\nОтдельно прогнал `python3 scripts/rule-census.py`."
    findings = module.judge_measurements(text)
    assert [f["fragment"] for f in findings] == ["112 документов"], findings


def test_a_percentage_counts_as_a_measurement():
    module = _module()
    assert module.judge_measurements("Недельный расход дошёл до 82%.")


def test_a_count_inside_a_fenced_block_stays_silent():
    """A fenced block is machine output rather than a sentence to the human."""
    module = _module()
    assert module.judge_measurements("```\n15 стопов\n```") == []


def test_ordinary_numbers_stay_silent():
    """A date, a clock time, a version, and an edit's own tally are no measurements handed over."""
    module = _module()
    for text in [
        "Инструкция пришла 2026-07-29 в 12:08.",
        "Поставил версию 4.3.0 и пошёл дальше.",
        "Правка тронула 3 файла и 40 строк.",
        "Поезд подошёл к станции в шесть утра.",
    ]:
        assert module.judge_measurements(text) == [], text


def test_the_citation_shape_stays_with_the_code_anchor_arm():
    """`row 386` is a citation the code-anchor law owns; this arm reads the mirror shape, `386 rows`."""
    module = _module()
    assert module.judge_measurements("Строка 386 висит с 18 июля.") == []


# ---- the law's prose homes -------------------------------------------------------------------------

def test_the_writing_register_states_the_rule():
    body = read_flat("skills/communicator/references/writing-register.md")
    assert "(rule 17)" in body
    assert "A number carries four things" in body
    assert "Its method" in body
    assert "Seventeen rules" in body


def test_the_communicator_body_carries_the_chat_face():
    body = read_flat("skills/communicator/SKILL.md")
    assert "A number is a fact with four parts" in body
    assert "hooks/midturn-chat-scan.py" in body


def test_the_decision_record_carries_the_instruction():
    body = read_flat("DECISIONS.md")
    assert "2026-07-29 12:08" in body
    assert "a number is never handed to you on its own" in body
    assert "every decision about how the work runs is written down" in body


def test_the_campaign_plan_carries_the_two_reader_rule():
    body = read_flat("docs/plans/2026-07-28-two-goals-one-campaign.md")
    assert "A place counts as a blocking stop when both readers of one round stopped there" in body
