# Mini spec — the same four rules, written in bullets to the bar

This is a preamble. Bracket codes like `INV-1` trail each criterion and point to the rule's home. A reader can ignore them.

## Glossary

- **widget** — one unit the product shows to a person.
- **panel** — the surface a widget sits on.
- **owner** — the person whose queue row created a panel and holds its pen.

## Requirement 1: A widget shows on its panel

**Context:** The product shows widgets to a person. A person opens a panel. The widget appears on it. The person reads what the widget shows.

**User Story:** As a person opening a panel, I want its widget to show, so that I see what the panel holds.

### Acceptance Criteria

**Case: the widget shows**

1. *when* a panel opens, the system *shall* show its widget. [INV-1]
   - the panel names the place;
   - the widget renders in that place;
   - every other panel on the screen stays untouched while the widget renders.
2. *when* the panel opens, the widget *shall* name its owner. [INV-2]
   - the owner reads the name first.
3. *when* a run ends, the system *shall* file the report. [INV-3]
   - the rows the report leaves open return to the queue.
4. *when* the gate runs, the system *shall* red the row. [INV-4]
   - the row cites its reason.

**Case: the sub-list ends where the criterion ends**

5. *when* the panel closes, the system *shall* drop the widget. [INV-5]

- this bullet sits at column zero, outside any criterion, so no criterion reads it, and it is long enough that a criterion which did read it would run past the word cap and red the long-criterion arm.
