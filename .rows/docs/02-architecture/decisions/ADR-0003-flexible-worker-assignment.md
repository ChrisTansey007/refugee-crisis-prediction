# ADR-0003: Flexible Worker Assignment Model

**Status:** Accepted
**Date:** 2026-05-06
**Deciders:** ROWS template architects

---

## Context

The ROWS system coordinates multiple AI workers (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) through a file-based orchestration model. In Prompt 1, the system established the repo as the orchestrator. In Prompt 2, we needed to define how tasks are assigned to workers.

The naive approach would be to hardwire tasks to specific tools: "Codex does all backend work," "Claude does all architecture." This creates fragility — if a tool is unavailable, the task stalls. If a better tool emerges, migration is difficult.

We needed an assignment model that:
- Routes work by what needs to be done, not by which tool is available
- Allows any worker to claim any task it is capable of performing
- Supports solo, multi-worker, and hybrid execution modes
- Enables worker replacement mid-task without losing context
- Prevents workers from self-approving their own work
- Makes all assignment state discoverable from repo files

---

## Decision

We implemented a four-layer assignment hierarchy:

```
capability → role → preferred worker → active worker
```

### Layer 1: Capability

Tasks declare required **capabilities** — discrete skills like `code-implementation`, `test-writing`, `architecture-planning`. Capabilities are the primary routing key. A capability registry (`capability-registry.json`) defines 21 capabilities with preferred workers, common roles, and expected evidence.

### Layer 2: Role

Tasks declare a **responsible role** — a job description like `backend-builder`, `qa-verifier`, `architect`. Roles are collections of capabilities organized around a responsibility. Ten role definition files exist in `agent-os/roles/`.

### Layer 3: Preferred Worker

Tasks may list **preferred workers** — recommendations based on known strengths. These are guidance, not hard requirements. The system must function if a different worker claims the task.

### Layer 4: Active Worker

The **active worker** is the worker that actually claimed the task. Recorded in the task file and `assignment-state.json`. Until claimed, it is `none`.

### Execution Modes

We support three execution modes, recorded in `assignment-state.json`:

- **Solo Worker Mode:** One worker does everything. Still requires task files, handoffs, evidence, and must not self-close without independent review or human approval.
- **Multi-Worker Mode:** Multiple workers divide work by task, role, or capability. Requires locks, handoffs, and independent review by a different worker.
- **Hybrid Mode:** One primary worker drives the project with specialized support workers for research, testing, review, or verification.

### Worker Replaceability

Workers are replaceable execution units. A task may be reassigned when:
- The current worker is blocked or unavailable
- The lock is stale
- A different worker is better suited for the required capabilities
- The human owner requests it

Reassignment requires: a handoff from the current worker, a reassignment record, and a new lock from the new worker.

### No Self-Closing

No worker may mark its own task as done. This is the hardest rule in the system. Completion requires independent verification by a different worker, automated validation, or human approval.

### Durable Repo Files Replace Private Chat Memory

All assignment state, task progress, handoffs, and verification evidence must be written to repo files. No worker may rely on private chat memory as durable project memory. This enables worker replacement and cross-session continuity.

---

## Consequences

### Positive

- **Tool agnosticism:** The system works with any subset of workers. New workers can be added by defining their capabilities.
- **Resilience:** If a worker is unavailable, tasks can be reassigned without losing context.
- **Flexibility:** Human owners can choose solo, multi-worker, or hybrid mode based on project needs.
- **Auditability:** All assignments are recorded in version-controlled files. Git history provides a full audit trail.
- **Quality gates:** The no-self-close rule and verification gates prevent fake completions.
- **Continuity:** Handoffs and reassignment records enable seamless worker switching.

### Negative

- **Coordination overhead:** Multi-worker mode requires locks, handoffs, and careful file collision avoidance.
- **Learning curve:** Workers must understand the assignment hierarchy and follow the claiming protocol.
- **File proliferation:** Assignment state is spread across multiple files (task files, assignment-state.json, capability-registry.json, worker-status.json).
- **Solo mode risk:** In solo mode, there is no independent worker review — the human must be the reviewer or automated validation must be trusted.

---

## Trade-offs

| Trade-off | Choice | Alternative |
|-----------|--------|-------------|
| Routing key | Capability first | Worker name first (simpler but fragile) |
| Worker assignment | Workers claim tasks | Coordinator assigns tasks (centralized but bottleneck) |
| Preferred workers | Recommendations only | Hard requirements (rigid but predictable) |
| Execution modes | Three modes (solo, multi, hybrid) | One mode only (simpler but inflexible) |
| Self-closing | Forbidden | Allowed with attestation (simpler but trust-based) |
| State storage | Repo files | External database (more powerful but less auditable) |

---

## Alternatives Considered

### 1. Hardwired Tool Assignment

Assign tasks directly to specific tools (e.g., "Codex owns all backend tasks").

**Rejected because:** Creates single points of failure. Prevents worker replacement. Encourages private-memory dependency. Makes the system fragile when tools are unavailable.

### 2. Centralized Coordinator Assignment

A coordinator (Hermes) assigns tasks to workers.

**Rejected because:** Creates a bottleneck and a single point of authority. Violates the "no worker is the boss" principle. Workers should claim tasks based on their own capability assessment.

### 3. Single Execution Mode

Support only one mode (e.g., always multi-worker).

**Rejected because:** Different projects have different needs. Solo developers should not be forced into multi-worker coordination overhead. The system should scale from solo to team.

### 4. Self-Closing with Attestation

Allow workers to close their own tasks if they attest completion.

**Rejected because:** Trust-based systems are vulnerable to fake completions. Independent verification is a core quality gate. The no-self-close rule is the hardest rule for good reason.

---

## Related Decisions

- [ADR-0001: Repo-Orchestrated Worker System](./ADR-0001-repo-orchestrated-worker-system.md) — Establishes the repo as the orchestrator
- [ADR-0002: Template Fork Workflow](./ADR-0002-template-fork-workflow.md) — Defines the fork-and-fill workflow

## Related Files

- [`agent-os/assignment-model.md`](../../../agent-os/assignment-model.md) — Full assignment hierarchy documentation
- [`agent-os/execution-modes.md`](../../../agent-os/execution-modes.md) — Execution mode details
- [`agent-os/role-capability-matrix.md`](../../../agent-os/role-capability-matrix.md) — Role-to-capability mapping
- [`agent-os/worker-switching-protocol.md`](../../../agent-os/worker-switching-protocol.md) — Reassignment protocol
- [`agent-os/state/assignment-state.json`](../../../agent-os/state/assignment-state.json) — Current assignment state
- [`agent-os/state/capability-registry.json`](../../../agent-os/state/capability-registry.json) — Capability definitions
