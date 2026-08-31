## Requirement 186: The settings card shows at setup and answers the standing question  [feature: F-attach]

**Context:** At the end of founding, and again at the end of adoption's orient, the system renders the settings card. The human reaches it twice — here at setup without asking, and any later time by asking. The card shows what the pack has set up and what is the human's to change, and asks nothing.

**User Story:** As a person new to the pack, I want the settings card shown at setup and re-rendered whenever I ask what I can customize, so that I see every setting and change any of them by speaking its change-line. [INV-87]

### Acceptance Criteria

**Case: the card shows at setup's end**

1. *when* founding ends, or adoption's orient ends and the project kind and the economy setting have settled, the system *shall* render the settings card. [INV-87, INV-36]
2. The card *shall* list every setting the pack knows, each row giving the setting's plain-words name, its current value for this host where one is recorded, and one line saying how to change it in plain speech. A recorded default *shall* be shown as told, and the card *shall* ask nothing. [INV-87, INV-31]
3. The system *shall* read each value from the settings ladder — the reader's own profiles and this host's recorded lines. [E-13, INV-87]
4. *when* the card opens, the system *shall* open it by the show rule, and *shall* pass the pre-show register lint on the fixed copy and the rendered values before it opens. [INV-67, INV-83]

**Case: the same card answers the standing question**

5. *when* the person later asks what they can customize, in any wording, the system *shall* answer with the same card re-rendered from the current truth, and *shall* let no hand-kept copy answer. [INV-87]

**Case: one catalog home**

6. The card and the standing answer *shall* derive from one source: the pack-defaults table joined with the reader's profile files and the host's recorded lines. No second hand-kept settings list *shall* exist. [INV-87]
7. Every card-visible table row *shall* appear on the card, every recorded profile line *shall* appear in the card's project-rules part, and every card row *shall* trace to a marked table row or a recorded profile line; a missing card-visible row and a card row with no source *shall* each be a defect. [INV-87]

**Case: the copy states rules, values stay the reader's own**

8. The card's fixed copy *shall* state each setting as a rule anyone can read, and *shall* show a personal value — a language, a name — only as the reader's current value, labelled as theirs to change. [INV-88]
9. The fixed copy *shall* never present one person's value as the product's prescription. [INV-88]

**Case: the render and its states**

10. A build-time script (`scripts/onboarding-card.py`) *shall* render the card from the pack-defaults table and the profile files, and *shall* fail the render loudly on a malformed table row. [INV-87]
11. *if* the personal profile is missing, *then* the script *shall* render the card on pack defaults, say plainly that no profile exists yet, and name how the founding offer creates one. [INV-87]
12. *when* the pack-defaults table grows a row, the system *shall* draft that row's card rule-copy on the clean-writer road before it first renders. [INV-84]

**Case: the card's facets**

13. *when* the viewport is a phone, or a window too narrow to hold multiple columns, the card *shall* read as one column top to bottom; on a window wide enough to hold them it *shall* keep its multi-column arrangement. [default] [INV-87]
14. The card *shall* be a static rendered page, plain structured HTML with headings and keyboard scrolling, and *shall* depend on no hover. [default] [INV-87]
15. The card's empty state *shall* be a missing personal profile, its error state a malformed catalog row, and its blocked state flagged text at the register lint. [INV-87, INV-83]
   - empty shows pack defaults, says the absence plainly, and names the founding offer;
   - error's render fails loudly;
   - blocked stops the showing until the text is fixed, and names what it flagged.
16. Rendering the card *shall* be read-only, so two sessions can render it at the same time; an open card *shall* show the truth of its render moment, and a later change *shall* not update the open page. [default] [INV-87]

---

