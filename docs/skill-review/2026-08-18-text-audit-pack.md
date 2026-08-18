# Skill review — text-audit-pack

SKILL-REVIEW

Skill: text-audit-pack

Date: 2026-08-18
Reviewer: skill-creator (Anthropic)

Verdict: ALLOW (second pass, after the fix in 02f63e46 — see "Second pass" below). The first pass's
ALLOW-WITH-NOTE and its findings stand as read; they are not erased, only closed.

## First pass (2026-08-18, against 34f02abe) — ALLOW-WITH-NOTE

First-pass verdict: ALLOW-WITH-NOTE — a genuine, first-time review of a new skill; one non-blocking
wording observation, no loadability or scoping defect.

## What changed

New skill. `skills/text-audit-pack/SKILL.md` is the pack-side adapter left behind when the text-audit
body moved to its own repository (`github.com/happysasha18/text-audit`) on 2026-08-18. It is written
against `skills/product-prover-pack/SKILL.md`'s established adapter shape (same frontmatter pattern,
`requires:` pin, version 5.0.0 matching the rest of the pack).

## Findings

Read the whole file, not the diff — it is new.

1. **Frontmatter loads and scopes correctly.** `name: text-audit-pack` matches its directory.
   `description` states the trigger plainly ("Load it whenever text-audit runs inside a live-spec
   project") and the negative scope ("It audits nothing itself") in the same sentence — a reader
   deciding whether to load this page does not need to open the body first. `metadata.version: 5.0.0`
   matches every other skill in the pack; `requires: text-audit >= 1.0.0
   (github.com/happysasha18/text-audit)` follows the exact shape product-prover-pack's `requires:`
   line uses. Folded as-is — no change needed.

2. **`guardrails/check-skill-loadability.sh` originally reported no "Work that belongs elsewhere"
   section (row 80) — a real defect, not a formality.** The file as first written had no such
   section; product-prover-pack satisfies the same gate only incidentally, through a pin-map table
   cell that happens to name a prover lens called "Work that belongs elsewhere," not through a real
   scoping section. text-audit-pack now carries a genuine one (added this review pass, before line
   30): it names the three things a reader might mistake this page for — running the cold-read loop
   itself, the product-prover pass, the design-reviewer pass — and states plainly that the page
   cannot run the audit loop alone, without the external skill's own SKILL.md loaded beside it. This
   is not a copy of product-prover-pack's table trick; it is written for what this specific page can
   and cannot do. Folded.

3. **Is a step here executable without the external body?** No step in this page is meant to run
   alone, and the page says so twice: once in the new "Work that belongs elsewhere" section, once in
   the opening paragraph ("An audit run inside a live-spec project reads the audit skill's own
   SKILL.md first and this page beside it"). The lint table (`## The mechanical lints this pack
   declares`) is host-contract data the EXTERNAL skill's Step 1 consumes via `.text-audit/lints.json`
   — it names commands, it does not itself invoke them, and the table's own framing sentence says as
   much. Nothing in this page could be mistaken for a self-contained procedure. Folded — no change.

4. **Non-blocking wording note: "one strong and one cheap reader" in "What a cheap reader means run
   inside this pack."** The section correctly states the CURRENT mechanism first (both of text-audit's
   two readers, prompted and unprompted, are cheap readers — verified directly against
   `/private/tmp/live-spec-textaudit/out/SKILL.md` line 87: "both readers of a round are cheap
   readers"), then cites rule `74ef247` for the word "cheap" itself. Read in isolation, "rule 74ef247,
   which first split a round into one strong and one cheap reader" could momentarily read as claiming
   today's loop still runs a strong/cheap PAIR, when the pack's own preceding sentence already says
   both are cheap. Checked against `git show 74ef247` directly: that commit did introduce a strong+cheap
   split on 2026-07-29, and the loop has since moved to two cheap readers (prompted/unprompted) — the
   citation is historically accurate as the term's origin, not a claim about today's roster. Not
   blocking: a reader who reads the two sentences in order (as written, in the order they appear)
   gets the right mechanism before hitting the historical aside. Left as a note rather than a required
   fix, since resolving it would mean rewording a sentence that is the owner's own word from
   2026-08-18, quoted for a reason.

5. **`docs/language-defects.md` cross-reference (`## Pack paths`) is a live, one-way pointer.** The
   page says plainly that a reader following that citation "now leaves the pack" — an honest flag
   rather than a silent dangling reference. Not a defect; the page could not fix this without editing
   `docs/language-defects.md` itself, which is out of scope for an adapter page.

No finding blocks. `check-skill-loadability.sh` passes (11 skills, all load, named, versioned,
negative-scoped) after finding 2's fix; re-run and confirmed green this pass.

## Second pass (2026-08-18, against 02f63e46) — ALLOW

Commit `02f63e46` edited this page again, after the first pass closed, to clear two census-ratchet
lints my own "Work that belongs elsewhere" section (finding 2, first pass) had tripped: a
`scripts/spec-style-lint.py` scissors catch, and one sentence over the 25-word cap
(`scripts/rule-census.py`). Neither lint was live when the first pass ran; both are read here.

What changed, read directly against `git show 02f63e46 -- skills/text-audit-pack/SKILL.md`:

- The first "Work that belongs elsewhere" bullet lost its trailing clause: "...loaded first, not
  this page;" became "...loaded first;". The struck words named what the bullet is not (this page);
  the surrounding sentence already carries that meaning without them — the bullet still says the
  external skill's own body runs the read, "loaded first," inside a list whose own lead-in sentence
  ("Skip it for:") already scopes every item as something this page does NOT do. Nothing the reader
  needs is gone.
- The paragraph "This page alone cannot run the audit loop: without... starts none, and its 'cheap
  reader' definition has no loop to apply to." (36 words, one sentence) split into three sentences at
  the same clause boundaries the colon and first "and" already marked: "This page alone cannot run
  the audit loop." / "Without the external skill's own SKILL.md loaded beside it, its lint table
  names commands but starts none." / "Its 'cheap reader' definition has no loop to apply to." Every
  clause survives, in its original order, with its original wording; only the joins between them
  changed from colon/comma-and to full stops.

Re-read the whole page in full after the edit, not just the diff hunk (the same standard the first
pass held itself to) — checked for an orphaned fragment or a dropped connective at either cut point.
Both hold: the first bullet still parses as a complete clause inside its list, and the three-sentence
version of the second paragraph reads in the same order, making the same three claims, as the
36-word original. No meaning is lost, softened, or added; only the punctuation carrying it changed.

The five findings of the first pass are untouched by this edit — finding 2's fix (the "Work that
belongs elsewhere" section itself) is what got rephrased here, not undone, and findings 1, 3, 4, 5 sit
outside the edited lines entirely (verified: `git show 02f63e46` touches only the two spans above).

Re-ran this pass: `python3 scripts/spec-style-lint.py skills/text-audit-pack/SKILL.md --tier full` —
OK, no scissors; `python3 scripts/rule-census.py skills/text-audit-pack/SKILL.md` — 6 long sentences
(the pre-existing debt named nowhere as this page's own, all outside the two edited spans), 0 style,
matching the file's recorded ceiling exactly; `bash guardrails/check-skill-loadability.sh` — still 11
skills, all load.

Verdict: ALLOW. Read for this pass: `git show 02f63e46` in full, the complete current text of
`skills/text-audit-pack/SKILL.md`, and re-confirmed finding 2's section still states what it stated
in the first pass.
