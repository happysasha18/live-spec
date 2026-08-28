#!/usr/bin/env python3
"""check-authority-anchor.py — the machine that holds the writing rule on HUMAN AUTHORITY
(SPEC INV-207, ROADMAP row 415).

THE LAW it enforces. Every claim in this pack stands on an artifact a reader can go and check. A
human's word is the one input with no artifact behind it, and therefore the one claim no agent,
prover, or gate questions. So a sentence that records a decision, word, or ruling AS the person's must
name the EXCHANGE it came from — at minimum a date a reader can go to and check. A sentence the pack
reasoned out for itself is written in the pack's own voice; it claims no human authority, is
challengeable by every reader, and is not this gate's business. An autonomy grant authorizes an agent
to DECIDE; it never authorizes recording that decision AS the human's.

WHAT THE GATE CAN AND CANNOT DO — read this before trusting it. The gate is a CHEAP FIRST PASS; the read-back below is the
defence. It catches an attribution that carries NO checkable anchor at all. It CANNOT catch a
fabrication that carries a plausible date: a session that invents a ranking invents the date under it
just as easily, and a date only has to PARSE for the anchor rule to pass it. The real defence against a
dated fabrication is the READ-BACK: `DECISIONS.md` shows the person the decisions the pack believes he
made, on his own clock, and he strikes what he never said — which is exactly how the founding incident
was caught (he read the resume file and recognised nothing). This gate exists to keep an unanchored
attribution from ever reaching that surface unnoticed, and to reach the churny surfaces where an
attribution first gets written. It does not stand in for the read-back.

THE THREE ACTS the gate serves:

  * The DECISION-SET RECORD (the enforced, push-wired HARD block). A file that declares itself a
    decision record with a `DECISION-RECORD` marker line (the touchpoint-kind gate's self-declaration
    shape) holds, by construction, nothing but decisions recorded as the person's. Every live on-record
    entry there must carry its exchange anchor (a real calendar date); a struck entry — a genuine
    ~~strikethrough~~ retraction, or an entry sitting in a `<!-- record:struck -->` region — is skipped,
    since the person has already reached in and struck it. A bullet, a wrapped multi-line entry, or a
    prose paragraph carrying an authority-claim all count as entries here. This surface is free of the
    rule-language noise below, so the anchor rule is unambiguous and false-positive-free — which is why
    it, and it alone, is the standing gate's HARD block.
  * The RISKY-SURFACE FIRST PASS (push-wired, ADVISORY). The founding fabrication was NOT written on a
    decision record — it was written in the resume file and travelled from there into a plan and a chat
    claim. So the standing scan also REACHES the churny surfaces where an attribution first gets
    written (the resume file, the active roadmap). There it cannot be a hard block: those surfaces are
    thick with the pack's own RULE language ("his word settles it", "blocked on his word") and with
    NARRATION of past incidents, both of which name the person's authority without a date and rightly
    need none. A deterministic gate cannot tell live narration from a live fabrication — only meaning
    can — so this pass REPORTS its candidates for the read-back and the human sweep to triage, and does
    NOT fail the push. A tight detector (rule-frame and copula forms exempted, a same-day time counted
    as an anchor) keeps the report from drowning in rule-language. The class itself is held by the
    judge, below.
  * The FIRST-SWEEP act (arg mode) and the JUDGE (--judge). Given files as arguments, the gate reports
    every authority-claim SENTENCE that names no date, for a one-time human sweep of the spec, the base
    rulebook, and the roadmap — WIDE recall, the triage list's job. The `--judge` mode hands the risky
    surfaces to the register judge (hooks/register_judge_core.py), which reads MEANING and separates a
    specific decision recorded as the person's from abstract rule language — the pack's own head-rule
    answer to a class a literal gate cannot hold. The judge is a sweep tool rather than a blocking push gate:
    a push-blocking model call would red on its own breakage and train the guarded to route around it,
    which is why the pack keeps its judges advisory everywhere.

An authority-claim is (patterns in authority-anchor.json, so this code names no person):
  * a possessive authority-noun with a DEFINITE possessor — "his word", "the owner's ruling", "her
    call", a named person's ranking (prepositional forms like "on his OK" / "per his word" are this case);
  * a verb of authority with a DEFINITE personal subject — "he decided", "the owner ordered", a named
    person chose.
The abstract-role possessors ("the human's", "the person's", "the reader's", "a human", "one") are
NOT authority-claims: they are the pack stating a rule in its own voice. The person names are a
per-host roster (data); the definite role forms ("his", "the owner's", "he decided") are
person-agnostic, so the law is stated for ANY person and ANY host.

THE ANCHOR. A claim passes when its sentence carries a REAL calendar date token (YYYY-MM-DD that names
an existing day — 2026-13-45 does not parse and does not satisfy the anchor). A bare time (~15:37)
alone is not enough on a decision record — the exchange's WHEN is a day; on the risky-surface first
pass, where the day is fixed by the file's own dated context, a same-day time counts as a pointer a
reader can follow. The profile's own style is the target shape: "<person> 2026-07-03, standing" /
"<person> 2026-07-14, on the passivity finding: ...". The person names live in the config data, never in
this code, so the detector names no person.

Usage:
  check-authority-anchor.py                 push mode: HARD-block scan of every DECISION-RECORD
                                            surface, plus an ADVISORY report over the risky
                                            attribution surfaces (resume file, roadmap).
  check-authority-anchor.py [--config F] FILE ...
                                            sweep/fixture mode: report each file's unanchored
                                            authority claims (a DECISION-RECORD file uses the strict
                                            per-entry rule; free prose uses the wide sentence rule).
  check-authority-anchor.py --judge FILE ... hand the files to the register judge (the class-holder),
                                            which separates a recorded decision from rule language.
Exit 0 = no unanchored authority-claim on an ENFORCED surface. Exit 1 = at least one.
"""
import argparse
import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys

DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
TIME = re.compile(r"~?\b\d{1,2}:\d{2}\b")
# A REAL strike is a strikethrough retraction the person reached in and made; a bare typed word
# "STRUCK" in a live bullet is not one, and must not silence a live claim (an author could type
# "STRUCK-review pending" to hide a fabrication). Only ~~...~~ counts as a strike here.
STRIKETHROUGH = re.compile(r"~~.+~~")
# The marker declares a file a decision record only as a STANDALONE line (the TOUCHPOINT-KIND shape),
# so a doc that merely MENTIONS `DECISION-RECORD` inline (the spec, the matrix, this gate) is not one.
RECORD_MARKER = re.compile(r"(?m)^\s*DECISION-RECORD\s*$")
ON_REGION = re.compile(r"<!--\s*record:on\s*-->")
NOTE_REGION = re.compile(r"<!--\s*record:note\s*-->")
STRUCK_REGION = re.compile(r"<!--\s*record:struck\s*-->")
BULLET = re.compile(r"^\s*[-*]\s+\S")

TEXT_EXT = (".md", ".txt")
SENT_SPLIT = re.compile(r"(?<=[.;:])\s+")
# The standing HARD scan reaches only DECLARED DECISION-RECORD surfaces, and spares the fixture homes
# (which carry DECISION-RECORD markers to be exercised, one deliberately unanchored) and the
# archive/diaries, exactly as check-shipped-language and check-freeze spare them.
SPARED_DIRS = ("guardrails/authority-anchor-fixtures/", "docs/", "attic/", "inbox/",
               ".live-spec/", "tests/", "evals/", "prototype/")
SPARED_FILES = ("JOURNAL.md", "MIGRATION.md")
# The RISKY attribution surfaces: where a decision-as-his first gets written, before it ever reaches a
# decision record. Scanned in push mode as an ADVISORY report (tight detector), never a hard block —
# they carry live narration a deterministic gate cannot tell from a live fabrication.
# ROADMAP.md stood here until 2026-08-28, when the queue's own file left the tree for attic/, a
# spared directory. PLAN.md took its place as the live list, and it is where a decision-as-his now
# first gets written.
RISKY_SURFACES = ("NEXT_STEPS.md", "PLAN.md")

# The rule-frame exemptions that keep the risky-surface report tight (see the module doc's second act):
# a copula predicate about authority-in-general ("his word IS the highest authority"), and an
# instrument/condition preposition before the possessor ("blocked ON his word", "CLOSED by his word").
COPULA_TAIL = re.compile(
    r"^\S*\s*(?:his|her|their|the\s+owner's|\w+'s)\s+(?:\S+\s+){0,2}\S+\s+"
    r"(?:is|are|was|were|settles?|decides?|stands?|questions?)\b", re.IGNORECASE)
INSTRUMENT_PRE = re.compile(r"\b(?:on|by|upon)\s+$", re.IGNORECASE)


