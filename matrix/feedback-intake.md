### [node: feedback-intake]

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-172 | The feedback-intake skill ships: SKILL.md loads (frontmatter name + version), states the three channels (spoken/typed · comment on something shown · dropped file via the inbox door) and the ledger's home and line shape (when · who/channel · concerns · plain words · route); never a skill file without the channels or the ledger shape [E-28] | string | `test_feedback_intake_ships` (red proven against HEAD — file absent there) | *built* |
| M-173 | The routing table names every route with its home (wish→queue row · fix→commit+journal · answer→archive+harvested row · field evidence→ledger line · workshop noise→problem ledger) and both fire sides (fires on receipt and at inbox sweep; never on the agent's own output, never opening a queue row on its own judgment); never a route without a named home [T-20] | string | `test_feedback_routes_have_homes` | *built* |
| M-174 | The never-lost law agrees across its three surfaces: the spec's INV-68 index line, the skill's own text, and inbox/README.md all speak route-homes (same session · one echo per item · re-mention appends its date · only the assigned session writes the ledger, outsiders via inbox); never a surface still speaking the old wishes-only harvest [INV-68] | string | `test_feedback_never_lost_in_both_homes` | *built* |

