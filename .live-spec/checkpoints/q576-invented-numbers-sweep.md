# q-576: every invented number found and fixed or honestly labeled
Status: open
Owner: director

## DONE

Worker finished, 4 commits, tree clean. Verified by hand, not taken on its word: config-health blocker it left (4 hooks drifted from ~/.claude/hooks/) - installed via scripts/install-pack-hooks.sh + scripts/install-session-hooks.sh + a direct copy for the 2 opt-in library files neither installer covers, now clean. Shipped-language gate red from my own earlier commits (PLAN.md:214, state-probe.sh:82 - Cyrillic without a clean user-language marker / needless Cyrillic in a code comment) - fixed, gate green. Pin-drift: 174/174 green, confirmed. Result: 6 removed (dead/invented/stale-duplicate), 12 really grounded, 27 honestly labeled and left open, 4 out of write-scope (product-prover, external clone), 3 of the 9 unsure were not thresholds at all.

## IN PROGRESS

One opus worker (Agent tool, spawned 27.08 23:42, this session) is going through the 45+9 findings file by file: grounding with a real source where one exists, deriving a principled default where possible, removing the one confirmed-dead entry, honestly labeling the rest as ungrounded engineering defaults where neither applies. As of 28.08 00:00: 18 files touched uncommitted, 6 commits already made.

## NEXT

Fixed on this session's own responsibility (his word: machinery, don't ask, decide yourself): all six fabricated decision-dossier-2026-08-15.md citations replaced with honest pointers to the real work/2026-08-15-unowned-numbers.md record; values left unchanged. 27 other honestly-labeled ungrounded numbers remain open, lower stakes, listed in PLAN.md Blockers. q-576 stays 🔄, not ✅ - real, non-trivial remainder, not a rubber stamp.

## DECISION SHEET

Goal: resolve the 45 ungrounded numeric thresholds an audit found (scripts/guardrails/hooks/templates, JSON configs). Known: audit tally is 45 ungrounded, 15 grounded, 9 unsure (see PLAN.md Blockers, 27.08). Specialist: one opus worker, spawned 27.08 23:42 from this session (Agent tool, no separate process id visible outside this chat until now), still running as of 28.08 00:00 — 18 files touched uncommitted, 6 commits already made and not yet pushed. Risk: none of this was visible to any other window until this checkpoint — director's own execution rule (open a checkpoint before the first specialist is called) was skipped for this and the two shorter opus consults earlier tonight; this is the fix, and the standing gap is recorded in PLAN.md Blockers. Evidence of done: PLAN.md's own audit tally re-run at 0 ungrounded/0 unsure, or each remaining one honestly labeled with a reason it can't be grounded, all tests green, q-576 itself flips to done only after this session reviews the worker's actual diff, not on the worker's own say-so.
