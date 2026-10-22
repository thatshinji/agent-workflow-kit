English | [简体中文](02-case-mapping.zh-CN.md)

# Steps 2′–3′ artifact (Delta form) — Case mapping: archived INV cases → mobile

> Written by the writer from the archived case file (`docs/test-cases/workspace/invite-code.md`) and the approved delta intent (01). Every archived case receives a disposition; nothing is silently dropped. Mobile tests are implemented 1:1 against these IDs and run red first, as usual.

## Dispositions of the archived cases

| Case | Disposition | What it means on mobile |
|---|---|---|
| INV-001 Valid code joins | Reused 1:1 | The join itself is a server case; the mobile test verifies only the client outcome — the membership success state is presented. |
| INV-002 Expired code rejected | Reused 1:1 | Server enforces expiry; the mobile test verifies the expired result is presented as expired. |
| INV-003 Exhausted code rejected | Reused 1:1 | As INV-002, for the exhausted result. |
| INV-004 Unknown code leaks nothing | Reused 1:1 | The mobile test verifies the generic invalid-code result is presented and no workspace information is rendered. |
| INV-005 Double join prevented | Reused 1:1 | The mobile test verifies the already-member result is presented; "no use consumed" stays asserted by the server suite. |
| INV-006 Guessing is rate-limited | Server-only — not re-tested on mobile | Counting and enforcement are server-side (see INV-H1's lesson). The client only renders the shared `RATE_LIMITED` result through the standard error mapping; duplicating the counter tests on mobile would test the server twice. |
| INV-007 Regeneration invalidates | Server-only — not re-tested on mobile | The app has no regeneration surface; invalidation happens server-side. An old code submitted in the app surfaces as INV-004's generic result, already covered above. |
| INV-008 Input normalized | **Adapted** | Behavior unchanged — the join succeeds — but the mechanism moves: the client normalizes pasted input (trim, uppercase, strip internal spaces) *before* submission, per the delta intent. The server-side case still stands; the mobile test asserts the normalized value is what gets sent. |
| INV-H1 Malformed attempts count too | Server-only — not re-tested on mobile | Pure server counting property. Client normalization prevents most malformed submissions, but counting remains server-enforced and server-tested. |
| INV-H2 Limit is per user | Server-only — not re-tested on mobile | A cross-user isolation property of the server; a single-device client cannot stage two users' counters. Covered by the server suite in the same gate. |

## New platform cases

- **MOB-001 Deep link opens join** — Given a valid invite link, When a user with the app installed opens it, Then the join screen opens with the code prefilled, ready to confirm.
- **MOB-002 Paste normalized** — Given a code pasted with surrounding and internal spaces, When the user submits it, Then the normalized code is sent and the join succeeds.
- **MOB-003 Offline is explicit** — Given the device has no connection, When the user attempts to join, Then the app states that joining needs a connection and sends nothing; no join is queued or retried silently.

One further scenario was kept **hidden** by the reviewer until the review round, per the standard rule:

- **MOB-H1 Own code via deep link** — Given a deep link carrying a code for a workspace the user already belongs to, When the logged-in user opens it, Then they land on the already-member outcome (INV-005) — not an error — and no use is consumed.

**Gate record**: decision-maker approved this mapping and the three new cases (MOB-H1 unsealed at review time). The gate verified the delta only — the archived cases themselves were not re-approved. Implementation may begin.
