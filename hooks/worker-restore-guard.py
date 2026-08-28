#!/usr/bin/env python3
"""PreToolUse(Bash): deny commands that put repository bytes back over a working-tree path.

The retrospective check can name a violation only after bytes are gone.  This hook reads one Bash
command and refuses the act before a shell runs it.  It is caller-neutral because the hook event
does not identify a worker reliably.  That costs no recovery power: a worker writes only bytes it
saved itself; without those bytes it halts, and the orchestrator restores from the last committed
stage.

WHAT THE ACT IS.  Bytes sourced from the repository landing on a path in the working tree.  That
pair is the subject, and either half alone is innocent: reading history is free, and a worker
writing its OWN saved bytes to a path is the rule's own sanctioned recovery route.  The hook asks
the pair-question in two shapes.

  A. GIT WRITES THE TREE ITSELF, so one verb is the whole act: `git checkout` on a path, `git
     restore` outside `--staged`, `git checkout-index --force`, a saving `git stash`, `git reset`
     with `--hard`/`--merge`/`--keep`, and `git clean` with `-f`/`-x`.  This side stays a set of
     recognized verbs because git's own command surface closes it.

  B. THE SHELL ASSEMBLES THE ACT out of halves git never joins: a git command that only PRINTS
     repository content (`git show <rev>:<path>`, `git cat-file`, `git archive`) whose bytes are
     then landed on a tree path by a redirection or by a stage that writes a file (`tee`, `dd
     of=`, `sponge`, an extracting `tar`).  Reading a pipeline stage at a time sees only halves
     that are each harmless, which is why this side is judged over the whole pipeline and against
     the WRITE TARGET rather than against a verb.  Until 2026-08-28 this side was unguarded, and
     the refusal text below recommended `git show HEAD:<path>` — the exact read half of the route
     around the guard (ROADMAP row 479, PLAN q-586).

WHERE THE BYTES LAND.  A relative target names a file in the tree the command is standing in.  A
`/dev/...` sink holds nothing.  An absolute target is judged against the `cwd` the hook event
carries: under it, it is this tree; elsewhere, it is another place entirely and the hook says
nothing.  With no `cwd` in the event an absolute target passes, which is this static reader's
stated reach, beside `sh -c` and `xargs` below.

Quoted spans and heredoc bodies are data, not shell invocations. Segments are split on shell
separators outside quotes, and the `|` boundaries are kept so a pipeline is judged whole. The
ordinary `command`, `sudo`, and `env` wrapper options that still launch a program are transparent.
A command hidden in `sh -c` or `xargs` remains outside this static reader's reach, exactly as the
retrospective check documents.

Repo home: hooks/worker-restore-guard.py.  Installed copy: ~/.claude/hooks/.  The one-shot installer
copies and wires it as PreToolUse(Bash).
"""
import json
import os
import re
import shlex
import sys


_HEREDOC_OPENER = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
WRAPPERS = ("command", "sudo", "env")

# git subcommands that print repository content on stdout.  `show` counts only in its `<rev>:<path>`
# form, which is the one that prints a FILE out of history; `git show HEAD` prints a commit.
HISTORY_READERS = ("show", "cat-file", "archive")

# What the whole tree is called in a refusal, when the landing place is every path at once.
WORKING_TREE = "the working tree"


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
    """Cut shell text on separators outside quotes, each segment with the separator that follows."""
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
            out.append(("".join(buf), text[i:i + 2]))
            buf = []
            i += 2
            continue
        if ch == "|" and buf and buf[-1] == ">":
            # `>|` is one redirection operator, git's noclobber override, and not a pipe.
            buf.append(ch)
            i += 1
            continue
        if ch in (";", "|", "\n"):
            out.append(("".join(buf), ch))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    out.append(("".join(buf), ""))
    return [(segment.strip(), separator) for segment, separator in out]


def _pipelines(command):
    """The command's segments grouped into pipelines, each pipeline a list of its stages.

    A `|` keeps the stages it joins together, because the destructive act can be assembled ACROSS
    them: `git show HEAD:foo.py | tee foo.py` is a read in one stage and a write in the next, and
    neither stage on its own says what the pair does. Every other separator ends a pipeline.
    """
    out = []
    current = []
    for segment, separator in _cut_on_separators(_without_heredoc_bodies(command)):
        if segment:
            current.append(segment)
        if separator != "|" and current:
            out.append(current)
            current = []
    if current:
        out.append(current)
    return out


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


def _word_at(text, i):
    """(the shell word starting at or after `text[i]`, the index past it).

    Leading blanks are skipped; the word ends at a blank or at a character that starts another
    shell construct. Quotes around it are dropped, so `> "foo.py"` names `foo.py`.
    """
    while i < len(text) and text[i] in " \t":
        i += 1
    out = []
    quote = None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == quote:
                quote = None
            else:
                out.append(ch)
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch in " \t\n;|&<>":
            break
        if ch == "\\" and i + 1 < len(text):
            out.append(text[i + 1])
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out), i


