# Skill review — live-spec-base (rule 36, who the person is)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-08-27
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand)

Verdict: PASS — no blocking findings.

## What changed

One new shared rule, 36, at the end of the numbered rules, and the frontmatter's own rule count
moved from twenty-one to twenty-two.

Rule 36 states who every human-facing sentence in this pack is addressed to: a single author of a
software product who drives the work by talking, installed the pack once, types nothing after that,
and opens none of the pack's files. From that it derives what the default register is (no gate
letters, no requirement codes, no file-and-line pins, no script names), binds refusal and error text
as hard as prose, names the one thing that raises the register (the person's own showing, never a
guess or an inference from a title), and closes with a rule that a mechanism the pack installed
unasked is the pack's own debt rather than a question to put to the person.

## Why it earned a rule rather than a note

The README already promises this reader. Nothing in the skills made the promise binding, and it was
broken in the place it matters most: the push gate's refusals printed gate letters and requirement
codes, and the pack's own owner hit one and could not tell what it wanted. A promise stated only in
the README is a wish; a numbered shared rule is what the twelve skills actually load.

## Checks against the skill-creator guide

- **Number.** 36 is the next free integer. The file's own header block lists the retired numbers
  (11, 14, 15, 18, 19, 20, 21, 23, 28, 30, 32–35), each retired and left open; none was reused.
  Checked against that list rather than assumed.
- **Self-count.** The frontmatter says how many rules the body carries, and this repo has shipped a
  stale count at least twice (a 2026-07-12 audit found "twenty-one" against a body of 23). So the
  new count was taken by command — `grep -cE "^[0-9]+\. \*\*"` returns 22 — rather than by eye.
- **Frontmatter description otherwise unchanged.** The description's job is triggering, and this
  rule changes no trigger. Only the count moved.
- **Progressive disclosure.** The rule is five short paragraphs in the body. It opens no reference
  file: it is read by every skill on every load, so putting it behind a door would defeat it.
- **One home.** `communicator` points at this rule rather than restating it. `grep -rn "rule 36"
  skills/` returns exactly the rule and that one pointer.
- **Register.** The rule is written in the register it demands — no codes, no paths, no skill names
  carrying meaning — which is the honest test of a rule about register.

## The dated example inside the rule

The closing clause cites 2026-08-27 and a plan file that had been given executable commands nobody
asked for, whose cost then surfaced as a question to its owner. That is a real incident from this
repo on that date, not an illustration invented to make the rule sound grounded. It is named
because the rule without it reads as taste, and with it reads as a bill someone already paid.

Findings: none blocking.

Blocking: none
