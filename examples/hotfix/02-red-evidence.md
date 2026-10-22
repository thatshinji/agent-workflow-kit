English | [简体中文](02-red-evidence.zh-CN.md)

# Hotfix evidence — Regression test red first, then green (Issue #137)

## Where the regression case comes from

The behavior is not new, and neither is its case. The archived checklist for this feature ([02](../invite-code/02-behavior-cases.md)) already contains:

- **INV-002 Expired code rejected** — Given a code past its expiry, When a non-member submits it, Then the join is rejected as expired and no membership is created.

—and the contract ([01](../invite-code/01-issue-intent.md) §Interface) already names the required error: `INVITE_EXPIRED` (410). What was never pinned is the *envelope*: INV-002's step-4 test asserted the service's domain result, which was correct all along. The regression test **HF-001** is INV-002 re-asserted at the response-envelope layer — the layer where the bug actually lives. Three neighboring rows of the same mapping table get envelope pins in the same file, so the fix cannot quietly move the fall-through elsewhere.

The tests live with the feature's code, in `examples/invite-code/04-implementation/test_invite_hotfix.py` (stdlib `unittest`, same as the feature suite).

## Red run (before the fix)

```text
$ python3 -m unittest test_invite_hotfix -v
test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping) ... FAIL
test_pin_exhausted_reports_exhausted (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_revoked_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_unknown_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok

======================================================================
FAIL: test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_invite_hotfix.py", line 38, in test_hf_001_expired_reports_expired
    self.assertEqual(resp.error_code, "INVITE_EXPIRED")
AssertionError: 'INVITE_NOT_FOUND' != 'INVITE_EXPIRED'
- INVITE_NOT_FOUND
+ INVITE_EXPIRED

----------------------------------------------------------------------
Ran 4 tests in 0.003s

FAILED (failures=1)
```

Exactly one failure — the reported bug, reproduced. The three neighboring pins pass, confirming the fall-through affects only the missing row.

## The fix

One row added to the error-mapping layer: an `EXPIRED` service result now maps to `INVITE_EXPIRED` (410), with its user-facing message. No business logic touched.

## Green run (after the fix)

```text
$ python3 -m unittest test_invite_hotfix -v
test_hf_001_expired_reports_expired (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_exhausted_reports_exhausted (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_revoked_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok
test_pin_unknown_reports_not_found (test_invite_hotfix.TestErrorMapping) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK
```

Full suite (feature + hotfix): 14 tests, OK — recorded in the reconciliation statement (03).
