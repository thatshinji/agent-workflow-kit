<!--
  TEMPLATE: docs/project-management/review-protocol.md
  REVIEW.md 背后的裁决协议：finding 如何格式化、如何裁决、如何修复、如何对账。
  这套机制是本工具包的核心——保持原样。
-->

[English](review-protocol.md) | 简体中文

# 审查与裁决协议

> 生效日期：<YYYY-MM-DD>。适用于本仓库的每一次 PR 审查。Reviewer 还须阅读 `REVIEW.md`；流程上下文见 `AGENTS.md`。

## 1. 原则

- 审查是抓真实问题；不是风格普查，也不是代写服务。
- **没有证据，就没有 finding。** 无法复现或引证的主张记为 `UNKNOWN`，不驱动任何动作。
- 决策者是唯一的合并权持有者，也是争议的最终裁决人。

## 2. Finding 格式（附录 A）

每条 finding 按以下形状报告：

```yaml
- id: R-<YYYYMMDD>-<NNN>          # 当日顺序编号，永不复用
  severity: Important | Nit | Pre-existing
  location: <file>:<line>
  class: <简短的问题类别，如 authz-missing / contract-drift / test-gap>
  claim: <一句话——用大白话说清错误行为>
  repro: <可执行的命令或步骤>        # 或用下面的 spec_ref
  spec_ref: <禁止此行为的文档 + 章节>   # repro 的替代项
  expected: <应该发生什么>
  actual: <实际发生什么>
  refute_hint: <什么结果能证明这条 finding 是错的>
```

规则：Important finding 优先；同一类问题只报一次、报全（把所有实例列在一条 finding 下，不要逐轮挤牙膏）；"清单之外"的 finding 要如实标注。

## 3. 裁决（三态）

每条 finding 由决策者、或未撰写该 finding 的 agent 独立裁决，恰好落入一态：

| 状态 | 含义 | 后果 |
|---|---|---|
| `TRUE` | 已复现 / 规格被明确违反 | 进入修复队列；Important + TRUE 阻塞合并 |
| `FALSE` | 被反证驳回 | 关闭，并记录反证 |
| `UNKNOWN` | 无法复现、证据不足 | **不**驱动返工，也**不**阻塞合并 |

**安全/合规例外**：对于高风险路径（认证、会话、支付、迁移、密钥、破坏性脚本）上的 finding，若一条 `UNKNOWN` 描述了可能严重的后果，须在合并前升级给决策者，而不是悄悄丢弃。

已裁决的 finding 记录在审查台账（`reviews/ledger.yaml`）中，后续审查永不重提。

## 4. 轮次

- 每个 PR 最多 **3 轮**。第 1 轮审查指定的全量 diff；第 2 轮起只审查新 diff。
- 若第 3 轮仍产生新的 Important finding，该 PR 停止迭代，回到设计层（清单/契约），由决策者裁决。
- Writer 可以用反证反驳 finding；由裁决人裁定。超出已批准清单范围的争议立即升级给决策者。

## 5. 修复与对账

- 修复时在提交信息或 PR 正文中引用 finding ID（`R-YYYYMMDD-NNN`、裁决结论、证据）。
- 全部 TRUE finding 修复完毕后，Writer 在 issue 上贴出**对账单**：一张包含每条 finding 的表（轮次、ID、严重度、位置、大白话描述、裁决结论、修复提交、验证证据）。
- 对账单以**一键验证命令**收尾：一条可复制粘贴的命令，决策者运行后几秒内即可复核对账单中的主张，并附大白话说明预期输出。
- 只有决策者核查过对账单之后，PR 才进入合并门（流程第 8 步）。

## 6. Reviewer 轮换与独立性

- Reviewer 永远不是同一变更的 Writer。优先选用与 Writer 不同的模型/agent。
- 无法执行命令的 Reviewer，其全部输出默认标记为 `UNKNOWN`；具备执行能力的裁决人在升级结论前先复现。
