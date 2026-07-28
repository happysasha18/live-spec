"""F-onboarding: the settings card (M-206..M-210, INV-87/INV-88).

The card is rendered by scripts/onboarding-card.py from the base skill's
package-defaults table (rows marked card-visible) plus the profile files.
Function-level rows run the real renderer and inspect the real output.
"""
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest

from conftest import ROOT, read, read_flat
RENDERER = os.path.join(ROOT, "scripts", "onboarding-card.py")
BASE = os.path.join(ROOT, "skills", "live-spec-base", "SKILL.md")
HOST_PROFILE = os.path.join(ROOT, ".live-spec", "profile.md")
NORM = os.path.join(ROOT, "docs", "norms", "onboarding-card-2026-07-10.html")

FIXTURE_PERSONAL = """# Personal profile (test fixture)

- `language.chat: Russian` — pinned (fixture, 2026-07-10)
- `address: Testname` — (fixture, 2026-07-10)
"""

EMPTY_PERSONAL = """# Personal profile (test fixture, no values)
"""

FIXTURE_HOST = """# Host profile (test fixture, value-free)

- `prover.cadence: before every push` — (fixture, 2026-07-10)
- the suite runs whole before any deploy (fixture prose rule, 2026-07-10)
"""

FIXTURE_HOST_MULTILINE = """# Host profile (test fixture, multi-line entries)

- `project.kind: skill pack — the fixture flagship; this repo doubles as the
  fixture host instance` — recorded 2026-07-10 (fixture).

- `fixture.long-rule: standing — accepted work rides the fixture rule on its own
  certification, wrapped across three physical lines to prove the
  join` — recorded 2026-07-10 (fixture).
"""


def visible_keys():
    """Parse the package-defaults table: keys of rows marked card-visible."""
    body = open(BASE, encoding="utf-8").read()
    keys = []
    for line in body.splitlines():
        m = re.match(r"\|\s*`([\w.-]+)`\s*\|.*\|\s*(visible|internal)\s*\|\s*$", line)
        if m and m.group(2) == "visible":
            keys.append(m.group(1))
    return keys


_TEMP_PATHS = []


def _temp(suffix, content=None):
    """A tracked temp file with the suite's own prefix — the hygiene law (SPEC INV-100, M-236)."""
    mode = "w" if content is not None else "w+b"
    kwargs = {"encoding": "utf-8"} if content is not None else {}
    fh = tempfile.NamedTemporaryFile(mode=mode, suffix=suffix, delete=False,
                                     prefix="livespec-test-", **kwargs)
    if content is not None:
        fh.write(content)
    fh.close()
    _TEMP_PATHS.append(fh.name)
    return fh.name


def tearDownModule():
    for p in _TEMP_PATHS:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


def render(personal, host=HOST_PROFILE, base=BASE, expect_ok=True):
    """Run the real renderer into a temp dir; return (exitcode, html_or_stderr)."""
    out_name = _temp(".html")
    proc = subprocess.run(
        [sys.executable, RENDERER, "--base", base, "--personal", personal,
         "--host", host, "--out", out_name],
        capture_output=True, text=True, timeout=30)
    if expect_ok and proc.returncode == 0:
        with open(out_name, encoding="utf-8") as fh:
            return proc.returncode, fh.read()
    return proc.returncode, proc.stderr + proc.stdout


def write_fixture(text):
    return _temp(".md", content=text)


