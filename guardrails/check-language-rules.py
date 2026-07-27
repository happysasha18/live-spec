#!/usr/bin/env python3
"""check-language-rules.py — the language-rules gate over the source and its generated consumers.

BLOCKING (guardrails/README.md convention 2): a fault exits non-zero and carries the contract's one
typed JSON line beside its human lines. It writes nothing at all, so convention 3 holds by having no
output to half-write.

THE LAW: `guardrails/language-rules.json` is the one home for the rules this project states about how
its own texts are written, and every consumer comes out of it through
`scripts/gen-language-consumers.py`. This gate holds these faults:

  - DRIFT. A committed artifact — `hooks/language-laws.json` or `docs/language-rules.md` — differs
    from a fresh build off the current source. This is the fault that makes the source the single
    home: a rule edited in an artifact is overwritten, a rule edited in the source travels.
  - NOTHING HOLDS IT, AND NOTHING SAYS WHY. A rule with no catcher reading `held`, and no reason
    stated anywhere on it. The reason is a sentence saying why nothing runs the rule. A status word
    repeats that nothing runs it and leaves the why unsaid, so a rule owes that sentence whatever its
    status word reads. The reason stands in the rule's own `notes`, or in the `note` of one of its
    catchers — "a person finds it", "telling a genuine enumeration from a rhetorical triad is a
    meaning call". A rule that
    reads `held` while nothing holds it reds on its own, since its own status word contradicts it.
    Every other reasonless rule counts against MAX_REASONLESS, the cap this arm shipped with, and
    the verdict line names each of them on every run.
  - A RECORD THAT IS NOT THERE. A rule carrying no `catchers` object, or no `armed` field. Those two
    are what a reader opens to learn whether anything runs a rule and where it fires.
  - A SOURCE THAT IS NOT THERE. A `sources` entry naming a repository path that does not exist, or a
    line number past that file's length. A path written as `~/...` names the reader's own tree, and
    the tree's own root decides: where the root stands on this machine, a pin under it names a file
    that should exist, and a missing one reds like any other; where the root is absent, every pin
    under it is counted unread and the count and the absent root are named in the verdict line, so
    the gate gives the same verdict on a machine that carries no personal layer.
  - TWO RULES UNDER ONE HANDLE. Two rules sharing an id, or two rules sharing a name.
  - A RULE THE ARTIFACTS CANNOT RENDER. A rule missing `rule`, `reader_test`, `surfaces`, or
    `status`, or binding a surface outside the generator's surface list.

It declares its expected-non-empty input with the shared guard (INV-218): a source that parses to zero
rules reds by name rather than passing over nothing.

It rides the suite rather than taking a push-gate letter (the letters a–z are spoken for): the suite is
push gate b, so a red here reds that gate and blocks the push.

Usage:
  check-language-rules.py [--source FILE] [--laws FILE] [--doc FILE] [--coverage FILE]
                          [--max-reasonless N]
Exit 0 when the source holds and both artifacts equal a fresh build (printing the reach line, INV-269);
exit 1 naming each fault. Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — green_reach, the gate family's shared verdict line
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-language-rules"

# The debt this arm was turned on over. Widening the catcher arm to read every rule found four rules
# standing with no held catcher and no reason stated anywhere on them (measured 2026-07-28 over 53
# rules). The home is another lane's to edit, so the arm ships as a ratchet rather than a red on four
# rules the day it lands: the count may fall and never rise. One more reasonless rule reds and names
# every rule in the state, and the verdict line names them whatever the count reads, so the debt is
# visible on every run. Lower the cap with the run's own count when the debt is paid.
MAX_REASONLESS = 4


def _load_generator():
    """Load the (hyphen-named) generator so the gate rebuilds the artifacts with the ONE builder —
    no second renderer here to drift from the one that writes them."""
    path = os.path.join(REPO_ROOT, "scripts", "gen-language-consumers.py")
    spec = importlib.util.spec_from_file_location("gen_language_consumers", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def file_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def split_source_pin(pin):
    """A `sources` entry as (path, line) — the line is None where the entry names a whole file."""
    path, sep, tail = pin.rpartition(":")
    if not sep:
        return pin, None
    try:
        return path, int(tail)
    except ValueError:
        return pin, None


def check_shape(rules, surfaces, gen):
    """Faults a rule's own shape carries: a missing field, an unknown surface, a shared handle."""
    problems = []
    seen_ids, seen_names = {}, {}
    for index, rule in enumerate(rules):
        rid = rule.get("id") or "rule #%d (no id)" % (index + 1)
        for field in gen.REQUIRED_FIELDS:
            if not rule.get(field):
                problems.append("%s is missing `%s`, which both artifacts read." % (rid, field))
        for surface in rule.get("surfaces") or []:
            if surface not in surfaces:
                problems.append("%s binds `%s`, which is no surface this project names (%s)."
                                % (rid, surface, ", ".join(surfaces)))
        if rule.get("id"):
            if rule["id"] in seen_ids:
                problems.append("%s carries an id a rule already carries — one rule, one id." % rid)
            seen_ids[rule["id"]] = index
        if rule.get("name"):
            first = seen_names.get(rule["name"])
            if first is not None:
                problems.append("%s carries the name `%s`, which %s already carries — one rule, one name."
                                % (rid, rule["name"], first))
            seen_names[rule["name"]] = rid
    return problems


