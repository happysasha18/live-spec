#!/usr/bin/env python3
"""spec-style-lint.py — the mechanical arm of the SPEC prose register (docs/spec-style.md).

Why this exists: re-styling the spec by hand drifted five times — a picked voice read fine on a
short sample, then degraded across long, constraint-heavy prose, and the tells only surfaced when a
human read it late. The tells are mechanical: a rule that OPENS with a negation instead of what
happens, machine jargon in user-facing prose, ALL-CAPS shouting where the plain statement carries
the force, and the banned contrast frame that names a thing by denying its neighbour. This scans the
register and flags each tell with its line, so the author (or a fresh session rewriting from scratch)
drives a section to clean against a machine, sparing a reader the patience. The register lives in docs/spec-style.md; this only holds
the floor it can check. Positive elegance (flow, sharpness) the linter cannot judge — that is what
the gold exemplars in docs/spec-style.md are for. Floor + exemplars = the whole quality system.

Checks (each maps to a rule in docs/spec-style.md):
  ERROR   negation-opener  a block leads with what it is NOT before what it IS (R4/plainness).
  ERROR   scissors         the contrast frame that names a thing by denying its neighbour, in a dash
                           or comma appositive, the parallel Russian negation-then-replacement forms,
                           or the English prose conjunctions "X rather than Y" / "X instead of Y" used
                           DEFINITIONALLY (a copula/naming lead, a determiner-both-sides rename, or a
                           parallel by/as/for) — an imperative directive ("use A instead of B") passes;
                           see the _rather_instead_scissors docstring for the residual uncaught class
                           (a GLOBAL, PERMANENT ban).
  ERROR   provenance-narrative  a birth-story ("(Born of …)", "(Set by …)", "; born of …", a "Born of …"
                           sentence) in a normative body; provenance stays out of the body, in a docs home
                           keyed by the rule's code (docs/spec-style.md R15, docs/lenses.md). The ordinary
                           verb ("a row born of a split") is left alone.
  ERROR   machine-jargon   a dev/corporate word that has no place in this user-facing spec (R7).
  WARN    caps-shout       an ALL-CAPS ordinary word; force comes from the statement, not caps (R12).
  WARN    second-person    "you"/"your" — the register speaks of named actors, not the reader (R3).

In --gate mode (the DONE-GATE, docs/prose-quality-gate-design.md) the two soft signals are PROMOTED to
blocking errors, two more mechanical rules join them (reassurance, future-narration), the normative-only
rules skip marked informative regions (a user-story line, a blockquote, a NOTE), and a machine-readable
waiver file (scripts/spec-waivers.json) moves a still-unfixed finding into a dated, counted debt bucket
instead of a silent pass. Default mode is unchanged (caps-shout and second-person stay advisory), so the
section-by-section workflow and its tests keep their contract.

Two tiers (INV-166, docs/spec-style.md "Two tiers"): the checks split by whom they bind. The UNIVERSAL
tier (negation-opener, scissors, machine-jargon) is the plainness every live-spec document holds whatever
its register, so it binds every host's gate. The PACK-REGISTER tier (caps-shout, second-person,
reassurance, future-narration) is the pack's own reference-documentation taste, a host adopts on its own
word. `--tier universal` runs the universal tier as the gate and leaves the register tier advisory
(warnings, visible, non-blocking); `--tier full` runs the union as the gate — the pack's own docs, and
identical to `--gate`, which stays as its alias. The default (no flag) is unchanged: universal errors,
caps-shout/second-person warnings, reassurance/future-narration not checked.

Usage: spec-style-lint.py [--gate | --tier universal|full] FILE   (or: cat text | spec-style-lint.py ... -)
Exit 0 = no ERROR (WARN may still print) · exit 1 = at least one ERROR.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
GUARDRAILS = os.path.join(REPO_ROOT, "guardrails")
sys.path.insert(0, SCRIPT_DIR)
import gate_common  # noqa: E402  (sibling module in scripts/)

# specformat.py (the core+parts reader) lives in the pack's guardrails/ dir, a sibling of scripts/.
# This script is ALSO vendored standalone into host repos by adopt/install-style-gates.sh (VENDOR_FILES),
# which does not vendor guardrails/specformat.py — a host runs the style gate on its own doc, with no
# core+parts convention assumed. So the import is optional: where specformat IS available (this
# pack's own checkout), a core file's `## Parts map` is expanded before scanning; where it is not (a
# vendored host), main() falls back to reading exactly the named file, unchanged from this script's
# behaviour before the core+parts fix.
sys.path.insert(0, GUARDRAILS)
try:
    import specformat as sf  # noqa: E402
except ImportError:
    sf = None

# --- the word sets this lint reads, each from its ONE home ---------------------------------------
# No word set is written in this file. Each lives in a JSON file that docs/language-rules.md also
# reads at build time, so the rule a writer reads and the words this script matches are the same
# list and cannot drift apart. A missing or unreadable home raises here rather than quietly
# shrinking the lint to nothing: a checker that passes because its list vanished is worse than a
# checker that refuses to start.
COINAGES_PATH = os.path.join(REPO_ROOT, "guardrails", "spec-coinages.json")
LISTS_PATH = os.path.join(SCRIPT_DIR, "spec-style-lint.json")


def _config(path, key, shown):
    """One list or map out of its home file, or a hard failure naming the home."""
    try:
        with open(path, encoding="utf-8") as f:
            value = json.load(f)[key]
    except (OSError, ValueError, KeyError) as e:
        raise SystemExit("spec-style-lint: cannot read `%s` from %s (%s) — that file is the one home "
                         "of this list and the lint will not run without it." % (key, shown, e))
    if not value:
        raise SystemExit("spec-style-lint: `%s` in %s is empty — a lint over an empty list passes on "
                         "everything." % (key, shown))
    return value


# --- negation-opener -------------------------------------------------------------------------
# A block (a paragraph line, a bullet, or a bold-titled rule) should open with what happens, not
# with what the thing is NOT. The ugly pattern is DEFINE-BY-EXCLUSION: the opening states what the
# subject is not, via a copula or a becoming verb ("X is not Y", "X does not become Y", "Not a Z"),
# instead of what it is. An ACTION prohibition ("does not ask", "never re-carves", "no design
# decision inside") is correct register (R4 blesses "does not"/"never" for prohibitions) and is NOT
# flagged. We examine only the block's opening clause, after stripping markdown markers and a
# leading **bold title** (the title names the rule; the body that follows carries the statement).
LEAD_MARKERS = re.compile(r"^\s*(?:(?:[-*+>]\s+)|(?:#{1,6}\s+))+")   # real bullet/quote/heading (marker + space), never a **bold** run
BOLD_TITLE = re.compile(r"^\s*\*\*[^*]+\*\*\.?\s*")          # a leading **bold title** (+ its period)
# Opening-clause window, in words. No incident or source behind the 12 — an engineering default, not
# a policy decision (the 2026-08-07 census, row 40, found no trace; the introducing commit d58960b is
# silent on it). It bounds how much of a block counts as its "opening"; the rule it serves is stated
# in prose above, and the magnitude is this reading of "opening", not a bar anything is measured to.
NEG_OPENER_WORDS = 12
COPULA = {"is", "are", "was", "were", "be", "been", "being"}
COPULA_NT = {"isn't", "aren't", "wasn't", "weren't"}         # contracted copula-negation
BECOMING = {"become", "becomes", "make", "makes", "mean", "means", "form", "forms",
            "constitute", "constitutes", "turn", "turns", "represent", "represents"}
# a subordinator fronts a CONDITION; a negation inside a condition ("priority when it is not
# normal") is legal, not define-by-exclusion. Only a negation NOT under a preceding subordinator
# counts as an opener tell.
SUBORD = {"when", "if", "where", "until", "once", "while", "unless", "whenever", "wherever",
          "as", "after", "before", "because", "since", "though", "although", "whether"}


def _strip_lead(line):
    """Remove markdown markers and a leading bold title; return the body that states the rule."""
    body = LEAD_MARKERS.sub("", line)
    body = BOLD_TITLE.sub("", body)
    return body.strip()


def _is_negation_opener(body):
    """A block opener defines by exclusion: it states what the subject is NOT (via a copula or a
    becoming verb) before what it is. Prohibitions on an action and negations inside a fronted
    condition are NOT tells."""
    words = [w.lower() for w in re.findall(r"[A-Za-z']+", body)][:NEG_OPENER_WORDS]
    if not words:
        return False
    if words[0] in ("not", "neither"):
        return True
    if words[0] == "no" and len(words) > 1 and words[1] == "longer":
        return True
    seen_subord = False
    for i, w in enumerate(words):
        if w in SUBORD:
            seen_subord = True
        if seen_subord:
            continue
        if w in COPULA_NT:
            return True
        if w in COPULA and i + 1 < len(words) and words[i + 1] == "not":
            return True
        if w in ("do", "does", "did") and i + 2 < len(words) \
                and words[i + 1] == "not" and words[i + 2] in BECOMING:
            return True
    return False


# --- scissors --------------------------------------------------------------------------------
# The contrast frame: defining a thing by denying its neighbour. A GLOBAL, PERMANENT ban.
# Four shapes are caught:
#   em-dash + not/never       the neighbour denied after a dash
#   comma appositive          the neighbour denied after a comma (the additive "… only" is exempt)
#   Russian «… , а не …»       the neighbour denied after a comma with «а не»
#   Russian «не … , а …» / «не столько … , сколько …»   the denial fronted
SCISSORS = re.compile(
    r"[—–]\s*(?:not|never)\b"                        # dash + not/never
    r"|(?<!\w)-{1,2}\s+(?:not|never)\b"              # double-hyphen + not/never
    r"|,\s+not\s+(?!only\b|just\b|merely\b|simply\b)"  # comma appositive, additive forms exempt
    r"|,\s*а\s+не\b"                                 # «… , а не …»
    r"|(?<!\w)не\s+столько\b"                        # «не столько … , сколько …»
    r"|(?<!\w)не\s+[^,]{1,60}?,\s*а\s"               # «не … , а …» (contrast)
    r"(?!не\b|если\b|когда\b|бы\b|то\b|также\b|тоже\b|потом\b|уже\b)",  # skip conditional/additive «а если/бы/…»
    re.IGNORECASE)

# --- scissors, prose conjunctions: "X rather than Y" / "X instead of Y" -----------------------
# The SAME contrast-by-denial as the dash/comma frame above, in its two English prose conjunctions.
# The census (docs/audit/2026-07-22-register-census.md, finding 1) found these two forms carry the
# MAJORITY of the corpus's real contrast-by-denial volume (943 of Tier D's 2,227 raw hits, 83 of
# Tier A's 134) yet escaped the dash/comma regex entirely — a file could carry dozens and pass clean.
#
# Precision over recall (a lint that cries wolf gets ignored, so a residual is left uncaught rather
# than risk a false alarm): a purely INSTRUCTIONAL substitution is lawful and must pass — "use A
# instead of B", "write to A rather than B", "route it to X rather than Y" are directives, not
# definitions. An occurrence is flagged only when BOTH hold:
#   1. a POSITIVE definitional signal ties to it (one of):
#        DEF_LEAD          a copula / linking-or-naming verb leads its clause ("it is a map rather
#                          than a restatement", "it functions as a tool rather than a guardrail");
#        APPOSITIVE_RENAME a determiner sits on BOTH sides — a noun-phrase renamed by denying its
#                          neighbour ("a tool rather than a guardrail", "a ... line instead of a ...
#                          string", "a tool rather than an orchestrator");
#        PARALLEL_PREP     a non-directional function word (by/as/for) repeats across the frame
#                          ("carried by statement rather than by keywords"). Directional to/into/
#                          onto/from are excluded — "write to A rather than to B" is a write-target
#                          directive, left lawful.
#   2. the clause carrying it is NOT imperative-led — a clause opening with a directive verb (use,
#      write, save, send, route, put, keep, prefer, choose, ...) is a command and passes, even when a
#      signal above would otherwise match ("write to the engine rather than the site").
# RESIDUAL, deliberately UNCAUGHT to hold precision near zero false positives (the recall price):
#   - a bare verb / participle-vs-gerund contrast with no copula, no determiner rename, no parallel
#     word ("the suite enforces the tag rather than trusting it", "travels with the text instead of
#     being filled");
#   - a genuine contrast that happens to OPEN with a directive verb ("recommend rather than ask") —
#     indistinguishable by regex from a lawful command, so it passes.
RATHER_INSTEAD = re.compile(r"(?<!\w)(?:rather than|instead of)(?!\w)", re.IGNORECASE)
# copula + linking/naming verbs that mark a definitional clause (contractions included). The
# naming verbs that double as common NOUNS in this register (a "read", "counts", "names", "acts",
# "reads", by "name") are admitted ONLY when anchored by a following "as" ("reads as a decision
# rather than …", "functions as a tool rather than …") — the "as" is what tells the verb sense from
# the noun ("dispatching reads rather than …", "say so by name instead of …" carry the noun and
# must NOT trip). Verbs with no common noun form (becomes/defines/describes/…) need no anchor.
DEF_LEAD = re.compile(
    r"(?<!\w)(?:"
    r"is|are|was|were|be|been|being|isn't|aren't|wasn't|weren't"
    r"|it's|that's|what's|there's|here's"
    r"|becomes?|defines?|defined|describes?|constitutes?|represents?|remains?"
    r"|(?:functions?|serves?|acts?|reads?|counts?|stands?|treats?)\s+as"
    r")(?!\w)",
    re.IGNORECASE)
# a determiner on BOTH sides of the frame: a noun phrase renamed by denying its neighbour. The
# [^,]{0,60} body forbids crossing a comma, keeping the two determiners in one appositive.
#
# On the 60 here and in PARALLEL_PREP and the object window below, unlike DEF_LEAD_WINDOW = 45 further
# down, which IS sized against a measured corpus example: no source, and no measurement can give it
# one. Swept over the whole live spec corpus (32 files: every spec/*.md plus PRODUCT_SPEC.md and
# ARCHITECTURE.md, 2026-08-27), every value from 30 to 150 produces byte-identical lint output — the
# figure is not load-bearing on any real text this project holds. The constraint that actually does
# the work is the comma class `[^,]`, which keeps the match inside one appositive; the digits are a
# belt behind it, bounding catastrophic backtracking rather than deciding a verdict. Kept as-is
# because nothing measurable argues for another value.
APPOSITIVE_RENAME = re.compile(
    r"(?<!\w)(?:a|an|the|its|his|her|their|our|my|your)\s+\S[^,]{0,60}?"
    r"(?:rather than|instead of)\s+(?:a|an|the|its|his|her|their|our|my|your)(?!\w)",
    re.IGNORECASE)
# the same non-directional function word repeated across the frame (by/as/for). Directional
# prepositions (to/into/onto/from) are excluded: they carry the lawful write-target directive.
PARALLEL_PREP = re.compile(
    r"(?<!\w)(by|as|for)\s+\S[^,]{0,60}?(?:rather than|instead of)\s+\1(?!\w)",
    re.IGNORECASE)
# a clause opening with one of these directive verbs is an imperative command -> the frame is a
# lawful substitution instruction and passes, even if a positive signal above matches.
IMPERATIVE_VERBS = frozenset({
    "use", "write", "save", "store", "send", "route", "put", "place", "call", "point", "read",
    "add", "set", "apply", "run", "keep", "prefer", "choose", "pick", "go", "refer", "defer",
    "name", "treat", "show", "give", "make", "do", "see", "append", "log", "record", "return",
    "pass", "leave", "hold", "carry", "report", "open", "close", "mark", "flag", "check", "scan",
    "push", "commit", "render", "derive", "state", "cite", "pin", "list", "drop", "load"})
# the frame's own clause ends at a sentence stop, an em-dash aside, or a coordinating break
# (", and" / ", so" / " and " / …) — so a copula governing a DIFFERENT predicate ("the finding is
# a question, and it recommends rather than blocks") does not read as this frame's definitional
# lead. Only a copula in the same local clause as the frame counts.
_CLAUSE_SPLIT = re.compile(
    r"[.!?;:]\s+|\s+[—–]\s+|\s+--\s+|,\s+(?:and|so|or|but|which|then|each)\s+|\s+(?:and|or|but)\s+")
_FIRST_WORD = re.compile(r"\s*([A-Za-z']+)")
# how close (chars) a copula/naming lead must sit before the frame to count as its definitional
# lead — a copula farther back is in a distant sub-clause and does not tie to this frame. Sized to
# clear the longest genuine lead in the corpus ("it is deterministic bash/YAML checking rather
# than …", ~34 chars) while dropping the em-dash-separated distant copula.
DEF_LEAD_WINDOW = 45


def _rather_instead_scissors(scrub):
    """True when a 'rather than' / 'instead of' occurrence on the line is a DEFINITIONAL contrast
    (a positive signal ties to it and its clause is not imperative-led). High precision: an
    occurrence with no positive signal, or one inside an imperative clause, passes."""
    for m in RATHER_INSTEAD.finditer(scrub):
        pre = scrub[:m.start()]
        clause = _CLAUSE_SPLIT.split(pre)[-1]          # the frame's own clause (after any . ! ? ; :)
        first = _FIRST_WORD.match(clause)
        if first and first.group(1).lower() in IMPERATIVE_VERBS:
            continue                                    # a lawful directive — pass this occurrence
        # DEF_LEAD must GOVERN the frame: close to it (a copula in a distant sub-clause — "he is
        # leaving … makes closing safe rather than closing" — is unrelated), and with no comma
        # between the copula and the frame (a genuine "X is Y rather than Z" runs comma-free from
        # copula to contrast; a cleft "that is what he meant, rather than discovering" puts a comma
        # between, and its copula governs the cleft, not the frame). So look only after the last
        # comma of the clause, within the proximity window. The determiner-rename and parallel
        # signals are already tight (a bounded body, determiners/word repeated across the frame).
        lead = clause.rsplit(",", 1)[-1][-DEF_LEAD_WINDOW:]
        window = clause + scrub[m.start():m.end() + 60]  # clause + the frame + its object
        if DEF_LEAD.search(lead) or APPOSITIVE_RENAME.search(window) or PARALLEL_PREP.search(window):
            return True
    return False


# --- machine jargon (read from its one home, never kept here) ------------------------------------
# The word set lives in guardrails/spec-coinages.json, which guardrails/check-vocabulary.py also
# reads. Until 2026-07-28 this file kept a set of its own, so a word added to either list was
# invisible to the other reader; the merged list is the one home and this arm reads it.
JARGON = set(_config(COINAGES_PATH, "coinages", "guardrails/spec-coinages.json"))
JARGON_RE = re.compile(r"(?<!\w)(%s)(?!\w)" % "|".join(sorted(JARGON)), re.IGNORECASE)

# --- caps-shout ------------------------------------------------------------------------------
# an ALL-CAPS alphabetic word of length >= 2 that is not a known acronym or defined term.
CAPS_ALLOW = {"JSON", "CI", "HTML", "CSS", "RFC", "API", "URL", "UI", "MVP", "TTL", "MECE",
              "LLD", "HLD", "PRD", "README", "LICENSE", "OK", "MD", "CLI", "ID", "IDE", "NLP", "SPEC",
              "LIVE", "STATE", "NEXT", "NOW", "MUST", "SHALL", "NOTE", "QA", "TODO", "HEAD",
              "KPI", "UX", "FIXME", "VCS", "DOM", "PID", "OS", "CDN", "CDP", "ASCII",
              "TBD", "ER", "CRUD", "ISO", "INCOSE",
              # doc / file names used as bare tokens
              "ARCHITECTURE", "ROADMAP", "JOURNAL", "VERSION", "LIVE-STATE", "MIGRATION", "CHANGELOG",
              # the audit record's milestone-read disposition values (INV-156), a closed vocabulary
              # pinned in the matrix (M-303) and the real docs/audit/ records — literal terms, not shout
              "MET", "OWED", "FLAG",
              # defined problem-ledger status values (E-24) and the prototype label
              "WATCHED", "OWNED", "AGREED", "NON-PROBLEM", "SOLVED", "ARCHIVED", "PROTOTYPE", "DECIDE",
              # defined prover/verify mode names — literal terms, not shout
              "CROSS-LINK", "FEATURE-FIT", "FULL", "RE-ENTRY",
              # defined bold law-part labels of the narration law (INV-35)
              "IDENTITY", "DIGEST", "HEARTBEAT",
              # the design-review loop's three named rest-states (INV-154), a closed vocabulary
              "CONVERGES", "WAITS", "STANDS", "DOWN",
              # the push-gate reach map's three named check-set categories (INV-45), a closed vocabulary
              "EXPLICIT", "CONSERVATIVE", "SELF-TESTED",
              # semantic-version tier names (the version-history rows in ARCHITECTURE.md), conventional caps
              "MAJOR", "MINOR", "PATCH", "GB",
              # prior-art framework proper names cited in the reading-order note (INV-75)
              "BMAD"}
FILENAME_RE = re.compile(r"\b[\w./-]+\.(?:md|py|sh|json|txt|html|js|css|yml|yaml|toml)\b")
# capture an ALL-CAPS token, including a hyphenated compound (CROSS-LINK) as one token, so a
# defined mode name is judged whole against the allowlist rather than split into "LINK".
CAPS_RE = re.compile(r"(?<![\w`\[])([A-Z]{2,}(?:-[A-Z]{2,})*)(?![\w`\]-])")

# --- second person ---------------------------------------------------------------------------
# The register speaks of named actors, not the reader (R3). A quoted product-copy literal is the
# exception: a double-quoted span is the PRODUCT's own voice (a line the product shows the human,
# e.g. the read contract "needs your word: what, by when"), not the spec's register, so a second
# person inside quotes is data the spec cites, not a leak. Only the second-person rule takes this
# exemption; caps/scissors/jargon stay global.
SECOND_PERSON = re.compile(r"(?<!\w)(you|your|you're|yours|yourself)(?!\w)", re.IGNORECASE)
QUOTED_SPAN = re.compile(r"\"[^\"]*\"")


def _second_person_outside_quotes(scrub):
    """True when a second-person word appears outside every double-quoted span (a real register
    leak); a match that lies wholly inside quotes is a cited product literal and does not count."""
    spans = [m.span() for m in QUOTED_SPAN.finditer(scrub)]
    for m in SECOND_PERSON.finditer(scrub):
        s, e = m.span()
        if not any(qs <= s and e <= qe for qs, qe in spans):
            return True
    return False

# --- reassurance / invitation (gate mode only, R4/R7) ----------------------------------------
# Reassuring or inviting the reader has no place in a normative sentence. Curated phrases, kept
# conservative so a legitimate word ("just one row" as a quantity) is not caught; "simply" and the
# listed phrases are the unambiguous tells (the recurring intro-block leak said "you can ignore").
REASSURANCE = ("don't worry", "no need to", "feel free", "of course", "rest assured",
               "you can ignore", "you don't have to", "as we saw", "as noted above",
               "needless to say", "simply put")
REASSURANCE_RE = re.compile(r"(?<!\w)simply(?!\w)", re.IGNORECASE)  # bare 'simply' is a tell on its own

# --- future narration (gate mode only, R4) ---------------------------------------------------
# A reference spec states what is true in the present. "the card will show", "the row that shall
# carry" is future narration; rephrase to present. Scoped to will/shall + a spec verb to avoid
# catching every "will".
FUTURE_NARRATION = re.compile(
    r"(?<!\w)(?:will|shall)\s+(?:%s)\b"
    % "|".join(_config(LISTS_PATH, "future_narration_verbs", "scripts/spec-style-lint.json")),
    re.IGNORECASE)

# --- provenance-narrative (global, R15) ------------------------------------------------------
# A normative body states the mechanism in plain present tense; the provenance — the date and the
# case that motivated the rule — lives in a docs home keyed by the rule's code (docs/lenses.md), never
# as an inline birth-story. The tell has three shapes, told apart from the ordinary verb by SHAPE, not
# by the word alone: a parenthetical aside "(Born of …)", a Formal-index trailing cell "…; born of …",
# and a sentence that OPENS with "Born of …" or says "… was born of …". The two ordinary-verb uses —
# "every row born of a split cites …", "a clause born of an approved look points at its norm" — are
# lowercase, mid-clause, and carry no story; none of the arms below match them. The one-token dated
# pointers the rule permits (INV-43's `norm: <path>`, INV-119's `commit <hash>`) carry no "born of".
PROV_PAREN = re.compile(r"\([^)]*\bborn of\b", re.IGNORECASE)   # parenthetical aside "(Born of …)"
PROV_CELL = re.compile(r";\s+born of\b", re.IGNORECASE)         # Formal-index trailing cell "…; born of …"
# a dated birth-story parenthetical opening with a provenance verb/phrase and carrying an ISO date:
# "(Set by …)", "(Set on …)", "(Born in the field: …)", "(Sharpened … :)", "(Raised by …)",
# "(recorded live … :)", "(recorded 2026-… :)", "(The trigger broadened … :)", "(the worked miss: …)".
# It is told from an ordinary dated note (which opens with a bare date, "Audit", "rows", "The owner's
# word", or a dateless "(recorded profile line …)") by its provenance OPENER, and the required ISO date
# keeps a dateless parenthetical from tripping. The `recorded` arm uses a lookahead so the date it needs
# is not consumed by the opener.
PROV_STORY_OPEN = re.compile(
    r"\(\s*(?:Set (?:by|on)|Born (?:of|in)|Sharpened|Raised by|Softened"
    r"|[Rr]ecorded (?=live |\d{4})|The trigger broadened|the worked miss)"
    r"[^)]*\d{4}-\d{2}-\d{2}")
# a clause OPENING with capital-B "Born of" (sentence/bullet start) or the "was born of" form; the
# capital B (no re.IGNORECASE) is what tells the story-opener from the lowercase ordinary verb.
PROV_SENTENCE = re.compile(r"(?<![A-Za-z])Born of\b")
PROV_WASBORN = re.compile(r"\bwas born of\b", re.IGNORECASE)


def _is_provenance_narrative(scrub):
    """A birth-story in a normative body: a parenthetical/cell aside or a story-opening sentence.
    Told from the ordinary verb by shape (parenthesis, leading `;`, or a capital-B/was-born opener)."""
    return bool(PROV_PAREN.search(scrub) or PROV_CELL.search(scrub)
                or PROV_SENTENCE.search(scrub) or PROV_WASBORN.search(scrub)
                or PROV_STORY_OPEN.search(scrub))


# --- TIERS (INV-166) --------------------------------------------------------------------------
# The checks split into two named tiers by whom they bind — a host adopts the floor without the
# pack's own taste. Named here as the code copy of the split; docs/spec-style.md "Two tiers"
# carries the prose.
#   UNIVERSAL       negation-opener, scissors, machine-jargon — the plainness every live-spec
#                   document holds whatever its register; binds every host's gate.
#   PACK-REGISTER   caps-shout, second-person, reassurance, future-narration — the pack's own
#                   reference-documentation taste, a host adopts on its own word.
# (provenance-narrative stays outside the split — a birth-story in a normative body has no
# register reading at all, so it runs as an error in every tier, unconditionally, as before.)
UNIVERSAL_RULES = frozenset({"negation-opener", "scissors", "machine-jargon"})
PACK_REGISTER_RULES = frozenset({"caps-shout", "second-person", "reassurance", "future-narration"})
TIERS = ("default", "universal", "full")


def lint(text, gate=False, tier=None):
    """Return (errors, warnings); each a list of (line_no, code, snippet).

    tier resolves the mode; when omitted it derives from gate (back-compat): tier="full" if
    gate else "default". Explicit values:
      "default"    negation-opener/scissors/machine-jargon are errors; caps-shout/second-person
                   are warnings; reassurance/future-narration are not checked. (today's default,
                   unchanged.)
      "universal"  the UNIVERSAL tier is the gate (errors); the PACK-REGISTER tier — all four
                   rules, including reassurance/future-narration — runs as advisory warnings;
                   informative-region skipping behaves as in "full".
      "full"       the union as errors (identical to --gate): caps-shout, second-person,
                   reassurance, and future-narration are all promoted to errors alongside the
                   UNIVERSAL tier.
    In both "universal" and "full" the normative-only rules (negation-opener, second-person,
    reassurance, future-narration) skip marked informative regions (user-story line, blockquote,
    NOTE) — global rules (scissors, machine-jargon, caps-shout, provenance-narrative) always run."""
    if tier is None:
        tier = "full" if gate else "default"
    if tier not in TIERS:
        raise ValueError("unknown tier: %r (expected one of %s)" % (tier, ", ".join(TIERS)))
    gate_like = tier in ("universal", "full")     # exempt-region skipping + reassurance/future-narration run
    register_errors = tier == "full"              # pack-register rules land as errors only at "full"

    errors, warnings = [], []
    lines = text.splitlines()
    # A fenced block is data: a command to run, a prompt to paste, a sample of output. Its words are
    # quoted rather than written, so no register rule reads them.
    in_fence = False
    exempt = gate_common.exempt_flags(lines) if gate_like else [False] * len(lines)
    # The person rule binds the numbered criteria of the requirements genre. Explanatory prose — a
    # skill body, a README, a reader page, and the Context paragraphs inside a spec — takes the
    # opposite rule, where the register addresses the reader directly (the rule home, r24 beside r25).
    spec_body = gate_common.spec_body_flags(lines)
    prev_blank = True
    for idx, raw in enumerate(lines):
        i = idx + 1
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            prev_blank = False
            continue
        if in_fence:
            prev_blank = False
            continue
        if not stripped:
            prev_blank = True
            continue
        # strip a leading bullet/quote marker (so "- Never …" is not read as a dash-cut), then
        # inline code spans and bracketed anchors, so `docs/decisions/` and [INV-4] never trip
        # caps / jargon / scissors. A **bold title** is kept — jargon/caps inside it still count.
        scrub = gate_common.scrub(stripped)
        exempt_here = exempt[idx]
        # bucket a pack-register rule by tier: at "full" the promoted rules are errors, else warnings.
        norm_bucket = errors if register_errors else warnings

        is_block_lead = prev_blank or bool(LEAD_MARKERS.match(line))
        if is_block_lead and _is_negation_opener(_strip_lead(line)) and not exempt_here:
            errors.append((i, "negation-opener", stripped[:110]))
        if SCISSORS.search(scrub) or _rather_instead_scissors(scrub):  # global
            errors.append((i, "scissors", stripped[:110]))
        if _is_provenance_narrative(scrub):                          # global
            errors.append((i, "provenance-narrative", stripped[:110]))
        for m in JARGON_RE.finditer(scrub):                          # global
            errors.append((i, "machine-jargon:%s" % m.group(1).lower(), stripped[:110]))
        for m in CAPS_RE.finditer(scrub):                            # global
            if m.group(1) not in CAPS_ALLOW:
                (errors if register_errors else warnings).append(
                    (i, "caps-shout:%s" % m.group(1), stripped[:110]))
        if spec_body[idx] and _second_person_outside_quotes(scrub) and not exempt_here:  # spec-body
            norm_bucket.append((i, "second-person", stripped[:110]))
        if gate_like and not exempt_here:
            low = scrub.lower()
            hit = next((p for p in REASSURANCE if p in low), None) or \
                (REASSURANCE_RE.search(scrub) and "simply")
            if hit:
                norm_bucket.append((i, "reassurance:%s" % hit, stripped[:110]))
            if FUTURE_NARRATION.search(scrub):
                norm_bucket.append((i, "future-narration", stripped[:110]))
        prev_blank = False
    return errors, warnings


def apply_waivers(findings, filename, waivers, today=None):
    """Split findings into (active_errors, waived). A finding is (line, code, snippet); its rule is
    the code's head before ':'. Records which waiver ids matched, for stale-waiver reporting."""
    active, waived, matched = [], [], set()
    for line, code, snip in findings:
        rule = code.split(":", 1)[0]
        w = gate_common.match_waiver(rule, filename, snip, waivers, today)
        if w:
            waived.append((line, code, snip, w["id"]))
            matched.add(w["id"])
        else:
            active.append((line, code, snip))
    return active, waived, matched


WAIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec-waivers.json")

# The rules this gate emits — used to scope the stale-waiver check to the style gate's own
# waivers, since the waiver file is shared with the redundancy gate (spec-redundancy).
STYLE_RULES = {"negation-opener", "scissors", "provenance-narrative", "machine-jargon",
               "caps-shout", "second-person", "reassurance", "future-narration"}


USAGE = "usage: spec-style-lint.py [--gate | --tier universal|full] FILE|-\n"


def _parse_argv(argv):
    """Return (tier, positional) or raise ValueError with a usage message. --gate is the alias for
    --tier full (back-compat, tests/test_convergence_locks.py calls --gate and must keep working
    unchanged); an explicit --tier wins ties with a redundant --gate on the same command line."""
    tier = None
    positional = []
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--gate":
            tier = tier or "full"
            i += 1
        elif a == "--tier":
            if i + 1 >= len(argv):
                raise ValueError(USAGE)
            tier = argv[i + 1]
            i += 2
        elif a.startswith("--tier="):
            tier = a.split("=", 1)[1]
            i += 1
        elif a.startswith("--"):
            raise ValueError(USAGE)
        else:
            positional.append(a)
            i += 1
    if tier is not None and tier not in ("universal", "full"):
        raise ValueError(
            "spec-style-lint.py: unknown --tier %r (expected 'universal' or 'full')\n" % tier)
    if len(positional) != 1:
        raise ValueError(USAGE)
    return (tier or "default"), positional[0]


