### [node: publish]

**responsibility** — the publish-quality gate: per-kind publication checklist (its one home) + the target-plugin seam; runs before the human's gate, never instead (row 98)

**owns** — E-20, INV-44, INV-96, INV-119, INV-228

**pins** —
- `skills/publish/SKILL.md:1` (frontmatter + when it fires)
- the kind-checklist table and target-plugin sections in the same file
- the release-note shape with its optional offers section (INV-228: the shape carries an optional offers section phrased as choices. The publish walk records the offer-or-none decision, consuming the touchpoint-frame classification.)

### [node: design-sync]

**responsibility** — an optional machine, [target: machine; wiring live]. A landing's declared components sync to the team's design project, human-gated (ROADMAP row 93). The machine's first real run remains.

**owns** — E-18

**pins** —
- wiring: `skills/live-spec-base/references/settings-ladder.md:60` (defaults table, `design-sync` row)
- wiring: `skills/communicator/SKILL.md:183` (rule 5's channel line)
- machine: —

### [node: feedback-collector]

**responsibility** — the outbound feedback arm, the pack's third arrow. On a rare genuinely-strong reaction it offers, with the human's positive consent, to draft a distilled non-public upstream note to the pack's authors. It deposits that note in the gitignored `outbox/` and sends nothing, so delivery stays the human's own step. It is off by default, under the `feedback-upstream` flag. It stands apart from feedback-intake, the inverse arrow, and from the measurement family (ROADMAP row 321).

**owns** — E-30, T-21, INV-161, INV-179

**pins** — `skills/feedback-collector/SKILL.md:1` (frontmatter + when it fires), the offer / upstream-note / outbox sections in the same file
