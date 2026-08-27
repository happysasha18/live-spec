# Prover record — 2026-08-27 roadmap-restore-and-communicator-reflow-range-review

PUSH-REVIEW

Range: cf4366d2..2809bbae (21 reviewed commits; two prover-record-only commits inside the range,
669d1f2 and a68a937, and one earlier-record commit that carries the record directory alone, 555c2a8,
need no review of their own). This record supersedes
`2026-08-27-context-prose-trim-and-range-review.md`, whose range trailed the six commits landed
after it (`bd11dfb6` through `2809bbae` below) and no longer covers the pushed head.
- 0041c42 spec: strip build-status narration from Context prose
- 38438ea Purge 94 provenance-orphaned ROADMAP rows on the owner's 27.08 order
- 1e2afe5 Six new steps, on the owner's word of 27.08
- 8513d50 Blockers: what this afternoon established, and what it left open
- fcd85fd Steps 10-17: names a person can read, and two steps he added today
- 0a00fb1 communicator: point rule 9's mark legend at its one canonical home
- 9fe0b8c Rotation gate: an escaped pipe in a row's own text broke field counting
- bc6f862 One list: ROADMAP's 142 rows join PLAN.md's tasks, on his word of 27.08
- d4a2aa0 A fact is stated, never announced
- 293929f Seven tasks matter now; the other 153 stop asking for attention
- 7be31e2 Both readers follow PLAN.md's task-list merge, not the old Steps shape
- 6bfa99b The probe leads with what matters now, across every category
- 1eced2b The seven top tasks say what, why now, and when they are done
- 01251b9 A task carries its links, its done, and its parallel cut
- 4f7b385 Skill review: communicator's rule-9 pointer and the new rule-7 sub-rule
- bd11dfb communicator: reflow the body back under the 500-line ideal
- 654b25c test_report_format: re-aim the legend test at the pointer, not the legend
- a054d87 test_traceability: re-aim two ROADMAP-table checks at PLAN.md's Tasks
- 8e3dc07 check-landing-next-steps: match the archived status's HEAD word, not any substring
- 4889b58 Restore the one row the purge should not have struck
- 831dd31 The manifest stops naming the row that came back
- 2809bba Skill review: communicator's reflow and the dropped contrast frame

The first fourteen (0041c42 through 01251b9) and 4f7b385 were already read in full by the
superseded record; that reading is not repeated here. Findings below cover what changed since:
`bd11dfb6` through `2809bbae`, seven commits.

Files read: `skills/communicator/SKILL.md` full diff `4f7b385..HEAD` (`git show bd11dfb6`, `git show
4889b58d -- skills/communicator/SKILL.md`); `guardrails/check-landing-next-steps.py` and
`tests/test_landing_next_steps.py` full diffs (`git show 8e3dc07e`); `tests/test_report_format.py`
full diff (`git show 654b25c1`); `tests/test_traceability.py` full diff (`git show a054d87f`);
`PLAN.md` and `docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md` full diffs (`git
show 4889b58d`); `ROADMAP.md` diff (`git show 831dd318`); `docs/skill-review/2026-08-27-
communicator-reflow-and-contrast-frame.md` in full, read before writing this line, not merely
committed and trusted; `git diff --stat cf4366d2..HEAD -- PRODUCT_SPEC.md ARCHITECTURE.md spec/
architecture/` and `git diff --stat 555c2a84..HEAD -- PRODUCT_SPEC.md ARCHITECTURE.md spec/
architecture/` to confirm what did and did not touch the guarded documents.

