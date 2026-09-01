## How it reads — human-first, in plain product language

A spec is read by a **human first** (a teammate, the author months later) and a prover second — and both from
**one** document. Write it in the **language of the product**: plain words a product person speaks — what the
thing is and does, in whole sentences. Machine fragments with markup have no place in it. It doesn't have to read like a textbook/lesson either;
**product language is the register**, whatever fits the project. Don't fork a "readable" copy and a
"checkable" copy; they drift apart and one goes stale. The format below serves both at once. It was tested on a real
project: a prover-facing spec that read like "machine fragments with markup" was rejected by its author and
stopped being read, and a spec no one reads stops doing its job.

- **The body is a list of requirements; each opens with its situation.** After the preamble and the
  glossary, the body is a list of requirements. A requirement is named by the situation it governs
  ("The spec keeps what is built apart from what is planned", "A wish is captured as a queue row that is
  never lost") and carries three parts in order: a **Context** block of two to four short sentences —
  when the situation arises, who is involved, what the reader sees; a one-sentence **User Story** — as a
  person in a named position, I want one thing, so that one benefit follows; and the **acceptance
  criteria**, the behaviour grouped into named cases. The reader meets the situation and the people in it
  before the first rule, and a term is introduced before a rule uses it. A person-facing requirement is
  also called a **scenario** — its heading carries a `[feature: F-x]` tag; a machinery or reference
  requirement is not a scenario.
- **Acceptance criteria group into named cases, one criterion carrying one trigger and one response.** A
  **case** is one bold line naming a situation ("**Case: a wish becomes a row at once**"), followed by two
  to six numbered criteria. Every criterion sits in exactly one case, and the numbering runs continuously
  through the requirement. The keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase
  italics: *shall* states a duty, *when* and *while* open a situation, *if* opens a condition and *then*
  its result. No word in the document is written in all capitals outside a code anchor or a filename. A
  guardrail holds this shape — `guardrails/check-requirement-shape.py` reds a requirement missing its
  Context, its User Story, or its `### Acceptance Criteria`, and a criterion whose case or anchor is wrong.
  The parser behind that guardrail reads fixed line forms, held in `guardrails/specformat.py`:
    - a requirement heading opens `## Requirement N: `;
    - the Context line opens `**Context:**`, and the story line opens `**User Story:**`;
    - the criteria sit under a `### Acceptance Criteria` heading, each one written `N. text`;
    - a case line reads `**Case: the situation**`, bold and alone on its line;
    - a glossary entry reads `- **term** — definition`.
- **Each scenario states how it is entered and how it exits (SPEC INV-127).** A scenario is a flow with
  edges, and its Context block carries them: it states how the situation arises — from which prior state,
  with what already true (the preconditions) — and what the situation leaves true when it resolves (the
  postcondition). An entry or exit that is trivially none — a top-level scenario entered from nowhere, a
  terminal one exiting to nowhere — is stated in one short clause, so a reader tells a decided edge from
  an overlooked one. The duty binds forward: a new scenario carries its edges from the first draft, and
  product-prover flags an existing scenario's unstated edge as a finding (its scenario-level
  precondition/postcondition lens, kin of the entry-symmetry lens INV-50).
- **The criteria carry the meaning; the machine handles stay quiet.** Every criterion is a plain sentence a
  person reads straight through. The short codes — `[INV-18]`, `[T-1]`, `[E-3]` — trail at the **end** of the
  line as quiet handles for the prover and the test matrix. A reader skims past them; the maintainer follows
  them. **Never open a criterion with its code.** A range such as `[T-1..T-7]` cites its whole run of codes
  in one anchor.
- **A generated code-to-location table closes the doc.** The spec closes with a `## Reference` section
  holding one table that maps every code its criteria carry → the requirement-and-criterion locations that
  carry it (for example `INV-1` → `R4.3, R4.4, R5.1`). The table is **generated output**, built from the
  body criteria by `scripts/build-index.py`; no one edits it by hand, and feature codes (`F-...`) live on
  their scenario headings and take no table row. The authored home of each code's plain statement is its
  criterion in the body and its noun in the glossary; the table carries locations only. The gate
  `guardrails/check-index-generated.py` reds a committed table that differs from a fresh build, a body code
  the table misses, or a table code no criterion carries — so the table can never drift into a second truth.
  Two commands work it. `python3 scripts/build-index.py PRODUCT_SPEC.md -o PRODUCT_SPEC.index.md` builds
  the table, and that output is spliced under `## Reference`. `python3
  guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` then reads the document
  beside its committed copy.
- **Name the situation in the case; put the exact threshold in the criterion.** The bold **case** line
  names the situation in plain words; the numbered criteria under it carry the exact number or condition.
  The reader gets the shape from the case; the builder drops into the criterion for the precise value.
- **Use lists inside a Context block or a criterion to break up a wall of prose.** The acceptance criteria
  are already a numbered list by construction; this rule governs the prose around them. When a Context block
  or a criterion spells out several forms, legs, or arms — a label's forms, a check's three legs, a law's
  four arms — lay them out as bullet or numbered items so the eye scans them, and keep prose for the
  reasoning that connects them.
