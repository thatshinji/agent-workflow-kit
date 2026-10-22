<!--
  TEMPLATE: docs/project-management/README.md
  The project-management scheme: one task pool, milestones by exit criteria,
  board discipline, roles, cadence. Adapt the milestone rows and views.
-->

# <Project Name> — Project Management

Established: <YYYY-MM-DD>. Scope: <who runs this project, e.g. one decision-maker + AI agents>. This document defines management only; it does not decide product scope and does not claim anything is implemented or accepted.

## Tooling

Use the code host's own Issues + Milestones + Projects as the single task pool. Do not run a second task system in parallel. <Adjust if your host differs — the rule is "exactly one pool", not the brand.>

## Milestones (defined by exit criteria, not dates)

| Milestone | Exit criteria |
|---|---|
| M0 · Baseline | Scope sources frozen, available hours known, existing assets inventoried, first acceptance flow written |
| M1 · First real loop | The chosen end-to-end flow works on real devices/services, with acceptance evidence |
| M2 · v1 scope complete | Every item on the M0-confirmed v1 list passes; deferred items have explicit change records |
| M3 · Closed beta | Security, privacy, recovery, and distribution conditions met; beta feedback loop closed |
| M4 · First public release | Release checklist passed; monitoring and incident ownership explicit |

Estimate dates only after M0; record actual effort for the first rounds and correct the plan from evidence.

## Board & task discipline

- States: Backlog pool → To Do → In Progress → Pending Acceptance → Done (plus Cancelled). Blockers are labels with a written reason and an unblock condition.
- WIP: at most **1** task In Progress while the workflow is new; at most **2** once it runs smoothly. Pending Acceptance also capped (≤2) — clear acceptance debt first.
- Every task states: intended result, acceptance criteria, source documents, dependencies, priority, milestone. The decision-maker is the owner; AI sessions and code links are recorded on the task — an AI is never the acceptor.
- Priorities: P0 blocks the milestone/release path; P1 is required by the current milestone; P2 can wait. Bug severity is recorded separately from priority.
- Task size: half a day to two days. Larger work is split into demonstrable results. Research tasks are time-boxed and must end with a conclusion plus a next step.
- Dates are filled only for real external constraints; effort is estimated coarsely (half-day / day / two days).

## Roles

| Role | Who | Owns |
|---|---|---|
| Decision-maker | <human> | Intent, ★ product decisions, acceptance gates, merging, closing issues |
| Writer | <agent(s)> | Drafts (intent, contracts, checklists), implementation, self-verification |
| Reviewer | <agent, different from writer where possible> | Independent tests, evidence-based review, adjudication drafts |

Principle: **decisions are serial, execution is parallel.** Architecture decisions converge on the decision-maker; writers/reviewers execute and never redefine interfaces or architecture unilaterally.

Collaboration rules: one issue is assigned to one agent at a time, claimed before work starts; one issue, one branch; directory ownership per `AGENTS.md`; contracts are fixed before cross-agent work begins; only the decision-maker merges.

## First round of work (baseline round)

1. Freeze the scope sources; resolve conflicts between planning documents; record which document is authoritative.
2. Inventory existing code/assets: reusable / needs verification / rewrite / not implemented — with evidence.
3. Write the first real flow's acceptance script: inputs, actors, outputs, failure branches.
4. Audit external dependencies (accounts, signing, services, vendors); list gaps and their handling order.
5. Split the first flow into half-day to two-day tasks and queue the next round.

## Completion standard

Merged ≠ done. A task is done when its acceptance criteria are met, evidence (build/version, test results, screenshots or decision records) is attached, and the decision-maker has confirmed the user-visible result. Features touching authorization, duplicate submission, offline recovery, notifications, or AI-written data must verify the relevant failure branches. Prototypes, mock data, and historical test runs are not acceptance evidence.

## Cadence

- Daily start (5 min): pick the main result, check dependencies, then start.
- Daily end (5 min): update status, evidence, next step, actual effort.
- Weekly review (20 min): demo finished results, clear blockers, pick next week's tasks, check scope changes.
- New ideas go to the backlog pool; inserting one into the current round requires naming which task it replaces and the impact.

## Task template

```text
Goal: what result does the user/project get when this is done?
Scope: what exactly is delivered?
Acceptance: observable, reproducible pass conditions.
Source: product docs, spec docs, original numbering.
Dependencies: issues or external conditions that must finish first.
Evidence: code changes, build/version, test results, screenshots/recordings, or decision records.
Wrap-up: actual result, unfinished items, follow-up tasks.
```

Bugs additionally state: reproduction steps, expected vs. actual, environment/version, impact scope, fix verification. Decisions additionally state: alternatives, reason for the choice, impact, decision date.
