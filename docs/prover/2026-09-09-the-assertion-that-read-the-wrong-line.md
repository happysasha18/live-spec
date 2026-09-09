# Prover record — 2026-09-09 the assertion that read the wrong line

Prover skill version: product-prover 1.6.0, the installed copy under `skills/product-prover/`, read
beside the pack bindings `skills/product-prover-pack/SKILL.md` (v6.1.4). The reviewer wrote none of
this change and changed no byte of this tree in any of its four rounds; every mutation it ran was on
a scratch copy.

PUSH-REVIEW

Mode: closure
Scope: the accepted row q-835 and nothing else — its definition of done, its own recorded acceptance
command at this commit, the diff of the pushed range, and the paths that diff touches read directly,
which are `scripts/inbox_lifecycle.py`, both copies of the status probe, `scripts/task-admission.py`
and `scripts/plan_checks_core.py` where they read and write a row's source letter,
`adopt/install-status-view.sh`, `inbox/README.md`, `tests/test_inbox_lifecycle.py` and
`tests/test_status_view_install.py`.
Range: b8ec3ee8..04f95252
- 04f95252 The architecture's pins follow the text that moved under them — written after this read
  and by the gate that caught them; it moves four line numbers and changes no behaviour
- a4554732 q-835 closed: the link is proved bound to the letter and to the row
- 9af50e9a Merge the inbox-state lane
- e7a7df99 q-835: an inbox letter carries its own state, and the board names the letter a row came from
- 086415d5 q-835 admitted and taken up: an inbox letter carries its own state
- b8ec3ee8 (base) The record's range reaches the second review it asked for
Files read: PLAN.md (row q-835), .live-spec/checkpoints/q-835.md, .live-spec/readers/q-835-reader.md, scripts/inbox_lifecycle.py, scripts/state-probe.sh, scaffold/status-view/state-probe.sh, scripts/task-admission.py, scripts/plan_checks_core.py, scripts/plan_checks.py, adopt/install-status-view.sh, guardrails/check-status-view-drift.py, guardrails/check-earned-message.py, guardrails/check-deposit-description.py, inbox/README.md, every letter under inbox/ and inbox/handled/, tests/test_inbox_lifecycle.py, tests/test_status_view_install.py, tests/test_probe_reads_state.py, tests/test_inbox_deposit_protocol.py
Checks run: the row's own acceptance command verbatim — exit 0, 95 tests; each of its three arms broken deliberately on a scratch copy and shown red; the new test file run against the three touched scripts restored to b8ec3ee8 while the new reader was kept, to establish the red-proof independently of the producer's claim — eight tests red, and every test that survived that reversal named; a mutation matrix of twelve behaviours run four times over the landing's rounds, each mutation removing one behaviour the done names and each shown to red; ten mutations of the letter-to-row link built and run; `_fields_only` attacked over twenty fenced shapes — an unterminated fence, nested and repeated fences, tilde fences, an indented fence, a fence inside a list, a real field before and after a fenced one, a fenced `Superseded-by:` beside a real `Status: superseded`, an info string, an indented code block; `plain_lines` attacked over eleven adversarial probe lines including a row titled like an inbox marker and a letter whose name extends another's; the real `scripts/state-probe.sh` driven over throwaway trees for every one of the four states, for a letter with no state line in each location, for a superseded letter naming nothing, naming a file off disk and naming one on disk, for an unknown state word, for a word in the wrong case, for an empty letter, a `.draft` and `README.md`; admission driven with `source.inbox` naming a real letter, an archived letter, a letter off disk, an empty string and nothing at all; the installer run into a fresh scratch host and its manifest and drift check read; `guardrails/check-earned-message.py` and `check-deposit-description.py` run over the real inbox with and without a `Status:` line; the guarded import exercised with the reader absent; `python3 -m pytest -q tests/test_inbox_lifecycle.py tests/test_task_admission.py tests/test_status_view_install.py tests/test_update_watcher.py tests/test_probe_reads_state.py tests/test_inbox_deposit_protocol.py` — 137 passed.
Findings: Every clause of the done now has a test that reds when its behaviour is removed, driving the real reader and the real status list. The reader is the one home for the four words and both callers reach it through a guarded import, so a tree carrying the probe without the reader falls back to listing by position rather than failing. The two probe copies are byte-identical in full. Thirteen letters on the record read correctly with no edit to any of them, and `git diff` over `inbox/` shows only the README. The refusals name the fault they met, and the fence rule and the case tolerance are each anchored by a test and written down where a depositor reads. Two link mutations survive the final shape and neither is a defect: one is an arbitrary index cutoff whose output is identical because the third letter carries no row, the same family as a gate on the `.md` suffix that every letter has, and the other moves the probe's own `shown` counter rather than the link, leaving every letter printed beside its own row. Three things stand outside this row's reach: the deposit gates enumerate `inbox/` by position and still gate a letter now marked handled, noted or superseded in place, which no letter uses yet; `state-probe.sh`'s import of `plan_checks` is unguarded, which predates this row and is answered by the installer seeding that file; and a tree where every open letter carries a row would catch the counter mutation for free.
Blocking: three, across four rounds, all reproducible and all closed before this commit. The reviewer wrote none of the change and none of the repairs; each `stands:` is the reviewer's own and the `closed:` beside it is the holder's, added after that round's read.
- The link test asserted against the plan row rather than the letter's own line. stands: its three assertions were satisfied by the PLAN section, which prints `q-1 ... inbox:a.md` whatever the inbox block does. Deleting the link outright left the test green, and the same test survived the reversal of all three scripts to the base commit — proof from a second direction that it read nothing this change did. closed: the assertion takes the line opening with the letter's own marker, with the colour stripped, and compares it whole.
- The repaired filter read the plan row again. stands: it excluded a line containing `"q-1 "`, and the plan row does not contain it — an escape sequence sits between the id and the space — so the plan row survived the filter and the letter's line was dropped. The test was green with a wrong title printed, green with a link invented for a letter no row names, and green with a link invented naming a row that does not exist; only the deleted link reddened it, and that through a line count rather than through content. closed: a helper strips the colour and keeps the lines opening with a given marker, and its docstring names why a substring test over raw output picks the wrong line. Ten link mutations die on the result.
- The link was never proved bound to the right letter or the right row. stands: every test in the file showed the probe a single letter and a single row, so a probe handing the first row it holds to whatever letter it is printing passed all of them, and so did one taking a link's id or title from whichever row comes first. Three mutations of the first kind and three of the second were shown green. closed: the test carries two rows and three letters — a neighbour sharing a first character, so a match comparing less than the whole name is caught, and a third letter naming no row, so a fallback still has somewhere to fire. All six mutations red on it, alongside the four the earlier shape caught.

## What this read did not cover

The scope was named before the read and did not grow with it. The spec, the architecture and the
matrix were not read; nothing in this range touches them. The full pytest suite was not run here:
CI's gate b runs it over this commit, and the row's own acceptance plus the five neighbouring files
were run at every round. One question the reviewer raised it also withdrew, and the withdrawal is
recorded because it decided the shipped rule: an unterminated fence blanks the rest of the letter,
which loses a real field standing after it, and that is what the letter renders as by the common
mark rules, while the matched-pairs alternative the reviewer prototyped brings back the defect the
repair exists for. Two things ride in the reviewed range that the row's own done does not name, and
both are named in the commit that carries them: the status-view installer now vendors the new
reader, and `tests/test_status_view_install.py` reads the installer's own array instead of keeping a
second copy of it. A fourth thing rides in the range and was written after this read: the four
architecture pins that the inbox README's new section and the plan parser's new field pushed down
the page. Gate g named each one, and each now names the line its own description stands on.
