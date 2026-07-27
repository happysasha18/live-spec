# Mini spec — the readability arms' clean side

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

1. *when* a panel opens, the system *shall* show its widget in the place the panel names, and *shall* leave every other panel on the screen untouched while it renders. [INV-1]
2. *when* the panel opens, the widget *shall* name its owner before it renders. [INV-2]
3. *when* a run ends, the system *shall* file the report, and the rows the report leaves open *shall* return to the queue. [INV-3]
4. *when* the gate runs, the system *shall* red the row. [INV-4, INV-5, INV-6]
