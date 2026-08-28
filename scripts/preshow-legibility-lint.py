#!/usr/bin/env python3
"""preshow-legibility-lint.py — the mechanical legibility gate for any STYLED artifact SHOWN to a human (SPEC INV-139).

Why this exists, and how it sits beside preshow-register-lint.py:
  The register lint guards that the WORDS a surface shows are the product's own plain language (no coined
  metaphor, no calque, no transliterated pack term). THIS lint guards a different thing at the same instant:
  that the words can actually be READ — that text meets a minimum contrast ratio against its background and a
  minimum size. Register and legibility are the two guards where text reaches a human's eye: one that the
  words are the product's own, one that they can be seen. Run BOTH at the pre-show gate.

The floors (stated defaults — a host may set its own on its word, INV-70):
  - normal text:        contrast ratio >= 4.5 : 1
  - large text:         contrast ratio >= 3   : 1   (font-size >= 24px, OR >= 18.66px when bold)
  - body / caption text: font-size >= 12px

What it CAN do (honestly, so no one over-trusts it):
  It reads DECLARED CSS — `<style>` blocks, inline `style="..."` attributes, and any `.css` file passed
  directly. It resolves one level of CSS custom properties (`var(--name)`) and computes the WCAG
  relative-luminance contrast ratio exactly as the spec defines it, converting px / pt / rem / em to
  pixels.

  A ratio is only worth as much as the background it was measured against, so a pair is SCORED only
  where the stylesheet itself determines that background. Three cases determine it. The rule sets a
  background on itself. An ancestor named in the rule's own compound chain sets one — `.gg .cap` is
  paired with `.gg`'s background when `.gg { background: ... }` is in the same stylesheet. Or the page
  element (`body`/`:root`/`html`) sets one and the stylesheet paints no other surface at all, which
  leaves the page as the only background any text in that file can be sitting on.

  Everything else is reported UNRESOLVED and never scored: a rule that paints itself in a colour this
  reader cannot pin down, a chain whose ancestors paint nothing while the stylesheet does paint
  surfaces of its own, and any file whose page element declares no background colour. The measured
  colour is named in every verdict, so a wrong pairing shows on its face.

What it CANNOT do:
  It is a PRAGMATIC STATIC FLOOR, not a browser. It does NOT run the full CSS cascade, specificity,
  inheritance across the DOM tree, media queries, opacity stacking, gradient/image backgrounds, or
  JS-applied styles. It skips named colors, translucent colors, unresolved variables, and unparseable
  or relative sizes (%/unitless/calc) rather than GUESS — a skipped declaration is never a hit. It
  cannot see DOM nesting that isn't expressed as a compound CSS selector (a sibling class that happens
  to paint the true ancestor in markup). The authoritative check for a real product surface is the
  BROWSER-COMPUTED assertion in the adopting project's own suite (the verify feel pass, INV-30/INV-136
  split); this script is the floor at the pre-show gate for a styled file about to be opened for a
  human.

Usage: preshow-legibility-lint.py FILE [FILE ...]      (or: cat file.html | preshow-legibility-lint.py -)
Exit 0 = clean · exit 1 = at least one hit (low-contrast and/or small-text) · exit 2 = usage error.
Unresolved pairs are reported separately and never affect the exit code.
"""
import bisect
import json
import re
import sys

# ---- The floors (defaults; a host may override on its word, INV-70) -----------------------------
# Derivation: WCAG 2.1 Level AA (Success Criteria 1.4.3, 1.4.11) — normal text 4.5:1, large text
# 3:1, where "large" starts at 18pt (24px) regular or 14pt (18.66px) bold. Not a project-invented
# number; the ratios and point sizes are the published standard's own floors.
CONTRAST_NORMAL = 4.5
CONTRAST_LARGE = 3.0
LARGE_PX = 24.0
LARGE_PX_BOLD = 18.66
SIZE_FLOOR_PX = 12.0


