[English](README.md) | 简体中文

# 模板

agent-workflow-kit 各文档的空白模板。每份模板只包含结构、填写指引（位于文件顶部的 HTML 注释）和 `<slot>` 占位符——从不预填某个具体项目的内容。

每份模板都有英文版与中文版，内容一一对应，按需取用。

## 每份模板的去向

| 模板（英文版） | 中文版 | 复制到 | 说明 |
|---|---|---|---|
| [`AGENTS.md`](AGENTS.md) | [`AGENTS.zh-CN.md`](AGENTS.zh-CN.md) | 仓库根目录 | Agent 宪法：铁律、目录归属、八步流程、DoD |
| [`REVIEW.md`](REVIEW.md) | [`REVIEW.zh-CN.md`](REVIEW.zh-CN.md) | 仓库根目录 | Reviewer 指南：failure 定义、证据规则、严重度、边界 |
| [`test-cases/TEMPLATE.md`](test-cases/TEMPLATE.md) | [`test-cases/TEMPLATE.zh-CN.md`](test-cases/TEMPLATE.zh-CN.md) | `docs/test-cases/TEMPLATE.md` | 单个功能的行为用例文件骨架 |
| [`test-cases/INDEX.md`](test-cases/INDEX.md) | [`test-cases/INDEX.zh-CN.md`](test-cases/INDEX.zh-CN.md) | `docs/test-cases/INDEX.md` | 覆盖矩阵与登记原则 |
| [`project-management/README.md`](project-management/README.md) | [`project-management/README.zh-CN.md`](project-management/README.zh-CN.md) | `docs/project-management/README.md` | 任务池、以退出条件定义的里程碑、看板纪律、角色、节奏 |
| [`project-management/review-protocol.md`](project-management/review-protocol.md) | [`project-management/review-protocol.zh-CN.md`](project-management/review-protocol.zh-CN.md) | `docs/project-management/review-protocol.md` | finding 格式、三态裁决、轮次、对账 |
| [`project-management/tdd-workflow-spec.md`](project-management/tdd-workflow-spec.md) | [`project-management/tdd-workflow-spec.zh-CN.md`](project-management/tdd-workflow-spec.zh-CN.md) | `docs/project-management/tdd-workflow-spec.md` | 四步 TDD 循环与合规门禁的设计 |
| [`project-management/contract-checklist.md`](project-management/contract-checklist.md) | [`project-management/contract-checklist.zh-CN.md`](project-management/contract-checklist.zh-CN.md) | `docs/project-management/contract-checklist.md` | 八部分组成的契约起草清单，含 ★ 产品决策 |
| [`project-management/platform-playbook.md`](project-management/platform-playbook.md) | [`project-management/platform-playbook.zh-CN.md`](project-management/platform-playbook.zh-CN.md) | `docs/project-management/<platform>-playbook.md` | 按平台的 Delta 模式手册；每个平台一份 |
| [`project-management/reviews-ledger.yaml`](project-management/reviews-ledger.yaml) | [`project-management/reviews-ledger.zh-CN.yaml`](project-management/reviews-ledger.zh-CN.yaml) | `docs/project-management/reviews-ledger.yaml` | 已裁决 finding 的台账；已裁决的 finding 不得重复提出 |
| [`specs/coding-standards.md`](specs/coding-standards.md) | [`specs/coding-standards.zh-CN.md`](specs/coding-standards.zh-CN.md) | `docs/tech-specs/coding-standards.md` | 活基线：机器强制矩阵 + 判断类约定 |

## lint 起步包

[lint-starters/](lint-starters/) 里是各技术栈的起步配置（Go、Web/TypeScript、Swift、Python），落实编码规范的三项决策——只拦新增与改动行、关键规则 error 级、工具版本在 CI 里写明完整版本号。`scripts/install.py --stack <名称>` 可把对应配置直接铺到你的仓库根目录。

## 新项目的填写顺序

1. 先填八个项目槽位（蓝图 §5）：数据隔离维度、项目铁律、failure 定义、高风险路径、★ 契约决策、强制失败分支、设计来源、风险分级。
2. 然后实例化 `AGENTS.md` 和 `REVIEW.md`——它们引用了大多数其他文档。
3. 在第一个功能开工前，先建好 `docs/test-cases/` 并放入 `TEMPLATE.md` 与 `INDEX.md`；第一个功能的用例文件在它的流程第 2 步中写成。


