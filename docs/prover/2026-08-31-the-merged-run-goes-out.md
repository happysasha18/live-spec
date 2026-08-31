# Prover record — 2026-08-31 the merged run goes out

PUSH-REVIEW

Range: 7159fed..c9f8fd6 (27 commits). Base commit `7159fed`, the head `origin/main` carries.
Every commit in the range, in order: `f052ec5`, `4431b7a`, `70bc57e`, `4a90e70`, `69d55c6`,
`1cd1617`, `46dd26a`, `c62fef2`, `d7b1896`, `1caa5c4`, `664dee9`, `0f3ae08`, `84f522c`, `64fbe3f`,
`f6ba125`, `70580bd`, `5107567`, `fc828a9`, `2c624c3`, `b8547fc`, `3ea8bbd`, `6452c4c`, `03acd21`,
`c7c4ab6`, `ef723ed`, `ecb8b81`, `c9f8fd6`.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## Why this record stands beside the one of 28.08

`docs/prover/2026-08-28-four-repair-lanes-merged-and-re-reviewed.md` covers `7159fed..c7c4ab6`, the
range as it stood when that pass ended. Two commits landed after it, `ecb8b81` and `c9f8fd6`, and
the pass that wrote it was cut off mid-sentence while extending its own header to name them. That
half-finished edit sat uncommitted in the tree for three days. It is reverted here rather than
finished: a record cannot honestly claim to have read commits written after it closed, and the
`Range:` header it was editing is the one line the gate reads for the range. So the 28.08 record
keeps the range it actually read, and this record covers the whole of what is being pushed, the two
later commits with it.

The push also falls on a different day from the work. The gate's push road wants a record dated the
day of the push, and the honest way to give it one is a review run today over the range as it stands
today. That is what this is: not a copy of the earlier record, but a second pass that re-derived
every landing the earlier one claims, against the merged tree rather than against any lane's prose.

## How this review was run

Read to refuse, on a tree nobody had touched in three days. Every claim below rests on a command run
today and its output, never on a report from the pass that built the work. Two fresh-context
readers with no part in building any of it were dispatched over the same range in parallel, one on
the guard, the lint and the two gates, one on the board's two readers, the archives and the
cross-document facts.

Files read: `hooks/worker-restore-guard.py`, `scripts/preshow-legibility-lint.py`,
`scripts/state-probe.sh`, `scripts/render-board.sh`, `scripts/plan_checks.py`,
`scripts/sync-skills.sh`, `scripts/install-worker-restore-guard.sh`,
`guardrails/check-prover-record.sh`, `guardrails/check-doc-rotation.py`,
`guardrails/check-landing-next-steps.py`, `guardrails/pre-push`, `.github/workflows/gates.yml`,
`tests/conftest.py`, `tests/test_guardrails.py`, `tests/test_listener_tripwire.py`, `PLAN.md`,
`NEXT_STEPS.md`, `matrix/guardrails.md`, `skills/communicator/SKILL.md`,
`skills/live-spec-base/SKILL.md`, `docs/prover/README.md`,
`docs/prover/2026-08-28-four-repair-lanes-merged-and-re-reviewed.md`,
`docs/skill-review/2026-08-28-communicator.md`, and the four archives under `docs/queue-archive/`
named `rotated-PLAN-2026-08-28-*`.

Checks run: fourteen, each with its result.

1. `python3 -m pytest -q`, the whole suite, alone on a clean tree with no other run on the
   machine — 2,556 passed, 5 skipped, 597.76s.
2. `hooks/worker-restore-guard.py` driven through its real hook entry on 31 command strings,
   20 that must be denied and 11 ordinary commands that must pass — 31 of 31 as intended, no false
   pass and no false denial. The denied set covers the shapes the range added: shell grouping
   (`{ …; }`, `( … )`), the `env`/`xargs`/`nohup`/`timeout` launchers, a leading `!`, a `-c`-bearing
   option cluster (`bash -lc`), `eval`, a single `&` as a separator, process substitution
   (`cp <(git show HEAD:X) X`), `find -exec`, `tee`, `dd of=`, an unparseable inline program as a
   sink, and the five git verbs that write the tree themselves.
3. The same guard, live and unasked: it refused this pass's own `git checkout -- <record>` when the
   half-finished edit was being reverted, and named the file-writing route instead. The revert was
   done that way.
4. `scripts/preshow-legibility-lint.py` on four pages built for the question. A page painting `div`
   white above `.card` dark passes, where before the specificity ranking it printed a red no viewer
   can see. A genuinely illegible pair reds. A gradient the text is under the floor at every stop of
   reds against the friendliest stop. A gradient the text clears over part of stands down by name
   for the eye. Exit codes 0, 1, 1, 0.
5. `python3 guardrails/check-doc-rotation.py` on the merged tree — OK, exit 0, every rotated row
   findable and every archive named in a manifest line.
