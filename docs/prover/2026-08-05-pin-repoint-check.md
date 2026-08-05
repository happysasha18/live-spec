# Prover check — the design-map pin repoint, 2026-08-05

Independent check of the uncommitted edit to `ARCHITECTURE.md`: 31 pin line-numbers moved, 31
insertions and 31 deletions, no other change to the file. This record is written by a seat that did
not make the edit (SPEC INV-237). It only names a broken pin if it finds one; fixing it stays the
edit's own worker's job.

## Method

Read `git diff ARCHITECTURE.md` to list every changed pin, old value and new value together. For
each changed pin, open the target file at the new line. Check whether that line carries what the
pin's label names, and quote the line's own text as proof. Then spot-check pins the diff left alone,
the same way. This makes the record speak to the map beyond the delta, past what one worker chose to
move. A `:1` pin names a whole file and sits outside this check; the spot-check draws only from pins
that carry a real line number.

## What was checked

31 changed pins, across five files. `skills/live-spec-base/SKILL.md` carries 21 of them: the
shared-rules block, the parallel-lanes sub-rules, and the settings-ladder rows. The rest split across
`skills/spec-author/SKILL.md` (3), `skills/build-pipeline/SKILL.md` (1),
`skills/communicator/SKILL.md` (4), and `templates/TEST_MATRIX.template.md` (1).

11 unchanged pins, spot-checked beyond the required 10, across `skills/spec-author/SKILL.md`,
`skills/product-prover/SKILL.md`, `skills/build-pipeline/SKILL.md`, `skills/communicator/SKILL.md`,
`.live-spec/profile.md`, and `adopt/ADOPT.md`.

## Changed pins — proof table

| Pin (new line) | Label | Line's own text (proof) | Verdict |
|---|---|---|---|
| `live-spec-base/SKILL.md:117` | rules | `## The shared rules` | holds |
| `live-spec-base/SKILL.md:160` | rule 6 checkpoint | `6. **Every long or delegated piece of work keeps a persistent checkpoint.**` | holds |
| `live-spec-base/SKILL.md:182` | rule 7 fence | `7. **The concurrent-edit fence, before every write and every commit.**` | holds |
| `live-spec-base/SKILL.md:297` | rules 15-16, door + work-kind + prototype | `15. **The door is named before any code.**` | holds |
| `live-spec-base/SKILL.md:339` | rule 19, workshop-noise law | `19. **The problem ledger — workshop noise is owned, never re-suffered.**` | holds |
| `live-spec-base/SKILL.md:358` | rule 20, skill search | `20. **Search for a skill before reinventing (SPEC INV-65).**` | holds |
| `live-spec-base/SKILL.md:368` | rule 21, clean-writer road | `21. **Human-facing prose is drafted by a clean writer (SPEC INV-84).**` | holds |
| `live-spec-base/SKILL.md:378` | rule 22, convergence principle | `22. **Every process converges on its goal (SPEC INV-98).**` | holds |
| `live-spec-base/SKILL.md:392` | rule 23, live-channel law | `23. **A behavioural rule that breaks mid-turn twice earns a live channel (SPEC INV-108).**` | holds |
| `live-spec-base/SKILL.md:661` | ladder | `## The settings ladder` | holds |
| `live-spec-base/SKILL.md:719` | defaults, `budget.pressure` row | `` `budget.pressure` `` row text opens "full — every check runs at full strength" | holds |
| `live-spec-base/SKILL.md:447` | rule 26, design principles | `26. **A project kind also declares design principles the verify pass runs (SPEC INV-136, INV-139).**` | holds |
| `live-spec-base/SKILL.md:455` | rule 27, seat decides | `27. **The orchestrator decides what it can decide, and surfaces only what it cannot (SPEC INV-143).**` | holds |
| `live-spec-base/SKILL.md:465` | rule 28, periodic full audit | `28. **A periodic full audit catches the drift no lint names (SPEC INV-145).**` | holds |
| `live-spec-base/SKILL.md:578` | rule 32, release-tier rule | `32. **A release's number answers what taking it costs a host (SPEC INV-217).**` | holds |
| `live-spec-base/SKILL.md:514` | rule 31, earned-message law | `31. **Agents talk on exactly two channels, and a message earns its passage (SPEC INV-183, INV-189).**` | holds |
| `live-spec-base/SKILL.md:209` | rule 7 worker-restore sub-rule, INV-298 | `- **A worker never restores a working tree with a git command (SPEC INV-298).**` | holds |
| `live-spec-base/SKILL.md:632` | rule 35, session extract | `35. **A session's record is read at both ends by an agent that did not live it (SPEC INV-302).**` | holds |
| `spec-author/SKILL.md:333` | fences | `## The regression fences — run first when the wish touches a surface that already lives` | holds |
| `spec-author/SKILL.md:349` | facet sweep | `## The facet sweep — run when a wish's door says feature` | holds |
| `spec-author/SKILL.md:154` | enumeration-threshold rule, INV-215 | `- **The enumeration threshold makes that checkable (SPEC INV-215).**` | holds |
| `build-pipeline/SKILL.md:336` | re-carve paragraph, INV-113 | `Re-carving the whole node map IS legal:` — the paragraph names INV-113 two lines down | holds |
| `live-spec-base/SKILL.md:186` | rule 7 lanes sub-rules | `The parallel-lanes rules underneath the fence, one each:` | holds |
| `live-spec-base/SKILL.md:210` | one row per landing commit | `- **One row per landing commit.**` | holds |
| `communicator/SKILL.md:299` | rule 10, decision page | `- **Several open picks → ONE interactive decision page.** *(rule 10)*` | holds |
| `communicator/SKILL.md:352` | rule 11, evidence walk | `- **"Did we actually do X?" is answered by walking the evidence...** *(rule 11)*` | holds |
| `communicator/SKILL.md:231` | rule 9, outcome-leads line shape | `And the line's SHAPE obeys the outcome-leads law (SPEC INV-28):` | holds |
| `communicator/SKILL.md:286` | rule 7, chat-arm clock sentence | `Time is a fact like the rest: a human-facing timestamp — the [HH:MM] a reply leads with` | holds |
| `templates/TEST_MATRIX.template.md:52` | coverage validation | `## How coverage is held` | holds |
| `live-spec-base/SKILL.md:716` | defaults, `design-sync` row | `` `design-sync` `` row text opens "off — a host with visual components may switch it on" | holds |
| `communicator/SKILL.md:181` | rule 5, channel line | `- **The channel is picked by the SEAT (SPEC INV-67).**` | holds |

