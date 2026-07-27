#!/usr/bin/env python3
"""check-criterion-readability.py — the criterion-readability ratchet (SPEC INV-287, INV-288).

BLOCKING (guardrails/README.md convention 2): a rise exits non-zero and carries the contract's one
typed line beside its human lines.

WHY THIS IS ITS OWN CHECK AND NOT AN ARM OF A SIBLING. The spec-format family already holds three
gates over the same document, and each owns a different fact (the pack's one-home rule):
check-requirement-shape owns whether a criterion is WELL-FORMED (its case, its numbering, its
anchor, its `*shall*`) and states in its own header that how densely a criterion is written is a
reader's judgment it does not make; check-size-ratchet owns the document's VOLUME, one number,
bytes per criterion; check-weak-words and check-vocabulary own single words. How a criterion READS
— its sentence length, its in-place definitions, its dangling close, its anchor noise — is a fourth
fact, so it takes a fourth home rather than a fifth rule inside a gate that owns something else.
It borrows both of its neighbours' mechanisms instead of re-inventing them: the one parser
(specformat.py) every format gate reads the document with, and the recorded-baseline shape of
check-size-ratchet. The register lint `scripts/spec-style-lint.py` is a different reach — it scans
any document line by line for register tells and cannot see a criterion, a requirement code, or an
anchor — so none of these four arms fits there.

REACH (INV-269). This gate opens two files: the document named on the command line, and its config
`guardrails/criterion-readability.json`. Inside the document it reads the ACCEPTANCE CRITERIA of
the body alone — the numbered criterion lines under each requirement's cases, with their trailing
anchors stripped for the prose arms. It also reads the glossary terms, used only to name the
already-defined term an inline gloss repeats. It does NOT read the preamble, the Context blocks,
the User Story lines, the case headings, or any other document.

THE FOUR ARMS, one per defect class the 2026-07-27 body survey measured:

  A. long-criterion — the criterion welds the whole rule into one sentence. A criterion body over
     `max_words` words reds. The stranger's failure is not vocabulary: by the closing clause the
     subject has been out of view too long to hold the duty and its scope together.

  B. inline-gloss — the criterion defines its own term in place, in a dash-pair aside or a
     parenthetical, while the glossary already owns that kind of fact. An aside longer than
     `max_aside_chars` that opens like a definition (an article, a determiner, `being`, `meaning`)
     reds, naming the glossary entry when the glossed term already holds one.

  C. absolute-tail — the criterion closes on an absolute construction: a comma, a noun phrase, and
     a participle, with no finite verb and no stated relation to what precedes it ("…, the rest
     becoming queue rows"). A closing clause of at least `min_tail_words` words that opens on a
     determiner, carries no finite-verb marker, and rests on a participle reds.

  D. anchor-noise — the anchor competes with the prose: more than `max_anchor_codes` codes in one
     trailing anchor, a code anchor sitting inside the sentence instead of at the line's end, or
     more than `max_code_spans` backticked spans running through the reading line.

NOT MECHANICALLY CHECKED, by design (reported, never silently skipped). Arm C sees the participial
absolute; it does not see the BARE appositive that drops the participle too ("…, the far-tier check
the precedent"), because separating that from a finite clause with an ordinary lexical verb needs a
part-of-speech read no regex makes. Arm B sees a definition-SHAPED aside; whether an aside is a
definition or a plain enumeration of members is the cold reader's call. Arm D counts code spans; it
does not judge which of them the sentence could have said in words. Those reads belong to the
cold-reader panel, and this gate holds the mechanical floor under them.

THE RATCHET (INV-288). A corpus this size cannot go green today, and a check that reds everything
is a check that gets skipped. So each arm records a BASELINE — the count of criteria breaking it
the day the baseline was taken. A count above the baseline reds and names the arm. A count at the
baseline passes. A count below it passes and reports the fall; `--rebaseline` writes the lower
counts back to the config. No run raises a baseline: a raise is a hand edit here with its reason
stated, run through the pipeline, exactly as check-size-ratchet's bound is (INV-265).

Usage:
  check-criterion-readability.py <document.md> [--rebaseline] [--all]
  CRITERION_READABILITY_CONFIG overrides the config path (the suite points it at a fixture config).
  --rebaseline lowers a fallen baseline and rewrites the config; it never raises one.
  --all prints every offender instead of the config's `report_limit` per arm.
Exit 0 when no arm stands above its baseline (printing the reach line, INV-269); exit 1 naming each
arm that rose, with the file, requirement code, line, the offending text, and what to write instead.
Stdlib only.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-criterion-readability"
CONFIG_PATH = os.environ.get("CRITERION_READABILITY_CONFIG",
                             os.path.join(SCRIPT_DIR, "criterion-readability.json"))
ARMS = ("long-criterion", "inline-gloss", "absolute-tail", "anchor-noise")

WORD_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z'’./-]*")
CODE_BRACKET_RE = re.compile(r"\[[^\]]*[A-Z]+-[0-9]+[^\]]*\]")
BACKTICK_RE = re.compile(r"`[^`]+`")
PAREN_RE = re.compile(r"\(([^()]*)\)")
PARTICIPLE_RE = re.compile(r"\b[A-Za-z]{3,}(?:ing|ed)\b")
EM_DASH = "—"


def _plain(text):
    """A criterion's prose with markdown emphasis markers dropped, for word and clause reads."""
    return text.replace("*", "").replace("**", "")


