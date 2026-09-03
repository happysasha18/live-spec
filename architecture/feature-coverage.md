## Feature coverage

The feature layer above the anchor matrix (SPEC E-29, INV-73). live-spec's primary unit is its
person-facing scenario. Each such heading in PRODUCT_SPEC.md carries an inline `[feature: F-x]` tag.
The table below maps every unit to the node or nodes that implement it, and to a test that exercises
it. The check runs both ways (`tests/test_traceability.py`, `TestFeatureCoverage`). Every tag is a row
here and every row is a tagged scenario. Every named node is real, and every named test exists. The infra machine package-docs implements guarantees rather than user features and sits outside this layer by the project type's own definition. guardrails sits outside it too, except for the prototype fence: the mechanical check is itself the person-facing guarantee, so F-prototype names it as an implementer. host-contract sits outside it for its settings arm and inside it for the agent records. The card is a person-facing surface an agent reads, so F-roster and F-agent-birth name it as an implementer [E-32, INV-184].

A name stands here only for a scenario the product performs today [INV-132]. A scenario still promised
carries its `[target]` marker in the spec and no feature name, and it takes its name in the change that
lands its build; the check reds a tagged scenario carrying that marker, so a promised surface cannot
reach this table by borrowing a neighbour's test. One thing a person is given carries one name: the
five entry conditions into attaching the pack to a project — a fresh host, a project already running,
a host moving to a newer pack, an engine and its instance taken as a pair, and the settings card that
closes any of them — are one thing under the one name F-attach, and its row names every test that
exercises one of its entries.

| feature | implemented by | test |
|---|---|---|
| F-first-read | director | test_the_grader_fails_a_wrong_verdict, test_new_checkpoint_director_requires_decision_sheet |
| F-wish | build-pipeline, parallel-lanes, communicator | test_capture_echo_and_board |
| F-prototype | guardrails, build-pipeline | test_prod_reference_fails |
| F-publish | publish | test_publish_skill_carries_checklist |
| F-feedback | feedback-intake, communicator, feedback-collector | test_feedback_routes_have_homes |
| F-feature-map | communicator | test_feature_map_on_demand |
| F-bug | build-pipeline | test_gap4_recurring_bug_escalates |
| F-problem-ledger | base-rulebook, templates | test_problems_template_shape |
| F-attach | attach, templates, onboarding-card | test_scaffold_bootstrap_runs, test_adopt_phases_cite_spec, test_pair_leadership_law, test_onboarding_card_completeness, test_catchup_walk |
| F-roster | host-contract, base-rulebook | test_card_and_scan_law |
| F-agent-ask | base-rulebook, inbox | test_earned_message_names_its_block |
| F-agent-birth | build-pipeline, host-contract | test_agent_birth_walk |

Two names left this table rather than standing on nothing. The published contract had no producer, no
consumer and no artifact anywhere on this machine, and its own requirement holds its enforcing gate
promised until a first contract arrives; the requirement stands with its `[target]` marker and takes
its name back when a host publishes one. The work board's page, source file, generator and validation
check were specified and none was built, and its row here had been naming the capture-echo test that
belongs to F-wish; that requirement retired on 2026-09-03 with the queue row that carried it, so the
name has nothing left to return to and the retired text rests at `attic/spec-work-board-R309.md`.
