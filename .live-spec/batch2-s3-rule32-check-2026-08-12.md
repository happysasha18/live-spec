# S3 — independent check of rule 32's rewrite, batch 2

Date: 2026-08-12. Fresh-context read against `.live-spec/batch2-s1-rule32-2026-08-12.md` (the ten
requirements) and the live rule text at `skills/live-spec-base/SKILL.md:555-568`. No S2 rationale read.

## 1-2. The ten requirements: carrying sentence, and reach

For all ten, the exact sentence S1 quoted from the old rule is present **verbatim, unchanged** in the
current text. The rule's normative sentences were not reworded; the bytes cut (2,205 to 1,449) came from
prose around them, not from the ten requirement sentences themselves.

1. CARRIED — "A release's number answers what taking it costs a host" (line 555), verbatim.
2. CARRIED — "The number reports what a host that vendored the previous version must do to take this
   one." (555-556), verbatim.
3. CARRIED — "A **patch** fixes a machine to hold a law already stated: no new capability, no changed
   contract, and the host takes it and does nothing." (556-557), verbatim.
4. CARRIED — "A **minor** grows what a host may adopt in a backward-compatible way: a new capability, a
   new law, or a new gate. The host takes it by re-running its catch-up walk [INV-91], with nothing it
   already carries rewritten." (557-559), verbatim, two sentences combining classification with the host
   action.
5. CARRIED — "A **major** is a release a host cannot take without changing what it already carries. Four
   things earn it: a reworded rule the host vendored, a renamed or removed surface a host depends on, a
   changed adoption or catch-up step, a moved law that forces host action." (559-561), verbatim.
6. CARRIED — "A major ships its dated `MIGRATION.md` chapter [INV-91]." (561-562), verbatim.
7. CARRIED — "The default is a patch. It is raised to a minor or a major only where the release earns the
   higher tier." (562-563), verbatim.
8. CARRIED — "This is a judgment the releasing session makes and states, **held by no machine**."
   (563-564), verbatim.
9. CARRIED — "The minor-versus-major call reads meaning a gate cannot, so it **stays a stated rule the
   session holds**, the same standing as a design-review finding that never blocks a lane [INV-141]."
   (564-566), verbatim.
10. CARRIED — "It keeps its published number as this cited boundary case." (568), verbatim.

No MISS. All ten are word-for-word present.

Reach, per prohibition in the old text, checked against the same words now:
- Requirement 8's prohibition ("held by no machine") — binds the same actor (any gate or script that
  might be built to make the call) in the same case, unchanged wording, full reach kept.
- Requirement 9's prohibition ("never blocks a lane") — binds the same actor (the push/release gate
  machinery) in the same case, unchanged wording, full reach kept.
- Requirement 3's constraint ("the host takes it and does nothing") — a description of patch handling
  rather than a standing prohibition; unchanged wording, same reach as before.

No prohibition was softened into a description. Since the sentences are byte-identical to what S1 quoted,
reach could only have dropped if S1 mis-quoted the old text, which its own verbatim-copy claim rules out.

## 3. First-time-reader stops

Reading lines 555-568 with no prior knowledge of this project's vocabulary, a first-time reader would
stop at:
- `INV-217`, `INV-91`, `INV-141` — bare invariant codes, meaning not given in this passage.
- "vendored" — used twice ("a host that vendored the previous version", "a reworded rule the host
  vendored") without definition; not a common English usage for "adopted a dependency version."
- "host" — carries a specific technical sense here (a downstream consumer that took a prior release) that
  an outside reader would not supply on first contact.
- "catch-up walk" — project-specific term for an adoption procedure, opaque without prior context.
- "gate" — used as a technical noun ("a new gate", "a gate cannot", referring to an automated check),
  distinct from its plain-English sense.
- "design-review finding that never blocks a lane" — assumes the reader already knows what a "lane" is
  and what it means for a finding not to block one.
- "boundary case" applied to a specific dated release (2.0.0) with no inline explanation of why that
  release, specifically, sits on the boundary, beyond the one terse sentence given.

Lint run: `python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md` →
`OK (preshow-register): no coined metaphor, calque, or transliterated pack term found.` Exit status **0**.
The lint's pass and this reading are not in conflict: the lint checks for coined metaphor, calque, and
transliterated pack terms, a narrower net than "everything an outside reader would stop on." Domain
jargon like "vendored," "host," and bare invariant codes falls outside what that lint screens for.

## 4. Contrast frame hunt

Searched lines 555-568 for the shape "X, not Y" or "X rather than Y" (`grep -niE "not | rather than |,
not|not \S+ but"`, and a manual re-read).

**None found.** The nearest candidates on manual read are not the flagged shape:
- "no new capability, no changed contract" — a list of exclusions, not a named contrast.
- "a release a host cannot take without changing what it already carries" — a "cannot ... without"
  construction, not "X, not Y."
- "held by no machine" and "never blocks a lane" — each a prohibition standing on its own sentence, which
  the brief itself exempts from the flag.

## 5. Verdict

10 of 10 requirements carried, all verbatim, no MISS. Every prohibition in the old text binds the same
actor in the same case in the new text — no softening. No contrast frame of the banned shape appears.
First-time-reader stops are domain jargon and bare invariant codes (INV-217, INV-91, INV-141; "vendored";
"host"; "catch-up walk"; "gate"; "lane"), all pre-existing project vocabulary carried over unchanged, not
new jargon introduced by the rewrite. Lint exit status 0.

**The rewrite stands.**
