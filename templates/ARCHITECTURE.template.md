# [Project name] — Architecture

How the product is built: the named nodes the spec's facts live in. It is written from the proven
`PRODUCT_SPEC.md`, and proven itself before the test matrix is derived from it. One node carries one
name and one responsibility. That is the one-surface-one-name rule applied to structure.

**When this doc changes:** a large or surface-class wish updates it before the matrix is touched. A bug
or a small wish cites the existing node it lands in. The document is re-proven only when it changes.

**This doc is written one landing at a time.** It maps the product as it stands, plus the landing in
flight. A node exists for what ships today, or for what the spec already promises under an open queue
row. A promised node carries the `[target]` mark in its heading and a single dash for its pins. A
future feature earns its node when its landing arrives. A speculative node is unbacked structure, and
the prover flags it as a node with no spec backing.

The prover's dated records live under `docs/prover/`, outside this document.

---

## The shape at a glance

The reader lands here first: the tiers in a few lines, what runs where, top to bottom. It comes before
any table detail, which is the reading order an architecture reader expects. Two to five lines in plain
words. A sketch is welcome where it genuinely helps.

> [e.g. "Everything heavy runs at build time on the author's machine and bakes to static files. A
> content network serves every visitor byte. The browser runs the walk. One narrow edge worker holds
> the secrets and the verdicts. The model service sits behind that worker."]

## Node structure by project.kind

The project's kind (`project.kind`, SPEC INV-36) is set once at founding or adoption, and it proposes
the starting node structure. The spec's facts then decide the final nodes. The proposal is a scaffold
to fit. A node still earns its place by owning a spec fact, and a speculative node is unbacked
structure the prover flags. Pick the row for this project's kind, then adjust it.

| project.kind | the nodes it usually splits into | the seam composition bugs hide in |
|---|---|---|
| fullstack app / static site | a frontend (views / components / client state) · a backend (services, interfaces, data) · a template or renderer that turns data into markup · a store | the browser-to-server contract, and template-to-data (a value rendered stale) |
| backend service | an entry / handler layer · the domain core it calls · a data store · each external integration | the published interface and the store boundary (a partial write, a schema drift) |
| CLI / library / interface | a command / entry surface · the core modules behind it · an input-and-output boundary — one node per public surface | entry-to-core (argument parsing) and core-to-boundary (a missing or malformed input) |
| skill pack (live-spec's own kind) | one node per skill · the shared rulebook · the templates · the guardrails — the skill is a node | skill-to-skill (the handoff) and base-to-working-skill (the inherited rule) |
| book / content | usually one docs node owns the whole outline; a new node only when the structure genuinely grows | section-to-section (the narrative flow, a forward reference) |
| a custom kind | derive the split from the spec's own surfaces; name the seams where two of them meet | wherever two surfaces share state or a format |

The kind sets the shape, and the facts fill it. Two projects of the same kind can end with different
node maps, because their specs differ. The table saves a blank-page start, and the coverage rule at the
foot of this document is what proves the map complete.

**Two shapes the plain rows miss:**

- **A derive-pipeline tier.** A data-heavy or machine-learning project's build is a multi-stage derive,
  more than simple templating. Several nodes chain by intermediate data contracts (`raw →
  catalog.json → vector.json → render-data.json`), and each contract has its own format owner. A
  human-overlay seam often sits in the chain, where a person's correction wins over the machine's
  guess. Where the build runs more than one hop from data to output, give each stage its own node and
  name the contract between them. Six derive steps collapsed into one build node hide five contracts.
- **Kinds blend: static-first with a narrow edge backend.** A static site and a fullstack app can
  coexist. A project can be static-first, its front a deterministic bake on a content network,
  crawlable with no script running. It can still carry one narrow server surface. That surface is an edge
  worker holding secrets, cache and state, and every verdict kept off the client. Name that worker
  its own backend node, and name its private-data seam — what the bake injects that never ships as a
  static asset. The kind is then "fullstack, static-first".

## Nodes

Every spec fact is owned by exactly one node. A spec fact is a code anchored on a criterion in
`PRODUCT_SPEC.md`, located through the generated code-to-location table at `PRODUCT_SPEC.index.md`.

Each node gets its own section under a `### [node: <name>]` heading. The test matrix groups its rows by
the same heading shape and the same node names, so the two documents carry one node set. A node
section carries four labelled fields:

- **responsibility** — one sentence naming what the node is for.
- **owns** — the spec anchors this node owns. An anchor may trail one parenthetical sentence saying
  why it sits here. The rule itself lives at the spec, and this section cites it; a restated law is a
  second home and a defect.
- **pins** — the `file:line` places the responsibility is carried on disk, each with a short label.
  Every pin comes from a grep or a read actually run, and it reads `` `src/render.py:120` (the render
  entry point) ``. In a new project the list is the single dash until code lands.
- **notes** — a few sentences for what the other fields cannot carry, present only when needed.

A node promised under an open queue row marks `[target]` in its heading. The suite holds the tie
between that mark and the single-dash pin list.

### [node: renderer]

**responsibility** — builds the rendered page from the analysis data

**owns** —
- INV-1 · T-3 · E-2

**pins** —
- 

### [node: store]

**responsibility** — holds what the product keeps between visits

**owns** —
- E-4 (the stored record's shape is one anchor, and the renderer reads it through this node)
- INV-4..6

**pins** —
- 

**notes** — this field stands only where the three fields above cannot carry something a reader needs.

### [node: analyzer] [target]

**responsibility** — reads the source data and writes the analysis the renderer consumes

**owns** —
- T-4

**pins** —
- 

## Seams

The places two nodes meet, named, because that is where composition bugs live. Each seam states what
crosses it and which side owns the format. A crossing can carry a real schema: a data contract, a
published interface shape, a file format. The row then says where that schema lives, which is the
contract's one home. A data-heavy project lists each intermediate contract this way, as the
derive-pipeline tier above describes.

| Seam | Between | What crosses | Format owner |
|---|---|---|---|
| [analysis → render] | [analyzer · renderer] | [the analysis data file] | [analyzer] |

## Feature coverage

The feature layer above the anchor matrix (SPEC E-29). The project's primary unit carries an inline `[feature: F-x]` tag
on its spec heading. That unit is a feature, a command, a guarantee, or an argument, named by
`project.kind`. This table maps every unit to the node or nodes that implement it and to a test
that exercises it. The check runs both ways: every tag is a row here, every row is a tagged unit, and
every named node and test is real.

| Feature | Implemented by | Test |
|---|---|---|
| [F-example] | [node name(s)] | [test name] |

## Runtime view

How each promised flow runs through the nodes (SPEC INV-74). The flow unit comes from the project's
kind. A web or app product walks its visitor scenarios, one visitor scenario to a flow. A command-line
product walks one invocation per command. A skill pack walks a wish through the skills. A book crosses
no machines and says so in one sentence, which satisfies the duty.

One short walk per flow: which node serves each step, what crosses each hop, and where the flow can
fail. Each hop cites the seam it crosses by name, and the payload and format stay the seam table's
fact. A flow the document cannot walk end to end is a finding: a node is missing, or a seam is unnamed.

Every named failure point carries its fallback. A failure point with no "if it fails" sentence is an
unfinished walk (SPEC INV-74).

| Flow | The walk through the nodes | Where it can fail | If it fails |
|---|---|---|---|
| [e.g. visitor plays a track] | [player loads the analysis file (seam: analysis → render) → renderer draws the charts → player syncs the playhead] | [a stale analysis file; a chart drawn before data arrives] | [the version check refuses the stale file and shows the reload note; charts wait on the data-ready event] |

## Placement view

The tiers-and-technology table, the kin of a definitive technology-stack table. It states where every
node runs (SPEC INV-75):

- build time on the author's machine;
- a static file on a content network;
- the client browser;
- an edge worker;
- an external service.

Beside each place it names the load-bearing technology choice where one exists, such as the embedding
model, the render harness, or the store.

It also states where SECRETS live: a keychain, a binding, or an environment store. It names the tier
that holds each verdict kept off the client. A secret's place is architecture, and it belongs here
rather than in an implementation footnote.

The table is first-class, so a reader answers "where does this run" for any node at a glance. Keep it,
or fold a "runs at" column into the node sections when the map is small. A single-place project, such
as a book or a local command-line tool, satisfies the duty with one sentence.

Heavy binary content names its home here too, such as an image archive, audio, video, or model
weights. The home is object storage, or the machine's archive plus a named backup. A version-control repository of large binaries
is the wrong home, since hosting caps apply per file and per repository. A derivation that finds one
raises it as a finding.

| Node | Runs at | Load-bearing technology |
|---|---|---|
| [e.g. renderer] | [build time, author's machine] | [python3 + jinja] |
| [e.g. story service] | [edge worker] | [Cloudflare Worker + KV] |

## Quality budgets

Measurable numbers, each with the instrumentation home where the number is measured and read (SPEC
INV-41). The project's kind proposes the dimensions:

- a product names paint and interaction times;
- a backend names latency, throughput, and errors;
- a command-line tool or pipeline names run time and per-unit cost;
- a skill pack names eval pass rate and suite time;
- prose names what honestly carries a number.

A quality with no honest number is said by name and left without one.

Numbers are the host's taste: propose each with a recommendation, and set it on the person's word at
the surface's first budget landing. Each budget also names its watcher, the mechanical check that reds
past the stated number, so the budget cannot silently rot. Where a budget is honestly read by eye, that
cell says so as a decided road.

| Budget | Number | Instrumentation home | Watcher |
|---|---|---|---|
| [e.g. first image on a cold visit] | [≤ 2 s] | [the perf line in the deploy check's output] | [the deploy check reds past 2 s] |

## Decisions — where they live

One pointer table, never a second home. This project's decisions already live in dated queue rows, the
journal's chapters, and the spec's open decision marks. This section is the document's single entry
point to them, holding the content of an architecture decision log as an index.

| Decision | Status | Lives at |
|---|---|---|
| [e.g. keep all axes, no prune] | resolved | [queue row N / journal entry] |
| [e.g. attic retention window] | open | [the spec's decision code D-x] |

---

*Coverage rule, walked at matrix derivation: every spec anchor appears in some node's owns field. An
orphan fact means a missing node or a missing assignment. A node owning nothing traces to no spec
backing, and is itself a finding.*
