# Skill review — the design-review skill defines its own words and names the files its steps need

SKILL-REVIEW

Skills: design-reviewer.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes — land it. No blocking finding. The change adds a definitions block, names the files
and numbers seven steps needed, and brings every sentence under the 25-word cap. It removes no
instruction. Four places restore a rule the cited code already carries, and each one is named below.
Four findings that would change an instruction are recorded here and left standing, for the human's
word.

The review returned nine non-blocking findings, three of them worth fixing before the landing commit.
All three were verified and fixed, and they are recorded under "What the review sent back".

## Why it was worth a change

A readability audit read this file twice with fresh readers. One reader held the 38-item stop list at
`skills/text-audit/references/reader-prompt.md`. The other held nothing and checked every named file,
script, code and number against the tree. The two sets overlap on eleven items and neither contains
the other.

Pass A returned 92 stops; 73 stand. Pass B returned 18; 17 stand. Seven of the confirmed stops named a
step a reader cannot carry out from the page alone. A session that loads a skill acts on it. A step it
cannot perform is skipped with no trace, and the output still looks complete.

## What changed

**A "Words this skill uses" section near the top.** It defines element, role sentence, same-kind
group, grouping, class, surface, surface registry, host, spec-delta, landing, station, lens, queue
row, taste call, architecture node, pins, decision archive, the verb red, and the human. A closing
paragraph says what the `INV-`, `E-` and `M-` codes are and where they resolve. It expands `M-6`,
`MINOR`, and the three prover review modes. It states that every path on the page is relative to the
root of the repository under review.

Every definition was taken from a source in the tree: the glossary of `PRODUCT_SPEC.md`, the same
section in `skills/product-prover/SKILL.md`, base rule 1, and the page's own sentences.

**The header banner.** It ran sixteen rule slogans together in one sentence. One of them,
"junior/senior split", named no base rule. The base carries thirty-five rules and the list was unmarked
as partial. The banner now names the base file, the rule count, and the four scopes of the settings
ladder, in the same shape `skills/text-audit/SKILL.md` already uses.

**A renamed heading.** `## Work that belongs elsewhere` headed two different sections. The second is
now `## When to stay silent`. The first keeps its title, which `guardrails/check-skill-loadability.sh`
requires.

**Addresses on seven steps.** The page now names `SURFACES.md`, `docs/prover/`, `docs/decisions/`,
`skills/product-prover/SKILL.md`, `skills/build-pipeline/SKILL.md`, `ROADMAP.md`,
`guardrails/node-file-cap.json` with its default of two nodes per file, the command that runs
`guardrails/node_growth_counter.py`, and `.live-spec/profile.md` for the host's own loop cap. The
record's outcome values are a table, with `answered(alike)` and `answered(different-by-intent)`
written out.

**Plain sentences.** Every sentence is now 25 words or fewer. Figurative phrases gave way to plain
ones: "carves the map", "fly the thing home", "cadence keys to", "is noise", "sees the work out the
door". Five style-lint findings cleared: two all-caps ordinary words, two blocks opening with what a
thing is not, and one contrast frame.

## Four rules restored, and one reason reworded

**The round counter's reset.** The loop section cites INV-154. That code's criterion R70.4 carries four
clauses and the page carried three. The fourth, "resetting when a fresh pass opens", is now on the
page. Without it a long-lived spec halts for good after its third declaration.

**The split proposal's trigger.** The node-growth section cites SPEC INV-233. That code's criterion
R244.4 owes the split proposal when a file's node count sits at its cap. The page stated only that the
counter reds an increase. Both facts now stand, and the cap file is named.

**The render-time assertion.** The page promised that "the render-time guardrail" would hold a
declared class "mechanically forever". R260.5 leaves the page-wide assertion to the products the pack
serves. The page now says the pack ships the rule and the prover lens, and that the assertion stays
the host's own to build.

**The older records.** R68.4 leaves records written before the review-record class was declared
unreshaped. The page now says so, since 2 of the 15 files under `docs/design-review/` carry the
outcome column the page describes.

**The push-gate reason.** The page said the `M-6` push-gate re-check "is its own mode". The prover
names three review modes and no fourth. The rule is unchanged — the design review stands down at the
push gate — and the page now states it flatly, pointing at the prover's own cadence list.

## What the review looked at

**Does the summary line still trigger correctly?** The frontmatter description is untouched. The
change sits in the body.

**Does the body still hold together?** Yes. The new section defines terms the body already used, so
nothing is stated twice. Two restatements the review did find were cleared: the never-holds-a-landing
property was stated twice inside one paragraph, and once as a colon tautology in the closing list.
Each now says it once.

**Could the change be read as permission to skip a step?** No step was softened. The two restored
rules widen when the reader owes work rather than narrow it. The renamed heading keeps both lists
whole.

