# Archived JOURNAL entries — 2026-07-04 to 2026-07-12

> ARCHIVED 2026-07-29 from JOURNAL.md, moved by hand so the live file stays under its byte bound — nothing lost (base rule 10, SPEC INV-209). The 170 entries below are dated 2026-07-12 and earlier. They stand byte for byte as they stood in the live file, in the same order. The live JOURNAL.md carries a pointer line naming this file.

## 2026-07-12 ~21:20 (build-worker) — LANE B of row 279: the shipped-language gate wires into the pack's own pre-push and CI (INV-120)

**What:** `guardrails/check-shipped-language.sh` now runs as gate i in live-spec's own pre-push hook (`guardrails/pre-push`, synced to `.git/hooks/pre-push`) and as its own step in `.github/workflows/gates.yml`, the way every other guardrail runs — so a new owner-name or stray-Cyrillic attribution in a shipped doc is blocked on both the local net and the CI net. The INV-118 and INV-120 spec clauses and their matrix rows (M-258, M-260) drop the "dated exemption pending the owner's decision / not yet wired" language and record the dated adoption instead.

**Red-first:** the wiring assertions went into the suite before the wiring. `test_pre_push_calls_all_four_checks`, `test_workflow_ships_and_mirrors_the_gates`, and the new `test_gate_wired_into_pre_push_and_ci` all went RED against the un-wired hook and workflow, then GREEN after gate i landed in both. A live demonstration confirmed the wired gate catches a real offence: a seeded "Alexander decided this line" appended to OVERVIEW.md made `check-shipped-language.sh` report `OVERVIEW.md:96 [owner-name]` / `offences:1`, and reverting the seed returned `offences:0`. The new `test_gate_green_on_the_swept_tree` pins that the pack's own real shipped set stays at zero.

**Scope decisions (stated plainly):** the gate's own machinery — the detector `scripts/check-shipped-language.py` (its regex names the very names it catches) and its allowlist `scripts/shipped-language-allowlist.json` (it lists the debt) — is excluded from the scan, the same treatment the fixture homes already get; scanning a detector against itself is a false positive by construction. The `prototype/` sketch home is excluded too: a fenced sketch is not shipped product (INV-17), and a prod allowlist may not point into a prototype home (the prototype-fence gate forbids exactly that), so the exclude, not a glob, is its home. The six "© Alexander Abramovich" authorship bylines stay by a dated `name_waivers` entry — INV-120's authorship-byline carve-out.

**Adopted, not exempt:** row 279's owner decision was ADOPT. The former self-exemption recorded in INV-118 (and legitimated in row 274's landing) is retired as of 2026-07-12; the pack's own shipped docs now carry the same impersonal voice the pack asks of every product it ships for others, and the local-only diaries (JOURNAL, NEXT_STEPS, ROADMAP, MIGRATION) remain the home for candid attribution, spared by the machine's own scope.

## 2026-07-12 ~21:06 (build-worker) — LANE A of row 279: the pack's own shipped docs adopt the impersonal voice; owner attributions move here (INV-118)

**What:** the owner (Alexander) flipped row 279 from the recommended exemption to ADOPT, so live-spec's own shipped tree now obeys INV-118 and INV-120 like any product it ships for others. The former standing exemption (INV-118's "this pack's own spec/matrix/roadmap keep a deliberate owner-attribution provenance… pending the owner's decision") is retired. Every owner-name attribution in the shipped set was rewritten impersonally in place — the name dropped, the date and the load-bearing reason kept — and the WHO/WHEN provenance is preserved HERE, in this journal, its one home from now on.

**The provenance that moved (WHO, so it is not lost):** every dated decision the sweep touched was Alexander's own word on the date it already carries. The shipped sentence keeps that date and its reason; only the personal name comes off. The moved attributions, grouped by shipped file:

- **PRODUCT_SPEC.md** (8): INV-128 entry-station clause + its Formal-index row (Alexander live 2026-07-12); INV-106 push-walk clause + index row (Alexander's word 2026-07-10 ~11:00); INV-127 scenario-edges clause + index row (Alexander 2026-07-09); INV-115 compaction-definition index row (Alexander 2026-07-12); INV-116 architecture-proof index row (Alexander's word 2026-07-12). Each rewritten to "recorded <date>" / "the owner's word (<date>)".
- **TEST_MATRIX.md** (2): M-245 (born of Alexander's word, 2026-07-10 ~11:00); M-269 (Alexander live 2026-07-12).
- **skills/live-spec-base/SKILL.md** (3): rule 2 no-calques, rule 9 dated-journal, rule 17 irreversible-push — each an Alexander 2026-07-05 decision.
- **skills/communicator/SKILL.md** (12): the born-of notes and register rules dated 2026-07-04 … 2026-07-07, plus three "to Alexander"/"(Alexander:)" references reworded to "the human".
- **skills/communicator/references/writing-register.md** (5): the 2026-07-09 flatness/allergy notes and two "to Alexander" references → "the human".
- **skills/product-prover/SKILL.md** (1): scenario-edges note (Alexander 2026-07-09).
- **skills/spec-author/SKILL.md** (1): the structure-first-rejection note (Alexander 2026-07-07).
- **scripts/render-doc.py** (1): the docstring's why-line — the name and its Russian aside ("как когда-то на VT220") both dropped for an impersonal reason (2026-07-06).
- **scripts/preshow-register-lint.py** (2): two source-comment attributions (Alexander 2026-07-10 / 2026-07-05·07) → dates only.
- **scaffold/guardrails/README.md + guardrails.config.example.json** (2): the example waiver's "owner Alexander" → the placeholder "owner <maintainer>" (it is sample config, not a real owner line).

**Kept in place by an INV-120 carve-out (not attributions, not moved):** the six authorship bylines "© Alexander Abramovich" / "Copyright Alexander Abramovich 2026" in README.md and the five skill READMEs are legitimate authorship, spared by a dated `name_waivers` allowlist entry (INV-120's "authorship bylines" carve-out). The gate's own machinery — `scripts/check-shipped-language.py` (its regex names the very names it catches) and `scripts/shipped-language-allowlist.json` (it lists the debt) — is now excluded from the scan the way the fixture homes already are, because scanning the detector against itself is a false positive by construction.

**Cyrillic (INV-120's other mechanical offence), resolved as deliberate user-language, not process-notes:** the register-example phrases embedded in PRODUCT_SPEC.md (INV-94, INV-95), TEST_MATRIX.md (M-196, M-223) and communicator/SKILL.md carry an inline `<!-- user-language -->` marker — they are the forbidden/spoken phrases the rule teaches, deliberate samples. Whole files that are Russian by function — `scripts/chat-law-hook.sh` (it emits the reminder in the human's language), `prototype/work-board-sketch.html` (mock UI in the user's language), `skills/communicator/references/field-examples.md` (a bank of chat-register examples) — are allowlisted as `user_language_globs`. No candid Russian process-note survives in the shipped set; those live only here and in NEXT_STEPS.

**Proof:** `python3 scripts/check-shipped-language.py --root .` reports `offences: 0` on the swept tree (was 134: 88 Cyrillic + 46 owner-name). LANE B wires this gate into the pack's own pre-push and CI.

## 2026-07-12 ~20:48 (build-worker, session 42) — INV-134's footprint check no longer lets a cutoff-day no-time row escape (ROADMAP row 297, M-275)

**What:** the footprint-note check treated a cutoff-day (2026-07-12) feature/refactor row with no `~HH:MM` stamp as time-None → not-required, so a post-law row that omitted both its time and its footprint note escaped unseen. The missing-time case now keys off the row's landing ORDER: a no-time cutoff-day feature/refactor row is required (fail-closed) unless it is one of the pinned genuinely-pre-law rows.

**Why not blanket fail-closed:** four real cutoff-day rows carry no time and no footprint note — 242, 274, 275, 276 — and all landed BEFORE INV-128 became law, so they owe no note by right. Blanket fail-closed would have wrongly reddened them. I verified each is pre-law by the commit that added its landed status, every one earlier than INV-128's landing commit d1bb6c4 (2026-07-12 17:07): row 242 @ 270edb6 (02:20), 274 @ 0692931 (10:39), 275 @ 48204a8 (11:00), 276 @ 0cfa0d7 (10:48). Those four are pinned exempt (documented with their SHAs in the test); every other no-time cutoff-day row is required. This is the task's "key off landing SHA/order rather than a bare timestamp" — the order settles what the absent timestamp cannot.

**Red-first:** `test_missing_time_cutoff_day_row_does_not_escape` went red against the escape-open `_required` (a forward no-time row `_required("2026-07-12", None, "999")` returned False — the escape), green after the fail-closed-unless-pinned fix. The real-file scan still passes, confirming the four pre-law rows stay exempt and every forward row carries its note. The escape is same-day only — after 2026-07-12 every feature/refactor row is required regardless of time — so the window this closes is nearly shut, but the floor is now honest.



**What:** the H3 heading-tag recognizer in `tests/test_scenario_heading_tag.py` accepted only `[feature: F-<lowercase>]`, so a heading validly tagged `[feature: F-12]` (a numeric id) or `[feature: F-a, F-b]` (several features) was read as untagged and reddened as a forgotten scenario tag. The recognizer now reads `F-[a-z0-9-]+(?:\s*,\s*F-[a-z0-9-]+)*` — numeric ids and comma-separated multi-feature tags both count as validly tagged; a truly untagged/unmarked H3 still reddens.

**Why:** a latent false-positive. No real heading uses a numeric or multi-feature id today, so nothing was broken in the shipped spec — but the check would block a legitimate heading the moment one appeared, which is exactly the "scope too narrow" class base rule 14 names. Red-first: `test_numeric_and_multi_feature_headings_are_accepted` went red against the lowercase-only recognizer (F-12 flagged as a gap) and green after the widening; the same test asserts a genuinely untagged heading still reddens, so the widening did not swallow a real gap.

**Class note (left as-is, on purpose):** the sibling recognizer in `tests/test_traceability.py` (the INV-73 feature-coverage MAPPING regex) still reads `F-[a-z-]+`. That is a different check — it maps a heading's feature id to the coverage table — and widening it to accept multi-feature headings would owe multi-feature coverage-table support, out of this lane's scope. With no real numeric/multi heading in the spec there is no active divergence; the note records the sibling so a future numeric/multi heading routes the coverage-mapping widening as its own row.



**What:** build-pipeline's junior-delegation passage carried a present-tense operative trigger — "delegate when ≥1 holds — >3 files touched/read for facts · a known script/suite runs >~30s · ... the edit strings or command are known verbatim". That is exactly the size/time trigger base rule 5 demoted ("Size is a weak hint only, never the decider") and the routing rule INV-69 replaced (the tier is proposed "beyond the row's size alone"). The passage now states delegation only as the judgment-vs-mechanical test and points at base rule 5 / INV-69 as the trigger's one home; the numeric bars are gone.

**Why it mattered:** an independent audit found it as the surviving arm of row 262's delegation consolidation — the consolidation shipped incomplete, leaving one skill still legislating a rule its own base skill had superseded. Base rule 14: a rule superseded at a broad scope goes stale at every narrower restatement the instant the broad rule changes, and the same change must sweep the copies. The broad rule (base rule 5 / INV-69) moved; this build-pipeline copy was the copy left quoting the old rule.

**Red-first, and why the scan is shaped the way it is:** the guard `tests/test_delegation_trigger_no_size.py` scans every `skills/**/SKILL.md`. It could not simply grep the bare numbers — product-prover legitimately says "scan in 30 seconds" and build-pipeline itself says the brief is "SIZED — at most ~8 files to edit". So the scan keys on the TRIGGER SHAPE a benign mention cannot wear: a `>` comparison threshold on a file count or a running time (">3 files", ">~30s"), or the "N files touched/read" file-count vocabulary. A demoted-proxy sentence ("size is a weak hint only, never the decider") carries neither, so a future sentence that mentions the proxy while pointing at INV-69 stays green. The scan went RED against the surviving trigger at build-pipeline line 489 and green after the rewrite; a companion `test_scan_has_teeth` proves the discriminator catches the three trigger forms and spares the two benign ones.

**Class hunt:** the whole-pack threshold-shape grep confirmed build-pipeline was the only skill carrying the numeric trigger — no sibling to sweep. The guard now holds the class shut for the whole pack going forward.

## 2026-07-12 (build-worker) — communicator body thinned under the ~500-line ideal (ROADMAP row 280)

**What:** the communicator SKILL.md body dropped from 578 to 499 lines, under the ~500 ideal row 280
chases, with all 22 rules and every normative sub-rule preserved and the suite green (579/579). A new
`skills/communicator/references/field-examples.md` holds the relocated worked examples; communicator
metadata is 1.0.9.

**Why the careful path (and not the s40 attempt's):** row 280 had failed once — a fresh clean-writer,
pack not loaded, tightened the body to 441 lines but silently dropped four load-bearing normative
sub-rules (live-status, offline-window, kill-list, frozen-text); the suite caught it and the draft was
reverted. The lesson: an auto-tighten-to-500 loses rules, not just anecdotes. So this pass inverted the
order — the conservation set was read FIRST off the test suite itself (149 phrases the tests pin to
`communicator/SKILL.md`, extracted by walking the test AST), and the rewrite was held to keeping every
one of those phrases in SKILL.md. That matters because the tests read `SKILL.md` directly (not its
`references/`), so a rule's test-pinned phrase cannot move to a sibling file without breaking the suite —
which bounds what may be relocated to genuinely-unpinned worked EXAMPLES.

**What moved (INV-109 accounting — each relocated, none cut):** rule 13's five worked examples (the
detached START/beat/DONE cadence, the offline window, the leave-word, live status, and a beat versus a
wall of silence), rule 6's two illustrations (the own-coinage "open leg" case and the one-name
resolver/backup case), rule 11's worked answer, the "Presenting a fork" template, and the five "Live
examples (from the field)" cases all moved to `references/field-examples.md` with pointers left in the
body; the three "Anti-patterns" bullets folded into a one-paragraph body note that still names each rule
they restate. Every rule's normative sentences (and every test-pinned phrase) stayed in the body; only
illustrations relocated. The remaining reduction was line-level tightening INV-109 leaves free —
collapsed blank-line separators, trimmed redundant provenance wording, and replaced the departures-board
case's duplicated inline provenance with a pointer to its now-single home.

**Verification:** all 22 `*(rule N)*` tags present; the pre-report walk's step-1 pointer to
`references/writing-register.md` resolves and the new `references/field-examples.md` pointers resolve;
three residual failures during the pass were line-wrap artifacts (phrases the non-flattening tests read
per physical line) and were fixed by re-wrapping, not by cutting; a conservation test rides the refactor
(the push gate requires a test alongside a user-facing change) — `tests/test_communicator_body_thinned.py`
(5 checks: body under 500, all 22 rule tags, the field-examples reference + pointer, the relocated
examples reachable, the register pointer resolving); full suite 584/584 green; guardrails
(skill-loadability, matrix-coverage, pin-drift) pass. The register lint on SKILL.md reports only its
pre-existing intentional teaching-quotes of its own pattern catalogue (unchanged in kind) and is not a
CI gate. Out of scope for this ~/live-spec pass: the global installed copy at
`~/.claude/skills/communicator/` was not synced.

## 2026-07-09 (session 29) — architecture structure by project.kind, validated read-only on tlvphoto (RUN item 5)

**What (b):** the ARCHITECTURE doc's node structure is now PROPOSED by `project.kind` (INV-36 — the existing
classifier, reused, not a new parallel setting). The architecture template gained a "Node structure by
project.kind" scaffold: a fullstack app splits frontend / backend / template / store; a backend service
entry / core / store / integrations; a CLI one node per command; a skill pack one node per skill; a book
usually one docs node. Build-pipeline step 3 points at it. The scaffold is explicitly a shape to fit, never
a frame to force — a node still earns its place by owning a spec fact, and a speculative node stays an
unbacked-structure finding.

**What (c):** ran the method READ-ONLY over the real tlvphoto tree (his standing word: do it after the
memory wipe — now OK). Touched nothing there; the derived architecture doc lives in the session scratchpad
and was opened for him. An Explore agent mapped tlvphoto's real components (11 nodes, 12 seams, every pin
from a grep/read actually run) and the exercise earned its keep by finding two shapes the plain scaffold
missed — both folded back into the template this session:
- **a derive-pipeline tier** — a data/ML project's "build" is a multi-stage derive (catalog.json →
  vector.json → gallery_data.json), each intermediate contract with its own format owner and a human-overlay
  seam; not one "build" node but a chain;
- **kinds blend** — tlvphoto is static-first (a deterministic bake on a CDN, crawlable JS-off) yet carries
  ONE narrow edge backend (`_worker.js`: secrets, KV, the quiz verdict, abuse fences), with a private-data
  seam (answers inlined into the worker at bake time because Pages never serves the worker as a static
  asset). The honest kind is "fullstack, static-first", not "static site".

**Why not commit the tlvphoto doc:** it names another private project's internal file structure; publishing
that in the public pack repo isn't warranted, so the specific doc stays in scratchpad and only the
generalizable learnings enter the template. **Why this validates the pack:** the per-kind scaffold had only
ever been dogfooded on live-spec's own package kind; running it on a real fullstack/static web project is
the first cross-kind proof, and it improved the scaffold rather than merely passing. Test
`TestArchitectureTiers`; suite 223 → 225 green. Versions: build-pipeline 0.2.41→0.2.42, pack 0.9.4→0.9.5.
Committed local; pushes with item 4 (his gate: "after 3 and 5").

## 2026-07-09 (session 29) — authoring terminology: the coined "needle" retired, a standard-vocabulary crosswalk added (RUN item 4)

**What:** Two authoring cleanups. First, the plain-language sweep: the pack had a coined metaphor,
"needle", for a *traceability check-phrase* — a verbatim prose literal the test suite asserts a section
still carries. That metaphor is the exact thing the no-coined-names rule bans, so it's gone from every live
surface — the `needle-extract.py` tool (its `needles_in` function → `trace_phrases_in`, its messages now
say "check-phrase"), the spec-author skill, and the prose-quality-gate design doc. The 200-odd local loop
variables named `needle` inside the test files were left as-is: an internal iterator name is not a surface
a reader reads, and renaming them is churn without value; the sweep targeted the language a reader meets.
The tool's filename stays `needle-extract.py` because the dated prover records reference it by that name.

Second, a **standard-vocabulary crosswalk** in spec-author: a compact table mapping our house terms to the
recognized requirements-engineering corpus — a use-case-first scenario ≈ a use case / user story (ISO
29148); composition across axes ≈ cross-cutting concerns (arc42 §8) / C4 relationships; the Formal index +
check-phrases ≈ a requirements traceability matrix; the facet sweep ≈ non-functional requirements (ISO
25010); nodes + seams ≈ C4 building blocks + arc42 §5. A one-line lineage pointer went into ARCHITECTURE's
intro too.

**Why this shape:** the crosswalk grounds the pack in a language a requirements engineer already speaks
without importing that field's document shapes — the table states the two boundaries it does not erase: the
spec stays one use-case-first document (never the Entities/States/Actors chapters), and a borrowed term
joins only when it is measurable or verifiable here, never for the authority alone. Behaviour-neutral
refactor for the rename (the tool re-run by deed, output unchanged); the crosswalk is new prose with a
string test (`TestAuthoringTerminology`). Suite 220 → 223 green. Versions: spec-author 0.1.21→0.1.22,
architecture v0.2.3→v0.2.4, pack 0.9.3→0.9.4. Committed local; pushes with item 5 (his gate: "after 3 and 5").

## 2026-07-09 (session 29) — the seven small design holes closed (rows 173-179 / findings F4-F10)

**What:** The 1.0 RUN's item 3. The 2026-07-09 full re-prove queued seven latent design questions; each is
now a stated rule with a test. None was a regression — they were seams the spec had left implicit.

- **Deferred rows now have an evaluation point (173/F5):** the milestone gate re-scans every deferred
  queue row's revisit trigger, and a fired trigger returns the row to the runnable queue — so a deferred
  wish can't wait forever on a trigger nobody reads.
- **A bug-parked feature re-proves on resume (174/F6):** T-9 gained a sixth criterion — on resume, before
  it integrates, a parked feature re-fences and re-proves its delta against the truth the bug's fix left
  behind, the way a later parallel lane does under INV-39. It was previously resuming "in original order"
  with no re-check, which could integrate a delta proven against stale law.
- **Bug vs. running milestone is now defined (175/F7):** a milestone gate is one indivisible pen-stage; a
  bug arriving mid-gate waits for the gate to finish (a half-run audit's verdict is incoherent), then
  takes the pen the instant the milestone lands. This is the single exception to "a bug cuts at the end of
  the current pen-stage."
- **The milestone-hold state is named apart from bug-parked (176/F8):** lanes quiescing for a milestone
  enter **held-for-milestone** — a clean checkpoint like a park, but named distinctly because nothing
  failed — and resume in landing order once the milestone lands.
- **The lane-claim back-off has a tie-breaker (177/F9):** "later claimant" is read by a total order —
  git ancestry, and on a genuine concurrent claim the lower inbox session token — so exactly one session
  backs off and mutual back-off can't happen.
- **The tight economy rung states its rollback (178/F10):** a batch-end red bisects to the culprit, reverts
  the batch to its last green base, re-applies the clean landings, and holds the culprit out for a fix —
  HEAD never sits red across a breakpoint.
- **An ARCHITECTURE prose nit fixed (179/F4):** the INV-67 note no longer reads as the guardrails node
  owning it; INV-67 (the showing channel matches the seat) is communicator's own, the INV-24 chat-arm
  wiring note kept separate. Mechanically unchanged — the owns-every-anchor-once check stayed green.

**Why this shape:** each hole was a real reachable situation the spec left blank (the class INV-72 is
about). All seven are clarifications of EXISTING invariants, so no new anchor — the fix is prose plus a
string-level test (`TestSmallDesignHoles`), and the process scaled to a short-form prove record
(`docs/prover/2026-07-09-small-holes.md`, INV-61). Also folded here: a scissors frame («guarantees, not
features») that had slipped into item 2's ARCHITECTURE Feature-coverage prose — caught because this pass
scanned ARCHITECTURE for tells, which item 2 had not. Suite 213 → 220 green (red-proven first). Versions:
spec v0.16.2→v0.16.3, architecture v0.2.2→v0.2.3, pack 0.9.2→0.9.3. Committed local, NOT pushed (his go).

## 2026-07-09 (session 29) — the feature-coverage trace: a per-project-type unit above the anchor matrix (E-29, INV-73)

**What:** The 1.0 RUN's item 2. The spec already traced facts at the anchor level (index ↔ architecture
node ↔ matrix row). This adds a layer above it, keyed to a project's PRIMARY UNIT — a parameter of the
project type: a web/app counts features, a CLI its commands, a package its guarantees, a book its
arguments. The unit carries a stable inline tag on its heading and one coverage table in ARCHITECTURE.md
maps each unit to its implementer node(s) and a test. live-spec dogfoods the web/app row because its
scenarios ARE its features: the nine person-facing scenarios (Throwing a wish, A prototype stays a sketch,
Publishing, Sending feedback in, the feature map, When a bug cuts the line, the problem ledger, bootstrap,
adoption) now each carry a `[feature: F-x]` tag, and the new "Feature coverage" table binds them to skills
and tests.

**Why this shape:** the mechanic reuses the existing anchor-ownership machinery a level up rather than
standing up a second machine to drift — the same reason the matrix's node×fact grid is one grid. The check
is two-way (`TestFeatureCoverage`): every tagged unit resolves to a real node and a real test, and every
promised scenario carries its tag; a dropped tag, an orphan row, a fake node, or a fake test all go red
(the never side runs the pure checker on a deliberately broken table). The infra machines (guardrails,
host contract) implement guarantees, not user features, so they stay outside the feature layer by the
project type's own definition — that boundary is stated in the spec so it reads as a decision, not an omission.

**Deferred, on purpose:** the clickable cross-links from a tag are a render-time convenience; `render-doc.py`
has no anchor resolution yet, so the source stays plain Markdown today (one tag + one table) and the
render-hypertext half is named in spec-author as the intended form, not claimed as built. A known boundary
(recorded in the prover record): the reverse guard is anchored to the known nine scenarios — it catches a
dropped tag and all tag↔table drift, but not a brand-new scenario authored later without a tag, because
telling a scenario H3 from a rule/reference H3 mechanically is itself ambiguous; the spec-author format
section carries the instruction to tag each new scenario.

**Where:** format's home = spec-author's new "primary unit — one per project type" section; the law =
PRODUCT_SPEC E-29/INV-73 (a new machine bullet under "The machines that hold the bounds" + index rows);
ownership = the guardrails node in ARCHITECTURE + the "unit → coverage" seam + the Feature coverage table;
matrix rows M-180/M-181. Design note that decided it: `docs/spec-format-by-project-type.md`. Prover record:
`docs/prover/2026-07-09-feature-coverage-trace.md` (CROSS-LINK, FOLD, one accepted boundary). Suite 209 → 213
green (red-proven first). Versions: spec v0.16.1→v0.16.2, architecture v0.2.1→v0.2.2, spec-author
0.1.20→0.1.21, pack 0.9.1→0.9.2. Committed local, NOT pushed (his go). The milestone 3-pass audit runs once
at the 1.0 gate (run item 7), not per run-item.

## 2026-07-09 (session 29) — the prover hunts the unwritten seam (INV-72 + C-1 axis)

**What:** Taught the method to catch the seam nobody wrote. A new invariant (INV-72): the prover reads the
whole axis list actively, deriving each stateful surface's reachable situations for itself instead of
trusting the author to have filled every one — every axis it passes through while already shown (view,
mode, tier, viewport, reopen) and every other surface that can be present at the same time (siblings on the
screen, one step before and after in the flow, stateful or not). A situation with a blank answer is a
finding, of the same class as a fact no node owns. And a matching new axis in the canonical list: "every
other live surface." The prover reports the gap; the author writes the sentence; the human is asked nothing.

**Why:** A wish from the tlvphoto window (`docs/wishes/2026-07-09-prover-unwritten-seams.md`). On tlvphoto's
live walk the caption kept showing the previous photo's title once the visitor reached the closing screen —
a textbook cross-section hole (caption surface × finale surface) that shipped because "what does the caption
show when the finale is in view?" was never written, so there was no seam for the prover to check. The prover
read a spec that looked complete because the missing state was invisible in it. INV-72 makes the prover
enumerate the reachable situations itself, so the absent seam becomes a finding rather than a silent pass.
The door re-running its entry fade on a viewport relayout is the same class (an already-shown surface under a
change nobody composed) and rides the same lens.

**How it went through the pipeline:** spec (INV-72 + C-1 axis, prose at the style-gate baseline — one scissors
tell caught by the linter and rewritten positively) → prove (product-prover on the delta; 4 should-clarify
folded in-pass, record `docs/prover/2026-07-09-inv72-prover-seam-hunt.md` — chiefly: trim INV-72 to own only
the prover's hunt so it derives to one node, cite C-1/INV-18 for the authoring half; a non-stateful co-present
screen is in scope) → architecture (INV-72 → product-prover node, pinned to the new lens; assignment only,
step 4 stood down) → matrix (M-179, skill-kind string row, both sides) → test (`test_prover_hunts_unwritten_seam`
red-first, then the two skill edits made it green) → code (product-prover gains the "Unwritten seams" stress
lens; spec-author's compose list gains the axis) → verify (full suite 209 green, pin-drift clean, the lens
fired against the tlvphoto case and flagged it) → commit. Versions: pack 0.9.1, product-prover 0.1.14,
spec-author 0.1.20, PRODUCT_SPEC v0.16.1, ARCHITECTURE v0.2.1. First of the run to 1.0.

## 2026-07-08 (session 27) — SPEC + ARCHITECTURE humanized (prose only; rules, anchors, tests unchanged)

**What:** Alexander drove a readability pass over the whole spec and ARCHITECTURE.md's prose. The spec had
accreted into dense, robotic law-walls over many sessions; he wanted it to read like a sharp colleague at a
whiteboard — plain, direct, native English written clearly for non-native readers — aggressively shorter,
with visual structure (bullets, `###` sub-headings), and the history pulled out of the body. His calibration,
in order: not "conversational" but native-plain; unify one voice across the file; cut hard; provenance to
this journal; and do not mirror his own multilingual chat register into the docs.

**Method** (delegated section by section, each result anchor-diffed and rule-checked by the senior): a voice
pass brought every dense section into the colleague voice; a structure+cut pass added bullets and `###`
groups and moved all dated provenance here; a native-read pass caught the last stiff seams (dropped
prepositions, "keep current" → "up to date", and one leftover incident clause); an adversarial fidelity
prover compared every section old-vs-new for meaning drift and found exactly one (the rhythm date-fence
carve-out had narrowed "wrong date" to "own date" — restored).

**Validation** (Alexander's frame: a form-only change must be invisible to meaning): the 145-anchor set is
identical before and after; every rule survives, verified per section; word counts held or dropped
(−16%..+6%), line growth is only from bulleting. The suite stayed green — but 32 traceability tests first
went red because they grepped the spec's exact old prose. That exposed a real brittleness in the method's
own tests: a traceability test keyed to a sentence forbids ever improving the prose. Fix (Alexander's call,
option B): re-point those tests to key on the ANCHOR plus a stable coined term, never a volatile sentence —
60 assertions across 31 tests, no guard weakened (broadly-cited anchors like INV-1/INV-4 were avoided as
sole guards). Suite 180 green. LESSON for test-author (own queue row to come): a traceability needle keys on
the anchor, not the sentence. Two follow-ups queued: bake the humanize method (voice + structure +
provenance→JOURNAL) into spec-author, referencing stop-slop by name rather than copying it (INV-13 across
skill boundaries); and the BMAD/Kiro architecture enrichment.

**Provenance moved out of the spec body (nothing lost — each was a dated incident the reworded rule no longer needs to carry):**
- 2026-07-05 — INV-9 (decision-page withdrawal): Alexander picked the shell-separator verdict at 23:49 and disavowed it minutes later, saying he hadn't understood what he was confirming; birthed the withdrawn-answer law.
- 2026-07-06 — INV-32 (decision cards in consequences): the shell-separator decision card explained the failure mechanism but not what was actually being decided; Alexander said he understood neither the problem, the consequences, nor the choice — the same incident behind INV-9.
- 2026-07-05 — T-15 (scope negotiation): Alexander said the walk plays with scope, not timelines.
- (undated) — T-17 (one wish = one user story): born from a project that fused two stories, a door and a gallery, into one queue row; the door half shipped, the row was declared complete, and the gallery stayed a rejected wall for four rebuilds.
- 2026-07-05 — INV-27 (departures board): Alexander's word before sleep — name the captured request in plain words, then report how each feature moves down the pipeline.
- 2026-07-06 — INV-37 (feature placement): Alexander's word — when a new request arrives, understand which feature it concerns (changes one, adds a new one, or needs restructuring), and this should be clear out of the box.
- 2026-07-06 (morning) — INV-28 (naming/lines): the first real departures board passed its eval and failed its reader — lines led with coined metaphor-titles like "a walk through the evidence" or "the clock grows teeth," carried row numbers he never opens, and squeezed facts into riddles only the writer could parse; the jargon family's third strike in two days.
- 2026-07-06 — INV-28 (bookkeeping never-list): two consecutive eval runs put "all 64 checks green, v0.9.16" straight into the human's message body.
- 2026-07-06 — INV-28 (mechanical voice): three windows leaked raw codes to their reader on the same day, prompting the chat-law-hook and preshow-lint mechanical enforcement for both this law and the narration law.
- 2026-07-08 — INV-28 (preshow-lint origin): a chat report led with "rows 166 and 148," which the reader couldn't parse.
- 2026-07-06 — INV-34: the session-13 closing report led with pack-internal names and loan-translated doc metaphors; Alexander bounced it, asking what language the report was even written in — the jargon family's fourth strike in two days, the first after INV-28 landed.
- 2026-07-06 — INV-35 (narration law): Alexander's word came twice in one day — a morning personal-profile line, then an afternoon repeat asking not to forget to report as the work goes, and to put it in the communication skill too; a habit held only in a personal profile hadn't carried across sessions, so it became pack law.
- 2026-07-06 (evening) — INV-35 (heartbeat/offline window): Alexander's third word the same day, after landing reports had gotten good but the mid-work trail was still thin — a session can go off for half an hour to an hour with it unclear where the time went; the same evening he also asked to say when he can go offline (e.g. while tests run locally), a request that returned again, pulled back every half hour by a question.
- 2026-07-06 — INV-51: Alexander's word, said twice in one minute — put the project's name in the visible content, never only the URL.
- 2026-07-06 — INV-52: Alexander's word — he'd open everything at the very end, and if anything re-opens mid-stretch, it only accumulates onto the same page.
- 2026-07-07 (morning) — INV-67: established as Alexander's word.
- 2026-07-08 — INV-71: born from two real gaps Alexander named — hours of near-silent tool calls whose work he couldn't see, and the built-in board being simply absent in the browser.
- 2026-07-07 — INV-57: after a 17-row night that ended, in Alexander's read, as nothing at all — unclear, with no closing word.
- 2026-07-06 — INV-64: in the promoter case, unmarked inference cost a review round — Alexander said he didn't know where the agent had gotten it all from; standing cross-project word since.
- 2026-07-06 — INV-42: born through the promoter window — three review rounds of one document got rejected in a single evening, the same failures repeating after they'd already been named.
- 2026-07-07 — INV-58: a rewrite of an approved opener in the promoter case introduced a banned pattern the approved wording never had.
- 2026-07-07 — E-26: a banned pattern returned into a campaign's most visible line even after the ban had been spelled out plainly, in the promoter case; only the executable scanner ended it.
- 2026-07-06 (approx.) — INV-59: Alexander's escalation in the promoter case — a stack of similar questions had already been answered, and he asked that the dialogues converge.
- (promoter case) — INV-60: Alexander's word — find it yourself, propose, then show.
- 2026-07-06 — INV-33: Alexander's word — when you write the product spec you are a strong product manager, when the architecture a strong software architect, when the test matrix a strong QA automation engineer.
- (undated) — INV-18 (facet holes): the exact hole the Room shipped through — hover-only openings, no phone layout — kept as a short illustration in the section body.
- 2026-07-06 — INV-29: Alexander's word — close the hole and write down how it was closed; and, with tlvphoto's shipped evidence in hand, do not torment the user with a barrage of questions.
- 2026-07-05 — INV-50: tlvphoto's door — a prover pass found six seams and missed the one-way face; Alexander's words: a state machine should always have a loop, if there's a get, there's a set.
- 2026-07-06 — INV-30: tlvphoto's transitions — cheap-feeling motion and an ugly affordance both shipped green through the whole pipeline, because "eyes on the artifact" had meant only "it renders and clicks."
- 2026-07-06 — INV-31: tlvphoto piled up eight untold choices and read unfinished everywhere because they'd never been surfaced; Alexander's word — if everything is fine for him, no confirmation is needed, and later the user will ask if they want something changed.
- 2026-07-08 — INV-70: born in the tlvphoto window, handed to the pack as a general rule — figure a parametrizable value as seems okay, proceed, report; at most update the parameter together; pushing to prod is fine whenever it's okay to the agent.
- 2026-07-06 — INV-62: a neighbour project shipped five full media-packs that died on one tone failure a one-paragraph sample would have caught.
- 2026-07-06 — INV-63: the promoter case's five-round trap — each round re-patched the output while the unchanged card re-made the same failure.
- 2026-07-06 — T-18 (lane cap): Alexander's word — don't sit on a hard two, take the independent work that exists; this set the cap at three, moved up from two.
- 2026-07-06 — INV-49: the first graph night proved both directions in one hour — three medium rows rolled as lanes, and the next five, all tiny, went serial by the graph's own word.
- 2026-07-05 — Evidence-based answering law (INV-25): the track-coach answer was right, but Alexander still couldn't tell which half of it had actually been checked — that gap prompted the rule.
- 2026-07-06 — Worker-contract clock rule (INV-24): the day briefs carried no clock, both eval arms led their reports with a wrong hour.
- undated — Adversarial-verify law (INV-46): the neighbours' verifier lesson (row 107) — a landing shipped green as "tasks completed, goal missed" because the same head that wrote the brief also read the result.
- undated — Brief-from-read-files law (INV-53): the neighbours' story-file lesson (row 107), and a separate night the anchors were quoted from memory — the worker walked into a wall twice.
- undated — Halt-list law (INV-54): the list's first full night, three workers halted on it and every stop was a real defect, two of them the senior's own.
- 2026-07-04 — adoption step ordering: the tlvphoto pilot's first real run proved the numbered phases don't force a strict order.
- 2026-07-04 — [A-0] target-phase deferral: the pilot's baseline-snapshot run set the precedent for recording deferred target phases in the journal.
- 2026-07-04 — [A-8] working-artifacts location: the pilot polluted the host's `data/` folder before the rule confined adoption's working files to `.live-spec/adopt/`.
- 2026-07-04 — [INV-8] version-control gate: the pilot ended up local-only on a mere recommendation, which is why a recommendation alone no longer closes the remote gate.
- 2026-07-07 — limping-thing-never-dams-flow: the clock drift had been hand-ceremonied ten times in one session while its owner, the hook row, sat open the whole time; the human then put the law in his own words — when one thing doesn't quite work, it should leave everything else free to move.
- 2026-07-07 — reuse-before-reinventing: five review rounds died on a voice failure that a public skill (stop-slop) had already carried as a written checklist for months; the search that would have caught it (promoter project) would have cost a minute and saved the five rounds.
- 2026-07-07 — problem-ledger-opening: this landing opened the pack's own problem ledger, seeded with that session's live entries.
- 2026-07-05/06 — INV-24 (date fence, files): the fence's first live run over-flagged the ledger's history lines, which legally quote past dates; the reading was narrowed to same-day added lines only.
- 2026-07-05/06 — INV-24 (chat timestamps): mid-session [HH:MM] leads ran up to seven minutes fast, twice in two days, before the write-time law was set.
- 2026-07-05/06 — INV-24 (mechanical hand): drift continued even under the written chat-timestamp law, and a ledger chat entry reopened after repeated catches (six catches in two days total, hand-swept twice) — this is what prompted the clock-hook.sh mechanical fix.
- 2026-07-07 — INV-61 (process bookkeeping): a night of eighteen landings measured that fixed per-landing bookkeeping (claim commit, full re-check record, journal chapter, resume rewrite) runs roughly 40% of wall time on a tiny row; Alexander asked why iterations run so long, prompting the reach-map idea applied to process.
- 2026-07-05 — hooks offered not imposed: Alexander said host hooks must be offered, never imposed — installed only where the host already uses git, and only after asking the human in plain words, since the human may not know what a git hook is.
- 2026-07-07 — snapshot machine design: D-3 decided the snapshot machine's design; the machine itself stays [target], with its first mechanical slice riding the guardrails scaffold, tracked at row 3.
- 2026-07-06 — push gate reach: a host audit saw a one-file README-only change pay for a 795-test run, which is what drove the reach-scoped gate design; Alexander's word was to understand what changed before deciding what to test.
- row 107 — blocking-gate contract: the neighbours' CLI lesson prompted the rule that every blocking gate emits one typed JSON failure line (`{severity, code, message, fix}`) alongside its human-readable output.
- 2026-07-05 — founding personal-vs-reusable question [B-2]: a project was founded as "a personal agent for three artifacts"; nobody asked the reusable-product question, and the human's standing answer was actually reusable.
- 2026-07-06 — project-kind update rule [INV-36]: his word — understand which kind of project this is, and update it when it changes, because everything evolves.
- 2026-07-05 — publish TARGET plugin model [E-18]: Alexander said each publish target is a plugin that embeds its own steps into the walk — a GitHub plugin brings its own stages (README-at-the-door, release notes).
- 2026-07-05 — norm-artifact rule (An approved look lives in its artifact): tlvphoto's door and gallery were rebuilt from spec prose alone; the seventy-five tests passed but the rebuild shipped a look-alike, which is why the norm now requires a frozen artifact the build must check against.
- 2026-07-07 — INV-66 (skill-list drift): the communicator's closing list was found naming four skills after the pack had grown past six; a worker halted and surfaced it, two skills missing since their birth.


## 2026-07-08 (session 26) — INV-71: where we are now is answerable in any seat (row 166)

**What:** Alexander pushed on the live "what are we working on now / what's next" board across several
messages: the harness's own task list and spinner are LOCAL-terminal only (a browser-seated session never
shows them) and go dark through hours of tool calls, so the status can't live there. Also a terminology
correction: "the pack" IS live-spec (the shared method every project runs by), not a thing inside it — so a
rule written into live-spec binds track-coach and tlvphoto too. Walked the pipeline: new invariant INV-71 in
the showing-cadence family beside the seat law (INV-67), index row, assigned to communicator (assignment
only), communicator's narration rule 13 gained a "Live status, any seat" bullet, matrix M-178, test
`test_live_status` red-proven then green, prover cross-link. The status is a short NOW (work + station) /
NEXT kept current in the CHAT (the one cross-seat surface), refreshed at each station with a heartbeat on
long stretches; the harness list stays a plain-worded courtesy, never the home. Also a landing today: the
pre-show jargon guard (INV-28's mechanical arm, scripts/preshow-lint.py) — born of my own leaked report that
led with "rows 166 and 148". Suite 180 green. Also DEMONSTRATED the discipline live: kept the harness task
list current through this build.

## 2026-07-08 (session 26) — INV-70: the agent sets tunable parameters itself and tells (row 172)

**What:** Alexander, from his tlvphoto conversation (handed to the pack as a general rule, no switch to
tlvphoto), asked for a parametrization rule: move every task that can move, ask only genuine questions, and
where a task carries a tunable KNOB (his example: image resolution) pick a sensible value as seems okay,
proceed, and report it after — at most the parameter is updated together later; and pushing to prod is fine
whenever the work is okay to the agent. Walked the full pipeline: new invariant INV-70 in the "Throwing a
wish" scenario beside the taste-told law (INV-31), Formal index row, assigned to build-pipeline (assignment
only, no re-prove), build-pipeline's landing-report step elaborates it (0.2.40), matrix M-176, test
`test_parameter_default` red-proven then green, prover CROSS-LINK addendum on the day's record. INV-70
carries INV-31's TELL to numeric/config knobs, is kin to the economy ladder (T-19), rests on INV-4, and
frames push-on-own-certification as the human's granted trust (INV-9, resolving as M-6 already does).
Suite 177 green.

