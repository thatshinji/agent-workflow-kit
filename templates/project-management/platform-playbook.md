English | [简体中文](platform-playbook.zh-CN.md)

<!--
  TEMPLATE: docs/project-management/<platform>-playbook.md — one per platform,
  created when that platform's development starts. It defines how the new
  platform consumes the EXISTING behavior library in Delta mode instead of
  re-running the full pipeline per feature.
-->

# <Platform> Development Playbook

> Purpose: start <Platform> development on top of the archived behavior library (`docs/test-cases/`) with minimal repeated verification. The behavior has already been decided once; this platform implements it.

## 1. Start gate

<Platform> feature work starts only when both hold:

- [ ] The feature's behavior cases are archived in `docs/test-cases/` and its matrix row exists.
- [ ] The design package for this platform is ready (<design source + exports location>).

If the behavior is not archived yet, the feature goes through the full eight-step pipeline on the reference platform first.

## 2. Infrastructure base (build once, before features)

- Network layer: <API client conventions — base URL from config, single entry point>.
- Error model: <typed error mapping from the contract's error envelope>.
- Secure storage: <tokens/credentials storage mechanism for this platform; never plain preferences/files>.
- Session handling: <token refresh, eviction on 401/403 per the contract>.
- Design system package: <colors/typography/spacing strictly from the design tokens; component naming matches the design source>.
- Test targets wired into the one-command gate: `<make test-<platform>>`.

## 3. Delta SOP (per feature)

1. **Lock the delta**: read the archived case file; write the delta list only — behaviors where this platform differs (system components, permissions, platform conventions) or explicit "no difference". The behavior body is not re-discussed.
2. **Approval gate (delta only)**: the decision-maker approves the delta list; archived behavior is not re-approved.
3. **Test mapping 1:1**: implement this platform's tests named/mapped by case ID (`<PREFIX>-NNN`); run them red first, as usual.
4. **Implement** per the platform conventions (§4) and the coding standards.
5. **Review** per `REVIEW.md`, with the case file as the primary reference.
6. **Archive**: update the coverage matrix — this platform's cell for the feature becomes ✅ (or ⚠️ with the gap noted); new platform-specific lessons go into the feature file.

## 4. Platform hard rules

- <Slot: e.g. no business-logic invention — behavior comes from the case library and contracts only.>
- <Slot: secrets storage rule for this platform.>
- <Slot: threading/lifecycle rule, e.g. UI state updates on the main thread; work bound to view lifecycle.>
- <Slot: every test carries its case ID; unmapped tests are treated as unplanned work.>

## 5. Rollout milestones

| Milestone | Content | Exit criteria |
|---|---|---|
| <P>-01 Infra | §2 base + one archived simple feature end-to-end | Gate green; matrix cell updated |
| <P>-02 Core loop | The product's core flow features | All archived core cases passing on this platform |
| <P>-03 Remaining v1 | Rest of the v1 feature set | Matrix shows no ❌ in v1 scope |
| <P>-04 Release hardening | Platform store/release requirements | Release checklist passed |
