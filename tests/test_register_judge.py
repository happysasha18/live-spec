# -*- coding: utf-8 -*-
"""The register judge holds the class a literal list cannot (ROADMAP rows 416+418, SPEC INV-203).

A register law that names a CLASS is held by a model that reads meaning; a list of literal patterns holds
only the instances someone thought of. This module red-proves both surfaces of that law:

  - CHAT (416): four empty intensifiers pass the literal scissors list untouched, and the judge reds them.
    A flat informative sentence passes both. A turn holding many messages is gathered whole, so an offence
    in an early inter-tool message reds — the PLACE fix as well as the KIND fix.
  - DOCUMENT (418): a Russian fixture carrying pack coinages as calques passes the literal preshow list,
    and the judge reds it.

The judge makes a live model call, so nothing here depends on a live `claude` binary. The mechanism's
PARSE / VALIDATE / DECISION logic is driven against canned model responses; the stand-down is driven by
faking a missing binary; the literal-list passes are real and deterministic.

Red-first: before hooks/register_judge_core.py exists, this module fails to import — that is the red.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(REPO, "hooks")
SCRIPTS = os.path.join(REPO, "scripts")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, HOOKS)
core = _load(os.path.join(HOOKS, "register_judge_core.py"), "register_judge_core")
judge_hook = _load(os.path.join(HOOKS, "register-judge.py"), "register_judge_hook")
lint = _load(os.path.join(SCRIPTS, "preshow-register-lint.py"), "preshow_register_lint")
scissors = _load(os.path.join(HOOKS, "scissors-scan.py"), "scissors_scan")


# SYNTHETIC personal-overlay stand-ins (privacy fix 2026-07-17): the owner's real personal scissors
# patterns are NOT reproduced in this shipped, soon-public test. These neutral placeholders exercise the
# SAME matching path — a personal overlay of extra literal patterns layered onto the universal scissors
# set — without shipping anyone's private register bank. They mirror the two shapes the real overlay
# carries, a contrast-by-denial frame and a praising-the-reader frame, in made-up vocabulary. The proof
# they carry is the MECHANISM (find_hits over a universal set plus a personal overlay), which needs no
# real personal phrase.
SCISSORS_PERSONAL = [
    r",\s+alpha\s+not\s+\S",           # a synthetic contrast-by-denial frame
    r"\bwidget\s+beats\s+gadget\b",    # a synthetic "X over Y" frame
    r"\bsharp\s+observation\b",        # a synthetic praise-the-reader phrase
    r"\bexactly\s+right,\s+you\b",     # another synthetic praise-the-reader phrase
]


def _full_literal_list():
    return [re.compile(p) for p in scissors.PATTERNS] + [re.compile(p) for p in SCISSORS_PERSONAL]


def _literal_hits(text):
    return scissors.find_hits(text, _full_literal_list())


# The four phrases the row probed — empty intensifiers that carry no fact.
FOUR_INTENSIFIERS = ["по-настоящему", "реально", "на самом деле", "действительно"]


# ---- KIND (416): the four intensifiers pass the list, red under the judge --------------------------

@pytest.mark.parametrize("phrase", FOUR_INTENSIFIERS)
def test_intensifier_passes_the_literal_list(phrase):
    """Each probed intensifier walks the literal list (universal frame + a synthetic personal overlay)
    untouched — the list's own gap that the class-reading judge exists to close."""
    sentence = "Это %s важный шаг для проекта, и мы его сделали." % phrase
    assert _literal_hits(sentence) == [], "the literal list should NOT catch %r" % phrase


def test_personal_overlay_patterns_are_exercised():
    """The synthetic overlay stand-ins DO fire on their own demo, proving the personal-overlay matching
    path actually runs — the test covers the mechanism without any real personal phrase."""
    assert _literal_hits("This is a sharp observation about the mix.") != []
    assert _literal_hits("The widget beats gadget in this run.") != []


@pytest.mark.parametrize("phrase", FOUR_INTENSIFIERS)
def test_intensifier_reds_under_the_judge(phrase):
    """The judge, handed the model's verdict, reds each intensifier the list let through."""
    sentence = "Это %s важный шаг для проекта, и мы его сделали." % phrase
    canned = json.dumps({"offences": [{"quote": sentence, "law": 2, "why": "intensifier, no fact"}]})
    offences, error = core.parse_offences(canned, sentence)
    assert error is None
    assert len(offences) == 1 and offences[0]["quote"] == sentence


