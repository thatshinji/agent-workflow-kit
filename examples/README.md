English | [简体中文](README.zh-CN.md)

# Examples

Worked examples of the workflow, each small enough to read in one sitting and complete enough to copy from.

| Example | What it shows |
|---|---|
| [invite-code/](invite-code/) | One feature ("join a workspace by invite code") through all eight pipeline steps: intent & contract → behavior checklist → approval gate → independent tests with real red/green evidence → review with adjudication → archive with unsealed hidden scenarios |
| [delta-mode/](delta-mode/) | The same feature lands on a second platform (mobile): intent shrinks to platform differences only, every existing case is mapped (reused / adapted / server-only), three platform cases are added — behavior is decided once, not per platform |
| [hotfix/](hotfix/) | A production bug (expired codes reported as not-found) through the compressed lane: what compresses (intent, gate, case list) and what never does (red-first regression, review with adjudication, archive back into the case library) |

Together the three cover the workflow's three tempos: a feature's full pipeline, a second platform's delta, and an urgent fix.
