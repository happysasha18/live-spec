#!/usr/bin/env python3
"""gen-tree-counts.py — build every count this repository publishes about its own tree from the tree.

WHAT IT DOES. It reads `guardrails/tree-counts.json`, runs each measurement's argument list over the
repository, and fills the generated block on every page that carries one. A page keeping its own
hand-written sentence is left alone here: the gate `guardrails/check-tree-counts.py` renders that
sentence from the same measurement and reds where the page does not carry it.

WHAT AN `ARGV` IS, AND WHY IT IS A CODE SURFACE. A measurement declares `argv`, a list of stages, each
stage a list of literal argument tokens. Two things come out of that one field: what runs, and what a
reader is shown. What runs is `subprocess.Popen` with `shell=False`, stages wired to each other by
pipes, so no shell is involved at any point and a token holding a semicolon, a backtick, a redirect or
a dollar sign is an ordinary argument with no power. What a reader is shown is `render_command`, which
prints the same list. The reader's copy and the run therefore cannot drift, because they are one
field. An edit to an `argv` changes what a push measures, so the registry is reviewed the way a change
to a check script is reviewed (SPEC R306, INV-305).

Three constraints bound an `argv`, and each reds by name before anything runs:

  - A PROGRAM ALLOWLIST. A stage's first token stands in the registry's `allowed_programs`, seven
    programs that read and none that writes. A stage naming anything else reds, and no stage of that
    command runs.
  - PATTERNS EXPAND INSIDE THE REPOSITORY. A token holding `*` or `?` is expanded here with `glob`
    against the root, sorted, so expansion never reaches a shell. A token that is absolute, that holds
    `..`, or that resolves outside the root reds. A pattern matching no file reds naming the pattern
    (SPEC INV-218).
  - A TOKEN IS ONE LINE. A token holding a newline or a null byte reds.

WHAT IT REFUSES. It refuses to build where a ground field is empty, where an empty baseline, direction
or target carries no written reason, where a word rendering falls outside the cardinal table, where a
home names a measurement no entry declares, and where a marker pair is missing from a page it is told
to fill. Every page is built and validated in memory before a byte is written, so a refused build
leaves the committed pages untouched (guardrails/README.md convention 3).

Usage:
  gen-tree-counts.py                     # fill every block on the repository's own pages
  gen-tree-counts.py --root DIR          # measure and read pages under DIR instead
  gen-tree-counts.py --registry FILE     # read a different registry (used by the suite)
  gen-tree-counts.py --out-dir DIR       # write the filled pages under DIR instead
Exit 0 after every page is written, naming each; exit 1 naming what refused to build. Stdlib only.
"""
import argparse
import glob as globmodule
import json
import os
import re
import shlex
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(REPO_ROOT, "guardrails"))
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402
from cleanup_notice import cleanup_notice  # noqa: E402

CHECK = "gen-tree-counts"

REGISTRY_REL = "guardrails/tree-counts.json"

BLOCK_OPEN_FMT = "<!-- generated:count:%s — scripts/gen-tree-counts.py owns the block below -->"
BLOCK_CLOSE_FMT = "<!-- /generated:count:%s -->"

# The seven parts a count carries beside its number, the union of what the rule home already says and
# what the working-state document adds. The generator refuses an entry leaving one of them empty.
GROUND_FIELDS = ("counts", "unit", "decision", "on_move", "compared_to", "better", "target")
# The three of them a count may leave empty where it states the reason it is empty.
GROUND_MAY_BE_EMPTY = ("compared_to", "better", "target")
DIRECTIONS = ("up", "down", "neither")
# A direction reading `neither` states why neither way is better, the same shape an empty baseline
# takes.
DIRECTION_OWES_REASON = "neither"

CLAIMS = ("equals", "at_least", "listing")
RENDERS = ("digits", "digits_grouped", "words", "words_capitalized", "lines")

# One through twenty. A measured value outside this table reds by name asking for a digit rendering or
# for a raised table, so the renderer's edge is visible on the line that reds.
CARDINALS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
             "fifteen sixteen seventeen eighteen nineteen twenty").split()

# A token holding one of these is a path pattern this runner expands itself.
PATTERN_CHARS = ("*", "?")

# How long one stage may run before the build gives up on it, in seconds.
STAGE_SECONDS = 120


class BuildError(Exception):
    """A count refused to build. Raised before anything is written, so the disk is untouched."""


def block_open(name):
    return BLOCK_OPEN_FMT % name


