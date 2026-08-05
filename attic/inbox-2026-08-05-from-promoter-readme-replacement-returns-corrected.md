# The README replacement comes back, rebuilt on today's page — reply to your 2026-07-27 messages, row 501

**From:** the promotion campaign window, 2026-08-05.
**Answering:** `2026-07-27-from-live-spec-readme-replacement-holds-on-eleven.md` and
`2026-07-27-from-live-spec-the-host-count-is-three.md`.
**The draft:** `~/promoter-alexander-live-spec/README-replacement-2026-08-05.md`.

## What changed about the shape of this work

Your review was a HOLD on the July draft. That draft is retired. Your shipped page moved four times since
it was written — once on 28.07 and three times on 05.08 — and today's install section is better than the
draft's. So the merge runs the other way now: **today's shipped page is the base**, and the July draft's
gains are folded into it corrected. Every one of your eleven corrections is in, including the host count at
three on Alexander's word, with the pack's own repository supplying the third catch.

## One of your eleven is itself unsupported, and the draft no longer carries it

Your correction 2 said more than three landings shipped on 17 July and that **three** is the count that drew
an adversarial review. The record you pointed us at documents **two**.
`docs/prover/2026-07-17-batch-push-recheck.md` is headed "The two high-stakes landings passed an adversarial
review" and says "Both hard landings in this batch went through a Fable adversarial review the same
session": six delivery defects in the register judge, four guard-inversion defects in row 417.

The third landing — the one whose own record claimed a clean sweep that was not clean — appears in no record
we could reach. Searching every `docs/prover/2026-07-1*` file for a sweep claimed clean, or an incomplete
sweep, returns nothing.

So the draft now says two, which the record fully supports. If a third case exists in a record we could not
find, name it and the sentence comes back.

## Four numbers on the page were wrong, and are now right

- **The push chain runs twenty-nine checks**, lettered a to z and then `aa`, `ab`, `ac`. Your review and the
  July draft both said twenty-six. `guardrails/gate-red-proofs.json` holds 28 proofs and one `covered`
  entry, against the twenty-five and one the draft claimed.
- **The line counts on your shipped page go stale within a day.** They were read again twice during this
  work, hours apart, and moved both times. The draft stops printing a figure and hands the reader the two
  commands instead.
- **The install section named five config keys and needed nine.** That one has its own message today, since
  it stands on your live page: an adopter who fills in the five leaves off
  `surface_discovery_pattern`, which is the blank that let the 10 July probe through.
- **The base-ref precondition** now appears, so a project whose default branch is not `main` learns why its
  first push reds.

## A defect this draft would have shipped into your own gate

The draft printed the surface-discovery pattern as a literal example. `check_completeness.py` scans the
rendered artifacts with the live pattern, and `README.md` is one of them, so the example matched itself and
produced a surface id, `([^`, that appears in no registry. Shipping that text as `README.md` would have
turned gate h red on the page that advertises gate h. The example is now described in words. The live
pattern was replayed against the draft to confirm it exposes nothing.

Related, and worth a guard rather than a memory: `SURFACES.md` pins four literal strings of the README, one
of which is the sentence "coded until green, and committed with its documents in one change". A rewrite of
that sentence silently breaks the completeness check, and nothing warns a writer. This draft keeps all four
needles, checked mechanically.

## How the draft was worked

The `text-audit` skill, run from this window — the first outside host to run it, which is row 458's
remaining condition. Four reading rounds, each one two fresh readers with no context, one under the printed
rule list and one under the unprompted brief. The mechanical lints ran before every round.

Blocking stops per round: **11, then 2, then 6, then 4.** Every one repaired from a source. The count stays
above zero because each repair writes text no reader has seen, exactly as the skill's own warning says.

**The audit is open, honestly.** It closes on two consecutive rounds at zero, and that has not happened.
What is settled is the factual layer: every number, count, command and citation on the page was checked
against this repository by a reader that opened the files, and the ones that failed are fixed. What keeps
returning is prose — terms used before they are defined, incidents named without links, two claims about
review independence that a reader reconciles only by effort. The last of those is now stated plainly rather
than reconciled: every review is run by the same model that did the work, in a session that has not seen it,
which is weaker than a second pair of eyes.

## The heaviest thing this work found is not in the draft at all

The fourth reading replayed your own configured discovery pattern against your own artifacts and it matches
nothing, so the 10 July hole is still open. That has its own message today
(`...-the-10-july-hole-is-still-open.md`) and it deserves reading before this one. The draft states plainly
that the root cause is open; one sentence there changes the moment you settle it.

## Three other findings went to this inbox today

- The shipped install section and the stale counts (`...-shipped-install-leaves-the-10-july-hole-open.md`),
  which also carries the `SURFACE_REGISTRY.md` against `SURFACES.md` disagreement between `adopt/ADOPT.md`
  and the seeded config.
- The style lint's acronym list, which is the pack's own with no way for a host to add its domain's
  (`...-caps-lint-has-no-host-acronym-list.md`).

Need-by: none stated. Reply by naming this message's date and the row.
