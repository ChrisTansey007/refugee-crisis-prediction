> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# Startup Sequence

> **Canonical startup order for any ROWS worker session.**

## Read in Order

1. `AGENTS.md` — constitution and top-level safety rules.
2. `agent-os/knowledge-model.md` — how knowledge files differ from work-state files.
3. `PROJECT_GOAL.md` — the project goal and constraints.
4. `PROJECT_CONTEXT.md` — distilled durable context before raw session history.
5. `agent-os/README.md` — how the agent OS is organized.
6. `agent-os/worker-contract.md` — required worker obligations.
7. `agent-os/state/system-state.json` — current repo state.
8. `agent-os/state/assignment-state.json` — execution mode and assignments.
9. `agent-os/state/capability-registry.json` — capability definitions.
10. Worker-specific file in `agent-os/workers/`.
11. Role file in `agent-os/roles/`.
12. Tool adapter file (`CLAUDE.md`, `.windsurf/README.md`, etc.).
13. Relevant task files, their `Context Snapshot`, and only the work-layer artifacts needed for the task.

## Purpose

This sequence ensures every worker starts from repo state instead of local memory and reduces drift between workers, sessions, and tools.

## Usage

- Keep this file as the canonical reference for startup order.
- Summarize it in `AGENTS.md` and worker adapters rather than duplicating the full sequence everywhere.