def block_close(name):
    return BLOCK_CLOSE_FMT % name


# --- reading the registry -------------------------------------------------------------------------

def load_registry(path):
    """The parsed registry. Raises BuildError where it does not parse or declares no count."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BuildError("cannot read the registry %s: %s" % (path, e))
    counts = data.get("counts") if isinstance(data, dict) else None
    if not isinstance(counts, dict):
        raise BuildError("the registry %s carries no `counts` map" % path)
    try:
        require_nonempty(CHECK, "the registry's counts", list(counts))
    except VacuousInputError as e:
        raise BuildError(str(e))
    if not data.get("allowed_programs"):
        raise BuildError("the registry %s names no `allowed_programs`, so nothing bounds what a "
                         "measurement may run" % path)
    return data


def ground_value(entry_name, field, held):
    """One ground field's value, with the empty-carrying-a-reason case settled.

    A field is a string, or an object carrying `value` and `reason`. An empty value is accepted where
    the reason is written and refused where it is not, and only the three fields a count may honestly
    leave empty may take that shape at all.
    """
    if isinstance(held, dict):
        value = str(held.get("value", "")).strip()
        reason = str(held.get("reason", "")).strip()
        if value and value != DIRECTION_OWES_REASON:
            return value
        if field not in GROUND_MAY_BE_EMPTY:
            raise BuildError("count %s leaves `%s` empty, and that part is owed on every count"
                             % (entry_name, field))
        if not reason:
            raise BuildError("count %s leaves `%s` empty and states no reason — an empty baseline, "
                             "direction or target is accepted where it carries a written reason and "
                             "refused where it carries none" % (entry_name, field))
        return value
    value = str(held or "").strip()
    if not value:
        raise BuildError("count %s leaves `%s` empty — a count states what it counts, its unit, the "
                         "decision it informs, what changes when it moves, its baseline, its better "
                         "direction and its target" % (entry_name, field))
    return value


def check_ground(entry_name, entry):
    """Every part a count carries beside its number. Raises BuildError naming the field."""
    ground = entry.get("ground")
    if not isinstance(ground, dict):
        raise BuildError("count %s carries no `ground` block, so its number would stand alone"
                         % entry_name)
    for field in GROUND_FIELDS:
        if field not in ground:
            raise BuildError("count %s carries no `%s` in its ground" % (entry_name, field))
        value = ground_value(entry_name, field, ground[field])
        if field == "better":
            held = ground[field]
            word = value or (held.get("value", "").strip() if isinstance(held, dict) else "")
            if word not in DIRECTIONS:
                raise BuildError("count %s reads `better` as %r, and the direction is one of %s"
                                 % (entry_name, word, ", ".join(DIRECTIONS)))


# --- what a measurement may run -------------------------------------------------------------------

def check_token(entry_name, token):
    """One argument token, read for the three constraints that bound it."""
    if not isinstance(token, str):
        raise BuildError("count %s carries the argument %r, which is no text" % (entry_name, token))
    if "\n" in token or "\0" in token:
        raise BuildError("count %s carries an argument holding a newline or a null byte, and a token "
                         "is one line: %r" % (entry_name, token))
    if os.path.isabs(token):
        raise BuildError("count %s carries the absolute argument %s, and a measurement reads inside "
                         "the repository root alone" % (entry_name, token))
    if ".." in token.split(os.sep) or token.startswith(".."):
        raise BuildError("count %s carries the argument %s, which climbs out of the repository root"
                         % (entry_name, token))


def check_argv(entry_name, measurement, allowed):
    """One measurement's whole argument list, read before any stage of it runs."""
    argv = measurement.get("argv")
    if not isinstance(argv, list) or not argv:
        raise BuildError("the measurement %s of count %s carries no `argv` stages"
                         % (measurement.get("name", "<unnamed>"), entry_name))
    for stage in argv:
        if not isinstance(stage, list) or not stage:
            raise BuildError("count %s carries an empty stage in %s"
                             % (entry_name, measurement.get("name", "<unnamed>")))
        program = stage[0]
        if program not in allowed:
            raise BuildError("count %s names the program %s, which the allowlist (%s) does not "
                             "carry; the gate ran no stage of that command"
                             % (entry_name, program, ", ".join(sorted(allowed))))
        for token in stage:
            check_token(entry_name, token)


