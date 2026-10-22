[English](05-review-round.md) | 简体中文

# 第 6–7 步产物 — Review 轮次与对账单（Issue #101）

## Reviewer 输出（第 1 轮）

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

## 裁决

| finding | 裁决结论 | 依据 |
|---|---|---|
| R-20260101-001 | **TRUE** | 已按描述精确复现；也被隐藏场景 INV-H1 抓到（第 1 轮时隐藏场景覆盖：2 条中 1 条通过） |
| R-20260101-002 | **TRUE**（Nit） | 文案已在修复提交中对齐；不阻塞合并 |
| R-20260101-003 | **FALSE** | 被 `refute_hint` 驳回：契约已定死生成字符集只含大写字母；且没有给出任何 repro |

## 修复与对账单（已发布到 issue #101）

| 轮次 | finding | 严重度 | 裁决结论 | 修复 | 验证 |
|---|---|---|---|---|---|
| 1 | R-20260101-001 | Important | TRUE | 失败计数移到格式处理之前：每一次被拒的尝试——包括格式错误的——都在返回查找结果之前先记入计数 | INV-H1 现已通过；全套测试跑绿 |
| 1 | R-20260101-002 | Nit | TRUE | 提示文案已对齐 | 全套测试跑绿 |
| 1 | R-20260101-003 | Important | FALSE | 无（已被驳回） | 引用了契约 §业务规则 |

隐藏场景最终结果：2 条全部通过（INV-H2——限流是按用户的、不是全局的——从一开始就通过，并证实这次修复没有把限流范围过度扩大）。

**一键验真命令**（供决策者使用）：

```bash
cd examples/invite-code/04-implementation && python3 -m unittest test_invite
# Expected: Ran 10 tests — OK
```

决策者已核对对账单与命令输出。PR 进入合并门（第 8 步）。
