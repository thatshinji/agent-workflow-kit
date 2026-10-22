[English](README.md) | 简体中文

# Scripts（脚本）

与技术栈无关的工作流门禁脚本。本目录中的一切均为零依赖，可以安全地复制到任何仓库。

## install.py

一键安装脚本。在**你自己的**仓库根目录运行它，把模板、门禁脚本及其配置一键铺到位。甚至不必先 clone kit——脚本会自举（装的是 v0.3.2 版；`--kit-version <标签>` 或 `--kit-version latest` 可换版本；它会把 kit 下载到临时目录再从那里安装）：

```bash
curl -fsSL https://raw.githubusercontent.com/thatshinji/agent-workflow-kit/v0.3.2/scripts/install.py | python3 -
```

或者在已经 clone 好 kit 的情况下：

```bash
python3 /path/to/agent-workflow-kit/scripts/install.py                    # 英文模板
python3 /path/to/agent-workflow-kit/scripts/install.py --lang zh-CN       # 中文模板（落地时用无后缀名）
python3 /path/to/agent-workflow-kit/scripts/install.py --stack go --stack web   # 同时把 lint 起步配置铺到根目录
python3 /path/to/agent-workflow-kit/scripts/install.py --dry-run          # 只打印计划，不写任何文件
```

安全语义：已存在的文件一律**跳过并报告，绝不静默覆盖**（`--force` 才覆盖，同样逐项报告）。写入前先检查全部源文件；缺任何一个就以退出码 2 中止并点名缺失文件。结尾摘要会打印装了什么、跳过了什么，以及下一步三行。

## check_tdd_compliance.py

出自 TDD 工作流规范（§4）的 TDD 合规门禁。它检查当前变更集（与基准 ref 的 `git diff`，外加已暂存、未暂存和未跟踪的文件），并强制执行：

- **配对** — 在已配置的区域内改动的生产文件，必须伴随*同一区域内*的测试文件改动。
- **反向断言** — 改动的测试文件必须新增至少一条反向/边界断言（按关键词匹配：HTTP 错误状态码、`invalid`、`rejects`、`assertThrows` 等）。
- **直接放行** — 仅涉及文档/配置的改动自动通过；门禁永远不评判存量代码。

### 用法

```bash
# 1. Configure: copy the example and adapt the globs to your layout
cp scripts/tdd-check.config.example.json tdd-check.config.json

# 2. Run locally (defaults: config ./tdd-check.config.json, base origin/master)
python3 scripts/check_tdd_compliance.py
python3 scripts/check_tdd_compliance.py --base HEAD~1

# Exit codes: 0 PASS · 1 FAIL (violations printed) · 2 config/usage error
```

### 把它接进你的一键门禁

Makefile（加到你的 lint 目标里，让 `make pr-check` 包含它）：

```make
tdd-check:
	python3 scripts/check_tdd_compliance.py --base origin/master
```

GitHub Actions（放在运行你 lint 套件的 job 里）：

```yaml
- name: TDD compliance
  run: python3 scripts/check_tdd_compliance.py --base origin/${{ github.base_ref }}
```

注意，checkout 需要为基准 ref 拉取历史记录（在 `actions/checkout` 上设置 `fetch-depth: 0`）。

### 测试

按本工具包「每个脚本都要有测试」的规矩，这个检查器自带测试，包括非法输入用例：

```bash
cd scripts && python3 -m unittest test_check_tdd_compliance -v
```

### 诚实的局限

关键词匹配只是底线，不是证明：它只保证*存在*反向断言文本，并不保证断言有意义。断言有没有意义是 reviewer 的工作（REVIEW.md §5）——这道门禁的存在意义，是让 reviewer 永远不需要为「根本没有反向用例」浪费一轮评审。
