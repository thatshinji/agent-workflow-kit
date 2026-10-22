English | [简体中文](README.zh-CN.md)

# Example: The hotfix lane — a production bug, compressed but not skipped

The eight-step pipeline in `templates/AGENTS.md` is sized for features. A production incident cannot wait for the full cycle — but "urgent" is exactly when teams skip the steps that would have caught the *next* incident. The hotfix lane is the pipeline's answer: **the same steps, compressed where compression is safe, at full strength where it is not.**

**What it is**: one regression test written red first, one full review round with adjudication, and the same archive write-back as any feature — wrapped around a deliberately tiny fix.

**What it is not**: a skip lane. Nothing is waived. The intent, the gate, the checklist, and the review all still happen; they shrink to fit the incident instead of disappearing.

**The incident**: in the [invite-code feature](../invite-code/README.md) (issue #101, already shipped), expired invite codes return `INVITE_NOT_FOUND` instead of `INVITE_EXPIRED`. Users cannot tell "this code expired" from "this code never existed" — and neither can support. This walkthrough fixes that bug (issue #137) without touching a single business rule.

**The cast**: unchanged — Decision-maker (human) · Writer (agent A) · Reviewer (agent B, different model).

## When the hotfix lane may be used

All three conditions must hold; if any fails, the work goes through the full pipeline:

1. **The production impact is real and current** — users are hitting the bug now, not "could someday."
2. **The blast radius is small** — the fix is confined to one known location; no business rules, data model, or contract decisions change.
3. **The decision-maker approves the fast lane** — explicitly, in the issue, before work starts.

## The walkthrough

| Artifact | What to notice |
|---|---|
| [01-hotfix-intent.md](01-hotfix-intent.md) | The intent is five lines — an incident summary, not a feature brief. Beside it, the kept-vs-compressed table states openly which steps shrink and which never do. |
| [02-red-evidence.md](02-red-evidence.md) | The regression test HF-001 is sourced from an existing library case (INV-002) and still runs red first. Compression never touches this step. |
| [03-review-and-archive.md](03-review-and-archive.md) | One complete review round with adjudication, a reconciliation statement, and the archive: the regression case is promoted into the library as INV-009, and the lesson becomes a standing contract-checklist item. |

## The one-sentence version

A hotfix earns its speed by shrinking the *paperwork around* the fix — never by shrinking the evidence, the review, or the write-back.
