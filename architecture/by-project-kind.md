## Footprint and proof by project.kind

The footprint categories and the test ladder are kind-abstract stations. Each `project.kind` [INV-36]
fills them with its own concrete layers and its own concrete proof kinds. A founding declares both in
the host profile, on `project.layers` and `project.proofs` (SPEC INV-135). This table is the per-kind
scaffold — the shape a founding fills, beside the node-structure-by-kind scaffold in
`templates/ARCHITECTURE.template.md`. The three
footprints (presentation-only · single-module · cross-cutting) hold for every kind; only the layer names
and the proof kinds change. A founding check reds a `project.kind` recorded with neither declared.

| project.kind | concrete layers (footprint categories) | concrete proof kinds (test-ladder rungs) |
|---|---|---|
| skill pack (live-spec itself) | the rulebook and spec · the working skills · the guardrails, templates, and suite | the pytest suite (string and render assertions against the shipped files) · the docs/prover records · the owner's read |
| code / fullstack app | frontend · backend · store | unit and integration tests · browser-computed and pixel renders · the owner's walk |
| photo portfolio / static site | content · rendering engine · deployment | a byte-diff of the baked output · the owner's eye-walk |
| prose / promotion campaign | message · channels · assets | the register lint · the owner's review |
| music project | arrangement · stems · mix | the analysis renders · the owner's ear |

The three real hosts fix the fixtures for the founding check: a code kind, a photo-visual kind, and a
prose kind. Each carries its own layers and proofs. A kind-only profile stands beside them, and it
must go red.

## Design principles by project.kind

Beside its layers and proofs, a project kind carries a set of **design principles**. These are
checkable design rules the kind's products must hold. They belong to the family of cross-surface
policy uniformity [INV-125] and paired-transition symmetry [INV-126] (SPEC INV-136). The pack ships
the starter set below. A founding that records a visual kind declares its design principles in the
host profile, on a `project.design-principles` line. That line carries the starter set plus any the
project adds. A founding check reds a visual kind recorded with none. The verify pass reads the
declared principles and runs each in the medium's own form. That run sits beside the visitor walk and
the feel pass [INV-30]. A principle the suite cannot green, such as motion feel or a real-device
gesture, is the human's own eye-walk [INV-77]. One the suite can hold becomes a matrix row in the
adopting project's own suite. This table is the per-kind scaffold; a kind with no entry yet carries none.

| project.kind | starter design principles | how each is checked |
|---|---|---|
| frontend / visual (fullstack app · static site · photo portfolio) | the visitor walk (first visit · return · cross-entry · from-any-point navigation · exits) · the feel pass scaled to a whole site (motion quality, affordance craft against the prototype bar) · motion and scroll feel as the human's gate · **interactive controls that belong to different layers occupy separate screen space** (the interactive-overlap rule) · cross-surface policy uniformity [INV-125] · paired-transition symmetry [INV-126] · **a legibility floor** — text meets a minimum contrast ratio against its background and a minimum size (SPEC INV-139) · **the build/configuration seam** (SPEC INV-291, stated in full below the table) | the walk and the feel pass are the human's eye-walk [INV-30, INV-77]; the interactive-overlap rule, the policy-uniformity and paired-transition rules each get a browser or pixel-level row in the adopting project's suite; the legibility floor is read at the verify feel pass (a product surface's computed colours/sizes) and at the pre-show gate (`scripts/preshow-legibility-lint.py` on the styled file), its browser-computed row living in the adopting project's suite; the seam is declared and checked as the paragraph below the table states |
| code / backend service | the promised flows all reachable · error and empty states answered · latency and error-rate budgets held · **the build/configuration seam** (SPEC INV-291, stated in full below the table) | integration tests and the budget rows [INV-41]; the seam's declaration and check are the same mechanism the row above cites |
| prose / promotion campaign | the register held across every surface · one thought per paragraph · the reading path stated | the register lint and the owner's review |
| skill pack | the description triggers when it should · install and commands shown · when-to-use stated | the skill-creator review [INV-99] and the eval suite |

**The interactive-overlap rule** is the frontend kind's founding design principle. It is
stated in full in the spec's founding design-principle clause, SPEC INV-136. This document carries its
projection into the adopting project's own suite alone. For each covering overlay the project defines, a
browser or pixel-level row opens the overlay. That row asserts every other interactive control is not
rendered or not pressable while the overlay stands. The computed forms are `pointer-events:none`,
`opacity:0`, or off-screen. The pack ships the law and the starter set, and leaves the pixel assertion
to the products it serves. live-spec itself has no UI.
This is the ship-the-shape pole of the pack-to-host split [INV-163].

