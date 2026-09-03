"""The catch-up walk — matrix rows M-217/M-218/M-219/M-220 (SPEC A-11, INV-89, INV-90, INV-91).

String-level rows on the SHIPPED guides: MIGRATION.md is the walk's operating guide, ADOPT.md holds
the canonical document set once, adoption.md and pair-adoption.md point and route. Red-proven against
the pre-rewrite guides on 2026-07-10 (the old MIGRATION.md was a single rename note with a
non-idempotent `git mv` step and no walk at all).
"""

import hashlib
import os
import re
import subprocess
import tempfile
import unittest

from conftest import read, read_all_flat, read_flat


class TestCatchupWalk(unittest.TestCase):
    """M-217 — the walk has one named home with routing, four phases, and the owner's gate."""

    def test_catchup_walk(self):
        # RE-PINNED pass-2 (see repin log): the pass-2 restore moved every pilot-unit feature
        # tag onto its own-line "[feature: F-...]" heading tag instead of citing it inline in the
        # User Story — the convention is applied consistently across all five, not just this one.
        # RE-PINNED again by plan-12: those five headings had carried five names for one thing a
        # person is given — the pack attached to a project, whether the project is empty, already
        # running, already attached and moving to a newer pack, or an engine and its instance, and
        # whether or not the settings card closed the walk. They converged on F-attach. This walk
        # is one entry into it, and the requirement below is still its own home; A-11 stays inline
        # in the User Story and the criteria.
        spec = read_flat("PRODUCT_SPEC.md")
        # the spec side: the scenario and its anchors exist
        self.assertIn(
            "## Requirement 180: The catch-up sequence brings an adopted host onto the current pack"
            " [feature: F-attach]",
            spec,
        )
        for anchor in ("[A-11]", "[INV-89]", "[INV-90]", "[INV-91]"):
            self.assertIn(anchor, spec, f"spec anchor {anchor} missing")

        mig = read_flat("MIGRATION.md")
        # routing opens the guide
        self.assertIn("## When to run this", mig)
        self.assertIn("A host that never adopted the pack goes to adoption", mig)
        self.assertIn("A host that already adopted goes to this catch-up walk", mig)
        # the four phases, in the spec's order
        for phase in (
            "Phase 1 — orient on the delta",
            "Phase 2 — plan, behind the owner's gate",
            "Phase 3 — execute, preserving facts",
            "Phase 4 — verify and re-record",
        ):
            self.assertIn(phase, mig, f"phase heading missing: {phase}")
        self.assertLess(
            mig.index("Phase 1 — orient"), mig.index("Phase 2 — plan"),
            "phases out of order",
        )
        self.assertLess(mig.index("Phase 2 — plan"), mig.index("Phase 3 — execute"))
        self.assertLess(mig.index("Phase 3 — execute"), mig.index("Phase 4 — verify"))
        # the gate before any file moves; the plan's home; reversibility; resumability
        self.assertIn("The owner's word on the plan comes before any file moves", mig)
        self.assertIn(".live-spec/adopt/", mig)
        self.assertIn("baseline commit", mig)
        self.assertIn("checkpoint", mig)

    def test_catchup_pair_and_machine_level(self):
        """M-217 (pair + once-per-machine legs)."""
        mig = read_flat("MIGRATION.md")
        self.assertIn("one inbox wish naming the other half's catch-up debt", mig)
        self.assertIn("runs the full adoption for that repo", mig)
        self.assertIn("once per machine", mig)
        self.assertIn("already-done check", mig)
        pair = read_flat("docs/pair-adoption.md")
        self.assertIn("one inbox wish naming the other half's catch-up debt", pair)


