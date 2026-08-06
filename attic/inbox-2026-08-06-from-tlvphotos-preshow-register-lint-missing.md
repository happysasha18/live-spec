# The register check named in the session rules does not exist

**The fault.** The live-spec session rules injected into every prompt in the tlvphotos
window state, as law 3: "Before showing an artifact — a page rendered from a document, a
mockup, a decision page, or a report page, in any language — run
`python3 scripts/preshow-register-lint.py <path>` from the project root; a non-zero exit
blocks the showing."

No file of that name exists in the tlvphotos tree. So the law cannot be obeyed, every
artifact shown from this window today went unchecked, and the rule reads to the session as
one it must skip. A rule that names a script nobody can run blocks nothing and teaches the
session that some named gates are theatre.

**Lived:** running the command the rule names, from the tlvphotos project root:
`python3 scripts/preshow-register-lint.py lab/arrive/index.html` → exit 2,
"can't open file '/Users/sashaabramovich/tlvphotos/scripts/preshow-register-lint.py'".
A search for `*register-lint*` across both `~/tlvphotos` and `~/.claude` returns nothing.
The nearest checker in the tree, `guardrails/check-shipped-language.py`, is aimed at shipped
code and documents: run on the page above it reports 39 offences, which are that page's
deliberate visitor-facing Russian copy. It is the wrong instrument for the moment the rule
describes, so no substitute is available either.

**What would settle it.** Either the script ships with the pack and lands in a host tree at
adopt time, or law 3 stops naming a script and names what the session must actually do. The
second half of law 3 — chat uses the standard industry word, never a word-for-word rendering
of pack-internal English — is unaffected and was followed.

**Who threw it.** The tlvphotos window, session of 2026-08-06 evening, at the owner's
explicit instruction to report it urgently after he was told the checker was missing.

Lived: the fault above, with the two command results as its evidence.
Need-by: none
Id: tlvphotos-2026-08-06-register-lint
