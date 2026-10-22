English | [简体中文](03-archive-state.zh-CN.md)

# Step 8 artifact (Delta form) — Archive state after merge

Delta mode compresses the front of the pipeline; the archive at the end runs in full. What changed in the library:

## ① Coverage matrix updated — Mobile column

`docs/test-cases/INDEX.md`, feature row:

| Feature | Case file | Server | Web | Mobile |
|---|---|---|---|---|
| Join by invite code | `workspace/invite-code.md` | ✅ | ✅ | ✅ |

Per-case state behind the Mobile cell (from the mapping in [02](02-case-mapping.md)):

| Case | Mobile state |
|---|---|
| INV-001…INV-005 | ✅ reused 1:1, passing |
| INV-006, INV-007, INV-H1, INV-H2 | ✅ covered by the server suite (server-only; not re-tested on mobile) |
| INV-008 | ✅ adapted (client-side paste normalization), passing |
| MOB-001…MOB-003, MOB-H1 | ✅ new platform cases, passing; filed in the feature file's platform-differences section |

## ② Review took one round — because scope was the delta

The review examined only the mapping, the adapted INV-008, and the MOB cases, per `REVIEW.md` with the case file as primary reference. It closed in a single round with no TRUE findings against the delta. That is the expected shape of a Delta review, not a shortcut: the behavior under the delta had already survived a full review in issue #101.

## ③ What was *not* re-opened

- The server contract and its five error codes — consumed as-is.
- The approved INV-001…INV-H2 cases — dispositions recorded, texts untouched.
- The adjudications of issue #101 (R-20260101-001 TRUE, R-20260101-002 Nit TRUE, R-20260101-003 FALSE) — verdicts stand; the INV-H1 lesson they produced is why INV-006/H1 could be marked server-only without discussion.

## ④ Review lesson distilled (feature file, §4 Review lessons)

- 2026-02-12 Entry points are platform behavior even when the feature is inherited: a deep link makes "already a member" a landing state instead of an error, so every new entry point earns its own case (MOB-H1) even when the underlying outcome (INV-005) is reused verbatim.

## What this buys the next platform

A third client now repeats exactly this walkthrough: inherit the contract and the library, state its differences, map the same ten cases, add only its genuinely new ones. The feature's behavior will have been decided **once** — in issue #101 — no matter how many platforms implement it.
