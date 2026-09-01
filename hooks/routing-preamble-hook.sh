#!/bin/sh
# UserPromptSubmit hook: injects the routing preamble — a one-line reminder of the zone-referral
# law (Requirement 196 [INV-190], spec/roles-and-agents.md) into every prompt's context, so a
# request meant for another adopted project's zone is caught before the session acts on it here.
# The hook only reminds; it never rewrites, redirects, or silently resends the person's own
# message (spec/roles-and-agents.md, Requirement 196 criterion 21). Sibling to
# hooks/chat-law-hook.sh — same shape, same install path.
# Repo home: hooks/routing-preamble-hook.sh; installed copy: ~/.claude/hooks/.
echo 'Routing preamble (live-spec) — before acting: if this request names or belongs to another adopted project zone, refer it back to whoever asked rather than acting on it here [INV-190, spec/roles-and-agents.md Requirement 196]. Say the referral in chat, or on the reply road when an agent asked; never rewrite, redirect, or silently resend the message itself.'
