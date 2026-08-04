# -*- coding: utf-8 -*-
"""Red-first evidence for the pre-show register lint (SPEC INV-83, queue row 170).

The lint reds on every fixture leak (coined metaphor / calque / transliterated pack term), greens on
the nine accepted reader docs (they passed the human bar), and — the proof it is WIRED — the
communicator skill names the lint as a BLOCKING pre-show step. That last test is RED until the senior
folds the communicator delta (scratchpad/row170/communicator-delta.md); the red is the wiring proof.
"""
import os
import sys
import importlib.util

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINT_PATH = os.path.join(REPO, "scripts", "preshow-register-lint.py")

# import the lint module by path (its filename has a hyphen, so importlib, not a plain import).
_spec = importlib.util.spec_from_file_location("preshow_register_lint", LINT_PATH)
lint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint)


# ---- fixtures: the exact leaks that MUST red -------------------------------------------------
EN_FIXTURES = [
    # bundled internal setting names shown raw (one line, two names) — the onboarding-mockup leak
    "working at full rigor — say 'work lean' when time is short",
    # a machine-flavoured abstraction, folded in as its exact caught phrases
    "Everything else comes up naturally when it first matters",
    # pack coinages shown raw
    "Drop the wish at the wish door and it walks the pipeline station by itself",
]

RU_CALQUE_FIXTURES = [
    "проверяем швы с соседями перед показом",          # ← 'seams with neighbours'
    "работники в поле уже дописали отчёт",             # ← 'workers in the field'
    "если случится смерть счёта, останавливаемся",      # ← 'budget death'
    "стыки поверхностей разъехались на бордюре",        # ← 'surface seams'
]

RU_KNOWN_BAD_FIXTURES = [
    "поставил растяжки на этот класс ошибок",           # profile known-bad ← 'tripwires'
    "это та же семья, что и вчерашний сбой",             # profile known-bad ← 'same incident family'
    "после посадки соберём свежие скриншоты",           # profile known-bad ← 'landing'
    "узел-владелец решает, куда падает факт",            # profile known-bad ← 'owner node'
]

RU_TRANSLIT_FIXTURES = [
    "прогнал через весь пайплайн",                       # transliterated ← 'pipeline'
    "воркер дописал и завершился",                       # transliterated ← 'worker'
    "стоим на этом стейшн и ждём ревью",                 # transliterated ← 'station'
]

ALL_RED_FIXTURES = EN_FIXTURES + RU_CALQUE_FIXTURES + RU_KNOWN_BAD_FIXTURES + RU_TRANSLIT_FIXTURES

NINE_READER_DOCS = [
    "README.md", "OVERVIEW.md", "docs/pipeline.md", "docs/architecture-method.md",
    "docs/test-method.md", "docs/onboarding-and-settings.md", "docs/push-law.md",
    "docs/worker-liveness.md", "docs/adoption.md",
]


@pytest.mark.parametrize("text", ALL_RED_FIXTURES)
def test_lint_reds_on_each_fixture_leak(text):
    """Every fixture leak is caught (at least one pattern hit)."""
    hits = lint.scan(text)
    assert hits, "register lint missed a known leak: %r" % text


def test_full_rigor_and_work_lean_both_caught_on_one_line():
    """The bundled EN line trips BOTH internal-setting-name patterns."""
    ids = {pid for _l, pid, _s, _src in lint.scan(EN_FIXTURES[0])}
    assert "en-full-rigor" in ids and "en-work-lean" in ids


@pytest.mark.parametrize("doc", NINE_READER_DOCS)
def test_lint_greens_on_accepted_reader_docs(doc):
    """The nine accepted reader docs passed the human bar; the lint must not red them.

    A red here is either a TRUE positive (a real leak in an accepted doc — investigate, keep the
    pattern) or a false positive (tighten the pattern). Either way the message prints the hits."""
    path = os.path.join(REPO, doc)
    text = open(path, encoding="utf-8").read()
    hits = lint.scan(text)
    assert not hits, "register lint reds on accepted doc %s: %r" % (doc, hits)


