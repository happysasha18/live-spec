## The completeness pass — run before declaring a section done

Ask each question out loud; a "no" or "don't know" is a gap to fill or mark ⟨DECIDE⟩.

- **Entities:** Is every domain noun defined once in the glossary? Does each measure carry a unit + valid
  range? Does each entity with a lifecycle list its states?
- **Transitions:** For every state, what action leaves it, and who triggers it? Is there a state with no
  exit?
- **Invariants:** What must never happen here (safety)? What must eventually happen (liveness)? Is each
  one stated explicitly?
- **Composition:** Does this surface carry state? Under which of the canonical axes (view / mode / tier /
  viewport size / persistence-reopen / concurrency / every other live surface) is it shown? For each, is
  its state still visible and reversible? Is the transition's effect (preserve / reset / block) stated? If
  it persists state, is the older-stored-value × current-code case handled? For every other surface that
  can be present at the same time — a sibling on the screen, the surface one step before or after in the
  flow — is this surface's behaviour stated while that one is present?
- **Facets (feature door):** Did the facet sweep run — does every entry of the canonical facet list end
  in a spec sentence, decided or `[default]`-tagged and reported?
- **Naming:** Is anything in this section also referred to by another name elsewhere? Unify it.
- **Single source of truth:** Does any other document in this repo also claim to be the spec or the matrix
  ("source of truth")? If so, demote it to a pointer — two docs claiming authority is undefined when they disagree.
- **Honesty:** Is any claim here something the system can't actually deliver, or a guess dressed as a fact?
  Mark it ⟨DECIDE⟩ or cut it.
- **Readability (human-first, product language):** Does each case name its situation in plain words a
  non-author grasps in one read? Are the criteria phrased in product words a person would say, with the
  keywords in lowercase italics and no all-capital words outside a code anchor? Are the codes at line-*ends*,
  never opening a criterion? Is there any edit-history note in the prose that belongs in the JOURNAL? Does
  the spec open with a preamble and a glossary?
- **Shape (requirements genre):** Does every requirement carry a Context block, a one-sentence User Story,
  and criteria grouped into named cases, numbered continuously through the requirement? Does
  `guardrails/check-requirement-shape.py` pass? Is every spine item present inside the requirements or the
  glossary? Does the generated code-to-location table match a fresh `scripts/build-index.py` build, with
  `guardrails/check-index-generated.py` green? After a restructure: is the anchor set identical to before
  (or every delta named)?

