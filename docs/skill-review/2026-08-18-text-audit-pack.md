# Skill review — text-audit-pack

SKILL-REVIEW

Skill: text-audit-pack

Date: 2026-08-18
Reviewer: skill-creator (Anthropic)

Verdict: ALLOW-WITH-NOTE — a genuine, first-time review of a new skill; one non-blocking wording
observation, no loadability or scoping defect.

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