- **The enumeration threshold makes that checkable (SPEC INV-215).** A prose paragraph carrying an
  enumeration of three or more distinct, parallel facts earns bullet or numbered structure — a filename
  rule with its collision law and its header fields and its body parts, run together in one paragraph, is
  a list the reader should scan, so lay the members out as items. Prose stays for the laws, their reasoning,
  and their boundaries; the enumeration of parallel members becomes the list. This stays a stated writing
  rule, read by eye and by the prover's cognitive-load lens, and it earns no mechanical lint. A regex
  flagging every three-comma sentence would trip on ordinary rhetorical triads — a neutral, precise, plain
  register, or a rule with its actor and its reason. Telling a genuine list-owed enumeration from a
  rhetorical triad is a meaning call the register judge and the prover make, past a regex's reach. The rule
  came from the owner, 2026-07-17, reading the promoter's inter-agent design doc: a paragraph packing a
  filename rule, a collision law, three header fields, and four body parts belongs in a bulleted list —
  the human language was already right, and the one remaining fix was reading efficiency.
- **A preamble and a glossary open the doc.** Open the spec with a short preamble: what the document covers
  in two or three sentences (no incident or source behind the 2-3 — an engineering default, not a policy
  decision), what the bracket codes are (each letter's kind, taken from the list under
  "The bracket codes" above — and that a reader can ignore them while a maintainer follows
  them), how the keywords *shall*, *when*, *while*, *if*, and *then* read, and that **edit history lives in
  the JOURNAL, apart from the spec itself.** A **glossary** follows, before the first requirement: every
  domain noun the body uses carries a one-sentence entry there, defined once under one name (closed
  vocabulary — a coined word is translated to a defined standard term before it enters the document). The
  gate `guardrails/check-vocabulary.py` reds a term defined twice, a glossary entry no body line uses,
  and a coinage listed in `guardrails/spec-coinages.json`. Its own header states what it leaves out.
  No script can tell a domain noun from ordinary English, so a used-but-undefined noun is caught by
  the cold reader instead.
- **The spec states the current truth — a changelog lives elsewhere.** No "changed in v0.8.3 from…" edit-history notes in the prose;
  the *why-we-changed-it* belongs in `JOURNAL.md` (dated, with the reason). A superseded rule may stay with a
  one-line "superseded by §X" pointer when the old shape still needs explaining — but the prose reads as
  today's truth.
- **Layer overview up front.** If the spec stacks layers (a credibility floor, then features on top), open
  with a 3–5 line "how the layers stack" map (no incident or source behind the 3–5 — an engineering
  default, not a policy decision) so a reader always knows where they are.
- **Readable-first beats terse.** Clipped machine-fragment prose gets rejected by humans as hard as a wall of
  fluff does. Err toward a sentence that *reads well*; keep the structure, lose the jargon. Terseness is not
  the goal. The goal is a headline the eye lands on, then detail it can drill into.
- **Write in the pack's technical-writer register.** Spec prose reads like a native-English open-source
  technical writer: neutral, precise, easy to follow. The full register (define abstract terms in plain
  words at first use, one term per concept, concrete nouns, active voice, cut nominalizations and filler,
  metaphors only as one-off color) and the per-section verification checklist live once in the
  `communicator` skill's writing register — `skills/communicator/references/writing-register.md` (its home
  since row 266) — spec prose follows it like every other human-facing text.
- **A machine gate holds the register — attention alone drifts — and the prose is written by a clean agent.**
  Re-styling a spec by hand drifts (a voice reads fine on a sample, then the same tells return round after
  round). A **tell** here is a writing habit a reader recognizes as machine-written. The durable fix has
  five parts, and parts 2 to 5 are proven and sealed in `docs/prose-quality-gate-design.md`:
    1. A fresh agent with the pack not loaded writes the prose from bare facts. A context that has
       loaded the pack writes ornate prose, so it only does the mechanical half. This leg is spec law
       (SPEC INV-84), restated in `skills/live-spec-base/SKILL.md`.
    2. `scripts/spec-style-lint.py --gate` blocks the tells a regex can see: contrast-by-denial frames,
       define-by-exclusion openers, jargon, shouted capitals, second person, reassurance, and future
       narration. Defined terms are allowlisted and marked informative regions are exempt.
    3. `scripts/spec-redundancy-precheck.py` catches lexical near-duplication. `scripts/spec-judge.py`
       then runs a fresh language-model judge against the hash-pinned rubric `scripts/judge-rubric.md`,
       for the redundancy and register a regex cannot see.
    4. An unfixed tell is recorded in `scripts/spec-waivers.json` as a dated waiver, and the running
       total is capped by `scripts/spec-debt-cap.json`.
    5. `scripts/spec-done-gate.py` is the one definition of done.

  Restyle each section through this loop: fresh writer → gate to 0 errors → anchor multiset
  unchanged → suite green → re-point any broken traceability check-phrase by narrowing to a register-clean phrase
  (log it) → commit. The floor is the machine; the ceiling stays the exemplars + a human's read.

This is the shape `product-prover` is tuned to read, and the one a human will actually keep open.

