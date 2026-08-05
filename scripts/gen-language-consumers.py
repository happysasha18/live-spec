#!/usr/bin/env python3
"""gen-language-consumers.py — build the language rules' consumers from their one home.

WHAT IT DOES. It reads the language rules and writes the four files that carry them onward — one page
per reader, and the rule text the judging model reads:

  - `docs/language-rules.md` — the WRITER's page. Per rule: the rule sentence, the reader test, the
    surfaces it binds, the examples, the exceptions, the thresholds, and every list the rule names.
    It opens with the six surfaces defined, the block rule, a roster of the rules binding each
    surface, and a legend for the words its companion page uses; it closes with an index that maps a
    writer's question to the rules answering it. Nothing on this page is about machinery.
  - `docs/language-rule-coverage.md` — the MAINTAINER's page. It opens with the status words and the
    arming events defined, the files that carry the rules, and how to run each kind of catcher by
    hand. Then, per rule: its status, what catches a break of it with how far each catcher reaches,
    where each catcher is armed, the rule text the judging model reads, the files that stated the
    rule before the source became its one home, and the notes with their history. A blind reader of
    the single old page skimmed exactly these fields and reported that none of them changes a word a
    writer writes, which is why they live here. The running instructions moved here on 2026-07-28
    from `docs/language-defects.md`, which is the record of where the rules came from and which
    cannot carry a runbook: a reader there met the arming events and the status words with neither
    defined on the page.
  - `hooks/language-laws.json` — the rule text the judging model reads, one body per surface. A rule
    appears in a surface's body when the rule binds that surface and names the model as a catcher.
    Each entry reads `LAW <n> — <the model-facing sentence>`, then the rule's reader test, then its
    exceptions, numbered from 1 inside each surface. `LAW` is the marker the judge's own parser
    matches (`hooks/register_judge_core.py` renumbers on it), so the marker stays as it is while the
    prose around it calls these rules.
  - `skills/text-audit/references/reader-prompt.md` — the COLD READER's page: the prompt a session
    pastes into a fresh reading session. Its hand-written frame stays as written — the title, the
    opening paragraphs, and the closing paragraph. The pasteable block's stop list is generated: one
    bullet per rule whose owner is a skill and which binds the human-prose surface, sorted by rule
    id, each bullet giving the rule's name and its reader test.

It also owns one BLOCK inside each of several hand-written pages:

  - `docs/language-defects.md` — the record of where the rules came from. Its prose is its own; the
    shared words and roles it is written in stand between the `generated:vocabulary` markers and are
    rewritten on every run. A cold reader is handed one page and cannot follow a pointer to another,
    so a word two pages share is defined on both, out of the one home. The same page states how many
    rules the home carries, which identifier is the highest, and how many stand retired; that sentence
    stands between the `generated:rule-home-totals` markers.
  - `skills/text-audit/references/human-prose-rules.md` — the audit skill's rule sheet. Its own prose
    is hand-written; the rules the skill holds a text to stand between the `generated:human-prose-rules`
    markers. The skill ships to a host and the rule home stays behind, so the skill carries the rules
    with it and still has one home for them. Until 2026-07-28 the skill stated seven of these rules
    again in its own words. The block stood inside `skills/text-audit/SKILL.md` until 2026-07-29, when
    the skill body was split to hold the ~500-line ideal.
  - `docs/plans/2026-07-28-top-level-readability.md` — the readability plan. Its opening count of the
    rules and of the ones binding the spec body stands between the `generated:rule-totals` markers.
  - `docs/language-worked-example.md` — the page that walks one text through the human-prose roster.
    The size of that roster stands between the `generated:human-prose-total` markers.

Those last three blocks landed on 2026-08-05. Each held a hand-typed total that drifted every time a
rule was added, folded, or retired: the plan said 54 rules where the home carried 63, and the record
said 53. A number a reader meets in prose is generated here or it goes stale.

WHAT IT READS. `guardrails/language-rules.json`, plus the config files a rule's `lists` field names:
a list entry carrying `source` and `key` is read out of that JSON at build time, so a list a rule
depends on can never drift from the list its checker reads. No rule text, no word list, and no
threshold is held here, so a rule is edited in the source and regenerated.

WHAT IT REFUSES. It refuses to write a partial result: every artifact is built and validated in
memory, and a failure in any of them leaves the committed files untouched (guardrails/README.md
convention 3). It refuses a source that parses to no rules, a rule missing a field an artifact needs,
a surface the list below does not name, a surface roster the source and this file disagree on, a
question-index entry naming a rule that is gone, a list naming a config file or a key that is gone,
and a human-prose surface bound by no skill-owned rule. It writes no date or count into an artifact
that the next run would change on its own.

Usage:
  gen-language-consumers.py                    # write every artifact under the repository root
  gen-language-consumers.py --out-dir DIR      # write them under DIR instead (used by the suite)
  gen-language-consumers.py --source FILE      # read a different source (used by the suite)
Exit 0 after every artifact is written, naming each; exit 1 naming what refused to build.
Stdlib only.
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(REPO_ROOT, "guardrails"))
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "gen-language-consumers"

SOURCE_REL = "guardrails/language-rules.json"
LAWS_REL = "hooks/language-laws.json"
DOC_REL = "docs/language-rules.md"
COVERAGE_REL = "docs/language-rule-coverage.md"
# The hand-written page that applies the human-prose roster to one text end to end. The writer's page
# points at it, and its own prose is hand-written; the one sentence stating how large that roster is
# comes from here, since the roster grows whenever a rule binding human prose is added.
WORKED_EXAMPLE_REL = "docs/language-worked-example.md"
# The plan that ordered the readability work. Its opening states how many rules this project holds its
# own writing to and how many of them bind the spec body — two counts out of the rule home.
PLAN_REL = "docs/plans/2026-07-28-top-level-readability.md"

# The hand-written record of where the rules came from. Its prose is its own, and the shared words it
# is written in are spliced into it between the markers below, so a cold reader handed that one page
# holds every word it uses. A page carrying such a block is a SPLICED consumer: the generator owns
# what stands between the markers and touches nothing else in the file.
RECORD_REL = "docs/language-defects.md"
# The audit skill's rule sheet, which ships to a host that installs the pack. The rule home stays
# behind, so the skill carries the rules a human-prose audit holds a text to, printed here out of that
# home. It sits under the skill's `references/` directory, which is where a skill body puts material a
# reader loads on demand; the skill body points at it.
AUDIT_SKILL_REL = "skills/text-audit/references/human-prose-rules.md"
# The cold reader's page: the prompt a session pastes into a fresh reading session. This one is a
# full artifact, not a spliced block — the generator owns the whole file, frame and all, because the
# frame's own claim about how many stop classes the block prints changes with the source.
READER_PROMPT_REL = "skills/text-audit/references/reader-prompt.md"
# This page is itself held to the human-prose rules it lists, so its own opening line states the
# same fact GENERATED_LINE does without the all-capitals word r23 bans outside a defined acronym.
READER_PROMPT_GENERATED_LINE = (
    "Generated by scripts/gen-language-consumers.py from %s. Edit the source and run the generator; "
    "a hand edit here reds guardrails/check-language-rules.py." % SOURCE_REL
)
BLOCK_OPEN_FMT = "<!-- generated:%s — scripts/gen-language-consumers.py owns the block below -->"
BLOCK_CLOSE_FMT = "<!-- /generated:%s -->"
# Each spliced page and the block it lends the generator. `guardrails/check-language-rules.py` reads
# this map to compare the standing block with a fresh build, so a page appears here once.
SPLICED = {RECORD_REL: "vocabulary", AUDIT_SKILL_REL: "human-prose-rules",
           PLAN_REL: "rule-totals", WORKED_EXAMPLE_REL: "human-prose-total"}
# A page lending a SECOND block. The record page states the rule-home totals in its opening and defines
# the shared words further down, and those two blocks answer to different parts of the source. The gate
# named above reads one block per page, so a block here is owned and rewritten on every run while its
# drift between runs goes unread; giving that gate a second loop is the repair.
SECOND_SPLICED = {RECORD_REL: "rule-home-totals"}


def block_open(name):
    return BLOCK_OPEN_FMT % name


def block_close(name):
    return BLOCK_CLOSE_FMT % name

# The surface names the source's rules bind to, in the order a reader meets them. This tuple is the
# list's one home: the gate `guardrails/check-language-rules.py` imports it, so the list stays
# in one place, and a rule naming anything outside it reds there. The source carries a definition and
# an example for each of these names, and a build reds when the two rosters disagree.
SURFACES = ("spec-body", "human-prose", "chat", "artifact", "commit", "worker-brief")

# The fields an artifact reads off every rule.
REQUIRED_FIELDS = ("rule", "reader_test", "surfaces", "status")

GENERATED_LINE = (
    "GENERATED by scripts/gen-language-consumers.py from %s. Edit the source and run the generator; "
    "a hand edit here reds guardrails/check-language-rules.py." % SOURCE_REL
)

CATCHER_NAMES = ("pattern", "model", "person")

# A list member longer than this reads as a sentence rather than a token, so its list is rendered as
# plain bullets instead of a run of backticked words.
INLINE_MEMBER_MAX_CHARS = 26


class BuildError(Exception):
    """An artifact refused to build. Raised before anything is written, so the disk is untouched."""


# --- reading the source -------------------------------------------------------------------------

def load_source(path):
    """The parsed source. Raises BuildError when it does not parse or carries no rules."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BuildError("cannot read the source %s: %s" % (path, e))
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list):
        raise BuildError("the source %s carries no `rules` list" % path)
    try:
        require_nonempty(CHECK, "the source's rules", rules)
    except VacuousInputError as e:
        raise BuildError(str(e))
    return data


