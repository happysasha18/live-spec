## Requirement 159: Reading the whole product map on demand  [feature: F-feature-map]

**Context:** Three standing questions describe the product: the departures board reports in-flight status, intake places each new wish on the map, and this ask answers the third — what the product does today. It answers with one map current as of the request, read live from the living documents, kept in no separate file. The map lists the requirements carrying a feature name, which are the things the product gives a person; the requirements without one state the machinery behind those things and stay off the map. The reading is done by the session that was asked, following the reporting skill's own text.

**User Story:** As a person asking what the product does today, I want one whole map read live from the spec and the queue on demand, so that I get a current answer with no third document to maintain or drift.

### Acceptance Criteria

**Case: the map is read live, with no third document**

1. *when* a person asks what the product does today, the system *shall* answer with the whole product map current as of the request, read from the spec's scenario sections, the header's current-versus-target paragraph, and the queue's open rows. [INV-38]
2. The system *shall* keep no third document for the map — no feature-list file and no cached copy — the spec's scenarios and the architecture's nodes constituting it. [INV-38, E-14]
3. The system *shall* separate shipped features from promised features at the granularity the target tag binds to — the scenario and its named promised parts, marking a scenario that holds both as shipped with named promised parts. [INV-38, S-0]

**Case: each line and how it is delivered**

4. The system *shall* give each map line its echo-name, what the feature gives its person, and the feature's status followed by its station, per the line law. [INV-38, INV-28]
5. The system *shall* deliver the map in chat by default and as a rendered page on request, *shall* keep routine reports at the departures board's in-flight scope, and *shall* return the whole map only on request. [INV-38, INV-27]

**Case: a host with nothing to read**

6. *if* a host has no spec and no scenario sections, *then* the system *shall* state that condition, direct the requester to bootstrap or adoption, and report only what currently exists. [INV-38]

**Case: the fences and the coverage measure**

7. The system *shall* hold the departures board's report scope, intake's placement rule, and the no-third-document law unchanged. [INV-27, INV-37, E-14]
8. The system *shall* yield a map whose feature set covers the spec's tagged scenarios one to one plus every open queue row that wish intake marked a new feature while its scenario stays unwritten. [INV-38, INV-37]
9. The system *shall* say, on a map a person reads, that a requirement carrying no feature name states machinery behind the product and names no thing the product gives them, and *shall* claim no coverage of those requirements. [INV-38, INV-321]
10. The system *shall* draw the map when a person asks for it, and *shall* claim no drawing of the map's own accord and no command that produces it. [INV-38, INV-321]

