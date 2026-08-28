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

  For an HTML page it also reads the MARKUP, and that is what makes a ratio worth having. The
  stylesheet says which rules paint; only the markup says which painted surface a given piece of
  text is inside. So a rule is measured against the nearest ancestor of its own element that paints,
  walking that element's real chain up to the page. A card's caption is scored against the card, and
  a heading beside the card is scored against the page, in the same file.

  A ratio is only worth as much as the background it was measured against, so a pair is SCORED only
  where the file determines that background. The rule may set one on itself. The element's own
  ancestor chain in the markup may set one. Failing markup — a `.css` file read on its own, or a
  selector matching nothing in the page — the stylesheet-only reading stands: an ancestor named in
  the rule's compound chain, or the page element where the stylesheet paints no other surface at all.

  Everything else is reported UNRESOLVED and never scored: a surface painted in a colour this reader
  cannot pin down (a gradient, an image, a translucent or a named colour), a rule whose text appears
  on more than one background in the page, a chain that reaches the page with nothing declaring a
  background, and text declared in a translucent colour, which renders as whatever it sits over. The
  measured colour is named in every verdict, so a wrong pairing shows on its face.

  Reading the markup landed 2026-08-28. Before it, the reader asked one question of the WHOLE FILE —
  does this stylesheet paint any surface of its own? — and stood every chainless rule down when the
  answer was yes. One `.card { background: … }` anywhere, or a single inline `style="background:…"`,
  therefore silenced every contrast check in the page while the run still printed OK.

What it CANNOT do:
  It is a PRAGMATIC STATIC FLOOR, not a browser. It does NOT run the full CSS cascade, specificity,
  inheritance across the DOM tree, media queries, opacity stacking, gradient/image backgrounds, or
  JS-applied styles. Where one element is painted by several rules — the usual shape of a page that
  restates its colours under `prefers-color-scheme: dark` — it keeps the FIRST, the unconditional one
  every viewer gets. It skips named colors, translucent colors, unresolved variables, and unparseable
  or relative sizes (%/unitless/calc) rather than GUESS — a skipped declaration is never a hit. It
  matches a selector against the markup only in its plain forms (tag, id, class, `*`, and descendant
  chains of those); a pseudo-class, a pseudo-element or an attribute test leaves the element
  unmatched, and the rule falls back to the stylesheet-only reading. Markup written by JavaScript is
  not there to be read. The authoritative check for a real product surface is the
  BROWSER-COMPUTED assertion in the adopting project's own suite (the verify feel pass, INV-30/INV-136
  split); this script is the floor at the pre-show gate for a styled file about to be opened for a
  human.

Usage: preshow-legibility-lint.py FILE [FILE ...]      (or: cat file.html | preshow-legibility-lint.py -)
Exit 0 = nothing under the floor · exit 1 = at least one hit (low-contrast and/or small-text) ·
exit 2 = usage error.

