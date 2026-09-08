# Notes beside q-829, from its global push review

True things the global review of the 6.1.1 push noticed outside what it blocks on. One paragraph
each. Nothing here opens a row or asks for a repair; the intake sweep decides whether any of it is
owed one.

`guardrails/judge-hooks.json` says in its own opening comment that every file under `hooks/` must
appear in exactly one of the two lists, `wired` and `library`. Twenty files ship under `hooks/` and
nineteen stems are listed; `dialog-warning-guard` is in neither. It has its own installer, so
nothing is broken by it, and it predates this push — the delta only reopened the file.

The comment this push added to that same file, `_file_comment`, says every stem that ships as a
file of its own carries a `file` entry, wired or library alike. Four stems that
`scripts/install-pack-hooks.sh` ships carry none: `language-laws`, `turn_reader`,
`register_judge_core` and `register-judge`. Nothing reads `file` for those four today —
`scripts/install-session-hooks.sh` reads it only for the three wired stems, and the data files ride
the `data` map by filename — so the sentence overstates what the map holds rather than breaking a
reader.

`scripts/checkpoint.py`'s `update_checkpoint(allow_closed=True)` is documented as writing "one line
into DONE and changes nothing else". That is a property of its one caller, not of the parameter:
driven directly, the flag lets a closed checkpoint's DONE, IN PROGRESS and NEXT bodies all be
replaced wholesale, with the status left reading closed. No caller in the tree reaches that today,
and the only route to the flag is `task-admission._write_anchor`, which passes `done` alone.

`matrix/build-pipeline.md` marks M-660 and M-663 as *todo* while naming
`test_manual_mode_starts_only_on_a_persons_own_command_and_decides_no_verdict` and
`test_a_run_ends_only_the_process_group_it_started`, both of which exist in
`tests/test_run_modes.py` and pass. Their neighbours in the same block read *built* on the same
kind of evidence.

`scripts/install-pack-hooks.sh`'s new refusal runs before any file is copied, so the first hook
that reaches `hooks/` without an installer stops the whole install — including the refresh of the
drifted copies that config-health (push gate m, the check that every installed hook matches its
source) is red about. That is the recurrence-stop working as written; it is worth knowing that the
day it fires, the fix has to land before any hook can be refreshed.

The installer no longer marks `.md` and `.json` files executable, which is right, but it only
copies a file whose content differs. A machine that ran an earlier version still carries
`language-laws.json` at mode 755 and nothing will lower it, since config-health compares content
and not mode. This machine's own `~/.claude/hooks/language-laws.json` is in that state.

plan-11's acceptance command reads red on this machine, naming q-827, q-828 and q-829 as undrawn.
The cause is that `board.html` was last rendered at 13:10 today, before those three rows reached
the plan; the page is gitignored and CI draws a fresh one before gate v, so this is local only and
it was already red at `origin/main`. `bash scripts/render-board.sh` clears it.

`tests/test_release_6_1_1.py`'s `test_every_file_under_hooks_reaches_the_installed_set` opens by
saying "Three of the twenty files are placed by their own installers", and the set it then builds
names five. The assertion is right; the sentence above it counts wrong.
