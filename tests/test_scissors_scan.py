# -*- coding: utf-8 -*-
"""scissors-scan reads EVERY assistant message shown since the last human turn, not only the last one
(row 482) — the same reach hooks/register-judge.py already has via turn_reader.turn_text.

Red-first: before the fix, scissors-scan.py read only the LAST assistant message
(last_assistant_text), so a contrast frame sitting in an earlier narration line within the same turn
slipped past undetected. This module proves the mid-turn frame IS now caught, and a frame from a
PRIOR turn (before the last human record) stays out of scope — the same turn boundary
register-judge.py already holds.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "hooks")
SCRIPT = os.path.join(HOOKS, "scissors-scan.py")


def _write_transcript(tmp_path, records):
    p = tmp_path / "transcript.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def _run(payload):
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True)


def test_mid_turn_contrast_frame_is_detected(tmp_path):
    """A contrast frame sitting in an early narration line, followed by a tool-result record and a
    clean final reply, must still be caught — the whole turn is read, not the last message alone."""
    records = [
        {"type": "user", "message": {"role": "user", "content": "do the thing"}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a1",
                                          "content": [{"type": "text",
                                                       "text": "I will run the check, not the full build."}]}},
        {"type": "user", "message": {"role": "user",
                                     "content": [{"type": "tool_result", "tool_use_id": "t1",
                                                  "content": "ok"}]}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a2",
                                          "content": [{"type": "text", "text": "Done."}]}},
    ]
    path = _write_transcript(tmp_path, records)
    r = _run({"transcript_path": path, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"
    assert "not the full build" in decision["reason"]


def test_prior_turn_contrast_frame_is_not_detected(tmp_path):
    """A contrast frame in an assistant message BEFORE the human record (a prior turn) is out of
    scope — only text since the last human turn is read."""
    records = [
        {"type": "assistant", "message": {"role": "assistant", "id": "a0",
                                          "content": [{"type": "text",
                                                       "text": "Earlier reply, not the current one."}]}},
        {"type": "user", "message": {"role": "user", "content": "do the thing"}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a1",
                                          "content": [{"type": "text", "text": "Done."}]}},
    ]
    path = _write_transcript(tmp_path, records)
    r = _run({"transcript_path": path, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    assert r.stdout.strip() == ""