def valid_date_in(text):
    """True when the text carries at least one REAL calendar date (an impossible date does not count)."""
    for y, m, d in DATE.findall(text):
        try:
            datetime.date(int(y), int(m), int(d))
            return True
        except ValueError:
            continue
    return False


def is_spared(rel):
    if any(rel == f or rel.endswith("/" + f) for f in SPARED_FILES):
        return True
    return any(rel.startswith(d) for d in SPARED_DIRS)


def load_config(path):
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def compile_claim(cfg, risky=False):
    """The authority-claim matcher from the declared roster and role forms, kept as data so the gate
    names no person. DEFINITE possessors/subjects only — the abstract-role forms are rule language.

    risky=True builds the TIGHT matcher for the churny attribution surfaces: it drops the config's
    `trigger_nouns` ("word"/"words", overwhelmingly a scheduling trigger or a quote header there) and
    the `recall_verbs` ("asked"/"said", which narrate many past asks), so the advisory report over the
    resume file and roadmap does not drown in rule- and quote-language. The wide matcher (risky=False)
    keeps the full lists for the record scan and the recall sweep."""
    names = cfg.get("person_names") or []
    nouns = cfg.get("authority_nouns") or []
    verbs = cfg.get("authority_verbs") or []
    if risky:
        trigger = set(cfg.get("trigger_nouns") or [])
        recall = set(cfg.get("recall_verbs") or [])
        nouns = [n for n in nouns if n not in trigger]
        verbs = [v for v in verbs if v not in recall]
    if not (nouns or verbs):
        return None
    name_alt = "|".join(re.escape(n) for n in names)
    # \b anchors the possessor so "her" does not match inside "whether"/"other"/"gather".
    poss = r"\b(?:his|her|their|the owner's"
    if name_alt:
        poss += r"|(?:%s)'s" % name_alt
    poss += r")"
    subj = r"\b(?:he|she|they|the owner"
    if name_alt:
        subj += r"|%s" % name_alt
    subj += r")"
    noun_alt = "|".join(re.escape(n) for n in nouns)
    verb_alt = "|".join(re.escape(v) for v in verbs)
    pats = []
    if noun_alt:
        # one or two tokens may sit between the possessor and the noun: "his 2026-07-06 word",
        # "his own considered ranking".
        pats.append(r"%s\s+(?:\S+\s+){0,2}(?:%s)\b" % (poss, noun_alt))
    if verb_alt:
        pats.append(r"\b%s\s+(?:%s)\b" % (subj, verb_alt))
    if name_alt:
        # the prepositional bare-name form the sweep would otherwise miss — "per <name>:"; the
        # possessive "per <name>'s word" is already the possessive case above. The name comes only from
        # the config roster (name_alt), so this code still names no person.
        pats.append(r"\bper\s+(?:%s)\b" % name_alt)
    return re.compile("(?:%s)" % "|".join(pats), re.IGNORECASE)


def is_rule_frame(sentence, mstart):
    """True when the matched authority-claim reads as the pack's own RULE language rather than a
    recorded decision — a copula predicate about authority-in-general, or the possessor sitting behind
    an instrument/condition preposition. Used only by the TIGHT risky-surface pass, to keep its
    advisory report from drowning in rule-language; the wide sweep and the strict record scan do not
    apply it."""
    if COPULA_TAIL.match(sentence[mstart:]):
        return True
    if INSTRUMENT_PRE.search(sentence[:mstart]):
        return True
    return False


def waived(rel, snippet, waivers):
    for w in waivers or []:
        if fnmatch.fnmatch(rel, w.get("file", "")) and w.get("snippet", "") in snippet:
            return True
    return False


def is_record(text):
    return bool(RECORD_MARKER.search(text))


