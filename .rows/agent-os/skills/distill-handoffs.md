# Skill: Distill Handoffs

Use this skill when active handoffs have accumulated enough durable knowledge that future agents should not need to read them all directly.

## Purpose

Promote durable context from `agent-os/handoffs/active/` into `PROJECT_CONTEXT.md`, then archive distilled handoffs when appropriate.

## Durable vs Ephemeral

Keep:

- stable facts about the system or repo
- constraints that will shape later tasks
- risks that continue beyond one session
- assumptions still being carried
- recurring verification or workflow lessons

Do not keep:

- raw command logs
- one-off terminal output
- transient next steps already captured in task files
- duplicated prose that adds no new meaning

## Steps

1. Read the active handoffs that matter for the current project state.
2. Run the draft distillation helper:

```bash
npm run distill:handoffs
```

3. Review the draft block inserted into `PROJECT_CONTEXT.md`.
4. Promote only durable items into the main sections of `PROJECT_CONTEXT.md`.
5. Update `Recently Distilled Handoffs` with links to the handoffs covered.
6. Move fully distilled handoffs from `agent-os/handoffs/active/` to `agent-os/handoffs/archive/` when they are no longer the source of current execution context.

## Cross-References

- Link to ADRs or decision-register entries when a handoff records a formal decision.
- Link back to archived handoffs when nuance matters and should remain auditable.