def _words(text):
    return WORD_RE.findall(text)


def _first_word(text):
    m = WORD_RE.search(text)
    return m.group(0).lower() if m else ""


def _asides(text):
    """Every aside inside a criterion: each parenthetical, and each em-dash-led span (a dash pair,
    or a dash that opens an aside running to the line's end)."""
    out = []
    for m in PAREN_RE.finditer(text):
        out.append(m.group(1).strip())
    if EM_DASH in text:
        parts = text.split(EM_DASH)
        for chunk in parts[1:]:
            out.append(chunk.strip())
    return [a for a in out if a]


def arm_long_criterion(crit, th):
    """A criterion body over the word cap."""
    body = _plain(crit.body)
    n = len(_words(body))
    if n > th["max_words"]:
        return "%d words in one criterion (cap %d)" % (n, th["max_words"])
    return None


def _is_enumeration(aside, connectors):
    """True when the aside lists members rather than defining a term: `A, B, or C`. An enumeration
    belongs to arm A's sub-list fix, so arm B leaves it to that arm and keeps its own advice — send
    the term to the glossary — true of every case it does report."""
    parts = [p.strip() for p in aside.split(",") if p.strip()]
    if len(parts) < 2:
        return False
    last = _first_word(parts[-1])
    return last in connectors


def arm_inline_gloss(crit, th, glossary_terms):
    """A definition-shaped aside inside the criterion."""
    body = _plain(crit.body)
    hits = []
    connectors = th.get("enumeration_connectors", ["or", "and"])
    for aside in _asides(body):
        if len(aside) <= th["max_aside_chars"]:
            continue
        if _first_word(aside) not in th["gloss_openers"]:
            continue
        if _is_enumeration(aside, connectors):
            continue
        if any(re.search(r"\b%s\b" % re.escape(w), aside.lower())
               for w in th.get("clause_markers", [])):
            continue        # a dash-led continuation of the rule, not an aside that glosses a term
        known = _glossed_term(body, aside, glossary_terms)
        note = (" — the glossary already defines `%s`" % known) if known else ""
        hits.append("%s…%s" % (aside[:60], note))
    if hits:
        return "; ".join(hits[:2])
    return None


def _glossed_term(body, aside, glossary_terms):
    """The glossary term the words just before this aside name, when the glossary holds one."""
    idx = body.find(aside)
    if idx <= 0:
        return None
    window = body[max(0, idx - 70):idx].lower()
    best, best_at = None, -1
    for term in glossary_terms:
        t = term.lower().strip()
        if len(t) < 4:
            continue
        at = window.rfind(t)
        # the term nearest the aside is the one the aside glosses; a longer term wins a tie.
        if at > best_at or (at == best_at and best is not None and len(t) > len(best)):
            if at >= 0:
                best, best_at = term, at
    return best


