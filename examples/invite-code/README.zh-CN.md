[English](README.md) | 简体中文

# 示例：「用邀请码加入」——一个功能走完八步全程

一个虚构但贴近真实的迷你功能，按照 `templates/AGENTS.md` 中的流水线端到端走完一遍。每一步的产物都是本文件夹里的真实文件，你可以清楚看到每个阶段产出什么、消费什么。代码是小体量的 Python（仅用标准库）——重点是工作流，不是技术栈。

**这个功能**：工作区所有者分享一个 6 位邀请码；任何拿到邀请码的人都能加入该工作区。邀请码会过期、使用次数有限、可以重新生成。猜码行为必须被限流，且错误信息绝不能泄露某个邀请码属于哪个工作区。

**角色阵容**：决策者（人类）· Writer（agent A）· Reviewer（agent B，不同的模型）。

## 走查全程

| 步骤 | 产物 | 要点 |
|---|---|---|
| 1. 意图与契约 | [01-issue-intent.zh-CN.md](01-issue-intent.zh-CN.md) | Writer 起草，决策者只做批准。★ 项是产品决策。非目标与不变行为在任何代码出现*之前*就先写明。 |
| 2. 行为清单与计划 | [02-behavior-cases.zh-CN.md](02-behavior-cases.zh-CN.md) | 用例是与平台无关的业务事实——没有「tap」、没有「toast」、没有 API 路径。每条用例都有稳定的 ID。这份文件后来正是归档入库的那一份。 |
| 3. 验收门 | （包含在 01 与 02 之中） | 决策者批准行为清单与 ★ 决策。此线以下的一切，在批准之前都不得开始。 |
| 4. 独立测试并冻结 | [04-implementation/test_invite.py](04-implementation/test_invite.py) + [03-red-evidence.zh-CN.md](03-red-evidence.zh-CN.md) | Reviewer 只依据行为清单写测试，拿测试对桩跑，把失败输出留作证据。2 条场景保持隐藏，直到终审轮。 |
| 5. 实现与自证 | [04-implementation/invite.py](04-implementation/invite.py) | 最小实现；测试名与用例 ID 一一对应（1:1）。合规门禁（`scripts/`）之所以通过，是因为测试与实现在同一个改动里一起变更。 |
| 6–7. Review 与裁决后修复 | [05-review-round.zh-CN.md](05-review-round.zh-CN.md) | finding 都带着 repro + expected/actual + refute_hint。其中一条裁决结论为 TRUE，一条被驳回（FALSE），一条是 Nit。本轮以对账单和一键验真命令收尾。 |
| 8. 合并与归档 | [06-archive-state.zh-CN.md](06-archive-state.zh-CN.md) | 隐藏场景解封进用例文件，教训被蒸馏，覆盖矩阵新增一行。此后，用例库就是*下一个*平台的事实源。 |

## 自己验证一遍

第 4–5 步的一切都可以真实运行：

```bash
cd examples/invite-code/04-implementation
python3 -m unittest test_invite -v        # 10 tests: 8 approved cases + 2 unsealed hidden scenarios
```

要复现第 4 步的跑红：把 `invite.py` 临时换成保留下来的桩文件（`invite_stub.py.txt`），再跑同一条命令——10 个测试全部以 `NotImplementedError` 失败，与 [03-red-evidence.zh-CN.md](03-red-evidence.zh-CN.md) 中记录的完全一致。