def rule_field(rule, field):
    value = rule.get(field)
    if value in (None, "", []):
        raise BuildError("rule %s is missing `%s`" % (rule.get("id", "<no id>"), field))
    return value


def surface_list(data):
    surfaces = (data.get("surfaces") or {}).get("list")
    if not surfaces:
        raise BuildError("the source carries no `surfaces.list`, so no surface can be defined for a "
                         "reader")
    return surfaces


def check_shape(data):
    """Every rule carries the fields the artifacts read, and every roster in the source resolves."""
    rules = data["rules"]
    for rule in rules:
        for field in REQUIRED_FIELDS:
            rule_field(rule, field)
        for surface in rule["surfaces"]:
            if surface not in SURFACES:
                raise BuildError("rule %s binds `%s`, which no surface name covers"
                                 % (rule["id"], surface))

    named = tuple(s["name"] for s in surface_list(data))
    if named != SURFACES:
        raise BuildError("the source defines the surfaces %s while this generator names %s — one "
                         "roster, one order" % (", ".join(named), ", ".join(SURFACES)))

    ids = {r["id"] for r in rules}
    for entry in data.get("question_index") or []:
        for rid in entry["rules"]:
            if rid not in ids:
                raise BuildError("the question `%s` names rule %s, which no rule carries — a folded id "
                                 "leaves the index pointing at nothing" % (entry["question"], rid))


def model_holds(rule):
    """True when the rule names the model as a catcher — the test for a law body's membership."""
    model = rule.get("catchers", {}).get("model", {})
    return model.get("status") != "absent" and bool(model.get("law_text", "").strip())


# --- the lists a rule names -----------------------------------------------------------------------

_CONFIG_CACHE = {}


def read_config(rel):
    """One config file, parsed and cached. A missing or unparseable file refuses the build, since a
    rule naming a list it cannot give is the defect this field exists to end."""
    if rel not in _CONFIG_CACHE:
        path = os.path.join(REPO_ROOT, rel)
        try:
            with open(path, encoding="utf-8") as f:
                _CONFIG_CACHE[rel] = json.load(f)
        except (OSError, ValueError) as e:
            raise BuildError("a rule names the list in %s and that file cannot be read: %s" % (rel, e))
    return _CONFIG_CACHE[rel]


