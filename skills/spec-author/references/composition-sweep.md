## The move most specs miss: compose every stateful surface across every axis

This move catches the bugs that pass every unit test, and a feature-focused author skips it.

When a surface (a player, a form, an editor, a panel) carries **state**, the system almost always also has
**global axes** it renders under. This is the **canonical axis list — its home is here; other docs point at it:**

- **view** (compact / detailed) · **mode** (quick / full, read / edit) · **tier** · **viewport size** ·
  **persistence / reopen** (any state that survives a reload — localStorage, a saved file) ·
  **concurrency** where it applies ·
  **every other live surface** — every other surface that can be present at the same time, whether or not
  that other surface holds state: a sibling sharing the screen, or a surface the flow reaches just before
  or after this one (a static end screen counts). For each, state what this surface does while that one is
  present: hold, clear, or hand off.

The bugs that pass every unit test live in the **product** of surface-state × axis, because each was
specified alone. The three authors forget most: viewport size (a grid that reflows below some width),
persistence/reopen (state written last session auto-restoring into a changed UI), and every other live
surface (a caption still naming the previous photo once the closing screen arrives, because "what the
caption shows when the finale is in view" was never written).

So, for every stateful surface, before its section is called done:

- **Enumerate it against each global axis.** For each axis value (each view/mode/tier), state what happens
  to the surface's state and controls. Is the state still *visible*? Still *reversible*? Does the axis
  transition *preserve, reset, or block* the state?
- **Name the composition invariant.** e.g. *"a per-stem mute/solo is reachable only while its control
  surface is visible; entering the compact view resets to the full mix."* Without it, the
  stranding bug follows: a state set in one view, hidden by another, with no way to see or undo it.
- **One surface, one name.** If the player's lanes and the `#stemlanes` canvas are the same thing, call
  them the same thing everywhere. A reviewer (human or prover) can only connect a cross-section hole when
  both sides are named identically and present in the same document — two names for one surface hides the
  seam.
- **If the surface persists state, compose the versions too.** When it writes localStorage/disk, enumerate
  version-N-1 state × version-N code explicitly: what does the current UI do when it reads a stored value
  that's older, partial, or belongs to a since-removed feature? State a migrate / ignore / clear rule — this
  is the seam behind "reopened it and it looked broken".

