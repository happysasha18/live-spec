# live-spec — Architecture

Derived from PRODUCT_SPEC.md. The package version has one home, the VERSION file, and is not pinned
here where it would read stale (row 265). A row number names the wish queue: an open row stands in
`ROADMAP.md`, and a closed one in the archive under `docs/queue-archive/`. Last reconciled with the spec: 2026-07-23.

This is how live-spec is built: the named nodes that the spec's facts live in. One node carries one name
and one responsibility — the one-surface-one-name rule, applied to structure. The dated record of every
architecture-lens prove lives at `docs/prover/architecture-prover-record.md`; this document states the
structure as it stands today. In the
field's vocabulary the nodes are the C4 model's building blocks and the arc42 building-block view (§5).
The seams below are their relationships. The runtime view is arc42's §6, and the placement view is its
deployment view (§7). The quality budgets are arc42 quality scenarios (§10).

The agent keeps this doc up to date by assignment. When a wish lands, its new facts go to the node that already
owns their kind, and the pin is refreshed. A fact with no home yet goes to the node that fits. A large or
surface-class wish updates the doc before the matrix is touched; a bug or small wish just cites the node it
lands in. An assignment changes no structure and triggers no re-prove. Only a new node or a new seam
does, and only then is the doc re-proved. The landing-by-landing history lives in JOURNAL.md; this doc
states the structure as it stands today. [E-14]

**What "pin" means here.** live-spec is a documentation-and-skills product: its shipped artifact is the
text. So a pin points to the `file:line` where a node's responsibility is stated or carried. A pin whose
line reads 1 names the file as a whole. Every pin
below comes from a grep or read actually run, never from memory. Two nodes carry a [target] mark in their
heading — specified, with some code still ahead. The same mark stands on an anchor, a pin, a
responsibility, or a table row, and it means the same thing there. A fully-target node keeps its pin
cell empty until its code lands (snapshot). A partly-live one pins what already ships, and leaves the
rest for the landing that follows (guardrails).

---

## The shape at a glance

live-spec is a skill pack: ten working skills plus the one shared rulebook they all load, each of them
text a model reads. Templates, guardrails, and its own dogfood documents sit beside them in one repo.
`editions/` holds a skill's public edition: the same method with every internal code resolved into the
rule it stands for. Where an edition stands, it is what that skill's public mirror ships.
Everything executes inside an agent session on the host machine.
The repo is the source of truth, and the installed copies under `~/.claude/skills/` are what a session
actually loads. Git hooks and CI re-run the same gates, and the human reads rendered pages in a
browser. No server, no runtime of its own.

## Nodes

Every spec fact is OWNED by exactly one node. A spec fact is a code anchored on a criterion in
PRODUCT_SPEC.md, located through the generated code-to-location table at `PRODUCT_SPEC.index.md`.
One split is deliberate. The wish walk `T-1..T-7` is one row of that table but two responsibilities:
the walk itself (T-1..T-6, build-pipeline) and the report step (T-7, communicator). Both sides are
named here and in the matrix.

### [node: base-rulebook]

**responsibility** — shared working rules stated once + package defaults + the settings ladder

