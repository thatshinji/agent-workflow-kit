<!--
  TEMPLATE: docs/project-management/tdd-workflow-spec.md
  The TDD loop that runs inside pipeline step 5, plus the machine gate that
  keeps "tests first" from decaying into a slogan. Adapt the file patterns and
  negative-assertion keywords in §4 to your stack.
-->

# Multi-Agent TDD Workflow Spec

> Version: v1.0 · Effective: <YYYY-MM-DD>
> Scope: all agents and the decision-maker in this repository. Companion docs: `AGENTS.md` (pipeline), `REVIEW.md`, `review-protocol.md`.

## 1. Why this exists: test-after bias

When the same agent writes code first and tests afterwards, three failures repeat: tests mirror the implementation and miss contract boundaries; happy paths dominate and failure branches surface only in review, costing extra rounds; issue acceptance criteria never map 1:1 onto named tests. This spec removes all three by making tests **earlier, independent, and machine-checked**.

## 2. The four-step loop

```text
Step 0: Spec mapping (acceptance criteria → test matrix)
  → Step 1: RED (write failing tests, prove they fail)
  → Step 2: GREEN (minimal implementation)
  → Step 3: REFACTOR & GATE (clean up, pass the compliance gate)
  → Step 4: independent REVIEW (see REVIEW.md)
```

### Step 0 — Test matrix

Before any production code is touched, list the test matrix from the issue's acceptance criteria and the contract. Every feature includes:

- **Positive cases**: success responses, required fields, state changes.
- **Mandatory negative branches** (adapt to your domain; this is the default set):
  - input validation failures (empty, malformed, illegal enum, oversized, trailing garbage);
  - authentication/authorization: unauthenticated, expired, disabled account, **cross-`<isolation-id>` access must be rejected**;
  - rate limiting and concurrency conflicts (duplicate submission, replay, race safety);
  - downstream failure behavior (what the user sees when a dependency times out or returns 5xx — never a misleading success).

### Step 1 — RED

- Write the tests **before** the implementation files are created or modified.
- Run them and confirm they fail *because the feature is missing* — and keep the failing output as evidence. A test that passes at this point, or cannot fail, is invalid.

### Step 2 — GREEN

- Write only the minimal code that turns the red tests green.
- No opportunistic extras: no unverified branches, no speculative fields, no drive-by refactors.

### Step 3 — REFACTOR & GATE

- With all tests green, clean up duplication, comments, and error messages; re-check the logging/redaction rules.
- Run the one-command gate (`<make pr-check>`, which includes the TDD compliance check of §4). 100% pass before opening a PR.

## 3. Per-area rules

- **Backend**: table-driven tests preferred; test names state the business semantics ("duplicate signup within 60s returns 429"). Integration tests run against a real test database (name suffixed `_test`) with per-test isolation — do not mock away the data layer's behavior. Failure cases assert both the status code and the error envelope (`code` + non-empty human-readable `message`).
- **Clients/Web**: contract-schema tests come first (required fields, enum bounds — prove bad payloads are rejected locally). State/network tests cover success, auth-expiry eviction, business-error surfacing, and offline/5xx degradation that does **not** log the user out spuriously.
- **Scripts/tooling**: every gate or utility script ships with its own tests, including invalid-input and failure-exit cases.

## 4. The compliance gate (machine check)

A zero-dependency script analyzes the branch diff (`git diff --name-only <base>...HEAD` plus uncommitted changes) and enforces:

| Rule | Trigger | Requirement | Exemptions |
|---|---|---|---|
| R1 Pairing (backend) | production source changed under `<server-source-glob>` | the same change includes a test file change | generated code (list the generated paths) |
| R2 Pairing (client) | business source changed under `<client-source-glob>` | the same change includes a test file change | type declarations, entry files, pure styles/assets |
| R3 Negative assertions | any test file changed | the new/changed test content contains negative/boundary assertions (keyword set per stack: status codes `400/401/403/404/409/429`, `Error`, `invalid`, `reject`, `toThrow`, …) | utility-script tests with explicit error assertions |

Zero-impact guarantees: documentation-only or config-only branches pass automatically; the gate never retroactively judges code that predates it.

## 5. PR evidence card

Feature/fix PRs include this record in the body:

```markdown
### TDD record
- **Step 1 (RED)**: added `<test file>:<test name>` — verified failing before implementation
- **Step 2 (GREEN)**: implemented `<source file>` — positive and negative tests all green
- **Step 3 (GATE)**: `<make tdd-check>` passed (pairing 100%, negative assertions present)
```
