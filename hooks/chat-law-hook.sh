#!/bin/sh
# UserPromptSubmit hook: one-line reminder of the seven session laws, names only.
# Shrunk 2026-08-17 on the owner's word (was ~4.5 KB of full one-line texts per prompt;
# the pre-shrink text stands in this repository's history, as this file at commit ca2d31f).
# Full law texts live in ~/.claude/live-spec/profile.md and
# ~/.claude/skills/live-spec-base/SKILL.md — open them when a law needs its wording.
# Repo home: hooks/chat-law-hook.sh; installed copy: ~/.claude/hooks/.
echo 'Session laws (live-spec), names only — full texts: ~/.claude/live-spec/profile.md and ~/.claude/skills/live-spec-base/SKILL.md. Act on them: 1 answer-first · 2 plain words, codes trail in parentheses, narrate the work · 3 industry words in chat; run scripts/preshow-register-lint.py before showing an artifact · 4 no contrast frames ("X, not Y") · 5 routing: this seat briefs and accepts, workers execute (opus=judgment, sonnet=mechanical multi-step, haiku=single step) · 6 re-test a deferral by derivability before parking it · 7 every work block and report line opens by naming its root (his request or standing instruction).'
