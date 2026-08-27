"""27.08: three 👁️ tasks (q-527, q-529, q-536) traced to `Source: found <date>`, an agent's own
discovery, not his word — and none of the three needed his eyes. scripts/check-eyes-marker.py
flags that class mechanically; this pins its logic against synthetic PLAN.md text so the check
itself can't silently stop finding what it exists to find.
"""
import importlib.util
import os
import unittest

from conftest import ROOT


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


find_suspect_eyes_markers = _load(
    os.path.join(ROOT, "scripts", "check-eyes-marker.py"), "check_eyes_marker"
).find_suspect_eyes_markers


HEADER = "## Tasks\n\n"


def _task(mark, title, task_id, source):
    return f"### {mark} {title} — id: {task_id}\n**Group:** Test · **Priority:** normal\n**Source:** {source}\n\n\n"


class TestEyesMarkerTracesToOwner(unittest.TestCase):
    def test_flags_a_found_sourced_eyes_task(self):
        text = HEADER + _task("👁️", "Something found, not asked", "q-1", "found 2026-07-29; a policy answer owed.")
        suspects = find_suspect_eyes_markers(text)
        self.assertEqual([t["id"] for t in suspects], ["q-1"])

    def test_does_not_flag_an_owner_sourced_eyes_task(self):
        text = HEADER + _task("👁️", "He asked directly", "q-2", 'owner 2026-08-01 10:00 — "which one do you want?"')
        suspects = find_suspect_eyes_markers(text)
        self.assertEqual(suspects, [])

    def test_does_not_flag_non_eyes_tasks_regardless_of_source(self):
        text = HEADER + _task("⬜", "Ordinary backlog", "q-3", "found 2026-07-10.")
        suspects = find_suspect_eyes_markers(text)
        self.assertEqual(suspects, [])

    def test_clean_on_the_real_plan(self):
        # 27.08: all three real offenders were re-marked the same night this check was written.
        # This just proves the check runs against the real file without crashing and agrees with
        # that day's own cleanup — not a promise the file stays clean forever.
        with open(os.path.join(ROOT, "PLAN.md"), encoding="utf-8") as f:
            text = f.read()
        suspects = find_suspect_eyes_markers(text)
        self.assertEqual(
            [t["id"] for t in suspects], [],
            "a 👁️ task's Source doesn't read as his own word — re-test it by derivability "
            "(profile.md's deferral rule) before asking him: %r" % [t["id"] for t in suspects],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
