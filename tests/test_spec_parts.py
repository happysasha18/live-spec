"""One spec, written across a core and its parts (the parts map, SPEC INV-250, INV-258, INV-259).

The spec is ONE document. It may be STORED as a core file plus part files: the core carries the
preamble, the glossary and a `## Parts map` table naming its parts in concatenation order, and each
part carries requirements only. `guardrails/specformat.py` is the single reader of that map — every
gate, the index builder and the suite's own `conftest.read()` go through it — so a consumer never
learns whether the spec is one file or thirty.

The map is EMPTY today: the core is the whole spec, and these proofs hold the identity that makes the
move safe — an empty map reads back the file's own bytes, and every consumer behaves as before. The
fixtures below carry a populated map, so the aggregating behaviour is proven now rather than at the
move: a core plus two parts parses, indexes and reads as the one-file document it was cut from, and a
part left out of the map is caught rather than silently dropped (INV-259).
"""
import ast
import glob
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT, SPEC, read, spec_paths

import specformat as sf

FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
MINI = os.path.join(FX, "mini_good.md")
INDEX = os.path.join(FX, "mini_index_good.md")
CORE = os.path.join(FX, "mini_core.md")
PART_A = os.path.join(FX, "mini_part_a.md")
PART_B = os.path.join(FX, "mini_part_b.md")
CORE_DROPPED = os.path.join(FX, "mini_core_part_dropped.md")
CORE_ABSENT = os.path.join(FX, "mini_core_part_absent.md")

BUILDER = os.path.join(ROOT, "scripts", "build-index.py")
INDEX_GATE = os.path.join(ROOT, "guardrails", "check-index-generated.py")


def run(script, *args):
    return subprocess.run(["python3", script, *args], capture_output=True, text=True)


def codes_and_places(text):
    """Every code the body carries, with the R-and-criterion place it sits at — the document's
    identity as far as the index is concerned, independent of which file the bytes came from."""
    return sorted((c.req_num, c.number, tuple(c.codes)) for c in sf.parse(text).criteria)


class TestTheLiveSpecReadsAsOneDocument(unittest.TestCase):
    def test_the_core_leads_the_path_list(self):
        paths = spec_paths()
        self.assertEqual(paths[0], os.path.join(ROOT, SPEC),
                         "the core is the first file of the spec and the source of the part order")

    def test_every_part_the_map_names_is_in_what_the_suite_reads(self):
        text = read(SPEC)
        for p in spec_paths():
            with open(p, encoding="utf-8") as f:
                body = f.read().strip()
            self.assertIn(body, text,
                          "%s is named by the parts map but its bytes are missing from the text the "
                          "suite reads through conftest.read()" % os.path.basename(p))

    def test_an_empty_map_reads_back_the_core_byte_for_byte(self):
        # The identity the infrastructure commit rests on: with no parts declared, the aggregating
        # read IS the plain file read, so the ~140 tests reading the spec see exactly what they saw.
        if len(spec_paths()) > 1:
            self.skipTest("the parts map now names parts — the byte identity below is the "
                          "before-the-move state and no longer applies")
        with open(os.path.join(ROOT, SPEC), encoding="utf-8") as f:
            self.assertEqual(read(SPEC), f.read())


# The names this suite conventionally spells the repository root with. A path anchored at the root
# and ending in the spec's name IS the live file; the same name anchored at a temp dir is a fixture
# repo's own document and none of this rule's business. These two are a FLOOR, not the rule — the
# root is recognised by the VALUE a module binds (see `_root_names`), because three files spell it
# `REPO_ROOT` and a rule that knew only the conventional spellings walked past them.
ROOT_NAMES = ("ROOT", "REPO")
# The reading node, in the spellings a test imports it by. `read_all`/`read_all_flat` go through
# read() themselves, so they reach the whole document too.
NODE_READS = ("read", "read_flat", "read_all", "read_all_flat")
# Calls that turn a name into an open file or its text.
OPENERS = ("open", "Path", "read_text", "read_bytes")


