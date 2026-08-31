"""A decision recorded as the person's names the exchange it came from; a claim the pack reasoned out
is written in the pack's own voice (SPEC INV-207, ROADMAP 415).

Every claim in this pack stands on an artifact a reader can go and check. A human's word is the one
input with no artifact behind it — the one claim no agent, prover, or gate questions — so a
challengeable judgment recorded AS the person's is a fabrication moved into the one slot nothing
reaches again. That is the defect born 2026-07-17, when a session recorded its own lane-ranking as the
person's decision and he recognised nothing on read-back.

Two machines hold the rule:
  * the read-back surface `DECISIONS.md` — the decision-set record, the read-back touchpoint the frame
    declares [INV-205], asynchronous and opened on request — shows the person the decisions the pack
    believes he made, so he strikes what he never said (a struck line retracted, kept with its note);
  * the gate `guardrails/check-authority-anchor.py` reads the decision set: in a declared
    `DECISION-RECORD` surface every live on-record entry carries its date, a struck entry skipped, so
    an unanchored one reds. Its standing scan hard-blocks two things — every declared decision record,
    per entry, and every other tracked text surface in the tree for a decision credited to a person the
    roster names with no date. The person-agnostic role forms ("his word", "the owner's ruling") stay
    advisory on the churny surfaces, since they are the pack's own rule language on nearly every page.

The fabricated lane-ranking is the corpus's first fixture.
"""
import json
import os
import subprocess

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "check-authority-anchor.py")
CONFIG = os.path.join(ROOT, "guardrails", "authority-anchor.json")
FIXTURES = os.path.join(ROOT, "guardrails", "authority-anchor-fixtures")


