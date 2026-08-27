#!/usr/bin/env python3
"""check-shipped-language.py — the machine that holds the English + no-personal-names
line on SHIPPED artifacts (ROADMAP row 275, SPEC INV-120). Composes with row 274, which
states the impersonal voice; this script is the machine that holds it.

Three MECHANICAL offences, each reported as file:line so the fix is mechanical:
  (1) cyrillic      a Cyrillic character outside a deliberately-emitted user-language string
  (2) owner-name    a personal name in a shipped spec / README / skill / code comment or prose,
                    matched against the DECLARED ALPHABET's out-of-alphabet name patterns held in
                    the allowlist data (ROADMAP 417) — so this code names no person
  (3) project-name  a foreign project's name, or a dated-incident provenance turn (a project name
                    beside an ISO date), in a CORE SPEC (SPEC INV-245). A core spec states the rule
                    that holds and leaves the project it was first met on and the day it was met to
                    the diaries; a sibling project's name coupled into a core spec binds the spec to
                    a neighbour it should not know, and a dated incident is history the spec carries
                    in place of the diaries that own it. Distinct rationale from (2): cross-project
                    coupling and history leaking into the spec, riding this same gate's mechanism.
                    The forbidden project names are held as allowlist DATA under
                    `project_name_patterns`, so this code names no project. SCOPE: PRODUCT_SPEC.md
                    and ARCHITECTURE.md are STRICT (a bare project name, or one beside an ISO date,
                    reds); TEST_MATRIX.md reds a dated-incident provenance turn while it permits the
                    fixture-ledger's own kind names (a bare name with no adjacent date) and a
                    project-name substring of a test-function name (word-bounded, so it never
                    matches). A package that declares no project_name_patterns leaves this arm inert.

The wish names a FURTHER offence — a coined non-English metaphor where a plain English term
belongs. That is NOT mechanically reliable (a metaphor is a judgement, not a pattern), so
this script deliberately does NOT attempt it: it is left to the human and to the existing
register lints (scripts/spec-style-lint.py — machine-jargon, scissors). Silence here is not
a clean bill on it.

SHIPPED SET (the files a reader outside this machine meets). Spared, by design, are the
local-only diaries and the fixture homes: JOURNAL.md, ROADMAP.md, NEXT_STEPS.md, MIGRATION.md,
and everything under docs/, attic/, inbox/, .live-spec/, tests/, evals/, prototype/ (a
fenced sketch is not shipped product, SPEC INV-17 — and a prod allowlist may not point into
it, so the exclude, not a glob, is its home). The gate's own
machinery is spared too — this detector's own source and its allowlist name the very tokens
they exist to catch, so scanning them would report the detector's patterns as offences.

ALLOWLIST (scripts/shipped-language-allowlist.json — same dated-debt shape as spec-waivers.json,
the equivalence-gate rule: a NEW offence reds, a listed one is counted debt, never a silent pass):
  declared_alphabet   : {out_of_alphabet_name_patterns:[...]} the shipped set's declared alphabet
                        (ASCII English + program strings). A personal name is out-of-alphabet content;
                        its patterns live here as DATA so this code names no person, and covering a
                        collaborator is one line here. A package declaring none leaves the name arm inert.
  project_name_patterns : [...] the foreign project names a CORE SPEC must not carry (SPEC INV-245),
                        held here as DATA so this code names no project; a package declaring none
                        leaves the project-name arm inert. Cross-project coupling and history leaking
                        into a spec, distinct from the personal-name arm above.
  project_name_waivers : [{file, snippet, note, added}] pre-existing project-name debt, counted.
  user_language_globs : files whose Cyrillic is deliberate program data. Cyrillic in them
                        is never an offence.
  authorship_globs    : files where an owner name is a legitimate authorship byline (LICENSE,
                        the plugin manifest's author field, a copyright line). Never an offence.
  cyrillic_waivers    : [{file, snippet, note, added}] pre-existing Cyrillic debt, counted.
  name_waivers        : [{file, snippet, note, added}] pre-existing owner-name debt, counted.
Region rule: Cyrillic inside a fenced ```user ... ``` block, or on a line carrying an inline
marker (`user-language` in a trailing #/<!-- --> comment), is a deliberate sample and spared.

Usage:
  check-shipped-language.py [--root DIR] [--allowlist FILE] [FILE ...]
Exit 0 = no active offence (waived debt may print) . Exit 1 = at least one active offence.
"""
import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS = os.path.join(os.path.dirname(SCRIPT_DIR), "guardrails")
sys.path.insert(0, GUARDRAILS)
import specformat as sf  # noqa: E402

