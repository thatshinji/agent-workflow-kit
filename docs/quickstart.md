# Quickstart — adopt the kit in about 30 minutes

English | [简体中文](quickstart.zh-CN.md)

This guide takes a fresh repository from zero to "ready for its first feature under the workflow". The deep explanations live in the [blueprint](blueprint.md); the artifact shapes live in the [worked example](../examples/invite-code/). This page is only the path.

## Who this is for

- Solo builders and small teams who write code with one or more AI coding agents.
- Any stack: native mobile, web, servers in any language.
- Not for: pure-human teams with no agents (you can still steal individual mechanisms, e.g. evidence-based review), or throwaway prototypes you will never maintain.

**Prerequisites**: a git repository (GitHub/GitLab/…), a human who will be the decision-maker, at least one AI coding agent (two roles are needed; two tools or two sessions both work), Python 3 if you want the gate script.

## Step 0 — Install in one command (1 min)

From the root of **your** repository:

```bash
curl -fsSL https://raw.githubusercontent.com/thatshinji/agent-workflow-kit/v0.3.3/scripts/install.py | python3 -
```

The script downloads the kit — always the latest release — into a temp directory and scaffolds everything into your repository: all templates (mapping below), the gate script, and its config. It never overwrites an existing file — conflicts are skipped and reported (`--force` overrides). To preview without writing, append `--dry-run` after `python3 -`. For the Chinese templates: `... | python3 - --lang zh-CN` (they land under plain names, so your repository stays monolingual). For a lint starter for your stack add `--stack go` (or `web` / `swift` / `python`). To install a specific older release instead: `--kit-version <tag>`.

Prefer not to pipe a remote script? Clone this repository and run `python3 /path/to/agent-workflow-kit/scripts/install.py` — same result. Copying by hand also works; the mapping is:

| From the kit | To your repo |
|---|---|
| `templates/AGENTS.md` | `AGENTS.md` (root) |
| `templates/REVIEW.md` | `REVIEW.md` (root) |
| `templates/test-cases/*` | `docs/test-cases/` |
| `templates/project-management/*` | `docs/project-management/` (rename `platform-playbook.md` per platform) |
| `templates/specs/coding-standards.md` | `docs/tech-specs/coding-standards.md` |
| `scripts/check_tdd_compliance.py` | `scripts/` |
| `scripts/tdd-check.config.example.json` | `tdd-check.config.json` (root) |

## Step 1 — Fill the eight slots (15 min – half a day)

This is the only step that requires real thought; everything else is mechanics. Each slot below names where it lands:

1. **Data-isolation dimension** — multi-tenant? multi-workspace? single-user? Write the rule into `AGENTS.md` hard rules (e.g. "every query carries `tenant_id`, taken from the session only"). If your app has no shared data, replace this slot with your highest-risk invariant.
2. **Project hard rules (3–6)** — your non-negotiables (money in integer minor units; no heavy ORM; statistics computed in code, never by an LLM…) → `AGENTS.md`.
3. **Failure definitions** — rewrite the table in `REVIEW.md` §2 for your directories; keep the universal four: contract drift, secrets in logs, irreversible migrations, docs claiming planned work is done.
4. **High-risk paths** — auth / sessions / payments / migrations / data deletion… list them in `AGENTS.md` and `REVIEW.md` §8.
5. **★ contract decisions** — defaults for idempotency, the authorization matrix, calculation rules, retention & true deletion, deletion semantics, stub scope → `contract-checklist.md` (or leave per-feature, but say so).
6. **Mandatory failure branches** — adapt the TDD spec's list to your domain (IoT adds reconnects; commerce adds stock-outs and duplicate orders…).
7. **Design source** — where designs live and how code is checked against them 1:1 (a design-tool export + manifest, or at minimum a page list + screenshots). "One design source, no invented pages" is not optional.
8. **Risk grading** — what Low/Medium/High mean in your project (it drives gate strictness) → `AGENTS.md` DoD / PR template.

## Step 2 — Wire the gate (5 min)

The installer already placed `scripts/check_tdd_compliance.py` and `tdd-check.config.json` in your repository. Edit the globs in the config to match your layout (the example contains ready-made Go / Web / Swift / Java areas), then wire it into your one-command gate and CI per [scripts/README.md](../scripts/README.md). Run it once on an unchanged tree: it must print `PASS`.

## Step 3 — Assign the roles (2 min)

Write into your `AGENTS.md` who is who:

- **Decision-maker**: you (or your lead). Approves intent, ★ decisions, checklists; the only one who merges.
- **Writer**: agent/tool A. Drafts intent, contracts, checklists; implements.
- **Reviewer**: agent/tool B — a *different model* if you can; the same tool in a separate, context-free session if you can't. Writes tests independently; reviews with evidence.

## Step 4 — Run the first feature (the real test)

Pick the smallest feature that still crosses a real boundary (UI → API → data, or equivalent). Walk it through all eight steps from `AGENTS.md`, keeping [examples/invite-code/](../examples/invite-code/) open beside you — every artifact you must produce has a finished specimen there, including the red-test evidence and the reconciliation statement.

Expect friction. That is the point of the trial run: afterwards, fix every annoyance **in the documents** (step 6 of the blueprint's adoption phases), not in your head.

## Step 5 — After the first merge

- The archive four actions happened (hidden scenarios unsealed, cases updated, lessons distilled, matrix row added) — if any was skipped, do it now and note why it was skippable.
- Update your `docs/test-cases/INDEX.md`: your first real row exists. The library is alive.
- Second platform later? It consumes the same library in Delta mode (see the platform playbook template) — never re-runs steps 1–4.

## Lighter path: the minimal tier

If the full kit feels heavy for your current stage, start with five mechanisms — `AGENTS.md` hard rules + the (compressed) pipeline, the behavior case library, evidence-based review, the machine gate, and the archive step — and add the rest (hidden scenarios, Delta mode, full reconciliation statements) as you grow. What you may not do is *downgrade* a mechanism you adopted: evidence rules without evidence, or behavior cases written with implementation words, are worse than not adopting them.

## Honest time expectations

| Phase | Typical effort |
|---|---|
| Steps 0–3 (setup) | 30 minutes of mechanics + slot-filling (15 min – half a day) |
| First feature trial | Within the first week; budget the feature's normal time × 1.5 |
| Payoff | From the second feature onward: fewer review rounds, no re-litigated decisions, tests that mean something |

## Common questions

- **Only one agent available?** Use it as writer in one session and as reviewer in a fresh session with only the checklist and design as input. Independence of *context* matters more than independence of *vendor*.
- **Existing codebase, lots of legacy code?** The gate is incremental by design (new and changed lines only); the case library grows feature by feature. Never retrofit the whole repo at once.
- **No server / no API?** Skip the contract checklist for pure-client work; keep everything else. The checklist returns the moment two components must agree on data.
