"""INV-157, INV-158 — the browser test harness launches muted, reaps the whole
process group of the browser it spawned, and bounds each command with a real
per-command deadline; and it has one canonical home, shipped once by the pack as
a template (templates/headless_harness.py) rather than a copy each project
maintains alone. This guard asserts on the SHIPPED files at the string level: the
template is the generic core (no project-specific methods), it carries the mute
flag, the process-group reap, and the per-command deadline; test-author states
the rule; the spec states the two invariants.

The token assertions run against a STRIPPED view of the template — the module
docstring and every comment removed (``_stripped_code`` / ``_func_code``) — so a
token that lives only in prose can no longer satisfy the net: removing the real
construct turns the guard RED even while the docstring still mentions it. Landed
2026-07-15."""
import ast
import py_compile
import re
from pathlib import Path

# _read IS the suite's one reading node: for the spec it returns the core and every part
# the map names, and for any other file the file itself.
from conftest import read as _read

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "headless_harness.py"


def _template():
    return TEMPLATE.read_text(encoding="utf-8")


def _strip_comments(text):
    """Drop full-line comments and trailing ``  # ...`` comments, line by line. A trailing comment is
    only cut when a ``#`` follows whitespace, so a ``#`` inside a string literal (never preceded by
    whitespace in this template, e.g. ``.split("#", 1)``) is left intact."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        out.append(re.sub(r"\s+#.*$", "", line))
    return "\n".join(out)


def _stripped_code():
    """The template source with the module docstring AND all comments removed — real code only."""
    src = _template()
    tree = ast.parse(src)
    if ast.get_docstring(tree, clean=False) is not None and tree.body:
        seg = ast.get_source_segment(src, tree.body[0])
        if seg:
            src = src.replace(seg, "", 1)
    return _strip_comments(src)


def _func_code(funcname, classname=None):
    """The source of the named function with its own docstring and comments stripped — so a token
    asserted against it must live in the function's real code, not its prose. ``classname`` scopes
    the lookup to a method of that class (e.g. ``Browser.__init__``, not ``_WS.__init__``)."""
    src = _template()
    tree = ast.parse(src)
    scope = tree
    if classname is not None:
        scope = next((n for n in ast.walk(tree)
                      if isinstance(n, ast.ClassDef) and n.name == classname), None)
        assert scope is not None, f"class not found in template: {classname}"
    search = ast.walk(scope) if classname is None else scope.body
    for node in search:
        if isinstance(node, ast.FunctionDef) and node.name == funcname:
            seg = ast.get_source_segment(src, node)
            if ast.get_docstring(node, clean=False) is not None and node.body:
                dseg = ast.get_source_segment(src, node.body[0])
                if dseg:
                    seg = seg.replace(dseg, "", 1)
            return _strip_comments(seg)
    raise AssertionError(f"function not found in template: {classname or ''}.{funcname}")


def test_template_exists():
    assert TEMPLATE.exists()


def test_template_compiles():
    # A syntax error must never ship green [F6].
    py_compile.compile(str(TEMPLATE), doraise=True)


def test_template_launches_muted():
    # Asserted against STRIPPED code, so removing --mute-audio from the argv turns this RED even
    # though the docstring still names the flag [F2].
    assert "--mute-audio" in _stripped_code()


def test_template_reaps_process_group():
    src = _stripped_code()
    for token in ("killpg", "SIGKILL", "start_new_session"):
        assert token in src, token


def test_template_bounds_commands_with_a_deadline():
    src = _stripped_code()
    for token in ("CMD_TIMEOUT", "_deadline", "settimeout(None)"):
        assert token in src, token


def test_mute_flag_lives_in_the_chrome_argv():
    # --mute-audio must sit in the real CHROME launch argv (Browser.__init__), not just the docstring.
    init = _func_code("__init__", "Browser")
    assert "--mute-audio" in init, "--mute-audio"
    assert "--headless=new" in init            # among the other launch flags


def test_close_reaps_the_group_unconditionally():
    # close() must SIGKILL the whole group even when the leader already exited: a wedged renderer
    # child would orphan forever otherwise, and the profile-dir marker is rmtree'd right after, so
    # the launch sweep could not find it either [F1]. os.killpg lives in close()'s real code.
    close = _func_code("close", "Browser")
    assert "os.killpg" in close, "os.killpg"
    assert "SIGKILL" in close, "SIGKILL"
    # the reap is not gated on the leader still running
    assert "poll()" not in close, "reap must not be gated on proc.poll()"


def test_sweep_reap_is_scoped_to_the_same_boot():
    # The sweep records a boot id with the pid and only killpg's a DEAD owner from the SAME boot; a
    # cross-boot dir (a reused pid could name an unrelated live group) is rmtree'd, never signalled;
    # an ownerless dir is skipped entirely [F3/F4]. All asserted against real code.
    sweep = _func_code("_sweep_stale_profiles")
    assert "os.killpg" in sweep, "os.killpg"          # the same-boot reap
    assert "_boot_id()" in sweep, "_boot_id()"        # reads the current boot
    assert "_pid_alive(owner)" in sweep, "_pid_alive(owner)"
    assert "def _boot_id" in _stripped_code()         # the boot-id helper exists in real code
    # the boot id is recorded at launch alongside the pid
    assert "_boot_id()" in _func_code("__init__", "Browser")


def test_template_sweeps_stale_profiles_at_launch():
    # A run KILLED before teardown (SIGKILL, power loss, sleep) never runs close(), so its Chrome
    # group and profile dir leak and pile up across runs [INV-157]. The launch sweep is the backstop:
    # a named sweep function, called from Browser.__init__, that reaps only THIS harness's own
    # crash leftovers — a dir whose recorded owner pid is dead — never a live concurrent run.
    src = _stripped_code()
    assert "def _sweep_stale_profiles" in src            # the sweep symbol
    assert "_sweep_stale_profiles()" in src              # invoked at launch
    assert "OWNER_PID" in src                            # each run records its Chrome pid…
    assert "def _pid_alive" in src                       # …so the sweep can skip a live owner
    # the sweep must be safe against a concurrent run: a live recorded owner is skipped, not reaped
    assert "_pid_alive(owner)" in src


def test_template_teardown_on_signal_and_atexit():
    # The catchable exits (Ctrl-C, a plain kill) must still run close() and reap the group; the
    # launch sweep is the backstop only for the uncatchable ones [INV-157].
    src = _stripped_code()
    assert "import atexit" in src
    assert "atexit.register" in src
    assert "def _install_teardown_hooks" in src
    for token in ("signal.SIGINT", "signal.SIGTERM"):
        assert token in src, token


def test_sweep_covers_every_temp_workspace():
    # A launch sweep that scans only the CURRENT tempdir leaves a launchd run and a terminal run
    # blind to each other's crash orphans — they hold different per-user temp roots on macOS, so
    # neither ever reaps the other's leftovers [Fable F5]. The sweep gathers profile dirs from every
    # workspace the harness could have used, not one. Asserted against real code.
    src = _stripped_code()
    assert "def _temp_roots" in src                       # the multi-root enumerator exists
    sweep = _func_code("_sweep_stale_profiles")
    assert "_temp_roots()" in sweep                       # the sweep iterates every root, not one
    roots = _func_code("_temp_roots")
    assert "/var/folders" in roots                        # macOS per-user temp roots
    assert "gettempdir()" in roots                        # the current root is still covered


def test_teardown_leaves_a_hosts_ignored_signal_intact():
    # If the host deliberately set SIG_IGN on SIGINT/SIGTERM, the harness must NOT resurrect it into a
    # process-killing handler — that overrides the host's stated intent [Fable F8]. The install skips
    # a signal whose prior disposition is SIG_IGN. Asserted against real code.
    install = _func_code("_install_teardown_hooks")
    assert "SIG_IGN" in install
    assert "prev is signal.SIG_IGN" in install


def test_harness_ships_by_deed_orphan_check_helper():
    # INV-157's net is a POST-RUN, by-deed orphan census a consumer asserts on — not a docstring the
    # consumer is asked to trust. The pack ships it in the harness's own home so a consumer adopts the
    # net WITH the harness rather than writing a private copy [Fable F7]. It reads real, live OS state.
    src = _stripped_code()
    assert "def orphan_guard" in src                      # the by-deed post-run net (context manager)
    assert "def surviving_orphans" in src                 # the census a consumer can assert on
    assert "def _own_live_owners" in src                  # the shared live-owner reader
    guard = _func_code("orphan_guard")
    assert "AssertionError" in guard                      # goes RED on a surviving orphan
    owners = _func_code("_own_live_owners")
    assert "_pid_alive" in owners                          # reads live process state — by deed


def test_orphan_net_scopes_to_this_process_own_launches():
    # F1: a machine-wide temp-dir census false-reds when a SIBLING process launches its own Chrome
    # inside the guarded window. The net must scope to what THIS process launched — the _LAUNCHED_OWNERS
    # set, recorded at each Browser launch — so a concurrent sibling in another process never blames
    # this suite. Asserted against real code.
    src = _stripped_code()
    assert "_LAUNCHED_OWNERS" in src                       # the process's own launch registry exists
    assert "_LAUNCHED_OWNERS.add" in _func_code("__init__", "Browser")   # each launch records its owner
    guard = _func_code("orphan_guard")
    assert "_LAUNCHED_OWNERS" in guard                     # the guard diffs its own set, not a census
    owners = _func_code("_own_live_owners")
    assert "_LAUNCHED_OWNERS" in owners


def test_sweep_reaps_old_ownerless_litter_by_age():
    # ROADMAP 333: the system temp is NOT self-purging, so an OLD ownerless profile dir (a killed run's
    # leftover that never recorded an owner) must be reaped by age; a YOUNG one is left alone (a live
    # sibling mid-launch). Asserted against real code.
    src = _stripped_code()
    assert "OWNERLESS_STALE_AGE" in src                    # the age threshold exists
    sweep = _func_code("_sweep_stale_profiles")
    assert "OWNERLESS_STALE_AGE" in sweep                  # the ownerless branch is age-bounded now
    assert "getmtime" in sweep                             # it reads the dir's age
    # the reap in the ownerless branch is rmtree-only (no pid to signal)
    assert "rmtree" in sweep


def test_harness_warns_on_a_temp_glut():
    # ROADMAP 333: a glut of the harness's own dirs at launch is surfaced loudly, so a filling temp
    # never masquerades as product test reds. Asserted against real code.
    src = _stripped_code()
    assert "PROFILE_GLUT_WARN" in src
    sweep = _func_code("_sweep_stale_profiles")
    assert "PROFILE_GLUT_WARN" in sweep
    assert "stderr" in sweep                               # the warning goes to stderr, loudly


def test_spec_states_the_temp_is_not_self_purging():
    spec = _read("PRODUCT_SPEC.md")
    assert "not self-purging" in spec
    assert "sweeps any stale process group and temp litter a prior run left" in spec


def test_template_is_generic_core_no_project_methods():
    src = _template()
    for method in ("def block", "def net_capture", "def net_clear", "def net_log",
                   "def pretend", "def set_local_storage", "def clear_storage",
                   "def local_storage"):
        assert method not in src, method


def test_template_docstring_cites_invariants():
    src = _template()
    assert "INV-157" in src
    assert "INV-158" in src


def test_test_author_states_the_harness_rule():
    ta = _read("skills/test-author/SKILL.md")
    assert "--mute-audio" in ta
    assert "INV-157" in ta


def test_spec_states_harness_invariants():
    spec = _read("PRODUCT_SPEC.md")
    assert "[INV-157]" in spec
    assert "INV-158, INV-110]" in spec  # INV-158 always co-brackets with a sibling code
    assert "launches muted" in spec


# --- ROADMAP row 364 (SPEC INV-157, matrix M-342/M-343): incident 2026-07-16 — Chrome for Testing
# 150 went frame-dead machine-wide (opened its debug port, answered CDP commands, but never produced
# a single compositor frame), bleeding false reds through every paint-waiting test; chrome-headless-shell
# 151 showed no such fault. The template now (1) prefers chrome-headless-shell in its binary resolution,
# dropping --headless=new on that road (the shell is headless by construction and does not accept the
# flag), and (2) probes for a compositor frame at launch, failing loudly and by name rather than letting
# a frame-dead browser masquerade as a wall of unrelated test reds. All four asserted against real code.

def test_template_prefers_headless_shell():
    # the resolution road NAMES chrome-headless-shell, and it stands BEFORE the Chrome-for-Testing
    # road in the resolution order — a newer-shell install always wins over Chrome for Testing.
    resolve = _func_code("_find_chrome")
    assert "chrome-headless-shell" in resolve
    assert resolve.index("chrome-headless-shell") < resolve.index("Google Chrome for Testing")


def test_shell_pick_drops_headless_new():
    # the shell is headless by construction and does not accept --headless=new; the launch path must
    # carry the mechanism that OMITS the flag on that road, not just the flag's bare presence — the
    # flag itself still lives in the code for the Chrome-for-Testing/system-Chrome roads (the
    # muted-launch guardrail scans the whole file, so --mute-audio must stay visible unconditionally).
    init = _func_code("__init__", "Browser")
    assert "_is_headless_shell" in init
    assert "--headless=new" in init
    assert "if not _is_headless_shell(CHROME):" in init
    assert "--mute-audio" in init


def test_template_probes_for_a_frame_at_launch():
    # the launch/start road carries a bounded frame probe wired behind a frame_probe parameter: a
    # data: navigation, one requestAnimationFrame awaited under the template's real per-command
    # deadline machinery (INV-155 — a bounded deadline, never a blanket sleep), invoked from
    # Browser.__init__ so a frame-dead browser is caught before the harness hands itself to the suite.
    src = _stripped_code()
    assert "def _probe_for_a_frame" in src
    assert "frame_probe" in src
    init = _func_code("__init__", "Browser")
    assert "frame_probe" in init
    assert "_probe_for_a_frame" in init
    probe = _func_code("_probe_for_a_frame", "Browser")
    assert "requestAnimationFrame" in probe
    assert "data:" in probe
    assert "timeout=timeout" in probe        # the bounded deadline machinery, not a blanket sleep
    assert "time.sleep" not in probe


def test_probe_failure_names_itself():
    # the probe's failure is its OWN named error (FrameProbeFailed), clearly distinct from a test
    # failure, and its message names the resolved browser, the compositor-frame miss, the
    # paint-waiting-test consequence, and the fix.
    src = _stripped_code()
    assert "class FrameProbeFailed" in src
    probe = _func_code("_probe_for_a_frame", "Browser")
    assert "FrameProbeFailed" in probe
    assert "FRAME PROBE FAILED:" in probe
    assert "no compositor frame" in probe
    assert "paint-waiting tests would red falsely on this browser" in probe
    assert "chrome-headless-shell@stable" in probe


def test_probe_covers_the_local_load_stall():
    # matrix M-343 (design-review fold, 2026-07-16): the frame-dead fault above is NOT the only browser
    # fault the same incident carried — Chrome for Testing 151 renders frames fine but STALLS loading
    # any 127.0.0.1 page (Page.navigate never completes; data: URLs load fine), a second fault a
    # data:-only probe would miss entirely. The probe now serves its throwaway page from the loopback
    # address so a LOAD leg catches this fault too, distinct from the FRAME leg. Asserted against the
    # probe's own real code (docstring/comments stripped), so a fix that only updates prose stays RED.
    probe = _func_code("_probe_for_a_frame", "Browser")
    assert "127.0.0.1" in probe                          # the probe serves from the loopback address
    assert "HTTPServer(" in probe                         # an http server bound to the loopback, in the probe
    assert "stalls loading loopback pages" in probe       # the load-stall leg names its own fault shape
    assert "finally" in probe                              # server teardown is unconditional


def test_probe_catches_socket_timeout():
    # Audit fold (2.3.0 audit, finding 1): on Python < 3.10 the deadline machinery's expiry raises
    # socket.timeout, which has no TimeoutError kinship there — a probe catching only TimeoutError
    # lets a stalled browser escape as a raw socket error and the loud named failure never fires.
    probe = _func_code("_probe_for_a_frame", "Browser")
    assert probe.count("socket.timeout") >= 2, "both probe legs must catch socket.timeout"
    assert "except (TimeoutError, socket.timeout)" in probe


def test_probe_failure_reaps_the_launched_browser():
    # Audit fold (2.3.0 audit, finding 4): a probe failure closes the just-launched Chrome at once;
    # the atexit hook is the backstop for interpreter exit, never the first line of cleanup.
    init = _func_code("__init__", "Browser")
    assert "_probe_for_a_frame" in init
    after_probe = init.split("_probe_for_a_frame", 1)[1]
    assert "self.close()" in after_probe, "probe failure must close() the launched browser"


def test_probe_fallback_leg_is_bounded():
    # Audit fold (2.3.0 audit, finding 5): the no-loopback fallback road's data: navigate rides the
    # probe's own ~2 s bound rather than the 60 s per-command default.
    probe = _func_code("_probe_for_a_frame", "Browser")
    assert 'timeout=timeout, url="data:' in probe