def _call_name(node):
    fn = node.func
    return fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)


def _from_conftest(node):
    """True for `conftest.read(...)` — the node reached through the module rather than by import."""
    fn = node.func
    return (isinstance(fn, ast.Attribute) and fn.attr in NODE_READS
            and isinstance(fn.value, ast.Name) and fn.value.id == "conftest")


def _is_root_expression(node):
    """True for an expression that WALKS UP FROM THIS FILE to the repository root.

    `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` and
    `Path(__file__).resolve().parent.parent` are the two the suite uses. What makes them the root is
    the shape — this file, then two steps up — not the name they are bound to, so a module may call
    the result ROOT, REPO, REPO_ROOT or anything else and still be judged the same.
    """
    dump = ast.dump(node)
    return "__file__" in dump and (dump.count("dirname") >= 2 or dump.count("parent") >= 2)


def _root_names(tree):
    """The names this module binds to the repository root, by value and by convention."""
    names = set(ROOT_NAMES)
    for node in tree.body:
        if isinstance(node, ast.Assign) and _is_root_expression(node.value):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "conftest":
            names.update(a.asname or a.name for a in node.names if a.name == "ROOT")
    return names


def _opens_a_file(node, roots):
    """True where this expression opens a file or builds a path from the repository root."""
    if isinstance(node, ast.Call):
        name = _call_name(node)
        if name in OPENERS:
            return True
        if name == "join" and any(_anchored_at_root(a, roots) for a in node.args):
            return True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) \
            and _anchored_at_root(node.left, roots):
        return True
    return False


def local_readers(tree, roots):
    """The module's own functions that READ A FILE, judged by their bodies.

    A helper is a reader because of what it does — it opens a file, or builds a path from the
    repository root, or calls another helper that does — never because of what it is called. Judging
    by name is how a `def flat(rel)` that opens a file stayed invisible to a guard that looked for
    "read" in the name, and how a module's own `def read(rel)` got taken for the node it shadows.
    A lambda bound to a module-level name is a function like any other and is read the same way.
    """
    defs = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Lambda):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs[t.id] = node.value
    readers, growing = set(), True
    while growing:
        growing = False
        for name, fn in defs.items():
            if name in readers:
                continue
            for node in ast.walk(fn):
                if _opens_a_file(node, roots) or (isinstance(node, ast.Call)
                                                  and _call_name(node) in readers):
                    readers.add(name)
                    growing = True
                    break
    return readers


def _anchored_at_root(node, roots):
    """True when this expression starts from the repository root rather than a temp dir."""
    if isinstance(node, ast.Name):
        return node.id in roots
    if isinstance(node, ast.Attribute):
        return node.attr in roots
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _anchored_at_root(node.left, roots)
    if isinstance(node, ast.Call):
        return _is_root_expression(node) or any(_anchored_at_root(a, roots) for a in node.args)
    return False