## 2026-07-08 (session 26) — 0.9.0 milestone: preventive audit + doc compaction, MINOR bump

**What:** the 0.9.0 milestone landed as Alexander framed it — a preventive audit plus doc compaction, then
the MINOR bump (0.8.75 → 0.9.0; plugin.json matched). What ran, all committed across the session:
- full whole-document SPEC re-prove (`docs/prover/2026-07-08-humanize-whole-doc.md`) — no must-fix;
- three parallel read-only audit passes (skill craft lens · compaction candidates · thin-loader/gates/index),
  record `docs/audit/2026-07-08/milestone-audit.md`; four craft/dedup folds landed (communicator 17→22
  rules, product-prover blank line, ARCHITECTURE intro de-dup, spec-author "when NOT" clause);
- stale-quote grep — fixed the OVERVIEW skill-roster drift (was five, omitted test-author + feedback-intake)
  + README miscount + one scissors, and EXTENDED the parity check to scan OVERVIEW with a red-proof;
- queue compaction — 38 terminally-landed rows archived (106 → 68 active), target-owner rows kept;
- SPEC "Open decisions" — D-2..D-5 collapsed to anchor-keeping pointers, rationale moved here.

**Honestly deferred:** the behavioural eval RE-RUN (spawning bare + with-skill arms per skill) was not run
this milestone — the evals' presence and four-section shape are green in the suite, and the craft lens
walked all 8 SKILL.md, but the behavioural arms are heavy and, per the evals' own honest-boundary note, a
"bare" session on this installed machine already carries the loader; a real behavioural re-run rides a
session that can spawn clean arms. Recorded, not silently skipped.

**Suite 176 green at the bump.** Not pushed — the push stays gated on Alexander's full-certification word.

## 2026-07-08 (session 26) — Open decisions D-2..D-5 collapsed to pointers; rationale moved here

**What:** the SPEC's "Open decisions" section held four already-decided items (D-2/D-3/D-4/D-5) carrying
their full dated rationale — settled history living in a live doc. Milestone compaction collapsed each to
a one-line resolved pointer that KEEPS its anchor (the anchors are cited elsewhere and belong to the
anchor-set guard), and the rationale moved here. Only D-1 (attic layout) stays genuinely open. Tested
constraints held: the D-3 close-needle "Decided 2026-07-07 (row 55)" stays in the section, the old open
D-3 wording stays absent, and D-2's forbidden open-override string never returns.

**The full rationale, as it stood in SPEC before the collapse:**

- **D-2 — model tier (decided 2026-07-07, row 56):** the model tier is proposed, never mechanically fixed
  — the routing rule reads the work's STEP and kind (not size alone) and the economy rung, proposes the
  cheapest sufficient tier, and the senior may override per wish with the override logged (proposed →
  chosen → why, on the checkpoint and the landing report). The rule's home is the delegation scenario
  (INV-69).
- **D-3 — snapshot retention (decided 2026-07-07, row 55):** last-only in the working tree; git history is
  the archive — the snapshot folder is git-tracked, an older baseline is one checkout away; a heavy surface
  keeps only its hash in git. Revisit if a dispute ever needs history git cannot serve.
- **D-4 — pack structure (decided 2026-07-05):** pack ↔ standalone-skill-repos structure is
  package-is-source — the pack repo is the single truth, standalone repos become read-only mirrors
  (Alexander's note: reusable parts must stay findable alone — exactly what mirrors give). The folder-NAME
  half had closed earlier the same day (`live-spec-base`). Execution: queue row 51 (mirrors + one sync
  command).
- **D-5 — personal-settings split (decided 2026-07-05):** all-into-profile — everything personal moves
  into live-spec settings with servlet-style scopes (nested, inherited), CLAUDE.md shrinks to a thin
  loader, and setup gains an "understand who you're working with" onboarding step. The scope model and the
  thin-loader shape are spec'd (the ladder and profile paragraphs, 2026-07-05, rows 52–53); the onboarding
  step remains row 54's landing.

## 2026-07-08 (session 26) — Architecture assignment-history moved out of ARCHITECTURE.md

**What:** ARCHITECTURE.md's intro carried a ~90-line inline log of every anchor-to-node assignment,
landing by landing. The method's own rule is history to JOURNAL, and the architecture doc should
state the structure as it stands today — so the log moved here and the doc's intro now points to it
in one sentence. Verified safe before the cut: every anchor the log named also lives in the
Nodes/Seams tables, and no test reads the intro prose (the anchor-ownership, pin-exist, and pin-drift
checks all read only the Nodes/Seams sections), so the anchor set and every gate stay unchanged.
Alexander's decision this session (the ARCHITECTURE humanize call: migrate the log, then
register-clean the reader-facing lines).

**The migrated log**, verbatim as it stood in ARCHITECTURE.md (assignment history from SPEC v0.7
through the row-47 landing):

