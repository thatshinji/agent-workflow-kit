English | [简体中文](01-delta-intent.zh-CN.md)

# Step 1 artifact (Delta form) — Issue #118: Invite-code joining in the mobile app

## Intent (drafted by the writer, approved by the decision-maker)

Six weeks after the web launch, joining by invite code comes to the mobile app. In Delta mode the intent does not restate the feature — it states only what this platform inherits and where it differs. The feature's behavior was decided in issue #101 and lives in `docs/test-cases/workspace/invite-code.md`; this document never overrides it.

### Inherited — not re-decided, not re-reviewed

- **Server contract, unchanged**: `POST /workspaces/join { code }` with the standard error envelope (`INVITE_NOT_FOUND`, `INVITE_EXPIRED`, `INVITE_EXHAUSTED`, `ALREADY_MEMBER`, `RATE_LIMITED`). The app is a new client of the same endpoint; no contract draft is written.
- **Business rules, unchanged**: 6-character codes; a repeated join returns `ALREADY_MEMBER` and does not consume a use; failed attempts are rate-limited at 10 per user per hour; codes live 7 days with 5 uses; regeneration invalidates the old code immediately.
- **Unchanged behaviors, unchanged**: member-list invitations work as before; joining grants the standard member role only; existing members are unaffected by regeneration.

### Platform differences (this platform only)

- **Codes arrive from outside the app**: an invite link opens the join screen directly via deep link, and a code can be scanned in-app. There is no "find the join form" step.
- **The app consumes codes; it never generates them.** Code creation and regeneration stay on the web (owner flows unchanged). The app has no owner-side code management.
- **Paste is normalized on the client**: pasted text is trimmed and stripped of internal spaces before submission, extending INV-008's input normalization to how codes actually arrive on mobile (copied from messages, with spaces).
- **Offline is explicit, never silent**: with no connection, the app says joining needs a connection and sends nothing. A join is never queued for silent retry later.
- **★ Deep link while logged out** — a code link is tapped by someone not logged in: drop the code, or keep it? → *Decision-maker: keep it — after login, the join resumes with the code already filled in.* `decided by decision-maker`

### Non-goals (this platform)

- No code generation, regeneration, or usage display in the app (web only, as decided in #101).
- No new error codes and no client-side rate limiting — counting stays server-side.

**Gate record**: decision-maker approved the difference list and the one new ★ decision. The archived behavior was not presented for re-approval, per the Delta SOP. Step 2′ (case mapping) may begin.