def test_communicator_names_the_lint_as_a_blocking_preshow_step():
    """WIRING PROOF — RED until the senior folds the communicator delta (step 5).

    The pre-show walk must NAME scripts/preshow-register-lint.py and mark it BLOCKING. This asserts
    the wiring, so it stays red until communicator/SKILL.md is edited. That red IS the evidence the
    step is not yet folded — expected to flip green when the senior applies the delta."""
    path = os.path.join(REPO, "skills", "communicator", "SKILL.md")
    text = open(path, encoding="utf-8").read().lower()
    assert "preshow-register-lint.py" in text, \
        "communicator's pre-show walk does not yet name the register lint (fold the delta)"
    assert "block" in text, \
        "communicator names the lint but not as a BLOCKING step (a red blocks the showing)"


def test_spec_retracts_the_growth_duty_and_names_the_judge():
    """M-197 second leg (INV-83), restated for rows 416+418: the grows-by-one duty is RETRACTED — the
    literal set grows by nobody's duty — and the register judge holds the residual class the list cannot."""
    path = os.path.join(REPO, "PRODUCT_SPEC.md")
    import re as _re
    text = _re.sub(r"\s+", " ", open(path, encoding="utf-8").read())
    assert "grows by one per caught leak" not in text, "the retracted growth doctrine must be gone (INV-83)"
    assert "grows by nobody's duty" in text, "SPEC must state the list grows by nobody's duty (INV-83)"
    assert "register judge" in text, "SPEC does not name the register judge as the residual's holder (INV-203)"
    assert "preshow-register-lint.py" in text, "SPEC does not name the register lint script (INV-83)"
    assert "scope its reach to the shown artifact" in text, "SPEC lost INV-83's reach sentence"
    assert "| INV-83 |" in text, "Formal index lost INV-83"


# ---- reach: a page that REPRODUCES another document (2026-08-04) ------------------------------
# A comparison page shows an original beside its rewrite, so the original's own coinages stand on the
# page by design. The fence marks what the page quotes; the page's own words stay under the full check.
_LEAK = "Drop the wish at the wish door and it walks the pipeline station by itself"


def test_a_leak_inside_a_closed_fence_is_read_as_quotation():
    page = ("<html><body>\n<!-- register-lint:quoted-source -->\n%s\n"
            "<!-- register-lint:/quoted-source -->\n</body></html>" % _LEAK)
    assert lint.scan(page) == []


def test_the_same_leak_outside_the_fence_still_reds():
    page = "<html><body>\n%s\n</body></html>" % _LEAK
    assert lint.scan(page), "a coined term in the page's own words must still be caught"


def test_the_page_own_words_are_still_checked_when_a_fence_is_present():
    page = ("<html><body>\n<!-- register-lint:quoted-source -->\n%s\n"
            "<!-- register-lint:/quoted-source -->\n%s\n</body></html>") % (_LEAK, _LEAK)
    hits = lint.scan(page)
    assert hits, "the unfenced copy is still charged"
    assert set(h[0] for h in hits) == {5}, (
        "only the unfenced copy is charged, and its reported line number points at the real line "
        "of the real file")


def test_an_unclosed_fence_exempts_nothing():
    page = "<html><body>\n<!-- register-lint:quoted-source -->\n%s\n</body></html>" % _LEAK
    assert lint.scan(page), "a fence left open buys no silence"


def test_two_fenced_regions_both_count_as_quotation():
    page = ("<!-- register-lint:quoted-source -->\n%s\n<!-- register-lint:/quoted-source -->\n"
            "plain wording a reader understands\n"
            "<!-- register-lint:quoted-source -->\n%s\n"
            "<!-- register-lint:/quoted-source -->\n") % (_LEAK, _LEAK)
    assert lint.scan(page) == []


def test_a_file_with_no_fence_is_untouched_by_the_mask():
    page = "%s\nsecond line\n" % _LEAK
    assert lint.mask_quoted_source(page) == page
