# Example: "Join by invite code" — one feature through all eight steps

A fictional but realistic mini-feature, walked end-to-end through the pipeline from `templates/AGENTS.md`. Every step's artifact is a real file in this folder, so you can see exactly what each stage produces and consumes. The code is small Python (stdlib only) — the workflow, not the stack, is the point.

**The feature**: a workspace owner shares a 6-character invite code; anyone with the code joins the workspace. Codes expire, have limited uses, and can be regenerated. Guessing codes must be rate-limited, and errors must never leak which workspace a code belongs to.

**The cast**: Decision-maker (human) · Writer (agent A) · Reviewer (agent B, different model).

## The walkthrough

| Step | Artifact | What to notice |
|---|---|---|
| 1. Intent & contract | [01-issue-intent.md](01-issue-intent.md) | The writer drafts; the decision-maker only approves. ★ items are product decisions. Non-goals and unchanged behaviors are stated *before* any code exists. |
| 2. Behavior checklist & plan | [02-behavior-cases.md](02-behavior-cases.md) | Cases are platform-neutral business facts — no "tap", no "toast", no API paths. Every case has a stable ID. This exact file later becomes the archived library entry. |
| 3. Approval gate | (inside 01 & 02) | The decision-maker approves the checklist and the ★ decisions. Nothing below this line may start before that approval. |
| 4. Independent tests, frozen | [04-implementation/test_invite.py](04-implementation/test_invite.py) + [03-red-evidence.md](03-red-evidence.md) | The reviewer writes tests from the checklist alone, runs them against a stub, and keeps the failing output as evidence. 2 scenarios stay hidden until the final round. |
| 5. Implementation & self-verification | [04-implementation/invite.py](04-implementation/invite.py) | Minimal implementation; test names map 1:1 to case IDs. The compliance gate (`scripts/`) passes because tests and implementation change together. |
| 6–7. Review & adjudicated fixes | [05-review-round.md](05-review-round.md) | Findings carry repro + expected/actual + refute hints. One is TRUE, one is refuted (FALSE), one Nit. The round ends with a reconciliation statement and a one-shot verification command. |
| 8. Merge & archive | [06-archive-state.md](06-archive-state.md) | Hidden scenarios are unsealed into the case file, lessons are distilled, and the coverage matrix gains its row. The library is now the source of truth for the *next* platform. |

## Verify it yourself

Everything in step 4–5 is runnable:

```bash
cd examples/invite-code/04-implementation
python3 -m unittest test_invite -v        # 10 tests: 8 approved cases + 2 unsealed hidden scenarios
```

To reproduce the step-4 red run, temporarily replace `invite.py` with the preserved stub (`invite_stub.py.txt`) and run the same command — all 10 tests fail with `NotImplementedError`, exactly as recorded in [03-red-evidence.md](03-red-evidence.md).
