# live-spec

The first action of every session is `bash scripts/state-probe.sh`. It prints the state a session
used to inherit as prose — where the tree stands, which plan step is open, and what has drifted.

The single entry point is `PLAN.md`, but a session taking a step does not read it whole: it opens
that one step with `bash scripts/plan-step.sh <id>` (plan-17). Reading the whole file more than
doubles a session's starting weight for no reason tied to the step in hand — read it whole only
when the work itself is about the plan's shape (adding a task, the fallback below).

Do not read the prose in this root to orient yourself. `JOURNAL.md`, `ARCHITECTURE.md`, `PRODUCT_SPEC.md`
and their neighbours run to more than a megabyte between them, and none of them says where the work
stands today. Open one only when a step names it.

If the session has drifted, the owner asks it to check against the plan. The recovery procedure is
`PLAN.md`'s own property, not restated here — see its "Fallback when drifted" section. This file
only needs to say where to look; two homes stating the same steps is the exact "two homes for one
fact" drift this project's own rules forbid.
