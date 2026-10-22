English | [简体中文](coding-standards.zh-CN.md)

<!--
  TEMPLATE: docs/specs/coding-standards.md
  Two layers: (1) machine enforcement — tools, config files, CI ownership;
  (2) judgment conventions machines cannot check. A standard that exists only
  in this document will be forgotten; every rule that CAN be a lint rule or a
  CI step MUST be one, with this document explaining why.
-->

# Coding Standards

> **Declaration**: this file is a *living baseline*. It is revised by ordinary PRs and is **not** subject to the frozen-spec rules that govern the other documents in this directory.

## 0. General conventions (all stacks)

1. **Business naming**: names use domain words and match the names in designs, API contracts, and behavior cases. No pinyin/abbreviation soup, no meaningless shortenings.
2. **Comments explain why**, never what. `TODO` comments must carry an issue number.
3. **User-visible copy is centralized** in constants/resource files, never scattered through code.
4. **Secrets and PII never leak**: phone numbers, codes, keys, tokens, and personal data never appear in logs, error messages, or test snapshots. Phone numbers are masked when logged at all.

## 1. Machine enforcement matrix

Fill one row per stack in your project. Critical rules are `error` level — a `warn` keeps CI green and therefore does not exist as a rule.

| Stack | Tools | Config file | CI ownership |
|---|---|---|---|
| <Backend language> | <formatter + linter set> | `<path>` | <CI job> |
| <Client A> | <linter + formatter> | `<path>` | <CI job / "on platform start"> |
| <Web> | <ESLint-equivalent + formatter> | `<path>` | <CI job> |
| <Styles> | <style linter, base set> | `<path>` | <state honestly: wired / not yet wired> |

**Enforcement decisions** (recommended defaults — record yours with a date):

1. **Incremental enforcement**: linters block only new files and changed lines; pre-existing issues are exempt and are cleaned up as files are touched. <Adopted / not adopted, date>
2. **Start from a base rule set**: <per stack, e.g. errcheck/staticcheck/ineffassign/unused equivalents>; style-heavy rule packs stay off until the base set runs clean. <Date>
3. **Default rule sets first for new platforms**, tuned rule by rule against real false positives after the first batch of code lands. <Date>

Tool versions are exact everywhere — full version numbers, always. No `@latest` anywhere in CI: a CI result must depend only on the repository's content.

## 2. Per-language conventions

One subsection per language in your project, 5–8 one-line rules each, anchored to the ecosystem's authoritative guides (<e.g. the language's official style guide, the framework vendor's API design guidelines>). Write rules a reviewer can check mechanically or by a single glance. Example shapes (replace with your stacks):

### 2.1 <Backend language>

- <Error handling: handle once, wrap with context, typed errors for control flow…>
- <Concurrency: every background task has an exit condition; no orphaned workers…>
- <Transactions: template for begin/defer-rollback/commit…>
- <Logging: structured logger only, request-scoped fields incl. request id and isolation id; no debug prints…>

### 2.2 <Client language>

- <No force-unwrapping / unsafe casts of external data…>
- <State management: state lives as close as possible; shared state via the project's chosen mechanism only; no state libraries without approval…>
- <Async UI: lifecycle-bound tasks; UI updates on the main thread…>

### 2.3 <Web stack>

- <Strict typing; `any`-equivalents banned at error level…>
- <Effects/state anti-patterns specific to the framework, with the sanctioned alternative…>
- <Design tokens only: colors/spacing come from the token file; machine-generated design exports are never hand-edited…>
- <Semantics & targets: interactive elements are real controls; touch targets ≥ platform minimum…>

## 3. Review linkage

Serious violations of this document are `failure` under `REVIEW.md` §2. When the same violation class appears a second time, it becomes a lint rule or a gate-script check (see the pipeline's archive step) rather than a recurring review comment.
