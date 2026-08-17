# Mini spec

This is a preamble. It states what the codes are: bracket codes like `INV-1` trail each criterion and point to the rule's home. A reader can ignore them.

## Glossary

- **widget** — one unit the product shows to a person.
- **panel** — the surface a widget sits on.

## Requirement 1: A widget shows on its panel

**Context:** The product shows widgets to a person. A person opens a panel. The widget appears on it. The person reads what the widget shows.

**User Story:** As a person opening a panel, I want its widget to show, so that I see what the panel holds.

### Acceptance Criteria

**Case: the widget shows**

1. *when* a panel opens, the system *shall* show its widget. [INV-1]
2. *if* the panel holds no widget, *then* the system *shall* show a placeholder. [INV-2]
3. *if* the panel holds no widget, *then* the system *shall* name that panel in the placeholder. [INV-2]

## Requirement 2: A widget closes cleanly

**Context:** A person is done with a widget. The person closes the panel. The widget leaves the screen with nothing left behind.

**User Story:** As a person done with a widget, I want the panel to close cleanly, so that nothing lingers.

### Acceptance Criteria

**Case: the panel closes**

1. *when* a person closes a panel, the system *shall* remove its widget from the screen. [INV-3]
