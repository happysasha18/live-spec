# `SKILL-REVIEW` — communicator, the dedup-into-pointers pass

Skill: communicator. Date: 2026-08-18 (first pass), reworked 2026-08-18 (second pass).
Range: 99050f5..HEAD.

Verdict: ALLOW (second pass, after the fix in d432fca9 — see "Second pass" below). The first pass's
REJECT and its findings stand as read; they are not erased, only closed.

Commits of the range touching `skills/communicator/`:

    99050f5 Dedup surviving chat-law paraphrases into pointers
    d432fca9 Restore the contrast-frame mechanism and name the personal profile

## First pass (2026-08-18, against 99050f5..HEAD before d432fca9) — REJECT

First-pass verdict: REJECT. One of the four trims silently drops the rule's mechanism instead of
pointing at it, and both new pointers name a filename two files in this project share without saying
which one.

## What changed

`skills/communicator/SKILL.md`'s calque bullet and no-contrast-frame bullet, and
`writing-register.md`'s rule 15 (twice), traded a restated law for a pointer to its home. Read against
`git show 99050f5` and the current text of both files in full.

## Findings

1. **SKILL.md's rule-15 fallback bullet lost the mechanism it exists to carry, not just its
   paraphrase.** `SKILL.md` line 431 now reads: *"Never the contrast frame (rule 15, ... — Home:
   profile.md key language.no-contrast-frame). The linter's scissors check holds the floor..."* — the
   whole definition of what a contrast frame IS (the em-dash/comma shape, the Russian equivalents,
   "say what the thing is") is gone, replaced by nothing but the Home pointer. This is the section
   whose own framing sentence (line 427) says it "holds only the two loudest rules so a reader meets
   them even without loading [writing-register.md]". A reader who takes that promise at face value
   and does not load writing-register.md now has zero mechanism to apply — only a pointer to a
   *different* file than the one this section exists to stand in for, and (finding 2) an ambiguous one.
   Contrast this with `writing-register.md`'s own rule 15 (lines 93-104): it trimmed only the
   redundant intro sentence and **kept** the shapes bullet ("the em-dash or a comma leading into the
   denied neighbour..."), so that file's own checklist item 9 ("scan ... for rule 15's shapes") still
   resolves inside the same document. SKILL.md's copy has no such fallback — it is a genuine
   information loss, not a dedup.

2. **The pointer's own text is ambiguous between two files literally named `profile.md` in this
   project.** Both new pointers read "Home: profile.md key language.no-contrast-frame" with no
   qualifier. This repo carries a *host* profile at `.live-spec/profile.md` (checked directly: it has
   no `language.*` keys at all — its bullets are `prover.cadence`, `project.kind`, `trust.push-grant`,
   etc.) and a *personal* profile at `~/.claude/live-spec/profile.md` (a symlink to
   `~/.claude/playbook/personal/profile.md`, a machine-wide file outside this repository, checked
   directly: its `## Language` section does carry `no-calques` and `no-contrast-frame` bullets with
   the full rule text). The pack's own vocabulary (OVERVIEW.md's table, TEST_MATRIX M-233 — "the law's
   home named (**personal** profile language.no-scissors)") always disambiguates with the word
   "personal" precisely because two same-named files exist. Both new pointers drop that word. A model
   resolving "profile.md" against the current tree, as bare filenames normally resolve, lands on
   `.live-spec/profile.md` and finds nothing — the law's actual text lives one directory scope further
   out, on a file that (per TEST_MATRIX M-208) is not guaranteed to exist on every host at all.

3. **No dangling reference otherwise, and the surviving pointer is sound.** SKILL.md's calque bullet
   ("base rule 2, no-calques") points into `skills/live-spec-base/SKILL.md` rule 2 (read directly,
   lines 87-96), which fully states the mechanism — docs-language terms never loan-translate into
   chat, say it in plain chat words, the original may trail in parentheses. That pointer resolves
   inside the shipped pack, with no ambiguity and no loss; it is the one trim of the four that works
   as designed.

4. **No orphaned fragments.** Read every edited line in full context (not just the diff hunks): no
   sentence is left starting mid-clause or missing a verb after the cuts. The em-dash lead-in before
   the calque bullet's worked example ("... no-calques). — *❌ ..."*) predates this commit and is
   unchanged.

## The net

Three of four trims are clean or acceptable; one drops instruction outright (finding 1) and both new
"Home:" pointers are ambiguous in a way this project's own conventions normally guard against
(finding 2). Not a formality rejection — a reader following either pointer as literally written, on a
fresh host or without already knowing the personal-profile convention, cannot recover the law.

Reviewer: read `git show 99050f5` in full, the complete current text of `skills/communicator/SKILL.md`
and `skills/communicator/references/writing-register.md`, `skills/live-spec-base/SKILL.md` rule 2,
`.live-spec/profile.md` in full, and `~/.claude/playbook/personal/profile.md`'s `## Language` section
directly on disk.

## Second pass (2026-08-18, against d432fca9) — ALLOW

Fix commit `d432fca9` closes both findings from the first pass:

- **Finding 1 closed.** `SKILL.md`'s rule-15 bullet (line ~431) now reads: *"Never the contrast frame
  (rule 15, ... — Home: personal profile `language.no-contrast-frame`). Never name a thing by denying
  its neighbour (an em-dash or comma leading into the denied alternative, and the parallel Russian
  shapes). Say what the thing IS in its own sentence. The linter's scissors check holds the floor..."*
  — read directly on disk. The mechanism sentence is back verbatim, word-for-word identical to the
  text that stood before 99050f5 (checked against `git show 99050f5` again). The section's own promise
  ("a reader meets [these rules] even without loading the file", line 427) now holds again: a reader of
  SKILL.md alone gets the shapes and the rewrite instruction, not just a pointer.
- **Finding 2 closed.** Both pointers now read "Home: personal profile `language.no-contrast-frame`"
  — checked in both `SKILL.md` (line 431) and `writing-register.md` (line 93), identical wording in
  both files. This matches how the rest of the pack names that file (TEST_MATRIX M-233: "the law's
  home named (personal profile ...)"), and disambiguates it from `.live-spec/profile.md`, the
  in-repo host profile confirmed (again, directly, this pass) to carry no `language.*` keys. The key
  name itself, `language.no-contrast-frame`, is the current one — verified directly against
  `~/.claude/playbook/personal/profile.md`'s `## Language` section, which is where the law's own text
  actually lives; M-233's `no-scissors` name is the law's retired name, so it was not copied verbatim,
  only its "personal profile" framing was.

No new findings on this pass. Checked: neither file gained an orphaned fragment or a grammar break
from the fix (read both changed regions in full, not just the diff — `git diff HEAD~1` for
`d432fca9` shows only the two additions, 5 insertions / 2 deletions total across both files); the
calque pointer (finding 3, first pass) and the no-orphaned-fragments finding (finding 4, first pass)
were untouched by this fix and still hold as read the first time.

Byte counts (both files, whole-file `wc -c`, at each commit in the range):

| file | before 99050f5 | after 99050f5 (first-pass state) | after d432fca9 (now) |
|---|---|---|---|
| `skills/communicator/SKILL.md` | 45,985 | 45,646 | 45,839 |
| `skills/communicator/references/writing-register.md` | 10,478 | 10,212 | 10,216 |

Verdict: ALLOW. Read for this pass: `git show d432fca9` in full, the complete current text of both
files, and re-confirmed `.live-spec/profile.md` and `~/.claude/playbook/personal/profile.md` on disk
unchanged since the first pass.
