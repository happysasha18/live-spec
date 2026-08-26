# Skill review — design-reviewer

SKILL-REVIEW

Skill: design-reviewer

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand; the
tool's own eval/iterate loop is out of scope for a pack-wide pass over 12 skills)

Verdict: no blocking findings; one genuine Progressive Disclosure gap worth carrying forward — the
skill has no `references/` at all while sitting on dense, growing content at 430 of the ~500-line
guideline, unlike its sibling communicator which already offloads that kind of weight.

## What changed

This is not a review of a code edit. It is the plan-mandated pack-wide skill-creator pass over every
working skill ahead of PLAN.md step 8 ("Релиз наружу"), and this record covers `design-reviewer` on its
own.

## Findings

1. **Frontmatter description** — passes, with a soft note. The `description` states WHAT precisely
   (check whether same-kind features behave consistently, flag ungrouped same-kind items the spec
   missed) and its most load-bearing behavioral fact (it holds no landing, every finding is a
   recommendation or a question — verified true throughout the body, see finding 3). WHEN is present
   ("after a spec is proven") but stays abstract next to the body's own detailed cadence table (FULL
   review mode, a surface add, feature intake's second-sibling exception, standing down at the push
   gate) — it does not name the concrete trigger phrases the way communicator's description does. This
   is not treated as a blocking gap: the pack's own routing (confirmed in `director/SKILL.md`, which
   dispatches to `product-prover-pack` by name from its own table rather than by phrase-matching a
   description) shows this skill is invoked by the pipeline's own station logic, not by an agent matching
   loose human phrasing against the frontmatter — so the abstract WHEN is consistent with how the skill
   actually gets loaded in this pack, even though a standalone reading of skill-creator's checklist would
   want more.

2. **Anatomy of a Skill** — the one real finding. The skill directory holds only `SKILL.md`, `README.md`,
   and `LICENSE` — no `references/`, `scripts/`, or `assets/`. Everything lives inline: four distinct,
   SPEC-code-dense lenses (the five-step similarity lens, the node-growth split proposal, the standing
   motion-parity lens, the standing named-part lens), the confidence-read and echo-channel mechanics, the
   loop-bounding and convergence rules, and the record-format table. None of that reads as clutter — it
   is all load-bearing — but it is also exactly the kind of material communicator's own review (finding 2
   above) found already offloaded to `references/` in that sibling skill: worked examples, rule
   provenance, and long tables. design-reviewer carries a comparable weight with no offload mechanism in
   place at all.

3. **Progressive Disclosure** — SKILL.md is 430 lines, under the ~500-line guideline but at 86% of it,
   with zero hierarchy into `references/` to absorb the next addition. Concretely, the worked-example
   incidents cited inline (the tlvphotos door-picture case, 2026-07-15; the landscape-phone caption case,
   2026-07-16) and the four lens definitions are strong candidates for a `references/` split the way
   communicator does it — a short pointer and the lens's operative steps stay in the body, the incident
   provenance and longer worked cases move out. This is not a violation as filed (the guideline is a
   rough line, not a hard cap, and 430 is still under it), but it is a real, checkable gap next to the
   sibling skill that already solved the same problem, and the next lens or incident added to this file
   has no offload path ready.

4. **Principle of Lack of Surprise** — passes. The description's central claim — "It holds no landing;
   every finding is a recommendation or a question" — was checked against the body rather than taken on
   the frontmatter's word: "The confidence read" section states a `confident` finding is written as a
   recommendation and a `likely` finding as a question, "How the answer closes the loop" states the loop
   "holds up no landing", and "When to stay silent" repeats "Never file a defect, never hold up a
   landing." No place in the body files a blocking defect or a red the way `product-prover` does. The
   description matches the behavior with no gap found.

5. **Writing style** — passes. Section and lens headers are imperative or descriptive without bare
   ALL-CAPS mandates ("Enumerate", "Describe by role", "Propose groups", "Check parity", "Fire the tight
   ask"), and the standing lenses are each grounded in a dated incident rather than asserted as abstract
   policy (the tlvphotos pinch-to-zoom case, 2026-07-15; the landscape-phone caption case, 2026-07-16).
   The worked examples double as the WHY for each lens, which is the pattern skill-creator asks for.

6. **Reference-file consistency** — trivially clean: there is no `references/`, `scripts/`, or `assets/`
   directory, so there is nothing to check for dead or orphaned links within the skill's own tree.
   Cross-pack, the body twice points at `skills/product-prover/SKILL.md` (lines 18 and 133, for the
   prover's Phase 1 extraction habit and its FULL/CROSS-LINK/FEATURE-FIT review-mode definitions) — a
   path that does not exist anywhere in this repository. This was checked rather than assumed broken: the
   sibling skill `product-prover-pack`'s own frontmatter states it binds "the external product-prover
   skill", and its body states outright that "the installed copy under `skills/product-prover/` is not
   tracked by this [repo]" — meaning the path only materializes inside a host project once the external
   skill is installed there, which is the pack's own established convention (the same convention
   `communicator/references/words.md` documents for cross-skill paths generally). The path resolves
   clean under that convention; it is not a dead link.
