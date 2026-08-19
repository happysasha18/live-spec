### [node: text-audit]

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-446 | A changed human-facing section ships only after the mechanical lints run clean and two consecutive fresh cold reads return zero blocking findings; a reader sent while the mechanical layer reds, a fifth round with new blocking findings and no escalation, or a reader-named source hole with no queue row reds; never a section shipped on one clean read alone [INV-266, INV-267, INV-268] | string | the text-audit loop's own suite (planned; the skill file `skills/text-audit/SKILL.md` bodies the loop today) | *todo* |

