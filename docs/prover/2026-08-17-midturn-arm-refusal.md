# Prover record — 2026-08-17 the tool-boundary chat arm

REVIEW-PASS

This record carries no push range. It is the adversarial read that REFUSED the repair attempted on the
mid-turn chat arm, kept because the refusal is what decided the arm's retirement and the reasoning
belongs beside the change that followed it.

Range: none — the reviewed change stood uncommitted in the working tree at base `f9eaecc`.
Files read: `hooks/midturn-chat-scan.py`, `hooks/turn_reader.py`, `hooks/chat-law-hook.sh`,
`tests/test_midturn_chat_scan.py`, `guardrails/check-hooks-can-fire.py`, `guardrails/hook-red-proofs.json`,
`guardrails/judge-hooks.json`, `guardrails/hook-red-fixtures/midturn-chat-scan/payload.json`,
`.live-spec/PROBLEMS.md`, `docs/PROGRESS.md`, `docs/prover/README.md`, `TEST_MATRIX.md` row M-461,
`ROADMAP.md` rows 537 and 543, `ARCHITECTURE.md:418`, `scripts/install-pack-hooks.sh`, the installed
hooks and settings under `~/.claude/`, the hook's own state files under `~/.claude/hooks/.midturn-chat/`,
and the session transcripts under `~/.claude/projects/` for the two recorded incidents.
Checks run: `pytest tests/test_midturn_chat_scan.py` — 34 passed, being the file's 31 tests plus the three the repair added; `check-hooks-can-fire.py` — exit 0;
the same hook fed the reconstructed live worker payload — deny emitted, exit 0; two mutation runs, one
deleting the guard's `subagents` branch (34 passed, gate exit 0 — the branch proved nothing) and one
deleting the guard entirely (2 failed of 34); `check-language-rules.py`, `check-shipped-language.sh`,
`check-judge-listed.py`, `check-named-checks.py`, `check-every-gate-can-fail.py`,
`check-matrix-reference.py`, `check-tree-counts.py` — all exit 0; `check-config-health.sh` — exit 1 on
drift in `guardrails/pre-push` and eleven skills that predates this change; a census over `~/.claude/projects` counted by
RECORD SHAPE rather than by text search — a record whose tool result opens with the scan's own refusal
line — giving 108 refusals delivered in all, 76 of them into a worker's tool result across 68 worker
transcripts, between 2026-07-27 and 2026-08-16. A text search over the same tree answers a different
question and a larger number, since a transcript of an agent READING about the refusal carries the same
words; the reviews of this change added several while it was under way.

Findings: three blocking, listed below, plus notes.

Blocking:

1. **The repair did not repair the fault.** stands: the change is abandoned and the arm retired instead.
   The guard stood the hook down unless the transcript's filename proved the call was the seat's. On this
   harness a worker's PreToolUse event carries the SEAT's `transcript_path` and the SEAT's `session_id`,
   so the guard read true and the worker was denied exactly as before. The reviewer rebuilt the
   2026-08-16 event from the transcripts and ran the fixed hook against it: it emitted its refusal. The
   corroborating counts are independent of that reconstruction — every one of the 31 state files the
   hook has written is named for a seat session and none for an agent, while 68 worker transcripts hold
   76 delivered refusals. A later probe closed the last door: a worker process carries the seat's
   `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID` unchanged, so the environment separates the two no better
   than the event does.

2. **The problems row claimed SOLVED on an unverified mechanism.** closed: the row now records the
   retirement, names the 2026-08-16 repair as illusory, and carries the review's counts.

3. **The hook comment replaced one false line with another.** closed: the comment now states the
   retirement, and states that the line read "stays off" from 2026-07-30 while the hook was wired and
   firing.

Notes, all closed by the retirement or carried forward:

- The guard's `subagents` branch was dead code no test distinguished. Gone with the arm.
- The test renames that accompanied the repair were forced rather than cosmetic: under the guard,
  `test_ordinary_russian_passes` would have asserted "not denied" vacuously. The test file is deleted
  with the arm, so the point stands only in this record.
