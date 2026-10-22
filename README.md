English | [简体中文](README.zh-CN.md)

# agent-workflow-kit

> A spec-first, test-first development workflow for solo builders and small teams who ship software with multiple AI coding agents.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![CI](https://github.com/thatshinji/agent-workflow-kit/actions/workflows/ci.yml/badge.svg)

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

## What's in the kit

```text
docs/blueprint.md   The full design: 12 core mechanisms, 5 adoption phases,
                    per-stack adaptation tables, project "slots", anti-patterns
templates/          Blank templates for all 11 workflow documents — AGENTS.md,
                    REVIEW.md, review protocol, TDD spec, contract checklist,
                    coding standards, project-management set, platform playbook,
                    review ledger, and the test-case library (TEMPLATE + INDEX)
scripts/            The TDD compliance gate (zero-dependency Python): production
                    changes must ship with paired tests containing negative
                    assertions. Configurable per stack; ships with its own tests
examples/           A complete worked example: "join by invite code" through all
                    eight steps, with runnable code and real red/green evidence
```

Start with the [worked example](examples/invite-code/) if you want to see the workflow's artifacts before reading the theory.

## Getting started

**Hands-on path**: follow the [Quickstart](docs/quickstart.md) ([简体中文](docs/quickstart.zh-CN.md)) — a 30-minute guided adoption: copy the templates, fill the eight slots, wire the gate, run your first feature. The conceptual path:

1. Read the [blueprint](docs/blueprint.md) — it defines the 12 core mechanisms, the five adoption phases, and the per-stack adaptation tables.
2. Copy the [templates](templates/) into your repository (the templates README maps each file to its destination) and fill in the eight project "slots" (data-isolation dimension, project invariants, failure definitions, high-risk paths, ★ decisions, mandatory failure branches, design source, risk grading).
3. Wire the [gate script](scripts/) into CI, then run one small real feature through the full pipeline before scaling up.

## Status

**v0.2.0** — Full Chinese documentation: every document in the kit now ships with a 简体中文 edition beside the English original. (v0.1.0 was the first public release: blueprint, full template set, gate script, and one complete worked example.) On the roadmap: the blueprint in English, more examples (Delta-mode second platform, hotfix flow), and lint starter configs per stack.

This repository follows its own workflow where it applies: its CI runs the kit's test suites on every push and PR, and PRs use the kit's conventions (`Refs #`, risk self-assessment, evidence).

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). For non-trivial changes, open an issue describing intent and non-goals first; that is the workflow the kit teaches.

## License

MIT © 2026 Shinji
