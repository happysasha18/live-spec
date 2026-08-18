"""INV-211 — the chat judges stay wired in settings.json (gate v, ROADMAP 420 candidate 2).

config-health (gate m) proves an installed hook FILE matches its source, and hands this residual
to the row 420 audit by name: it does not prove settings.json still LISTS the judge entries. A
judge whose file is present still never runs when its settings.json entry is gone — the run comes
from the entry, not the file. That is the no-verdict failure this movement hit. check-judge-listed.py
reads the wired-hook declaration (guardrails/judge-hooks.json), asserts every hook under hooks/ is
classified there, and asserts each wired hook is referenced in its surface's array in the installed
~/.claude/settings.json; where settings.json cannot be read it stands down by name.
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import read, read_flat

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "guardrails", "check-judge-listed.py")
DECL = os.path.join(REPO, "guardrails", "judge-hooks.json")


def run_check(env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["python3", CHECK], cwd=REPO, capture_output=True, text=True, env=env)


def wrapped(hook_file):
    # settings.json wraps every hook command in the hook-meter; mirror that shape
    return "python3 ~/.claude/hooks/hook-meter.py ~/.claude/hooks/%s" % hook_file


# The pack wires no hook to PreToolUse today: the mid-turn chat scan that did was retired on 2026-08-17
# (PRODUCT_SPEC.md Requirement 295). This synthetic name keeps the third surface exercised, so the gate's
# reading of a PreToolUse array stays proven against the day a hook rides it again.
COMPLETE_PRE = ["a-pretooluse-hook.py"]


def settings_with(stop_hooks, ups_hooks, pre_hooks=COMPLETE_PRE):
    def arm(cmds):
        return [{"hooks": [{"type": "command", "command": c}]} for c in cmds]
    return {
        "hooks": {
            "Stop": arm([wrapped(h) for h in stop_hooks]),
            "UserPromptSubmit": arm([wrapped(h) for h in ups_hooks]),
            "PreToolUse": arm([wrapped(h) for h in pre_hooks]),
        }
    }


COMPLETE_STOP = ["scissors-scan.py", "hedge-scan.py", "affirmation-scan.py",
                 "code-anchor-scan.py", "register-judge-collect.sh"]
COMPLETE_UPS = ["clock-hook.sh", "chat-law-hook.sh", "register-judge-report.sh"]


def write_settings(tmpdir, stop, ups, pre=COMPLETE_PRE):
    path = os.path.join(tmpdir, "settings.json")
    with open(path, "w") as f:
        json.dump(settings_with(stop, ups, pre), f)
    return path


class TestJudgeListed(unittest.TestCase):
    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(CHECK))

    def test_decl_json_ships_and_parses(self):
        with open(DECL) as f:
            data = json.load(f)
        self.assertIn("wired", data)
        self.assertIn("library", data)

    def test_real_settings_stands_down_or_passes(self):
        # on the owner's machine the real settings.json lists every judge (returncode 0);
        # on a CI checkout with no settings.json the gate stands down by name (returncode 0).
        r = run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_complete_settings_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_settings(tmp, COMPLETE_STOP, COMPLETE_UPS)
            r = run_check({"JUDGE_SETTINGS_JSON": path})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_stop_arm_reds(self):
        # drop register-judge-collect from Stop — the collect judge goes dark
        with tempfile.TemporaryDirectory() as tmp:
            path = write_settings(tmp, ["scissors-scan.py"], COMPLETE_UPS)
            r = run_check({"JUDGE_SETTINGS_JSON": path})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("register-judge-collect", r.stdout)
            self.assertIn("Stop", r.stdout)

    def test_missing_userpromptsubmit_arm_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_settings(tmp, COMPLETE_STOP, ["clock-hook.sh", "register-judge-report.sh"])
            r = run_check({"JUDGE_SETTINGS_JSON": path})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("chat-law-hook", r.stdout)

    def test_absent_settings_stands_down(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "nope.json")
            r = run_check({"JUDGE_SETTINGS_JSON": missing})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("stands down", r.stdout)

    def test_undeclared_hook_reds(self):
        # a hook under hooks/ that judge-hooks.json classifies neither way reds asking it be classified
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "brand-new-hook.sh"), "w").close()
            path = write_settings(tmp, COMPLETE_STOP, COMPLETE_UPS)
            r = run_check({"JUDGE_HOOKS_DIR": tmp, "JUDGE_SETTINGS_JSON": path})
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("brand-new-hook", r.stdout)

    def test_every_real_source_hook_is_classified(self):
        # the real hooks/ dir is fully classified in judge-hooks.json, so the honesty arm passes
        with tempfile.TemporaryDirectory() as tmp:
            path = write_settings(tmp, COMPLETE_STOP, COMPLETE_UPS)
            r = run_check({"JUDGE_SETTINGS_JSON": path})
            self.assertNotIn("not classified", r.stdout)

    def test_gate_wired_into_pre_push(self):
        self.assertIn("check-judge-listed.py", read("guardrails/pre-push"))

    def test_gate_is_a_carveout_not_mirrored_in_ci(self):
        # gate v reads personal-layer settings.json absent on CI, so it is a declared carve-out,
        # never a CI step (mirroring config-health gate m). Its letter must be in ci-mirror.json.
        with open(os.path.join(REPO, "guardrails", "ci-mirror.json")) as f:
            carve = json.load(f)["ci_excluded"]
        self.assertIn("v", carve)
        self.assertNotIn("check-judge-listed.py", read(".github/workflows/gates.yml"))

    # --- traceability across the four documents ---

    def test_spec_states_the_law(self):
        # The spec's rewrite dropped implementation filenames from its prose (they now
        # live only in ARCHITECTURE.md, checked below); the spec names the gate and
        # its declaration by their behavioural names instead.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-211]", spec)
        self.assertIn("the wiring check", spec)
        self.assertIn("the wired-hook declaration", spec)

    def test_formal_index_row(self):
        self.assertIn("| INV-211 |", read("PRODUCT_SPEC.md"))

    def test_architecture_owns_the_invariant(self):
        arch = read("ARCHITECTURE.md")
        self.assertIn("INV-211", arch)
        self.assertIn("check-judge-listed.py", arch)

    def test_matrix_row_covers_the_law(self):
        self.assertIn("INV-211", read("TEST_MATRIX.md"))


if __name__ == "__main__":
    unittest.main()
