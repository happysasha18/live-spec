# Eval — spec-author (SPEC E-19)

## Scenario

Both arms get the same task; the with-skill arm first reads `skills/spec-author/SKILL.md` and the
`skills/spec-author/references/` pages it points at, and works by them. Prompt (verbatim):

> Write the PRODUCT_SPEC.md section for this new feature of a photo-gallery web app: "clicking a photo opens a
> lightbox — the photo shown enlarged, with prev/next arrows".
> Context you know about the app: it shows a folder of the user's photos and already ships two views, a
> compact grid and a detailed list.

**Prompt history.** The first run's prompt (2026-07-05) enumerated facet hints (phones, two windows,
renamed/deleted files) and contaminated the bare arm's MET BARE scores; de-contaminated at the
2026-07-06 push-gate re-run per the authoring rule (evals/README.md) — the wish sentence plus
discoverable context only, no failure modes named. First-run scores below that leaned on those hints
are marked; the re-run's scores are the honest ones for the facet criteria.

## Criteria

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| No silent micro-decisions: every invented choice is ⟨DECIDE⟩-asked or `[default]`-tagged and BATCHED back (INV-5/INV-18) | RED — ~10 behaviours decided silently (no-wraparound, resolve-at-press, per-window state, close set…), zero tags, zero questions | GREEN — one genuine ⟨DECIDE⟩ asked (photo identity), five `[default]`s tagged in place and surfaced as one batch |
| Regression fences open the delta when a live surface is touched (T-14) | RED — absent | GREEN — fences first, with an honest note that citations need the real anchors |
| The delta closes with non-goals + a success measure (INV-20/21) | RED — absent | GREEN — both present, measure `[default]`-tagged |
| Facet sweep completeness: accessibility, performance envelope, visual hierarchy, empty/error/loading (T-13) | RED — a11y partial (keys only, no focus trap/contrast), no performance envelope, no hierarchy | GREEN — focus trap + contrast + alt text, preload envelope, hierarchy sentence |
| Composition across canonical axes stated explicitly (C-1), incl. persistence/reopen | MET BARE (view, two-windows, missing-source — prompt-fed; reopen covered) | GREEN — full axis walk incl. explicit mode/tier N/A |
| Use-case-first shape, anchors trail, index closes the doc | MET BARE (loader-fed: scenario prose + formal index) | GREEN |
| The fit walk (SPEC INV-29, added 2026-07-06): the journey lenses walked — arrival, where-next from every state, return visit, cross-entry, implied neighbour state, invited-next; trivially-closable holes closed AND written how; only genuine taste calls go out | RED (2026-07-06 push re-run) — edge cases yes, journey no | GREEN (same re-run) — explicit fit-walk section, holes closed and written how |

## The red

The bare run (bare run: 2026-07-05, Sonnet worker, zero tool uses — record
`docs/evals/2026-07-05-first-run/bare-spec-author.md`) wrote a structurally impressive spec — and
decided roughly ten product questions SILENTLY: no-wraparound at the ends, resolve-at-press-time,
per-window lightbox state, the close-trigger set — none marked, none asked, exactly the hole the Room
shipped through. It also skipped fences, non-goals, the success measure, the performance envelope, and
most of accessibility. The with-skill run (same day, record `with-skill-spec-author.md`) flipped every
one of those: the invented choices became one ⟨DECIDE⟩ plus five tagged `[default]`s surfaced as a
batch, fences opened the delta, the two closing sentences closed it.

## Re-run

One Sonnet worker per arm. Bare arm: the scenario + "do not invoke any tools or skills". With-skill arm:
"First read skills/spec-author/SKILL.md and every page under skills/spec-author/references/, and work
strictly by them" + the same scenario. BEFORE the next
run: de-contaminate the prompt (drop the enumerated hints; put the context in a small repo fixture the
scenario points at). Score per criterion; append the dated record to `docs/evals/`.