def test_flat_informative_sentence_passes_both():
    """A plain sentence carrying a fact passes the literal list and draws an empty verdict from the judge."""
    sentence = "Suite is 921 tests green and the three judge arms are wired in settings.json."
    assert _literal_hits(sentence) == []
    offences, error = core.parse_offences('{"offences": []}', sentence)
    assert error is None and offences == []


# ---- the bare-code-lead universal law (base rule 2, "never open a line with a code") ----------------

def test_universal_law_carries_the_bare_code_class():
    """The universal chat law names the bare-code-opening class, not only the scissors frame."""
    law = core.UNIVERSAL_CHAT_LAW
    assert "no bare internal code opening a sentence" in law
    # it names what a code is and that a TRAILING anchor is the pass case
    assert "an invariant code" in law and "TRAIL" in law


def test_renumber_laws_makes_a_single_sequence():
    """A universal block joined to a personal overlay (each numbered from its own base) renumbers to one
    unbroken 1..N sequence, so the judge cites no duplicate number. The universal block's law count is
    read from the block itself: it is generated from the rule home, and a rule added to the chat surface
    raises it. Pinning the count here once red-ed this test for a rule that had simply been added."""
    universal_count = len(re.findall(r"LAW \d+ —", core.UNIVERSAL_CHAT_LAW))
    assert universal_count >= 4, "the universal chat law lost laws: %d" % universal_count
    personal = "LAW 2 — synthetic personal one.\n\nLAW 3 — synthetic personal two."
    combined = core.UNIVERSAL_CHAT_LAW + "\n\n" + personal
    heads = re.findall(r"LAW (\d+) —", core.renumber_laws(combined))
    assert heads == [str(n) for n in range(1, universal_count + 3)], heads
    alone = re.findall(r"LAW (\d+) —", core.renumber_laws(core.UNIVERSAL_CHAT_LAW))
    assert alone == [str(n) for n in range(1, universal_count + 1)], alone


def test_chat_law_body_is_sequentially_numbered():
    """The assembled chat law (universal + whatever personal overlay is installed) carries no duplicate
    law number."""
    heads = re.findall(r"LAW (\d+) —", judge_hook.chat_law())
    assert heads == [str(i) for i in range(1, len(heads) + 1)], heads


def test_bare_code_lead_reds_under_the_judge():
    """The judge, handed the model's verdict, reds a chat sentence opening with a bare internal code."""
    sentence = "INV-237 is the new invariant and the release pass now runs from a clean context."
    canned = json.dumps({"offences": [{"quote": sentence, "law": 2, "why": "code leads the sentence"}]})
    offences, error = core.parse_offences(canned, sentence)
    assert error is None
    assert len(offences) == 1 and offences[0]["quote"] == sentence


def test_trailing_anchor_sentence_passes_the_judge():
    """A sentence that opens in plain words and only TRAILS its anchor draws an empty verdict."""
    sentence = "The release pass now runs from a clean context (INV-237)."
    offences, error = core.parse_offences('{"offences": []}', sentence)
    assert error is None and offences == []


# ---- The broadened universal classes: grading worth, and an unglossed coined/jargon term ------------
# The audit's worked instance (2026-07-19): the judge caught "с сильным результатом" this session but let
# a graded THOUGHT («сильная мысль») and a graded RHYME («красивая рифма») through, and let an unglossed
# jargon term («развилки») reach the reader. The narrow reading ("grades how important a RESULT is") is
# one instance; the class is grading importance OR quality of ANYTHING with no fact, and any coined/jargon
# term shown with no plain gloss. The universal law must name both classes, not the scissors/bare-code
# pair alone.

# Praise that grades worth with no fact behind it — a strong thought, a beautiful rhyme, far better.
GRADING_FIXTURE = "Это сильная мысль, и рифма красивая — в разы лучше прежнего."
# A coined/jargon term dropped into chat with no plain gloss — «развилки» where the reader never met it.
UNGLOSSED_FIXTURE = "Здесь у нас развилки, дальше пойдём по первой."


