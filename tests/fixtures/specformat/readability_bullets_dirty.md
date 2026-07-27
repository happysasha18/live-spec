# Mini spec — one bullet defect per readability arm

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
   - the widget renders in the place the panel names and leaves every other panel on the screen untouched while it renders, since a panel that moves under a reader's hand costs the reader the line they were holding and the place they had reached.
2. *when* the panel opens, the widget *shall* name its owner. [INV-2]
   - the owner — the person whose queue row created the panel and holds its pen — reads the name first.
3. *when* a run ends, the system *shall* file the report. [INV-3]
   - the report closes the run, the rest becoming queue rows.
4. *when* the gate runs, the system *shall* red the row. [INV-4]
   - the row cites [INV-5] as its reason.
