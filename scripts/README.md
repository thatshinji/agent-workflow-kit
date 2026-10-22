English | [简体中文](README.zh-CN.md)

# Scripts

Stack-agnostic gate scripts for the workflow. Everything here is zero-dependency and safe to copy into any repository.

## check_tdd_compliance.py

The TDD compliance gate from the TDD workflow spec (§4). It inspects the current change set (`git diff` against a base ref, plus staged, unstaged, and untracked files) and enforces:

- **Pairing** — production files changed in a configured area must be accompanied by test file changes *in the same area*.
- **Negative assertions** — changed test files must add at least one negative/boundary assertion (keyword-based: HTTP error statuses, `invalid`, `rejects`, `assertThrows`, …).
- **Pass-through** — documentation/config-only changes pass automatically; the gate never judges pre-existing code.

### Usage

```bash
# 1. Configure: copy the example and adapt the globs to your layout
cp scripts/tdd-check.config.example.json tdd-check.config.json

# 2. Run locally (defaults: config ./tdd-check.config.json, base origin/master)
python3 scripts/check_tdd_compliance.py
python3 scripts/check_tdd_compliance.py --base HEAD~1

# Exit codes: 0 PASS · 1 FAIL (violations printed) · 2 config/usage error
```

### Wiring it into your one-command gate

Makefile (add to your lint target so `make pr-check` includes it):

```make
tdd-check:
	python3 scripts/check_tdd_compliance.py --base origin/master
```

GitHub Actions (inside the job that runs your lint suite):

```yaml
- name: TDD compliance
  run: python3 scripts/check_tdd_compliance.py --base origin/${{ github.base_ref }}
```

Note the checkout needs history for the base ref (`fetch-depth: 0` on `actions/checkout`).

### Tests

The checker ships with its own tests, per the kit's rule that every script is tested, including invalid-input cases:

```bash
cd scripts && python3 -m unittest test_check_tdd_compliance -v
```

### Honest limits

Keyword matching is a floor, not a proof: it guarantees *some* negative assertion text exists, not that the assertion is meaningful. Meaning is the reviewer's job (REVIEW.md §5) — this gate exists so the reviewer never has to spend a round on "no negative cases at all".
