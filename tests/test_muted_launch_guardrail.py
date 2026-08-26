"""INV-157's third net — a tracked script that drives a real headless browser must launch it MUTED.

The pack's own two nets for INV-157 (the shipped template's string-check, the consumer's by-deed
process-group diff) never HEAR a divergent fork's sound: a project that hand-rolls or forks its own
browser launch instead of adopting `templates/headless_harness.py` [INV-158] can play audio during a
test run and neither net catches it — tlvphotos did exactly this. The third net is a guardrail,
`guardrails/check-muted-launch.sh`, that reds a file whose CODE carries both a browser-LAUNCH signal
(`--headless`, `--remote-debugging-port`, `puppeteer.launch`, `chromium.launch`) and a code INVOCATION
token (`subprocess`, `Popen`, `.launch(`, and kin) with no `mute-audio` anywhere in that code. The check
is FILE-level, not per-line, because a real launch's arg list often spans multiple lines; it reads the
comment-stripped code on both the launch and the mute side, so a mute flag named only in a comment cannot
satisfy it, and a docstring that merely NAMES a flag with no real invocation is not flagged.

These tests assert the guardrail exists, passes the clean repo, reds a planted unmuted launch (red-first)
including a multi-line arg list, lets a muted launch and a launch-free file through, and — the two
regressions the fresh-eyes audit found — reds a launch whose only mute flag sits in a COMMENT, and passes
a file that only NAMES the flags in a docstring with no invocation. And that the spec states the net."""
import os
import subprocess
import tempfile
from conftest import ROOT, read

GUARD = os.path.join(ROOT, "guardrails", "check-muted-launch.sh")


def _run(target=None):
    cmd = ["bash", GUARD] + ([target] if target else [])
    return subprocess.run(cmd, capture_output=True, text=True)


def _scan(body, name="probe.py"):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, name)
        with open(p, "w") as f:
            f.write(body)
        return _run(p)


def test_guardrail_passes_the_clean_repo():
    # the pack's own real launcher is templates/headless_harness.py, which carries --mute-audio —
    # no tracked script drives a browser unmuted, so the real repo is green.
    r = _run()
    assert r.returncode == 0, r.stdout + r.stderr


def test_reds_on_an_unmuted_headless_launch():
    # red-first: a real headless-Chrome launch (subprocess invocation + flags) with no mute flag is
    # the footgun that played sound during a tlvphotos test run.
    r = _scan(
        "import subprocess\n"
        "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222'])\n"
    )
    assert r.returncode != 0, "guardrail passed an unmuted headless launch — the footgun is unguarded"
    assert "INV-157" in (r.stdout + r.stderr)