def test_universal_chat_law_carries_the_grading_worth_class():
    """The universal chat law names grading importance/quality WITHOUT a concrete fact as a class, so a
    graded thought or rhyme reds like a graded result — not the narrow 'a result' phrasing alone. (RED
    before the fix: the universal law named only the scissors and bare-code classes.)"""
    law = core.UNIVERSAL_CHAT_LAW.lower()
    assert "grad" in law and ("importance" in law or "quality" in law or "worth" in law)
    assert "fact" in law


def test_universal_chat_law_carries_the_unglossed_term_class():
    """The universal chat law names a coined/jargon term shown with no plain gloss as a class, so an
    unglossed «развилки» in chat reds. (RED before the fix.)"""
    law = core.UNIVERSAL_CHAT_LAW.lower()
    assert "gloss" in law and ("jargon" in law or "coined" in law)


def test_grading_worth_reds_under_the_judge():
    """Handed the model's verdict, the judge reds a graded-worth chat sentence the narrow list missed."""
    canned = json.dumps({"offences": [{"quote": GRADING_FIXTURE, "law": 3, "why": "grades worth, no fact"}]})
    offences, error = core.parse_offences(canned, GRADING_FIXTURE)
    assert error is None and len(offences) == 1 and offences[0]["quote"] == GRADING_FIXTURE


def test_unglossed_term_reds_under_the_judge():
    """Handed the model's verdict, the judge reds an unglossed coined/jargon term shown in chat."""
    canned = json.dumps({"offences": [{"quote": UNGLOSSED_FIXTURE, "law": 4, "why": "coined term, no gloss"}]})
    offences, error = core.parse_offences(canned, UNGLOSSED_FIXTURE)
    assert error is None and len(offences) == 1 and offences[0]["quote"] == UNGLOSSED_FIXTURE


# ---- PLACE (416): a turn holding many messages reds on the one that offends -------------------------

def _transcript(tmp_path, messages):
    """messages: list of (role, text). Writes a JSONL transcript and returns its path."""
    p = tmp_path / "transcript.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for role, text in messages:
            if role == "user":
                rec = {"type": "user", "message": {"role": "user", "content": text}}
            else:
                rec = {"type": "assistant",
                       "message": {"role": "assistant", "id": "m%d" % id(text),
                                   "content": [{"type": "text", "text": text}]}}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def test_turn_gathers_every_message_not_only_the_last(tmp_path):
    """The offence sits in an EARLY inter-tool message; the last message is clean. turn_text must still
    hold the offending line, so the judge sees it — proving PLACE, not only KIND."""
    offending = "Это по-настоящему меняет ход работы над задачей."
    path = _transcript(tmp_path, [
        ("user", "поехали"),
        ("assistant", offending),                    # early, between tool calls
        ("assistant", "Промежуточный шаг выполнен."),
        ("assistant", "Готово, тесты зелёные."),      # the LAST message is clean
    ])
    gathered = judge_hook.turn_text(path)
    assert offending in gathered, "the whole turn must be gathered, not the last message alone"
    # the old last-message-only read would have missed it:
    assert "Готово, тесты зелёные." in gathered


def _realistic_transcript(tmp_path, records):
    """Write raw record dicts as JSONL — for turns that carry tool_use / tool_result records, which the
    simple (role, text) helper cannot express."""
    p = tmp_path / "realistic.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def test_turn_boundary_skips_tool_result_user_records(tmp_path):
    """In a real Claude Code transcript EVERY tool result is a type:"user" record. Walking back to the
    last type:"user" record lands ON a tool_result, so turn_text would read only the clean text AFTER the
    last tool call and miss an offence earlier in the turn. The boundary is the real HUMAN user record,
    which carries human text rather than a tool_result. (RED before the skip: the offence is excluded.)"""
    offending = "Это по-настоящему меняет ход работы над задачей."
    path = _realistic_transcript(tmp_path, [
        {"type": "user", "message": {"role": "user", "content": "поехали"}},          # the real human turn
        {"type": "assistant", "message": {"role": "assistant", "id": "a1",
                                          "content": [{"type": "text", "text": offending}]}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a2",
                                          "content": [{"type": "tool_use", "id": "t1",
                                                       "name": "Bash", "input": {"command": "ls"}}]}},
        {"type": "user", "message": {"role": "user",                                    # a TOOL RESULT, not a human turn
                                     "content": [{"type": "tool_result", "tool_use_id": "t1",
                                                  "content": "file.txt"}]}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a3",
                                          "content": [{"type": "text", "text": "Готово, тесты зелёные."}]}},
    ])
    gathered = judge_hook.turn_text(path)
    assert offending in gathered, "the human-turn boundary must skip the tool_result user record"
    assert "Готово, тесты зелёные." in gathered


