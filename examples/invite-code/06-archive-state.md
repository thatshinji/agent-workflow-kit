English | [简体中文](06-archive-state.zh-CN.md)

# Step 8 artifact — Archive state after merge

Merging is not the end of the pipeline. Four archive actions close the loop:

## ① Hidden scenarios unsealed into the case file

The reviewer supplied behavior-level drafts; the writer added them to `docs/test-cases/workspace/invite-code.md` (the archived home of the file drafted in [02](02-behavior-cases.md)) verbatim, format only:

- **INV-H1 Malformed attempts count too** — Given a user submitting malformed codes (empty, wrong shape), When the failed attempts reach the rate limit, Then further attempts — even with a valid code — are rate-limited.
- **INV-H2 Limit is per user** — Given one user rate-limited by failed attempts, When a different user submits a valid code, Then the join succeeds.

## ② Case-file changes from this PR are in the current version

The archived file is the step-2 checklist + the two unsealed cases + §4 below. No other behavior changed during implementation (if it had, the sync rule would have required updating this file in the same PR).

## ③ Review lessons distilled (feature file, §4 Review lessons)

- 2026-01-01 Rate limiting must count *every* rejected attempt, including malformed input — format validation is not a security boundary. (from R-20260101-001)
- 2026-01-01 A finding that contradicts the contract's stated alphabet is refuted by the contract, not by debate — cite the clause. (from R-20260101-003)

## ④ Coverage matrix row added

`docs/test-cases/INDEX.md` gains:

| Feature | Case file | Server | Web | Mobile |
|---|---|---|---|---|
| Join by invite code | `workspace/invite-code.md` | ✅ | ✅ | — |

## What this buys the next feature

When the mobile app implements joining next quarter, it does not re-run steps 1–4: it consumes this file in Delta mode — states its platform differences, maps tests 1:1 to INV-001…INV-H2, and flips its matrix cell to ✅. The probing hole (INV-H1) will never be re-introduced, because the case — and the lesson that explains it — now live in the library, not in a closed PR.
