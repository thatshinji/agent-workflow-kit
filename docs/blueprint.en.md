English | [中文](blueprint.md)

# Replicating an AI-Collaboration Development Workflow — Blueprint v0.1

> Distilled from the live workflow of a real project in active development (solo developer + multiple AI agents collaborating, app and server advancing in parallel — below, "the reference project"): AGENTS.md (eight-step pipeline + hard rules + DoD), REVIEW.md v1.4, TDD Collaboration Spec v1.0.0, the backend contract-draft checklist, the behavior-layer test-case archive system (docs/test-cases/), the full-stack coding standards, and the project-management plan (docs/project-management/README.md).
> Purpose: replicate this workflow when building any new app (iOS / Android / Web / mini program / server, any language). This document covers only the portable parts; the original project's business content (tenant fields, design tools, business terminology, etc.) is abstracted into "slots" that each new project fills in itself.

---

## 0. Feasibility Verdict

**Feasible.** This workflow's effectiveness does not come from Go, Swift, or any specific tool. It comes from a set of platform-independent collaboration mechanisms: who decides, who writes, who reviews, what counts as evidence, and where knowledge accumulates. Swap in Java/Node/Kotlin and every mechanism still holds; the only thing to replace is the outermost tool-name mapping (the adaptation tables in §4).

When porting, think in three layers:

| Layer | Contents | How to port |
|---|---|---|
| **Kernel** (§1, 12 mechanisms) | Roles, process, evidence rules, test-case library, gates, accumulation | Copy verbatim — no renaming, no reordering |
| **Adaptation layer** (§4) | Test frameworks, lint, contract formats, migration tools | Look up and substitute per tech stack |
| **Slots** (§5) | The project's hard rules, failure definitions, ★ product decisions, mandatory failure branches | Filled in by each new project at kickoff — filling them wrong is worse than not filling them |

One illusion to dispel up front: this workflow is designed for "one person (or a small team) + multiple AI agents collaborating." A purely human team, or a solo developer writing everything by hand, will find it too heavy. Its payoff points — stopping an agent from back-filling tests to match its own implementation, stopping evidence-free review rework, stopping standards from living only as verbal agreements — are diseases specific to AI collaboration.

---

## 1. The Kernel: 12 Platform-Independent Mechanisms

### 1.1 Three Roles + a Single Merge Key