def list_members(entry, rule_id):
    """The members of one `lists` entry: read out of a config file, or carried inline.

    A member is a string, or a (written, repair) pair where the list is a mapping or a list of
    objects carrying two named fields. `shape` says which the config holds:
      plain  a list of strings (the default)
      map    an object, read as pairs of key and value
      field  a list of objects, one named field taken from each
      pairs  a list of objects, two named fields taken from each as a pair
    """
    if "members" in entry:
        return list(entry["members"])
    node = read_config(entry["source"])
    for step in entry["key"].split("."):
        if not isinstance(node, dict) or step not in node:
            raise BuildError("rule %s names the list `%s` in %s, and no key `%s` stands there"
                             % (rule_id, entry["name"], entry["source"], entry["key"]))
        node = node[step]
    shape = entry.get("shape", "plain")
    where = "rule %s names the list `%s` in %s at `%s`" % (rule_id, entry["name"], entry["source"],
                                                           entry["key"])
    if shape == "map":
        if not isinstance(node, dict) or not node:
            raise BuildError("%s as a mapping, and what stands there is no mapping" % where)
        return [(k, v) for k, v in node.items()]
    if not isinstance(node, list) or not node:
        raise BuildError("%s, and what stands there is no list" % where)
    try:
        if shape == "field":
            return [item[entry["field"]] for item in node]
        if shape == "pairs":
            return [(item[entry["from"]], item[entry["to"]]) for item in node]
    except (KeyError, TypeError):
        raise BuildError("%s, and a member there carries no such field" % where)
    return list(node)


def render_lists(rule):
    """Every set a rule names, given in full, with the home each set was taken from."""
    entries = rule.get("lists") or []
    if not entries:
        return []
    out = ["**The lists this rule names.**", ""]
    for entry in entries:
        members = list_members(entry, rule["id"])
        if "members" in entry:
            home = "%d members, whose home is %s" % (len(members), entry["home"])
        else:
            home = ("%d members, read at build time from `%s` under `%s`"
                    % (len(members), entry["source"], entry["key"]))
        if entry.get("note"):
            home += "; %s" % entry["note"].strip().rstrip(".")
        paired = members and isinstance(members[0], tuple)
        inline = not paired and all(len(str(m)) <= INLINE_MEMBER_MAX_CHARS for m in members)
        if inline:
            out.append("- *%s* — %s: %s" % (entry["name"], home,
                                            ", ".join("`%s`" % m for m in members)))
        else:
            out.append("- *%s* — %s:" % (entry["name"], home))
            for member in members:
                if paired:
                    out.append("    - %s → %s" % (code(member[0]), code(member[1])))
                else:
                    out.append("    - %s" % member)
    out.append("")
    return out


# --- the rule text the judging model reads --------------------------------------------------------

def sentence(text):
    """A source phrase closed as a sentence, so a law body reads in prose."""
    text = text.strip()
    return text if text.endswith((".", "?", "!")) else text + "."


def render_law(number, rule):
    """One law: its numbered statement, the reader test, and the exceptions the rule carries."""
    model = rule["catchers"]["model"]
    lines = ["LAW %d — %s" % (number, sentence(model["law_text"]))]
    lines.append("Reader test: %s" % sentence(rule["reader_test"]))
    exceptions = rule.get("exceptions") or []
    if exceptions:
        label = "Exception" if len(exceptions) == 1 else "Exceptions"
        lines.append("%s: %s" % (label, sentence("; ".join(e.strip() for e in exceptions))))
    return "\n".join(lines)


def model_checkers(rule):
    """The checkers that RUN a rule's model law, read off `catchers.model.where`.

    A `where` is a comma-separated list of homes, each opening with the checker's own path and naming
    the mechanism it runs through after `via` (the source's `_comment` states the convention). Taking
    the opening path of each home is what separates two readers of one mechanism: the chat judge and
    the pre-show document lint both run through `hooks/register_judge_core.py` while holding different
    laws.
    """
    out = []
    for home in (rule["catchers"]["model"].get("where") or "").split(","):
        home = home.strip()
        if not home:
            continue
        checker = home.split()[0].split(":")[0]
        if checker and checker not in out:
            out.append(checker)
    return out


def build_laws(data):
    """The law artifact: one body per checker and surface, its laws numbered from 1 inside that body.

    A body holds the laws one checker runs on one surface, so a checker asking for its own body by
    name is handed the laws it holds and no others.
    """
    pairs = {}
    for rule in data["rules"]:
        if not model_holds(rule):
            continue
        for checker in model_checkers(rule):
            for surface in rule["surfaces"]:
                pairs.setdefault((checker, surface), []).append(rule)

    bodies = {}
    for checker in sorted({c for c, _ in pairs}):
        by_surface = {}
        for surface in SURFACES:
            members = pairs.get((checker, surface))
            if not members:
                continue
            laws = []
            for rule in members:
                model = rule["catchers"]["model"]
                entry = {
                    "number": len(laws) + 1,
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "home": model.get("where", ""),
                    # A home under `~/` is the reader's own layer; the package ships no personal rule, so
                    # a consumer reading this artifact tells the two apart without parsing the path.
                    "personal_home": "~/" in model.get("where", ""),
                    "text": render_law(len(laws) + 1, rule),
                }
                if "personal_override" in rule:
                    entry["personal_override"] = rule["personal_override"]
                laws.append(entry)
            by_surface[surface] = {"laws": laws,
                                   "text": "\n\n".join(law["text"] for law in laws)}
        bodies[checker] = by_surface
    return {
        "_generated": GENERATED_LINE,
        "source": SOURCE_REL,
        "generator": "scripts/gen-language-consumers.py",
        "reading": ("A body is keyed by the checker that runs the law and the surface it runs on: "
                    "`bodies[<checker path>][<surface>]`. It holds the rules binding that surface whose "
                    "`catchers.model.where` names that checker, numbered from 1 inside the body. `text` "
                    "is the body to hand the model; `laws` names each law's rule and the home its text "
                    "comes from, and `personal_home` marks a law whose home is the reader's own personal "
                    "layer, which the package ships to nobody — a checker filters those out and lets the "
                    "reader's own overlay supply them at run time."),
        "bodies": bodies,
    }


