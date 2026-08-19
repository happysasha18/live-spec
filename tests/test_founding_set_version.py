# -*- coding: utf-8 -*-
"""A grown founding question reaches hosts that founded before it (ROADMAP row 394, SPEC INV-227).

When the pack grows its founding-question set, a host that already answered the old set never learns a new
question exists: the update check reads FILES and says nothing about QUESTIONS, so a host founded at an
older set version carries a frozen answer set (the agent card E-32/INV-184 is the live example — every
existing tree predates it). This row versions the founding-question set, records the version a host
answered, and extends the daily update check (scripts/check-pack-update.sh, E-25) with a founding arm that
names each never-answered question beside the stale files the pin arm already reports (INV-177).

Kin of INV-159 (a duty binds forward): a never-answered question is surfaced for the host to answer at
catch-up, answered on no one's behalf.

Red-first: against HEAD 573d8ea there is no scripts/founding-questions.json, the host profile carries no
founding.set-version line, and check-pack-update.sh has no founding arm — so the fixture-host assertions
below fail. The red is recorded in docs/prover/2026-07-18-rows-370-394.md.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from conftest import SPEC, read

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(REPO, "scripts", "check-pack-update.sh")

sys.path.insert(0, os.path.join(REPO, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


def run_check(tmp, founding_manifest=None, host_profile=None, remote_version="9.9.9"):
    """Drive the update check with test overrides, bypassing the network."""
    remote = os.path.join(tmp, "REMOTE_VERSION")
    open(remote, "w").write(remote_version)
    stamp = os.path.join(tmp, "stamp")
    args = ["bash", CHECK, "--remote-file", remote, "--stamp-file", stamp, "--force",
            "--installed-file", os.path.join(REPO, "VERSION"), "--pack-root", REPO]
    if founding_manifest:
        args += ["--founding-manifest", founding_manifest]
    if host_profile is not None:
        args += ["--host-profile", host_profile]
    return subprocess.run(args, cwd=tmp, capture_output=True, text=True)


def _manifest(tmp):
    """A fixture founding-question set: current version 4, the card question entering at 4."""
    man = os.path.join(tmp, "founding-questions.json")
    json.dump({"set_version": 4,
               "questions": [
                   {"since": 1, "anchor": "INV-36", "key": "project.kind",
                    "question": "what kind of project is this?"},
                   {"since": 3, "anchor": "INV-135", "key": "project.layers + project.proofs",
                    "question": "what are this project's concrete layers and proof kinds?"},
                   {"since": 4, "anchor": "E-32/INV-184", "key": ".live-spec/agent.md",
                    "question": "the agent card — does this tree carry its self-declaring card?"},
               ]}, open(man, "w"))
    return man


class TestFoundingArmNamesNeverAnswered(unittest.TestCase):
    def test_old_host_gets_unanswered_question_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = _manifest(tmp)
            profile = os.path.join(tmp, "profile.md")
            # a host that founded before the card existed: answered set version 3
            open(profile, "w").write("- `founding.set-version: 3` — founded before the card\n")
            r = run_check(tmp, founding_manifest=man, host_profile=profile)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("FOUNDING QUESTIONS", r.stdout)
            self.assertIn(".live-spec/agent.md", r.stdout,
                          "the never-answered card question is not named for the older host")
            self.assertIn("E-32/INV-184", r.stdout)
            # a question the host already answered (since 1, 3) is NOT re-named
            self.assertNotIn("project.kind", r.stdout,
                             "an already-answered question was named — the arm names too much")

    def test_current_host_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            man = _manifest(tmp)
            profile = os.path.join(tmp, "profile.md")
            open(profile, "w").write("- `founding.set-version: 4` — current on the set\n")
            r = run_check(tmp, founding_manifest=man, host_profile=profile)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn("FOUNDING QUESTIONS", r.stdout,
                             "a host current on the set was told it owes a question")

    def test_versionless_host_is_told_the_set_is_versioned(self):
        # a host with no recorded founding.set-version founded before the set was versioned:
        # every question is potentially owed (the versionless-record rule, INV-91 kin)
        with tempfile.TemporaryDirectory() as tmp:
            man = _manifest(tmp)
            profile = os.path.join(tmp, "profile.md")
            open(profile, "w").write("- `project.kind: skill pack`\n")  # no founding.set-version line
            r = run_check(tmp, founding_manifest=man, host_profile=profile)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("FOUNDING QUESTIONS", r.stdout)
            self.assertIn(".live-spec/agent.md", r.stdout)


class TestPackHostIsCurrent(unittest.TestCase):
    def test_pack_manifest_and_profile_agree(self):
        """The pack's own host records the current set version and carries every question that
        applies to it, so its real founding-questions.json and profile agree — no question named."""
        man = json.load(open(os.path.join(REPO, "scripts", "founding-questions.json")))
        self.assertIsInstance(man.get("set_version"), int)
        profile = open(os.path.join(REPO, ".live-spec", "profile.md"), encoding="utf-8").read()
        self.assertIn("founding.set-version:", profile)
        import re
        recorded = int(re.search(r"founding\.set-version:\s*(\d+)", profile).group(1))
        self.assertEqual(recorded, man["set_version"],
                         "the pack's recorded set version lags its own founding-question manifest")


class TestSpecStatesTheLaw(unittest.TestCase):
    def test_spec_states_the_law(self):
        # PRODUCT_SPEC.md states this law in plain behaviour; the literal set-is-versioned framing
        # and the founding-questions.json manifest filename moved to ARCHITECTURE.md's INV-227
        # ownership row (see test_architecture_owns_the_invariant) — the rewrite's document-
        # boundary convention (spec = behaviour, architecture = implementation file).
        spec = read(SPEC)
        self.assertIn(
            "read the host's recorded `founding.set-version` against the current set", spec
        )
        self.assertIn("[INV-227]", spec)
        self.assertIn("founding.set-version", spec)
        self.assertIn("name each founding question the host has never answered", spec)

    def test_formal_index_row(self):
        spec = read(SPEC)
        self.assertIn("| INV-227 |", spec, "INV-227 has no Reference index row")
        self.assertIn(
            "founding.set-version", spec,
            "INV-227's body criterion doesn't carry the founding-set-version phrase",
        )

    def test_architecture_owns_the_invariant(self):
        arch = open(os.path.join(REPO, "ARCHITECTURE.md"), encoding="utf-8").read()
        nodes = archformat.parse_nodes(arch)
        attach = next((n for n in nodes if n.name == "attach"), None)
        self.assertIsNotNone(attach, "ARCHITECTURE.md carries no attach node")
        self.assertIn("INV-227", attach.anchors_expanded, "attach does not own INV-227 in the owns-list")

    def test_matrix_row_covers_the_law(self):
        mat = read("TEST_MATRIX.md")
        self.assertIn("| M-408 |", mat)
        row = next((l for l in mat.splitlines() if "| M-408 |" in l), "")
        self.assertIn("INV-227", row)

    def test_catchup_orient_names_the_gap(self):
        # the SPEC clause claims two guide homes — founding/orient (ADOPT.md) and the catch-up walk's
        # orient phase (MIGRATION.md, the operating guide for A-11). Assert both guides actually carry
        # the step, not just the spec prose (the audit's finding: a claimed home must be wired).
        spec = read(SPEC)
        self.assertIn("name each question added since", spec,
                      "the spec's catch-up orient phase does not name the never-answered questions")

        adopt = open(os.path.join(REPO, "adopt", "ADOPT.md"), encoding="utf-8").read()
        self.assertIn("founding.set-version", adopt,
                      "ADOPT.md's founding/orient does not record the answered set version")
        self.assertIn("INV-227", adopt)

        migration = open(os.path.join(REPO, "MIGRATION.md"), encoding="utf-8").read()
        low = migration.lower()
        self.assertIn("founding.set-version", migration,
                      "MIGRATION.md's catch-up orient does not read the host's answered set version")
        self.assertIn("never answered", low,
                      "MIGRATION.md's catch-up orient does not name the never-answered questions")
        self.assertIn("INV-227", migration)


if __name__ == "__main__":
    unittest.main(verbosity=2)
