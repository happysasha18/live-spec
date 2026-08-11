# Skill review — the install repair across eight files (plan v3, step R1)

`SKILL-REVIEW`

Skills: product-prover, spec-author, text-audit, publish, test-author, feedback-intake,
feedback-collector, and communicator's references/words.md
Date: 2026-08-11
Reviewer: a fresh reviewer raised for this review alone, with clean context. It did not author the
repair, and it wrote no file. Base rule 33 asks for that freshness. The 2026-08-09 attempt's review
was never filed — it survives only in that session's transcript — and this record closes that gap
for the present round.

First verdict: blocked, on one clause. Line 12 of words.md reused "beside this one" where the
phrase resolves to the references/ folder, sending a reader into the wrong directory for the base
skill — the exact reader failure the 2026-08-09 finding 3 described. Four pages also made loading
live-spec-base mandatory while pointing only at the public repository address, although an install
places that skill one folder over.

What the review confirmed, each by hand:
- Six of the seven 2026-08-09 findings closed as claimed. Communicator's body stands untouched at
  499 lines with rule 8's test sentence and rule 14's line shape intact. Every page names the
  public address github.com/happysasha18/live-spec. No paragraph classifies docs/ wholesale; each
  page names its own docs pages by side. No new backticked directory name entered any page.
- Every named pack path was verified on disk, on both trees. One exception: docs/deltas/ exists
  nowhere and its sentence was ruled redundant.
- The eight pages agree with each other and with words.md on every directory two of them name.
  PRODUCT_SPEC.md reads as the host project's on all five sites in the diff.
- Style held: register findings 0 on all eight files, style counts identical to the versions
  before the repair, longest new sentence 22 words, no contrast frames, no coined terms.
- The scoped tests passed, 86 of 86. The full suite showed 3 red, all from other units' known
  state at the time (the architecture record owed for R6, and the installed copies trailing the
  working tree until the same-day sync).

Repairs ordered and applied the same morning: the words.md clause names its anchor plainly; the
four GitHub-only pages say live-spec-base sits beside this skill's folder after an install; the
words.md locating paragraph covers its own page's pack paths, naming templates/ and adopt/ as pack
directories an install copies nowhere; the redundant docs/deltas/ sentence is gone; text-audit's
second "beside this one" names its anchor too.

Standing findings this record hands to other owners:
- build-pipeline and design-reviewer still place PRODUCT_SPEC.md in the pack repository, against
  the other nine pages — a follow-on unit of the same class (R1b).
- No machine reads any locating paragraph, so this repair class ships ungated; a check proposal
  waits as a decision candidate under the campaign's rule 2, which reserves new checks for
  Alexander's word.
- Minor items recorded and accepted: communicator's conditional pointer to words.md, the
  unlocated script names inside text-audit's tool list, the third-tree examples on test-author and
  publish pages.
