# Prover record — 2026-08-17 the slimming packet and its architecture pin renumber

PUSH-REVIEW

This record covers the integration of the three-commit slimming packet onto `origin/main`, and the
repair the review demanded of it. The packet moves reference material out of three skill bodies
without rewriting a word of it, so `ARCHITECTURE.md` had to follow the text with new line numbers.
That renumber is what obliges this record: `M-6`/`INV-116` want the prover pass to cover the
architecture, and the packet as it arrived carried none.

Range: 9efe559..2139bad (base 9efe559, the remote head; four reviewed commits listed below; this
record's own commit follows them and touches `docs/prover/` alone, which gate a exempts because a
record cannot name the commit that first ships it)
- 2139bad The census keeps the three untouched entries as the last landing recorded them
- cb26b70 communicator: the rule histories move to references, word for word
- 88c4622 build-pipeline: five reference sections move out of the body, word for word
- 5295b06 live-spec-base: the glossary and the worked examples move to references, word for word

Files read: `ARCHITECTURE.md` in full and its diff line by line; the three bodies
`skills/live-spec-base/SKILL.md`, `skills/build-pipeline/SKILL.md`, `skills/communicator/SKILL.md`
before and after; the eight new reference files `references/glossary.md`,
`references/worked-examples.md`, `references/architecture-step-detail.md`,
`references/footprint-read.md`, `references/lanes-and-pen.md`, `references/mockup-first-entry.md`,
`references/verify-step-detail.md`, `references/rule-histories.md`, and the grown
`references/delegation-protocol.md`; `guardrails/rule-census.json` against its 9efe559 copy entry by
entry; `guardrails/node-file-cap.json`; `guardrails/check-prover-record.sh`,
`guardrails/check-config-health.sh`, `guardrails/check-tests.sh`, `guardrails/check-pin-drift.sh`;
`tests/test_guardrails.py` `TestGateA_ProverRecord` and `TestGateB_Tests`;
`tests/test_progress_report.py`; `tests/test_worker_restore.py`; `docs/prover/README.md`.

Checks run: `check-pin-drift.sh` — exit 0, 207 pins proved (65 line pins against their own line, 136
file-level, 6 unlabelled) plus 53 r5 range pins; the five architecture test files
(`test_architecture_format`, `_pins`, `_prove_seam`, `_proved_at_full_pass`,
`_redesign_owes_rework`) — 24 passed; `check-skill-loadability.sh` — exit 0, 11 skills;
`tests/test_rule_census_ratchet.py` — 8 passed; `check-doc-findings-bound.py` (gate aa) — exit 0,
137 live documents, 26 held at zero, none above its record; the focused integration set of twelve
files — 381 passed, 1 failed, 2 skipped; `python3 -m pytest -q tests/ --deselect
tests/test_guardrails.py` — **2,396 passed, 3 failed, 53 skipped, 78 deselected, 1 error** in 3
minutes 19 seconds; `tests/test_guardrails.py` alone — **76 passed, 2 failed** in 20 minutes 46
seconds; and a word-for-word audit of the move itself, described under Findings.

Findings: one blocking, closed below, and five notes. The move's central claim — that the text
travels unchanged — was tested rather than taken on trust. Every `.md` file under each of the three
skill directories was concatenated at 9efe559 and again at cb26b70 and compared as a word stream:
of 504, 501 and 461 sentences of eight words or more, the handful that did not survive a literal
match all proved to be my own splitter joining a heading across the seam where a section was cut,
and each was then found present verbatim by fragment search. No sentence of the moved material is
lost or reworded. The three bodies fall 56,083 to 52,466, 64,143 to 52,432 and 45,861 to 44,881
bytes; the eight new files hold 22,090 bytes; the code route, base plus build-pipeline, falls
120,226 to 104,898 bytes.

Blocking: two, argued in full below.
- closed: 2139bad returns the three untouched census entries to the values 9efe559 recorded.
- stands: the three changed skills carry no skill-creator review record, so gate s reds. That review
  is a pass this record cannot perform for itself, and it is owed before the range can land.

1. **The census recount rewrote three entries the packet never touched.** In 5295b06 the rebuild of
   `guardrails/rule-census.json` carried three files' byte counts along with it: `PRODUCT_SPEC.md`
   702,954 to 703,125, `TEST_MATRIX.md` 484,277 to 484,267, and
   `docs/audits/2026-08-07-number-census.md` 31,991 to 32,027. None of the three is edited anywhere
   in this range. Their drift belongs to an earlier landing, and a slimming packet silently
   restating another change's numbers puts them beyond the reach of whoever owns them.
   closed: 2139bad returns exactly those three `bytes` fields to their 9efe559 values and nothing
   else — three lines, the entries then byte-identical to the base copy field by field. The ratchet
   and gate aa are green over the restored file.

