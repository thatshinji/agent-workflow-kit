<!--
  TEMPLATE: REVIEW.md — copy to your repository root and fill in every <slot>.
  This file tells every reviewer (human or AI) what counts as a failure here,
  what evidence a finding needs, and where review stops. Keep it short and
  executable; if a rule cannot be applied mechanically, rewrite it until it can.
  The structure and evidence rules are the kit's mechanism — keep them as-is.
  The failure-definition table is your project's slot: rewrite its rows.
-->

# REVIEW.md — Reviewer Guide

> Read together with `AGENTS.md`. The full process (adjudication, rounds, reconciliation) lives in `docs/project-management/review-protocol.md`.

## 1. What this repository is

- <One or two lines: who builds this (e.g. one decision-maker + multiple AI agents), current stage, stack summary.>
- Review exists to **catch real problems and reduce rework** — not to enumerate style nits, and not to rewrite the author's work.
- **Judgment priority** (when sources conflict, this chain decides): `AGENTS.md` hard rules > frozen specs & coding standards > the decision-maker-approved behavior checklist for this issue > the TDD spec > this file > general engineering common sense.

## 2. What counts as a failure (by directory)

Rewrite each row for your project. The four universal rows (contract drift, secrets in logs, irreversible migrations, documentation claiming planned work is done) should survive in some form in every project.

| Path | What "failure" looks like |
|---|---|
| `<server/>` | Build/test failure; authorization bypass (missing `<isolation-id>` check); non-atomic transactions; un-rollback-able migrations; secrets or PII in logs; error-envelope inconsistency; serious violation of the coding standards; production change without paired tests, or new tests covering only the happy path |
| `<server/migrations/>` | Up without down; editing migration history; a `down` that silently drops data |
| `<apps/>` | API path or DTO drift from the contract source; pages built outside the design source or unregistered in the design manifest; unhandled 401/403/429 states; serious violation of the coding standards; core-logic change without paired tests or without negative cases |
| `<docs/specs/>` | Contradicting the frozen baseline; writing a proposal as if already in effect; fields inconsistent with migrations |
| `<docs/>` | Broken links; planned work described as implemented; conclusions without evidence or dates |
| `<.github/>` | Bypassing gates; auto-closing keywords; breaking CI/template semantics |
| `<scripts/>` | Destructive operations without confirmation; hard-coded environment names; swallowed errors; script change without paired tests |

## 3. Severity

| Label | Meaning | Handling |
|---|---|---|
| **Important** | Wrong behavior, security, data risk, contract/CI bypass | Must be adjudicated; if `TRUE`, must be fixed |
| **Nit** | Style, naming, cleanup; no behavior change | At most 3 per PR; never blocks a merge |
| **Pre-existing** | Existed before this PR | Label it; not the author's debt; file a separate issue |

## 4. Evidence requirements

- Every finding must provide: `file:line` + an executable `repro` (or a citable `spec_ref`) + `expected / actual`.
- If you cannot reproduce it, label it `UNKNOWN` — do not write it up as a bug.
- Every finding must include a `refute_hint`: what result would prove you wrong.
- **Not accepted**: "might / maybe / best practice / could break in production" — claims without evidence.
- Review only the diff of the specified commit SHA. From round 2 on, review only the new diff.
- A reviewer who cannot execute commands produces `UNKNOWN` by default; an adjudicator reproduces before anything is upgraded.

## 5. Scenario & test duties

- **Before implementation**: after the writer submits the behavior checklist, the reviewer writes the tests independently from the checklist (or adversarially audits the writer's tests), working from the design and checklist only — never from the writer's implementation approach. Tests must be run red and the failing output kept as evidence; a test that cannot go red is invalid and is sent back.
- **Test freeze**: approved, frozen tests may not be modified by the writer. A test changed without re-approval is an Important finding on sight.
- **Hidden scenarios**: the reviewer (or decision-maker) keeps 2–3 hidden scenarios, runs them only in the final review round, and does not reveal them during fix rounds. A hidden-scenario failure is Important. After the final round passes, the reviewer produces the behavior-level draft of the hidden scenarios so the writer can archive them verbatim at merge time.
- **Coverage check**: review step one is always the approved checklist — every case needs a corresponding passing test; a case with no test is treated as unimplemented. Findings about behavior outside the checklist are allowed under §2 but must be labeled "outside checklist".
- **Mappability check**: new/changed behavior cases are checked against the forbidden-words list (implementation words such as click/tap/swipe, toast, modal, component names, routes, pixel values). Expected results must be business facts any platform can implement.
- **Library sync check**: if this PR changes the behavior of an already-archived feature, the diff must include the matching update to `docs/test-cases/`. Missing sync is Important.
- **Stub behavior**: cases labeled "real behavior (activates on integration)" are not a basis for findings this round.

## 6. Skip paths

- Generated code: <e.g. `<generated-dir/>` — change the source definitions instead>
- Lock files, binaries, vendored assets
- Findings already adjudicated in the review ledger (`docs/project-management/reviews/ledger.yaml`) — do not re-raise
- Pure formatting (leave it to the formatter/linter)

## 7. Output format

Start with one summary line:

```text
<N> findings: Important <a> / Nit <b> / Pre-existing <c>
```

Plus one coverage line:

```text
Scenario coverage: approved <N>, passing <M>; hidden <K>, passing <J>.
```

If there are no blocking findings:

```text
No blocking findings. Optional note: <risks without evidence go here>
```

Each finding uses the YAML format from the review protocol's appendix, Important first.

## 8. Review boundaries

- You are responsible for this diff and its direct effects only. Do not demand refactors or future features.
- At most 3 rounds. Beyond that, the author goes back to the design level instead of iterating findings.
- Report each class of problem once, completely — do not drip one instance per round.
- Security-sensitive and high-risk paths (<auth, sessions, migrations, CI, secrets, frozen contracts, destructive scripts — adjust to your project>) get a separate security pass, confirmed by the decision-maker.

## Changelog

| Version | Date | Change |
|---|---|---|
| v1.0 | <YYYY-MM-DD> | Initial version |
