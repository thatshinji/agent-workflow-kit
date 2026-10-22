[English](03-review-and-archive.md) | 简体中文

# 紧急修复评审与归档（Issue #137）

## Reviewer 输出（第 1 轮——也是唯一一轮）

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

## 裁决

| Finding | 裁决结论 | 依据 |
|---|---|---|
| R-20260114-001 | **TRUE**（Nit） | 文案在修复提交中对齐；不阻塞 |

## 对账单（已贴到 issue #137）

| 轮次 | Finding | 严重度 | 裁决结论 | 修复 | 核验 |
|---|---|---|---|---|---|
| — | （事故本身） | 中等 | 已由 HF-001 跑红确认 | 给错误映射层补上缺失的 `EXPIRED` 行 | HF-001 跑绿；3 个相邻钉测跑绿 |
| 1 | R-20260114-001 | Nit | TRUE | 过期码文案与契约用词对齐 | 完整套件跑绿 |

**一键验真命令**（给决策者）：

```bash
cd examples/invite-code/04-implementation && python3 -m unittest test_invite test_invite_hotfix
# Expected: Ran 14 tests — OK
```

决策者已核对对账单与命令输出。本 PR 进入合并门。

## 归档动作（同一个 PR 内，合并前完成）

紧急修复的归档和功能完全一样——这正是快速通道存在的意义所要保护的那一步：

1. **回归用例升入用例库。** HF-001 以行为层形式写入 `docs/test-cases/workspace/invite-code.md`，按顺序编为下一条 **INV-009**：
   - **INV-009 Expired is reported as expired**（过期就报过期）——Given 一个已过期的码和一个不存在的码，When 分别提交两者，Then 过期码的拒绝要报告原因是*已过期*——与未知码的笼统无效码结果可区分——同时两个响应都不泄露任何工作区信息。（来源：事故 #137；INV-002 的错误信封层钉测。）
   用例库缺的不是这个行为——INV-002 已覆盖"拒绝"——缺的是"*报告出来的原因*必须在翻译进错误信封后依然成立"这条要求。INV-009 把它永久写明了。
2. **补库 issue 由这同一个 PR 了结。** Issue #138（"backfill: pin INV-002 at the envelope layer in the case library"）在事故分诊时就已立项；归档动作 1 本身就是补库，所以 #138 随本 PR 一起关闭，而不是留成跟进欠账。
3. **教训沉淀**进功能文件的评审教训：
   - 2026-01-14 一个永远到不了响应错误信封的域结果，就是一份被打破的契约——而一条笼统错误的安全规则（INV-004）恰好能掩盖这种断裂。错误映射表的*每一行*都要钉住，不只是顺利的那些行。（来自事故 #137）
4. **映射表成为契约清单的常查项。** 契约清单新增一条永久条目：*每个不同的域结果在错误映射表里都要有一行，且每一行都被错误信封层的测试钉住。* 紧急修复教一次的东西，清单在之后每个功能上都会问——这符合流程的规则：同一类 finding 反复出现，就要变成机器可查的条目，而不是一句提醒。
5. **覆盖矩阵**：不变——同一个功能，没有新平台。INV-009 加入既有那一行的用例文件。

事故关闭；它暴露的洞也随之关闭——关在用例库和清单里，不只是关在代码里。