def check_shape(registry):
    """The whole registry read before anything runs: the ground, the argument lists, the claims, the
    renderings, and every home's pointer into its own entry."""
    allowed = set(registry["allowed_programs"])
    for name, entry in registry["counts"].items():
        check_ground(name, entry)
        measurements = entry.get("measurements") or []
        if not measurements:
            raise BuildError("count %s declares no measurement, so nothing produces its number"
                             % name)
        handles = set()
        for measurement in measurements:
            handle = measurement.get("name")
            if not handle:
                raise BuildError("count %s carries a measurement with no name" % name)
            handles.add(handle)
            check_argv(name, measurement, allowed)
            claim = measurement.get("claim")
            if claim not in CLAIMS:
                raise BuildError("the measurement %s of count %s reads its claim as %r, and a claim "
                                 "is one of %s" % (handle, name, claim, ", ".join(CLAIMS)))
            if claim == "at_least" and not isinstance(measurement.get("floor"), int):
                raise BuildError("the measurement %s of count %s claims at-least and declares no "
                                 "whole-number floor" % (handle, name))
            if measurement.get("render") not in RENDERS:
                raise BuildError("the measurement %s of count %s renders as %r, and a rendering is "
                                 "one of %s" % (handle, name, measurement.get("render"),
                                                ", ".join(RENDERS)))
        homes = entry.get("homes") or []
        if not homes:
            raise BuildError("count %s declares no home, so no page states it" % name)
        for home in homes:
            if home.get("kind") not in ("block", "sentence"):
                raise BuildError("count %s carries a home of kind %r, and a home is a block or a "
                                 "sentence" % (name, home.get("kind")))
            if not home.get("page"):
                raise BuildError("count %s carries a home naming no page" % name)
            if home["kind"] == "sentence":
                if home.get("measurement") not in handles:
                    raise BuildError("count %s states a sentence on %s reading the measurement %r, "
                                     "which the count does not declare"
                                     % (name, home["page"], home.get("measurement")))
                if not home.get("template"):
                    raise BuildError("count %s states a sentence on %s with no template"
                                     % (name, home["page"]))
            else:
                if not home.get("marker"):
                    raise BuildError("count %s states a block on %s naming no marker"
                                     % (name, home["page"]))
                if not home.get("text"):
                    raise BuildError("count %s states a block on %s carrying no text"
                                     % (name, home["page"]))
            if home.get("claim") is not None:
                if home["claim"] not in CLAIMS:
                    raise BuildError("count %s states a home on %s claiming %r, and a claim is one "
                                     "of %s" % (name, home["page"], home["claim"],
                                                ", ".join(CLAIMS)))
                if home["claim"] == "at_least" and not isinstance(home.get("floor"), int):
                    raise BuildError("count %s states a home on %s reading its measurement as a "
                                     "floor and declares no whole-number floor" % (name, home["page"]))
            if home.get("render") is not None and home["render"] not in RENDERS:
                raise BuildError("count %s states a home on %s rendering as %r, and a rendering is "
                                 "one of %s" % (name, home["page"], home["render"],
                                                ", ".join(RENDERS)))


# --- running a measurement --------------------------------------------------------------------------

def expand_stage(entry_name, stage, root):
    """One stage's tokens with every path pattern expanded here, sorted, inside the root."""
    out = []
    for token in stage:
        if not any(char in token for char in PATTERN_CHARS):
            out.append(token)
            continue
        matches = sorted(globmodule.glob(os.path.join(root, token)))
        inside = []
        root_real = os.path.realpath(root)
        for match in matches:
            if os.path.commonpath([os.path.realpath(match), root_real]) != root_real:
                raise BuildError("count %s expands the pattern %s onto %s, which stands outside the "
                                 "root" % (entry_name, token, match))
            inside.append(os.path.relpath(match, root))
        if not inside:
            raise BuildError("count %s reads the pattern %s, which matches no file — a measurement "
                             "over nothing reports a number while counting nothing (SPEC INV-218)"
                             % (entry_name, token))
        out.extend(inside)
    return out


