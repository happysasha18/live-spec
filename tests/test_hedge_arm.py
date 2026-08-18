# -*- coding: utf-8 -*-
"""The hedge gate reds a reply carrying an offering-hedge frame (ROADMAP 429, SPEC INV-238).

An offering-hedge is a sentence that offers to do a thing the seat could already derive and could
already reverse through git, holding the offer open for a cue — "just say the word", "let me know
if you want me to" — instead of doing the thing and reporting it done. This is the machine for the
standing no-only-say-hedge behaviour [profile proactivity.no-only-say-hedge, base rule 29, INV-152].

Modeled exactly on the scissors scan [INV-173]: a literal-pattern Stop-gate, an inline universal
English pattern list plus an optional personal-overlay JSON, a quoted span/backticked span/code
fence stripped before matching so citing a hedge phrase to talk about it never fires it.

Red-first: before hooks/hedge-scan.py exists, this module fails to import — that is the red.
"""
import importlib.util
import glob
import json
import os
import re
import subprocess

from conftest import ROOT

HOOKS = os.path.join(ROOT, "hooks")
FIXTURES = os.path.join(ROOT, "tests", "hedge_fixtures")
SCRIPT = os.path.join(HOOKS, "hedge-scan.py")

# The committed overlay-format list — mirrors ~/.claude/hooks/hedge-personal.json's content, the
# personal layer's own file this build self-installs. The RU fixtures are asserted against a
# compiled copy of this exact list, independent of whatever machine's overlay happens to be live.
RU_OVERLAY_PATTERNS = [
    r"жду\s+(твоего\s+)?слова",
    r"только\s+скажи",
    r"если\s+хочешь,?\s+могу",
    r"дай\s+знать,?\s+если\s+(хочешь|захочешь|нужно)",
    r"скажи\s+слово",
    r"готов[аы]?\b[^.!?\n]{0,40}если\s+(скажешь|захочешь|нужно)",
    r"напиши,?\s+если\s+(нужно|хочешь|захочешь)",
    r"скажешь\s*[—–-]\s*сделаю",
]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hs = _load(SCRIPT, "hedge_scan")


def _fixtures(prefix):
    return sorted(glob.glob(os.path.join(FIXTURES, prefix + "*.txt")))


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _fires(text, patterns):
    return bool(hs.find_hits(text, patterns))


# ---- The measurable proxy: hedges fire, legit questions and quoted demos pass -------------------------

def test_every_hedge_fixture_fires():
    """Every English hedge fixture fires against the inline universal PATTERNS."""
    en_patterns = [re.compile(p, re.IGNORECASE) for p in hs.PATTERNS]
    en_fixtures = [p for p in _fixtures("hedge_") if "_ru_" not in os.path.basename(p)]
    assert len(en_fixtures) >= 8, "one fixture per universal English frame, at least eight"
    missed = [os.path.basename(p) for p in en_fixtures if not _fires(_read(p), en_patterns)]
    assert not missed, "these English hedge fixtures did not fire: %s" % missed

    # The RU fixtures fire against the committed overlay-format pattern list (the personal-layer
    # shape this build self-installs at ~/.claude/hooks/hedge-personal.json).
    ru_patterns = [re.compile(p, re.IGNORECASE) for p in RU_OVERLAY_PATTERNS]
    ru_fixtures = [p for p in _fixtures("hedge_ru_")]
    assert len(ru_fixtures) >= 2, "at least two Russian hedge fixtures"
    missed_ru = [os.path.basename(p) for p in ru_fixtures if not _fires(_read(p), ru_patterns)]
    assert not missed_ru, "these Russian hedge fixtures did not fire: %s" % missed_ru


def test_no_legitimate_question_is_flagged():
    """A genuine taste/policy/irreversible question, a status report, a plain question — none fire."""
    legits = _fixtures("legit_")
    assert len(legits) >= 3
    falsely = [os.path.basename(p) for p in legits if _fires(_read(p), hs._compiled_patterns())]
    assert not falsely, "these legitimate replies were falsely flagged: %s" % falsely


