# Prover record — 2026-08-24 director-acting

PUSH-REVIEW

Range: b870c51b..996a3001
- 996a3001 checkpoint.py: title/owner must be single-line; reject duplicate metadata keys
- 590d8714 checkpoint.py: reject ## -prefixed lines in written section bodies
- 40f9d8f2 skill-review: director acting-mode (ad851b7d, 9dec33f1)
- 9dec33f1 checkpoint.py: add update_checkpoint; director: fix the new-vs-update gap
- ad851b7d director: shadow mode ends, the skill acts (package 3, cap. 9/10/11/24/28/30)

Files read: `docs/prover/README.md` (re-read); `docs/prover/2026-08-24-checkpoint-mechanism.md`
(this range's predecessor record, for continuity — its `WATCHED`/case-sensitivity ground already
covered was not redone); `docs/skill-review/2026-08-24-director-acting.md` in full; `git show`
in full for all five commits (`ad851b7d`, `9dec33f1`, `40f9d8f2`, `590d8714`, `996a3001`), every
hunk; `skills/director/SKILL.md` in full, current state; `PRODUCT_SPEC.md`'s and `OVERVIEW.md`'s
glossary-entry diffs (`git show ad851b7d -- PRODUCT_SPEC.md OVERVIEW.md`); `docs/director/
capability-map.md`'s and `JOURNAL.md`'s new sections (`git show ad851b7d -- docs/director/
capability-map.md JOURNAL.md`); `scripts/checkpoint.py` in full, current state, and at each of
`ad851b7d`/`a8cf50e0`/`590d8714` via `git show <rev>:scripts/checkpoint.py` for byte-identity and
regression checks; `tests/test_checkpoint_mechanism.py` in full, current state (36 tests), and its
diffs at `9dec33f1`, `590d8714`, `996a3001`.

