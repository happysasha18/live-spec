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
Blocking: three, named here and argued in full below.
- stands: the repair did not repair the fault, so it was abandoned and the arm retired instead.
- closed: the problems row records the retirement now, rather than the illusory 2026-08-16 fix.
- closed: the hook comment states the retirement, rather than the second false line it had carried.

1. **The repair did not repair the fault.** stands: the change is abandoned and the arm retired instead.
   The guard stood the hook down unless the transcript's filename proved the call was the seat's. On this
   harness a worker's PreToolUse event carries the SEAT's `transcript_path` and the SEAT's `session_id`,
   so the guard read true and the worker was denied exactly as before. The reviewer rebuilt the
   2026-08-16 event from the transcripts and ran the fixed hook against it: it emitted its refusal. The
   corroborating counts are independent of that reconstruction — of the 31 state files the hook ever wrote,
   none names an agent — 30 resolve to a seat transcript and the odd one is this session's own bench
   fixture — while 68 worker transcripts hold 76 delivered refusals. A later probe closed the last door: a worker process carries the seat's
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
- `docs/PROGRESS.md` carried regenerated churn from the night before this work. It rides IN the
  retirement commit rather than beside it: the retirement shrinks the specification, so the page that
  publishes its size had to move with it.
- `tests/test_config_health.py` holds two reds on installed-versus-source drift in `pre-push` and
  eleven skills. They fail identically against `HEAD` with this change stashed, so they predate it and
  are untouched by it.

---

## Second pass — the retirement itself, also REFUSED, then repaired

The retirement that followed the refusal above was read by a second adversarial reviewer and refused on
ten blocking findings. The wiring side was clean; the prose side was not. Every finding is closed below,
and each closure names what changed.
Blocking: ten, all closed in the same pass. Each carries its `closed:` below.

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
   closed: the counts are gone rather than corrected — the prose names the declaration instead of
   repeating a number that drifts with it.
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

## The suite on the committed tree

`python3 -m pytest -q` against the retirement as committed at `49f26a7`: **2,474 passed, 2 failed,
54 skipped**, 20 minutes 17 seconds. Both failures are `tests/test_config_health.py` — the installed
copies of `guardrails/pre-push` and eleven skills drifting from their sources, and the personal
permission-path arm. They fail identically against `f9eaecc` with this change stashed, so they predate
it; `ROADMAP.md` row 537 owns them.

The final pass also closed four reds this change had made and one it inherited: `ARCHITECTURE.md` broke
two of its own laws under the retirement edit (a node field carrying a date, and a 38-word sentence in a
document held at zero findings); the specification's findings ceiling had to come down from 1,863 to
1,862, which the census refused until the retirement prose in `guardrails/language-rules.json` was cut
into shorter sentences; and gates a, b and g read red only while the record itself stood uncommitted.

---

## Fourth pass — the pushed range, REFUSED, then repaired

PUSH-REVIEW

Range: f9eaecc..HEAD (base f9eaecc; six reviewed commits listed below; this record's own commit follows
them and touches the record directory alone, which gate a exempts because a record cannot name the commit
that first ships it)
- e35408b A gate that reds on an interrupted write joins the problems journal (a flake this push met,
  recorded rather than retried in silence: `check-pin-drift.sh` exits non-zero when a signal interrupts
  its own `printf`, reddening gate g on a tree whose pins are fine)
