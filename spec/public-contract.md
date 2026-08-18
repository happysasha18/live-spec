## Requirement 194: A published contract is read on the reader's own clock  [feature: F-contract]

**Context:** A consumer agent arrives here from the scan holding a producer's card and the path its artifact lives at. A published contract is a surface in the producer's own spec, paired with a machine-readable artifact carrying its own version and generation stamp. The consumer reads it read-only on its own clock, and data past its staleness bound stops the analysis.

**User Story:** As a consumer agent needing another agent's numbers, I want to read its published contract on my own clock rather than ask it, so that I depend on a stated, versioned interface instead of an unstamped snapshot.

### Acceptance Criteria

**Case: the contract and its artifact**

1. a published contract *shall* be a surface in the producer's own spec, written, proven, and tested where the producer's other surfaces are and earning its feature coverage there. [E-33, INV-73]
2. each contract field *shall* name what the field means, the window it is measured over, how it is aggregated, and the source it derives from, and the reviewer *shall* read a field missing any of the four as an incomplete surface. [E-33, INV-101]
3. the published artifact *shall* live at the path the producer's card names and *shall* state the contract version it was generated under and the moment it was generated, so a reader tells its shape and its age from the artifact itself. [E-33, E-32, E-14, INV-24]

**Case: nothing publishes by default**

4. a contract *shall* publish no field until the owner records an explicit permission for it in the producer's tree with its date and author. [INV-185, INV-24]
5. a field with no recorded permission *shall* stay in the producer's tree, the way a neighbour's product is built granting no permission, and the reviewer's review *shall* read a declared contract's fields against their permission records. [INV-185, INV-150]
6. credentials *shall* cross no channel under any permission, the published artifact being the one road a producer's product data takes between two agents. [INV-185, INV-183]

**Case: the producer's cadence**

7. the producer *shall* declare one cadence — how often it regenerates the artifact — and *shall* hold to it whatever its consumers do, a deploy refreshing the artifact as a bonus and never triggering it. [INV-186]
8. the producer's own session-start check *shall* fail *when* its scheduled regeneration did not run, beside the pack-update check that runs there, and the consumer's staleness bound *shall* stand as the second, independent watcher that catches a producer gone quiet. [INV-186, INV-187, E-25]

**Case: the consumer's read**

9. the consumer *shall* declare one staleness bound — how old the artifact may be for its analysis — and its freshness check *shall* fail past that bound before any analysis runs. [INV-187, INV-41]
10. the consumer *shall* pin the contract version it was written against and *shall* carry a compatibility test that fails *when* its pinned version and the artifact's version diverge. [INV-187]
11. the consumer *shall* read the artifact read-only — over the filesystem when co-located, over git when remote under its recorded read grant — and *when* the generation stamp reads past its staleness bound it *shall* name the stale data aloud and stop. [INV-187, INV-112, INV-232, INV-67]

**Case: two numbers, set apart**

12. the cadence and the staleness bound *shall* be two numbers set independently, and neither side *shall* read the other's. [INV-186, INV-187]

**Case: data reads, it never asks**

13. a consumer wanting a producer's data *shall* read the contract rather than send a message asking for it. [INV-188]
14. *when* a consumer wants a field the contract lacks, the system *shall* treat it as a request about the contract's shape, which the earned message governs. [INV-188, INV-189]

**Case: the default-deny gate is promised**

15. the gate that reds a default-deny violation on the producer's suite *shall* stay promised until a host's first real contract. [INV-185]
    [target]

---