Kept current through SPEC v0.14.0 by assignment
(E-16 → host-contract; the doors landing 2026-07-05: T-12/INV-16 → build-pipeline, E-17 → base-rulebook,
INV-17 → guardrails, A-10 → attach; the facet-sweep landing 2026-07-05 evening: T-13/INV-18 →
spec-author, the canonical facet list's one home; the fences landing 2026-07-05 night: T-14/INV-19 →
spec-author (the fence-authoring rule); the intake-trio landing 2026-07-05 night: T-15 → build-pipeline
(intake rider), INV-20/INV-21 → spec-author (the delta's closing sentences); the founding/design-sync
landing 2026-07-05 night: B-2 → attach (deliberately apart from templates' B-1: templates own the SHAPES,
attach owns the WALK that asks — the founding ask fires at bootstrap and at orient); the work-kind
landing 2026-07-05 evening, session 8: T-16/INV-22 → build-pipeline (intake classification + the per-kind
step table are its domain) — assignment only, no node or seam change, no re-prove per this doc's own
rule; the row-57 landing 2026-07-05, session 9: E-21 → attach (the installer it already pinned),
E-22 → communicator (rule 10, the seam report → human already carried the page) — assignment only;
E-18 → NEW [target]
node design-sync — a node ADD is a
structure change, its architecture-lens re-prove rides tonight's milestone audit (row 84) — assignments + pins, no node or seam change, so no
re-prove per this doc's own rule); the row-100 landing 2026-07-05 ~23:35, session 10: INV-23 →
base-rulebook (the workshop-noise law joins the shared rules), E-24 → templates (the ledger's shape is
a document shape; the pack's own `.live-spec/PROBLEMS.md` is package-docs' dogfood instance, pinned
there without moving the anchor) — assignments + pins only, no node or seam change, no re-prove per
this doc's own rule; the row-103 landing 2026-07-05 ~23:43, session 10: INV-24 → guardrails (the
clock fence is a mechanical check, its first slice living in the suite like the rest of gate b) —
assignment + pin only; the row-101 landing 2026-07-06 night, session 11: INV-25 → communicator (the
done-claim evidence walk is an answering exchange — its shape lives in rule 11, the pin updated by the
same landing) — assignment + pin only, no node or seam change, no re-prove per this doc's own rule; the row-102
landing 2026-07-06 night, session 11: T-17/INV-26 → build-pipeline (the one-story intake split and the
close-only-whole law are queue lifecycle, its domain; the resume template's per-leg line rides the
templates node's existing pins) — assignment + pin only, no node or seam change, no re-prove per this
doc's own rule; the row-105 landing 2026-07-06 night, session 11: INV-27 → communicator (the capture
echo and the departures board are exchange shapes — rule 12 and rule 9's station line; build-pipeline's
step zero cites the echo, the citation is not a second home) — assignment + pin only, no node or seam
change, no re-prove per this doc's own rule; the row-124 landing 2026-07-06 ~13:05, session 13: INV-33 →
build-pipeline (the craft ladder is the step list's own domain; four line pins re-run after the ladder's
insertion shifted them) — assignment + pin refresh only, no node or seam change, no re-prove per this
doc's own rule; the rows-126/127/128 landing 2026-07-06 ~13:47, session 14: INV-34 → communicator (the
pre-report walk is an exchange shape — the SPEC paragraph states the law, the walked procedure lives in
the skill); INV-28's bookkeeping NEVER-list rides communicator's existing INV-28 assignment; INV-24
STAYS with guardrails (the invariant is the clock law and its fences) while its chat arm's shipped
sentence pins in communicator — a wiring pin, not a second owner, same shape as design-sync's wiring
pins — assignments + pin refresh only, no node or seam change, no re-prove per this doc's own rule;
the row-131 landing 2026-07-06 session 15: INV-35 → communicator (working narration is an exchange
shape — the third voice between the echo and the report, the rule lives in the skill) — assignment
only, no node or seam change, no re-prove per this doc's own rule; the rows-129/132 landing
2026-07-06 session 16: INV-36 → attach (the founding walk that asks is attach's domain — B-2's own
precedent; the recorded `project.kind` line is a host-contract instance like every profile line),
INV-37 → build-pipeline (intake classification is its domain — T-16's precedent; communicator's
rule 12 carries the spoken arm as a wiring pin, not a second home) — assignments + pins only, no
node or seam change, no re-prove per this doc's own rule; the row-133 landing 2026-07-06 session 17:
INV-38 → communicator (the map on demand is an exchange shape — an answer to the human's ask, kin of
the echo's spoken placement; the sources it reads — spec scenarios, header, queue — stay owned by
their own nodes, the rule only reads them aloud) — assignment only, no node or seam change, no
re-prove per this doc's own rule; the row-135 landing 2026-07-06 session 18: T-18/INV-39 →
build-pipeline (the parallel-lanes law and the landing-purity invariant are wish-lifecycle law — INV-2
and T-9's own domain; ACT-3's isolated-tree sentence rides base-rulebook's existing ACT-3 assignment;
communicator's rule 9 carries the waiting-lane board face as a wiring pin, not a second home) —
assignment + pins only, no node or seam change, no re-prove per this doc's own rule; the row-136
landing 2026-07-06 session 18 (lane A of the first double-lane run): E-25 → attach (delivery and
version awareness are its domain — E-21/A-7's own kin; the script pin runs beside install.sh) —
assignment + pin only, no node or seam change, no re-prove per this doc's own rule; the row-54
landing 2026-07-07 session 23: B-3 → attach (the who-am-I-working-with step is the founding walk's
first breath — B-2 and INV-36's own precedent; the profile template ships as a document shape cited
inside B-3, the templates node's anchor list unchanged) — assignment + pin only, no node or seam
change, no re-prove per this doc's own rule; the row-165 landing 2026-07-07 session 23: INV-65 →
base-rulebook (a workshop-wide move, INV-23's own kin — the search fires at the same struggle moments
the ledger owns; ADOPT's setup line and the SPEC's ledger-scenario paragraph are wiring, not second
homes) — assignment + pin only, no node or seam change, no re-prove per this doc's own rule; the row-168 landing 2026-07-07 session 23: INV-67 →
communicator (the seat-switched showing channel is an exchange shape, rule 5's own domain; the
personal profile's show line is the local arm, said in the law) — assignment only, no node or seam
change, no re-prove per this doc's own rule; the row-167 landing 2026-07-07 session 23: INV-66 →
guardrails (a mechanical list-parity check, INV-24's first-slice-in-the-suite precedent) — assignment
only, no node or seam change, no re-prove per this doc's own rule; the row-55 landing 2026-07-07
session 23: E-7's DESIGN decided (home · manifest · advance-at-landed · last-only-with-git-archive,
D-3 closed with it) — the snapshot node stays [target] with its pin empty until the machine lands
(the guardrails scaffold, row 3, owns the first slice); prose update only, no node or seam change,
no re-prove per this doc's own rule; the
row-163 landing 2026-07-07 session 23: E-27 → NEW node test-author (the skill IS a node, the
spec-author/product-prover precedent) — a node ADD is a structure change: the architecture lens ran
with the landing (record `docs/prover/2026-07-07-row163.md`), the derivation seam named
(build-pipeline · test-author), the two working-skills seam cells recounted five → six;
The row-47 landing 2026-07-07 session 24: E-28/T-20/INV-68 → NEW node feedback-intake (the skill IS a
node, the test-author precedent) — a node ADD is a structure change: the architecture lens ran with
the landing (record `docs/prover/2026-07-07-row47.md`), two seams named (item → its home;
feedback ↔ communicator's echo), the outside-wish seam widened to outside ITEM (wish or feedback,
harvest destination by route, T-20), and the two working-skills seam cells reworded count-free (the
row-167/169 count-drift class: lists that enumerate stay complete, everything else describes without
counting); last full architecture-lens prove: v0.1, 2026-07-05. [E-14]

---

---

## 2026-07-07 (session 24, ~18:31) — First structured SPEC sheet + register finally in force

**What:** The prototype section was swept in two iterations. First a register rewrite of the two dense
paragraphs into short sentences. Then a restructure into lists (the label forms, the guardrail's three
legs, the norm law's four arms) with an H3, and a retitle from the scissors frame "A prototype is not
the product" to the positive "A prototype stays a sketch". The rename touched six live homes in one
commit: the SPEC header, three Formal-index cells, base rule 16 in live-spec-base, and two checks in
test_traceability. 11/11 phrases preserved, anchors intact, suite 175 green, prover cross-link recorded.

**Why:** Alexander pushed on three things this session, each a real gap. (1) The section titles and prose
should be structured, not a wall — lists where content is a genuine enumeration; this became a spec-author
rule ("use lists inside a scenario", guarded against the rejected structure-first shape). (2) The title
itself broke the scissors ban, so it was renamed. (3) The register kept leaking into chat because the
deployed `~/.claude/skills` copy was STALE — the register was committed to the repo but never installed,
so it never loaded. Root cause found via audit; `install.sh` re-run, deployed==repo. The profile gained
`language.register` as a clean always-on source, and the aim is to keep per-turn hooks minimal as the docs
model the voice.

**Result:** Format and register are now the standard for the rest of the sweep. Clean point to `/clear`;
the next fresh session continues the sheets in the structured format. Memory safe to wipe.

## 2026-07-07 (session 24, ~16:37) — Cold-start item 0: PLAYBOOK + CLAUDE.md rewritten in the register

**What:** The two human-facing method documents outside the live-spec tree — `PLAYBOOK.md` (in the
private playbook repo) and `~/.claude/CLAUDE.md` (the boot loader) — now read in the pack's writing
register (communicator's "The writing register" section: neutral native-English technical-writer voice).
Pushed to `happysasha18/playbook` at commit 18ec7b0.

**Why:** The register was frozen this session, and the documents that model the standard should follow
it first. Alexander named this as the cold-start first task, to be done on a clean context because clean
context writes prose better. PLAYBOOK got a full style pass: long dash-chained sentences split into short
SVO ones, one idea per sentence, active voice with a named actor, filler cut, and the three bold
scissors-frame rule titles ("a lead, not evidence" and siblings) rewritten as positive sentences.
CLAUDE.md got a gentle touch only, since it loads every session: caps softened, `⇒` arrows spelled out,
two semicolon run-ons split. Meaning was held constant and verified mechanically — all 15 section
headers identical, every date preserved, every anchor and repo name and path present. On Alexander's
"клод тоже правь" the one stale fact in CLAUDE.md was corrected: the pack has seven working skills now,
not four.

**Result:** Alexander read the rendered PLAYBOOK selectively and approved it ("sounds perfect"), and
told me to keep the reporting register I used. Item 0 closed; next is the SPEC-humanize sweep (item 1).

## 2026-07-07 (session 24, ~13:20) — Row 56: the model router lands (INV-69), D-2 decided

**What:** The pack now has a written rule for which model tier a piece of work is *proposed* at, and D-2
(the open question of whether size mechanically fixes the tier) is closed. SPEC INV-69 states it: a
judgment step (spec, prove, architecture, matrix-level calls, taste) proposes the senior and is never
routed down; a no-decision one-shot proposes haiku; a self-contained multi-step brief proposes sonnet.
The economy rung moves the threshold (`full` = the map as written, `lean` = an airtight brief one tier
cheaper, `tight` = the cheapest sufficient tier always). The proposal is advisory — the senior may
override per wish, logged as `proposed → chosen → why`. Owned by the build-pipeline node; elaborated in
its SKILL; matrix M-175, test `test_routing_rule`, red-proven then green. Pack 0.8.75, SPEC v0.15.61,
suite 175 green.

**Why the STEP, not the size:** the roadmap framed the router as "queue size-class → tier", but a large
row still holds mechanical sub-briefs and a small one is often pure judgment. Keying the proposal on the
step and kind (with size only a coarse prior) is what makes it honest — otherwise every large row would
route its spec work to a worker.

**Why advisory (D-2):** a mechanical tier-lock would strip the senior of the one call that catches a
brief that *looks* mechanical but hides a decision. So the router proposes and the senior may overrule
aloud; the log is the discipline that keeps the overrule from going silent.

**First routed landing (the second done-when leg):** this build routed itself — spec/prove/architecture/
matrix on the senior, the version-bump + installed-copy sync on a sonnet worker (~10 min saved,
checkpoint `row56-versionsync.md`), with one override logged: the SPEC prose clause sat in the code step
but was kept on the senior (routed up from the size-proposed sonnet) because spec prose is taste-heavy
[INV-62]. That override line is the proof the rule works in the hand, not just on paper.

**Prover:** CROSS-LINK, 4 findings, all folded — the one must-fix was the `[router target]` tag sweep
(the target-ownership test would have gone red on landing with the tag still live); the fold dropped the
tag from ACT-3's index fact, the header target-list, and the test's target map (the self-closing design).

**Alexander's feedback at landing:** the step-zero intake echo read as spec-jargon — he didn't follow
it. Two threads opened from that (both in NEXT_STEPS): (1) a human-first re-layout of the whole SPEC, to
be done from a fresh session (a responsible, standalone step); (2) the reporting/orchestration persona is
a **project manager** — reports to him in plain product-outcome language, jargon only trailing in parens.

## 2026-07-04 — Package born

**What:** Created the livespec skeleton repo — directory structure, four bundled skills, templates, adopt procedure, guardrails outline, install script.

**Why:** The method (spec → prove → reconcile → matrix → test → code → verify → commit) has been running in production on track-coach for over a year and is proven. It lives scattered: CLAUDE.md rules, four skill repos, a playbook, and a habit. The goal of livespec is to make the whole thing one attachable package — clone it, run `./install.sh`, and the skills land in `~/.claude/skills/` ready for any project. One home, not four.

**Why "livespec":** Alexander's coinage (2026-07-04). Working name; a better name may emerge (queued in ROADMAP).

**Status:** Skeleton only. Skills are read-only copies (source repos unchanged). No SPEC authored yet — that waits for Alexander's signal to publish, so spec-author runs on the full intended scope, not a moving target. Unpublished; local only.

**Decided:** Local-only for now. No GitHub creation, no push. When Alexander says publish, that is ROADMAP item 1 — create the repo, push, wire the skill install to the real source.

## 2026-07-04 — SPEC v0.1: the first self-application run
Alexander caught a real hole in ADOPT (it inventoried code but not existing DOCUMENTS) and added two more
wishes (attic-not-delete; version-control gate). Instead of patching ADOPT.md pointwise, livespec was run
on itself: three wishes → queue rows 8-10 → SPEC.md v0.1 authored covering the whole package (wish
lifecycle, both entry modes, actors, milestones, self-application invariant M-4). ADOPT.md and README will
be updated AFTER the prover pass (row 7) — spec before docs, by the book.

## 2026-07-04 — prover pass (row 7) + the honesty correction
FULL product-prover pass over SPEC v0.1: 11 findings (wish exit states; preemption path; surface-registry
entity; current-vs-target marking; profile owner+trust rule; provenance reconcile transition; baseline
advance timing; INV homes; human-gate re-listing; skill-version drift; checkpoint home). All folded → v0.2.
Alexander then challenged the "pioneers / no prior art" claim as possible people-pleasing. He is partly
right: artifact-baseline diffing is MATURE prior art in testing tooling (Jest snapshots, Percy, Chromatic
visual regression). Our narrower true claim: declared-scope diff as an agent pre-push guardrail + the
continuous-intake combination. README rewritten to credit lineage and link BMAD; long-tail search of the
skill ecosystem launched before publish.

## 2026-07-04 — first REAL adopt run (tlvphoto) + dogfood fix to ADOPT.md (row 4)
The adopt procedure ran end-to-end on a live host for the first time. The run's own story lives where it
belongs — in the HOST's journal (tlvphoto JOURNAL.md, entry "2026-07-04 — livespec adopt"); this entry keeps
only what changed LIVESPEC. (Trimmed 2026-07-04 late: the host story was originally written here too —
that duplication is exactly what the write-ownership rule now forbids.)

**Why this changed livespec itself:** the run proved `adopt/ADOPT.md` was STALE vs SPEC (it still had the old
inventory→reverse-spec→snapshot order, missing orient/attic/VCS-gate). Rewrote ADOPT.md to the SPEC A-0…A-7
sequence. One genuine refinement the run surfaced and I folded: the **version-control gate belongs FIRST**
(before orient touches anything) so the whole run is reversible — annotated SPEC A-0/A-5 (codes name
meanings, not a frozen order). A re-prove of the adopt section is due at the next milestone (minor reorder,
not blocking). Closes ROADMAP row 4; completes the "update ADOPT.md to the proven spec" tail of row 7.
Note: livespec repo was concurrently edited by another session (publish + rows 12-15) — this entry touched
only ADOPT.md, SPEC A-0/A-5, ROADMAP row 4, and this journal.

## 2026-07-04 — parallel-session protection (row 16) + codes-never-speak (row 17)
Two sessions edited this repo the same evening: one publishing (rows 1, 12–15), one running the tlvphoto
adopt (row 4) — the adopt session edited ADOPT.md/SPEC/ROADMAP/JOURNAL directly and avoided a collision only
by NOTICING the foreign commits and being surgical. Alexander: that must be mechanics, not luck — and a host
run's story belongs in the HOST's docs, not here.

Landed (SPEC v0.3): **INV-10 write-ownership** — only a session the human assigned to livespec itself writes
this repo; every other session is read-only except creating one new `inbox/` file. **INV-11 concurrent-edit
fence** — re-check HEAD/`git status` before every write and every commit; foreign changes ⇒ stop, re-read,
proceed surgically or back off; never push while another session is live (push coordination is the human's);
applies to host repos too. **E-11/T-10 inbox/** — one new file per outside wish; file-creation cannot collide,
so no-wish-is-lost holds without outsiders touching shared files. ADOPT.md now states the host-session
read-only rule. The row-4 entry above stays (it documents a real livespec change); under the new rule that
change would have arrived as an inbox wish.

Same evening, second leak of the same class (row 17): a session told Alexander "INV-8 рекомендует
GitHub-бэкап" — a spec handle spoken to the human. communicator rule 6 hardened from a soft "translate
internal ids" to a hard gate: spec handles (INV-x, E-x, A-x, T-x, row numbers, ⟨DECIDE⟩) are machine anchors
that never appear in a sentence addressed to the human; the leak itself is the rule's ❌ example now.

## 2026-07-04 — late refinements: anchors-in-parens, journal cleanup, push gate + its first run
Three refinements from Alexander the same night, all landed before the v0.3 push:
1. **Anchors in parentheses are allowed — with the WHY recorded** (row 17 refined): the plain sentence
   carries the meaning for the human; the trailing code serves the MODEL — transcripts are what it greps
   and self-monitors against, so a stable anchor makes past reasoning findable. Rule 6 rewritten from
   "codes never appear" to "a code never does the talking"; installed copy synced.
2. **Journal cleanup by the new ownership rule:** the row-4 entry held the tlvphoto run's full story — a
   HOST's story in the package's journal, the exact duplication the write-ownership rule forbids. Trimmed
   to the livespec-only part with a pointer to tlvphoto's JOURNAL (verified present there first).
3. **Push gate (M-6, row 18):** Alexander — livespec specifically gets a fresh whole-spec re-check before
   EVERY push. Spec'd and enforced immediately: prover pass docs/prover/2026-07-04-v03-push.md over v0.3
   found 7 findings in the new seams — the gate could regress on itself (fold→re-prove forever), an
   outsider's uncommitted inbox file would trip the very fence built to receive it, an inbox wish could
   wait durably-recorded but invisible, plus name-collision/record-naming/standing-routine edges. Six
   folded into SPEC same session (gate no-regress rule; outsider commits its inbox file + fence treats
   inbox files as benign; sessions sweep inbox first + milestone lists unharvested files; `-2` counter;
   dated record naming; standing routines count as assignment). Seventh recorded onto row 3's scope
   (guardrails scaffold also mechanizes the fence and the push gate). First push of v0.3 follows this entry.

## 2026-07-04 — first real inbox harvest + four wishes from Alexander (rows 19–26)
The inbox worked on its first night: the tlvphoto session dropped one committed wish file (three adopt
gaps, each with a primary source — remote never actually made to happen; adopt artifacts polluting the
host's data/; pre-existing gitignored cruft left on disk) and touched nothing else. Harvested → rows 19–21,
file removed in this commit per the inbox contract.

Alexander's four wishes the same hour:
- **Use-case-first spec (row 22, the big one):** the spec must read as a PRODUCT document — scenarios of
  what the human does and sees lead, codes only trail as anchors; explicitly ONE document, not a human copy
  and a model copy in sync (he named that alternative and prefers one readable doc). Held for his OK on a
  sample section shown in chat; guard for the restructure: the anchor SET before/after must be identical
  (grep-diff) so nothing formal is lost, then full prover + push gate. Propagation to the template and
  spec-author is row 23, strictly after.
- **Skill freshness is not event-only (row 25, landed):** at every safe breakpoint, re-stat installed
  skills + package on disk and re-read what changed — a parallel session may have shipped an update.
- **Base skill, the "Object class" (row 24, queued):** the rules every skill inherits (re-read-on-change,
  write-ownership/fence, anchors, checkpoints) stated once, referenced everywhere — also serves milestone
  compaction.
- **Context hygiene for long work (row 26, landed):** at a safe breakpoint the context may be compacted or
  cleared — the breakpoint's whole point is that disk holds the resume.
Push deferred: bundling with row 22's landing so the push-gate prover run covers both.

## 2026-07-04 — SPEC v0.4: the spec now reads as a product document (row 22)
Alexander OK'd the sample shape the same night ("давай полный прогон, потом пуш"). The whole spec
restructured use-case-first: sections are now scenarios ("Throwing a wish", "When a bug cuts the line",
"The package repo: who may write", "Attaching to a live project") — the prose talks to the human, every
code only trails in parentheses/brackets, and a Formal index closes the doc as the machine map. Explicitly
ONE document, not a human copy and a model copy in sync — the index is declared a derived map, and the
milestone now re-checks it against the prose so it can never become a second truth.

The guard held: anchor set v0.3 → v0.4 byte-identical (49 anchors, grep-extract diff). Push-gate prover
pass (docs/prover/2026-07-04-v04-push.md): 4 findings, all folded — package-governance section moved out
of the product story's path; index-drift check added to the milestone; D-1's expired "first adopt run"
trigger refreshed to "next"; README got the one sentence naming the new shape (full propagation to the
template + spec-author is row 23, its own landing).

Also folded from Alexander the same hour (row 26 refined): at a safe breakpoint the agent compacts its own
context to keep working and SAYS so — never silently; a full wipe/clear of the conversation is the human's
move. And row 27 opened: he floated renaming to "live-spec" (hyphen) — recommendation recorded (keep the
unbroken token), his call, awaiting his word; if renamed, the adopted host projects must be told.

## 2026-07-04 — communicator rule 8: retell, don't reference (row 28)
End of the same night, a live communication failure taught the last rule: the report "the inbox worked —
harvested into rows 19–21" meant nothing to Alexander until retold as a story (the other project's session
found three adoption gaps; before tonight it would have edited the package directly; instead it left one
inbox file and touched nothing else; the findings became queue rows). Same fact, only the second telling
communicated. Landed as communicator rule 8 (seven rules → eight): an event is REPORTED as a story that
stands on its own; internal bookkeeping (row numbers, file names) may only trail as an anchor, never
substitute. The failed/working pair is the skill's live example. Installed copy synced; the general
principle also recorded in the playbook. Old three skill repos: Alexander deleted them tonight — the
package is now the skills' only public home.
Push note: SPEC.md is byte-unchanged since the v0.4 push-gate record (2026-07-04-v04-push.md), so that
record covers this push's spec state per the gate's own terms.

## 2026-07-05 — the use-case-first shape propagated to the template + spec-author (row 23)
Row 22 proved the shape on livespec's own spec (v0.4); today the shape became the DEFAULT every future
spec is born with. `templates/SPEC.template.md` rewritten from a structure-first skeleton (Purpose /
Entities / States / Actors / Invariants / Composition / Glossary chapters) to a use-case-first one:
scenario sections lead ("what the person does" is the section name), entities are defined in bold where
the walk first meets them, invariants read as "always true while this runs" sentences, anchors trail at
line-ends, and a Formal index closes the doc — with all 11 sample anchors in the body covered by the
sample index, so the template models its own rule. `skills/spec-author/SKILL.md` updated to teach it: the
spine reframed from a section ORDER to a completeness CHECKLIST that lives inside the scenarios; two new
"How it reads" rules (scenarios lead · the index is a derived map, never a second truth); the anchor-set
guard for restructures written down as method (diff the sorted anchor list before/after — identical sets
prove no rule was lost); shape questions added to the completeness pass; two new anti-patterns
(structure-first layout, index drift). WHY the glossary changed: the proven v0.4 exemplar defines terms in
place (bold at first use) and has no glossary section, so the checklist now says exactly that, with a
separate glossary only when in-place stops scaling. Sibling skills swept for old-shape assumptions
(product-prover / build-pipeline reference no section order) — clean. Installed spec-author copy synced.

Session note (the morning's near-miss, cross-project): the session began with a wrong-project resume — I
picked up track-coach's NEXT_STEPS instead of livespec's (home-launched sessions share one memory; volume
of old track-coach notes ≠ assignment) and spawned two workers toward track-coach's tests before Alexander
stopped it. Both killed before a single write landed (git status clean, no files created — verified).
Rule saved to memory: cwd=home + no project named ⇒ ask which project, listing the NEXT_STEPS files on
disk; never infer from memory volume. Mechanical fix offered: launch each project session from its own
directory.

## 2026-07-05 — push-gate prover pass (fresh, on Alexander's word) + the push
Alexander cleared the push and asked for a fresh spec check first. Full prover pass over SPEC.md v0.4
(docs/prover/2026-07-05.md): 5 findings, 0 must-fix. One folded with the record per the gate's own-fold
rule — when a second bug arrives while one already holds the lane, the spec now says bugs take the lane
in arrival order and the parked wish waits until no bug does (T-9; before, two rules both claimed the
next slot and the agent would have picked silently). The other four became queue rows 29–32: one size
vocabulary for wishes (spec's four classes vs the queue column's S/M) · closed rows ARCHIVE at milestones
(reconciles "never deleted" with "nothing grows unboundedly") · versions need a disk home before A-7's
old→new note is writable · the global-default profile path is still unnamed. Anchor-set guard: byte-set
identical before/after the fold (checked against HEAD). Pushed: row 23 (use-case-first template +
spec-author) + this gate's record + the fold.

Also today, on Alexander's word, the working setup became a standing global rule (playbook 79d45a1 —
CLAUDE.md lives in the playbook repo via symlink, hence that commit): one window = one project (livespec ·
track-coach · tlvphoto), ask when the project is unsure, never infer from memory; livespec runs on Fable
only, as the package that will rule the other projects.

## 2026-07-05 — the three adoption fixes from the first real adopt run (rows 19–21) + row 33 opened
The tlvphoto pilot's inbox wishes became rules. (1) The remote is now a NAMED deliverable, not a
recommendation: by the first landing it exists or the human explicitly declined it, outcome recorded in
the run's journal — the pilot had ended local-only on a mere "recommended"; the bootstrap sentence carried
the same weakness and was fixed as the same class (A-5, INV-8). (2) Adoption's working artifacts (orient
digest, inventory, reconcile notes) got a home: `.livespec/adopt/`, TRACKED in git as the run's audit
trail — recommended pick recorded in row 20, Alexander may flip to gitignored; the pilot had polluted the
host's data/ (A-8). (3) The optional cruft sweep is spec'd as the ONE gated exception to never-delete:
regenerable junk only, listed with counts and sizes, human's explicit OK, authored content always via the
attic — INV-7 reworded to "never bends for anything authored" so the exception is a gate, not a buried
contradiction (A-9; ADOPT Phase 0.5). Push gate: CROSS-LINK prover pass over the three seams
(docs/prover/2026-07-05-adopt.md) — one drift found and folded (INV-7's index line), 0 must-fix.
Anchors: deliberate add of exactly A-8/A-9, indexed. Row 33 opened: Alexander asks whether the playbook
repo + CLAUDE.md symlink are still needed — recommendation recorded (keep as the thin private layer;
audit/shrink after rows 12 and 24), his call.

## 2026-07-05 — the classifier learns priority, the queue speaks one language (rows 29+34), the roadmap gets a face (row 35); rows 34–36 opened
Alexander asked for two things in passing and both landed as one classification scheme. First, priority
(row 34): a wish is now classed by size AND priority — critical (the shipped product is broken for its
user) lands before everything, a quick win may bubble up between landings with the jump marked in its row,
and an ambiguous call is ASKED at intake, never guessed — until answered the wish carries normal and the
lane keeps moving (INV-12, T-11, T-9 graded). The starvation edge is fenced: after one bubbled landing the
queue head goes next. Second, the size vocabulary unified (row 29, queued since the morning prover pass):
the queue's S/M column swept to the spec's four words — bug / small / surface / large — as a Class column
that also carries the priority mark. SPEC v0.4 → v0.5; anchors: deliberate add of exactly T-11 + INV-12.
Push-gate CROSS-LINK pass (docs/prover/2026-07-05-classes.md): 3 findings, all folded before push — order
among two waiting critical bugs (by arrival) · a bug in the lane is never itself interrupted, so at most
one wish is ever parked · the real catch: ROADMAP.template.md still TAUGHT the old S/M/L scale, so every
future host would have contradicted the one-vocabulary rule on day one — template rewritten (the
never-patch-pointwise rule earning its keep). Row 35 landed the same hour: when reporting where-we-are,
the roadmap renders as a bulleted icon list (✅🔨⬜🙋), current item marked, finished stretches collapsed —
communicator rule 9, installed copy synced. This landing itself ran as a quick win bubbling ahead of
row 24 — on Alexander's explicit word, and marked in the rows. Mid-landing Alexander threw row 36
(package defaults a host overrides — e.g. full prover pass per push for livespec vs big-versions-only for
track-coach; refined minutes later: some settings are personal and global, like docs-English /
chat-Russian): recorded as a three-layer design (package defaults → global personal profile → per-host
override), to be designed with row 24's base skill.

## 2026-07-05 — roadmap list lines gain substance (row 37)
Alexander's read on row 35's first use: the icon list reads fine, but the lines are bare titles — he
wants each a bit more informative. Refined communicator rule 9: every line now carries one clause of
substance matched to its status — a landed item says what it changed, an in-work item what is happening
now, a queued item what it will give, a waiting item exactly what is asked. The WHY is quoted in the rule
so the refinement survives a memory wipe. Installed copy synced; landed as a quick win inside the same
report exchange (row 37). Push gate: SPEC unchanged since the same-day green pass, verified by blob hash
(docs/prover/2026-07-05-rule9-detail.md).

## 2026-07-05 — the base skill + the settings ladder (rows 24+36, with debts 31+32; SPEC v0.6)
The pack grew its fifth skill and its spine. Until today every working skill carried its own near-copy of
the shared working rules, and copies drift — the evidence sweep that opened this landing (a junior read of
all four SKILL.md files + templates + ADOPT.md, raw greps kept in the session scratchpad, spot-checked by
re-running one) caught the anchor convention told two ways and the concurrent-edit fence stated only in
the adoption text while every writing skill needs it. So the shared rules now live ONCE, in
`skills/livespec-base/` — twelve of them, the list derived from what the sweep actually found repeated,
not from memory — and each working skill opens with a one-line inherit note instead of restating them;
pruning the old restatements is deliberately deferred to milestone compaction, skill by skill, never one
risky rewrite (SPEC E-12, INV-13).

Settings became a three-step ladder (SPEC E-13, INV-14): package defaults (a table in the base skill) →
personal profile at `~/.claude/livespec/profile.md` (about the human, follows him everywhere — his
language split, max-proactive mode, written from his recorded standing words) → host profile in
`.livespec/` (about the project). Host beats personal beats default; an override exists only as a written,
dated line; an unknown line is ignored aloud, never silently. livespec's own push gate turned out to BE
the worked example — the every-push prover re-check is now also recorded as this repo's host-profile
override of the "before MINOR bumps" default, one fact with M-6 as its normative home.

Two queued debts landed on the way, as their rows had planned: versions got homes (root VERSION 0.1.0 +
`version:` frontmatter in all five skills — row 31, SPEC M-7) and the global profile path got its name
(row 32, open pick D-5). The prover's cross-link pass (docs/prover/2026-07-05-base-skill.md) folded three
must-fixes before push — the sharpest: the inherit notes pin the base version as four literal copies, so
the spec now obliges the landing that bumps the base to sweep the pins the same session — and opened row
38 (the personal profile has no git home yet). Open picks for Alexander, lane not blocked: base folder
name (D-4, `livespec-base` current) and personal-profile home (D-5).

## 2026-07-05 — decision page prototype + the first mined gap folded (rows 39, 12; skills → 0.1.1)
Alexander proposed a better way to be asked: instead of reading an MD questionnaire, an interactive local
HTML page in the browser — radio options, a note field per question, a Download JSON button — the way he
already tunes images in tlvphoto; the agent then reads the downloaded JSON. Taken as row 39 (quick win,
jumped the queue inside the same exchange) and used immediately for real: the five standing open picks
(base folder name, personal-profile home, livespec vs live-spec, playbook fate, adopt artifacts in git)
became the first page, headless-render gate before showing (6 cards + live counter). The page is a session
artifact; the durable record is the downloaded JSON folded back into this queue. Folding the mechanism
into communicator is queued as its own landing.

Row 12 folding began with gaps 1+2 taken as one class — primary-source discipline. The rule existed only
in the private playbook; now it is base rule 13 (a claim about what code does / what happened / who
decided rests on a citation — file:line, commit, a command just run; memory, a worker's summary, a doc's
prose are leads, not evidence), with its two working faces referenced where they bite: build-pipeline's
reconcile step (the reconcile note cites primary sources, never the doc's own prose) and a product-prover
meta-rule (claims about the shipped system key on the reconciliation note's citations — prose that outran
the code would otherwise "prove" dead behaviour). Base bump 0.1.0 → 0.1.1 swept the four inherit-note pins
the same session, as the spec obliges (E-12); all five skills and the package VERSION now read 0.1.1. The
mining map itself moved from /tmp to the private playbook repo (it quotes the private rules — not public
material), commit 05b13af there; row 12 pointer updated. No test suite exists in this repo yet to extend
(guardrails are row 3) — the folded rule's verification stays the prover's push-gate pass for now.

Also answered aloud: other project windows already receive pack updates by themselves — install.sh copies
the skills to the global ~/.claude/skills, every session loads from there, and base rule 8 (freshness)
makes long-running sessions re-stat and re-read on change; the livespec session's only duty is to sync
installed copies after each landing. What is NOT automatic yet is formal adoption (the .livespec/ attach)
— track-coach is queued as the first formal adopt-host.

## 2026-07-05, 11:50–12:20 — The lost layers return; the package becomes live-spec

The morning decision page came back as JSON (answered 08:49; archived in docs/decisions/) — the first
full round-trip of the mechanism, five picks harvested the same session. Three of them landed today's
movements; two grew into new design work.

**The lost layers (row 41, Alexander: "очень важный момент").** When the method was distilled from
track-coach practice into the pack, the layers between the proven spec and the tests silently dropped
out — a matrix TEMPLATE shipped, but not the method that produces a matrix, and no architecture document
at all. Both are now first-class pipeline steps no wish may jump: an ARCHITECTURE.md written from the
proven spec (named nodes, one responsibility each, every spec fact owned by exactly one node, named
seams; in live code every node pinned to its owning file:line — which is where the old standalone
"reconcile" step now lives), proven by product-prover with an architecture lens whenever it changes; then
the matrix DERIVED node × fact, closing with a coverage-validation checklist that is actually walked
(SPEC v0.7: E-14, E-15, INV-15; new ARCHITECTURE template; build-pipeline 0.2.0; prover + spec-author
0.1.2 for the lens and the pointer). Decided by delegation ("или как сам решишь"): the architecture
prover pass fires when the doc CHANGES, not on every landing — a bug cites its node and moves.

**Decision page becomes law; time enters the records (rows 39/45/46).** Communicator rule 10 now states
the mechanism: several open picks → one interactive page, radio + recommendation + free-form per card,
JSON filename carrying the PROJECT name (several projects share one Downloads folder — Alexander caught
it this morning), answers archived and harvested same session. Base rule 9 now requires date AND time on
journal entries and harvested records — "вчера вечером ты написал X" must be answerable from the record
(communicator 0.1.2, base 0.1.2, four inherit pins swept).

**The rename (rows 27/40).** Alexander picked live-spec over the keep-recommendation. One name
everywhere, so the sweep took the machine tokens too: 97 occurrences across 14 files (a sonnet junior ran
it; senior re-ran the verification grep), the base skill folder is live-spec-base (closing the name half
of D-4), the host folder .live-spec/, the profile home ~/.claude/live-spec/. Dated history — this
journal's older entries, prover records, decision JSONs — intentionally keeps the old spelling; MIGRATION.md
tells each adopted host what its own session runs at the next update. GitHub repo + local clone dir
rename wait for the reviewed push, so the outward move is one atomic step.

**New in the queue from midday messages:** feedback-collection as a pack skill (row 47), a maintenance
skill with measurement plugins — analytics per user story/axis (row 48), A/B experiments for software
hosts (row 49), learning from other frameworks as its own version bump (row 44). Rows 42 (pack
structure) and 43 (personal-settings split) went out as today's second decision page, worked examples
included, gate-checked before showing.

**Status:** three commits today before this entry; VERSION goes 0.1.1 → 0.2.0 with the whole-spec prover
pass that closes the session (MINOR gate: this pack has no matrix yet — guardrails are row 3 — so the
audit is the prover pass + the queue re-listing, said honestly). Push held for Alexander's review.

## 2026-07-05, 12:40–13:10 — Gate green, 0.2.0, and the afternoon answers

The session's prover gate ran as a FULL pass over SPEC v0.7 (record: docs/prover/2026-07-05-lost-layers.md)
and did its job: 10 findings, the sharpest being that the new layer invariant was unsatisfiable for every
EXISTING host — live-spec's own repo first — because nothing owned creating the two new documents, and
adoption still produced the old flat matrix. All ten folded the same session (bring-up rule + queue row 50;
adoption Phase 5 rewritten "architecture, then the matrix"; a bug may now ASSIGN an orphan fact to a node
so no critical fix is ever the thing the rules forbid; the template owns the coverage checklist; stale step
numbers and one-vs-at-least-one wording swept). VERSION 0.1.1 → 0.2.0 — the MINOR gate's matrix-audit leg
is honestly N/A until row 50 exists; said, not skipped.

The afternoon decision page came back at 12:48 (archived docs/decisions/2026-07-05-decisions-2.json):
**package-is-source** — the pack repo is the single truth, standalone repos become per-skill mirrors
(Alexander's note about reusable parts staying findable alone is exactly what mirrors give; row 51), and
**all-into-profile** — against the recommendation: everything personal moves into live-spec settings with
servlet-style scopes (nested, inherited), CLAUDE.md shrinks to a thin loader, and setup gains an
"understand who you're working with" onboarding step (rows 52–54). The mid-session interruption cost
nothing: three commits were already on disk, the uncommitted folds survived in the tree, and the resume
file told the truth — the discipline paid for itself the first time it was tested.

## 2026-07-05, ~13:30 — Push released (session 4)

Alexander's steady-state call came in plain words: nothing left to review at a green gate — push. Fence
re-check passed (clean tree, no inbox deposits, remote unmoved), and the five held commits went out
(b6e2827..70b71f9): the lost layers, the decision-page law, the rename-in-content, the 0.2.0 gate. The
one piece the harness would not let this session do is the OUTWARD half of row 40 — renaming the GitHub
repo itself (an external write the permission layer reserves for a human). So the rename is now split
honestly: content says live-spec everywhere (pushed), the repo/clone-dir rename waits on one command from
Alexander (`gh repo rename live-spec --repo happysasha18/livespec --yes`), after which the local dir move
and remote URL update are mechanical. Recorded here so the split is a fact with a reason, not a drift.

## 2026-07-05, ~14:00 — Row 50 lands: the flagship gets its own architecture and derived matrix

The bring-up the lost-layers session promised: live-spec now walks its own new pipeline. ARCHITECTURE.md
v0.1 names 12 nodes (five skills, templates, attach = ADOPT+installer, inbox, host-contract, the pack's
own docs, and the two honest [target] machines — guardrails and snapshot); all 69 spec anchors are owned
exactly once, every pin taken from a command run this session, none from memory. The architecture-lens
prover pass (docs/prover/2026-07-05-architecture.md) earned its keep on the first walk: the sharpest
find was S-0's broken promise — the spec swears every [target] machine has a queue row, and two didn't
(snapshot, model router → rows 55–56); it also caught the spec still claiming two decision pages were
"out" that Alexander had already answered (D-4/D-5 rewritten to their decided state, SPEC v0.7.1), and
a queue header with no date where M-3 requires one. Eight findings total: three must-fix folded in
session, two queued as row 57 (installer and decision page deserve spec sentences), three recorded.

TEST_MATRIX.md v0.1 derives 64 rows node × fact, every row with a DO and a NEVER side, and the honest
adaptation for a text product recorded in its header: the "rendered level" here is a string assertion
against the SHIPPED file — no browser surface exists, so the browser-level clause holds vacuously and
re-arms the day one ships. The coverage validation is not a checklist walked once: it is mechanized in
tests/test_traceability.py — 20 tests, zero deps, green with zero skips — and the walk went red on real
defects before it went green (unowned A-6/E-7, a range token double-counted), which is exactly the
red-first the method asks for. INV-15 binds from this landing. VERSION 0.2.1. Push held for Alexander's
look; the prover record doubles as the push-gate re-check for this state.

## 2026-07-05, ~14:10 — Iterativity enters the method (row 58), everything pushes

A piggyback wish with a perfect origin story: tlvphoto's agent asked Alexander "should I write the
architecture several milestones ahead?" — and the method had no sentence to answer with. Now it does,
in every home the question could be asked from: SPEC E-14 (v0.7.2) — the architecture doc is iterative,
maps the product as it stands plus the landing in flight; a node exists for what ships or what an owned
queue row already promises ([target], pin empty); a future feature earns its node when its landing
arrives, and a speculative node is unbacked structure, the structural twin of a silent micro-decision.
Same sentence in ARCHITECTURE.template.md and build-pipeline step 3 (skill 0.2.1, installed copy synced
so every host on this machine reads it at the next freshness check). Cross-link prover check green
(docs/prover/2026-07-05-iterativity.md) — the [target] node rule and INV-15's assign-on-landing already
compose with it cleanly. Row 58 landed the hour it was spoken. VERSION 0.2.2. Push follows on
Alexander's word given in the same message.

## 2026-07-05, ~15:45 — Rows 53 + 3 land, row 51 lands reduced, row 52 designed (session 4, afternoon)

**What:** Four movements in one afternoon stretch, on Alexander's "поехали" (~15:05) — he also set the
version plan: the next MINOR bump goes straight to **0.5.0** (his word, marking the volume since 0.2),
with the 3-pass preventive audit before it as always.

- **Row 53 (scope model):** SPEC v0.8.0 — the settings ladder generalized to four NESTED scopes with
  inheritance, resolution narrowest-out: session > host > personal > package default. The session scope
  is named for the first time: the human's live word, never a file; the agent never writes it; making it
  outlive the session is a PROMOTION into a profile, journaled. Base skill ladder rewritten (0.1.3, four
  inherit pins swept, installed copies synced). Prover pass docs/prover/2026-07-05-scopes.md: 3 findings
  (1 must-fix — the migration fork must never write a foreign repo), all folded same pass. New anchor
  E-16 owned by host-contract; matrix M-002 updated, M-065 added (70/70 anchors).
- **Row 52 (personal-layer migration) — designed, flip gated:** migration map + thin-loader draft +
  profile-v2 draft written to ~/.claude/playbook/row52/ (private repo — doubles as the git home row 38
  asked for, via a proposed symlink). Flip blocked on: folding row 12 gap 3 (fix-the-class — the one
  CLAUDE.md rule with no pack home yet) and Alexander's review of both drafts. Rollback = one copy back.
- **Row 3 (guardrails, pack slice) — landed by a Sonnet worker:** guardrails/ with pre-push gates
  (prover record · green suite · anchor ownership · matrix coverage) + opt-in commit fence + install.sh;
  hooks installed, each gate proven by deed incl. a failure case; 15 new tests. The worker caught its own
  test-recursion bug (pre-push invoked inside the suite re-discovering the suite) and fixed it with
  scratch-copy fixtures. Spec/architecture/matrix reconciled to the shipped slice (M-4 now mechanical
  for the pack; E-6 host-facing set stays [target]).
- **Row 51 (mirrors, reduced) — landed by a Sonnet worker:** scripts/sync-mirrors.sh + product-prover
  mirror synced to 0.2.2 (idempotency proven). Discovery: spec-author had NO standalone repo — the
  standing note was wrong. Creating four mirrors awaits Alexander's word (new public repos are his gate;
  the permission classifier enforced the same line when the first worker brief included repo creation).

**Why this order:** Alexander asked to distribute and economize — judgment (scope design, spec, prover)
stayed on Fable; both bounded rows ran on Sonnet in parallel with checkpoints. Old-name leftover
("livespec") found and fixed in the personal profile — a file outside the repo the row 40 sweep missed.

## 2026-07-05, 15:05 — Gap 3 folded (fix the class, sweep look-alikes) + three decisions from Alexander

**What:** The "never patch pointwise" rule got its pack home: base rule 14 (a found defect is a sample of
its class — sweep the repo and every user-facing surface before calling the fix done), the bug entry path
in build-pipeline now says the matrix row and red-on-bug test cover the CLASS not the instance, and
product-prover Phase 3e gained an eighth stress family, "Sibling instances" (sweep the document, write one
class finding listing every instance). The rule-list in all four working skills' headers + their base pin
(v0.1.4) swept in the same change — itself an application of the new rule. Versions: base 0.1.4,
build-pipeline 0.2.2, prover 0.1.3, spec-author 0.1.3, communicator 0.1.3.

**Also landed, same sitting:** (1) SPEC v0.8.1 — hooks are OFFERED, never imposed: on a host, git hooks
only where git exists and only after asking the human with a plain-words explanation (Alexander's word,
~15:00; rides E-6, row 57 keeps the installer/decision-page half). (2) README status line — the drifting
pinned "v0.1.0" replaced by the rule (release number lives in VERSION only) plus a plain explanation of the
two counters: VERSION counts package releases, the SPEC header counts spec revisions, and the spec's
counter runs ahead by design. Class-swept: no other drifting version pin in prose (the base-pin lines in
skill headers are deliberate written-against pins).

**Decisions by Alexander (this session, ~15:00):** NO new mirror repos — live-spec stays the one pack
repo, product-prover the sole standalone mirror, name unchanged (row 51 closed for good); one push after
today's tidy-up, not now; night audit run by Opus with a Fable spot-check of one pass (the model-comparison
sample), skill-creator eval (row 5) rides the same night.

**Why:** Gap 3 was the one CLAUDE.md rule with no pack home — the named blocker on row 52's flip
(CLAUDE.md → thin loader + profile). With it folded, the flip waits only on the drafts review.

## 2026-07-05, ~15:40 — The 0.5.0 preventive audit: run, compared across models, folded (session 5)

**What:** The full MINOR gate, run in daylight instead of overnight on Alexander's "поехали". Three audit
passes plus the skill-creator eval ran as parallel Opus workers; pass 1 (whole-spec prover) ran TWICE —
Opus and Fable independently, same brief, no cross-reads — as the model-comparison sample Alexander asked
for. Two workers hit the plan's session limit at the finish line but had already written their reports to
disk (checkpoint discipline paying for itself — zero loss, no resume needed). All records in
`docs/audit/2026-07-05/` (five reports + `model-comparison.md`).

**Results:** matrix pass — suite 35 green at audit time, 70/70 anchors each owned exactly once, zero
must-fix; composition pass — 20 surfaces, clean naming, zero must-fix; prover passes — Opus 4 must-fix /
8 should / 2 worth, Fable 1 / 5 / 3, agreeing on the headline defect: INV-2's serial-lane rule never said
how it scales to two sessions or delegated workers, while the flagship's own journal records blessed
parallel workers. Skill eval: all five skills sound, repo/installed copies byte-identical; one cross-skill
defect (top-level `version:` where the canonical validator wants `metadata.version`).

**Folded the same sitting (SPEC v0.8.1 → v0.9.0, anchor set unchanged):** the lane got its token (the
single in-work row; workers may overlap only on disjoint files under the fence, landings close serially);
a parked wish resumes ahead of any quick-win bubble; inbox harvest is one atomic commit per file,
idempotent on re-sweep; closed queue rows ARCHIVE at milestones, never delete (folds row 30 — the INV-1
vs compaction contradiction Opus caught); push-gate folds are enumerated in the record and stay local;
profile files got explicit tracked-ness (host profile tracked, created at attach; personal profile may
live in a PRIVATE human-owned git home — the wording fix that unblocked the row-52 flip); the inbox is
now host-general (every host gets the parallel-safe door); unrecognized profile lines leave a durable
journal note, not just a report line; [target] adoption phases are recorded-and-skipped; arrival ties
resolve by row order; M-1 gains the derived-header re-pin rule; version homes moved to `metadata.version`
across all ten SKILL.md copies (matrix M-001/M-002/M-012 reconciled, M-066 added, new
`test_settings_ladder_documented`). Architecture pins re-verified — one (`:83` ladder) was stale BEFORE
this session; all four corrected. Non-folded findings became queue rows 59–69.

**Model comparison verdict (the budget question):** Opus was fully sufficient for scaffolded document
review — denser findings, sound severity, best single fix proposal (the lane token). Fable's edge showed
in cross-document timeliness (catching that E-16's old wording would contradict the imminent row-52
landing) and severity restraint. Split confirmed: audits on Opus, fold triage and spec wording on Fable.

**Verified:** suite 36 green, zero skips — worker's run AND the senior's own re-run (the session's
delegate spot-check). VERSION 0.2.4 → 0.5.0 on Alexander's standing word (the straight-to-0.5.0 plan,
~15:00). Push still held for his review, per the same word.

**Also:** Alexander OK'd the row-52 five-line summary (~15:34) — the loader flip executes immediately
after this commit; its own journal entry follows.

## 2026-07-05, ~15:50 — Row 52 flip staged to one human command; row 38 closed (session 5)

**What:** Alexander OK'd the five-line summary (~15:34). Executed the reviewed checklist: pre-migration
`~/.claude/CLAUDE.md` AND the old personal profile attic'd (`playbook/row52/attic/*.2026-07-05`); profile
v2 written to its git home `playbook/personal/profile.md` (private repo, pushed — 5aa79a8) with
`~/.claude/live-spec/profile.md` now a symlink to it, which lands row 38's backup/history debt with the
same move; the final loader text staged at `row52/CLAUDE.final.md`.

**The one step that did NOT execute by agent hand — by design:** the permission classifier refused the
agent's rewrite of `~/.claude/CLAUDE.md` (self-modification of the global instruction file on a
narrated OK). That refusal is the method's own INV-9/ACT-1 line drawn by an outside machine: the swap of
the human's standing instruction file is the human's move. Alexander runs one command
(`cp ~/.claude/playbook/row52/CLAUDE.final.md ~/.claude/CLAUDE.md`); rollback is the same command from
attic. Row 52 marked "flip staged"; it closes on his copy.

**Why journal this:** the audit had just folded the worker-contract seam as a queue row (who may write
what a session's own machinery may not) — and an hour later a live permission gate enforced exactly that
seam against the senior itself. Primary evidence for row 59's design.

## 2026-07-05 (session 6, evening) — the 0.5.0 push lands; the Room incident files rows 70–71

Row 52 closed at Alexander's own hand (~16:12, the one `cp`; diff-verified identical) — the thin-loader
migration is live. The push gate then ran as designed: FULL prover pass on an Opus worker (per the
morning's model-split decision), senior triage. It found two real must-fix holes the morning's audit
folds had left — the lane token was a bare read, not a committed claim (two parallel sessions could
double-land, INV-2), and the milestone archive could swallow a deferred wish whose revisit trigger
hadn't fired (INV-1 violated by its own clause). Both folded as narrow wording fixes + three smaller
folds (inbox arrival = harvest moment; unreachable harvest-recovery parenthetical rewritten; the
architecture's stale loader pin flipped to landed). SPEC v0.9.0 → v0.9.1, anchor set unchanged, suite 36
green twice (before and after folds). Record: docs/prover/2026-07-05-v05-push.md.

**The Room incident (why rows 70–71 exist and cut the line).** Alexander, hot and right: tlvphoto's
similarity room was hand-built over the infrastructure past the pipeline — its own spec named Room a
"later surface, not yet specified", and no pack law made that line binding, no law defined "prototype",
no machine check compared the prod build against the spec. The agreement was "load casually, the system
lines it up" — the recognition half was never made a mandatory step. Rows 70 (feature-recognition
tripwire: classification said aloud before any code; hard triggers replace judgment) and 71 (prototype
quarantine + prod-traceability guardrail) land next, one pipeline landing; wish relayed to tlvphoto's
inbox (created with the file — the host had none). Fitting coda: while filing those very rows the
traceability suite went red on the senior's own class-cell vocabulary — the gate caught the gatekeeper,
live evidence that tripwires beat judgment.

## 2026-07-05 (session 6, ~17:40) — rows 70–71 land: the door law + the prototype law (the Room incident folded into the method)

Why this exists: Alexander, this afternoon, hot and right — tlvphoto's similarity room was hand-built
past the pipeline and shown as product while its own spec said "later surface, not yet specified". The
agreement was "load casually, the system lines it up"; the recognition half was guidance, not law. Two
laws land, one pipeline landing (door: feature, size: surface):

**The door (SPEC T-12, INV-16).** Classification is an explicit step said BEFORE any code: every wish
names size · priority · door (feature · bug · refactor · docs-only · skip) in one intake line. Hard
tripwires replace judgment — new visible surface / new state / new interaction / a [target]-marked
surface / unbacked behaviour ⇒ feature, however casual the ask. The verdict outranks a casual "bugfix"
label; queue-cutting stays with the bug door; the door re-fires mid-work the moment work is about to
create something its door doesn't grant.

**The prototype (SPEC E-17, INV-17, A-10).** Exploring is legal but fenced: prototype/ home, label per
artifact kind, senior-only creation, shown only as a sketch; promotion re-enters at the spec step.
Machine tooth shipped: guardrails gate (e) `check-prototype-fence.sh` — a prod file referencing into a
prototype home blocks the push (red-first proven). Adoption now gives every unbacked live surface a
human verdict: promote / quarantine / attic.

Pipeline walked in full: spec delta → CROSS-LINK prove (Opus worker; 4 must-fix + 6 clarify, ALL folded
— record docs/prover/2026-07-05-doors.md) → architecture assignments (T-12/INV-16 → build-pipeline,
E-17 → base-rulebook, INV-17 → guardrails, A-10 → attach; no node/seam change, no re-prove per the
doc's own rule) → matrix M-067..M-071 → tests (traceability class TestDoorLawAndPrototype + guardrails
TestGateE, red-first) → code (base rules 15–16 v0.1.5; build-pipeline step zero v0.2.3; prover ninth
lens v0.1.4; communicator PROTOTYPE-label line v0.1.4; spec-author [target]-tag rule v0.1.4; installed
copies synced) → sweep (README step 0, ROADMAP header + template, PLAYBOOK principle line — pushed).
Suite 36→43 green. Worker split held: Opus proved, Sonnet built the fence + its tests (checkpoint
`.live-spec/checkpoints/2026-07-05-prototype-fence.md`), Fable folded and worded. Alexander's second
wish of the evening (feature intake must sweep the standard facets a layman can't name — responsive,
touch, states) filed as row 72, enters next; row 44 (learn-from-others) will feed it.

## 2026-07-05 (evening, session 7) — row 72: the facet sweep — SPEC v0.11.0, pack 0.5.2

WHY: the Room incident's third lesson (after the door and the prototype laws). Alexander can't be
expected to ask "and what happens on a phone?" — the dimensions a layman can't name (narrow layout,
touch-vs-hover, empty/error/loading, accessibility, performance) simply never got a sentence, and the
Room shipped hover-only with no phone layout. The fix: when a wish's door says feature, drafting the
spec-delta walks the canonical facet list (its one home: spec-author). Every facet ends as a SPEC
SENTENCE — decided, or the recommended default taken with the literal `[default]` tag and reported back
as a plain-words tradeoff, batched. Silence stopped being a legal outcome.

Pipeline walked in full: spec delta → CROSS-LINK prove (Opus worker; 1 must-fix + 4 clarify + 2
worth-considering, ALL SEVEN folded — record docs/prover/2026-07-05-facets.md; the must-fix was real:
a defaulted facet had no durable home, hence the `[default]` tag) → architecture assignment
(T-13/INV-18 → spec-author, pin :144; no node/seam change, no re-prove) → matrix M-072..M-073 → tests
(TestFacetSweep, red-first proven) → code (spec-author facet-sweep section + completeness bullet
v0.1.5; communicator rule-10 tradeoff line v0.1.5; build-pipeline step-1 sweep sentence v0.2.4;
installed copies synced) → suite 45 green, 0 skips. Per the prover's process finding (F4) the MINOR
spec bump owes a FULL pass at the push gate — run before this push per M-6.

Same evening, before the landing: Alexander banned calques outright (Russian chat had been carrying
loan-translated pack terms — «растяжки», «та же семья»). Contract line `language.no-calques` live in
his profile (playbook 234bce6); pack-general rule filed as row 73 (communicator + base), lands next.

Push gate (M-6): FULL pass on an Opus worker (docs/prover/2026-07-05-v11-push.md) — ready-to-push, zero
must-fix, 77 anchors symmetric, all seven facet folds verified in prose. Its one should-clarify (a
headless feature — new persistent state, no visible surface — would owe layout sentences) folded same
sitting: the sweep scopes to VISIBLE surfaces, a headless feature writes one explicit "no visible
surface — facets N/A" line -> SPEC v0.11.1. Suite 45 green; pushed.

## 2026-07-05 (evening, session 7, second landing) — row 73: no calques — base 0.1.6, pack 0.5.3

WHY: twice in one day a Russian-chat report carried English pack terms as literal translations
(«растяжки» for tripwires, «та же семья»); Alexander: "НЕЛЬЗЯ использовать кальки… это позорит наш
продукт". The personal contract line (`language.no-calques`, his profile) had already landed; this
landing bakes the language-pair-general rule into the pack itself. One home per rule held: the ban
lives in base rule 2 (the plain-words rule — a calque is its cross-language case), communicator rule 6
elaborates with the field example. Spec step concluded NO spec delta: the rule elaborates an existing
base rule; SPEC's one-rulebook clause (INV-13) already owns the home. Test test_no_calques_rule; base
0.1.6 (pins swept across the four working skills by a Sonnet worker, checkpoint
2026-07-05-row73-mechanical.md — the delegation rule held this time), communicator 0.1.6, spec-author
0.1.6, build-pipeline 0.2.5, product-prover 0.1.5; installed copies synced; suite 46 green. Same
sitting: row 74 filed (a plain-language map of the whole structure — Alexander can't hold where things
live; he is right, and the two research agents on row 44 homework are running in the background).

## 2026-07-05 (night, session 7) — rows 77+85: non-goals, appetite, success measure — SPEC v0.13.0

WHY: Alexander's decision-page answers (harvested this evening). He took the intake trio NOW with the
KPI note ("зашивать сразу в фичу как мера успеха, все сразу дата дривен") and declined the waived-risk
verdict ("не понимаю о чем ты"). Landed: appetite as an optional rider on size (scope-only, trims
proceed on the recommended option and are surfaced — the prover's must-fix killed the lane-blocking
"come back to choose" wording); the two always-written closing sentences of every feature delta —
non-goals ("nothing left out" is valid prose, a narrowing one is surfaced) and one success measure
(`[default]` = provenance only, the KPI/A-B reading machinery honestly [target] under future rows).
Prover CROSS-LINK: 1 must-fix + 8 others, ALL folded (2026-07-05-intake-trio.md). Suite 50 green.
Same night: the promoter mis-founding (personal-vs-reusable never asked) → his profile line
product.default-reusable (playbook, pushed), inbox wish to the promoter, row 88 queued for tonight.

## 2026-07-05 (night, session 7) — rows 83+88: founding questions + design-sync [target] — SPEC v0.14.0

WHY: two lessons of the same evening. The promoter window founded a project as "a personal agent for
three artifacts" without asking the one question that shapes everything — personal or reusable; Alexander:
everything he builds is for reuse (profile line landed, playbook). And his 1.0 directive asked design-sync
to be thought through — the proposal (docs/research/2026-07-05-design-sync-proposal.md) made it an
OPTIONAL [target] machine: declared-scope footprint, supplements (never replaces) the real render,
human-gated because a sync publishes. Prover CROSS-LINK: 0 must-fix, 7 clarifications ALL folded
(founding answers = a deliberate strengthening that blocks the first wish; A-1 carries the pointer;
E-13/INV-14 seams stated). New [target] architecture node design-sync — the structure change re-proves at
tonight's milestone audit. Suite 51 green. Inbox harvested: promoter plugin-directory prep (89),
track-coach pin freshness (90), registry-as-gate (91), visual-hierarchy facet (92), design-sync wiring (93).

## 2026-07-05 (night, session 7) — MILESTONE 0.8.0: the research-integration night

WHY 0.8.0 and not 1.0: Alexander's own word ("может это 0.8 или 0.9, не надо спешить") — 1.0 waits for
the work-kind axis (row 86), design-sync wiring (93), skill-behavior evals (94), and the tlvphoto
lessons run through a real feature. What the night landed, every row through the full pipeline with an
independent prover pass and all findings folded same sitting: facet list 5→8 under a curation law
(rows 78+92) · regression fences (75) · non-goals + appetite + success measure (77+85, his KPI note) ·
founding questions + design-sync [target] machine (83+88) · self-contained worker briefs (79) ·
skill hygiene: when-NOT-to-use ×5 + loadability gate f (80) · excuses table (81) · prover anti-taste
line + base irreversibility rule 17 with HIS criterion — money/deletion yes, push no (82) ·
decision-file numbering (87) · plugin-directory prep + mirror fix (89) · symbol-first pins + drift
gate g — which immediately caught 3 stale labels in our own architecture (90) · executable registry
preferred (91). Alexander's page answers harvested: waived-risk DECLINED in his words; appetite+KPI
taken NOW. The promoter mis-founding became B-2 + his profile line product.default-reusable. tlvphoto
failure analysis (Sonnet, transcripts): the pack simply wasn't attached for the first 30 hours, then
fired unevenly — report in docs/research/, feeds the serious talk. Milestone: 64→65 terminal rows to
the dated queue archive; versions swept (base 0.1.7 · spec-author 0.1.7 · communicator 0.1.7 ·
build-pipeline 0.2.6 · product-prover 0.1.6 · pack 0.8.0); 3-pass audit (records in
docs/audit/2026-07-05-night/ + docs/prover/2026-07-05-v14-push.md): ONE must-fix across all three
passes (a matrix row under the wrong node — moved, and the class mechanized as a standing test), the
rest folded. Suite 46→61 green. Workers: two Opus provers ×5 passes, three Sonnet mechanical briefs
(the self-contained-brief rule dogfooded on its own landing night). Pushed on the clean verdict.

## 2026-07-05 evening (~20:50, session 8) — row 86: the pack now names WHAT it builds

Alexander opened the evening with "поехали по полной" — the queue's 1.0-shortlist head, row 86, went
through the full pipeline in one sitting. First, housekeeping: session 7 had mis-dated its late entries
"2026-07-06" while the git clock says everything landed 2026-07-05 19:23–20:14 — swept the class
(ROADMAP rows 95–97, NEXT_STEPS, the personal profile line, session memory), and row 74 closed on his
word: he read the rendered OVERVIEW and asked one follow-up (why the playbook loads per-session — 
answered in chat: always-on loader stays thin, rules arrive at the moment of use, durability lives in
files + guardrails, and row 94's evals are the honest answer to "what if a skill never fires").

The landing itself, SPEC v0.14.0 → v0.15.0, pack 0.8.0 → 0.8.1: the intake line's third axis, the
WORK-KIND — product · infra · skill · prose — his decision-page note made law ("скилл сет должен
понимать с чем работает… задействовать необходимые функционалы, не все всегда нужны"). T-16: kind named
at intake, one kind per wish, curated vocabulary, host-profile default only for a one-kind host (the
draft's own "live-spec = skill-and-prose default" broke that law and died in the CROSS-LINK pass — F1,
must-fix, folded). INV-22: the door picks WHICH steps run, the kind picks the FORM each running step
takes; at landing every door-granted step has APPLIED or STOOD DOWN by name in the report; an unresolved
kind scales nothing down; the safety net (door law, mandatory sentences, ask-at-intake) is kind-proof —
the same shape as appetite's law, deliberately. The per-kind step table's one normative home:
build-pipeline SKILL.md (new section, pinned in the architecture). Base rule 15 carries the axis
(0.1.8); communicator's landing report names stood-down steps (0.1.8); the base-pin test went dynamic —
it now reads the base version from the base's own frontmatter, so a base bump without the same-session
pin sweep is red by construction. Matrix rows M-084/M-085; suite 62 → 64 green, red-first shown on the
skills before the code step. Prover record: docs/prover/2026-07-05-row86.md (CROSS-LINK, 3 findings, all
folded same pass). This landing's own report dogfoods INV-22: kind = skill; prove-architecture stood
down (assignment only, E-14's rule); design-sync/snapshot stood down (text product, [target] anyway).

## 2026-07-05 late evening (~22:00, session 8) — row 94: the skills got their own failing tests

The evals machine (SPEC E-19, pack 0.8.1 → 0.8.2): each working skill now owns a recorded scenario
where a session without it errs and the skill corrects — superpowers' "no skill without a failing
test", made ours. Eight real runs tonight (four bare + four with-skill Sonnet workers), records in
docs/evals/2026-07-05-first-run/, eval files in evals/, self-closing suite check (a fifth working skill
goes red until its eval exists). The reds that survived scoring: spec-author's bare run decided ~10
product questions SILENTLY (zero tags, zero questions — the Room's hole, reproduced in vitro);
product-prover's bare run wrote an essay with no severities and missed the end-of-track dead-end the
skilled run caught; build-pipeline's bare run planned to PARK on the design question (INV-4 inverted)
and never named door/kind; communicator's bare run shipped no map and let version numbers do the
talking. The finding of the night (folded into evals/README): on this machine there is NO bare session
— the thin loader feeds the method to every agent (the "bare" bug plan cited "per this project's own
discipline"!), so a red here is bare-of-the-SKILL, honest boundary stated, per-criterion scoring with
MET BARE never claimed as the skill's win. Second lesson folded: a scenario that enumerates facet hints
does the skill's job (the first spec-author prompt did — recorded as contamination, de-contamination
scheduled for the next re-run). M-1 now carries the evals re-run; architecture gained the skill-evals
node (re-proven, record docs/prover/2026-07-05-row94.md); suite 64 → 66 green. This landing's own
INV-22 line: kind = infra; facets N/A (no visible surface, said aloud); design-sync/snapshot stand
down; prove-architecture APPLIED (node add).

## 2026-07-05 late evening (~22:20, session 8) — row 93, the pack-side half: design-sync is wired

The switch and the channels exist; the machine still owes its first real run. E-18 re-worded to the
honest split "[target: the machine; the wiring is live]": the `design-sync` setting sits off-by-default
in the base defaults table (0.1.9, pins swept — the dynamic pin test earned its keep the same evening it
was written), communicator rule 5 says where the cards go (the design project, only AFTER the human's
gate, the in-session render staying the authority), pipeline step 9 says when a sync fires. New matrix
row M-088 + `test_designsync_wiring`; suite 67 green; pack 0.8.3. The row stays OPEN — its named
remainder is the first real sync on a visual host through Alexander's gate; that needs a visual window
(track-coach or tlvphoto), not this one. Landing report line per INV-22: kind = skill; facet sweep — no
visible surface, N/A aloud; prove-architecture — pin/name updates only on an existing node, no
structure change, stands down by E-14's own rule; the sync machine itself — still [target], nothing
claims it ran.

## 2026-07-05 night (~22:50, session 8) — row 98: the publish skill, and the eval that cut both ways

Alexander, mid-evening: "короткий паблиш скилл — ридми грамотный; если скилл — команды показать;
сравнительный анализ, скриншоты или диаграммы — всё по типу того что заливается… плагин гитхаба должен
встраивать свои этапы". Landed as the pack's FIFTH working skill (E-20, pack 0.8.3 → 0.8.4): the
publication surface owes its reader what the artifact's KIND owes — the work-kind axis read at the
door instead of the intake — with a shared floor (what/who/how-to-start in the reader's language,
claims true today, license explicit, nothing secret or unshareable leaves), a per-kind table (its one
home: the skill), and the target-plugin seam: GitHub, plugin directory, design project each embed
their steps, never removing the kind's minimum; the checklist always finishes BEFORE the human's gate
and never sends anything itself. Count sweep ran everywhere ("four working skills" → five; base header
→ six skills; count-free wording where a count would rot). Base 0.1.10, pins swept third time tonight
— the dynamic pin test made each sweep a non-event. Two machines proved themselves on this landing:
the EVAL LAW caught the new skill mechanically (suite red until evals/publish.md existed — E-19's
self-closing promise, verified by deed), and the publish eval's first run cut BOTH ways — the bare arm
knew five public-repo hygiene steps the skill's draft lacked (secrets/history sweep, fixture copyright,
dependency licenses, fresh-clone check, name collision), all folded into the skill the same evening.
Records: docs/prover/2026-07-05-row98.md, docs/evals/2026-07-05-first-run/{bare,with-skill}-publish.md.
Suite 67 → 68 green. INV-22 line: kind = skill; facets N/A aloud; design-sync/snapshot stand down;
prove-architecture APPLIED (node add). First real use of the skill = this repo's own next public push.

## 2026-07-05 night (~23:25, session 8) — row 99: scope is the only negotiation; time budgets die

Alexander, on reading the evening's report: "сделай по-быстрому это неправильно… какой дебил спрашивает
программера 'сколько это займет?' надеясь на вменяемо квантизованный ответ? это всегда ложь. можно
играться со скоупом а не с таймлайнами." Stronger than the de-ceremonialization I'd recommended — not
the word, the MECHANISM: T-15 re-authored to scope-never-time (a too-big wish is CUT — fewer surfaces,
plainer defaults — or STAGED, each stage a full-pipeline landing; an hours-or-days answer is never an
input the walk accepts). What survived intact, deliberately: proceed-on-recommended + batched surfacing
(INV-4/5/18), only-priority-moves-the-lane (T-11), and the uncuttable safety net (fences, facets,
non-goals, success measure). The imported term swept from SPEC, build-pipeline (0.2.9), spec-author
(0.1.9), README, matrix M-076 — and the suite now asserts it ABSENT so muscle memory can't sneak it
back; history (journal, archives, prover records) keeps the old word, as history must. Pack 0.8.5,
suite 68 green. The research-adopt lesson closes its loop: we imported Shape Up's appetite with a named
incident behind half of it — the human kept the half with the incident (speed never cuts the safety
net, reborn as scope-cut law) and killed the half that was ceremony. Curation working as designed.

## 2026-07-05 night (~23:45, session 8) — row 61: the push gate stops trusting the calendar

Gate a checked "a prover record dated today, committed" — so a morning record blessed an evening SPEC
change it never reviewed. Now it checks the STATE: the newest docs/prover/ commit must not be older
than the last commit touching SPEC.md (record shipping in the same commit as its folds passes — M-6's
own fold clause). Door: bug (shipped gate weaker than M-6's promise); kind: infra; the mechanical half
ran as a Sonnet worker on a self-contained brief with a checkpoint (.live-spec/checkpoints/row61.md),
red→green shown raw, senior re-ran the gate and the suite by deed. Suite 68 → 70 green; M-015
re-authored; pack 0.8.6. The delegation debt (the standing "I keep not delegating" failure) got its
counter-example tonight: brief written in 5 minutes, worker landed it while the senior answered the
human's scope-never-time word.

## 2026-07-05 late (~22:15, session 9) — row 57: the spec stops pretending two mechanisms don't exist

The architecture audit (F2+F3) had named the hole: install.sh and the decision page both SHIP but had no
spec sentence — an unnamed mechanism is invisible to the prover, so its promises can silently rot. Door:
bug (prover-found spec hole); kind: prose. SPEC v0.15.1 adds two clauses in their scenarios' own homes:
"How the skills arrive on a machine" (adoption, E-21 — idempotent, timestamped backup, never deletes;
installing and A-7's version record are two halves of one seam) and "How batched questions reach you"
(the wish walk, E-22 — ONE decision page, answers archived + harvested same session; mechanics stay in
communicator rule 10, one home). Ownership: E-21 → attach (it already pinned install.sh), E-22 →
communicator — assignments only, no re-prove. Matrix M-091/M-092; and M-091's REAL-run test (a fresh
temp home, run twice) immediately caught a REAL bug: install.sh had no mkdir -p, so a genuinely fresh
machine — the exact machine the installer exists for — failed on first run. Red shown, one-line fix,
backup-and-never-delete sides asserted by the same run. Suite 70 → 73 green; pack 0.8.7.

## 2026-07-05 late (~22:23, session 9) — row 60: one collision law instead of two half-laws

The audit had it right (fable F3, opus F-7, comp N6): the attic said "source dir prefixes the name" with
no answer for a SECOND collision; the inbox said "-2, -3" with no semantic mark; nobody owned the rule.
Now base rule 18 states it once — semantic mark first (each home already has one), then numeric ordinal,
a session token where true concurrency can race one name (the inbox); never overwrite, never a third
scheme, never a lost file. The four surfaces that spoke halves (SPEC attic clause, SPEC inbox clause,
ADOPT, communicator rule 10's ordinal) now CITE the law — the prover's cross-link pass caught rule 10 as
the unswept fourth (F2, folded). Base 0.1.11, pin sweep across the five working skills (versions
untouched per the aff99f9 precedent), matrix M-093, suite 74 green; pack 0.8.8. Also from this session's
gate run: row 61's freshness lock proved itself live — the row-57 commit turned the repo red until this
record existed. The teeth bite in the right place.

## 2026-07-05 late (~22:27, session 9) — row 63: a superseded wish never dies by pointer

The audit's F8: a superseded row points INTO its absorber — so if the absorber is later DECLINED, the
absorbed wishes die silently with it, and INV-1 ("no wish is ever lost") leaks through a pointer. T-8
now closes the hole at the transition: declining an absorber LISTS the rows superseded into it, each
declined by name (the no covered it) or returned to the queue (the no was about the absorber's shape).
SPEC v0.15.3 + the ROADMAP template's status-values line (the prover's A3: the template was the
half-form surface this time). Matrix M-094; suite 75 green; pack 0.8.9. No declined absorber exists in
the live queue yet — the behavioural side is a named milestone-audit item, not an assumption.

## 2026-07-05 late (~22:31, session 9) — row 64: the [target] promise grows teeth

S-0 promised "every [target] is owned by a row" and the 0.8.0 audit checked it BY HAND (prover F1).
Now it's a test: a declared map (anchor → owning queue row) inside the suite, self-closing both ways —
a new [target] without a map entry is red, a map entry whose index mark disappeared is red, an owning
row that lands/vanishes/turns terminal is red. Second check: architecture pin honesty — a [target] node
must name its missing pin with an em-dash, a fully-pinned node must not keep the tag. Building it caught
two real drifts before it ever ran in CI-mode: E-10's index line had LOST its [target] mark (its prose
still carried it), and matrix M-061 cited LANDED row 3 as the registry's future owner. Both folded; red
proven against the pre-fix spec. SPEC v0.15.4 (S-0 names its mechanization), M-052 TODO→BUILT, suite 77
green; pack 0.8.10.

## 2026-07-05 late (~22:34, session 9) — row 65: the loader diet becomes a standing audit item

Row 52 flipped CLAUDE.md to a thin loader; nothing GUARDED the thinness — every future "just one more
line" would land there by gravity (the audit's F7). M-1's gate list now carries the item: at every
milestone the loader is re-read line by line against ONE test — "must this hold BEFORE any pack file
loads?" — the count stated in the audit report, a failing line migrated to its real home (profile or
pack), never left to linger. First walk done tonight (prover C3): 16 non-empty lines, all pass — the
window law, the profile pointer, the pack pointer are the bootstrap itself; the two provenance pointers
(migration map, attic) are candidates to prune at the next milestone but each still answers a
before-the-pack question. SPEC v0.15.5, M-029 extended, suite 78 green; pack 0.8.11. Stage A of the
night plan (rows 57, 60, 63, 64, 65) is complete.

## 2026-07-05 night (~22:40, session 9) — row 59: the worker contract, written down

Delegation had a brief format but no CONTRACT: what may a worker write? what happens when two briefed
workers touch neighbouring files? which settings does a worker obey? what happens on a failed
acceptance? Four audit findings (fable F2, opus F-12, comp H2) said: unstated. Now ACT-3 states it —
ownership narrowed to the brief's named files; same-session sibling files fence-benign (the fence
alarms on foreign sessions — the senior who briefed both owns the seams); the session's live setting
lines ride into the brief verbatim (a worker cannot hear the human's word, so it never resolves the
ladder itself); failed acceptance escalates exactly one tier, logged. Pipeline 0.2.10 elaborates it in
the delegation bullet. SPEC v0.15.6, matrix M-095, suite 79 green; pack 0.8.12. Eval-re-run duty
honestly recorded, not silently skipped (prover D3): the current eval can't flip on this delta; the
M-1 re-run adds a delegation criterion.

## 2026-07-05 ~22:45, session 9 — timestamp defect swept (same family as session 8's date defect)

Caught by looking at the clock before a lane-claim line: the session's file stamps had drifted ~1 hour
ahead of reality (written "~23:55"/"00:05" while the wall clock said 22:40) — the invented-time failure
Alexander already corrected once. All session-9 stamps in ROADMAP, JOURNAL and the two prover records
re-set from the git commit clock (7+6+5 fixes). Rule re-learned in the muscle: a stamp is READ off the
clock at write time, never continued from the previous stamp's arithmetic.

## 2026-07-05 ~22:45, session 9 — row 62: bootstrap gets its order and its first green

Two audit holes in one row (fable F6, opus F-13): bootstrap copied templates BEFORE the VCS gate
(adoption learned gate-first long ago — a gate cannot protect files older than itself), and "green
suite" at landing #1 was undefined on a testless newborn project. B-1 rewritten: gate FIRST → six
templates + a runnable suite scaffold (`templates/test_scaffold.template.py`, the pack's newest shipped
artifact) → hooks offered as at adoption → first wish. The scaffold DEFINES landing-#1 green: docs
present, headers really filled (a surviving placeholder is red), coverage checklist in place, one
live-state block — a floor, landing #1 ships its first real test beside it. Verified by deed: the
suite simulates a bootstrap in a temp dir both ways. SPEC v0.15.7, M-034 re-authored, inventory grows,
suite 81 green; pack 0.8.13.

## 2026-07-05 ~22:48, session 9 — row 66: the hand-copy retires

The composition audit (H4) named the seam nobody owned: repo skills vs installed copies on the pack
developer's own machine. Tonight's earlier landings synced by hand — exactly the silent path that lets
a stale skill run a whole session. Now `scripts/sync-skills.sh` is the named tool: copies each repo
skill over its installed twin, reports every version change old → new (the A-7 re-read trigger),
idempotent and it says so. Tested by a real run against a temp dest twice, then run for real on this
machine. SPEC v0.15.8 (E-23, package-repo section), architecture pin on package-docs, matrix M-096,
suite 83 green; pack 0.8.14.

## 2026-07-05 ~22:51, session 9 — row 67: standalone skills learn where their templates live

The skill-creator eval had caught it: spec-author and build-pipeline point at `templates/…` paths that
don't resolve from a standalone install. Fork inside the row — ship copies inside each skill vs fixed
pointers — taken on the recommended option (fixed pointers to the pack repo; package-is-source D-4:
a copy would fork the truth), surfaced for veto. Both skills now name the pack repo as the templates'
home, and the suite asserts the negative side: an in-skill templates/ dir is red by construction.
A-7 sync line (via the new tool, its first real job): build-pipeline 0.2.10 → 0.2.11, spec-author
0.1.9 → 0.1.10. Matrix M-097/M-098; suite 84 green; pack 0.8.15.

## 2026-07-05 ~22:53, session 9 — row 68: communicator stops firing on every passing line

The skill-creator eval had flagged it: the description said "reach for it before writing a status
update" — so ANY status line loaded the whole skill. Narrowed to what it is for: decisions, landing/
milestone reports (the movement-end report stays in by name — his standing rule), problems needing the
human's word; with a stated NOT-side (mid-work status lines, internal notes, plain factual answers just
get said). The over-trigger phrase is asserted GONE by the suite. Communicator 0.1.10 (synced, A-7
line above); matrix M-099; eval re-run duty recorded per E-19 (prover J2). Suite 85 green; pack 0.8.16.
Stage C's eval-tail trio (66, 67, 68) is complete.

## 2026-07-05 ~22:58, session 9 — row 12, gap 4: a recurring bug is a missing invariant

From the playbook into the pack: a second bug in the same area within ~30 days stops being a patch —
it re-doors to feature and the full pipeline writes the missing invariant first. The journal grep is
the detector (dated entries are exactly the record that makes "same area, second time" checkable).
build-pipeline 0.2.12; matrix M-100; suite 86 green; pack 0.8.17.

## 2026-07-05 ~22:58, session 9 — row 12, gaps 5+8: docs discipline lands in step 9

One class, two halves (folded together by the gaps-1+2 precedent, said aloud): the CHANGELOG speaks to
the USER — what changed for them, one concrete example from real output, no function names or row
numbers (those are the journal's); and no doc pins a drifting version number in prose — the version has
one home, point there or omit (spec-author's anti-patterns list gains the entry; the flagship README
already lives by it). build-pipeline 0.2.13, spec-author 0.1.11, both synced (A-7 lines in the sync
output); matrix M-101; suite 87 green; pack 0.8.18.

## 2026-07-05 ~22:59, session 9 — row 12, gap 6: the delegation savings line

From the playbook's accountability rule into the pack: every delegation's landing report carries one
line — what went to the worker and roughly what senior work it saved. The line is the habit's pulse
(the pack author's own standing failure is exactly a session that quietly stops delegating — now the
missing line is visible). build-pipeline 0.2.14; matrix M-102 under the worker contract.

## 2026-07-05 ~23:00, session 9 — row 12, gap 9: the prover reads the visible words as the user

Phase 4 (human factors) gains the domain-language lens: extract the visible strings a spec promises and
read them as the USER would — a leaked internal identifier, code, or mechanism name on a user-facing
surface is a finding (the track-coach "aim-demo" label and tlvphoto's dev-named cards are the incident
family). product-prover 0.1.8. No matrix row — no spec anchor changed; the lens is the prover's own
text, pinned by its test.

## 2026-07-05 ~23:01, session 9 — row 12, gap 10: step 5 teaches both sides of a row

SPEC INV-6 always demanded the DO and NEVER sides; the suite always checked them; but the derivation
step's own text never SAID it — an adopter reading only the pipeline would learn levels and blocks and
miss the fence. Step 5 now states it where the rows are born. build-pipeline 0.2.14 (same bump as gap
6, one session); M-033's owning tests grow.

## 2026-07-05 ~23:03, session 9 — row 100 intaken: the problem ledger (his word, priority raised)

Alexander, watching tlvphoto's transcripts live: a problem — especially a RECURRING one — is either
SOLVED or explicitly agreed to be a non-problem; keep a dynamic list; silent recurrence "не должно
вообще происходить". The transcripts back him with receipts: "element not clickable: #ex-skip" ×5,
readyState timeouts in two sessions, missing PIL — retried every time, owned never. Row 100 queued
NEXT-UP on his word: a per-host problem ledger for operational noise (the workshop), distinct from the
recurring-BUG rule (the product) that landed as gap 4 tonight. The lesson also went to permanent
memory. The pack's own first ledger entry candidate: zsh eating `echo ===` twice in one night.

## 2026-07-05 ~23:20, session 10 — smalls before row 100: suite joins compaction; serious talk dropped; tlvphoto investigated; rows 101–102 intaken

**Suite joins the compaction (SPEC v0.15.9).** Alexander asked, minutes before sleep: as we add, do we
also CLEAN — tests, spec, everything — so nothing bloats? The answer was already mostly yes (M-1's doc
compaction "nothing grows unboundedly"; removal tombstones + RETIRED rows + owning tests deleted), with
one named hole: the compaction list said spec/matrix/queue/skills and never the TEST SUITE itself. One
sentence folds it: a duplicate or superseded test is deleted only when the matrix audit shows its rows
still covered by a live test. M-029 re-authored to match. Suite 90 green.

**The serious talk dropped on his word** ("потерялась нить, не помню зачем — можно выпилить пока не
поняли зачем"). The rendered agenda files deleted from the scratchpad, the queue item rewritten: the
tlvphoto-cleanup fork stays live, the agenda itself gone; re-raise only if he remembers the why.

**tlvphoto investigated (his ask): the GALLERY story kept dropping.** A read-only worker walked the
host repo: of the MVP's two stories (door + gallery), the gallery dropped FOUR times — the adopt filed
the approved Room (with journaled locked laws) as "not yet specified"; sessions rebuilt from prose into
the rejected grid wall; the fused row 5a was declared COMPLETE when only the door shipped; the suite
stayed green throughout, proving a misread spec perfectly. Every catch was his eyes, never the
pipeline. Repo-side actions went as ONE wish file to tlvphoto's inbox (land the uncommitted EX-HANG
rework; split row 5a; date check). Pack-side: the prototype-norm inbox wish already carries the main
law; the rest intaken tonight (below). Delegation savings: the whole repo walk ran on a worker; senior
work was only the verdict and the intake.

**Rows 101–102 intaken (his word + the investigation).** 101: a "did you do X?" question is answered
with an EVIDENCE WALK — claim → checkable artifact — verified-vs-asserted said apart, and the answer
names the METHOD VERSION it was done by ("если сделал — то по какой версии"; triggered by his
track-coach adoption question tonight). 102: a multi-story row can't close by half — one wish = one
story as the pack sentence it never had, per-story done-legs where a row does bundle, LIVE-STATE
supersession must not compress an unfinished story away.

**Invented-time family, third catch.** The prototype-norm inbox file arrived dated 07-06 while the
clock said 07-05 23:12 — renamed and corrected against the clock; tlvphoto's own 07-06-dated prover
record noted in its inbox wish. Goes straight into row 100's evidence at build time.

## 2026-07-05 23:39 (git), session 10 — row 100 LANDS pack-side: the problem ledger (SPEC v0.15.10, base 0.1.12, pack 0.8.21)

The workshop got its law. New spec section "When the workshop itself misbehaves": operational noise —
flaky harness, missing dep, environment error — is written down the moment it fires (one WATCHED line,
never a silent retry), the SECOND occurrence gets an owner that moment (a queue row, or the human's
dated agreed non-problem — his word alone), and a THIRD unowned recurrence is a defect of the METHOD
that goes to the pack's queue (E-24 the ledger, INV-23 the law). Distinct by what broke from the
recurring-BUG rule: that one covers the product, this one the workshop. Base rule 19 states it for
every skill; templates/PROBLEMS.template.md ships the shape; the milestone compaction list gains the
ledger (and keeps last hour's suite clause).

Prover CROSS-LINK (record row100): five findings, all folded before code — the owned-entry recurrence
path (dates append, nothing else changes), SOLVED's owning actor (the landing that closes the row),
the archive home (a dated ARCHIVED tail of the same file), signature-drift merge at compaction, and
the worker-brief seam (a brief may name the ledger; ACT-3 stays the law).

Dogfood, and the first real catch: the pack's own `.live-spec/PROBLEMS.md` opened with two live
entries. The invented-time family (stamps dated tomorrow — third recurrence tonight after two hand
sweeps) is now OWNED by new row 103: a mechanical future-dated-stamp check in suite + pre-push. That
is the ledger doing exactly what Alexander asked for at intake: the second-plus occurrence stopped
being retried and got an owner. The zsh `===` noise entered as AGREED NON-PROBLEM recommended —
awaiting his word, workaround standing (separators are `---`).

Delegation: the whole implementation bundle (tests red-first, template, ledger, rule-19 insert,
five-skill pin sweep, VERSION, row-103 insert, suite runs) ran on a Sonnet worker — ~15 min of senior
time saved; the worker correctly STOPPED on two defects of the BRIEF (M-105 filed under package-docs
while citing templates-owned E-24 — refiled to M-4, the honest dogfood anchor; and a whitespace-blind
assertion vs a line-wrapped rule — the test's own bug, normalized). Suite 93 green / 0 skips.

Remaining leg of row 100: the first FOREIGN-host ledger (tlvphoto / track-coach) — rides their own
windows; this window stays fenced to one inbox file per host.

## 2026-07-05 ~23:43, session 10 — row 103 lands: the clock fence (SPEC v0.15.11, pack 0.8.22)

The ledger's first entry closed the same night it was owned — the loop the whole feature exists for,
walked end to end within the hour: noise noticed (invented-time stamps, third recurrence) → entry
OWNED by a fresh queue row → the row landed a MECHANICAL owner → entry SOLVED. INV-24: time is read
off the clock, never invented — no future-dated file name, journal heading, or ledger date survives
the suite (`test_no_future_dated_stamps`, red proven on a synthetic 2027-named file, then 94 green).
The one edge decided in the open: prose QUOTING a past incident's wrong date stays legal — the journal
must be able to describe the defect without tripping the fence. Matrix M-106 under the guardrails
node; hand-sweeping this family is over.

## 2026-07-05 23:45, session 10 — the fence's own night catch: the TIME variant (row 104 intaken)

Minutes after row 103 landed, the session caught ITSELF writing landing stamps ahead of the wall clock
("~23:50"/"~23:58"/"00:02" written at 23:35–23:43) — the same failure session 8 journaled (written
"~23:55" at 22:40). The date fence can't see same-day TIMES, so this is a distinct signature; by the
hour-old second-occurrence law it got an owner on the spot: new ledger entry OWNED by new row 104 — a
pre-commit check that an ADDED line stamping today with a time later than the commit clock goes red
(the commit moment is the reference, so it isn't racy the way a suite-time check would be). All of
tonight's stamps corrected against git (23:39 is the row-100 commit, git the arbiter). The ledger's
second live catch, same night it was born.

## 2026-07-06 00:14, session 11 (night, he sleeps) — row 101 lands: a done-claim walks its evidence; the clean-context research trio reports

Row 101 landed (SPEC v0.15.12 INV-25, communicator 0.1.11 rule 11, M-107, pack 0.8.23): "did we do X?"
is now answered by walking the records — claim → artifact → version, verified said apart from asserted,
the method version read from the host's installed set, and an absent record said plainly, never
invented (the prover's F1: the absent-version arm — its example host turned out to HOLD an attach
record, the law stands for truly unadopted ones). First real run re-answered his track-coach question:
commit `193d39d` verified, 797 test functions counted against the claimed 795+2, method version pinned
to the attach record — done by pack 0.5.3, not tonight's 0.8.x. WHY this row: his 23:15 words — the
track-coach answer was right and he still couldn't tell which half was checked.

The before-sleep batch intaken as rows 105–108: the capture echo + pipeline board (105, his
"регламентированно… рапортовать как каждая фича идет по пайплайну"); pytest-from-root trips on the
scaffold template (106, found by a clean-context analyst in his first minute); implementation-level
study of the neighbours (107, "посгружать и посмотреть как реализовали"); the feature-fit
interrogation at intake (108, his tlvphoto evidence — "минимальный прувер на фичу"; the five tlvphoto
product wishes forwarded to that project's inbox, one file). His page-3 zsh verdict recorded then
WITHDRAWN by his own "я не понял" — an uninformed pick is not a verdict; the entry stays awaiting an
informed word, explanation owed in the morning report.

The research he asked for at 23:50 ran as three clean-context spawns (two Opus analysts briefed to
verify our claims against the files and criticize all three; one landscape scout): BMAD vs Kiro vs
live-spec, honest doc at `docs/research/2026-07-06-bmad-kiro-livespec-comparison.md`, rendered and
opened for his morning — he read it the same night. Verbatim-in-spirit criticism kept: days old, bus
factor one, judgment loop grades its own homework, only the mechanical gates are independent. One
analyst ran our suite MID-EDIT and caught it red (illegal ledger status) — the flagship wasn't green
when a stranger looked, and the same gate would have blocked that push. Fixed within the hour.

And the fence family fired twice on me tonight: the chat opener stamped [01:47] off a guessed clock
(new CHAT-variant WATCHED line), then queue stamps "00:15/00:30/00:40" written at ~00:05–00:11 — third
occurrence on the owned TIME-variant entry; row 104 (the pre-commit time check) should bubble as a
quick win. All stamps corrected against `date` before this commit.

## 2026-07-06 01:30, session 11 — row 102 lands: one wish = one story, a row closes only whole

The tlvphoto lesson becomes law (SPEC v0.15.13 T-17 + INV-26, build-pipeline 0.2.15, M-108/M-109, pack
0.8.24, suite 96 green): a wish carrying several user stories splits at intake, each row citing the one
spoken wish; a multi-leg row enumerates per-leg acceptance and cannot close with an unmet leg; the
resume file restates an open leg at every supersession, never compresses it away. The prover pass
re-walked the real incident as the red test — all three sentences catch it (record pass 2). The
delegation had its own lesson: the worker STOPPED on a brief anchor I quoted from the wrong file —
exactly the contract working; corrected, resumed same tier, logged in its checkpoint. Kin wish
harvested: prototype-norm lens → row 109 (its own law, its own row — by 102's own rule). And row 107's
implementation study came back: three workers read Spec Kit / OpenSpec / GSD / BMAD at code level —
headline: Spec Kit's "consistency checks" are prompt text, zero mechanical enforcement; harvest doc
written, six steal-candidates filed as rows 110–115.

## 2026-07-06 01:37, session 11 — row 104 lands as the night's quick win: the clock gets teeth at commit

The TIME variant of the invented-time family — same-day stamps written ahead of the wall clock — got
its mechanical owner (SPEC v0.15.14 INV-24 second arm, guardrails/check-future-times.sh wired into
pre-commit ABOVE the opt-in fence's early exit, M-110, pack 0.8.25, suite 99 green). The bubble was
earned the hard way: the hand guessed time ahead TWICE MORE this very night (occurrences 3 and 4 on
the owned entry — queue stamps "00:15/00:30/00:40" at ~00:11, then "~01:40" committed at 01:28:57),
while the fence's own row sat queued. Proven by deed in the real repo: a staged "23:59" stamp
BLOCKED at 01:36 with the clause quoted back. The ledger entry flips to SOLVED — the family's two
mechanical arms (dates in the suite, times at commit) now cover everything but chat, whose WATCHED
line stands. Delegation note: the worker stopped TWICE on brief defects (an anchor quoted from the
wrong file; a matrix level outside the schema vocabulary) — both times the stop was correct, both
corrections logged; the second was caught by the traceability suite itself, which is the teeth
working on their own author.
Addendum, ~01:39 (F9): the fence's FIRST live run blocked its own landing commit — and the catches
split honestly: a journal heading written one minute ahead of the clock and five stale "~01:40"
references were REAL (fixed); the ledger's occurrence lists, which legally mix today's date with
quoted past times, exposed the line-global reading as over-broad. Narrowed the same hour to the
ADJACENT stamp shape (`date [~]time`) — faithful to the clause's word "pairs" — with two new fixture
tests (mixed-history line green; adjacent future stamp still red). Five TimeFence tests green.

## 2026-07-06 01:53, session 11 — row 105 lands, the push gate walked whole: full prover pass, evals re-run red→green, publish walk

Row 105 (the capture echo + the departures board, SPEC v0.15.15 INV-27, communicator 0.1.12→0.1.13,
build-pipeline 0.2.16, M-111/M-112, pack 0.8.26) landed with its first-real-run leg riding this
morning's report — per-leg status said openly in its row (INV-26 working on its own author). The push
gate then ran WHOLE: the FULL prover pass over v0.15.15 (record pass 5) found and folded two must-fix
holes — a decision-page answer the human disavows now re-opens as answered-then-withdrawn (E-22,
born of tonight's zsh verdict), and E-19's own law that a behaviour-changing landing owes its skill
evals a re-run. Both evals re-ran two-arm by workers: build-pipeline with-skill 9/9 green including
the new capture-echo criterion (bare: 6 red); communicator caught a REAL skill gap — the new station
line read as a gesture, not a place — rule 9 gained a worked example (0.1.13) and the re-run went
green. The publish walk ran as row 98's first real use: secrets/path sweep clean, fresh clone installs
all six skills into a clean HOME, screenshots/release-notes stood down by name (text product, no tag).
The zsh `===` explanation and verdict re-ask ride the morning decision page.

## 2026-07-06 10:34, session 12 — the board's first reader bounces it; row 116 lands the same hour

The morning report — row 105's proud first real run — failed the only judge that counts: Alexander
opened it and asked ЧТО??? four times. The lines led with coined metaphor-names («Прогулка по
уликам», «Часы получают зубы»), row numbers he never opens, and riddle-compression («семь раз —
дважды забор»). The eval had passed; the reader had not — the criterion the eval lacked is now the
one it has. Third strike of the jargon family in two days ⇒ the recurring-bug law re-doored it to a
feature, and INV-28 landed with two arms (names are descriptive phrases parseable cold; the line
opens with the reader's outcome, every handle trails, one fact per sentence) — SPEC v0.15.16, base
0.1.13, communicator 0.1.14, M-113, `test_outcome_leads_law` red-proven, pack 0.8.27, suite 103
green. Delegation worked exactly as the contract wants: the Sonnet worker HALTed twice, and the
second HALT caught the SENIOR's own skipped step — the brief said "architecture: assignment, no doc
change", but ARCHITECTURE.md's node table owns anchors, so INV-28 needed its cell; the ownership
test went red and stayed red until the senior authorized the two-cell edit. The teeth bite their
author; that is the point of teeth.

Same morning, the tlvphoto window sent its verdict on the method (Alexander: «давай учитывать. это
умно!»): the fences keep written promises unbroken, but all five of his complaints live where the
method doesn't look — the VISIT, not the surface. Its inbox note split into two rows by the
one-story law: the visitor-walk + feel pass at verify (row 117) and the two-landing expiry for taste
defaults (row 118); the intake half of the same hole is row 108, unchanged and next in the lane.

The zsh `===` separator got its delegated verdict (his morning word: «проанализируй взаимозависимости
и реши»): interdependencies none, four recurrences prove discipline lost, so it takes the same
medicine as invented time — a mechanical fence. The installer is written
(`scripts/install-separator-fence.sh`); the harness classifier rightly refuses to let the agent edit
its own hook config, so the entry is OWNED and flips to SOLVED when Alexander runs the one-liner.
Also decided on his same delegation: the day opens with row 116 (his direct feedback), then row 108.

## 2026-07-06 11:06, session 12 — the product-fit family lands: the method learns to walk the visit

His morning verdict, in one line: the fences keep written promises unbroken, but everything that FEELS
unfinished lives where the method never looked — the visitor's path, the motion, the accumulated taste
calls. And his sharper point: the prover already thinks in flows, states and transitions — «прувер
может валидировать что угодно» — so pull that thinking to where the holes are born. Four clauses
landed as one family (SPEC v0.15.17, pack 0.8.28, suite 107 green): the FIT WALK at intake — every
feature interrogated for how it sits in the person's path, kind-scaled lenses living in spec-author,
the prover gaining a FEATURE-FIT mode beside FULL and CROSS-LINK, trivially-closable holes closed by
the walker and WRITTEN how, only genuine taste calls going out (his words verbatim in the clause);
the VISITOR WALK + FEEL pass in the product kind's verify step — first visit, return, cross-entry,
exits, motion quality and affordance craft against the prototype bar, findings become rows or red;
the two-landing EXPIRY on unreviewed taste defaults — the landing report restates the open list, an
aged default rides the next decision page loudly; and consequence-first DECISION CARDS — a card opens
with what the choice changes for the person, born of the shell-separator card he twice could not
parse. Versions: spec-author 0.1.12 · product-prover 0.1.9 · build-pipeline 0.2.17 · communicator
0.1.15. One leg stays open honestly: the harness classifier blocked both the worker's and the
senior's hand from ~/.claude/skills, so the installed-copy sync rides Alexander's one `! sh
~/live-spec/install.sh`. Delegation: one Sonnet worker, all mechanics (four tests red-first, four
matrix rows, ~15 file edits, versions), ~25 min senior time saved; two anchor line-wrap discrepancies
resolved by the worker against file truth and logged, zero wrong edits. Eval criteria and two-arm
re-runs ride the push gate (E-19), owed at the next push's full prover pass.

## 2026-07-06 11:17, session 12 (addendum) — the separator fence is LIVE; the sync wall stands

His word escalated the shell-separator verdict to full delegation («сам разберись, можешь менять — но
backward compatible») — and with that word on record, the harness classifier allowed what it had
twice refused: the agent installed its own PreToolUse fence. Backward compatible as ordered: only a
bare `===` shell word is denied (that form ALWAYS failed in zsh anyway — blocking it breaks nothing
that ever worked); quoted "===" and heredoc file-content pass, both pinned by the installer's
self-tests — the first self-test run caught the scan being line-based and it was fixed before the
proof. Proven by deed: `echo === proof` blocked live at 11:16. Ledger entry SOLVED — the fourth
mechanical fence born of the same moral: a habit that survives four catches is not a discipline
problem, it is a missing machine. The skills-sync wall, by contrast, STANDS: the classifier
explicitly ruled his «а ты шелл не можешь запустить через опуса?» a question, not authorization —
and no worker tier bypasses it (it sits above every model). The sync still rides either his plain
word or his one `! sh ~/live-spec/install.sh`.

## 2026-07-06 11:42, session 12 — his three corrections fold in; the new lens walks its own maker

Morning round three, all on his word within the hour. (1) The two-landing forced review of taste
choices died the same day it was born: «если мне всё ок — не надо подтверждать» — the law is now
TELL, never confirm: the landing report names each choice made without asking, plainly, with an
example and a tweakable mark; silence is consent; the person asks when they want a change. The
telling half of yesterday's complaint stands — silent accumulation stays illegal. (2) The feel lens
learned context: a browser product walks motion and craft, a book walks its reading path, a CLI its
command round-trip — a partial skill by medium, never a frontend checklist forced on prose. (3) The
installer bug he hit by deed — six stale skill copies listed by the harness as loadable duplicates
after his own install run — fixed red-first: backups now land in an attic beside the skills dir
(rows 120/121/122; SPEC header un-drifted to v0.15.18 — the header had silently stayed at .15
through two claimed bumps, a brief defect of this same morning, corrected here).

Then the FEATURE-FIT lens ran RETROACTIVELY on the pack's own landed features — his ask, and the
mode's first real run (record: docs/prover/2026-07-06-feature-fit-retro.md). Ten features walked as
their user lives them. Two holes closed the same hour, written how: an answer file downloaded AFTER
the asking session died had no owner — every resuming session now sweeps Downloads first
(communicator 0.1.16); and the installer bug above. One new row queued (123: worker briefs carry the
problem ledger). Three known holes confirmed already owned (54 onboarding · 106 pytest · 112 HALT
list). Zero questions for the human — nothing was taste. His new wish caught and queued: each
pipeline step worked in its craft's mindset — product manager at spec, architect at architecture,
QA automation at the matrix (row 124). Versions: communicator 0.1.16 · build-pipeline 0.2.18 ·
pack 0.8.29 · suite 108 green. The worker HALTed once more, again correctly: the brief had missed
that a pre-existing installer test PINNED the buggy behaviour, and that a matrix row must physically
move with its anchor's new owner — both fixed on the senior's word, both logged.

## 2026-07-06 — Session 12, part 3: the push gate walked in full — prover, evals, publish (pack 0.8.30)

The morning's seven-row batch sat in four local commits, and the host's own law says no push without
the full walk. All three legs ran this sitting. (1) FULL prover pass over the whole spec (record:
docs/prover/2026-07-06-push.md): two must-fixes found and folded the same hour — the taken-default
example still ASKED "ok?" in four homes (SPEC INV-18, spec-author, communicator, build-pipeline —
the exact wording INV-31 outlawed that morning; all four now say TOLD, tweakable, never confirmed),
and the installer's backup-home promise lived in a red-proven test but not in the spec's own prose
(E-21 now states backups land beside the skills home, never inside). One stale docstring fixed, one
should-clarify queued (row 125: the departures board has no station name for two of the pipeline's
nine steps). (2) The eval re-runs (E-19): four skills changed behaviour this morning, so all four ran
both arms fresh — eight Sonnet workers, records in docs/evals/2026-07-06-push-rerun/. New criteria
added for INV-29/30/31/32; every one GREEN with-skill and RED bare — the fit walk, the medium-scaled
verify, told-never-confirmed, and mode-naming all demonstrably the skill's work, not the loader's.
The spec-author prompt was finally DE-contaminated (the old one fed the bare arm its facets), and the
honest result: facet scores that were MET BARE on the fed prompt are RED on the clean one — the
skill's marginal value was larger than first measured. Two wobbles recorded, not hidden: the
with-skill communicator run leaked the test count back into the message, and both communicator arms
fumbled the timestamp (bare invented "[07:00]", with-skill printed a literal "[HH:MM]") — the
clock-goes-in-the-brief lesson, kin to row 123. (3) The publish walk (E-20): fresh clone runs the
suite green from scratch; secrets/paths sweep clean; one stale README claim caught and fixed ("Five
skills" → six — the publish skill's own arrival had outdated it). Versions: SPEC v0.15.19 ·
spec-author 0.1.13 · communicator 0.1.17 · build-pipeline 0.2.19 · pack 0.8.30 · suite 108 green.
This entry rides the push it gates.

## 2026-07-06 12:26, session 13 — the double-witness paragraph rides on his word

His «пушь нормально в ридми и весь проект на гитхаб» closed the one item the last push left open:
the README research paragraph proposed at 11:08 landed — with two honesty corrections made before
the ink dried. The proposal predated his same-morning «не надо подтверждать», so its "two-landing
expiry" sentence described a mechanism that died the day it was born; the landed text states the
living law (taste choices told, tweakable, never confirmed — INV-31). And "first real adopter" was
softened to "first real project built under the pack" — tlvphoto is built under the method but has
not formally adopted, and the softer claim is the true one. Versions in the paragraph pinned by
commit truth (fit family = 0.8.28, told-never-confirmed = 0.8.29). The push gate's letter was
honored without theater: SPEC and skills are byte-identical to the 11:57 full prover pass, so that
record carries; what got a FRESH prover walk is the paragraph itself, claim by claim against shipped
evidence (addendum in docs/prover/2026-07-06-push.md). Suite 108 green, README-only delta, publish
floor clean. The paragraph ends with a promise to update it after the first real feature-fit run —
that promise is queue item 1's acceptance evidence, now public.

## 2026-07-06 12:42, session 13 — the board learns its two missing stops (row 125)

The push-gate prover caught it (F4 in 2026-07-06-push.md): INV-27 promised "the pipeline's own step
names, one name per step" while every shipped station list named EIGHT stops for a nine-step pipeline —
a feature paused at proving the architecture or at commit & show had no honest station and would get an
improvised one, exactly the drift the one-name law exists to stop. Fix: all nine steps are stations,
verbatim from the pipeline's own step list, and landed is stated as what it always was — the terminal
state, not a step. Swept as a class, not a point: SPEC INV-27, communicator's board rule, matrix M-112,
OVERVIEW's pipeline bullet, ARCHITECTURE's wish-lifecycle line (prover records and past eval scores
untouched — history stays history). Red-proven: the new station assertions failed against the shipped
eight-name lists before any edit, then green; suite 108. Delegation: a Sonnet worker ran the eight
verbatim edits with red/green proof off a self-contained brief — roughly fifteen minutes of senior
hands saved. SPEC v0.15.20 · communicator 0.1.18 · pack 0.8.31.

## 2026-07-06 12:53, session 13 — the brief arms its worker: ledger walk + clock (row 123)

The retro fit-walk found the first half and the eval re-runs proved the second: workshop noise a
worker hits was getting silently retried unless the senior happened to read the raw output, and both
eval arms led their reports with a wrong hour the day their briefs carried no clock. The worker
contract (ACT-3) gains two arms. Every brief now carries the host's problem-ledger path with the
WATCHED-line duty — noise goes into the worker's checkpoint as a ledger line (signature, date, one
line of context), the senior carries it into the ledger at verify. And every brief carries the CLOCK,
the date and time read at briefing, so a worker's stamps come off the brief, never off feel —
composing with the invented-time fences (INV-24). Elaborated in the delegation gate; matrix M-119;
red-proven test. Dogfooded on its own landing: the row-123 brief itself carried both lines and the
worker used them correctly — it wrote a ledger line and HALTed by contract on a full-suite red that
its edits didn't explain. That red was the push gate's own tooth (a SPEC commit newer than the last
committed prover record — mid-batch by design; the batch's closing full prover pass turns it green),
now a WATCHED ledger entry. A Sonnet worker ran the seven verbatim edits red→green off a
self-contained brief (~15 min senior hands saved). SPEC v0.15.21 · build-pipeline 0.2.20 · pack 0.8.32.

## 2026-07-06 13:05, session 13 — every step gets its craft's head (row 124)

His morning words, now law: «когда ты делаешь продукт-спеку — ты крутой продакт, когда архитектуру —
крутой архитект, когда матрицу тестов — крутой QA-автоматчик». A pipeline walked by one generalist
head produces generalist artifacts — so every step now names the profession whose head is worn while
walking it: product manager at spec, the prover's formal reviewer at both prove steps, software
architect at architecture, QA automation at matrix and tests, senior developer at code, the visitor's
own eyes (never the builder's) at verify, a careful release hand at commit & show. SPEC binds the law
(INV-33); the full step→craft ladder lives in ONE home, build-pipeline's step list; matrix M-120;
red-proven test. The prove-architecture step bit its author again, correctly: the senior briefed the
worker without an ARCHITECTURE change, the suite went red on "INV-33 has no owning node", the worker
HALTed by contract, and the assignment (INV-33 → build-pipeline node) plus a pin refresh (the ladder's
insertion had shifted four line pins) was made on the senior's word — second time this month the teeth
catch the senior's own stood-down step. A Sonnet worker ran the seven verbatim edits red→green off a
self-contained brief that carried the clock and the ledger walk, both used correctly (~15 min senior
hands saved). SPEC v0.15.22 · build-pipeline 0.2.21 · pack 0.8.33.

## 2026-07-06 13:15, session 13 — the batch's push gate: full prover walk, eval re-runs, three folds

The gate's letter, walked whole. The prover pass (record `2026-07-06-push-2.md`): the 11:57 FULL
record carries for every unchanged byte (diff-verified — only the three landed clauses moved), the
three deltas walked fresh against all their seams. Three findings, all folded within the hour: the
row-125 family one layer deeper (the pipeline's own full order lines still called step 9 "commit"
while its heading says "commit & show" — five sites swept); the brief's clock doesn't stop GUESSED
elapsed time (the row-123 worker proved it by deed, stamping +20 invented minutes — a sighted worker
now re-reads the machine clock, the brief's line is the floor); and the craft ladder was medium-blind,
the same family Alexander corrected in row 121 — the craft now wears the KIND's face (on prose the
code step is a writer's, on infra a toolsmith's). Eval re-runs (E-19, both behaviour-changed skills,
both arms, four Sonnet workers, records in `docs/evals/2026-07-06-batch2-rerun/`): build-pipeline
with-skill walks door → echo → recurrence check → class sweep → both-sides rows → close-only-whole;
communicator with-skill delivers the map, the plain station line and a consequences-framed question —
and leaked bookkeeping numbers into the message a SECOND consecutive run, so the leak got its owner
that moment: row 126 (rule 8 gains a NEVER-list). The eval briefs carried the clock and no record
misstamped — row 123's fix held on its first live test. Two more rows born at the gate: 127 — the
chat-stamp drift hit its second occurrence (my own hand, ~7 minutes fast mid-session, the fence
catching one queue stamp born of it), so the read-at-write-time sentence moves into communicator.
Installed skills re-synced (build-pipeline 0.2.21 → 0.2.22 at the folds). SPEC v0.15.23 · pack 0.8.34.

## 2026-07-06 13:23, session 13 — the closing report bounced: the jargon family's fourth strike

Alexander bounced the session's movement-end report on sight («это ты на каком языке вообще
разговариваешь???»): its lines led with pack-internal names — the board, the armed brief, the craft
ladder as Russian calques — exactly what INV-28 and the no-calques profile line forbid, and the first
strike AFTER the law landed. The lesson written into the queue as row 128: an invariant with no
enforcement step on the senior's own chat does not hold there — before any movement-end report the
communicator rules are re-read and every phrase passes "does this stand for a reader outside the
pack". The report was re-given in plain words in the same exchange (nine steps of building a feature,
named in full; helper tasks now carry the wall-clock time and the write-the-obstacle-down duty; work
each step in its specialist's role). Two side catches while writing it: the row-128 queue stamp was
written 4 minutes ahead of the clock — a recurrence on the owned chat-drift entry (row 127), date
appended; nothing else changed.

## 2026-07-06 13:53, session 14 — rows 126·127·128 land as one communicator sitting

The three lessons of session 13's close move from the queue into the skill, smallest-first by pain:
the bounced report (128) becomes a WALKED step — before any movement-end or milestone report the
communicator rules are re-read and the draft passes phrase by phrase through "does this sentence
stand for a reader outside the pack" (SPEC INV-34, the walk's home a new section in communicator);
the bookkeeping leak (126, bug door) gives rule 8 its NEVER-list with the worked ❌/✅ example, the
SPEC carve-out sharpened by the prover's own pass (a direct question about a number, or the evidence
walk, keeps the number as the answer — F1, folded in-pass); the chat-stamp drift (127) becomes the
clock law's third face — a human-facing timestamp is read off the clock at write time, never
extrapolated (INV-24 chat arm; the invariant stays with the fences node, communicator carries the
sentence — a wiring pin, one owner). WHY one sitting: three small clauses, one skill, one eval
re-run — the queue's own kin note. The sitting dogfooded both its rows: the session's own leads
drifted ~9 minutes before the clause shipped (caught at the eval-brief clock read, appended to the
ledger entry, which then flipped SOLVED with the landing), and this entry's report is the first
drafted under the pre-report walk — row 128's acceptance leg rides Alexander's read of it. Eval
re-run (two Sonnet workers, records `docs/evals/2026-07-06-rows126-128-rerun/`): the with-skill arm
shipped ZERO bookkeeping tokens as message content on the first run under the shipped NEVER-list,
after two consecutive red runs before it — numbers trailing in parens, "tested clean and saved"
doing the talking; one watched note — the station line said "review" where the step name is "prove",
first eval occurrence of that drift. Prover CROSS-LINK record `docs/prover/2026-07-06-rows126-128.md`
(F1 folded, F2 — narration lines deliberately outside the walk's scope — rejected with reason).
Suite 110 → 113 green, all three new tests red-proven first. Row 124's open leg closes: the landing
report names the hat each artifact was made under. Versions: SPEC v0.15.24 · communicator 0.1.19 ·
pack 0.8.35; installed copy synced.

## 2026-07-06 14:19, session 15 — row 131: work is narrated while it runs (and row 132 queued)

His resume message asked twice-in-one-day for the same thing — "не забывай отчитываться и по ходу
действия… это должно быть и в проекте коммуникации зафиксировано" — and the repetition IS the
lesson: the morning's word had been recorded only as a personal-profile line, and a habit that lives
only in a profile does not carry across sessions. So the rule moved into the pack: SPEC INV-35 (the
third voice between the capture echo and the landing report — beats said as they happen, plain
roadmap terms, the reports' voice, the grind quiet; a narration line is chat, not a report),
communicator rule 13 as its one home, the profile line shrunk to his tuning plus a pointer (prover
F3). The prover's other stitches: INV-28's line enumeration now names narration lines (F1), the
communicator description's NOT-side reworded so it no longer contradicts the rule it advertises —
narration is a standing habit, never a load-trigger (F2); the narration-vs-"(себе)" boundary left as
a deliberate judgment line (F4, rejected with reason). One fence renegotiated by letter, not fact:
row 68's test pinned the description's exact old phrase; the guarded fact (a stated NOT-side, no
over-triggering) is intact, so only the test's needle moved to the new wording. WHY red-first held:
the new test was proven red against the pre-edit communicator before the rule text landed. The
Sonnet worker ran the mechanical tail and stopped correctly twice — once on the senior's own wrong
matrix anchor (M-124 first placed under a section that doesn't own INV-35; corrected, resumed same
tier), once on the row-68 needle conflict (escalated — the senior's call by contract). Dogfood both
ways: the session narrated by the rule while building it, and the clock law's chat face recurred
TWICE mid-session (leads extrapolated ahead of the wall clock; both catches owned aloud, ledger
dates appended — next recurrence re-opens as a method-defect row). Mid-landing his second wish
arrived and queued as row 132: a new wish is placed on the product's feature map at intake — change
vs new vs restructure, plus a restructure trigger for the module map; kin row 129, one head. Suite
113 → 114 green. Versions: SPEC v0.15.25 · communicator 0.1.20 · pack 0.8.36; installed copy synced.

## 2026-07-06 15:58, session 16 — rows 129+132 land as one head: the product knows itself

His morning message set the day's frame: the tlvphoto windows kept receiving ideas without ever
hearing back "this is feature X, we're changing it / adding a new one" — and that complaint is
exactly the wish he had already queued mid-landing yesterday (row 132), plus its kin (row 129). So
the product-self-knowledge family landed as one head. SPEC v0.15.26: INV-36 — a project knows its
own KIND (book / backend / static site / fullstack / CLI / skill pack / custom via the queue), asked
at founding and at adoption's orient, never profile-seeded, one home in the host profile, alive as
the project evolves; INV-37 — every wish is PLACED on the product's feature map at intake, the
placement spoken with the echo and written in the row's `map:` note (changes X / new / restructure),
the map being the spec's scenarios + the architecture's nodes — no third document — and a
restructure verdict queuing its own row, re-carved only through the architecture step's re-prove.
The prover's CROSS-LINK pass found four seam holes (echo enumeration needed a one-home pointer;
project.kind vs work-kind.host-default needed a stated winner; a spoken-only verdict evaporates —
now written in the row; profile-seeding can't answer a host question) — all folded in-pass, record
docs/prover/2026-07-06-rows129-132.md. The pack's own profile now carries `project.kind: skill pack`
by deed; the first real HOST line is row 129's one open leg. Mid-landing he threw a new wish —
«покажи все фичи», transparency commands — queued as row 133 with the family's first real spoken
placement (a NEW feature beside the departures board). And the chat clock drifted AGAIN (~6 min,
caught at the worker-brief clock read) — the ledger's named next-session recurrence, so the entry
re-opened as a METHOD defect: row 134, a hook that injects the wall clock into the reply. Row 131's
open leg closed by deed: this session narrated unprompted from its first minute — no third ask
needed. He also said Fable is being taken away tomorrow (probably returns later) — the session
closed everything whole on purpose.

## 2026-07-06 16:09, session 16 (second movement) — обкатка checks on his word; Fable pulled tomorrow

He corrected the record: Anthropic pulls FABLE from Claude Code tomorrow (API-only after, return
expected «в какой-то момент») — so today runs at maximum and closes wipe-ready. Three checks on his
ask, all green: the feature list spoken in chat off the spec's scenarios — row 133's first informal
run, evidence that the map reads off existing documents; skill sizes — all six SKILL.md under the
500-line ideal (largest 382), row 69's extraction pressure eased, evidence pinned in row 130; spec
format laws — scenarios lead (17 sections), anchors trail, the 19 line-start codes are wrap
artifacts, not code-led rules. He confirmed the обкатка direction: tlvphoto window is already
exercising the pack live, the pack keeps exercising itself.

## 2026-07-06 16:27, session 17 — row 133 lands: the feature map on demand (rows 135+136 queued)

Row 133 walked the full pipeline in one movement. The wish («покажи все фичи», his transparency ask of
yesterday afternoon) became SPEC v0.15.27's new scenario "Asking what the product does" (INV-38): on the
human's ask the WHOLE map is read at ask-time off the spec's scenario sections, the current-vs-target
header, and the queue's open rows — no third document, chat by default, never uninvited. The prover's
CROSS-LINK pass caught two seams worth having: statuses must bind at the promised-tag's own granularity
(a scenario holding both shipped law and promised parts reads "shipped, with promised parts", never one
blanket status — S-0's letter), and a wish placed NEW at intake but not yet spec'd was invisible to a
scenarios-only read — the queue's `map:` notes now feed the map too. Both folded in-pass
(docs/prover/2026-07-06-row133.md). Communicator 0.1.22 carries rule 14 (the fourteenth rule) + the
when-it-fires arm (f); M-127 red-proven then green; suite 117. The row keeps one open leg by INV-26's
letter: the law itself forbids showing the map uninvited, so the first real post-law run rides HIS next
ask. One workshop note: the target-ownership machine read the index row's mention of the tag as the tag
itself — the index line now says "promised-tag" in prose; the machine was right to be literal.

Same movement, two wishes queued from his messages mid-work: row 135 (parallel lanes — feature-level
parallelism, «токены не жалко, скорость важнее»; today's session is its own pre-evidence: three
read-only analysis agents ran row 130's walks in the background while row 133 held the lane) and row 136
(the pack checks GitHub for its own updates daily and PROPOSES, never installs silently). Row 130's
walk itself came back with findings from all three agents — folding is the next movement.

## 2026-07-06 16:37, session 17 — row 130 lands: the six skills walk skill-creator (row 137 queued)

The walk itself was the session's parallel arm: three read-only analysis agents (two skills each) ran
skill-creator's craft lens over the repo copies while row 133 held the lane — the senior kept judgment,
the agents kept the reading. Thirteen findings; seven folded (the prover link that named a second repo
now points into the pack; base, prover and communicator descriptions carry their NOT-sides and lose
history scars and bare rule numbers — communicator's row-68 fence held, its pinned phrases verbatim;
build-pipeline's PLAYBOOK references name the private playbook repo so a fresh agent stops grepping for
a file that isn't there; publish gains its worked before/after example), four rejected with written
reasons (pack-wide header boilerplate stays one home; the pipeline's caps are a deliberate register for
a model reader; the When-NOT redundancy is intentional standalone support), two re-queued as row 137 —
the dense-paragraph scanability class is a restructure-scale rewrite around pinned strings, not a
drive-by. The standing law: M-1's milestone checklist now carries the re-walk item and a skill joining
the pack walks skill-creator at birth (M-128, red-proven then green). Record:
docs/audit/2026-07-06-skill-creator-walk.md. All six sizes stay under the 500-line ideal.

## 2026-07-06 17:21, session 18 — row 135 lands (pack side): parallel lanes — two trains, one pen

WHY: his word yesterday's echo (~16:20, session 17) — «надо продумать параллелизм… это тратит токены,
но зато ускоряет процесс». The design insight: the lane was never serial because everything in it must
be serial — only the writes to the SHARED TRUTH must be. So the law names that one thing the **pen**
(spec/architecture/matrix/queue/journal/resume-file edits, integration, row close — one lane at a time)
and frees the rest: the second train builds code and tests in an isolated copy of the tree, read-only
analysis rides free (row 130's walk during row 133's lane was the pre-evidence). Landing purity is its
own invariant now: a landing commit carries exactly one row's delta, gate on a clean tree,
second-lands-re-verifies (INV-39). Kept whole and fenced: the atomic committed claim, foreign-session
back-off, whole-row closing, bug preemption (now parking per-lane — the prover caught the "at most one
parked" contradiction), the batched decision page (cards name their lane's row). Prover CROSS-LINK:
7 findings, all folded in-pass — the three real ones were the T-9 contradiction, the waiting-lane
board face designed-but-not-written, and the disjoint-file worker road leaking another lane's
unfinished files into a landing gate (closed: second train = isolated tree ONLY). Delegation: the
whole mechanical batch (matrix rows, red-first tests, three skill edits, version bumps + citation
re-pins, sync, suite) went to one Sonnet worker on a verbatim brief — roughly 25 minutes of senior
hands returned, zero brief defects. Versions: SPEC v0.15.29, base 0.1.16, build-pipeline 0.2.25,
communicator 0.1.24, pack 0.8.40, suite 120 green. OPEN LEG (INV-26): the first real double-lane run —
rides the next pair of independent wishes.
(The pre-commit clock fence caught the hand a FOURTH time at this very landing — a 17:22 stamp at a
17:21 clock; row 134's case grows again.)

## 2026-07-06 18:01, session 18 — row 136 lands: the pack update check (LANE A of the FIRST double-lane run)

WHY: his word (~16:24 s17) — the pack should notice its own updates instead of waiting for a hand.
Design: no daemon — the proposal belongs where he reads, so the check rides the session's first
freshness point of the day (dated stamp throttles), asks the public repo's VERSION, and PROPOSES
(versions + journal pointer + install.sh/pull road) — never installs; offline = one honest skip line
NAMING the address (prover F1: a dead URL must not masquerade as a plane ride), ahead-of-public = up
to date, forward only (prover F2). E-25 born beside E-21/A-7, owner attach. THE RUN ITSELF IS THE
NEWS: this landed as lane A while row 137's train built in an isolated worktree in the background —
the first real T-18 run; the landing tree held only lane A's delta (INV-39 by construction), and the
independence judgment shaped the work (base left untouched so no citation re-pin would cross into
lane B's files). Delegation: lane B entire = a Sonnet worker in a worktree; lane A stayed senior
(spec-heavy, small script). Suite 122 green; pack 0.8.41.

## 2026-07-06 18:11, session 18 — row 137 lands: dense rules get scannable shapes (LANE B; the double-lane run completes)

WHY: the skill-creator walk's two re-queued findings (6+11) — build-pipeline's step-zero bullet and
communicator's rules 6/8/9/10/11 failed the 30-second scan a fresh agent needs. Refactor door: FORM
only. The worker's method deserves the journal: extracted each block's raw text programmatically
(protecting the six raw-read pinned substrings from mid-string newlines), split at sentence
boundaries, and VERIFIED token-sequence equality old-vs-new before writing — zero words moved, the
suite as the second detector, run after every rule. THE METHOD NEWS: this was lane B of the FIRST
double-lane run — built start-to-finish in an isolated worktree while lane A (row 136) walked the
document stages and landed; integration waited for the pen, the gate re-ran on the new truth,
landed-first won and the second re-verified — T-18 and INV-39 lived exactly as the law reads two
hours after it was written. One workshop find: the harness parks worker worktrees INSIDE the repo
(.claude/worktrees/) — gitignored as a class at lane A's landing so no future train's tree can ride a
landing commit. Delegation: lane B entire = one Sonnet worker (roughly 40 minutes of senior hands
returned; the token-equality rigor was the worker's own craft, worth naming). Suite 122; versions:
build-pipeline 0.2.26, communicator 0.1.25, pack 0.8.42.
(The clock fence's FIFTH catch, right at this landing: 18:21/18:22 stamps at an 18:11 clock — the hand
extrapolates whenever it stops reading; row 134's case is now five strong in two days.)

## 2026-07-06 18:13, session 18 — row 135 closes WHOLE: the double-lane run is no longer a promise

The final leg (one real double-lane run, board readable) was MET by rows 136+137 landing clean in the
same session the law shipped: lane A walked the document stages and landed while lane B built in its
isolated worktree; integration waited for the pen; each landing commit carried exactly its own row's
delta; the two-train board (working/waiting faces) was read live in chat. The method grew a
capability and proved it on itself within two hours. Rows 135, 136, 137 all close whole; row 138
(offline windows) queued from his word; row 134 (clock hook) now carries FIVE catches and heads the
practical queue.

## 2026-07-06 20:38, session 19 — row 139: the narration law grows teeth that account for the time

His third ask in the narration family, sharpest yet: the movement-end reports had become good and the
mid-work trail was still thin — «заход на полчаса-час, и непонятно, на что реально ушло время». The
law (INV-35) grew three teeth: IDENTITY — every beat names the wish and station in hand (with two
trains rolling this is also what keeps the interleaved chat readable, the prover noted it as the
composition working); DIGEST — a station's completion is itself a beat, its line saying what the
station PRODUCED in the work's own words (the seam with the bookkeeping law held deliberately: a
digest speaks what is covered or promised, never a count); HEARTBEAT — a beatless stretch past ~10
minutes [default] owes a line naming what grinds. Prover CROSS-LINK found the worker-voice hole (a
lane-B station can close with nobody speaking — folded: the senior's beat the moment the result
lands), the missing threshold, and one over-specific wording; all folded in-pass. WHY beyond the
wish: today's tlvphoto transcript audit (seven sessions, 24 hours, two reader agents) found narration
silence to be the single most recurring failure across every window — 12-to-70-minute silent
stretches, one explicitly broken "continuing without pause" promise, «did something stall?» asked
twice in one session — so this row and row 134 (the mechanical clock hand) are exactly the pair the
field data ordered. Landing hiccup worth keeping: the VERSION file briefly lost its trailing newline
and the pin-drift guardrail caught it before commit — the teeth bite their own builder, as designed.

## 2026-07-06 20:44, session 19 — row 134 builds its mechanical hand; the disease bites the landing that cures it

Lane B of the session's double-lane run: a Sonnet worker built the clock hook in an isolated worktree
while lane A (row 139) held the pen — red-proven on the absent script, then green, suite whole twice
(worktree + integrated tree). The evening supplied its own proof of need: while the hand's row was
being integrated, the commit fence BLOCKED row 139's landing on stamps written minutes ahead of the
20:38 clock, and the session's chat leads had drifted the same ~4 minutes — the eighth catch on the
ledger's chat entry, caught this time by a fence, not by luck. Install: the harness classifier
blocked the agent's own hand from wiring ~/.claude/settings.json (self-config) — the road the
Done-when named in advance; the installer script ships with row 141 and waits for Alexander's one
`!` command. The row stays in-work: the zero-drift session and the ledger's SOLVED flip ride the
install.

## 2026-07-06 20:49, session 19 — row 141: the chat laws get a voice no window can fail to hear

Born from live fire: while this session was integrating the clock hand, tlvphoto wrote «новый раздел
EX-SHARE… перед надгробием стены» straight into Alexander's chat — raw anchor codes and a doc
metaphor leading the sentence — and he asked whether anything can be DONE about communication at
all. The day's audit had already named the class: the language and narration laws live in skills,
and the failing sessions were exactly the ones that never loaded them. The fix is delivery, not
another sentence: the same prompt-hook mechanism as the clock injects a one-line reminder of both
laws into EVERY prompt on the machine — a window that never invoked a single pack skill still hears
plain-words-talk-codes-trail and narrate-with-digests on every turn. The prover's real find (two
texts, one law — the reminder could drift from its home) folded mechanically: the suite pins the
reminder's teeth, so a law change forces the hook text to move with it. Install rides the same road
as the clock: the classifier blocks the agent's self-config hand — deliberately right — so ONE
installer covers both hooks and waits for Alexander's `!` command. The honest boundary stands: chat
has no suite; the hook reminds, the eval watches, the field is the test.

## 2026-07-06 ~21:17 — row 142: the lane cap moves on his word (session 20)
**What:** T-18's parallel-lanes cap flipped 2 → 3 [default]; a fourth lane now opens only on
Alexander's asked word, never silently. SPEC v0.15.34; M-022 reworded so the cap NUMBER has one home
(T-18) and the queue law just points at it; M-129/M-130 never-sides generalized ("never a fourth
unasked"); base 0.1.17, build-pipeline 0.2.27, communicator 0.1.27; pack 0.8.46; suite 129 green,
red-proven on the skills first.
**Why:** His live word ~21:04 — a hard two-train default wastes independent work that exists; take
two-three lanes and ASK whether he wants more in parallel. Session 19's report had already named the
cap a tagged [default] one word moves — the word arrived the next session, and the settings-ladder
machinery carried it as designed (row 142's F3). The same message re-raised the communication pain
("опять непонятно что над чем работает") — answered by the board discipline, not new law: every
rolling train narrated on the departures board (INV-27/INV-35 stand).

## 2026-07-06 ~21:26 — row 140: the economy ladder, build legs (session 20)
**What:** New SPEC section "When money or time run short" — `budget.pressure` (full [default] · lean ·
tight) moved only by Alexander's word; lean = node-scoped mid-work test runs + CROSS-LINK with FULL
deferrable as dated debt + one-tier-cheaper workers; tight = + batched landing gates (purity kept,
batch-end red bisects by landing order, push still full-green at HEAD) + cheapest sufficient tier; the
never-bend list stated once (door law, red-before-fix, his gates, the report with named sheds, landing
purity, push gate, safety net, narration; a host's explicit line outlives any rung). SPEC v0.15.35
(T-19/INV-40, base-rulebook node), base 0.1.18, pack 0.8.47, M-134/M-135, suite 130 green (the suite
itself caught the missing architecture owner and the wrong matrix block mid-landing — the derivation
teeth working). Field leg OPEN: the first budget-named session.
**Why:** His 20:23 wish (row 140) — economy must be a setting moved by his word, not an improvisation
under pressure. Also this session: row 144 queued from his screenshot — the task list on his screen
must speak plain words (the language law's surface it already claims but nothing names); the open
tasks were renamed to plain Russian the same minute.

## 2026-07-06 ~21:45 — his correction batch: the skill fixes itself, not the host (session 20)
**What:** Three deltas from one message. (1) Row 143 built: the architecture step now OWES measurable
quality budgets (performance first) + an instrumentation home for every user-facing surface, asserted
by acceptance, binding from a surface's next landing — SPEC v0.15.36 INV-41, build-pipeline 0.2.28,
spec-author 0.1.16 (the performance facet ends as a budget sentence). (2) Row 144 built with his
correction folded: the session's task list speaks plain ENGLISH (docs language, not chat Russian —
the first reading was wrong) — communicator 0.1.28 rule 6. (3) Row 140 amended: the economy rung is
asked — or the default told — at a project's SETUP alongside the kind question (SPEC T-19, base
0.1.19, ADOPT orient). Also: the status vocabulary cleaned — a row whose build is done and only field
evidence rides now reads "build legs MET; field legs OPEN", not "in-work": it holds no pen and rolls
no lane, so it never eats the lane cap (rows 134/141/140/143/144 all renamed; suite 132 green).
**Why:** His words: the live-spec window should not fix tlvphoto — it should fix the SKILL so tlvphoto
fixes itself. And it already had: tlvphoto's own window landed the first-image fix + budgets + a
timings export the same evening (its c93d2cd) — evidence for INV-41's shape before the clause shipped.
The tlvphoto inbox wish was already consumed by that window; nothing to take back.

## 2026-07-06 ~21:55 — his second correction batch: think wider than the frontend (session 20)
**What:** (1) Row 143 AMENDED — the budgets law is kind-wide, not frontend-only: the project's KIND
proposes what is measurable (backend: latency/throughput/errors; CLI/pipeline: run time, per-unit
cost; skill pack: eval pass rate, suite time; prose: what honestly has a number), and a quality with
no honest number is said by name, never given a vanity metric (SPEC v0.15.37 INV-41, build-pipeline
0.2.29, M-136). (2) Communicator 0.1.29 — the calque rule now names MY OWN report coinages ("open
leg" → «открытое плечо») as the trap, with his «что это такое???» as the incident; translating after
the fact does not fix it. (3) The host profile gains `other-projects: AUDIT-ONLY` (INV-14 note: set
on his explicit word ~21:50): a project he names in this window is a case study for improving the
PACK — never intervene there, not even an inbox wish; the earlier tlvphoto inbox move was the
counterexample that taught it. Memory file written so the rule survives wipes. Pack 0.8.49, suite 132.
**Why:** His words: "смотри не только числа для фронтенда… по типу классификации проекта понять, что
измеряемое вообще"; "тлвфото сам справится, не надо его тут менеджить… НИКОГДА в тот проект активно
не вмешиваться, это только аудит".

## 2026-07-06 ~22:10 — row 138: the narration says when he can step away (session 21)
**What:** The offline-window face landed on the narration heartbeat — NOT a fourth tooth: when a
coming stretch needs nothing from the human (a suite run, a worker batch, a long render), narration
says BEFORE it starts that he may step away, an honest range (unknown said as unknown, never a guess
dressed as a promise), and what he is needed for at its end; the needed-again moment is its own beat —
a chat line awaiting his return, never a summons; beats keep landing inside the window, questions
batch to its end, an off-range end (overrun, done sooner, blocked on his word) says itself. Homes:
SPEC v0.15.38 INV-35 + communicator 0.1.30 heartbeat tooth; M-138, `test_offline_window` red-proven on
the communicator side (the superseded row-139 fence sentence asserted gone from both homes). Prover
CROSS-LINK folded two seams in-pass: the window's three ends, and the needed-again beat as a waiting
line, not a promise to reach an absent human. The first live «можешь отойти» was spoken at this very
landing's close — the field leg met by deed. Pack 0.8.50.
**Why:** His word twice — 2026-07-06 ~17:26 («надо иногда писать, когда можно оффлайн — например,
если тесты бегут») and this evening's resume ask about being pulled back every half hour: the honest
answer to «может, запустить тебя в /loop?» was that the loop mechanism doesn't cure being ASKED
things — the pack owes the offline sentence and batched questions instead; the mechanism note (loops,
wakeups) stays a profile habit, not pack law.
**Also this session:** the session hooks fired for the FIRST time (his install between sessions —
rows 134+141): the clock line stamped the prompt and the chat-laws reminder arrived. But the zero-
drift field leg did NOT close: mid-turn, record stamps drifted 2 min ahead of the wall clock again
(twelfth catch, ledger updated) — the hook owns the prompt moment; mid-turn stamps stay on the
date-before-any-stamp habit and the commit fence. Rows 134/141 field legs remain OPEN for a clean
session.

## 2026-07-06 ~22:26 — row 145: his word read as meant; the voice core goes home to the promoter (session 21)
**What:** The promoter window's inbox wish (authored-copy voice, six bans) was re-scoped on Alexander's
word — «это он перестарался»: the confident-specialist voice core belongs to the promoter's own voice
skill, not the pack; the pack kept the two GENERAL elements as communicator rule 15 / SPEC v0.15.39
INV-42: (a) cuts stay cut — a phrasing he killed in a review round stays killed in every later draft,
the kill-list written in the artifact's project records (the prover's fold: never only in session
memory, a wipe must not resurrect a cut); (b) sarcasm is not instruction — his vivid phrase is adopted
only as meant, intent read or asked. Two of the wish's six bans already lived here (no empty drama;
no approval-begging) — cross-linked, never restated. M-139, `test_his_word_read_right` red-proven;
communicator 0.1.31 (fifteen rules now), pack 0.8.51. The inbox file was deleted from the working
tree by another hand (its own window taking it back, consistent with his verdict) — git history
(f59419d) is the record; not restored.
**Why:** One home per fact and the craft split: the communicator owns the EXCHANGE with the human;
how to write persuasive copy is a host project's craft. The general spine — honouring his cuts and
reading his intent — is exchange law and belongs to the pack.

## 2026-07-06 ~22:56 — row 109: an approved prototype becomes the norm its clause points at (session 22)
**What:** The tlvphoto look-alike incident (an approved prototype's clause rebuilt from TEXT alone,
75 green tests proving the misreading) became pack law — SPEC v0.15.40 INV-43, one law with four arms
in four homes: spec-author 0.1.17 states the pointer format (`norm: <path>` at the clause's line end;
approval FREEZES the artifact into `docs/norms/` with a dated provenance line); build-pipeline 0.2.30
grew the door-step bullet (a mockup-first entry condition is written in the wish's queue row, cancelled
only by the human naming it) and the code-step clause (a norm-pointered surface builds with the
artifact OPEN, one-line plan-vs-prototype diff recorded, the verify feel bar reading the same pointer);
product-prover 0.1.11 carries the norm lens. M-140, `test_prototype_norm_pointer` red-proven then
green, suite 135. Pack 0.8.52. The inbox wish is archived with its landed pointer
(docs/queue-archive/). Prover CROSS-LINK (`docs/prover/2026-07-06-row109.md`): the sharpest find was
the pointer FIGHTING the shipped prototype-fence scan — SPEC.md is in that check's scan set, so a
pointer into a live `prototype/` home would go red at push; the docs/norms/ freeze resolves it and
keeps the fence absolute.
**Also this session, on his word:** rows 146 (the shopfront is fresh at every push — README + kind-owed
visuals ride every version push; walked by DEED on this very push: README's pipeline section got the
two new law lines, diagrams verified current) and 147 (the push gate scales to the diff's reach — his
dependency-graph word + track-coach's own written answer folded in: a declared, conservative,
self-tested REACH MAP of which checks read which file classes; a naive "only .md skips tests" is named
a trap because SPEC/matrix/SKILL.md ARE tested documents). Track-coach's "leave as is" for its own
rare-push cadence respected — AUDIT-ONLY.
**Why:** Tests derived from a misread spec cannot catch the misreading — only the artifact itself can;
the norm pointer makes the artifact reachable at every step that owes it a look (author, build,
verify, prove), and the freeze makes the pointer legal beside a one-way fence.

## 2026-07-06 ~23:06 — row 146: the shopfront is fresh at every push (session 22)
**What:** His 22:44 word became law the same evening — SPEC v0.15.41 INV-44: a push that ships a new
version re-opens the SHOPFRONT even when the diff never touched a doc; the README's claims must match
the pushed truth and the kind-owed visuals ride along (skill pack: diagrams; visual product: fresh
screenshots; tool: example runs). The walk lives in the publish skill (0.1.2) — its fire-list gained
"any push that ships a new version" (the prover's fold: the list was DIFF-triggered while the incident
class is TRUTH-triggered — a version push changes the product under an untouched README); the
pipeline's commit-and-show step (build-pipeline 0.2.31) points at it and the landing report carries
the outcome line ("shopfront checked — current"). M-141, `test_shopfront_fresh_at_push` red-proven
then green, suite 136, pack 0.8.53. Walked by deed on its own landing: the row-109 push had already
refreshed the README's pipeline lines by hand on his word; this push adds the step-9 shopfront line.
**Why:** A stale README is a false claim in prose exactly as a stale screenshot is in pixels; the
truth changes at every version push, so the freshness trigger must be the push, not the diff.

## 2026-07-06 ~23:19 — row 147: the push gate scales to the diff's reach (session 22)
**What:** His track-coach audit case («README поменял — весь прогон; давай думать что мы не до конца
прописали») + his dependency-graph word became SPEC v0.15.42 INV-45: the push gate derives its
check-set from a declared REACH MAP — which checks read which file classes — mechanically from the
diff's file list. Three teeth: EXPLICIT (guardrails/check-push-reach.sh, patterns a human reads),
CONSERVATIVE (unmapped/new file ⇒ full suite; SPEC/matrix/architecture/queue/SKILL.md are TESTED
documents and stay full-reach — track-coach's own written caveat, folded), SELF-TESTED (3 fixture
tests, red-proven bare at exit 127). The two standing "suite green" sentences (the never-bend bullet,
the machines bullet) were re-read through the map IN the same delta — the prover's must-fix. Gate b in
pre-push now scopes: prose-only diff stands the suite down BY NAME; proven by deed both ways
(README→0, SPEC→1). M-142, suite 140 green, build-pipeline 0.2.32, pack 0.8.54.
**A worker HALT worth keeping:** the Sonnet worker stopped by contract on the suite's red — and the
red was the SENIOR's brief defect (a compound word in the matrix row's level field against the closed
level vocabulary; the same trap row 104's worker hit). The traceability tooth caught it exactly as
designed; the senior fixed his own file and the suite went whole.
**Why:** "Run everything" reads rigorous and double-misses — it burns minutes on checks that read
nothing in the diff while the checks a prose diff CAN break (stale claims, dead links, a stale
shopfront) run never. Rigor = every check the diff can reach, green — thoroughness by knowledge, not
by ritual.

## 2026-07-06 ~23:25 — row 106: a stranger's first minute is clean (session 22)
**What:** `python3 -m pytest` from the repo root used to trip over templates/test_scaffold.template.py
(its test_* NAME gets collected, its import fails) — found by a clean-context analyst in their first
minute. Fix: pytest.ini pins `testpaths = tests`; the template stays a template, never collected.
Red-proven first (`test_pytest_collects_clean_from_root` failed on the pre-fix tree, exit 1 at
collection), then green: 141 collected from root, zero errors. M-143. Class swept: exactly one
collectable template in the repo; scripts/render-doc.py is not test-named. Delegation decision said
aloud: kept on the senior — a brief would cost more than the two-file edit.
**Also this session, his word ~23:24:** row 148 queued — the pack's own SPEC.md rewritten to read
like its craft wrote it (product voice in product places), with tonight's OWN new law walked at
intake: the row declares "entry: mockup-first" — a rendered before/after sample of two sections goes
to his morning eye before any whole-doc rewrite (INV-43's door arm, dogfooded the night it landed).
**Why:** The first minute IS a shopfront — a stranger's standard command failing on a shipped file is
a false claim about the repo's quality, the same family as a stale README.

## 2026-07-06 ~23:56 — rows 110 + 114 + 115: the first three-lane night (session 22)
**What:** Three laws landed as three parallel lanes off a declared dependency graph (his ~23:33 word
walked by deed the same hour; no shared files between lanes, one pen for the shared docs, one batch
landing with a shared prover record — the batch shape rows 126–128 and 143–144 already used).
- **Row 110 (SPEC v0.15.43 INV-46, M-144):** verify's ADVERSARIAL option — a fresh-context checker
  briefed with only the landing's spec sentences + artifact paths, hypothesis "tasks completed, goal
  missed", ladder exists → substantive → wired → flows + stub greps; MANDATORY for delegated
  surface-sized landings. build-pipeline 0.2.33 (step 8).
- **Row 114 (INV-47, M-145):** the gate contract — a blocking gate's red emits one typed JSON line
  {severity, code, message, fix} beside its human lines; blocking/advisory declared; all-or-nothing
  writes; home guardrails README; first gate converted by deed: the prototype fence (real scratch-run
  proof, JSON parsed); the reach decider exempt by name.
- **Row 115 (INV-48, M-146):** the resume file is a digest ≤ 100 lines [default]; open legs restate
  as one terse line each (INV-26 by form); check red-proven on a synthetic bloated file; template
  states the cap; the pack's own file is at 68.
**The night's best minute:** INV-46 ran ON ITS OWN LANDING — the fresh checker (no worker summaries,
no senior plan) returned GOAL MET plus three real findings: a matrix row over-claiming two never-
clauses with no home, a test needling one word where the law ships six stub patterns, and a
self-contradicting matrix phrase. All three were the SENIOR's own edits — the law caught its author
twice in its first hour. All folded before the landing commit; suite 147 green.
**Why:** a worker's green and a senior's satisfaction are both leads; only derivation from the spec
by uninvolved eyes is evidence — and the dependency-graph night proves parallel lanes and the pen can
coexist without a single cross-lane clobber.

## 2026-07-07 ~00:09 — rows 149 + 150 + 151 + 152: his midnight words become law (session 22)
**What:** Four laws from four of his live messages inside one late-evening hour, landed as one serial
lane (the graph's own tiny-rows word applied to its own landing):
- **Row 149 (SPEC v0.15.44 INV-49, M-147):** lanes are picked by a dependency graph — edges = shared
  surfaces/sections/files; independent set up to the cap; integration-only collisions declare their
  landing order at claim; tiny rows ride serial and the choice is said on the board. The deed preceded
  the law by an hour: three medium rows rolled as lanes, five tiny ones went serial.
- **Row 150 (INV-50, M-148):** a conditionally-entered face owes a deliberate re-entry path or a
  written one-way («если есть гет — есть сет»); spec-author's journey lens asks it, the prover's new
  entry-symmetry lens reads for it. The tlvphoto inbox wish archived with its pointer.
- **Row 151 (INV-51, M-149):** anything handed to the human leads with its passport — the project's
  name in the visible content + "needs your word: what, by when" or "just an update". Fixed live on
  the decisions page the minute he asked; now law (communicator rule 16).
- **Row 152 (INV-52, M-150):** during an away-stretch windows accumulate to ONE page and one opening
  at the stretch's end; precedence: WHEN (this rule) · HOW (the show rule) · WHAT (the passport).
  Communicator rule 17; seventeen rules now, 0.1.32.
**Worker discipline note:** the shared worker HALTed by contract on a 3-red suite — one was the
senior's own matrix-block misplacement (the symmetry row filed under the wrong node), one the known
mid-batch prover-record red, one a cascade. The traceability teeth caught the senior for the third
time tonight; all fixed pre-commit, suite whole after the landing commit.
**Why:** the night's pattern — his one-line corrections are the pack's highest-value input, and the
pipeline turns them into enforced law within the hour without losing a single one.

## 2026-07-07 ~00:14 — rows 111 + 112 + 113: the brief's birth gets its three laws (session 22)
**What:** SPEC v0.15.45 INV-53/54/55 + the delegation gate (build-pipeline 0.2.35): a brief editing
existing files is born from READING them in full (three recorded lines per file; steps back-reference
spec sentences; claims cite sources); the worker HALT list is closed (ambiguous requirement · two
consecutive unexplained failures · missing dependency · acceptance impossible — stop with evidence);
a brief is SIZED (~300 lines, ~8 files [default], splits above; paths, never inlined bodies — the
prover's must-fix: the row promised numbers and the draft said "bounded share", the vanity-avoidance
instinct overcorrected into vagueness). M-151..153, `test_brief_trio_laws` red→green, suite 152.
**Why:** the night itself wrote these laws — every brief read its files, carried the list, passed
paths; three workers HALTed by the list and every stop was a real defect. Law catching up with deed
is the cheapest law there is.

## 2026-07-07 ~00:23 — row 14: the CI mirror goes live (session 22)
**What:** The public repo now runs its own gates on every push — `.github/workflows/gates.yml` (SPEC
v0.15.46, M-5's [target] off): the same guardrail scripts as the local pre-push, a SECOND net that
always runs the full set (the reach map stays a developer-latency optimization, said in the SPEC, the
README, and the workflow's own comments). fetch-depth 0 because the prover-record freshness rule
reads commit history; TZ pinned to the author's day so a post-midnight push doesn't hunt yesterday's
record in UTC. Host guidance in guardrails/README (copy, swap the test command, never redefine a
check). The [target] tooth worked exactly as designed: index, header list, and the suite's declared
target map each went red in turn until the landing updated all three. M-154, TestCIMirror red-proven,
suite 154, pack 0.8.58.
**Why:** the gates' truth lives in one place; CI re-RUNS it. And the shopfront law gets its mechanical
cousin: a public repo whose checks run in the open is a claim a stranger can verify.

## 2026-07-07 ~00:30 — the CI mirror's first catch, fixed the same half-hour (session 22)
**What:** the mirror's FIRST live run went red on a real environment truth — the pin-drift gate
demanded `~/.claude/CLAUDE.md`, a file that exists only on the author's machine. Fix: a machine-local
pin (~/ or absolute) is NOTED and skipped when CI=true, strict everywhere else — proven by deed both
ways (foreign HOME + CI → note + exit 0; foreign HOME local → hard FAIL), regression-tested
(`test_machine_local_pins_skip_in_ci_only`, with the scratch-copy guard its siblings wear), M-154's
never-side extended. Alexander got GitHub's failure mail and asked — answered with the passport: his
project, just an update, nothing needed from him; the mail's very existence was the second net doing
its job on its first breath.

## 2026-07-07 ~00:36 — row 153: a limping thing never dams the flow (session 22)
**What:** his 00:17 word became SPEC v0.15.47 INV-56 + base rule 19's new clause (0.1.20, inherit
pins swept in all five skills by the freshness tooth): a KNOWN owned problem PARKS behind a written
holder and unrelated lanes keep rolling; hand-fix loops cap at two-strikes; a mechanically-owned
defect is serviced in BATCH — silent fence fixes, one session-end ledger append — never per-instance
ceremony. Applied by deed BEFORE it landed: the clock-drift ceremony (ten hand-passes in one night
while its owner row sat open) retired to batch mode at 00:18. One honesty note: the red-first order
slipped (skill edit preceded the test); the red was proven against HEAD's shipped state via git show
and owned aloud. M-155, suite 156, pack 0.8.59.
**Why:** the method's own failure mode is perfectionism-in-place — orbiting one limp while the queue
waits. The ledger already owned recurrence; this law owns the FLOW.

## 2026-07-07 ~00:57 — row 154: the stretch's end is unmissable (session 22)
**What:** his 00:53 complaint — a seventeen-row night that ended, to his eye, «без сообщения» — became
SPEC v0.15.48 INV-57 + communicator rule 18 (0.1.33, eighteen rules): every stretch ends with one
SHORT final line, LAST after all tool calls — what closed · what's next · what's needed · when the
agent wakes; the long report above; a page deliverable repeats its passport there. Delivery, not
existence. M-156, red→green, suite 157, pack 0.8.60.
**Why:** the 00:38 report existed and drowned; a law that measures existence instead of delivery
measures nothing the reader feels.

## 2026-07-07 ~01:03 — rows 158 + 160 + 162: the promoter audit's first harvest lands (session 22)
**What:** his ~00:53 audit ask ran as a read-only case study over both promoter repos (an Explore
reader, file-cited); eight pack lessons queued (rows 155–162), the communicator trio landed the same
hour — SPEC v0.15.49, communicator 0.1.34 (twenty-one rules): **approved text is frozen** (a revision
applies exactly the named correction — the promoter's v1.1 opener rewrote an approved sample and
smuggled in a banned pattern; INV-58, rule 19); **no question asked twice + dialogues converge**
(search the recorded word before any ask; answered closes forever, harvested same session; round N+1
only new — his escalating hour: «на кучу похожих вопросов уже давали ответы»; INV-59, rule 20); **a
taste ask carries a mined proposal** («сам нашёл, предложил — потом показывай»; INV-60, rule 21).
M-157..159, one shared red-proven test, suite 158.
**Still queued from the harvest:** 155 (process cost scales to the delta — his iteration-length
question, the senior's own 40%-bookkeeping audit), 156 (smallest sample first), 157 (rejected
artifact reopens its source), 159 (mechanical kill-list template), 161 (provenance chips +
commentable reviews).
**Why:** the promoter window paid five rejected rounds to learn these; the pack writes them once so
no host pays twice.

## 2026-07-07 ~01:27 — row 155: process bookkeeping scales to the delta (session 22)
**What:** his «каждая итерация очень длинная» became SPEC v0.15.50 INV-61 + the pipeline's gates
sentence (0.2.36) + the host profile's cadence line reconciled: the pre-push re-check keeps its rigor
(previous records · the delta walked · a verdict) and scales its FORM — small deltas ride a three-line
short-form record, surface/structural deltas keep the full walk; claims batch per lane, journal and
resume once per batch; the irreducible named (writing the law well, red-first, the delta prove, the
gates). The ~40% bookkeeping audit of tonight's own landings is the row's evidence. M-160, suite 159.
This very landing ships the FIRST short-form record — the law's own dogfood.

## 2026-07-07 ~01:29 — rows 156 + 157: the sample gate and the source-reopen law (session 22)
**What:** two more promoter lessons into the pipeline (SPEC v0.15.51, build-pipeline 0.2.37):
taste-heavy deliverables build SMALLEST-FIRST — the cheapest judgeable sample takes his word before
the full build spends (INV-62; five full media-packs once died where one paragraph would have) — and
a REJECTED artifact reopens its SOURCE: correct the card/clause/brief, rebuild from it, never
line-patch the output (INV-63, the five-round trap banned by name; composes with the frozen-approved
law — two ends of one review). M-161/162, shared red-proven test, suite 160, pack 0.8.63. Short-form
record per the new bookkeeping law.

## 2026-07-07 ~01:31 — row 161: review surfaces show their sources and take his pen (session 22)
**What:** the promoter's «я не знаю, откуда ты всё это взял» + his standing never-a-read-only-wall
word became SPEC v0.15.52 INV-64 + communicator rule 22 (0.1.35, twenty-two rules): anything shown
FOR REVIEW carries per-claim provenance (artifact · his recorded word · MY INFERENCE — inferences
loudest) and is commentable with the decision page's JSON answer capture extended to review pages.
M-163, red vs HEAD, suite 161, pack 0.8.64. Short-form record.

## 2026-07-07 ~01:34 — row 159: the kill-list grows teeth (session 22)
**What:** the audit's last harvest row — SPEC v0.15.53 E-26: the pack ships the kill-list TEMPLATE
(dated literals, appended the moment a cut happens, never removed) + guardrails scanner guidance (a
test greps the artifact's surfaces for every killed literal; a reappearance is red). Born of the
promoter's scissors returning into the headline after the ban was «written on the forehead». The law
stays with the cuts-stay-cut rule; this is its mechanism. M-164, red vs HEAD, inventory entry, suite
162, pack 0.8.65. Short-form record. **The promoter audit is fully harvested: eight lessons, eight
landings (149-through-162 family) in one night.**

## 2026-07-07 ~08:35 — session 23 morning: row 54 landed (build legs), rows 163+165 queued, row 148 rounds 3–4 (his eye in)
**Row 54 (onboarding):** the pack now learns WHO it works with before any founding question resolves —
SPEC v0.15.54 B-3 + ADOPT's first-breath-of-orient paragraph + the base rulebook's found-or-founded
clause + templates/profile.template.md (every placeholder marked so nothing passes for the human's
word; INV-9 is the ceiling). B-3 → attach. `test_onboarding_step` red-proven against HEAD, then green;
suite 163; base 0.1.21, pins swept; pack 0.8.66. The whole mechanical bundle ran on a Sonnet worker,
which correctly STOPPED on one brief defect (the requirement's test row belonged in the attach
component's section; the brief had placed it by number order) — the senior placed it; the stop itself
is the worker-contract law working. Field leg OPEN: first real run rides the next real setup.
**Why now:** his overnight loop word — take without-him rows to landing.
**Rows 163 + 165 queued from the morning's two harvests:** the test-methodology extraction into a
test-author skill (inbox from track-coach's close, archived with pointer), and skill discovery at
setup + at every struggle (promoter audit: five review rounds died on failures a public skill,
stop-slop, already carried as a checklist — with the borrowing practice: invoke found skills as-is,
paraphrase + credit for folded lessons, verbatim only under license). The inbox wish on commentable
review surfaces was already covered by row 161's night landing — archived with a pointer, no new row.
**Row 148 (spec readability), his morning eye:** round 2 killed (~07:59 — the rule-book genre out; bar
= use-case genre per BMAD+Kiro, both formats researched); round 3 killed on language (~08:11 —
STRUCTURE approved; scissors banned FOREVER globally → profile law, native-plain English named);
round 4 rewritten in place, awaiting his word. Two more of his morning words went to the profile:
the calque sharpening (narration in the industry's standard vocabulary, coined terms stay in docs) —
after «ломаный ассоциативный» hit my own narration line; and the clock fence caught an invented
stamp mid-commit (catch #21) — the fence blocked the commit until the stamp was read off `date`.

## 2026-07-07 ~09:38 — session 23: row 165 landed (build legs), row 148 round 4 answered, row 166 born out-of-turn
**Row 165 (skill discovery):** the workshop now searches for an existing skill before reinventing —
at setup (beside the founding questions) and at every struggle (a ledger entry's second occurrence, a
taste artifact rejected twice); found skills adopted or rejected by name; borrowing practice: invoke
as shipped · paraphrase + named credit · verbatim only under license. SPEC v0.15.55 INV-65 · base
0.1.22 rule 20 · M-166 · red-proven test · pack 0.8.67 · suite 164. Worker-run bundle, zero deviations.
**Row 148 round 4 answered (~09:34, JSON archived):** genre and language approved; three adjustments —
pre/postconditions where they exist · an epic grouping proposal · a SERIOUS VALIDATION with a thorough
plan before the whole-doc rewrite; the WHEN/THEN/SHALL caps killed («псевдодраматичность»). Validation
inventory (every mechanical consumer of SPEC.md's shape) delegated to a scout this session.
**Row 166 born on his out-of-turn word:** a live work board — what the agent does at every moment, the
whole process always visible. Mockup-first entry declared; prototype on real data goes to his eye.

## 2026-07-07 ~10:36 — session 23: row 163 landed (build legs) — the test-author skill is born
**What:** the pack's seventh skill. The test method that rebuilt track-coach's suite — the level
ladder (string / DOM-text / browser-computed / pixel), real-artifact assertions, red-first proof, the
pinned skip-set, traceability as a standing test, the state-space walk — now lives in ONE home,
skills/test-author (0.1.0), invoked by build-pipeline at the matrix and test steps the way the spec
and prove steps invoke theirs (SPEC v0.15.56 E-27; architecture: new node, derivation seam named,
lens re-proven with the landing). Credits in the skill name track-coach (MIT) per the borrowing law.
**The eval ran for real (E-19):** two same-model arms on one derivation task. Honest red: the bare
arm's craft was strong; the skill's edge is the method layer — the matrix as an artifact, a level
pinned per row with its reason, red-first, the pinned skip-set, standing traceability — and it caught
a planted anchor gap the bare arm walked past. evals/test-author.md holds the record.
**Two worker HALTs, both correct:** (1) the communicator's closing pack list turned out to predate
the publish skill — four skills listed, two missing; the class (lists drift) got row 167, a
mechanical parity check; (2) my own skill file shipped a flat version key and no eval — both fixed by
the senior, the worker never touched beyond its grant. Suite 165 green; pack 0.8.68; installed
copies synced (test-author absent → 0.1.0).

## 2026-07-07 ~10:41 — session 23: row 167 landed — pack lists can no longer drift silently
**What:** one pure checker over the real files: every place the pack lists its skills (the SPEC's
working-skills sentence, the skills' closing lists, the README table) must name the same complete
set; a missing name goes red at every commit (SPEC v0.15.57 INV-66, M-168, suite 167). The never
side is permanent: the second test runs the checker on the historic four-skill communicator footer —
the exact artifact that drifted — and demands it fail. Second occurrence of the lists-drift class
(cross-audit F2 was the first); the ledger's law fired, the class now has a mechanical owner.

## 2026-07-07 ~10:51 — session 23: row 55 landed — the snapshot design is decided
**What:** the last-accepted-baseline machine got its full design (SPEC v0.15.58): home
`.live-spec/snapshot/` with a per-surface manifest (what · landing · hash), the baseline advances
only at a landing and only for declared surfaces (the asymmetry that catches unasked change), and
retention closed the open decision: last-only in the working tree, git history as the archive — an
older baseline is one checkout away, so a second archive mechanism never exists; heavy surfaces keep
only their hash in git. The machine itself stays a target: its first mechanical slice rides the
guardrails scaffold row. Suite 168 green; pack 0.8.70.

## 2026-07-07 ~11:02 — session 23: row 168 landed — the showing channel matches the session's seat
**What:** his morning question («локально — хтмл, а на удаленке — клод в браузере; распознаёшь?»)
became law: a locally-seated session opens rendered pages in a browser window; a remotely-seated one
sends the same content through its own channel (an artifact page or the chat), same passport, same
round-trip; the seat is detected from what the session can actually reach and the pick is said aloud.
A local path handed to a remote reader is now a named defect. SPEC v0.15.59; communicator 0.1.37;
the personal profile's show line marked as the local arm. Suite 169; pack 0.8.71. Field leg open:
the first real cloud-seated session.

## 2026-07-07 ~11:19 — session 24 opens: inbox swept, row 169 landed — the plugin shopfront tells the truth
**What:** the resume file said "inbox EMPTY", the sweep found one unswept wish (promoter window,
that morning): marketplace.json ships no description, the validator warns, directory submission runs
the same check. Harvested as row 169 (bug door, infra kind) and fixed the same hour — and the class
widened at the fix, exactly per the sweep law: plugin.json carried two SIBLINGS nobody had named —
a five-skill description (the lists-drift class of row 167, alive in shipped metadata the parity
scanner never reads) and a version pinned 0.8.0 against VERSION 0.8.71. All three fixed in one
change; both descriptions now describe the pack without enumerating skills, so the list cannot
drift again; plugin.json's version is asserted equal to VERSION on every suite run. M-171,
`TestPluginMetadata` red-proven against the real shipped files, then green. Validator re-run:
the description warning is gone; the icon warning stays by the wish's own word (agreed safe).
Suite 171 green; pack 0.8.72.
**Short-form record:** previous prover records clean (row 165's one open row is the field leg,
riding); delta = plugin metadata truth + its matrix row and tests, no spec prose touched; verdict —
green, push-ready.
**Why:** the shopfront is the first thing a stranger reads; a five-skill list and a 0.8.0 pin were
quietly lying about the pack. The fix follows the row-167 lesson to its metadata sibling: complete
lists live where the parity check reads, everything else describes without counting.

## 2026-07-07 ~11:47 — session 24: row 47 lands — the pack learns to LISTEN (feedback-intake, the eighth skill)
**What:** the "шикарная вещь" wish from 2026-07-05 shipped whole: a new scenario "Sending feedback in"
(SPEC v0.15.60, E-28/T-20/INV-68) and the **feedback-intake** skill (0.1.0) — anything a person hands
back (a remark, an answer, a screenshot, a dropped file, a relayed user report) takes exactly one of
five routes, each citing the law that already owns it, and lands the same session in that route's
home. The routes that had no home get one: **FEEDBACK.md**, the append-only field-evidence ledger
beside the queue — the first honest slice of INV-21's reading machinery (plugins and aggregation stay
[target] under row 48). The inbox door widened from wishes to items (wish or feedback), harvest
destination by route, the one-commit sweep law kept.
**The prover earned its keep:** the draft promised a ledger line for EVERY item — double bookkeeping
against the queue, the archive, and the journal (the INV-61 drift risk); the fold gave routes their
own homes and the ledger only what was homeless. The inbox contradiction (harvest says "into a queue
row") was caught as a fence I had wrongly declared and re-authored properly.
**The eval was honestly red:** the bare Sonnet arm archived the decision, fixed the typo, owned the
workshop warning — a strong floor — but scattered field evidence (a vague friend-remark became queue
spam, a visitor's praise a journal note), named no sweep-commit law, no append-date discipline. The
with-skill arm routed all six by the table.
**Also serviced in passing:** the count-drift class (rows 167/169's family) swept again — SPEC header
"six skills", README "The six skills" heading, two seam cells; and test-author's architecture pin
label lied about its vicinity (the gate's standing DRIFT warning since yesterday) — label fixed, pin
gate fully clean for the first time today.
**Delegation:** the row-47 context dump and both eval arms ran on Sonnet workers (~25 min of senior
time saved); the footer/README edits stayed on the senior — smaller than their brief.
**Why:** decision pages carry work out; until today nothing owned what comes BACK. Now the exchange
has both halves, and success measures have a place where real signals can accumulate — row 96's first
loop can run on a real project.

---

## 2026-07-07 12:09 — Row 12 CLOSED: CLAUDE.md/PLAYBOOK mining complete (session 24)

The large mining row (map every CLAUDE.md/PLAYBOOK rule → skill → gap, fold the gaps) is done. Its
map had two remaining items after session 9's folds.

**Gap 7 — standing default-delegate list (verify-only).** The claim in the map was "partial: tier
examples exist but the standing category list isn't distilled into build-pipeline". Stale: the
≥1-holds trigger list in build-pipeline §Junior delegation IS that standing list, just phrased as
triggers — >3 files read for facts (audit across files), a known script/suite >~30s (run a suite),
output is a report/list/dump, edit strings/command known verbatim (apply defined edits). Moved
partial→folded in the map with the citation; no skill change. (Translate-text is the one category
not spelled as its own trigger — falls under dump/command-known, not worth a bespoke line.)

**Gap 11 — supersession sweep (folded).** "When a global rule supersedes an earlier one, sweep the
project-level copies" was a real un-homed gap. Folded as a named clause on live-spec-base **rule 14**
(fix-the-class sweep) rather than a new maintenance rule — a rule superseded at a broad scope makes
its restatements at narrower scopes (a host CLAUDE.md, a project playbook copy, an installed skill)
stale siblings, swept in the same change. Chose to extend rule 14 over inventing a rule so the pack
does not grow where an existing class already owns the case (compaction discipline). base 0.1.24.

**Class swept while here (rule 14 applied to the guard itself).** Bumping base 0.1.24 tripped the
base-pin sweep: 7 skills cite `` `live-spec-base` (vX) ``, all moved to 0.1.24. But the pin-drift
gate (`test_traceability.py`) only enforced 5 of the 7 — test-author and feedback-intake (newer
skills) had added the pin without being added to the gate's list. Widened the gate to all 7 real
citers, so the guard now covers the whole class it guards.

**No delegation:** all edits were single-file reasoning edits or one verbatim sed (7 identical pin
swaps) — sub-brief; a worker's saving would have been seconds. The real fan-out is reserved for the
0.9.0 milestone audit.

Pack 0.8.74, base 0.1.24, suite 174 green. Map banner-closed (all 11 ranked gaps resolved).
**Next:** row 56 (model router) opens the 0.9.0 movement; the milestone (3-pass preventive audit +
doc compaction) lands the MINOR bump — Alexander's ask this session.

## 2026-07-09 ~22:23–23:17 — session 30: the evening queue drained — rows 180-187, eight landings

Alexander's word at open: continue the run, everything left, to the end. What was left after his
evening verdicts: the reopened architecture item, the worker-liveness inbox wish, the five
test-method lessons, and the pre-ask scan. All eight landed this session; items 6 (onboarding
mockup) and 7 (the 1.0 gate) stay on his word, untouched.

**Intake first (209f84e).** The tlvphoto worker-liveness inbox wish harvested (moved to
docs/wishes/, inbox EMPTY), and the evening's wishes got queue rows 180-187 — the intake commit
from the previous evening had written wish files without rows.

**Row 180 (019d793) — the architecture owes a runtime view and a placement view (INV-74/75).** His
verdict on the tlvphoto derivation reopened RUN item 5: the derived doc never traced a flow through
the nodes and held placement only as prose. WHY the shape: the failure was an enforcement failure —
the three-check architecture lens never ASKED for budgets or views, so the derivation skipped them.
So the landing grew the lens to six checks in all three homes (SPEC prose, product-prover Phase 0,
build-pipeline step 4), gave the template four missing sections (Runtime view · Placement view ·
Quality budgets · Feature coverage — sections the law mandated and the template never prompted
for), and made our own ARCHITECTURE.md (v0.3.0) model all three, skill-pack-scaled: the wish-walk
runtime table, the five-places placement table, budgets (suite ≤ 60 s [default] — measured ~30 s).
Validation re-ran read-only over tlvphoto with a sonnet worker's fact-gather (941 lines, citations;
~15 min senior time saved): prose lint 0 errors, and the diff against tlvphoto's real hand-grown
ARCHITECTURE.md left NO unnamed hole — one deferral by name (an at-a-glance diagram stays the
author's option). The reverse diff (the real doc lacks the two views) went to tlvphoto's own window
as one inbox wish, the sanctioned channel. En route, the class sweep also fixed two pre-existing
negation-opener lint errors in old spec prose.

**Row 181 (186ee8b) — a background worker outlives a memory wipe (INV-76).** The tlvphoto race
distilled: ps and the harness task list are never proof of death; the handoff note records the
worker's id (→ its checkpoint), its briefed write-set, and the two liveness checks (~30 s file-time
watch + ~2 min reply window, both [default], told per INV-70); a prior-context worker is a FOREIGN
writer until verified — the same-session fence-benign courtesy never crosses a wipe; no second
worker until the first halts by its own reply or is declared dead; prefer halting workers before a
wipe. Base rules 6 and 7 carry the elaboration; base 0.1.26, pins re-synced in all 7 skills.

**Rows 182-186 (c16bbf3, 1a7010b, 352a822, ef00380, 2275300) — the tlvphoto week's five lessons.**
Each a method rule, never a project patch: INV-77 the real-device boundary (a walk row the suite
can never green, kin of the feel gate); INV-78 geometry asserts relative-wide-long so cumulative
drift shows; INV-79 an extracted engine tests on engine-shaped fixtures + a content contract per
donor constant (test-author + spec-author halves, one law); row 185 rode the bug door — the miss
mechanism NAMED: the composition lens (INV-72) landed only that morning, and adoption's
skip-the-re-prove exemption was lens-blind, so ADOPT.md now requires the same prover version and
every prover record opens naming the version that ran; INV-80 the suite's plumbing must not lie
(skip helper imports at module load · shim re-export completeness · a background/delegated run's
verdict is the suite log's tail line, never the wrapper's exit).

**Row 187 (3380c11) — the pre-ask scan covers questions (INV-81).** Before any question to the
human: the outside-reader read plus the FIRST gate "can I decide or verify this myself?"; a
surviving question carries its recommendation. Scoped so narration stays question-free (INV-35
untouched).

**The workshop's own lessons tonight, honestly:** the clock hook BLOCKED two commits for invented
future stamps (~23:05, ~23:10 vs the real clock) — the mechanical hand works, and stamps are now
read via `date` at write time; and one commit went through on a red suite because my command chain
read the log's tail instead of the verdict — exactly INV-80's third leg, landed the same hour; the
red was the gate's own record-ordering check, fixed by amending the same row's commit (ef00380),
suite verified green after.

Session totals: SPEC v0.16.3 → v0.16.10 (INV-74..81, eight new invariants) · base 0.1.26 ·
build-pipeline 0.2.43 · product-prover 0.1.15 · spec-author 0.1.23 · communicator 0.1.41 · pack
0.9.8 · suite 225 → 236 green, ~30 s wall (inside its new budget). Delegation: the tlvphoto
fact-gather rode a sonnet worker; everything else was judgment or sub-brief edits.
**Next:** item 6 waits his eye on onboarding mockup v2; item 7 (M-1 audit → 1.0.0 → push) waits his
explicit go and runs AFTER item 6 lands, so the audit covers it.

## Session 31 — the night run, phase 1: the docs pass (2026-07-10, overnight)

**The 1.0 docs condition landed.** Nine reader-facing documents were written by nine spawned
workers, each draft folded and gated by the senior: README.md rewritten crisp at 72 lines
(what / who / install / one worked example / the eight-skill table / docs map), OVERVIEW.md
rewritten as the five-minute conceptual tour, and seven new pages under docs/ — pipeline.md (the
station-by-station walk, wish to shown result), architecture-method.md (template sections, the
runtime and placement views, budgets, the prover's six-check lens), test-method.md (matrix
derivation, the level ladder, the five field lessons), onboarding-and-settings.md (the settings
ladder, both profiles, session hooks), push-law.md (the done-gate, the commit rule, the push law,
log-tail verdicts), worker-liveness.md (spawn briefs, the two liveness checks, git discipline,
resume), adoption.md (the guide into ADOPT.md, migration, templates, what stays optional).

Every page passed spec-style-lint and preshow-lint (worker's run re-verified by the senior's own),
rendered clean through render-doc.py, and the full suite stayed at 239 green (~33 s), read from the
run's own tail. One senior fix during folding: the README's worked example still claimed a push
waits for the human's word; corrected to push-by-rule with the named-release exception (INV-82).
Workers reported their unsourced-fact notes honestly; none invented content — two brief-vs-repo
mismatches (MIGRATION.md's actual scope, the scaffold's planned-code note) were resolved from the
real files. Docs-only wave: VERSION untouched, no skill file changed.

## Session 31 — the night run, phase 2: the global pass + three landings on his night words (2026-07-10, overnight)

**The audit.** Eight parallel reviewers (opus for judgment, sonnet for the mechanical eval run — his
~00:38 word landed as the standing model routing: the senior orchestrates and accepts, workers carry
the work). Full spec re-prove found one real contradiction — the new push law read as an automatic
push grant and ignored the peer-session fence; folded as two clauses (INV-82, spec v0.16.14) with the
tight rung's push line inheriting the reach map. Matrix audit: mechanized coverage airtight, the
artifact inventory had drifted (two newest skills, seven reader docs, one template — folded; the
base-pin test now covers all eight skills with the version half). Composition check: no contradiction
of substance, three naming drifts folded (verify by deed / behaviour-traces-to-spec / host). Formal
index: clean on all five axes, four of them manual-only — a standing symmetry test queued (row 196).
Deferred-triggers re-scan: the render-doc cross-link deferral FIRED (nine cross-linking reader docs
landed while the renderer resolves nothing — row 195, and the false resolution claim in spec-author
and the format doc corrected to the truth the same hour); five his-word backlog items got durable
queue homes (rows 203-207). Skill craft walk: no dead references; small fixes queued (rows 200-202);
a stray stale SKILL.html removed. Eval protocol re-run over all seven skills: red-bare/green-with
reproduced, no regression. Doc compaction: candidates listed, all milestone-gated.

**Three landings on his words, same night.** Row 170 (his priority): the pre-show register lint —
anything shown to a human passes scripts/preshow-register-lint.py, a red BLOCKS the showing (INV-83,
spec v0.16.15); red-proven on tonight's real leaks (the onboarding mockup's three lines he bounced,
the calques a sibling window's chat showed him — «швы с соседями», «смерть счёта» class), green on
the nine reader docs; communicator 0.1.42 wires it as the walk's step 4; the chat-law hook gained the
no-calques reminder, installed copy refreshed. Row 208 (his ~00:53 word): human-facing prose is
drafted by a clean writer (INV-84, spec v0.16.16, base rule 21) — the marinated session briefs,
reviews, lands, never writes; born of tonight's evidence: nine clean-drafted docs passed his bar
first time, the marinated onboarding text bounced three times; the law's own wording came through the
clean road. Row 209 (his ~01:17 word): the README owes a Known issues section — publish checklist
floor (0.1.4) + the pack's own five honest issues as the first instance.

**The clean judge, confirmed on his ~01:22 word.** Both prose judgments tonight ran as the protocol
demands — a fresh opus spawn, locked rubric, planted-defect canary (all planted defects caught both
runs). The judge's surviving findings on the settled text (eleven, all metaphor/redundancy family:
«a limping thing never dams the flow», «the shell eats a command», the no-third-document restatement)
are row 210's worklist — the plainer-prose rewrite gets its first concrete list. Tonight's added
clauses drew zero findings. Style-gate debt unchanged at the recorded 63 (the parked Formal-index
restyle); one new caps error introduced and fixed the same hour.

**Onboarding.** Mockup v3 bounced (~00:50, the third bounce — a method defect, признан): his three
exhibit lines are now the lint's red fixtures; v4 rides the clean-writer road and is shown in the
morning; the build stays parked on his verdict.

**Workshop honesty.** My own chat carried the same calque disease tonight («стыки поверхностей») —
the lint's pattern list holds it now. Mid-train suite runs proved meaningless (the tree is a mixture
between staged commits); the batch-end full gate is the verdict, exactly as the tight-rung clause
folded tonight states. Commit train: 6fe54d7 (global pass) → 0e36780 (row 170) → e3e54a2 (row 208) →
5d4bed3 (row 209), byte-verified against the gated finals before the closing commit.

Versions: SPEC v0.16.13 → v0.16.16 (INV-83, INV-84; INV-82 amended) · base 0.1.27 · communicator
0.1.42 · spec-author 0.1.25 · build-pipeline 0.2.45 · publish 0.1.4 · pack 0.9.12 · suite 239 → 266+
green. Delegation: nine doc writers + eight auditors + two clean drafters + one judge pair on
opus/sonnet; the senior's hands held folds, gates, and the train.

## Session 31 — the night run, phase 3: the queue wave (2026-07-10, overnight, ~02:07)

**Four more landings.** Row 195: rendered docs resolve their cross-links — render-doc.py rewrites
relative .md links to rendered neighbours and gives headings GitHub-style ids; four tests red on the
old script, green after; the false already-resolves claim corrected at both homes; the README's
Known-issues bullet left the list the push its fix shipped. Rows 211/212: the post-fold re-check's
wording seams folded — one question per gap at the first push moment; the register lint names its
artifact-only reach; the clean-writer road names its unit (the touched section), its chat edge, and
the mechanical-correction carve-out; base 0.1.28. Row 190 (method legs): the engine/instance split
is proposed at founding and orient, never imposed; the pair is led as two full hosts with the inbox
door as the only seam; the producer-wish walk stated entry to exit; two open decisions ride with
recommended picks (D-6, D-7); the delta was drafted by a clean-road worker and folded by the senior.
Field validation of the pair stays open by design — the first real pair executes in its own window.

**Research recorded for his morning word.** Row 191 (field test norms): the level ladder measures
what a test can SEE, the field's unit/integration/e2e measures how much it exercises — orthogonal
axes, no replacement needed; two real adoptions proposed (test-data hermeticity as a standing duty;
property-based tests for input-space invariants). Row 193 (missing stages): the pipeline's honest
gaps are an executable release step with rollback for hosted products and a data/ML eval gate wired
into the budgets law; monitoring stays deliberately deferred save a liveness eyeball at release.

**Gates.** Judge v3 (fresh opus, canary passed): nine surviving findings, all in settled text, none
touching tonight's delta — row 210's worklist. Pair-wave delta prover: zero must-fix, two folds
shipped same pass (the founding-question count made consistent; the carve-out), three seams to row
213; verdict safe to push v0.16.19. Style gate at the recorded 63; suite 273 green at the batch's
head. Onboarding v4: drafted clean, register lint green, outside-reader check passed all sections —
opens for his eye in the morning. The push to the remote is BLOCKED by the harness's own classifier
(above any model); the wave waits for his hand: `! git -C ~/live-spec push origin main`.

## Session 31 — the night run, phase 4: the small-rows wave, and the session's own register lesson (2026-07-10, ~02:22)

Rows 196 (the Formal index's standing symmetry test, seeded-defect red-proof), 200 (README + LICENSE
for the two newest skills, clean-drafted), 202 (four craft fixes; the vocabulary crosswalk moved to
its design-note home and the two needle tests followed the fact lawfully) and the pair-adoption
teaching page landed; suite 277 green at HEAD, tree clean. Row 201 (the build-pipeline delegation
trim) was launched into a write collision with row 202's pin bump, stopped before any write, and
stays queued — the collision itself is a fresh sample for the pack-orchestration row (206).

His night words folded as they came: the model routing (the senior orchestrates and accepts; opus
drafts and audits; sonnet does mechanics) · the clean-writer road as law · Known issues in the README
· the clean judge confirmed as the standing protocol · and for tomorrow: the tlvphoto migration onto
the pair law — their windows execute, this window teaches and supervises, never writes their trees
(the audit-only rule's named amendment, recorded in the resume file).

The session's own lesson, honestly: my chat slid into the same loan-translated dialect twice tonight
(«стыки поверхностей», «иголочные тесты») and he caught both. The mechanical reminder now fires in
every window; the artifact lint blocks what is shown; live chat remains the weakest surface — his
call to wipe this session's memory and resume fresh from the files is the right one, and this
chapter closes with everything needed for that cold start on disk.

## Session 32 — the night run, phase 5: the leftover queue drained by the charter (2026-07-10, ~02:45–03:20)

A fresh window resumed cold from the resume point and worked the night plan's leftover queue —
rows 213, 210, 201, plus the tlvphoto inbox wish intaken as row 214 — one clean-writer spawn per
item (opus, pack not loaded, self-contained briefs), the senior folding and gating each landing,
one commit per row. Suite went 277 → 278 green; the tree is clean; the push still waits his hand.

**Row 213** (e819b89, spec v0.16.20): the pair-wave's three seams discharged as the prover record
demanded — the F-pair walk now names its liveness net (the dated blocked-on-engine debt line rides
every instance status report [INV-27] — the one anchor the fix itself adds), INV-86's inbox sentence
carries its carve-out inside itself ("beyond that one inbox file"), and the declined-split reuse
note got the fixed key `reuse.split-declined: <date>` in body and index.

**Row 210** (a760f1c, spec v0.16.21): the clean judge's nine surviving findings plus one filler nit
reworded plain — and the flagged phrases' exact siblings swept where they still stood as current
text: the "limping/dams" rule sentence in the base rulebook and matrix row M-155, "they go dark" in
communicator. Two needle tests followed the reworded facts in lockstep (the facts stand, the wording
moved lawfully — row 202's precedent). Base 0.1.30, communicator 0.1.43, seven base-version pins
refreshed. The re-run judge came back with the canary fully caught and ZERO surviving findings;
anchors proven identical by multiset; style debt 63 → 62, redundancy candidates 11 → 11. Row 148's
first concrete worklist is done.

**Row 201** (0b5aee8, bp 0.2.46): the delegation-block trim, relaunched after session 31's write
collision, landed clean this time — and the audit narrowed the row's own claim: the true
restatements of base rule 5 were just the tier ladder and the raw-output sentence (now one pointer);
everything else in the block is build-pipeline's pinned own delta, asserted by the needle tests,
and stays.

**Row 214** (8b72248, test-author 0.1.3, bp 0.2.47): the tlvphoto wish — "state the small-fix
red-first path" — answered the same night it arrived. The call: option (b) with red-first kept as
the default order at every size; a one-batch fix+test on a tiny reversible edit inside the skip
boundary is legal only when the batch closes with the mechanical red proof (restore the pre-change
file, run, watch the new rows fail, restore) named in the landing record. Why (b): the law's own
words already accept a red run "against the pre-change state", the field session's recovered proof
was exactly this protocol, and a written escape valve with a mandatory proof holds better under
time pressure than an order that already decayed once. M-205 pins the needle test, itself proven
red against the pre-change tree. The wish file moved inbox → docs/wishes; inbox is empty.

**Versions this session (A-7 line, old → new):** spec v0.16.19 → v0.16.21 · base 0.1.29 → 0.1.30 ·
communicator 0.1.42 → 0.1.43 · build-pipeline 0.2.45 → 0.2.47 · test-author 0.1.2 → 0.1.3; installed
copies synced at each landing. 22 commits ahead of origin.

**The teeth worked, twice.** The clock hook blocked a commit whose record stamped ~03:15 against a
03:12 wall clock — the stamp was reread and fixed (INV-24 doing its job). And the matrix id for the
new row was first picked off a too-narrow grep (M-200, already taken past M-199); the duplicate-id
test caught it at once and the row renumbered to M-205 — the traceability net catching its own
author.

**The register lesson continues, honestly.** This session's chat reused the exact calque session 31
was caught on («иголочные» for the needle tests) before the journal's own lesson was reread. The
hook now reminds every prompt and the lint blocks shown artifacts; live chat stays the weakest
surface and row 203's case file grows by one more sample.

## Session 32, the morning after (2026-07-10 ~09:16–09:22) — his three words landed

He read the night report and spoke three times. **The push grant**: «сам пуши! не надо меня ждать» —
recorded as a standing host-profile line the same minute; the push-law's grant question for this host
is answered, and the waiting-for-his-hand line retires. **The onboarding verdict**: v4 accepted with
one class fix — the page had hardcoded his personal setting values (Russian for chat, "Alexander" for
the name, a Russian-pinned example) as if the product prescribed them; his rule instead: conversation
follows whatever language the user writes, written work is always good English, the name is whatever
the user gives. Three spots fixed by a clean writer within the hour, lint green, page re-shown; the
BUILD gate is now open on the accepted mockup. **The migration**: goes today — his window plan stands
(tlvphoto windows execute, this window teaches and supervises); the audit-only amendment is now also
written into the host profile where the original line lives. README's Known-issues counts refreshed
at the push walk (style debt 62, redundancy candidates 11).

## Session 32, the morning build (2026-07-10 ~09:38–10:47) — the settings card lands, and the convergence principle is born

The last construction piece before 1.0 walked the whole pipeline in one morning. A worker inventoried
every setting the pack knows (14 keyed + the unkeyed founding answers); a clean writer drafted the
scenario ("Meeting your settings": the card at setup's end + the standing "what can I customize?"
answer, one catalog home, rules never personal values — his 09:16 law became INV-88); the prover's
seam pass found one real conflict (every-table-row vs the curated approved page) folded by the base
table's new Card column (visible/internal, base 0.1.31); architecture, five matrix rows, five tests
proven red before any code.

**Then the bounce that taught the day.** The first render shipped green and HE bounced it on sight:
an invented "yours today — yours to change" chip on every row, raw keys as headings ("Address",
"Trust commit"), the priority-ladder section stripped of its explaining example. A fresh-eyes check
found two more real defects under it: multi-line profile entries truncated at the first physical
line (raw markdown leaking into the shown page, a recorded project-kind value never reaching its
row), and only 4 of the norm's 7 sections rendered. Root cause, honestly named: the approved norm
was neither the template nor a test — it was held by my attention, and attention drifts at every
model tier. My own briefing skipped two written laws (build with the norm OPEN and the
plan-vs-prototype diff line; the verify walk against the norm side by side).

**The fix was convergence, not patching.** The frozen norm became the LITERAL template (the renderer
injects values into the approved file and can no longer invent markup); a norm-conformance test and
a multi-line/robustness test were proven red on the bounced render, then five tight worker rounds
closed them (v2 template rebuild · v3 example rules are data, replaced by the real host lines · v4
long lines elided · v5 no raw key ever a heading + unmatched personal entries collapse into one
counted summary row). The register lint BLOCKED one intermediate showing — his own profile's
no-calques rule quotes banned words, and the gate caught them on the card — the first live proof of
the INV-83 teeth catching their own author. Final: 286 green, lint clean, sections identical to the
norm by diff, shown and — his word pending on the look — landed.

**His words of the morning, all recorded as rows:** parallelism enters the architecture step's
checks (215, post-1.0) · a norm-pointered surface owes a conformance row (216) · the convergence
audit — every quality lock itself tested to hold — blocks 1.0 (217) · the convergence principle
enters the base rulebook: every process names its goal as an artifact and moves toward it, always;
a proxy never replaces the goal (218, his frame verbatim in my permanent memory) · every skill-kind
landing walks skill-creator's review, the classifier is the trigger (219) · audit 24h of the
tlvphoto exchanges first (220), then make his one-sentence migration start work, teach-only (221) ·
tests clean up after themselves, a matrix-template law — and our own new card tests are the first
caught leak (222).

Versions: spec v0.16.22 · base 0.1.31 · communicator 0.1.44 · VERSION 0.9.13; pins refreshed twice;
installed copies synced at every bump. Delegation carried the day: five clean-writer drafts, one
inventory worker, five renderer rounds and a fresh-eyes check — the senior wrote briefs, folded,
and gated.

## Session 32 — 1.0.0 (2026-07-10 ~11:30, his «поехали» at ~11:26)

The five-angle audit closed at ~11:21 (record: docs/prover/2026-07-10-m1-audit.md — zero must-fix,
every fold landed the same hour, three convergence locks newly held by red-proven tests) and he gave
the go five minutes later, with one release decision of his own: versions ALIGN at the major — the
pack, all eight skills, the spec header and the pins all read 1.0.0 from this moment (each skill
resumes its own patch rhythm from here; when else to align is row 231, his open half). Rows 173-187
archived whole to docs/queue-archive/2026-07-10-v1.0.0-milestone.md per the standing milestone note.
289 green on the aligned tree. What 1.0 means by his own bar, set 2026-07-09 and met: everything on
the run's list landed here, plus the docs pass; the two field items ride real windows next — the
cloud session, and the tlvphoto migration his one sentence will start. The morning's lesson rides
into the release: the day's laws (norm-conformance, convergence, cleanup, cross-cutting, mirror-ban,
CI-verdict) are queued post-1.0 by his word — the release is the floor they land on, not the ceiling.

## Session 33 — the catch-up walk lands, and the field gets two new neighbours read (2026-07-10 ~12:00–13:20)

**Row 221 — «подгрузи лайвспек и давай переверстывать документацию» now works.** The morning's dry
run of that sentence had found the guides wanting: the old MIGRATION.md was a single stale rename
note with a non-idempotent first step and no walk at all. The row went through the full pipeline.
The spec grew the catch-up section (F-catchup: the four-phase walk, the half-done-state law, the
preserve-and-re-home law, version-chained migration chapters, the before-and-after self-test with a
named restore point — A-11, INV-89..92), seven prover findings folded at review and his two midday
words folded as INV-91/INV-92 (docs/prover/2026-07-10-row221.md). Ten tests written and red-proven
against the pre-rewrite guides, then the guides themselves: MIGRATION.md rewritten whole as the
walk's operating guide with the 1.0.0 chapter absorbing the rename note idempotently (an opus
worker drafted to the needle contract, senior-validated); ADOPT.md gained the routing fork and THE
one canonical-document-set list; adoption.md and pair-adoption.md now point and route; the base
defaults table gained the `spec.file` row (internal). Verify-by-deed ran as two cold opus reads
role-playing the tlvphoto window, guides only. The first said NO and earned its keep: a real hole
(a commit-pin record has no readable version — where does the chapter chain start?) plus two weak
spots (the pair's blocked-verify tension; the machine-global loader sweep). All three folded the
same hour, the hole red-proven first by its own test. The second cold read: YES, zero holes, every
planted trap answered by a named clause. 268 green; VERSION 1.0.1 (spec header, base 1.0.1, seven
base pins, plugin.json — synced to the machine).

**The resume file shed its shipped history.** The 100-line cap caught NEXT_STEPS still carrying the
1.0 run's finished charter; the file was cut to the live state (66 lines), the history already in
these chapters — the cap did exactly what it was written for.

**The field read: Superpowers and gstack (his ~12:57 word, row 233's material pulled forward).**
Two source-verified research passes ran as parallel workers while the landing continued. The short
truth: Superpowers (obra, ~251k stars) is the field's strongest process discipline and its design
doc is a dated per-feature file closed at approval — process-centric by third-party reading, no
living spec, no invariants, no requirement-to-code trail; gstack (garrytan, ~121k stars since
March) is role-based review plus a Codex second opinion plus real-browser QA, and its /spec files a
GitHub issue whose archive stays local — third parties name the missing spec-anchoring outright.
The verdict he asked for: we are not late; the ground live-spec claims is still unoccupied, and
their execution discipline is the honest bar to cite. The README's why-section was first restored
whole (its own commit, the born-of incident of row 233's law), then extended with both frameworks
by the clean-writer road; the full sourced notes landed as
docs/research/2026-07-10-superpowers-gstack.md. One inbox wish carried the research to the promoter
(promoter-alexander/inbox/), for the campaign that will promote live-spec and product-prover.

**His words of the hour, registered:** managing one project's independent parallel lanes becomes
row 234 (this very session is the born-of example: the landing lane, the research lane, and the
hand-off ran at once); the all-projects migration order stands answered from the fleet survey —
tlvphoto pair first (his fire starts it), then track-coach, then the promoter family on his word,
then the playbook name sweep.

**Row 232 — the time-estimates law lands (~13:45, first of the law batch on his ~13:20 raise).**
Every ask now hears an honest time range at its echo, long work is explained up front in plain
steps, a long stretch occasionally says roughly how much remains, and the landing report settles
estimate against actual (INV-93; communicator rules 12/13/8; M-222 red-proven). His reminder from
the café was the second born-of case: the session gave ranges but no standing shape — now it is
law, not manners. Also this hour: rows 234 (parallel lanes) and 235 (the leave-command: «я ухожу»
winds down to a shutdown-safe stop and says «можно выключать») queued on his words; the playbook's
old-name sweep done and pushed (one annotation — the other mention was already correct history);
the cloud-seat facts fetched from the current docs for his browser-session question (same
subscription price, local and cloud; notes in the session trail).

**Row 237 — no line certifies its own sincerity (~13:57, his word at ~13:53, landed the same
hour).** The README's fresh lineage paragraph opened with "we say so plainly" and he called it:
when everything said is meant to be true, saying so distinguishes nothing — mention not-A only
where not-A was a live alternative. Now law (INV-94, beside the register-lint law): the spec
clause, the communicator's never-list, five caught phrases as lint patterns (floor 17→22), and
the README swept — four self-certifying phrasings rewritten to carry the fact instead ("published
in full", "reviewed at every push"). The same hour the clock hook blocked an invented ~13:58
stamp written at 13:49 — both catches recorded as the day's convergence proof: the locks bite.

**The originality audit (~14:16, his ~13:56 ask — inside the hour he gave).** Two passes: a
borrowings inventory (eighteen mechanisms adopted from named neighbours, every one traceable —
six credited in shipped text, twelve in the research docs and queue rows) and a verbatim scan
(seven shipped files against eleven neighbour documents, zero shared runs of eight or more words;
the scanner proven on a planted control first). Two findings, both closed the same hour: a dead
provenance pointer in guardrails/README.md repointed to the audit, and the rationalization table
he approved on 2026-07-05 turned out never built — re-queued as row 238 under the
never-drop-a-sound-thought law. The record: docs/research/2026-07-10-originality-audit.md, linked
from the README's why-section. Also this hour: the lineage paragraph redrafted by a clean writer
as a plain acknowledgment (his read on my in-session rewrites: they drift — the clean-writer road
now holds for every README touch), and row 222 grew its placement half (test files are born in a
temp home; the bouncing Downloads icon is the born-of, his ~14:11 word).

## Session 33 — the leave-command lands (2026-07-10 ~14:40–14:55)

Row 235, his ~13:30 word from the café: one spoken «я ухожу» must reach a point where the laptop
can close. The law landed as INV-95 with three homes — the spec clause beside the time-estimates
law, a leave-word rule in the communicator's narration family (next to the offline window, its
natural sibling: the window says when he MAY step away, the leave-word handles when he IS), and a
firing sentence on base checkpoint rule 6, which already owned every piece the walk needs (red
never committed, workers halted before sleep per the worker-liveness law). The WHY of the shape:
the walk invents nothing — it fires standing laws all at once and adds only the two things that
were missing: the minutes-to-safe first beat and the fenced closing line, said only when the whole
walk holds. The never side is the point: an early «можно выключать» that leaves a worker writing
into a sleeping machine is exactly the defect the law kills. Red-proven (5 fails on the pre-law
homes), then 311/311; traceability caught the unassigned anchor and the matrix row before any
human could — the teeth work. Poetic justice logged: the row was built inside the very 30-minute
café window it legislates, and its first real firing is expected within the hour.

## Session 34 — attribution and the honest shopfront (2026-07-10 ~16:27–~16:39)

Two of his words landed back to back. The made-with attribution (row 244, INV-96): every artifact
built with the method says so — one standard line, "made with live-spec" linking to the pack repo,
its wording living once in the publish skill's shared floor, checked at every publish like any
floor item. The WHY of the shape: the floor already demanded "attribution state explicit", so the
law sharpens an existing item instead of growing a second checklist; and the pack keeps its hands
off foreign trees — track-coach got the first application wish in its inbox, the rest follow
through their own queues. Distribution rides every future publication for free — his monetization
lever, wired into the gate that cannot be skipped. Before that, row 245: the web session's curator
read held — the README's opening claimed executable gates wider than a host's out-of-box truth.
The fix went truth-first: the opening now says the eight git-wired checks gate THIS repo (they
blocked two commits the same day — the claim is deed-backed), while a host's four checks ship as
specifications until the runnable versions land (row 241, already first major movement). Clean
writer wrote the paragraph, the register lint passed it. The catalog submission waits for 241 —
narrow the promise to the truth today, widen the truth to the promise in code next.

## Session 34 — the gates go runnable, and the cloud passes its first exam (2026-07-10 ~16:50–~17:38)

Row 241 landed its first leg end to end, split exactly along the method's seam: the head here
(the contract clause, the architecture assignment, the matrix contract row, the self-contained
brief), the hands in a CLOUD session Alexander fired himself — the first real cloud worker in
the project's history. The worker held the whole contract without a reminder: red-first as two
separate commits (22 recorded failures before any check code), the write-set exact to the file,
the checkpoint force-added past the gitignore so the evidence survived, and an environmental
caveat documented with a clean-main reproduction instead of hand-waving — the two container
reds trace to a machine-local architecture pin, not to its work. Integration verified by deed:
my own planted defect (an invented rendered section) went red with the right typed line before
any merge was trusted. Then the pack ate its own cooking: SURFACES.md + guardrails.config.json
written, and the attach walk's first real catch came at home — a bare-heading needle flagged as
empty content, the registry corrected, the check stood its ground. The four checks now run as
pre-push gate h on every push of this repo. The README's morning boundary sentence retired the
same hour by the clean writer, the Known-issues line with it: the promise and the truth
converged from both sides in one day. WHY it matters beyond the row: the moat claim — everyone
else enforces by prompt text, we enforce by executable gates — is now attachable by any host in
fifteen minutes, which is what the catalog submission was waiting for. Open leg: one external
host attaches (track-coach's catch-up is the natural first).

## Session 34 — the evening close: two clouds fly, the machine sleeps safe (2026-07-10 ~18:02)

The day ends with the seam between seats settled and USED: two cloud sessions run without this
machine — tlvphotos rewrites its spec into plain language on its own branch, and a manual cloud
order refreshes the standalone prover repo's shopfront (row 246, branch row246-shopfront) —
while every local lane sits committed and pushed. The attribution line grew his version idea the
same hour it was asked (1.0.9): the made-with line now names the pack version the project runs,
so adoption reads off the shopfronts themselves. The cloud facts were settled by experiment, not
belief: two probes proved a remote request from a terminal falls back local, so firing clouds is
the owner's browser act, and the brief-in-repo (or brief-in-prompt) pattern bridges the seam.
The first real leave-walk of the leave-command law closes this chapter: workers halted, lanes at
their checkpoints, the closing line said — the law born at 14:40 fired for real the same evening.

## Session 35 — the two clouds come home, and one of them brings a hole (2026-07-11 ~21:27–~22:05)

Both evening branches collected, and the second changed the day's shape. The prover-shopfront
branch (row 246) was verified by deed and SUPERSEDED rather than merged: the mirror's own README
banner names sync-mirrors.sh as the one write channel, so the cloud's two fixes were landed in
the PACK and the script itself learned to stamp the made-with line from the live VERSION file —
a hand-written mirror footer would carry an invented number and be wiped by the next rsync (the
class fixed, not the point: every future mirror now gets the line for free). A fresh-context
prover pass on the delta returned zero must-fix and three findings, all folded the same hour:
the self-mirror sentence into the attribution clause, a floor-lockstep drift guard, a dead-branch
comment (INV-96, M-225). The mirror now stands byte-identical to canon plus footer.

The second branch was the one Alexander had to point at twice — gate-check-protocol, from his
"Gate push blocker verification" cloud window. Yesterday's record said the external check PASSED;
the truth is there were TWO probes. The first (~18:18, three planted desyncs at the check level)
did pass clean and its record was honest. The second — four real pushes through the installed
hook against a decoy remote — landed its protocol at 18:34, two minutes after the leave-walk's
last resume commit, and was never collected: Tests 0–2 held physically, and Test 3's invented
rendered surface sailed through GREEN, because the pack's own guardrails.config.json left
surface_discovery_pattern null and thereby disarmed the one branch of the completeness check
that looks from the rendered content back to the registry. The machinery was sound; the first
host never armed it on itself. Fixed the same hour and proven live in both directions: the
pattern set, the analyst's exact planted break now turns the gate red with the typed line, the
clean tree stays green, and a lock test keeps the pattern armed forever (red-proven on the
nulled config — M-226; the protocol collected as its own record beside the first probe's,
docs/prover/2026-07-10-external-push-probe.md). Row 251 closed in the same motion: the attach
walk now OPENS with the config step and names the pre-config red as by-design, and the fresh
FULL clone re-ran the whole suite 319/319 green, retiring the analyst's shallow-clone caveat.
WHY it matters: the moat claim survived a real outside attack twice — but only the collected
protocol, not the optimistic summary, told the whole truth. A cloud branch is not integrated
until its file is ON main and read to the end.

## Session 36 — the night the method got its teeth into its own keeper (2026-07-11 ~22:51 – 2026-07-12 ~01:28)

Sixteen rows in one night, and the real story is HOW the last ten landed. The session started
conventionally: the senior read anchors, wrote briefs, a sonnet worker applied (rows 248, 249, 218,
219, 222, 223 — the detached-work visibility cadence, the no-scissors reminder, the convergence
principle into the base rulebook and the playbook's opening chapter, skill-creator review bound to
every skill-kind landing by the classifier, test hygiene with the suite's own leak check, the
declared cross-cutting laws with a clean 33-cell first station run). Alexander watched the token
meter and asked the two questions that reshaped the rest: why does the orchestrator do delegable
work itself when the rules say otherwise, and why do those rules live in files read once. The
answers landed as rows the same hour: the routing reminder joined the chat hook (253), the
delegation line became a suite-checked queue fact (254), the drafter-applier overlap became
pipeline law (255), and the general cure — a twice-broken behavioural rule earns a live channel
that moment — became base rule 23 (256). From row 224 on, Opus drafters prepared each next row's
exact strings while sonnet appliers landed the current one; the orchestrator's own hands touched
only briefs, acceptance, and pushes. His grants moved the harness itself: hooks and installs by
the agent's hand (trust.self-install, ~23:30), the next orchestrator session pinned to Opus
(~00:31, settings.local.json + the loader line), the 1.1.0 bump on the agent's own certification
if the audit runs clean (~00:35). Also landed mid-batch: the voiced-fix tripwire (225), one
canonical state dir + worktree isolation on overlap (227), the CI verdict as the session's own
immediate bug (228), landings close their checkpoints (226 — six of the night's own checkpoints
swept closed as the law's first deed). Two rows were caught by drafters' reads before wasting a
landing: 231 split (its core half waits his word on alignment moments), 234 routed to the full
pipeline as a five-story surface. Drafts for 233/239/240 wait on disk under checkpoints/. The
worker fleet: five opus drafters, ten sonnet appliers, two extraction hands — every landing's
delegation line is in its queue row, as the new law demands.

## Session 37 — the audit that shipped 1.1.0 (2026-07-12 ~01:30 – ~04:27)

The Fable seat opened on a /loop word: work NEXT_STEPS to empty, delegate everything, standing
push grant. Session 36's mode carried the whole night unchanged — opus drafts, sonnet applies,
the orchestrator briefs and accepts — and the queue emptied through it. The pending drafts
landed first: row 233 stopped the moment the formal-index density test met the INV-109/M-247
reservation (a reserved number and a dense index cannot coexist; the orchestrator lifted the
reservation, codes now consume in landing order, 233 renumbered to INV-109/M-247), then 239/240,
then 242 — whose prose came from a fresh clean writer and whose landing gate h correctly blocked
until the paragraph got its M-250 string pin. Row 250 closed as a duplicate of row 223 by an
opus analysis with no build. Row 247 landed the inbox remote arm with one orchestrator call (the
stable settings path over the session-scoped installation URL) and one leg left honestly open —
the first real remote deposit is Alexander's browser click, never self-certified. The inbox
swept three wishes into rows 257-260, among them Alexander's live design-principles wish (entry
impact analysis over spec+architecture+code, footprint-proportional routing, per-project-kind
process modularity, tests as part of the set, periodic compaction) — a deep-thinking architect
drafted the fourteen-principle set (P0-P12), rendered to his browser for comments. Rows 257/258
landed after both drafts missed the same ARCHITECTURE.md owning-node edit — the applier's
red-first pass caught each, and the twice-seen class became row 263 (a standing self-verify list
for drafter briefs). Row 260 split into 260a/260b as the bundle it was.

Then the 1.1.0 audit ran end-to-end by delegation: the full prover pass (0 must-fix; its three
should-fixes folded the same hour with a ratchet test pinning the index's Section column), the
minor-gate walk, the once-read-rules sweep (clean), the delegation de-dup (7 duplicate clusters,
3 divergences between playbook and pack — row 262, his word owed), the composition walk — whose
one must-fix was the method catching its own contradiction: M-6 ordered a prover re-check before
every push while the hours-old INV-112 ordered a remote seat to push an inbox file with no
prover; the inbox-only carve-out plus three scope clauses landed before the gate — the skill
evals re-run (7/7 green on fresh behavioural arms), the skill-creator craft sweep (zero
must-fix), the first code compaction pass (the shared test-read helpers extracted to
tests/conftest.py, 36 copies deleted, same 422 green), and the deferred-trigger rescan (row 192
fired, row 260's premise died). 1.1.0 shipped on the standing grant: single push, CI read green,
installed copies and mirrors synced (over the night: build-pipeline 1.0.5→1.0.10, communicator
1.0.3→1.0.4, product-prover 1.0.1→1.0.3 — the A-7 lines). Skill/pin version alignment stayed
deliberately open per row 231's half that waits his word.

WHY it matters: the whole MINOR audit — five judgment passes, three fix batches, a bump — ran
with the orchestrator's hands touching only briefs, acceptances, and two design calls; and the
method caught its own drafts three times (index density, owning node twice) plus its own
push-law contradiction the same night the conflicting law was born, before the first remote
seat could ever hit it.

## 2026-07-12 (session 39) — the buildable smalls backlog cleared: eleven rows, three new invariants

**What:** eleven queued smalls landed in one serial-by-the-graph batch (the rows all collided on the
shared spec/matrix/architecture, so parallelism bought nothing — INV-49's own "tiny rows ride serial"
verdict, said aloud). In landing order: 263 (the drafter self-verify list made durable in the
drafter-applier law — index density, owning node, matrix-under-owner), 273 (the `architecture → prove`
seam row + the Prover-record table's append-duty and catch-up), 269 (the CI prover-freshness script's
inbox-only carve-out, mirroring M-6's prose so an inbox deposit on a recordless day no longer reds CI),
264 (behavioural-rule breaks route to one home, PROBLEMS.md, with the routing/delegation break logged
there and rows 253/254/256 pointing back), 265 (the derived-doc header version policy — no frozen
spec-version, point at VERSION, a dated Last-reconciled line; both headers reconciled), 266 (the
communicator writing register extracted to `references/writing-register.md`, 679→565 lines), 267
(spec-author judged INV-39's three statements KEEP-ALL-THREE, derived from the spec's own compaction
clause that names it as the canonical reinforcement example), 268 (eval-craft: S1 a dated decision that
the plain-words form of INV-27 is acceptable, S2 a delegation-forcing scenario variant, N1 the risen
bare-arm floors folded), 270 (derive-from-a-proven-artifact-before-a-fork, the read-the-doc twin of
ask-never-guess, INV-121), 260a (the three-question node fitness test, INV-122), 260b (compaction as a
scheduled station for code as well as docs with its second trigger, INV-123).

**New invariants:** INV-121 (derive-before-fork), INV-122 (node fitness test), INV-123 (code compaction),
matrix rows M-261..M-264. INV-108 edited (one-home for behavioural breaks). Skills: live-spec-base 1.0.6
(all seven working skills re-pinned to it), build-pipeline 1.0.14, product-prover 1.0.3, communicator
1.0.5, spec-author 1.0.3. Delta-scoped prover pass, 0 must-fix (docs/prover/2026-07-12-s39-backlog-batch.md).
Suite 490 green.

**WHY it matters:** the backlog of "no owner word needed" smalls is the debt that quietly accretes between
milestones; clearing it in one batch keeps the pack's own spec honest before the next feature movement
(row 259, still blocked on his design-principles comments). Two of the rows are his own design-principles
wish made real — the fitness test (P7) and the code-compaction station (P4-6) — so the pack now gates its
own abstractions the way he asked, and the derive-before-fork law (born of a track-coach fork he corrected)
is the discipline this very session ran on: rows 265 and 267 were both DERIVED from existing artifacts
rather than forked to him.

**Three honestly-flagged forward legs** (INV-26, restated in the resume file): row 266's "under ~500" is
arithmetically unreachable by the register extraction alone (the 22-rules core is ~423 lines) — an owner
call owed; row 270's leg 3 (row 259 cites INV-121) is wired into 259's Done-when; row 260b's first real
code-compaction pass fires at the next milestone audit (the 1.1.0 audit already ran at s37).

**Not yet pushed** — the batch is committed locally and the prover record clears the push gate, but the
eleven-row batch waits on his OK before it goes to main.

## 2026-07-12 (session 40) — a confirmed bug drives a class hunt before it closes (row 281, INV-124)

**The wish.** From the tlvphotos window: Alexander's standing frustration that friends' bugs cluster in
roughly the same district of the product, visit after visit, because each report gets its one instance
fixed and the siblings right next to it are left standing — so the next friend trips over the next one. A
point fix looks done and is not; the class is never swept. His instruction: when one bug is caught, look
for ALL the look-alikes, look at the architecture, check the specs, and talk to the human when the class
boundary needs a read.

**What landed.** A new invariant, INV-124: a confirmed bug is not closed on its single instance; before it
is called done the method drives four moves — (1) name the defect abstractly and actively SEARCH every
surface for the un-seen siblings, fixing all in the same change; (2) check the architecture for a
structural cause (a boundary drawn wrong or left silent) and update ARCHITECTURE.md when there is one; (3)
check the spec — a spec silent on or under-describing the broken behaviour is the real defect, fixed first
so the prover can flag it, then the code lands under it; (4) escalate to the human when the class boundary
needs his read. The four moves are the bug door's close condition, so a point fix that leaves the siblings
standing is a status, never a landing (INV-26).

**Where it lives.** Four homes, one fact each: the F-bug spec clause + Formal-index row (INV-124);
build-pipeline's bug entry (the four moves at the bug door, v1.0.15); product-prover's class lens (the
former "Sibling instances" lens widened from the document sweep to the three questions — same kind
elsewhere · architecture accounts for it · spec describes it — v1.0.4); and base rule 14, sharpened from
"fix the class you already see" to "go FIND the class not yet seen" plus the escalate line (live-spec-base
v1.0.7, all working-skill base-version pins lockstepped). This is the wish's own worked example turned into
law: the exhibition's pinch-zoom bug, where naming the class — a browser zoom desyncing the scroll animator,
guarded on only some gestures — turned one report into five live siblings, all real and all fixed together.

**Why base rule 14 needed the sharpening.** The old rule already said "search the whole repo and every
surface," so move 1 was partly present — but it read as sweeping the class you already recognise. The wish
asked for the active hunt: name the KIND abstractly and go looking for the siblings you have NOT seen yet.
The three added moves (architecture, spec, escalate) were genuinely new: the architecture check catches a
structural cause a code fix would paper over; the spec check generalizes the spec-under-describes-composition
lesson (a prover cannot catch what the spec never states) to every bug; the escalate line names when to
stop and ask rather than guess the class boundary.

**Method notes.** Door: feature; kind: skill. Red-first proven — `tests/test_class_hunt.py` (7 assertions)
written against the pre-delta repo tree, run RED (the repo skill copies and M-265 lacked the strings), then
green after the four homes + matrix + owns-list landed. Suite 497 green (490 + 7). Prover cross-link short
form (INV-61, small skill-kind delta): 0 must-fix — `docs/prover/2026-07-12-s40-inv124-class-hunt.md`.
Delegation: none — a law edit spanning eight homes with cross-reference precision (Formal index, owning
node, matrix row under owner); routing override logged (mechanical by tier, senior-held for the pack-tree
git-contamination risk + the eight-home precision, as rows 260b/270). SPEC v1.1.1, pack 1.1.1.

## 2026-07-12 (session 40) — cross-surface policy uniformity (row 287, INV-125), the preventive twin

**The wish.** From the tlvphotos window, during a phone test: a gesture policy — "browser pinch-zoom is
refused" — was decided and shipped, but the clause and the code wrote it for the walk alone. The door, the
series side-room, and the polaroid table kept the browser default, so pinch still zoomed there. Every test
was green (the suite asserted the one surface the clause named), the spec read fine (each surface described
on its own), and the gap surfaced only when Alexander pinched each surface by hand on a real phone. A policy
uniform in intent, non-uniform in fact, and nothing caught it. His steer: let the prover write itself a
check — or let live-spec decide the best mechanism.

**What landed.** INV-125: when a decision governs a KIND that recurs across sibling surfaces or elements,
the spec states it once at the surface-CLASS level (the clause names the class and enumerates its members),
and a policy written for one surface while siblings of the same kind exist is a spec defect. Three
enforcement faces, following his (1)+(3) lean and the derive-from-his-steer read: the spec-class rule is the
upstream root; the product-prover carries the cross-surface-policy lens (enumerate the surfaces of that kind
from the surface registry, flag any the clause does not cover — the check he asked the prover to write for
itself); and a rendered product's completeness guardrail asserts the policy DOM-wide, red until every
sibling root carries it, so the walk-only fix goes red the day it lands rather than under a thumb on a real
device. The pack itself has no DOM, so it ships the rule and the lens and leaves the DOM-wide assertion to
the products it serves.

**Broadened the same landing.** Mid-work he clarified that uniformity is not only spatial (a policy across
sibling surfaces) but also covers repeating state transitions (the same open/close animation on every card)
and features / repeated elements shared across places (a filter, a caption, a control that should look and
behave alike everywhere). The clause and index now name all three, and state plainly that consistency of
this kind is itself an invariant — the thing that must hold the same across a class of similar surfaces,
transitions, and elements.

**Where it sits in the family.** INV-125 is the preventive twin of INV-124 (the class hunt): the class hunt
sweeps the siblings once a bug is confirmed, this holds the policy uniform before a bug is ever filed. It is
the class-level companion of INV-72 (the unwritten-seam hunt asks whether a surface's behaviour is stated
while a sibling is present; INV-125 asks whether a decided policy holds across the whole class). Homes: the
composition clause, product-prover's lens (beside the unwritten-seams lens), build-pipeline's completeness
guardrail. Owned by the product-prover node (owns-list + M-266).

**Method notes.** Door: feature; kind: skill. Red-first — `tests/test_cross_surface_policy.py` (6
assertions) red against the pre-delta tree, then green. Suite 503 green. Prover short form (INV-61): 0
must-fix. Delegation: none — a law across three skill homes + spec + matrix + owns-list, senior inline. SPEC
v1.1.2, product-prover 1.0.5, build-pipeline 1.0.16, pack 1.1.2.

## 2026-07-12 (session 40) — paired-transition symmetry (row 288, INV-126), the temporal twin

**The wish.** From the tlvphotos window, another phone test: opening the polaroid side-room plays a soft
transition — the room dresses under a black veil and is revealed in one breath — but closing it is a hard
cut, one click and gone, no transition at all. The way in and the way out of the same surface do not match,
and nobody decided that on purpose: the entry got the crafted breath, the exit was left instant. A soft way
in with a hard way out, passing every test (the exit "works" — the room does close), reading fine in the
spec (each direction described on its own), caught only by a human feeling the asymmetry on a real device.

**What landed.** INV-126: when a surface has a pair of opposite state changes (open/close, enter/exit,
expand/collapse, show/hide), a transition crafted for one direction is a decision about the pair, so the
other direction is stated too. The default is symmetry — the exit mirrors the enter's feel unless a reason
is written — and a shorter or deliberately-instant exit is a valid STATED answer rather than a silence. It
rides the standard-facet sweep as its own facet (his option 2, the cheapest true home, plus option 3's
default-and-ask as the resolution). Because motion feel is the human's own gate (INV-30), an undecidable
pair is surfaced to him rather than shipping a crafted-in and instant-out pair silently. The prover flags a
pair with one direction's transition described and the opposite unstated.

**The family, now three deep.** These three landings are one wish-family from his phone test, all about a
decision made for one member of a set and silently not carried to the rest: INV-124 (the class hunt — sweep
the siblings of a confirmed bug), INV-125 (cross-surface uniformity — hold a policy the same across sibling
surfaces in space), and INV-126 (paired-transition symmetry — hold a transition the same across the two
directions of one change in time). INV-125 and INV-126 are spatial and temporal twins; INV-124 is the
reactive cousin that fires once a bug is already filed.

**Method notes.** Door: feature; kind: skill. Red-first — `tests/test_paired_transition.py` (6 assertions)
red against the pre-delta tree, then green. Suite 509 green. Prover short form (INV-61): 0 must-fix. The new
facet joins spec-author's canonical list carrying its named incident, satisfying the curated-list rule.
Delegation: none — a law across spec + facet list + prover + matrix + owns-list, senior inline. SPEC v1.1.3,
spec-author 1.0.4, product-prover 1.0.6, pack 1.1.3.

## 2026-07-12 (session 40) — scenario entry/exit contracts (row 192 → 289, INV-127)

**The wish, revived.** Alexander asked for this on 2026-07-09 late evening — the prover should say, where
needed, which preconditions and postconditions hold, how a scenario is ENTERED and how it is EXITED (his
tlvphoto example: how we exit scenarios, how we enter). He called it "большая тема" and deferred it with a
recorded revisit trigger: the next prover-method landing. Today's INV-125 and INV-126 both touched the
prover, so the trigger fired; on his word this session, it was built.

**What landed.** INV-127: a person-facing scenario is a flow with edges. It states how the walk ARRIVES —
from which prior scenario or state, with what already true (the preconditions) — and how it LEAVES — to
where the person lands, and what it leaves true for the next scenario (the postcondition). This lifts the
per-operation precondition and postcondition lenses (already in the prover's phase-3 list) to the SCENARIO
level. It is kin of the entry-symmetry lens (INV-50, which asks a conditionally-entered face for its
re-entry path) and the runtime view's flow walks (INV-74, which trace a flow through the nodes). The prover
carries the scenario-level lens; a flow whose entry or exit is unstated is a finding.

**Bounded, not a retrofit.** The row was tagged "large" because it could mean writing entry/exit on every
scenario in the spec. The LAW is bounded: it binds forward (INV-15). A new scenario states its edges from
the first draft; the prover flags an existing scenario's silent edge as a finding rather than blocking the
lane on a backlog older scenarios never wrote. So the large theme landed as a bounded skill-kind law.

**Validated on one real spec.** The pack's own F-bug scenario ("When a bug cuts the line") already states an
explicit Precondition and Postcondition — the convention grounded in a working example — while other
scenarios leave their edges implicit, exactly the gaps the new lens flags.

**Method notes.** Door: feature; kind: skill. Red-first — `tests/test_scenario_entry_exit.py` (6
assertions) red against the pre-delta tree, then green. Suite 515 green. Prover short form (INV-61): 0
must-fix. Owned by the spec-author node (M-268); the prover lens is wiring, as with INV-50. Delegation:
none — a law across spec + spec-author + prover + matrix + owns-list, senior inline. SPEC v1.1.4,
spec-author 1.0.5, product-prover 1.0.7, pack 1.1.4.

## 2026-07-12 (session 40) — the entry impact-analysis station (row 259, INV-128), Fable-audited

**The wish.** Alexander live 2026-07-12: every incoming request gets an entry analysis reading the spec AND
the architecture AND the code together; presentation-only, single-module, and cross-cutting are three kinds
of work; the footprint is named before any work starts and decides the route. The fourteen-principle
architect draft (P0-P12) worked it out; row 259 is the entry station (P1-P6). His word this session: build
on the draft as accepted, then a Fable audit and the prover, then his review — later softened to "you
handle it" once the audit proved it could catch what a self-review misses.

**What landed.** INV-128: beside the door (which steps run) and the work-kind (what form each step takes), a
THIRD dimension is read at intake — the FOOTPRINT, read from three sources at once (spec · architecture ·
code), producing one named footprint (presentation-only · single-module · cross-cutting), spoken in the
capture echo and written in the row's `footprint:` note. The footprint COMPOSES with the door and never
overrides it: the door picks the steps, the footprint sizes how far each step reaches, and a feature never
skips the spec step whatever its footprint. A source disagreement is a finding routed to its owner (a bug
row, a spec fix, a restructure row); the three-source read is the verdict the derive-before-fork rule
(INV-121) rests on — which closes row 270's leg 3. The footprint re-classifies mid-work, the sibling of the
door's mid-work re-fire. And the station carries the boundary-health law in ARCHITECTURE: a right boundary
keeps a typical request in one node, repeated cross-cuts on the same node pair being the signal to move a
boundary through the architecture step. Homes: the intake clause + Formal index, build-pipeline step zero,
ARCHITECTURE's boundary-health law, product-prover's three-source lens, communicator's capture echo (grown
with the work-kind and footprint fields). Owned by the build-pipeline node (M-269).

**The Fable audit earned its keep — the case for auditing always.** I built this myself and my own prover
pass read it clean (0 must-fix). A fresh Fable context, adversarial hypothesis "goal missed", primary
sources only, caught a real contradiction my own review shared the blind spot on: the single-module road as
first written let a feature enter at the matrix step, silently skipping the spec step the door law forbids
(INV-16). It also caught the docs-only/skip widening asserted only inside INV-128 (a one-fact-two-homes
divergence), the omitted interface-test deferral, and the missing work-kind field in the echo. All folded
before landing. Alexander's read: a self-review shares the author's blind spot, so the adversarial audit
should be a standing station with a broadened trigger, not the senior's option — its own row next.

**Dogfood.** Row 259's own landing is the law's first act, and it obeys the law: its footprint is
cross-cutting (five homes across the method), recorded in the row's `footprint:` note, held through the
landing with no re-classification.

**Method notes.** Door: feature; kind: skill; footprint: cross-cutting. Red-first —
`tests/test_impact_analysis_entry.py` (10 assertions) red against the pre-delta tree, then green. Suite 525
green. Prover record with the Fable fold: docs/prover/2026-07-12-s40-inv128-entry-impact-analysis.md. SPEC
v1.1.5, build-pipeline 1.0.17, product-prover 1.0.8, communicator 1.0.6, pack 1.1.5. The deeper mechanical
enforcement (footprint-note check, per-kind layers declaration, interface-test machinery, cross-cut counter)
rides the architect draft's follow-on rows R0/R1/R3/R5.

## 2026-07-12 (session 40) — the adversarial audit becomes a standing station (row 290, INV-46 broadened)

**The wish.** After the Fable audit of row 259 caught a real contradiction with the door law that my own
author's prover pass had read clean, Alexander's live word: as you see, an audit is always needed — think
how best to write it in and at what stages. The lesson stared back: a self-review shares the author's blind
spot, so the fresh-context audit cannot be the senior's option exactly where it is most needed.

**What landed.** INV-46's mandatory trigger broadens. It was mandatory only when the code step was delegated
AND the delta was surface-sized. It fires mandatory now when the change is high-stakes AND its only review
is the author's own. High-stakes means surface-sized, or a change to the method itself — a rule whose
meaning changed (a wording-only edit that changes no meaning is not a method edit). The author's own review
means no independent read has happened, where an independent read is a differently-contexted head briefed
from the primary sources on the goal-missed hypothesis; a prover pass in the author's own context never
counts, and delegation never makes the review independent. One fresh checker per landing batch covers the
batch. A sharpening in place — no new invariant code, since the trigger's one home is INV-46.

**Dogfood — the audit of the audit-law fixed the audit-law.** This change edits a method invariant, so by
its own new rule it owed a fresh audit. A Fable pass ran and caught a must-fix I would have shipped: a
pre-existing briefing phrase, "primary sources only, apart from the worker's summary or your own plan",
reads as its own opposite ("apart from" as "besides") and its own test pinned the broken string green. It
also caught two definitional gaps in my first draft of the trigger — no proportionality floor (a one-word
invariant tweak would have forced a spawned worker) and a case that both leaked and swallowed (in normal
solo mode every landing is self-built, so "the only reviewer is the author" made the audit near-universal).
The high-stakes-AND-author-only redesign, the meaning-change threshold, the one-checker-per-batch rule, and
the defined "independent read" fold all three. The very first instance of the broadened law obeyed the
broadened law.

**Method notes.** Door: refactor; kind: skill; footprint: single-module (INV-46's own homes). Red-first —
the extended `test_adversarial_verify_option` red against the pre-delta build-pipeline copy then green; suite
525 green. Prover record with the Fable fold:
docs/prover/2026-07-12-s40-inv46-audit-trigger-broadened.md. A register-lint catch on a shout-cap in the
spec prose ("MEANING") was fixed the same landing. SPEC v1.1.6, build-pipeline 1.0.18, pack 1.1.6.

## 2026-07-12 (session 40) — deferred-row revisit at every queue-take (row 282, INV-129, prover F3)

**What.** Prover finding F3: a deferred queue row carries a revisit trigger, and a time-bound one ("before
the next release", "when the campaign ships") can come true and lapse in the gap between two milestone
gates — the milestone re-scan [M-1] was the trigger's only reader, so the promise that no deferred row waits
on a trigger nobody reads [INV-1] held only at milestone cadence. The fix names a second reader: at every
queue-take the session re-scans each deferred row's revisit trigger against the current moment, and a fired
trigger returns its row to the runnable head [INV-49] right then. The two cadences read the same triggers by
the same rule, whichever comes first.

**Why the taste fork went this way.** The finding offered two arms — add the queue-take cadence, or restrict
the trigger vocabulary to milestone-safe conditions. A queue-cadence reader is strictly the more capable of
the two (it keeps free-form, human-worded triggers working while closing the window), so restricting the
vocabulary would have been a narrowing with no gain once the reader runs often enough. Chose the added
cadence; the vocabulary stays free-form, noted in the clause.

**Homes.** New invariant INV-129 (the queue-take clause is its home, beside the graph-picks-lanes paragraph),
its Formal-index row, the build-pipeline queue-take walk (v1.0.19), and matrix M-270 under the build-pipeline
block. Red-first: `test_deferred_revisit_cadence` (four assertions) red against the pre-delta tree, then
green; full suite 529 green. Door: feature; kind: skill; footprint: single-module (the build-pipeline node).
Delegation: none — the delta is judgment-dense wiring across spec, index, architecture, matrix, and skill on
one node; proposed senior / chosen senior. SPEC v1.1.6, build-pipeline 1.0.19, pack 1.1.6.

## 2026-07-12 (session 40) — a withdrawn decision converges after two withdrawals (row 285, INV-130, prover F6)

**What.** Prover finding F6: an answered question closes forever [INV-59], but a withdrawn decision re-asked
"in plainer terms" [INV-9] with no cap of its own, so a genuine taste call could loop unbounded. INV-130
bounds it: on the second withdrawal of the same decision the session takes the recommended option and
surfaces it as a `[default]` on the landing report — silence stays consent from there [INV-31], never
re-asked. It is the same convergence an answered question already has, now given to the withdrawal path. A
later real change of mind rides the ordinary channel as a new wish, never a reopening of the closed decision.

**Why the bound is two, and why it does not run over the human.** The finding proposed N=2, and two is the
natural bound: the first ask, one re-ask "in plainer terms", and if the second phrasing still bounces the
question is not going to resolve by re-wording — a genuine taste call. INV-9 (the human owns the decision) is
bounded, not overridden: the converged pick carries only as a tweakable `[default]`, which is exactly
INV-31's silence-is-consent contract, so the human still has the last word without the loop.

**Homes.** New invariant INV-130 (the decision-page clause is its home, in the E-22 block), its Formal-index
row, communicator's rule 10 (v1.0.7 — counts withdrawals from the decision archive's answered-then-withdrawn
log), and matrix M-271 under the communicator block. Red-first: `test_withdrawal_convergence` (4 assertions)
red against the pre-delta tree, then green; full suite 533 green. Door: feature; kind: skill; footprint:
single-module (communicator node). Delegation: none — judgment-dense wiring across spec, index, architecture,
matrix, and skill on one node; proposed senior / chosen senior. SPEC v1.1.6, communicator 1.0.7, pack 1.1.6.

## 2026-07-12 (session 40) — a mid-work re-door rebuilds the independence graph (row 286, INV-131, prover F7)

**What.** Prover finding F7: a lane re-doored to feature mid-work [INV-16] can create a surface overlapping a
rolling sibling, but the parallel-lanes independence graph [INV-49] was not rebuilt, so the departures board
kept saying "independent" after it stopped being true. INV-131 makes the same mid-work re-check re-run the
independence edges against every rolling lane; a new edge pulls the re-doored lane back to serial (waiting
behind the lane it now shares a surface with) with a board line, so the board never asserts a stale
independence after the ground moved.

**Why this is an observability fix, not a new safety net.** The integration re-fence [INV-39] already caught
such a collision at landing, so correctness was never at risk — the gap was that the board lied between the
re-door and the landing. The clause is honest about this: it closes the observability gap (the board tells
the truth the moment the edge appears, not only when two landings collide), and it does NOT introduce an
automatic independence checker — the spec's existing "the senior judges independence and says so aloud" line
stands, the re-door named only as the moment that judgement is owed again.

**Homes.** New invariant INV-131 (the mid-work re-door clause is its home, in the door section), its
Formal-index row, build-pipeline's door re-fire (v1.0.20), and matrix M-272 under the build-pipeline block.
Red-first: `test_redoor_independence_rebuild` (4 assertions) red against the pre-delta tree, then green; full
suite 537 green. Door: feature; kind: skill; footprint: single-module (build-pipeline node). Delegation:
none — judgment-dense wiring across spec, index, architecture, matrix, and skill on one node; proposed
senior / chosen senior. SPEC v1.1.6, build-pipeline 1.0.20, pack 1.1.6.

## 2026-07-12 (session 40) — every scenario heading carries its tag, untagged is red (row 283, INV-132, prover F4)

**What.** Prover finding F4: INV-73's reverse direction ("every scenario carries its tag") was not
mechanically enforceable as written — the checker could not tell an untagged NEW scenario from a
legitimately-untagged machinery, rules, or reference section, so an untagged scenario could ship green and
uncovered. INV-132 adds a heading convention: every H3 heading in PRODUCT_SPEC.md carries either its
`[feature: F-x]` tag (a person-facing scenario the coverage table maps) or the explicit `[not a scenario]`
marker (a machinery/rules/reference section, legitimately untagged). An H3 carrying neither is unambiguously
red, so a forgotten scenario tag can no longer ship uncovered.

**The taste call — the marker.** The finding offered two arms: require every H3 under a person-facing parent
to carry a tag, or mark the non-scenario sections explicitly. A parent-based rule fails here because the
build-loop H2 mixes scenario H3s (Throwing a wish, Publishing) with machinery H3s (The rhythm, From the spec
to the tests), so "under a person-facing parent" has no clean boundary. The explicit marker is the robust
choice: one `[not a scenario]` marker on the 10 machinery/rules/reference H3s, and the rule becomes
spec-wide and unambiguous. Chose `[not a scenario]` as the marker word — plainly true of every one of them
(machinery, rules, reference), greppable, and carrying no anchor token so the Formal-index and split parsers
are unaffected.

**Homes.** New invariant INV-132 (the feature-coverage clause is its home), its Formal-index row, spec-author
(v1.0.6 — states the convention beside the tag law), the 10 marked headings, and matrix M-273 under the
guardrails block. Red-first: `test_scenario_heading_tag` — the mechanical check listed exactly the 10
unmarked H3s against the pre-delta tree, and a seeded untagged-H3 red-proof stands permanent; then green,
full suite 542. The existing forward-direction check (`test_every_scenario_carries_its_feature_tag`) is
untouched, so both directions now hold. Door: feature; kind: skill; footprint: single-module (guardrails
node). Delegation: none — the marker design and the 10-heading classification were the judgment; proposed
senior / chosen senior. SPEC v1.1.6, spec-author 1.0.6, pack 1.1.6.

## 2026-07-12 (session 40) — critical-priority preemption bound, echoed at intake (row 284, INV-133, prover F5)

**What.** Prover finding F5: "critical" is defined in bug terms but liftable onto any door, so a critical
non-bug (a violated safety gate the tripwires route to the feature door) headed the queue and then waited for
the current lane — only the bug door preempts — while a human who said "critical" for a live break expected
bug-like preemption. INV-133 states the boundary unambiguously: a critical non-bug heads the queue but never
preempts a rolling lane (it lands at the current lane's checkpoint, ahead of everything else waiting); a
genuine live break that must stop the work now is a bug; and the capture echo [INV-27] says the bound back
when a wish is marked critical on a non-bug door, so the human can re-door it a bug rather than discovering at
the next report that the work he thought was stopped kept running.

**The taste call — the fork.** The finding offered two arms: restrict "critical" to bug-door conditions with
a separate urgency mark for a non-bug break, or state the no-preempt bound plainly and echo it at intake.
Chose the second. The first would need a second urgency word and would re-touch every intake surface for a
distinction the queue already draws (preemption is bug-door-only, T-9); stating the bound and echoing it at
intake keeps one urgency vocabulary and closes the gap at the exact moment the human could be misled. The
spec already stated the bound at line 274 (critical heads the queue whatever its door; only the bug door
preempts) — the new work is the unambiguous no-preempt sentence and, above all, the intake echo.

**Homes.** New invariant INV-133 (the priority clause is its home), its Formal-index row, communicator's
capture echo rule 12 (v1.0.8), and matrix M-274 under the build-pipeline block. Red-first:
`test_critical_preempt_bound` (4 assertions) red against the pre-delta tree, then green; full suite 546.
Door: feature; kind: skill; footprint: single-module (build-pipeline node). Delegation: none — the fork
choice and echo wording were the judgment; proposed senior / chosen senior. SPEC v1.1.6, communicator 1.0.8,
pack 1.1.6.

## 2026-07-12 (session 41) — delegation/routing rule de-duplicated: the pack side crisped (row 262)

**What.** Base rule 5 in `skills/live-spec-base/SKILL.md` is rewritten as the ONE clear statement of
delegation, anchored to the routing law SPEC INV-69. The settled rule now reads: the lead — the
orchestrator seat, whatever tier holds it — orchestrates, briefs, and accepts, and does no grunt itself;
every unit of work routes on its own merits, PER UNIT, the trigger being judgment against mechanical with
size only a weak hint; the tier is PROPOSED (one-shot → haiku, multi-step mechanical → sonnet, judgment or
design → senior, a judgment step never routed down); a worker's green is a lead the lead ACCEPTS by
re-checking; a large or high-stakes landing earns an independent fresh-context checker (SPEC INV-46); every
override of a proposed tier and every failed-acceptance escalation is logged, proposed → chosen → why. The
raw-output-is-evidence clause is kept intact — base rule 13 points at it as its delegation face.

**Why / what left.** Row 262's audit found the delegation rule stated in two homes (the pack and the
personal cross-project playbook) with three divergent bars. Per base rule 4 (one home per fact) the pack's
routing law is the normative home; the playbook's Delegation section was already collapsed to a pointer in
its own repo, so this landing finishes the job on the pack side. The three superseded bars are gone from
base rule 5: the numeric >3-files / >30s / edit-strings-known triggers (replaced by judgment-against-
mechanical, size a weak hint), "default to the junior" (replaced by propose-per-unit, never default), and
the one-per-session spot-check (replaced by accept-by-re-checking plus the fresh-context checker on
high-stakes landings). OD-1 answered: the pack is the normative home outright. OD-2 answered: the standing
junior task-list lives in the project's own ROADMAP/NEXT_STEPS, the playbook holding only cross-project
principle.

**No parallel restatement remains.** Grep confirmed no other pack file nor the personal profile
(`~/.claude/live-spec/profile.md`) restates the full mechanism. build-pipeline's "Junior delegation"
section elaborates the routing law as its own pipeline domain and points back to base rule 5 — that is the
pack's by-design elaboration (the base header names it), not a second full statement, so it stays.

**Homes / versions.** Base rule 5 (its one home); base skill 1.0.7 → 1.0.8 with the seven working-skill
inherit-pins lockstepped; VERSION and plugin.json 1.1.6 → 1.1.7. Door: refactor; kind: prose; footprint:
cross-cutting (the base rulebook plus its version/pin lockstep). No new spec code — INV-69 already carries
its Formal-index row and its owning node (build-pipeline). Full suite 546/546 green. Delegation accounting
(INV-103): proposed senior → chosen senior → why — prose judgment on the shared rulebook, no mechanical
grunt worth routing down (the seven-pin lockstep was one inline sed).

## 2026-07-12 (session 41) — the footprint note is enforced on every landed feature/refactor row (row 291, INV-134)

**What.** INV-128 (row 259) states the three-source footprint read and writes the verdict in the row's
`footprint:` note, but it explicitly deferred the mechanical enforcement to a follow-on row. This is that
follow-on. New invariant INV-134: a landed feature-or-refactor row carries its footprint note, and a suite
check reads the queue (ROADMAP.md) and reddens a landed feature-or-refactor row that omits it. This is the
mechanical floor under INV-128's read, built to the same shape the delegation-accounting check (INV-103)
gives the routing rule — prose states the read, the check holds it on every landing.

**The forward-binding problem, and its cut.** INV-128 only landed mid-session-40 (~17:01, 2026-07-12), so
the rows that landed earlier that same day predate the footprint concept and carry no note; binding the
check from the bare date (as INV-103 could, because delegation lines predated their check) would have
reddened ~39 historical rows. The honest cut is INV-128's own landing moment: a feature/refactor row landed
on 2026-07-12 at or after ~17:01, or on any later date, owes the note; rows before it stay as they landed.
The scan parses the landed date and, on the cutoff day, the `~HH:MM` stamp. It matches the `footprint:`
note itself (the colon form with one of the three values), not the bare word — prose uses "footprint"
freely (row 259's own status says "footprint HELD"), and an early red-proof attempt was foiled by exactly
that until the match was tightened.

**Homes / red-first.** New clause after INV-128's in the spec + its Formal-index row; the ROADMAP row
template gains the footprint field (beside door/kind/map); the capture echo already carried the field from
INV-128. `tests/test_footprint_note.py` (5 tests): the string tests red against the pre-delta tree, and the
queue-scan red-proven by stripping row 259's footprint note and watching it go red, then restored.
ARCHITECTURE's build-pipeline node gains INV-134; TEST_MATRIX gains M-275. Door: feature; kind: infra (the
buildable deliverable is the check + template field); footprint: cross-cutting (five homes), HELD through
the landing. SPEC v1.1.6→1.1.8, VERSION/plugin 1.1.7→1.1.8. Full suite 553 green. Delegation accounting
(INV-103): proposed senior → chosen senior → why — the check-scoping (the forward cutoff at INV-128's
landing time, the colon-note match) was the judgment; no mechanical grunt worth routing down.

## 2026-07-12 (session 41) — per-kind concrete-layers and proofs declaration (row 292, INV-135)

**What.** P0k of the fourteen-principle architect draft: the entry impact read, the footprint categories,
and the test ladder are kind-ABSTRACT stations. They read cleanly as presentation/single-module/cross-cutting
and string/DOM/browser/pixel only for a codebase — a photo site, a promotion campaign, and a music project
each decompose and prove differently. New invariant INV-135 (base rule 24): the pack states the abstract
station once, and each project's founding declares its own concrete layers (`project.layers`) and its
concrete proof kinds (`project.proofs`) in the host profile beside `project.kind` (INV-36). A founding check
reds a kind recorded with neither.

**Why it matters.** A principle set that assumes code fits one project and breaks the rest. The three
footprints generalize (a presentation-only change touches what the audience meets, a single-module change
stays in one owned layer, a cross-cutting change moves a shared law) but the LAYERS are the project's own:
a codebase's frontend/backend/store, a photo site's content/rendering-engine/deployment, a campaign's
message/channels/assets. The proofs follow: tests and rendered checks for code, a byte-diff plus an eye-walk
for a photo site, a register lint plus the owner's review for a campaign. So the one method fits every
window instead of a code method worn awkwardly by a photo site.

**Homes (seven).** base rule 24 (the rule's home); the spec founding clause after INV-36 + Formal index;
the live host profile now declares live-spec's own layers (the rulebook and spec · the working skills · the
guardrails, templates, and suite) and proofs (the pytest suite · the docs/prover records · the owner's
read); ARCHITECTURE gains the per-kind footprint-and-proof table (skill-pack, code, photo, prose, music
rows); ADOPT.md's founding step prompts the two lines; spec-author reads the declared layers, test-author
the declared proofs; the founding check `tests/test_founding_layers_proofs.py`.

**Red-first, and a real trap caught.** 9 tests. The founding check reds against a kind-only fixture and a
missing-only-proofs fixture; the three passing fixtures are the three real hosts (track-coach=code/music,
tlvphotos=photo, promotion=prose). One trap: the check first read the live host profile via read_flat,
which flattens newlines, so its line-anchored `project.*:` regexes matched nothing and the incomplete live
profile passed FALSELY. Fixed to read raw — then the live profile went red until its own layers/proofs
lines landed, so the check has real teeth. A second placement trap: M-276 first sat under the build-pipeline
matrix block, but INV-135 is base-rulebook-owned, so the matrix-row-under-owner check red-caught it; moved
to the base-rulebook block.

**Scope.** This lands the declaration and the founding check. The footprint check (INV-134) and the
test-level rule actually READING the declared categories mechanically, rather than a hardcoded code list,
is named as the ratchet but left to the R3/R5 machinery — a stated non-goal.

**Versions.** Door: feature; kind: skill+infra; footprint: cross-cutting (seven homes), HELD. SPEC
v1.1.8→1.1.9, base 1.0.8→1.0.9 (pins lockstepped ×7), spec-author 1.0.6, test-author 1.0.2, VERSION/plugin
1.1.8→1.1.9. Full suite 562 green. Prover: CROSS-LINK 0 must-fix. Delegation (INV-103): proposed senior →
chosen senior → why — the per-kind vocabulary, the founding-check format, and the seven-home wiring were the
judgment; no mechanical grunt worth routing down.

## 2026-07-12 (session 41) — the cross-cut counter (row 293, boundary-health mechanized)

**What.** P6 of the fourteen-principle architect draft. The boundary-health law (INV-128) already states
the bar — a right node boundary keeps a typical request in one node — and the signal — repeated
cross-cutting landings on the same node pair mean the boundary sits in the wrong place — and it deferred
the mechanical half. This builds it: `guardrails/crosscut_counter.py` reads the closed queue's
cross-cutting landings, counts per unordered node pair how many cross-cutting changes touched both nodes,
and flags a pair reaching the threshold (3 by default) as a boundary-move candidate for the MINOR audit —
the mechanized "seen twice, own it" (base rule 19) applied to boundaries.

**Advisory, not a gate.** The flag is an audit SIGNAL, never a per-push red: a boundary moves only through
the architecture step and its re-prove (INV-37), so the counter's `__main__` exits 0 always and just prints
the flagged pairs for the MINOR audit to weigh. No new invariant — this mechanizes the already-stated
INV-128 boundary-health law and rides INV-37 for the re-carve, the derive-before-invent choice (INV-128
itself named this counter as its follow-on).

**Homes.** ARCHITECTURE's Boundary-health section now names the landed counter, its threshold, and its
advisory nature (was a deferral sentence); build-pipeline's before-a-MINOR gate runs it. Red-first:
`tests/test_crosscut_counter.py` (8 tests) — red as an ImportError before the module existed, then a
synthetic queue proves the over-threshold pair is flagged, the below-threshold pair is not, and moving the
threshold moves the line; the ROADMAP adapter reads cross-cutting rows. Run on the live queue the counter
flags exactly `architecture <-> spec` (3 cross-cutting landings — the recent method-law rows, which by
nature touch spec and architecture together), a true advisory reading the MINOR audit weighs.

**Structural re-prove.** Because this touches the node-map's own law, the architecture was re-proven with
the architecture lens (`docs/prover/2026-07-12-s41-crosscut-counter-architecture.md`, 0 must-fix, no new
node or seam) and the ARCHITECTURE Prover-record table gained its dated row (INV-116). Swept live along the
way: build-pipeline's INV-128 deferral note repointed — the footprint check (INV-134), the per-kind
declaration (INV-135), and this counter marked landed, only the interface-test machinery still deferred
(rule 4, pointers kept live).

**Versions.** Door: feature; kind: infra; footprint: cross-cutting, HELD. build-pipeline 1.0.20→1.0.21,
VERSION/plugin 1.1.9→1.1.10. No spec change (the law was already stated). Full suite green. Delegation
(INV-103): proposed senior → chosen senior → why — the per-pair tally design, the advisory-not-blocking
decision, and the architecture re-prove were the judgment; no mechanical grunt worth routing down.

## 2026-07-12 (session 41) — interface-test machinery (row 294, P8+P9, INV-101)

**What.** Two architect principles, one landing. P8 — the test level follows the footprint's layer: a
presentation change is asserted at browser-computed or above (the user sees it), a single-module change at
its module's interface, a cross-cutting law by a string/traceability test across every surface. P9 — each
module's tests assert its declared INTERFACE (one interface-level row per architecture-node block, not the
internals or a neighbour's render), and a cross-cutting law from the declared-laws home (INV-101) gets one
test per surface it governs.

**Homes.** test-author gains the layer-to-level rule and the interface-test requirement, and its coverage
checklist (step 8) gains both; the matrix template's coverage checklist gains all three items (interface
row per block · level follows the layer · every declared law a test per surface); product-prover's
declared-laws station gains the per-surface-test duty — a law stated everywhere but tested nowhere is a
finding of the same class as an untested surface (anchor INV-101). No spec or ARCHITECTURE change — the
rules extend the existing INV-101 and the level ladder, so no new invariant and no re-prove.

**Mechanical floor, green-on-real / red-on-synthetic.** `tests/test_interface_coverage.py` (9 tests)
extends traceability in two directions: (A) a declared law with a surface that has no test row goes red,
(B) a module block with no interface-level row goes red. Each is red-proven on a synthetic fixture (a law
governing three surfaces with one untested; an empty and a note-only block). The real matrix satisfies
both — all 18 node blocks own an interface row (a BUILT row at a ladder level with an owning test), and the
pack's three declared laws each have a covering row — so the suite stays green while the checks bite on a
real violation. This is the same shape as the cross-cut counter and INV-134's scan: state the rule in prose,
hold it with a check that reds on a violation, prove the red synthetically without reddening the shipped
state.

**Scope.** Full per-surface register wiring across every surface stays its own work; this lands the rule
and the mechanical floor. Door: feature; kind: skill+infra; footprint: cross-cutting, HELD. test-author
1.0.2→1.0.3, product-prover 1.0.8→1.0.9, VERSION/plugin 1.1.10→1.1.11. Full suite 579 green. Delegation
(INV-103): proposed senior → chosen senior → why — the two check designs, the green-on-real/red-on-synthetic
split, and the P8/P9 prose were the judgment; no mechanical grunt worth routing down.

This closes the architect-draft follow-ons R0/R1/R3/R5 (rows 291-294): the footprint-note check, the
per-kind concrete-layers-and-proofs declaration, the cross-cut counter, and the interface-test machinery —
the mechanical halves INV-128 deferred.

---