def _bindings(tree, filename, seen=None):
    """`(node_names, reader_names)` for one module: which names here ARE the node, and which read a
    file by themselves.

    Legality follows the import, and an import may take one more hop: `test_formal_index` gets its
    `read` from `test_traceability`, which got it from conftest. So an import from a SIBLING test
    module is resolved against that module's own bindings — the node stays the node across the
    re-export, and a sibling's local opener stays an opener. Without this the re-exported call is
    neither, which is the same silence a missing rule gives.

    A name is also bound by plain ASSIGNMENT — `tracked = read`, `canon = read_all_flat`, which is
    how two modules here give the node a name that says what the read is FOR. That rebinding carries
    the node's standing, and it would carry an opener's just as well, so it is followed to a
    fixpoint in both directions.
    """
    seen = seen or set()
    roots = _root_names(tree)
    node_names, readers = set(), local_readers(tree, roots)
    here = os.path.dirname(os.path.abspath(filename))
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if node.module == "conftest":
            for alias in node.names:
                if alias.name in NODE_READS:
                    node_names.add(alias.asname or alias.name)
            continue
        sibling = os.path.join(here, node.module.split(".")[-1] + ".py")
        if node.module in seen or not os.path.isfile(sibling):
            continue
        with open(sibling, encoding="utf-8") as f:
            sib_tree = ast.parse(f.read(), sibling)
        sib_nodes, sib_readers = _bindings(sib_tree, sibling, seen | {node.module})
        for alias in node.names:
            if alias.name in sib_nodes:
                node_names.add(alias.asname or alias.name)
            elif alias.name in sib_readers:
                readers.add(alias.asname or alias.name)

    growing = True
    while growing:
        growing = False
        for node in tree.body:
            if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Name)):
                continue
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            source_is = (node_names if node.value.id in node_names
                         else readers if node.value.id in readers else None)
            if source_is is None:
                continue
            for t in targets:
                if t not in source_is:
                    source_is.add(t)
                    growing = True
    return node_names, readers


def spec_file_reads(source, filename):
    """Every place a test module reads the LIVE spec file, split into node reads and walk-arounds.

    Returns `(node_reads, offenders)` as lists of line numbers, read off the PARSED TREE rather than
    off the text. The rule has to hold for the class, not for one spelling of it: `open(...)`, a
    pathlib `(ROOT / name).read_text()`, a `Path(...)`, a name handed to a module's own `_read`
    helper — a substring scan written against the first of those found four readers of the last kind
    not at all.

    A read is a naming of the spec that is ALSO anchored at the repository root or handed to an
    opener. Naming the file without reading it — an assertion message, a list of document names, a
    fixture repo's own `PRODUCT_SPEC.md` under a temp dir — is not this rule's business and is left
    alone. Of the reads, the legal form is the sole argument of the one node: read/read_flat (and
    read_all/read_all_flat, which pass through it), under whatever name the module imported,
    re-exported or assigned it.

    KNOWN LIMITS, recorded rather than papered over. This rule reads one module's syntax, so four
    shapes are outside it by construction, and a green here does not speak for them:

      - A METHOD reader. `self.read(rel)` resolves through an instance, which syntax alone cannot
        follow. The one in this suite (tests/test_scaffold_guardrails.py) reads its own host fixture
        repo, so flagging it would be WRONG, and telling the two cases apart needs the type, not the
        tree. A class that read the live spec through a method would pass unseen.
      - A reader assembled AT CALL TIME: `getattr(mod, name)(rel)`, a dispatch dict, `functools
        .partial`. Nothing in the suite does this; catching it means interpreting the module.
      - A reader imported from OUTSIDE tests/. The re-export hop resolves sibling test modules; an
        import from a package elsewhere stops where the file lookup does.
      - A read through a SUBPROCESS — a gate invoked with the spec's path on its command line. That
        is a different rule's business: those paths come from `spec_paths()`, and the seven CLI
        tests widened for it are proven in their own files.

    Each limit is a place where this guard is silent, not a place where it says yes.
    """
    tree = ast.parse(source, filename)
    parent = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[id(child)] = node

    # The node is the node whatever a module imports it AS — `from conftest import read as _read`
    # binds it under a private name, and that is how a module with its own helper adopts the node
    # without touching a call site. But the name alone blesses nothing: `read` is legal here only
    # where it came FROM CONFTEST. Seeding this set with the bare names blessed eleven modules that
    # define their own `def read(rel)` over an `open()`, which is the very shadow being hunted.
    node_names, readers = _bindings(tree, filename)
    roots = _root_names(tree)

    # The spec is named by its literal, and also by whatever name is BOUND to that literal —
    # `from conftest import SPEC`, or a module's own `SPEC = "PRODUCT_SPEC.md"`. Once the node
    # exports the constant, `open(os.path.join(ROOT, SPEC))` is the likeliest next regression, and
    # a rule that only knew the literal would not see it.
    spec_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "conftest":
            for alias in node.names:
                if alias.name == "SPEC":
                    spec_names.add(alias.asname or alias.name)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                and node.value.value == SPEC:
            spec_names.update(t.id for t in node.targets if isinstance(t, ast.Name))

    def _names_the_spec(n):
        return ((isinstance(n, ast.Constant) and n.value == SPEC)
                or (isinstance(n, ast.Name) and n.id in spec_names))

    node_reads, offenders = [], []
    for node in ast.walk(tree):
        if not _names_the_spec(node):
            continue
        up = parent.get(id(node))
        if isinstance(up, ast.Call):
            name = _call_name(up)
            if (isinstance(up.func, ast.Name) and name in node_names) or _from_conftest(up):
                node_reads.append(node.lineno)
                continue
            if _opens_a_file(up, roots) or name in readers:
                # an opener, a path built from the root, or the module's own file-reading helper —
                # whatever that helper is called, including `read` itself. Unless the call also
                # carries a root of its own (`_write(tmp, SPEC, ...)`, `read(SPEC, root=project)`):
                # then the file is a fixture repo's own copy and not the document under this rule.
                elsewhere = [a for a in up.args
                             if a is not node and isinstance(a, ast.Name) and a.id not in roots]
                elsewhere += [kw.value for kw in up.keywords
                              if isinstance(kw.value, ast.Name) and kw.value.id not in roots]
                if not elsewhere:
                    offenders.append(node.lineno)
                continue
        elif isinstance(up, ast.BinOp) and isinstance(up.op, ast.Div) \
                and _anchored_at_root(up.left, roots):
            offenders.append(node.lineno)
    return node_reads, offenders


