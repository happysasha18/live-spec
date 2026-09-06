### [node: communicator]

**responsibility** — the human-facing exchange. It carries reports, batched questions, decision pages, and done-claim answers. It also carries the capture echo and departures board, the feature map on demand, the pre-report walk, and working narration.

**owns** — T-7 · E-22 · INV-25 · INV-27 · INV-28 · INV-32 · INV-34 · INV-35 · INV-38 · INV-93 · INV-94 · INV-95 · INV-109 · INV-42 · INV-51 · INV-52 · INV-57 · INV-58 · INV-59 · INV-60 · INV-64 · INV-71 · INV-81 · INV-83 · INV-130 · INV-67 · INV-223 · INV-286 · INV-314
- T-7 is the report step, and the walk before it is build-pipeline's.
- INV-286 is the showing walk's clearing arm, the same shape as INV-223. The law is this node's. Its check rides the suite and takes no gate letter. The record homes are declared as host config in the guardrails node's config file.

**pins** —
- `skills/communicator/SKILL.md:38` (the rules)
- `skills/communicator/SKILL.md:300` (rule 10 — the decision page)
- `skills/communicator/SKILL.md:351` (rule 11 — the evidence walk)
- `skills/communicator/SKILL.md:234` (rule 9's outcome-leads line shape)
- `skills/communicator/SKILL.md:470` (the pre-report walk)
- `skills/communicator/SKILL.md:287` (rule 7's chat-arm clock sentence)
- `scripts/sweep-rendered.py:1` (INV-286 — the clearing mechanism and the home rule's one home)
- `guardrails/check-rendered-sweep.py:1` (INV-286 — the sweep check, report-only against the tree, rides the suite not the push chain)
- `guardrails.config.json:1` (INV-286 — the homes declared outside the sweep's reach under `rendered_pages.outside_reach`)
- `scripts/render-doc.py:1` (INV-286 — the renderer that stamps the generator mark the clearing rule reads; its cross-link laws stay with M-4)
- `attic/MANIFEST.md:1` (INV-286, INV-7 — where a clearing's declaration line lands)

**notes** —
- also carries the clock law's chat-arm sentence as a wiring pin. That clock invariant's owner is the guardrails node.
- also carries the two earned-message tells — the deposit-tell and the decline-tell — as status-report wiring. They stand in a plain notice register, and the base-rulebook owns them.

### [node: work-board] [target]

**responsibility** — the standing page that shows the whole queue as columns of cards, the work in hand among them. It carries four parts. The page itself. The one source file in the host's tree, holding the craft set and — when it is built — each task's statement and its validation record. The generator that renders that file with the queue into the page. And the statement-validation check a task passes before it enters work (Requirement 309, q-816). Three of the four ship: the generator is the one source file and the one home for the craft set, and it draws the page. The validation check is still ahead, so this node stays [target].

**owns** — INV-308, INV-309, INV-310, INV-311, INV-312, INV-313

**pins** —
- `docs/norms/work-board.html` (the frozen norm the page's form follows)
- `scripts/render-board.sh:1` (the generator, and the one source file: it holds the craft set and reads every other field from the plan, the checkpoints, git's own lanes, the waiting list, the archive and the registry)
- the drawn page `board.html` — generated, gitignored, published by `.github/workflows/pages.yml:1` at the one stable link the registry row names; it is an output, so no line of it is pinned
- `SURFACES.md:1` (the registry row the board refuses to render without)
- `tests/test_work_board.py:1` (one test per built fact of `matrix/work-board.md`)
- — (the statement-validation check is specified; its code is still ahead)

**notes** —
- the three-question fitness test at this node's birth (SPEC INV-122), answered. **Testable alone:** the generator renders the page from fixture queue rows, fixture archive rows, and fixture lane records. The node is proven with no session and no live repository behind it. **A real second place needs it:** the statement-validation check serves queue-take beside the page. Take-up reads a row's validated statement whether or not anyone opens the board. Two callers stand on this node. **Parallel-safe:** the board's source file is written under the pen like any shared document (INV-11, INV-39). A session writing it and a neighbour's session queue on the pen, never on each other.
- the generator and the page are pinned above. What is still ahead is the statement-validation check, and it waits on a datum nothing in the tree records — a statement's own time estimate, carried by no ticket field, no checkpoint line and no delivery report — so the mechanical floor of Requirement 309 criterion 49 has nothing to read. `matrix/work-board.md` rows M-531 to M-535 stay *todo* and their cells say so.
- the board takes no report duty from communicator. The chat's departures board, the narration, and the live status line keep their scope, and the board adds a view beside them (INV-27, INV-35, INV-71).
