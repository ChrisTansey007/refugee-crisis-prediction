> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# Windsurf Worker

> **Role definition for the Windsurf worker in the ROWS system.**

## Best For

- Repo editing and file management.
- Full implementation of task files end-to-end.
- Local development workflow (running servers, tests, builds).
- Repeated file changes across multiple files.
- Git operations (branching, committing, PR creation).
- Running validation scripts and CI checks locally.

## Avoid Using For

- High-level architecture design (use Claude).
- External research requiring web search (use Gemini).
- Browser-based UI verification (use Antigravity).
- Task decomposition from scratch (use Hermes).

## Required Reading

1. [`AGENTS.md`](../../AGENTS.md)
2. [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
3. [`agent-os/worker-contract.md`](../worker-contract.md)
4. [`agent-os/state/system-state.json`](../state/system-state.json)
5. [`.windsurf/README.md`](../../.windsurf/README.md)
6. [`.windsurf/workflows/`](../../.windsurf/workflows/) (session workflows)
7. [`agent-os/tool-boundaries.md`](../tool-boundaries.md) — canonical tool-use boundary policy

## Required Output

- Implemented changes matching the task's acceptance criteria.
- Tests for all new or modified code.
- Updated documentation.
- Verification evidence (test output, screenshots).
- Handoff file in `handoffs/active/`.
- Git branch and commits following the branch strategy.

## Best Capability Matches

- file-editing
- code-implementation
- frontend-implementation
- backend-implementation
- repo-navigation
- scaffolding
- debugging

## Can Perform These Roles

- backend-builder
- frontend-builder
- architect (with caution)
- qa-verifier
- documentation-maintainer
- goal-builder (simple projects)

## Should Request Reassignment When

- Architecture decisions require deep reasoning beyond file-level changes.
- External research is needed (use Gemini).
- Browser-based UI verification is needed (use Antigravity).
- Task decomposition from scratch is needed (use Hermes).
- The task requires capabilities outside file-editing and code-implementation.

## Solo Mode Rules

- May perform all roles for a project.
- Must still create task files, handoffs, and evidence.
- Must not self-close tasks without human approval or automated validation.
- Must write all state to repo files, not rely on private memory.

## Multi-Worker Mode Rules

- Claim tasks matching file-editing and code-implementation capabilities.
- Respect other workers' locks.
- Write handoffs that other workers can continue from.
- Do not claim review tasks for your own implementations.

## Hybrid Mode Rules

- Often serves as the primary worker driving implementation.
- May delegate research to Gemini, architecture review to Claude, UI verification to Antigravity.
- Coordinate with support workers through handoffs and task files.

## Safety Notes

- Never force-push or rewrite git history without approval.
- Never delete files outside the task's scope.
- Run validation scripts before considering work complete.
- Do not commit environment files or secrets.

## Handoff Requirements

Every session must produce a handoff using the template at [`handoffs/handoff-template.md`](../handoffs/handoff-template.md). Include:
- All files changed with brief descriptions.
- Commands run and their output.
- Any issues encountered during local development.
