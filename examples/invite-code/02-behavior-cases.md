English | [简体中文](02-behavior-cases.zh-CN.md)

# Step 2 artifact — Behavior checklist for "Join by invite code"

> Written by the writer from the approved contract (01), in the format of `templates/test-cases/TEMPLATE.md`. This is the version the decision-maker approved at the step-3 gate. The final archived version — after hidden scenarios are unsealed and lessons are added at step 8 — is shown in [06-archive-state.md](06-archive-state.md).

## 1. Intent

### Intent
A workspace owner shares a short invite code through any channel; anyone with a valid code becomes a member of that workspace in one step.

### Unchanged behaviors
- Member-list invitations work exactly as before.
- Joining grants the standard member role only.
- Regenerating a code does not affect existing members.

### Non-goals
- No per-person invite links; no approval queue; no usage analytics display.

## 2. Behavior cases

- **INV-001 Valid code joins** — Given a live code for a workspace, When a non-member submits it, Then they become a member of that workspace and one use is consumed.
- **INV-002 Expired code rejected** — Given a code past its expiry, When a non-member submits it, Then the join is rejected as expired and no membership is created.
- **INV-003 Exhausted code rejected** — Given a code whose uses are used up, When a non-member submits it, Then the join is rejected as exhausted and no membership is created.
- **INV-004 Unknown code leaks nothing** — Given a code that does not exist, When anyone submits it, Then the join is rejected with a generic invalid-code result that reveals no workspace information.
- **INV-005 Double join prevented** — Given a user who is already a member, When they submit the code again, Then the join is rejected as already-a-member and no additional use is consumed.
- **INV-006 Guessing is rate-limited** — Given a user who has failed 10 join attempts within an hour, When they submit any further code (even a valid one), Then the attempt is rate-limited.
- **INV-007 Regeneration invalidates** — Given an owner regenerates the workspace's code, When anyone submits the previous code, Then it is rejected as invalid, and the new code joins successfully.
- **INV-008 Input normalized** — Given a valid code, When a user submits it with different letter case or surrounding spaces, Then the join succeeds.

Platform differences: none identified at this step (joining is identical on all clients; sharing the code happens outside the app).

## Plan outline (summary)

- Server: invite-code storage + join endpoint per contract; failed-attempt counter per user.
- Clients: one join form + error mapping for the five contract error codes. No client-specific cases.
- Tests affected: none existing (new feature). New tests: one per case, written by the reviewer at step 4.

**Gate record**: decision-maker approved the checklist (8 cases) and the outline. Step 4 may begin.
