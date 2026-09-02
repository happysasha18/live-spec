
---

# A second gate with the same shape: the language marker has no opener a JavaScript file can carry

Found an hour later, in the same day's work, and filed here because it is the same failure: a vendored
gate that a legitimate case cannot satisfy.

`check-shipped-language.py` spares a deliberate visitor-facing string when the line carries the marker
`user-language`. It recognises the marker behind two comment openers:

    USER_REGION_MARK = re.compile(r"(?:#|<!--)\s*user-language")

A JavaScript source can carry neither. So a line like

    hint.textContent = 'листайте дальше — колесо, палец или стрелки';

reds the push, and no marker the language allows can clear it. The remedies the failure message offers
all miss: a fenced block belongs to prose, the allowlist is for pre-existing debt rather than for new
deliberate copy, and moving the string elsewhere is a code change the gate has no business forcing.

This host added `/*` and `//` to the openers and recorded the reason in the file. The gate's intent is
untouched: an unmarked Cyrillic string still reds, and marking one is still a deliberate act a reviewer
can see in the diff.

Worth noting where this bites hardest: any project whose product speaks a language other than English
will meet it the first time a string is written in client code rather than in a translation file.
