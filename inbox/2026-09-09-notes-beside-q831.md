# Notes beside q-831 — 2026-09-09

Two things the global review of the 6.1.2 push found true outside the surface it was scoped to.
Neither opens a row and neither asks for a repair; they are left here for the intake sweep to judge.

The daily update watcher names the wrong installer for five of the files it reports stale. In
`scripts/check-pack-update.sh`, the manifest arm sorts stale entries by whether the key begins with
`scaffold/guardrails/`: those get `adopt/install-scaffold.sh --force`, and everything else gets
`adopt/install-style-gates.sh --force`. The five run-mode files that `adopt/install-scaffold.sh`
vendors are pinned under their host-relative paths instead — `guardrails/check-acceptance-rerun.py`,
`guardrails/run_modes.py`, `guardrails/worker-admission-guard.py`, `scripts/task-admission.py` and
`scripts/checkpoint.py` (adopt/install-scaffold.sh:61-67 and its manifest pass at :139) — so a host
whose only stale files are those is handed the style-gate installer, whose vendor set
(adopt/install-style-gates.sh:97-107) contains none of them. Driven here against a manifest pinned
at the real 6.1.1 contents of every vendored file, the watcher reported
`guardrails/check-acceptance-rerun.py` and `scripts/task-admission.py` stale and printed the
style-gate road alone. This is the same misrouting the 2026-07-16 note in that file says it fixed,
returning through the newer pins rather than through the branch it repaired; it predates this push,
which is only the first release that changes those two files.

A row whose estimate names a unit the close cannot convert records a false number in its own
delivery trail. The estimate a statement carries takes any alphabetic unit — the pattern
`read_statement` reads, scripts/task-admission.py:343 — and `_elapsed` (:1498) converts for hours
and for days and otherwise falls through to `"%d %s" % (minutes, unit)`, so a row estimated in
"weeks" or in "sessions" closes with `estimate 2–3 weeks → actual 740
weeks`, a minute count wearing the row's own word. Nothing reads that number today: the new
duration reader only parses minutes, hours and days, so such a line contributes nothing to any
history or estimate. What is left is the line a person reads on the checkpoint.