class TestTheSuiteHasOneReadingNode(unittest.TestCase):
    def test_no_test_reads_the_spec_off_its_own_path(self):
        """The claim the whole split rests on: the suite reads the spec through ONE node.

        It was not true when that node landed, and it took three passes to become true, each one
        closing a subclass while the class stayed open. 50 sites opened
        `os.path.join(ROOT, "PRODUCT_SPEC.md")`. Twenty-two more reached the same file by a pathlib
        spelling or through a module's own `_read` helper — invisible to a scan for `open(` on the
        line. Thirty-five more sat behind a module's own `def read(rel)` over an `open()`, blessed
        because the rule seeded the legal names with the bare word `read` and never asked where that
        `read` came from, and behind a `def flat(rel)` that a name-based rule could not see at all.

        So the rule asks the tree two questions and no others. WHERE does the name stand: anchored
        at the repository root, or handed to something that opens files? And WHAT is that something:
        a helper is a reader because its BODY opens a file or builds a path from the root, never
        because of what it is called; the node is the node only where the module imported it FROM
        CONFTEST. Name-based reasoning is what let both of the last two subclasses through.
        """
        offenders = []
        for path in sorted(glob.glob(os.path.join(ROOT, "tests", "*.py"))):
            if os.path.basename(path) in ("conftest.py", os.path.basename(__file__)):
                continue        # the node itself, and this guard, name the file by their nature
            with open(path, encoding="utf-8") as f:
                source = f.read()
            _node_reads, walkarounds = spec_file_reads(source, path)
            offenders += ["%s:%d" % (os.path.basename(path), line) for line in walkarounds]
        self.assertEqual(offenders, [],
                         "a test reads the live spec off its own path instead of through conftest "
                         "(read/read_flat/open_spec); it would go blind to every part the map "
                         "names: %s" % ", ".join(offenders))

    def test_the_guard_names_a_reader_that_walks_around_the_node(self):
        """Red proof for the guard above: each spelling a test could reach the file by is caught.

        Without this, the guard's green says only that nothing matched — including the case where it
        matches nothing because it cannot see, which is how the first two versions of this rule each
        certified a claim that was untrue as they landed. Every shape below was found in this suite,
        by a later version of the rule, after an earlier one had passed it.
        """
        walkarounds = [
            'x = open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8").read()\n',
            'x = (ROOT / "PRODUCT_SPEC.md").read_text(encoding="utf-8")\n',
            'x = (REPO / "PRODUCT_SPEC.md").read_text()\n',
            'x = Path("PRODUCT_SPEC.md").open().read()\n',
            'def _read(rel):\n    return (ROOT / rel).read_text()\nx = _read("PRODUCT_SPEC.md")\n',
            # a module's own `read`, holding the node's own name over an opener: legality has to
            # follow the import, or the shadow is blessed by the very word it shadows
            'def read(rel):\n    with open(os.path.join(REPO, rel)) as f:\n        return f.read()\n'
            'x = read("PRODUCT_SPEC.md")\n',
            # ... and a helper with no reading word in its name at all, which is why a helper is
            # judged by its body
            'def flat(rel):\n    with open(os.path.join(ROOT, rel)) as f:\n'
            '        return " ".join(f.read().split())\nx = flat("PRODUCT_SPEC.md")\n',
            # a reader that is a lambda rather than a def — a function is a function
            'read = lambda rel: open(os.path.join(ROOT, rel)).read()\nx = read("PRODUCT_SPEC.md")\n',
            # an opener given a second name by plain assignment: the rebinding carries the opener's
            # standing exactly as it carries the node's
            'def r(rel):\n    with open(os.path.join(ROOT, rel)) as f:\n        return f.read()\n'
            'tracked = r\nx = tracked("PRODUCT_SPEC.md")\n',
            # the root under a name the conventions do not list, recognised by the value it binds
            'REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
            'x = open(os.path.join(REPO_ROOT, "PRODUCT_SPEC.md")).read()\n',
            # the likeliest NEXT regression: the node exports the name, so the path can be built
            # from the constant and never spell the file at all
            'from conftest import ROOT, SPEC\nx = open(os.path.join(ROOT, SPEC)).read()\n',
            'SPEC = "PRODUCT_SPEC.md"\nx = (ROOT / SPEC).read_text()\n',
        ]
        for src in walkarounds:
            _reads, offenders = spec_file_reads(src, "<walkaround>")
            self.assertTrue(offenders, "the guard passed a reader that walks around the node:\n%s"
                            % src)

        for src in ['from conftest import read\nx = read("PRODUCT_SPEC.md")\n',
                    'from conftest import read_flat\nx = read_flat("PRODUCT_SPEC.md")\n',
                    'from conftest import read as _read\nx = _read("PRODUCT_SPEC.md")\n',
                    'import conftest\nx = conftest.read("PRODUCT_SPEC.md")\n',
                    # the node given a name that says what the read is FOR — two modules here do
                    # exactly this, and before the rule followed assignment their calls were
                    # classified as neither a node read nor an offender
                    'from conftest import read\ntracked = read\nx = tracked("PRODUCT_SPEC.md")\n',
                    'from conftest import read_all_flat\ncanon = read_all_flat\n'
                    'x = canon("PRODUCT_SPEC.md")\n']:
            reads, offenders = spec_file_reads(src, "<node>")
            self.assertEqual(offenders, [], "the guard named the one node an offender:\n%s" % src)
            self.assertTrue(reads, "the guard did not see the node's read at all:\n%s" % src)

        # Naming the file without reading the live one is nobody's business here: an assertion
        # message, a list of document names, a fixture repo's own copy under a temp dir. A guard
        # that reds on these would be turned off within the week.
        for src in ['self.assertIn("PRODUCT_SPEC.md", out)\n',
                    'DOCS = ["PRODUCT_SPEC.md", "ROADMAP.md"]\n',
                    'open(os.path.join(tmp, "PRODUCT_SPEC.md"), "w").write("# fixture\\n")\n']:
            reads, offenders = spec_file_reads(src, "<mention>")
            self.assertEqual((reads, offenders), ([], []),
                             "the guard read a mention as a read of the live spec:\n%s" % src)

    def test_the_guard_follows_a_name_re_exported_by_a_sibling_module(self):
        """A test may take its reader from another TEST module rather than from conftest.

        `test_formal_index` does exactly that — `from test_traceability import read`, and that
        module took it from conftest. The name must stay the node across the hop, and a sibling's
        own opener must stay an opener across the same hop; a rule that resolved neither would call
        both of them nothing at all, which reads exactly like a clean tree.
        """
        with tempfile.TemporaryDirectory(prefix="livespec-test-parts-") as tmp:
            def write(name, text):
                p = os.path.join(tmp, name)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(text)
                return p

            write("sib_node.py", "from conftest import read\n")
            write("sib_own.py",
                  'def read(rel):\n    with open(os.path.join(ROOT, rel)) as f:\n'
                  '        return f.read()\n')

            through_node = write("mod_a.py",
                                 'from sib_node import read\nx = read("PRODUCT_SPEC.md")\n')
            through_own = write("mod_b.py",
                                'from sib_own import read\nx = read("PRODUCT_SPEC.md")\n')

            with open(through_node, encoding="utf-8") as f:
                reads, offenders = spec_file_reads(f.read(), through_node)
            self.assertEqual((bool(reads), offenders), (True, []),
                             "the node stopped being the node across a sibling's re-export")

            with open(through_own, encoding="utf-8") as f:
                reads, offenders = spec_file_reads(f.read(), through_own)
            self.assertTrue(offenders,
                            "a sibling module's own opener passed as if it were the node")


