# Inventory — live-spec-base SKILL.md, "The shared rules"

Read-only inventory. Target: `skills/live-spec-base/SKILL.md`, section "## The shared rules",
22 live rules (numbers 1-10,12,13,16,17,22,24-27,29,31,36), retired numbers 11,14,15,18,19,20,21,
23,28,30,32,33,34,35 excluded (already moved to `attic/live-spec-base-unbacked-rules-2026-08-26.md`).
Section measures 33,888 bytes across the 22 rules (task's "~34 KB, 22 rules" confirmed by direct count).

Duplication checked against: `~/.claude/CLAUDE.md`, `~/.claude/live-spec/profile.md`,
`~/.claude/skills/director/SKILL.md`, and this skill's own `references/{glossary,settings-ladder,
worked-examples,session-handover,worker-restore}.md`.

Enforcement checked by: `grep -rl <code>` over `~/live-spec/{scripts,tests,guardrails,hooks}`, plus a
direct search for literal `base rule N` citations in guardrail scripts and tests (a rule cited by
number rather than only by INV-code is flagged — renumbering it would silently break that citation).

---

## Rule-by-rule

### 1. Ask, never guess (969 B)
- **Core:** Ask or mark it DECIDE with a recommendation only for gaps the artifacts don't already
  settle; never invent intent or offer a false choice.
- **Rest:** restatement of the same instruction in the doc-reading frame ("the read-the-doc twin of
  ask-never-guess") ~35%; cross-reference to rule 27 (twice) ~15%; INV-4/5/12/121 citations ~5%;
  elaboration of the "derive the requirement, cite the section" procedure ~45%.
- **Duplicated elsewhere?** Partial. `profile.md` "how-to-ask" ("Ask only on a real fork or
  approval-grade condition... give options with plus, minus, my pick") and "deferral" cover the same
  ground in the profile's own language, not a verbatim restatement.
- **Enforcement:** The `⟨DECIDE⟩` marker this rule introduces is the same token
  `guardrails/check-deferral-marker.py` polices (that script is named in rule 29, not rule 1). No
  check found that cites "rule 1" by number — safe to renumber.

### 2. Plain words carry the meaning; the code trails, quietly (977 B)
- **Core:** Write every human-facing sentence in plain language; never let a code or coined term
  carry the meaning, and never calque a doc term into chat.
- **Rest:** chat-vs-document anchor placement convention (parens vs `[INV-8]` bracket) ~30%; the
  no-calques sub-rule restated as its own named rule ~25%; dated justification, 2026-07-05 ~15%;
  restatement ("Chat may run in one language while docs run in another...") ~30%.
- **Duplicated elsewhere? YES.** `profile.md`: `no-calques: Never loan-translate a pack term or a
  coined metaphor; use plain words in the chat language or name the mechanism.` and `industry-words:
  Narrate in standard industry terms; keep coined terms in docs.` — near-verbatim restatement of this
  rule's second half.
- **Enforcement:** `hooks/code-anchor-scan.py` cites **"base rule 2"** by number — renumbering
  breaks that citation.

### 3. One surface = one name, everywhere (188 B)
- **Core:** Give one surface exactly one name everywhere; two names for one thing breaks every
  cross-check that assumes one.
- **Rest:** one sentence naming the vocabulary's source (the host's SPEC) ~40%; otherwise the rule
  is already near its Core.
- **Duplicated elsewhere?** No. (Rule 36 in this same file restates the same principle for one
  narrower case, "one item carries one name... on every surface" — an internal near-duplicate, not
  an external one.)
- **Enforcement:** `guardrails/check-one-name.py` (name match; not confirmed to cite the rule by
  number).

### 4. One canonical home per fact (299 B)
- **Core:** Keep exactly one canonical home per fact; repoint every reference the same session a
  doc moves or is superseded.
- **Rest:** the "undefined behaviour when two documents disagree" framing sentence, restatement
  only, ~40%.
- **Duplicated elsewhere?** No exact duplicate. `director/SKILL.md`'s "Work that states a rule
  names the rule's one home" is the same principle applied to a narrower domain (routing new
  rules), not a restatement of this one.
- **Enforcement:** no dedicated check found by keyword search; plausibly folded into
  `check-doc-rotation.py` / `check-pin-drift.sh`, not confirmed.

### 5. The seat orchestrates; cheapest tier per unit (1081 B, SPEC INV-69)
- **Core:** The seat orchestrates and never does grunt work itself; route each unit to the cheapest
  tier that passes its brief, judgment never routed down.
- **Rest:** the raw-output/evidence sub-rule ("only raw output is evidence... a worker's green is a
  lead") ~30%; independent-checker escalation for large/high-stakes work (SPEC INV-46) ~15%;
  override-logging requirement ~10%; restatement of the tiering criterion in different words ~20%;
  SPEC code citations ~10%.
- **Duplicated elsewhere? YES.** `profile.md` "lean-seat" and "fable-tokens": "dispatch every
  authored artifact and every read past a glance to workers; hold briefs and decisions" / "every
  read, draft, and sweep goes to workers on cheaper tiers."
- **Enforcement:** `guardrails/check-tier-refusal.py`; `tests/test_delegation_trigger_no_size.py`
  cites **"base rule 5"** by number.

### 6. Every long or delegated piece of work keeps a persistent checkpoint (1675 B)
- **Core:** Every long or delegated task keeps a live checkpoint file (done/in-progress/next),
  closed in the same landing that ships its items.
- **Rest:** the red-at-a-pause sub-rule (failing test becomes the checkpoint) ~15%; the
  background-worker checkpoint content (id, write-set, liveness checks: file times, heartbeat,
  message) ~35%; heartbeat interval defaults (~60s/~2min) ~10%; "never frame output as finished
  while the worker may still run" (SPEC INV-76) restated ~10%; leave-word cross-reference (SPEC
  INV-95) ~10%.
- **Duplicated elsewhere?** Functional duplicate in `director/SKILL.md`, not textual: director
  operationalizes this rule directly ("New work opens a checkpoint before the first specialist is
  called... `python3 scripts/checkpoint.py new <path>`...") rather than restating it as prose.
- **Enforcement:** `scripts/checkpoint.py` (the operational script, named directly in the rule and
  in director); `tests/test_checkpoint_closes.py` cites **"base rule 6"** by number;
  `tests/test_checkpoint_mechanism.py` covers the mechanism broadly.

### 7. The concurrent-edit fence, before every write and every commit (5079 B) — largest live rule
- **Core:** Before every write or commit, re-check git status and HEAD against what you last read;
  stop and re-read if the tree moved.
- **Rest:** this rule is a bundle of eight further sub-laws, each carrying its own SPEC code and
  its own actionable content that the Core sentence above cannot carry: lane cap under the pen
  (SPEC T-18), the lane-open act's three-step mechanics, worktree isolation on overlap (SPEC
  INV-105), brief-time disjointness (SPEC ACT-3/INV-11), no-unprotected-concurrency including the
  nested-repo case, the worker-restore ban (SPEC INV-298, delegated whole to
  `references/worker-restore.md`), one-row-per-landing-commit (SPEC INV-39), prior-context-worker
  treatment (SPEC INV-76), and the session-identity tie-break (SPEC INV-117). Combined these
  sub-laws are roughly 85% of the rule's bytes; the fence sentence itself and its read-only-repo
  clause are the remaining ~15%.
- **Duplicated elsewhere?** Partial. `profile.md` `lanes.cap: 3` restates only the lane-cap
  sub-bullet, not the fence itself or the other seven sub-laws.
- **Enforcement:** `guardrails/check-worker-restore.py` (worker-restore sub-rule, named directly in
  the rule text and read at the verify step); `scripts/open-lane.sh` (lane-open act, reads
  `lanes.cap`); `tests/test_brief_time_disjointness.py`, `test_lane_open_act_convergence.py`,
  `test_lane_branch_road.py`. `references/worker-restore.md`'s own heading cites "rule 7's
  worker-restore sub-rule" by number — a second place renumbering rule 7 would need to touch.
  **This rule resists a single-sentence compression** — see summary below.

### 8. Freshness: versions are re-checked at every breakpoint (311 B)
- **Core:** Re-check modification times of installed skills, packs and profiles at every
  breakpoint; re-read any changed file before continuing, journal old to new.
- **Rest:** near its Core already; only the journal-line requirement (SPEC A-7, M-7) and code
  citations are additional, ~25%.
- **Duplicated elsewhere?** No. (`CLAUDE.md`'s "a profile that did not load says so" is a related
  but distinct concern — reporting a load failure, not re-checking freshness on every breakpoint.)
- **Enforcement:** no dedicated check found by keyword search (no script/test matched "freshness",
  "modification time", or the SPEC codes A-7/M-7 in a targeted way). Flagged as apparently
  prose-only.

### 9. History lives in the journal; docs travel with the change (674 B)
- **Core:** Log every movement's dated reason in JOURNAL.md the same session; keep the spec,
  next-steps and plan stating only current truth, each entry dated and timed.
- **Rest:** the worked micro-example ("yesterday evening you wrote X, so I did Y") ~25%; the
  shipped-change doc-update list (README/CHANGELOG/SKILL.md) ~20%; dated justification 2026-07-05
  ~10%; restatement of "dated and timed" requirement ~15%.
- **Duplicated elsewhere?** No.
- **Enforcement:** no dedicated check found by keyword search. Flagged as apparently prose-only.

### 10. Nothing is silently deleted (303 B)
- **Core:** Never silently delete; move a superseded file to the attic with a manifest line,
  tombstone a removed feature, and get human approval first.
- **Rest:** near its Core already; SPEC code citations (INV-7, A-4, A-9) are the only addition,
  ~15%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `guardrails/check-board.py`, `check-doc-rotation.py`, `check-rendered-sweep.py`
  all cite **"base rule 10"** by number in their own print messages — three separate scripts whose
  user-facing text would go stale on a silent renumber.

### 12. The human's gates are the human's (340 B)
- **Core:** Irreversible moves, authored-content moves, publishing and gated pushes, taste and
  domain wording are proposed with a recommendation, executed only on the human's word.
- **Rest:** near its Core already; the cross-reference to rule 27 for the boundary line is the only
  addition, ~30%.
- **Duplicated elsewhere? YES.** `profile.md` `mode: max-proactive: take the recommendation, batch
  questions, pause only for taste, design, or irreversible-outside-git calls` restates the same
  gate list in the proactivity frame.
- **Enforcement:** no rule-12-specific check found; plausibly covered piecemeal by
  `check-broad-kill.sh` / `check-deletion-only-push.sh` for the irreversible-action cases, not
  confirmed as reading this rule specifically.

### 13. A claim needs its primary source (3695 B)
- **Core:** Ground every asserted fact in evidence you can point to — a file:line, a commit, a
  command's real output — never trust memory or a summary alone.
- **Rest:** this rule bundles two genuinely separate mechanisms under one number. (a) The
  primary-source discipline itself and its tie to rule 5's raw-output clause, ~15% of bytes. (b)
  A second, larger mechanism: human-attribution — a decision recorded as the human's needs a dated
  exchange it can be checked against, `DECISIONS.md`'s anchored-entry requirement, the
  `guardrails/check-authority-anchor.py` hard-block description, and its own worked incident
  (2026-07-27, a fabricated "direct instruction" that shaped a whole movement) — roughly 65% of the
  rule's bytes. Cross-references and SPEC codes (INV-207, INV-205, INV-206) ~10%; restatement
  ("An instruction carries the authority of whoever gave it...") ~10%.
- **Duplicated elsewhere?** Partial. `profile.md` `authority: Set a mode or trust line only on his
  word (INV-9)` covers only the narrow mode/trust case of the attribution sub-mechanism.
- **Enforcement:** `guardrails/check-authority-anchor.py` (named directly in the rule);
  `tests/test_authority_anchor.py` and `tests/test_traceability.py` cite **"base rule 13"** by
  number. **This rule is a borderline case for resisting compression** — see summary below.

### 16. A prototype stays a sketch (884 B, SPEC E-17/INV-17)
- **Core:** Keep every sketch fenced in `prototype/` under a PROTOTYPE label, never wired into
  production or shown unlabeled; promotion re-enters at the spec step.
- **Rest:** the label-format enumeration (screen banner / `_prototype: true` / CLI banner / name
  marker) ~20%; the see-vs-have distinction with its rule-1 cross-reference ~25%; the
  who-may-open-one clause (assigned senior only, not a worker) ~25%; restatement ("Promotion is not
  a merge...") ~10%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `guardrails/check-prototype-fence.sh` (name match; not confirmed cited by
  number).

### 17. Irreversible means gone, not merely public (569 B)
- **Core:** Stop for the human's word on any truly irreversible action — spending money, deleting
  data, sending to an audience; a repo push is not irreversible.
- **Rest:** the push-is-not-irreversible clarification restated twice ~25%; the "when unsure, treat
  as irreversible" default ~15%; dated worked criterion, 2026-07-05 ("money yes, deletion yes, a
  push no") ~20%.
- **Duplicated elsewhere? YES.** `profile.md` `mode: ...pause only for taste, design, or
  irreversible-outside-git calls` uses this rule's own criterion ("outside git") as its proactivity
  boundary, and the `push` trust line separately restates the push-is-reversible conclusion.
- **Enforcement:** `guardrails/check-runaway-child.py` and `guardrails/reap_owned_group.py` cite
  **"base rule 17"** by number, tied to the rule's own cited incident (a broad name-based sweep
  once closed the owner's real browser).

### 22. Every process converges on its goal (1068 B, SPEC INV-98)
- **Core:** Name the goal up front as a concrete artifact (a norm, a test, a written acceptance)
  and measure every iteration against it directly, never a proxy.
- **Rest:** the four lock-mechanisms list (norm template, conformance test, lint floor, ratcheting
  cap) ~25%; the labelled-exploration exception with its rule-16 cross-reference ~15%; pointer to
  the owner's private playbook chapter (unreadable outside the project) ~20%; restatement ("The
  distance to the goal only shrinks...") ~20%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `tests/test_convergence_rule.py`. Thin footprint otherwise — INV-98 appears in
  only 2 files project-wide. (Note: `tests/test_code_compaction_station.py` cites "base rule 19" —
  a *retired* number — in a context that looks like it should be rule 22's territory; see
  contradiction note below.)

### 24. The process stations are kind-abstract (1759 B, SPEC INV-135)
- **Core:** Each project kind fills the pack's abstract stations with its own concrete layers and
  proof kinds, declared once at founding as `project.kind`.
- **Rest:** the three footprint categories defined generically (presentation-only /
  single-module / cross-cutting) ~20%; pointer to `references/worked-examples.md` for the per-kind
  illustration ~10%; the `project.layers`/`project.proofs` profile-line mechanics and the
  incomplete-if-neither flag ~30%; cross-reference to `ARCHITECTURE.md`'s footprint-and-proof table
  and to spec-author/test-author reading it ~20%; closing restatement ("A method written only for
  code would fit a photo site badly") ~10%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `tests/test_founding_layers_proofs.py`, `test_design_principles.py`,
  `test_composition_axes.py`, `test_agent_card_gate.py`, `test_config_surface.py` (11 files cite
  INV-135 project-wide).

### 25. The seat reads to decide; discovery reads go to workers (1973 B, SPEC INV-137)
- **Core:** Keep the seat's context to orchestration only; dispatch any file read past a small
  glance to a worker and read back only its distilled result.
- **Rest:** the glance-is-bounded definition (near-verbatim elsewhere, see duplication) ~15%; the
  verification-read exception (checking a claim stays with the seat, tied to rule 13) ~20%; the
  "seat never reads a file merely to hand a worker its anchors" clause with its own SPEC-INV-53
  composition note ~25%; the delegation-accounting record requirement ~15%; restatement ("The
  leanness is load-bearing...") ~15%.
- **Duplicated elsewhere? YES**, strongly. `profile.md` `lean-seat`: "dispatch every authored
  artifact and every read past a glance to workers; hold briefs and decisions. A glance is a read
  copied out as it stands: one small file, or a handful of targeted lines." vs. this rule's "A
  glance is bounded. It is one small file, or a handful of targeted lines whose result is itself
  the deliverable" — near-verbatim overlap of the operative definition.
- **Enforcement:** `tests/test_minor_gate_reconciliations.py` cites **"base rule 25"** by number;
  `tests/test_orchestrator_read_discipline.py` covers the discipline broadly.

### 26. A project kind also declares design principles the verify pass runs (678 B, SPEC INV-136/139)
- **Core:** A project kind also declares checkable design principles; the verify pass runs each in
  its medium's own form, falling to a human eye-walk only if no suite can green it.
- **Rest:** near its Core already; the frontend-kind worked examples (interactive-overlap,
  legibility floor) ~25%; pointer to `ARCHITECTURE.md`'s per-kind table and starter sets ~25%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `tests/test_design_principles.py`, `test_legibility_floor.py`,
  `test_composition_axes.py` (9 and 5 files cite INV-136/INV-139 project-wide).

### 27. The seat decides what it can decide (1059 B, SPEC INV-143)
- **Core:** The seat decides mechanical steps, artifact-determined values and sensible defaults on
  its own; it surfaces only a taste call, an unsettled trade-off, or a correctness redefinition.
- **Rest:** the "never parks derivable work" restatement with INV-4 cross-reference ~20%; the
  resumed-session posture clause (SPEC INV-48) ~15%; the "every other rule that needs the set
  points here" cross-reference note ~15%; SPEC code citations ~15%.
- **Duplicated elsewhere? YES.** `profile.md` "deferral" line restates this rule's three-way split
  in different words: "derivable from an artifact means mine — do it, cite the artifact, drop the
  marker. His only where the answer needs a taste, a policy, or an act irreversible outside git."
- **Enforcement:** `tests/test_seat_acts_by_default.py` cites **"base rule 27"** by number.

### 29. A deferral must justify itself (1630 B, SPEC INV-152)
- **Core:** Re-test every needs-the-human's-word marker for derivability at writing and every
  touch; if an artifact already answers it, do the work, cite it, drop the marker.
- **Rest:** the three marker-kinds enumeration (queue row / NEXT_STEPS line / setup-script
  decision) ~15%; the "writing a marker requires naming the human-only fact" sub-rule ~15%;
  cross-reference to rule 27 and the pipeline's closed-door-set twin (INV-151) with the shared
  routing principle (INV-153) ~30%; enforcement-pointer prose (naming both scripts inline) ~20%;
  SPEC codes ~10%.
- **Duplicated elsewhere? YES**, strongly. `profile.md` "deferral": "Re-test each 'needs his word'
  marker by derivability every time it is touched, never obey it on sight: derivable from an
  artifact means mine — do it, cite the artifact, drop the marker" — a close paraphrase of this
  rule's own Core.
- **Enforcement:** `guardrails/check-deferral-marker.py` (named in the rule text, and its own
  print output cites **"base rule 29"** internally — a script whose user-facing message hardcodes
  the number); `hooks/chat-law-hook.sh` (named in the rule text, reminder-only, cannot block).

### 31. Agents talk on exactly two channels (5856 B, SPEC INV-183/189) — second-largest live rule
- **Core:** Agents exchange only through the receiver's inbox for one-shot requests or a published
  contract for recurring reads; a message must name the sender's own blocked work.
- **Rest:** like rule 7, this rule is a bundle of six further named sub-laws, each with its own
  SPEC code and its own actionable content: the earned-message test itself (~15%), "a referral
  travels back to whoever asked" (~15%), "data never travels as a message" (~15%), "an agent
  recognises a neighbour's zone on its own" (~10%), the two-crossing cap (~10%), "a concern no
  agent's zone owns goes to the pack" (~10%), and "a capability another agent's zone owns is taken
  through one of the two channels" (~10%). The agent/skill definition and card-scanning preamble is
  a further ~10%; enforcement-pointer prose ~5%.
- **Duplicated elsewhere?** No.
- **Enforcement:** `guardrails/check-earned-message.py` (named in the rule text; its own print
  output cites **"base rule 31"** internally); `guardrails/route_agent_transport.py`.
  **This rule resists a single-sentence compression** — see summary below.

### 36. Who the person is, by default, and what changes that (2821 B)
- **Core:** Write by default for a non-technical single reader — no codes, file:line pins, or
  script names in what they read; deepen only when they show that depth themselves.
- **Rest:** the register-raising trigger detail ("state an opinion... use the vocabulary
  themselves... ask for the mechanism") ~15%; the two surface laws (richer view offered never
  imposed; one name per item everywhere) ~30%; the "default the person did not choose" closing
  sub-rule with its own dated worked incident (2026-08-27, an unasked plan-file mechanism) ~30%;
  restatement of the refusal-text binding ~15%.
- **Duplicated elsewhere? YES**, strongly, across two files. `CLAUDE.md`: "The language is what a
  person gets. No file names, no gate letters, no counts of rules or findings: this list goes on
  his board, and he has to see what each line gives him." — near-verbatim restatement of this
  rule's Core. `profile.md` `register`, `no-hedge`, `answer-first`, `no-inflation` lines cover
  overlapping ground for the same reader.
- **Enforcement:** `guardrails/check-language-rules.py`, `check-vocabulary.py`; `hooks/register-judge.py`.

---

## The five non-rule sections

### "Where the paths and the codes point" (350 B)
- **Core:** Two path trees (pack machinery vs. host documents) and two code kinds (`INV-x`, a
  roadmap row) resolve once in `references/glossary.md`; open it on demand.
- **Bytes/rest:** already near its Core — it is a two-sentence pointer stub.
- **Duplicated elsewhere?** YES, internally: `references/glossary.md` carries a section with the
  identical heading ("Where the paths and the codes point") and the full content this stub only
  points at — the SKILL.md section is a pure pointer, so the "duplication" is by design, not drift.

### "The words this file uses" (553 B)
- **Core:** Every term this file's rules use is defined once in `references/glossary.md`; open it
  when a term needs resolving.
- **Bytes/rest:** the "the seat" naming note (glossary keeps one name among four source synonyms)
  ~40% — this is actual content, not pointer boilerplate.
- **Duplicated elsewhere?** Partial: `glossary.md`'s own opening restates "Open it when a term is
  being resolved, and not before" verbatim.

### "The rule of thinking, above all the rest" (1240 B)
- **Core:** Treat every incoming item — a person's feedback, a self-found issue, or another agent's
  message — as a symptom; name its class, state the rule, and sweep every other live instance.
- **Rest:** the three-channels-are-one-filter framing ~15%; the historical note that this
  generalizes the director's bug-to-sibling-sweep discipline ~15%; pointer to
  `references/worked-examples.md` for the guard-built-as-a-pattern-list failure, plus its closing
  aphorism ("If the answer to a class is a list, the design is wrong") ~30%.
- **Duplicated elsewhere?** No verbatim duplicate, but `director/SKILL.md` operationalizes the same
  principle directly: "Accepted work that turns out to be a confirmed bug still owes a sweep before
  it counts as finished. Name the mistake's class and search for its siblings in the same change."

### "Work that belongs elsewhere" (557 B)
- **Core:** This file is pack-internal only, never a general style guide and never a place for
  host- or person-specific values.
- **Rest:** the dated ownership citation (2026-07-16) and the "closes the recurring scope question
  for good" framing, ~40%.
- **Duplicated elsewhere?** No.

### "The settings ladder" (1731 B, includes the closing pack roster)
- **Core:** Settings resolve session > host > personal > package-default; the full table and rule
  live in `references/settings-ladder.md`, opened on demand.
- **Rest:** the pack-roster block at the file's end (the twelve skills, one line each) is folded
  into this section by my byte count but is not part of the settings-ladder instruction at all —
  it is the file's closing directory and arguably shouldn't be charged to this section in a real
  edit.
- **Duplicated elsewhere?** YES, twice over. `profile.md`: "order: His live word wins, then host
  profile, then this file, then package defaults (E-13)" restates the same resolution order.
  `references/settings-ladder.md` itself opens with "session beats host beats personal beats
  package default (SPEC E-13)" — near-verbatim of this section's own sentence, i.e. the pointer
  stub and the module it points to both state the resolution order in full, not just the module.

---

## Byte budget

**Core sentence + enforcement pointer only, nothing else, for all 22 rules: 5,176 bytes.**

(Against the section's current 33,888 bytes, that is roughly a 6.5x reduction — past the ~4x
target — but this number strips every dated citation, cross-reference, and worked justification;
it is not a recommended edit, only the floor the task asked for.)

## Rules that resist compression

- **Rule 7** (the concurrent-edit fence, 5079 B) — genuinely eight sub-laws under one number (lane
  cap, the lane-open act, worktree isolation, brief-time disjointness, no-unprotected-concurrency,
  the worker-restore ban, one-row-per-commit, prior-context-worker handling, session-identity
  tie-break — that's nine, each with its own SPEC code and its own actionable instruction a session
  needs). One 25-word sentence can state the fence; it cannot also state the other nine.
- **Rule 31** (agent channels, 5856 B, the largest live rule) — same structural shape: six named
  sub-laws (earned message, referral, data-never-travels, zone recognition, two-crossing cap,
  unowned-concern routing, capability-channel), each independently actionable and each carrying its
  own SPEC code.
- **Rule 13** (primary source, 3695 B) — borderline. It reads as two rules filed under one number:
  the primary-source discipline (compresses fine alone) and the human-attribution/DECISIONS.md
  mechanism (a distinct, larger instruction with its own hard-blocking script and its own worked
  incident). A single 25-word sentence can carry one or the other, not both.

No other rule earns this flag — most of the remaining prose in the other 19 rules is dated
citation, cross-reference, or restatement, which is exactly the material the task expects to be cut.

## Contradicts the premise / found along the way

1. **Retired rule numbers are still cited live in the test suite.** SKILL.md states rules 14, 15,
   18, 19, 20, 21, 23, 28, 30, 32, 33, 34, 35 were "cut whole... each number is retired and stays
   open" (2026-08-26). But `tests/test_class_hunt.py`, `test_code_compaction_station.py`,
   `test_code_anchor_scan.py`, `test_traceability.py` (x2), `test_live_spec_base_body_thinned.py`,
   `test_minor_gate_reconciliations.py`, `test_release_tier_rule.py`, `test_clean_context_review.py`,
   and `test_resume_rederive.py` still cite "base rule 14/18/19/20/21/23/28/32/33/34" by number.
   Some of these (e.g. `test_release_tier_rule.py`, `test_live_spec_base_body_thinned.py`) carry
   their own comment acknowledging the retirement and flagging themselves as out-of-scope debt
   ("flagged in the report rather than fixed here") — this is known, already-logged drift, not new.
   Others (`test_class_hunt.py`'s docstring naming "base rule 14" as a live home with no such
   disclaimer) look like they were never updated after the 2026-08-26 cut. This is not part of the
   assigned inventory (it is test-suite drift, not SKILL.md content) but it directly bears on the
   task's premise that "each number is retired" — in the test tree, several are not treated that
   way.
2. **A likely mismatched citation.** `tests/test_code_compaction_station.py` cites "base rule 19"
   (retired) in a context that reads like rule 22's (convergence) territory — worth a human check,
   not confirmed by me as a bug since I did not read that file's body past the citation line.
3. **Five guardrail scripts hardcode rule numbers in their own print output**: `check-board.py`,
   `check-doc-rotation.py`, `check-rendered-sweep.py` (all "base rule 10"), `check-deferral-marker.py`
   ("base rule 29"), `check-earned-message.py` ("base rule 31"), plus `check-runaway-child.py` and
   `reap_owned_group.py` ("base rule 17"), and five test files cite rules 2, 5, 6, 13, 25, 27 by
   number. A renumbering pass done for the compression project would need to touch these files too,
   not just SKILL.md — the task's framing ("cutting its weight... without losing any rule") is safe
   for content loss but silent on renumbering; if the compression pass renumbers rules (e.g. to
   close the gaps left by 11/14/15/... being retired), these citations break silently.
