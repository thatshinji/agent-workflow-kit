[English](REVIEW.md) | 简体中文

<!--
  模板：REVIEW.md —— 复制到你的仓库根目录，填好每一个 <slot>。
  本文件告诉每个 Reviewer（人或 AI）：这里什么算 failure、一条 finding
  需要什么证据、评审到哪里为止。保持短、可执行；一条规则若不能机械地
  套用，就改写到能机械套用为止。
  结构与证据规则是这套工具包的机制本体 —— 原样保留。
  failure 定义表是你的项目槽位：逐行改写成你自己的。
-->

# REVIEW.md — Reviewer 指南

> 与 `AGENTS.md` 配合阅读。完整流程（裁决（adjudication）、轮次、对账）见 `docs/project-management/review-protocol.md`。

## 1. 这个仓库是什么

- <一两行：谁在建这个项目（例如一名决策者 + 多个 AI agent）、当前阶段、技术栈速览。>
- 评审的目的是**发现真问题、减少返工** —— 不是罗列样式层面的吹毛求疵，也不是重写作者的代码。
- **判定优先级**（来源冲突时按此链条裁定）：`AGENTS.md` 铁律 > 已冻结（frozen）的规格与编码规范 > 本 issue 经决策者批准的行为清单 > TDD 规格 > 本文件 > 一般工程常识。

## 2. 什么算 failure（failure，按目录定义）

逐行改写为你项目的版本。四条通用行（契约漂移、日志里出现密钥、不可回滚的迁移、文档把计划中的工作写成已完成）在每个项目里都应以某种形式保留。

| 路径 | “failure”长什么样 |
|---|---|
| `<server/>` | 构建/测试失败；鉴权绕过（缺 `<isolation-id>` 检查）；事务非原子；迁移不可回滚；密钥或个人敏感信息写进日志；错误信封格式不一致；严重违反编码规范；生产代码变更未配测试，或新测试只覆盖快乐路径 |
| `<server/migrations/>` | 有 up 无 down；修改迁移历史；`down` 静默丢数据 |
| `<apps/>` | API 路径或 DTO 偏离契约源；页面在设计源之外构建，或未登记进设计 manifest；401/403/429 状态未处理；严重违反编码规范；核心逻辑变更未配测试，或没有反向用例 |
| `<docs/specs/>` | 与已冻结基线矛盾；把提案写得像已生效；字段与迁移不一致 |
| `<docs/>` | 链接失效；把计划中的工作写成已实现；结论没有证据（evidence）或日期 |
| `<.github/>` | 绕过门禁；自动关单关键词；破坏 CI/模板语义 |
| `<scripts/>` | 破坏性操作无确认；环境名写死；吞掉错误；脚本变更未配测试 |

## 3. 严重度（severity）

| 标签 | 含义 | 处理 |
|---|---|---|
| **Important** | 行为错误、安全问题、数据风险、绕过契约/CI | 必须裁决；若为 `TRUE` 必须修复 |
| **Nit** | 样式、命名、清理；不改变行为 | 每个 PR 至多 3 条；永不阻塞合并 |
| **Pre-existing** | 本 PR 之前就存在 | 标出来；不是作者的债；另开 issue |

## 4. 证据要求

- 每条 finding 必须给出：`file:line` + 一个可执行的复现步骤（repro）（或可引用的 `spec_ref`）+ `expected / actual`。
- 复现不出来，就标 `UNKNOWN` —— 不许写成 bug。
- 每条 finding 必须附 `refute_hint`：什么结果能证明你错了。
- **不接受**：“可能 / 也许 / 最佳实践 / 上线会炸”—— 没有证据的说法。
- 只审指定 commit SHA 的 diff。第 2 轮起只审新 diff。
- 无法执行命令的 Reviewer，默认产出 `UNKNOWN`；裁决人先复现，再谈升级。

## 5. 场景与测试职责

- **实现之前**：Writer 提交行为清单后，Reviewer 依据清单独立写测试（或对 Writer 的测试做对抗性审计），只看设计与清单 —— 绝不参考 Writer 的实现思路。测试必须先跑红，并把失败输出留作证据；跑不红的测试无效，退回。
- **测试冻结**：已批准、已冻结的测试，Writer 不得修改。未经重新批准改测试，一经发现即 Important finding。
- **隐藏场景**（hidden scenarios）：Reviewer（或决策者）保管 2–3 条隐藏场景，只在最后一轮评审时运行，修复轮中不披露。隐藏场景失败即 Important。最后一轮通过后，Reviewer 产出隐藏场景的行为层底稿，Writer 在合并（merge）时逐字归档、解封（unseal）入用例库（test-case library）。
- **覆盖核对**：评审第一步永远是已批准的清单 —— 每条用例都要有对应的、通过的测试；有用例无测试，视为未实现。清单之外的行为 finding 可以按 §2 提出，但必须标 “outside checklist”。
- **可映射性核对**：新增/变更的行为用例要对照禁用词表核查（实现词，例如 click/tap/swipe、toast、modal、组件名、路由、像素值）。预期结果必须是任何平台都能实现的业务事实。
- **用例库同步核对**：若本 PR 改动了已归档功能的行为，diff 里必须包含 `docs/test-cases/` 的对应更新。缺同步即 Important。
- **桩行为**：标为 “real behavior (activates on integration)” 的用例，本轮不构成 finding 的依据。

## 6. 跳过路径

- 生成代码：<例如 `<generated-dir/>` —— 改源定义>
- 锁文件、二进制文件、vendored 资源
- 已在评审台账（`docs/project-management/reviews/ledger.yaml`）里裁决过的 finding —— 不许重复提出
- 纯格式化（交给格式化工具/linter）

## 7. 输出格式

以一行摘要开头：

```text
<N> findings: Important <a> / Nit <b> / Pre-existing <c>
```

再加一行覆盖情况：

```text
Scenario coverage: approved <N>, passing <M>; hidden <K>, passing <J>.
```

若没有阻塞性 finding：

```text
No blocking findings. Optional note: <没有证据的风险写在这里>
```

每条 finding 使用评审协议附录的 YAML 格式，Important 在前。

## 8. 评审边界

- 你只对这份 diff 及其直接影响负责。不许要求重构或未来功能。
- 最多 3 轮。超过 3 轮，作者回到设计层，而不是继续逐条迭代 finding。
- 同一类问题一次报全 —— 不许一轮挤一条。
- 安全敏感与高风险路径（<认证、会话、迁移、CI、密钥、冻结契约、破坏性脚本 —— 按你的项目调整>）单独过一遍安全审查，并经决策者确认。

## 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | <YYYY-MM-DD> | 初版 |