# ---- WCAG relative luminance / contrast (used exactly as SPEC INV-139 states) -------------------
def _lin(c):  # c in 0..1
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(r, g, b):  # r,g,b in 0..255
    R, G, B = _lin(r / 255), _lin(g / 255), _lin(b / 255)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast(rgb1, rgb2):
    l1, l2 = _luminance(*rgb1), _luminance(*rgb2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ---- Colour parsing (hex #rgb/#rrggbb/#rrggbbaa, rgb()/rgba(); named/unparseable -> None) --------
# A TRANSLUCENT colour is not a colour this reader knows: `rgba(127,127,127,.14)` renders as whatever
# it is composited over, and the layer beneath it is exactly what a static stylesheet read cannot see.
# Reading it as its opaque triple invents the number every ratio below then rests on, so it parses to
# None and the declaration is skipped like a named colour or an unresolved variable.
def _channel(tok):
    tok = tok.strip()
    if tok.endswith("%"):
        return round(float(tok[:-1]) * 255 / 100)
    return int(round(float(tok)))


def _opaque(tok):
    """True when an alpha component is absent or fully opaque; False when it lets the layer through."""
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) >= 100.0
    return float(tok) >= 1.0


def parse_color(v):
    if v is None:
        return None
    v = v.strip()
    m = re.match(r"#([0-9a-fA-F]{3,8})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return tuple(int(ch * 2, 16) for ch in h)
        if len(h) == 4:  # #rgba
            if int(h[3] * 2, 16) < 255:
                return None
            return tuple(int(h[i] * 2, 16) for i in range(3))
        if len(h) in (6, 8):  # #rrggbb / #rrggbbaa
            if len(h) == 8 and int(h[6:8], 16) < 255:
                return None
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        return None
    m = re.match(r"rgba?\(([^)]+)\)$", v, re.I)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        try:
            if len(parts) > 3 and not _opaque(parts[3]):
                return None
            return (_channel(parts[0]), _channel(parts[1]), _channel(parts[2]))
        except (ValueError, IndexError):
            return None
    return None


def _first_color_token(v):
    """A colour may be a shorthand (`background: #fff url(...)`); pull the first colour token out."""
    if v is None:
        return None
    m = re.search(r"#[0-9a-fA-F]{3,8}\b", v)
    if m:
        return parse_color(m.group(0))
    m = re.search(r"rgba?\([^)]*\)", v, re.I)
    if m:
        return parse_color(m.group(0))
    return None


# ---- Size parsing (px as-is; pt*96/72; rem/em*16; skip %/unitless/calc) --------------------------
def parse_px(v):
    if v is None:
        return None
    v = v.strip()
    if "%" in v or "calc" in v.lower():
        return None
    m = re.match(r"^([\d.]+)(px|pt|rem|em)\b", v)
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2)
    if u == "px":
        return n
    if u == "pt":
        return n * 96 / 72
    return n * 16.0  # rem / em against a 16px base


# ---- var() resolution (one level; unresolved -> None so the declaration is skipped) --------------
def resolve_var(value, varmap):
    if value is None or "var(" not in value:
        return value
    m = re.search(r"var\(\s*(--[-\w]+)\s*(?:,\s*([^)]+))?\)", value)
    if not m:
        return value
    name, fallback = m.group(1), m.group(2)
    if name in varmap:
        return value[: m.start()] + varmap[name] + value[m.end():]
    if fallback is not None:
        return value[: m.start()] + fallback.strip() + value[m.end():]
    return None  # unresolved — caller skips


# ---- Line-number bookkeeping --------------------------------------------------------------------
def _line_starts(text):
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _line_of(starts, offset):
    return bisect.bisect_right(starts, offset)


# ---- CSS collection: (css_text, base_offset, selector_or_None) segments --------------------------
def _css_segments(text, is_css_file):
    """Yield (css_text, base_offset, forced_selector) for every place CSS lives in the file."""
    if is_css_file:
        yield (text, 0, None)
        return
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S | re.I):
        yield (m.group(1), m.start(1), None)
    for m in re.finditer(r"""style\s*=\s*(?:"([^"]*)"|'([^']*)')""", text, re.I):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        base = m.start(1) if m.group(1) is not None else m.start(2)
        yield (body, base, "inline style")


