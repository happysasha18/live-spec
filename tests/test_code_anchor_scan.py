# -*- coding: utf-8 -*-
"""hooks/code-anchor-scan.py — an internal code may only trail a sentence as a quiet anchor.

The law is old (base rule 2, SPEC INV-28): plain words carry the meaning in every human-facing
sentence, and internal handles — queue row numbers, INV/M/E/T codes — may only trail in parentheses.
The law had no machine, so it decayed exactly where it costs most: on 2026-07-27 the human was handed
"rows 386 and 412, hanging since 18 July" with no word saying what those wishes are, and he answered
that he does not remember row numbers and cannot tell what is being asked of him.

Red-first: written before the scan existed, so the naked-reference case fails on a missing script.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "hooks", "code-anchor-scan.py")


def _transcript(tmp_path, assistant_text):
    p = tmp_path / "transcript.jsonl"
    records = [
        {"type": "user", "message": {"role": "user", "content": "статус"}},
        {"type": "assistant", "message": {"role": "assistant", "id": "a1",
                                          "content": [{"type": "text", "text": assistant_text}]}},
    ]
    with open(p, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def _run(tmp_path, text):
    payload = {"transcript_path": _transcript(tmp_path, text), "stop_hook_active": False}
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True)


def _blocked(res):
    if not res.stdout.strip():
        return False
    return json.loads(res.stdout).get("decision") == "block"


def test_naked_russian_row_reference_reds(tmp_path):
    """The live failure verbatim: row numbers carrying no plain-word description of the wish."""
    res = _run(tmp_path, "Строки 386 и 412 висят с 18 июля без единого коммита — закрыть или доделать.")
    assert _blocked(res), res.stdout


def test_naked_english_row_reference_reds(tmp_path):
    res = _run(tmp_path, "Row 490 is the next thing I take. Row 483 follows it.")
    assert _blocked(res), res.stdout


def test_naked_invariant_code_reds(tmp_path):
    res = _run(tmp_path, "INV-152 says the item is the seat's own to do, so I did it.")
    assert _blocked(res), res.stdout


def test_trailing_anchor_in_parentheses_passes(tmp_path):
    """The lawful shape: the wish is named in plain words and the code trails in parentheses."""
    text = ("Ветки и рабочие копии для параллельных дорожек висят с 18 июля (строка 386), и открытие "
            "дорожки как шаг конвейера рядом с ними (строка 412).")
    res = _run(tmp_path, text)
    assert not _blocked(res), res.stdout


def test_bracketed_anchor_in_a_document_line_passes(tmp_path):
    res = _run(tmp_path, "The deferral must name its human-only fact [INV-152], and this one does.")
    assert not _blocked(res), res.stdout


def test_table_row_passes(tmp_path):
    """A table gives every number its describing cell, so the number is never naked there."""
    text = "| 490 | the legibility check pairs each colour with its own surface | bug |"
    res = _run(tmp_path, text)
    assert not _blocked(res), res.stdout


def test_code_block_passes(tmp_path):
    text = "```\nrow 490 lives here as sample data\n```"
    res = _run(tmp_path, text)
    assert not _blocked(res), res.stdout


def test_clean_reply_passes(tmp_path):
    res = _run(tmp_path, "Готово: проверка читаемости теперь берёт фон той поверхности, где лежит цвет.")
    assert not _blocked(res), res.stdout


# ---- F6 (2026-07-27 prover record): this repository's own citation idioms, missed --------------------

def test_document_name_citation_reds(tmp_path):
    """'ROADMAP 480' — the document-name-plus-number idiom this repo's own architecture, matrix and
    prover records use daily — is a naked code exactly like 'row 480' and must red the same way."""
    res = _run(tmp_path, "ROADMAP 480 landed last night and the queue is clean.")
    assert _blocked(res), res.stdout


def test_spaced_inv_code_reds(tmp_path):
    """'INV 281' — the code word and its number read aloud, with a space rather than the dash the
    inline pattern required — must red the same as the hyphenated form."""
    res = _run(tmp_path, "INV 281 now reaches the whole turn.")
    assert _blocked(res), res.stdout


def test_hash_row_reference_reds(tmp_path):
    """'row #386' — a hash between the word and the number — must red like the plain 'row 386'."""
    res = _run(tmp_path, "row #386 is still open.")
    assert _blocked(res), res.stdout


# ---- F6: two lawful shapes the scan wrongly reds --------------------------------------------------

def test_russian_file_line_reference_passes(tmp_path):
    """'строке 484 файла PRODUCT_SPEC.md' names a LINE IN A FILE, not a queue row — a plain,
    resolvable fact with no anchor owed. The word 'файла' right after the number is the signal."""
    res = _run(tmp_path, "Ошибка в строке 484 файла PRODUCT_SPEC.md.")
    assert not _blocked(res), res.stdout


def test_parenthetical_anchor_wrapped_across_a_line_passes(tmp_path):
    """A parenthetical anchor broken across a line by wrapping is still the lawful trailing-anchor
    shape — the bracket span must tolerate an embedded newline, not just a single physical line."""
    text = "Both are still open (row 386,\nand row 412 too)."
    res = _run(tmp_path, text)
    assert not _blocked(res), res.stdout


# ---- A6 (2026-07-27 prover addendum): the internal-code patterns match uppercase only --------------
# re.IGNORECASE on the multi-letter (INV|ROW|ACT) and single-letter dash patterns made ordinary
# lowercase English red as an internal code. These four are the false-positive direction the
# addendum named: a step or a play's "act 3", and the letter-dash-digit codes "b-2", "f-16", "c-4".

def test_lowercase_act_as_ordinary_word_passes(tmp_path):
    res = _run(tmp_path, "We open act 3 of the play tonight.")
    assert not _blocked(res), res.stdout


def test_lowercase_b_dash_sample_passes(tmp_path):
    res = _run(tmp_path, "Take the b-2 sample from the second run.")
    assert not _blocked(res), res.stdout


def test_lowercase_f_16_passes(tmp_path):
    res = _run(tmp_path, "An f-16 flew over the base today.")
    assert not _blocked(res), res.stdout


def test_lowercase_c_4_wiring_passes(tmp_path):
    res = _run(tmp_path, "The c-4 wiring is done.")
    assert not _blocked(res), res.stdout


def test_uppercase_row_spaced_reds(tmp_path):
    """The uppercase forms must still fire once the patterns narrow to case-sensitive."""
    res = _run(tmp_path, "ROW 386 is still open.")
    assert _blocked(res), res.stdout


def test_uppercase_act_spaced_reds(tmp_path):
    res = _run(tmp_path, "ACT 3 of the pipeline is where this stands.")
    assert _blocked(res), res.stdout


def test_uppercase_m_dash_code_reds(tmp_path):
    res = _run(tmp_path, "M-458 covers this fact.")
    assert _blocked(res), res.stdout


# ---- S2 (2026-07-27 fold review): three stand-down criteria, pinned by their own tests --------------
# R293.10 and R293.11 shipped in main()'s guards with no test naming them. Each test here pins a
# criterion the fold added but never proved: the stop hook already active, stdin that will not parse,
# and a transcript_path pointing nowhere. Each must stay silent (exit 0, no block) even against text
# that would otherwise red.

def test_stop_hook_already_active_stands_down(tmp_path):
    """R293.10: a naked row reference that would otherwise red must stay silent when the payload
    carries stop_hook_active: true — the scan never runs a second time on the same stop."""
    transcript_path = _transcript(tmp_path, "Row 490 is the next thing I take. Row 483 follows it.")
    payload = {"transcript_path": transcript_path, "stop_hook_active": True}
    res = subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert not res.stdout.strip(), res.stdout


def test_malformed_stdin_stands_down(tmp_path):
    """R293.11: stdin that does not parse as JSON leaves the hook silent with exit 0, never a crash."""
    res = subprocess.run(["python3", SCRIPT], input="not valid json {{{",
                          capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert not res.stdout.strip(), res.stdout


def test_unreadable_transcript_path_stands_down(tmp_path):
    """R293.11: a transcript_path pointing nowhere leaves the hook silent with exit 0 — the turn's
    record cannot be read, so the scan reads no text and blocks nothing."""
    payload = {
        "transcript_path": str(tmp_path / "does-not-exist.jsonl"),
        "stop_hook_active": False,
    }
    res = subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert not res.stdout.strip(), res.stdout
