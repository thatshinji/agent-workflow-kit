English | [简体中文](TEMPLATE.zh-CN.md)

<!--
  TEMPLATE: one file per feature, stored in docs/test-cases/<domain>/<feature>.md
  This file is the living behavior contract of a feature. Implementation PRs
  update it in the same change (out-of-sync = review failure). Write cases at
  the behavior layer only: business facts that ANY platform can implement and
  test against. Never write implementation words (see the forbidden list in §2).
-->

# <Feature Name> — Behavior Test Cases

> Feature: <domain>/<feature> | Status: <platforms, e.g. Web ✅ Implemented | iOS ❌ Not implemented> | Last updated: <YYYY-MM-DD>
> <Optional: design source — screens/flows this feature's behavior comes from.>

## 1. Intent

### Intent
<Who this feature serves and what problem it solves, in 2–4 plain sentences.>

### Unchanged behaviors
<Behaviors this feature deliberately does NOT change, listed one per line. These guard against regressions disguised as improvements.>

### Non-goals
<What this feature explicitly does not do, one per line. Anything not listed here and not covered by a case is undecided — flag it, don't invent it.>

### Change history
- <YYYY-MM-DD>: <what changed in the behavior, and which PR/decision changed it. One line per change; newest last.>

## 2. Behavior cases

Case ID format: `<PREFIX>-<NNN>` (prefix is per-feature, e.g. `AUTH-001`). Each case is one row/set in this shape:

- **<PREFIX>-001 <short business name>**
  - Given <precondition, stated as business facts>
  - When <a business action or event — never a UI gesture>
  - Then <observable business outcome>

Writing rules (checked in review — violating them fails the mappability check):
- ✅ Allowed words: submit, confirm, receive, display (of information content), expire, reject…
- ❌ Forbidden words (implementation layer): click, tap, swipe, long-press, toast, modal, dialog, spinner, grayed-out, button, component names, screen routes, API paths, pixel values, storage details — anything only one platform or one implementation can say.
- Expected results must be business facts (state changes, data outcomes, who can see what), never presentation details.
- Three legal exceptions: ① pure display cases — state the information content as a business expectation and append "(layout per design source)"; ② unobservable internal behavior — do not write it at all; ③ genuinely single-platform behavior — move it to §3 Platform differences.
- Interception/rejection cases must assert the negative explicitly (e.g. "…and no <record> is created", "the API is not called") — a case that only asserts the happy-path message can pass against a broken implementation.
- Every case cites its origin in the section notes where useful: design screen / contract clause / hard rule.

<Add cases here. Replace this line. Keep IDs stable forever: never renumber; superseded cases are marked, not deleted silently — record the change in §1 Change history.>

## 3. Platform differences

<Behaviors where platforms legitimately differ (system components, permissions, platform conventions), one entry per difference:>

- <PREFIX>-D1: <what differs, per platform, and why it is a platform fact rather than a behavior difference>

## 4. Review lessons

<One line per lesson distilled from reviews of this feature: pitfall + remedy. Newest last. This section is why the same mistake is never paid for twice.>

- <YYYY-MM-DD> <lesson> (from <PR or finding ID>)
