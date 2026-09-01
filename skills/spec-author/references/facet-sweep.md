## The facet sweep — run when a wish's door says feature (SPEC T-13, INV-18)

A person asks for a feature in the words they have; the dimensions below exist whether or not anyone
names them ("add a room where photos hang" never says "and decide what happens on a phone"). When the
door says feature, drafting the spec-delta walks this checklist — the **canonical facet list; its home is
here**, one list for every project.

**Read the project's declared layers, do not assume code (SPEC INV-135).** Which surfaces a facet sweep
reaches, and what a footprint's layer means for this project, come from the host profile's declared
`project.layers` line (SPEC INV-36, INV-135) — a photo site's layers are content, rendering engine, and
deployment, a campaign's are message, channels, and assets, and the pack's own are the rulebook, the
working skills, and the guardrails. The facet dimensions below are kind-abstract; read the declared
layers so the sweep names this project's real surfaces; do not assume a codebase's.

**Read the kind's declared design principles too (SPEC INV-136).** Beside its layers and proofs a
project kind carries a set of design principles — checkable design rules the kind's products must hold,
homed in the per-kind design-principles table in ARCHITECTURE.md and declared for a visual kind on the
host profile's `project.design-principles` line. When the wish touches a surface a declared design
principle governs, write the principle's answer as a spec sentence the same way a facet ends as a
sentence — the frontend kind's interactive-overlap rule (interactive controls that belong to different
layers occupy separate screen space) is answered wherever a covering overlay opens over floating chrome,
so the delta states which controls retract while the overlay stands. The pipeline's verify station
runs the declared design principles, each in its medium's own form (ARCHITECTURE.md, `docs/pipeline.md`
station 9). The spec names the answer so that station has something to check.

**Read the surface's composition axes from the kind too (SPEC INV-244).** Beside its layers, proofs,
and design principles, a project kind owes every surface a further axis set beyond the kind-independent
C-1 floor — the composition axes a surface answers because its kind renders under them, homed in the
per-kind axis table in ARCHITECTURE.md and declared on the host profile's `project.axes` line, an
explicit "none beyond the C-1 floor" a legitimate answer for a kind with no visitor-facing surface.
The C-1 floor is the canonical axis list above: view, mode, tier, viewport size, persistence and
reopen, concurrency, and every other live surface.
Composing a surface reads these declared axes from the kind before folding the facet sweep below, the
same way it reads the declared layers, so the delta answers each axis this kind owes; it does not
assume another kind's set. And where an owed axis adds runtime code to cover it (SPEC INV-248), the
delta states how that axis is delivered — the surface shipping whole for a named architectural reason
(one bundle, one page never torn down, a no-server delivery, a payload too small for a split to pay),
or owing a delivery road a later row lands (a platform split, a lazy load) — so the artifact's
separability is a decided sentence beside the axis's behaviour, read by the prover's
delivery-separability lens.

**Adding or deriving one axis owes the whole set a verdict (SPEC INV-244).** An axis is not only read
at composing time; a wish can also add a new composition axis to the kind's own declared set, or
derive one that belongs there. Either time, the session runs a bounded pass over every other axis
already in that set and returns one of three verdicts for each — already composed against, added now,
or out of scope with its stated reason; a sibling axis with no verdict is the pass left unfinished, not
a clean sweep. The same asking-what-else-is-like-this reflex that already runs across sibling surfaces
runs one level up over this set too, and it repeats at every level above that: a hand-written list stops
at the two obvious cases, the pass is what finds the third.

**Naming the value in between two poles owes its own sentence (SPEC INV-244).** An axis whose value
space is modeled as combinable capabilities — the elementary poles owed and answered up front, per
the axis's own duty — is not finished once each pole is answered alone. The values co-occur on one
real device, and the case where both poles hold at once is a value in its own right, not a blend the
two poles' separate answers already cover: a tablet carries touch and a fine pointer's hover together,
and a surface answered only for "touch alone" and "a fine pointer alone" still leaves that device's
behaviour unstated. Composing the axis names the co-occurrence value the same way it names each
pole — a decided sentence, or the recommended default carrying the `[default]` tag — before the axis
counts as covered. The refinement values past the two poles — a stylus, a keyboard-only reach, a
device the person registers — stay the human's taste and enter later; this duty reaches only the
co-occurrence of the poles already owed, not those.

- **the viewport bands** — width and height both run in bands (narrow, wide, short, tall, and the
  bands a future device adds), so every layout-bearing feature ends the sweep with a decided or
  `[default]` sentence per band its layout law names or excludes, and a law scoped to one band answers
  for the others. This is the author-side of the viewport-quantifier lens the prover holds. That lens is the
  worked instance of the range law's general sub-domain duty: a guarantee scoped to a named part of its domain
  answers for the remainder, and a user state or a locale draws the same sweep on its own parts (SPEC INV-138).
  This folds the old width-only phone facet together with orientation / short viewport: a landscape
  phone is wide and short, a band a width-thinking sweep misses, so a rotated phone meets a stated
  layout (incident: tlvphotos's caption zone printed over the picture on a
  landscape phone — the layout law said "on a phone", the styles mapped phone to width ≤ 640px, and a
  rotated phone fell out of both sentences, 2026-07-16);
