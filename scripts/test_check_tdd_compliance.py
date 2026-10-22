#!/usr/bin/env python3
"""Unit tests for check_tdd_compliance.py (stdlib unittest, no dependencies).

Run:  python3 -m unittest test_check_tdd_compliance -v     (from scripts/)
Covers: glob matching incl. brace expansion, classification, pairing rules,
negative-assertion detection, pass-through behavior, config loading errors.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_tdd_compliance as gate

CONFIG = gate.DEFAULT_CONFIG


class TestGlobMatching(unittest.TestCase):
    def test_brace_expansion(self):
        pats = gate.expand_braces("src/**/*.{ts,tsx}")
        self.assertIn("src/**/*.ts", pats)
        self.assertIn("src/**/*.tsx", pats)

    def test_plain_pattern_unchanged(self):
        self.assertEqual(gate.expand_braces("a/b.go"), ["a/b.go"])

    def test_double_star_matches_nested(self):
        self.assertTrue(gate.matches_any("server/internal/api/handler.go", ["server/**/*.go"]))

    def test_no_match(self):
        self.assertFalse(gate.matches_any("README.md", ["server/**/*.go"]))


class TestClassify(unittest.TestCase):
    def test_test_file(self):
        kind, area = gate.classify("server/internal/api/handler_test.go", CONFIG)
        self.assertEqual((kind, area), ("test", "backend"))

    def test_source_file(self):
        kind, area = gate.classify("server/internal/api/handler.go", CONFIG)
        self.assertEqual((kind, area), ("source", "backend"))

    def test_exempt_beats_source(self):
        kind, _ = gate.classify("server/internal/repository/users.sql.go", CONFIG)
        self.assertEqual(kind, "exempt")

    def test_web_test_with_brace_glob(self):
        kind, area = gate.classify("apps/web/src/pages/Login.test.tsx", CONFIG)
        self.assertEqual((kind, area), ("test", "web"))

    def test_passthrough_doc(self):
        kind, _ = gate.classify("docs/specs/contract.md", CONFIG)
        self.assertEqual(kind, "passthrough")


class TestPairingRule(unittest.TestCase):
    def test_source_without_test_fails(self):
        v = gate.check(["server/internal/api/handler.go"], "", CONFIG)
        self.assertEqual(len(v), 1)
        self.assertIn("backend", v[0])

    def test_source_with_test_passes_pairing(self):
        v = gate.check(
            ["server/internal/api/handler.go", "server/internal/api/handler_test.go"],
            "expect 403 forbidden",
            CONFIG,
        )
        self.assertEqual(v, [])

    def test_cross_area_test_does_not_satisfy_pairing(self):
        v = gate.check(
            ["server/internal/api/handler.go", "apps/web/src/pages/Login.test.tsx"],
            "error 500",
            CONFIG,
        )
        self.assertTrue(any("backend" in msg for msg in v))

    def test_exempt_only_change_passes(self):
        v = gate.check(["server/internal/repository/users.sql.go"], "", CONFIG)
        self.assertEqual(v, [])


class TestNegativeRule(unittest.TestCase):
    def test_happy_path_only_test_fails(self):
        v = gate.check(
            ["server/internal/api/handler_test.go"],
            "user := createUser(); assert name equals input",
            CONFIG,
        )
        self.assertEqual(len(v), 1)

    def test_status_code_counts_as_negative(self):
        v = gate.check(
            ["server/internal/api/handler_test.go"],
            "if resp.Code != 403 { t.Fail() }",
            CONFIG,
        )
        self.assertEqual(v, [])

    def test_case_insensitive_keyword(self):
        v = gate.check(
            ["apps/web/src/pages/Login.test.tsx"],
            "await expect(submit()).rejects.toThrow()",
            CONFIG,
        )
        self.assertEqual(v, [])


class TestPassthrough(unittest.TestCase):
    def test_docs_only_passes(self):
        self.assertEqual(gate.check(["docs/a.md", "README.md"], "", CONFIG), [])

    def test_config_only_passes(self):
        self.assertEqual(gate.check([".github/workflows/ci.yml"], "", CONFIG), [])

    def test_empty_change_passes(self):
        self.assertEqual(gate.check([], "", CONFIG), [])


class TestConfigLoading(unittest.TestCase):
    def test_invalid_json_returns_exit_2(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write("{ not json")
            path = fh.name
        try:
            self.assertEqual(gate.main(["--config", path]), 2)
        finally:
            os.unlink(path)

    def test_example_shaped_config_is_valid_json(self):
        cfg = json.dumps(CONFIG)
        self.assertIn("areas", json.loads(cfg))


if __name__ == "__main__":
    unittest.main()