def _record_entries(lines):
    """Yield (line_no, kind, text) logical entries of a DECISION-RECORD surface, region-aware.

    Region rule: everything is ON-RECORD except lines inside a `<!-- record:struck -->` region. The
    on-record region marker turns it back on; the note region stays on-record (a live claim rendered
    under Notes is still a claim, and a struck-word evasion under Notes must not hide it). A bullet
    ABOVE the first marker is on-record too — the initial state is on-record, so nothing hides above the
    markers.

    An entry groups a bullet with its wrapped continuation lines (indented, non-bullet), so a date that
    falls on the continuation line still anchors the entry. A non-bullet prose line that is not a
    continuation is yielded as a 'prose' entry."""
    in_struck = False
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        if STRUCK_REGION.search(raw):
            in_struck = True
            i += 1
            continue
        if ON_REGION.search(raw) or NOTE_REGION.search(raw):
            in_struck = False
            i += 1
            continue
        if in_struck:
            i += 1
            continue
        if BULLET.match(raw):
            start = i
            text = [raw]
            j = i + 1
            # gather continuation lines: indented, non-blank, not a new bullet, not a marker
            while j < n:
                nxt = lines[j]
                if not nxt.strip():
                    break
                if BULLET.match(nxt) or STRUCK_REGION.search(nxt) or ON_REGION.search(nxt) \
                        or NOTE_REGION.search(nxt):
                    break
                if not (nxt[:1] in (" ", "\t")):
                    break
                text.append(nxt)
                j += 1
            yield (start + 1, "bullet", "\n".join(text))
            i = j
            continue
        if raw.strip():
            yield (i + 1, "prose", raw)
        i += 1


def scan_record(path, rel, claim_re, waivers):
    """A declared DECISION-RECORD surface (the HARD block): every live on-record entry must carry a
    real date. A bullet entry (with its wrapped continuation lines) reds if it names no date and is not
    a ~~strikethrough~~ retraction. A prose paragraph reds only if it CARRIES an authority-claim with no
    date, so the surface's own header and rule prose (which name no definite possessor) pass while a
    fabrication smuggled in as a paragraph does not."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except (UnicodeDecodeError, OSError):
        return
    for ln, kind, text in _record_entries(lines):
        if STRIKETHROUGH.search(text):
            continue
        if valid_date_in(text):
            continue
        if kind == "prose" and not claim_re.search(text):
            continue
        snip = text.strip().splitlines()[0][:120]
        if waived(rel, snip, waivers):
            continue
        why = ("on-record decision entry names no date" if kind == "bullet"
               else "on-record paragraph records an authority claim with no date")
        yield (ln, snip, why)


def scan_prose(path, rel, claim_re, waivers, tight=False):
    """Free prose. In the WIDE sweep (tight=False, arg mode) report every authority-claim sentence
    naming no date — the triage list wants recall. In the TIGHT risky-surface pass (tight=True) exempt
    the rule-frame forms and count a same-day time as an anchor, so the advisory report stays readable."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except (UnicodeDecodeError, OSError):
        return
    for i, raw in enumerate(lines, 1):
        for sent in SENT_SPLIT.split(raw):
            if STRIKETHROUGH.search(sent):
                continue
            m = claim_re.search(sent)
            if not m or valid_date_in(sent):
                continue
            if tight and (TIME.search(sent) or is_rule_frame(sent, m.start())):
                continue
            snip = sent.strip()[:120]
            if waived(rel, snip, waivers):
                continue
            yield (i, snip, "authority claim names no date")


def record_surfaces(root):
    for r in _tracked(root):
        if not r.endswith(TEXT_EXT) or is_spared(r):
            continue
        p = os.path.join(root, r)
        try:
            if is_record(open(p, encoding="utf-8").read()):
                yield (p, r)
        except (UnicodeDecodeError, OSError):
            continue


def risky_surfaces(root):
    for r in _tracked(root):
        base = os.path.basename(r)
        if base in RISKY_SURFACES:
            p = os.path.join(root, r)
            if os.path.isfile(p):
                yield (p, r)


def _tracked(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"],
                             capture_output=True, text=True, check=True).stdout
        return out.splitlines()
    except Exception:
        rels = []
        for dp, _, fns in os.walk(root):
            for fn in fns:
                rels.append(os.path.relpath(os.path.join(dp, fn), root))
        return rels


