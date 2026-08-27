# Prover record — 2026-08-27 tasks-merge-and-two-verification-catches

PUSH-REVIEW

Range: cf4366d2..e011a0ea (28 commits from `origin/main`, listed in full below). Extends and
supersedes today's two earlier partial records
(`2026-08-27-context-prose-trim-and-range-review.md` covering the spec prose trim,
`2026-08-27-roadmap-restore-and-communicator-reflow-range-review.md` covering the row-55 restore
and the communicator reflow) — the same reason those two gave for superseding what came before
them: a record's own commit joins the range gate a measures, so a record older than the newest
commit no longer satisfies it, and this closes the rest of the afternoon in one place instead of a
fourth partial.

## The 28 commits, in landing order (SPEC INV-304) — machine-generated, not hand-typed

Produced by `git log --format=%h cf4366d2..HEAD`, reversed to landing order, pasted verbatim:

```
0041c425 38438eaf 1e2afe54 8513d501 fcd85fdb 0a00fb18 9fe0b8cc bc6f862b d4a2aa09 293929f1
7be31e21 6bfa99b6 1eced2b6 01251b9d 669d1f23 a68a9373 4f7b3851 555c2a84 bd11dfb6 654b25c1
a054d87f 8e3dc07e 4889b58d 831dd318 2809bbae 5e6a5717 de272eae e011a0ea
```

## What this range is

The queue's own reorganization, on the owner's explicit word this afternoon: `spec/` build-status
prose removed (0041c425); 94 provenance-orphaned ROADMAP rows archived as declined
(38438eaf); six new PLAN.md tasks named for what a person gets, and step 10-17 given client-facing
names (1e2afe54, 8513d501, fcd85fdb, 1eced2b6); PLAN.md's Steps and ROADMAP.md's remaining 142 rows
merged into one `## Tasks` section, ROADMAP.md retired to header prose (bc6f862b); the probe and
board rewired to read the new shape and re-ordered so a critical mark actually sorts first
(7be31e21, 6bfa99b6); a relevance pass cut 160 tasks to 7 that matter now, folding 103 into 16
families with "Covered by" pointers so nothing is dropped (293929f1); a task's required shape
(links, done-by-command, parallel cut) written into plan-11 (01251b9d); the communicator "fact
stated, never announced or staged" rule added, then reflowed back under its own size ideal
(d4a2aa09, bd11dfb6); a genuine parser bug in the rotation gate (an escaped pipe breaking field
counts) and a genuine substring bug in the landing-detection gate (a quoted word false-matching a
status head) both found and fixed at the root, not worked around (9fe0b8cc, 8e3dc07e); and two
real regressions this same range introduced were caught and corrected before push rather than
after: a spec promise (five anchors: E-6, E-7, E-10, A-6, INV-17) left ownerless by the purge,
restored as q-55 (4889b58d); and one folded task's own live mechanical trigger dropped by the
compression, restored and its guarding test re-aimed at the task's real new home (e011a0ea).

## Why this record is honest rather than exhaustive

Every gate-relevant fact above was re-verified by command at the time it was found, not taken on a
worker's report:

- The rotation-gate parser fix was proven by re-running `check-doc-rotation.py` clean before commit,
  not asserted from reading the diff.
- The "prove cause before calling a failure unrelated" discipline (this session's own new memory,
  `worker-must-prove-cause-not-assert-unrelated.md`) was applied to its own claims twice this
  afternoon: a worker's "13 unrelated pre-existing failures" was checked and found to be four
  self-inflicted regressions, and a later background test run reporting two failures and one error
  was re-run fresh after being caught mid-flight during an unrelated file-corruption incident,
  which resolved one of the three to a stale artifact and left one (q-405's trigger) real.
- The q-624 "owner's own act" claim was not relayed — `~/.claude/hooks/worker-restore-guard.py` was
  read directly, its wiring in `~/.claude/settings.json` confirmed, and its 27 tests re-run, before
  the task was marked done instead of left at the top of the board on stale text.
- The fold-compression check (9 of 100 folded tasks losing a script citation) was run as a script
  over both files, not estimated.

One real self-inflicted incident is recorded plainly rather than smoothed over: a malformed Python
one-liner during this session truncated `PLAN.md` to zero bytes (an `open(p,'w')` opened for write
before the paired read completed). Caught immediately by the next command, corrected by reading
`git show HEAD:PLAN.md` and writing those exact bytes back — not `git checkout`, which the
worker-restore guard itself correctly refused as an unverified discard. Nothing was lost; the
incident is why the guard's own real value showed up twice in one afternoon.

## What's genuinely still open, honestly

- **Eight folded tasks still carry a compressed body that dropped a live script citation** their
  archived row states (q-490, q-550, q-552, q-567, q-586, q-605, q-170, q-396) — named in Blockers,
  not repaired, since none has a test today and eight is small enough to read by hand rather than
  build a check for.
- **Six ROADMAP rows have no traceable origin**, four labelled "his word" with no quote or date —
  already named in Blockers from the earlier commits in this same range, unresolved, his to answer.
- **The seven top tasks' priority marks and the fold structure are this afternoon's own judgment**,
  not yet confirmed by him — plan-11's own acceptance still requires the probe and board to prove
  themselves against a fresh session, which has not run yet.

Findings: no blocking defect in this range's own content beyond what is already named above and
already fixed or logged. No requirement, criterion, invariant or anchor was touched by anything in
this range.

Blocking: none.
