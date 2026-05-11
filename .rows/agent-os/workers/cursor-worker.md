> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# Cursor Worker

> **Role:** Adaptive repository worker for teams using Cursor.

## Startup Sequence

Before any action, Cursor must read:
1. [`AGENTS.md`](../../AGENTS.md)
2. [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
3. [`agent-os/worker-contract.md`](../worker-contract.md)
4. [`agent-os/state/system-state.json`](../state/system-state.json)
5. [`CURSOR.md`](../../CURSOR.md)
6. [`agent-os/tool-boundaries.md`](../tool-boundaries.md)
7. Relevant files in [`.cursor/rules/`](../../.cursor/rules/)

## Required Output

Cursor should leave the same durable artifacts as other workers:
- task updates
- handoffs
- verification evidence
- status updates

## Notes

- Use the canonical tool-boundary policy.
- Keep `.cursor/rules/` additive and project-specific.
- Cursor is optional; do not assume it exists in every fork.
