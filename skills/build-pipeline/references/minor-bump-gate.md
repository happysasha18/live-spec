# Before a MINOR (0.x.0) bump

The full gate procedure referenced from `SKILL.md`'s "Gates worth remembering" section.

**Before a MINOR (0.x.0) bump:** the 3-pass preventive audit — product-prover on the whole spec + a matrix
audit + a surface-composition check. The full **design review** runs here too, beside the
surface-composition check (SPEC INV-141): the whole element inventory, every proposed same-kind grouping,
its likely divergences echoed as at most three asks (no incident or source behind the 3; an engineering
default, not a policy decision) — recommendations and questions only, never a block. The gate also runs the **cross-cut counter** (`guardrails/crosscut_counter.py`,
SPEC INV-128 boundary-health, INV-37): it counts the closed queue's cross-cutting landings per node pair,
and a pair reaching the threshold (3 by default) is flagged as a boundary-move candidate for the audit to
weigh — the flag is a signal, never a push-blocking red, and a boundary still moves only through the
architecture step and its re-prove. Fix holes by the book; record the rest. The gate also runs
**code compaction as a station beside doc compaction (SPEC INV-123):** duplicate logic merges, dead weight
leaves with its listing (INV-109), a ripened abstraction is extracted only through the three-question
fitness gate (INV-122), and each pass locks its reached level with a test or lint where newly reached, else the existing suite that holds it green (rows 216-218). The
station has a second trigger beyond this gate — the second occurrence of the same problem
opens the duplication's own compaction row at that moment (the problem ledger's own owner) as well as at the milestone; the
row lands through the ordinary pipeline (one row's delta, INV-39; a known duplication never blocks its
lane, INV-56). The duplication becomes a queued row, held back from an on-the-spot in-place fix.

The gate also **re-runs the skill evals and sends every skill in the pack through skill-creator's
craft review (SPEC M-1):** each finding either gets folded in or turned away, the
call recorded and dated, and a skill joining the pack for the first time takes this same walk at
birth, before it ever reaches its own first gate.