- **touch where the design assumed a mouse** — anything hover-only needs a touch answer;
- **the empty, error, and loading states** of each new surface (spelled "empty, error, and loading");
- **accessibility** — reachable by keyboard, readable contrast;
- **the performance envelope** — at what input size it must stay usable; for a user-facing surface
  this facet ends as a measurable budget sentence ("the first image appears within 2 s on a cold
  visit"), never an unmeasurable "fast enough" — the architecture step pairs the budget with an
  instrumentation home and acceptance asserts it (SPEC INV-41);
- **visual hierarchy** — the gap between separate things larger than the gap within one thing (nesting
  depth drives spacing, never per-element guesswork); a heading never dimmer or smaller than the body it
  heads, sizes from one scale (incident: track-coach's inverted panel margins, 2026-07-05);
- **two windows at once** — the same stored state open in two windows; what one window's change does to
  the other (incident: track-coach's persisted aim auto-swapping cards, 2026-07-02);
- **a missing source** — an input file renamed, moved, or gone: the feature says what it shows and asks
  the person; it never guesses (incident family: the ask-don't-guess stem/source cases, track-coach 2026-06/07);
- **paired-transition symmetry** — when a surface has a pair of opposite state changes (open/close,
  enter/exit, expand/collapse, show/hide), the exit's motion mirrors the enter's unless a reason is written;
  the default is symmetry, and because motion feel is the human's own gate (SPEC INV-30) an undecidable pair
  is surfaced as a real question. A pair that enters with craft and exits instantly is never shipped silently; the answer
  ends as a spec sentence — mirror, a named shorter exit, or deliberately instant — decided or
  `[default]`-tagged like any facet (SPEC INV-126; incident: tlvphotos's polaroid room revealed under a soft
  veil in one breath and closed on a hard cut with no transition, found by hand on a real phone, 2026-07-12).
  That first part asks about the motion. Two further parts follow it, so the facet ends as three
  sentences rather than one.
    - The second part asks the reversibility of the means. Where the surface opens by a continuous,
      reversible gesture — a pinch, a drag, a lift — the same gesture reversed is written among its
      ways to close. A decided sentence may instead state why it is absent. Silence there is a
      finding, and the rightness of the reason stays the human's gate (SPEC INV-126). The incident:
      tlvphotos's pinch-to-zoom layer opened by a finger-tracked scale-up and closed only by a
      control. No reverse pinch, felt on a phone, 2026-07-14.
    - The third part asks magnitude beside existence. Where the pair rides a continuous, reversible
      quantity — a pinch span, a drag distance, a wheel accumulation — the author writes whether the
      two directions demand the same magnitude. That answer is symmetry or a named deliberate
      asymmetry, decided or `[default]`-tagged like any facet (SPEC INV-126). The incident:
      tlvphotos's inspect zoom opened on any spread past rest, and closed only at a squeeze to
      ~0.82× of rest. The reverse existed at a deeper cost to the hand. Every prover pass came clean
      because the lens asked only existence, felt on a real phone, 2026-07-16.
- **Edge completeness — both ends of a gate, and the three faces of a wait.** When the surface has a
  behaviour gated on a quantity that runs on a line (elapsed time since a last visit, a count, a distance, a
  size), write what it does at both ends of the range — below the low end and above the high end, beyond
  the one point the wish named; "on return", "after a while", "once there are several" each owe their two
  bounds. And when a slot is filled by asynchronously produced content, write the three faces of a wait —
  pending, arrived, failed — with a visible pending face while the content is in flight; this is the
  empty/error/loading facet above made specific for a reserved slot, its loading state named and shown. Each edge becomes a
  spec sentence, decided or `[default]`-tagged like any facet (SPEC INV-138).

**The list is curated, each facet earning its place by named incident.** A facet joins only with a named real incident it would have
caught. Five of the ten entries above name theirs, and the other five carry none. The list is
re-justified at milestones; a checklist
that grows by taste becomes a forty-row form nobody walks (the Google launch-checklist lesson).

**The declared-laws line rides every new section (SPEC INV-101).** Where the spec keeps a declared-laws home — the one place naming its cross-cutting laws (measurement, accessibility, error handling, a register: what the product declares) — a new surface's section states its line against each declared law, the clause or a dated exemption, before the prover ever reads the delta. Each declared law also carries its net — the review or gate that enforces it — written beside the law in that home, so the assignment lives where the laws are declared (SPEC INV-150). A law belongs to a mechanical gate where a deterministic guardrail or test decides the violation, to the prover where the violation pins to a stated sentence, and to the design review where the deciding fact lives only in the human's intent. The prover's cross-cutting station then audits the declared lines. It no longer has to discover them. A spec with no such home yet earns the home first, and a declared law with no named net is a finding there.

**Every facet ends as a spec sentence.** Either the human (or the walk's
batched questions) decided it, or the recommended option is taken so the lane keeps moving and the
sentence is written carrying the literal tag `[default]` at its line end — so a later prover tells a
taken default from a hole, and the matrix derives the facet's test row either way. Every defaulted facet
is then told on the delivery report's defaults list as a plain-words tradeoff in the product's terms
("on a phone this gallery stacks into one column — tweakable"), never one ping per facet and never a
confirmation request (SPEC INV-31) — communicator owns the report shape; a veto
becomes a new wish. A facet with no sentence is a spec defect the prover flags. The sweep scopes to the feature's visible
surfaces — a headless feature (new persistent state only) satisfies it with one explicit sentence, "no
visible surface — facets N/A", never a silent skip.

Boundaries, stated once: a wish re-doored to feature mid-work walks the sweep before work resumes — the
late-recognized surface is exactly the one whose facets nobody looked at. A fenced prototype is never
swept (a sketch has no facets to promise); the sweep fires when promotion makes it a feature. On an
adopted or promoted surface that already lives, a default is read from the shipped truth and reconciled
like any re-engineered claim, never invented greenfield. And the sweep versus the canonical axes above:
the sweep authors the facet sentences when the feature is first specified; the axes compose and test them
across views once the surface exists — one dimension, split by time, never specified twice.

