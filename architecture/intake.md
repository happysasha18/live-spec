### [node: inbox]

**responsibility** — the parallel-safe intake door for wishes born outside a live-spec session. Its remote arm serves granted seats. Its stranger arm bridges Issues and Discussions into inbox files through a monitor. Two hosts on one repo converge on a single surfacing by a claim on the shared item.

**owns** —
- E-11 · T-10 · INV-10 · INV-112 · INV-146 · INV-147 · INV-148 · INV-149 · INV-174 · INV-192
- INV-232 (the read-direction sibling of the remote arm's push grant this node owns)
- INV-249 (the concurrency half of E-11's one-file law)

**pins** —
- `inbox/README.md:3` (one door, one new file)
- `inbox/README.md:10` (file format)
- `inbox/README.md:109` (commit rule)
- `inbox/README.md:120` (remote arm)
- `inbox/README.md:125` (stranger arm)
- `scripts/stranger-wish-monitor.py:1` (the monitor bridge, INV-147)
- `scripts/stranger-wish-monitor.py:103` (the cross-host claim + arbitration, INV-149)
- `.github/ISSUE_TEMPLATE/wish.yml:1` (the wish template requesting a source, INV-146)
- `.github/workflows/stranger-monitor.yml:1` (the package repo's scheduled monitor, INV-148)
- `scripts/read-grant.py:1` (the read-grant honest-failure check, INV-232)
- `scripts/read-grant-ask.md:1` (the read grant ask, beside `scripts/grant-ask.md`, INV-232)

**notes** — INV-232: the consumer's read the spec-author node owns. INV-232: the honest-failure check `scripts/read-grant.py`. INV-232: the real cross-machine read field-gated on a private producer-and-consumer pair over a private repo, rows 385 and 247, this landing the law arm alone.

### [node: feedback-intake]

**responsibility** — the intake half of the exchange. It receives anything handed back through three channels and routes each item to the home its law owns. It keeps the feedback ledger's shape and echoes every arrival (row 47).

**owns** — E-28, T-20, INV-68

**pins** — `skills/feedback-intake/SKILL.md:1` (frontmatter + when it fires), the routing table and ledger-shape sections in the same file