def run_argv(entry_name, argv, root):
    """The last stage's standard output, stages wired to each other by pipes with no shell."""
    env = dict(os.environ)
    # Byte order, so the same command sorts the same way on every machine that runs this gate.
    env["LC_ALL"] = "C"
    processes = []
    previous = None
    for stage in argv:
        expanded = expand_stage(entry_name, stage, root)
        try:
            process = subprocess.Popen(expanded, cwd=root, env=env, shell=False,
                                       stdin=previous.stdout if previous else subprocess.DEVNULL,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            raise BuildError("count %s could not start %s: %s" % (entry_name, expanded[0], e))
        if previous is not None:
            previous.stdout.close()
        processes.append(process)
        previous = process
    try:
        out, err = processes[-1].communicate(timeout=STAGE_SECONDS)
    except subprocess.TimeoutExpired:
        for process in processes:
            process.kill()
            cleanup_notice(ended="pid=%d" % process.pid,
                           what="count stage for %s (ran past %d seconds)" % (entry_name, STAGE_SECONDS),
                           owned_via="pid=%d (a stage this run spawned)" % process.pid)
        raise BuildError("count %s ran past %d seconds and was ended" % (entry_name, STAGE_SECONDS))
    for process in processes[:-1]:
        process.wait()
    if processes[-1].returncode != 0:
        raise BuildError("count %s ran `%s` and it exited %d: %s"
                         % (entry_name, render_command(argv), processes[-1].returncode,
                            err.decode("utf-8", "replace").strip()))
    return out.decode("utf-8", "replace")


def measure(entry_name, measurement, root):
    """One measurement's value: a whole number, or the lines a listing returns."""
    text = run_argv(entry_name, measurement["argv"], root)
    if measurement["claim"] == "listing":
        lines = [line for line in text.split("\n") if line.strip()]
        if not lines:
            raise BuildError("the measurement %s of count %s returned no line"
                             % (measurement["name"], entry_name))
        return lines
    stripped = text.strip()
    try:
        return int(stripped)
    except ValueError:
        raise BuildError("the measurement %s of count %s returned %r, which is no whole number"
                         % (measurement["name"], entry_name, stripped[:80]))


def measure_all(registry, root):
    """Every measurement's value, keyed by count name and measurement handle."""
    values = {}
    for name, entry in registry["counts"].items():
        for measurement in entry["measurements"]:
            values[(name, measurement["name"])] = measure(name, measurement, root)
    return values


# --- rendering ----------------------------------------------------------------------------------

def render_value(entry_name, value, kind):
    """One measured value in the form a page states it."""
    if kind == "lines":
        if not isinstance(value, list):
            raise BuildError("count %s renders a whole number as lines" % entry_name)
        return "\n".join(value)
    if isinstance(value, list):
        raise BuildError("count %s renders a listing as a number" % entry_name)
    if kind == "digits":
        return str(value)
    if kind == "digits_grouped":
        return "{:,}".format(value)
    if not 0 <= value < len(CARDINALS):
        raise BuildError("count %s measures %d and states it as a word, and the cardinal table this "
                         "generator holds runs from zero to twenty — state the count in digits, or "
                         "raise the table" % (entry_name, value))
    word = CARDINALS[value]
    return word.capitalize() if kind == "words_capitalized" else word


def render_command(argv):
    """The reader's copy of a reproduction command, printed from the list the gate runs.

    Every token is quoted the way a shell needs it, except a path pattern: that one is printed bare,
    so the shell a reader hands the line to expands it the way this runner expands it.
    """
    stages = []
    for stage in argv:
        tokens = []
        for token in stage:
            if any(char in token for char in PATTERN_CHARS) and not re.search(r"[\s'\"$`|&;<>()]",
                                                                              token):
                tokens.append(token)
            else:
                tokens.append(shlex.quote(token))
        stages.append(" ".join(tokens))
    return " | ".join(stages)


def rendering_for(measurement, home):
    """The rendering one statement uses: the home's own where it states one, the measurement's
    otherwise. Two statements of one count may spell it differently — a heading capitalizes a word a
    sentence carries in lower case."""
    return home.get("render") or measurement["render"]


def measurement_by_name(entry, handle):
    for measurement in entry["measurements"]:
        if measurement["name"] == handle:
            return measurement
    raise BuildError("no measurement named %r stands under this count" % handle)


def fill(entry_name, text, entry, home, values):
    """A block's text with every declared slot replaced.

    Two slots stand: `{<handle>}` takes the measured value in the rendering that statement uses, and
    `{command:<handle>}` takes the reproduction command printed from the same argument list the gate
    runs. So the command a reader is invited to run is never typed into the prose beside the number
    it produced (SPEC R306.8).
    """
    filled = text
    used = 0
    for measurement in entry["measurements"]:
        command_slot = "{command:%s}" % measurement["name"]
        if command_slot in filled:
            filled = filled.replace(command_slot, render_command(measurement["argv"]))
            used += 1
        slot = "{%s}" % measurement["name"]
        if slot not in filled:
            continue
        rendered = render_value(entry_name, values[(entry_name, measurement["name"])],
                                rendering_for(measurement, home))
        filled = filled.replace(slot, rendered)
        used += 1
    if not used:
        raise BuildError("count %s carries a block naming no measurement slot, so nothing in it "
                         "comes from the tree" % entry_name)
    return filled


def build_block(entry_name, entry, home, values):
    """The whole text of one generated block."""
    return fill(entry_name, home["text"], entry, home, values).strip()


def render_sentence(entry_name, entry, home, values):
    """The sentence one page is required to carry, rendered from the measurement it states."""
    measurement = measurement_by_name(entry, home["measurement"])
    template = home["template"]
    if "{n}" not in template:
        return template
    rendered = render_value(entry_name, values[(entry_name, measurement["name"])],
                            rendering_for(measurement, home))
    return template.replace("{n}", rendered)


# --- the pages ------------------------------------------------------------------------------------

def extract_block(text, marker):
    """The committed text between one marker pair, or None where the pair is not there."""
    opener, closer = block_open(marker), block_close(marker)
    start = text.find(opener)
    end = text.find(closer)
    if start < 0 or end < 0 or end < start:
        return None
    return text[start + len(opener):end].strip()


def splice(text, block, marker):
    """`text` with the marked block replaced. Raises BuildError where the markers are gone."""
    opener, closer = block_open(marker), block_close(marker)
    start = text.find(opener)
    end = text.find(closer)
    if start < 0 or end < 0 or end < start:
        raise BuildError("the page carries no `%s` … `%s` pair, so that generated block has nowhere "
                         "to land" % (opener, closer))
    return "%s%s\n\n%s\n\n%s" % (text[:start], opener, block, text[end:])


def block_homes(registry):
    """Every block home as (count name, entry, home), in registry order."""
    out = []
    for name, entry in registry["counts"].items():
        for home in entry["homes"]:
            if home["kind"] == "block":
                out.append((name, entry, home))
    return out


def sentence_homes(registry):
    """Every sentence home as (count name, entry, home), in registry order."""
    out = []
    for name, entry in registry["counts"].items():
        for home in entry["homes"]:
            if home["kind"] == "sentence":
                out.append((name, entry, home))
    return out


def check_renderings(registry, values):
    """Every statement of every count rendered in memory, so a rendering that cannot be made reds
    before a page is touched. The generator writes no sentence home; it renders one here to hold the
    same refusals over it that a block gets."""
    for name, entry, home in sentence_homes(registry):
        render_sentence(name, entry, home, values)


def build_pages(registry, values, root, out_dir):
    """Every page carrying a block, as {relative path: whole text}, built in memory.

    A page absent under `out_dir` is passed over, which is what lets a fixture run build into a
    scratch directory holding none of the repository's own pages. A page that is there and has lost
    its markers raises, so nothing at all is written.
    """
    pages = {}
    for name, entry, home in block_homes(registry):
        rel = home["page"]
        path = os.path.join(out_dir, rel)
        if not os.path.exists(path):
            continue
        if rel not in pages:
            with open(path, encoding="utf-8") as f:
                pages[rel] = f.read()
        pages[rel] = splice(pages[rel], build_block(name, entry, home, values), home["marker"])
    return pages


def write(pages, out_dir):
    written = []
    for rel, text in pages.items():
        path = os.path.join(out_dir, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        written.append(path)
    return written


def main(argv):
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Build this repository's published tree counts.")
    parser.add_argument("--root", default=REPO_ROOT,
                        help="measure the tree under this directory and read its pages there")
    parser.add_argument("--registry", default=None, help="the registry to read; the pack's own by default")
    parser.add_argument("--out-dir", default=None, help="write the filled pages under this directory")
    args = parser.parse_args(argv[1:])
    root = os.path.abspath(args.root)
    registry_path = args.registry or os.path.join(root, REGISTRY_REL)
    out_dir = os.path.abspath(args.out_dir) if args.out_dir else root

    try:
        registry = load_registry(registry_path)
        check_shape(registry)
        values = measure_all(registry, root)
        check_renderings(registry, values)
        pages = build_pages(registry, values, root, out_dir)
    except BuildError as e:
        print("%s: nothing written — %s" % (CHECK, e))
        return 1
    if not pages:
        print("%s: no page under %s carries a generated block" % (CHECK, out_dir))
        return 0
    for path in write(pages, out_dir):
        print("%s: wrote %s" % (CHECK, path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