def laws_text(obj):
    """The artifact's exact bytes: escaped to ASCII, so a law quoting the reader's own alphabet
    travels through the shipped-language gate as program data."""
    return json.dumps(obj, indent=2, ensure_ascii=True) + "\n"


# --- pieces both pages share ------------------------------------------------------------------------

def code(text):
    """A value shown as code where it holds no backtick of its own."""
    text = str(text)
    return "`%s`" % text if "`" not in text else text


def join_phrases(items):
    return "; ".join(str(i).strip() for i in items)


def render_thresholds(thresholds):
    parts = []
    for name, value in thresholds.items():
        if isinstance(value, list):
            # A pair of numbers is a band, and reads as one; a longer list reads as a list.
            shown = " to ".join(str(v) for v in value) if len(value) == 2 else ", ".join(
                str(v) for v in value)
        else:
            shown = str(value)
        parts.append("%s = %s" % (name, shown))
    return join_phrases(parts)


def render_override(override):
    parts = []
    for field, value in override.items():
        if isinstance(value, list):
            shown = join_phrases(value) if value else "nothing"
        else:
            shown = str(value)
        parts.append("the rule's `%s` with %s" % (field, shown))
    return join_phrases(parts)


LEGEND_TITLES = {
    "rule_status": "A rule's **status** says whether anything catches a break of it today.",
    "catcher_status": "Each **catcher** under a rule carries a status of its own.",
    "armed": "**Armed at** names the moment a catcher runs, and what a break costs there.",
    "owner": "A rule's **owner** names the one thing that decides a break of it. The status words "
             "above say what runs today; the owner says what is meant to run.",
}


def render_legend(data, closing):
    """The status words and the arming events, defined on each page a reader meets them from."""
    legend = data.get("legend") or {}
    if not legend:
        raise BuildError("the source carries no `legend`, so the status words stand undefined")
    out = ["## The words these pages use", ""]
    for group, body in legend.items():
        out.append(LEGEND_TITLES.get(group, "**%s**." % group))
        out.append("")
        for word, meaning in body.items():
            out.append("- `%s` — %s." % (word, meaning.rstrip(".")))
        out.append("")
    out.append(closing)
    out.append("")
    return out


def render_vocabulary(data):
    """The words and roles every page here is written in, defined on each page that uses them.

    A cold reader is handed one page and cannot follow a pointer to another, so a word two pages
    share is defined on both. The source is the one home; this renderer is how it reaches each page.
    """
    vocab = data.get("vocabulary") or {}
    words = vocab.get("words") or []
    roles = vocab.get("roles") or []
    if not words or not roles:
        raise BuildError("the source carries no `vocabulary` with both `words` and `roles`, so the "
                         "shared words stand undefined on every page built from it")
    out = ["## The words on this page", ""]
    note = vocab.get("note", "")
    if note:
        out.extend([note, ""])
    for entry in words:
        out.append("- **%s** — %s." % (entry["word"], entry["definition"].rstrip(".")))
    out.append("")
    out.append("Five roles appear wherever these rules are discussed.")
    out.append("")
    for entry in roles:
        out.append("- **%s** — %s." % (entry["role"], entry["definition"].rstrip(".")))
    out.append("")
    closing = vocab.get("closing", "")
    if closing:
        out.extend([closing, ""])
    return out


def render_surfaces(data, rules):
    """The six surfaces defined, the block rule, and the roster of rules binding each surface."""
    out = ["## The surfaces, and which rules bind each one", ""]
    out.append((data.get("surfaces") or {}).get("note", ""))
    out.append("")
    for surface in surface_list(data):
        binding = [r["id"] for r in rules if surface["name"] in r["surfaces"]]
        out.append("### %s" % surface["name"])
        out.append("")
        definition = surface["definition"]
        out.append("%s%s Example: %s" % (definition[:1].upper(), definition[1:], surface["example"]))
        out.append("")
        out.append("Binds %d of the %d rules: %s." % (len(binding), len(rules), " · ".join(binding)))
        out.append("")
    return out


# --- the writer's page --------------------------------------------------------------------------

def render_rule_writer(rule):
    """One rule as a writer meets it: what to do, how to test a sentence, and every list it names."""
    out = ["### %s — %s" % (rule["id"], rule["name"]), ""]
    out.append("**Rule.** %s" % sentence(rule["rule"]))
    out.append("")
    out.append("**Reader test.** %s" % sentence(rule["reader_test"]))
    out.append("")
    out.append("**Binds.** %s" % " · ".join(rule["surfaces"]))
    out.append("")
    if rule.get("examples"):
        out.append("**Examples.**")
        out.append("")
        for example in rule["examples"]:
            out.append("- %s → %s" % (code(example["written"]), code(example["repair"])))
        out.append("")
    if rule.get("exceptions"):
        out.append("**Exceptions.** %s" % sentence(join_phrases(rule["exceptions"])))
        out.append("")
    if rule.get("personal_override"):
        out.append("**In force for this reader.** The reader's own layer replaces %s, and that "
                   "replacement is what binds a text written here."
                   % render_override(rule["personal_override"]))
        out.append("")
    if rule.get("thresholds"):
        out.append("**Thresholds.** %s" % sentence(render_thresholds(rule["thresholds"])))
        out.append("")
    out.extend(render_lists(rule))
    return out


def render_question_index(data, rules):
    """The closing index: a writer's question, and the rules that answer it."""
    entries = data.get("question_index") or []
    if not entries:
        return []
    by_id = {r["id"]: r for r in rules}
    out = ["## An index of questions", "",
           "A writer arrives with a question and not yet the name of a defect, and every rule title on "
           "this page is written as the name of a defect. Each question below names every rule that "
           "answers it.", ""]
    for entry in entries:
        out.append("**%s**" % entry["question"])
        out.append("")
        for rid in entry["rules"]:
            out.append("- %s — %s" % (rid, by_id[rid]["name"]))
        out.append("")
    return out


