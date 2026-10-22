English | [简体中文](README.zh-CN.md)

# Lint starters

Ready-to-copy lint configs for the stacks this kit's adapter layer covers. Copy the folder for your stack into your project, then tune rule by rule against real false positives — do not bulk-import a giant rule pack on day one.

## The principle: block new code only

Every config here enforces the rules **only on new files and changed lines**; pre-existing issues are exempt and get cleaned up as files are touched.

Why: a rule only exists if it can fail a build. If you turn on a linter against a legacy codebase all at once, you get hundreds of findings, the team either spends a week on cleanup or — worse — someone downgrades the critical rules to `warn` to make CI green again. A `warn` keeps CI green and therefore does not exist as a rule. Starting with new-code-only enforcement means the rules have teeth from day one, the legacy debt shrinks every time a file is touched, and nobody is ever blocked by someone else's old code.

Two companion rules, from the coding standards:

- **Critical rules are `error` level.** Style preferences can warn; correctness rules never do.
- **Tool versions are pinned in CI.** No `@latest`, no floating ranges for the linter itself: a CI result must depend only on the repository's content, never on what a tool released last night.

## Go — golangci-lint

Config: [`go/.golangci.yml`](go/.golangci.yml). Copy it to your backend root.

- **What it is**: golangci-lint running a small base set — `errcheck`, `gosimple`, `govet`, `ineffassign`, `staticcheck`, `unused`. These catch real bugs (unchecked errors, dead code, unreachable assignments), not style. Style-heavy packs (e.g. revive) stay off until this base set runs clean.
- **Why error**: golangci-lint findings fail the run by default; keep it that way. The moment you add `--issues-exit-code=0` or downgrade, the rules stop existing.
- **New code only**: built in — `issues.new-from-rev: origin/master` makes golangci-lint report only findings on lines changed since `origin/master`. Point it at your default branch if it isn't `master`.
- **Pin the version**: in CI, install an exact version, e.g. the official action with `version: v1.64.8` (pick your version, but write the full number). Never `latest`.

## Web — ESLint (flat config)

Config: [`web/eslint.config.mjs`](web/eslint.config.mjs). Copy it to your web app root.

- **What it is**: ESLint flat config combining typescript-eslint's recommended set with eslint-plugin-react-hooks, plus one deliberate upgrade: `@typescript-eslint/no-explicit-any` is set to `error`, not the recommended `warn`. `any` silently disables the type system exactly where a human (or an AI writer) was in a hurry — and a `warn` has no constraining power over an AI writer, because the build stays green either way.
- **New code only**: ESLint has no "changed lines" mode, so enforce it in CI by linting only the files a PR touches:

```bash
git diff --name-only --diff-filter=ACM origin/master...HEAD -- '*.ts' '*.tsx' \
  | xargs -r npx eslint
```

  A legacy file only gets linted when someone modifies it — and then only that file, which is a fair price for touching it.
- **Pin the version**: pin `eslint`, `typescript-eslint`, and `eslint-plugin-react-hooks` to exact versions in `devDependencies` and commit the lockfile.

## Swift — SwiftLint

Config: [`swift/.swiftlint.yml`](swift/.swiftlint.yml). Copy it to your app root.

- **What it is**: SwiftLint's default rule set, plus exactly one opt-in rule on day one: `force_unwrapping`. Force-unwrapping external or optional data is the classic crash source, and the coding standards ban it — so it is opted in from the start instead of waiting for the first crash report.
- **Line length** warns at 120. It is a warning on purpose: line length is a style preference, not a correctness rule, and style preferences don't get to block merges.
- **New code only**: SwiftLint lints whole files. If you want strict new-code-only enforcement, run it in CI on the files changed in the PR (same `git diff --name-only` trick as the web stack). Running it repo-wide is also acceptable here because the default set is conservative.
- **Pin the version & tune slowly**: pin the SwiftLint version in CI (exact release, not a branch). Expect to tune: start from defaults, and when a rule produces a false positive, adjust that one rule with a comment saying why — never disable the tool, and never adopt a giant shared config wholesale.

## Python — Ruff

Config: [`python/ruff.toml`](python/ruff.toml). Copy it to your project root (or merge the `[lint]` section into `pyproject.toml`).

- **What it is**: Ruff with a compact rule selection — `E` (pycodestyle errors), `F` (pyflakes: unused imports, undefined names), `I` (import sorting), `UP` (pyupgrade: modern syntax), `B` (bugbear: likely bugs). Line length 100. These are bug-and-hygiene rules, not formatting opinions; formatting is Ruff's formatter's job (`ruff format`), configured separately.
- **Why error**: Ruff exits non-zero on any selected finding by default. Keep it that way — no `--exit-zero`.
- **New code only**: Ruff has no built-in "only new lines" mode, so scope it in CI to the files a PR changes:

```bash
git diff --name-only --diff-filter=ACM origin/master...HEAD -- '*.py' \
  | xargs -r ruff check
```

- **Pin the version**: pin Ruff exactly wherever CI installs it (e.g. `pip install ruff==0.9.0` — pick your version, write the full number).

## Files

| File | Stack | Copy to |
|---|---|---|
| `go/.golangci.yml` | Go (golangci-lint) | backend project root |
| `web/eslint.config.mjs` | Web (ESLint + TypeScript + React) | web app root |
| `swift/.swiftlint.yml` | Swift (SwiftLint) | app project root |
| `python/ruff.toml` | Python (Ruff) | project root |