def run_judge(pairs):
    """Hand each file to the register judge (the class-holder). Advisory: prints the judge's findings,
    stands down cleanly on any breakage (no binary, timeout, unreadable answer), never a blocking gate."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks"))
        import register_judge_core as rj
    except Exception as e:
        print("judge stood down: cannot load the register judge (%s)" % e)
        return 0
    law = (
        "LAW 1 — a specific decision recorded AS the person's must name the exchange it came from. "
        "A sentence that records what the human decided, ruled, ranked, or asked for, attributed to "
        "him as his own word, with no date or time a reader could go to and check, breaks this law. "
        "A sentence stating a RULE in the pack's own voice ('the human's word settles it', 'blocked "
        "on his word'), or NARRATING a past incident, or an attribution that DOES name its exchange, "
        "all pass — only a live, specific, unanchored decision-as-his is the offence.")
    any_found = False
    for path, rel in pairs:
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        offences, err = rj.judge(text, law, surface="the pack's decision records and resume file")
        if err:
            print("judge stood down on %s: %s" % (rel, err))
            continue
        for o in offences:
            any_found = True
            print("  %s  [judge] %s" % (rel, o.get("quote", "")[:120]))
    if not any_found:
        print("OK (authority-anchor, judge): no specific unanchored decision-as-his found by the judge.")
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default=None)
    ap.add_argument("--judge", action="store_true",
                    help="hand the files (or the risky surfaces) to the register judge, advisory")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args(argv[1:])
    default_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "authority-anchor.json")
    cfg = load_config(a.config or default_cfg)
    claim_re = compile_claim(cfg)
    waivers = cfg.get("waivers")

    if claim_re is None:
        print("OK (authority-anchor): no authority patterns declared — the gate stands inert.")
        return 0

    if a.judge:
        pairs = ([(f, os.path.relpath(f, a.root)) for f in a.files]
                 if a.files else list(risky_surfaces(a.root)))
        return run_judge(pairs)

    # --- ENFORCED scan: the decision-record surfaces (a hard block) ---
    if a.files:
        enforced = [(f, os.path.relpath(f, a.root)) for f in a.files]
        advisory = []
    else:
        enforced = list(record_surfaces(a.root))
        advisory = list(risky_surfaces(a.root))

    offences = []
    for path, rel in enforced:
        try:
            record = is_record(open(path, encoding="utf-8").read())
        except (UnicodeDecodeError, OSError):
            record = False
        if record:
            gen = scan_record(path, rel, claim_re, waivers)
        else:
            gen = scan_prose(path, rel, claim_re, waivers, tight=False)
        for ln, snip, why in gen:
            offences.append((rel, ln, snip, why))

    # --- ADVISORY first pass: the risky attribution surfaces (reported, never fails the push) ---
    risky_re = compile_claim(cfg, risky=True) or claim_re
    reported = []
    for path, rel in advisory:
        for ln, snip, why in scan_prose(path, rel, risky_re, waivers, tight=True):
            reported.append((rel, ln, snip, why))

    if reported:
        print("NOTE (authority-anchor): the risky-surface first pass flags candidate attributions on")
        print("the churny surfaces where a decision-as-his first gets written. These are NOT push")
        print("failures — a deterministic gate cannot tell live narration from a live fabrication.")
        print("Read each on the read-back surface (DECISIONS.md) and strike or anchor it; the read-back,")
        print("not this gate, is the defence against a dated fabrication (SPEC INV-207):")
        for rel, ln, snip, why in reported:
            print("  %s:%d  [candidate]  %s" % (rel, ln, snip))
        print("  Run `check-authority-anchor.py --judge` to have the register judge separate a recorded")
        print("  decision from rule language on these surfaces.")

    if not offences:
        if not enforced:
            print("OK (authority-anchor): no DECISION-RECORD surface in the tree yet — the standing "
                  "hard gate stands down by name (SPEC INV-207).")
        else:
            print("OK (authority-anchor): every live entry on a decision record names a real date, so no "
                  "attribution stands with NO anchor to check. The gate catches the unanchored case; a")
            print("fabrication carrying a plausible date only PARSES here and is caught by the read-back")
            print("(DECISIONS.md), where the person strikes what he never said (SPEC INV-207).")
        return 0

    print("FAIL (authority-anchor): something here is written down as the product owner's own word, but")
    print("  nothing says when or where they actually said it (SPEC INV-207). That person's word is")
    print("  treated as final by every other check, so one that can't be traced back can never be")
    print("  verified or corrected:")
    for rel, ln, snip, why in offences:
        print("  %s:%d  [%s]  %s" % (rel, ln, why, snip))
    print("  Fix: ask your agent to name the real moment it came from — at minimum a real date")
    print("  (\"<person> 2026-07-03, standing\" / \"...2026-07-14, on X: ...\"). If no such moment")
    print("  exists, it was the agent's own judgment call — rewrite it as that instead, on the")
    print("  read-back surface (DECISIONS.md), and never record a decision as the person's own unless")
    print("  they actually said it.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
