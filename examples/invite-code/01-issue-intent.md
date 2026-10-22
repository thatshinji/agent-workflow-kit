English | [简体中文](01-issue-intent.zh-CN.md)

# Step 1 artifact — Issue #101: Join a workspace by invite code

## Intent (drafted by the writer, approved by the decision-maker)

Workspace owners currently invite members one by one from the member list, which breaks down when a whole team or class needs to join at once. This feature lets an owner generate a short invite code and share it through any channel; anyone with the code joins the workspace in one step.

### Unchanged behaviors (writer's proposal — approved)

- Member-list invitations keep working exactly as before.
- Only owners can see or manage workspace settings; joining grants the standard member role, nothing more.
- Existing members are unaffected by code regeneration.

### Non-goals (writer's proposal — approved)

- No per-person invite links in this round.
- No approval queue: a valid code joins immediately.
- No code usage analytics page (counts are stored, not displayed).

## Contract draft (writer, walked through the contract checklist)

Each item marked `decided` / `follows standard` / `open question`:

- **Interface** — `POST /workspaces/join { code }` → `200 { workspace_id }`. Errors use the standard envelope: `INVITE_NOT_FOUND` (404), `INVITE_EXPIRED` (410), `INVITE_EXHAUSTED` (409), `ALREADY_MEMBER` (409), `RATE_LIMITED` (429). `decided`
- **Data model** — one live code per workspace; a code row holds `code` (unique), `workspace_id`, `expires_at`, `max_uses`, `uses`, `revoked_at`. Regeneration revokes the previous row rather than deleting it (audit). `decided`
- **Business rules** — codes are 6 characters from an uppercase alphanumeric alphabet without ambiguous glyphs (no `0/O`, `1/I`); input is normalized (trim + uppercase) before lookup. `decided`
- **★ Idempotency** — joining twice with the same code must not double-count a use or duplicate the membership. → *Decision-maker: second join returns `ALREADY_MEMBER` and does not consume a use.* `decided by decision-maker`
- **Authorization & security** — unknown, revoked, and malformed codes all return the same generic `INVITE_NOT_FOUND`; responses never include workspace names before a successful join. Failed attempts are rate-limited per user. `decided`
- **★ Rate-limit parameters** — how many failed attempts, per what window? → *Decision-maker: 10 failed attempts per user per hour, then `RATE_LIMITED` even for the correct code.* `decided by decision-maker`
- **★ Code lifetime & uses** — defaults? → *Decision-maker: 7 days, 5 uses; owners may regenerate at any time, which immediately invalidates the old code.* `decided by decision-maker`
- **External dependencies** — none this round (sharing happens outside the app). `decided`
- **Acceptance hand-off** — the assertions above feed the behavior checklist (step 2) verbatim. Stub group: none — no external dependency is stubbed.

**Gate record**: decision-maker approved the intent, both lists, and the three ★ decisions. Step 2 may begin.
