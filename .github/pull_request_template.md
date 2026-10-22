## Summary / 摘要

<!-- What changed, in plain language. -->
<!-- 用通俗的语言说明改了什么。 -->

Refs #<!-- issue number — never Fixes/Closes; issues are closed manually after verification -->
<!-- 填写关联的 issue 编号——切勿写 Fixes/Closes；issue 要在核实后手动关闭。 -->

## Risk self-assessment / 风险自评

<!-- Pick one; it decides how closely the decision-maker reads before merging. -->
<!-- 三选一；它决定决策者在合并前会看得多仔细。 -->

- [ ] **Low** — docs, copy, template wording, no behavior change
- [ ] **Medium** — ordinary behavior change, covered by tests
- [ ] **High** — auth, data, CI/gates, contracts, or destructive operations

## Verification evidence / 验证证据

<!-- Commands actually run and their results. Claims without output are not evidence. -->
<!-- 实际运行过的命令及其结果。没有输出的主张不算证据。 -->

```text
...
```

## Review findings addressed (if any) / 已处理的评审发现（如有）

<!-- One line per finding: R-YYYYMMDD-NNN — verdict (TRUE/FALSE/UNKNOWN) — how it was fixed or refuted. -->
<!-- 每条发现写一行：R-YYYYMMDD-NNN —— 裁决（TRUE/FALSE/UNKNOWN）—— 是如何修复或驳斥的。 -->

## Checklist / 检查清单

- [ ] Production changes ship with paired tests, including negative/boundary cases
- [ ] Behavior changes are synced into the relevant docs/templates in this same PR
- [ ] No secrets, tokens, or personal data in the diff