def stated_reason(rule):
    """Where the rule says why no catcher holds it, or None where it says nowhere.

    Two places count. The rule's own `notes` carry the long form. A catcher's `note` carries the
    short one — "a person finds it", "the actor check is item 5 of the text-audit checklist" — and
    that sentence is the reason a reader is after, so it discharges the duty where it stands.
    """
    if (rule.get("notes") or "").strip():
        return "`notes`"
    catchers = rule.get("catchers")
    if isinstance(catchers, dict):
        for name, catcher in catchers.items():
            if isinstance(catcher, dict) and (catcher.get("note") or "").strip():
                return "the %s catcher's own note" % name
    return None


def check_catchers(rules, cap=MAX_REASONLESS):
    """Every rule's catcher record, read whatever the rule's status word says.

    Returns (problems, the ids standing with no held catcher and no stated reason). A rule claiming
    to be `held` with nothing holding it reds on its own, since its own status word contradicts it.
    Every other reasonless rule counts against the cap, and the count going past the cap reds and
    names each of them.
    """
    problems, reasonless = [], []
    for rule in rules:
        rid = rule.get("id") or "a rule with no id"
        catchers = rule.get("catchers")
        if not isinstance(catchers, dict) or not catchers:
            problems.append("%s carries no `catchers` record — name the pattern, the model and the "
                            "person under it, each with its own status." % rid)
            catchers = {}
        if not rule.get("armed"):
            problems.append("%s carries no `armed` record — name the event or the gate its catchers "
                            "run at, or the word `nowhere`." % rid)
        if any(isinstance(c, dict) and c.get("status") == "held" for c in catchers.values()):
            continue
        if stated_reason(rule):
            continue
        if rule.get("status") == "held":
            problems.append("%s reads `held` while no catcher under it reads `held`, and its `notes` "
                            "are empty — name the catcher that runs it, or say in `notes` why nothing "
                            "does." % rid)
            continue
        reasonless.append(rid)
    if len(reasonless) > cap:
        problems.append("%d rules name no catcher reading `held` and state no reason — %s. The cap "
                        "in guardrails/check-language-rules.py stands at %d and only falls. A status "
                        "word repeats that nothing runs the rule and says nothing about why, so each "
                        "of these owes a sentence in `notes` or in the note of one of its catchers."
                        % (len(reasonless), ", ".join(reasonless), cap))
    return problems, reasonless


def personal_layer_root(path):
    """The reader's own tree a `~` pin stands in: `~/.claude` for `~/.claude/skills/x/SKILL.md`.

    The root is what decides whether a missing file is absent or unread. A pin under a root that
    stands on this machine names a file that should be there.
    """
    parts = path.replace("\\", "/").split("/")
    return os.path.expanduser("/".join(parts[:2]) if len(parts) > 1 else path)


def check_sources(rules):
    """Every `sources` pin resolves. Returns (problems, in-repo pins read, home pins read, home pins
    left unread, the personal-layer roots that are absent on this machine).

    A pin under a personal-layer root that stands here is read like a repository pin: a missing file
    reds. A pin under a root that is absent here is counted unread and its root is named, so a
    machine carrying no personal layer gets the same verdict as this one.
    """
    problems = []
    in_repo = home_read = home_unread = 0
    absent_roots = []
    for rule in rules:
        for pin in rule.get("sources") or []:
            path, line = split_source_pin(pin)
            if path.startswith("~"):
                root = personal_layer_root(path)
                if not os.path.isdir(root):
                    home_unread += 1
                    if root not in absent_roots:
                        absent_roots.append(root)
                    continue
                full = os.path.expanduser(path)
                if not os.path.isfile(full):
                    problems.append("%s names `%s`, the reader's own layer stands at %s, and no file "
                                    "stands at that path."
                                    % (rule.get("id", "a rule with no id"), pin, root))
                    continue
                home_read += 1
            else:
                full = os.path.join(REPO_ROOT, path)
                if not os.path.isfile(full):
                    problems.append("%s names `%s`, and no file stands at that path."
                                    % (rule.get("id", "a rule with no id"), pin))
                    continue
                in_repo += 1
            if line is None:
                continue
            total = file_lines(full)
            if line < 1 or line > total:
                problems.append("%s names `%s`, and that file runs to line %d."
                                % (rule.get("id", "a rule with no id"), pin, total))
    return problems, in_repo, home_read, home_unread, absent_roots


