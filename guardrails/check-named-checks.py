#!/usr/bin/env python3
"""check-named-checks.py — gate ae: the check registry says what each runnable file is (SPEC INV-306).

A skill body names a check by path. A project that adopts this pack holds almost none of those paths,
so the pack owes a record of what each named file is: what it does, which tree it judges, whether it
belongs in an adopting project, and what it needs to run. The record is `scripts/check-registry.json`.
This gate keeps that record true by recomputing every field from the tree.

Eight arms:

  A  key        — every key names an existing file under `scripts/` or `guardrails/`.
  B  kind       — check, library or data, recomputed from the tree and compared with the record.
  C  name       — a check carries a lowercase hyphenated handle, unique across the registry; a
                  library or a data entry carries none.
  D  reach      — every document name the entry's own code states appears in reach, read with
                  comments and docstrings stripped, where a reach member whose basename is that
                  name declares it; every reach member naming a path inside the pack exists in the
                  tree.
  E  needs      — every module the entry imports from `scripts/` or `guardrails/` appears in needs,
                  and every needs member is itself a registry key.
  F  root       — argument, working-directory or own-tree. One direction is proved: an entry
                  recorded argument or working-directory whose source carries a scan-root default
                  built from its own file's location reds. The reverse direction stays unproved, so
                  an entry recorded own-tree passes this arm on its record alone.
  G  domain     — a `scripts/` or `guardrails/` path standing in command position in a skill body
                  with no registry entry reds.
  H  kit        — kit is recomputed from reach and compared with the record, and a check whose kit
                  reads pack-only reds when a skill body names it in command position.

Arms G and H read `skills/*/SKILL.md`. A skill's reference pages carry their own command lines and
join a later row.

This gate judges the pack that holds it, so `--root` defaults to that pack's tree and the green line
names the tree it read. The checks the registry records are held to the host-root contract instead:
each of those takes the tree it judges as an argument.

Usage:
  check-named-checks.py [--root DIR] [--registry PATH] [--skills DIR]
"""
import argparse
import io
import json
import os
import re
import sys
import tokenize

CHECK = "check-named-checks"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)

KINDS = ("check", "library", "data")
ROOTS = ("argument", "working-directory", "own-tree")
KITS = ("ships", "host-optional", "pack-only")

# The directories holding machinery this pack authors. A reach member under one of them is what
# makes a check pack-only.
MACHINERY = ("guardrails", "scripts", "skills", "hooks", "adopt",
             "templates", "scaffold", "editions", "evals")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DOC_RE = re.compile(r"\b[A-Z][A-Z_]{2,}\.md\b")
IMPORT_RE = re.compile(
    r"^\s*(?:from\s+([A-Za-z_][A-Za-z0-9_]*)\s+import|import\s+([A-Za-z_][A-Za-z0-9_]*))", re.M)
COMMAND_RE = re.compile(r"(?:python3\s+|bash\s+|sh\s+|\./)((?:scripts|guardrails)/[A-Za-z0-9_./-]+)")
MAIN_RE = re.compile(r"^if\s+__name__\s*==", re.M)
# A scan-root default that resolves to the directory holding the check's own file.
OWN_TREE_RE = re.compile(r"(?:default\s*=|DEFAULT_[A-Z_]*\s*=)[^\n#]*?"
                         r"(__file__|HERE|SCRIPT_DIR|REPO_ROOT)")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_python(src):
    """Return the source with comments and docstrings removed, so a name inside usage text passes."""
    out = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return src
    start_of_line = True
    for i, tok in enumerate(toks):
        if tok.type == tokenize.COMMENT:
            continue
        if tok.type == tokenize.STRING and start_of_line:
            j = i + 1
            while j < len(toks) and toks[j].type in (tokenize.COMMENT, tokenize.NL):
                j += 1
            if j < len(toks) and toks[j].type == tokenize.NEWLINE:
                continue
        if tok.type in (tokenize.NEWLINE, tokenize.NL, tokenize.INDENT,
                        tokenize.DEDENT, tokenize.ENCODING):
            if tok.type in (tokenize.NEWLINE, tokenize.NL):
                start_of_line = True
            out.append(tok.string)
            continue
        start_of_line = False
        out.append(tok.string + " ")
    return "".join(out)