class TestCatchupHalfDoneSafety(unittest.TestCase):
    """M-218 — every step safe on a half-done state (INV-89)."""

    def test_precondition_and_merge_law(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("reads its precondition from the tree", mig)
        self.assertIn("already holds is reported done and skipped", mig)
        self.assertIn("merge file by file", mig)
        self.assertIn("never nest the old directory inside the new one", mig)
        self.assertIn("never overwrite the new form with the old", mig)
        self.assertIn("rides the plan to the owner's gate", mig)
        # the concrete born-of case: both state dirs exist
        self.assertIn("both exist", mig)
        # the installed set is read from disk, and the shared-profile write re-reads first
        self.assertIn("version lines of the skills actually installed", mig)
        self.assertIn("immediately before appending", mig)

    def test_never_a_bare_git_mv(self):
        """The old non-idempotent step 1 is gone: no unconditional rename instruction."""
        mig = read_flat("MIGRATION.md")
        self.assertNotIn(
            "`git mv .livespec .live-spec` — the host's pack folder",
            mig,
            "the old unconditional git-mv step is still in the guide",
        )


class TestCatchupPreserveAndRehome(unittest.TestCase):
    """M-219 — preserve facts, re-home them, one canonical list (INV-90)."""

    def test_no_blanket_rewrite_and_naming(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn(
            "Settled prose is rewritten only where the owner rejected it "
            "or where the new shape cannot hold it as written",
            mig,
        )
        self.assertIn("spec.file", mig)
        self.assertIn(".live-spec/checkpoints/", mig)

    def test_canonical_set_has_one_home(self):
        heading = "## The canonical document set"
        self.assertIn(heading, read_flat("adopt/ADOPT.md"))
        # adopt/START.md, the founding walk, joins the swept siblings (SPEC R308, INV-307).
        for other in ("docs/adoption.md", "docs/pair-adoption.md", "MIGRATION.md", "adopt/START.md"):
            self.assertNotIn(
                heading, read_flat(other),
                f"second canonical-set list in {other} — the one home is ADOPT.md",
            )
        self.assertIn("The canonical document set lives in `adopt/ADOPT.md`", read_flat("docs/adoption.md"))

    def test_the_two_shared_phase_headings_have_one_home(self):
        """The founding walk points at ADOPT.md's version-control and orient phases rather than
        restating them, so each heading text stands in ADOPT.md alone (SPEC R308, INV-307)."""
        for heading in ("Phase 0 — Version-control gate first",
                        "Phase 1 — Orient: read everything first"):
            self.assertIn(heading, read_flat("adopt/ADOPT.md"))
            for other in ("adopt/START.md", "MIGRATION.md", "docs/adoption.md",
                          "docs/pair-adoption.md"):
                self.assertNotIn(
                    heading, read_flat(other),
                    f"{other} restates an ADOPT.md phase heading — the one home is ADOPT.md",
                )

    def test_spec_file_row_in_defaults_table(self):
        self.assertIn("spec.file", read_all_flat("skills/live-spec-base/SKILL.md"))


class TestCatchupSelfTest(unittest.TestCase):
    """M-221 — the walk's before-and-after self-test and the named restore point (INV-92)."""

    def test_before_after_inventory_and_restore(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-92]", spec)
        mig = read_flat("MIGRATION.md")
        self.assertIn("pre-walk inventory", mig)
        self.assertIn("fingerprint", mig)
        self.assertIn("anchor multiset", mig)
        self.assertIn("at least as green as before", mig)
        self.assertIn("restore point", mig)
        self.assertIn("restore command", mig)

    def test_a_test_runner_rewritten_tracked_file_is_a_named_known_difference(self):
        """PLAN q-814, from the tlvphotos 2.7.0 -> 6.1.0 catch-up finding: the walk's own step 0
        fingerprints tracked content, but a host whose test suite rewrites a tracked file mid-walk
        (a timings or cache artifact, `tests/suite_timings.json` the case found) always shows that
        file as a difference at the rollback check — a false positive, not specific to tlvphotos,
        for any host whose test runner rewrites a tracked file. The guide now names that file class
        as an accounted-for difference by name, not by a plan item."""
        mig = read_flat("MIGRATION.md")
        self.assertIn("test runner rewrites", mig)
        self.assertIn("suite_timings.json", mig)
        self.assertIn("known, non-leak side effect", mig)
        # the named class sits in the same accounting paragraph as the plan-item classes, not off
        # on its own — a reader meets it as one more way a difference is accounted for
        para_start = mig.index("Every difference must be accounted for")
        para = mig[para_start:para_start + 900]
        self.assertIn("test runner rewrites", para)

    def test_test_runner_rewritten_tracked_file_no_longer_false_positives_the_rollback_check(self):
        """Behavioural proof, not string-only: a scratch repo models the walk's own fingerprint
        mechanism (`git ls-files -z | xargs shasum`) over a tracked file a 'before' suite run
        rewrites, exactly the tlvphotos shape (`tests/suite_timings.json`). The fingerprint delta
        this produces is real (first assertion) — the bug is not imagined. The guide's own known-
        difference sentence is what now waves that exact delta through the accounting rule instead
        of blocking the verify phase (second part): the same file name the fixture's diff names is
        the one the guide's text accounts for by name."""

        def _fingerprint(repo):
            out = subprocess.run(
                ["git", "ls-files"], cwd=repo, capture_output=True, text=True, check=True
            ).stdout.splitlines()
            digest = {}
            for relpath in out:
                with open(os.path.join(repo, relpath), "rb") as f:
                    digest[relpath] = hashlib.sha256(f.read()).hexdigest()
            return digest

        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
            subprocess.run(["git", "config", "user.email", "a@example.com"], cwd=tmp, check=True)
            subprocess.run(["git", "config", "user.name", "a"], cwd=tmp, check=True)
            timings_path = os.path.join(tmp, "tests", "suite_timings.json")
            os.makedirs(os.path.dirname(timings_path), exist_ok=True)
            with open(timings_path, "w", encoding="utf-8") as f:
                f.write('{"run": 1, "seconds": 12.3}\n')
            subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "before-walk baseline"], cwd=tmp, check=True)

            # step 0: the pre-walk fingerprint, taken exactly as found
            before = _fingerprint(tmp)

            # the "before" suite runs mid-walk and rewrites its own timings file, as a real test
            # runner does — nothing else in the tree changes
            with open(timings_path, "w", encoding="utf-8") as f:
                f.write('{"run": 2, "seconds": 11.9}\n')
            subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "suite run rewrote its timings file"], cwd=tmp,
                            check=True)

            # step 9: the post-walk fingerprint the rollback check compares against
            after = _fingerprint(tmp)

            diffed = {p for p in before if before.get(p) != after.get(p)}
            self.assertEqual(diffed, {"tests/suite_timings.json"},
                              "the fixture must reproduce exactly the one difference the finding "
                              "names — proof the bug is real, not the fix itself")

            # the fix: the guide's own accounting rule now names this exact file class, so a walk
            # applying it waves this diff through instead of blocking the verify phase on it
            mig = read_flat("MIGRATION.md")
            self.assertIn("suite_timings.json", mig)
            self.assertIn("test runner rewrites", mig)


