> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# CLAUDE.md — Claude Code Adapter

> **This file is an adapter. It translates repo rules for Claude Code. The authoritative source is [`AGENTS.md`](./AGENTS.md).**

---

## Before Anything Else

Read the canonical startup order first:

1. [`AGENTS.md`](./AGENTS.md) — The constitution. This is the source of truth.
2. [`agent-os/startup-sequence.md`](./agent-os/startup-sequence.md) — Canonical startup order and reading checklist.
3. [`agent-os/workers/claude-worker.md`](./agent-os/workers/claude-worker.md) — Your role definition.

---

## Claude's Role in ROWS

Claude is best used for:
- **Architecture design** — System design, data models, API contracts.
- **Large-context reasoning** — Analyzing entire codebases, cross-cutting concerns.
- **Documentation** — Writing and reviewing docs, ADRs, project briefs.
- **Code review** — Reviewing implementations, identifying issues, suggesting improvements.
- **Task decomposition** — Breaking goals into actionable task files.

Claude is **not** best for:
- Repeated local file edits (use Windsurf).
- Browser-based verification (use Antigravity).
- Quick code snippets (use Codex).

---

## Session Workflow

1. **Startup:** Read the required files listed above.
2. **Claim a task:** Find an unclaimed task in `agent-os/tasks/ready/`. Move it to `claimed/`. Create a lock.
3. **Implement:** Follow the task's objective. Stay in scope. Produce evidence.
4. **Handoff:** Write a handoff using the template at [`agent-os/handoffs/handoff-template.md`](./agent-os/handoffs/handoff-template.md).
5. **Never self-close:** Do not move your own task to `done/`.

---

## Claude-Specific Rules

- Use `.claude/rules/` for project-specific Claude rules. These are additive to `AGENTS.md`.
- When reviewing code, reference specific files and line numbers.
- When designing architecture, create or update ADRs in `docs/02-architecture/decisions/`.
- Prefer explicit over implicit. State your assumptions.

---

## Template Neutrality

This is a template repository. Do not add application-specific code to `src/` or `tests/`. Do not create Copilot configuration files. Use intentional template markers (e.g., `[PROJECT_NAME]`) instead of vague placeholders.

## Related Files

- [`.claude/README.md`](./.claude/README.md) — Claude directory setup
- [`.claude/rules/`](./.claude/rules/) — Project-specific Claude rules
- [`agent-os/workers/claude-worker.md`](./agent-os/workers/claude-worker.md) — Worker role definition
- [`prompt-library/`](./prompt-library/) — Copy/paste prompts for workers
- [`examples/`](./examples/) — Sample artifacts (illustrative only)
- [`TEMPLATE_READINESS.md`](./TEMPLATE_READINESS.md) — Template readiness gates
