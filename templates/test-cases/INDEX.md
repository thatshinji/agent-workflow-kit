English | [简体中文](INDEX.zh-CN.md)

<!--
  TEMPLATE: docs/test-cases/INDEX.md — the coverage ledger of the behavior
  test-case library. It records facts, not plans: a feature gets a row only
  when its case file is archived. Adapt the platform columns to your project.
-->

# Behavior Test-Case Library — Index & Coverage Matrix

The library in this directory is the single source of truth for feature behavior across platforms. One file per feature, organized by business domain. New platforms consume the same files in Delta mode (see the platform playbook).

**Registration principles**

1. **Domain organization**: files live in per-domain subdirectories (e.g. `auth/`, `billing/`), never as a flat pile.
2. **Register only what is archived**: a feature appears here only after its case file exists. The matrix grows row by row with real work — never pre-fill future features.
3. **Lessons live with the feature**: review lessons are kept in each feature file's "Review lessons" section; there is no central lessons file.
4. **Honest states**: use the legend exactly; a partially-covered feature is ⚠️, not ✅.

**Legend**: ✅ Implemented & covered | ⚠️ Partially covered (gaps noted in the feature file) | ❌ Not implemented | — Not applicable on this platform

## Coverage matrix

| Feature | Case file | <Platform A> | <Platform B> | <Platform C> | Notes |
|---|---|---|---|---|---|
| <example row — delete when the first real feature lands> | `<domain>/<feature>.md` | ✅ | ❌ | — | |