def build_doc(data):
    """The writer's page: the surfaces, the legend, one entry per rule, and the index of questions."""
    rules = data["rules"]
    out = ["<!-- %s -->" % GENERATED_LINE, ""]
    out.append("# Language rules — what to write")
    out.append("")
    out.append("This page states every rule this project holds its own texts to, in the words a writer "
               "applies to a sentence. Its companion `%s` carries the machinery: what catches a break of "
               "each rule, how far that catcher reaches, where it is armed, and where the rule was "
               "stated before `%s` became its one home. Nothing on that page changes a word you write. "
               "One page carrying the whole human-prose roster at once stands at `%s`, with the rule "
               "ids named at each fix."
               % (COVERAGE_REL, SOURCE_REL, WORKED_EXAMPLE_REL))
    out.append("")
    out.append("Read this page in one order. Find your surface below and read the rules its roster "
               "names — that roster is the whole set governing your text. Each rule is written out once, "
               "in id order, under **The rules**. When you arrive with a question rather than a defect, "
               "the index at the end names the rules that answer it.")
    out.append("")
    out.append("This page is generated from `%s`, which is where every one of these rules is edited. A "
               "change made here is overwritten by the next run of `scripts/gen-language-consumers.py`, "
               "and the gate `guardrails/check-language-rules.py` reds a page that has drifted from the "
               "source." % SOURCE_REL)
    out.append("")
    out.extend(render_vocabulary(data))
    out.extend(render_surfaces(data, rules))
    out.extend(render_legend(
        data,
        "No rule on this page carries a status, and that is deliberate: a rule binds a text whether or "
        "not a machine checks it. The words above are defined here because `%s` states them of every "
        "rule." % COVERAGE_REL))
    out.append("## The rules")
    out.append("")
    for rule in rules:
        out.extend(render_rule_writer(rule))
    out.extend(render_question_index(data, rules))
    return "\n".join(out).rstrip("\n") + "\n"


# --- the maintainer's page ------------------------------------------------------------------------

# The operating half of this page: which files carry the rules, and how a person runs each kind of
# catcher over a text by hand. It stands here rather than in the source because it describes the
# machinery around every rule and not any one rule.
OPERATING = """## The files that carry the rules

Every command on this page runs from the repository root, the directory that holds `PRODUCT_SPEC.md`,
`guardrails/`, and `scripts/`.

- `%(source)s` — the source. Every rule is edited here and nowhere else.
- `%(doc)s` — the writer's page, built from the source. A hand edit here is thrown away by the next run
  of the generator.
- `%(coverage)s` — this page, built from the source and thrown away the same way.
- `%(laws)s` — the rules in the form the judging model reads, built from the source, one body per
  catcher and surface.
- `scripts/gen-language-consumers.py` — the generator. It reads the source and writes the three built
  files above.
- `guardrails/check-language-rules.py` — the gate. It refuses a built file that has drifted from the
  source, and a rule pointing at a file or a line that is gone.

Rebuild the three built files, then check them:

```
python3 scripts/gen-language-consumers.py
python3 guardrails/check-language-rules.py
```

## Running a catcher by hand

Each rule below names its catchers. A rule's **Status** line names the events its catchers are armed
at, and the legend above says what a break costs at each of those events.

### A script catcher

A rule's `pattern` catcher names the file that carries it. Those files are Python scripts, and each
takes the text to read as its argument:

```
python3 guardrails/check-vocabulary.py PRODUCT_SPEC.md
python3 scripts/preshow-register-lint.py %(doc)s
```

Each prints one line on a clean run. A script under `guardrails/` also states how far it read, so its
passing verdict says how much of the text it covered.

`scripts/preshow-register-lint.py` is one script making two passes over a document that is about to be
shown to a person. It always reads the text line by line against its own list of coined phrases, loan
translations, and respellings. It also makes the model call described below, and it makes that call
only when the environment variable `PRESHOW_REGISTER_JUDGE` is set to `1`, since the call costs a live
model run.

### The model catcher

The model catcher is one model call, made by `hooks/register_judge_core.py`. That module is handed the
text together with the rules binding the text's surface, which it reads from `%(laws)s`, and it
answers with the sentences that break one. Two scripts make the call, one on each surface it runs on
today.

On chat, `hooks/register-judge.py` makes the call. `hooks/register-judge-collect.sh` runs at the
session's Stop event, starts that script in the background and returns at once;
`hooks/register-judge-report.sh` runs when the person sends their next message and prints whatever
verdict landed in the meantime. The person has already read the reply that broke the rule by then, so
the correction reaches them one turn later.

Making that call by hand needs a session transcript, which the script takes as a Stop-hook payload on
its standard input. A transcript is a `.jsonl` file at
`~/.claude/projects/<project>/<session>.jsonl`, where `<project>` is the working directory's path with
its slashes turned into dashes and `<session>` is the session's own identifier. Neither is worth typing
out; take the newest transcript on the machine instead:

```
transcript=$(ls -t ~/.claude/projects/*/*.jsonl | head -1)
printf '{"transcript_path": "%%s"}' "$transcript" | python3 hooks/register-judge.py
```

When the turn breaks a rule, the script prints one JSON line. It names what broke and tells the session
to hold its reply until a correction goes out. A clean turn gets no output.

On a document, `scripts/preshow-register-lint.py` makes the call, at the moment the document is about
to be shown to a person. One call took about 33 seconds when it was measured on 2026-07-17, almost all
of it spent starting the `claude` command-line program the call runs through:

```
PRESHOW_REGISTER_JUDGE=1 python3 scripts/preshow-register-lint.py docs/language-defects.md
```

Either script stands down on its own breakage: no `claude` binary on the path, a timeout, or an answer
the script cannot parse leaves the text unjudged, says so on standard error, and blocks nothing.

### A person reading the text

A person is the catcher no script and no model replaces, and a reading runs the same way every time.
Hand the reader the text alone — no repository, no earlier draft, and no chance to ask the writer a
question — together with the job the text is meant to serve, where it serves one. Ask for every place
the reading stopped: what the reader stopped on, the guess the reader made there, and whether the stop
kept the reader from going on. Write the answer to a dated file under `docs/language-reads/`, and
repair the text from those stops rather than from the one sentence in front of you.
`docs/language-defects.md` records what every past reading returned and what each one changed.

""" % {"source": SOURCE_REL, "doc": DOC_REL, "coverage": COVERAGE_REL, "laws": LAWS_REL}