**Does it instruct anything new?** It names files, numbers and commands the steps already implied.
That is a definition, and it makes an existing step performable.

**Is the words section accurate against the tree?** Spot-checked. `SURFACES.md` opens "# Surface
registry". `docs/pipeline.md` heads its third step "Station 3 — prover review of the spec".
`guardrails/node-file-cap.json` holds `"default": 2`. `skills/live-spec-base/SKILL.md` carries 35
numbered rules, and its ladder reads "session beats host beats personal beats package default".
Base rule 1 lists a taste call beside a threshold and a policy. The prover's review-modes section
names exactly FULL, CROSS-LINK and FEATURE-FIT. The glossary of `PRODUCT_SPEC.md` supplied host,
landing, decision archive, spec-delta, surface registry, and architecture node word for word.

## What the review sent back

Three findings were fixed before this record was finished. Each was verified against the tree first.

**The path-scope sentence was wrong.** It read "Every path on this page is relative to the root of the
repository under review". Most paths on the page name a file in the pack's own repository.
`adopt/install-ratchet.sh` vendors only `guardrails/check-freeze.sh` and
`guardrails/spec-coinages.json` into a host, so a session reviewing a host repo would have run
`python3 guardrails/node_growth_counter.py` against a file that is not there. The page now splits the
two repositories by name, and the counter is run from the pack's own root.

**`MINOR` was defined as a `0.x.0` bump.** The pack sits at 4.3.0, so its next minor is 4.4.0. The
loose form came from `skills/build-pipeline/SKILL.md`; `skills/product-prover/SKILL.md` writes
`x.Y.0`. A glossary is where a reader settles a notation, so the page now carries the exact form.

**The MINOR audit's passes were miscounted.** `skills/build-pipeline/SKILL.md` lists the full design
review as running *plus* that audit's three passes. The page implied it was one of them. It now runs
beside them.

Two further points were taken. The banner's copy of the base's rule count was dropped, since no gate
holds that number here and it goes stale the day a thirty-sixth rule lands; the banner points at the
base file instead. One duplicated sentence was removed from the echo channel, where the record section
already owned the fact.

Four review findings are recorded and left: the skill's `README.md` still measures 16 census findings
and is its own delivery; the two wrong citations below now have identified right answers; and the
words block holds nineteen definitions.

## Findings

None blocking. Four are recorded and left standing, since repairing any of them would change what the
skill instructs anyone to do.

1. **The record's version line.** The page has the record open by naming the design-reviewer skill
   version. R273.2 (INV-178) requires a record's version line to name the pack version. They agree
   today at 4.3.0 and will part at the next skill-only bump.
2. **The project kind's own form.** R61.6 requires the design review to run in the project kind's own
   form. The page carries R61.5 beside it and drops this one.
3. **`[INV-30]` on the batched-question path.** INV-30 is the verify-by-deed visitor walk and the feel
   pass. The decision-page law the sentence describes is R7.1, under `[E-22, INV-4]` — the two codes
   already beside it. The repair is a deletion.
4. **`(SPEC INV-18)` on the curated producer list.** INV-18 heads "Every facet ends as a spec
   sentence"; its criteria govern decided and `[default]`-tagged facet sentences. The curation rule
   the sentence quotes is R52.5, under `[T-13, INV-226]`.

Which requirement a sentence pins to is an authority-anchor decision, held by
`guardrails/check-authority-anchor.py` and the spec path.

Two smaller gaps stay open because no answer exists in the tree. The page does not say what happens to
a fourth strong signal inside one pass, and it does not define what makes a re-derived ask match an
open recorded one.

One observation for a later pass. `guardrails/rule-census.json` still records this file at 72
findings, and it now measures 0. The findings-bound gate passes and prints "fell". Lowering that
ceiling belongs to whoever next owns `guardrails/`.

## Checks run

`python3 scripts/rule-census.py skills/design-reviewer/SKILL.md` — 0 findings, down from 72. Longest
sentence 25 words, down from 92.

`python3 scripts/preshow-register-lint.py skills/design-reviewer/SKILL.md
docs/skill-review/2026-08-05-design-reviewer-readability.md` — exit 0.

`python3 scripts/spec-style-lint.py --tier full skills/design-reviewer/SKILL.md` — 0 errors, down
from 5.

`sh guardrails/check-skill-loadability.sh` — OK, 11 skills load.

`python3 -m pytest tests/test_config_health.py tests/test_traceability.py -q` — 208 passed, including
the check that the repository copy and the installed copy hold the same bytes.

The six tests that pin this skill's wording — `tests/test_design_reviewer.py`,
`tests/test_node_growth.py`, `tests/test_review_record_class.py`,
`tests/test_second_sibling_intake.py`, `tests/test_paired_transition.py`,
`tests/test_gesture_overlay_parity.py` — pass.
