# Glossary

> **Customize after forking. Define project-specific terminology so all workers share a common vocabulary.**

## Project Terms

| Term | Definition |
|------|------------|
| [TERM_1] | [DEFINITION] |
| [TERM_2] | [DEFINITION] |

## ROWS System Terms

| Term | Definition |
|------|------------|
| Worker | An AI tool (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) that executes repo-defined tasks. |
| Task | A unit of work defined as a Markdown file in `agent-os/tasks/`. |
| Handoff | A Markdown file documenting a worker session's work, placed in `agent-os/handoffs/active/`. |
| Lock | An advisory JSON file in `agent-os/locks/` that declares a worker's intent to modify specific files. |
| Verification Gate | A checkpoint that must be passed before a task can be marked done. |
| ADR | Architecture Decision Record — a document capturing a significant architectural choice. |

## How to Add Terms

When you introduce a new concept, add it to this glossary. Workers should reference this file to ensure consistent terminology.

## Related Files

- [`AGENTS.md`](../../AGENTS.md) — System constitution
- [`../05-decisions/decision-register.md`](../05-decisions/decision-register.md) — Decision register
