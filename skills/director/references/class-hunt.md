# The class hunt

The four moves referenced from `SKILL.md`'s "Execution" section: what a confirmed bug still
owes once the first fix lands, before the work can be called closed (SPEC INV-124).

1. **Name the defect's class, then go looking for its relatives.** State the mistake in the
   abstract — too narrow a scope, a guard that was never added, a premise safe here but false one
   step over — and use that description to actively search every place
   the same mistake could be hiding, fixing every instance found in this same change. The point is
   turning up the relatives nobody has reported yet, beyond the one that got caught. This is the
   same duty base rule 14 states; the matrix row and its red-on-bug test are what extend coverage
   from the single occurrence to the whole class.
2. **Read the architecture for a structural cause.** When the mistake traces back to a boundary
   that was drawn poorly, or never drawn at all, or a node quietly owning something it shouldn't,
   update `ARCHITECTURE.md` in the same change. Several instances turning up in one district of the
   system is itself a sign the architecture is off.
3. **Read the spec for the same gap.** If the spec says nothing about the broken behaviour, or says
   too little, that silence is the actual defect — fix the spec first, so the prover has something to
   flag it against, and only then land the code fix beneath it (the generalized form of the
   spec-under-describes-composition lesson).
4. **Bring the human in where the class boundary is a judgment call.** Deciding which behaviours
   belong to one class, what the design was meant to be, or whether a whole area needs rethinking is
   not something to guess at — stop and ask.

Skipping any of these four leaves siblings standing; the work stays a status update until the
sweep is complete, and only then does it land (SPEC INV-26).
