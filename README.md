# agent-workflow-kit

> A spec-first, test-first development workflow for solo builders and small teams who ship software with multiple AI coding agents.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Most AI coding workflows fail in predictable ways: the agent writes tests that mirror its own implementation (so the tests prove nothing), reviewers raise findings with no reproducible evidence (so fixes thrash), and project conventions live in chat logs (so they are forgotten within a week). This kit is a complete, portable workflow distilled from a production project that runs on it daily. It is **stack-agnostic**: the mechanisms work the same for iOS, Android, Web, and servers in Go, Java, Node.js, Python, or anything else — only the tool mapping changes.

## The workflow at a glance

- **Three roles, one merge key.** A human decision-maker approves intent, contracts, and acceptance checklists, and is the only one who merges. A *Writer* agent drafts and implements. A *Reviewer* agent (ideally a different model) writes tests independently and reviews with evidence.
- **An eight-step pipeline per feature.** Intent & contract → behavior checklist & plan → approval gate → independent tests, frozen → implementation with self-verification → evidence-based review → adjudicated fix loop → merge & archive.
- **A behavior-level test-case library as the single source of truth.** Test cases are written as platform-neutral business behavior (Given/When/Then, no implementation words), one file per feature, with a coverage matrix across every client platform. New platforms consume the same library in a compressed "Delta mode".
- **Contracts before code.** Server/API contracts are drafted against an eight-part checklist; product decisions are flagged ★ and only the human decides them.
- **Evidence-based review.** Every finding needs a file:line, a reproduction (or a spec reference), expected vs. actual, and a hint for how to refute it. Unverifiable findings don't drive rework.
- **Machines enforce, documents explain.** Anything a machine can check becomes a lint rule or a CI gate. Critical rules are `error`, never `warn` — a warning that keeps CI green is not a rule.
- **Everything is archived.** Hidden acceptance scenarios, review lessons, and coverage status are written back into the library after every merge, so each mistake is paid for exactly once.

Full design document: [docs/blueprint.md](docs/blueprint.md) (Chinese for now; English translation is on the roadmap).

## Repository layout (roadmap)

```text
docs/        Design documents, starting with the workflow blueprint
templates/   Blank templates for the 10 workflow documents (AGENTS.md, REVIEW.md, ...)
scripts/     Stack-agnostic gate scripts (e.g. the TDD compliance checker)
examples/    A tiny feature walked through all eight steps, end to end
```

Items land step by step; this README only lists what exists or is explicitly planned.

## Getting started

1. Read the [blueprint](docs/blueprint.md) — it defines the 12 core mechanisms, the five adoption phases, and the per-stack adaptation tables.
2. Copy the templates (when they land) into your repository and fill in the eight project "slots" (data-isolation dimension, project invariants, failure definitions, high-risk paths, ★ decisions, mandatory failure branches, design source, risk grading).
3. Wire the gates into CI, then run one small real feature through the full pipeline before scaling up.

## Status

v0.1 under construction. Current step: repository foundation + blueprint. Templates and gate scripts follow the roadmap in the blueprint (§2, five phases).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The project follows its own workflow for non-trivial changes: open an issue describing intent and non-goals first.

## License

MIT © 2026 Shinji