**The seam between the build and the configuration** (SPEC INV-291) is the principle every deployed
kind carries. A founding names it on the host's own `project.config-surface` line. That line sits
beside the layers, the proofs, the design principles, and the axes [INV-135, INV-136, INV-244]. A
kind is deployed when its product runs where its readers reach it. That product also reads values it
did not have to be rebuilt to receive. The static-site, fullstack, photo-portfolio, and backend kinds
stand on that side. A book, a prose campaign, a CLI, and a skill pack stand off it. A CLI carries a
configuration file, and that file sits on the reader's machine. Its owner turns nothing in it without
a release the reader takes. A reader places one thing on one side of the seam by a single question.
Does the shipped product already know how to behave once this value changes? A value the running code
already reads belongs to the configuration. A change that needs the code to do something it does not
do today belongs to the build. A value the product reads at build time stays on the build side until
that reading moves to run time. `guardrails/check-config-surface.py` reads the host profile and
reports three things. The first is a kind recorded with no declaration. The second is a declaration
with no words after its key. The third is a "none" written beside a `project.layers` line that names
a deployment layer. It carries no list of kinds, since which kinds are deployed is the judgment this
table states and a founding answers. Whether a declared value truly reaches production with no build
sits past a profile line's reach. The founding conversation and the proof by deed hold that half: the
owner turns a switch in production, and no build runs.

## Composition axes by project.kind

Beside its concrete layers and proof kinds [INV-135] and its design principles [INV-136], a
project kind declares the **composition axes**. It owes them to every surface beyond the
kind-independent C-1 floor. They are the further axes a surface answers because its kind renders
under them (SPEC INV-244). The floor holds for every stateful surface whatever its kind [C-1]. That
floor is view · mode · tier · viewport · reopen · concurrency · every co-present surface. The axes
below are the kind-owed tail, an open set each kind names one member at a time [INV-226]. The pack
ships the starter set below. A founding declares its kind's axis set in the host profile, on a
`project.axes` line. A founding check reds a kind recorded with no axis-set declaration at all. That
is the same rank a kind recorded with no layers or proofs carries [INV-135, A-10]. A kind may declare
**none beyond the floor** as an explicit stated decision. The per-kind design-principles set already
legitimises that empty case for a kind with no visitor-facing surface [INV-136]. The check reds on
silence and passes on an explicit "none". Before composing a surface, spec-author reads its axes from
the kind, the way it already reads the declared layers [INV-135]. It writes each owed axis's answer
as a facet-sweep sentence, decided or `[default]`-tagged like any facet [INV-18, INV-31]. This table is the per-kind scaffold; a kind with
no entry yet carries none.

| project.kind | composition axes owed beyond the C-1 floor | axis-set shape |
|---|---|---|
| static site | **input-capability** — the input the surface is used through (touch · a fine pointer), the visual kinds' first named member; its sibling axes (browser engine · locale and text direction · connection and data reach · first-versus-returning visit · accessibility · measurement reach) ride the general per-kind duty and enter as their own increments [INV-226] | open — a member named at a time |
| fullstack | **input-capability**, the same visitor-facing surface set as static site, its sibling axes riding the same open duty [INV-226] | open — a member named at a time |
| backend | **load · version · tenant** — the non-visual kind's own owed set, the disproof of the empty-for-every-non-visual reading | its own increment |
| book | none beyond the floor (an explicit stated decision) | empty |
| CLI | none beyond the floor (an explicit stated decision) | empty |
| skill pack | none beyond the floor (an explicit stated decision) | empty |
| custom | none beyond the floor (an explicit stated decision) | empty |

This story lands the input-capability coverage for the visual kinds, `static site` and `fullstack`.
It records every other kind's declaration as founding data. Each non-visual kind's own coverage rides
its own increment, the backend's load, version, and tenant among them (SPEC INV-244, INV-36). The
declaration is the facet sweep's half alone. An owed axis is covered only once the surface is also
composed and tested against each elementary value of the axis. That second half waits for the surface
to exist, so the two halves split one dimension by time [C-1, INV-18]. The input-capability axis
carries a value space of its own. Touch and a fine pointer are combinable capabilities a single
device holds at once. A tablet with a trackpad and a touchscreen laptop each hold both. So a surface
answers for them in combination. The co-occurrence value, hover present alongside touch, rides in
with the deferred forcing step that makes the author answer for the in-between [target]. The founding
check reads the same three real hosts the footprint check's fixtures do [INV-135]. The first is a
visual kind owing input-capability. The second is a kind declaring none beyond the floor, this pack
being a skill pack. The third is a kind-only profile with no `project.axes` line, and it must go
red.
