# -*- coding: utf-8 -*-
"""hooks/midturn-chat-scan.py — the seat's narration is judged at the first boundary after it is written.

On 2026-07-27 ~14:47 the seat wrote a line to the human between two tool calls:

    строка 482 закрыта целиком в архиве, строка 55 честно показывает открытую ногу.

Two offences stand in it. Two queue rows are named by bare number with no plain-word naming of the
wish, which the code-anchor law forbids. And «ногу» is a loan-translation of the pack's internal word
for an acceptance criterion, which the no-calques law forbids.

The Stop-side scan does fire on that exact line. The Stop event arrives when the whole turn ends, so
the human had already read the sentence many minutes earlier. The earliest boundary a hook can reach
after a narration line is the next tool call, which is the PreToolUse event. This scan lives there.

Red-first: written before the hook existed, so every judging case fails on a missing script.
"""
import importlib.util
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "hooks", "midturn-chat-scan.py")
CALQUES = os.path.join(ROOT, "hooks", "chat-calques.json")
FIXTURE_DIR = os.path.join(ROOT, "guardrails", "hook-red-fixtures", "midturn-chat-scan")

LIVE_FAILURE = "строка 482 закрыта целиком в архиве, строка 55 честно показывает открытую ногу."


# ---- harness ---------------------------------------------------------------------------------------

def _write_transcript(path, assistant_texts):
    records = [{"type": "user", "message": {"role": "user", "content": "статус"}}]
    for i, text in enumerate(assistant_texts):
        records.append({
            "type": "assistant",
            "message": {"role": "assistant", "id": "a%d" % i,
                        "content": [{"type": "text", "text": text}]},
        })
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(path)


def _payload(transcript_path, session_id="s-test"):
    return {
        "session_id": session_id,
        "transcript_path": transcript_path,
        "cwd": ROOT,
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "ls"},
    }


def _run_raw(home, stdin_text):
    env = dict(os.environ)
    env["HOME"] = str(home)
    return subprocess.run(["python3", SCRIPT], input=stdin_text,
                          capture_output=True, text=True, env=env)


def _run(tmp_path, texts, session_id="s-test", transcript_name="transcript.jsonl"):
    """One PreToolUse call against a turn carrying `texts`, with $HOME isolated to tmp_path so the
    per-session state file never touches the real home."""
    if isinstance(texts, str):
        texts = [texts]
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    tp = _write_transcript(tmp_path / transcript_name, texts)
    return _run_raw(home, json.dumps(_payload(tp, session_id)))


def _denied(res):
    out = res.stdout.strip()
    if not out:
        return False
    body = json.loads(out).get("hookSpecificOutput", {})
    return body.get("permissionDecision") == "deny"


def _reason(res):
    return json.loads(res.stdout).get("hookSpecificOutput", {}).get("permissionDecisionReason", "")


# ---- the live failure ------------------------------------------------------------------------------

