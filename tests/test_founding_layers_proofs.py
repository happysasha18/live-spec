"""A project.kind founding declares its concrete layers AND proof kinds — M-276 (SPEC INV-135, row 292).

P0k of the architect draft: the entry impact read, the footprint categories, and the test ladder are
kind-ABSTRACT stations. Each project kind fills them with its own concrete layers and its own concrete
proof kinds — a photo site decomposes and proves nothing like a codebase. The pack states the abstract
station once; a project's founding declares its concrete fill, recorded in the host profile beside
`project.kind` (SPEC INV-36). A founding check reds a profile that records a kind with no declared layers
and no declared proofs, the way an unbacked surface is flagged at adoption.

The check is red-proven against three real hosts as fixtures — a code/music kind (track-coach), a photo
kind (tlvphotos), a prose kind (the promotion campaign) — each with its own layers and proofs, plus a
kind-only profile that must go red.
"""

import re
import unittest

from conftest import open_spec, read, read_all_flat, read_flat

KIND = re.compile(r"(?m)^\s*[-*]?\s*`?project\.kind:")
LAYERS = re.compile(r"(?m)^\s*[-*]?\s*`?project\.layers:")
PROOFS = re.compile(r"(?m)^\s*[-*]?\s*`?project\.proofs:")


def founding_complete(profile_text):
    """The founding check: a profile that records a project.kind must also declare its
    concrete layers and its concrete proof kinds. Returns (ok, reason)."""
    if not KIND.search(profile_text):
        return True, "no project.kind recorded — nothing to complete"
    missing = []
    if not LAYERS.search(profile_text):
        missing.append("project.layers")
    if not PROOFS.search(profile_text):
        missing.append("project.proofs")
    if missing:
        return False, "project.kind recorded with no declared " + " and no ".join(missing)
    return True, "kind, layers, and proofs all declared"


# --- three real hosts as fixtures, each its own kind with its own layers and proofs ---
FIXTURE_CODE = """# Host profile — track-coach
- `project.kind: code / music project`
- `project.layers: arrangement · stems · mix`
- `project.proofs: the analysis renders · the pytest suite · the owner's ear`
"""

FIXTURE_PHOTO = """# Host profile — tlvphotos
- `project.kind: photo portfolio (fullstack, static-first)`
- `project.layers: content · rendering engine · deployment`
- `project.proofs: a byte-diff of the baked output · the owner's eye-walk`
"""

FIXTURE_PROSE = """# Host profile — promotion campaign
- `project.kind: prose / promotion campaign`
- `project.layers: message · channels · assets`
- `project.proofs: the register lint · the owner's review`
"""

FIXTURE_KIND_ONLY = """# Host profile — a half-founded project
- `project.kind: code / fullstack app`
"""


class TestFoundingCheck(unittest.TestCase):
    def test_three_kind_fixtures_pass(self):
        for name, fx in (("code", FIXTURE_CODE), ("photo", FIXTURE_PHOTO), ("prose", FIXTURE_PROSE)):
            ok, reason = founding_complete(fx)
            self.assertTrue(ok, "%s fixture should be complete: %s" % (name, reason))

    def test_kind_without_layers_or_proofs_goes_red(self):
        ok, reason = founding_complete(FIXTURE_KIND_ONLY)
        self.assertFalse(ok, "a kind-only profile must be flagged incomplete")
        self.assertIn("project.layers", reason)
        self.assertIn("project.proofs", reason)

    def test_missing_only_proofs_goes_red(self):
        half = FIXTURE_CODE.replace("- `project.proofs: the analysis renders · the pytest suite · the owner's ear`\n", "")
        ok, reason = founding_complete(half)
        self.assertFalse(ok, "a profile missing only proofs must be flagged")

    def test_live_host_profile_is_complete(self):
        """The pack's own flagship host must satisfy the founding check it ships.
        Read RAW — the check reads line-anchored `project.*:` records, not flattened prose."""
        ok, reason = founding_complete(read(".live-spec/profile.md"))
        self.assertTrue(ok, "live-spec's own host profile is incomplete: " + reason)


class TestFoundingLaw(unittest.TestCase):
    def test_base_rulebook_states_layers_and_proofs(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        for needle in (
            "the stations are kind-abstract",
            "declares its concrete layers",
            "its concrete proof kinds",
            "SPEC INV-36",
            "INV-135",
        ):
            self.assertIn(needle, base, "base rulebook lost the per-kind declaration rule: %s" % needle)

    def test_spec_clause_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # R174 heading: requirements-format rewrite retitles the same clause.
        self.assertIn("Founding declares the project's concrete layers and proof kinds", spec)
        self.assertIn("[INV-135]", spec)
        row = None
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-135 |"):
                    row = line
                    break
        self.assertIsNotNone(row, "INV-135 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — the "layer"/"proof" prose check
        # moves onto the body heading asserted above, which carries both words.

    def test_architecture_has_per_kind_footprint_and_proof_table(self):
        arch = read_flat("ARCHITECTURE.md")
        self.assertIn("Footprint and proof by project.kind", arch)
        for needle in ("skill pack", "content · rendering engine · deployment", "register lint"):
            self.assertIn(needle, arch, "ARCHITECTURE per-kind table lost: %s" % needle)

    def test_spec_author_and_test_author_read_declared_layers(self):
        sa = read_all_flat("skills/spec-author/SKILL.md")
        ta = read_flat("skills/test-author/SKILL.md")
        self.assertIn("declared layers", sa, "spec-author does not read the declared layers")
        self.assertIn("declared proof", ta, "test-author does not read the declared proofs")

    def test_adopt_founding_prompts_layers_and_proofs(self):
        """The host-profile founding record is set at adoption's orient (ADOPT.md), not the
        personal profile template — the founding declares the host's own layers and proofs."""
        adopt = read_flat("adopt/ADOPT.md")
        self.assertIn("project.layers", adopt)
        self.assertIn("project.proofs", adopt)
        self.assertIn("SPEC INV-135", adopt)


if __name__ == "__main__":
    unittest.main()