def test_turn_scopes_to_the_current_turn(tmp_path):
    """Only assistant text AFTER the last human message is this turn's output."""
    path = _transcript(tmp_path, [
        ("user", "first"),
        ("assistant", "prior turn reply that should be out of scope"),
        ("user", "second"),
        ("assistant", "this turn's reply"),
    ])
    gathered = judge_hook.turn_text(path)
    assert "this turn's reply" in gathered
    assert "prior turn" not in gathered


# ---- The mechanism: parse / validate / stand-down ---------------------------------------------------

def test_hallucinated_quote_is_dropped():
    """A quote the model invents that is not verbatim in the text is no evidence."""
    offences, error = core.parse_offences(
        '{"offences":[{"quote":"a line never written","law":1,"why":"x"}]}', "the real text")
    assert error is None and offences == []


def test_trivially_short_quote_is_rejected():
    """A hallucinated offence quoting a trivial substring like "the" is no evidence — substring-only
    validation would keep it, so a minimum meaningful length floor drops it. (RED: currently kept.)"""
    text = "the quick brown fox jumps over the lazy dog and keeps on running"
    canned = json.dumps({"offences": [{"quote": "the", "law": 1, "why": "x"}]})
    offences, error = core.parse_offences(canned, text)
    assert error is None and offences == []


def test_long_offence_recovered_when_model_truncates_over_the_cap(tmp_path):
    """A real offending sentence longer than the quote cap forces the model to truncate and append an
    ellipsis; the truncated+ellipsis string is not a verbatim substring, so substring-only validation
    DROPS a real offence. The fix recovers the longest verbatim leading span. (RED: currently dropped.)"""
    offending = "Это " + "очень " * 25 + "важный и по-настоящему длинный вывод о проекте."
    text = "Начало разговора. " + offending + " Конец."
    truncated = offending[:100].rstrip() + "…"      # what a capped model returns for a long sentence
    canned = json.dumps({"offences": [{"quote": truncated, "law": 2, "why": "intensifier, no fact"}]})
    offences, error = core.parse_offences(canned, text)
    assert error is None
    assert len(offences) == 1, "a genuine long offence must not be dropped over the quote cap"
    assert offences[0]["quote"] in text, "the kept quote is a verbatim span of the text"
    assert len(offences[0]["quote"]) >= 40


def test_unreadable_shape_stands_down():
    offences, error = core.parse_offences("I could not comply", "the real text")
    assert offences == [] and error is not None


def test_code_fence_is_stripped():
    offences, error = core.parse_offences('```json\n{"offences": []}\n```', "the real text")
    assert error is None and offences == []


def test_judge_stands_down_when_no_binary(monkeypatch):
    """No claude on PATH stands the judge down with an error, never a block on its own breakage."""
    def _boom(*a, **k):
        raise FileNotFoundError("no claude")
    monkeypatch.setattr(core.subprocess, "run", _boom)
    offences, error = core.judge("some text here", core.UNIVERSAL_CHAT_LAW)
    assert offences == [] and "no claude binary" in error


def test_judge_stands_down_on_nonzero_exit(monkeypatch):
    def _fail(*a, **k):
        return subprocess.CompletedProcess(a, 1, stdout="", stderr="boom")
    monkeypatch.setattr(core.subprocess, "run", _fail)
    offences, error = core.judge("some text here", core.UNIVERSAL_CHAT_LAW)
    assert offences == [] and error is not None


# ---- The universal/personal law split (SPEC INV-173) -----------------------------------------------

def test_universal_chat_law_ships_and_names_the_scissors_frame():
    assert "not Y" in core.UNIVERSAL_CHAT_LAW or "а не" in core.UNIVERSAL_CHAT_LAW


def test_personal_law_overlay_rides_the_personal_layer(tmp_path):
    """The personal laws (empty intensifier, grading the person) load from an overlay the personal layer
    owns; a missing overlay falls back to universal-only, silently."""
    assert core.load_personal_law(path=str(tmp_path / "absent.md")) == ""
    overlay = tmp_path / "register-judge-personal.md"
    overlay.write_text("LAW 2 — no empty intensifier.\nLAW 3 — no grading the person.", encoding="utf-8")
    body = core.load_personal_law(path=str(overlay))
    assert "empty intensifier" in body and "grading the person" in body


