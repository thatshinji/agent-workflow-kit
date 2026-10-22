English | [简体中文](AGENTS.zh-CN.md)

<!--
  TEMPLATE: AGENTS.md — copy to your repository root and fill in every <slot>.
  This file is the constitution of the workflow: every AI agent reads it before
  starting work. Keep it short, imperative, and verifiable. Anything that cannot
  be checked does not belong here — it belongs in a design doc.
  Universal rules are pre-filled; project-specific rules go in the marked slots.
-->

# AGENTS.md — <Project Name> Agent Working Rules

> All AI coding agents working in this repository must read this file and `docs/project-management/README.md` before starting.
> Established: <YYYY-MM-DD>. Changes to this file require the decision-maker's approval.

## Project overview

- **<Project Name>**: <one sentence — what it is, and its core loop or value proposition>.
- **Architecture**: <e.g. monorepo: `apps/` clients + `server/` backend / or your layout>.
- **Stack**: <languages, frameworks, database, deployment shape>.
- **Authoritative specs**: `<docs/specs/>` — frozen contracts and baselines. Read-only; changes go through the versioned-proposal process (new `-v2` file + a dated decision record).

## Hard rules (violating any of these means rework)

1. **No direct pushes to the main branch.** Everything lands via PR; only the decision-maker merges.
2. **One issue, one branch.** Branch name: `<agent>/<issue-number>-<short-description>`.
3. **Never modify frozen specs in place.** Evolve them by versioned proposal instead.
4. **Never touch secrets.** Do not read or write `.env`, keys, tokens, or passwords. If a task needs a credential, ask the decision-maker.
5. **No destructive operations.** No deleting migration history, no force pushes, no modifying other agents' branches.
6. **No unapproved dependencies or heavy architecture.** New dependencies must be justified in the issue and approved first. <Project slot: name the heavy components banned here, e.g. heavy ORMs, message queues, premature microservices.>
7. **No code before the approval gate.** Intent, contract, and behavior checklist must be approved (step 3 of the pipeline) before implementation starts. No PR without tests; every new test suite must include negative/boundary cases (see the TDD spec).
8. **Review findings require adjudication.** A finding enters the fix queue only after independent adjudication marks it `TRUE` (with reproducible evidence). Unverifiable opinions (`UNKNOWN`) never block a merge. Reviewers must read `REVIEW.md` first; review runs at most 3 rounds.
9. <Project slot: your data-isolation rule — e.g. "Every query/write on tenant data must carry `<tenant_id>`, taken from the authenticated session, never from client input.">
10. <Project slot: 0–3 more project invariants, e.g. money is integer cents; statistics are computed deterministically, never by an LLM.>

## Directory ownership

No agent modifies directories outside its assignment.

| Directory | Owner agent(s) | Scope |
|---|---|---|
| `<server/>` | <agent> | <backend, API, migrations, workers> |
| `<apps/<client-a>>` | <agent> | <client A> |
| `<apps/<client-b>>` | <agent> | <client B> |
| `<packages/>`, `<docs/>` | shared — announce in the issue first | contracts, shared code, documents |

## The eight-step pipeline (per feature / issue)

No step starts until the previous one passes.

