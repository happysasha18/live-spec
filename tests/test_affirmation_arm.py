# -*- coding: utf-8 -*-
"""hooks/affirmation-scan.py — empty affirmation and validation aimed at the user is banned.

F4 (2026-07-27 prover record): affirmation-scan.py ships to every adopter through
scripts/install-pack-hooks.sh (JUDGE_FILES; the host wires it since 2026-08-17), with one red fixture in
guardrails/hook-red-proofs.json and no test module of its own. Every sibling scan carries a
dedicated module holding both directions — the hedge arm (tests/test_hedge_arm.py). A Stop hook that blocks every turn is paid for
by the human on the FALSE-POSITIVE direction most of all, so that direction gets the larger share
of cases here.

This module tests the script's ACTUAL behaviour as read from hooks/affirmation-scan.py, not a
wished-for behaviour. Two disagreements with that behaviour are reported in the delegation's final
summary rather than fixed here, per the brief: this file must not change the hook.
"""
import importlib.util
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "hooks")
SCRIPT = os.path.join(HOOKS, "affirmation-scan.py")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


afm = _load(SCRIPT, "affirmation_scan")

# The committed overlay-format list — mirrors ~/.claude/hooks/affirmation-personal.json's content,
# the personal layer's own file this build self-installs. The RU cases are asserted against a
# compiled copy of this exact list, independent of whatever machine's overlay happens to be live
# (the same discipline tests/test_hedge_arm.py's RU_OVERLAY_PATTERNS holds).
RU_OVERLAY_PATTERNS = [
    r"ты\s+(был[аи]?\s+)?(прав|права|неправ|не\s+прав)",
    r"вы\s+(были\s+)?правы",
    r"тво[йяе]\s+интуици\w*",
    r"интуици\w*\s+(верн|бьёт|тебя\s+не\s+подвел|в\s+точку)",
    r"бьёт\s+в\s+точку",
    r"\bв\s+точку\b",
    r"(хорош|отличн|прекрасн|верн|точн|справедлив|резонн|дельн)\w*\s+(вопрос|замечани|наблюдени|мысл|иде|подмечено|подметил|удар)",
    r"верно\s+подмечено",
    r"честнее,?\s+чем\s+на\s+глаз",
    r"а\s+не\s+(обсуждать|говорить|решать)\s+на\s+глаз",
    r"\bсогласен\b",
    r"\bрезонно\b",
    r"спасибо\s+за\s+(удар|фидбек|фидбэк|обратн|замечани|поправк|подсказк)",
    r"\bокупил\w*",
    r"оправдал[ао]?\s+себя",
    r"\bне\s+зря\b",
    r"принес\w*\s+плоды",
    r"дал[ао]?\s+плоды",
    r"сработал[ао]?\s+как\s+надо",
]


def _fires(text, patterns):
    return bool(afm.find_hits(text, patterns))


def _universal():
    return [re.compile(p, re.IGNORECASE) for p in afm.PATTERNS]


# ---- The firing direction: several distinct English phrasings, against the shipped universal tier ---

def test_universal_english_affirmations_fire():
    """Each is a distinct phrasing of the banned frame — praising the human, his question, his
    intuition, or the exchange — read straight off the shipped PATTERNS list."""
    universal = _universal()
    cases = [
        "You're absolutely right, the bug is in the parser.",
        "You are totally right about the timing.",
        "You're not wrong about the regression.",
        "You're onto something with that theory.",
        "That's a great question.",
        "Good catch — the regression is real.",
        "Spot-on, the vendor is cheaper by 18%.",
        "Well spotted, that was the bug.",
        "Exactly right, the parser was the issue.",
        "Your intuition was right on this one.",
    ]
    missed = [t for t in cases if not _fires(t, universal)]
    assert not missed, "these English affirmations did not fire: %s" % missed


# ---- The firing direction: Russian, via the personal-overlay mechanism -------------------------------

def test_russian_affirmations_fire_via_the_personal_overlay():
    """The universal tier is English-only by design (the docstring's own "UNIVERSAL tier holds the
    language-neutral English validation phrases" line); Russian validation reaches the hook only
    through the optional overlay. These fire against the committed overlay-format list above."""
    ru_patterns = [re.compile(p, re.IGNORECASE) for p in RU_OVERLAY_PATTERNS]
    cases = [
        "Ты был прав насчёт бага в парсере.",
        "Хороший вопрос, стоит проверить это дальше.",
        "Согласен, это стоило усилий.",
        "Твоя интуиция верна.",
        "Верно подмечено — тест был неполным.",
    ]
    missed = [t for t in cases if not _fires(t, ru_patterns)]
    assert not missed, "these Russian affirmations did not fire against the overlay list: %s" % missed
    # And the same text must NOT fire against the universal-only tier — the overlay is what carries it.
    universal = _universal()
    assert not _fires(cases[0], universal), "a Russian phrase must not fire on the English-only tier"