def render_catcher(name, catcher):
    """One catcher line: what it is, its status, where it lives, and how far it reads."""
    where = catcher.get("where", "").strip()
    line = "- **%s** — %s." % (name, catcher.get("status", "absent"))
    if where:
        line += " Lives at %s." % where
    reach = catcher.get("reach", "").strip()
    if reach:
        line += " Reach: %s" % sentence(reach)
    note = catcher.get("note", "").strip()
    if note:
        line += " Reads: %s" % sentence(note)
    law = catcher.get("law_text", "").strip()
    if law:
        line += " Rule text the judging model reads: %s" % sentence(law)
    return line


def render_rule_coverage(rule):
    """One rule as a checker-maintainer meets it: what runs, where, how far, and what came before."""
    out = ["### %s — %s" % (rule["id"], rule["name"]), ""]
    out.append("**Binds.** %s" % " · ".join(rule["surfaces"]))
    out.append("")
    out.append("**Status.** %s, armed at %s."
               % (rule["status"], ", ".join(rule.get("armed") or ["nowhere"])))
    out.append("")
    owner = rule.get("owner")
    if owner:
        out.append("**Owner.** %s — %s" % (owner["by"], sentence(owner["why"])))
        out.append("")
    if rule.get("personal_override"):
        out.append("**Personal layer.** The reader's own layer replaces %s."
                   % render_override(rule["personal_override"]))
        out.append("")
    out.append("**What catches a break of it.**")
    out.append("")
    for name in CATCHER_NAMES:
        catcher = rule.get("catchers", {}).get(name)
        if catcher:
            out.append(render_catcher(name, catcher))
    out.append("")
    sources = rule.get("sources") or []
    out.append("**Stated before this page, at.** %s"
               % (", ".join(sources) if sources else
                  "nowhere; no file outside the source stated the rule."))
    out.append("")
    if rule.get("notes", "").strip():
        out.append("**Notes.** %s" % sentence(rule["notes"]))
        out.append("")
    return out


def build_coverage(data):
    """The maintainer's page: the legend, then what runs each rule and what stated it before."""
    rules = data["rules"]
    out = ["<!-- %s -->" % GENERATED_LINE, ""]
    out.append("# Language rules — what catches a break of each one")
    out.append("")
    out.append("This page is for whoever maintains the catchers. Its companion `%s` states the rules "
               "themselves, in the words a writer applies; this page adds, per rule, its status, what "
               "catches a break of it and how far each catcher reads, where each catcher is armed, the "
               "rule text the judging model reads, the files that stated the rule in prose before `%s` "
               "became its one home, and the notes with their history." % (DOC_REL, SOURCE_REL))
    out.append("")
    out.append("It opens with three things a reader needs before any single rule: the status words and "
               "the arming events defined, the files that carry the rules, and how to run each kind of "
               "catcher over a text by hand. `docs/language-defects.md` is the record of where these "
               "rules came from, and it sends a reader here for all of it.")
    out.append("")
    out.append("The entries stand in the same order as on the writer's page, under the same headings, "
               "so one rule is read on both pages by its id.")
    out.append("")
    out.append("This page is generated from `%s`. A change made here is overwritten by the next run of "
               "`scripts/gen-language-consumers.py`, and the gate `guardrails/check-language-rules.py` "
               "reds a page that has drifted from the source." % SOURCE_REL)
    out.append("")
    out.extend(render_vocabulary(data))
    out.extend(render_legend(
        data,
        "A path written as `~/...` names the reader's own `.claude` tree, which the package ships to "
        "nobody; every other path is relative to the repository root."))
    out.extend(OPERATING.rstrip("\n").split("\n"))
    out.append("")
    out.append("## The rules")
    out.append("")
    for rule in rules:
        out.extend(render_rule_coverage(rule))
    return "\n".join(out).rstrip("\n") + "\n"


# --- the cold reader's page ------------------------------------------------------------------------

def reader_prompt_rules(data):
    """Every rule the cold-reader prompt prints, sorted by id.

    A rule prints here when its owner is a skill — deciding a break of it needs a model reading the
    text for meaning, the same judgment a cold reader makes — and it binds the human-prose surface.
    """
    rules = [r for r in data["rules"]
             if r.get("owner", {}).get("by") == "skill" and "human-prose" in r["surfaces"]]
    if not rules:
        raise BuildError("no skill-owned rule binds human-prose, so the cold-reader prompt would ship "
                         "empty")
    return sorted(rules, key=lambda r: r["id"])


def render_reader_prompt_stops(rules):
    """The stop list inside the pasteable block: one bullet per rule, its name then its reader test."""
    out = []
    for rule in rules:
        test = rule["reader_test"].strip()
        if test:
            test = test[:1].lower() + test[1:]
        out.append("- %s — %s" % (rule["name"], test))
    return out


