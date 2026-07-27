#!/bin/sh
# The chat clock's mechanical hand (row 134, SPEC INV-24 chat face): wired as a
# UserPromptSubmit hook in ~/.claude/settings.json, it injects the wall clock into
# every prompt's context so the reply's leading stamp reads off the machine, not
# off the hand. Repo home: hooks/clock-hook.sh; installed copy: ~/.claude/hooks/.
date '+Wall clock at this prompt: %H:%M, %d.%m.%Y. Lead the reply with a [HH:MM] read off this clock (later if work ran long since) — never a continued or extrapolated stamp.'