class TestTheMap(unittest.TestCase):
    def test_the_map_names_its_parts_in_order(self):
        with open(CORE, encoding="utf-8") as f:
            self.assertEqual(sf.parts_map(f.read()), ["mini_part_a.md", "mini_part_b.md"])

    def test_a_core_with_no_map_is_the_whole_document(self):
        with open(MINI, encoding="utf-8") as f:
            self.assertEqual(sf.parts_map(f.read()), [])
        self.assertEqual(sf.spec_paths([MINI]), [MINI])

    def test_a_core_expands_to_itself_and_its_parts(self):
        self.assertEqual(sf.spec_paths([CORE]), [CORE, PART_A, PART_B])

    def test_naming_core_and_parts_is_the_same_list(self):
        # A caller may pass the whole list (the gates' command lines do); expansion does not
        # duplicate a part that is already named, so the document is never read twice.
        self.assertEqual(sf.spec_paths([CORE, PART_A, PART_B]), sf.spec_paths([CORE]))

    def test_a_part_named_in_another_spelling_is_still_one_file(self):
        # A person types relative paths at a shell prompt while the map expands to absolute ones.
        # Sameness is the FILE, not the string: were it the string, the parts below would be read
        # twice and every count built over the document — index rows, criteria, bytes — would double.
        rel = [os.path.relpath(p, ROOT) for p in (CORE, PART_A, PART_B)]
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            self.assertEqual(len(sf.spec_paths(rel)), 3)
            self.assertEqual(len(sf.spec_paths([rel[0], PART_A, rel[2]])), 3)
            _paths, joined = sf.read_document(rel)
            self.assertEqual(joined.count("## Requirement 2:"), 1,
                             "a part named in two spellings was read twice")
        finally:
            os.chdir(cwd)


