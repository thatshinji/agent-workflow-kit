English | [简体中文](05-review-round.zh-CN.md)

# Steps 6–7 artifact — Review round & reconciliation (Issue #101)

## Reviewer output (round 1)

```text
3 findings: Important 1 / Nit 1 / Pre-existing 0, plus 1 refuted at adjudication.
Scenario coverage: approved 8, passing 8; hidden 2, passing 1.
```

```yaml
- id: R-20260101-001
  severity: Important
  location: invite.py (join / failure counting)
  class: rate-limit-bypass
  claim: Failed attempts are counted only for well-formed unknown codes; malformed inputs (empty, symbols, wrong length) raise before the counter, so probing with malformed codes is unlimited. (Found by hidden scenario INV-H1.)
  repro: submit 10 malformed codes, then the valid code — the valid join succeeds instead of returning RATE_LIMITED
  expected: every failed attempt counts toward the per-user limit (contract §security)
  actual: malformed attempts are not counted
  refute_hint: show a run where 10 malformed attempts trigger RATE_LIMITED
- id: R-20260101-002
  severity: Nit
  location: invite.py (INVITE_EXHAUSTED message)
  claim: The exhausted-code message says "no uses left" while other messages use plainer wording; align copy tone.
  expected/actual: copy only, no behavior change
  refute_hint: n/a (style)
- id: R-20260101-003
  severity: Important
  location: invite.py (_normalize)
  claim: Upper-casing the input breaks codes, because codes might contain lowercase letters.
  repro: none provided
  expected: codes round-trip exactly
  actual: reviewer assumption, unverified
  refute_hint: the contract's generator alphabet is uppercase-only (01 §Business rules), so normalization cannot break a generated code
```

## Adjudication

| Finding | Verdict | Basis |
|---|---|---|
| R-20260101-001 | **TRUE** | Reproduced exactly as described; also caught by hidden scenario INV-H1 (hidden coverage: 1 of 2 passing at round 1) |
| R-20260101-002 | **TRUE** (Nit) | Copy aligned in the fix commit; does not block |
| R-20260101-003 | **FALSE** | Refuted by `refute_hint`: the contract fixes an uppercase-only alphabet; no repro was produced |

## Fix & reconciliation statement (posted to issue #101)

| Round | Finding | Severity | Verdict | Fix | Verification |
|---|---|---|---|---|---|
| 1 | R-20260101-001 | Important | TRUE | Failure counting moved ahead of format handling: every rejected attempt — malformed included — is recorded before the lookup result is returned | INV-H1 now passes; full suite green |
| 1 | R-20260101-002 | Nit | TRUE | Message copy aligned | suite green |
| 1 | R-20260101-003 | Important | FALSE | none (refuted) | contract §Business rules cited |

Hidden scenarios final: 2 of 2 passing (INV-H2 — the limit is per user, not global — passed from the start and confirmed the fix did not over-broaden the limit).

**One-shot verification command** (for the decision-maker):

```bash
cd examples/invite-code/04-implementation && python3 -m unittest test_invite
# Expected: Ran 10 tests — OK
```

Decision-maker checked the statement and the command output. The PR proceeds to the merge gate (step 8).
