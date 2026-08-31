# Prover record — 2026-09-01, three lanes landed, the merge repaired, the board tidied

PUSH-REVIEW

Range: bff2715a..HEAD
- 1becbcf9 Fix off-by-one in test_guardrail_fixture_proofs.py's own docstring count (this review's own repair, finding 2 below)
- 834db84b NEXT_STEPS: heals landing d470d2be, heals landing dbf0fc01, heals landing 1bdd55c1
- a99ba2b0 Merge repair: shipped-language, cleanup-notice, and the NEXT_STEPS refresh the range still owed
- 35c6dca9 Merge branch 'worktree-agent-a9025f83a5ab923ff'
- 6270ea70 Merge branch 'worktree-agent-abd7150f4a2a849bf'
- 6410246e Merge branch 'worktree-agent-af48375be508cea17'
- 9702213f Board hygiene: three dead rows archived, q-48 correctly kept (owns a live target), three overbuilt rows narrowed before dispatch
- 1bdd55c1 Add wind-down.py: one command to safely halt workers, checkpoint, and push before leaving
- dbf0fc01 q-581 lands: a session is warned before a command can raise a security dialog
- d470d2be q-489: one check proves it can catch its own problem, and a walking test binds the rest
- eaf35306 NEXT_STEPS catches up: tonight's push landed, and what actually happened

Files read: PRODUCT_SPEC.md (INV-21, INV-120/245, INV-204, INV-242 anchors), ARCHITECTURE.md,
hooks/dialog-warning-guard.py, tests/test_dialog_warning_guard.py, scripts/wind-down.py,
tests/test_wind_down.py, guardrails/cleanup_notice.py, tests/test_guardrail_fixture_proofs.py,
guardrails/check-prototype-fence.sh, PLAN.md (rows q-48, q-398, q-536, plan-14, plan-15, q-453,
q-751), NEXT_STEPS.md, tests/test_traceability.py (TARGET_ROW_OWNERS),
docs/queue-archive/rotated-PLAN-2026-08-31-hostile-review-archive.md, guardrails/pre-push,
guardrails/check-doc-rotation.py, guardrails/check-landing-next-steps.py,
guardrails/check-authority-anchor.py, guardrails/check-shipped-language.sh,
guardrails/check-cleanup-notice.sh, scripts/install-worker-restore-guard.sh,
hooks/worker-restore-guard.py, ~/.claude/settings.json, ~/.claude/hooks/ (installed-side state).

Checks run: python3 -m pytest -q, whole suite, alone on the merged tree at 834db84b, run by the
orchestrating session immediately before this review — 2680 passed, 6 skipped, 0 failed. This
review did not repeat that run (standing rule: no second full-suite run while another process may
touch the tree). Independently, this review ran: (1) python3 -m pytest -q tests/test_wind_down.py
tests/test_dialog_warning_guard.py tests/test_guardrail_fixture_proofs.py tests/test_traceability.py
— 209 passed, 2 skipped; (2) python3 guardrails/check-doc-rotation.py — OK; (3) python3
guardrails/check-landing-next-steps.py — OK, with three expected WARNs (d470d2be, dbf0fc01,
1bdd55c1) each naming its own heal by 834db84b, matching the claimed HEAL ROAD use; (4) python3
guardrails/check-authority-anchor.py — OK (NOTE candidates only, non-blocking, unrelated to this
range); (5) bash guardrails/check-shipped-language.sh — OK, 0 offences (confirms the "Alexander"
comment removed from scripts/wind-down.py by a99ba2b0 does not recur elsewhere); (6) bash
guardrails/check-cleanup-notice.sh — OK (confirms signal_worker()'s cleanup_notice.cleanup_notice()
call added in a99ba2b0 satisfies INV-204); (7) `ls guardrails/check-*.py guardrails/check-*.sh | wc
-l` — 41, matched by direct Python re-derivation of test_guardrail_fixture_proofs.py's GRANDFATHERED
set (40) + PROVEN (1) against the real directory listing — exact match, no stale entries, no
uncovered new arrivals; (8) grep + manual read of tests/test_traceability.py's TARGET_ROW_OWNERS —
confirmed INV-21 maps to q-48, and confirmed plan-15/q-453/q-751 appear nowhere as a value in that
map, so archiving them cannot orphan a spec anchor; (9) git log --graph plus a grep for conflict
markers across the merge range — three merges, zero conflict markers, confirming the "merged with
no conflicts" claim; (10) diff of every line the three lanes added against HEAD's own files (spot
read, not exhaustive) — no content silently dropped by the merges; (11) read of
~/.claude/settings.json's hooks.PreToolUse array and ls of ~/.claude/hooks/ — see finding 1.

Findings: five. One repaired here. One stands, non-blocking, reported for the orchestrating
session's judgment. Three checked clean.

