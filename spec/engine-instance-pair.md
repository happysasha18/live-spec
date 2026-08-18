## Requirement 187: Running an engine and its instance as a pair  [feature: F-pair]

**Context:** When founding takes the engine-and-instance split, the two repos run as a pair. Each repo is a full host with its own spec, queue, journal, and settings folder. No third document spans the pair. A lesson crosses between the two only through the inbox.

**User Story:** As the owner of an engine-and-instance pair, I want each repo to run as its own full host with the inbox as the only cross-seam channel, so that one window serves one repo and neither half writes the other's tree. [INV-86]

### Acceptance Criteria

**Case: each repo is a full host**

1. Each repo of the pair *shall* carry its own spec, queue, journal, and `.live-spec/` folder, and no third document *shall* span the pair. [INV-86, E-1, E-14]
   [GAP: whether one reading view is stitched across the pair's two queues, or strictly two are kept, is an open decision; today's practice is two plain queues, recorded open in DECISIONS.md. D-6]
2. The engine's spec *shall* state what the mechanism does for any instance and *shall* cite no instance's content; the instance's spec *shall* state what the product is for its real user and *shall* cite the engine only by its content-contract handles. [INV-79, INV-86, D-7]
   [GAP: whether the instance's spec may cite engine facts, or only the content-contract handles, is an open decision; today's practice is handles-only, recorded open in DECISIONS.md. D-7]

**Case: wishes and lessons cross the seam**

3. *when* a request is shaped for both engine and instance, the system *shall* split it at intake into one queue row in each repo, each citing the one spoken request. [T-17, INV-1, INV-37]
4. The system *shall* keep each repo's own inbox as the place outside items arrive; the instance's inbox is where the human hands in requests. [E-11, INV-37]
5. *when* a lesson travels between the two, the system *shall* carry it only through the inbox under write-ownership: the learning window files one new inbox file in the other repo and journals the hand-off in its own tree, writing no foreign tree beyond that one file. [E-11, INV-10, T-10]
6. One window *shall* serve one repo of the pair, *shall* stay read-only on the other half save for that one inbox file, and *shall* keep the concurrent-edit fence binding inside each repo. [INV-10, INV-11, INV-86]

**Case: the load-bearing crossing**

7. *when* the human throws a request at the instance window and intake finds a generic part and the instance's own part, the system *shall* route each part to its own home. [INV-37, T-17, E-11, INV-10, INV-56]
   - the generic part is filed as one engine inbox request;
   - the instance's own part is parked as a dated blocked-on-engine debt line;
   - this keeps the lane moving.
8. The dated debt line *shall* appear in the instance's every status report until the engine ships the request. [INV-27]
9. *when* the engine's session sweeps its inbox, the system *shall* land the request through the full pipeline on the engine's generic fixtures, make each new plug-in point a named content-contract entry with a works-without-it test, and ship and version on the engine's own rhythm. [T-10, INV-79, E-3]
10. *when* the engine ships, the system *shall* update the instance to that engine version, plug the real content into the new entry, verify on the real product, un-park the parked row, and close it whole. [INV-56, T-17]

**Case: the engine's spec carries its own provenance**

11. The engine's spec *shall* cite only the engine's own public commits for provenance and *shall* give each mechanism a neutral name in the engine's own vocabulary. [INV-119]
12. *where* a running instance shows a locale-specific label for a mechanism, the engine's spec *shall* note that string as instance-supplied copy and *shall* keep the neutral term as the mechanism's one name. [INV-79, E-4]
13. The publish gate *shall* check a generalized pack for two leaks: a private-instance provenance hash, and an instance's locale label standing as a mechanism name. [E-20, INV-119]

---