CYRILLIC = re.compile(r"[Ѐ-ӿԀ-ԯ]")
# The owner-name arm inverts to a DECLARED ALPHABET (ROADMAP 417). The shipped set's declared alphabet
# is ASCII English plus deliberate program strings; content outside it reds — a stray script (the
# Cyrillic arm) or a personal name. A name is one instance of out-of-alphabet content, so the specific
# out-of-alphabet name patterns are DECLARED AS DATA in the allowlist rather than enumerated in this
# code, and this detector's own source names no person: covering a collaborator is one data line, not a
# code edit. The alphabet is a per-package declaration; a package that declares none leaves the name arm
# inert, its script (Cyrillic) arm still standing.
# The project-name arm (SPEC INV-245). A core spec — the product spec, the architecture, the test
# matrix — states the rule and leaves the project it was first met on and the day it was met to the
# diaries. The forbidden project names are DECLARED AS DATA in the allowlist (project_name_patterns),
# so this detector's own source names no project, the same discipline the owner-name arm keeps. The
# STRICT specs red a bare project name; every core spec reds a dated-incident provenance turn — a
# project name standing within PROJECT_DATE_WINDOW characters of an ISO date.
#
# Each of the three is written as a CORE file plus PART files (specformat's Parts map): the core
# names its parts, and a part carries requirements/nodes/rows only, no `## Parts map` of its own. The
# project-name rule is a property of the DOCUMENT, not of the one file that happens to open it, so a
# foreign project name landing in a part — e.g. spec/wish-intake.md, a PRODUCT_SPEC.md part — must red
# exactly as it would sitting in the core. Matching by basename alone would only ever see the three
# core filenames and miss every part; `_split_doc_rels` expands each core through
# specformat.spec_paths so the rel-path SET this arm checks against is the whole document.
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
STRICT_PROJECT_FILES = ("PRODUCT_SPEC.md", "ARCHITECTURE.md")
DATED_PROJECT_FILES = ("TEST_MATRIX.md",)
# Character proximity window: a project name this close to an ISO date reads as a dated incident
# mention (allowed) rather than a bare project reference (flagged). No incident or source behind the
# 40 — an engineering default, not a policy decision (the 2026-08-07 census, row 62, found no trace;
# the introducing commit 31437f6 is silent on it). It is a reading of "beside", and it only ever
# EXCUSES a mention: a wrong value lets a bare name pass, it never invents a finding.
PROJECT_DATE_WINDOW = 40


def _split_doc_rels(root, core_name):
    """The relative paths (to `root`) of a split document's core file plus every part its own
    `## Parts map` names — the file-identity set the project-name arm treats as ONE document. A core
    absent from `root`, or carrying no map, resolves to just `{core_name}` (a repo with no split docs,
    or a fixture that passes a bare file, behaves exactly as the old basename check did)."""
    core_path = os.path.join(root, core_name)
    if not os.path.isfile(core_path):
        return {core_name}
    resolved = sf.spec_paths([core_path], root=root)
    return {os.path.relpath(p, root) for p in resolved}


# The marker's openers cover every comment form a marked line can stand in: hash and HTML for
# prose and scripts, slash-star and double-slash for JavaScript and CSS sources. A host once met
# a deliberate visitor-facing string in client code that no allowed opener could clear. The
# opener is anchored to start-of-line or a preceding whitespace character, so a URL fragment
# (`https://user-language...`, opener preceded by a colon) or a path (`docs//user-language.md`,
# opener preceded by a letter) cannot masquerade as a real trailing comment — only an opener that
# actually starts a comment token clears the line.
USER_REGION_MARK = re.compile(r"(?:^|\s)(?:#|<!--|/\*|//)\s*user-language")
FENCE_USER_OPEN = re.compile(r"^\s*```+\s*user\b")
FENCE_ANY = re.compile(r"^\s*```")

EXCLUDE_DIRS = ("docs/", "attic/", "inbox/", ".live-spec/", "tests/", "evals/", "prototype/")
EXCLUDE_FILES = ("JOURNAL.md", "ROADMAP.md", "NEXT_STEPS.md", "MIGRATION.md", "DECISIONS.md",
                 "check-shipped-language.py", "shipped-language-allowlist.json",
                 "check-authority-anchor.py", "authority-anchor.json")
TEXT_EXT = (".md", ".py", ".sh", ".json", ".txt", ".yml", ".yaml", ".html", ".js", ".css")


def load_allowlist(path):
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def compile_owner(allow):
    """Build the out-of-alphabet name matcher from the allowlist's DECLARED ALPHABET, or return None
    when the package declares none. The patterns are the alphabet's data, kept out of this code so the
    detector names no person (ROADMAP 417)."""
    patterns = (allow.get("declared_alphabet") or {}).get("out_of_alphabet_name_patterns") or []
    if not patterns:
        return None
    return re.compile("|".join(patterns), re.IGNORECASE)


def compile_project(allow):
    """Build the foreign-project-name matcher from the allowlist's DECLARED patterns, or return None
    when the package declares none (the arm inert). The patterns are held as data so this code names
    no project (SPEC INV-245)."""
    patterns = allow.get("project_name_patterns") or []
    if not patterns:
        return None
    return re.compile("|".join(patterns), re.IGNORECASE)


def _near_iso_date(raw, span):
    """True when an ISO date sits within PROJECT_DATE_WINDOW characters of the match span — the
    dated-incident shape a project name beside a day makes."""
    s, e = span
    for d in ISO_DATE.finditer(raw):
        if d.start() - e <= PROJECT_DATE_WINDOW and s - d.end() <= PROJECT_DATE_WINDOW:
            return True
    return False


