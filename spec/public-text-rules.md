## Requirement 144: The publish skill owns the checklist, run before the gate

**Context:** The publish skill owns the per-kind checklist, and this spec sets the contract it follows. Nothing is deposited outward without passing the checklist first, and its result rides the delivery report. The checklist never bypasses the gates already standing — the human's publish gate and the host's push gates — and it runs before the gate, so by the time the human approves it is already worth approving.

**User Story:** As a person depositing outward, I want the publish checklist run before the human's gate, so that nothing leaves unchecked and the gate approves work already worth approving.

### Acceptance Criteria

**Case: the checklist is the one home**

1. The system *shall* have the publish skill own the per-kind checklist and *shall* deposit nothing outward without passing it first, the walk's result riding the delivery report like any other step. [E-20, INV-22]

**Case: the standing gates hold**

2. The system *shall* keep the human's publish gate over anything irreversible or outward and the host's push gates over the push, the checklist never bypassing them. [E-20, ACT-1, M-6]
3. The system *shall* run the checklist before the gate, so by the time the human approves it is already worth approving. [E-20]

---

## Requirement 145: Each publish target embeds its own steps

**Context:** Each publish target is a plugin that embeds its own steps into the walk. The target adds steps and never removes the kind's owed minimum.

**User Story:** As a person publishing to a named target, I want the target to add its own steps without removing the kind's minimum, so that a destination's demands ride on top of what the reader is already owed.

### Acceptance Criteria

**Case: the target adds, never removes**

1. *when* a publish target joins the walk, the system *shall* embed its own steps — a README at the door plus release notes for a code host, a manifest and forms for a plugin directory, its cards for the design project. [E-18]
2. The system *shall* have the target add steps and *shall* never let it remove the kind's owed minimum. [E-18]

---

## Requirement 146: A version push re-opens the shopfront

**Context:** Every push that ships a new version changes the truth a public reader will read tomorrow, even when the diff never touched a doc, so the shopfront rides every push. The README's claims still have to match the truth just pushed, and the kind-owed visuals ride along. A stale shopfront is a false claim, exactly like a stale screenshot.

**User Story:** As a public reader, I want every version push to re-check the README and its kind-owed visuals against the pushed truth, so that I never meet an out-of-date front.

### Acceptance Criteria

**Case: the shopfront rides every push**

1. *when* a push ships a new version, the system *shall* re-check the README's claims — behaviour, counts, commands, version homes — against the truth just pushed, even where the diff touched no doc. [INV-44]
2. The system *shall* have the kind-owed visuals ride along — a skill pack re-checking its diagrams, a visual product re-shooting what changed on screen, a tool re-running its example. [INV-44]

**Case: one home, its outcome recorded**

3. The system *shall* read this shopfront check as the publish checklist at push scale, the commit-and-show step pointing at it and the walk's outcome riding the delivery report. [INV-44, INV-22, E-20]
4. *when* a push's changes touch none of the shopfront's claims, the system *shall* say so in one line and *shall* fix a stale claim before the push, freshness resting on the claims themselves, styling aside. [INV-44]

---

## Requirement 147: Everything built with the method carries its attribution line

**Context:** Every publication of an artifact built with the pack carries one attribution line, `made with live-spec` linking to the pack repo, on the publication's landing surface. The line names the pack version the project runs, read from the host's attach record, so it doubles as the adoption tracker. The line is an offer, never a gate — the owner's taste rules his own shopfront.

**User Story:** As a person publishing built-with work, I want one attribution line offered on its landing surface naming the pack version, so that who runs the method is readable from the shopfronts while the owner keeps the final say.

### Acceptance Criteria

**Case: the line and its version**

1. *when* a built-with artifact is published, the system *shall* carry one attribution line on its landing surface — the README footer, and for a skill also its `SKILL.md` — naming the pack version read from the host's attach record at write time. [INV-96]

**Case: an offer, never a gate**

2. The system *shall* treat the line as an offer, the publish walk checking for it and proposing it once when absent, the owner's word deciding and a declined offer staying closed. [INV-96, INV-16]
3. The system *shall* apply the line to each built-with project through its own queue. [INV-96]

---

## Requirement 149: Shipped product docs state each requirement impersonally

