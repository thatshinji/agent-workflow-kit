English | [简体中文](review-protocol.zh-CN.md)

<!--
  TEMPLATE: docs/project-management/review-protocol.md
  The adjudication protocol behind REVIEW.md: how findings are formatted,
  judged, fixed, and reconciled. The mechanism is the kit's — keep it intact.
-->

# Review & Adjudication Protocol

> Effective: <YYYY-MM-DD>. Applies to every PR review in this repository. Reviewers also read `REVIEW.md`; the pipeline context is in `AGENTS.md`.

## 1. Principles

- Review catches real problems; it is not a style census and not a rewrite service.
- **No evidence, no finding.** A claim that cannot be reproduced or cited is recorded as `UNKNOWN` and drives nothing.
- The decision-maker is the only merge authority and the final arbiter of disputes.

## 2. Finding format (Appendix A)

Every finding is reported in this shape:

```yaml
- id: R-<YYYYMMDD>-<NNN>          # sequential per day, never reused
  severity: Important | Nit | Pre-existing
  location: <file>:<line>
  class: <short problem class, e.g. authz-missing / contract-drift / test-gap>
  claim: <one sentence — the wrong behavior, in plain language>
  repro: <executable command or steps>        # or spec_ref below
  spec_ref: <document + section that forbids this>   # alternative to repro
  expected: <what should happen>
  actual: <what happens>
  refute_hint: <what result would prove this finding wrong>
```

Rules: Important findings first; each class of problem is reported once, completely (list every instance under one finding instead of dripping them across rounds); "outside checklist" findings are labeled as such.

## 3. Adjudication (three states)

Each finding is independently adjudicated — by the decision-maker or an agent who did not author the finding — into exactly one state:

| State | Meaning | Consequence |
|---|---|---|
| `TRUE` | Reproduced / spec clearly violated | Enters the fix queue; Important + TRUE blocks merge |
| `FALSE` | Refuted by counter-evidence | Closed with the counter-evidence recorded |
| `UNKNOWN` | Cannot be reproduced, evidence insufficient | Does **not** drive rework and does **not** block merge |

**Security/compliance exception**: for findings on high-risk paths (auth, sessions, payments, migrations, secrets, destructive scripts), an `UNKNOWN` that describes a plausible severe impact is escalated to the decision-maker before merge instead of being silently dropped.

Adjudicated findings are recorded in the review ledger (`reviews/ledger.yaml`) and are never re-raised in later reviews.

## 4. Rounds

- At most **3 rounds** per PR. Round 1 reviews the full specified diff; rounds 2+ review only the new diff.
- If round 3 still produces new Important findings, the PR stops iterating and goes back to the design level (checklist/contract), with the decision-maker arbitrating.
- The writer may rebut a finding with counter-evidence; the adjudicator rules. Disputes beyond the approved checklist scope escalate to the decision-maker immediately.

## 5. Fix & reconciliation

- Fixes reference finding IDs in commit messages or the PR body (`R-YYYYMMDD-NNN`, verdict, evidence).
- When all TRUE findings are fixed, the writer posts a **reconciliation statement** on the issue: a table of every finding (round, ID, severity, location, plain-language description, verdict, fixing commit, verification evidence).
- The statement ends with a **one-shot verification command**: a single copy-paste command the decision-maker can run to re-check the claims in seconds, with the expected output described in plain language.
- Only after the decision-maker checks the statement does the PR proceed to the merge gate (pipeline step 8).

## 6. Reviewer rotation & independence

- The reviewer is never the writer of the same change. Prefer a different model/agent than the writer's.
- A reviewer who cannot execute commands marks all output `UNKNOWN` by default; an adjudicator with execution ability reproduces before upgrading.
