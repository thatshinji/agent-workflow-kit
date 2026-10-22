#!/usr/bin/env python3
"""One-command installer for the agent-workflow-kit.

Zero-dependency (Python 3.9+ stdlib only). Lays the workflow templates and
the TDD gate into one of your own repositories, so adopting the kit is one
command instead of a dozen manual copies:

    python3 scripts/install.py [--target DIR] [--lang en|zh-CN]
                               [--stack go|web|swift|python ...]
                               [--dry-run] [--force]

The kit root is derived from this script's location (scripts/ lives one
level below it), so the installer works from any working directory.

No local clone? This script can bootstrap itself: when it cannot find a
kit next to itself (for example when piped in over stdin), it downloads
the kit source archive from GitHub into a temp directory, installs from
there, and cleans up. Adoption becomes a single line:

    curl -fsSL https://raw.githubusercontent.com/thatshinji/agent-workflow-kit/v0.3.2/scripts/install.py | python3 - [--lang zh-CN]

Bootstrap downloads the release named by --kit-version (default v0.3.2;
"latest" resolves the newest release through the GitHub API). The flag
is ignored when a local kit is found next to the script.

What lands where (target side):

    AGENTS.md, REVIEW.md                      repository root
    docs/test-cases/{TEMPLATE,INDEX}.md       behavior-case library skeleton
    docs/project-management/*.md|yaml         pipeline specs and review ledger
    docs/tech-specs/coding-standards.md       living style baseline
    scripts/check_tdd_compliance.py           the TDD compliance gate
    tdd-check.config.json                     gate config (from the example)

Options:

  --lang zh-CN   Install the Chinese template editions — under the plain,
                 unsuffixed target names, so your repository stays
                 single-language and the templates' internal links work
                 as-is. Scripts and JSON are identical in both languages.
  --stack        Also install a lint starter config from
                 templates/lint-starters/ at the target root. Repeatable:
                 go -> .golangci.yml, web -> eslint.config.mjs,
                 swift -> .swiftlint.yml, python -> ruff.toml.
  --kit-version  Bootstrap mode only: which kit release to download
                 (a tag such as v0.3.2, or "latest" for the newest
                 release). Ignored when the script runs from a local
                 clone, where the files next to it are the source.

Safety:

  - Existing target files are never overwritten silently: each is skipped
    and reported. --force overwrites, and reports that too.
  - --dry-run prints the plan and writes nothing.
  - A target that is not a git repository gets a one-line warning on
    stderr, not a stop — the files are just as useful in a plain folder.

Exit codes: 0 = done (any mix of installed / skipped / planned),
2 = a kit source file is missing (each one is named), the bootstrap
download failed, or a usage error.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

KIT_REPO = "thatshinji/agent-workflow-kit"
KIT_VERSION = "v0.3.2"

ARCHIVE_URL_TEMPLATE = "https://github.com/{repo}/archive/refs/tags/{tag}.zip"
LATEST_RELEASE_API = "https://api.github.com/repos/{repo}/releases/latest"
USER_AGENT = "agent-workflow-kit-installer"


def _local_kit_root() -> Path | None:
    """The kit root next to this script, or None when there is none.

    Running from a clone, this file lives at <kit>/scripts/install.py and
    the kit root is its grandparent — valid only if templates/ is really
    there. Piped over stdin (curl | python3 -), __file__ is undefined and
    there is no local kit at all; a copy of the script on its own (no
    templates/ next to it) is in the same position.
    """
    try:
        script = Path(__file__).resolve()
    except NameError:
        return None
    root = script.parent.parent
    return root if (root / "templates").is_dir() else None


# The local kit root when this script runs from a clone; None means
# bootstrap mode (see fetch_kit). Tests may substitute either value.
KIT_ROOT: Path | None = _local_kit_root()

# (source relative to the kit root, destination relative to the target repo).
# Template sources are language-selected by localized_source(); the target
# names never carry a language suffix.
TEMPLATE_FILES = [
    ("templates/AGENTS.md", "AGENTS.md"),
    ("templates/REVIEW.md", "REVIEW.md"),
    ("templates/test-cases/TEMPLATE.md", "docs/test-cases/TEMPLATE.md"),
    ("templates/test-cases/INDEX.md", "docs/test-cases/INDEX.md"),
    ("templates/project-management/README.md", "docs/project-management/README.md"),
    ("templates/project-management/review-protocol.md", "docs/project-management/review-protocol.md"),
    ("templates/project-management/tdd-workflow-spec.md", "docs/project-management/tdd-workflow-spec.md"),
    ("templates/project-management/contract-checklist.md", "docs/project-management/contract-checklist.md"),
    ("templates/project-management/platform-playbook.md", "docs/project-management/platform-playbook.md"),
    ("templates/project-management/reviews-ledger.yaml", "docs/project-management/reviews-ledger.yaml"),
    ("templates/specs/coding-standards.md", "docs/tech-specs/coding-standards.md"),
]

# Language-independent files: identical bytes for en and zh-CN installs.
KIT_FILES = [
    ("scripts/check_tdd_compliance.py", "scripts/check_tdd_compliance.py"),
    ("scripts/tdd-check.config.example.json", "tdd-check.config.json"),
]

STACK_FILES = {
    "go": ("templates/lint-starters/go/.golangci.yml", ".golangci.yml"),
    "web": ("templates/lint-starters/web/eslint.config.mjs", "eslint.config.mjs"),
    "swift": ("templates/lint-starters/swift/.swiftlint.yml", ".swiftlint.yml"),
    "python": ("templates/lint-starters/python/ruff.toml", "ruff.toml"),
}

NEXT_STEPS = [
    "Fill in the <slot> placeholders in AGENTS.md and REVIEW.md for your project.",
    "Adapt tdd-check.config.json to your stack's directory layout.",
    "Run the gate once: python3 scripts/check_tdd_compliance.py",
]


class BootstrapError(Exception):
    """The kit source could not be downloaded or unpacked."""


def kit_archive_url(tag: str) -> str:
    """The source-archive URL for one kit release tag."""
    return ARCHIVE_URL_TEMPLATE.format(repo=KIT_REPO, tag=tag)


def _download(url: str, dest: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response, dest.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def _latest_tag() -> str:
    """Resolve "latest" to a release tag via the GitHub API."""
    url = LATEST_RELEASE_API.format(repo=KIT_REPO)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
    except (OSError, ValueError) as exc:
        raise BootstrapError(
            f"could not look up the latest kit release at {url}: {exc}"
        ) from exc
    tag = data.get("tag_name") if isinstance(data, dict) else None
    if not tag:
        raise BootstrapError(f"no tag_name in the GitHub response from {url}")
    return tag


def fetch_kit(version: str, dest: Path) -> Path:
    """Download the kit source for `version` into dest; return its root.

    `version` is a release tag (e.g. "v0.3.2") or "latest". Raises
    BootstrapError on any network or archive failure. Kept small and
    module-level so tests can substitute it and never touch the network.
    """
    try:
        tag = _latest_tag() if version == "latest" else version
        url = kit_archive_url(tag)
        archive = dest / "kit.zip"
        _download(url, archive)
        unpacked = dest / "unpacked"
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(unpacked)
    except BootstrapError:
        raise
    except (OSError, zipfile.BadZipFile) as exc:
        raise BootstrapError(
            f"could not download or unpack the kit source "
            f"(version {version!r}): {exc}"
        ) from exc
    roots = [p for p in unpacked.iterdir() if p.is_dir()]
    if len(roots) != 1 or not (roots[0] / "templates").is_dir():
        raise BootstrapError(
            f"the archive for version {version!r} does not look like "
            "the kit source (no single root with templates/)"
        )
    return roots[0]


def localized_source(source_rel: str, lang: str) -> str:
    """Map a template source to its --lang edition.

    templates/AGENTS.md -> templates/AGENTS.zh-CN.md (lang "zh-CN");
    lang "en" is the identity. Only the source name changes — targets
    are always the plain names from TEMPLATE_FILES.
    """
    if lang == "en":
        return source_rel
    head, dot, ext = source_rel.rpartition(".")
    return f"{head}.{lang}{dot}{ext}"


def build_plan(lang: str, stacks: list[str]) -> list[tuple[str, str]]:
    """The full (source, destination) list for one install run."""
    plan = [(localized_source(src, lang), dst) for src, dst in TEMPLATE_FILES]
    plan += KIT_FILES
    for stack in stacks:
        plan.append(STACK_FILES[stack])
    return plan


def run_plan(
    plan: list[tuple[str, str]], kit_root: Path, target: Path,
    dry_run: bool, force: bool
) -> tuple[list[str], list[str], list[str]]:
    """Execute (or, for dry runs, rehearse) the plan.

    Returns (installed, skipped, planned) destination paths and prints one
    line per file as it goes. Existing files are skipped unless force is
    set; a skipped file is never touched.
    """
    installed: list[str] = []
    skipped: list[str] = []
    planned: list[str] = []
    for src_rel, dst_rel in plan:
        src = kit_root / src_rel
        dst = target / dst_rel
        exists = dst.exists()
        if exists and not force:
            skipped.append(dst_rel)
            print(f"  skipped    {dst_rel} (already exists; --force overwrites)")
            continue
        if dry_run:
            planned.append(dst_rel)
            suffix = " (would overwrite)" if exists else ""
            print(f"  planned    {dst_rel}{suffix}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        installed.append(dst_rel)
        suffix = " (overwrote existing)" if exists else ""
        print(f"  installed  {dst_rel}{suffix}")
    return installed, skipped, planned


def print_summary(
    installed: list[str], skipped: list[str], planned: list[str]
) -> None:
    print()
    print("Install summary:")
    for title, items in (
        ("Installed", installed),
        ("Skipped", skipped),
        ("Planned", planned),
    ):
        print(f"  {title} ({len(items)}):")
        if items:
            for item in items:
                print(f"    - {item}")
        else:
            print("    (none)")
    print()
    print("Next steps:")
    for i, step in enumerate(NEXT_STEPS, 1):
        print(f"  {i}. {step}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install agent-workflow-kit templates and gate scripts "
        "into your own repository"
    )
    parser.add_argument(
        "--target", default=".",
        help="repository to install into (default: current directory)",
    )
    parser.add_argument(
        "--lang", choices=["en", "zh-CN"], default="en",
        help="template language (default: en)",
    )
    parser.add_argument(
        "--stack", action="append", choices=sorted(STACK_FILES), default=[],
        metavar="STACK",
        help="also install a lint starter config; repeatable "
        "(go, web, swift, python)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="print the plan and write nothing",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="overwrite existing target files (each overwrite is reported)",
    )
    parser.add_argument(
        "--kit-version", default=KIT_VERSION, metavar="TAG",
        help="bootstrap mode only: kit release to download (a tag such "
        f"as {KIT_VERSION}, or 'latest'); ignored when a local kit is "
        f"found next to this script (default: {KIT_VERSION})",
    )
    args = parser.parse_args(argv)

    target = Path(args.target)
    stacks = list(dict.fromkeys(args.stack))  # dedupe, keep order
    plan = build_plan(args.lang, stacks)

    kit_root = KIT_ROOT
    tmp_dir: Path | None = None
    if kit_root is None:
        # Bootstrap mode: no kit next to this script (e.g. it was piped
        # in over stdin). Download the source into a temp directory and
        # install from there; the finally clause below removes it.
        tmp_dir = Path(tempfile.mkdtemp(prefix="agent-workflow-kit-"))
        print(
            "note: no local kit found; downloading the kit source "
            f"({args.kit_version}) from github.com",
            file=sys.stderr,
        )
        try:
            kit_root = fetch_kit(args.kit_version, tmp_dir)
        except BootstrapError as exc:
            print(f"error: bootstrap failed: {exc}", file=sys.stderr)
            print(
                "hint: bootstrap mode needs network access to github.com; "
                f"alternatively, clone https://github.com/{KIT_REPO} and "
                "run scripts/install.py from the clone instead.",
                file=sys.stderr,
            )
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return 2
    try:
        missing = [src for src, _ in plan if not (kit_root / src).is_file()]
        if missing:
            for src in missing:
                print(
                    f"error: kit source file missing: {src}", file=sys.stderr
                )
            return 2

        if not (target / ".git").exists():
            print(
                f"warning: {target} is not a git repository; "
                "installing anyway",
                file=sys.stderr,
            )

        installed, skipped, planned = run_plan(
            plan, kit_root, target, args.dry_run, args.force
        )
        print_summary(installed, skipped, planned)
        return 0
    finally:
        if tmp_dir is not None:
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