def _tail(body):
    """The criterion's closing clause: the text after its last comma."""
    stripped = body.rstrip().rstrip(".")
    idx = stripped.rfind(",")
    if idx < 0:
        return ""
    return stripped[idx + 1:].strip()


def arm_absolute_tail(crit, th):
    """A closing clause that is a noun phrase with no finite verb."""
    body = _plain(crit.body)
    tail = _tail(body)
    if not tail:
        return None
    words = [w.lower() for w in _words(tail)]
    if len(words) < th["min_tail_words"]:
        return None
    if words[0] not in th["np_openers"]:
        return None
    if any(w in th["finite_markers"] for w in words):
        return None
    if not PARTICIPLE_RE.search(tail):
        return None
    return "closes on `, %s`" % tail[:70]


def arm_anchor_noise(crit, th):
    """Too many codes in the anchor, a code anchor mid-sentence, or code spans through the prose."""
    reasons = []
    codes = crit.codes
    if len(codes) > th["max_anchor_codes"]:
        reasons.append("%d codes in one anchor (cap %d): %s"
                       % (len(codes), th["max_anchor_codes"], ", ".join(codes)))
    body = crit.body
    mid = CODE_BRACKET_RE.findall(body)
    if mid:
        reasons.append("a code anchor %s sits inside the sentence" % mid[0])
    spans = BACKTICK_RE.findall(body)
    if len(spans) > th["max_code_spans"]:
        reasons.append("%d backticked spans run through the reading line (cap %d)"
                       % (len(spans), th["max_code_spans"]))
    return "; ".join(reasons) if reasons else None


def measure(doc, cfg):
    """Every arm's findings over the document's criteria: arm name → list of (criterion, detail)."""
    arms = cfg["arms"]
    terms = doc.glossary_terms
    found = dict((name, []) for name in ARMS)
    for crit in doc.criteria:
        detail = arm_long_criterion(crit, arms["long-criterion"]["threshold"])
        if detail:
            found["long-criterion"].append((crit, detail))
        detail = arm_inline_gloss(crit, arms["inline-gloss"]["threshold"], terms)
        if detail:
            found["inline-gloss"].append((crit, detail))
        detail = arm_absolute_tail(crit, arms["absolute-tail"]["threshold"])
        if detail:
            found["absolute-tail"].append((crit, detail))
        detail = arm_anchor_noise(crit, arms["anchor-noise"]["threshold"])
        if detail:
            found["anchor-noise"].append((crit, detail))
    return found


def _reach_line(path, scanned, terms):
    return ("reach: files=[%s, %s]; read the %d acceptance criteria of the body (anchors stripped "
            "for the prose arms) and the %d glossary terms; the preamble, Context blocks, and User "
            "Story lines are outside this gate's reach"
            % (os.path.basename(path), os.path.basename(CONFIG_PATH), scanned, terms))