Checks run: `python3 -m pytest tests/test_communicator_body_thinned.py -q` (5 passed — confirms
`bd11dfb6`'s claimed 499-line count and that no wording was cut to reach it); `python3 -m pytest
tests/test_report_format.py tests/test_traceability.py tests/test_landing_next_steps.py -q` (202
passed, 1 skipped — the three fix commits' own suites, and the traceability suite that carried the
two commits the earlier record left `stands:` under Blocking); `python3 -m pytest
tests/test_traceability.py -v -k "roadmap_class_vocabulary or targets_owned_by_open_rows"` (1
passed, 1 skipped — see Findings); `python3 -m pytest tests/test_doc_rotation.py -q` (31 passed —
gate t's own suite, covering the manifest-line fix `831dd318` made); `python3
guardrails/check-doc-rotation.py` (OK — every rotated row findable in its archive, every archive
named in the manifest); `bash guardrails/check-shipped-language.sh` (OK, 0 offences); `bash
guardrails/check-skill-review.sh` (OK — communicator carries a fresh review record, after
`2809bbae` landed).

Findings: this record was specifically asked to review six commits — `bd11dfb6`, `654b25c1`,
`a054d87f`, `8e3dc07e`, `4889b58d`, `831dd318` — plus the skill-review record `2809bbae` that this
same push carries. None of the seven touches `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `spec/`, or
`architecture/` (checked directly with `git diff --stat 555c2a84..HEAD` over those four paths,
which returns nothing); no requirement, User Story, acceptance criterion, invariant, or anchor
changed anywhere in this delta.

`bd11dfb6` rewraps four paragraphs in `skills/communicator/SKILL.md` onto denser lines, 516 lines
down to 499. Read hunk by hunk against the pre-image: every changed line is a line-break move: no
word added, removed, or reordered. `tests/test_communicator_body_thinned.py` confirms the count.

`654b25c1`, `a054d87f`, `8e3dc07e` are three test repairs, each following its own commit message's
stated diagnosis and each confirmed against the code it now asserts on, not against the message
alone: `654b25c1` rewrites the legend test to assert the pointer sentence `0a00fb18` introduced,
which the file itself carries at the cited line. `a054d87f` re-aims two ROADMAP-table checks at
PLAN.md's Tasks section following `bc6f862b`'s retirement of the live table; one check
(`test_roadmap_class_vocabulary`) is left explicitly skipped rather than forced to a vacuous pass,
with a guard that reds if a Class field reappears — confirmed live: `PLAN.md`'s task shape carries
no size-class field, so the skip is honest, not a swept-under-the-rug red. `8e3dc07e` adds
`_is_landed_status`, a head-word check mirroring the OLD-trigger's existing `_live_status` guard,
and a regression fixture for the NEW-trigger sibling of that class — read against the bug it fixes
(a bare "landed" substring inside an archived row's own quoted Done-when text was misread as a
landing move) and against the existing OLD-trigger guard it mirrors; the fix is the same shape, not
a new one invented for this case.

`4889b58d` and `831dd318` restore ROADMAP row 55 as `PLAN.md` task `q-55` and correct the rotation
manifest line accordingly. Cross-checked directly: the row is gone from
`docs/queue-archive/rotated-ROADMAP-2026-08-27-provenance-purge.md`'s table (with a note at the
file's end explaining the restoration and where it now lives), row 55 no longer appears in
`ROADMAP.md`'s manifest line naming that archive, and `q-55` in `PLAN.md` names the same five spec
anchors (E-6, E-7, E-10, A-6, INV-17) the commit message claims. `python3
guardrails/check-doc-rotation.py` reads this state clean.

The earlier record's one blocking item — `test_roadmap_class_vocabulary` and
`test_targets_owned_by_open_rows` red, left `stands:` as out of scope for that pass — is now closed
by these same two commits, not by this record: `a054d87f` turned the first into an explicit skip
(a real design decision, not a fix), and `4889b58d`'s q-55 restoration gives A-6 (and the other four
anchors) an owning row again, which is what the second test checks for. Both are green now, run
directly above.

`2809bbae` is this push's own skill-creator review of communicator's `bd11dfb6`/`4889b58d` changes
— read in full before this line was written. It names one of the earlier review's two open
criticisms as resolved (the line count) and states plainly that the other (overlap with the
"honestly / no sugar-coating" bullet) still stands, untouched by either commit. A review record
naming an open problem honestly is the shape gate s exists to require, not a defect in itself, and
adds no new risk of its own.

Blocking: none.
