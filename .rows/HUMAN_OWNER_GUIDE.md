# HUMAN_OWNER_GUIDE.md

> **Guide for the human project owner using ROWS.**

---

## What Is ROWS?

ROWS (Repo-Orchestrated Worker System) is a GitHub template that turns your repository into an operating system for AI-assisted development. The repo is the orchestrator. AI tools (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) are workers.

## Core Concepts

- **The repo is the orchestrator.** Rules, tasks, state, and evidence live in version-controlled files.
- **Roles are jobs, workers are tools.** Tasks route by capability, not by tool name.
- **Workers are replaceable.** Any task can be reassigned if handoffs preserve context.
- **No worker may self-close.** Independent verification is required.

## Execution Modes

| Mode | Description | Self-Close Rule |
|------|-------------|-----------------|
| Solo | One worker does everything | Must use human approval or automated validation |
| Multi-Worker | Multiple workers divide work | Different worker must review |
| Hybrid | One primary + support workers | Support worker or human must review |

Set mode in `agent-os/state/assignment-state.json`.

## First Hour After Forking

1. Fork the template on GitHub.
2. Clone your fork locally.
3. Fill in `PROJECT_GOAL.md` completely.
4. Choose an execution mode.
5. Run `npm run audit`.
6. Give a worker the prompt from `prompt-library/goal-intake-to-tasks.md`.
7. Review generated tasks in `agent-os/tasks/backlog/`.
8. Move approved tasks to `agent-os/tasks/ready/`.
9. Start workers using prompts from `prompt-library/`.
10. Review handoffs as workers complete sessions.

## How to Review Work

- **Handoffs:** Read `agent-os/handoffs/active/` after every worker session.
- **Verification evidence:** Check `agent-os/reports/verification/` for test results, screenshots, logs.
- **Task completion:** Only approve when all acceptance criteria are met, evidence exists, and an independent reviewer confirms.

## Validation Commands

See [`docs/03-development/commands.md`](./docs/03-development/commands.md) for the canonical command list.

Typical owner checks:

```bash
npm run audit
npm run validate:agent-os
npm run validate:template
```

## Common Mistakes

1. Skipping `PROJECT_GOAL.md` — workers make incorrect assumptions.
2. Letting workers self-close — always require independent review.
3. Relying on private chat memory — everything must be in repo files.
4. Not reviewing handoffs — they are your window into worker activity.
5. Not running validation — catches issues early.
6. Treating preferred workers as requirements — they are recommendations.
7. Using Copilot — this system intentionally excludes Copilot.
8. Adding app-specific code to the template — keep `src/` and `tests/` generic until committed to a project.

## Hard Rules

1. **No worker may mark its own task as done.**
2. **Private chat memory is not durable project state.**
3. **Solo mode does not mean self-approval mode.**
4. **The repo is the orchestrator — not any single AI tool.**
5. **All durable state must be written back into repo files.**

## Related Files

- [`AGENTS.md`](./AGENTS.md) — Worker constitution
- [`PROJECT_GOAL.md`](./PROJECT_GOAL.md) — Project definition
- [`TEMPLATE_USAGE.md`](./TEMPLATE_USAGE.md) — Fork workflow
- [`prompt-library/`](./prompt-library/) — Copy/paste prompts for workers
- [`examples/`](./examples/) — Sample artifacts