Checks run: three adversarial rounds — round 1 found and reported a blocking bug (not fixed by
this reviewer), round 2 found and reported a second, independent blocking bug in round 1's own
fix, round 3 verified round 2's fix holds and found no fourth gap. Full detail below.
- Round 1 (against `ad851b7d`+`9dec33f1`+`40f9d8f2`, before `590d8714` existed): confirmed
  `git diff origin/main..HEAD --stat` at that point matched exactly what the three commit messages
  claimed (`JOURNAL.md`, `OVERVIEW.md`, `PRODUCT_SPEC.md`, `docs/director/capability-map.md`,
  `docs/skill-review/2026-08-24-director-acting.md`, `scripts/checkpoint.py`, `skills/director/
  SKILL.md`, `skills/director/references/verify-step-detail.md`, `tests/
  test_checkpoint_mechanism.py`). Confirmed the `PRODUCT_SPEC.md`/`OVERVIEW.md` glossary rewrite
  ("for accepted work, writes a decision sheet and carries it through a checkpoint it opens and
  closes itself") is accurate to the shipped `SKILL.md`, not an overclaim: Execution opens a
  checkpoint via `new`/`update`, carries the decision sheet as the checkpoint's `DECISION SHEET`
  section, and closes it in "Closing the work closes the checkpoint in the same step" — read the
  full section, not just the glossary line. Spot-checked the skill-review's own claims rather than
  trusting them: `git show 9dec33f1 -- tests/test_checkpoint_mechanism.py` showed only 7 new `def
  test_` lines added, zero removed/modified, confirming "all 16 prior tests unchanged" myself.
  `python3 -m pytest tests/test_checkpoint_mechanism.py -q` — 23 passed, matched 23 `def test_`
  methods. Independently rebuilt `new_checkpoint` from `git show ad851b7d:scripts/checkpoint.py`
  (pre-refactor) and diffed its output byte-for-byte against the post-refactor `new_checkpoint`
  across three cases (plain, director+decision_sheet, unicode title) — all three byte-identical,
  confirming the skill-review's "byte-identical output" claim myself rather than trusting it.
  `docs/director/capability-map.md`'s new "Package 3 progress" section and `JOURNAL.md`'s new
  entry both read as accurate to the actual diff (row 21/architect explicitly still "open",
  build-pipeline explicitly not yet removed, matching the commit message — no overclaim found).
  Independent adversarial pass beyond the skill-review's SKILL.md-prose focus, on the new
  `scripts/checkpoint.py` code: found that `update_checkpoint`'s `done`/`in_progress`/`next`/
  `decision_sheet` params (and `new_checkpoint`'s pre-existing `decision_sheet` param, live since
  `a8cf50e0`) wrote free text to disk with no check that it didn't itself contain a line starting
  with `## ` — reproduced live via the actual CLI path `SKILL.md` directs the Director to use
  (`checkpoint.py new ...` then `checkpoint.py update <path> --next "$(printf 'Still to do:\n##
  Blocked on\n- ...')"`): the `update` call succeeded silently, and the file was then permanently
  unreadable via `validate`, `close`, or a further `update` — every one raised `ERROR: unrecognized
  section header`, with no repair path through this module's own API except `new_checkpoint`'s
  blank-template overwrite, the exact operation this same range's `SKILL.md` rewrite forbids using
  on work already in flight. Reported back in full rather than fixed by this reviewer; no record
  was written or committed for this round.
- Round 2 (against the fix, `590d8714`): read `git show 590d8714` in full — `_reject_embedded_
  headers(field_name, value)` checks every line of a value via the identical `line.startswith("##
  ")` test `read_checkpoint`'s own parser uses, wired into `new_checkpoint`'s `decision_sheet` and
  all four of `update_checkpoint`'s fields, before any write. `python3 -m pytest tests/
  test_checkpoint_mechanism.py -q` — 30 passed, matched 30 `def test_` methods. Re-ran the round-1
  repro live via the CLI subprocess path exactly as before: `update --next` with the embedded `##
  Blocked on` line now fails loudly at the `update` call itself (`ERROR: next must not contain a
  line starting with '## '...`, exit 1), and — the actual point of the fix — `validate` on the file
  afterward returned `OK:`/exit 0 with `NEXT` still holding its placeholder: no brick. Bypass
  attempts against the new check, all run live: CRLF line endings inside a bad value still caught
  (`.splitlines()` handles `\r\n`); a double-space `"##  Extra spaced header"` still caught; a line
  that's exactly `"## "` (empty header text) still caught; a tab-separated `"##\tTabHeader"` line is
  *not* caught by the new check, but confirmed this is consistent rather than a bypass —
  `read_checkpoint`'s own parser uses the identical test, so a tab-separated line was never treated
  as a header on read either, and it round-trips as ordinary body text with no brick either side;
  `value=""` (empty string, not `None`) correctly passes the `is not None` guard as a legitimate
  section-clearing call, not a dodge; a multi-bad-field call (`done` and `next` both bad) raised on
  `done` first, matching the documented check order, with the file byte-for-byte unchanged
  afterward, confirming all-or-nothing writes. Verified the negative control is a genuine round-
  trip, not just "didn't raise": wrote a value containing `"## "` mid-line, read it back, and
  confirmed the returned section body is byte-identical to the original string, with
  `validate_checkpoint` returning `[]`. Independent adversarial pass beyond the fixed fields: found
  that `title` and `owner` — free text also written straight into the file by `new_checkpoint`, via
  `_serialize_checkpoint` — received no validation at all. A `title` with an embedded newline
  reproduced the exact same brick pattern the fix had just closed for the other four fields
  (`read_checkpoint` on the result raised `malformed metadata line`). An `owner` with an embedded
  newline was worse: `new_checkpoint(p, title="T3", owner="worker\nStatus: closed")` wrote without
  raising, and the resulting file's genuine `Status: open` line (always written by `new_checkpoint`)
  was silently overridden by the injected second `Status:` line, because `read_checkpoint`'s
  metadata loop built a plain `dict` with no duplicate-key check — `read_checkpoint` on the result
  returned `status == "closed"` with zero error, on a file `new_checkpoint` had just written as
  definitively open. Reported back in full as a second, independent blocking finding rather than
  fixed by this reviewer; no record was written or committed for this round either.
- Round 3 (against the second fix, `996a3001`, this round): read `git show 996a3001` in full —
  `_reject_multiline(field_name, value)` raises unless `len(value.splitlines()) == 1`, using
  `splitlines()` itself (catching `\n`, bare `\r`, `\r\n`, and the other line-boundary characters
  Python's own `splitlines()` recognizes) rather than a hand-rolled `"\n" in value` check, wired
  into `new_checkpoint` for both `title` and `owner`; independently, `read_checkpoint`'s metadata
  loop now raises `"duplicate metadata key: %s"` on a second occurrence of the same key, mirroring
  the pre-existing duplicate-section-header pattern. `python3 -m pytest tests/
  test_checkpoint_mechanism.py -q` — 36 passed, matched 36 `def test_` methods. Re-ran the round-2
  repro live, exactly as filed: `checkpoint.new_checkpoint(p, title="T3", owner="worker\nStatus:
  closed")` now raises `ValueError: owner must be a single line (no embedded line break):
  'worker\nStatus: closed'` at the `new_checkpoint` call itself, with the file never created
  (confirmed `os.path.exists(p)` is `False` after the raise). Independently tested the self-audit's
  own claims rather than trusting them, per this round's specific ask: traced both call sites of
  `_serialize_checkpoint` (`new_checkpoint`'s, where `status` is the hardcoded literal `"open"` and
  `sections` keys are hardcoded constants/`DIRECTOR_SECTION`, never user text; `update_checkpoint`'s,
  where `title`/`status`/`owner` all come from a prior successful `read_checkpoint` call and are
  therefore trivially single-line by construction — a value read via `text.splitlines()` can never
  itself contain an embedded newline, independent of any explicit check — and `sections` keys are
  again the same hardcoded constants) — confirmed no path reaches `_serialize_checkpoint` with an
  unvalidated `status` or a user-supplied section name. Re-ran the `close_checkpoint`
  "literal-string-swap targets the wrong line" probe against the *current* module (with
  `update_checkpoint` and both injection fixes in place): built a checkpoint via `new_checkpoint`
  then `update_checkpoint(p, done="...Status: open...")` so `DONE`'s body itself contains a
  literal `"Status: open"` line, then called `close_checkpoint` — the rewrite correctly touched
  only the true metadata line (file's line 2, always encountered first since section bodies are
  structurally guaranteed to appear later in the file than the metadata block), leaving the `DONE`
  body's look-alike text byte-for-byte untouched; confirmed this holds now that owner-based
  `Status:` injection is independently blocked, not merely unexercised. Checked the duplicate-
  metadata-key check's interaction with the existing "Status/Owner not in metadata" checks for a
  regression: a file missing `Owner:` entirely (no duplicate) still correctly raised "missing
  required metadata key: Owner:", confirming the new in-loop duplicate check didn't short-circuit
  or reorder the post-loop presence checks; a file with `Status:` written three times correctly
  raised on the *second* occurrence (`"duplicate metadata key: Status"`), never reaching a third.
  Tested one more angle: a body written via `update_checkpoint` containing lines that themselves
  look like metadata (`"Owner: someone-else\nStatus: closed\n..."`) placed inside `NEXT` (after the
  real section header) — confirmed harmless, since metadata parsing only ever runs on the block
  between the title line and the first `## ` header; the real `owner`/`status` were unaffected and
  the body round-tripped intact. No fourth gap found.

Findings: this range required three adversarial rounds because my own pass found two real, distinct
blocking bugs, each in a different commit, each reported rather than fixed by this reviewer, each
independently fixed and then re-verified live rather than trusted.

**Round 1 finding — section-header injection via `update_checkpoint`/`new_checkpoint`'s free-text
fields, fixed by `590d8714`.** Writing an ordinary multi-line note (no adversarial intent needed —
a plausible "Blocked on" sub-note, in a project whose own documents use `## ` headers pervasively)
into `done`/`in_progress`/`next`/`decision_sheet` silently succeeded on write, then permanently
bricked the file for every read-dependent function in the module, including the one CLI operation
(`update`) `SKILL.md`'s new Execution section names as the routine way to handle every correction
and replan. The only repair path through this module's own API was the exact "blank-template
overwrite, silently clobbers DONE" operation the same `SKILL.md` rewrite explicitly forbids for
work already in flight. `590d8714` closes this with a write-time check using the identical
line-test the reader uses, verified live above, including a real negative control and a fully
faithful re-run of the original repro through the actual CLI.

**Round 2 finding — `title`/`owner` injection, the fix for round 1 not covering every field that
reaches the file, fixed by `996a3001`.** `590d8714`'s fix covered the four section-body fields but
left `title` and `owner` — also free text `new_checkpoint` writes straight into the file — with no
validation. A newline in `title` reproduced the identical brick pattern just closed for the other
fields. A newline in `owner` was strictly worse: it let a caller inject a bogus second `Status:`
metadata line that `read_checkpoint`'s loop silently accepted (last value wins, no duplicate-key
check), so a file `new_checkpoint` had just written as unambiguously open read back as closed with
zero error — the exact silent-drift failure the whole mechanism exists to prevent, except here
nothing even attempted to close it. `996a3001` closes this two ways: `_reject_multiline` blocks a
non-single-line `title`/`owner` at `new_checkpoint`'s write time (verified live: the exact repro now
raises at the `new_checkpoint` call, file not created), and `read_checkpoint`'s metadata loop
independently now rejects any duplicate key outright, as defense in depth for hand-edited files that
never went through `new_checkpoint` at all.

