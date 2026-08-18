## Requirement 177: Adoption runs as an ordered set of phases  [feature: F-adoption]

**Context:** Adoption attaches the pack to a project already under way. It runs as a sequence where each phase finishes before the next starts, and it assumes no blank slate. The version-control gate runs first so the whole run stays reversible.

**User Story:** As a person attaching the pack to a running project, I want adoption to read everything first and re-engineer it into the pack's shapes without trusting or losing anything, so that the existing work is preserved and checked before it is trusted.

### Acceptance Criteria

**Case: orient and inventory**

1. *when* adoption begins, the system *shall* read every existing document — README, roadmap, spec, test suite, journals, TODO files, and repo wikis — before touching anything, and *shall* answer the founding questions about what was found. [A-1]
2. *when* orient completes, the system *shall* list the code, the user-facing surfaces, and the document set, each entry named with its owner, and surfaces named to file and line. [A-2]
3. Listing the surfaces *shall* seed the host's surface registry. [E-10]
4. The system *shall* keep adoption's working artifacts — the orient digest, the inventory, the reconcile notes — in the host's `.live-spec/adopt/`, tracked in git, and *shall* keep them out of the host's own folders. [A-8]

**Case: re-engineer the documents**

5. *when* the system re-engineers an existing spec, the system *shall* keep its claims as spec sections and mark them unverified. [A-3]
6. The system *shall* seed the architecture document's nodes from the inventory's file-and-line entries, turn existing tests into matrix rows cited at their real level, and turn an existing roadmap or TODO into queue rows. [E-14, E-15]
7. The system *shall* reconcile every unverified claim — pin it to file and line, or remove it — at the first delivery that touches its surface, or by the first milestone, whichever comes first. [A-3]

**Case: version-control gate, baseline, and incremental**

8. The system *shall* run the version-control gate before touching or moving anything. [A-5]
9. The system *shall* save a first baseline snapshot of the host's artifacts as found, git-tracked, as the diff baseline the snapshot machinery guards. [A-6, E-7]
10. *when* the earlier phases are done, the system *shall* run the host on the same request lifecycle as a bootstrapped host, and *shall* record the installed skill versions in `.live-spec/` at attach time. [A-7]
11. *when* the pack's version or an installed skill's version changes, the freshness check *shall* re-read the changed skill before continuing and write a one-line journal note naming old and new. [A-7, M-7]
12. *when* a safe breakpoint is reached, the freshness check *shall* re-stat the installed skills and the pack on disk and re-read whatever changed, and *shall* ask the public repo once a day whether the pack has moved. [A-7, M-2, E-25]

---

