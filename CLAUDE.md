# live-spec

The single entry point is `PLAN.md`. Read it whole before anything else.

The first action of every session is `bash scripts/state-probe.sh`. It prints the state a session
used to inherit as prose — where the tree stands, which plan step is open, and what has drifted.

Do not read the prose in this root to orient yourself. `JOURNAL.md`, `ROADMAP.md`, `PRODUCT_SPEC.md`
and their neighbours run to more than a megabyte between them, and none of them says where the work
stands today. Open one only when a step names it.

If the session has drifted, the owner asks it to check against the plan. That means: run the probe,
read `PLAN.md` whole, look at `git log --oneline -15`, `git status` and what is on disk, then report
in `Canon:` and give a separate line to everything that disagrees between the plan, the repository
and the disk. Change nothing until he answers.
