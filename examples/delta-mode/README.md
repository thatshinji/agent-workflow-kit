English | [简体中文](README.zh-CN.md)

# Example: Delta mode — "Join by invite code" on a second platform

The invite-code feature from [../invite-code/](../invite-code/) ships in the project's mobile app, six weeks after the web launch. The server contract and the behavior library already exist and are approved — so this walkthrough shows what the pipeline looks like when it **compresses**: only the platform differences are written, gated, and reviewed; everything inherited is consumed as-is.

**The point of Delta mode**: behavior is decided once, in the library. A new platform states how it *differs*, maps its tests 1:1 to the archived case IDs, and updates its own column of the coverage matrix. Steps 1–4 of the full pipeline are not re-run, the contract is not re-drafted, and prior adjudications are not re-opened.

**The cast**: Decision-maker (human) · Writer (agent A) · Reviewer (agent B, different model) — the same cast; only the scope shrinks.

## The walkthrough

| Delta step | Artifact | What to notice |
|---|---|---|
| 1′. Delta intent | [01-delta-intent.md](01-delta-intent.md) | Two lists only: what is inherited (not re-decided) and what differs on this platform. Exactly one new ★ decision appears — everything else was settled in issue #101. |
| 2′–3′. Case mapping & delta gate | [02-case-mapping.md](02-case-mapping.md) | Every archived case gets a disposition — reused 1:1, adapted, or server-only — plus the few genuinely new platform cases. The approval gate verifies *this table and the new cases only*. |
| 4′–7′. Tests, implementation, review | (summarized in 02 & 03) | Tests are implemented 1:1 against case IDs and run red first, as usual. Review scopes to the delta, so one round suffices. |
| 8′. Archive | [03-archive-state.md](03-archive-state.md) | The coverage matrix gains the Mobile column's states; the lesson is written back into the feature file. The library — not this PR — remains the source of truth. |

## Verify it yourself

There is no new server code to run: the endpoint and its tests are the ones from [../invite-code/04-implementation/](../invite-code/04-implementation/). The mobile work is verified against the mapping in [02-case-mapping.md](02-case-mapping.md) — each row names the case ID its test carries.