- **Decision-maker** (human): only answers judgment calls — approves intent, approves product decisions in contracts, approves acceptance checklists, presses merge. Writes no code, fills in no forms.
- **Writer** (AI agent): drafts the intent section, contract drafts, scenario checklists, and the implementation; responsible for listing "questions to confirm" explicitly, and never allowed to invent requirements.
- **Reviewer** (another AI agent, ideally a different model from the Writer's): independently writes tests or adversarial audit tests, reviews under the evidence rules, and drafts adjudications.
- Principle: **decisions are serial, execution is parallel**; the merge key stays in the decision-maker's hands forever, and no agent merges any PR. A coordinator (if any) only splits tasks, fixes interfaces, and runs the process — it does not enter the coding loop.

### 1.2 The Hard-Rules Layer (AGENTS.md at repo root)

Every repository has one file every agent must read before starting work, containing: a project overview, **hard rules (violating one means rework)**, directory/domain boundaries (which agent may touch which directories), the main process, the DoD, and PR conventions. Hard rules come in two kinds:

- **Universal hard rules** (copy directly): never push straight to the main branch; one issue per branch; never touch secrets; no destructive operations; no adding dependencies on your own; no starting work without approval; no PR without tests; review conclusions must pass independent adjudication.
- **Project hard rules** (slots, §5): this project's non-negotiables (e.g., the data-isolation dimension, money conventions, heavyweight components that must not be introduced).

### 1.3 The Eight-Step Pipeline

Every feature (one issue) follows the steps strictly in order; a step that hasn't passed blocks the next:

1. **Intent & contract**: the Writer drafts the intent section (who it's for, what it solves) plus drafts of the **Non-goals** and **Unchanged behavior** columns; the decision-maker signs off. Anything touching the server goes through the contract-draft flow (§1.5).
2. **Scenario checklist & plan outline**: for the scenario checklist, consult the test-case library first (extend, revise, or create new; behavior-layer wording per §1.4). The plan outline covers change scope, PR splitting, a **data-model check** (every field appearing in the design/requirements is checked item by item against the current table schema; a missing column goes through a proposal first), and existing tests affected.
3. **Approval gate**: no code until the checklist + outline are approved by the decision-maker. The decision-maker verifies only behavior-layer facts and the points of difference, never test code; high-risk items are walked through one by one, low-risk ones spot-checked.
4. **Independent tests & freeze**: the Reviewer independently writes tests (or adversarial audits) from the approved checklist, **runs them red first and keeps the evidence** (a test that doesn't go red is invalid), then freezes them — the Writer may not change tests during development; changing a test goes back to step 3. The case checklist is also published to the issue in plain language, and work starts only after the decision-maker confirms it.
5. **Development & self-proof**: the Writer implements via the TDD inner loop (§1.6). A PR may be opened only when the self-proof materials are complete (all tests green, one-command gate passing, before/after comparison images for visual work).
6. **Review**: the Reviewer executes per REVIEW.md (§1.8); scope is three things: scenario coverage, full regression green, hard-rule compliance.
7. **Fix loop & adjudication**: findings go through three-state adjudication (§1.9); the loop is capped at 3 rounds, beyond which the work returns to the plan layer. The loop closes with a full reconciliation statement (every finding's adjudication and fix evidence) plus one verification command the decision-maker can run in a single shot.
8. **Merge & accumulation**: the decision-maker merges; after merging, the four archive items (§1.11) are mandatory.

Supporting constraints: WIP limits (1 during the trial period, at most 2 once things run smoothly); a single PR stays within a few hundred lines — beyond that, split it into stacked PRs per the outline.

### 1.4 The Behavior-Layer Test-Case Library (single source of truth across platforms)

- What gets archived is **a feature's behavior cases**, not one PR's test records: `docs/test-cases/` holds one file per feature (subdirectories by business domain), with four fixed sections — Intent (intent / unchanged behavior / non-goals / change history), Behavior Cases (with stable IDs, e.g. `AUTH-003`), Platform Differences, and Review Lessons.
- **Behavior-layer wording rules**: Given/When/Then state business facts, and expectations are business outcomes; implementation words are banned (click / swipe / Toast / modal / component names / routes / API paths / UI pixels). The criterion is **mappability**: a test engineer on any platform can write that platform's tests from the case alone, without guessing.
- Three exception classes: pure display expectations (one business expectation + "per the design source"), unobservable internal behavior (not written), and genuinely single-platform behavior (demoted into Platform Differences).
- **INDEX coverage matrix**: rows = features, columns = the platforms the project actually has (Web / iOS / Android / mini program / server), cells = coverage status (✅ implemented / ⚠️ partial / ❌ not implemented / — not applicable). Only archived features are registered; the matrix grows row by row naturally, with no pre-filled future universe — the INDEX is a factual ledger, not a planning chart.
- **Living documents**: cases evolve with the feature and are updated to the current version inside the same PR; no historical versions are kept. Behavior changed but the document didn't = an Important in review.
- **New platforms use Delta mode**: when a second or later platform consumes the same library, the process compresses — intent covers only the platform differences relative to the archived cases, the approval gate checks only the delta, tests are implemented keyed 1:1 to case IDs, and after merging, the corresponding INDEX column lights up.

### 1.5 Contracts First (server / cross-platform interfaces)

- When drafting a contract, the Writer walks the *Contract Draft Checklist* item by item, marking each one of three ways: `Decided` / `Existing standard` (cite the source) / `Open question`. The Reviewer first checks for gaps and inconsistencies; anything left unexplained is sent straight back. The decision-maker approves only the ★-marked product-decision items.
- The checklist's eight groups (content is universal; ★ items are tuned per project): ① Interfaces (endpoints, validation, error codes, pagination; ★ idempotency) ② Data model (constraints, indexes, paired migrations, soft delete, audit fields, data volume & archival) ③ Business rules (state machines, invariants, ★ calculation conventions, concurrency conflicts, transaction boundaries) ④ Permissions & security (★ authorization matrix, isolation dimension taken only from the login session, an enumerated list of privilege-escalation points, sensitive data stored as hashes only, anti-abuse rate limiting, ★ data retention & true deletion) ⑤ External dependencies & async (for each third party: really integrated this round or stubbed, ★ stub scope, failure strategy, async jobs & compensation) ⑥ Time & boundaries (timezone conventions, boundary values, ★ the relational semantics of deletion) ⑦ Client coordination (nullability, error-code-to-user-message mapping, change blast radius) ⑧ Acceptance handoff (every contract behavior written as a testable assertion feeding the scenario checklist; every stub behavior's return values spelled out item by item).
- Once an important contract is approved it enters the frozen zone (version-proposal system: changing a contract means issuing a new-version file + an adjudication record, never editing the frozen version directly); a small contract takes effect on approval inside its issue.
- The contract's machine form: pick one of OpenAPI / Protobuf / JSON Schema as the project's single source of truth; client DTOs align to it, and drift counts as a failure.


### 1.6 The TDD Inner Loop (the execution method inside step 5)

Four steps: **Step 0 Spec mapping → Step 1 Red → Step 2 Green → Step 3 Refactor & Gate**, plus the Reviewer's independent re-check at Step 4.

- Step 0: map the issue's acceptance conditions one by one into a test matrix. Every feature point must include both positive cases and **mandatory failure branches** (tuned per project domain; the universal skeleton: parameter-validation failure, unauthenticated / expired authentication, accessing another user's data, rate limiting & concurrency conflicts, degraded behavior when an external dependency fails).
- Step 1: write the tests first and run them to confirm red — a test that doesn't fail while the feature is unimplemented is an invalid test.
- Step 2: write only the minimal implementation that turns red to green; no opportunistic extra fields, no unverified branches.
- Step 3: refactor under full-green protection, pass the one-command gate, then open the PR; the PR body carries a TDD evidence card (red test names → implementation files → gate results).

One hard rule guards against "tests back-filled to fit the implementation": **acceptance conditions must map one-to-one to test functions** (test names or comments carry the case ID); any mismatch is non-compliant.

### 1.7 Hidden Scenarios

- For each feature, the Reviewer or the decision-maker keeps 2–3 hidden scenarios, never shared with the Writer, run only in the final review round; a failure is handled at the highest severity.
- After merging, the Reviewer produces a behavior-layer draft and the Writer files it into the test-case library as-is (formatting only, no semantic changes) — hiddenness exists only during development; in the end all knowledge is archived in full and no information asymmetry accumulates.

### 1.8 Review Under Evidence Rules (REVIEW.md at repo root)

- **Criterion precedence chain** (fixed in writing): AGENTS.md hard rules > frozen contracts & coding standards > the decision-maker-approved scenario checklist > the TDD spec > REVIEW.md > general engineering common sense. Conflicts are adjudicated by this chain, not argued.
- **Failure defined per directory**: REVIEW.md contains a table spelling out, for each directory, "what failure looks like" (build/test failure, privilege escalation, non-rollbackable migration, sensitive information leaking into logs, drift from the contract, a document writing a plan as if implemented…). The Reviewer matches findings against the table instead of improvising. The table's content is a slot; its structure is copied as-is.
- **Three severity levels**: Important (wrong behavior / security / data risk — must fix), Nit (no behavior change; ≤3 per PR, never blocking), Pre-existing (flagged and moved to a separate issue; not charged to the author).
- **The evidence four-pack**: every finding must provide `file:line` + a runnable repro (or a citable spec clause) + `expected/actual` + a `refute_hint` (what result would prove me wrong). If no repro can be produced, mark it `UNKNOWN` — never write it up as a bug. Evidence-free phrasing like "might / maybe / best practice" is not accepted.
- **Review scope discipline**: review only the diff of the named commit; from round 2 on, look only at the new diff; a skip list applies (generated artifacts, lockfiles, already-adjudicated findings, pure formatting issues); high-risk paths (auth, sessions, migrations, CI, secrets, frozen contracts, destructive scripts) get a separate security review + decision-maker confirmation.

### 1.9 The Adjudication Mechanism

- Every finding is adjudicated independently into three states: `TRUE` (enters the fix queue), `FALSE` (closed with counter-evidence attached), `UNKNOWN` (must not drive rework and must not block a merge; security/compliance items are handled strictly under an exception clause).
- The fix loop closes by publishing a *Full Finding Adjudication & Fix Reconciliation Statement*: round, ID, severity, location, plain-language description, adjudication verdict, fix commit, and verification evidence — plus a one-shot verification command for the decision-maker.
- Disputes beyond the scope of the approved checklist are not bounced back and forth between agents; they escalate directly to the decision-maker.

### 1.10 Machine Checks First

- Any convention a machine can judge must become a machine check (a lint rule / gate script / CI step); verbal agreements in documents are only a transition.
- **Rule level is binding force**: key rules must be error-level — a warning's exit code is 0, CI stays green, and an agent weighing trade-offs will keep the warning, which equals having no rule. Warnings are allowed only for purely informational hints.
- **Incremental blocking, legacy exemption**: a brand-new project may block everything from day one; when introducing this into an existing codebase, block only new and changed lines and let the legacy be paid down as it is touched — otherwise the whole repo goes red on adoption day and forces fake fixes.
- **One-command gate**: the repository provides a single entry point (e.g. `make pr-check` or an equivalent script) chaining formatting, lint, the TDD compliance check (production code paired with tests, presence of negative assertions), the full test suite, two-way migration verification, and the build; a PR may be opened only at 100% local pass, and CI re-runs the same standard.
- Tool versions must be pinned; floating dependencies like `@latest` are banned — CI results should depend only on the repository's contents.

### 1.11 The Accumulation Loop (four archive items after merge)

Mandatory after every feature PR merges: ① hidden scenarios unsealed and filed; ② this PR's behavior-case additions and changes land in the feature file's current version; ③ review lessons distilled (one line each: the pitfall + the handling) into that feature file's "Review Lessons" section (no central lessons file — lessons travel with the feature); ④ the INDEX coverage matrix is updated.

**Anti-rot rule**: when the same class of finding appears a second time, it must become a machine check or a regression test, tracked by an issue — review may not repeat it verbally a third time. This is the fundamental reason the workflow gets lighter the longer it runs: every pitfall is handled by hand exactly once.

### 1.12 The Project-Management Skeleton

- **A single task pool**: use the code host's Issues + board (e.g. GitHub Issues + Projects); never run a second task system in parallel. Five states: backlog → to-do → in progress → awaiting acceptance → done (+ cancelled); blockers are labeled with the reason and the unblocking condition.
- **Milestones defined by exit conditions** ("the first-release scope passes item by item"), not by piling up task counts against dates. Every task must state: outcome, acceptance conditions, origin, dependencies, priority, milestone. Task granularity is half a day to two days; anything bigger gets split.
- **Claim system**: one issue is given to one agent at a time; claim it and leave a comment before starting. PRs link with `Refs #n`; **Fixes/Closes auto-closing is banned** — after merging, the issue moves to awaiting acceptance, and the decision-maker closes it manually after personal verification.
- **PR conventions**: title and body in the team's working language, stating the change points and verification evidence, with a risk self-assessment (Low/Medium/High — it decides how closely the decision-maker reads before merging); review fixes list the finding IDs and adjudication outcomes.
- **DoD**: merged ≠ done; a task is done only when the acceptance conditions are met + the evidence is complete + the decision-maker has confirmed the user-visible result.

---

## 2. The Universal Rollout Blueprint: A New Project from 0 to 1 in Five Phases

### Phase A: Repository Skeleton (Day 1)

- Create the repo + directory structure (a monorepo with multiple platforms, or one repo per platform — both work; with split repos, each keeps its own AGENTS.md, and contracts and the test-case library live in a shared repo).
- Settle: the task pool and board, branch naming `<agent>/<issue-no>-short-description`, the PR template (with risk self-assessment and evidence fields), and the milestone skeleton (by exit conditions).
- Fill in the first version of the slots (§5): project hard rules, directory boundaries, the high-risk path list.

### Phase B: The Document Set Lands (Days 1–2)

Build the "structure" of the 10 documents per the §3 checklist, with minimal content at first (enough to run the first feature through); don't try to write them fully in one pass — the document set itself is living documentation, iterated by lessons from every later PR.

### Phase C: Wiring Up the Gates (Days 2–3)

- Pick the toolchain per the §4 adaptation tables; commit each platform's lint/format config and CI; get the unified one-command gate entry running (it must be green even on an empty repo).
- Implement the TDD compliance check script (diff analysis: production changes must be paired with test changes, and tests must contain negative-assertion keywords) — the logic is language-independent; the reference implementation is zero-dependency Python, and its path rules can be reused directly.

### Phase D: First Feature, Full Trial Run (Week 1)

Pick the smallest yet complete real closed-loop feature and run it strictly through all eight steps (including hidden scenarios and the four archive items). The goal is not shipping the feature — it is exposing every point of friction in the process: checklist granularity, gate runtime, review round-trips. Fix every awkwardness found during the trial run in the documents on the spot; don't stockpile it.

### Phase E: Solidify & Trim (After the Trial Run)

- The decision-maker reviews: which gates actually caught real problems (keep), which are pure ceremony (remove or downgrade); write the trial-run lessons into each document's change log.
- When team size or platform count changes, return to §6 and adjust the tier.

---

## 3. The Document Set Checklist (the 10 documents a new project creates)

| # | Document | Universal skeleton (copy as-is) | Project-filled (slots) |
|---|---|---|---|
| 1 | `AGENTS.md` (repo root) | Six-section structure: overview / hard rules / directory boundaries / eight steps / DoD / PR conventions | Hard-rule content, directories and their owning agents, high-risk list |
| 2 | `REVIEW.md` (repo root) | Criterion chain / failure table / three severity levels / evidence four-pack / skip paths / output format / review boundaries | The failure table, row by row |
| 3 | `docs/project-management/review-protocol.md` | Three-state adjudication, reconciliation-statement format, round cap, dispute escalation | — (copy essentially as-is) |
| 4 | `docs/project-management/tdd-workflow-spec.md` | Four-step loop, test matrix, positive/negative branch requirements, evidence card | Mandatory failure branches tuned per domain |
| 5 | `docs/project-management/contract-checklist.md` | Eight-group checklist + ★ marking + three-way marking | ★ items and the isolation dimension |
| 6 | `docs/specs/coding-standards.md` (living baseline; the file header declares the freeze rules don't apply) | Two-layer structure: a machine-check layer (tools + config + CI ownership table) + a judgment-conventions layer (four universal rules + 5–8 per language) | Language rules, tool versions |
| 7 | `docs/test-cases/TEMPLATE.md` + feature files + `INDEX.md` | Four-section structure, behavior-layer wording rules, banned-word list, mappability criterion, coverage-matrix format | The set of platform columns |
| 8 | `docs/project-management/README.md` | Tool-choice rationale, milestone exit-condition table, board rules, role division, task template, daily rhythm | Milestone content, rhythm timing |
| 9 | `docs/project-management/<platform>-playbook.md` (one per added platform) | Startup gates, infra-baseline rules, Delta SOP, platform-specific hard rules | The platform's technical details |
| 10 | `docs/project-management/reviews/ledger.yaml` | Finding IDs (`R-YYYYMMDD-NNN`), adjudication-status ledger | — (copy as-is) |

Two more document kinds as needed: the frozen-contract zone (contracts and adjudication records under `docs/specs/`, under the version-proposal system), and the environment & external-dependency register (accounts, vendors, signing certificates, and other kickoff dependencies).

---

## 4. Adaptation Tables by Platform and Language (the adaptation layer)

The kernel mechanisms don't change; only the tool counterparts in the tables below are swapped. Principle: for each language pick **that ecosystem's mainstream default** — no exotic choices; pin versions; commit the configs to the repo.

### 4.1 Clients

| Dimension | iOS (Swift) | Android (Kotlin) | Web (TS/React etc.) | Cross-platform (Flutter/RN etc.) |
|---|---|---|---|---|
| Test framework (keyed to case IDs) | XCTest / swift-testing | JUnit 5 + Espresso (UI) | Vitest / Jest + Testing Library | flutter_test / Jest |
| Contract consumption | OpenAPI-generated Codable models | OpenAPI-generated data classes | OpenAPI-generated TS types | Same as left, generated into a shared package |
| Lint / format | SwiftLint + SwiftFormat | detekt + ktlint | ESLint (key rules at error) + Prettier | dart analyze / ESLint |
| Design-source constraints | Design-tool export + design-token files | Same as left | Same as left; machine-generated directories are read-only, never hand-edited | Same as left |
| Delta consumption notes | Permission / system-component differences go in Platform Differences | Permission / background-limit differences likewise | Browser / SEO differences likewise | Differences for the two platforms get separate columns |

### 4.2 Servers

| Dimension | Go | Java | Node.js (TS) | Python |
|---|---|---|---|---|
| Test framework | go test (table-driven) | JUnit 5 + Testcontainers | Vitest / Jest + supertest | pytest |
| Integration test store | Separate `_test` store + transaction isolation | Testcontainers spin up a real DB | Test store/container; never fully mock DB behavior | pytest + real-DB fixtures |
| Lint / format | gofmt + go vet + golangci-lint (start with the base set) | Spotless + Checkstyle/PMD; ArchUnit guards layering | ESLint + Prettier + tsc strict | ruff + mypy |
| Contract source of truth | OpenAPI + code validation | springdoc/OpenAPI or contract tests (Pact) | OpenAPI (aligned via zod / type generation) | OpenAPI (FastAPI auto-generation must be diffed against the frozen version) |
| Paired migrations | up/down SQL (goose etc.) | Flyway/Liquibase (versioned, history never edited) | Prisma Migrate / knex (keep rollback scripts) | Alembic (downgrade mandatory) |
| Layering guard | Repository-layer isolation + static checks | ArchUnit rules inside tests | Dependency-direction lint rules | import-linter |
| One-command gate | Makefile | Maven/Gradle wrapper tasks, or a Makefile wrapper | npm scripts + root Makefile/Taskfile | Makefile + optional pre-commit |

### 4.3 Cross-Stack Counterparts

- **Gate scripts**: writable in any language; the reference implementation uses zero-dependency Python + `git diff` analysis — the two rules "production change ↔ test pairing" and "negative-assertion keywords" are language-independent; only file suffixes and directory patterns change per stack.
- **Coverage-matrix columns** = the project's platform set; adding or removing a platform changes only the INDEX header and a playbook, never the mechanisms.
- **Error envelope**: one unified error structure project-wide (code + human-language message); the error-code-to-user-message mapping belongs to the client and is part of the contract.

---

## 5. Slots Every Project Must Fill Itself (kickoff checklist)

If the slots below are filled wrong or left empty, the workflow spins uselessly or misfires; the decision-maker must complete them before the first feature starts:

1. **Data-isolation dimension**: multi-tenant / multi-organization / single-user? What is the isolation field, where is it taken from (the login session only), and how are privilege-escalation points enumerated? (E.g., tenant_id for SaaS, workspace_id for collaboration products; a standalone tool may have none — if none, replace the privilege-escalation item in "mandatory failure branches" with this project's high-risk item, such as local-data corruption recovery.)
2. **3–6 project hard rules**: the business/technical invariants this project must never violate (e.g., money in integer cents, statistics computed deterministically and never via a model, banned architectural components).
3. **Failure definition table**: row by row per directory, "what failure looks like"; must include the four universal items — contract drift, sensitive information landing in logs, non-rollbackable migration, documentation distortion — plus this project's own items.
4. **High-risk path list**: which paths get item-by-item acceptance + a separate security review (universal starting point: auth, sessions, payments, data migration, data deletion, CI & secrets).
5. **The contract checklist's ★ items**: idempotency, authorization matrix, calculation conventions, data retention & true deletion, deletion's relational semantics, stub scope — give this project's default answer for each, or leave them to be decided per feature.
6. **Mandatory failure branch table**: adjusted per this project's domain (e.g., IoT adds disconnect/reconnect, content products add moderation failure, e-commerce adds insufficient stock and duplicate orders).
7. **Design source**: where designs come from and how they are reconciled 1:1 with code (with a design tool: export packages + a manifest; without one: the lightweight form of "prototype images/screenshots + a page list" — but "one single design source, never invent pages" may not be dropped).
8. **Risk-grading conventions**: the criteria dividing Low/Medium/High (they decide how closely acceptance and merges are read).

---

## 6. Trimming Tiers (choose by project scale)

| Tier | Fits | Mechanisms enabled |
|---|---|---|
| **Minimal** | Prototype-validation stage, single platform, 1 person + 1 agent | §1.1 roles (Writer/Reviewer may be the same agent in different sessions, but the merge key stays with the human), §1.2 hard rules, the eight steps simplified to "intent → checklist → approval → implementation → review → accumulation", §1.4 test-case library, §1.8 evidence rules, §1.10 machine gates, §1.11 accumulation. Deferred: hidden scenarios, Delta, the reconciliation statement (replaced by a one-line adjudication record) |
| **Standard** (the reference project's current tier) | A real product, multiple platforms or planning for them, with a server | All 12 mechanisms in full |
| **Enhanced** | Payments / medical / strong compliance involved, multi-person collaboration | Standard + two Reviewers in parallel with cross-arbitration, two-person confirmation on high-risk paths, ledger auditing, release gates and rollback drills |

Trimming principle: a mechanism may be deferred, but the standards inside an adopted mechanism may not be downgraded (if you adopt the evidence rules, evidence-free findings are not allowed; if you adopt the test-case library, implementation words are not allowed).

---

## 7. Anti-Patterns (field lessons — write them straight into the new project's AGENTS.md notes when porting)

1. **Trusting the executor's "verified" without checking yourself**: when a report gives conclusions without the original text, key files must be re-read personally — line counts / anchors — before being believed. This lesson was paid for in real money.
2. **Warning-level rules left hanging long-term**: equivalent to no rule, and they pollute logs and mask real warnings. Either error, or delete.
3. **Documentation claims not matching what actually landed**: a standard claiming "connected to CI" when it isn't — documentation is a contract, and claims must be verifiable; when unsure, honestly write "not yet connected".
4. **Standards written as documents but never wired up**: a standard with no lint config and no CI step is inevitably forgotten within three months.
5. **Back-filled test bias**: tests written to fit the implementation inevitably miss contract boundaries and failure branches — tests first + an independent author + a red run with evidence kept: all three are indispensable.
6. **Unbounded review rounds**: a 3-round cap; beyond it, return to the plan layer. State a whole class of recurring problems at once, by class.
7. **The decision-maker dragged into filling forms**: intent, drafts, and checklists are all drafted by the Writer; the decision-maker only answers judgment calls. A process that makes the decision-maker fill in blanks won't survive two weeks.
8. **One-shot big-bang instructions**: give an agent one thing at a time, with boundaries nailed down; big all-encompassing instructions are inevitably misunderstood (design and coding alike).
9. **Writing plans as if already implemented**: the most common distortion in documents and reconciliation statements; in review it is handled as a failure.

---

## 8. New-Project Kickoff Checklist (tick item by item)

- [ ] Repository and task pool ready; milestones defined by exit conditions
- [ ] All 8 slots in §5 filled and written into AGENTS.md / REVIEW.md
- [ ] The 10-document structure built (§3), contents at minimal version
- [ ] One-command gate runs green on the empty repo; key lint rules at error level; tool versions pinned
- [ ] TDD compliance check script adapted to this stack's path rules
- [ ] First feature chosen (smallest real closed loop), ready for a full trial run with friction recorded
- [ ] Trial-run retrospective scheduled; its conclusions written back into each document's change log

---

_Version: v0.1, 2026-10-21._
