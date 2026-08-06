#!/usr/bin/env python3
"""check-tree-counts.py — gate ad: a count this repository publishes about its own tree is built from
the tree (SPEC R306, INV-305).

BLOCKING (guardrails/README.md convention 2): a fault exits non-zero and carries the contract's one
typed JSON line beside its human lines. It writes nothing at all, so convention 3 holds by having no
output to half-write.

THE LAW. Every count this repository publishes about its own tree is declared in
`guardrails/tree-counts.json` with the measurement that produces it and every page statement of it.
Four counts on this pack's two front pages were false on 2026-08-06: the gate roster said thirteen
gates against 29 in the push hook, the rules paragraph said 6,328 lines under `skills/` against 6,370
measured, the same paragraph said 5,178 skill-body lines against 5,216 measured, and the guardrails
page said 80 worker runs against a command whose reading moves between two runs minutes apart. Each
was typed by a person and went stale as the tree grew.

WHAT IT RUNS, AND WHY THE REGISTRY IS A CODE SURFACE. A measurement declares an argument list, and
`scripts/gen-tree-counts.py` runs it through `subprocess.Popen` with `shell=False`, stages wired to
each other by pipes, over a seven-program allowlist that reads and never writes, expanding patterns
inside the repository root. No shell is involved at any point. An edit to an argument list changes
what a push measures, so that registry is reviewed the way a change to a check script is reviewed.

THE PRECONDITION. Before either arm reads, the gate reds where `git status --porcelain` reports an
uncommitted change to a path a measurement reads or to a page holding a statement, naming the path.
Without it a green line could rest on bytes the push does not send.

ARM ONE — DRIFT. For every generated block, a fresh build equals the committed block. This is the
first fault of `guardrails/check-index-generated.py`, applied to counts.

ARM TWO — THE PUBLISHED COMMAND AGAINST THE PUBLISHED NUMBER. For every measurement, the gate runs the
argument list and compares its output against what the pages state: at a generated block, against the
number the committed block carries; at a hand-written sentence, by rendering the template from the
measured value and requiring the page to carry that sentence, whitespace runs collapsed on both sides;
at a claim read as a floor, by requiring the measured value to sit at or above the declared floor with
the literal sentence present.

VACUITY. It declares its expected-non-empty inputs through `guardrails/nonempty_input.py`
(SPEC INV-218): a registry parsing to zero counts reds by name, and a pattern matching zero files reds
by name naming the pattern.

WHAT IT DOES NOT CLAIM. It reads whether a published count matches the tree. It reads nothing about
whether the count is worth publishing, whether the decision named beside it is the real decision, or
whether the ground the paragraph gives is the right ground. Those are readings, and they rest on the
cold reader, on the audit skill's reading step, and on the owner.

Usage:
  check-tree-counts.py [--root DIR] [--registry FILE] [--allow-uncommitted]
`--allow-uncommitted` stands the precondition down so the two arms can be read by hand during a
landing, before the commit. The push chain hands it to nothing.
Exit 0 when every published count matches the tree, printing the reach line (SPEC INV-269); exit 1
naming each fault. Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — green_reach, the gate family's shared verdict line

CHECK = "check-tree-counts"

GENERATOR_REL = "scripts/gen-tree-counts.py"

WHAT_IT_LEAVES_TO_A_PERSON = (
    "this gate judges whether a published count matches the tree, and leaves to the person whether "
    "the count is worth publishing and whether the ground stated around it is the right ground")


def load_generator():
    """Load the (hyphen-named) generator, so the gate rebuilds a block with the ONE builder that
    writes it and no second renderer stands here to drift from it."""
    path = os.path.join(REPO_ROOT, GENERATOR_REL)
    spec = importlib.util.spec_from_file_location("gen_tree_counts", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def flat(text):
    """The text with whitespace runs collapsed, so a sentence wrapped across lines still matches."""
    return " ".join(text.split())


# How much of a rebuilt block a red line quotes. A block carries a whole roster, and a red that
# printed all of it would bury the one sentence a reader needs.
OPENING_CHARS = 160


def opening(text):
    return text if len(text) <= OPENING_CHARS else text[:OPENING_CHARS].rstrip() + " …"


def states(text, rendered):
    """Whether a page states this rendered value as a value of its own.

    Plain containment is not enough: the digits `30` sit inside `INV-301`, so a roster naming that
    code would answer for a gate count that had drifted. The value is matched as a whole token, with
    the digit-grouping comma and the full stop held to be part of a number beside it.
    """
    if "\n" in rendered:
        return flat(rendered) in flat(text)
    return re.search(r"(?<![\w,.])%s(?![\w,.])" % re.escape(rendered), flat(text)) is not None


# --- the precondition -------------------------------------------------------------------------

def measured_paths(gen, registry, root):
    """Every path a measurement reads today, and every pattern it reads them through.

    The expanded paths catch a file that stands; the patterns catch one the working tree has dropped
    or renamed, which `glob` can no longer see and which the push would still send.
    """
    paths, patterns = set(), set()
    for name, entry in registry["counts"].items():
        for measurement in entry["measurements"]:
            for stage in measurement["argv"]:
                for token in stage:
                    if any(char in token for char in gen.PATTERN_CHARS):
                        patterns.add(token)
                        try:
                            expanded = gen.expand_stage(name, [stage[0], token], root)[1:]
                        except gen.BuildError:
                            # A pattern matching nothing reds when the measurement runs, by name.
                            expanded = []
                        for rel in expanded:
                            paths.add(rel)
                    elif os.path.isfile(os.path.join(root, token)):
                        paths.add(token)
    return paths, patterns


def porcelain_paths(root):
    """Every path `git status --porcelain` reports, or None where the root carries no git work tree."""
    inside = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0:
        return None
    result = subprocess.run(["git", "-C", root, "status", "--porcelain"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return None
    out = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        body = line[3:]
        # A rename reads `old -> new`; both sides are paths this push moves.
        for part in body.split(" -> "):
            out.append(part.strip().strip('"'))
    return out


def check_precondition(gen, registry, root, pages):
    """The paths a push would send unchanged while this run measures something else."""
    import fnmatch

    reported = porcelain_paths(root)
    if reported is None:
        return [], "the root carries no git work tree, so the uncommitted-change read stood down"
    paths, patterns = measured_paths(gen, registry, root)
    problems = []
    for rel in reported:
        if rel in pages:
            problems.append("the page %s carries an uncommitted change — this run would read bytes "
                            "the push does not send" % rel)
            continue
        if rel in paths or any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
            problems.append("the measured path %s carries an uncommitted change — this run would "
                            "measure bytes the push does not send" % rel)
    return problems, "read %d path(s) git reports against %d measured path(s) and %d page(s)" % (
        len(reported), len(paths), len(pages))


# --- the two arms ---------------------------------------------------------------------------------

def page_text(root, rel, cache):
    if rel not in cache:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            cache[rel] = None
        else:
            with open(path, encoding="utf-8") as f:
                cache[rel] = f.read()
    return cache[rel]


def check_homes(gen, registry, values, root):
    """Both arms over every statement of every count. Returns (problems, commands run)."""
    problems = []
    commands = []
    cache = {}

    for name, entry in registry["counts"].items():
        for measurement in entry["measurements"]:
            commands.append(gen.render_command(measurement["argv"]))
        for home in entry["homes"]:
            rel = home["page"]
            text = page_text(root, rel, cache)
            if text is None:
                problems.append("count %s states a home on %s, and no such page stands" % (name, rel))
                continue

            if home["kind"] == "block":
                committed = gen.extract_block(text, home["marker"])
                try:
                    fresh = gen.build_block(name, entry, home, values)
                except gen.BuildError as e:
                    problems.append("count %s could not be built: %s" % (name, e))
                    continue
                if committed is None:
                    problems.append(
                        "%s carries no `generated:count:%s` marker pair, so no built block stands "
                        "there for a reader; the tree measures %s, read with `%s`"
                        % (rel, home["marker"], measured_summary(gen, name, entry, values),
                           "`, `".join(gen.render_command(m["argv"])
                                       for m in entry["measurements"])))
                    continue
                # ARM ONE — the committed block against a fresh build.
                if flat(committed) != flat(fresh):
                    problems.append(
                        "the %s block on %s differs from a fresh build — the block is generated "
                        "output; rebuild it with `python3 %s`. The fresh build opens: %s"
                        % (home["marker"], rel, GENERATOR_REL, opening(flat(fresh))))
                # ARM TWO — the published number against the command the page publishes.
                for measurement in entry["measurements"]:
                    slot = "{%s}" % measurement["name"]
                    if slot not in home["text"]:
                        continue
                    rendered = gen.render_value(name, values[(name, measurement["name"])],
                                                gen.rendering_for(measurement, home))
                    if not states(committed, rendered):
                        problems.append(
                            "%s publishes a %s figure the tree does not carry: the command `%s` "
                            "returns %s %s today, and the committed block does not state it"
                            % (rel, name, gen.render_command(measurement["argv"]), rendered,
                               entry["ground"]["unit"] if isinstance(entry["ground"]["unit"], str)
                               else ""))
            else:
                measurement = gen.measurement_by_name(entry, home["measurement"])
                value = values[(name, measurement["name"])]
                claim = home.get("claim") or measurement["claim"]
                try:
                    sentence = gen.render_sentence(name, entry, home, values)
                except gen.BuildError as e:
                    problems.append("count %s could not render its sentence on %s: %s"
                                    % (name, rel, e))
                    continue
                if flat(sentence) not in flat(text):
                    problems.append(
                        "%s does not carry the sentence count %s renders from the tree: %r. The "
                        "command `%s` returns %s today."
                        % (rel, name, sentence, gen.render_command(measurement["argv"]), value))
                if claim == "at_least":
                    floor = home.get("floor", measurement.get("floor"))
                    if value < floor:
                        problems.append(
                            "count %s publishes a floor of %d %s on %s and the tree measures %d — "
                            "the command `%s` is what a reader runs"
                            % (name, floor, entry["ground"]["unit"], rel, value,
                               gen.render_command(measurement["argv"])))
    return problems, commands


def measured_summary(gen, name, entry, values):
    """What the tree says for one count, each number naming what it counts."""
    parts = []
    for measurement in entry["measurements"]:
        value = values[(name, measurement["name"])]
        if isinstance(value, list):
            parts.append("%d %s" % (len(value), entry["ground"]["counts"]))
        else:
            parts.append("%d %s" % (value, entry["ground"]["unit"]))
    return " and ".join(parts)


# --- the run ----------------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Hold every published tree count to the tree.")
    parser.add_argument("--root", default=REPO_ROOT, help="read the tree under this directory")
    parser.add_argument("--registry", default=None, help="the registry to read; the pack's own by default")
    parser.add_argument("--allow-uncommitted", action="store_true",
                        help="stand the uncommitted-change read down, for a run by hand during a "
                             "landing; the push chain hands this to nothing")
    args = parser.parse_args(argv[1:])
    started = time.time()
    root = os.path.abspath(args.root)
    gen = load_generator()
    registry_path = args.registry or os.path.join(root, gen.REGISTRY_REL)

    def red(problems, fix):
        print("%s: %d published-count fault(s) under %s:" % (CHECK, len(problems), root))
        for problem in problems:
            print("  - %s" % problem)
        print(json.dumps({
            "severity": "error",
            "code": "tree-counts",
            "message": "%d fault(s) between the counts this repository publishes and the tree: %s"
                       % (len(problems), " ".join(problems)),
            "fix": fix,
        }))
        return 1

    try:
        registry = gen.load_registry(registry_path)
        gen.check_shape(registry)
    except gen.BuildError as e:
        return red([str(e)],
                   "repair %s so every count carries its ground, its measurement and its homes."
                   % os.path.relpath(registry_path, root))

    pages = []
    for _name, entry in registry["counts"].items():
        for home in entry["homes"]:
            if home["page"] not in pages:
                pages.append(home["page"])

    if not args.allow_uncommitted:
        problems, precondition_reach = check_precondition(gen, registry, root, pages)
        if problems:
            return red(problems,
                       "commit the paths named above, or push without them; this gate measures what "
                       "the push sends.")
    else:
        precondition_reach = "the uncommitted-change read stood down on the command line"

    try:
        values = gen.measure_all(registry, root)
    except gen.BuildError as e:
        return red([str(e)], "repair the measurement named above in %s."
                   % os.path.relpath(registry_path, root))

    problems, commands = check_homes(gen, registry, values, root)
    if problems:
        return red(problems,
                   "run `python3 %s` to rebuild every generated block, and repair a hand-written "
                   "sentence the tree disagrees with." % GENERATOR_REL)

    elapsed = time.time() - started
    print(sf.green_reach(
        CHECK, pages, len(registry["counts"]), len(registry["counts"]),
        "counts read: %s; commands run: `%s`; %s; the run took %.1f seconds against the %s seconds "
        "this registry expects; %s"
        % (", ".join(sorted(registry["counts"])), "`, `".join(commands), precondition_reach, elapsed,
           registry.get("expected_seconds", "unstated"), WHAT_IT_LEAVES_TO_A_PERSON)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