READ THE VERDICT LINE, NOT ONLY THE EXIT CODE. Unresolved pairs do not move the exit code, and they
do change the verdict: a run that could not measure everything prints STOOD DOWN IN PART instead of
OK, and names how many pairs went unread. The exit code stays put on purpose. What makes a pair
unresolvable is usually a gradient, an image or a translucent surface, and none of those is a defect
an author can lift to a floor — a gate that reds on them is a gate that gets switched off, taking
the real hits with it. What was wrong until 2026-08-28 was not the exit code but the sentence beside
it: an unread page printed "text meets the contrast and size floor", which is a claim about text
this reader never looked at.
"""
import bisect
import json
import re
import sys
from html.parser import HTMLParser

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


def is_translucent(v):
    """True when a declared colour carries an alpha that lets the layer beneath it through.

    `parse_color` returns None for such a colour, the same answer it gives a named or unparseable
    one, and a caller cannot tell the two apart from that. The difference matters at the foreground:
    text declared in a translucent colour is text this reader must report rather than pass over in
    silence, and a colour it simply does not know how to read has always been skipped.
    """
    if v is None:
        return False
    m = re.search(r"#([0-9a-fA-F]{3,8})\b", v)
    if m:
        h = m.group(1)
        if len(h) == 4:
            return int(h[3] * 2, 16) < 255
        if len(h) == 8:
            return int(h[6:8], 16) < 255
        return False
    m = re.search(r"rgba?\(([^)]*)\)", v, re.I)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1).strip()) if p]
        if len(parts) > 3:
            try:
                return not _opaque(parts[3])
            except ValueError:
                return False
    return False


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
                # `inline_at` is how the block finds its own element in the markup below.
                blocks.append({"selector": forced_sel, "decls": decls, "inline_at": base})
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


# A background value that composes its own pixels out of several colours, or out of an image. The
# surface is real and its colour is not one colour, so there is nothing here to measure against.
_COMPOSED_SURFACE = re.compile(r"\b(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(|"
                               r"\burl\s*\(|\bimage-set\s*\(|\bcross-fade\s*\(|\belement\s*\(", re.I)


def _block_bg(block, varmap):
    """Resolved background colour a block sets on itself, or None when it sets none this reader
    can pin down. `_block_paints` tells the two apart.

    A gradient or an image is where the two used to disagree: `_block_paints` said the rule was its
    own surface, and this function reached past the function name and returned the gradient's first
    stop as though it were the surface. Text over the far end of that gradient was then scored
    against the near end (2026-08-28).
    """
    for prop in ("background-color", "background"):
        if prop in block["decls"]:
            resolved = resolve_var(block["decls"][prop][0], varmap)
            if resolved and _COMPOSED_SURFACE.search(resolved):
                return None
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
    """True when the stylesheet paints a background on anything other than the page element.

    A question about the WHOLE FILE, and so the last resort. It is asked only where the markup
    cannot say which surface a rule's text actually sits on — a `.css` file read on its own, or a
    selector that matches nothing in the page. Asked of a page whose markup IS readable, it turns
    one painted card anywhere in the file into a stand-down for every rule in it, which is the
    defect the ancestor walk below removes (2026-08-28).
    """
    for block in blocks:
        if not _block_paints(block):
            continue
        if all(p.strip() in _ROOT_MARKERS for p in block["selector"].split(",")):
            continue
        return True
    return False


# ---- The markup, so a rule is judged against the surface its own text sits on --------------------
# The stylesheet says which rules paint. Only the markup says which painted surface a given piece of
# text is INSIDE. Without it the reader has to answer "could this text be on a painted surface?" for
# the file as a whole, and the honest answer is almost always yes — one `.card { background: … }`
# anywhere then stands every rule in the page down, including the near-invisible one this lint
# exists to catch. With it the question narrows to the element's own ancestor chain, where it has a
# real answer: the nearest ancestor that paints is the background, and nothing else in the file
# bears on it.

_VOID_TAGS = frozenset((
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
))

# A selector token this reader can match against an element: a tag, an id, classes, `*`, or a
# compound of those. Anything carrying a pseudo-class, a pseudo-element or an attribute test is
# left unmatched rather than guessed at.
_SIMPLE_TOKEN = re.compile(r"^\*?(?:[A-Za-z][-\w]*)?(?:[.#][-\w]+)*$")


class _Element:
    __slots__ = ("tag", "ident", "classes", "style", "parent")

    def __init__(self, tag, ident, classes, style, parent):
        self.tag = tag
        self.ident = ident
        self.classes = classes
        self.style = style
        self.parent = parent

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class _Markup(HTMLParser):
    """Every element in the page, each holding its own ancestor chain.

    Tolerant by design: an unclosed tag, a stray close, or a fragment with no `<html>` leaves the
    rest of the tree readable. A page this cannot parse yields no elements, and the file then falls
    back to the stylesheet-only reading.
    """

    def __init__(self, starts):
        HTMLParser.__init__(self, convert_charrefs=True)
        self._starts = starts
        self._stack = []
        self.elements = []
        self.by_style_offset = {}

    def _offset(self):
        line, col = self.getpos()
        return self._starts[line - 1] + col if line - 1 < len(self._starts) else 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element = _Element(
            tag.lower(),
            (attributes.get("id") or "").strip(),
            frozenset((attributes.get("class") or "").split()),
            attributes.get("style"),
            self._stack[-1] if self._stack else None,
        )
        self.elements.append(element)
        if element.style:
            # The inline block's declarations were found by offset in the raw text; the same span is
            # how that block finds the element it belongs to.
            start = self._offset()
            end = start + len(self.get_starttag_text() or "")
            self.by_style_offset[(start, end)] = element
        if tag.lower() not in _VOID_TAGS:
            self._stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1].tag == tag.lower():
            self._stack.pop()

    def handle_endtag(self, tag):
        tag = tag.lower()
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return


def _read_markup(text, starts):
    parser = _Markup(starts)
    try:
        parser.feed(text)
        parser.close()
    except Exception:  # a page too broken to parse leaves the stylesheet-only reading in place
        return [], {}
    return parser.elements, parser.by_style_offset


def _token_matches(token, element):
    """Whether one simple selector names this element, or None where the reader cannot tell."""
    token = token.strip()
    if not token:
        return None
    if token in _ROOT_MARKERS:
        return element.tag == ("html" if token == ":root" else token)
    if not _SIMPLE_TOKEN.match(token):
        return None
    tag = re.match(r"^\*|^[A-Za-z][-\w]*", token)
    if tag and tag.group(0) != "*" and element.tag != tag.group(0).lower():
        return False
    for ident in re.findall(r"#([-\w]+)", token):
        if element.ident != ident:
            return False
    for name in re.findall(r"\.([-\w]+)", token):
        if name not in element.classes:
            return False
    return True


def _chain_matches(run, element):
    """Whether a descendant chain (`.gg .cap`) names this element and its ancestry."""
    if not run:
        return False
    last = _token_matches(run[-1], element)
    if last is not True:
        return False
    remaining = list(run[:-1])
    for ancestor in element.ancestors():
        if not remaining:
            break
        if _token_matches(remaining[-1], ancestor) is True:
            remaining.pop()
    return not remaining


def _selector_matches(selector, element):
    """Whether any comma-alternative of a selector names this element."""
    for part in selector.split(","):
        if _chain_matches(_selector_run(part), element):
            return True
    return False


def _elements_for(block, elements, by_style_offset):
    """The elements in the markup a block styles, or None where the markup cannot say."""
    if "inline_at" in block:
        for (start, end), element in by_style_offset.items():
            if start <= block["inline_at"] < end:
                return [element]
        return None
    matched = [e for e in elements if _selector_matches(block["selector"], e)]
    return matched or None


def _element_paint(element, blocks, varmap):
    """(rgb, paints) for one element in the markup: its inline background, else the FIRST rule that
    names it and paints. `paints` says it is a surface; `rgb` is its colour where there is one.

    First rather than last, the same way `_selector_own_bg` already reads a token's own colour. The
    cascade says last wins, and this reader does not run the cascade: a media query is invisible to
    it, so a page that states its light colours and then restates them under
    `prefers-color-scheme: dark` looks like one surface painted twice. Taking the first keeps the
    unconditional rule, which is the one every viewer gets.
    """
    if element.style:
        pseudo = {"decls": {}}
        for prop, value, _ in _iter_declarations(element.style, 0):
            pseudo["decls"][prop] = (value, 0)
        if _block_paints(pseudo):
            return _block_bg(pseudo, varmap), True
    for block in blocks:
        if "inline_at" in block or not _block_paints(block):
            continue
        if _selector_matches(block["selector"], element):
            return _block_bg(block, varmap), True
    return None, False


_WHY_MARKUP_OWN = ("the surface this text sits on is painted in a colour this reader cannot pin "
                   "down (a gradient, an image, a translucent or a named colour)")
_WHY_MARKUP_SPLIT = ("this rule's text appears on more than one background in the page, so there "
                     "is no single pair to measure")
_WHY_MARKUP_BARE = ("nothing from this text up to the page declares a background colour, so the "
                    "file states nothing to measure it against")


def _resolve_bg_in_markup(block, blocks, varmap, elements, by_style_offset):
    """(rgb, kind, why) read off the element's own ancestor chain, or None where the markup cannot
    say. `kind` is 'markup' when the pair is determined, 'unresolved' when the chain does not
    determine it, and the caller falls back to the stylesheet-only reading on a None return."""
    targets = _elements_for(block, elements, by_style_offset)
    if not targets:
        return None
    grounds = set()
    split = False
    for element in targets:
        found = None
        for node in [element] + list(element.ancestors()):
            rgb, paints = _element_paint(node, blocks, varmap)
            if paints:
                found = rgb
                break
        grounds.add(found)
        if len(grounds) > 1:
            split = True
    if split:
        return None, "unresolved", _WHY_MARKUP_SPLIT
    ground = grounds.pop()
    if ground is None:
        # Either nothing in the chain paints at all, or the surface it does sit on is painted in a
        # colour this reader cannot read. The two are different things to tell a person.
        painted = any(_element_paint(node, blocks, varmap)[1]
                      for element in targets for node in [element] + list(element.ancestors()))
        return None, "unresolved", _WHY_MARKUP_OWN if painted else _WHY_MARKUP_BARE
    return ground, "markup", None


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


def _resolve_bg(block, blocks, varmap, page_bg, own_surfaces, elements=(), by_style_offset=None):
    """Return (rgb, kind, why) — kind in 'markup' / 'own' / 'ancestor' / 'page' / 'unresolved'.
    `why` is the plain reason on 'unresolved', None otherwise.

    A rule that paints its own background answers for its own text, and nothing outside it bears on
    the pair. Otherwise the markup answers where it can: it is the only thing that says which
    painted surface a given piece of text is inside. The stylesheet-only reading below stands for a
    `.css` file with no page to read and for a rule that matches nothing in the markup.
    """
    if _block_paints(block):
        own = _block_bg(block, varmap)
        return (own, "own", None) if own is not None else (None, "unresolved", _WHY_OWN)
    if elements:
        answer = _resolve_bg_in_markup(block, blocks, varmap, elements, by_style_offset or {})
        if answer is not None:
            return answer
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
    elements, by_style_offset = ((), {}) if is_css_file else _read_markup(text, starts)
    hits = []
    unresolved = []
    for block in blocks:
        sel = block["selector"]
        decls = block["decls"]
        # --- contrast ---
        if "color" in decls:
            resolved = resolve_var(decls["color"][0], varmap)
            fg = _first_color_token(resolved)
            if fg is None and is_translucent(resolved):
                # The text itself is declared translucent, so what it renders as depends on the
                # layer under it — the one thing a static stylesheet read cannot see. Scoring it as
                # its opaque triple, which this lint did until 2026-08-28, invents the number.
                # Dropping it in silence is the same defect the rest of this pass removes, so it is
                # reported for the eye like any other pair the stylesheet does not determine.
                unresolved.append((
                    _line_of(starts, decls["color"][1]), sel,
                    "the text is declared in a translucent colour, so what it renders as depends on "
                    "the layer beneath it — check the real rendered pair by eye",
                ))
            if fg is not None:
                bg, bg_kind, why = _resolve_bg(block, blocks, varmap, page_bg, own_surfaces,
                                               elements, by_style_offset)
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
        if not hits and not unresolved:
            print("OK (preshow-legibility): %s — text meets the contrast and size floor" % label)
        elif not hits:
            # The stand-down, in the shape preshow-register-lint.py already prints when its judge
            # could not read a file: say what was covered rather than let silence read as a pass.
            # Until 2026-08-28 this printed the OK line above however much went unmeasured, so a
            # page the reader could not see half of came back saying its text met the floor.
            print("STOOD DOWN IN PART (preshow-legibility): %s — %d pair(s) below could not be "
                  "measured. Every pair this reader COULD measure meets the contrast and size "
                  "floor; the rest went unread. Read the list before showing the page."
                  % (label, len(unresolved)))
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
            print("UNRESOLVED (preshow-legibility): %s — the stylesheet text does not determine what" % label)
            print("this text renders against; these pairs do NOT block, but check them by eye:")
            json_unresolved = []
            for line_no, snippet, detail in unresolved:
                print("  line %d  [unresolved]  %s" % (line_no, snippet))
                print("          ↳ %s" % detail)
                json_unresolved.append({"line": line_no, "selector": snippet, "detail": detail})
            print(json.dumps({"severity": "info", "code": "legibility-unresolved", "hits": json_unresolved}))
    return 1 if any_hit else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
