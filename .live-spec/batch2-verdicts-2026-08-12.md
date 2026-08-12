# Stage-2 batch 2 — rule 32, the release-tier rule — 2026-08-12

Root: the accepted plan (his «принято» 2026-08-11 21:22), stage 2 recipe S1–S5; the queue runs
by price (his word 2026-08-09 11:22).

## Batch choice

Batch 1 took rule 7, the second rule by day-1 census price, because the top rule, rule 31, carries
Alexander's open word on the two senses of "owner" (ROADMAP.md row 536, open since 2026-08-05;
NEXT_STEPS.md line 29 states the fallback: absent his word, the next rule by price). Rule 31 still
holds no answer, so batch 2 falls through to the rule after rule 7 on the same price list: rule 32,
2,205 bytes by the day-1 census, unchanged from a live re-measurement (`.live-spec/batch2-s1-rule32-2026-08-12.md`).

## Verdict lines, one per step

- **S1 (inventory).** Commit `0bf9844`. Rule 32, the release-tier rule (SPEC INV-217), body
  `skills/live-spec-base/SKILL.md` lines 555–579 at 2,205 bytes, re-measured against the live tree
  and matching the census figure exactly, no drift. Ten requirements, each quoted verbatim with its
  addressee — mostly the releasing session (assigns the number, classifies the tier, writes the
  major's `MIGRATION.md` chapter, makes the minor-versus-major call unassisted) and the host that
  takes a release (does nothing on a patch, re-runs its catch-up walk on a minor). Surfaces: one
  pinning test file (`tests/test_release_tier_rule.py`, all 7 functions), one incidental hit
  excluded (`tests/test_description_field.py`, a bare code mention, no assertion on this rule); ten
  `PRODUCT_SPEC.md` anchors; two `ARCHITECTURE.md` anchors, one already drifted (`:553` pointing at
  a line the rule no longer opens on, the live opening is `:555`) — found and left for the pin-drift
  script's own owner, not repaired here; four `TEST_MATRIX.md` anchors; one other-skill citation
  (`skills/build-pipeline/SKILL.md:471`); zero living `docs/` hits; 21 historical `docs/` files, 51
  line-hits. Page: `.live-spec/batch2-s1-rule32-2026-08-12.md`.
- **S2 (rewrite).** Commit `0ac3b19`. Body 2,205 → 1,449 bytes (−756), lines 560–574 of the current
  file. All ten requirement sentences carried; the cut came from the worked-example framing and
  surrounding prose around them, not from the requirements themselves.
- **S3 (clean-context check, fresh Sonnet).** Commit `deba91b`. Verdict: the rewrite stands. Ten of
  ten requirements found word-for-word, no MISS; every prohibition ("held by no machine," "never
  blocks a lane") binds the same actor in the same case as before; no contrast frame of the banned
  "X, not Y" shape; `python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md` exits
  0. Page: `.live-spec/batch2-s3-rule32-check-2026-08-12.md`.
- **S4 (surfaces).** Commit `4b20af9`. Five `ARCHITECTURE.md` pins repointed for the rule's
  fourteen-line shrink and the cascading shift it carries through later rules' line numbers: the
  ladder pin 637→629, the defaults-table pin 694→686, the design-sync row pin 691→683, rule 35's
  pin 607→599, and rule 32's own pin — which S1 had found already drifted at `553` — corrected to
  `555`, the line the rule opens on today. Every `PRODUCT_SPEC.md`, `TEST_MATRIX.md`, and
  `build-pipeline` citation re-checked against the new text and confirmed to still read true.
- **S5 (closing measures).** Rulebook volume by the campaign's own command: opening 72,929 bytes →
  72,173 after rule 32's rewrite (−756, S2 alone) → 72,466 after the folded restorations (+293:
  the rule-30 retirement note at the rulebook's head and rule 7's three small findings restored,
  commit `e17eea9`; row 593's one-home dedup for the rule count, commit `dc78db9`, touches no file
  under `skills/live-spec-base/`, so it moves this figure by zero). Re-measured live with the
  campaign's exact command:

  ```
  { find skills/live-spec-base -name '*.md' -not -name 'README.md' -print0 | xargs -0 cat; cat ~/.claude/live-spec/profile.md; } | wc -c
  ```

  → **72,466 bytes**, matching the figure carried above exactly. No drift between the recorded
  figure and the live tree.

## The batch's own test

The plan requires the rulebook's volume at close to stand below its volume at open: 72,466 <
72,929. **Passes**, a net fall of 463 bytes across the batch (−756 from rule 32's rewrite, +293
from the folded restorations that queue rows 590, 593, and 595 required).

## Who the rule reaches

The releasing session at every release: assigning the number, classifying patch versus minor
versus major, writing a major's dated `MIGRATION.md` chapter, and making the minor-versus-major
call itself — a judgment the rule states no gate holds. The host that vendored a prior version:
doing nothing on a patch, re-running its catch-up walk on a minor, changing what it already carries
on a major. The push/release gate machinery, told this call never blocks a lane. Anyone who later
audits or reconsiders the 2.0.0 release's number, pointed at its own cited boundary case.

## Queue rows closed

Five: 590, 591, 592, 593, 595 (NEXT_STEPS.md line 32, all marked *done* in `ROADMAP.md`). Two of
these — 591 (the stale `M-313` build-pipeline home in `TEST_MATRIX.md`) and 592 (the
compaction-every-pass guard test pinned to a bare code mention instead of its own sentence) —
closed alongside this batch by a separate small-items-sweep commit, `7521782`, run before batch 2's
own S1 opened. The other three closed inside this batch's own folded commits: 590 (the retired
rule-30 number named at the rulebook's head) and 595 (rule 7's three small findings restored) in
`e17eea9`; 593 (the rule-count copies pointed at one home) in `dc78db9`.

## Carried forward

- Rule 31 still waits Alexander's word on the two senses of "owner" (ROADMAP.md rows 536, 539,
  open since 2026-08-05).
- The day-1 census's next-priced rule below rule 32 that no batch has yet taken is **rule 29**
  (2,138 bytes, SPEC INV-152 — the parked-item re-derivability rule) — the highest remaining figure
  under 2,205 once rule 31 (held) and rule 7 (batch 1, 5,477 bytes) are set aside. Batch 3 starts
  there.
