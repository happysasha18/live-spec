### [node: director]

**responsibility** — the first reader of a person's message. It decides which of the seven acts the message carries before anything answers it or changes a file, opens work only behind an act that asked for work, writes the decision sheet into that work's own checkpoint, and names which accepted work runs next. It stands in front of the walk below rather than inside it: the pipeline's stations begin once this node has said the message was an instruction.

**owns** —
- E-36 · INV-316 · INV-317 (the first read, the acceptance door, and what holds them)
- INV-318 · INV-319 (the decision sheet in its one checkpoint, and the order accepted work runs in)
- E-37 · INV-320 (the idea shelf. Its requirement carries the `[target]` marker: no file holds the shelf, no command writes to it, and no test reads it. The pins below reach the two lines of the skill that name it and the eval field that grades whether a scenario shelved.)

**pins** —
- `skills/director/SKILL.md:25` (the seven acts and the table that decides between them — the first read's one home)
- `skills/director/SKILL.md:213` (the decision sheet's fields, in the order the sheet writes them)
- `skills/director/SKILL.md:38` (the idea act's own row, the line that names the idea shelf)
- `scripts/checkpoint.py:55` (the one place the checkpoint machinery couples to this node: an owner reading `director` is what makes a decision sheet required at creation and at validation)
- `evals/director/check.py:1` (the grader that judges a recorded run against its written scenario. It is deterministic and it calls no model; the run it grades is produced elsewhere and stored, so the score speaks about the recorded runs rather than about today's session)
- `evals/director/scenarios.json:1` (the written scenarios and their expected verdicts — the goal this node's reading is measured against)
- `scripts/state-probe.sh:261` (the probe's own arm: it prints the score at a session's start and says plainly when the traces are older than the skill, so a replay of old runs is read as saying nothing about the skill as it stands)

**notes** —
- Nothing on this machine puts a message through this node. The pack ships no hook on message arrival and no gate that reads a transcript for the reading; the door is a sentence in the person's boot file that a session reads and follows. INV-317 is the requirement that states so, and a reader who takes it at its word will find no wire to look for.
- The idea shelf is the one part of this node with nothing behind it at all. It is specified and marked promised.

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
- `skills/director/references/work-kind-table.md:4` (the door + work-kind relationship — the door picks which steps run, this table picks the form each running step takes)
- `skills/build-pipeline/SKILL.md:21` (the craft ladder — step→craft one home, Requirement 51 backs it at the SPEC level)
- `skills/director/references/work-kind-table.md:1` (the work-kind table — per-kind meanings' one home)
- `skills/director/SKILL.md:260` (steps — the dynamic Execution graph that replaces the old fixed nine-step sequence)
- `skills/build-pipeline/SKILL.md:45` (gates — the MINOR-bump gate, this node's own remaining "Gates worth remembering" section)
- `skills/architect/SKILL.md:141` (re-carve paragraph — INV-113 redesign-owes-rework)
- `skills/director/references/delegation-protocol.md:71` (the worker-brief register-laws clause — no-scissors + no-dramatization, INV-221)
- `guardrails/check-tier-refusal.py:1` (the tier-refusal gate. It reads the record's shape and a pattern's evidence. Its `--brief` step turns a matching task away before any model call. It rides the suite, taking no gate letter, INV-300)
- `guardrails/tier-refusal.json:1` (the instruction, the tier ladder, the promotion threshold and the promoted phrases as data, INV-300)
- `docs/measure/tier-refusals.md:1` (the refusal record the patterns grow from, INV-300)
- `tests/test_tier_refusal.py:1` (its red proof, INV-300)

**notes** —
- INV-247: standing beside the queue-take trigger re-scan [INV-129]. That reads whether the row returns, and this reads whether its described internals still hold.
- INV-247: homing the spec clause (rule 34's informal restatement retired to attic). INV-247: ROADMAP 430.
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
- `skills/director/references/lanes-and-pen.md:32` (the penless overlap set, the pen-stages, and the re-fence after a landing)
- `skills/director/references/lanes-and-pen.md:13` (the graph picks the lane set at queue-take)
- `skills/director/references/lanes-and-pen.md:59` (a mid-work re-door re-runs the independence edges against every rolling lane)
- `skills/live-spec-base/SKILL.md:127` (rule 7's lanes sub-rules — three lanes under one pen; the cap and the lane-open act have their one home here, and the director's reference points at it rather than restating it)
- `skills/live-spec-base/SKILL.md:145` (one row per landing commit)
- `scripts/open-lane.sh:1` (the lane-open act's performable form. It carries the row→in-work claim commit on main, the cap refusal, and the lane branch cut into its own worktree, INV-214.)
- the lane-opening script is the first file this node owns of its own. Its law otherwise lives inside the two skills that perform it and its cited pins there. The branch road's carriers land with ROADMAP row 386 [target].

**notes** —
- the node's live half is carried in shipped skill text today and pinned above. That half is the pen and the claim's atomicity, the cap, the graph, and the one-row landing commit with its clean-tree precondition. It also holds the re-fence after a landing and the independence re-check a re-door fires.
- the branch road is specified with its carriers still ahead. Those carriers are the lane branch and its walk, the pen-moves-main clause, the fast-forward landing, the conflict law, and the vendored project-instructions line. The road rides ROADMAP row 386 [target], with the prover's station as its net meanwhile.
- also carries the mechanism the worktree-isolation default fires. The condition itself and the session identity the pen tie-break orders on stay base-rulebook's.
- the restructure merge gate stays product-prover's, since it judges a restructure's delta by token identity. An ordinary lane's landing gate is the full suite on the rebased tree.
