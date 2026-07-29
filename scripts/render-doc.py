#!/usr/bin/env python3
"""render-doc.py — render a Markdown doc into one readable, self-contained HTML page.

Why this exists: documents a human must READ deserve typography, not a code editor
(2026-07-06: a rendered page reads far better than a plain code-editor view). Zero
dependencies — a deliberately modest converter covering what our docs actually use:
headings, paragraphs, bold/italic, inline code, fenced code blocks, lists, tables,
blockquotes, links, horizontal rules.

Usage: render-doc.py IN.md [OUT.html]   (default OUT: alongside IN, .html)
"""
import html
import re
import sys
from pathlib import Path


def slugify(text):
    """GitHub-style heading slug: strip inline markdown markers, lowercase,
    drop punctuation (keep word chars, spaces, hyphens), spaces -> hyphens."""
    text = re.sub(r"[`*]", "", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def unique_slug(text, seen):
    """Slug with GitHub dedupe: a repeated slug gains -1, -2, ..."""
    base = slugify(text)
    if base not in seen:
        seen[base] = 0
        return base
    seen[base] += 1
    return "%s-%d" % (base, seen[base])


def rewrite_href(href):
    """Resolve a doc cross-link: a relative .md target becomes its rendered
    .html neighbour (path kept, extension swapped, fragment slugified); a bare
    in-page #anchor is slugified to land on a heading id; http(s), mailto and
    non-.md paths are left untouched."""
    if href.startswith(("http://", "https://", "mailto:", "tel:", "//")):
        return href
    if href.startswith("#"):
        return "#" + slugify(href[1:])
    path, sep, frag = href.partition("#")
    if path.endswith(".md"):
        newpath = path[:-3] + ".html"
        return newpath + ("#" + slugify(frag) if sep else "")
    return href


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: '<a href="%s">%s</a>' % (rewrite_href(m.group(2)), m.group(1)), s)
    return s


def render(md):
    out, i, lines, seen = [], 0, md.split("\n"), {}
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(html.escape(lines[i]))
                i += 1
            out.append("<pre><code>%s</code></pre>" % "\n".join(block))
            i += 1
            continue
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            n = len(m.group(1))
            hid = unique_slug(m.group(2), seen)
            out.append('<h%d id="%s">%s</h%d>' % (n, hid, inline(m.group(2)), n))
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|?\s*$", lines[i]):
                    cells = [c.strip() for c in lines[i].strip("|").split("|")]
                    rows.append(cells)
                i += 1
            if rows:
                thead = "<tr>%s</tr>" % "".join("<th>%s</th>" % inline(c) for c in rows[0])
                tbody = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r)
                                for r in rows[1:])
                out.append("<table><thead>%s</thead><tbody>%s</tbody></table>" % (thead, tbody))
            continue
        if line.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i].lstrip("> "))
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(block)))
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.) (.*)$", line)
        if m:
            ordered = m.group(2)[0].isdigit()
            items = []
            while i < len(lines):
                m2 = re.match(r"^(\s*)([-*]|\d+\.) (.*)$", lines[i])
                if m2:
                    items.append(m2.group(3))
                    i += 1
                elif lines[i].startswith(("  ", "\t")) and lines[i].strip() and items:
                    items[-1] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue
        if line.strip():
            block = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|```|\s*([-*]|\d+\.) )", lines[i]):
                block.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(block)))
            continue
        i += 1
    return "\n".join(out)


# The mark every page this renderer produces carries, and the one home of its wording. The clearing
# (`scripts/sweep-rendered.py`, SPEC INV-286) reads this exact string to tell a render from a page a
# person built by hand.
GENERATOR = "live-spec render-doc"

STYLE = """
:root { color-scheme: light dark; }
body { font-family: -apple-system, "Segoe UI", Georgia, serif; max-width: 46rem;
       margin: 3rem auto 6rem; padding: 0 1.5rem; line-height: 1.65; font-size: 1.06rem; }
h1 { font-size: 1.7rem; line-height: 1.25; } h2 { font-size: 1.3rem; margin-top: 2.2rem; }
h3 { font-size: 1.1rem; }
code { font-family: ui-monospace, Menlo, monospace; font-size: .9em;
       background: rgba(127,127,127,.14); padding: .1em .35em; border-radius: 4px; }
pre { background: rgba(127,127,127,.10); padding: 1rem; border-radius: 8px; overflow-x: auto; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; margin: 1.2rem 0; display: block; overflow-x: auto;
        position: relative; left: 50%; transform: translateX(-50%);
        width: max-content; max-width: calc(100vw - 3rem); font-size: .84rem; }
th, td { border: 1px solid rgba(127,127,127,.35); padding: .35rem .6rem; text-align: left;
         vertical-align: top; white-space: nowrap; }
td:nth-child(2) { white-space: normal; }
th { background: rgba(127,127,127,.12); }
blockquote { border-left: 3px solid rgba(127,127,127,.4); margin: 1rem 0; padding: .1rem 1.2rem;
             opacity: .85; }
hr { border: none; border-top: 1px solid rgba(127,127,127,.35); margin: 2rem 0; }
a { color: #2f6fed; }
"""


def main():
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".html")
    md = src.read_text(encoding="utf-8")
    title = html.escape(next((l.lstrip("# ") for l in md.split("\n") if l.startswith("# ")), src.name))
    # The generator mark. A page this renderer produced was built for one reading, and the mark is
    # how the clearing recognises it later — after its source document has been renamed or deleted,
    # and without ever mistaking a hand-built page or a host's built site for a render (SPEC INV-286).
    page = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<meta name='generator' content='%s'>"
            "<title>%s</title><style>%s</style></head><body>%s</body></html>"
            % (GENERATOR, title, STYLE, render(md)))
    dst.write_text(page, encoding="utf-8")
    print(dst)


if __name__ == "__main__":
    main()
