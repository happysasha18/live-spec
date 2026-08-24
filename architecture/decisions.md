## Decisions — where they live

The pack's decisions live in three homes already. The first is the queue's dated rows, each landing's
verdicts inline. The second is JOURNAL.md's chapters, which hold the why. The third is DECISIONS.md's
open-decision entries: D-1, D-6, D-7, covering attic layout, pair queue view, and engine-fact
citation. They moved there from the retired Formal index at the 4.0.0 format migration, and the spec's
`[GAP: ...]` lines now point to them. This section is the doc's one entry point to them, and it holds
pointers rather than the decisions themselves. Structure-changing decisions also appear in the
architecture prover record at `docs/prover/architecture-prover-record.md`, one line each. Every full
pass that proves this document beside the spec appends its dated row to that prover record (INV-116).
Those passes run at an M-1 milestone gate and at an M-6 push gate. The gate walk carries the duty, so
the record stays current with the architecture's freshness rule rather than trailing it. The M-1
milestone gate also runs the design review on the re-proven spec (INV-141). Its dated design-review
record lands in `docs/design-review/`, beside the prover record. A structure-changing design decision
it settles appears in that prover record's rows like any other.

*Coverage rule (walked at matrix derivation): every spec anchor appears in some node's "owns" column. An
orphan fact means a missing node or a missing assignment. A node that owns nothing has no spec backing,
and that is itself a finding. Mechanized in `tests/test_traceability.py`.*

**Boundary health — a typical request lands in one node (SPEC INV-128).** A right node boundary shows
one sign. An edit inside a node leaves its neighbours untouched, so a typical request's footprint is
single-module. When requests repeatedly cut across the same several nodes, the boundary sits in the
wrong place. The signal is the entry impact read recording a cross-cutting footprint on the same node
pair again and again. The recorded footprints are the evidence a boundary move rests on. A boundary
moves only through the architecture step and its re-prove, as a restructure row [E-14, and INV-37 in
the spec]. It never moves on a guess, and it never stays wrong in denial while the cross-cuts pile up.
The **cross-cut counter** mechanizes the signal. `guardrails/crosscut_counter.py` reads the closed
queue's cross-cutting landings. It counts, per unordered node pair, how many cross-cutting changes
touched both nodes. A pair reaching the threshold, 3 by default and tunable, is flagged for the MINOR
audit as a boundary-move candidate. That is the mechanized form of "seen twice, own it" (base rule 19)
applied to boundaries. The flag is an audit signal, never a per-push red. The count is evidence the
MINOR audit weighs. The boundary still moves only through the architecture step and its re-prove
[INV-37]. This law states the bar and the signal; the counter is the recorded footprints made
countable.
