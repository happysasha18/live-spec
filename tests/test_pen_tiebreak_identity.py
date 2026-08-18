"""The pen tie-break rests on an identity every session owns (SPEC INV-117, row 277).

The parallel-lanes pen tie-break used to break a no-ancestry concurrent claim by the lower
inbox session token, but that token is minted only at an inbox slug collision — a session
that never raced a slug had none. The fix mints a stable per-session identity at session
start, independent of the inbox, and the pen tie-break orders on it.
"""

import unittest

from conftest import open_spec, read_flat


class TestPenTiebreakIdentity(unittest.TestCase):
    def test_session_identity_minted_at_start_phrase(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("session identity", spec)
        self.assertIn("minted at its start", spec)

    def test_tiebreak_orders_on_session_identity(self):
        # the inline "[INV-117]" right after the phrase moved to the criterion's trailing codes
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("session identity sorts lower", spec)

    def test_inbox_token_is_projection_phrase(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "make the inbox source-mark's short session token a projection of that same one identity",
            spec,
        )

    def test_spec_anchor(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-117]", spec)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "session", spec.lower(),
            "INV-117's body criterion doesn't carry the session phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-117 |"):
                    return
        self.fail("INV-117 index row missing")


if __name__ == "__main__":
    unittest.main()
