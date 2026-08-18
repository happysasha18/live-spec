# PUSH-REVIEW — the layered README and the progress-report scratch road

Date: 2026-08-18 late morning. Range: 1c85db1..HEAD — two merged branches:
readme/2026-08-18-layered (7c7931b) and fix/2026-08-18-progress-scratch (d747bcd).
Root: the owner's direction of 2026-08-18 morning — the pack is turn-key, the
non-technical customer is a first-class reader, docs are layered ("no tupi"
direction, verbatim in the coordinator's window); and the night's twice-proven
mechanism defect: the test suite rewrote the protected docs/PROGRESS.md.

What landed:
- README.md restructured in two layers: the top layer is customer-complete
  (install in three steps with zero manual config/regex/git-hook work; the setup
  walk automates them), a "For builders" section carries the by-hand road, and
  one line points programmers at the inbox for technical wishes. OVERVIEW.md and
  docs/adoption.md checked — already read correctly as deeper docs, unchanged.
- scripts/progress-report.py gains --out PATH (default unchanged);
  tests/test_progress_report.py writes to its own scratch — a full run leaves
  docs/PROGRESS.md untouched (red-then-green proven in the branch record).

Checks run:
- Cold readers, two rounds (the cap): non-technical 7→4 blocking with targeted
  fixes verified against source; programmer 1→1→fixed. Hostile review: BLOCK on
  a real contradiction, both findings fixed, second pass clean.
- Register lint, tree-counts gate (exit 0 on the merged tree), host-count regex,
  pin-drift, SURFACES.md needles, link resolution — green.
- Focused pytest on the merged tree: test_progress_report + test_setup_entry —
  43 passed, 1 error under parallel contention; the erroring node re-run alone —
  1 passed in 0.04 s (the error is the known shared-tmp artifact of two suites
  running at once, recorded in the night report).

Findings:
- Three factual bugs in README fixed en route (mis-attributed error line, a
  self-contradicting two-roads claim, a dead placeholder disclosed in Known
  Issues). One honest gap stands: round-2 reader fixes were verified against
  pins and sources, not by a third read — the reading budget is two rounds.

Blocking:
- none.
