## Requirement 200: The human owns the taste calls and the working contract

**Context:** The human owns taste, design, the irreversible and publish and push gates, domain wording, and the human's own working contract. The settings ladder resolves to that contract before every human-facing exchange. Mode and trust are set only on the human's word; the agent may propose a level and never raises its own.

**User Story:** As the person a project serves, I want taste and the gates and my own working contract to stay mine and my mode and trust set only on my word, so that every call that turns on taste or preference rests with me.

### Acceptance Criteria

**Case: the human owns the taste calls**

1. The system *shall* keep taste, design, the irreversible and publish and push gates, domain wording, and the human's working contract with the human. [ACT-1, INV-9]
2. Communicator *shall* resolve the whole settings ladder to the working contract before every human-facing exchange, reading the resolved contract rather than one file. [E-13]

**Case: mode and trust move only on the human's word**

3. The system *shall* set proactivity mode and trust only on the human's word, and the agent *shall* propose a level while it never raises its own. [INV-9]
4. The system *shall* hold the lines about the human — proactivity mode, trust, language, and domain vocabulary — in the human's personal profile, following the human across every project. [E-13]

**Case: the host profile lives with the host**

5. The system *shall* create the host profile at attach and keep it git-tracked in the host repository beside the adopt artifacts. [A-8, E-8]
6. The system *shall* keep only the checkpoints ignored inside `.live-spec/`, every other host-profile line staying tracked. [ACT-3, E-8]

---

## Requirement 201: A done-claim is settled by an evidence walk

**Context:** A fluent story can answer any done-claim and might even be right, yet it does not tell a verified fact from a narrated one. So no one answers a done-claim from memory: every claim pins to a checkable artifact walked fresh — an adoption record, a prover record, a suite run with its count, a git commit, a matrix row. The answer states what the walk verified apart from what it merely asserts and names the method version the work was done under.

**User Story:** As a person asking whether a piece of work is done, I want the answer walked fresh from claim to artifact to method version, so that a done-claim rests on freshly checked evidence.

### Acceptance Criteria

**Case: the claim walks its evidence**

1. *when* a done-claim is answered, the system *shall* walk it fresh from the claim to a checkable artifact to the method version, and *shall* state what the walk verified apart from what it merely asserts. [INV-25]
2. The system *shall* read the method version from the host's installed set, naming the pack and skill versions from their version homes. [INV-25, M-7]
3. The system *shall* answer no done-claim from memory, treating a claim with no walked artifact behind it as unproven. [INV-25]

**Case: the version is named or its absence is**

4. The system *shall* name the method version on the claim line, so one claim line reads claim, then artifact, then version. [INV-25, M-7]
5. *if* the host carries no installed set, *then* the system *shall* say exactly that, an absent version being an honest answer and never an invented one. [INV-25, M-7]

---

## Requirement 202: Settings climb a four-scope ladder and the narrowest word wins

**Context:** Every way the pack behaves for the human is a named setting with a home in exactly one of four nested scopes: the package defaults, the personal profile, the host profile, and the session's live word. The scopes nest, and resolution reads from the narrowest outward — the session word over the host, the host over the personal profile, the personal profile over the package default. Profiles are re-read at the same freshness points as skills.

**User Story:** As a person whose preferences live at different scopes, I want each setting resolved from the narrowest scope outward, so that a project or a single sitting can override a broader default on my word.

### Acceptance Criteria

**Case: each setting has one scope and the narrowest wins**

1. The system *shall* give every setting a home in one of four nested scopes — the package defaults in the base skill, the personal profile, the host profile, and the session's live word. [E-13, E-12, E-8]
2. The system *shall* resolve a setting from the narrowest scope outward, the session word overriding the host, the host overriding the personal profile, and the personal profile overriding the package default. [E-13]

**Case: profiles are re-read and an unreadable line is ignored aloud**

