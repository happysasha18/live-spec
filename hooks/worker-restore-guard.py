#!/usr/bin/env python3
"""PreToolUse(Bash): deny git commands that discard uncommitted work before Bash runs them.

The retrospective check can name a violation only after bytes are gone.  This hook reads one Bash
command and denies the five forms in the worker rule: path checkout, worktree restore, saving stash,
destructive reset, and live clean.  It is caller-neutral because the hook event does not identify a
worker reliably.  That costs no recovery power: a worker writes only bytes it saved itself; without
those bytes it halts, and the orchestrator restores from the last committed stage.

Quoted spans and heredoc bodies are data, not shell invocations. Segments are split on shell
separators outside quotes. The ordinary `command`, `sudo`, and `env` wrapper options that still
launch a program are transparent. A command hidden in `sh -c` or `xargs` remains outside this static
reader's reach, exactly as the retrospective check documents.

Repo home: hooks/worker-restore-guard.py.  Installed copy: ~/.claude/hooks/.  The one-shot installer
copies and wires it as PreToolUse(Bash).
"""
import json
import re
import shlex
import sys


_HEREDOC_OPENER = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
WRAPPERS = ("command", "sudo", "env")


def _without_heredoc_bodies(command):
    lines = command.split("\n")
    kept = []
    i = 0
    while i < len(lines):
        line = lines[i]
        kept.append(line)
        i += 1
        for match in _HEREDOC_OPENER.finditer(line):
            word = match.group(2)
            while i < len(lines) and lines[i].strip() != word:
                i += 1
            if i < len(lines):
                i += 1
    return "\n".join(kept)


def _cut_on_separators(text):
    """Cut shell text on separators outside quotes."""
    out = []
    buf = []
    quote = None
    i = 0
    while i < len(text):
        ch = text[i]
        if quote == "'":
            buf.append(ch)
            if ch == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if ch == "\\" and i + 1 < len(text):
                buf.extend((ch, text[i + 1]))
                i += 2
                continue
            buf.append(ch)
            if ch == '"':
                quote = None
            i += 1
            continue
        if ch == "\\" and i + 1 < len(text):
            buf.extend((ch, text[i + 1]))
            i += 2
            continue
        if ch in "'\"":
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if text[i:i + 2] in ("&&", "||"):
            out.append("".join(buf))
            buf = []
            i += 2
            continue
        if ch in (";", "|", "\n"):
            out.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    out.append("".join(buf))
    return [segment.strip() for segment in out if segment.strip()]


def _tokens(segment):
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def _is_assignment(token):
    if token.startswith("-") or "=" not in token:
        return False
    name = token.split("=", 1)[0]
    return bool(name) and all(c.isalnum() or c == "_" for c in name)


def _command_tokens(segment):
    tokens = _tokens(segment)
    while tokens:
        if _is_assignment(tokens[0]):
            tokens = tokens[1:]
            continue
        wrapper = tokens[0].rsplit("/", 1)[-1]
        if wrapper not in WRAPPERS:
            break
        tokens = tokens[1:]
        if wrapper == "command":
            if tokens and tokens[0] == "--":
                tokens = tokens[1:]
            if tokens and tokens[0] == "-p":
                tokens = tokens[1:]
        elif wrapper == "env":
            while tokens:
                token = tokens[0]
                if token == "--":
                    tokens = tokens[1:]
                    break
                if token in ("-i", "-0", "--ignore-environment", "--null"):
                    tokens = tokens[1:]
                elif token in ("-u", "--unset") and len(tokens) > 1:
                    tokens = tokens[2:]
                elif token.startswith("-u") or token.startswith("--unset="):
                    tokens = tokens[1:]
                else:
                    break
        else:  # sudo
            while tokens:
                token = tokens[0]
                if token == "--":
                    tokens = tokens[1:]
                    break
                if token in ("-u", "-g", "-h", "-p", "-r", "-t", "-C") and len(tokens) > 1:
                    tokens = tokens[2:]
                elif token in ("-E", "-H", "-K", "-k", "-n", "-S", "-b", "-v") \
                        or token.startswith(("--user=", "--group=", "--host=", "--prompt=")):
                    tokens = tokens[1:]
                else:
                    break
    return tokens


def _git_args(segment):
    tokens = _command_tokens(segment)
    if not tokens or tokens[0].rsplit("/", 1)[-1] != "git":
        return None
    args = tokens[1:]
    while args:
        if args[0] in ("-C", "-c", "--namespace", "--work-tree", "--git-dir") \
                and len(args) > 1:
            args = args[2:]
        elif args[0].startswith(("--git-dir=", "--work-tree=")) \
                or (args[0].startswith("-c") and len(args[0]) > 2):
            args = args[1:]
        else:
            break
    return args


def matched_form(segment):
    """Return the forbidden form's name, or None."""
    args = _git_args(segment)
    if not args:
        return None
    sub, rest = args[0], args[1:]
    if sub == "checkout":
        if any(a in ("-b", "-B", "--orphan") for a in rest):
            return None
        non_flags = [a for a in rest if not a.startswith("-")]
        if "--" in rest or "." in non_flags or len(non_flags) >= 2:
            return "git checkout on a path"
    elif sub == "restore":
        if not ("--staged" in rest and "--worktree" not in rest and "-W" not in rest):
            return "git restore of the worktree"
    elif sub == "stash":
        verb = next((a for a in rest if not a.startswith("-")), "")
        if verb in ("", "push", "save", "create", "store"):
            return "git stash" + (" " + verb if verb else "")
    elif sub == "reset" and any(a in ("--hard", "--merge", "--keep") for a in rest):
        return "git reset --hard/--merge/--keep"
    elif sub == "clean":
        dry = any(a == "--dry-run" or
                  (a.startswith("-") and not a.startswith("--") and "n" in a)
                  for a in rest)
        forced = any(a.startswith("-") and ("f" in a or "x" in a) for a in rest)
        if forced and not dry:
            return "git clean -f/-x"
    return None


def find_forbidden(command):
    for segment in _cut_on_separators(_without_heredoc_bodies(command)):
        form = matched_form(segment)
        if form:
            return segment, form
    return None, None


def deny_payload(segment, form):
    reason = (
        "worker-restore-guard: `%s` is %s and can discard uncommitted bytes the caller did not "
        "write (ROADMAP row 479, SPEC INV-298/INV-299). A worker may restore only its own saved "
        "bytes by writing them back. If it did not save those bytes, it must halt and report the "
        "file. The orchestrator owns recovery from the last committed stage, which it may read "
        "with `git show HEAD:<path>` before a normal file write. Do not run this command."
        % (segment, form)
    )
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        return 0
    if payload.get("tool_name") not in (None, "Bash"):
        return 0
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0
    segment, form = find_forbidden(command)
    if segment:
        print(json.dumps(deny_payload(segment, form)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
