# Prompt Library

> **Copy/paste prompts for giving to AI workers. These are starter instructions — the repo files (`AGENTS.md`, `PROJECT_GOAL.md`, `agent-os/`) are the authority.**

## What This Is

The prompt library contains ready-to-use prompts you can give to different AI workers (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) to start specific types of sessions.

## When to Use Each Prompt

| Prompt | Use When |
|--------|----------|
| `goal-intake-to-tasks.md` | You've filled in `PROJECT_GOAL.md` and want a worker to create initial tasks |
| `solo-worker-start.md` | You want one worker to do everything |
| `multi-worker-start.md` | You want multiple workers to divide work |
| `hybrid-primary-worker-start.md` | You want one primary worker with support workers |
| `support-worker-start.md` | You want a worker to do research, docs, testing, or review |
| `reviewer-worker-start.md` | You want a worker to review another worker's output |
| `verification-worker-start.md` | You want a worker to verify task completion |
| `reassignment-continuation.md` | You're switching a task from one worker to another |
| `status-report-request.md` | You want a summary of current repo state |
| `template-publish-check.md` | You want to verify the repo is ready to publish as a template |

## Important Warnings

1. **Prompts do not replace repo files.** The authoritative rules are in `AGENTS.md` and `agent-os/`. Prompts are starter instructions only.
2. **Workers must write durable state back into repo files.** No private chat memory dependency.
3. **Prompts are not authority over `AGENTS.md`.** If a prompt contradicts `AGENTS.md`, `AGENTS.md` wins.
4. **Always review worker output.** Prompts start work; you verify completion.

## Related Files

- [`../AGENTS.md`](../AGENTS.md) — Worker constitution
- [`../PROJECT_GOAL.md`](../PROJECT_GOAL.md) — Project definition
- [`../agent-os/README.md`](../agent-os/README.md) — Agent OS overview