class TestConcatenation(unittest.TestCase):
    def test_a_core_and_its_parts_are_the_one_file_document(self):
        _paths, joined = sf.read_document([CORE])
        with open(MINI, encoding="utf-8") as f:
            one_file = f.read()
        self.assertEqual(codes_and_places(joined), codes_and_places(one_file))
        self.assertEqual([r.number for r in sf.parse(joined).requirements],
                         [r.number for r in sf.parse(one_file).requirements])
        self.assertEqual(sf.parse(joined).glossary_terms, sf.parse(one_file).glossary_terms)

    def test_one_path_and_no_parts_is_the_file_itself(self):
        _paths, text = sf.read_document([MINI])
        with open(MINI, encoding="utf-8") as f:
            self.assertEqual(text, f.read())

    def test_the_join_never_fuses_two_lines(self):
        # mini_part_a.md deliberately ends WITHOUT a trailing newline — a file a person can write
        # and an editor can save. Without the join's own newline its last criterion and the next
        # part's heading would land on one physical line, and both would stop parsing.
        with open(PART_A, encoding="utf-8") as f:
            self.assertFalse(f.read().endswith("\n"),
                             "the fixture that arms this proof gained a trailing newline; the join's "
                             "newline branch is unexercised again")
        _paths, joined = sf.read_document([CORE])
        self.assertIn("[INV-2]\n## Requirement 2:", joined)
        self.assertNotIn("[INV-2]## Requirement", joined)
        self.assertEqual([r.number for r in sf.parse(joined).requirements], [1, 2])