def strip_shell(src):
    return "\n".join(re.sub(r"(^|\s)#.*$", r"\1", line) for line in src.splitlines())


def stripped_source(path, src):
    if path.endswith(".py"):
        return strip_python(src)
    if path.endswith(".sh"):
        return strip_shell(src)
    return src


def imported_modules(root, key, src):
    """Return the registry-shaped paths of the modules KEY imports from scripts/ or guardrails/."""
    found = set()
    for match in IMPORT_RE.finditer(src):
        name = match.group(1) or match.group(2)
        for directory in ("guardrails", "scripts"):
            candidate = "%s/%s.py" % (directory, name)
            if os.path.exists(os.path.join(root, candidate)) and candidate != key:
                found.add(candidate)
    return found


def has_entry_point(src):
    return src.startswith("#!") or bool(MAIN_RE.search(src))


def derive_kind(key, src, imported_by, referenced):
    """Return the kind the tree states for KEY, or None when no kind derives."""
    if key.endswith(".json"):
        return "data" if key in referenced else None
    if key in imported_by and not MAIN_RE.search(src or ""):
        return "library"
    if has_entry_point(src or ""):
        return "check"
    return None


def derive_kit(reach):
    if not reach:
        return "ships"
    for member in reach:
        head = member.split("/")[0]
        if "/" in member and head in MACHINERY:
            return "pack-only"
    return "host-optional"


def is_pack_path(root, member):
    """A reach member names a path inside the pack when its first segment is a pack directory."""
    if "/" not in member or member.startswith("~") or member.startswith("/"):
        return False
    head = member.split("/")[0]
    return os.path.isdir(os.path.join(root, head))


def own_tree_lines(src):
    return [i + 1 for i, line in enumerate(src.splitlines()) if OWN_TREE_RE.search(line)]


def command_positions(skills_dir):
    """Return (skill_body_count, [(relative path, line number, named path)])."""
    hits = []
    bodies = 0
    if not os.path.isdir(skills_dir):
        return 0, hits
    for entry in sorted(os.listdir(skills_dir)):
        body = os.path.join(skills_dir, entry, "SKILL.md")
        if not os.path.isfile(body):
            continue
        bodies += 1
        for number, line in enumerate(read(body).splitlines(), 1):
            for match in COMMAND_RE.finditer(line):
                hits.append((body, number, match.group(1).rstrip(".,;:`)")))
    return bodies, hits


