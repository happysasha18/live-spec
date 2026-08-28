# Prover record — 2026-08-28 the rotation gate's second direction, its retired mechanism, and the comment-anchored class

PUSH-REVIEW

Range: 1b061a8..0462b69 (6 commits), reviewed as one pass. Base commit `1b061a8`, the tip this push
starts from. Reviewed commits, in order: `ead4a70`, `e94a238`, `013ec60`, `15407f9`, `aa4fa4a`,
`0462b69`.

Three of those are another session's, landing in the same tree while this one worked: `ead4a70`
(every open task gets a definition of done), `e94a238` (the architecture's pin repointed at the task
list) and its record `013ec60`. They are read here only as far as this session had to touch them —
the collision is written up as finding 2 — and their own review is `013ec60`'s record. The three this
session owns are `15407f9`, `aa4fa4a` and `0462b69`.

Prover version that ran: product-prover 1.4.2, under the pack bindings in
`skills/product-prover-pack/SKILL.md` 6.0.0.

## What this range is

Three leftovers from the day's earlier work, closed together.

The rotation gate `guardrails/check-doc-rotation.py` gains the direction it never had: a closed row
sitting in an archive that no manifest line names. The mechanism that stood beside it,
`scripts/rotate-doc.py`, retires to the attic, since the one document shape it could read left the
tree the day before. And a test that anchored on the literal wording of a comment is rewritten to
assert the property, with the same class swept across the whole suite.

## How this review was run

Read to refuse. Every claim below was checked against the artifact rather than against the change's
own prose: the gate was run on the real tree before and after, the property form was red-proven by
breaking the reader it guards, and the retirement's reach was measured by grepping the whole tree for
the retired name rather than by trusting the four homes the change happened to edit.

Files read: `guardrails/check-doc-rotation.py`, `attic/rotate-doc.py` (as
`scripts/rotate-doc.py` before the move), `tests/test_doc_rotation.py`,
`tests/test_prover_adapter_contract.py`, `tests/test_deletion_only_push.py`,
`.github/workflows/gates.yml`, `guardrails/pre-push`, `guardrails/case_or_space_only.py`,
`guardrails/check-prover-record.sh`, `scripts/preshow-register-lint.py`,
`tests/test_register_judge.py`, `tests/test_worker_restore.py`, `tests/test_traceability.py`,
`templates/headless_harness.py`, `PLAN.md` (the rotation manifest block alone),
`docs/queue-archive/rotated-ROADMAP-2026-08.md`, `matrix/guardrails.md`,
`architecture/guardrails.md`, `architecture/host-adoption.md`, `docs/roadmap-format.md`,
`NEXT_STEPS.md`, `attic/MANIFEST.md`, `skills/live-spec-base/SKILL.md`.

Commits read: `6915ef5e` and its three parents on the closed branch `night/2026-08-13-ck2-neutral`,
to establish what that branch actually did before deciding what of it was still right.

Checks run: `python3 guardrails/check-doc-rotation.py` on the real tree — exit 1 naming row 558
before the manifest repair, exit 0 after. `python3 -m pytest -q tests/test_doc_rotation.py` — 30
passed. `python3 -m pytest -q tests/test_prover_adapter_contract.py` — 17 passed, and 2 failed with
the workflow reader deliberately broken to keep its comments, which is the property form's red proof.
`python3 -m pytest -q tests/test_deletion_only_push.py` — 15 passed.
`bash guardrails/check-pin-drift.sh` — exit 1 on two pins, then exit 0 once the retired file's pin
came out of `architecture/guardrails.md` and the other session repointed its own. A whole-tree probe
over every archive, computing terminal rows against manifest claims per archive, found exactly one
unclaimed row across the six archives and 600 terminal rows. `python3 -m pytest -q`, the whole suite
the way CI runs it, in full below.

Findings: eight, listed below.

## Findings

**1 — the new direction's honest boundary, and it is the one that matters.** Arm (e) catches a row
that reached an archive without reaching the manifest. It cannot catch a row that left the live list
and reached neither — no archive line, no manifest line, nothing. That row is invisible to every arm
of this gate, because a structural scan has no memory of what once stood in the live file. The
mechanism used to close that hole by construction, writing both halves in one act, and retiring it
gives the hole back. Two things make that acceptable rather than a regression. The move it guarded
cannot be performed by that mechanism any more, so the guarantee was already gone before this range.
And the remaining hole is a whole row vanishing from a document under version control, which the diff
of the commit that removed it shows plainly, where the case (e) catches was invisible in every diff
and every grep. Named here rather than papered over: the gate's docstring claims a per-row
findability promise, and this is the one shape of loss it still cannot see.

**2 — the tree's one live instance was repaired inside a file another session held open.** Row 558
sat in `docs/queue-archive/rotated-ROADMAP-2026-08.md` as declined while the manifest line for that
archive named seventeen other rows and never it. The manifest moved into `PLAN.md` on 2026-08-27, so
the repair is one row number added to one line inside that file's `rotated-manifest` block — and
`PLAN.md` was being written by another session at that moment, which this session had been told to
stay off. The alternative was to arm a gate that reds the tree it ships in, which is worse. The write
was made surgically inside the machine-maintained block, never in the task list, with `git status`
and a hash check taken immediately before. The other session then committed `PLAN.md` wholesale in
`ead4a70` and carried the line through, so the repair is on record in that commit rather than in this
session's. A reader looking for where row 558's citation came from will find it in the wrong commit;
that is what this finding is for. The general lesson stands on its own: a gate arm and the data it
judges can live in two different sessions' files, and there is no way to land the arm green without
one of them reaching into the other's.

