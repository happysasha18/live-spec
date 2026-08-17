## The primary unit — one per project type, traced end to end (SPEC E-29, INV-73)

A spec has a primary unit: the thing the reader counts, the product's spine repeated. The unit is a
parameter of the project's type — the way a domain swaps a template — declared once, then it sets the
heading style, the acceptance-criterion shape, and what the coverage check means.

| project type | primary unit | the coverage check validates |
|---|---|---|
| web / app | a user-facing **feature** (a visible flow) | every feature → architecture node(s) + a test |
| CLI / library / API | a **command** / function / endpoint | every surface → its contract, an owning module + a test |
| methodology package | a rule or **guarantee** the pack promises | every guarantee → an enforcing mechanism (a script, a gate, a template) |
| content / book / article | an **argument** / chapter / section | every promised argument → a home in the outline (a structure check; no technical architecture) |

**The mechanic is one, for every type.** Each unit carries a stable inline tag on its heading — the same
family as the anchors, e.g. `[feature: F-wish]` — and the downstream artifacts back-reference it: one
coverage table in ARCHITECTURE.md names the implementer node(s) and a test per unit. The two-way check reads
both directions — every unit has an implementer and a test, and every promised unit carries its tag. In this
pack that check is the feature-coverage trace in `tests/test_traceability.py`, reading ARCHITECTURE.md's
`## Feature coverage` table. This
is the anchor-ownership machinery extended a level up, never a second machine to keep in sync.

**No file explosion.** One PRODUCT_SPEC.md, one ARCHITECTURE.md, one TEST_MATRIX.md; the unit tags live
inline in the prose and the one coverage table binds them. Shard into per-feature files only for a
genuinely huge project, and only by explicit call.

**The source is plain Markdown; the render resolves the links.** The source stays plain Markdown — a
tag plus one table. When a doc is rendered, a relative `.md` cross-link opens its rendered `.html`
neighbour and its `#anchor` lands on the target heading (ROADMAP row 195, shipped 2026-07-10). Linking
a trailing bracket code to its row in the code-to-location table stays an optional later leg; until that lands, a reader
follows a bare tag by searching the source.

**On live-spec itself.** live-spec is a package, but its scenarios are the product's features, so it
dogfoods the web/app row: each person-facing scenario heading tags `[feature: F-x]` and the Feature
coverage table maps it to its skills and its test. The machines that work behind the scenes (guardrails,
host contract) implement guarantees; they are not user-facing features, and they stay outside the feature layer
by the type's own definition of its unit. The decided design note is `docs/spec-format-by-project-type.md`.

**The heading convention makes the reverse direction mechanical (SPEC INV-132).** For the two-way check to
catch a scenario whose tag was forgotten, an untagged heading has to be unambiguous — and it is not on its
own, since the checker cannot tell a new scenario missing its tag from a machinery or reference section
that never had one. So every requirement heading — `## Requirement N: …`, the level every person-facing
scenario uses — carries either its `[feature: F-x]` tag (a person-facing scenario) or the explicit
`[not a scenario]` marker (a machinery, rules, or reference section, legitimately untagged), and an
untagged, unmarked requirement heading is unambiguously red. The parts under it — the `### Acceptance
Criteria` sub-heading and the bold case lines — nest inside a requirement already tagged or marked, so they
owe nothing. When a section that is not a person-facing scenario is added, state its `[not a scenario]`
marker in the same edit — a new machinery heading that passes silently is the gap this closes.