def is_excluded(rel):
    if any(rel == e or rel.endswith("/" + e) for e in EXCLUDE_FILES):
        return True
    return any(rel == d[:-1] or rel.startswith(d) for d in EXCLUDE_DIRS)


def shipped_set(root):
    """Every shipped text file the delivery holds: the index, which carries a file staged for this
    delivery and not yet committed as well as the already-tracked ones. The index is the boundary on
    purpose — a local working note or a vendored directory a person keeps in the tree belongs to no
    delivery, and a blocking gate has no business reading it."""
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"],
                             capture_output=True, text=True, check=True).stdout
        rels = sorted(set(out.splitlines()))
    except Exception:
        rels = []
        for dp, _, fns in os.walk(root):
            for fn in fns:
                rels.append(os.path.relpath(os.path.join(dp, fn), root))
    return [r for r in rels if r.endswith(TEXT_EXT) and not is_excluded(r)]


def globbed(rel, globs):
    return any(fnmatch.fnmatch(rel, g) for g in (globs or []))


def waived(rel, snippet, waivers):
    for w in waivers or []:
        if fnmatch.fnmatch(rel, w.get("file", "")) and w.get("snippet", "") in snippet:
            return True
    return False


def scan_file(path, rel, allow):
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except (UnicodeDecodeError, OSError):
        return
    cyr_file_ok = globbed(rel, allow.get("user_language_globs"))
    name_file_ok = globbed(rel, allow.get("authorship_globs"))
    owner_re = allow.get("_owner_re")
    project_re = allow.get("_project_re")
    # Membership in the split document's WHOLE rel-path set (core + parts), not a basename match —
    # a part file (e.g. spec/wish-intake.md) is the same document as its core (PRODUCT_SPEC.md) for
    # this arm's purposes. See `_split_doc_rels`.
    project_strict = rel in allow.get("_strict_project_rels", ())
    project_dated = rel in allow.get("_dated_project_rels", ())
    in_user_fence = False
    for i, raw in enumerate(lines, 1):
        if FENCE_USER_OPEN.match(raw):
            in_user_fence = True
            continue
        if in_user_fence and FENCE_ANY.match(raw):
            in_user_fence = False
            continue
        snip = raw.strip()[:110]
        if not cyr_file_ok and not in_user_fence and not USER_REGION_MARK.search(raw):
            if CYRILLIC.search(raw) and not waived(rel, snip, allow.get("cyrillic_waivers")):
                yield (i, "cyrillic", snip)
        if not name_file_ok and owner_re is not None:
            if owner_re.search(raw) and not waived(rel, snip, allow.get("name_waivers")):
                yield (i, "owner-name", snip)
        if project_re is not None and (project_strict or project_dated):
            for m in project_re.finditer(raw):
                if project_strict or _near_iso_date(raw, m.span()):
                    if not waived(rel, snip, allow.get("project_name_waivers")):
                        yield (i, "project-name", snip)
                    break


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--allowlist", default=None)
    ap.add_argument("files", nargs="*")
    a = ap.parse_args(argv[1:])
    default_allow = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "shipped-language-allowlist.json")
    allow = load_allowlist(a.allowlist or default_allow)
    allow["_owner_re"] = compile_owner(allow)
    allow["_project_re"] = compile_project(allow)
    # Expand each of the three split documents (core + Parts map) once, so the project-name arm
    # checks a part file the same as its core rather than missing it under a bare basename match.
    allow["_strict_project_rels"] = set().union(
        *(_split_doc_rels(a.root, f) for f in STRICT_PROJECT_FILES))
    allow["_dated_project_rels"] = set().union(
        *(_split_doc_rels(a.root, f) for f in DATED_PROJECT_FILES))

    if a.files:
        pairs = [(f, os.path.relpath(f, a.root)) for f in a.files]
    else:
        pairs = [(os.path.join(a.root, r), r) for r in shipped_set(a.root)]

    offences = []
    for path, rel in pairs:
        for ln, code, snip in scan_file(path, rel, allow):
            offences.append((rel, ln, code, snip))

    if not offences:
        print("OK (shipped-language): no Cyrillic, owner-name, or project-name offences in the shipped set.")
        print('{"severity":"ok","code":"shipped-language","offences":0}')
        return 0

    print("FAIL (shipped-language): a shipped artifact carries Cyrillic outside a deliberate")
    print("user-language string, an owner/personal name (SPEC INV-120), or a foreign project name /")
    print("dated incident in a core spec (SPEC INV-245).")
    for rel, ln, code, snip in offences:
        print("  %s:%d  [%s]  %s" % (rel, ln, code, snip))
    print("  Fix: state the requirement impersonally (row 274) and move candid/Russian process")
    print("  notes to the local-only diaries; state the rule with no project name and no date and")
    print("  move the history (who/when/why) to JOURNAL.md; mark a deliberate sample with a ```user")
    print("  fence or an inline 'user-language' comment; add known pre-existing debt to the allowlist.")
    print('{"severity":"error","code":"shipped-language","offences":%d}' % len(offences))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