class TestCatchupVersionChain(unittest.TestCase):
    """M-220 — per-version migration chapters, the chain walked oldest first (INV-91)."""

    def test_chapters_and_chain(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("## Migration chapters", mig)
        self.assertIn("### 1.0.0", mig)
        self.assertIn("oldest first", mig)
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("dated migration chapter", spec)

    def test_current_version_owes_a_chapter_or_says_nothing_owed(self):
        """INV-91: a release owing host action ships a dated MIGRATION chapter; a release owing
        nothing says so in its changelog. Red-proven 2026-08-13: VERSION read 5.0.0 (the external
        product-prover major, a host-visible install step) while the chapter chain ended at 4.3.0
        and the journal carried no owes-nothing line — the chain could route no host past 4.3.0."""
        version = read_flat("VERSION").strip()
        mig = read_flat("MIGRATION.md")
        # The DATED half, which this docstring has always stated and the check never held: a bare
        # `### 5.0.0 —` heading satisfied `f"### {version} " in mig` while carrying no date, so a
        # chapter a host cannot place in the chain passed as one that could.
        chapter = re.compile(r"###\s+%s\s+[—-]\s+\d{4}-\d{2}-\d{2}" % re.escape(version))
        if chapter.search(mig):
            return
        # The owes-nothing line must discharge THIS release. `version in line and "owes nothing" in
        # line` passed any sentence that mentioned the number anywhere — including prose about the
        # law itself — so the line is now read as one clause: the release, then what it owes.
        journal = read("JOURNAL.md")
        discharge = re.compile(r"\b%s\b[^.]{0,120}?owes nothing" % re.escape(version))
        self.assertTrue(
            any(discharge.search(line) for line in journal.splitlines()),
            f"VERSION {version} has no dated MIGRATION chapter and no changelog line tying it to "
            f"`owes nothing` — a host reading the chain cannot tell where {version} leaves them",
        )

    def test_versionless_record_starts_at_earliest_chapter(self):
        """The dry-read hole (2026-07-10): an old-format record has no readable version —
        the chain's start must be stated, in the spec and in the guide.

        RE-PINNED (see repin log): MIGRATION.md's sentence subject is "a record" ("... starts
        the chain..."), while PRODUCT_SPEC.md's rewritten Requirement 180 criterion 3 casts
        every clause as "the system *shall*..." ("...shall start the chain..." — grammatical
        conjugation only, same fact). The shared substring below matches the same meaning at
        both homes without depending on either home's subject/verb form.
        """
        for rel in ("MIGRATION.md", "PRODUCT_SPEC.md"):
            self.assertIn(
                "the chain at the earliest chapter", read_flat(rel),
                f"no-readable-version fallback missing in {rel}",
            )


class TestCatchupWalkVendorsTheStatusView(unittest.TestCase):
    """PLAN.md plan-14. `adopt/install-status-view.sh` was a founding-only step
    (`adopt/ADOPT.md`) — an already-adopted host running catch-up never got it, so the tool
    only ever reached a freshly founded host. Phase 4 gained a step re-running it the same
    unconditional, non-clobbering way `install-scaffold.sh --force` already runs there,
    right beside it."""

    def test_install_status_view_runs_in_phase_4(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("adopt/install-status-view.sh", mig)
        phase4 = mig[mig.index("Phase 4 — verify"):]
        self.assertIn(
            "adopt/install-status-view.sh", phase4,
            "install-status-view.sh must run inside Phase 4, not only in ADOPT.md's founding walk",
        )
        self.assertLess(
            phase4.index("install-scaffold.sh --force"),
            phase4.index("install-status-view.sh"),
            "the status-view re-vendor step should sit right after the gate-scaffold one it mirrors",
        )


class TestCatchupWalkVendorsTheStyleGateKit(unittest.TestCase):
    """PLAN.md, the preshow-lint-script-missing finding (`inbox/2026-08-12-preshow-lint-script-missing.md`).
    `adopt/install-style-gates.sh` was a founding-only step (`adopt/ADOPT.md`, "Then wire the style
    gate") — an already-adopted host running catch-up never re-ran it, so a file the kit later grew
    (`scripts/preshow-register-lint.py`, added to VENDOR_FILES beside `guardrails/spec-coinages.json`)
    only ever reached a freshly founded host. Phase 4 now runs it the same unconditional,
    non-clobbering way `install-status-view.sh` already runs there, right beside it."""

    def test_install_style_gates_runs_in_phase_4(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("adopt/install-style-gates.sh --force", mig)
        phase4 = mig[mig.index("Phase 4 — verify"):]
        self.assertIn(
            "adopt/install-style-gates.sh --force", phase4,
            "install-style-gates.sh must run inside Phase 4, not only in ADOPT.md's founding walk",
        )
        self.assertLess(
            phase4.index("install-status-view.sh"),
            phase4.index("install-style-gates.sh --force"),
            "the style-gate re-vendor step should sit right after the status-view one it mirrors",
        )


if __name__ == "__main__":
    unittest.main()
