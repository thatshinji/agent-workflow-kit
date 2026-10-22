# Lint 起步包

[English](README.md) | 简体中文

为本工具包适配层覆盖的各技术栈准备的开箱即拷 lint 配置。把你所用技术栈的文件夹拷进你的项目，然后针对真实误报逐条调规则——第一天不要整包导入一个巨大的规则集。

## 原则：只拦新增与改动行

这里的每个配置都**只对新文件和改动的行**强制执行规则；存量问题豁免，在文件被改动时顺带清理。

为什么：一条规则只有能让构建失败才算存在。如果一上来就拿 linter 对着存量代码库全量开启，你会得到几百条 finding，团队要么花一周清理，要么——更糟——有人把关键规则降级为 `warn` 让 CI 重新变绿。`warn` 永远不会让 CI 变红，因此作为规则等于不存在。从只拦新增与改动行开始，规则从第一天就有牙齿；每当一个文件被改动，存量债务就缩小一点；而且没有人会被别人留下的旧代码卡住。

配套的两条规则，来自编码规范：

- **关键规则一律 error 级。** 风格偏好可以 warn；正确性规则永远不可以。
- **工具版本在 CI 里钉死。** linter 本身不用 `@latest`、不用浮动版本范围：CI 的结果只能取决于仓库内容，永远不能取决于某个工具昨晚发了什么新版。

## Go — golangci-lint

配置：[`go/.golangci.yml`](go/.golangci.yml)。拷到你的后端根目录。

- **它是什么**：golangci-lint 跑一小组基础 linter——`errcheck`、`gosimple`、`govet`、`ineffassign`、`staticcheck`、`unused`。它们抓的是真 bug（未检查的错误、死代码、无效赋值），不是风格。风格重的规则包（如 revive）先不开，等这组基础集跑干净再说。
- **为什么 error 级**：golangci-lint 的 finding 默认让运行失败；保持这样。一旦你加上 `--issues-exit-code=0` 或做类似降级，规则就不再存在。
- **只拦新增与改动行**：内置支持——`issues.new-from-rev: origin/master` 让 golangci-lint 只报告自 `origin/master` 以来改动的行上的 finding。如果你的默认分支不叫 `master`，改指向你的默认分支。
- **钉死版本**：在 CI 里安装确切版本，例如官方 action 写 `version: v1.64.8`（版本可以自己选，但要写全版本号）。永远不要用 `latest`。

## Web — ESLint（flat config）

配置：[`web/eslint.config.mjs`](web/eslint.config.mjs)。拷到你的 Web 应用根目录。

- **它是什么**：ESLint flat config，组合了 typescript-eslint 的 recommended 集与 eslint-plugin-react-hooks，外加一处刻意的升级：`@typescript-eslint/no-explicit-any` 设为 `error`，而不是 recommended 里的 `warn`。`any` 会在人（或 AI 写手）赶时间的地方悄悄关掉整个类型系统——而 `warn` 对 AI 写手没有约束力，因为构建照样是绿的。
- **只拦新增与改动行**：ESLint 没有「只看改动行」的模式，所以在 CI 里只对 PR 触及的文件跑 lint 来实现：

```bash
git diff --name-only --diff-filter=ACM origin/master...HEAD -- '*.ts' '*.tsx' \
  | xargs -r npx eslint
```

  存量文件只有在有人改动它时才会被 lint——而且只 lint 那一个文件，这是动它应付的公平代价。
- **钉死版本**：把 `eslint`、`typescript-eslint`、`eslint-plugin-react-hooks` 在 `devDependencies` 里钉为确切版本，并提交 lockfile。

## Swift — SwiftLint

配置：[`swift/.swiftlint.yml`](swift/.swiftlint.yml)。拷到你的 App 根目录。

- **它是什么**：SwiftLint 的默认规则集，外加第一天就启用的一条 opt-in 规则：`force_unwrapping`。对外部或可选数据强制解包是经典的崩溃来源，编码规范也明文禁止——所以从一开始就把它启用，而不是等第一份崩溃报告。
- **行长**在 120 时 warn。这是有意设为警告：行长是风格偏好，不是正确性规则，风格偏好无权阻断合并。
- **只拦新增与改动行**：SwiftLint 以整文件为单位 lint。若想要严格的只拦新增与改动行，在 CI 里对 PR 改动的文件运行（与 Web 栈相同的 `git diff --name-only` 技巧）。全仓运行也可以接受，因为默认规则集足够保守。
- **钉死版本、慢慢调**：在 CI 里钉死 SwiftLint 版本（确切的 release，不要用分支）。要有逐条调的预期：从默认起步，某条规则产生误报时，就只调那一条规则并写注释说明原因——永远不要停用整个工具，也永远不要整包照搬一份巨大的共享配置。

## Python — Ruff

配置：[`python/ruff.toml`](python/ruff.toml)。拷到你的项目根目录（或把其中的 `[lint]` 段合并进 `pyproject.toml`）。

- **它是什么**：Ruff 配一组紧凑的规则选择——`E`（pycodestyle 错误）、`F`（pyflakes：未用导入、未定义名字）、`I`（导入排序）、`UP`（pyupgrade：现代语法）、`B`（bugbear：疑似 bug）。行长 100。这些是 bug 与卫生类规则，不是格式意见；格式化是 Ruff 格式化器（`ruff format`）的事，单独配置。
- **为什么 error 级**：Ruff 默认对任何选中的 finding 以非零码退出。保持这样——不要加 `--exit-zero`。
- **只拦新增与改动行**：Ruff 没有内置的「只看新增行」模式，所以在 CI 里把它限定到 PR 改动的文件：

```bash
git diff --name-only --diff-filter=ACM origin/master...HEAD -- '*.py' \
  | xargs -r ruff check
```

- **钉死版本**：在 CI 安装 Ruff 的地方钉确切版本（例如 `pip install ruff==0.9.0`——版本自己选，写全版本号）。

## 文件清单

| 文件 | 技术栈 | 拷到 |
|---|---|---|
| `go/.golangci.yml` | Go (golangci-lint) | 后端项目根目录 |
| `web/eslint.config.mjs` | Web (ESLint + TypeScript + React) | Web 应用根目录 |
| `swift/.swiftlint.yml` | Swift (SwiftLint) | App 项目根目录 |
| `python/ruff.toml` | Python (Ruff) | 项目根目录 |