def test_the_live_failure_sentence_denies_the_tool_call():
    """The sentence the human read on 2026-07-27, verbatim, judged at the next tool call."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        import pathlib
        res = _run(pathlib.Path(tmp), LIVE_FAILURE)
        assert _denied(res), res.stdout + res.stderr


def test_deny_carries_the_documented_pretooluse_shape(tmp_path):
    """https://code.claude.com/docs/en/hooks — PreToolUse denies through hookSpecificOutput with
    hookEventName, permissionDecision and permissionDecisionReason, and exits 0. The top-level
    decision/reason pair belongs to other events and must not be used here."""
    res = _run(tmp_path, LIVE_FAILURE)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert set(out.keys()) == {"hookSpecificOutput"}, out
    body = out["hookSpecificOutput"]
    assert body["hookEventName"] == "PreToolUse", body
    assert body["permissionDecision"] == "deny", body
    assert isinstance(body["permissionDecisionReason"], str) and body["permissionDecisionReason"]


def test_reason_names_both_offending_fragments(tmp_path):
    """The reason quotes what was written, so the seat can find the sentence it must repeat."""
    reason = _reason(_run(tmp_path, LIVE_FAILURE))
    assert "482" in reason, reason
    assert "ног" in reason, reason


def test_reason_names_the_plain_replacement_for_the_calque(tmp_path):
    """A calque entry carries the plain industry word the reply should have used, and the deny says it."""
    reason = _reason(_run(tmp_path, LIVE_FAILURE))
    assert "критерий приёмки" in reason or "открытый пункт" in reason, reason


def test_reason_asks_for_the_sentence_in_plain_words_now(tmp_path):
    reason = _reason(_run(tmp_path, LIVE_FAILURE))
    assert "следующем сообщении" in reason or "next message" in reason, reason


# ---- the two counts, separately --------------------------------------------------------------------

def test_naked_queue_row_alone_denies(tmp_path):
    res = _run(tmp_path, "Строки 386 и 412 висят с 18 июля без единого коммита.")
    assert _denied(res), res.stdout


def test_calque_alone_denies(tmp_path):
    res = _run(tmp_path, "У этого требования одна нога приёмки ещё открыта.")
    assert _denied(res), res.stdout


def test_pack_calque_list_covers_the_seven_seeded_words(tmp_path):
    """Each seeded calque fires in the sense the pack uses it."""
    cases = [
        "Проверка краснеет на каждом прогоне.",
        "Эта станция конвейера ещё не готова.",
        "Дверь в пакет — это файл навыка.",
        "Шов между движком и сайтом держит.",
        "Сеть молчит, потому что её никто не включил.",
        "Доска ожидания разрослась до тридцати строк.",
    ]
    for i, text in enumerate(cases):
        res = _run(tmp_path, text, session_id="calque-%d" % i, transcript_name="t%d.jsonl" % i)
        assert _denied(res), (text, res.stdout)


def test_ordinary_russian_passes(tmp_path):
    """The same words in their everyday sense carry no offence and must stay silent."""
    cases = [
        "У стола подломилась ножка, надо чинить.",
        "Он открыл дверь и вышел на улицу.",
        "Рыбак весь вечер чинил сеть.",
        "На доске в коридоре висит расписание.",
        "Поезд подошёл к станции в шесть утра.",
        "Шов на куртке разошёлся по рукаву.",
        "Помидор краснеет на солнце.",
    ]
    for i, text in enumerate(cases):
        res = _run(tmp_path, text, session_id="plain-%d" % i, transcript_name="p%d.jsonl" % i)
        assert not _denied(res), (text, res.stdout)


def test_a_quoted_mention_of_a_calque_passes(tmp_path):
    """Text ABOUT the word carries no offence. This matters most for the correction the hook itself
    asks for, which quotes the calque and its replacement side by side."""
    res = _run(tmp_path, "Слово «открытую ногу» — это калька, здесь надо «критерий приёмки».")
    assert not _denied(res), res.stdout


def test_clean_narration_passes(tmp_path):
    res = _run(tmp_path, "Готово: проверка читаемости берёт фон той поверхности, где лежит цвет.")
    assert not _denied(res), res.stdout


def test_lawful_trailing_anchor_passes(tmp_path):
    res = _run(tmp_path, "Параллельные дорожки висят с 18 июля (строка 386).")
    assert not _denied(res), res.stdout


# ---- the no-block-loop rule ------------------------------------------------------------------------

def test_same_transcript_denies_once_then_passes(tmp_path):
    """The offending text stays in the transcript forever. A fragment is reported once per session;
    every later tool call in that session sees it silently."""
    home = tmp_path / "home"
    home.mkdir()
    tp = _write_transcript(tmp_path / "transcript.jsonl", [LIVE_FAILURE])
    first = _run_raw(home, json.dumps(_payload(tp, "loop-session")))
    assert _denied(first), first.stdout
    second = _run_raw(home, json.dumps(_payload(tp, "loop-session")))
    assert second.stdout.strip() == "", second.stdout


def test_a_fresh_offence_after_a_reported_one_still_denies(tmp_path):
    """Reporting once does not go blind: a NEW offending line later in the same turn still denies."""
    home = tmp_path / "home"
    home.mkdir()
    tp = tmp_path / "transcript.jsonl"
    _write_transcript(tp, [LIVE_FAILURE])
    first = _run_raw(home, json.dumps(_payload(str(tp), "grow-session")))
    assert _denied(first), first.stdout
    _write_transcript(tp, [LIVE_FAILURE, "Строка 777 тоже висит."])
    second = _run_raw(home, json.dumps(_payload(str(tp), "grow-session")))
    assert _denied(second), second.stdout
    assert "777" in _reason(second), _reason(second)


def test_state_is_per_session(tmp_path):
    """A second session judges the same text on its own, since its human never saw the correction."""
    home = tmp_path / "home"
    home.mkdir()
    tp = _write_transcript(tmp_path / "transcript.jsonl", [LIVE_FAILURE])
    first = _run_raw(home, json.dumps(_payload(tp, "session-one")))
    assert _denied(first), first.stdout
    other = _run_raw(home, json.dumps(_payload(tp, "session-two")))
    assert _denied(other), other.stdout


# ---- standing down ---------------------------------------------------------------------------------

def test_unreadable_payload_stands_down(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    res = _run_raw(home, "this is not json")
    assert res.returncode == 0, res.stderr
    assert res.stdout.strip() == "", res.stdout


def test_missing_transcript_stands_down(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    res = _run_raw(home, json.dumps(_payload(str(tmp_path / "nowhere.jsonl"))))
    assert res.returncode == 0, res.stderr
    assert res.stdout.strip() == "", res.stdout


def test_turn_with_no_assistant_text_stands_down(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    tp = tmp_path / "empty.jsonl"
    with open(tp, "w", encoding="utf-8") as f:
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "статус"}}) + "\n")
    res = _run_raw(home, json.dumps(_payload(str(tp))))
    assert res.returncode == 0, res.stderr
    assert res.stdout.strip() == "", res.stdout


# ---- the calque list as data -----------------------------------------------------------------------

def test_calque_file_ships_and_every_entry_carries_its_replacement():
    with open(CALQUES, encoding="utf-8") as f:
        data = json.load(f)
    entries = data["calques"]
    assert len(entries) >= 7, len(entries)
    for entry in entries:
        assert entry["pattern"], entry
        assert entry["say"], entry
        assert entry["note"], entry


def test_calque_file_says_how_the_list_grows():
    with open(CALQUES, encoding="utf-8") as f:
        data = json.load(f)
    assert "one line every time" in data["_comment"], data["_comment"]


# ---- cost ------------------------------------------------------------------------------------------

def _load_module():
    spec = importlib.util.spec_from_file_location("midturn_chat_scan", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_judging_a_realistic_turn_costs_under_a_tenth_of_a_second(tmp_path):
    """It runs before every tool call, so its whole judgment is a regex pass and one small state file."""
    mod = _load_module()
    texts = ["Прошёл шаг конвейера, собрал матрицу, поднял набор тестов и записал результат. " * 6
             for _ in range(200)]
    texts.append(LIVE_FAILURE)
    tp = _write_transcript(tmp_path / "big.jsonl", texts)
    start = time.time()
    hits = mod.judge(mod.read_turn(tp))
    elapsed = time.time() - start
    assert hits, "the seeded offence must still be found in a realistic turn"
    assert elapsed < 0.1, elapsed


# ---- wiring ----------------------------------------------------------------------------------------

def test_wired_as_a_pretooluse_hook():
    with open(os.path.join(ROOT, "guardrails", "judge-hooks.json"), encoding="utf-8") as f:
        decl = json.load(f)
    assert decl["wired"]["midturn-chat-scan"] == "PreToolUse", decl["wired"]
    assert "chat-calques" in decl["library"], decl["library"]


def test_red_proof_and_fixture_ship():
    with open(os.path.join(ROOT, "guardrails", "hook-red-proofs.json"), encoding="utf-8") as f:
        proofs = json.load(f)["proofs"]
    entry = proofs["midturn-chat-scan.py"]
    assert entry["fixture"] == "hook-red-fixtures/midturn-chat-scan", entry
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "payload.json"))
    assert os.path.isfile(os.path.join(FIXTURE_DIR, "transcript.jsonl"))
    with open(os.path.join(FIXTURE_DIR, "transcript.jsonl"), encoding="utf-8") as f:
        assert LIVE_FAILURE in f.read()


def test_install_script_ships_and_wires_it():
    with open(os.path.join(ROOT, "scripts", "install-pack-hooks.sh"), encoding="utf-8") as f:
        body = f.read()
    assert "midturn-chat-scan.py" in body
    assert "chat-calques.json" in body
    assert 'wire("PreToolUse", "midturn-chat-scan.py"' in body


def test_any_failure_of_its_own_stands_down(tmp_path):
    """SPEC R295.7: a check at the tool boundary never stops the session's work. A transcript path
    pointing at a directory raises inside the reader; the hook must still exit 0 and print nothing."""
    payload = {"transcript_path": str(tmp_path), "session_id": "boom", "hook_event_name": "PreToolUse"}
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert p.stdout.strip() == "", p.stdout
