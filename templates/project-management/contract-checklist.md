<!--
  TEMPLATE: docs/project-management/contract-checklist.md
  The checklist a writer walks, item by item, when drafting a backend/API
  contract in pipeline step 1. Adapt the ★ items and the isolation dimension
  to your project; keep the "three-way marking" rule.
-->

# Contract Draft Checklist

> Purpose: the item-by-item checklist for contract drafting (pipeline step 1). For every item the writer marks exactly one of: `decided` / `follows standard` (cite the source) / `open question`. Items flagged ★ are **product decisions** — the writer never decides them; they are listed as open questions for the decision-maker. The reviewer checks the draft for blanks first: any unmarked item sends the draft back.

## 1. Interface

- Endpoint list (method + path + purpose); request parameters and validation rules (required, type, range, length caps)
- Response shapes and status codes; business error-code table (reuse the project's single error envelope)
- List endpoints: pagination, default ordering, page-size cap
- ★ Idempotency: can a duplicate submission or network retry double-create or double-charge? (Mandatory to answer for creation and payment endpoints.)

## 2. Data model

- Tables and fields: types, defaults, nullability; unique, foreign-key, and CHECK constraints
- Indexes designed from real query patterns (who queries, by which fields)
- Migrations in up/down pairs; backfill and compatibility for existing data
- Soft-delete convention; audit fields (created_at / updated_at / actor)
- Data growth estimate for one year; cleanup/archival strategy

## 3. Business rules

- State machine: states, legal transitions, who triggers each
- Invariants (rules that must always hold — write them as testable sentences)
- ★ Calculation rules: <e.g. money in integer minor units; statistics computed deterministically in code, never by an LLM>
- Concurrency conflicts: strategy when the same record is edited simultaneously (optimistic lock / last-write-wins / explicit conflict)
- Transaction boundaries: steps that must succeed or fail together

## 4. Authorization & security

- ★ Authorization matrix: for each endpoint — who can read, who can write, who can delete (per role)
- Data isolation: `<isolation-id>` is taken from the authenticated session only, never from client input; state how each query verifies ownership
- Authorization test points: list every "change the ID, reach someone else's data" spot (these feed the behavior checklist's mandatory security cases directly)
- Sensitive data: secrets/codes/tokens stored hashed only; log redaction rules apply
- Abuse limits: rate caps for code sending, login attempts, invite/token guessing
- ★ Data retention & true deletion: what happens to the data on account closure / workspace dissolution

## 5. External dependencies & async work

- Every third-party dependency (messaging, identity providers, push, storage…): real integration this round or a stub — ★ the stub's scope is a product decision
- Failure strategy per dependency: timeouts, retry counts, retry side effects (e.g. duplicate messages), what the user sees on total failure
- Async & scheduled work: triggers, owners, failure compensation (reminders, expirations, periodic generation…)

## 6. Time & boundaries

- Storage in UTC, display in the user's/workspace's timezone; definitions of "today / this week"
- Boundary values: null, overlong input, 0, negatives, duplicate names
- ★ Deletion semantics: when an entity is deleted, what happens to its related data (keep / transfer / anonymize)

## 7. Client coordination

- Field nullability and defaults (what the client does with a null)
- Error-code → user-message mapping (server provides codes; clients translate to plain language)
- Change impact: which clients must be updated when a live endpoint changes

## 8. Acceptance hand-off

- Every contract behavior is written as a testable assertion and feeds the behavior checklist (pipeline step 2)
- Stub behaviors specify their exact return values; the checklist's "stub behavior" group is written from this section
