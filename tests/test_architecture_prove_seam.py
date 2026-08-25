"""The architecture → prove seam and the Prover-record append-duty — row 273 (SPEC INV-116).

INV-116 sends ARCHITECTURE.md into the prover at every M-1 and M-6 gate, the exact analogue of the
named `spec → prove` seam. Two gaps trailed the law (fresh prover pass, 2026-07-12 s38, findings
F-arch-1/F-arch-2): the Seams table carried no `architecture → prove` row, and nothing in the gate
walk said an architecture pass appends its row to the architecture's Prover record table, so the table
drifted. This closes both.
"""

import unittest

from conftest import read_flat

ARCH = "ARCHITECTURE.md"
PIPE = "skills/architect/SKILL.md"
APPEND_DUTY = "appends its dated row to"


class TestArchitectureProveSeam(unittest.TestCase):
    def test_seam_row_present(self):
        body = read_flat(ARCH)
        self.assertIn("| architecture → prove |", body)

    def test_append_duty_in_architecture(self):
        self.assertIn(APPEND_DUTY, read_flat(ARCH))

    def test_append_duty_in_gate_walk(self):
        self.assertIn(APPEND_DUTY, read_flat(PIPE))

    def test_record_table_caught_up_to_1_1_0(self):
        # Since the row-456 format conversion the dated prover-record table lives in its own home under
        # the prover records, the architecture stating today's structure alone (SPEC INV-279).
        body = read_flat("docs/prover/architecture-prover-record.md")
        self.assertIn("2026-07-12-full-pass-pre-1.1.0.md", body)
        self.assertIn("2026-07-12-s38-inv115-inv116-and-architecture.md", body)


if __name__ == "__main__":
    unittest.main()
