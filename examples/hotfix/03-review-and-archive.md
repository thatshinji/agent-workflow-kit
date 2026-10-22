English | [简体中文](03-review-and-archive.zh-CN.md)

# Hotfix review & archive (Issue #137)

## Reviewer output (round 1 — the only round)

```text
1 finding: Important 0 / Nit 1 / Pre-existing 0.
Regression coverage: HF-001 red→green evidence checked; neighboring mapping rows pinned, 3 of 3 passing.
```

```yaml
- id: R-20260114-001
  severity: Nit
  location: error messages (INVITE_EXPIRED message)
  claim: The new expired-code message says "this code has lapsed" while every other message uses the contract's own plain wording ("invalid code", "no uses left"); say "this code has expired".
  expected/actual: copy only, no behavior change
  refute_hint: n/a (style)
```

## Adjudication

| Finding | Verdict | Basis |
|---|---|---|
| R-20260114-001 | **TRUE** (Nit) | Copy aligned in the fix commit; does not block |

## Reconciliation statement (posted to issue #137)

| Round | Finding | Severity | Verdict | Fix | Verification |
|---|---|---|---|---|---|
| — | (the incident itself) | Medium | confirmed by HF-001 red run | Missing `EXPIRED` row added to the error-mapping layer | HF-001 green; 3 neighboring pins green |
| 1 | R-20260114-001 | Nit | TRUE | Expired-code message aligned to the contract's wording | full suite green |

**One-shot verification command** (for the decision-maker):

```bash
cd examples/invite-code/04-implementation && python3 -m unittest test_invite test_invite_hotfix
# Expected: Ran 14 tests — OK
```

Decision-maker checked the statement and the command output. The PR proceeds to the merge gate.

## Archive actions (same PR, before merge)

A hotfix archives exactly like a feature — this is the step the fast lane exists to protect:

1. **The regression case is promoted into the case library.** HF-001 is written into `docs/test-cases/workspace/invite-code.md` in behavior-layer form, numbered next in sequence as **INV-009**:
   - **INV-009 Expired is reported as expired** — Given a code past its expiry and a code that does not exist, When each is submitted, Then the expired code's rejection reports the reason *expired* — distinguishable from the generic invalid-code result for the unknown code — while neither response reveals any workspace information. (Source: incident #137; envelope-level pin of INV-002.)
   The library was not missing the behavior — INV-002 covered rejection — it was missing the requirement that the *reported reason* survive translation into the envelope. INV-009 states it permanently.
2. **The backfill issue is discharged by this same PR.** Issue #138 ("backfill: pin INV-002 at the envelope layer in the case library") was filed when the incident was triaged; archive action 1 *is* the backfill, so #138 closes with this PR instead of lingering as follow-up debt.
3. **Lesson distilled** into the feature file's review lessons:
   - 2026-01-14 A domain result that never reaches the response envelope is a broken contract — and a generic-error security rule (INV-004) can mask exactly that break. Pin *every* row of the error-mapping table, not just the happy rows. (from incident #137)
4. **The mapping table becomes a standing contract-checklist item.** The contract checklist gains a permanent entry: *every distinct domain result has a row in the error-mapping table, and every row is pinned by a test at the envelope level.* What a hotfix teaches once, the checklist asks on every future feature — per the pipeline's rule that a repeated class of finding becomes a machine-checkable item, not a reminder.
5. **Coverage matrix**: unchanged — same feature, no new platform. INV-009 joins the existing row's case file.

The incident is closed; the hole it revealed is closed with it — in the library and in the checklist, not just in the code.