def test_allows_a_muted_launch():
    r = _scan(
        "import subprocess\n"
        "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222', '--mute-audio'])\n"
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_allows_a_file_with_no_launch():
    r = _scan('import os\nprint("no browser here")\n', name="helper.py")
    assert r.returncode == 0, r.stdout + r.stderr


def test_catches_a_multiline_arg_list_without_mute():
    # proves the file-level design: the launch flags sit on separate lines from the invocation, no
    # single line carries both a launch signal and mute-audio, yet the file drives an unmuted browser.
    r = _scan(
        "import subprocess\n"
        "args = [\n"
        "    'chrome',\n"
        "    '--headless',\n"
        "    '--remote-debugging-port=9222',\n"
        "    '--disable-gpu',\n"
        "]\n"
        "subprocess.Popen(args)\n"
    )
    assert r.returncode != 0, "guardrail missed a multi-line unmuted launch — it is checking per-line"
    assert "INV-157" in (r.stdout + r.stderr)


def test_allows_multiline_args_with_mute():
    r = _scan(
        "import subprocess\n"
        "args = [\n"
        "    'chrome',\n"
        "    '--headless',\n"
        "    '--remote-debugging-port=9222',\n"
        "    '--mute-audio',\n"
        "]\n"
        "subprocess.Popen(args)\n"
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_comment_only_mute_still_reds():
    # the fresh-eyes audit's highest finding: a mute flag named only in a COMMENT must NOT satisfy the
    # mute check — the file still launches a real browser unmuted and plays sound. This red went GREEN
    # (wrongly passed) before the mute check was moved onto the comment-stripped code.
    r = _scan(
        "import subprocess\n"
        "# TODO: someday add --mute-audio here\n"
        "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222'])\n"
    )
    assert r.returncode != 0, "a comment-only --mute-audio satisfied the mute check — sound plays unheard"
    assert "INV-157" in (r.stdout + r.stderr)


def test_names_flags_in_docstring_without_launch_passes():
    # the audit's false-positive finding: a file that merely NAMES the launch flags in a docstring, with
    # no real invocation, must NOT red — else every doc/test naming the flag needs a hardcoded exclusion.
    r = _scan('"""This module documents the --headless and --remote-debugging-port flags."""\nx = 1\n')
    assert r.returncode == 0, "a docstring naming the flags was falsely flagged as an unmuted launch"


def test_jsx_puppeteer_launch_unmuted_reds():
    # coverage widened to .jsx/.tsx (a React test harness): a puppeteer launch with no mute flag reds.
    r = _scan(
        "const b = await puppeteer.launch({ args: ['--headless', '--remote-debugging-port=9222'] });\n",
        name="harness.jsx",
    )
    assert r.returncode != 0, "an unmuted puppeteer.launch in a .jsx harness slipped past the guardrail"
    assert "INV-157" in (r.stdout + r.stderr)


def test_spec_states_the_third_net():
    spec = read("PRODUCT_SPEC.md")
    assert "the third mute-launch net still catching a forked unmuted launch" in spec


def test_js_comment_only_mute_still_reds():
    # batch audit 2026-07-16, F2: the comment strip was `#`-only, so a JS `// --mute-audio` comment
    # above a real unmuted launch satisfied the mute check. Per-extension stripping closes it.
    r = _scan(
        "// TODO: someday add --mute-audio here\n"
        "const b = await puppeteer.launch({ args: ['--headless', '--remote-debugging-port=9222'] });\n",
        name="harness.js",
    )
    assert r.returncode != 0, "a JS comment-only --mute-audio satisfied the mute check"
    assert "INV-157" in (r.stdout + r.stderr)


def test_js_block_comment_mute_still_reds():
    r = _scan(
        "/* --mute-audio lives here in prose */\n"
        "const b = await puppeteer.launch({ args: ['--headless', '--remote-debugging-port=9222'] });\n",
        name="harness.ts",
    )
    assert r.returncode != 0, "a TS block-comment --mute-audio satisfied the mute check"


def test_js_real_mute_still_passes():
    r = _scan(
        "const b = await puppeteer.launch({ args: ['--headless', '--mute-audio', '--remote-debugging-port=9222'] });\n",
        name="harness.js",
    )
    assert r.returncode == 0, "a really muted JS launch was falsely flagged"


# --- F5 (2026-07-16 batch audit, row 356): the extensionless-shebang scope hole -------------------
#
# The default (no-arg) scan selects files with `git ls-files '*.sh' '*.py' ... 'scripts/*'` — an
# extension allowlist. A tracked, extensionless, shebang-first-line script OUTSIDE scripts/ (a real
# executable, e.g. `bin/serve`) matches none of those patterns and was never read by the scan, so it
# could drive a real headless browser unmuted with the gate staying green. `_scan()` above can't
# exercise this: it hands the guardrail a single-file target, which bypasses the git-ls-files
# extension gate entirely regardless of extension. These tests build a real throwaway git tree (the
# pattern in tests/test_guardrails.py) and run the guardrail with NO target, so it takes the same
# default/no-arg path the push gate uses.

def _init_repo(tmp):
    subprocess.run(["git", "init", "-q"], cwd=tmp)
    subprocess.run(["git", "config", "user.email", "a@example.com"], cwd=tmp)
    subprocess.run(["git", "config", "user.name", "a"], cwd=tmp)


def _write(tmp, relpath, content):
    path = os.path.join(tmp, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _commit_all(tmp, msg):
    subprocess.run(["git", "add", "-A"], cwd=tmp)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=tmp)


def test_extensionless_shebang_script_outside_scripts_dir_is_scanned():
    # The F5 red: a tracked, extensionless, shebang-first-line launcher outside scripts/, carrying an
    # unmuted real headless-Chrome launch, must red the default scan the same as a `.py` file does.
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(
            tmp,
            "bin/serve",
            "#!/usr/bin/env python3\n"
            "import subprocess\n"
            "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222'])\n",
        )
        os.chmod(os.path.join(tmp, "bin", "serve"), 0o755)
        _commit_all(tmp, "add extensionless launcher")
        r = subprocess.run(["bash", GUARD], cwd=tmp, capture_output=True, text=True)
        assert r.returncode != 0, (
            "an extensionless tracked shebang script outside scripts/ escaped the scan entirely — "
            "the F5 extension-allowlist scope hole:\n" + r.stdout + r.stderr
        )
        assert "bin/serve" in (r.stdout + r.stderr)


def test_extensionless_shebang_muted_launch_passes():
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(
            tmp,
            "bin/serve",
            "#!/usr/bin/env python3\n"
            "import subprocess\n"
            "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222', '--mute-audio'])\n",
        )
        os.chmod(os.path.join(tmp, "bin", "serve"), 0o755)
        _commit_all(tmp, "add extensionless muted launcher")
        r = subprocess.run(["bash", GUARD], cwd=tmp, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


def test_extensionless_node_shebang_routes_to_js_comment_rules():
    # The checker picks its checker by the shebang interpreter: a `#!/usr/bin/env node` extensionless
    # file is JS, so a `// --mute-audio` LINE COMMENT must not satisfy the mute check (JS-comment
    # stripping), the same regression test_js_comment_only_mute_still_reds pins for a real `.js` file.
    # A default `#`-stripper misreads this file's `//` comment as live code and would wrongly pass it.
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(
            tmp,
            "bin/harness",
            "#!/usr/bin/env node\n"
            "// TODO: someday add --mute-audio here\n"
            "const b = await puppeteer.launch({ args: ['--headless', '--remote-debugging-port=9222'] });\n",
        )
        os.chmod(os.path.join(tmp, "bin", "harness"), 0o755)
        _commit_all(tmp, "add extensionless node launcher")
        r = subprocess.run(["bash", GUARD], cwd=tmp, capture_output=True, text=True)
        assert r.returncode != 0, (
            "an extensionless node-shebang file with a comment-only --mute-audio was falsely passed — "
            "the checker did not route it to JS comment-stripping:\n" + r.stdout + r.stderr
        )


def test_extensionless_shebang_inside_scripts_dir_still_covered():
    # scripts/* already matched every file under scripts/ regardless of extension before this fold;
    # the extensionless-shebang addition must not regress or double-report that existing coverage.
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(
            tmp,
            "scripts/serve",
            "#!/usr/bin/env python3\n"
            "import subprocess\n"
            "subprocess.Popen(['chrome', '--headless', '--remote-debugging-port=9222'])\n",
        )
        os.chmod(os.path.join(tmp, "scripts", "serve"), 0o755)
        _commit_all(tmp, "add extensionless scripts/ launcher")
        r = subprocess.run(["bash", GUARD], cwd=tmp, capture_output=True, text=True)
        assert r.returncode != 0, r.stdout + r.stderr
        hit_lines = [l for l in (r.stdout + r.stderr).splitlines() if "scripts/serve" in l]
        assert len(hit_lines) == 1, "scripts/serve reported more than once: " + repr(hit_lines)


def test_extensionless_file_with_no_shebang_is_not_swept_in():
    # a tracked extensionless file that ISN'T a script (no shebang first line) must stay out of scope,
    # same as before this fold — only a real shebang marks it executable code to scan.
    with tempfile.TemporaryDirectory() as tmp:
        _init_repo(tmp)
        _write(tmp, "NOTES", "--headless --remote-debugging-port=9222 subprocess.Popen(\n")
        _commit_all(tmp, "add extensionless non-script")
        r = subprocess.run(["bash", GUARD], cwd=tmp, capture_output=True, text=True)
        assert r.returncode == 0, (
            "a non-shebang extensionless file was swept into the scan: " + r.stdout + r.stderr
        )


def test_big_muted_file_survives_the_pipe():
    # CI-only red of 2026-07-17 (v2.5.0 push): under `set -o pipefail`, `printf "$stripped" |
    # grep -q mute-audio` reds falsely on a LARGE muted file — grep matches early and exits,
    # printf catches SIGPIPE once the remainder outgrows the pipe buffer, pipefail turns that
    # 141 into "no match", and the muted file is flagged as unmuted. Deterministic here: the
    # mute flag on line 1, ~1 MB of code lines behind it, the launch/invoke signals at the tail.
    body_lines = ['CHROME_ARGS = ["--mute-audio"]  # muted at the source\n']
    body_lines += ['x_%d = "padding line that is plain code, long enough to fill the pipe buffer quickly %d"\n' % (i, i) for i in range(12000)]
    body_lines += ['import subprocess\n',
                   'subprocess.Popen(CHROME_ARGS + ["--headless", "--remote-debugging-port=0"])\n']
    r = _scan("".join(body_lines), name="big_muted_launcher.py")
    assert r.returncode == 0, r.stdout + r.stderr