def main(argv=None):
    parser = argparse.ArgumentParser(description="the check registry says what each runnable file is")
    parser.add_argument("--root", default=REPO_ROOT)
    parser.add_argument("--registry")
    parser.add_argument("--skills")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    registry_path = args.registry or os.path.join(root, "scripts", "check-registry.json")
    skills_dir = args.skills or os.path.join(root, "skills")
    registry_label = os.path.relpath(registry_path, root) if registry_path.startswith(root) \
        else registry_path

    findings = []

    if not os.path.exists(registry_path):
        print("%s: RED — the registry is missing at %s." % (CHECK, registry_path))
        print("  Fix: write the registry, one entry per runnable file a skill body names.")
        return 1

    try:
        data = json.loads(read(registry_path))
    except ValueError as err:
        print("%s: RED — the registry at %s does not parse: %s" % (CHECK, registry_label, err))
        print("  Fix: repair the JSON.")
        return 1

    entries = data.get("entries") or {}
    if not entries:
        print("%s: RED — the registry at %s holds 0 entries, so this run measured nothing."
              % (CHECK, registry_label))
        print("  Fix: fill the registry from the tree before running this gate.")
        return 1

    # ---- the tree, read once -------------------------------------------------------------
    sources = {}
    for key in entries:
        path = os.path.join(root, key)
        if os.path.isfile(path) and not key.endswith(".json"):
            try:
                sources[key] = read(path)
            except (OSError, UnicodeDecodeError):
                sources[key] = ""

    imported_by = set()
    for key, src in sources.items():
        imported_by |= imported_modules(root, key, src)

    referenced = set()
    for entry in entries.values():
        for member in list(entry.get("needs") or []) + list(entry.get("reach") or []):
            referenced.add(member)

    # ---- arm A: the key ------------------------------------------------------------------
    for key in sorted(entries):
        head = key.split("/")[0]
        if head not in ("scripts", "guardrails"):
            findings.append(
                ("A", "entry %s lies outside scripts/ and guardrails/, which bound the registry's "
                      "domain. Fix: drop the entry, or move the file into one of those two "
                      "directories." % key))
        elif not os.path.isfile(os.path.join(root, key)):
            findings.append(
                ("A", "entry %s names no file in the tree. Fix: correct the key to the file's "
                      "current path, or drop the entry." % key))

    # ---- arm B: the kind -----------------------------------------------------------------
    for key in sorted(entries):
        recorded = entries[key].get("kind")
        if recorded not in KINDS:
            findings.append(
                ("B", "entry %s records the kind %r, and the three kinds are check, library and "
                      "data. Fix: record one of the three." % (key, recorded)))
            continue
        if not os.path.isfile(os.path.join(root, key)):
            continue
        derived = derive_kind(key, sources.get(key), imported_by, referenced)
        if derived is None:
            findings.append(
                ("B", "entry %s records the kind %s, and the tree states no kind for it: it carries "
                      "no entry point, no other entry imports it, and no entry reads it as data. "
                      "Fix: drop the entry, or give the file the shape its kind states."
                      % (key, recorded)))
        elif derived != recorded:
            findings.append(
                ("B", "entry %s records the kind %s, and the tree states %s. Fix: record the kind "
                      "the tree states." % (key, recorded, derived)))

    # ---- arm C: the name -----------------------------------------------------------------
    seen_names = {}
    for key in sorted(entries):
        entry = entries[key]
        name = entry.get("name")
        if entry.get("kind") == "check":
            if not name:
                findings.append(
                    ("C", "entry %s carries no name, and a check carries the handle a skill body "
                          "uses. Fix: add the name." % key))
                continue
            if not NAME_RE.match(name):
                findings.append(
                    ("C", "entry %s carries the name %r, and a name is lowercase words joined by "
                          "single hyphens. Fix: rewrite the name in that shape." % (key, name)))
            if name in seen_names:
                findings.append(
                    ("C", "entry %s carries the name %r, which entry %s already carries. Fix: give "
                          "one of the two a name of its own." % (key, name, seen_names[name])))
            else:
                seen_names[name] = key
        elif name:
            findings.append(
                ("C", "entry %s is a %s and carries the name %r, and nothing addresses a module or "
                      "a word list by name. Fix: drop the name."
                      % (key, entry.get("kind"), name)))

    # ---- arm D: the reach ----------------------------------------------------------------
    for key in sorted(entries):
        entry = entries[key]
        if entry.get("kind") != "check":
            if entry.get("reach"):
                findings.append(
                    ("D", "entry %s is a %s and carries a reach, and a reach belongs to a check. "
                          "Fix: drop the reach." % (key, entry.get("kind"))))
            continue
        reach = entry.get("reach")
        if reach is None:
            findings.append(
                ("D", "entry %s carries no reach, and a check states what it reads that nobody "
                      "handed it. Fix: add the reach, with an empty list where every target "
                      "arrives on the command line." % key))
            continue
        src = sources.get(key)
        if src is not None:
            declared = set(reach) | set(os.path.basename(m) for m in reach)
            for document in sorted(set(DOC_RE.findall(stripped_source(key, src)))):
                if document not in declared:
                    findings.append(
                        ("D", "entry %s states the document %s in its own code, and its reach does "
                              "not declare it. Fix: add %s to the reach, or take that document on "
                              "the command line." % (key, document, document)))
        for member in reach:
            if is_pack_path(root, member) and not os.path.exists(os.path.join(root, member)):
                findings.append(
                    ("D", "entry %s reaches %s, which the tree does not hold. Fix: correct the "
                          "reach member to the path it means, or drop it." % (key, member)))

    # ---- arm E: the needs ----------------------------------------------------------------
    for key in sorted(entries):
        entry = entries[key]
        kind = entry.get("kind")
        needs = entry.get("needs")
        if kind == "data":
            if needs:
                findings.append(
                    ("E", "entry %s is a data file and carries needs, and a data file reads "
                          "nothing. Fix: drop the needs." % key))
            continue
        if needs is None:
            findings.append(
                ("E", "entry %s carries no needs, and an entry states what it reads at run time. "
                      "Fix: add the needs, with an empty list where it reads nothing." % key))
            continue
        for member in needs:
            if member not in entries:
                findings.append(
                    ("E", "entry %s needs %s, which is no registry entry. Fix: give %s its own "
                          "entry, or drop it from the needs." % (key, member, member)))
        src = sources.get(key)
        if src:
            for module in sorted(imported_modules(root, key, src)):
                if module not in needs:
                    findings.append(
                        ("E", "entry %s imports the module %s, and its needs do not name it. Fix: "
                              "add %s to the needs." % (key, module, module)))

    # ---- arm F: the root -----------------------------------------------------------------
    for key in sorted(entries):
        entry = entries[key]
        if entry.get("kind") != "check":
            if entry.get("root"):
                findings.append(
                    ("F", "entry %s is a %s and records a root, and a root belongs to a check. "
                          "Fix: drop the root." % (key, entry.get("kind"))))
            continue
        recorded = entry.get("root")
        if recorded not in ROOTS:
            findings.append(
                ("F", "entry %s records the root %r, and the three roots are argument, "
                      "working-directory and own-tree. Fix: record one of the three."
                      % (key, recorded)))
            continue
        if recorded == "own-tree":
            continue
        src = sources.get(key)
        if not src:
            continue
        for line in own_tree_lines(src):
            findings.append(
                ("F", "entry %s records the root %s, and %s:%d sets a scan-root default built from "
                      "its own file's location. Fix: record the root own-tree, or take the tree on "
                      "the command line." % (key, recorded, key, line)))

    # ---- arms G and H: the registry against the skill bodies -----------------------------
    bodies, hits = command_positions(skills_dir)
    for body, number, named in hits:
        label = os.path.relpath(body, root) if body.startswith(root) else body
        entry = entries.get(named)
        if entry is None:
            findings.append(
                ("G", "%s:%d names %s in command position, and the registry holds no entry for it. "
                      "Fix: add the entry, or name the file in prose." % (label, number, named)))
            continue
        if entry.get("kind") == "check" and entry.get("kit") == "pack-only":
            reach = ", ".join(entry.get("reach") or []) or "this pack's own tree"
            findings.append(
                ("H", "%s:%d names the check %s in command position, and its kit reads pack-only "
                      "from the reach %s. Fix: name the check in prose, or move what it reads out "
                      "of the pack's own machinery." % (label, number, named, reach)))

    for key in sorted(entries):
        entry = entries[key]
        if entry.get("kind") != "check":
            if entry.get("kit"):
                findings.append(
                    ("H", "entry %s is a %s and records a kit, and a kit belongs to a check. Fix: "
                          "drop the kit." % (key, entry.get("kind"))))
            continue
        recorded = entry.get("kit")
        if recorded not in KITS:
            findings.append(
                ("H", "entry %s records the kit %r, and the three kits are ships, host-optional "
                      "and pack-only. Fix: record one of the three." % (key, recorded)))
            continue
        derived = derive_kit(entry.get("reach") or [])
        if derived != recorded:
            findings.append(
                ("H", "entry %s records the kit %s, and its reach derives %s. Fix: record the kit "
                      "its reach derives." % (key, recorded, derived)))

    # ---- the verdict ---------------------------------------------------------------------
    if findings:
        print("%s: RED — %d finding(s) over %d registry entries and %d skill bodies."
              % (CHECK, len(findings), len(entries), bodies))
        for arm, message in findings:
            print("  arm %s: %s" % (arm, message))
        print('{"severity":"error","code":"%s","findings":%d}' % (CHECK, len(findings)))
        return 1

    kinds = {}
    for entry in entries.values():
        kinds[entry.get("kind")] = kinds.get(entry.get("kind"), 0) + 1
    print("%s: OK — reach: registry=%s; %d entries read (%d checks, %d libraries, %d data files); "
          "%d skill bodies scanned; %d command-position paths found; tree=%s"
          % (CHECK, registry_label, len(entries), kinds.get("check", 0), kinds.get("library", 0),
             kinds.get("data", 0), bodies, len(hits), root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