2. **The three changed skills owe a skill-creator review record, and the packet brought none.** Gate s
   (SPEC INV-208) holds that a substantively changed skill carries a committed record under
   `docs/skill-review/` whose verdict is at least as new as the skill's own last change. All three
   bodies this range edits are named: `build-pipeline` last changed in 88c4622, `communicator` in
   cb26b70, `live-spec-base` in 5295b06, and no record covers any of them. Moving text out of a body
   into its references is not the version-stamp bump the gate exempts by construction.
   stands: the fix the gate names is to run the skill-creator review over each changed skill and
   commit its verdict. That is a review pass, not an edit, and writing three verdicts I did not
   obtain would be inventing the evidence this whole record exists to refuse. The range does not land
   until those three records exist.

## What the push gate said, run in full

`bash guardrails/pre-push < /dev/null` over this tree at 434f1b9: **PUSH BLOCKED**, 1,496 seconds,
29 gates. Four reds, and they are not one class:

- **gate a** reddened on THIS record, and the defect was mine. The blocking field read
  `Blocking: one, closed in 2139bad.` as a lone line, and the gate's parser reads the field only as
  far as the first blank line and wants the literal token `closed:` or `stands:` in what it finds.
  My own check had run `check-prover-record.sh` without `--push`, which never reaches that arm, so I
  certified a shape the real gate rejects. The field is now bullets directly under it, the shape the
  house already used.
- **gate s** reddened on the three missing skill reviews — blocking finding 2 above.
- **gate b** reddened on five tests. Four are machine-local and reproduce identically at the base
  9efe559 in a second worktree: `test_config_health` twice, `test_judge_listed` once — that one reds
  because six judges declared wired to Stop and UserPromptSubmit are absent from this machine's
  `~/.claude/settings.json` — and the worker-restore transcript gate. The fifth,
  `TestGateB_Tests::test_real_content_passes`, also reds at the base, and reds there for the same
  single inner test. None of the five is this range's work.
- **gate m** reddened on the same machine state from the other side: the installed copies of the
  three slimmed skills, plus a `chat-law-hook.sh` hook drift that predates this range entirely.

The four machine-local reds have no documented road past them. The repository's own written remedies
are repairs, not bypasses: `scripts/sync-skills.sh` and `scripts/install-session-hooks.sh` write into
the owner's `~/.claude`, and the worker-restore counting start moves only on a recorded finding and
only as far as that finding requires — which this one does not need, since it ages out of the gate's
24-hour window on its own. `docs/push-law.md` states the governing rule: loosening a gate takes a
recorded profile entry, never a silent skip. `--no-verify` appears in `NEXT_STEPS.md` as a way to
avoid paying for the same 25-minute chain twice on a green verdict, not as a road past a red one.

Notes:

- **`ARCHITECTURE.md`'s change is 33 lines and all 33 are pins.** Every changed line is a
  `skills/*/SKILL.md:NNN` pin following its text to a new line number; no prose, no node, no
  invariant moved. Gate g proves each of them lands on its own line within tolerance.
- **Two suite reds predate this range and are not its work.**
  `tests/test_worker_restore.py::TestTheGateIsArmedWhereItSaysItIs::test_the_gate_runs_against_this_machines_own_transcripts`
  reds on a `git stash push -u -q` and a `git checkout --` run by agent `ac85659f` in
  `/private/tmp/live-spec-slimdown/wt` at 2026-08-17T15:33Z and 15:54Z — yesterday's builder, not a
  tree this range touches. stands: it is a true finding against the machine's transcripts, owned by
  whoever answers for that run, and no edit in this range can clear it.
- **`TestGateB_Tests::test_real_content_passes` is pre-existing, and was measured to prove it.** A
  second worktree was cut at the base, `git worktree add … --detach 9efe559`, and the same node run
  there alone: 1 failed, 1 passed in 8 minutes 5 seconds, the failure identical and resting on the
  same single inner test as above. stands: the node reds at the base as it reds here. The two
  scratch runs are also the whole of the file's 20-minute cost — each copies the repository and runs
  the full 208-file suite through `check-tests.sh`; nothing hangs.
- **`tests/test_config_health.py` reds on installed-skill drift, and this range caused it.** The
  gate diffs `skills/<name>/` against `~/.claude/skills/<name>`, and this packet slims exactly the
  three skills it names. stands: the prescribed repair, `scripts/sync-skills.sh`, writes outside the
  repository into the owner's own configuration. That is the owner's word to give and it is
  escalated, not taken here.
- **The suite rewrites `docs/PROGRESS.md` where it runs.** `tests/test_progress_report.py` executes
  `scripts/progress-report.py` with the repository root as its working directory, so any full run
  leaves the generated page modified in that tree. The behaviour predates this range — the test
  stands unchanged at 9efe559 — and the file is left as the run wrote it rather than restored by a
  discarding command. The single suite error, a leaked `/tmp/livespec-test-suite-log.*`, was my own:
  two pytest sessions ran at once and the session-scoped no-trace fixture of one saw the temp file
  of the other. It is an artifact of how I ran the suite, not of the change.