3. The system *shall* re-read profiles at the same freshness points as skills. [A-7]
4. *when* a profile line falls outside the current pack's vocabulary, the system *shall* ignore it aloud through a dated journal note and a line in the session's next status report, the journal note standing even *if* the session dies before its report. [E-13]

---

## Requirement 203: No override is ever silent

**Context:** An override exists only as a written line in the profile it governs, and setting one leaves a dated note in that home's journal — the host's journal for a host line, the package's journal for a default change. This is the no-silent-micro-decisions rule applied to settings.

**User Story:** As a person auditing how the pack was tuned, I want every override written as a profile line and journaled where it governs, so that no setting changes silently and the record stays readable.

### Acceptance Criteria

**Case: an override is written and journaled**

1. The system *shall* record every override as a written line in its profile file and *shall* leave a dated journal note in the home it governs. [INV-14, INV-5]
2. The system *shall* journal a host line in the host's journal and a default change in the package's journal. [INV-14]

**Case: a tighter host line is recorded**

3. The system *shall* let a host contract tighten a package default and *shall* record the tighter line where a reader sees it rather than assume it. [M-6, INV-14]
4. The system *shall* keep the push gate's own cadence as the worked example, the package default asking a full prover pass before a minor bump and a host contract tightening it to before every push. [M-6]

---

## Requirement 204: The session scope is never a file

**Context:** The session scope is the one scope that is never a file: a session override lives only in the human's spoken word and dies with the conversation, and the agent never writes it on its own. Should it outlive the session, that is a promotion into the profile it describes, made on the human's word and journaled. A full wipe ends the sitting and the session lines die with it by design.

**User Story:** As a person setting something for one sitting, I want the session override to live only in my spoken word and die with the conversation unless I promote it, so that a passing choice never silently becomes permanent.

### Acceptance Criteria

**Case: the session word dies with the sitting**

1. The system *shall* keep a session override only in the human's spoken word and *shall* never write it to a file on its own. [INV-14]
2. *when* a session override should outlive the session, the system *shall* promote it into the profile it describes on the human's word and journal it like any other override. [INV-14]

**Case: a wipe ends the sitting**

3. *when* an announced self-compaction runs, the system *shall* carry the live session lines forward in its summary. [M-2, INV-14]
4. *when* a full wipe ends the sitting, the system *shall* let the session lines die with it, since that loss is the human's own move. [INV-14]

---

## Requirement 205: The personal layer has one home and the loader stays thin

**Context:** Everything personal lives in one place, the personal profile, and the machine-global instruction file shrinks to a thin loader carrying only the bootstrap lines that must hold before any pack file loads. Migrating an existing rule file into this shape forks each rule to the scope it describes — a method rule stays the pack's, a personal line moves to the profile, a project line moves to that project's host profile. A rule-by-rule mapping proves the move lossless and the old file stays in the attic.

**User Story:** As a person consolidating a tangled rule file, I want each rule forked to the scope it describes with the old file kept in the attic, so that the personal layer has one home and one move rolls the whole change back.

### Acceptance Criteria

**Case: one home and a thin loader**

1. The system *shall* keep the personal layer in the personal profile and *shall* shrink the global instruction file to a thin loader carrying only the bootstrap lines that must hold before any pack file loads. [E-16, INV-13]
2. The system *shall* keep the loader the one home for those bootstrap lines and *shall* never restate them in the profile. [INV-13]

**Case: a rule file forks by scope, losing nothing**

3. *when* an existing rule file is migrated, the system *shall* fork each rule to the scope it describes. [E-16, INV-10]
   - a method rule stays the pack's;
   - a personal line moves to the profile;
   - a project line becomes a migration note for that project's own session to land.
4. The system *shall* prove the move lossless rule by rule and *shall* keep the old file in the attic, so one move rolls the change back. [E-16, INV-7]
5. *while* the promotion sits outside any repository fence, the system *shall* re-read the file immediately before appending, its git home standing as the recovery net. [INV-11, E-16]

---

