[English](README.md) | 简体中文

# 示例：Delta 模式——第二个平台上的「凭邀请码加入」

[../invite-code/](../invite-code/README.zh-CN.md) 中的邀请码功能，在 Web 上线六周后进入本项目的移动 App。服务端契约和行为用例库都已存在且已批准——所以这个走查展示的是流程**压缩**后的样子：只把平台差异写出来、过验收门、评审；继承的东西一律原样消费。

**Delta 模式的要点**：行为只在用例库里决定一次。新平台说明自己有何*不同*，把测试 1:1 映射到已归档的用例 ID，并更新覆盖矩阵中自己那一列。完整流程的步骤 1–4 不重跑，契约不重写，既往裁决不重开。

**参与角色**：决策者（人）· Writer（agent A）· Reviewer（agent B，不同模型）——角色不变，只是范围缩小。

## 走查

| Delta 步骤 | 产物 | 看点 |
|---|---|---|
| 1′. Delta 意图 | [01-delta-intent.zh-CN.md](01-delta-intent.zh-CN.md) | 只有两张清单：继承什么（不重新决策）、本平台有何不同。只出现一条新的 ★ 决策——其余都在 issue #101 里定过了。 |
| 2′–3′. 用例映射与 Delta 验收门 | [02-case-mapping.zh-CN.md](02-case-mapping.zh-CN.md) | 每个已归档用例都有处置结论——原样复用、适配或服务端专属——外加少数真正新增的平台用例。验收门只验*这张表和新用例*。 |
| 4′–7′. 测试、实现、评审 | （在 02 与 03 中概述） | 测试按用例 ID 1:1 实现、照例先跑红。评审范围限于 Delta，一轮即可收尾。 |
| 8′. 归档 | [03-archive-state.zh-CN.md](03-archive-state.zh-CN.md) | 覆盖矩阵的 Mobile 列写入状态；教训回写进功能文件。用例库——而不是这个 PR——仍是唯一事实来源。 |

## 自己验证

没有新的服务端代码可跑：接口和它的测试就是 [../invite-code/04-implementation/](../invite-code/04-implementation/) 那一份。移动端的工作对照 [02-case-mapping.zh-CN.md](02-case-mapping.zh-CN.md) 中的映射来验证——每一行都写明了其测试所对应的用例 ID。
