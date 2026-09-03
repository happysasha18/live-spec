# Every project gets its own status view
Status: open
Owner: director

## DONE

(nothing yet)

## IN PROGRESS

(nothing yet)

## NEXT

(nothing yet)

## DECISION SHEET

Goal: the plan/probe/board trio (state-probe.sh, render-board.sh, plan_checks.py, plan-step.sh) becomes an installable, host-path-generic template a host adopts through the pack's own install walk, proven against a real host (tlvphotos), per PLAN.md's own plan-14. Outcome: bash <host>/scripts/state-probe.sh prints that host's own tasks with marks computed by that host's own checks, and lists its unhandled inbox files; grep finds no hard-coded host-directory roster inside this pack's own state-probe.sh (today's one hardcoded line: 'for h in ~/tlvphotos ~/exhibition-engine ~/promoter ~/promoter-alexander ~/tc-cloud-validate' at scripts/state-probe.sh:360 -- read from a profile-declared host list instead, the same settings-ladder pattern lanes.cap already uses). Dimensions: architecture (a real generic/specific split inside plan_checks.py -- CHECKS.get() is baked directly into parse_tasks() at line 459, coupling the generic parser to this project's own project-specific check registry; this is the actual reason a prior session judged this not a mechanical narrowing); cross-project (install-walk wiring, a new adopt/install-*.sh installer following the exact pattern install-scaffold.sh/install-style-gates.sh already set: vendor + pin in ratchet-manifest.json + print manual steps); quality (new tests proving genericity: a scratch host with its own PLAN.md and its own CHECKS gets a working probe/board with zero of this project's own task ids/content bleeding in). Known: adopt/ADOPT.md's own 'Installing the gates' section is the exact wiring point and pattern to follow; this project may only write inside its own tree, and touches tlvphotos only via a dry run on a throwaway clone (the established precedent from plan-9's own migration dry-run) plus one inbox wish for tlvphotos's own session to run the real install -- never a direct write to that live host. Unknown: exact shape of the host's own profile line naming its status-view path (grep the host-drift section in state-probe.sh for the existing pattern reading .claude/skills/live-spec-base/SKILL.md's version, which already reads a profile-relative path). Risk: real -- this walk is what every future adoption depends on; a wrong wiring choice is hard to unwind, per this row's own 31.08 finding. Specialist: opus-tier worker (judgment: the generic/specific split of plan_checks.py, and getting the installer pattern right on the first real try) -- this is exactly the class of work the profile's worker-tier rule calls a justified exception to the sonnet default. Evidence: new tests (a scratch-host fixture, the same harness tests/test_scaffold_install.py already uses for the other three installers) red-then-green proving zero project-specific content leaks into a fresh host's copy; a dry run against a throwaway clone of tlvphotos showing the installed trio prints that clone's own tasks; full suite green. Next: dispatch worker with this brief, adopt/ADOPT.md's 'Installing the gates' section, scripts/plan_checks.py, scripts/state-probe.sh, scripts/render-board.sh, and adopt/install-scaffold.sh (as the pattern to match) as primary sources.
