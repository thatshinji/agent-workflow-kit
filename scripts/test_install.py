#!/usr/bin/env python3
"""Unit tests for install.py (stdlib unittest, no dependencies).

Run:  python3 -m unittest test_install -v     (from scripts/)
Covers: fresh install lands everything byte-identical to the kit sources,
re-running skips everything, --lang zh-CN picks the Chinese sources under
plain target names, --dry-run writes nothing, --force overwrites local
edits, --stack installs the lint starter, missing sources exit 2, and
bootstrap mode (no local kit: the download function is substituted with
a fake, so these tests never touch the network).
"""

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import install as installer

REAL_KIT_ROOT = installer.KIT_ROOT
PLAN = installer.build_plan("en", [])


def make_fake_kit_root(dest):
    """A minimal stand-in kit root under dest: the real templates/ and
    scripts/ trees, copied. Used as the bootstrap download's result."""
    root = Path(dest) / "agent-workflow-kit-fake"
    shutil.copytree(REAL_KIT_ROOT / "templates", root / "templates")
    shutil.copytree(REAL_KIT_ROOT / "scripts", root / "scripts")
    return root


def run_install(argv):
    """Run installer.main with stdout/stderr captured; return (code, out, err)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = installer.main(argv)
    return code, out.getvalue(), err.getvalue()


class InstallTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.target = Path(self._tmp.name) / "repo"
        self.target.mkdir()

    def install(self, *extra):
        return run_install(["--target", str(self.target), *extra])


class TestFreshInstall(InstallTestCase):
    def test_everything_lands_byte_identical(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        for src_rel, dst_rel in PLAN:
            landed = self.target / dst_rel
            self.assertTrue(landed.is_file(), f"missing: {dst_rel}")
            self.assertEqual(
                landed.read_bytes(),
                (REAL_KIT_ROOT / src_rel).read_bytes(),
                f"content differs: {dst_rel}",
            )

    def test_example_config_becomes_live_config(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        landed = self.target / "tdd-check.config.json"
        example = REAL_KIT_ROOT / "scripts/tdd-check.config.example.json"
        self.assertEqual(landed.read_bytes(), example.read_bytes())

    def test_gate_script_lands_under_scripts(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        self.assertTrue((self.target / "scripts/check_tdd_compliance.py").is_file())


class TestRerunSkips(InstallTestCase):
    def test_second_run_skips_everything_and_touches_nothing(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        agents = self.target / "AGENTS.md"
        agents.write_bytes(b"local edits the user made\n")
        code, out, _err = self.install()
        self.assertEqual(code, 0)
        self.assertIn(f"Skipped ({len(PLAN)}):", out)
        self.assertEqual(agents.read_bytes(), b"local edits the user made\n")


class TestLangZhCN(InstallTestCase):
    def test_chinese_sources_under_plain_target_names(self):
        code, _out, _err = self.install("--lang", "zh-CN")
        self.assertEqual(code, 0)
        agents = self.target / "AGENTS.md"
        zh_source = REAL_KIT_ROOT / "templates/AGENTS.zh-CN.md"
        self.assertEqual(agents.read_bytes(), zh_source.read_bytes())
        # No suffixed copies in the target: it stays single-language.
        self.assertFalse((self.target / "AGENTS.zh-CN.md").exists())

    def test_chinese_ledger_under_plain_name(self):
        code, _out, _err = self.install("--lang", "zh-CN")
        self.assertEqual(code, 0)
        ledger = self.target / "docs/project-management/reviews-ledger.yaml"
        zh_source = (
            REAL_KIT_ROOT / "templates/project-management/reviews-ledger.zh-CN.yaml"
        )
        self.assertEqual(ledger.read_bytes(), zh_source.read_bytes())


class TestDryRun(InstallTestCase):
    def test_dry_run_writes_nothing(self):
        code, out, _err = self.install("--dry-run")
        self.assertEqual(code, 0)
        files = [p for p in self.target.rglob("*") if p.is_file()]
        self.assertEqual(files, [])
        self.assertIn(f"Planned ({len(PLAN)}):", out)


class TestForce(InstallTestCase):
    def test_force_restores_locally_edited_file(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        agents = self.target / "AGENTS.md"
        agents.write_bytes(b"local edits the user made\n")
        code, out, _err = self.install("--force")
        self.assertEqual(code, 0)
        source = REAL_KIT_ROOT / "templates/AGENTS.md"
        self.assertEqual(agents.read_bytes(), source.read_bytes())
        self.assertIn(f"Installed ({len(PLAN)}):", out)


class TestStack(InstallTestCase):
    def test_stack_go_installs_golangci_config(self):
        # The lint-starters tree is built by a separate track; use a fake
        # kit root (real templates/scripts copied, sentinel Go config) so
        # this test does not depend on that track's progress.
        fake_root = Path(self._tmp.name) / "kit"
        shutil.copytree(REAL_KIT_ROOT / "templates", fake_root / "templates")
        shutil.copytree(REAL_KIT_ROOT / "scripts", fake_root / "scripts")
        go_dir = fake_root / "templates/lint-starters/go"
        go_dir.mkdir(parents=True, exist_ok=True)
        (go_dir / ".golangci.yml").write_bytes(b"# sentinel golangci config\n")
        old_root = installer.KIT_ROOT
        installer.KIT_ROOT = fake_root
        try:
            code, _out, _err = self.install("--stack", "go")
        finally:
            installer.KIT_ROOT = old_root
        self.assertEqual(code, 0)
        landed = self.target / ".golangci.yml"
        self.assertTrue(landed.is_file())
        self.assertEqual(landed.read_bytes(), b"# sentinel golangci config\n")


class TestMissingSource(InstallTestCase):
    def test_missing_source_exits_2_and_names_it(self):
        empty_root = Path(self._tmp.name) / "empty-kit"
        empty_root.mkdir()
        old_root = installer.KIT_ROOT
        installer.KIT_ROOT = empty_root
        try:
            code, _out, err = self.install()
        finally:
            installer.KIT_ROOT = old_root
        self.assertEqual(code, 2)
        self.assertIn("templates/AGENTS.md", err)


class TestBootstrap(InstallTestCase):
    """Bootstrap mode: no local kit (KIT_ROOT is None, as when the script
    is piped over stdin via curl). fetch_kit is substituted with a fake
    that builds a kit root inside the temp dir main hands it — no network.
    """

    def setUp(self):
        super().setUp()
        self.fetch_versions = []
        self._real_fetch = installer.fetch_kit
        self._real_root = installer.KIT_ROOT

        def fake_fetch(version, dest):
            self.fetch_versions.append(version)
            return make_fake_kit_root(dest)

        installer.fetch_kit = fake_fetch
        installer.KIT_ROOT = None
        self.addCleanup(self._restore_bootstrap)

    def _restore_bootstrap(self):
        installer.fetch_kit = self._real_fetch
        installer.KIT_ROOT = self._real_root

    def test_bootstrap_installs_when_local_kit_missing(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        self.assertEqual(len(self.fetch_versions), 1)
        for _src_rel, dst_rel in PLAN:
            landed = self.target / dst_rel
            self.assertTrue(landed.is_file(), f"missing: {dst_rel}")
        agents = self.target / "AGENTS.md"
        source = REAL_KIT_ROOT / "templates/AGENTS.md"
        self.assertEqual(agents.read_bytes(), source.read_bytes())

    def test_default_version_is_the_pinned_constant(self):
        code, _out, _err = self.install()
        self.assertEqual(code, 0)
        self.assertEqual(self.fetch_versions, [installer.KIT_VERSION])

    def test_kit_version_flag_is_passed_through(self):
        code, _out, _err = self.install("--kit-version", "v9.9.9-test")
        self.assertEqual(code, 0)
        self.assertEqual(self.fetch_versions, ["v9.9.9-test"])

    def test_bootstrap_dry_run_writes_nothing(self):
        code, out, _err = self.install("--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(len(self.fetch_versions), 1)
        files = [p for p in self.target.rglob("*") if p.is_file()]
        self.assertEqual(files, [])
        self.assertIn(f"Planned ({len(PLAN)}):", out)

    def test_bootstrap_failure_exits_2_with_hint(self):
        def failing_fetch(version, dest):
            raise installer.BootstrapError("simulated network failure")

        installer.fetch_kit = failing_fetch
        code, _out, err = self.install()
        self.assertEqual(code, 2)
        self.assertIn("simulated network failure", err)
        self.assertIn("clone https://github.com/", err)


class TestBootstrapUrls(unittest.TestCase):
    def test_archive_url_construction(self):
        self.assertEqual(
            installer.kit_archive_url("v1.2.3"),
            "https://github.com/thatshinji/agent-workflow-kit"
            "/archive/refs/tags/v1.2.3.zip",
        )

    def test_repo_and_version_constants(self):
        self.assertEqual(installer.KIT_REPO, "thatshinji/agent-workflow-kit")
        self.assertTrue(installer.KIT_VERSION.startswith("v"))


if __name__ == "__main__":
    unittest.main()