def check_drift(gen, data, artifacts):
    """Both committed artifacts against a fresh build. Returns (problems, built texts)."""
    problems = []
    try:
        built = gen.build(data)
    except gen.BuildError as e:
        return ["the artifacts refuse to build off this source, so drift could not be read: %s" % e], {}
    for rel, path in artifacts.items():
        committed = read_text(path)
        if committed is None:
            problems.append("%s is absent at %s — it is generated output; build it with "
                            "scripts/gen-language-consumers.py." % (rel, path))
            continue
        if committed != built[rel]:
            problems.append("the committed %s differs from a fresh build off the current source — it "
                            "is generated output, never hand-kept; rebuild it with "
                            "scripts/gen-language-consumers.py." % rel)
    return problems, built


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description="Hold the language rules and their "
                                                                "generated consumers.")
    gen = _load_generator()
    parser.add_argument("--source", default=os.path.join(REPO_ROOT, gen.SOURCE_REL))
    parser.add_argument("--laws", default=os.path.join(REPO_ROOT, gen.LAWS_REL))
    parser.add_argument("--doc", default=os.path.join(REPO_ROOT, gen.DOC_REL))
    parser.add_argument("--coverage", default=None)
    parser.add_argument("--max-reasonless", type=int, default=MAX_REASONLESS,
                        help="how many rules may stand with no held catcher and no stated reason; "
                             "the number only falls")
    args = parser.parse_args(argv[1:])

    if not os.path.isfile(args.source):
        print("%s: cannot read %s — the gate stands on the language-rules source."
              % (CHECK, args.source))
        return 1
    try:
        with open(args.source, encoding="utf-8") as f:
            data = json.load(f)
    except ValueError as e:
        print("%s: %s does not parse as JSON: %s" % (CHECK, args.source, e))
        return 1
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list):
        print("%s: %s carries no `rules` list." % (CHECK, args.source))
        return 1
    try:
        require_nonempty(CHECK, "the source's rules", rules)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    # The coverage page sits beside the writer's page, so a fixture run that names only --doc finds
    # the fixture's own coverage build rather than the repository's.
    args.coverage = args.coverage or os.path.join(os.path.dirname(args.doc),
                                                  os.path.basename(gen.COVERAGE_REL))
    artifacts = {gen.LAWS_REL: args.laws, gen.DOC_REL: args.doc, gen.COVERAGE_REL: args.coverage}
    problems = check_shape(rules, gen.SURFACES, gen)
    if problems:
        problems.append("the artifacts were not rebuilt, since a rule the generator cannot render "
                        "makes a drift verdict meaningless.")
        drift_read = False
    else:
        drift, _built = check_drift(gen, data, artifacts)
        problems += drift
        drift_read = True
    catcher_problems, reasonless = check_catchers(rules, cap=args.max_reasonless)
    problems += catcher_problems
    source_problems, in_repo, home_read, home_unread, absent_roots = check_sources(rules)
    problems += source_problems
    if home_unread:
        unread_note = ("leaving %d home pins unread on this machine, since %s does not stand here"
                       % (home_unread, " and ".join(absent_roots)))
    else:
        unread_note = "leaving no home pin unread on this machine"
    if reasonless:
        debt_note = ("%s name no catcher reading `held` and state no reason, against a cap of %d that "
                     "only falls" % (", ".join(reasonless), args.max_reasonless))
    else:
        debt_note = ("every rule either names a held catcher or states why nothing holds it; lower "
                     "the cap in this gate from %d to 0" % args.max_reasonless)

    files = [os.path.basename(args.source), gen.LAWS_REL, gen.DOC_REL, gen.COVERAGE_REL]
    if problems:
        print("%s: %d language-rule fault(s) in %s:" % (CHECK, len(problems), args.source))
        for p in problems:
            print("  - %s" % p)
        record = {
            "severity": "error",
            "code": "language-rules",
            "message": "%d fault(s) across the language rules and their generated consumers: %s"
                       % (len(problems), " ".join(problems)),
            "fix": "edit guardrails/language-rules.json, then run scripts/gen-language-consumers.py "
                   "so both artifacts come out of it again.",
        }
        print(json.dumps(record))
        return 1

    print(sf.green_reach(
        CHECK, files, 0, len(rules),
        "read every rule's fields, catchers, arming point, surfaces and sources in the source; "
        "rebuilt both artifacts in memory and compared them byte for byte with the committed pair "
        "(%s); resolved %d source pins inside the repository and %d under the reader's own home "
        "tree, %s; %s"
        % ("read" if drift_read else "not read", in_repo, home_read, unread_note, debt_note)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