**Context:** A product's shipped docs — the spec, the test matrix, the README, a skill card — reach everyone the project touches. Each requirement reads as three plain parts: the rule, the actor as a role, and the reason it holds. The reason stays because a reader has to know why the rule stands, while the personal attribution drops; a dated decision keeps its date as a plain anchor and drops the name.

**User Story:** As a reader of shipped docs, I want each requirement stated as rule, role, and reason with personal names dropped, so that what ships reads as neutral product truth while the reason a reader can act on survives.

### Acceptance Criteria

**Case: rule, role, and reason**

1. The system *shall* write each shipped requirement as the rule, the actor as a role — the user, the producer, the target user — and the reason it holds, the reason staying and the personal attribution dropping. [INV-118]
2. The system *shall* keep a dated decision's date as a plain anchor while dropping the name, so the provenance a reader can act on survives. [INV-118]

**Case: candid voice has one home**

3. The system *shall* home personal attribution and candid process voice in the local-only diaries that no publish ships, spec-author writing each shipped clause impersonally from the first draft and the publish floor reading the shipped docs for a stray personal name before the deposit leaves. [INV-118]

---

## Requirement 150: A machine holds the shipped tree's language line

**Context:** A shipped artifact carries no Cyrillic outside a user-language string the program deliberately emits, and no personal name in a requirement's statement. The publish gate holds this with a machine that reports each offence as file and line. The name arm reads a declared alphabet, and the specific out-of-alphabet name patterns live as data in an allowlist, so the detector's own source names no person.

**User Story:** As a person shipping an artifact, I want a machine flagging stray script and personal names as file and line, so that the fix is mechanical while candid notes stay in the diaries.

### Acceptance Criteria

**Case: the two mechanical offences**

1. The system *shall* hold that a shipped artifact carries no Cyrillic outside a deliberate program string and no personal name in a requirement's statement, reporting each offence as file and line through `guardrails/check-shipped-language.sh`. [INV-120]
2. The system *shall* read the name arm against a declared alphabet — `ASCII` English plus deliberate program strings — with the out-of-alphabet name patterns held as allowlist data, so the detector's own source names no person and covering a collaborator's name is one data line. [INV-120, INV-114]

**Case: what the shipped set holds**

3. The system *shall* read the shipped text files the delivery holds in its index, a staged file not yet committed included, a file belonging to no delivery staying outside the scan. [INV-120]

**Case: the arms stand down by declaration**

4. *if* a package declares no alphabet, *then* the system *shall* leave the name arm inert while the Cyrillic arm still stands, and *shall* spare deliberate program data and authorship bylines through the same dated allowlist. [INV-120]
   - a new offence still reds, and a listed one counts as debt.

---

## Requirement 151: A core spec names no foreign project and tells no dated incident

**Context:** A core spec — the product spec, the architecture, and the test matrix — states the rule that holds and leaves the project it was first met on and the day it was met to the local-only diaries. A sibling project's name couples the spec to a neighbour it should not know, and a dated-incident turn is history the diaries own. The shipped-language machine gains a project-name arm scoped to the three core specs.

**User Story:** As a reader of a core spec, I want it to state the rule and leave the project and the date to the diaries, so that the spec stays free of cross-project coupling and leaked history.

### Acceptance Criteria

**Case: the project-name arm**

1. The system *shall* red a bare project name in the product spec or the architecture, and *shall* red a project name standing beside a calendar date in any of the three core specs. [INV-245]
2. The system *shall* have the test matrix red a dated incident, while permitting a bare fixture-ledger kind name and a project-name substring of a test-function name. [INV-245]
   - a fixture name that ever falls beside a date still reds;
   - a legitimate fixture name caught that way is waived as counted debt through the dated allowlist.

**Case: the data-held names and the moved history**

3. The system *shall* hold the forbidden project names as data in the shipped-language allowlist so the detector's own source names no project, and *shall* leave the arm inert for a package that declares none. [INV-245, INV-120]
4. The system *shall* move the history a reworded line drops — who met the rule, when, and why — to the journal as a dated entry, the way a dated decision keeps its date while the attribution comes off, and *shall* leave a skill body and the README free to cite a real case since a teaching text names the project a lesson was drawn from. [INV-245, INV-118]