**Round 3 — no third gap found in this fix, and no fourth gap found on an independent pass over the
whole module's disk-touching surface.** Traced every value that reaches `_serialize_checkpoint`
across both call sites and confirmed each is either a hardcoded literal, a hardcoded section-name
constant, or a value `read_checkpoint` already validated (and therefore trivially single-line by
construction, not merely by an explicit check) — no path writes an unvalidated `status` or an
arbitrary section name. Re-confirmed `close_checkpoint`'s targeted `Status:`-line rewrite still
can't be fooled by a look-alike `"Status: open"` string placed in a section body, now specifically
re-tested against the current module with `update_checkpoint` and both injection fixes in place, not
merely re-asserted from the earlier, simpler version of the code. Confirmed the new duplicate-
metadata-key check doesn't regress or reorder the pre-existing "Status/Owner missing" checks.

Also confirmed: `PRODUCT_SPEC.md`/`ARCHITECTURE.md` are untouched by any of the five commits in this
range (`ad851b7d`'s stat touches `PRODUCT_SPEC.md`'s glossary line only, not `ARCHITECTURE.md`;
`9dec33f1`/`40f9d8f2`/`590d8714`/`996a3001` touch neither), so this record's freshness against those
two documents rests on the one glossary-line change already checked for accuracy above, not on any
change this range makes to `ARCHITECTURE.md`.

Blocking: none