All 31 changed pins hold.

## Unchanged pins, spot-checked

| Pin | Label | Line's own text (proof) | Verdict |
|---|---|---|---|
| `spec-author/SKILL.md:221` | spine | `## The spine — what every spec must contain (not its section order)` | holds |
| `spec-author/SKILL.md:247` | [target] tag tripwire | `**Name the future with the [target] tag — it is a tripwire that drives the pipeline.**` | holds |
| `spec-author/SKILL.md:374` | axes composition | `**Read the surface's composition axes from the kind too (SPEC INV-244).**` | holds |
| `product-prover/SKILL.md:276` | review modes | `## Review modes` | holds |
| `product-prover/SKILL.md:723` | unwritten-seam hunt | `- **Unwritten seams** — for every stateful surface, derive the reachable situations yourself` | holds |
| `.live-spec/profile.md:6` | gate cadence instance | `` `prover.cadence: a re-check before EVERY push` `` | holds |
| `product-prover/SKILL.md:362` | restructure-merge gate | `**The restructure-merge gate: judge the delta.**` | holds |
| `build-pipeline/SKILL.md:107` | step zero | `- **Step zero, before ANY tool call: name the door aloud...**` | holds |
| `build-pipeline/SKILL.md:217` | work-kind table | `## The work-kind table — WHAT the wish builds scales HOW each step runs` | holds |
| `communicator/SKILL.md:105` | the rules | falls inside rule 8's body; the heading sits separately at line 35 | holds, on a broad reading, see note |
| `adopt/ADOPT.md:44` | VCS gate first | `## Phase 0 — Version-control gate first (SPEC A-5, done early for reversibility)` | holds |

11 pins spot-checked, one past the 10 asked for. Ten land on the exact thing their label names.

**Note on `communicator/SKILL.md:105`.** This pin's label reads plainly "(the rules)"; its
neighbours read "(rule N)" instead, naming one rule apiece. The shared-rules block in that file runs
from the heading at line 35 through line 419. Line 105 sits inside that span, in rule 8's own text;
the heading itself is separate. Read as a pointer to one exact line, it misses. Read as a pointer
into the rules block the label names in general, it lands.
`docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md`, written earlier today, reviewed
this same pin and reached this same call: it lands inside the rules section its label names. This
record repeats that earlier call on a second look. It flags the pin as worth tightening to the
heading line, the next time this node's pins are swept. A suggestion for that sweep, held here as an
open item.

## Verdict

All 31 pins the delta moved hold: each new line carries what its label names. All 11 spot-checked
pins the delta left alone hold too, one under the broad-label reading above. No pin fails, so this
record carries no attention flag and needs no attention marker.

## Reach

Files read directly, by line, to produce the proof above: `ARCHITECTURE.md` (diff and full pin
listing), `skills/live-spec-base/SKILL.md`, `skills/spec-author/SKILL.md`,
`skills/build-pipeline/SKILL.md`, `skills/communicator/SKILL.md`,
`templates/TEST_MATRIX.template.md`, `skills/product-prover/SKILL.md`, `.live-spec/profile.md`,
`adopt/ADOPT.md`. Also read for form and precedent:
`docs/prover/2026-08-05-architecture-pointer-catchup-recheck.md` and
`docs/prover/2026-07-23-row480-shortform.md`.