6. `python3 guardrails/check-landing-next-steps.py` over `origin/main..HEAD` — OK, exit 0.
7. `python3 -m pytest -q tests/test_config_health.py`, after both installers ran — 34 passed.
8. `bash scripts/install-worker-restore-guard.sh` and `bash scripts/sync-skills.sh` — the installed
   guard already byte-identical, the wiring already in place, its two self-tests green; every pack
   skill already fresh, and the external prover clone skipped by the fence that owns it.
9. Every gate the CI workflow runs outside the suite and outside the record gate, run here by hand
   against `LIVE_SPEC_DIFF_BASE=origin/main` — matrix reference, pin drift, skill loadability,
   prototype fence, shipped language, broad kill, muted launch, cleanup notice, touchpoint kind,
   board, authority anchor, skill review, doc rotation, generated index, agent card, architecture
   reference. Sixteen gates, all exit 0.
10. The four host checks of gate h — completeness, tests present, traces to spec, conflicts — all
    exit 0 against `origin/main`.
11. `bash guardrails/check-config-health.sh` and `bash guardrails/check-freeze.sh` — both exit 0.
12. `bash scripts/state-probe.sh` and `bash scripts/render-board.sh` — both run clean on the merged
    tree, the board draws all 62 tasks, and the tree stays clean after.
13. A sweep over each of the four lane branches: every line the lane added, longer than a few words,
    looked for in the merged file at `HEAD`. Every line missing is accounted for by a documented
    conflict resolution or by one of this range's own later repairs.
14. `grep` for every pointer at the three renamed archives across the tree, and for the pre-rename
    names — every pointer resolves to a file that exists, and no pre-rename name survives.

Findings: five, listed below. None blocks the push.

**1. The half-finished record edit was reverted rather than completed.** The dirty file carried
`Range: 7159fed..c9f8fd6 (26 commits)` in its header while its own body, twelve lines further down,
still read `Range: 7159fed..c7c4ab6` — one record claiming two ranges, and the wider of the two
covering commits written after the record closed. Reverting restores the record to the range it
read, and today's record covers the rest. The pass's own reason for the edit still stands and is
answered here: the gate does need a record covering `ecb8b81` and `c9f8fd6`, and this is it.
**Closed.**

**2. The two repoints the 28.08 record recorded as already paid really are paid.** Checked by hand
rather than taken from the record: `tests/test_listener_tripwire.py:120` and `matrix/guardrails.md`
row M-412 both name `docs/queue-archive/rotated-PLAN-2026-08-28-q405-agent-messaging-stale-premise.md`,
which exists. A grep across the whole tree for pointers at the four `rotated-PLAN-2026-08-28-*`
archives returns twenty-three, every one resolving to a file on disk; the three synthetic names in
`tests/test_landing_next_steps.py` are its own fixtures and name nothing on disk by design. No
pre-rename name survives anywhere. **Nothing to repair.**

**3. Every landing the 28.08 record claims is in the merged tree, and each was re-derived here.**
The legibility lint ranks painting rules by specificity and stands down by name where a surface is
unresolvable; the worker-restore guard reads grouping, launchers, `-c` clusters, `eval`, the single
`&`, and both process substitutions; the board and the probe both give a done row whose acceptance
key fails the blocked mark and drop it from the done count; the suite's leak check ranges over the
run's own temp root under `RUN_TEMP_ROOT`; the meta-test's digest store carries a `(last red)` key
whose recorded red outranks a green on the same digest. Checks 2, 4 and 12 above are the evidence,
and the three archives carry their index tables and their manifest lines. **Nothing to repair.**

**4. The trimmed legibility bullet keeps the instruction its own tool needs.** `c9f8fd6` cut the
bullet in `skills/communicator/SKILL.md` from 1,279 characters to 966, dropping the account of what
the lint does at each end of a gradient. Checked against the lint's real behaviour rather than
against the commit's claim: a gradient the text clears over part of exits 0 and prints its
stand-down as an info line, so a session reading only the exit code would show a page carrying a
pair nobody has looked at. The sentence that survives the trim is exactly the one that prevents
that — read the verdict line, not only the exit code. The removed half is mechanism, and the lint
says it in its own output at the moment it matters. The removal is accounted for in
`docs/skill-review/2026-08-28-communicator.md`, which ships in the same commit and which
`guardrails/check-skill-review.sh` accepts. **Nothing to repair.**

**5. The two narrownesses the 28.08 record left standing still stand, and one of them is wider than
that record says.** The landing gate's rotation trigger still wants the removal and the archive line
in one commit, so a hand splitting the act across two commits evades it; the rotation gate holds the
nothing-lost half of the same act, and closing the rest means the gate carrying state across
commits. And the suite's leak check now reads one directory, so a test writing to the system temp by
an absolute path is outside its reach — `scripts/state-probe.sh` writes `/tmp/probe-next.txt` at
line 185 and reads it at line 304, and the suite runs that script. That second one has no row on the
board yet, which the earlier record said was the honest place for it. Adding a row is a change to
`PLAN.md` outside the two things a session may edit there, and that very rule is one of the open
questions already waiting for the owner in §Blockers. So it is written here, under its own date,
rather than legislated at a push. **Both stand.**

Blocking: none
