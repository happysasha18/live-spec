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
- INV-302 (the two session steps sit beside the checkpoint and resume rules — rule 35's own informal restatement retired to attic, unbacked by an eval fixture or an executable script. Both steps stay a discipline the seat holds; the session extract's machine, `scripts/session-extract.py`, is the guardrails node's.)

**pins** —
- `skills/live-spec-base/SKILL.md:55` (rules)
- `skills/live-spec-base/SKILL.md:105` (rule 6 checkpoint incl. INV-107 closing half)
- `skills/live-spec-base/SKILL.md:123` (rule 7 fence, INV-10/INV-11)
- `skills/live-spec-base/SKILL.md:233` (rule 16, prototype fence)
- `skills/live-spec-base/SKILL.md:249` (rule 22, INV-98 — the convergence principle)
- `skills/live-spec-base/references/settings-ladder.md:1` (ladder — the on-demand module beside the rulebook; `skills/live-spec-base/SKILL.md:454` carries the pointer to it)
- `skills/live-spec-base/references/settings-ladder.md:43` (defaults incl. `budget.pressure` — the economy ladder's setting; the rungs' one home is the SPEC's economy-ladder section)
- `skills/live-spec-base/SKILL.md:303` (rule 26, INV-136/INV-139 — a project kind declares design principles the verify pass runs; the per-kind table lives in this doc)
- `skills/live-spec-base/SKILL.md:311` (rule 27, INV-143 — the seat decides what it can decide, surfaces only what it cannot)
- `skills/live-spec-base/SKILL.md:340` (rule 31, the earned-message law INV-183/INV-189 the named-reference machinery joins. The pair-travels register [E-35], the living-description heal [INV-240], and the earned auto-deposit [T-24] ride this rule's build, ROADMAP 424 [target]. The prover's station stands as their net until they ship, per [INV-150].)
- `skills/live-spec-base/SKILL.md:150` (rule 7's worker-restore sub-rule, INV-298 — the worker holds its own bytes, halts when it holds none, and the orchestrator owns recovery)
- `attic/live-spec-base-unbacked-rules-2026-08-26.md:1` (rules 11, 14, 15, 18, 19, 20, 21, 23, 28, 32, 33, 34, 35 — cut whole, per PLAN.md step 7: covered by neither an eval fixture nor an executable script. INV-23, INV-65, INV-84, INV-108, INV-145, INV-217, INV-237, INV-247, INV-302 stay owned as formal PRODUCT_SPEC.md requirements; only their informal SKILL.md restatement moved.)

**notes** — INV-11, INV-117, E-31: three of these are read by the parallel-lanes node and stay here, each for a stated reason; INV-225: ROADMAP 388

### [node: host-contract]

**responsibility** — the recorded settings instances. Those are this host's profile, the human's personal profile, and the thin loader that boots the personal layer. The agent records sit here too: the self-declaring card in each agent's own tree, found by the pack's live scan.

**owns** — E-8, E-16, E-32, INV-184 (the card's flag at founding and at adoption's orient is carried by attach as wiring; ownership stays here)

**pins** — `.live-spec/profile.md:1` (host), personal: `~/.claude/live-spec/profile.md` (symlink → playbook repo `personal/profile.md`, its git home), loader: `~/.claude/CLAUDE.md:1` (thin loader live)

### [node: onboarding-card]

**responsibility** — the settings card. A build-time renderer parses the base's package-defaults table and the profile files into the card page, per the frozen norm. The card is shown at the end of founding or adoption, and on the standing "what can I customize?" question (F-attach).

**owns** — INV-87, INV-88

**pins** — `scripts/onboarding-card.py:1` (renders the card), `docs/norms/onboarding-card-2026-07-10.html` (the frozen norm), trigger wiring: `adopt/ADOPT.md` (setup-end line) + `skills/communicator/SKILL.md` (standing-question line) — wiring pins, ownership stays here
