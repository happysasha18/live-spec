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
  directly. It resolves one level of CSS custom properties (`var(--name)`), pairs a rule block's own
  `color` with the same block's `background-color` when both are set. Otherwise it walks the SAME
  selector's own compound chain for the nearest ancestor that declares a background — `.gg .cap` is
  paired with `.gg`'s background when `.gg { background: ... }` is in the same stylesheet — falling
  back to the page background (`body`/`:root`/`html`, else the most common declared background, else
  white with the assumption NOTED) only for a bare selector with no chain, or a chain that genuinely
  reaches a body/:root/html marker. A chain that dead-ends without reaching one — the true background
  sits on a sibling class or in markup this static reader cannot see — is reported UNRESOLVED rather
  than silently guessed (fix for the 2026-07-27 wrong-background bug: it used to pair every colour
  with the page background regardless, blocking cards that painted their own light background and
  missing genuine failures elsewhere that only looked fine against the far-away page colour). It
  computes the WCAG relative-luminance contrast ratio exactly as the spec defines it, and it converts
  px / pt / rem / em sizes to pixels.

What it CANNOT do:
  It is a PRAGMATIC STATIC FLOOR, not a browser. It does NOT run the full CSS cascade, specificity, inheritance
  across the DOM tree, media queries, opacity stacking, gradient/image backgrounds, or JS-applied styles. It
  skips named colors, unresolved variables, and unparseable or relative sizes (%/unitless/calc) rather than
  GUESS — a skipped declaration is never a hit. It cannot see DOM nesting that isn't expressed as a compound
  CSS selector (a sibling class that happens to paint the true ancestor in markup) — those pairs are reported
  UNRESOLVED, not scored. The authoritative check for a real product surface is the BROWSER-COMPUTED assertion
  in the adopting project's own suite (the verify feel pass, INV-30/INV-136 split); this script is the floor
  at the pre-show gate for a styled file about to be opened for a human.

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
def _channel(tok):
    tok = tok.strip()
    if tok.endswith("%"):
        return round(float(tok[:-1]) * 255 / 100)
    return int(round(float(tok)))


def parse_color(v):
    if v is None:
        return None
    v = v.strip()
    m = re.match(r"#([0-9a-fA-F]{3,8})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return tuple(int(ch * 2, 16) for ch in h)
        if len(h) == 4:  # #rgba — ignore alpha
            return tuple(int(h[i] * 2, 16) for i in range(3))
        if len(h) in (6, 8):  # #rrggbb / #rrggbbaa — ignore alpha
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        return None
    m = re.match(r"rgba?\(([^)]+)\)$", v, re.I)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        try:
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


def _block_bg(block, varmap):
    """Resolved background colour a block sets on itself, or None."""
    for prop in ("background-color", "background"):
        if prop in block["decls"]:
            resolved = resolve_var(block["decls"][prop][0], varmap)
            rgb = _first_color_token(resolved)
            if rgb is not None:
                return rgb
    return None


_PAGE_SEL = {"body", ":root", "html"}


def _selector_tokens(selector):
    return set(re.split(r"[\s,>+~]+", selector.strip()))


def _page_background(blocks, varmap):
    """(rgb, assumed_default) — a body/:root/html bg wins; else the most common; else white (noted)."""
    prefer = {"body": None, ":root": None, "html": None}
    counts = {}
    for block in blocks:
        rgb = _block_bg(block, varmap)
        if rgb is None:
            continue
        counts[rgb] = counts.get(rgb, 0) + 1
        for tok in _selector_tokens(block["selector"]):
            if tok in prefer and prefer[tok] is None:
                prefer[tok] = rgb
    for tok in ("body", ":root", "html"):
        if prefer[tok] is not None:
            return prefer[tok], False
    if counts:
        return max(counts, key=counts.get), False
    return (255, 255, 255), True


def _hex(rgb):
    return "#%02x%02x%02x" % rgb


# ---- Ancestor background resolution (fix for the wrong-background bug, 2026-07-27 inbox) ---------
# The lint used to pair every foreground colour with the PAGE background, never a nearer ancestor
# that actually paints one — wrong in both directions on a page whose cards paint their own
# backgrounds (false low-contrast hits on light cards; genuine failures elsewhere waved through
# because they read fine against the far-away page colour). The fix stays text-only (no browser, no
# DOM): it walks the SAME selector's own compound chain (`.gg .cap` under `.gg { background:#fff }`)
# for an ancestor that declares a background, nearest first. A bare selector with no chain at all
# keeps the old page-background default (there is no contrary information to act on). A selector
# that DOES carry a chain but dead-ends — no ancestor in it paints, and the chain never reaches a
# body/:root/html marker — is UNRESOLVED: the true background sits on a sibling class or in markup
# this static reader cannot see, and it must never be guessed as the page background.
_ROOT_MARKERS = {"body", ":root", "html"}


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
    """First block whose own selector (any comma-alternative) equals `token` exactly and paints."""
    for block in blocks:
        for part in block["selector"].split(","):
            if part.strip() == token:
                rgb = _block_bg(block, varmap)
                if rgb is not None:
                    return rgb
    return None


def _resolve_bg(block, blocks, varmap, page_bg):
    """Return (rgb, kind) — kind in 'own' / 'ancestor' / 'root' / 'unresolved'."""
    own = _block_bg(block, varmap)
    if own is not None:
        return own, "own"
    run = _selector_run(block["selector"])
    if len(run) <= 1:
        return page_bg, "root"  # bare selector: no chain to act on, keep the page-background default
    ancestors = run[:-1]
    for token in reversed(ancestors):  # nearest ancestor first
        rgb = _selector_own_bg(token, blocks, varmap)
        if rgb is not None:
            return rgb, "ancestor"
    if ancestors[0] in _ROOT_MARKERS:
        return page_bg, "root"
    return None, "unresolved"


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
    page_bg, assumed = _page_background(blocks, varmap)
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
                bg, bg_kind = _resolve_bg(block, blocks, varmap, page_bg)
                if bg_kind == "unresolved":
                    detail = (
                        "background could not be resolved from the stylesheet text (no ancestor in "
                        "the selector chain paints, and the chain never reaches body/:root/html) — "
                        "check the real rendered pair by eye"
                    )
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
                        note = " [background assumed #ffffff]" if (bg_kind == "root" and assumed) else ""
                        detail = "ratio %.1f:1 < %.1f:1 (color %s on %s)%s" % (
                            ratio, floor, _hex(fg), _hex(bg), note,
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