1. **Intent & contract.** The decision-maker supplies the design/requirement. The writer drafts the *intent section* (who it serves, what it solves) plus proposed **non-goals** and **unchanged behaviors** for the decision-maker to approve — work does not start without the approved pair. For backend work, the writer also drafts the contract by walking the contract checklist item by item, marking each `decided` / `follows standard <ref>` / `open question`. Items flagged ★ are product decisions: the writer never decides them, they go to the decision-maker. Major contracts are frozen via the spec-proposal process; small ones take effect on approval inside the issue. The writer never invents requirements — anything not derivable becomes an open question.
2. **Behavior checklist & plan outline.** (a) Checklist: search `docs/test-cases/` first — extend the existing file or create one from the template. Cases are written at the **behavior layer** (platform-neutral Given/When/Then → business outcome; no implementation words — see the test-cases template). Platform-specific interactions go in the *platform differences* section. Every case cites its source (design screen / contract clause / hard rule). Stub-dependent behavior is split into two groups: *stub behavior* (accepted this round) and *real behavior* (activates on integration; not frozen as contract). (b) Plan outline: files to change, PR split, **data-model check** (every field in the design verified against the current schema; missing columns go through spec proposal first), list of existing tests affected.
3. **Approval gate.** Checklist + outline must be approved by the decision-maker before any code is written. The decision-maker verifies behavior facts and differences only, not test code. High-risk work (auth, sessions, migrations, payments, data deletion) is reviewed line by line; low-risk may be spot-checked.
4. **Independent tests, frozen.** Test code is written by the reviewer from the approved checklist (or adversarially audited if the writer wrote it) — the reviewer works from the design and checklist, never from the writer's implementation ideas. Tests are committed **red first, with the failing output kept as evidence** (a test that cannot fail is invalid), then **frozen**: the writer may not modify them during implementation; changing a test goes back to step 3. The reviewer/decision-maker keeps 2–3 **hidden scenarios** undisclosed until the final review round. After the freeze, the checklist is also posted to the issue in plain language, and the decision-maker confirms it before step 5 begins.
5. **Implementation & self-verification.** The writer implements via the TDD loop (see the TDD spec). A PR requires: all approved tests green, the one-command gate (`<make pr-check>`) passing, and — for UI work — a side-by-side screenshot against the design source.
6. **Review.** The reviewer works per `REVIEW.md`. Scope is three things only: checklist coverage, regression suite green, hard-rule compliance. Severity, evidence, and round rules live in `REVIEW.md` and the review protocol — they are not repeated here.
7. **Fix loop & reconciliation.** Per the adjudication protocol. Disputes beyond the approved checklist go straight to the decision-maker, not back and forth between agents. When fixes are done, a full **reconciliation statement** is posted to the issue: every finding with its round, severity, location, plain-language description, verdict, fixing commit, and verification evidence — plus one copy-paste verification command the decision-maker can run to check the claims in seconds.
8. **Merge & archive.** The decision-maker merges (for high-risk paths, after reading the key diffs personally). After merging, four archive actions are mandatory: ① hidden scenarios are unsealed from the reviewer's behavior-level draft and written into `docs/test-cases/` verbatim; ② this PR's behavior-case changes land in the feature file's current version; ③ review lessons are distilled (one line each: pitfall + remedy) into the feature file's *review lessons* section; ④ the coverage matrix in `docs/test-cases/INDEX.md` is updated. **When the same class of finding appears a second time, it must become a machine check (CI/lint/gate-script rule) or a regression test, tracked by an issue — never a third round of human reminders.**

**Additional platforms (Delta mode).** When a second (or later) platform implements a feature whose behavior cases are already archived, the pipeline compresses: the intent states only the platform differences relative to the archived cases; the approval gate verifies only the delta; tests are implemented 1:1 against the archived case IDs; after merge, the new platform's column in the coverage matrix is updated. See the platform playbook template.

PR size budget: a few hundred lines. Larger work is split into stacked PRs per the plan outline.

## Definition of Done

1. **Claim**: comment on the issue + self-assign; move the board card to In Progress. WIP limit: <1 while the workflow is new, at most 2 once it runs smoothly>.
2. **Read first**: `docs/project-management/README.md`, the TDD spec, and the relevant contracts. Cross-platform work follows the API contract.
3. **Plan**: features follow the eight-step pipeline. Complex non-feature work presents a plan for approval first.
4. **Gates** (all must pass before opening a PR):
   - TDD compliance: production changes ship with paired tests in the same domain; new tests include negative/boundary assertions (`<make tdd-check>`).
   - <Backend slot: test database and full-suite command, e.g. `go test -race ./...` 100% green.>
   - <Client slot: design-source compliance check, e.g. pages must match the design export 1:1 and be registered in the manifest (`<make design-check>`).>
   - Database changes ship as paired up/down migrations, verified to roll back cleanly (`<make migrate-verify>`).
   - The one-command gate `<make pr-check>` passes 100% locally.
5. **PR conventions**:
   - Written in <the team's working language>; standard technical terms may stay in English.
   - **Never** use auto-closing keywords (`Fixes #`, `Closes #`). Always `Refs #<issue>`.
   - State what changed, the verification commands, and their output evidence.
   - Include a risk self-assessment (Low / Medium / High) — it decides how closely the decision-maker reads before merging.
   - If the PR fixes review findings, list each finding ID (`R-YYYYMMDD-NNN`) with its verdict (`TRUE`/`FALSE`/`UNKNOWN`) and evidence.
   - Tick off the issue's acceptance checkboxes as they are verified.
   - After merge, the issue moves to Pending Acceptance; the decision-maker verifies and closes it manually.
6. **Archive**: record the agent session link, branch, and PR link on the issue. An AI is never the final acceptor.

## Code conventions (summary — full text in the coding standards)

- Comments explain *why*, in plain language a non-specialist can follow.
- <Slot: layering rule, e.g. "Business code never writes raw SQL; data access lives in the repository layer.">
- <Slot: error rule, e.g. "Upstream errors are translated into plain-language messages; raw stack traces never reach clients.">
- <Slot: logging rule, e.g. "Phone numbers, codes, tokens, and passwords are never logged; phone numbers are masked.">