def _report(path, arm, findings, limit, show_all):
    lines = []
    shown = findings if show_all else findings[:limit]
    for crit, detail in shown:
        lines.append("      %s:%d R%d.%d — %s"
                     % (os.path.basename(path), crit.line_no, crit.req_num, crit.number, detail))
    rest = len(findings) - len(shown)
    if rest > 0:
        lines.append("      … and %d more (run with --all to see every one)" % rest)
    return lines


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = set(a for a in argv[1:] if a.startswith("--"))
    unknown = flags - {"--rebaseline", "--all"}
    if len(args) != 1 or unknown:
        print("%s: usage: %s <document.md> [--rebaseline] [--all]"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    path = args[0]
    if not os.path.isfile(path):
        print("%s: cannot read %s — the gate stands on the document file." % (CHECK, path))
        return 1
    if not os.path.isfile(CONFIG_PATH):
        print("%s: no config at %s — the gate cannot read its thresholds or its baselines "
              "(INV-287)." % (CHECK, CONFIG_PATH))
        return 1
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    missing = [name for name in ARMS if name not in cfg.get("arms", {})]
    if missing:
        print("%s: the config declares no threshold for the arm(s) %s — every arm is tunable from "
              "this one file (INV-287)." % (CHECK, ", ".join(missing)))
        return 1

    with open(path, encoding="utf-8") as f:
        doc = sf.parse(f.read())
    try:
        crits = require_nonempty(CHECK, "the document's criteria", doc.criteria)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    found = measure(doc, cfg)
    counts = dict((name, len(found[name])) for name in ARMS)
    limit = int(cfg.get("report_limit", 12))
    show_all = "--all" in flags
    scanned = len(crits)
    reach = _reach_line(path, scanned, len(doc.glossary_terms))

    unseeded = [name for name in ARMS if cfg["arms"][name].get("baseline") is None]
    if unseeded and "--rebaseline" not in flags:
        print("%s: OK (baselines not yet seeded for %s) — measured %s over %d criteria in %s. %s. %s"
              % (CHECK, ", ".join(unseeded),
                 ", ".join("%s=%d" % (n, counts[n]) for n in ARMS), scanned,
                 os.path.basename(path),
                 cfg.get("reason", "seed the baselines with --rebaseline (INV-288)"), reach))
        return 0

    risen = []
    fallen = []
    for name in ARMS:
        base = cfg["arms"][name].get("baseline")
        if base is None:
            continue        # unseeded: --rebaseline seeds it below; the plain run returned already
        if counts[name] > base:
            risen.append(name)
        elif counts[name] < base:
            fallen.append(name)

    if "--rebaseline" in flags:
        if risen:
            print("%s: %s stands above its baseline — the ratchet moves only down, so a rise is "
                  "fixed in the document, never recorded here (INV-288)." % (CHECK, ", ".join(risen)))
            for name in risen:
                print("  - %s: %d criteria, baseline %s"
                      % (name, counts[name], cfg["arms"][name].get("baseline")))
            return 1
        for name in ARMS:
            cfg["arms"][name]["baseline"] = counts[name]
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("%s: baselines rebased to %s in %s. %s"
              % (CHECK, ", ".join("%s=%d" % (n, counts[n]) for n in ARMS),
                 os.path.basename(CONFIG_PATH), reach))
        return 0

    if risen:
        print("%s: %d arm(s) above baseline in %s:" % (CHECK, len(risen), path))
        for name in risen:
            arm = cfg["arms"][name]
            print("  - %s: %d criteria break it, baseline %d — %s"
                  % (name, counts[name], arm["baseline"], arm["reds"]))
            print("    write instead: %s" % arm["fix"])
            for line in _report(path, name, found[name], limit, show_all):
                print(line)
        print("  %s" % reach)
        # The gate contract's typed line: one parseable object beside the human lines, `fix` the
        # same sentence a person reads (guardrails/README.md convention 1).
        print(json.dumps({
            "severity": "error",
            "code": "criterion-readability",
            "message": "%s above their recorded count in %s (%s)"
                       % (", ".join(risen), os.path.basename(path),
                          ", ".join("%s %d/%d" % (n, counts[n], cfg["arms"][n]["baseline"])
                                    for n in risen)),
            "fix": "Rewrite the criteria this run names until each arm is back at its recorded "
                   "count, or state the reason and change the recorded count in %s through the "
                   "pipeline." % os.path.basename(CONFIG_PATH),
        }))
        return 1

    tail = ", ".join("%s=%d/%d" % (n, counts[n], cfg["arms"][n]["baseline"]) for n in ARMS)
    extra = "counts at or under baseline (%s)" % tail
    if fallen:
        extra += "; %s fell — run --rebaseline to record the lower count (INV-288)" % \
                 ", ".join(fallen)
    print(sf.green_reach(CHECK, [os.path.basename(path), os.path.basename(CONFIG_PATH)],
                         sum(counts.values()), scanned, extra))
    print("  %s" % reach)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
