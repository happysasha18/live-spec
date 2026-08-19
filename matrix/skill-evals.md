### [node: skill-evals]

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-086 | Every working skill owns an eval file: scenario · criteria · dated bare-run record (red proven, never asserted) · re-run instructions; the required set derives from skills/ itself, so a fifth working skill is red until its eval exists; never a skill without its eval [E-19] | string | `test_skill_evals_present` | *built* |
| M-087 | The eval method states its honest boundary (bare = bare-of-the-SKILL, the machine loader still feeds method) and the authoring rule (the scenario speaks like the human — no enumerated facet hints); run records are dated and append-only; evals re-run at milestones (M-1 list) and at behaviour-changing skill landings; never a contaminated red sold as clean [E-19] | string | `test_eval_readme_states_honest_boundary`; re-run discipline: milestone audit (M-1) | *built* |