- A third worker-transcript layout exists that the guard's docstring did not name,
  `<session>/subagents/workflows/wf_<id>/agent-<id>.jsonl`. Moot once the arm is retired.
- `TEST_MATRIX.md` row M-461 was stale before this change and is now rewritten as retired.
- `ROADMAP.md` row 543 said the script "sits disabled" carrying `exit 0` on line 2 of the installed
  copy. It carried no such line and was firing. The row is corrected and now covers the two scripts
  that do.
- `docs/PROGRESS.md` carries regenerated churn from the night before this work and rides along
  uncommitted; it is left out of the retirement commit.
- `tests/test_config_health.py` holds two reds on installed-versus-source drift in `pre-push` and
  eleven skills. They fail identically against `HEAD` with this change stashed, so they predate it and
  are untouched by it.

---

## Second pass — the retirement itself, also REFUSED, then repaired

The retirement that followed the refusal above was read by a second adversarial reviewer and refused on
ten blocking findings. The wiring side was clean; the prose side was not. Every finding is closed below,
and each closure names what changed.

Blocking:

1. `PRODUCT_SPEC.md` R230.6 still required the retired arm to read through the shared reader, against
   R295.1 requiring it not to exist. closed: the tool-boundary scan is out of that criterion's list.
2. `ARCHITECTURE.md` contradicted itself inside one sentence — "six checks read through" with a
   five-name list. closed: the count word is corrected, and `tests/test_architecture_pins.py` grew a net
   that reads the number itself, proven red against the six-word text and green against five.
3. `ARCHITECTURE.md` INV-285 still described the arm as live. closed: it names the retirement and says
   the pack wires no hook to PreToolUse today.
4. `docs/onboarding-and-settings.md`, the human-facing setup page, sent a new host after a hook that no
   longer ships and stated ten wired hooks against eight. closed: counts and text corrected.
5. `scripts/install-session-hooks.sh` carried the same stale counts in a file this change had edited.
   closed: eight and six throughout.
6. `guardrails/judge-hooks.json` stated "every one of the ten today" against a map of eight. closed.
7. `hooks/code-anchor-scan.py` justified its fragment/context split by a caller now in the attic.
   closed: the docstring names the retirement and why the split still earns its place.
8. The one law fully disarmed by the retirement was still published as armed: r72 read `status: armed`
   with every catcher absent. closed: `stated-only`, the retirement written into its notes, and the
   catcher's reach put in the past tense. The generated pages were rebuilt from the source.
9. The headline number was wrong. "77 stoppages" was a count of files matching a text search, and that
   search counts a transcript of an agent READING about the refusal. closed: counted by record shape —
   108 refusals delivered, 76 into a worker's tool result across 68 worker transcripts, 32 into the
   seat's own across 19 — and the method is now stated wherever the number appears.
10. Over-deletion: `tests/test_measurement_carries_method.py` held five tests, and only one touched the
    arm. The other four guarded the measurement law's PROSE homes, which this same change rewrites, so
    deleting them would have left that law with no machine and no net at once. closed: the four stand in
    `tests/test_measurement_law_homes.py`, with a fifth asserting the rewritten homes promise no machine.

Notes from the same pass, closed: the stale PreToolUse fixture comment in `tests/test_judge_listed.py`;
the retired arm's entry in `tests/test_architecture_pins.py`; `ROADMAP.md` row 537's drift list; the
orphaned `guardrails/measured-number-fixtures/` pair, retired to the attic with its manifest line; the
deleted test file named in `work/2026-08-15-unowned-numbers.md`; the `turn_reader.py` example in
`guardrails/judge-hooks.json`'s comment.

Carried forward, not closed here: `.live-spec/r3-rule-fires-2026-08-11.md` D10.4 proposes wrapping the
retired arm in the hook meter. It is a dated working record rather than a live queue row, and it is left
standing as the record of what was proposed that day.

