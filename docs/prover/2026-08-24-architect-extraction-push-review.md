# Prover record — 2026-08-24 architect-extraction push-review

PUSH-REVIEW

Range: 32a3b755..de8600c2
- de8600c2 skill-review: cover communicator's skill-count fix (INV-208)
- 3cc8b47f architect: extract as standalone skill from build-pipeline (package 3, cap. 21)

Files read: `docs/prover/README.md` (re-read, for record shape/conventions); `docs/prover/
2026-08-24-director-acting.md` (re-read in full as the rigor example this record follows); `git
show 3cc8b47f` and `git show de8600c2` in full, every hunk (11 files + 1 file respectively);
`skills/architect/SKILL.md` in full at its committed state; `docs/skill-review/
2026-08-24-architect-extraction.md` in full, current state (post both commits); `docs/director/
capability-map.md` row 21 and its "Package 3 progress" note, current state; `skills/director/
SKILL.md`'s specialist table and its new `skills/…` vs `references/…` cell-convention paragraph;
`skills/live-spec-base/SKILL.md`'s frontmatter description, opening heading, and closing roster;
`skills/live-spec-base/references/glossary.md`'s path-resolution paragraph; `skills/communicator/
README.md`'s opening paragraph; `PRODUCT_SPEC.md`'s `working skill` glossary entry, old and new;
`ARCHITECTURE.md`'s "shape at a glance" line; `OVERVIEW.md`'s roster heading and list;
`README.md`'s opening line and skill-links line; `guardrails/check-prover-record.sh` in full
(all four gate arms and the STAND-DOWN markers); `tests/test_skill_count_agrees.py`'s `HOMES`
list and docstring, to confirm which documents the mechanical test actually covers (README.md,
OVERVIEW.md, ARCHITECTURE.md, `skills/live-spec-base/SKILL.md` only — not PRODUCT_SPEC.md,
`skills/communicator/README.md`, or `skills/live-spec-base/references/glossary.md`, which the
review below re-checked by hand instead of trusting the test's coverage).

Checks run:
- `python3 -m pytest tests/test_skill_count_agrees.py -q` — 13 passed.
- `python3 -m pytest tests/test_director_scenarios.py -q` — 11 passed.
- `bash guardrails/check-skill-loadability.sh skills` — `OK (loadability): 13 skill(s) load,
  named, versioned, negative-scoped.`
- `bash guardrails/check-skill-review.sh` — exit 0, four `OK` lines: `architect`, `communicator`,
  `director`, `live-spec-base` each named as carrying a fresh record
  (`docs/skill-review/2026-08-24-architect-extraction.md`).
- `ls guardrails/check-prover-record.sh` exists; read it in full. Ran both
  `bash guardrails/check-prover-record.sh` and `bash guardrails/check-prover-record.sh --push`:
  both **FAIL** — `the newest committed prover record predates the last PRODUCT_SPEC.md change.
  PRODUCT_SPEC.md last changed in commit 3cc8b47f...; newest docs/prover/ commit is 32a3b755...`.
  This is the expected, unremarkable state of any range that touches PRODUCT_SPEC.md before its
  own push-review record is committed — it is exactly the gap this record exists to close, not a
  defect in the two reviewed commits. This record, once committed, becomes the newest
  `docs/prover/` commit and post-dates `3cc8b47f` (the commit that touched PRODUCT_SPEC.md and
  ARCHITECTURE.md), so committing it satisfies gate a's two freshness arms
  (`SPEC_COMMIT`/`ARCH_COMMIT` vs `RECORD_COMMIT`). It also satisfies the push-range arms: the
  `Range:` line above names the base short hash (`32a3b75`) and both reviewed commits'
  short hashes (`3cc8b47`, `de8600c`), and every required field (`PUSH-REVIEW`, `Range:`,
  `Files read:`, `Checks run:`, `Findings:`, `Blocking:`) carries a value, as this file's own
  shape shows. Confirmed the field pattern the script's `grep -m1 -E "^${field}:"` arm looks for
  is satisfied verbatim for all five fields.
- `ls guardrails/*.sh guardrails/*.py` — skimmed the full list for anything plausibly reachable
  by this diff's files. Ran, with correct CLI args recovered from `guardrails/pre-push` and
  `.github/workflows/gates.yml` (each script needs positional file arguments; a bare invocation
  just prints usage and exits 2, which is not a red — confirmed this before treating any usage
  message as a finding):
  - `python3 guardrails/check-architecture-reference.py ARCHITECTURE.md ARCHITECTURE.index.md` —
    OK, 401 anchors agree node-to-table, committed Reference equals a fresh build. (ARCHITECTURE.md's
    only change in this range is the "eleven"→"twelve" prose line in "The shape at a glance," not a
    node/`owns` section, so this result is unsurprising but confirmed rather than assumed.)
  - `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK, 394
    codes agree body-to-table, committed index equals a fresh build. (PRODUCT_SPEC.md's only change
    is the `working skill` glossary line's prose, not a `[req]`/anchor addition.)
  - `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md` — OK, 541
    rows scanned, committed Reference equals a fresh build. (TEST_MATRIX.md is untouched by this
    range; run anyway since the task flagged "matrix" as a plausible name-match — confirmed clean.)
  - `python3 guardrails/check-vocabulary.py PRODUCT_SPEC.md` — OK, every glossary term used in the
    body, no banned coinage.
  - `python3 guardrails/check-one-name.py PRODUCT_SPEC.md` — OK, no known alias present across the
    tracked alias list (13 aliases of 5 artifacts).
  - `python3 guardrails/check-touchpoint-kind.py`, `python3 guardrails/check-authority-anchor.py`,
    `python3 guardrails/check-doc-rotation.py` — all OK (pre-push's fast local chain includes
    these; none of this range's files are inputs any of the three reasons about, but ran them for
    completeness since they are wired into the same push gate).
  - Did not find a script whose name suggests "redundancy" as a standalone push gate distinct from
    the index/reference/matrix trio above (`scripts/spec-redundancy-precheck.py` exists but lives
    under `scripts/`, not `guardrails/`, and is a pre-check tool the index/matrix gates already
    subsume per its own header comment) — confirmed by reading `scripts/spec-redundancy-precheck.py`'s
    top-of-file comment rather than assuming from the name alone.
- `git diff origin/main..HEAD -- skills/build-pipeline/` — empty (0 lines). Confirmed
  build-pipeline is genuinely untouched by this range, matching both commit messages' explicit
  claim of "no partial migration."
- `skills/architect/SKILL.md` read in full at its committed state (199 lines): coherent
  standalone prose, correct YAML frontmatter (`name`, `description`, `metadata.version: 5.0.0`
  matching sibling skills), no broken markdown, no dangling links, no truncation. The closing
  "pack, whole" roster block-quote lists all fifteen named entities (`live-spec-base` +
  fourteen names including `product-prover` and `text-audit` as separate list entries alongside
  their `-pack` adapters) — this enumeration style is pre-existing (the same pattern appears
  verbatim, minus `architect`, in every sibling skill's own closing roster, e.g.
  `skills/live-spec-base/SKILL.md`'s roster) and is not the same count the "eleven/twelve working
  skills" headline states (which counts on-disk `skills/` folders, twelve, excluding
  `live-spec-base`) — these are two different, long-standing enumeration conventions in this
  repo, not something this range introduced or was obligated to reconcile. Confirmed by diffing
  the old vs. new `PRODUCT_SPEC.md` glossary line: the old line already enumerated the same
  fourteen-minus-`architect` names, so the mismatch between this list's item count and the
  headline "eleven" number predates this range and is untouched by it.
- Broad stale-count grep from the worktree root:
  `grep -rn "eleven working\|11 working skill\|eleven skills" . --include="*.md" 2>/dev/null`,
  then hand-filtered every hit against the task's exclusion list
  (`docs/prover/`, `docs/skill-review/`, `attic/`, `.git/`) plus, by the same dated-historical-record
  logic, every other hit found: `JOURNAL.md` (both hits sit inside dated `## 2026-08-05, ...`
  entries — the file's own header states "Edit history lives here... this file explains how we
  got there," i.e. every entry is a dated historical record by construction), `ROADMAP.md:208`
  (row 537's prose describes a *past*, dated 2026-07-30 drift snapshot for context, not a live
  "how many skills does the pack ship today" claim), `prototype/2026-07-22-spec-format/…`,
  `prototype/2026-07-23-architecture-format/…` (frozen, dated prototype exploration output, not
  live docs), `docs/reports/2026-07-28-…`, `docs/language-reads/2026-07-29-…`,
  `.live-spec/r2-repetition-2026-08-11.md` (all dated report/read artifacts). No hit found in any
  live, current-facing, undated document — i.e. nothing beyond what `3cc8b47f`/`de8600c2` already
  fixed (`README.md`, `OVERVIEW.md`, `ARCHITECTURE.md`, `PRODUCT_SPEC.md`,
  `skills/live-spec-base/SKILL.md`, its `glossary.md`, `skills/communicator/README.md`).
- `git log origin/main --oneline -3` — tip is still `32a3b755` (matches the range's stated base;
  `origin/main` has not moved out from under this branch).
- `git fetch --dry-run 2>&1` — no output, nothing to fetch; confirms the local `origin/main` ref
  is current.
- `git status --short` in the worktree — clean before this record was written (no stray
  uncommitted changes riding along).

Findings: no defect found in either reviewed commit. Re-verified, rather than trusted, every
substantive claim the skill-review record (`docs/skill-review/2026-08-24-architect-extraction.md`)
makes about its own two blocking findings and their fixes:
1. The stale-count fix: confirmed all seven now-updated homes (six named in `3cc8b47f`'s message
   plus `docs/director/capability-map.md`'s prose, which isn't a "how many skills" home but is the
   row this whole slice resolves) read "twelve"/"architect" consistently, and the mechanical test
   (`test_skill_count_agrees.py`) passes 13/13 rather than the 3-failed state the record says it
   found pre-fix.
2. The dropped-enforcement-sentence fix: read the shipped Quality budgets section
   (`skills/architect/SKILL.md` lines 88–90) and confirmed it states the same substance
   `build-pipeline`'s own copy states at line 391 ("Each budget is asserted by a matrix-row
   acceptance, never a hope in prose") — enforcement runs through a `test-author`-derived
   `TEST_MATRIX.md` row, not prose alone.
3. The second-commit fix (INV-208, `de8600c2`): confirmed `skills/communicator/README.md:10` now
   reads "twelve skills" and that this is the only change `communicator` carries in this whole
   range — re-read `git show 3cc8b47f -- skills/communicator/README.md` and
   `git show de8600c2` to confirm no other line in `communicator`'s tree changed, backing the
   record's own claim that this one-word fix is the entirety of `communicator`'s INV-208 review
   scope.

One pre-existing, out-of-scope quirk noted but not folded: `PRODUCT_SPEC.md`'s `working skill`
glossary-entry enumeration (and each skill's own closing "pack, whole" roster block-quote) lists
`product-prover` and `text-audit` as separate items alongside their `-pack` adapters, so its item
count (14, now including `architect`) has never equalled the "eleven/twelve working skills"
headline count (which counts on-disk folders under `skills/`, excluding `live-spec-base`). This
mismatch predates `3cc8b47f` (the old glossary line already enumerated 13 items against a
contemporaneous "eleven" headline) and neither commit in this range was obligated to reconcile it
— `test_skill_count_agrees.py`'s `HOMES` list does not cover this enumeration, by design (it checks
the stated *number*, not every roster's item count). Flagging for awareness, not as a blocking
finding of this range.

`build-pipeline` is confirmed genuinely untouched (`git diff origin/main..HEAD -- skills/build-pipeline/`
is empty), matching both commit messages' "no partial migration" claim. `origin/main` has not
moved (`32a3b755`, matching this range's stated base); nothing new to fetch.

Blocking: none