def build_reader_prompt(data):
    """The cold-reader prompt: its hand-written frame kept, its stop list generated from the rules."""
    rules = reader_prompt_rules(data)
    out = ["<!-- %s -->" % READER_PROMPT_GENERATED_LINE, ""]
    out.append("# The cold-reader prompt, ready to paste")
    out.append("")
    out.append("This file belongs to the `text-audit` skill, whose body is [`../SKILL.md`](../SKILL.md). "
               "One test in the body decides whether a finding blocks: the reader could not go on, or "
               "would have applied the text wrongly. The body's section \"The cold reader\" lists the "
               "kinds most blocking findings fall into. It also says who reads under this prompt and "
               "what to do with what comes back.")
    out.append("")
    out.append("This prompt prints every rule bound to human prose whose owner is a skill: %d of the "
               "%d rules the rule home carries. The rules at "
               "[`human-prose-rules.md`](human-prose-rules.md) name every other class an audit holds a "
               "text to. Judging those classes needs a rulebook the cold reader does not hold. The "
               "prompt's last instruction takes every other stop the reader met, so a class the printed "
               "list does not name still comes back." % (len(rules), len(data["rules"])))
    out.append("")
    out.append("Paste the block below verbatim into the cold-reader session, under that one test for "
               "a blocking finding, with the text appended.")
    out.append("")
    out.append("```")
    out.append("You are reading a piece of text for the first time. You have no background on it: no")
    out.append("project history, no earlier draft, no knowledge of what the author meant beyond the "
               "words")
    out.append("on the page. Read it once, straight through, as a stranger who needs to understand it "
               "and")
    out.append("act on it.")
    out.append("")
    out.append("Mark every place you stop. A stop is any one of these:")
    out.extend(render_reader_prompt_stops(rules))
    out.append("")
    out.append("For each stop, write one entry with five parts:")
    out.append("1. the quoted phrase;")
    out.append("2. where it sits (the heading or the opening words of its paragraph);")
    out.append("3. what a stranger cannot tell from the page alone;")
    out.append("4. the guess you made in place of the missing answer;")
    out.append("5. blocking or non-blocking.")
    out.append("")
    out.append("Do not fix anything. Report only where you stopped and why. Return the entries as a "
               "numbered")
    out.append("list. If you stopped nowhere, say so in one line.")
    out.append("")
    out.append("At every relational word, ask the three questions and write which one is unanswered: "
               "relative")
    out.append("to what? by what measure? or else what alternative? A word the list above does not "
               "name, that")
    out.append("still stopped you, is a real find — report it and note that it is new.")
    out.append("")
    out.append("--- TEXT ---")
    out.append("<paste the text here>")
    out.append("```")
    out.append("")
    out.append("That last instruction keeps a reader catching words the list does not carry yet. A new "
               "slot-opening word joins the weak-word list, and the skill body's weak-word lint says "
               "which copy of that list takes the edit.")
    return "\n".join(out).rstrip("\n") + "\n"


# --- building, validating, writing -----------------------------------------------------------------

def build(data):
    """Every artifact as {relative path: text}. Raises BuildError before any write."""
    check_shape(data)
    laws = build_laws(data)
    outputs = {LAWS_REL: laws_text(laws), DOC_REL: build_doc(data), COVERAGE_REL: build_coverage(data),
               READER_PROMPT_REL: build_reader_prompt(data)}
    validate(outputs, data)
    return outputs



CYRILLIC = re.compile("[\u0400-\u04FF]")


def shipped_case(rule):
    """The case this rule shows inside a shipped skill: the first one written in the Latin alphabet.

    The audit skill ships to hosts whose reader may speak any language, and the shipped-language gate
    holds a shipped artifact to one alphabet. A rule whose recorded evidence is Russian therefore carries
    an English case beside it, and the whole record stays in the rule home.
    """
    for example in rule.get("examples") or []:
        if not CYRILLIC.search(example["written"] + example["repair"]):
            return example
    return None


def human_prose_definition(data):
    """What the human-prose surface covers, read out of the source the surfaces are defined in."""
    for surface in surface_list(data):
        if surface["name"] == "human-prose":
            return surface["definition"].strip()
    raise BuildError("the source defines no human-prose surface, so the audit skill cannot say what "
                     "the rules it prints bind")


def render_human_prose_rules(data):
    """Every rule binding human-prose, for the audit skill that ships without the rule home."""
    rules = [r for r in data["rules"] if "human-prose" in r["surfaces"]]
    if not rules:
        raise BuildError("no rule binds the human-prose surface, so the audit skill would ship ruleless")
    out = ["## The rules this audit holds human prose to", "",
           # The claim over the printed set states its size and says why a code is missing, so a
           # reader counting the codes meets the answer here rather than a contradiction (r70).
           "Every rule below binds human prose, which is %s" % sentence(human_prose_definition(data)),
           "",
           "This block prints %d of the %d rules the source carries. A code missing from the run below "
           "belongs to a rule binding other surfaces only, or to a retired rule whose code left the "
           "set. A rule binding human prose may also bind chat, a commit message, or a worker brief. "
           "Its recorded case may come from one of those surfaces." % (len(rules), len(data["rules"])),
           "",
           "They are printed here out of `%s`, which is where each one is edited. A change made in this "
           "block is overwritten by the next run of `scripts/gen-language-consumers.py`." % SOURCE_REL,
           "",
           "Each entry names the class of mistake, states the rule, gives the question to ask of a "
           "sentence, and carries one recorded case under it. The case shows written text on the left. "
           "The right side shows its repair, or an instruction where the repair depends on facts the "
           "case does not carry. Every case the class was built from lives in the rule home.", ""]
    for rule in rules:
        # The class name stands on its own line, so a reader meets the mistake before its rule, and
        # so neither line carries the other's words past the sentence cap.
        out.append("- **%s** (`%s`)" % (rule["name"], rule["id"]))
        out.append("  %s" % sentence(rule["rule"]))
        out.append("  *Ask:* %s" % rule["reader_test"])
        example = shipped_case(rule)
        if example:
            # One case, on one line. A case written across several lines would break the list it sits in,
            # so its line breaks close up into spaces.
            out.append("    - %s → %s" % (code(" ".join(example["written"].split())),
                                          code(" ".join(example["repair"].split()))))
    out.append("")
    return out


# --- the totals a page states in its own prose ----------------------------------------------------

RULE_ID = re.compile(r"^r(\d+)$")

# A count under ten reads as a word in the pages these blocks stand in, and as digits above it.
COUNT_WORDS = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def count_word(number):
    return COUNT_WORDS[number] if 0 <= number < len(COUNT_WORDS) else str(number)


def rule_numbers(rules):
    """The number inside each rule's id. A id of another shape refuses the build, since the totals
    below are counted off these numbers and a silent skip would understate them."""
    numbers = []
    for rule in rules:
        match = RULE_ID.match(rule["id"])
        if not match:
            raise BuildError("rule id `%s` is not of the form r<number>, so the identifiers cannot be "
                             "counted" % rule["id"])
        numbers.append(int(match.group(1)))
    return numbers


def binding(data, surface):
    """The rules binding one surface."""
    return [r for r in data["rules"] if surface in r["surfaces"]]