- 8b6521f A hand-copied count leaves the prose for the declaration that holds it (this pass's own repair)
- 19efaed The communicator edit carries its skill review
- 5a51a41 The published counts catch up with the retirement's one-finding drop
- 6889b19 The retirement's record carries the suite it was measured against
- 49f26a7 Retire the tool-boundary chat arm: it could not prove whose work it stopped
Files read: the whole delta commit by commit, PRODUCT_SPEC.md and ARCHITECTURE.md as they now stand,
TEST_MATRIX.md rows M-461 and M-465, ROADMAP.md rows 537 and 543, JOURNAL.md's new entry,
.live-spec/PROBLEMS.md, attic/MANIFEST.md, docs/PROGRESS.md, docs/skill-review/2026-08-17-communicator.md,
guardrails/judge-hooks.json, guardrails/language-rules.json, guardrails/rule-census.json, the installers,
the hooks, the skills the range edits, and the live ~/.claude configuration.
Checks run: the refusal census recounted independently by record shape — 108 delivered, 76 into workers
across 68 transcripts, 32 into the seat across 19, matching every published figure; the census sum —
129 files, 4,950 findings, 24 at zero, PRODUCT_SPEC.md at 702,954 bytes and 1,862 findings, matching
docs/PROGRESS.md; `scripts/progress-report.py` rerun, leaving the tree byte-identical, so the page is
reproducible rather than typed; `pytest --collect-only` — 2,530 collected, agreeing with the suite line;
eighteen gates at exit 0, including hooks-can-fire, judge-listed, language-rules, named-checks,
doc-findings-bound, tree-counts, every-gate-can-fail, index-generated, matrix-reference,
requirement-shape, criterion-readability, shipped-language, config-health and skill-review;
`pytest` over 25 test files touching this change — 142 passed — and over 16 consistency files — 422
passed, 3 skipped.

Findings: one blocking, repaired below, and seven notes, six of them closed.
Blocking: one, closed in commit 8b6521f — the wired-hook count still read ten in three live documents
and four edited files. Its `closed:` line stands below.

1. **The wired-hook count drifted in three more documents, the same class the second pass made blocking
   three times.** The retirement takes the declaration from ten wired hooks to eight, and three live
   present-tense sentences still said ten: `PRODUCT_SPEC.md` Requirement 298's Context ("declares ten
   wired session hooks … reaches all ten"), `ARCHITECTURE.md`'s installer pin ("the other eight", in a
   pin whose own file this range had already corrected to "the rest"), and `TEST_MATRIX.md` row M-465's
   live clause ("installs and wires all ten declared hooks"). Every one was true before this range and
   false after it. Four more sites carried the same number in files this range had edited:
   `scripts/install-session-hooks.sh`'s header, `tests/test_install_session_hooks.py` in three places,
   and `tests/test_chat_law_hook.py`.
   closed: every site now names the declaration rather than repeating a count that drifts with it. That
   is the repair the number deserved the first time — a count hand-copied into prose is the defect, and
   correcting ten to eight would only have reset the clock on it.

Notes:

- **The governing law has no home.** The commit message and Requirement 295 both appeal to a law — a
  check that cannot prove whose work it stops does not get to stop work — that is stated nowhere in
  PRODUCT_SPEC.md. It lives as a lesson in `.live-spec/PROBLEMS.md` and in JOURNAL.md, and no queue row
  opens it. stands: minting a law in the specification is the owner's word to give, and this record
  carries the gap rather than closing it quietly. The next hook of this class has nothing to be judged
  against.
- **A number handed over without its method, inside the requirement retiring the measurement machine.**
  Requirement 295's User Story said "stopped 76 times" with no method beside it, which is the very rule
  the retired arm used to hold. closed: the criterion now carries how the number was counted and what it
  decided.
- **The record carried three statements the tree had left behind** — that `docs/PROGRESS.md` was kept
  out of the retirement commit, that the installer counts were corrected "eight and six throughout", and
  that the suite stood at two failures. closed: all three now say what is true, the last of them because
  the owner's word on 2026-08-17 allowed the two documented sync scripts to run and both failures went
  green.
- **"All 31 state files are named for seat sessions" was 30 of 31.** closed: the texts now say none names
  an agent, thirty resolve to a seat transcript, and the odd one is this session's own bench fixture.
- **"The pack wires no hook to PreToolUse today" was broader than the truth** — the pack ships a separator
  fence that wires one, and this machine carries an unrelated personal entry there. closed: the sentence
  now speaks of the pack's default settings.
- **A dead path in a live measured document:** `docs/audits/2026-08-07-number-census.md` pointed at the
  retired file's old home. closed: it points at the attic and says why.
- **The fence row's re-opening named the wrong owner.** It read the two occurrences as a re-arm that
  fails to fire, where `guardrails/post-commit` re-arms only on a fence already carrying this session's
  own token — so a session inheriting an ended session's arm blocks once by design. closed: the row now
  states that, with the proof from this session, and asks the real question instead.

