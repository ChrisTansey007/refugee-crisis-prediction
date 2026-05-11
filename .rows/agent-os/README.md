# Agent OS — The Agent Operating System

> **This directory is the operating system for multi-agent development. It owns the rules, tasks, state, handoffs, and verification gates.**

## What Is Agent OS?

Agent OS is a file-based operating system for coordinating AI workers. It replaces the need for a centralized orchestration server with a set of conventions enforced through files and folders in the repository.

## Core Concepts

### Knowledge Layer vs Work Layer
ROWS separates evergreen knowledge from current execution state. See [`knowledge-model.md`](./knowledge-model.md).

- Knowledge layer: rules, goals, context, ADRs, decisions, graph outputs
- Work layer: tasks, handoffs, blockers, locks, triggers, verification artifacts

### The Repo Is the Control Plane
Every worker derives its authority from files in this repo. No worker's local memory, chat session, or external state is authoritative.

### Roles Are Jobs, Workers Are Tools
A role describes the type of work being performed (e.g., backend-builder). A worker describes the AI tool or human executing the work (e.g., Codex). One worker can perform multiple roles. One role can be performed by different workers.

### Workers Are Replaceable Execution Units
Workers (Windsurf, Codex, Claude, Gemini, Hermes, Antigravity) are stateless execution units. They read state from the repo, perform work, and write results back. Tasks route by capability, not by tool name. Any worker can be replaced if handoffs are preserved.

### State Through Files
All system state lives in version-controlled files. No external database. Git history provides auditability.

### Task Queue Through Folders
Task state is represented by which folder a task file resides in (`backlog/`, `ready/`, `claimed/`, `in-progress/`, `review/`, `blocked/`, `done/`).

### Handoffs as Continuity
Every worker session produces a handoff file. Handoffs enable any worker to pick up where another left off.

### Verification as Anti-Fake-Completion Gate
No worker can mark its own task done. Independent verification is required.

## Directory Structure

```
agent-os/
├── README.md                     ← This file
├── repo-orchestration-model.md   ← How the repo orchestrates workers
├── assignment-model.md           ← Assignment hierarchy
├── execution-modes.md            ← Solo, multi-worker, hybrid modes
├── role-capability-matrix.md     ← Role-to-capability mapping
├── worker-switching-protocol.md  ← Reassignment protocol
├── task-routing-rules.md         ← Task flow and routing
├── startup-sequence.md           ← Canonical worker startup order
├── glossary.md                   ← Core ROWS terminology
├── mcp.md                        ← Optional MCP policy and setup
├── worktree-strategy.md          ← Parallel worker worktree rules
├── provider-routing.md           ← Provider tier routing guidance
├── prompt-injection-policy.md    ← External content safety rules
├── tool-boundaries.md            ← Canonical tool-use boundary policy
├── worker-contract.md            ← Universal obligations for all workers
├── task-lifecycle.md             ← Task state machine
├── definition-of-done.md         ← What "done" means
├── verification-gates.md         ← Verification checkpoints
├── escalation-rules.md           ← When and how to escalate
├── branch-strategy.md            ← Git branch naming conventions
├── file-ownership.md             ← Collision avoidance
├── workers/               ← Worker capability definitions
├── roles/                 ← Role definitions (jobs)
├── tasks/                 ← Task lifecycle folders
├── handoffs/              ← Worker handoff files
├── checkpoints/           ← Partial-progress checkpoint notes
├── proposals/             ← Coordination proposals
├── milestones/            ← Milestone templates and planning state
├── checklists/            ← Operational checklists
├── schedules/             ← Cadence definitions
├── state/                 ← System state (JSON)
├── locks/                 ← Advisory file locks
├── reassignment/          ← Worker reassignment records
├── observability.md       ← Observability attachment guidance
└── reports/               ← Generated reports
    ├── audits/                   ← Audit reports
    ├── status/                   ← Status reports
    ├── verification/             ← Verification reports
    ├── assignments/              ← Assignment reports
    ├── template-readiness/       ← Template readiness reports
    ├── links/                    ← Link validation reports
    ├── placeholders/             ← Placeholder audit reports
    ├── locks/                    ← Lock validation reports
    ├── provider-routing/         ← Provider routing validation reports
    ├── startup-consistency/      ← Startup sequence validation reports
    └── security/                 ← Secret scan reports
```

## Quick Start for Workers

1. Read [`AGENTS.md`](../AGENTS.md).
2. Read [`knowledge-model.md`](./knowledge-model.md).
3. Read [`../PROJECT_GOAL.md`](../PROJECT_GOAL.md) and [`../PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md).
4. Read [`worker-contract.md`](./worker-contract.md).
5. Read state files such as [`state/system-state.json`](./state/system-state.json) and [`state/assignment-state.json`](./state/assignment-state.json).
6. Read your worker file in [`workers/`](./workers/) and the role file for the role you are performing in [`roles/`](./roles/).
7. Read the task, its `Context Snapshot`, and only the work-layer artifacts relevant to that task.
8. Claim a task from [`tasks/ready/`](./tasks/ready/).
9. Follow the task lifecycle.

## Related Files

- [`AGENTS.md`](../AGENTS.md) — Primary constitution
- [`PROJECT_GOAL.md`](../PROJECT_GOAL.md) — Project definition
- [`assignment-model.md`](./assignment-model.md) — Assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Execution modes
- [`startup-sequence.md`](./startup-sequence.md) — Canonical worker startup order
- [`glossary.md`](./glossary.md) — Core ROWS terminology
- [`mcp.md`](./mcp.md) — Optional MCP policy and setup
- [`worktree-strategy.md`](./worktree-strategy.md) — Parallel worker worktree rules
- [`provider-routing.md`](./provider-routing.md) — Provider tier routing guidance
- [`prompt-injection-policy.md`](./prompt-injection-policy.md) — External content safety rules
- [`tool-boundaries.md`](./tool-boundaries.md) — Canonical tool-use boundary policy
- [`../HUMAN_OWNER_GUIDE.md`](../HUMAN_OWNER_GUIDE.md) — Guide for human owners
- [`../TEMPLATE_READINESS.md`](../TEMPLATE_READINESS.md) — Template readiness gates
- [`../prompt-library/`](../prompt-library/) — Copy/paste worker prompts
- [`../examples/`](../examples/) — Sample artifacts
