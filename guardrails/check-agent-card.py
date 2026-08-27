#!/usr/bin/env python3
"""check-agent-card.py — a live-spec host tree carries its agent card (SPEC INV-219, gate y).

INV-184's declaration law: a tree's presence grants nothing and writing a card grants everything.
A host tree standing on a mission with no `.live-spec/agent.md` is undeclared — an agent no other
window can find, address, or read a zone from. The law flagged a card-less tree where its siblings
are flagged (beside the project kind [INV-36] and the declared layers [INV-135], the sibling of
the kind-with-no-layers flag [A-10]) and named the mechanical gate reading a tree for its card as
ROADMAP row 387's [target] — a declared law with no net ranking as a broken invariant [INV-101].

This gate is that net. It reads a tree root and reds when the root carries no `.live-spec/agent.md`,
naming the missing card and the one act that supplies it. The pack itself is a host — its own first
host [INV-97] — and carries its own card, so the default read passes; that honest self-application
is what keeps the gate from reddening this very push. For every OTHER standing host the duty binds
forward [INV-159]: a pre-law tree writes its card at its catch-up walk [A-11], and adoption's own
document `adopt/ADOPT.md` names the card so the walk knows to write it.

The gate reads the pack root by default; `AGENT_CARD_TREE` overrides the root a host's own push
gate reads its own tree, and the red-proof points it at a card-less temp tree. Discovery of OTHER
agents' cards under nearby roots stays the live scan [E-32]; this gate reads one tree — the host's
own — the way the pack's own suite reads its own card on disk.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

TREE = os.environ.get("AGENT_CARD_TREE", REPO_ROOT)
CARD_REL = os.path.join(".live-spec", "agent.md")


def main():
    if not os.path.isdir(TREE):
        print("agent-card: the tree root %s does not exist — the gate reads a real host tree." % TREE)
        return 1

    card = os.path.join(TREE, CARD_REL)
    if not os.path.isfile(card):
        print("agent-card: this project has no .live-spec/agent.md card yet (SPEC INV-219) — without "
              "one, no other session can find, address, or read from it.")
        print("  Fix: ask your agent to write the card at %s — its name, mission, the zones it owns, "
              "and its inbox address." % card)
        return 1

    print("agent-card: OK (this host tree carries its card at .live-spec/agent.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
