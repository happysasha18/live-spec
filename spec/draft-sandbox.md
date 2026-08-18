## Requirement 98: A prototype is a fenced sketch that carries its label  [feature: F-prototype]

**Context:** Exploring an idea before committing to it is allowed, and a prototype is that exploration kept as a sketch. It lives fenced off in its own clearly named home, and the fence runs one way — influence crosses out of the prototype and never into the shipped product. Every artifact the prototype produces announces itself.

**User Story:** As a person exploring an idea, I want the sketch fenced off and labelled in whatever form its kind can show, so that a try-it-out experiment never leaks into the product a user meets.

### Acceptance Criteria

**Case: the label rides every artifact**

1. *when* a prototype produces an artifact, the system *shall* mark it with the `PROTOTYPE` label in the form its kind can show — an on-screen banner for a rendered page, a `_prototype: true` field or header for an API or data payload, a first-line banner for a script, and the marker in the name or header line for a bare file. [E-17]
2. The system *shall* keep the prototype's code sitting apart in its own named home, with nothing in the shipped product reaching into it. [E-17]

**Case: the fence runs one way**

3. The system *shall* let influence cross out of a prototype and never into a prod surface: never wiring a prototype into a prod surface, never linking to a prototype from a prod surface, and never styling a prod surface to match a prototype. [INV-17]
4. *when* a prototype is shown to the human, the system *shall* show it only under its label, and *shall* let nothing reach the human as the product until its surface has walked the full pipeline. [E-17, INV-17]

---

