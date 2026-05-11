# ADR-0001: Repo-Orchestrated Worker System

## Status

Accepted

## Date

2026-05-06

## Context

Multi-agent AI development faces a fundamental coordination problem: each AI tool has its own context window, memory, and session state. Without a shared source of truth, workers duplicate effort, make conflicting changes, and produce unverifiable output. We need a system where the repository itself acts as the control plane, owning rules, state, tasks, and verification.

## Decision

We will use the repository as the orchestrator. All rules, task definitions, state, handoffs, locks, and verification gates live as files in the repo. Workers (AI tools) read from and write to the repo, never relying on local memory or chat session state as authoritative.

Key design choices:
- **File-based state:** JSON and Markdown files are the canonical state store. No external database.
- **Folder-based lifecycle:** Task state is represented by which folder the task file resides in.
- **Advisory locks:** Workers declare intent via lock files. Locks are advisory but required by process.
- **Handoff requirement:** Every session produces a handoff file for continuity.
- **Independent verification:** No worker can mark its own task done.

## Consequences

**Positive:**
- Any worker can pick up where another left off by reading handoff files.
- State is version-controlled and auditable via git history.
- No single point of failure — the repo is distributed via git.
- Workers are replaceable; the system does not depend on any specific AI tool.

**Negative:**
- Workers must be disciplined about reading files before acting.
- File-based state requires careful merge conflict resolution.
- Stale state files are possible if workers fail to update them.
- Human oversight is still required for critical decisions.

## Alternatives Considered

1. **Centralized orchestration server:** Rejected because it introduces a single point of failure and operational overhead.
2. **Agent-to-agent messaging:** Rejected because it lacks auditability and persistence.
3. **Database-backed state:** Rejected because it adds infrastructure complexity and reduces git-based auditability.

## Related Files

- [`AGENTS.md`](../../../AGENTS.md) — System constitution
- [`agent-os/repo-orchestration-model.md`](../../../agent-os/repo-orchestration-model.md) — Orchestration model
