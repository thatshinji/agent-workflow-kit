#!/usr/bin/env python3
"""TDD compliance gate for the agent-workflow-kit pipeline.

Zero-dependency (Python 3.9+ stdlib only). Run it in any git repository:

    python3 scripts/check_tdd_compliance.py [--config PATH] [--base REF]

What it enforces (see docs/project-management/tdd-workflow-spec.md §4):

  R1/R2 Pairing  — when production source files in a configured "area" change,
                   the same change set must also change test files in that area.
  R3 Negatives   — when test files change, the added test content must contain
                   at least one negative/boundary assertion (keyword match).
  Pass-through   — documentation-only or config-only changes pass automatically.
                   The gate never judges code that predates its adoption.

Configuration is JSON (default: ./tdd-check.config.json). A fully commented
example ships next to this script as tdd-check.config.example.json.

Exit codes: 0 = PASS, 1 = FAIL (violations listed), 2 = usage/config error.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys

DEFAULT_CONFIG = {
    "areas": [
        {
            "name": "backend",
            "source_globs": ["server/**/*.go"],
            "test_globs": ["server/**/*_test.go"],
            "exempt_globs": ["server/internal/repository/*.sql.go"],
        },
        {
            "name": "web",
            "source_globs": ["apps/web/src/**/*.{ts,tsx}"],
            "test_globs": ["apps/web/src/**/*.test.{ts,tsx}"],
            "exempt_globs": ["apps/web/src/main.tsx", "apps/web/src/vite-env.d.ts"],
        },
    ],
    # Files that never trigger the gate when they are the only changes.
    "passthrough_globs": ["docs/**", "*.md", "Makefile", ".github/**", "*.json", "*.yaml", "*.yml", "*.toml"],
    # Added test content must contain at least one of these (case-insensitive).
    "negative_keywords": [
        "400", "401", "403", "404", "409", "410", "429", "500",
        "error", "invalid", "reject", "denied", "forbidden", "unauthorized",
        "tothrow", "expectthrows", "assertraises",
    ],
}


def expand_braces(pattern: str) -> list[str]:
    """Expand one level of {a,b,c} alternation in a glob pattern."""
    start = pattern.find("{")
    if start == -1:
        return [pattern]
    end = pattern.find("}", start)
    if end == -1:
        return [pattern]
    head, tail = pattern[:start], pattern[end + 1:]
    options = pattern[start + 1:end].split(",")
    out: list[str] = []
    for opt in options:
        out.extend(expand_braces(head + opt + tail))
    return out


def matches_any(path: str, globs: list[str]) -> bool:
    for glob in globs:
        for pat in expand_braces(glob):
            if fnmatch.fnmatch(path, pat):
                return True
    return False


def classify(path: str, config: dict) -> tuple[str, str | None]:
    """Return (kind, area_name): kind in test|source|exempt|passthrough|other."""
    for area in config["areas"]:
        if matches_any(path, area.get("exempt_globs", [])):
            return "exempt", area["name"]
    for area in config["areas"]:
        if matches_any(path, area.get("test_globs", [])):
            return "test", area["name"]
    for area in config["areas"]:
        if matches_any(path, area.get("source_globs", [])):
            return "source", area["name"]
    if matches_any(path, config.get("passthrough_globs", [])):
        return "passthrough", None
    return "other", None


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_files(base: str) -> list[str]:
    """Files changed vs base (committed) plus working-tree and untracked files."""
    files: set[str] = set()
    out = git("diff", "--name-only", f"{base}...HEAD")
    files.update(p for p in out.splitlines() if p)
    out = git("diff", "--name-only")
    files.update(p for p in out.splitlines() if p)
    out = git("diff", "--name-only", "--cached")
    files.update(p for p in out.splitlines() if p)
    out = git("ls-files", "--others", "--exclude-standard")
    files.update(p for p in out.splitlines() if p)
    return sorted(files)


def added_lines(base: str, paths: list[str]) -> str:
    """All added lines ('+' diff lines) for the given paths, committed + working."""
    if not paths:
        return ""
    chunks = []
    for spec in (f"{base}...HEAD", None, "--cached"):
        args = ["diff", "--unified=0"]
        if spec:
            args.append(spec)
        args += ["--", *paths]
        try:
            chunks.append(git(*args))
        except RuntimeError:
            continue
    added = []
    for line in "\n".join(chunks).splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    return "\n".join(added)


def check(changed: list[str], added_test_text: str, config: dict) -> list[str]:
    """Pure rule evaluation. Returns a list of violation messages (empty = pass)."""
    classified = [(p, *classify(p, config)) for p in changed]
    business = [c for c in classified if c[1] in ("source", "test")]
    if not business:
        return []  # docs/config/other only -> pass-through

    violations: list[str] = []
    areas_with_source = {c[2] for c in classified if c[1] == "source"}
    areas_with_tests = {c[2] for c in classified if c[1] == "test"}
    for area in sorted(areas_with_source - areas_with_tests):
        files = [c[0] for c in classified if c[1] == "source" and c[2] == area]
        violations.append(
            f"[{area}] production files changed without any test file change: "
            + ", ".join(files)
        )

    test_files = [c[0] for c in classified if c[1] == "test"]
    if test_files:
        haystack = added_test_text.lower()
        keywords = [k.lower() for k in config.get("negative_keywords", [])]
        if keywords and not any(k in haystack for k in keywords):
            violations.append(
                "test files changed but no negative/boundary assertion found "
                f"(looked for any of: {', '.join(keywords)}) in: " + ", ".join(test_files)
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TDD compliance gate")
    parser.add_argument("--config", default="tdd-check.config.json",
                        help="path to config JSON (falls back to built-in defaults)")
    parser.add_argument("--base", default="origin/master",
                        help="git ref to diff against (default: origin/master)")
    args = parser.parse_args(argv)

    config = DEFAULT_CONFIG
    try:
        with open(args.config, encoding="utf-8") as fh:
            config = json.load(fh)
    except FileNotFoundError:
        print(f"note: {args.config} not found, using built-in defaults", file=sys.stderr)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {args.config}: {exc}", file=sys.stderr)
        return 2

    try:
        changed = changed_files(args.base)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    test_paths = [p for p in changed if classify(p, config)[0] == "test"]
    try:
        text = added_lines(args.base, test_paths)
    except RuntimeError:
        text = ""
    violations = check(changed, text, config)
    if violations:
        print("TDD compliance: FAIL")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"TDD compliance: PASS ({len(changed)} changed file(s) checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
