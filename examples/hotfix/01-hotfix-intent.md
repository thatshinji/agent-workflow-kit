English | [简体中文](01-hotfix-intent.zh-CN.md)

# Hotfix intent — Issue #137: Expired invite codes report the wrong error

## Incident summary (the intent, five lines — approved by the decision-maker in this issue)

- **Phenomenon**: submitting an expired invite code returns `INVITE_NOT_FOUND` (404). The contract (invite-code [01](../invite-code/01-issue-intent.md) §Interface) requires `INVITE_EXPIRED` (410).
- **Impact**: every user holding an expired code is told, in effect, "no such code." Support cannot distinguish *expired* from *never existed* in reports, so expired-code complaints are closed as user error.
- **Severity**: Medium — no data loss, no security exposure (the wrong answer is the *more* generic one), but the failure reason is undiagnosable for users and support alike.
- **Root cause (located before the fix was approved)**: the join service already returns distinct results — expired is detected correctly, and case INV-002 passes at the domain layer. The defect is in the layer that translates service results into the response envelope: its mapping table has no `EXPIRED` row, so expired results fall through to the default `INVITE_NOT_FOUND`. The fall-through went unnoticed because INV-004's security rule (unknown, revoked, and malformed codes all return the generic `INVITE_NOT_FOUND`) made the wrong output look intentional.
- **Fix scope**: add the missing row to the error-mapping layer so an expired result surfaces as `INVITE_EXPIRED`, plus the user-facing message for it. Nothing else.

## Explicitly out of scope

- No business rules change: expiry, uses, rate limiting, and normalization behave exactly as the archived contract specifies.
- No other error mapping is redesigned in this PR — the neighboring rows are *pinned by tests* (see 02), not modified.
- The other features' mappings are audited by a separate, non-urgent issue; they are not part of this incident.

## Kept at full strength vs. compressed

| Kept at full strength (never compressed) | Compressed (safe to shrink) |
|---|---|
| Regression test written and run **red first**, output kept as evidence (02) | Intent: this five-line incident version instead of a full feature brief |
| One complete review round with **adjudication** of every finding (03) | Approval gate: the decision-maker approves the fast lane and the scope directly in this issue — no separate gate artifact |
| **Archive write-back**: regression case promoted into the case library, lesson distilled, checklist updated (03) | Case list: the regression case plus envelope pins for the adjacent mapping rows only — not the feature's full checklist |
| One-shot verification command for the decision-maker (03) | Plan outline: one line — "one mapping row, one message" replaces the file-level plan |

**Gate record**: the decision-maker confirmed all three fast-lane conditions in issue #137 (production impact real; blast radius = one mapping row; fast lane approved) and approved this intent and scope. Work may begin.
