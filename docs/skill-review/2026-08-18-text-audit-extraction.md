# Skill review — text-audit

SKILL-REVIEW

Skill: text-audit

Date: 2026-08-18
Reviewer: skill-creator (Anthropic)

Verdict: ALLOW — the skill left this repository; nothing of its body remains here to review as a
live artifact, and this record says so rather than reviewing a copy that no longer ships from here.

## What changed

text-audit moved to its own repository (`github.com/happysasha18/text-audit`), the same move
product-prover made on 2026-08-12/14. `skills/text-audit/` — `SKILL.md`, `LICENSE`, `README.md`, and
the four `references/*.md` files — is deleted from this tree entirely (`git diff origin/main --stat`
confirms seven deletions under `skills/text-audit/`, zero additions there). The extraction's own
record, `/private/tmp/live-spec-textaudit/out/`, holds the frozen copy that becomes the external
repository's first commit; that copy is not this repository's concern and carries no review
obligation here. `skills/text-audit-pack/` is the thin adapter left behind in its place, reviewed
separately (`docs/skill-review/2026-08-18-text-audit-pack.md`).

## Findings

1. **Nothing under `skills/text-audit/` is a "change" in the sense this gate normally reviews — it is
   a removal.** There is no instruction, procedure, or scope decision inside this repository's copy of
   the skill left to fold or reject; the body itself is gone. The only thing left to check is whether
   the removal is CLEAN — no dangling reference this repository's own gates would miss.

2. **Two generator dependencies on the removed body are cut, not left dangling.**
   `scripts/gen-language-consumers.py` and `guardrails/check-language-rules.py` used to build and
   drift-check `skills/text-audit/references/reader-prompt.md` and
   `skills/text-audit/references/human-prose-rules.md` on every run. Read both files directly: the
   generator functions that wrote into those two paths (`build_reader_prompt`,
   `render_human_prose_rules`, and their `outputs`/`SPLICED` entries) are removed, and
   `check-language-rules.py`'s reach in `scripts/check-registry.json` now names
   `docs/language-rules.md` / `docs/language-rule-coverage.md` instead of the two removed paths. Ran
   `python3 guardrails/check-language-rules.py` directly — OK, no reference to the deleted files.

3. **`ARCHITECTURE.md`'s `[node: text-audit]` pinned `skills/text-audit/SKILL.md:1`, a now-missing
   file — a genuine pin-drift bug, closed in this same push.** The node's responsibility line now
   states plainly that the loop's mechanics live outside this tree as of 2026-08-18; its pins
   redirect to `skills/text-audit-pack/SKILL.md` (frontmatter, the mechanical-lints section, the
   cheap-reader section) with the same "pins stand on the tracked adapter instead" framing
   `product-prover`'s node already used for the same situation. Verified with
   `bash guardrails/check-pin-drift.sh` — clean.

4. **`.live-spec/r5-rule-prices-2026-08-11.md` pinned five of text-audit's own numbered rules by exact
   line range — a second pin-drift surface the first pass missed, because it is not read through
   ARCHITECTURE.md.** Those five rows (the loop's five steps) have no line anywhere in this repository
   that still carries their text; they are retired from the price table and the per-rule section list
   rather than repointed at a file that cannot carry them, with a dated note explaining the removal
   and the new totals (53 rules / 44,067 combined price → 48 rules / 40,235). Verified with
   `bash guardrails/check-pin-drift.sh`'s r5 leg — clean, 48 range pins.

5. **The eight roster lists `TestPackListParity` enforces all name `text-audit-pack` beside the
   surviving `text-audit` entry, honestly worded** — see the combined review
   (`docs/skill-review/2026-08-18-textaudit-roster-additions.md`) for the five pack-skill rosters, and
   `PRODUCT_SPEC.md`'s glossary / `OVERVIEW.md` / `README.md` for the other three, none of which
   claims the skill still lives in this tree.

No finding blocks. What would have been silent breakage — a dangling pin, a generator writing into a
path that no longer exists, a roster claiming a body this repository does not ship — is closed by the
findings above, verified directly against the gates each one names.