def _gate(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def _fix(name):
    return os.path.join(FIXTURES, name)


def test_readback_declares_its_touchpoint():
    text = read("DECISIONS.md")
    assert "TOUCHPOINT-KIND: decision-readback" in text, "DECISIONS.md does not declare its touchpoint"
    manifest = read("guardrails/touchpoints.json")
    assert "decision-readback" in manifest, "the manifest does not declare the decision-readback point"
    assert '"surface": "DECISIONS.md"' in manifest, "the manifest does not point at DECISIONS.md"


def test_readback_is_a_decision_record():
    assert "DECISION-RECORD" in read("DECISIONS.md"), "DECISIONS.md carries no DECISION-RECORD marker"


def test_template_ships():
    tmpl = os.path.join(ROOT, "templates", "DECISIONS.template.md")
    assert os.path.isfile(tmpl), "templates/DECISIONS.template.md missing"
    text = read("templates/DECISIONS.template.md")
    assert "DECISION-RECORD" in text and "TOUCHPOINT-KIND: decision-readback" in text


# --- the gate: the decision-record surface ---

def test_gate_reds_the_fabricated_ranking():
    """The corpus's first fixture: a lane-ranking recorded as his with no exchange named."""
    r = _gate(_fix("record-unanchored.md"))
    assert r.returncode == 1, r.stdout
    assert "his ranking" in r.stdout.lower() or "ranking" in r.stdout.lower()


def test_gate_passes_a_dated_record():
    assert _gate(_fix("record-anchored.md")).returncode == 0


def test_gate_passes_a_struck_record():
    """A struck line is retracted; the gate skips it, since the person has already struck it."""
    assert _gate(_fix("record-struck.md")).returncode == 0


# --- the boundary: a dated fabrication PASSES (the gate's honest limit) ---

def test_gate_passes_a_dated_fabrication_the_readback_is_the_defence():
    """A fabrication that carries a plausible date PASSES this gate — a date only has to PARSE, and a
    session that invents a ranking invents its date just as easily. This documents the gate's limit: the
    READ-BACK (DECISIONS.md), where the person strikes what he never said, is the defence against a dated
    fabrication, not a text gate. Making this test go green by 'catching' the dated case would be a lie."""
    r = _gate(_fix("prose-dated-fabrication.txt"))
    assert r.returncode == 0, "a dated fabrication must PASS the gate — the read-back is its defence"


def test_gate_rejects_an_impossible_date():
    """An anchor must be a REAL calendar date. 2026-13-45 only matches the shape; it names no day a
    reader can go to, so it does not satisfy the anchor (red-first: passed wrongly before the fix)."""
    assert _gate(_fix("record-impossible-date.md")).returncode == 1


# --- the four record-surface evasions (each passed wrongly before the fix) ---

def test_evasion_typed_struck_word_does_not_silence_a_live_claim():
    """An author typing the word STRUCK ('STRUCK-review pending') into a LIVE on-record bullet must not
    silence it — only a genuine ~~strikethrough~~ retraction is a strike."""
    assert _gate(_fix("record-evasion-typed-struck.md")).returncode == 1


def test_evasion_note_region_bullet_is_still_scanned():
    """A live claim smuggled as a bullet under `<!-- record:note -->` renders as a live claim and reds;
    only a `<!-- record:struck -->` region exempts an entry."""
    assert _gate(_fix("record-evasion-note-region.md")).returncode == 1


def test_evasion_paragraph_in_on_record_region_is_scanned():
    """A fabrication written as a PARAGRAPH (not a bullet) in the on-record region carries an authority
    claim with no date and reds — it cannot hide by not being a bullet."""
    assert _gate(_fix("record-evasion-paragraph.md")).returncode == 1


def test_evasion_bullet_above_first_marker_is_scanned():
    """A bullet ABOVE the first region marker is on-record (the initial state) and reds — nothing hides
    above the markers."""
    assert _gate(_fix("record-evasion-above-marker.md")).returncode == 1


# --- the wrapped-entry false positive (reded wrongly before the fix) ---

def test_wrapped_entry_date_on_continuation_line_passes():
    """A legitimate multi-line entry whose date falls on the CONTINUATION line is one logical entry, so
    its date anchors it and it passes (red-first: it reded wrongly under the per-physical-line scan)."""
    assert _gate(_fix("record-wrapped-date.md")).returncode == 0


# --- the gate: the first-sweep act over free prose ---

def test_gate_reds_unanchored_prose():
    assert _gate(_fix("prose-unanchored.txt")).returncode == 1


def test_gate_passes_dated_prose():
    assert _gate(_fix("prose-anchored.txt")).returncode == 0


def test_gate_passes_rule_language():
    """The pack's own rule language ('the human's word settles it') is an abstract role, not a
    recorded decision — the law's own challengeable side, needing no anchor."""
    assert _gate(_fix("prose-rule-language.txt")).returncode == 0


def test_sweep_catches_widened_attribution_shapes():
    """NIT-7 recall: the sweep reaches 'he asked for X', 'his preference', 'per Alexander:', and
    'he requested X', not only the narrow 'his word / he decided' shapes."""
    r = _gate(_fix("prose-widened-shapes.txt"))
    assert r.returncode == 1, r.stdout
    for shape in ("asked for", "preference", "Per Alexander", "requested"):
        assert shape in r.stdout, "the sweep missed the %r attribution shape" % shape


def test_judge_mode_is_wired_and_advisory():
    """The register judge (the class-holder) is wired as a sweep tool, not a blocking push gate: the
    source loads register_judge_core and exposes --judge, and the judge stands down cleanly (advisory,
    exit 0) when its own machinery is unavailable — a push-blocking model call would train route-around."""
    src = read("guardrails/check-authority-anchor.py")
    assert "register_judge_core" in src and "--judge" in src
    # force the judge to stand down fast (tiny timeout / missing binary) → advisory exit 0
    import subprocess as _sp
    env = dict(os.environ, REGISTER_JUDGE_TIMEOUT="0.01")
    r = _sp.run(["python3", GATE, "--judge", _fix("prose-rule-language.txt")],
                capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr


# --- the real surfaces and the standing scan ---

def test_gate_passes_the_readback_surface():
    """DECISIONS.md, the host's real decision record, is fully anchored."""
    assert _gate(os.path.join(ROOT, "DECISIONS.md")).returncode == 0


def test_gate_standing_scan_hard_blocks_records_and_reaches_risky_surfaces():
    """Push mode HARD-blocks the DECISION-RECORD surfaces (a real block) and REACHES the churny
    attribution surfaces the founding incident used — the resume file and the roadmap — as an advisory
    report. It does not SPARE them: the first build spared exactly the surfaces the fabrication lived on,
    and this replaces that coverage hole. The advisory report never fails the push (those surfaces carry
    live narration a deterministic gate cannot tell from a live fabrication), so with the tree's records
    anchored the standing gate is green."""
    r = _gate()  # no args → push mode
    assert r.returncode == 0, r.stdout
    src = read("guardrails/check-authority-anchor.py")
    # the risky attribution surfaces are REACHED, not spared
    assert "NEXT_STEPS.md" in src and "PLAN.md" in src, "the risky surfaces must be named"
    assert "RISKY_SURFACES" in src, "the gate must declare a risky-surface set it reaches"
    # JOURNAL stays spared (pure history); it is not a live attribution surface
    assert "JOURNAL.md" in src


def test_a_named_attribution_reds_on_any_surface_and_the_tree_as_it_stands_passes(tmp_path):
    """Both directions of q-497's first leg, in one test.

    RED: a sentence crediting a person the roster names with an instruction no date stands behind reds
    in push mode wherever it is written — here on an ordinary spec page, which carries no
    `DECISION-RECORD` marker and is not the read-back page. Before this arm the same plant passed
    silently: the standing hard block reached declared decision records only, so the two surfaces it
    reached in this tree were the read-back page and its template, and a fabrication written anywhere
    else — which is where the founding one was written — never reached a red.

    GREEN: the same sentence naming its exchange passes, and the tree as it stands passes, so the arm
    reds a fabrication rather than the pack's own pages.

    The eight red plants are the shapes an adversarial read of 2026-08-31 planted against the first
    build of this arm, which passed seven of them. Two causes, both closed: the name-and-verb pattern
    demanded the two words sit adjacent, and the arm inherited the copula and instrument exemptions,
    which are keyed on exactly the shapes a fabricated instruction is written in once a name is in it.
    Each plant stays here so neither can come back unnoticed."""
    assert _gate().returncode == 0, "the tree as it stands must pass push mode"

    root = str(tmp_path)
    os.mkdir(os.path.join(root, "spec"))
    plant = os.path.join(root, "spec", "queue-order.md")
    person = json.loads(read("guardrails/authority-anchor.json"))["person_names"][0]

    def write(sentence):
        with open(plant, "w", encoding="utf-8") as f:
            f.write("# Queue order\n\n%s\n" % sentence)
        subprocess.run(["git", "-C", root, "add", "-A"], check=True,
                       capture_output=True)

    subprocess.run(["git", "init", "-q", root], check=True, capture_output=True)

    reds = [
        "%s asked for the release lane to run before the communication lane.",
        "%s's ruling was that the release lane runs first.",
        "Decided on %s's instruction: the communication lane is dropped.",
        "The cap of three was set by %s's ruling.",
        "According to %s, the cap is three.",
        "%s himself asked for the second lane to be cut.",
        "%s has asked for the release lane to run first.",
        "%s later decided the release lane goes first.",
    ]
    for shape in reds:
        sentence = shape % person
        write(sentence)
        r = _gate("--root", root)
        assert r.returncode == 1, (
            "this attribution names no exchange and must red on an ordinary surface: %r\n%s"
            % (sentence, r.stdout))
        assert "spec/queue-order.md" in r.stdout, r.stdout

    write("%s 2026-07-03 asked for the release lane to run before the communication lane." % person)
    r = _gate("--root", root)
    assert r.returncode == 0, "the same attribution naming its exchange must pass\n" + r.stdout


def test_a_date_stamped_at_the_head_of_the_line_anchors_the_claim_on_it(tmp_path):
    """An attribution that carries its date in a leading stamp passes, and one carrying no date at all
    still reds.

    RED BEFORE THE FIX: the arm split each line into sentences on `:` before looking for a date, so a
    leading `2026-08-31:` stamp was severed from the sentence it dated and the claim reddened with its
    date standing two words to the left. `DECISIONS.md` writes its own entries in exactly that form, so
    the first live page to carry a dated named attribution would have blocked the push.

    The date must still be a real calendar date and must still stand on the line, which is what keeps
    this narrower than the advisory pass's bare-time exemption."""
    root = str(tmp_path)
    os.mkdir(os.path.join(root, "spec"))
    plant = os.path.join(root, "spec", "queue-order.md")
    person = json.loads(read("guardrails/authority-anchor.json"))["person_names"][0]

    def write(line):
        with open(plant, "w", encoding="utf-8") as f:
            f.write("# Queue order\n\n%s\n" % line)
        subprocess.run(["git", "-C", root, "add", "-A"], check=True, capture_output=True)

    subprocess.run(["git", "init", "-q", root], check=True, capture_output=True)

    for line in ["2026-07-03: %s asked for the release lane to run first." % person,
                 "**2026-07-03**: %s decided the release lane runs first." % person]:
        write(line)
        r = _gate("--root", root)
        assert r.returncode == 0, (
            "the date stands on this line, so the claim is anchored and must pass: %r\n%s"
            % (line, r.stdout))

    write("%s asked for the release lane to run first." % person)
    r = _gate("--root", root)
    assert r.returncode == 1, (
        "no date stands anywhere on this line, so the claim must still red\n" + r.stdout)


def test_the_two_honest_sentences_this_arm_still_reds_stay_named(tmp_path):
    """The arm reds two shapes a person could write honestly, and both stay red on purpose.

    A year-less date is not a date a reader can resolve on its own, and no deterministic matcher reads
    a denial. Each costs a writer one edit and neither lets a fabrication through, which is why the
    anchor is not widened to take them. This test reds if either quietly starts passing, so the choice
    stays a choice rather than drifting into a silent hole, and the gate's own opening says both."""
    root = str(tmp_path)
    os.mkdir(os.path.join(root, "spec"))
    plant = os.path.join(root, "spec", "queue-order.md")
    person = json.loads(read("guardrails/authority-anchor.json"))["person_names"][0]

    def write(line):
        with open(plant, "w", encoding="utf-8") as f:
            f.write("# Queue order\n\n%s\n" % line)
        subprocess.run(["git", "-C", root, "add", "-A"], check=True, capture_output=True)

    subprocess.run(["git", "init", "-q", root], check=True, capture_output=True)

    for line in ["%s asked for the release lane to run first on 03.07." % person,
                 "This is not %s's word, it is the session's own call." % person]:
        write(line)
        r = _gate("--root", root)
        assert r.returncode == 1, (
            "this shape reds on purpose and its reason is written in the gate's opening: %r\n%s"
            % (line, r.stdout))

    source = read("guardrails/check-authority-anchor.py")
    assert "TWO WAYS THIS ARM REDS AN HONEST SENTENCE" in source, (
        "the gate's opening must keep naming the two honest sentences it reds")


def test_the_reach_the_named_arm_does_not_cover_is_written_down(tmp_path):
    """The other half of an honest verdict: what the arm does NOT hold, held as a test so the
    documentation cannot drift away from it.

    A page in the spared set passes, and a sentence crediting the person with no authority word beside
    the name passes. Both are recorded escapes: the spared set is history, and a bare-name source form
    carries nothing a pattern can key on. The gate's own opening says both, and this test reds if that
    sentence is ever deleted as though the hole had closed."""
    root = str(tmp_path)
    os.mkdir(os.path.join(root, "docs"))
    person = json.loads(read("guardrails/authority-anchor.json"))["person_names"][0]
    with open(os.path.join(root, "docs", "record.md"), "w", encoding="utf-8") as f:
        f.write("# Record\n\n%s asked for the release lane to run first.\n" % person)
    os.mkdir(os.path.join(root, "spec"))
    with open(os.path.join(root, "spec", "order.md"), "w", encoding="utf-8") as f:
        f.write("# Order\n\nThe lane order came from %s.\n" % person)
    subprocess.run(["git", "init", "-q", root], check=True, capture_output=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True, capture_output=True)

    r = _gate("--root", root)
    assert r.returncode == 0, (
        "these two are the arm's recorded escapes and must stay green until the arm really covers "
        "them; a red here means the gate changed and its own opening is now wrong\n" + r.stdout)

    src = read("guardrails/check-authority-anchor.py")
    assert "WHAT THIS ARM DOES NOT REACH" in src, \
        "the gate no longer states its own reach, so a reader takes it for more than it holds"
    assert "came\n    from <person>" in src or "came from <person>" in src, \
        "the bare-name escape is no longer named in the gate's own opening"


def test_push_mode_reports_risky_surface_candidates():
    """Push mode emits the advisory candidate report over the resume file / roadmap, proving it reaches
    the surfaces the incident used rather than sparing them. The report is advisory: exit stays 0."""
    r = _gate()  # push mode
    assert r.returncode == 0, r.stdout
    assert "[candidate]" in r.stdout and "NOTE (authority-anchor)" in r.stdout, r.stdout
    assert "NEXT_STEPS.md" in r.stdout or "PLAN.md" in r.stdout


def test_gate_names_no_person_in_code():
    """The person roster lives in the config DATA; the gate's own code names no person (the
    shipped-language allowlist's rule)."""
    import json
    src = read("guardrails/check-authority-anchor.py")
    roster = json.loads(read("guardrails/authority-anchor.json")).get("person_names", [])
    assert roster, "the config declares no person roster"
    for name in roster:
        assert name not in src, "the gate's code names %r — it must live only in the config data" % name


def test_gate_wired_into_pre_push():
    assert "check-authority-anchor.py" in read("guardrails/pre-push"), \
        "pre-push does not wire the authority-anchor gate"


# --- traceability across the four documents ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-207]" in spec
    assert "authority-anchor gate" in spec
    assert "DECISIONS.md" in spec


def test_formal_index_row():
    assert "| INV-207 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-207" in arch
    assert "check-authority-anchor.py" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "M-388" in matrix
    assert "INV-207" in matrix