def render_rule_totals(data):
    """The readability plan's opening count: the rules in force, and the ones binding the spec body."""
    return ("The rules this project holds its own writing to are %d, of which %d bind the spec body."
            % (len(data["rules"]), len(binding(data, "spec-body"))))


def render_rule_home_totals(data):
    """The record page's opening count: how many rules the home carries, the highest identifier it has
    reached, and how many identifiers below that one no rule holds."""
    rules = data["rules"]
    numbers = rule_numbers(rules)
    highest = max(numbers)
    retired = len(set(range(1, highest + 1)) - set(numbers))
    return ("The rule home carries %d rules and its highest identifier is `r%02d`, so %s stand retired."
            % (len(rules), highest, count_word(retired)))


def render_human_prose_total(data):
    """The worked example's count of the roster it walks a text through."""
    return "The human-prose roster binds %d rules." % len(binding(data, "human-prose"))


def build_blocks(data):
    """The spliced blocks as {relative path: block body}, markers excluded. One block per page, which
    is the shape `guardrails/check-language-rules.py` reads to catch a hand edit inside a block."""
    return {
        RECORD_REL: "\n".join(render_vocabulary(data)).rstrip("\n"),
        AUDIT_SKILL_REL: "\n".join(render_human_prose_rules(data)).rstrip("\n"),
        PLAN_REL: render_rule_totals(data),
        WORKED_EXAMPLE_REL: render_human_prose_total(data),
    }


def build_second_blocks(data):
    """The second block a page lends, as {relative path: block body}."""
    return {RECORD_REL: render_rule_home_totals(data)}


def splice(text, block, name):
    """`text` with the marked block replaced by `block`. Raises BuildError when the markers are gone."""
    opener, closer = block_open(name), block_close(name)
    start = text.find(opener)
    end = text.find(closer)
    if start < 0 or end < 0 or end < start:
        raise BuildError("the page carries no `%s` … `%s` pair, so that generated block has nowhere "
                         "to land" % (opener, closer))
    return "%s%s\n\n%s\n\n%s" % (text[:start], opener, block, text[end:])


def validate(outputs, data):
    """Every output is checked in memory, so a failure leaves the committed files untouched."""
    for rel, text in outputs.items():
        if not text.strip():
            raise BuildError("the build of %s came out empty" % rel)
    if GENERATED_LINE not in outputs[LAWS_REL].splitlines()[1]:
        raise BuildError("%s does not open by naming itself generated" % LAWS_REL)
    for rel in (DOC_REL, COVERAGE_REL):
        if GENERATED_LINE not in outputs[rel].splitlines()[0]:
            raise BuildError("%s does not open by naming itself generated" % rel)
    if READER_PROMPT_GENERATED_LINE not in outputs[READER_PROMPT_REL].splitlines()[0]:
        raise BuildError("%s does not open by naming itself generated" % READER_PROMPT_REL)

    try:
        reparsed = json.loads(outputs[LAWS_REL])
    except ValueError as e:
        raise BuildError("%s does not parse as JSON: %s" % (LAWS_REL, e))
    bodies = reparsed["bodies"]
    for rule in data["rules"]:
        if not model_holds(rule):
            continue
        for checker in model_checkers(rule):
            for surface in rule["surfaces"]:
                body = bodies.get(checker, {}).get(surface, {}).get("text", "")
                if rule["catchers"]["model"]["law_text"].strip().rstrip(".") not in body:
                    raise BuildError("the %s body on the %s surface misses rule %s, which names that "
                                     "checker as its model catcher" % (checker, surface, rule["id"]))
    for checker, by_surface in bodies.items():
        for surface, body in by_surface.items():
            numbers = [law["number"] for law in body["laws"]]
            if numbers != list(range(1, len(numbers) + 1)):
                raise BuildError("the %s body on the %s surface is numbered %s, which does not run "
                                 "from 1" % (checker, surface, numbers))
    for rel in (DOC_REL, COVERAGE_REL):
        for rule in data["rules"]:
            if "### %s — " % rule["id"] not in outputs[rel]:
                raise BuildError("%s carries no entry for rule %s" % (rel, rule["id"]))
    for rule in reader_prompt_rules(data):
        if "- %s — " % rule["name"] not in outputs[READER_PROMPT_REL]:
            raise BuildError("%s carries no stop bullet for rule %s" % (READER_PROMPT_REL, rule["id"]))


def page_blocks(data):
    """Every spliced page as {relative path: [(block name, block body), ...]}, in splice order."""
    pages = {}
    for rel, block in build_blocks(data).items():
        pages.setdefault(rel, []).append((SPLICED[rel], block))
    for rel, block in build_second_blocks(data).items():
        pages.setdefault(rel, []).append((SECOND_SPLICED[rel], block))
    return pages


def prepare_spliced(data, out_dir):
    """The spliced pages as whole texts, built in memory before anything is written.

    A page lending more than one block takes them in turn over the same text, so one page is written
    once with every block it lends already in place. A spliced target absent under `out_dir` is
    skipped, which is what lets the suite build into a scratch directory carrying no hand-written
    pages. A target that is present and has lost its markers raises, so nothing is written at all.
    """
    prepared = {}
    for rel, blocks in page_blocks(data).items():
        path = os.path.join(out_dir, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for name, block in blocks:
            text = splice(text, block, name)
        prepared[rel] = text
    return prepared


def write(outputs, out_dir):
    written = []
    for rel, text in outputs.items():
        path = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        written.append(path)
    return written


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description="Build the language rules' consumers.")
    parser.add_argument("--source", default=os.path.join(REPO_ROOT, SOURCE_REL))
    parser.add_argument("--out-dir", default=REPO_ROOT)
    args = parser.parse_args(argv[1:])
    try:
        data = load_source(args.source)
        outputs = build(data)
        outputs.update(prepare_spliced(data, args.out_dir))
    except BuildError as e:
        print("%s: nothing written — %s" % (CHECK, e))
        return 1
    for path in write(outputs, args.out_dir):
        print("%s: wrote %s" % (CHECK, path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
