# Templates

Blank templates for the agent-workflow-kit documents. Each template contains structure, filling guidance (in HTML comments at the top), and `<slot>` placeholders — never content filled in for a specific project.

## Where each template goes

| Template | Copy to | Notes |
|---|---|---|
| `AGENTS.md` | repository root | The agent constitution: hard rules, directory ownership, the eight-step pipeline, DoD |
| `REVIEW.md` | repository root | Reviewer guide: failure definitions, evidence rules, severity, boundaries |
| `test-cases/TEMPLATE.md` | `docs/test-cases/TEMPLATE.md` | Per-feature behavior case file skeleton |
| `test-cases/INDEX.md` | `docs/test-cases/INDEX.md` | Coverage matrix and registration principles |

## Coming in later steps

Per the blueprint (§3, document set): review protocol, TDD workflow spec, contract checklist, coding standards, project-management README, platform playbook, and the review ledger. They will land in this directory with the same conventions.

## Filling order for a new project

1. Fill the eight project slots first (blueprint §5): data-isolation dimension, project hard rules, failure definitions, high-risk paths, ★ contract decisions, mandatory failure branches, design source, risk grading.
2. Then instantiate `AGENTS.md` and `REVIEW.md` — they reference most other documents.
3. Create `docs/test-cases/` with `TEMPLATE.md` and `INDEX.md` before the first feature starts; the first feature's case file is written during its pipeline step 2.
