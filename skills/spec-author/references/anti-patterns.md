## Anti-patterns (refuse these)

- **Speccing a surface on one axis only** — the player described as play/mute/solo with no word on what the
  compact view does to it. Always compose.
- **Two names for one surface** — "the lanes" and "#stemlanes" as if separate. Unify.
- **Filling a gap silently** — inventing a threshold or a behavior the author never decided. Ask or
  ⟨DECIDE⟩.
- **Speccing after the code** — writing the spec to match what was built. The spec should lead, and the
  prover should find the holes before code exists.
- **Pinning a drifting version number in prose** — "current version: vX.Y" in a header or README always
  goes stale; the version has one home (the VERSION file, the frontmatter) — point there or omit it.
  This binds a **derived doc's header** too (ARCHITECTURE.md, TEST_MATRIX.md): a derived doc's header
  carries no frozen spec-version number — it names what it derives from, points at the version's one
  home (VERSION), and carries a dated "Last reconciled" provenance line, so
  a reader never meets a stale number that reads as the current version. A version string has no place
  in that header. The lint `tests/test_derived_doc_header_policy.py` holds the two headers to this (row 265).
- **A wall of undifferentiated prose** — behaviour run together in paragraphs with no case to land on. The
  fix is named cases with numbered criteria, so the reader scans the behaviour; machine-terse fragments are
  the opposite failure and get rejected just as hard (see "How it reads").
- **Codes opening the line / edit-history in the prose** — `INV-18:` as a criterion's first word, or "in v0.8
  we changed…" baked into a rule. Codes trail at line-ends; history goes in the JOURNAL.
- **Prose where a criterion belongs** — a behaviour told as a narrative paragraph, leaving the reader no
  numbered line to key on. Each rule is a criterion carrying one trigger, one response, and a trailing
  anchor, sitting in a named case.
- **A hand-edited code-to-location table** — editing the generated Reference table by hand, or letting it
  lag the body. The table is generated output (`scripts/build-index.py`); `guardrails/check-index-generated.py`
  reds a table that differs from a fresh build. Regenerate it; never hand-edit it.

