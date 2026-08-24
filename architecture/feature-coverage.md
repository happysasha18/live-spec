## Feature coverage

The feature layer above the anchor matrix (SPEC E-29, INV-73). live-spec's primary unit is its
person-facing scenario. Each such heading in PRODUCT_SPEC.md carries an inline `[feature: F-x]` tag.
The table below maps every unit to the node or nodes that implement it, and to a test that exercises
it. The check runs both ways (`tests/test_traceability.py`, `TestFeatureCoverage`). Every tag is a row
here and every row is a tagged scenario. Every named node is real, and every named test exists. The infra machine package-docs implements guarantees rather than user features and sits outside this layer by the project type's own definition. guardrails sits outside it too, except for the prototype fence: the mechanical check is itself the person-facing guarantee, so F-prototype names it as an implementer. host-contract sits outside it for its settings arm and inside it for the agent records. The card is a person-facing surface an agent reads, so F-roster and F-agent-birth name it as an implementer [E-32, INV-184].

| feature | implemented by | test |
|---|---|---|
| F-wish | build-pipeline, parallel-lanes, communicator | test_capture_echo_and_board |
| F-prototype | guardrails, build-pipeline | test_prod_reference_fails |
| F-publish | publish | test_publish_skill_carries_checklist |
| F-feedback | feedback-intake, communicator, feedback-collector | test_feedback_routes_have_homes |
| F-feature-map | communicator | test_feature_map_on_demand |
| F-bug | build-pipeline | test_gap4_recurring_bug_escalates |
| F-problem-ledger | base-rulebook, templates | test_problems_template_shape |
| F-bootstrap | attach, templates | test_scaffold_bootstrap_runs |
| F-adoption | attach | test_adopt_phases_cite_spec |
| F-pair | attach | test_pair_leadership_law |
| F-onboarding | onboarding-card, attach | test_onboarding_card_completeness |
| F-catchup | attach | test_catchup_walk |
| F-roster | host-contract, base-rulebook | test_card_and_scan_law |
| F-contract | spec-author, base-rulebook | test_contract_default_deny |
| F-agent-ask | base-rulebook, inbox | test_earned_message_names_its_block |
| F-agent-birth | build-pipeline, host-contract | test_agent_birth_walk |
| F-work-board | work-board, communicator | test_capture_echo_and_board |

The work board's row names a test that exists. That test exercises the neighbouring status-view
promise the board extends — the capture echo and the departures board this page grows out of. The
board's own tests arrive with its build (ROADMAP row 166), and the row's test cell is re-pointed at
them then.
