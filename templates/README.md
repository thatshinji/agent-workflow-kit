English | [简体中文](README.zh-CN.md)

# Templates

Blank templates for the agent-workflow-kit documents. Each template contains structure, filling guidance (in HTML comments at the top), and `<slot>` placeholders — never content filled in for a specific project.

## Where each template goes

| Template | Copy to | Notes |
|---|---|---|
| `AGENTS.md` | repository root | The agent constitution: hard rules, directory ownership, the eight-step pipeline, DoD |
| `REVIEW.md` | repository root | Reviewer guide: failure definitions, evidence rules, severity, boundaries |
| `test-cases/TEMPLATE.md` | `docs/test-cases/TEMPLATE.md` | Per-feature behavior case file skeleton |
| `test-cases/INDEX.md` | `docs/test-cases/INDEX.md` | Coverage matrix and registration principles |
| `project-management/README.md` | `docs/project-management/README.md` | Task pool, milestones by exit criteria, board discipline, roles, cadence |
| `project-management/review-protocol.md` | `docs/project-management/review-protocol.md` | Finding format, three-state adjudication, rounds, reconciliation |
| `project-management/tdd-workflow-spec.md` | `docs/project-management/tdd-workflow-spec.md` | The four-step TDD loop and the compliance-gate design |
| `project-management/contract-checklist.md` | `docs/project-management/contract-checklist.md` | The eight-part contract drafting checklist with ★ product decisions |
| `project-management/platform-playbook.md` | `docs/project-management/<platform>-playbook.md` | Per-platform Delta-mode playbook; one copy per platform |
| `project-management/reviews-ledger.yaml` | `docs/project-management/reviews/ledger.yaml` | Adjudicated-finding ledger; never re-raise a decided finding |
| `specs/coding-standards.md` | `docs/specs/coding-standards.md` | Living baseline: machine-enforcement matrix + judgment conventions |

## Filling order for a new project

1. Fill the eight project slots first (blueprint §5): data-isolation dimension, project hard rules, failure definitions, high-risk paths, ★ contract decisions, mandatory failure branches, design source, risk grading.
2. Then instantiate `AGENTS.md` and `REVIEW.md` — they reference most other documents.
3. Create `docs/test-cases/` with `TEMPLATE.md` and `INDEX.md` before the first feature starts; the first feature's case file is written during its pipeline step 2.

## Coming next

Step 3 of the roadmap: stack-agnostic gate scripts (the TDD compliance checker and friends) under `scripts/`, followed by a worked example under `examples/`.