class TestOnboardingCard(unittest.TestCase):

    def test_onboarding_card_completeness(self):
        """M-206 (INV-87): every card-visible table row on the card, every card
        row traced to a source; renders within the 1 s budget."""
        keys = visible_keys()
        self.assertGreaterEqual(len(keys), 5, "the base table lost its card-visible marks")
        code, html = render(write_fixture(FIXTURE_PERSONAL))
        self.assertEqual(code, 0, "renderer failed: %s" % html[:400])
        # the 1 s budget, read from the script's own instrumentation (spawn excluded)
        out_name = _temp(".html")
        proc = subprocess.run(
            [sys.executable, RENDERER, "--base", BASE,
             "--personal", write_fixture(FIXTURE_PERSONAL),
             "--host", HOST_PROFILE, "--out", out_name],
            capture_output=True, text=True, timeout=30)
        ms = re.search(r"render-ms: (\d+)", proc.stdout)
        self.assertIsNotNone(ms, "the renderer must report its own render time")
        self.assertLess(int(ms.group(1)), 1000,
                        "the render blew its 1 s budget (%s ms)" % ms.group(1))
        rendered = set(re.findall(r'data-setting-key="([\w.-]+)"', html))
        for key in keys:
            self.assertIn(key, rendered, "card-visible row missing from the card: %s" % key)
        for key in rendered:
            self.assertIn("data-source=", html, "card rows must carry their source mark")
        internal = {"worker.tiering", "checkpoints.home", "work-kind.host-default"}
        self.assertFalse(internal & rendered,
                         "internal rows leaked onto the card: %s" % (internal & rendered))
        # host profile recorded lines appear in the project-rules part
        self.assertIn("project-rules", html, "the card lost its project-rules part")

    def test_onboarding_card_copy_rules(self):
        """M-207 (INV-88): fixed copy states rules; personal values only in the
        reader's-own slot; a value-free render carries no personal value."""
        code, html = render(write_fixture(FIXTURE_PERSONAL))
        self.assertEqual(code, 0, html[:400])
        self.assertIn("whatever language you write", html,
                      "the language rule frame left the fixed copy")
        self.assertIn("Testname", html, "the reader's own recorded value must show")
        self.assertIn("Russian", html, "the reader's own recorded language must show")
        # the value-free render: BOTH profiles are fixtures, so anything personal
        # left in the output can only come from the fixed copy itself (M-207's cell)
        code2, html2 = render(write_fixture(EMPTY_PERSONAL),
                              host=write_fixture(FIXTURE_HOST))
        self.assertEqual(code2, 0, html2[:400])
        self.assertIn("whatever language you write", html2)
        for personal_value in ("Testname", "Russian", "Alexander"):
            self.assertNotIn(personal_value, html2,
                             "a personal value is baked into fixed copy: %s" % personal_value)

    def test_onboarding_card_missing_profile(self):
        """M-208 (INV-87): a missing personal profile renders package defaults
        with a plain absence notice naming the founding offer."""
        missing = os.path.join(tempfile.gettempdir(), "no-such-profile-xyz.md")
        if os.path.exists(missing):
            os.unlink(missing)
        code, html = render(missing)
        self.assertEqual(code, 0, "a missing profile must render, not crash: %s" % html[:400])
        self.assertIn("No personal profile exists yet", html,
                      "the absence must be said plainly")
        self.assertIn("founding offer", html,
                      "the absence notice names how the founding offer creates one")

    def test_onboarding_card_malformed_row(self):
        """M-209 (INV-87): a malformed table row fails the render loudly."""
        body = open(BASE, encoding="utf-8").read()
        broken = body.replace(
            "| `language.docs` |", "| `language.docs` broken-no-pipes ", 1)
        base_fixture = write_fixture(broken)
        code, out = render(write_fixture(FIXTURE_PERSONAL), base=base_fixture,
                           expect_ok=False)
        self.assertNotEqual(code, 0, "a malformed row must fail the render loudly")
        self.assertIn("language.docs", out,
                      "the failure must name the malformed row")

    def test_onboarding_card_norm_conformance(self):
        """M-211 (INV-88): the card's sections and row names match the frozen
        norm; no invented value formula."""
        norm = open(NORM, encoding="utf-8").read()
        norm_headings = set(re.findall(r"<h2>(.*?)</h2>", norm))
        # the project-rules section's rows are DATA (one host's recorded rules),
        # not template: their names are excluded from the must-match set and the
        # rendered card replaces them with the real host lines
        rules_section = re.search(
            r"<h2>Two rules this project sets for itself</h2>.*?</section>", norm, re.S)
        data_names = set(re.findall(r'<div class="name">(.*?)</div>',
                                    rules_section.group(0))) if rules_section else set()
        norm_rownames = set(re.findall(r'<div class="name">(.*?)</div>', norm)) - data_names
        self.assertGreaterEqual(len(norm_headings), 5, "the norm lost its sections")
        code, html = render(write_fixture(FIXTURE_PERSONAL))
        self.assertEqual(code, 0, html[:400])
        for heading in norm_headings:
            self.assertIn("<h2>%s</h2>" % heading, html,
                          "a norm section is missing from the card: %s" % heading)
        for name in norm_rownames:
            self.assertIn(name, html,
                          "a norm row name is missing from the card: %s" % name)
        self.assertNotIn("yours today", html,
                         "an invented value formula drifted from the norm")
        self.assertNotIn("Trust commit", html,
                         "a raw profile key rendered as a row heading")
        # plain words lead, codes trail: no bare dotted key stands as a row heading
        for name in re.findall(r'<div class="name">([^<]*)</div>', html):
            self.assertIsNone(re.fullmatch(r"[\w-]+(\.[\w-]+)+", name.strip()),
                              "a raw key stands as a row heading: %s" % name)
        # the example rules are replaced by the real host lines, never shown beside them
        code3, html3 = render(write_fixture(EMPTY_PERSONAL),
                              host=write_fixture(FIXTURE_HOST))
        self.assertEqual(code3, 0, html3[:400])
        self.assertIn("before every push", html3,
                      "the host's own recorded rule must reach the project-rules part")
        for example in data_names:
            self.assertNotIn(example, html3,
                             "a norm example rule shows beside real host lines: %s" % example)

    def test_onboarding_card_multiline_host_lines(self):
        """M-212 (INV-87): a multi-line keyed host entry renders whole — the
        value reaches its row, no raw markdown leaks, no truncation."""
        code, html = render(write_fixture(EMPTY_PERSONAL),
                            host=write_fixture(FIXTURE_HOST_MULTILINE))
        self.assertEqual(code, 0, html[:400])
        kind_row = re.search(
            r'data-setting-key="project\.kind".*?(?=data-setting-key="(?!project\.kind)|</section)',
            html, re.S)
        self.assertIsNotNone(kind_row, "the project-kind row left the card")
        self.assertIn("skill pack", kind_row.group(0),
                      "a multi-line recorded value never reached its card row")
        self.assertNotIn("- `", html, "raw markdown leaked into the card")
        self.assertIn("wrapped across three physical lines to prove the join", html,
                      "a multi-line host rule was truncated at its first physical line")

    def test_onboarding_card_robustness(self):
        """M-213 (INV-87): real-shaped and hostile inputs — markup in a value is
        escaped; a missing host profile renders with a plain no-rules line; nested
        sub-bullets and wrapped lines leak no raw markdown; a fresh project on the
        template profile renders with placeholders never shown as recorded values."""
        hostile = write_fixture(
            "# fixture\n\n- `address: <b>Bold&Co</b>` — (fixture, 2026-07-10)\n")
        code, html = render(hostile)
        self.assertEqual(code, 0, html[:400])
        self.assertNotIn("<b>Bold&Co</b>", html,
                         "a recorded value injected raw markup into the card")
        self.assertIn("Bold&amp;Co", html, "the value must still show, escaped")
        missing_host = os.path.join(tempfile.gettempdir(), "no-such-host-xyz.md")
        if os.path.exists(missing_host):
            os.unlink(missing_host)
        code2, html2 = render(write_fixture(FIXTURE_PERSONAL), host=missing_host)
        self.assertEqual(code2, 0, "a missing host profile must render, not crash: %s" % html2[:400])
        self.assertIn("project-rules", html2)
        nested = write_fixture(
            "# fixture\n\n- `chat.process-notes: dense working notes` — (fixture)\n"
            "  - a nested sub-bullet under the habit\n"
            "  - another nested line\n")
        code3, html3 = render(nested)
        self.assertEqual(code3, 0, html3[:400])
        self.assertNotIn("- `", html3, "raw markdown leaked from a nested profile shape")
        template_profile = os.path.join(ROOT, "templates", "profile.template.md")
        if os.path.exists(template_profile):
            code4, html4 = render(template_profile, host=missing_host)
            self.assertEqual(code4, 0, html4[:400])
        # unmatched personal entries never wall the card: however many there are
        # (here two, one quoting banned vocabulary), they collapse into ONE plain
        # summary row; their own words stay in the profile
        long_rule = ("- `language.no-calques: in chat never loan-translate a doc "
                     "term; the known-bad examples are «растяжки» and «узел-владелец» "
                     "and more words making this line run far past any card-sized "
                     "value, wrapped and long` — (fixture, 2026-07-10)\n"
                     "- `chat.process-notes: dense working notes marked so he can "
                     "skip them` — (fixture, 2026-07-10)\n")
        code5, html5 = render(write_fixture("# fixture\n\n" + long_rule))
        self.assertEqual(code5, 0, html5[:400])
        self.assertNotIn("растяжки", html5,
                         "an unmatched recorded line rendered whole onto the card")
        self.assertIn("2 more preferences", html5,
                      "the unmatched entries must collapse into one counted summary row")
        self.assertIn("personal profile", html5,
                      "the summary must say plainly where the lines live")
        self.assertNotIn("language.no-calques", html5,
                         "an unmatched raw key leaked onto the card")

    def test_onboarding_card_wiring(self):
        """M-210 (INV-87): the trigger sentences stand in their homes and the
        norm pointer resolves."""
        adopt = read_flat(os.path.join("adopt", "ADOPT.md"))
        self.assertIn("settings card", adopt,
                      "adoption lost the setup-end settings-card line")
        comm = read_flat(os.path.join("skills", "communicator", "SKILL.md"))
        self.assertIn("what can I customize", comm,
                      "communicator lost the standing-question line")
        # The dated frozen-norm pointer is a dated provenance reference; the requirements-format spec
        # body bans dates (SPEC INV-253/no-history), so the norm pointer's home is ARCHITECTURE.md's
        # onboarding-card node, where the wiring and ownership live.
        arch = re.sub(r"\s+", " ", read("ARCHITECTURE.md"))
        self.assertIn("docs/norms/onboarding-card-2026-07-10.html", arch,
                      "the architecture lost the frozen-norm pointer")
        self.assertTrue(os.path.exists(NORM), "the frozen norm file is gone")


if __name__ == "__main__":
    unittest.main()
