"""The seat verifies write-set disjointness at brief-time before spawning a second concurrent writer.

The concurrent-edit fence [INV-11] stays silent between same-session sibling workers (fence-benign),
so the reactive net cannot catch two of the seat's OWN helper workers colliding on a shared
file. This law puts the check where the silence forces it: at brief-time, before the second concurrent
writer is spawned, the seat confirms the two briefs' write-sets are disjoint or gives the later worker
an isolated tree. It extends ACT-3 / INV-11 (a spawn-time obligation on the existing "the seat owns
the seams" duty), so it homes on the worker contract and adds no new invariant. Born of a real
two-sibling-worker collision that self-corrected (tlvphotos 2026-07-13).
"""

import unittest

from conftest import read_flat, read_all, read_all_flat

# The shared imperative, punctuation-identical across every home so one needle matches all.
# N-ary (disjoint from EVERY already-running writer, since T-18 allows up to three lanes), R1 folded.
IMPERATIVE = (
    "before spawning another concurrent writer, the seat confirms its brief's write-set is "
    "disjoint from every already-running writer's brief"
)


class TestBriefTimeDisjointness(unittest.TestCase):
    def test_spec_worker_contract_carries_the_imperative(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # R207.3 [INV-11, INV-105, ACT-3]: same imperative, new requirements-format phrasing
        # (drops "already-" and folds fence-benign framing into the "since" clause).
        self.assertIn(
            "the seat means to spawn another concurrent writer, it *shall* confirm "
            "the brief's write-set is disjoint from every running writer's brief",
            spec,
        )
        # settled at brief-time, not discovered at the write: the check is framed as a
        # prospective act ("means to spawn ... shall confirm"), before the spawn itself.
        self.assertIn("means to spawn another concurrent writer, it *shall* confirm", spec)
        # homed on the worker-contract clause: the seat is the named actor who confirms.
        self.assertIn("the seat means to spawn", spec)

    def test_build_pipeline_carries_the_operational_imperative(self):
        # delegation-protocol.md now lives in skills/build-pipeline/references/: delegation is
        # execution, and execution moved out of Director with the classifier/pipeline split (q-822).
        sk = read_all_flat("skills/build-pipeline/SKILL.md")
        self.assertIn(IMPERATIVE, sk)
        self.assertIn("settled when the briefs are written", sk)

    def test_live_spec_base_carries_the_pointer(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn(IMPERATIVE, base)
        self.assertIn("brief-time", base)


if __name__ == "__main__":
    unittest.main()
