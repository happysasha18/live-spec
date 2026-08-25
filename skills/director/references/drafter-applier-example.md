# The drafter-applier pipeline

The worked form of the standard colliding-rows pattern, referenced from
`references/lanes-and-pen.md`'s "Trains, one pen — the lane law" section (SPEC INV-49).

**The drafter-applier pipeline is the standard colliding-rows form (SPEC INV-49):** on colliding rows
the penless DRAFT stage overlaps the current landing: a drafter worker at the judgment tier prepares the
next row's exact edit strings with self-verified needles while the applier lands the current row under
the pen. Before handoff the drafter walks a standing self-verify list against the suite's cross-reference
laws — index density (every new INV anchor gets its Formal-index row), owning node (every new anchor's
node stands in ARCHITECTURE.md's owns-list), and matrix-row-under-owner (every new M-row sits under its
owning node) — so the draft catches these suite-enforced cross-references itself, sparing the applier a
red-first STOP the drafter's own read could have closed. The landing order stays declared and the numbers follow it. This form ran live 2026-07-12, the
night the law batch serialized on the spec/matrix/version chain and still moved at two rows an hour
[T-18, INV-39, INV-49].
