# Repo Orchestration Model

> **How the repository acts as the control plane for multi-agent development.**

## Core Architecture

```
┌─────────────────────────────────────────┐
│              REPOSITORY                  │
│  (Control Plane — Source of Truth)      │
│                                         │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │  RULES  │  │  STATE   │  │ TASKS  │ │
│  │ AGENTS  │  │  JSON    │  │  MD    │ │
│  └─────────┘  └──────────┘  └────────┘ │
│                                         │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │ HANDOFFS│  │  LOCKS   │  │REPORTS │ │
│  │   MD    │  │  JSON    │  │  MD    │ │
│  └─────────┘  └──────────┘  └────────┘ │
└──────────────┬──────────────────────────┘
               │  Read / Write
    ┌──────────┼──────────────────┐
    │          │                  │
    ▼          ▼                  ▼
┌───────┐ ┌───────┐         ┌───────┐
│Worker │ │Worker │   ...   │Worker │
│   A   │ │   B   │         │   N   │
└───────┘ └───────┘         └───────┘
```

## Key Principles

### 1. Repo as Control Plane
The repository is the single source of truth. Every worker reads its instructions, state, and context from the repo. Every worker writes its output, evidence, and handoffs back to the repo.

### 2. Roles Are Jobs, Workers Are Tools
A role describes the type of work being performed. A worker describes the AI tool or human executing the work. A single worker may perform multiple roles. A single role may be performed by different workers over time. The repo must preserve continuity through durable files, not private chat memory.

### 3. Workers as Replaceable Execution Units
Workers are stateless. They do not maintain persistent memory between sessions. All context needed for continuity is stored in handoff files. Tasks route by capability first, then role, then preferred worker. Any worker can be replaced if handoffs are preserved.

### 4. State Through Files
System state is stored in JSON and Markdown files. This means:
- State is version-controlled.
- State changes are auditable via `git log`.
- State can be reviewed in PRs.
- No infrastructure beyond git is needed.

### 5. Task Queue Through Folders
Task lifecycle is represented by folder location:
- `backlog/` — Proposed, not yet approved.
- `ready/` — Approved and claimable.
- `claimed/` — Claimed by a worker, lock created.
- `in-progress/` — Work is happening.
- `review/` — Awaiting independent verification.
- `blocked/` — Cannot proceed due to dependency or issue.
- `done/` — Verified and complete.

### 6. Handoffs as Continuity
Every worker session produces a handoff file. Handoffs contain:
- What was done.
- What was not done.
- Known issues.
- Next steps.
- Evidence produced.

This enables any worker to continue where another left off.

### 7. Verification as Anti-Fake-Completion Gate
No worker can mark its own task as done. A different worker or a human must independently verify that acceptance criteria are met.

### 8. Humans as Final Authority
When the system cannot resolve a conflict, when a decision has significant consequences, or when a worker is uncertain, the human owner is the final authority.

## Information Flow

1. **Human** writes `PROJECT_GOAL.md` and selects an execution mode.
2. **Worker** (typically Hermes or Claude) reads the goal and decomposes it into task files in `backlog/`, each with required capabilities and preferred workers.
3. **Human** reviews tasks and moves approved ones to `ready/`.
4. **Worker** checks `assignment-state.json` for execution mode, confirms capability fit, claims a task from `ready/`, creates a lock, and moves it to `in-progress/`.
5. **Worker** implements the task, produces evidence, writes a handoff.
6. **Worker** moves the task to `review/`.
7. **Different worker or human** verifies the task.
8. **Verifier** moves the task to `done/`, removes the lock, archives the handoff.

In solo mode, steps 4-6 are performed by one worker. In multi-worker mode, steps are distributed. In hybrid mode, a primary worker drives with support workers assisting.

## Reassignment Flow

When a worker must be replaced:
1. Current worker writes a handoff.
2. Lock is closed or marked stale.
3. Reassignment record is created.
4. New worker reads the handoff, task file, and evidence.
5. New worker creates a new lock and continues.

## Related Files

- [`assignment-model.md`](./assignment-model.md) — Assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Execution modes
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment protocol
- [`worker-contract.md`](./worker-contract.md) — Worker obligations
- [`task-lifecycle.md`](./task-lifecycle.md) — Task state machine
- [`verification-gates.md`](./verification-gates.md) — Verification checkpoints
