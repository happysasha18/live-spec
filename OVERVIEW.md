# live-spec — the ideas in five minutes

This page is for a developer who has read the README and wants the ideas before opening any skill
file. Normative rules live in `PRODUCT_SPEC.md` and the skill files; this page explains and points.

## The living spec is the product's source of truth

A project running under the pack keeps one document, `PRODUCT_SPEC.md`, stating what the product
promises today. That project is called the host, and the pack's own repository is a host too.
The document opens with a glossary that defines every domain noun, then a body of
requirements: each carries a short context (when the situation arises, who is involved, what the
reader sees), one user story, and acceptance criteria grouped into named cases. Short codes such as `[INV-104]` or
`[E-6, T-12]` trail at line ends as anchors for the machine; a reader can ignore them. A generated code-to-location table
closes the document. The pack's own spec is the reference shape; its version lives in `VERSION`.

The spec is living in a precise sense. Work enters it before code: a new behaviour arrives as a spec
delta, gets reviewed, and only then gets built. Shipped behaviour traces back to it: a guardrail
check goes red when a user-facing behaviour has no spec sentence behind it. And it stays current:
a removed feature leaves a dated tombstone, and history moves to `JOURNAL.md`.

## The pipeline — a wish becomes shipped, tested work

A wish is a request in plain words, thrown at any moment. It becomes one row in the queue,
`ROADMAP.md`, the moment it is spoken (SPEC E-2). Intake names its door aloud — feature,
bug, refactor, docs-only, skip — before any code; fixed tripwires decide, so a casual ask that
creates a new surface still enters as a feature (SPEC T-12). A feature walks nine stations in order.

1. **Spec** — `spec-author` writes the delta: entities, states, transitions, invariants, regression
   fences on touched live surfaces, a sweep of the standard facets (the viewport bands, touch,
   the empty and error states, keyboard reach), non-goals, one success measure.
2. **Prove** — `product-prover` reviews the grown spec; findings are recorded and folded.
3. **Architecture** — `ARCHITECTURE.md` maps named nodes, each owning spec facts, pinned to real
   `file:line`. The document also owes a runtime view (each promised flow walked node by node, with
   a fallback at every failure point, INV-74) and a placement view saying where every node runs (INV-75).
4. **Prove the architecture** — the prover again, with an architecture lens: every fact owned,
   every node backed by the spec, every seam named, both views present.
5. **Test matrix** — `test-author` derives `TEST_MATRIX.md`, one block per node, one row per fact;
   every row states what the fact does and what it must never do, and pins a test level (string /
   DOM-text / browser-computed / pixel).
6. **Tests** — written against the real shipped artifact; each new test is watched failing first.
7. **Code** — implement until green; mechanical work goes to cheaper worker models under precise
   briefs, and judgment stays with the senior model.
8. **Verify by deed** — run the real thing and look at it; green means zero failures and exactly
   the expected skip list.
9. **Commit and show** — docs travel with the change; the human sees the real render; accepted
   work is pushed to the host's remote by rule, the README re-checked at every push (INV-82).

A bug shortcuts to matrix → test → code. A refactor changes no behaviour, so it enters at the verify
station with the full suite and an audit of the touched matrix sections. A docs-only change re-reads the
changed section as it renders, plus one search for a claim the code no longer supports. The skip door
covers a one-file edit that adds no state and no visible behaviour, and it still ships a test.

Four mechanical guardrails on the pre-push hook enforce the structure. A change without a test, an
empty surface, a behaviour without a spec sentence, or a duplicated anchor turns the push red. The
host wires that hook itself, in the second install step the README states. The normative walk lives
in `skills/build-pipeline/SKILL.md`.

## The prover is a formal-review step

`product-prover` reads documents the way a formal-methods reviewer reads a model: entities, states,
transitions, invariants, safety, liveness, atomicity, and the composition between surfaces. It runs
at two stations (spec and architecture) and, on the pack itself, again before every push. Findings
land in dated files under `docs/prover/`. Each one carries a marked fate with a reason — folded,
queued, recorded, rejected, or still open — so the fate of every defect stays checkable after a
memory wipe. The prover finds holes in what documents
claim; the tests then cover the facts.

## The settings ladder

How the pack behaves is a named setting living in one of four nested scopes; a narrower scope wins.
The normative table and the default values live in `skills/live-spec-base/SKILL.md` (SPEC E-13).

| Scope | Home | Describes |
|---|---|---|
| package defaults | `live-spec-base` | the pack out of the box |
| personal profile | `~/.claude/live-spec/profile.md` | one human, across all their projects |
| host profile | `<host>/.live-spec/profile.md` | one project |
| session | the human's spoken word | this conversation only |

An override exists only as a written line in its profile file. Setting one leaves a dated journal
note, so every divergence stays visible. The session scope is spoken only and dies with the conversation; making
it permanent is a promotion into a profile, on the human's word.

## Ten working skills, plus the one shared rulebook they all load

- **live-spec-base** — the shared rulebook and the default settings, stated once; on any apparent
  rule conflict, this file wins.
- **spec-author** — writes and grows the living spec, use-case-first and prover-ready.
- **product-prover** — reviews specs and architecture documents with formal-verification thinking.
- **product-prover-pack** — the pack adapter for the external canonical product-prover: the pin
  map, the pack paths, the record home, and the mode names; it reviews nothing itself.
- **design-reviewer** — reviews the design itself once the spec is proven: groups the same-kind
  things the text never declared, checks each kind behaves alike, and brings the strongest likely
  difference to the human. It recommends and questions, leaving the landing free.
- **build-pipeline** — sequences the whole arc from wish to shipped, tested, committed change.
- **test-author** — derives the matrix from the proven spec and writes the tests.
- **communicator** — shows work plainly and asks only the decisions the human can actually make.
- **feedback-intake** — receives everything a person hands back and routes each item to its home.
- **feedback-collector** — on a rare strong reaction, offers (with your yes) a private note up to the pack's authors; off by default, never sends on its own.
- **text-audit** — reads any human-facing text as a stranger and fixes where a reader stops. It
  closes after two rounds in a row where both fresh readers find nothing blocking.
- **publish** — the quality gate when work leaves the machine, owing what the artifact's kind owes.

## What the spec learned recently

The newest invariants each fix a field failure as a class. The architecture now owes the runtime
and placement views above (INV-74, INV-75). A background worker outlives a memory wipe, so a
resuming session proves it dead or alive before touching shared files (INV-76). The test layer
gained a set of lessons: behaviour past a headless browser's reach gets a real-device walk row; a
geometry fact asserts relative distances, at several viewport sizes, over repeated steps; an engine
extracted from one project tests on its own generic fixtures; and the suite's own plumbing is itself
tested, so a skip path or a wrapper's exit code can never fake a pass (INV-77–INV-80). Every
question to the human first passes the gate "can I decide or verify this myself" (INV-81), and
accepted work reaches the remote by rule, the pipeline's last station (INV-82).