def test_quoted_or_fenced_hedge_is_not_flagged():
    """A hedge phrase quoted in «guillemets», in `backticks`, or in a ``` fence never fires — it is
    talk ABOUT the frame, not a live instance of it."""
    quoted = _fixtures("quoted_")
    assert len(quoted) >= 3
    falsely = [os.path.basename(p) for p in quoted if _fires(_read(p), hs._compiled_patterns())]
    assert not falsely, "these quoted/fenced demonstrations were falsely flagged: %s" % falsely


# ---- Regressions the adversarial audit named (2026-07-20) -----------------------------------------

def test_limitation_sentence_is_not_flagged():
    """A boundary statement ("if you want, I can't force it") must stay green — the `(?!['’]t)`
    after "i can" keeps a limitation off a net built for an OFFER to act. The audit's false red."""
    text = "You can override this in settings if you want, I can't force it."
    assert not _fires(text, hs._compiled_patterns()), "a limitation sentence was falsely flagged"


def test_reversed_and_paraphrase_hedges_fire():
    """The net catches the common frames beyond the exact-forward phrasing: reversed order, the
    'let me know and I'll' frame, and the 'give me a nod' frame. These are not verbatim copies of a
    single inline pattern, so they prove the fixtures are not tautological (the audit's finding 4)."""
    en_patterns = [re.compile(p, re.IGNORECASE) for p in hs.PATTERNS]
    for text in ["I can rename it if you'd like.",
                 "Let me know and I'll update the config.",
                 "The test is ready to add — just give me a nod."]:
        assert _fires(text, en_patterns), "a common hedge paraphrase slipped: %r" % text


# ---- End to end on the Stop event -----------------------------------------------------------------

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


def _run(payload, env=None):
    run_env = dict(os.environ)
    if env:
        run_env.update(env)
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True, env=run_env)


def test_stop_hook_blocks_on_a_hedge(tmp_path):
    hedge = _read(os.path.join(FIXTURES, "hedge_just_say_word.txt"))
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", "One moment."), ("assistant", hedge)])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"
    assert decision["suppressOutput"] is True


def test_stop_hook_is_silent_on_a_clean_reply(tmp_path):
    clean = _read(os.path.join(FIXTURES, "legit_status_report.txt"))
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", clean)])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_stop_hook_active_stands_down(tmp_path):
    """Never loop: a prior stop-hook already fired this turn stands the arm down."""
    hedge = _read(os.path.join(FIXTURES, "hedge_just_say_word.txt"))
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", hedge)])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": True})
    assert r.stdout.strip() == ""


def test_reads_the_whole_turn_not_only_the_last_message(tmp_path):
    """The arm reads EVERY assistant message shown since the last human turn (row 482), not the last
    one alone — a hedge sitting in an earlier narration line reds even when the final reply is clean."""
    hedge = _read(os.path.join(FIXTURES, "hedge_just_say_word.txt"))
    tp = _transcript(tmp_path, [("user", "go"), ("assistant", hedge),
                                ("assistant", "Done — the gate is wired and the suite is green.")])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.returncode == 0
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block", "a hedge in an earlier narration line must still fire"


def test_prior_turn_hedge_is_out_of_scope(tmp_path):
    """A hedge sitting in an assistant message BEFORE the last human record (a prior turn) is out of
    scope — only text since the last human turn is read."""
    hedge = _read(os.path.join(FIXTURES, "hedge_just_say_word.txt"))
    tp = _transcript(tmp_path, [("assistant", hedge), ("user", "go"),
                                ("assistant", "Done — the gate is wired and the suite is green.")])
    r = _run({"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": False})
    assert r.stdout.strip() == "", "a hedge from a prior turn must not fire on this turn's stop"


# ---- The personal overlay --------------------------------------------------------------------------

