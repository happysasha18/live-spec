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

## Handled, 2026-09-09 09:15, live-spec

The first finding holds and is repaired; the second is noted and left where it stands. The owner
handed both on this morning, naming the repair for the first and holding the second out of it.

**The installer road — repaired (q-832, released as 6.1.3).** The cause is the one this note names.
`scripts/check-pack-update.sh` sorted stale manifest keys by whether they began with
`scaffold/guardrails/`, and `adopt/install-scaffold.sh` also vendors five run-mode files pinned
under their host-relative paths, which that prefix never reaches. Driven here against a manifest
pinning those five, the watcher printed the style-gate road alone — the reproduction this note
recorded, seen again on the real script. The sorting now asks which installer's own vendor set
carries the key, and it reads `install-scaffold.sh`'s `VENDOR_MODES` array out of that installer
rather than keeping a second copy of the list, because a second copy is how the 2026-07-16 fix came
undone: the branch it repaired stayed right while the list beside it grew. Three cases in
`tests/test_update_watcher.py` drive the real watcher script, red-proven against the old sorting
before they were trusted green.

The first attempt at that repair read `install-scaffold.sh`'s array alone and let everything it did
not claim fall to the style-gate road by default, which is this same defect with a different set of
victims. The independent verification caught it before the push: `adopt/install-status-view.sh`
keeps its own `VENDOR` array of eight keys and writes them into the same manifest, and a host stale
on `scripts/render-board.sh` or `scaffold/status-view/state-probe.sh` was handed the style-gate road
by exactly the same fall-through. So the sorting reads every `adopt/install-*.sh` for its own vendor
arrays and maps each key to the installer that states it, and a key no installer claims is said out
loud. Seven cases drive the real script: the five run-mode files, the style-gate set alone,
the status-view set alone, all three kits at once, a key no installer vendors, an old pin with
nothing stale naming only the kits it pins, and every installer's whole array walked one at a
time.

**The estimate unit a close cannot convert — noted, no row.** The owner asked for this one to be
left alone this morning. It is true as written: `read_statement` takes any alphabetic unit, and
`_elapsed` converts hours and days and otherwise prints minutes wearing the row's own word, so a row
estimated in weeks or sessions closes with a line like `estimate 2–3 weeks → actual 740 weeks`. What
it costs is bounded: nothing reads that number — the duration reader parses minutes, hours and days
alone, so such a line reaches no history and no estimate. What is left is one line a person reads on
a checkpoint, and no row of this tree has ever carried either unit. It stands here for a later review
to find again if a row ever does.