def test_personal_overlay_loads_and_falls_back_silently(tmp_path, monkeypatch):
    """Missing or malformed overlay falls back to universal-only, silently (the docstring's own
    contract), mirroring the shape hedge-scan's and scissors-scan's overlay carve-out holds."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    overlay = home / ".claude" / "hooks" / "affirmation-personal.json"
    overlay.write_text(json.dumps(["ты\\s+молодец"]), encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    assert afm._load_personal_patterns() == ["ты\\s+молодец"]

    # missing overlay -> silently []
    monkeypatch.setenv("HOME", str(tmp_path / "no-overlay-home"))
    assert afm._load_personal_patterns() == []

    # malformed overlay (not JSON) -> silently []
    bad_home = tmp_path / "bad-home"
    (bad_home / ".claude" / "hooks").mkdir(parents=True)
    (bad_home / ".claude" / "hooks" / "affirmation-personal.json").write_text(
        "not json", encoding="utf-8")
    monkeypatch.setenv("HOME", str(bad_home))
    assert afm._load_personal_patterns() == []

    # not a JSON list -> silently []
    dict_home = tmp_path / "dict-home"
    (dict_home / ".claude" / "hooks").mkdir(parents=True)
    (dict_home / ".claude" / "hooks" / "affirmation-personal.json").write_text(
        json.dumps({"not": "a list"}), encoding="utf-8")
    monkeypatch.setenv("HOME", str(dict_home))
    assert afm._load_personal_patterns() == []


# ---- The false-positive direction: this matters more for a hook that blocks every turn ---------------

def test_plain_factual_replies_are_not_flagged():
    """Information carries no validating clause and must never fire."""
    universal = _universal()
    cases = [
        "The parser throws on line 42 when the input is empty.",
        "The suite takes 8 minutes to run end to end.",
        "Three of the five tests are currently skipped.",
        "The vendor's price is $18 per seat per month.",
    ]
    falsely = [t for t in cases if _fires(t, universal)]
    assert not falsely, "these plain factual replies were falsely flagged: %s" % falsely


def test_agreeing_with_a_fact_is_not_flagged():
    """Confirming a measurement is information, not validation of the human — the case the brief
    names directly: this is a report on the world, not a compliment to the person who said it."""
    text = "That measurement is correct, the suite takes 8 minutes."
    assert not _fires(text, _universal()), "confirming a fact was misread as affirmation"


def test_quoting_a_banned_phrase_to_talk_about_it_is_not_flagged():
    """Demonstrating the banned frame inside «guillemets», "double quotes", `backticks`, or a fenced
    ``` block is talk ABOUT the phrase, not a live instance — the docstring's own stated carve-out."""
    universal = _universal()
    cases = [
        'The rule bans phrases like «you\'re absolutely right» in replies.',
        'The rule bans phrases like "you\'re absolutely right" in replies.',
        "The rule bans phrases like `you're absolutely right` in replies to the user.",
        "The banned frame looks like this:\n```\nYou're absolutely right, great catch.\n```\nDon't send it.",
    ]
    falsely = [t for t in cases if _fires(t, universal)]
    assert not falsely, "quoted/fenced demonstrations were falsely flagged: %s" % falsely


# ---- The boundary the docstring states: only the LAST assistant message is read -----------------------

def _transcript(tmp_path, msgs):
    p = tmp_path / "t.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for role, txt in msgs:
            if role == "user":
                rec = {"type": "user", "message": {"role": "user", "content": txt}}
            else:
                rec = {"type": "assistant",
                       "message": {"role": "assistant", "id": "m%d" % id(txt),
                                   "content": [{"type": "text", "text": txt}]}}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def _run(payload):
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True)


def test_affirmation_in_an_early_narration_line_reds(tmp_path):
    """The whole turn is read, so an affirmation in an early narration line reds like one in the final
    reply — the reach every sibling hook took at the row-482 fix, which this one had missed. The human
    reads those narration lines as they stream, so a hook blind to them ships the offence untouched."""
    tp = _transcript(tmp_path, [
        ("user", "go"),
        ("assistant", "You're absolutely right, great catch."),
        ("assistant", "Done — the fix is merged."),
    ])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    assert r.stdout.strip(), "an affirmation in an early narration line must fire, the whole turn being read"


def test_docstring_boundary_the_final_message_still_fires(tmp_path):
    """The mirror case: a clean earlier message, an affirming final message — the final one is what
    the human reads and it must fire."""
    tp = _transcript(tmp_path, [
        ("user", "go"),
        ("assistant", "One moment."),
        ("assistant", "You're absolutely right, great catch."),
    ])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"


def test_stop_hook_active_stands_down(tmp_path):
    """Never loop: a prior stop-hook already fired this turn stands the arm down."""
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", "You're absolutely right.")])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": True})
    assert r.stdout.strip() == ""


def test_end_to_end_block_carries_the_reason_and_suppresses_output(tmp_path):
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", "You're absolutely right, good catch.")])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"
    assert decision["suppressOutput"] is True
    assert "AFFIRMATION CHECK" in decision["reason"]
