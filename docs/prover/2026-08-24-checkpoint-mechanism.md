# Prover record — 2026-08-24 checkpoint-mechanism

PUSH-REVIEW

Range: 6fe95c7b..a8cf50e0
- a8cf50e0 checkpoint.py: close the section-header allowlist gap (adversarial review of 6ce6fca0)
- 6ce6fca0 checkpoint mechanism: schema, writer, reader, validator (package 3, cap. 27)

Files read: `docs/prover/README.md` in full; `docs/prover/2026-08-24-redundancy-coverage-fix.md`
in full, for shape/rigor calibration; `scripts/checkpoint.py` in full at both 6ce6fca0 (`git show
6ce6fca0:scripts/checkpoint.py`) and its current state after a8cf50e0 (worktree read); `tests/
test_checkpoint_mechanism.py` in full at both commits (`git show 6ce6fca0:tests/
test_checkpoint_mechanism.py`, then the current 16-test file); `git show 6ce6fca0` and `git show
a8cf50e0` (every hunk of both, `--stat` and full diff); `.live-spec/checkpoints/row241-worker.md`
in full, and every `.live-spec/checkpoints/*.md` file's `## ` header list (`grep -n "^## "`), to
independently check the fix's claim about a pre-existing `WATCHED` convention.

Checks run: two passes, pytest plus hand-run bypass probes each time — full detail below.
- First pass (against 6ce6fca0 alone, before the fix existed): `python3 -m pytest tests/
  test_checkpoint_mechanism.py -q` — 14 passed, matching the file's 14 `def test_` methods. Hand
  probes against `scripts/checkpoint.py`'s functions (not against the test suite's claims) for:
  empty file, `#`-only title, metadata line with no colon, CRLF line endings, `### DONE` /
  `##DONE` malformed headers, unicode title/owner, a section body containing a `## `-prefixed
  line inside a markdown code fence, a nonexistent path to `read_checkpoint`/`validate_checkpoint`,
  and `close_checkpoint` where the literal string "Status: open" appears inside a section body.
  Found a real bug: any `## `-prefixed line was accepted as a new section with no check against a
  known name, so a section named e.g. `## silently-hidden real work` placed after `## IN PROGRESS`
  containing only the placeholder `(nothing)` would truncate `IN PROGRESS`'s parsed body to just
  `(nothing)`, filing the real unfinished-work text into an unchecked section — `validate_
  checkpoint` returned `[]` and `close_checkpoint` succeeded on a checkpoint that still had real
  open work in it, reproduced and confirmed live against the committed module, not inferred from
  reading the source. Also confirmed clean at that point: CLI `validate` with neither a path nor
  `--all` errors via `argparse.error` (exit 2, no raw traceback); importing `checkpoint` produces
  no stdout and touches no disk (CLI gated under `if __name__ == "__main__":`); `grep -rln
  "checkpoint" guardrails scripts --include="*.py"` minus the two new files hits only `scripts/
  session-extract.py` and `scripts/sweep-rendered.py`, both prose mentions, confirmed via a second
  grep for `import checkpoint`/`from checkpoint`/`checkpoint\.py` across those and `guardrails/*.py`
  finding no hits — nothing else in the repo imports this module yet, as the commit message says.
  This blocking finding was reported back rather than fixed by this reviewer, per the process; no
  record was written or committed for that pass.