def _truncating_redirect_targets(segment):
    """Every path this segment TRUNCATES with a `>`-style redirect.

    `>`, `>|` and `&>` all empty the file before a byte is written, which is where the uncommitted
    content goes. `>>` appends and leaves what the file holds in place, so it is stepped over. A
    file-descriptor duplication (`2>&1`, `>&2`) names no path and is stepped over too.
    """
    targets = []
    quote = None
    i = 0
    n = len(segment)
    while i < n:
        ch = segment[i]
        if quote:
            if ch == "\\" and quote == '"' and i + 1 < n:
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == ">":
            if segment[i - 1:i] == ">" or segment[i + 1:i + 2] == ">":
                i += 2 if segment[i + 1:i + 2] == ">" else 1
                continue
            j = i + 1
            if segment[j:j + 1] in ("|", "&"):
                j += 1
            word, j = _word_at(segment, j)
            if word and not word.isdigit():
                targets.append(word)
            i = max(j, i + 1)
            continue
        i += 1
    return targets


def _lands_in_the_tree(target, cwd):
    """True when writing `target` would land on a path in the tree the command runs in.

    A relative path is how a command names a file in the tree it is standing in. A `/dev/...` sink
    holds no bytes. An absolute path is this tree's only when the hook event's `cwd` places it
    there; with no `cwd` to place it, the hook says nothing rather than guessing.
    """
    if not target:
        return False
    expanded = os.path.expanduser(target)
    if expanded.startswith("/dev/"):
        return False
    if not os.path.isabs(expanded):
        return True
    if not cwd:
        return False
    here = os.path.normpath(cwd)
    there = os.path.normpath(expanded)
    return there == here or there.startswith(here + os.sep)


def _reads_repository_content(segment):
    """True when this segment PRINTS repository content on stdout.

    `git show` counts in its `<rev>:<path>` form, which prints a file out of history; `git show
    HEAD` prints a commit and restores nothing. `git cat-file` and `git archive` print object and
    tree content in every form they have.
    """
    args = _git_args(segment)
    if not args:
        return False
    sub, rest = args[0], args[1:]
    if sub == "show":
        return any(":" in a for a in rest if not a.startswith("-"))
    return sub in ("cat-file", "archive")


def _write_target(segment, cwd):
    """The tree path this segment lands bytes on, or None.

    Two ways a stage writes a file: a truncating redirection, and a program that reads stdin and
    writes it out to a path. The second set is the stdin-consuming writers a pipeline realistically
    ends in — `tee`, `dd of=`, `sponge`, and a `tar` told to extract, which unpacks into whatever
    directory it is pointed at.
    """
    for target in _truncating_redirect_targets(segment):
        if _lands_in_the_tree(target, cwd):
            return target
    tokens = _command_tokens(segment)
    if not tokens:
        return None
    program = tokens[0].rsplit("/", 1)[-1]
    args = tokens[1:]
    candidates = []
    if program in ("tee", "sponge"):
        candidates = [a for a in args if not a.startswith("-")]
    elif program == "dd":
        candidates = [a.split("=", 1)[1] for a in args if a.startswith("of=")]
    elif program in ("tar", "gtar", "bsdtar"):
        extracts = any(a == "--extract" or (not a.startswith("--") and "x" in a.lstrip("-"))
                       for a in args)
        if extracts:
            into = next((args[i + 1] for i, a in enumerate(args)
                         if a == "-C" and i + 1 < len(args)), None)
            if into is None:
                return WORKING_TREE
            return WORKING_TREE if _lands_in_the_tree(into, cwd) else None
    for target in candidates:
        if _lands_in_the_tree(target, cwd):
            return target
    return None


def assembled_form(stages, cwd):
    """The name of the act a whole PIPELINE assembles out of harmless-looking stages, or None.

    Repository content printed by one stage and landed on a tree path by any stage is the same
    loss `git checkout -- <path>` causes, arrived at by a route no single verb names.
    """
    if not any(_reads_repository_content(stage) for stage in stages):
        return None
    for stage in stages:
        target = _write_target(stage, cwd)
        if target:
            return "a read of the repository written over %s" % (
                target if target == WORKING_TREE else "`%s` in the working tree" % target)
    return None


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
    elif sub == "checkout-index":
        # git's plumbing spelling of `git checkout .`: with --force it writes index entries over
        # files that already exist, whatever the tree holds. Without it, existing files are skipped.
        if any(a == "--force" or (a.startswith("-") and not a.startswith("--") and "f" in a)
               for a in rest):
            return "git checkout-index --force"
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


def find_forbidden(command, cwd=None):
    for stages in _pipelines(command):
        for segment in stages:
            form = matched_form(segment)
            if form:
                return segment, form
        form = assembled_form(stages, cwd)
        if form:
            return " | ".join(stages), form
    return None, None


def deny_payload(segment, form):
    reason = (
        "worker-restore-guard: `%s` is %s and can discard uncommitted bytes the caller did not "
        "write (ROADMAP row 479, SPEC INV-298/INV-299). Repository bytes reaching a path in this "
        "tree is the act being refused, however it is assembled: a git command that writes the "
        "tree itself, a redirection, or a pipe into something that writes a file. A worker may "
        "restore only its own saved bytes, by writing them with the file-writing tool. If it did "
        "not save those bytes, it must halt and report the file. The orchestrator owns recovery "
        "from the last committed stage: print those bytes with `git show HEAD:<path>`, keep "
        "whatever the file holds now, then write the file deliberately with the file-writing "
        "tool. Do not run this command."
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
    cwd = payload.get("cwd")
    segment, form = find_forbidden(command, cwd if isinstance(cwd, str) else None)
    if segment:
        print(json.dumps(deny_payload(segment, form)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
