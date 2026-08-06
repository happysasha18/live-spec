# Prover record — the check registry and its gate, 2026-08-06

The design under review: `scratchpad/design-B-host-scripts.md`, how an adopting project gets the
pack's runnable parts. The review is `scratchpad/prove-B-host-scripts.md`. The reworked design that
landed is `scratchpad/design-B2-host-scripts.md`, the first slice alone. The landed requirement is
Requirement 307 (INV-306), matrix rows M-505 through M-511, queue row 556, and gate ae.

## The verdict

Rework, then build the named first slice. The review gave three independent reasons the design could
not land in one pass: it touched more than thirty files across six write sets, four of which carry
their own gate; it invented four mechanisms where three of them depended on a fifth that did not
exist, a host-root contract; and its central field, the route column, had no stated membership, so
the work could not be divided without someone first making forty-five undelivered decisions.

The slice it named: the classification and its gate, with no execution mechanism. That is what landed.

## The findings and their fate

Thirteen must-fix, eight should-fix, two recorded.

**Answered by the slice's scope.** F1 (a resolved check reads the pack's own tree and reports green
over it), F2 (the route column has no stated membership), F3 (vendored checks reach no host push
gate), F4 (the resolver trusts an unversioned candidate), F5 (the runner has no reachable install
location), F6 (the registry cannot source the vendor list), F9 (a check and its data may take
different routes), F10 (six rows practice-gated by their own justification) and F12 (the manifest's
object shape breaks the watcher's hash comparison) all sit on the resolver, the runner, the vendored
set and the watcher. This slice ships none of them. Nothing executes differently after it lands.

**Answered in the landed design.**

- **F7 — the new gate would land with no known-red proof and no CI mirror row.** Gate ae carries a
  `proofs` entry and a mirrored step, and the design states the two red proofs verbatim: a pack-only
  check restored to the text-audit body, and a declared root changed to disagree with the code.
- **F8 — two files on the write list are generated artifacts a hand edit reds.** Both left the write
  set, and the design names them and the generator that owns them.
- **F14 — the gate's first arm reds on prose that names a check as a noun.** A command position is now
  defined as a path preceded on its line by `python3`, `bash`, `sh`, or a leading `./`; every other
  mention is prose and keeps its path.
- **F19 — nine decisions a builder must invent.** The registry's fields are stated one at a time, the
  kit is derived from the reach rather than typed, and the host-root contract is written out in
  section 2 so every later slice reads one settled answer.

**Recorded.** The review's two recorded items were the language-rules quartet's deferral, which the
design had already declared, and the provisional identifiers, which this landing fixed: Requirement
307, INV-306, matrix rows M-505 through M-511, queue row 556, gate ae.

**Open questions the author answered.** The registry's domain stays scoped to what skill bodies name
and what those entries read, rather than every installable file; the five scaffold checks are a later
row's decision. The vendored-against-resolved axis is dropped from this slice with the route column.

## What this slice does not claim

The gate holds the shape of the record: an entry per runnable file a skill names, a kind that agrees
with the tree, a kit derived from a declared reach, a declared root, and no pack-only check standing
in a host's steps. Whether a check should exist, and whether the reach it declares is the right
reach, stay with the person. The six later rows in the design's section 9 carry the mechanism.

## Note on the state of the tree at the time of writing

This record was written while the landing's code was still being edited. At the time of writing,
`scripts/check-registry.json`, `guardrails/check-named-checks.py` and `tests/test_check_registry.py`
do not stand in the tree, so the matrix rows M-505 through M-511 read *todo* and name that test file
as their owner. They flip to *built* when the landing's own files arrive.

## Reach

Read directly: `scratchpad/design-B-host-scripts.md`, `scratchpad/prove-B-host-scripts.md` including
its ranked must-fix list and its fate ledger, `scratchpad/design-B2-host-scripts.md` sections 1
through 9, `guardrails/pre-push`, `guardrails/gate-red-proofs.json`,
`.github/workflows/gates.yml`, and `skills/text-audit/SKILL.md`.