def test_personal_overlay_patterns_load(tmp_path, monkeypatch):
    """A personal-layer overlay at ~/.claude/hooks/hedge-personal.json loads and its patterns fire,
    missing/malformed falls back to [] silently (mirrors scissors-scan's overlay contract)."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    overlay = home / ".claude" / "hooks" / "hedge-personal.json"
    overlay.write_text(json.dumps(["зову\\s+вас"]), encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    patterns = hs._load_personal_patterns()
    assert patterns == ["зову\\s+вас"]

    # missing overlay -> silently []
    monkeypatch.setenv("HOME", str(tmp_path / "no-overlay-home"))
    assert hs._load_personal_patterns() == []

    # malformed overlay -> silently []
    bad_home = tmp_path / "bad-home"
    (bad_home / ".claude" / "hooks").mkdir(parents=True)
    (bad_home / ".claude" / "hooks" / "hedge-personal.json").write_text("not json", encoding="utf-8")
    monkeypatch.setenv("HOME", str(bad_home))
    assert hs._load_personal_patterns() == []


# ---- Wiring: pack installer + judge classification --------------------------------------------------

def test_pack_installer_ships_the_arm_unwired():
    """SPEC INV-238 + Requirement 311: a universal pack hook lives as source in hooks/ and its file is
    placed by the setup walk. Since 2026-08-17 the installer wires none of the six it ships — the host
    does, in its own settings.json. The installer never copies the personal overlay (hedge-personal.json
    stays the personal layer's own file, the same carve-out scissors-personal.json gets)."""
    src = _read(os.path.join(ROOT, "scripts", "install-pack-hooks.sh"))
    assert "hedge-scan.py" in src
    assert 'wire("Stop", "hedge-scan.py"' not in src
    assert "wire(" not in src, "the pack installer wires a hook again — all six are opt-in"
    assert "hedge-personal.json" not in src.split("JUDGE_FILES=")[1].split("\n")[0]


def test_classified_in_judge_hooks():
    """The arm is a library entry, off in the pack's default wiring, with its surface and its command
    form still declared so a host turning it on reads them rather than guessing (Requirement 311)."""
    decl = json.loads(_read(os.path.join(ROOT, "guardrails", "judge-hooks.json")))
    assert "hedge-scan" not in decl.get("wired", {})
    assert "hedge-scan" in decl.get("library", [])
    assert decl["opt_in_surface"]["hedge-scan"] == "Stop"
    assert decl["command"]["hedge-scan"] == "python3 ~/.claude/hooks/hedge-scan.py"
    assert decl["file"]["hedge-scan"] == "hedge-scan.py"


# ---- Traceability: the law stands in every document it is owed in (SPEC INV-238) --------------------

def test_spec_states_the_law():
    spec = _read(os.path.join(ROOT, "PRODUCT_SPEC.md"))
    # R232.1: subjunctive shall-form ("shall block") replaces the old descriptive sentence, and
    # the anchor now shares one combined bracket with INV-173 rather than standing alone.
    assert "shall* block the stop with a rewrite instruction" in spec
    assert "INV-238" in spec


def test_formal_index_row():
    spec = _read(os.path.join(ROOT, "PRODUCT_SPEC.md"))
    assert "| INV-238 |" in spec
    # index now carries locations only (SPEC INV-271) — the "hedge gate" prose check moves onto
    # the body requirement heading that carries INV-238.
    assert "Two Stop-hook soft signals: the hedge gate and the lean-orchestrator arm" in spec


def test_architecture_owns_the_invariant():
    arch = _read(os.path.join(ROOT, "ARCHITECTURE.md"))
    import sys as _sys
    _sys.path.insert(0, os.path.join(ROOT, "guardrails"))
    import archformat as _af
    owners = [n.name for n in _af.parse_nodes(arch) if "INV-238" in n.anchors_expanded]
    assert owners == ["guardrails"], "INV-238 must be owned by the guardrails node, got %r" % owners
    assert "hooks/hedge-scan.py:1" in arch


def test_matrix_row_covers_the_law():
    mat = _read(os.path.join(ROOT, "TEST_MATRIX.md"))
    assert "| M-420 |" in mat and "INV-238" in mat