def main(argv):
    try:
        tier, src = _parse_argv(argv)
    except ValueError as exc:
        sys.stderr.write(str(exc))
        return 2
    gate_like = tier in ("universal", "full")
    if src == "-":
        text = sys.stdin.read()
    elif sf is not None:
        # Read through the core+parts mechanism (specformat.spec_paths / read_document) rather than
        # opening `src` directly: a core file carrying a `## Parts map` expands to the core followed
        # by its parts and the lint below sees the WHOLE document, not just the core's preamble and
        # glossary. A file with no map (or an ordinary non-core file) is unaffected — expansion is
        # idempotent by `spec_paths`'s own construction, so this reads exactly the same bytes it
        # always did.
        _resolved, text = sf.read_document([src])
    else:
        # Vendored standalone (no guardrails/specformat.py alongside) — read exactly the named file,
        # same as before the core+parts fix.
        text = open(src, encoding="utf-8").read()
    errors, warnings = lint(text, tier=tier)

    waived, stale = [], []
    if gate_like:
        all_waivers = gate_common.load_waivers(WAIVER_PATH)
        errors, waived, matched = apply_waivers(errors, src, all_waivers)
        # The waiver file is shared with other gates (spec-redundancy). Scope the stale check to
        # THIS gate's own rules, so a live redundancy waiver is never reported stale by the style
        # gate (it matches no style finding by design).
        mine = [w for w in all_waivers if w.get("rule") in STYLE_RULES]
        stale = gate_common.stale_waivers(mine, matched)

    if not errors and not warnings and not waived:
        label = {"default": "", "universal": "/universal", "full": "/gate"}[tier]
        print("OK (spec-style%s): no register tells found." % label)
    if errors:
        print("SPEC-STYLE LINT — ERROR (docs/spec-style.md): a rule opens with what it is NOT,")
        print("shouts, uses machine jargon, cuts with «X — not Y», carries a birth-story in the body,")
        print("reassures, or narrates the future.")
        for line_no, code, snip in errors:
            print("  line %d  [%s]  %s" % (line_no, code, snip))
    if warnings:
        print("SPEC-STYLE LINT — warn (soft signals; a fully-converted section clears these too):")
        for line_no, code, snip in warnings:
            print("  line %d  [%s]  %s" % (line_no, code, snip))
    if waived:
        print("SPEC-STYLE LINT — WAIVED (dated debt, scripts/spec-waivers.json; still counted):")
        for line_no, code, snip, wid in waived:
            print("  line %d  [%s]  (%s)  %s" % (line_no, code, wid, snip))
    if stale:
        print("SPEC-STYLE LINT — stale waivers (defect gone; remove these from spec-waivers.json):")
        for w in stale:
            print("  [%s]  %s" % (w.get("id"), w.get("snippet")))
    print('{"severity":"%s","code":"spec-style","errors":%d,"warnings":%d,"waived":%d,"stale":%d}'
          % ("error" if errors else "advisory", len(errors), len(warnings), len(waived), len(stale)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