def test_chat_law_composes_universal_plus_personal(monkeypatch, tmp_path):
    overlay = tmp_path / "register-judge-personal.md"
    overlay.write_text("LAW 2 — no empty intensifier.", encoding="utf-8")
    monkeypatch.setattr(core.os.path, "expanduser", lambda p: str(overlay)
                        if "register-judge-personal" in p else os.path.expanduser(p))
    law = judge_hook.chat_law()
    assert "not Y" in law or "а не" in law          # universal present
    assert "empty intensifier" in law               # personal appended


# ---- DOCUMENT (418): the Russian calque fixture passes the list, reds under the judge ---------------

# A calque of pack coinages ("wish door", "pipeline stations") — a machine-dialect leak the literal list
# never listed in Russian. The audit's worked instance.
RU_CALQUE_FIXTURE = "Брось пожелание в дверь желаний, и оно само пройдёт конвейер по станциям."


def test_document_calque_passes_the_literal_list():
    """The fixture carries the pack's coinages as Russian calques; the literal preshow list misses it."""
    assert lint.scan(RU_CALQUE_FIXTURE) == [], "the literal list should NOT catch the calque fixture"


def test_document_calque_reds_under_the_judge():
    canned = json.dumps({"offences": [
        {"quote": RU_CALQUE_FIXTURE, "law": 1, "why": "calque of an internal coinage"}]})
    offences, error = core.parse_offences(canned, RU_CALQUE_FIXTURE)
    assert error is None and len(offences) == 1


def test_document_judge_is_opt_in_and_stands_down(monkeypatch):
    """Off by default so the suite and push gate stay deterministic; on, it stands down on breakage."""
    monkeypatch.delenv("PRESHOW_REGISTER_JUDGE", raising=False)
    assert lint.judge_document(RU_CALQUE_FIXTURE) == []      # disabled -> empty
    monkeypatch.setenv("PRESHOW_REGISTER_JUDGE", "1")
    monkeypatch.setattr(core.subprocess, "run",
                        lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    # even enabled, a missing binary stands it down without raising
    assert lint.judge_document(RU_CALQUE_FIXTURE) == []


def test_document_law_ships():
    assert "calque" in core.DOCUMENT_REGISTER_LAW and "reader" in core.DOCUMENT_REGISTER_LAW


# ---- The growth duty is RETRACTED (418) ------------------------------------------------------------

def test_growth_duty_retracted_in_the_lint_docstring():
    src = open(os.path.join(SCRIPTS, "preshow-register-lint.py"), encoding="utf-8").read()
    assert "GROWS BY ONE per caught leak" not in src
    assert "grows by NOBODY's duty" in src or "grows by nobody's duty" in src.lower()


def test_inv94_no_longer_commands_per_catch_list_growth():
    """INV-83's growth duty is retracted, so INV-94 must not still ORDER each caught phrase to join the
    literal pattern family — an imperative per-catch growth command in both its homes (the prose and the
    Formal index). The judge holds the class; a caught phrase informs it without a standing append duty."""
    spec = open(os.path.join(REPO, "PRODUCT_SPEC.md"), encoding="utf-8").read()
    assert "joins the register lint's pattern family" not in spec
    # INV-94's actual subject stays intact.
    assert "No line certifies its own sincerity" in spec


def test_growth_duty_retracted_in_the_spec():
    spec = open(os.path.join(REPO, "PRODUCT_SPEC.md"), encoding="utf-8").read()
    # INV-83's paragraph no longer commands the list to grow per leak.
    assert "The set grows by one per caught leak" not in spec
    assert "grows by nobody" in spec.lower()


# ---- Wiring: the pack installer ships the judge (SPEC INV-173) --------------------------------------

def test_pack_installer_ships_the_judge_arms_unwired():
    """The installer places all three files and wires neither arm: both went opt-in on 2026-08-17
    (PRODUCT_SPEC.md Requirement 311), so a host adds them to its own settings.json."""
    src = open(os.path.join(SCRIPTS, "install-pack-hooks.sh"), encoding="utf-8").read()
    assert "register-judge-collect.sh" in src
    assert "register-judge-report.sh" in src
    assert "register_judge_core.py" in src
    assert "wire(" not in src