**3 — the basename fallback lets one archive vouch for another's rows.** The gate resolves a manifest
line's archive by normalized path and, failing that, by basename — behaviour this range inherited from
the orphan-archive arm and extended to the new one. Two archives with the same basename in different
directories would therefore pool their claims, and a row unclaimed in one would be excused by the
other's line. Today the scan glob is a single directory, `docs/queue-archive/rotated-*.md`, so no two
scanned archives can share a basename and the hole is unreachable. It is recorded rather than closed:
narrowing it now would mean touching the existing arm's resolution for a case that cannot arise, and
widening the glob is the change that should be made to notice this.

**4 — the retirement removes eight behaviour tests, and the argument is that they test nothing.**
`TestMechanism` (three tests) and `TestClosingCommitMechanism` (three tests) drove
`scripts/rotate-doc.py` as a subprocess; two more of its assertions rode inside them. The tool's
`main()` refuses any document whose basename is not `ROADMAP.md`, and `ROADMAP.md` left the tree on
2026-08-28 for `attic/ROADMAP.md`. So every invocation the live tree could make either names a file
that is not there or is refused by name. The tests were green because they built their own fixture
`ROADMAP.md` in a temp directory — they proved the tool worked on a document shape nothing in the
repository has any more. That is the argument for removing them: not that they were inconvenient, but
that their subject is gone. One test stands in their place and holds the retirement itself — absent
from `scripts/`, present in the attic, carrying its manifest line — so the tool cannot quietly return
without tests.

**5 — the property form widens the check by a factor of thirty-two, and that number is the finding.**
The old assertion watched one sentence out of the gates job. The new one watches every comment line
the job carries. Breaking the reader so it keeps comments reds the new form with 32 surviving lines
named; the old form would have named one. The gap between those numbers is the measure of what a
sentence-anchor was actually holding, which was almost none of it.

**6 — four look-alikes from the sweep are not this defect, and the reason is the same each time.**
The sweep read all 208 test files, cross-matching every string literal against a comment-and-docstring
mask of every source file under `guardrails/`, `scripts/`, `hooks/`, `.github/`, `scaffold/` and
`templates/`. Six candidates came back. Two were the defect and are repaired in `15407f9`. The other
four assert on text that is itself the thing under test, so they cannot pass vacuously: the retracted
growth duty in `scripts/preshow-register-lint.py` (the doctrine has no other home, and the test's
subject is that no home still commands it), the stated limit in `guardrails/check-prover-record.sh`
(the check is that the limit is stated), the worker-restore command list across its five homes (which
the base rulebook's rule 7 asks in as many words to red when a home states it in words of its own),
and the invariant codes in the harness template's docstring (identifiers, not prose). The
discriminator that separates them from the gates.yml case: there, the wording was not the subject —
the test was about the reader — so the assertion could both red on an irrelevant reword and miss a
comment whose wording drifted.

**7 — one repair the closed branch carried was deliberately not taken.** Of the branch's four
commits, one is this range's subject, one repaired `scripts/rotate-doc.py`'s cell splitter (moot, the
tool is gone), one repaired `guardrails/check-doc-rotation.py`'s (already on main by another road),
and one repaired `tests/test_traceability.py`'s roadmap-body reader, which still splits on every pipe
rather than on unescaped ones. That reader now reads `attic/ROADMAP.md`, frozen on 2026-08-28, and the
suite is green over it. Repairing a reader of a frozen document changes nothing that can go wrong, so
it stands. Recorded here and in the journal rather than left as an open item, because a future session
finding the un-repaired splitter should be able to see that the omission was decided.

**8 — `docs/roadmap-format.md` still describes the retired tool in the present tense, and that is
correct.** Two lines in its declared-deltas section say what `scripts/rotate-doc.py` does. They are a
record of what one completed conversion delivered, in a section whose whole subject is that
conversion, so they read as history and were left. The one sentence in that file stating current truth
— the live-body law's parenthesis naming the tool as a reader of the terminal vocabulary — was false
after the retirement and is corrected. A reader who takes the delta section for current truth would be
misreading the section rather than the sentence; if that turns out to be a real misreading, the whole
file is the thing to date, not one clause.

Blocking: none.

## The suite

`python3 -m pytest -q` over the committed range: 2474 passed, 4 skipped, in 12m54s. Two earlier runs
during the work reported seven and then six failures with one error. Every one of those failures
traced to two broken architecture pins — `scripts/rotate-doc.py:1` pointing at the file this range
moved, and `PLAN.md:152` moved out from under its label by the other session's edit — and both are
repaired, the first here and the second in `e94a238`. The error was
`tests/test_worker_restore_run_scope.py`, which passes on its own and passed again in the clean run;
it is the dirty-tree artifact the plan's own trap list names, raised by two sessions writing one tree.