def _iter_declarations(body, body_base):
    """Yield (prop_lower, raw_value, abs_offset) for each `prop: value` in a declaration body."""
    for m in re.finditer(r"([-\w]+)\s*:\s*([^;{}]+)", body):
        yield (m.group(1).lower(), m.group(2).strip(), body_base + m.start(1))


def _collect_blocks(text, is_css_file):
    """Return (blocks, varmap). A block = dict(selector, decls={prop:(value,offset)}, order)."""
    blocks = []
    varmap = {}
    for css_text, base, forced_sel in _css_segments(text, is_css_file):
        if forced_sel is not None:
            # inline style attribute: one implicit block, no braces
            decls = {}
            for prop, value, off in _iter_declarations(css_text, base):
                if prop.startswith("--"):
                    varmap.setdefault(prop, value)
                decls[prop] = (value, off)
            if decls:
                blocks.append({"selector": forced_sel, "decls": decls})
            continue
        for rm in re.finditer(r"([^{}]+)\{([^{}]*)\}", css_text):
            selector = " ".join(rm.group(1).split())
            body_base = base + rm.start(2)
            decls = {}
            for prop, value, off in _iter_declarations(rm.group(2), body_base):
                if prop.startswith("--"):
                    varmap.setdefault(prop, value)
                decls[prop] = (value, off)
            blocks.append({"selector": selector, "decls": decls})
    return blocks, varmap


_ROOT_MARKERS = {"body", ":root", "html"}

_NO_PAINT = {"none", "transparent", "inherit", "initial", "unset", "revert"}


def _block_paints(block):
    """True when a block sets a background of its own — whatever colour, resolvable or not.

    Whether a rule paints a surface is a different question from what colour it paints it, and only
    the first one is always answerable from the text. `background: linear-gradient(...)` and
    `background: rgba(0,0,0,.4)` both make the rule its own surface while telling this reader nothing
    about the colour, and both must stop a walk that would otherwise measure against something else.
    """
    for prop in ("background-color", "background"):
        if prop in block["decls"]:
            value = block["decls"][prop][0].strip().lower()
            if value and value.split()[0] not in _NO_PAINT:
                return True
    return False


def _block_bg(block, varmap):
    """Resolved background colour a block sets on itself, or None when it sets none this reader
    can pin down. `_block_paints` tells the two apart."""
    for prop in ("background-color", "background"):
        if prop in block["decls"]:
            resolved = resolve_var(block["decls"][prop][0], varmap)
            rgb = _first_color_token(resolved)
            if rgb is not None:
                return rgb
    return None


def _selector_tokens(selector):
    return set(re.split(r"[\s,>+~]+", selector.strip()))


def _page_background(blocks, varmap):
    """The colour the page element itself declares, or None where the stylesheet does not say.

    There is no substitute for a page background the file never states. It belongs to the browser's
    default and to the viewer's own theme, and standing in the most commonly declared colour, or
    white, invents the input every ratio in the file then rests on. This used to return that guess
    and mark only the white one as assumed.
    """
    for block in blocks:
        for part in block["selector"].split(","):
            if part.strip() in _ROOT_MARKERS and _block_paints(block):
                return _block_bg(block, varmap)
    return None


def _paints_its_own_surfaces(blocks):
    """True when the stylesheet paints a background on anything other than the page element."""
    for block in blocks:
        if not _block_paints(block):
            continue
        if all(p.strip() in _ROOT_MARKERS for p in block["selector"].split(",")):
            continue
        return True
    return False


def _hex(rgb):
    return "#%02x%02x%02x" % rgb