- Second pass (a8cf50e0, the fix): `git show a8cf50e0` read in full — the fix adds `ALLOWED_
  SECTIONS = {DONE, IN PROGRESS, NEXT, DECISION SHEET, WATCHED}` and one `if header not in
  ALLOWED_SECTIONS: raise ValueError(...)` check inside `read_checkpoint`'s section loop, plus two
  new regression tests; nothing else in the file changes (confirmed by re-diffing `git show
  a8cf50e0 -- scripts/checkpoint.py` for non-docstring/non-allowlist hunks — none exist). Re-ran my
  exact original repro by hand against the fixed module (not the new test's name) —
  `read_checkpoint` now raises `ValueError: unrecognized section header: ## silently-hidden real
  work` at parse time, before `validate_checkpoint`/`close_checkpoint` ever see the file. Bypass
  attempts against the closed allowlist, all run live: lowercase/mixed-case variants (`watched`,
  `Watched`, `done`, `DONE.`) all correctly rejected — no case-insensitivity hole; leading/trailing
  whitespace around `WATCHED` (`"WATCHED "`, `" WATCHED"`) normalizes via the existing `.strip()`
  to the one allowed name, not a new unchecked one — not a bypass, just permissive whitespace
  handling pre-existing before this fix. `python3 -m pytest tests/test_checkpoint_mechanism.py -q`
  — 16 passed, matching the file's 16 `def test_` methods (up from 14, the two new regression
  tests). Re-confirmed CLI `validate` with no path/no `--all` still errors via `argparse.error`
  (exit 2); import still produces no stdout; `grep` for imports of `checkpoint.py` across
  `guardrails`/`scripts` still empty — all three unchanged from the first pass, consistent with the
  diff touching only `read_checkpoint`'s section loop and docstrings/comments. Independently
  checked the fix's claim that `WATCHED` is "a pre-existing... convention already used by worker
  checkpoints in this project": `grep -n "WATCHED" .live-spec/checkpoints/row241-worker.md` — one
  real hit, line 77, confirming the substring claim is true. Also ran `python3 scripts/
  checkpoint.py validate --all` against the repo's real, gitignored `.live-spec/checkpoints/`
  directory (18 files) to check whether the new allowlist regresses parsing of real pre-existing
  checkpoints: every file errors with `missing required metadata key: Status:` (or a malformed-
  metadata-line variant) — i.e. every real file already fails at the metadata-parsing step, before
  the code ever reaches section-header parsing, on both 6ce6fca0 and a8cf50e0 alike (these files
  predate the `Status:`/`Owner:` schema entirely). The allowlist fix does not newly break any file
  that was parsing cleanly before; nothing in `.live-spec/checkpoints/` was parsing cleanly before.
  Constructed a targeted probe for a residual gap in the fix itself: a checkpoint with `## IN
  PROGRESS` holding only the placeholder `(nothing)` and real unfinished-work prose
  ("Actually still wiring the retry path here, not really done, do not close!") filed under `##
  WATCHED` instead — `validate_checkpoint` returns `[]` for both open and closed status, and
  `close_checkpoint` succeeds. This is real and reproducible, but by design and disclosed in the
  fix's own comments ("stays allowed but, like before, ignored by validate_checkpoint") — `WATCHED`
  is a single, fixed, documented reserved name a checkpoint author must type deliberately, not an
  arbitrary accidental heading, and the one real example of `WATCHED` usage found in this repo
  (`.live-spec/checkpoints/row241-worker.md:77-79`, "noticed the CLI --all glob needs a stable
  sort; not blocking, just logging it") matches the "workshop noise, not real open work" intent the
  name implies. Judged non-blocking: see Findings.

Findings: this range was reviewed in two passes because the first pass found a blocking defect,
which was fixed in the second commit and re-verified rather than trusted.

**Pass 1 (6ce6fca0 alone) — blocking, reported back, not committed as a record.** `read_checkpoint`
accepted any `## `-prefixed line as a new section with no check against a known name. A section
body containing a stray `## `-prefixed line (plausible inside a code fence, a pasted example, or an
ad hoc subheading) silently truncated the real section at that point and filed the remainder into
an unchecked, arbitrarily-named section that `validate_checkpoint` never inspects (it only checks
`DONE`/`IN PROGRESS`/`NEXT`/`DECISION SHEET` by name). Constructed and ran a case where `##
IN PROGRESS`'s visible body was exactly the placeholder `(nothing)` with genuine unfinished-work
text hidden past a stray header: `close_checkpoint` succeeded, flipping the file to `Status:
closed` while real open work sat, unflagged, in the file. This directly contradicted the module's
own stated guarantee ("closing a checkpoint with open work left in it is now a hard error instead
of a silent drift"; `close_checkpoint`'s docstring, "content is never silently discarded").

**Pass 2 (a8cf50e0, the fix) — closes the reported gap; no new blocking issue found.**
`ALLOWED_SECTIONS` now rejects any `## ` header outside `{DONE, IN PROGRESS, NEXT, DECISION SHEET,
WATCHED}` as a structural `ValueError`, at parse time, before `validate_checkpoint`/`close_
checkpoint` can be reached. My exact original repro now raises `ValueError: unrecognized section
header: ## silently-hidden real work` — re-run live against the fixed module, not assumed from the
new test's name or docstring. I tried to find a way past the closed allowlist itself (case
variants, whitespace variants, near-miss names) and found none — every non-exact match is rejected,
and the whitespace tolerance that does exist (`.strip()` on the header text) only ever normalizes
onto the same five allowed names, never opens a new unchecked one. The one residual gap is `##
WATCHED` itself, which — as documented in the fix's own comments — remains completely unchecked by
`validate_checkpoint`/`close_checkpoint` by design; genuine unfinished-work prose filed there
(deliberately or by author confusion) would not block a close. I judge this non-blocking: it
requires typing one specific, disclosed, reserved section name rather than any arbitrary heading or
code-fence accident, the fix's commit message and code comments are explicit that `WATCHED` stays
unchecked, and the one real usage of the convention in this repo (`.live-spec/checkpoints/
row241-worker.md:77`) matches the "non-blocking workshop noise" intent rather than smuggled open
work. This is a narrower, disclosed design choice, not the accidental, silent hole the first pass
found — but it is worth a future reviewer's attention if `WATCHED` usage in practice ever drifts
toward carrying real state.

Also checked: `docs/prover/README.md`'s "What the gate holds" list — a record dated today, no
older than `PRODUCT_SPEC.md`/`ARCHITECTURE.md` (both untouched by this range — confirmed via `git
show a8cf50e0 --stat` and `git show 6ce6fca0 --stat`, neither names those files), fresh against the
full pushed range (both commits named above), naming the base commit and every reviewed commit.

Blocking: none