**owns** —
- E-12 · E-13 · INV-5 · INV-9
- INV-11 (the fence fires before every write and every commit in every writing skill with no lane rolling at all)
- INV-13 · INV-14 · INV-23 · INV-56 · INV-65 · INV-76 · INV-84 · INV-98 · INV-108 · T-19 · INV-40 · ACT-1 · ACT-2
- ACT-3 (the brief's isolated-tree clause likewise stays with the delegation law that states it)
- M-2 · M-7 · E-17 · INV-105 · INV-107
- INV-117 (the session identity is minted by every session at its start and feeds both the pen tie-break and the inbox source-mark's projection)
- INV-135 · INV-136 · INV-139 · INV-291 · INV-143 · INV-145 · INV-152 · INV-163 · INV-217
- E-31 (the state-directory anchor is one anchor carrying two unrelated facts. Those are the canonical `.live-spec` directory and the worktree-isolation default that fires on two lanes' overlapping write-sets. It sits here with its leading fact and its stated category, while the lanes node owns the mechanism that default fires.)
- INV-182 · INV-183 · INV-188 · INV-189 · INV-190 · INV-191 · INV-193 · INV-194 · INV-195 · INV-196 · INV-197
- INV-225 (the sibling of the far-tier report-shape check)
- E-35 · INV-240 · T-24
- INV-298 (the worker-restore rule sits in rule 7 beside the concurrent-edit fence [INV-11], since a discarding command reaches past a brief's write-set. The orchestrator's half sits with it: the restore from the last committed stage and the fresh brief. The halt on the delivery report and the committed stage before the next worker complete that half. The mechanical arm that reads it, `guardrails/check-worker-restore.py`, is the guardrails node's.)
- INV-302 (the two session steps sit in rule 35 beside the checkpoint and resume rules. Both steps stay a discipline the seat holds; the session extract's machine, `scripts/session-extract.py`, is the guardrails node's.)

**pins** —
- `skills/live-spec-base/SKILL.md:108` (rules)
- `skills/live-spec-base/SKILL.md:157` (rule 6 checkpoint incl. INV-107 closing half)
- `skills/live-spec-base/SKILL.md:173` (rule 7 fence, INV-10/INV-11)
- `skills/live-spec-base/SKILL.md:284` (rules 15-16, door + work-kind + prototype)
- `skills/live-spec-base/SKILL.md:326` (rule 19, INV-23 — the workshop-noise law)
- `skills/live-spec-base/SKILL.md:347` (rule 20, INV-65 — skill search at setup and struggle)
- `skills/live-spec-base/SKILL.md:358` (rule 21, INV-84 — the clean-writer road)
- `skills/live-spec-base/SKILL.md:368` (rule 22, INV-98 — the convergence principle)
- `skills/live-spec-base/SKILL.md:382` (rule 23, INV-108 — the live-channel law)
- `skills/live-spec-base/references/settings-ladder.md:1` (ladder — the on-demand module beside the rulebook; `skills/live-spec-base/SKILL.md:628` carries the pointer to it)
- `skills/live-spec-base/references/settings-ladder.md:43` (defaults incl. `budget.pressure` — the economy ladder's setting; the rungs' one home is the SPEC's economy-ladder section)
- `skills/live-spec-base/SKILL.md:440` (rule 26, INV-136/INV-139 — a project kind declares design principles the verify pass runs; the per-kind table lives in this doc)
- `skills/live-spec-base/SKILL.md:448` (rule 27, INV-143 — the seat decides what it can decide, surfaces only what it cannot)
- `skills/live-spec-base/SKILL.md:457` (rule 28, INV-145 — the periodic full audit)
- `skills/live-spec-base/SKILL.md:560` (rule 32, INV-217 — the release-tier rule, minor/major/patch by the host cost)
- `skills/live-spec-base/SKILL.md:494` (rule 31, the earned-message law INV-183/INV-189 the named-reference machinery joins. The pair-travels register [E-35], the living-description heal [INV-240], and the earned auto-deposit [T-24] ride this rule's build, ROADMAP 424 [target]. The prover's station stands as their net until they ship, per [INV-150].)
- `skills/live-spec-base/SKILL.md:200` (rule 7's worker-restore sub-rule, INV-298 — the worker holds its own bytes, halts when it holds none, and the orchestrator owns recovery)
- `skills/live-spec-base/SKILL.md:604` (rule 35, INV-302 — the session extract, the closing step written by a fresh agent, and the opening decision sweep)

**notes** — INV-11, INV-117, E-31: three of these are read by the parallel-lanes node and stay here, each for a stated reason; INV-225: ROADMAP 388

### [node: spec-author]

**responsibility** — authoring method for a living, use-case-first, prover-ready PRODUCT_SPEC.md

**owns** —
- E-4 · C-1 · T-13 · INV-18 · INV-29 · INV-50 · T-14 · INV-19 · INV-20 · INV-21 · INV-101 · INV-118 · INV-126 · INV-127 · INV-138 · INV-226 · INV-244
- INV-248 (the lens carried by product-prover)
- INV-150 · INV-167 · INV-168 · E-33 · INV-185 · INV-186 · INV-187 · INV-215

**pins** —
- `skills/spec-author/SKILL.md:228` (spine)
- `skills/spec-author/SKILL.md:254` ([target] tag tripwire)
- `skills/spec-author/SKILL.md:381` (axes composition)
- `skills/spec-author/SKILL.md:340` (fences)
- `skills/spec-author/SKILL.md:356` (facet sweep — the canonical facet list)
- `skills/spec-author/SKILL.md:161` (the enumeration-threshold structure rule, INV-215)

**notes** —
- also carries the prototype-norm pointer's format sentence (`norm: <path>`, frozen copy in `docs/norms/`) — wiring, the invariant's owner is build-pipeline
- also carries the pole-declaration duty for a new host-specific capability (the pack-to-host split, owner base-rulebook)

### [node: product-prover]

**responsibility** — formal review of spec and architecture; executes the push-gate re-check

**owns** —
- M-6 · INV-61 · INV-72 · INV-114 · INV-125 · INV-140 · INV-170 · INV-171
- also carries lenses it does not own, each named beside its actual owner:
    - the entry-symmetry lens (owner spec-author)
    - the entry-state lens (owner spec-author)
    - the transition-payload lens (owner spec-author)
    - the declared-laws station (owner spec-author)
    - the paired-transition-symmetry lens (owner spec-author)
    - the scenario-level entry/exit lens (owner spec-author)
    - the edge-condition-completeness lens (owner spec-author)
    - the delivery-separability lens (owner spec-author)
    - the interactive-overlap lens (owner base-rulebook)
    - the cross-source-disagreement lens (owner build-pipeline)
    - the prototype-norm lens (owner build-pipeline)
- the discovery-side sibling of the declared-class uniformity lens is the design review (owner design-reviewer)

**pins** — the prover's mechanics live in a repository this pack does not own. The pack
cannot promise a line number there, so its pins stand on the tracked adapter instead. The
adapter is the one place the pack updates when a lens moves in a prover release.
- `skills/product-prover-pack/SKILL.md:15` (mode names — the review modes the pipeline asks for)
- `skills/product-prover-pack/SKILL.md:90` (unwritten seams — the stress-lens family, INV-72)
- `.live-spec/profile.md:6` (gate cadence instance)
- `skills/product-prover-pack/SKILL.md:60` (restructure-merge gate — INV-114 delta-judging)

### [node: build-pipeline]

**responsibility** — the wish lifecycle, walked station by station. The walk runs intake → classify → spec → prove → architecture → prove architecture. It then runs matrix → test → code → verify → commit & show → landed.

**owns** —
- E-2 · T-1..T-6 · T-8 · T-9 · T-11 · T-12 · T-15 · T-16 · T-17 · INV-1 · INV-3 · INV-4 · INV-12 · INV-16 · INV-22 · INV-26 · INV-30 · INV-31 · INV-33 · INV-37 · INV-41 · INV-43 · INV-46 · INV-53 · INV-54 · INV-55 · INV-62 · INV-63 · INV-69 · INV-70 · INV-74 · INV-75 · INV-82 · INV-99 · INV-103 · INV-137 · INV-104 · INV-106 · INV-113 · E-14 · E-15 · INV-15 · M-1 · INV-115 · INV-116 · INV-121 · INV-122 · INV-123 · INV-124 · INV-128 · INV-129 · INV-133 · INV-134 · INV-144 · INV-151 · INV-153 · INV-159 · INV-164 · INV-166
- INV-247 (the resume-side twin of the primary-source rule and the architecture step's pin-from-a-command)
- INV-221 (the pack owes the general law the profile holds as a personal value)
- INV-222 (the queue's far tier — the report-shape home is communicator, carried there as wiring)
- INV-233 (kin of the three-question fitness test [INV-122] and the boundary-health law [INV-128])
- T-22
- INV-235 (the expensive-decision class and its adversarial-read road)
- INV-237 (generalizing verify's fresh-eyes freshness [INV-46] and the periodic audit's adversarial stance to the release pass the 2.7.0 release ran in-context)
- INV-300 (the expensive-tier case of the routing rule this node already owns [INV-69]. Three parts carry it. The refusal instruction opens a brief, and the recorded refusal is re-run a tier down. The promoted phrase turns a task away before any model call. The data behind all three sits in the file the pins below name. The refusals themselves are a record under `docs/measure/`.)
- also carries three steps whose governing law is the parallel-lanes node's. Those steps are the queue-take that reads the runnable head, the claim that flips a row to in-work, and the landing commit. The steps stay here as wiring. The lane set, the claim's atomicity, and the landing commit's one-row shape are owned there and cited rather than restated.
- the mid-work re-door is this node's step, and the independence re-check it fires is the lanes node's law

**pins** —
- `skills/build-pipeline/SKILL.md:107` (step zero: the door + work-kind)
- `skills/build-pipeline/SKILL.md:91` (the craft ladder — step→craft one home)
- `skills/build-pipeline/SKILL.md:226` (the work-kind table — per-kind meanings' one home)
- `skills/build-pipeline/SKILL.md:241` (steps)
- `skills/build-pipeline/SKILL.md:536` (gates)
- `skills/build-pipeline/SKILL.md:347` (re-carve paragraph — INV-113 redesign-owes-rework)
- `skills/build-pipeline/references/delegation-protocol.md:71` (the worker-brief register-laws clause — no-scissors + no-dramatization, INV-221)
- `guardrails/node_growth_counter.py:1` (the node-growth counter, rides the suite not the push chain, INV-233)
- `guardrails/node-file-cap.json:1` (the nodes-per-file ratchet seeded at the current count, INV-233)
- `tests/test_node_growth.py:1` (the node-growth suite check, rides the suite not the push chain, INV-233)
- `guardrails/check-tier-refusal.py:1` (the tier-refusal gate. It reads the record's shape and a pattern's evidence. Its `--brief` step turns a matching task away before any model call. It rides the suite, taking no gate letter, INV-300)
- `guardrails/tier-refusal.json:1` (the instruction, the tier ladder, the promotion threshold and the promoted phrases as data, INV-300)
- `docs/measure/tier-refusals.md:1` (the refusal record the patterns grow from, INV-300)
- `tests/test_tier_refusal.py:1` (its red proof, INV-300)

**notes** —
- INV-247: standing beside the queue-take trigger re-scan [INV-129]. That reads whether the row returns, and this reads whether its described internals still hold.
- INV-247: homing the spec clause and base rule 34. INV-247: ROADMAP 430.
- INV-233: three homes with no new home.
- INV-233: the prover's seventh architecture lens (the growth re-ask, carried by product-prover as wiring).
- INV-233: the proposed number two nodes per code file set on the host's word [INV-41]. INV-233: ROADMAP 390.
- INV-235: the spec is the law's one home, with no skill-prose fork.
- INV-235: the full anchor citations live in the spec clause; the generated index carries locations only. INV-235: ROADMAP 395.
- INV-237: carried into this node's verify station and product-prover as wiring.
- INV-237: the rest a discipline the seat holds. INV-237: ROADMAP 422.

### [node: parallel-lanes]

**responsibility** — concurrent work on one repo. The pen serializes every shared-truth write. The cap and the graph pick the lane set. The lane's branch sits in its own worktree. The lane-open act opens each lane, and the integration lands it.

**owns** — T-18, INV-2, INV-39, INV-49, INV-131, E-34, T-23, INV-198, INV-199, INV-200, INV-201, INV-214

**pins** —
- `skills/build-pipeline/SKILL.md:563` (trains, one pen — the cap, the penless overlap set, the pen-stages, the re-fence after a landing)
- `skills/build-pipeline/SKILL.md:580` (the graph picks the lane set at queue-take)
- `skills/build-pipeline/SKILL.md:152` (a mid-work re-door re-runs the independence edges against every rolling lane)
- `skills/live-spec-base/SKILL.md:180` (rule 7's lanes sub-rules — three lanes under one pen)
- `skills/live-spec-base/SKILL.md:201` (one row per landing commit)
- `scripts/open-lane.sh:1` (the lane-open act's performable form. It carries the row→in-work claim commit on main, the cap refusal, and the lane branch cut into its own worktree, INV-214.)
- the lane-opening script is the first file this node owns of its own. Its law otherwise lives inside the two skills that perform it and its cited pins there. The branch road's carriers land with ROADMAP row 386 [target].

**notes** —
- the node's live half is carried in shipped skill text today and pinned above. That half is the pen and the claim's atomicity, the cap, the graph, and the one-row landing commit with its clean-tree precondition. It also holds the re-fence after a landing and the independence re-check a re-door fires.
- the branch road is specified with its carriers still ahead. Those carriers are the lane branch and its walk, the pen-moves-main clause, the fast-forward landing, the conflict law, and the vendored project-instructions line. The road rides ROADMAP row 386 [target], with the prover's station as its net meanwhile.
- also carries the mechanism the worktree-isolation default fires. The condition itself and the session identity the pen tie-break orders on stay base-rulebook's.
- the restructure merge gate stays product-prover's, since it judges a restructure's delta by token identity. An ordinary lane's landing gate is the full suite on the rebased tree.

### [node: communicator]

**responsibility** — the human-facing exchange. It carries reports, batched questions, decision pages, and done-claim answers. It also carries the capture echo and departures board, the feature map on demand, the pre-report walk, and working narration.

**owns** — T-7 · E-22 · INV-25 · INV-27 · INV-28 · INV-32 · INV-34 · INV-35 · INV-38 · INV-93 · INV-94 · INV-95 · INV-109 · INV-42 · INV-51 · INV-52 · INV-57 · INV-58 · INV-59 · INV-60 · INV-64 · INV-71 · INV-81 · INV-83 · INV-130 · INV-67 · INV-223 · INV-286 · INV-314
- T-7 is the report step, and the walk before it is build-pipeline's.
- INV-286 is the showing walk's clearing arm, the same shape as INV-223. The law is this node's. Its check rides the suite and takes no gate letter. The record homes are declared as host config in the guardrails node's config file.

**pins** —
- `skills/communicator/SKILL.md:35` (the rules)
- `skills/communicator/SKILL.md:299` (rule 10 — the decision page)
- `skills/communicator/SKILL.md:352` (rule 11 — the evidence walk)
- `skills/communicator/SKILL.md:231` (rule 9's outcome-leads line shape)
- `skills/communicator/SKILL.md:440` (the pre-report walk)
- `skills/communicator/SKILL.md:286` (rule 7's chat-arm clock sentence)
- `guardrails/check-far-tier.py --window` (INV-223 — the far-tier report-shape check's fixture)
- `scripts/sweep-rendered.py:1` (INV-286 — the clearing mechanism and the home rule's one home)
- `guardrails/check-rendered-sweep.py:1` (INV-286 — the sweep check, report-only against the tree, rides the suite not the push chain)
- `guardrails.config.json:1` (INV-286 — the homes declared outside the sweep's reach under `rendered_pages.outside_reach`)
- `scripts/render-doc.py:1` (INV-286 — the renderer that stamps the generator mark the clearing rule reads; its cross-link laws stay with M-4)
- `attic/MANIFEST.md:1` (INV-286, INV-7 — where a clearing's declaration line lands)

**notes** —
- also carries the clock law's chat-arm sentence as a wiring pin. That clock invariant's owner is the guardrails node.
- also carries the two earned-message tells — the deposit-tell and the decline-tell — as status-report wiring. They stand in a plain notice register, and the base-rulebook owns them.

### [node: templates]

**responsibility** — the document shapes a host copies at bootstrap; the matrix's generated reference section

**owns** — E-3, E-5, INV-6, B-1, E-24, INV-48, E-26

**pins** — `templates/TEST_MATRIX.template.md:52` (coverage validation), `templates/ROADMAP.template.md:1`, `templates/PRODUCT_SPEC.template.md:126` (index), `templates/PROBLEMS.template.md:1` (E-24 — the ledger's shape)

### [node: attach]

**responsibility** — attaching the pack to a host. That covers the adoption phases, the VCS gate, the attic, and the who-am-I-working-with step. It also covers the skill install, the version record, and the pack update check. The catch-up walk that brings an already-adopted host onto the current pack sits here too.

**owns** —
- E-1 · E-9 · INV-7 · INV-8 · B-2 · B-3 · INV-36 · A-0 · A-1 · A-2 · A-3 · A-4 · A-5 · A-7 · A-8 · A-9 · A-10 · A-11 · INV-89 · INV-90 · INV-91 · INV-92 · INV-110 · INV-111 · E-21 · E-25 · INV-85 · INV-86 · INV-172 · INV-177
- INV-227 (the recorded `founding.set-version` profile line is carried by host-contract as wiring, ownership stays here beside E-25 and INV-177)
- INV-178 · INV-180
- INV-307 (the spoken setup entry. One skill description carries the sentences. The routing card resolves the pack's own tree and picks the walk. `adopt/START.md` is the founding walk. The description field is carried by build-pipeline as wiring; ownership stays here beside A-0 and E-21.)

**pins** —
- `adopt/ADOPT.md:47` (VCS gate first)
- `adopt/ADOPT.md:199` (unbacked-surface verdict)
- `adopt/ADOPT.md:210` (attic)
- `adopt/ADOPT.md:289` (attach record)
- `adopt/ADOPT.md:88` (B-3 — who am I working with, first step of orient)
- `adopt/START.md:1` (B-1 — the founding walk)
- `skills/build-pipeline/references/project-setup.md:1` (INV-307 — the setup routing card)
- `MIGRATION.md:1` (A-11 — the catch-up walk's operating guide)
- `install.sh:1` (E-21 — the installer itself)
- `scripts/check-pack-update.sh:1` (E-25 — the update check + the founding arm, INV-227)
- `scripts/founding-questions.json:1` (INV-227 — the versioned founding-question set)
- `adopt/install-ratchet.sh:1` (INV-172 — the ratchet kit installer)

### [node: inbox]

**responsibility** — the parallel-safe intake door for wishes born outside a live-spec session. Its remote arm serves granted seats. Its stranger arm bridges Issues and Discussions into inbox files through a monitor. Two hosts on one repo converge on a single surfacing by a claim on the shared item.

**owns** —
- E-11 · T-10 · INV-10 · INV-112 · INV-146 · INV-147 · INV-148 · INV-149 · INV-174 · INV-192
- INV-232 (the read-direction sibling of the remote arm's push grant this node owns)
- INV-249 (the concurrency half of E-11's one-file law)

**pins** —
- `inbox/README.md:3` (one door, one new file)
- `inbox/README.md:10` (file format)
- `inbox/README.md:109` (commit rule)
- `inbox/README.md:120` (remote arm)
- `inbox/README.md:125` (stranger arm)
- `scripts/stranger-wish-monitor.py:1` (the monitor bridge, INV-147)
- `scripts/stranger-wish-monitor.py:103` (the cross-host claim + arbitration, INV-149)
- `.github/ISSUE_TEMPLATE/wish.yml:1` (the wish template requesting a source, INV-146)
- `.github/workflows/stranger-monitor.yml:1` (the package repo's scheduled monitor, INV-148)
- `scripts/read-grant.py:1` (the read-grant honest-failure check, INV-232)
- `scripts/read-grant-ask.md:1` (the read grant ask, beside `scripts/grant-ask.md`, INV-232)

**notes** — INV-232: the consumer's read the spec-author node owns. INV-232: the honest-failure check `scripts/read-grant.py`. INV-232: the real cross-machine read field-gated on a private producer-and-consumer pair over a private repo, rows 385 and 247, this landing the law arm alone.

### [node: host-contract]

**responsibility** — the recorded settings instances. Those are this host's profile, the human's personal profile, and the thin loader that boots the personal layer. The agent records sit here too: the self-declaring card in each agent's own tree, found by the pack's live scan.

**owns** — E-8, E-16, E-32, INV-184 (the card's flag at founding and at adoption's orient is carried by attach as wiring; ownership stays here)

**pins** — `.live-spec/profile.md:1` (host), personal: `~/.claude/live-spec/profile.md` (symlink → playbook repo `personal/profile.md`, its git home), loader: `~/.claude/CLAUDE.md:1` (thin loader live)

### [node: package-docs]

**responsibility** — live-spec's own host instance (dogfood): spec, queue, journal, resume file, version, records, dev-machine skill sync, its own problem ledger

**owns** — S-0, M-3, M-4, D-1, D-2, D-4, D-6, D-7, E-23

**pins** — `PRODUCT_SPEC.md:1`, `ROADMAP.md:34` (queue table), `JOURNAL.md:1`, `VERSION:1`, `scripts/sync-skills.sh:1` (E-23), `.live-spec/PROBLEMS.md:1` (E-24's dogfood instance; anchor owned by templates)

### [node: guardrails] [target]

**responsibility** — mechanical pre-push checks + surface registry + CI mirror

**owns** —
- E-6 · E-10 · M-5 · INV-17 · INV-24 · INV-45
- INV-224 (the reach map's directory classes stand as host config, read from the file the pins below name. The pack's own values stand as the default. A host adopts through its own declared project layers, with no vendored-script edit, ROADMAP 380.)
- INV-47
- INV-97 (the four host checks' shipping contract; code pin lands with row 241, [target])
- INV-66 · E-29 · INV-73 · INV-132
- INV-120 (the shipped-language gate, wired into the pack's own pre-push as gate i and the CI mirror — row 279)
- INV-245 (the project-name arm on gate i)
- INV-173 · INV-175 · INV-176 · INV-202 · INV-203
- INV-205 (the frame's home for its four instance rows 402/403/408/409)
- INV-206
- INV-229 (the parked-question default arm on the same waiting-list gate `guardrails/check-board.py`)
- INV-207, INV-208
- INV-209 (it composes with the growth law rows 390 and 392 carry. The bound governs what is shown. The archive keeps every row and stays grepable, so a row cited by number stays findable.)
- INV-210, INV-211, INV-212
- INV-213 (notice-first through the shared `guardrails/cleanup_notice.py`, whose cleanup-notice shape [ROADMAP 417] sits on the test-author node. It ends no process, so it can never become the broad-sweep footgun it guards.)
- INV-216 (config-health's arm over a permission path that no longer resolves)
- INV-218
- INV-219 (it is the declaration law's mechanical net, the target deferral coming off that law with it)
- INV-220 (retired: the Stop-hook arm's machinery is gone, its file retired at `attic/answer-first-scan.py`. The answer-first law itself stands untouched, stated in the personal profile and reminded by `hooks/chat-law-hook.sh`.)
- INV-238 (the machine for the standing no-only-say-hedge behaviour, profile `proactivity.no-only-say-hedge`)
- INV-230 (the reap and detection arms of the runaway-child class this node owns, a process-space habit at teardown taking no gate letter)
- INV-231
- INV-234 (the growable-doc sibling of gate t [INV-209] in this node's own doc-grooming family)
- INV-236 (the transport arm of the two-channel law the base-rulebook states)
- INV-239 (the description-field gate named in the pins below, dormant until the back-describe migration)
- INV-241 (the net for the orchestration laws that had none)
- INV-246 (off by default and opt-in. `judge-hooks.json` classifies it as a library entry [INV-211], and the pack's default `settings.json` leaves it unwired. It sits at the orchestration-law family's boundary [INV-241].)
- INV-242 (`guardrails/check-landing-next-steps.py`)
- INV-243
- INV-250..INV-265 (the requirements-format laws and their format-gate family, armed at the row-445 conversion delivery)
- INV-269 (`gatelib`-shaped reach lines asserted in each gate's own tests)
- INV-270 (the suite-riding armed tests are the record)
- INV-271
- INV-272 (ROADMAP 477)
- INV-273, INV-274
- INV-275 (ROADMAP 480) [target]
- INV-276 [target]
- INV-277 [target]
- INV-278 (the architecture-format member: node sections inheriting the family laws from the spec format, defined in `docs/architecture-format.md`, armed at this conversion delivery)
- INV-279 (the owns-anchor cites and carries no history. A restated law reds, and a sentence the spec lacks moves to the spec. The dated prover-record relocated.)
- INV-280 (the one-reader law over the node sections)
- INV-281 (the whole-turn reach shared through `hooks/turn_reader.py`)
- INV-282 (the hook-side sibling of gate w's registry [INV-212], rides the suite not the push chain, no gate letter)
- INV-283 (the machine the plain-language anchor law had none of; that law's own home stays communicator)
- INV-284 (the empty-validation scan, shipped, covered, classified and metered on the same terms as the hedge gate [INV-238])
- INV-285 (the tool-boundary arm of the chat laws, retired. It stood before every tool call in the tree. Its refusal landed on whichever call was in flight, a background worker's included. No field of that event names whose call it is. The pack wires no hook to PreToolUse today, and the arm's files rest in `attic/`, ROADMAP 495.)
- INV-287 (the criterion-readability arms over the spec's acceptance criteria. `guardrails/check-criterion-readability.py` reads through the family's shared parser `guardrails/specformat.py`. It rides the suite and takes no push-gate letter, the way the size ratchet does.)
- INV-288 (the per-arm recorded counts in `guardrails/criterion-readability.json`, the readability sibling of the size ratchet's bound [INV-264, INV-265])
- INV-289 (the setup-walk installer generates its coverage from guardrails/judge-hooks.json's file/command/matcher/data/personal_overlay fields and chains to scripts/install-pack-hooks.sh, closing row 495's setup-walk leg; ROADMAP 506)
- INV-290 (a push carrying deletions alone stands the whole gate chain down. Its script reads git's own ref-update lines fed to the pre-push hook's stdin. It reports whether every one is a pure deletion. `guardrails/pre-push` calls it from the top, before any lettered gate. It takes no gate letter of its own, the way `check-suite-budget.sh` and several INV-230/231/236/242 arms already do, ROADMAP 502.)
- INV-292 (`guardrails/language-rules.json`, the one home where each rule about this project's own texts sits with its own fields)
- INV-293 (`scripts/gen-language-consumers.py` writes the consumers. Those are the per-surface law bodies at `hooks/language-laws.json` and the writer's rendering at `docs/language-rules.md`. The third is the maintainer's rendering at `docs/language-rule-coverage.md`, which carries each rule's status, its catchers and their reach. `guardrails/check-language-rules.py` reds a consumer that no longer matches the home, and a pin naming no file. It rides the suite with no push-gate letter.)
- INV-294 (the catcher record each rule carries, its arming point beside it, and the reason where nothing runs it)
- INV-295 (the surface list each rule carries, and the personal layer's override of a carve-out with the shipped default kept beside it)
- INV-296 (these rules stand as relatives and move in one working pass)
- INV-297 (a reader's finding lands as a named class with its examples under it. The cold reads that produce those findings run at the text-audit node.)
- INV-301 (the findings ratchet over every live document. `guardrails/check-doc-findings-bound.py` stands as gate aa and reads `guardrails/rule-census.json` as its ceiling. It is the readability sibling of the size ratchet [INV-264] and the growable-doc bound [INV-234], and it holds a cleared document at zero.)
- INV-299 (the mechanical arm of the worker-restore rule. It is the gate script pinned below, with its call site inside the pipeline's verify step. Beside it stands the wording check `tests/test_worker_restore.py`, run over the rulebook, the pipeline skill, the delegation protocol, the agent-card template and the lane-opening script. The rule those homes state is the base-rulebook's, stated once in its rule 7.)
- INV-305 (a count this repository publishes about its own tree. `guardrails/tree-counts.json` is the machine home of every such count. It carries the measurement that produces the count and every page statement of it. `scripts/gen-tree-counts.py` fills the generated blocks. `guardrails/check-tree-counts.py` stands as gate ad over both. Whether a count is worth publishing stays with the person.)
- INV-306 (the record of what each runnable file the pack ships is. `scripts/check-registry.json` is the machine home of the kind, name, kit, root, reach and needs per file, and `guardrails/check-named-checks.py` stands as gate ae over it. It keeps a check that judges this pack's own documents out of the steps a host project follows. Both files are pinned below.)
- INV-304 (the adversarial review a push carries over the change it sends. It rides the one record a push already owes. `guardrails/check-prover-record.sh` holds it as gate a on the push road, over the record home `docs/prover/`. It holds what a script can hold. The record exists, is committed, and is fresh against the newest commit in the range. It names that range, carries each field with a value, and closes or explains each blocking finding. Whether the review was genuinely adversarial stays outside its reach. The requirement and the script's own header both say so. The second gate that once held this alone rests at `attic/check-push-review.sh`.)

**pins** —
- `guardrails/pre-push:1` (gates)
- `hooks/hedge-scan.py:1` (the hedge-scan Stop-gate, modeled on the scissors scan, INV-238)
- `guardrails/net_meter.py:1` (the net-liveness meter, INV-202)
- `guardrails/touchpoints.json:1` (the touchpoint manifest, INV-205)
- `guardrails/check-touchpoint-kind.py:1` (the touchpoint-kind gate, INV-205)
- `guardrails/check-board.py:1` (the waiting-list gate, INV-206)
- `WAITING.md:1` (the waiting-list board, INV-206)
- `guardrails/check-far-tier.py:1` (the far-tier report-shape check, report-only, rides the suite not the push chain, INV-222/INV-223)
- `guardrails/check-wrong-referral.py:1` (the wrong-referral report-shape check, report-only, rides the suite not the push chain, INV-225)
- `guardrails.config.json:1` (the guardrails config: gated-doc list, ratchet, and the reach map's `reach_classes` — infra/prose/referrer directory classes as host config, INV-224)
- `guardrails/check-authority-anchor.py:1` (the authority-anchor gate, INV-207)
- `guardrails/authority-anchor.json:1` (the declared person roster + role forms as data, INV-207)
- `DECISIONS.md:1` (the read-back / decision-set record, the decision-readback touchpoint surface, INV-207)
- `templates/DECISIONS.template.md:1` (the shipped read-back template, INV-207)
- `guardrails/check-skill-review.sh:1` (the skill-review gate, INV-208)
- `docs/skill-review/README.md:1` (the review-record home, INV-208)
- `templates/skill-review.template.md:1` (the shipped review record template, INV-208)
- `guardrails/check-doc-rotation.py:1` (the doc-rotation gate, gate t, INV-209)
- `scripts/rotate-doc.py:1` (the rotation mechanism, INV-209)
- `guardrails/check-matrix-reference.py:1` (the matrix-reference gate, gate d, INV-273)
- `guardrails/check-doc-bound.py:1` (the growable-doc bound watcher, gate z, INV-234)
- `guardrails/doc-bounds.json:1` (the four docs' declared byte ceilings, INV-234)
- `guardrails/check-ci-mirror.sh:1` (the CI-mirror gate, gate u, INV-210)
- `guardrails/ci-mirror.json:1` (the declared CI carve-out set, INV-210)
- `guardrails/check-judge-listed.py:1` (the judge-listed gate, gate v, INV-211)
- `guardrails/judge-hooks.json:1` (the wired-hook declaration, INV-211, INV-289)
- `guardrails/check-every-gate-can-fail.py:1` (the meta-gate over the chain, gate w, INV-212)
- `guardrails/gate-red-proofs.json:1` (the per-gate red-proof registry, INV-212)
- `guardrails/tree-counts.json:1` (the published tree counts: measurement, ground and page homes per count, INV-305)
- `scripts/gen-tree-counts.py:1` (the generator that fills each marked block from the tree, INV-305)
- `guardrails/check-tree-counts.py:1` (the published-count gate, gate ad, INV-305)
- `guardrails/check-hooks-can-fire.py:1` (the hook-side red-proof runner, executes each hook against its own fixture, rides the suite not the push chain, INV-282)
- `guardrails/hook-red-proofs.json:1` (the per-hook red-proof registry: a fixture per hook plus the declared entries whose output can carry no verdict, each with its reason, INV-282)
- `guardrails/hook-red-fixtures/scissors-scan/payload.json:1` (the fixture root's shape, one directory per hook under `guardrails/hook-red-fixtures/`, INV-282)
- `hooks/code-anchor-scan.py:1` (the code-anchor Stop-hook scan, an internal code trails a sentence as a quiet anchor, INV-283)
- `hooks/affirmation-scan.py:1` (the empty-validation Stop-hook scan, universal tier plus a personal overlay, INV-284)
- `guardrails/check-runaway-child.py:1` (the runaway-child Stop-time notice, report-only, INV-213)
- `guardrails/reap_owned_group.py:1` (the worker-teardown reap + idle-output detection, process-space habit not a push gate, INV-230)
- `guardrails/check-listener-tripwire.py:1` (the listener tripwire, a deferred-row mechanical revisit trigger, rides the suite not the push chain, INV-231)
- `guardrails/route_agent_transport.py:1` (the traffic-kind transport router, rides the suite not the push chain, INV-236)
- `guardrails/check-landing-next-steps.py:1` (the landing-refreshed-map gate, reds a `landed`-flipping commit whose diff omits NEXT_STEPS.md, rides the suite not the push chain, INV-242)
- `guardrails/check-description-field.py:1` (the non-empty description-field gate, arms at the back-describe migration, INV-239) [target]
- `guardrails/check-deposit-description.py:1` (the agent-channel deposit-time description lint, homed beside check-earned-message.py, INV-239) [target]
- `hooks/register_judge_core.py:1` (the register judge mechanism, INV-203)
- `hooks/turn_reader.py:1` (the shared full-turn reader five checks read through. Each reads every assistant message shown since the last human turn. The five are the contrast-frame scan, the hedge scan, the register judge, the code-anchor scan, and the empty-validation scan, INV-281.)
- `hooks/register-judge.py:1` (the chat-surface judge, INV-203)
- `hooks/register-judge-collect.sh:1` (the Stop arm)
- `hooks/register-judge-report.sh:1` (the UserPromptSubmit arm)
- `hooks/conduct-judge.py:1` (the conduct judge reading the turn's action trace, INV-241)
- `hooks/conduct-judge-collect.sh:1` (its Stop arm)
- `hooks/conduct-judge-report.sh:1` (its UserPromptSubmit arm)
- `hooks/lean-orchestrator-scan.py:1` (the lean-orchestrator arm, a Stop-hook soft signal warning a session that hoards raw file content inline with no worker dispatch, opt-in/library, INV-246)
- `guardrails/check-push-reach.sh:1` (the reach map's deciding script, gate b's scope: prose stand-down · the scoped middle road · full)
- `guardrails/check-suite-budget.sh:1` (the suite wall-time budget's net)
- `guardrails/check-prototype-fence.sh:1` (prototype fence, gate e)
- `guardrails/check-shipped-language.sh:1` (shipped-language gate, INV-120)
- `scripts/check-shipped-language.py:1` (its machine)
- `guardrails/pre-commit:1` (commit fence)
- `guardrails/install.sh:1`
- `hooks/clock-hook.sh:1` (the chat clock's hand)
- `hooks/scissors-scan.py:1` (the canonical universal scan hook)
- `scripts/install-pack-hooks.sh:1` (chained by install-session-hooks.sh, INV-289)
- `guardrails/check-config-health.sh:1` (INV-175; +skill-copy arm INV-243)
- `guardrails/check-config-health-perms.py:1` (the dead-permission-path arm, INV-216)
- `guardrails/nonempty_input.py:1` (the shared non-empty-input shape, INV-218)
- `guardrails/check-index-prose.py:1` (the retired index-prose gate — check-index-generated.py took over gate x at the row-445 conversion, INV-218)
- `guardrails/check-agent-card.py:1` (the agent-card gate, gate y, INV-219)
- `tests/test_guardrails.py:1`
- `tests/test_traceability.py:1` (the feature-coverage trace, E-29/INV-73)
- `guardrails/archformat.py:1` (the node reader every consumer reads through, INV-280)
- `tests/test_architecture_format.py:1` (the architecture-format checks: node-section shape INV-278, no-restated-law INV-279, one-reader INV-280, riding the suite)
- `scripts/install-session-hooks.sh:1` (the setup-walk installer, generates its own two hooks from the declaration and chains to install-pack-hooks.sh for the other eight, INV-289)
- `tests/test_install_session_hooks.py:1` (the two-directions coverage proof, INV-289)
- `.github/workflows/gates.yml:1` (the CI mirror)
- `guardrails/check-deletion-only-push.sh:1` (the deletion-only push stand-down, INV-290)
- `tests/test_deletion_only_push.py:1` (its red proof, both directions)
- `guardrails/language-rules.json:1` (the one home for the language rules, INV-292)
- `scripts/gen-language-consumers.py:1` (the consumer generator, INV-293)
- `hooks/language-laws.json:1` (the generated law bodies, one per surface, INV-293)
- `docs/language-rules.md:1` (the generated writer's rendering, INV-293)
- `docs/language-rule-coverage.md:1` (the generated maintainer's rendering: each rule's status, its catchers and their reach, INV-293)
- `guardrails/check-language-rules.py:1` (the gate over the home and its consumers, rides the suite not the push chain, INV-292, INV-294)
- `tests/test_language_rules.py:1` (its red proof)
- `guardrails/check-prover-record.sh:1` (the one review-record gate a push runs, gate a, M-6, INV-116, INV-304)
- `docs/prover/README.md:1` (the record home and the shape a record carries, INV-304)
- `guardrails/check-doc-findings-bound.py:1` (the per-document findings ratchet, gate aa, INV-301)
- `guardrails/rule-census.json:1` (the recorded finding count per live document, the ratchet's ceiling, INV-301)
- `scripts/rule-census.py:1` (the measure both the report and the gate read through, INV-301)
- `tests/test_doc_findings_bound.py:1` (its red proof, both directions, INV-301)
- `guardrails/check-worker-restore.py:1` (the worker-restore gate, blocking, run at the pipeline's verify step and once more in the suite against this machine's own transcript root, INV-299)
- `tests/test_worker_restore.py:1` (its red proof, and the one-wording check. That check reads the rulebook, the pipeline skill, the delegation protocol, the agent-card template and the lane-opening script, INV-299.)
- `skills/build-pipeline/references/delegation-protocol.md:49` (the clause in the delegation protocol, INV-299)
- `scripts/session-extract.py:1` (the session extract's machine, INV-302)
- `templates/agent.template.md:38` (the clause in the agent card a brief is written from, INV-299)
- `scripts/open-lane.sh:100` (the clause in the printed brief stub, INV-299)
- `scripts/check-registry.json:1` (the check registry: kind, name, kit, root, reach and needs per runnable file, INV-306)
- `guardrails/check-named-checks.py:1` (the check-registry gate, gate ae, INV-306)
- registry: —

**notes** —
- the pack's own gates and opt-in fence are LIVE (hooks installed), together with the chat clock's mechanical hand. The CI mirror is LIVE too (row 14 — `.github/workflows/gates.yml`, the same scripts as a second net). Host-facing checks and the registry are still [target] (row 55).
- INV-24: the clock law's chat-arm sentence is carried by communicator as wiring. The human-facing timestamp read lives in the communicator skill, and ownership of the clock law stays here.
- INV-213: the owned-identity discipline the test-author node owns, the browser-kill lesson of row 334.
- INV-213: live wiring a documented owner-run install step, kept out of any auto-wire into a running session's Stop hook.
- INV-213: the cleanup-notice and owned-identity disciplines applied to an orphaned worker descendant.
- INV-216: personal-layer. INV-216: rides gate m's CI carve-out and known-red proof, no new gate letter.
- INV-216: kin of config-health [INV-175] and the judge-listed gate [INV-211].
- INV-219: the sibling of the kind-with-no-layers flag.
- INV-229: an arm extending the existing gate q, no new gate letter.
- INV-229: it consumes the parked-feedback-question touchpoint classification the touchpoint-kind frame [INV-205] declares.
- INV-230: safe for that reason under the owned-identity discipline the test-author node owns.
- INV-230: the idle habit's worker-contract home is the base-rulebook worker contract, carried here as wiring.
- INV-234: the architecture-budget rule's budget-plus-watcher shape lifted to every growable artifact.
- INV-236: correcting the two-channel law's refused git-universal premise (the owner's word).
- INV-236: rides the suite and takes no push-gate letter the way the listener tripwire does [INV-231].
- INV-238: installs by the setup walk beside the scissors scan [INV-173]. Config-health parity covers it [INV-175], `guardrails/judge-hooks.json` classifies it [INV-211], and the meter reads its runs and fires [INV-202].
- INV-239: both check presence only and ship with this feature's build, target.
- INV-245: riding gate i's mechanism and known-red proof with no new gate letter. INV-245: ROADMAP 441.
- INV-246: the mechanical net the lean-orchestrator law lacked, one of the orchestration laws the conduct judge holds [INV-241].
- INV-246: stands down silently on its own breakage [INV-203], runs/fires read by the net-meter [INV-202].
- INV-250..INV-265: the shape and word gates are `guardrails/check-requirement-shape.py` [INV-250, INV-251, INV-252, INV-257], `guardrails/check-no-history.py` [INV-253], `guardrails/check-vocabulary.py` [INV-254], `guardrails/check-one-name.py` [INV-255], and `guardrails/check-weak-words.py` [INV-256]. The generated index `guardrails/check-index-generated.py` with `scripts/build-index.py` [INV-258, INV-259] stands as gate x. The delta classifier `guardrails/check-delta-record.py` [INV-260..263] is armed by availability from the conversion-end freeze baseline. The size ratchet `guardrails/check-size-ratchet.py` with `guardrails/spec-ratchet.json` [INV-264, INV-265] is seeded at that freeze.
- INV-250..INV-265: the shared parser `guardrails/specformat.py` is their one reader.
- INV-287/INV-288: the fourth fact this family reads off one document. The other three are shape [INV-250..252], volume [INV-264], and words [INV-254, INV-256], each in its own gate.
- INV-289: `scripts/install-session-hooks.sh` covered only two of the ten declared hooks, while `guardrails/judge-hooks.json` already named ten (ROADMAP row 495). `scripts/install-pack-hooks.sh` already covered the other eight. The session-hook installer chains to it without rewriting it, since its own literal source is pinned by four other tests.

### [node: snapshot] [target]

**responsibility** — saved baseline of the last accepted run; declared-scope diff (ROADMAP row 55)

**owns** — E-7, A-6

**pins** — — (specified; code still ahead)

### [node: design-sync]

**responsibility** — an optional machine, [target: machine; wiring live]. A landing's declared components sync to the team's design project, human-gated (ROADMAP row 93). The machine's first real run remains.

**owns** — E-18

**pins** —
- wiring: `skills/live-spec-base/references/settings-ladder.md:60` (defaults table, `design-sync` row)
- wiring: `skills/communicator/SKILL.md:181` (rule 5's channel line)
- wiring: `skills/build-pipeline/SKILL.md:498` (the design-sync line in step 9)
- machine: —

### [node: skill-evals]

**responsibility** — behaviour tests for the pack's own skills: per working skill one scenario, red proven bare, re-run at milestones (row 94)

**owns** — E-19

**pins** — `evals/README.md:1` (the method + honest boundary), `evals/` (one file per working skill), `tests/test_traceability.py` (`test_skill_evals_present`, self-closing over skills/)

### [node: publish]

**responsibility** — the publish-quality gate: per-kind publication checklist (its one home) + the target-plugin seam; runs before the human's gate, never instead (row 98)

**owns** — E-20, INV-44, INV-96, INV-119, INV-181, INV-228, INV-303

**pins** —
- `skills/publish/SKILL.md:1` (frontmatter + when it fires)
- the kind-checklist table and target-plugin sections in the same file
- the release-note shape with its optional offers section (INV-228: the shape carries an optional offers section phrased as choices. The publish walk records the offer-or-none decision, consuming the touchpoint-frame classification.)
- `guardrails/check-release-note.py:1` (the release-note offer report-shape check, report-only, rides the suite not the push chain, INV-228)
- the mirror sync `scripts/sync-mirrors.sh:1` (publish-source selection · banner · release history · attribution · language scan)

### [node: test-author]

**responsibility** — the test method's one home. It derives TEST_MATRIX.md from the proven spec through the proven architecture, and it writes the tests. Its parts are the level ladder, real-artifact assertions, red-first proof, the pinned skip-set, and traceability as a standing test (row 163).

**owns** — E-27, INV-77, INV-78, INV-79, INV-80, INV-100, INV-102, INV-155, INV-157, INV-158, INV-160, INV-162, INV-204

**pins** —
- `skills/test-author/SKILL.md:1` (name + description)
- the level-ladder table and the two step sections in the same file
- `templates/headless_harness.py:1` (the canonical hardened and muted harness template; shell-first resolution and launch frame probe; the cleanup-notice emitter at each reap)
- `guardrails/cleanup_notice.py:1` (the shared cleanup-notice shape, INV-204)
- `guardrails/check-cleanup-notice.sh:1` (the notice gate, INV-204)

**notes** —
- also carries the canonical browser test harness the pack ships once as a template. A consumer adopts it by updating, and layers its own methods on (row 327, INV-157/158).
- the harness's process-group reap reports what it ended, INV-204

### [node: feedback-intake]

**responsibility** — the intake half of the exchange. It receives anything handed back through three channels and routes each item to the home its law owns. It keeps the feedback ledger's shape and echoes every arrival (row 47).

**owns** — E-28, T-20, INV-68

**pins** — `skills/feedback-intake/SKILL.md:1` (frontmatter + when it fires), the routing table and ledger-shape sections in the same file

### [node: feedback-collector]

**responsibility** — the outbound feedback arm, the pack's third arrow. On a rare genuinely-strong reaction it offers, with the human's positive consent, to draft a distilled non-public upstream note to the pack's authors. It deposits that note in the gitignored `outbox/` and sends nothing, so delivery stays the human's own step. It is off by default, under the `feedback-upstream` flag. It stands apart from feedback-intake, the inverse arrow, and from the measurement family (ROADMAP row 321).

**owns** — E-30, T-21, INV-161, INV-179

**pins** — `skills/feedback-collector/SKILL.md:1` (frontmatter + when it fires), the offer / upstream-note / outbox sections in the same file

### [node: onboarding-card]

**responsibility** — the settings card. A build-time renderer parses the base's package-defaults table and the profile files into the card page, per the frozen norm. The card is shown at the end of founding or adoption, and on the standing "what can I customize?" question (F-onboarding).

**owns** — INV-87, INV-88

**pins** — `scripts/onboarding-card.py:1` (renders the card), `docs/norms/onboarding-card-2026-07-10.html` (the frozen norm), trigger wiring: `adopt/ADOPT.md` (setup-end line) + `skills/communicator/SKILL.md` (standing-question line) — wiring pins, ownership stays here

### [node: design-reviewer]

**responsibility** — the design-review pass

**owns** —
- INV-141 (ROADMAP row 310)
- INV-142 · INV-154
- INV-156 (ROADMAP row 323. This node holds the class because it reached the one-class reading from the record-sibling seam it already owns, design review → record. The class is declared once here, and product-prover and build-pipeline cite it without restatement.)
- INV-165 · INV-169

**pins** — `skills/design-reviewer/SKILL.md:1` (frontmatter + when it fires), the similarity-lens, confidence-read, echo-channel, and record-discipline sections in the same file

### [node: text-audit]

**responsibility** — the audit-and-fix loop for human-facing texts. It runs the mechanical register lints first, then fresh zero-context cold reads. Each finding is fixed at its source until two consecutive reads come back clean.

**owns** — INV-266, INV-267, INV-268 (text-audit is the skill that runs this loop)

**pins** — `skills/text-audit/SKILL.md:1` (frontmatter + when it fires), the mechanical-lint and cold-read-loop sections in the same file

**notes** —
- the tenth working skill, named in the pack's skill roster and the pipeline-roles glossary. Its cold-read comprehension loop is the mechanical-lints-then-panel discipline the format-laws requirements state, homed here.
- this node carries the working-skill roster's text-audit member without owning that anchor. The roster entity's home stays base-rulebook.

### [node: work-board] [target]

**responsibility** — the standing page that shows the whole queue as columns of cards, the work in hand among them. It carries four parts. The page itself. The one source file in the host's tree, holding each task's statement, its validation record, and the craft set. The generator that renders that file with the queue into the page. And the statement-validation check a task passes before it enters work (F-work-board, ROADMAP row 166).

**owns** — INV-308, INV-309, INV-310, INV-311, INV-312, INV-313

**pins** —
- `docs/norms/work-board.html` (the frozen norm the page's form follows)
- — (the source file, the generator, and the validation check are specified; their code is still ahead)

**notes** —
- the three-question fitness test at this node's birth (SPEC INV-122), answered. **Testable alone:** the generator renders the page from fixture queue rows, fixture archive rows, and fixture lane records. The node is proven with no session and no live repository behind it. **A real second place needs it:** the statement-validation check serves queue-take beside the page. Take-up reads a row's validated statement whether or not anyone opens the board. Two callers stand on this node. **Parallel-safe:** the board's source file is written under the pen like any shared document (INV-11, INV-39). A session writing it and a neighbour's session queue on the pen, never on each other.
- the source file's name and the generator's path land with the machinery at row 166. Until then this node names the parts and pins none of them, per the [target] rule at the top of this document.
- the board takes no report duty from communicator. The chat's departures board, the narration, and the live status line keep their scope, and the board adds a view beside them (INV-27, INV-35, INV-71).

## Seams

The places two nodes meet — named, because that is where composition bugs live. Each seam states what
crosses it and which side owns the format. Where a crossing has a real schema, the row names the schema's home. For this pack the shapes *are* the templates, and the templates node owns them.

| Seam | Between | What crosses | Format owner |
|---|---|---|---|
| communicator ↔ attach | communicator → attach | a cleared page and its manifest line: the page's bytes move into `attic/` and one dated line naming the page, why it read as a render, and where it went appends to `attic/MANIFEST.md` [INV-286, INV-7] | attach (the attic and its manifest shape are the adoption node's, and the clearing writes to that shape) |
| spec → prove | package-docs · product-prover | PRODUCT_SPEC.md, whole document | spec-author (the shape both sides speak) |
| architecture → prove | package-docs · product-prover | ARCHITECTURE.md, whole document — sent into the prover at every M-1 and M-6 gate beside the spec (INV-116) | build-pipeline (the architecture step's shape, `templates/ARCHITECTURE.template.md`) |
| prove → record | product-prover · package-docs | prover record `docs/prover/YYYY-MM-DD[-suffix].md`, folded/rejected column | product-prover |
| pipeline → shapes | build-pipeline · templates | the document shapes the steps produce, incl. the matrix's generated reference section | templates |
| outside item → its home | inbox · package-docs | one item file (wish or feedback), harvested at sweep into the home its route owns — a ROADMAP row, or by the routing law (T-20) | inbox (file naming law); feedback-intake (the routing) |
| handed-in item → its home | feedback-intake · package-docs | the routed landing: a wish row, a ledger line, a harvested answer — the route named in the echo | feedback-intake (the routing law) |
| feedback ↔ the echo | feedback-intake · communicator | the one echo per received item (a wish-shaped item keeps the wish echo, INV-27) | communicator (the echo's shape) |
| attach → host state | attach · host-contract | `.live-spec/` (profile, installed versions, checkpoints home) | attach |
| base → working skills | base-rulebook · the working skills | the inherit pin (base name + version each skill opens with) | base-rulebook |
| ladder resolution | host-contract · base-rulebook | the resolved working contract communicator reads before every exchange | base-rulebook (ladder rule); host-contract (the lines) |
| report → human | communicator · the human | plain-language report · decision page + `<project>-decisions-<date>.json` | communicator |
| checks → push [target] | guardrails · build-pipeline | pre-push verdict (red blocks the push) | guardrails |
| baseline → checks [target] | snapshot · guardrails | declared-scope diff vs baseline | snapshot |
| sync → design project [target] | design-sync · the human | a landing's declared components as rendered cards; every sync passes the human's publish gate (base rule 17, ACT-1) | design-sync |
| evals ↔ working skills | skill-evals · the working skills | each scenario's green-criteria against the SKILL.md's promised behaviour | skill-evals |
| evals → milestone gate | skill-evals · package-docs | the re-run item in M-1's list + dated run records in docs/evals/ | package-docs (the gate list's home is the spec) |
| publish → the human's gate | publish · the human | the prepared deposit (README/listing/cards, checklist walked) handed to the publish/push gate — the gate stays the human's (base rules 12/17, M-6) | publish (the checklist); the human (the gate) |
| lane set → the pipeline's steps | parallel-lanes · build-pipeline | which queued rows roll as lanes and in what order — computed at queue-take from the independence graph under the cap, re-computed when a mid-work re-door creates a surface that did not exist when the lanes opened [INV-49, INV-131, INV-16] | parallel-lanes (the graph's edges and the cap); build-pipeline (the steps that read them) |
| lane branch → main | parallel-lanes · package-docs | one lane's delta: the branch rebased onto main's tip, gated on the rebased tree, fast-forwarded into main under the pen — one row per landing commit, the branch and its worktree removed at the landing [T-23, INV-39, INV-199] | parallel-lanes (the branch name `lane/<row>-<slug>`, the walk, the fast-forward) |
| lane branch → the machine's checks [target] | parallel-lanes · guardrails | the merge-base verdict standing ahead of the landing gate (the branch's merge-base with main equals main's tip), and the config-health reads of `git worktree list` and `git branch --list 'lane/*'` against the queue's open rows plus the primary tree holding main [INV-198, INV-199] | parallel-lanes (the predicates); guardrails (the checks that run them) |
| isolation default → the host's instructions | parallel-lanes · attach | one vendored worktree line into the host's project instructions, citing the isolation condition rather than restating it, versioned in that host's own tree and carried to an already-adopted host by the catch-up walk [INV-201, INV-105, A-11] | parallel-lanes (the line's content and its one-home citation); attach (the adoption step and the catch-up walk that place it) |
| fence + identity → the pen | base-rulebook · parallel-lanes | the fence's verdict before every write and every commit, the condition that fires worktree isolation (two lanes' write-sets overlap), and the stable session identity the pen tie-break orders on when no git ancestry settles a concurrent claim [INV-11, INV-105, INV-117, INV-2] | base-rulebook (the three rules); parallel-lanes (the pen that reads them) |
| lane board → human | parallel-lanes · communicator | the departures board's lane lines: each opening narrated, a waiting lane naming whom it waits behind, and cross-lane questions carried as one batched page [T-18, INV-27] | communicator (the board and the batched-question path) |
| matrix & tests derivation | build-pipeline · test-author | the proven spec + architecture in; TEST_MATRIX.md + owning tests out (steps 5–6 invoke the skill the way steps 1–2 invoke theirs) | test-author (the ladder and the assertion shapes) |
| unit → coverage | package-docs · guardrails | each `[feature: F-x]` tag on a scenario heading, mapped to its implementer node(s) + a test in the Feature coverage table below (E-29, INV-73) | guardrails (the two-way check); spec-author (the tag format) |
| catalog → card | base-rulebook · onboarding-card | the package-defaults table (with the per-row card-visible/internal mark) read at render time | base-rulebook (the table and the mark) |
| profiles → card | host-contract · onboarding-card | the personal and host profile lines the card renders as the reader's own values and the project's rules | host-contract (the line format) |
| card → human | onboarding-card · communicator | the rendered card page, through the pre-show register lint and the seat's showing channel (INV-83, INV-67) | communicator (the showing walk) |
| spec → design review | package-docs · design-reviewer | PRODUCT_SPEC.md, the proven document — read after the prover's pass at every full pass and, scoped, at every surface add and at a feature intake whose second-sibling question answers yes (INV-169) (INV-141) | spec-author (the shape both sides speak) |
| design review → record | design-reviewer · package-docs | the dated design-review record `docs/design-review/YYYY-MM-DD[-suffix].md`, per-finding outcome column (the `-suffix` arms a same-day second scoped run, mirroring the prover record) | design-reviewer |
| design-review ask → human | design-reviewer · communicator | a likely same-kind divergence as one batched question — two objects each with its spec sentence and a recommended default (INV-142), riding the batched-question path | communicator (the batched-question path) |
| card + scan → any agent | host-contract · base-rulebook | the looked-up agent's card (name, mission, zones, published contracts with their artifact paths, inbox address) read from its own tree, read-only, found by the scan's two globs under each root | host-contract (the card format) |
| agent → neighbour's inbox | base-rulebook · inbox | one message file carrying the sender's named blocked work, its stable identifier, and its need-by — deposited by the arms the inbox already owns (local: the file alone; remote: one committed file under a grant) | inbox (the file naming and deposit law); base-rulebook (the earned-message law the sweep's gate reads) |
| queue → the board [target] | package-docs · work-board | the open queue's rows with the status each records: the id, the wish text, the class, the status word and its date. The board reads a row's column off that status cell and its placement tag off the row's own map and footprint notes [INV-308, INV-277, INV-37] | package-docs (`ROADMAP.md` and its row cells); guardrails (the row lint that holds the status vocabulary, INV-277) |
| archive → the done column [target] | package-docs · work-board | the month's archived rows under `docs/queue-archive/`: each closed row's terminal state, its door, and the time it took. The current month is read by default and an older month on the person's ask [INV-311, INV-276, INV-134] | package-docs (the archive file and its rows) |
| checkpoint → the running step [target] | parallel-lanes · work-board | the movement's checkpoint record for a step in flight: the craft the seat named in the worker's brief, its icon, and the tier logged while the step runs, a mid-flight tier change updating it. The board reads a running step's worker there and shows the step unnamed where the record names no craft [INV-308, INV-69, INV-33] | build-pipeline (the checkpoint record's shape and the craft standards, INV-69, INV-33) |
| waiting board → the board's waiting region [target] | guardrails · work-board | `WAITING.md`'s items, rendered in the board's waiting region, which keeps no list of its own, so one clearing rule and one gate hold every waiting item [INV-308, INV-206] | guardrails (`WAITING.md`'s shape, its clearing rule, and the gate over it, INV-206) |
| lane record → the row's details [target] | parallel-lanes · work-board | an in-work row's branch and worktree, read from the lane's own claim commit and its checkpoint, plus the lane cap the in-work column splits its lanes by [INV-308, E-34, T-18] | parallel-lanes (the branch name `lane/<row>-<slug>`, the claim commit, and the cap) |
| board → human [target] | work-board · communicator | the rendered board page, carried to the person at one stable link through the render conventions and the pre-show register lint the seat's showing channel already runs [INV-308, INV-67, INV-51] | communicator (the showing walk and the render conventions); work-board (the page's own form, per the frozen norm) |
| design review → re-prove (the loop) | design-reviewer · product-prover | a human-accepted class sentence [INV-125] or decided sentence [INV-59] re-enters the prover, which re-reads the changed part; the design review re-reads what the declaration re-partitions plus any element a prover fix added; the loop rests in one of three named ways (converge / wait / stand-down), bounded at three progressing rounds counted by the design review — per prove pass, advancing only on a progressing round, persisting across the human's asynchronous answers, reset when a fresh pass opens (INV-154) — surfaced to the human at the cap without holding the landing | spec-author (the class / decided sentence) |

## Feature coverage

The feature layer above the anchor matrix (SPEC E-29, INV-73). live-spec's primary unit is its
person-facing scenario. Each such heading in PRODUCT_SPEC.md carries an inline `[feature: F-x]` tag.
The table below maps every unit to the node or nodes that implement it, and to a test that exercises
it. The check runs both ways (`tests/test_traceability.py`, `TestFeatureCoverage`). Every tag is a row
here and every row is a tagged scenario. Every named node is real, and every named test exists. The infra machine package-docs implements guarantees rather than user features and sits outside this layer by the project type's own definition. guardrails sits outside it too, except for the prototype fence: the mechanical check is itself the person-facing guarantee, so F-prototype names it as an implementer. host-contract sits outside it for its settings arm and inside it for the agent records. The card is a person-facing surface an agent reads, so F-roster and F-agent-birth name it as an implementer [E-32, INV-184].

| feature | implemented by | test |
|---|---|---|
| F-wish | build-pipeline, parallel-lanes, communicator | test_capture_echo_and_board |
| F-prototype | guardrails, build-pipeline | test_prod_reference_fails |
| F-publish | publish | test_publish_skill_carries_checklist |
| F-feedback | feedback-intake, communicator, feedback-collector | test_feedback_routes_have_homes |
| F-feature-map | communicator | test_feature_map_on_demand |
| F-bug | build-pipeline | test_gap4_recurring_bug_escalates |
| F-problem-ledger | base-rulebook, templates | test_problems_template_shape |
| F-bootstrap | attach, templates | test_scaffold_bootstrap_runs |
| F-adoption | attach | test_adopt_phases_cite_spec |
| F-pair | attach | test_pair_leadership_law |
| F-onboarding | onboarding-card, attach | test_onboarding_card_completeness |
| F-catchup | attach | test_catchup_walk |
| F-roster | host-contract, base-rulebook | test_card_and_scan_law |
| F-contract | spec-author, base-rulebook | test_contract_default_deny |
| F-agent-ask | base-rulebook, inbox | test_earned_message_names_its_block |
| F-agent-birth | build-pipeline, host-contract | test_agent_birth_walk |
| F-work-board | work-board, communicator | test_capture_echo_and_board |

The work board's row names a test that exists. That test exercises the neighbouring status-view
promise the board extends — the capture echo and the departures board this page grows out of. The
board's own tests arrive with its build (ROADMAP row 166), and the row's test cell is re-pointed at
them then.

## Runtime view

How each promised flow runs through the nodes [INV-74]. live-spec's kind is a skill pack, so its flow
unit is a wish or a handed-in item walking through the skills. Each hop below crosses a seam named in
the Seams table, and the payload stays that table's fact. One line per flow: the walk, then where it
can fail.

| Flow | The walk through the nodes | Where it can fail | If it fails |
|---|---|---|---|
| F-wish | the human speaks → build-pipeline (door, intake) → communicator (capture echo) → parallel-lanes (queue-take: the graph picks the lane set under the cap; the claim commits to main under the pen and the lane's branch is cut from that commit) → spec-author (delta) → product-prover (prove → record) → build-pipeline (architecture step, this doc) → test-author (matrix + tests) → build-pipeline (code, verify — on the lane's own branch in its own worktree) → parallel-lanes (integration: the pen, the rebase onto main's tip, the gate on the rebased tree, the fast-forward) → communicator (delivery report, show) | a misread door (the tripwires outrank labels); an unfolded defect (the record's folded column); a red suite at the gate; a lane landing on a base main has moved under | the tripwires re-door it mid-work; an unfolded defect blocks the landing until folded or rejected in the record; a red suite blocks the commit (the gate itself says no); the merge-base check reds a branch whose base sits behind main's tip so the gate never reads a stale tree [target], and git refuses a second worktree's attempt to move main on its own today |
| F-bug | build-pipeline (bug door, queue-cut) → test-author (red-on-bug row + test) → build-pipeline (fix, class sweep) → guardrails (gate) | a fix without its red test; a class fixed at one instance only | the traceability test goes red until the row and test exist; the class sweep is checked at review — a point fix reopens |
| F-page-clearing | a person's exchange closes → communicator (rule 5: the page's reading is over) → `scripts/sweep-rendered.py` (reads the renderer's mark, skips what git tracks and the four homes outside the reach) → attach (the page moves into `attic/`, its manifest line appends and flushes) → communicator (the declaration line rides the delivery report) | a page the process cannot move (a read-only directory, an attic standing as a file); a page committed before the law existed | the run halts and reports by name, every page already moved carrying its own flushed manifest line; a committed page stands outside the reach and waits for a deliberate deletion commit |
| F-release-sweep | publish (the shopfront walk at a version push) → `scripts/sweep-rendered.py` over the whole tree → communicator (the outcome in one line on the delivery report) | a release that forgets to sweep | `guardrails/check-rendered-sweep.py` reds the suite while a page stands, so gate b blocks the push before the release leaves |
| F-feedback | any session receives → feedback-intake (routing table) → the item's home (a queue row · the fixing commit · the decision archive · FEEDBACK.md · PROBLEMS.md) → communicator (the one echo) | an item routed to two homes; an arrival with no echo | the routing table has a home for every route by construction; an unroutable item gets one plain question, never a guess |
| F-prototype | a see/try ask → build-pipeline (prototype home, fenced) → guardrails (prototype fence) → promotion re-enters at F-wish's spec step | a sketch wired into a prod surface (the fence goes red) | the fence turns the push red; the sketch stays in its home until promoted through the spec step |
| F-publish | a push intent → publish (kind checklist) → guardrails (pre-push, reach map) → the human's gate | a stale shopfront claim; a gate skipped on a "just docs" diff | the reach map is conservative — an unmapped file runs the full suite; a stale claim blocks the push until fixed |
| F-feature-map | the human asks → communicator reads the spec's scenario headings + the queue's open rows → the answer in chat | an answer built from memory, bypassing the read documents | a host with nothing to read is answered honestly with the bootstrap/adoption pointer |
| F-problem-ledger | workshop noise fires → base-rulebook (the ledger walk) → PROBLEMS.md (WATCHED → OWNED → SOLVED) | a silent retry with no line; a third unowned recurrence | a third unowned recurrence escalates to the pack's own queue — the method itself owns it |
| F-bootstrap | scaffold → templates (copies) → attach (founding questions, B-3 profile step) | a founding question guessed rather than asked | a founding question with no answer parks as an open decision marker, asked, never invented |
| F-adoption | attach (orient → VCS gate → attic → attach record) → host-contract (profile, installed versions) | a host file overwritten with no attic line; an unbacked surface passed silently | the attic keeps every superseded file restorable; an unbacked surface goes red at the gate until specced or fenced |
| F-pair | attach (founding/adoption orient proposes the engine/instance split, human's word decides) → the two repos, each a full host (own spec/queue/journal/inbox) → the instance's inbox (lessons travel only through this door) | the split imposed rather than proposed; a third document across the seam; a window writing the pair's other tree beyond one inbox file | the human's word is the only decider, both outcomes recorded; each repo stays a full host with no third document; a window unsure of which repo it serves asks rather than writes |
| F-onboarding | setup's end (founding or adoption's orient) or the standing question → onboarding-card reads the base table + profiles → the card page → the pre-show register lint → shown by the seat's channel | a malformed table row; a missing personal profile; a register-lint block on the showing; a card row with no source | a malformed row fails the render loudly (never a silently dropped row); a missing profile renders package defaults with a plain absence notice naming the founding offer; a lint-blocked card is not shown until the flagged text is fixed; the completeness test goes red on any card/table mismatch |
| F-roster | an agent meets something possibly outside its zone → host-contract (a live scan of two globs per root finds every card) → host-contract (the owning agent's card in its own tree names its mission, zones, contracts and their paths, inbox address) → base-rulebook (the reader acts on the answer: read a contract, send a message, refer, or drop) | a tree carrying no card; a card written with no founding ratification behind it; a lookup answered from memory | a card-less tree is flagged at founding and at adoption's orient the way a kind with no layers is, and a lookup against it reports the absence rather than inventing a mission; write-ownership grants the card, so writing one needs no second permission act; a scan finding only the reader's own card answers that the reader is the only declared agent |
| F-contract [target: row 385] | Stated in the conditional until a real producer exists: this pack publishes no contract, so four of this walk's hops name no node today (the permission record, the producer's clock, the freshness check, the analysis) and the fallbacks below ship with row 385's three arms. When a host declares its first contract, its own nodes fill the walk. producer: spec-author (the contract as a spec surface — every field naming meaning, window, aggregation, source) → the owner's per-field permission, dated, in the producer's tree → the producer's own clock regenerates the artifact at its declared cadence → consumer: host-contract (the card names the path) → spec-author (the consumer's pinned version + its own staleness bound) → the freshness check → the analysis | a field published with no recorded permission; a producer whose scheduled regeneration silently stopped; a consumer analyzing an artifact past its bound; a pinned version diverging from the artifact's | each fallback ships with row 385 [target]: the producer's suite is to red on a permission-less field so the field stays home; the cadence's watcher is to red when the regeneration did not run, with the consumer's staleness bound as its independent second net for the dormant-producer case; the consumer's freshness check is to red before any analysis, naming stale data aloud; the compatibility test is to red on version divergence |
| F-agent-ask | the sender's own work blocks on a neighbour's zone → base-rulebook (the earned-message law: name the blocked work, or the message is never born) → host-contract (the card names the inbox address) → inbox (one new file, by the arms that already stand) → the receiver's sweep → the receiver's queue as a proposal → the reply road back through the sender's inbox as the message's terminal state | a message carrying no named blocked work; a question forwarded to the zone's owner; an agent's proposal relayed as an instruction; a message dying in a dormant window | the receiving sweep's gate reds while an unearned file sits in the inbox, and the sweep clears it by declining at the door, so no human reads it; a referral travels back to the asker and the zone's owner receives nothing; a proposal stays a proposal until the owner ratifies it, relaying changing only its carrier; the stated need-by expires into an escalation that surfaces in the sender's own status report for the human to read |
| F-agent-birth | a capability pins to no agent's zone, or has outgrown its host → any agent proposes (the capability, the zone, the contracts it would publish) → the owner ratifies the founding → build-pipeline (the new tree's founding walk) → host-contract (the new card in the new tree, the founding entry in the new tree's journal) → the migrated contract's consumers keep their pins | a birth inferred rather than ratified; a migration breaking a consumer's pin; a grain call made for the owner | ratifying the founding is the owner's act and a declined proposal leaves no tree and no card, its record staying in the proposing agent's own journal; a migration that breaks a pin has broken the contract rather than moved it, so the consumer reads its pinned version until it chooses to move; the skill-or-agent grain is taste, so the owner's word settles it and the proposing agent's journal records the call with its date |
| F-agent-ask · earned auto-deposit [T-24] | an agent's own work earns a message under a named birth [INV-189, INV-197] → base-rulebook (the earned-message law gates the auto-deposit exactly as it gates a hand-sent one) → host-contract (the card names the neighbour's inbox address) → inbox (one new file by the arms that already stand, references carrying the pair [E-35]; the deposit-time lint reds a referenced code with no description) → the neighbour's sweep on its next run → communicator (the sending agent emits the deposit-tell in its own status report [INV-27], naming the subject by the pair and the neighbour); if the law then declined a message the agent had drafted to send, communicator emits the decline-tell with the reason | an unearned auto-deposit (empty, curious, or tidy); a deposit-tell read as a confirmation; a decline-tell fired on a suppressed impulse; a code deposited with no description | the births gate the auto-deposit so no empty, curious, or tidy message is born [INV-189]; the tell's register stays a plain notice [INV-31]; the decline-tell fires only on a drafted-then-refused message [INV-190, INV-191]; the deposit-time lint reds the pairless code [INV-239] |
| the living description heals [INV-240] | a reader re-asks about a term at some window → base-rulebook (the re-question is the signal the description did not land [INV-83]); same-window: the owning agent records it and overwrites the description in the field's one home on its next penned run [base rule 4]; cross-window: that window deposits a fault-birth earned message [INV-189] to the owning agent's inbox (agent → neighbour's inbox) → inbox (the owning agent sweeps it) → base-rulebook (on its next penned run the owning agent reformulates and overwrites the description in its one home) → parallel-lanes (the penned write takes the description home's pen [INV-39, INV-198]) → product-prover (the overwrite rides as a named delta to the restructure-identity merge gate [INV-111]) | a reactive mid-turn write; an overwrite landing with no pen; a rewrite the identity gate did not expect | the deferral holds the write to the next penned run; the pen serializes every shared-truth write; the merge gate expects the matched token and reds an unnamed change |
| F-work-board [target: row 166] | a wish arrives → build-pipeline (door, intake) → package-docs (the queue row, its status recorded) → work-board (the generator re-renders; the card stands in the column that recorded status names, before any validation runs) → work-board (the statement-validation check: the mechanical floor, then the clean-context reader's three questions and the echo-name test) → package-docs (a passed statement writes the row's status to *ready*, dated) → parallel-lanes (queue-take pulls the row into a free lane under the cap) → work-board (the row moves to the in-work column with its statement's estimate on it, its plan shown, the running step's craft and tier read from the movement's checkpoint) → work-board (every stage change, take-up, worker spawn and finish, landing, and person-waiting state re-renders the page inside its budget, the file's update riding the landing's own commit) → package-docs (the close archives the row) → work-board (the done column reads the month's archive and stands the actual beside the estimate) → communicator (the page reaches the person at one stable link) | a task entering work on an unvalidated statement; a queue row shown in no column or in two; a stage change that leaves the page stale, or a page update that holds the stage back; a done column built from anything but the archive; two sessions writing the board's source file at once | validation stands in front of take-up, so an unvalidated statement keeps its task out of work and the row out of the in-work column; the column is read off the recorded status, so a row with a status has exactly one home and a row with none is a queue-lint red before the board ever draws it; the update budget is asserted by the generator's own suite timing assertion at its landing and the page's build stamp is what a reader judges freshness by, so a stale page shows its own staleness rather than lying; the archive is the done column's only source, so a closed row's terminal state and time pair cannot be composed on the page; the board's source file is written under the pen like any shared document, and a blocked write re-reads the file and re-applies its own row |
| F-catchup | the owner's ask at an adopted host → attach (MIGRATION.md routing: never-adopted → adoption; adopted → catch-up) → orient on the delta (record + tree + pack VERSION) → the plan document → the owner's gate → execute (baseline commit, checkpointed steps, merges per the half-done-state law) → host gates re-run → host-contract (installed-set re-record, profile lines re-homed) | a step run on an assumed precondition; a merge nesting the old dir into the new; a walk interrupted mid-execute; a pair window writing the other half's tree | every step re-reads its precondition from the tree (a done step skips); the merge law forbids nesting and old-over-new overwrites; the checkpoint resumes the walk under the already-given gate; the pair's other half gets one inbox wish and its own window walks it |

## Placement view

Where everything runs [INV-75], secrets included. A skill pack executes nowhere by itself: the skills are text a model
reads, so the "runtime" is the agent session that loads them. Five places carry the pack:

| Place | What runs or lives there | Load-bearing technology |
|---|---|---|
| the agent session on the host machine | every skill executes here — the pipeline, the prover, the exchange are behaviours of the model reading the installed SKILL.md text; session hooks (clock, chat laws) fire here | Claude Code; the pack's skills as markdown |
| the installed skills dir `~/.claude/skills/` | the copies any session actually loads; synced from the repo | `scripts/sync-skills.sh` |
| the pack repo `~/live-spec` (source: github.com/happysasha18/live-spec) | the source of truth: skills, templates, guardrails, docs, tests; the suite and gates run here at commit/push time | python3 + pytest; bash git hooks |
| the host project's repo | the documents the method writes for that host: spec, queue, journal, checkpoints, ledgers | plain markdown in the host's tree |
| GitHub + CI · the human's browser | the remote copy and the gates' second net; rendered artifacts, decision pages, and the settings card open here | `.github/workflows/gates.yml`; `scripts/render-doc.py`; `scripts/onboarding-card.py` (runs in the agent session on the host machine, output opens in the browser) |

No secret lives in this pack. The repo, the templates, and the installed skills carry none. A *host's* secrets stay in that host's own keychain or platform bindings. Its placement table names the holder (the pack's own validation derivations model this).

The work board [target] runs in three placements the table already names. Its generator runs in the
agent session on the host machine, once at every update the board's law fires. Its page is a static
file in the host project's repo, beside the documents the method already keeps there. That file's
update rides the landing's own commit. Its published copy sits at one stable link in the human's
browser, updated from that same source file. The person opens the board from any device, with no
server of the pack's own.

The named-reference machinery [E-35] runs in two placements the table already names. The two presence gates run client-side at gate time. The non-empty description-field gate `guardrails/check-description-field.py` runs at commit and push time in the repo, with its CI mirror as a second net. The agent-channel deposit-time lint `guardrails/check-deposit-description.py` runs the moment an agent deposits a `from-<agent>` inbox file. That run happens in the depositing session, on the author's own machine [target]. The earned auto-deposit [T-24] and the living-description overwrite [INV-240] are behaviours of the model in the writing session, reading the installed skill text.

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
| frontend / visual (fullstack app · static site · photo portfolio) | the visitor walk (first visit · return · cross-entry · from-any-point navigation · exits) · the feel pass scaled to a whole site (motion quality, affordance craft against the prototype bar) · motion and scroll feel as the human's gate · **interactive controls that belong to different layers occupy separate screen space** (the interactive-overlap rule) · cross-surface policy uniformity [INV-125] · paired-transition symmetry [INV-126] · **a legibility floor** — text meets a minimum contrast ratio against its background and a minimum size (SPEC INV-139) · **the seam between the build and the configuration** — an experiment switch, a piece of copy, a threshold or budget, and a feature toggle reach production by a deploy of configuration alone, while behaviour and structure stay in the code the build ships (SPEC INV-291) | the walk and the feel pass are the human's eye-walk [INV-30, INV-77]; the interactive-overlap rule, the policy-uniformity and paired-transition rules each get a browser or pixel-level row in the adopting project's suite; the legibility floor is read at the verify feel pass (a product surface's computed colours/sizes) and at the pre-show gate (`scripts/preshow-legibility-lint.py` on the styled file), its browser-computed row living in the adopting project's suite; the build-and-configuration seam is declared at founding on the host's `project.config-surface` line and read by `guardrails/check-config-surface.py`, its proof by deed the owner turning a switch in production while no build runs |
| code / backend service | the promised flows all reachable · error and empty states answered · latency and error-rate budgets held · **the seam between the build and the configuration** — an experiment switch, a piece of copy, a threshold or budget, and a feature toggle reach production by a deploy of configuration alone, while behaviour and structure stay in the code the build ships (SPEC INV-291) | integration tests and the budget rows [INV-41]; the build-and-configuration seam is declared at founding on the host's `project.config-surface` line and read by `guardrails/check-config-surface.py`, its proof by deed the owner turning a flag or a budget in production while no build runs |
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

## Quality budgets

What quality means for a skill pack, in numbers [INV-41]. Numbers proposed by the agent, tunable on
the human's word [INV-70]. Each is asserted by a matrix row, and its instrumentation home is where the
real number is read.

| Budget | Number | Instrumentation home | Watcher |
|---|---|---|---|
| full suite wall-time | ≤ 1780 s on the dev machine [default] (written with no thousands separator, because `check-suite-budget.sh` reads the figure with `grep -oE '≤ *[0-9]+'` and a comma would truncate it) — what it counts: the serial wall-time of one full `python3 -m pytest -q` run at 2,506 tests with the suite-in-suite meta-test firing; the decision it informs: a push may proceed. Derived 2026-08-13 at 03:03 from the seven full runs of the 2026-08-12 evening pass, in the order they were taken: 1,221.81 s, 1,281.39 s, 1,304.65 s, 1,605.37 s, 1,559.15 s, 1,387.88 s and 1,451.77 s. The bound is the slowest of them plus a tenth as headroom, the same slowest-plus-spread method the 2026-08-07 row used when it put 74 s on a 726 s run. Read the spread before the number: the same suite on trees differing by a handful of documents ran 1,221.81 s and 1,605.37 s, a 31% swing, while the code added across the whole pass measures under a second. This budget is reading the machine's load, and it refused three pushes tonight on that reading alone. Queue row 622 asks for a measure that survives a shared machine, and queue row 553 owns the one code term that dominates every run, `tests/test_guardrails.py` at 640.59 s. Until one of them lands, the ceiling sits above the loudest measurement the day produced. The figure it replaces read ≤ 1410 s, derived at 20:08 on 2026-08-12 from four runs of 993.31 s, 1,159.75 s, 1,221.81 s and 1,281.39 s. Before it the row read ≤ 1280 s, derived at 16:00 the same day from runs of 1,159.75 s and 993.31 s. Before it the row read ≤ 800 s, derived on the morning of the same day from runs of 516.86 s, 537.39 s and 726.28 s, and the whole rise sits in one file: `/usr/bin/time -p python3 -m pytest tests/test_guardrails.py -q` measured **640.59 s** at 15:58, against the near-282 s this row claimed for it, so that one file is 55% of every full run. Queue row 553 holds the work that brings it down and now carries the fresh measurement. Direction: re-measured at every landing, and it falls when the suite gets faster. The row it replaces before that read ≤ 605 s at 2,492 tests, derived 2026-08-07 from 473/525/539 s plus that day's 66 s load spread; before it, 474 s at 2,502 tests on the morning of 2026-08-07, one second above its own measurement, which is the headroom that redded a push on a working machine; before it, 470 s at 2,404 tests on 2026-08-06 and 383–405 s at 1,856 tests on 2026-07-24. The meta-test's own file takes 640.59 s of the run as measured on 2026-08-12, so a diff outside the gate-machinery class skips it and runs far shorter. Queue row 553 holds the work that brings this number down by narrowing the meta-test's own run | the pytest tail line in the suite run's log, read by `guardrails/check-suite-budget.sh` on every full gate run and red past the budget naming both figures (M-346, row 361) | `guardrails/check-suite-budget.sh` reds past the budget on every full gate run, naming both figures (M-346) |
| skill evals | every per-skill scenario green at each milestone | dated run records in `docs/evals/` | the eval suite reds any red scenario at each milestone run (INV-99) |
| resume-file form | `NEXT_STEPS.md` is a digest with no redundancy, one live-state block (INV-48; the numeric cap struck on the owner's ~01:10 word, row 576) | the suite's own check and the prose-level census | `test_template_states_the_law` holds the template's statement of the law, and the census record holds the file's prose level (INV-48) |
| spec prose register | style lint: 0 errors on PRODUCT_SPEC.md | `scripts/spec-style-lint.py` JSON tail | the style-lint gate reds on any error at the pre-show and push gates (INV-83) |
| work board update [target] | ≤ about 5 s from the stage change it records [default], and no stage delayed by its own board update | the page's own build stamp — the time the generator last wrote the page, read off the rendered board | the generator's own suite timing assertion at its landing (ROADMAP row 166); until that landing the budget stands unwatched [target] |
| settings card render | ≤ 1 s on a pack-sized catalog [default] | the render script's own run, asserted by its matrix row | its matrix-row test (M-206) reds past the 1 s budget, read from the render script's own instrumentation |

A skill's judgment quality beyond the evals has no honest number. It is said by name here and judged
by the human's eye on real landings, never given a vanity metric.

## Decisions — where they live

The pack's decisions live in three homes already. The first is the queue's dated rows, each landing's
verdicts inline. The second is JOURNAL.md's chapters, which hold the why. The third is DECISIONS.md's
open-decision entries: D-1, D-6, D-7, covering attic layout, pair queue view, and engine-fact
citation. They moved there from the retired Formal index at the 4.0.0 format migration, and the spec's
`[GAP: ...]` lines now point to them. This section is the doc's one entry point to them, and it holds
pointers rather than the decisions themselves. Structure-changing decisions also appear in the
architecture prover record at `docs/prover/architecture-prover-record.md`, one line each. Every full
pass that proves this document beside the spec appends its dated row to that prover record (INV-116).
Those passes run at an M-1 milestone gate and at an M-6 push gate. The gate walk carries the duty, so
the record stays current with the architecture's freshness rule rather than trailing it. The M-1
milestone gate also runs the design review on the re-proven spec (INV-141). Its dated design-review
record lands in `docs/design-review/`, beside the prover record. A structure-changing design decision
it settles appears in that prover record's rows like any other.

*Coverage rule (walked at matrix derivation): every spec anchor appears in some node's "owns" column. An
orphan fact means a missing node or a missing assignment. A node that owns nothing has no spec backing,
and that is itself a finding. Mechanized in `tests/test_traceability.py`.*

**Boundary health — a typical request lands in one node (SPEC INV-128).** A right node boundary shows
one sign. An edit inside a node leaves its neighbours untouched, so a typical request's footprint is
single-module. When requests repeatedly cut across the same several nodes, the boundary sits in the
wrong place. The signal is the entry impact read recording a cross-cutting footprint on the same node
pair again and again. The recorded footprints are the evidence a boundary move rests on. A boundary
moves only through the architecture step and its re-prove, as a restructure row [E-14, and INV-37 in
the spec]. It never moves on a guess, and it never stays wrong in denial while the cross-cuts pile up.
The **cross-cut counter** mechanizes the signal. `guardrails/crosscut_counter.py` reads the closed
queue's cross-cutting landings. It counts, per unordered node pair, how many cross-cutting changes
touched both nodes. A pair reaching the threshold, 3 by default and tunable, is flagged for the MINOR
audit as a boundary-move candidate. That is the mechanized form of "seen twice, own it" (base rule 19)
applied to boundaries. The flag is an audit signal, never a per-push red. The count is evidence the
MINOR audit weighs. The boundary still moves only through the architecture step and its re-prove
[INV-37]. This law states the bar and the signal; the counter is the recorded footprints made
countable.