# ---- Background resolution (text-only: no browser, no DOM) --------------------------------------
# One rule decides every pairing: a pair is measured only against a background the stylesheet
# DETERMINES, and every other pair is reported for a human eye.
#
# The first half of this landed on 2026-07-27, against a lint that paired every foreground colour
# with the page background and nothing else: it walks the rule's own compound chain (`.gg .cap` under
# `.gg { background:#fff }`) for the nearest ancestor that paints. What it left behind was the same
# defect one case narrower. A selector carrying no chain — the common shape, since a class is usually
# written on its own — still fell back to the page background, so text sitting on a card was scored
# against the page behind the card, and the verdict was wrong in both directions again: on a dark page
# with white cards, dark card text was reported unreadable at 2.3:1 while near-white card text passed
# at 14.6:1 and was in truth invisible at 1.3:1.
#
# What a chainless selector determines depends on the rest of the stylesheet. Where the page element
# is the only thing the file paints, the page background is the only background any of its text can
# be on — determined, and scored. Where the file paints surfaces of its own, the text may be on any
# of them, and there is nothing to measure against — UNRESOLVED. The same weighing covers a chain
# whose ancestors paint nothing: naming `body` as an ancestor says no more about the card in between
# than naming nothing does, so it is not the stronger evidence it was read as.


def _selector_run(selector):
    """Tokens connected to the LAST simple selector via descendant/child combinators only.
    A sibling combinator (+/~) breaks the run since it does not express an ancestor relation.
    Only the first comma-separated alternative of a grouped selector is walked."""
    first_part = selector.split(",")[0].strip()
    run = []
    for part in re.split(r"(>|\+|~)", first_part):
        part = part.strip()
        if part == ">":
            continue
        if part in ("+", "~"):
            run = []
            continue
        if not part:
            continue
        run.extend(part.split())
    return run


def _selector_own_bg(token, blocks, varmap):
    """(rgb, paints) for the first block whose own selector (any comma-alternative) equals `token`
    exactly and paints. `paints` says the token is a surface; `rgb` is its colour where there is one."""
    for block in blocks:
        for part in block["selector"].split(","):
            if part.strip() == token and _block_paints(block):
                return _block_bg(block, varmap), True
    return None, False


# The plain reasons a pair goes unscored, each naming what the stylesheet did not say.
_WHY_OWN = ("the rule paints its own background in a colour this reader cannot pin down "
            "(a gradient, an image, a translucent or a named colour)")
_WHY_ANCESTOR = ("the nearest ancestor in the selector chain that paints does so in a colour this "
                 "reader cannot pin down")
_WHY_NO_PAGE = ("the page itself declares no background colour, so the file states nothing to "
                "measure this text against")
_WHY_SURFACES = ("the selector names no painting ancestor, and the stylesheet paints surfaces of "
                 "its own that this text may be sitting on")


def _resolve_bg(block, blocks, varmap, page_bg, own_surfaces):
    """Return (rgb, kind, why) — kind in 'own' / 'ancestor' / 'page' / 'unresolved'.
    `why` is the plain reason on 'unresolved', None otherwise."""
    if _block_paints(block):
        own = _block_bg(block, varmap)
        return (own, "own", None) if own is not None else (None, "unresolved", _WHY_OWN)
    run = _selector_run(block["selector"])
    for token in reversed(run[:-1]):  # nearest ancestor first
        if token in _ROOT_MARKERS:
            break  # the page element — weighed below, against what else the stylesheet paints
        rgb, paints = _selector_own_bg(token, blocks, varmap)
        if paints:
            return (rgb, "ancestor", None) if rgb is not None else (None, "unresolved", _WHY_ANCESTOR)
    if page_bg is None:
        return None, "unresolved", _WHY_NO_PAGE
    if len(run) == 1 and run[0] in _ROOT_MARKERS:
        return page_bg, "page", None  # the rule styles the page element itself
    if own_surfaces:
        return None, "unresolved", _WHY_SURFACES
    return page_bg, "page", None


def _is_bold(block):
    if "font-weight" in block["decls"]:
        w = block["decls"]["font-weight"][0].strip().lower()
        if w in ("bold", "bolder"):
            return True
        m = re.match(r"^(\d+)", w)
        if m and int(m.group(1)) >= 700:
            return True
    return False