1. **hooks/dialog-warning-guard.py sits on disk but is not wired, and there is no install script
   for it, unlike its sibling.** The file itself is already copied to
   `~/.claude/hooks/dialog-warning-guard.py` (mtime 2026-09-01 00:12, byte-identical to the repo
   copy), but `~/.claude/settings.json`'s `hooks.PreToolUse` array names only
   `block-triple-equals.sh` and `worker-restore-guard.py` — this hook is absent from it. It will
   never fire in its current state: PreToolUse hooks run only if `settings.json` lists them.
   `worker-restore-guard.py` has `scripts/install-worker-restore-guard.sh` (idempotent, validates
   settings.json, backs up, wires the PreToolUse entry); `dialog-warning-guard.py` has no matching
   install script anywhere in this range or the tree. The hook's own docstring is honest about this
   ("installed copy (once a host wires it, the way `scripts/install-worker-restore-guard.sh` wires
   its neighbour): ~/.claude/hooks/") and q-581's stated acceptance in PLAN.md (a flat list beside
   one rule, a test hitting every listed command, `grep` finding the rule stated once) does not
   itself demand installation or wiring — so marking the row done is consistent with its own
   written acceptance. But as shipped, the feature protects nobody yet: the exact dialog class it
   was built to warn about (deposit 2026-08-07, two interruptions the same session) can still fire
   silently tonight, on this machine, because the copy in `~/.claude/hooks/` is inert. **Not
   closed here** — writing an install script or wiring the settings.json entry is a judgment call
   about scope (the same class of call q-567 made explicitly, as its own row, for a related
   portability gap) rather than a bug in the code that landed. Reported for the orchestrating
   session; not blocking, since the row's own acceptance criteria were met as written and the gap
   is disclosed in the shipped docstring rather than hidden.

2. **tests/test_guardrail_fixture_proofs.py's docstring miscounted the GRANDFATHERED set by one.**
   The module prose said "this file does not retrofit the other thirty-nine" and "GRANDFATHERED
   (the other 39, named here explicitly...)" — the actual frozenset has 40 entries (41 real
   `check-*.py`/`check-*.sh` files under `guardrails/`, minus the 1 in PROVEN). Confirmed by
   re-parsing the file's own GRANDFATHERED literal (40 items) and by `ls guardrails/check-*.py
   guardrails/check-*.sh | wc -l` (41). The walking test itself is data-driven off the real
   frozenset and directory listing, so this was a prose-only defect with no effect on what the
   test actually checks — but the class this row exists to prevent (a check shipping unaccounted
   for) would have been exactly this kind of silent off-by-one had the set itself, not just its
   prose count, been short one real entry. **Closed here:** both occurrences ("thirty-nine" and
   "39") corrected to forty/40 in `tests/test_guardrail_fixture_proofs.py`; suite re-run clean
   (5 passed) after the edit.

3. **q-48/INV-21, and the three archived rows, checked independently rather than taken on the
   commit message's word.** `tests/test_traceability.py`'s `TARGET_ROW_OWNERS["INV-21"] = "q-48"`
   is real, so keeping q-48 open (deferred, not archived) is correct — archiving it would have
   orphaned a live spec anchor. `plan-15`, `q-453`, `q-751` appear nowhere as a value in that same
   map, so their archival in
   `docs/queue-archive/rotated-PLAN-2026-08-31-hostile-review-archive.md` (with its manifest line
   and Index table) is safe by the same test. Clean.

4. **check-doc-rotation.py, check-landing-next-steps.py, check-authority-anchor.py all genuinely
   pass on the current tree**, run directly rather than trusted from a commit message.
   check-landing-next-steps.py's WARN lines line up exactly with the three landing commits the
   range's own text says were healed forward (d470d2be, dbf0fc01, 1bdd55c1, all citing 834db84b),
   which confirms the HEAL ROAD convention was actually used correctly rather than merely claimed.
   Clean.

5. **The merge-repair commit (a99ba2b0) fixes are real and land exactly where claimed.**
   `git show a99ba2b0` confirms: the "Alexander" comment in `scripts/wind-down.py`'s SCOPE
   docstring is replaced with "the project's owner", and `check-shipped-language.sh` finds zero
   offences on the current tree; `signal_worker()` gained a `cleanup_notice.cleanup_notice(...)`
   call on the "stopped" outcome path, and `check-cleanup-notice.sh` passes. `scripts/wind-down.py`'s
   `build_ancestor_set()` and `signal_worker()` were read directly: the self-guard walks
   `os.getpid()`'s own ancestor chain via `ps -eo pid=,ppid=` and refuses to signal any pid found
   there, reporting it as still-open rather than silently skipping or force-killing it. The
   accompanying `tests/test_wind_down.py` spawns a real live `sleep 60` subprocess, confirms it is
   actually killed on the green path, confirms a red push gate withholds the push rather than
   bypassing it, and confirms a worktree locked under the *test's own* pid (an ancestor of the
   wind-down subprocess it spawns) is left running — this is a real, live-process proof of the
   self-guard, not a mocked one. Clean.

Blocking: none

Finding 1 (the unwired dialog-warning-guard.py) is disclosed here for the orchestrating session's
attention rather than held blocking: the row's written acceptance did not ask for installation,
the gap is stated honestly in the shipped code's own docstring, and the closest precedent in this
board's own history (q-567) treated "wired everywhere it needs to run" as its own separate row
rather than folding it into the row that first proves the mechanism. Whether q-581 needs a sibling
installation row, the way q-567 got one, is a board-shape question, not a defect in this range's
code.