class TestTheBuilderOverParts(unittest.TestCase):
    def test_the_table_over_a_core_equals_the_one_file_table(self):
        r = run(BUILDER, CORE)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(INDEX, encoding="utf-8") as f:
            self.assertEqual(r.stdout, f.read())
        self.assertEqual(r.stdout, run(BUILDER, MINI).stdout)

    def test_naming_the_parts_explicitly_builds_the_same_table(self):
        self.assertEqual(run(BUILDER, CORE, PART_A, PART_B).stdout, run(BUILDER, CORE).stdout)


class TestAPartLeftOutIsCaught(unittest.TestCase):
    def test_the_whole_document_passes_the_index_gate(self):
        r = run(INDEX_GATE, CORE, INDEX)
        self.assertEqual(r.returncode, 0, "the gate red a core whose parts carry the whole "
                                          "committed table:\n%s" % r.stdout)

    def test_a_part_dropped_from_the_map_reds(self):
        # Risk 1 of the split: a part falls out of the map and is silently not indexed. The codes
        # its criteria carry then have no body home, and the committed table over-carries them —
        # the gate reds naming them (INV-259) instead of passing over a document with a hole in it.
        r = run(INDEX_GATE, CORE_DROPPED, INDEX)
        self.assertNotEqual(r.returncode, 0,
                            "a part missing from the map passed unnoticed:\n%s" % r.stdout)
        self.assertIn("INV-259", r.stdout)
        self.assertIn("INV-3", r.stdout, "the gate does not name the code the dropped part carried")

    def test_a_part_the_map_names_and_the_tree_lacks_reds(self):
        r = run(INDEX_GATE, CORE_ABSENT, INDEX)
        self.assertNotEqual(r.returncode, 0,
                            "a map naming a part that is not there passed:\n%s" % r.stdout)
        self.assertIn("cannot read", r.stdout)
        self.assertIn("mini_part_gone.md", r.stdout)

    def test_the_builder_reds_on_a_part_the_map_names_and_the_tree_lacks(self):
        r = run(BUILDER, CORE_ABSENT)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("cannot read", r.stdout)


class TestFreshnessSeesTheParts(unittest.TestCase):
    def test_the_freshness_check_reads_the_parts_directory(self):
        # gate a's freshness rule compares the newest prover record against the newest spec commit.
        # Reading PRODUCT_SPEC.md alone would go blind to a change that lands in a part.
        with open(os.path.join(ROOT, "guardrails", "check-prover-record.sh"), encoding="utf-8") as f:
            self.assertIn("-- PRODUCT_SPEC.md spec/", f.read())


if __name__ == "__main__":
    unittest.main()