# ---- The scan -----------------------------------------------------------------------------------
def scan(text, is_css_file=False):
    """Return (hits, unresolved).
    hits: (line_no, code, snippet, detail) for every legibility-floor hit (blocks the pre-show gate).
    unresolved: (line_no, snippet, detail) for pairs whose effective background couldn't be resolved
    from the stylesheet text — reported for a human to check by eye, never silently paired."""
    starts = _line_starts(text)
    blocks, varmap = _collect_blocks(text, is_css_file)
    page_bg = _page_background(blocks, varmap)
    own_surfaces = _paints_its_own_surfaces(blocks)
    hits = []
    unresolved = []
    for block in blocks:
        sel = block["selector"]
        decls = block["decls"]
        # --- contrast ---
        if "color" in decls:
            resolved = resolve_var(decls["color"][0], varmap)
            fg = _first_color_token(resolved)
            if fg is not None:
                bg, bg_kind, why = _resolve_bg(block, blocks, varmap, page_bg, own_surfaces)
                if bg_kind == "unresolved":
                    detail = why + " — check the real rendered pair by eye"
                    unresolved.append((_line_of(starts, decls["color"][1]), sel, detail))
                else:
                    ratio = contrast(fg, bg)
                    fs_px = None
                    if "font-size" in decls:
                        fs_px = parse_px(resolve_var(decls["font-size"][0], varmap))
                    large = fs_px is not None and (
                        fs_px >= LARGE_PX or (fs_px >= LARGE_PX_BOLD and _is_bold(block))
                    )
                    floor = CONTRAST_LARGE if large else CONTRAST_NORMAL
                    if ratio < floor:
                        detail = "ratio %.1f:1 < %.1f:1 (color %s on %s)" % (
                            ratio, floor, _hex(fg), _hex(bg),
                        )
                        hits.append((_line_of(starts, decls["color"][1]), "low-contrast", sel, detail))
        # --- size ---
        if "font-size" in decls and not sel.startswith(":root") and "html" not in _selector_tokens(sel):
            fs_px = parse_px(resolve_var(decls["font-size"][0], varmap))
            if fs_px is not None and fs_px < SIZE_FLOOR_PX:
                detail = "%gpx < %gpx floor" % (fs_px, SIZE_FLOOR_PX)
                hits.append((_line_of(starts, decls["font-size"][1]), "small-text", sel, detail))
    hits.sort(key=lambda h: h[0])
    unresolved.sort(key=lambda u: u[0])
    return hits, unresolved


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("usage: preshow-legibility-lint.py FILE [FILE ...]  (or - for stdin)\n")
        return 2
    any_hit = False
    for src in argv[1:]:
        if src == "-":
            text = sys.stdin.read()
            is_css = False
            label = "<stdin>"
        else:
            text = open(src, encoding="utf-8").read()
            is_css = src.lower().endswith(".css")
            label = src
        hits, unresolved = scan(text, is_css_file=is_css)
        if not hits:
            print("OK (preshow-legibility): %s — text meets the contrast and size floor" % label)
        else:
            any_hit = True
            print("PRE-SHOW LEGIBILITY LINT (SPEC INV-139): a styled surface a human is about to see carries")
            print("text under the legibility floor (contrast >= 4.5:1 normal / 3:1 large, size >= 12px). File: %s" % label)
            json_hits = []
            for line_no, code, snippet, detail in hits:
                print("  line %d  [%s]  %s" % (line_no, code, snippet))
                print("          ↳ %s" % detail)
                json_hits.append({"line": line_no, "code": code, "selector": snippet, "detail": detail})
            print(json.dumps({"severity": "error", "code": "legibility-floor", "hits": json_hits}))
        if unresolved:
            print("UNRESOLVED (preshow-legibility): %s — background could not be resolved from the" % label)
            print("stylesheet text; these pairs do NOT block, but check the real rendered pair by eye:")
            json_unresolved = []
            for line_no, snippet, detail in unresolved:
                print("  line %d  [unresolved]  %s" % (line_no, snippet))
                print("          ↳ %s" % detail)
                json_unresolved.append({"line": line_no, "selector": snippet, "detail": detail})
            print(json.dumps({"severity": "info", "code": "legibility-unresolved", "hits": json_unresolved}))
    return 1 if any_hit else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
