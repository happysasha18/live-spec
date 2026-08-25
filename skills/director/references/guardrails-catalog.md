# The four mechanical guardrails

The full catalog referenced from `SKILL.md`'s "Guardrails — the pipeline's mechanical enforcement" section. Each project
INSTANTIATES these checks for its own surfaces; the pipeline REQUIRES the check exists and is green.

- **Completeness** — a SURFACE REGISTRY + a render-scan test that fails if any user-facing surface is empty OR
  is rendered but not in the registry (so a new surface goes red until registered + asserted). No partial/
  stripped artifact can ship or be shown. Self-closing: the DOM is the source of truth, checked directly, with no hand-list to maintain.
  The family also holds **cross-surface policy uniformity (SPEC INV-125):** a policy decided for an interaction
  KIND that lives on sibling surfaces — a gesture policy (browser pinch-zoom refused), an affordance, an
  input-to-action mapping — is asserted across EVERY registered sibling root, including every sibling beyond the surface where it
  was born; the check goes red until every sibling carries it, so a walk-only fix cannot ship while the door
  and the side-rooms keep the browser default. The spec-class rule is the upstream root (the clause names the
  surface class and enumerates its members); this guardrail is the mechanical floor a rendered product wires,
  catching the non-uniformity mechanically, the day the single-surface fix lands, so a human's review is not what has to catch it.
- **Tests-present** — a diff that touches a user-facing module MUST touch `tests/`. No change without a test.
- **Behaviour-traces-to-spec (bounds)** — every user-facing behaviour traces to a SPEC clause; a behaviour with no
  spec backing (a silent micro-decision — a default, an auto-mute, a sort order) is RED. This is what catches
  freelancing mechanically: you cannot ship an unasked, unrecorded behaviour.
- **Conflicts** — id duplicates, a spec invariant with no matrix row, a ⟨DECIDE⟩ marked RESOLVED but still
  live, a surface named two ways. (This is today's `test_traceability`, widened.)
