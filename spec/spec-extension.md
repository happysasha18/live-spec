## Requirement 316: A rule in this document names what makes it happen

**Context:** This document states what the product does. Behind each rule stands one of four carriers: a command the machine runs, an instruction a session reads and follows, a surface drawn when somebody asks for it, or nothing yet. A rule that reads the same whichever of the four stands behind it tells a reader the product is stronger than it is. So a rule says which carrier it has, and a rule with nothing behind it takes the `[target]` marker this document's opening explains.

**User Story:** As a person deciding what to rely on, I want each rule to say what makes it happen, so that I can tell a rule a machine holds from a rule that rests on a session remembering to follow it.

### Acceptance Criteria

**Case: each rule names its carrier**

1. *where* a command, a gate, or a test performs the behaviour a criterion states, the criterion *shall* name that command, gate, or test. [INV-321]
2. *where* only a skill's own text asks a session to perform the behaviour, the criterion *shall* say so and *shall* claim no command, gate, or hook behind it. [INV-321]
3. *where* the behaviour is a surface drawn when somebody asks for it, the criterion *shall* name the act that draws it and *shall* claim no drawing of the surface's own accord. [INV-321]
4. *where* the tree holds nothing that performs the behaviour, the requirement or the criterion *shall* carry the `[target]` marker. [INV-321]

---

## Requirement 317: The spec is one document written across a core and its parts

**Context:** The spec grew past one file. It is a core file carrying the opening, the glossary, and a parts map, followed by the part files that map names, read in the order the map gives. Every reader — a person, a session, or a check — reads the core and its parts as one text. A part file the map names nowhere is read by nobody, and a requirement number claimed twice makes one citation point at two rules at once.

**User Story:** As a person reading one rule of the spec, I want the whole document to be exactly the files its own map names, so that the rule I read is the rule the system holds and its number points at one place.

### Acceptance Criteria

**Case: the core names every part**

1. The system *shall* read the spec as the core file followed by the part files the core's parts map names, in the order that map gives. [INV-322]
2. *when* a part file is added, the system *shall* add its row to the core's parts map in the same change. [INV-322]
3. *where* a file sits among the parts the map names and the map names it nowhere, `guardrails/check-index-generated.py` *shall* red and *shall* name that file. [INV-322]

**Case: a number names one requirement**

4. The system *shall* let one requirement number stand for one requirement across the whole document. [INV-323]
5. *where* two parts open one requirement number, `guardrails/check-index-generated.py` *shall* red and *shall* name the number and the lines that open it. [INV-323]

**Case: who opens a change to this document**

6. The system *shall* open a change to this document only from work a person accepted, and *shall* let a delegated worker write only the part its brief names. [INV-322, INV-317]
7. The system *shall* carry the map law and the number law into the architecture and the test matrix, which are written in this document's format and split the same way. [INV-322]

---
