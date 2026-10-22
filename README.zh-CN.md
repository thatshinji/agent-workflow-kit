[English](README.md) | 简体中文

# agent-workflow-kit

> 一套规范先行、测试先行的开发工作流，面向与多个 AI 编程 agent 协作交付软件的独立开发者和小团队。

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![CI](https://github.com/thatshinji/agent-workflow-kit/actions/workflows/ci.yml/badge.svg)

大多数 AI 编程工作流都以可预见的方式失效：agent 写的测试只是照着自己的实现复刻一遍（于是测试什么都证明不了），审查者提出的 finding 没有可复现的证据（于是修复来回拉锯），项目约定只活在聊天记录里（一周之内就被忘光）。这套工具包是从一个每天都在真实运行它的生产项目中提炼出的完整、可移植的工作流。它**与技术栈无关**：无论 iOS、Android、Web，还是 Go、Java、Node.js、Python 或任何其他语言的服务端，机制都一样——变的只有工具映射。

## 工作流一览

- **三个角色，一个合并键。** 一位人类决策者审批意图、契约和验收清单，并且是唯一能合并的人。*Writer* agent 负责起草和实现。*Reviewer* agent（最好是不同的模型）独立编写测试，并按证据做审查。
- **每个功能走八步流程。** 意图与契约 → 行为清单与计划 → 验收门 → 独立测试并冻结 → 实现与自证 → 基于证据的审查 → 经裁决的修复循环 → 合并与归档。
- **以行为层用例库为单一事实源。** 行为用例按平台中立的业务行为书写（Given/When/Then，不用实现词），一个功能一个文件，并有一张覆盖全部客户端平台的覆盖矩阵。后续平台以压缩过的「Delta 模式」消费同一份用例库。
- **契约先于代码。** 服务端/API 契约按一份八组契约清单起草；产品决策标注 ★，只能由人来拍板。
- **基于证据的审查。** 每条 finding 必须给出文件:行号、复现方式（或规范出处）、期望与实际，外加一条如何推翻它的提示。无法验证的 finding 不驱动返工。
- **机器负责执行，文档负责解释。** 凡是机器能判定的，都落成 lint 规则或 CI 门禁。关键规则必须是 `error`，绝不用 `warn`——一个让 CI 照样变绿的警告不算规则。
- **一切都要归档。** 隐藏验收场景、审查教训和覆盖状态在每次合并后都写回用例库，让每个错误只付一次学费。

完整设计文档：[中文](docs/blueprint.md) / [English](docs/blueprint.en.md)。

## 工具包包含什么

```text
docs/blueprint*.md  The full design (Chinese + English editions): 12 core
                    mechanisms, 5 adoption phases, per-stack adaptation
                    tables, project "slots", anti-patterns
templates/          Blank templates for all 11 workflow documents — AGENTS.md,
                    REVIEW.md, review protocol, TDD spec, contract checklist,
                    coding standards, project-management set, platform playbook,
                    review ledger, and the test-case library (TEMPLATE + INDEX)
                    — plus lint-starters/ with per-stack lint configs
scripts/            The one-command installer (install.py: scaffolds the whole
                    kit into your repository, never overwrites existing files)
                    and the TDD compliance gate (zero-dependency Python):
                    production changes must ship with paired tests containing
                    negative assertions. Both ship with their own tests
examples/           Three worked examples: "join by invite code" (the full
                    pipeline, runnable code, real red/green evidence), a
                    Delta-mode second platform, and a hotfix lane
```

如果你想在读理论之前先看这套工作流的实际产物，从[完整示例](examples/invite-code/)开始。

## 开始使用

**动手路径**：照着 [Quickstart](docs/quickstart.md)（[简体中文](docs/quickstart.zh-CN.md)）走——一份 30 分钟的上手引导：拷模板、填八个槽位、接上门禁、跑通你的第一个功能。概念路径：

1. 读[蓝图](docs/blueprint.md)——它定义了 12 个核心机制、五个落地阶段和各技术栈的适配表。
2. 把脚手架铺进你的仓库——在仓库根目录运行[安装脚本](scripts/)（或手动复制[模板](templates/)，模板目录的 README 写了每个文件的目标位置），并填好八个项目「槽位」（数据隔离维度、项目不变量、failure 定义、高风险路径、★ 决策、强制失败分支、设计源、风险分级）。
3. 把[门禁脚本](scripts/)接进 CI，然后先拿一个小而真实的功能完整跑一遍流程，再扩大使用。

## 状态

**v0.3.0**——路线图完结：蓝图中英双语，Delta 模式与 hotfix 两个走通示例与邀请码示例会合，各技术栈 lint 起步包就位，一键安装脚本可把整套脚手架铺进你的仓库。（此前：v0.2.0 全套中文文档；v0.1.0 第一个公开发布版。）

本仓库在适用处遵循自己的工作流：它的 CI 在每次推送和每个 PR 时运行工具包的测试套件，PR 也使用工具包的约定（`Refs #`、风险自评、证据）。

## 参与贡献

欢迎贡献——见 [CONTRIBUTING.md](CONTRIBUTING.md)。非琐碎的改动请先开 issue 说明意图与非目标；这正是本工具包所教授的工作流。

## 许可证

MIT © 2026 Shinji
