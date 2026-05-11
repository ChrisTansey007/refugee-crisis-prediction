# Handoffs

This directory contains worker handoff files. Handoffs enable continuity between worker sessions.

## Directory Structure

| Folder | Purpose |
|--------|---------|
| [`active/`](./active/) | Current handoffs from recent sessions |
| [`archive/`](./archive/) | Handoffs from completed tasks |

## Handoff Template

Use [`handoff-template.md`](./handoff-template.md) to create new handoffs.

## Rules

- Every worker session MUST produce a handoff. No exceptions.
- Handoffs are required even if the task is incomplete.
- Handoffs go in `active/` during work, then move to `archive/` when the task is done.
- Durable knowledge should be distilled into [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) before active handoffs become the default history source.
- A handoff is a work-layer artifact. Keep evergreen context in the knowledge layer once it proves durable.

## Related Files

- [`../worker-contract.md`](../worker-contract.md) — Handoff requirements
- [`../task-lifecycle.md`](../task-lifecycle.md) — When handoffs are required
