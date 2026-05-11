# Task Routing Rules

> **How tasks move from goal to backlog, through approval, and into execution. Tasks route by capability first, then role, then preferred worker.**

---

## Task Flow Overview

```
PROJECT_GOAL.md
      │
      ▼
┌──────────┐
│ backlog  │  ← Task proposed by worker (goal decomposition)
└────┬─────┘
     │ Human reviews and approves
     ▼
┌──────────┐
│  ready   │  ← Approved and claimable
└────┬─────┘
     │ Worker claims (capability match)
     ▼
┌──────────┐
│ claimed  │  ← Lock created
└────┬─────┘
     │ Worker begins
     ▼
┌──────────┐      ┌──────────┐
│in-progress│─────▶│ blocked  │
└────┬─────┘      └──────────┘
     │ Worker completes
     ▼
┌──────────┐
│  review  │  ← Awaiting independent verification
└────┬─────┘
     │ Independent verifier approves
     ▼
┌──────────┐
│   done   │  ← Verified and complete
└──────────┘
```

---

## How Tasks Move from Goal to Backlog

1. A worker (typically Hermes or Claude) reads `PROJECT_GOAL.md`.
2. The worker decomposes the goal into discrete, claimable tasks.
3. Each task is written using the task template and placed in `backlog/`.
4. The worker writes a handoff summarizing the decomposition.
5. The human reviews all generated tasks.

---

## How Tasks Are Approved into Ready

1. Human reviews each task in `backlog/`.
2. Human verifies:
   - Objective is clear and scoped.
   - Acceptance criteria are testable.
   - Required capabilities are appropriate.
   - Preferred workers are reasonable.
   - Dependencies are noted.
3. Human moves approved tasks from `backlog/` to `ready/`.
4. Only tasks in `ready/` can be claimed by workers.

---

## How Tasks Are Routed by Capability

### Primary Routing Key: Capability

Every task declares `## Required capabilities`. This is the primary routing key.

A worker may claim a task only if:
- The worker possesses all required capabilities (or can reasonably perform them).
- The worker checks `capability-registry.json` to confirm capability fit.

### Secondary Routing Key: Role

Every task declares `## Responsible role` and optionally `## Supporting roles`.

The responsible role owns the task outcome. Supporting roles assist.

### Tertiary Routing Key: Preferred Worker

The task's `## Preferred workers` list is guidance, not a hard requirement.

A worker not on the preferred list may still claim the task if it has the required capabilities.

---

## How a Worker Selects or Is Assigned a Task

### Self-Selection (Default)

1. Worker reads `assignment-state.json` to understand execution mode.
2. Worker reads `capability-registry.json` to understand its own capabilities.
3. Worker scans `tasks/ready/` for tasks matching its capabilities.
4. Worker selects a task and follows the claiming process.

### Human Assignment

1. Human reviews `tasks/ready/` and `worker-status.json`.
2. Human decides which worker should claim which task.
3. Human communicates the assignment (via PR comment, issue, or direct instruction).
4. Worker claims the assigned task.

### Coordinator Proposal (Hermes)

1. Hermes reviews the task queue and worker statuses.
2. Hermes proposes assignments in a coordination handoff.
3. Human reviews and approves the proposals.
4. Workers claim tasks per the approved proposals.

---

## How Preferred Workers Are Used

Preferred workers are recommendations. They are used to:

1. **Guide initial task creation** — The task creator suggests which workers are best suited.
2. **Help workers self-select** — Workers can see which tasks prefer them.
3. **Inform human assignment** — Humans can use preferences to route work.
4. **Flag capability mismatches** — If a non-preferred worker claims a task, it may indicate a capability gap.

Preferred workers are NOT used to:
- Block a capable worker from claiming a task.
- Create hard dependencies on specific tools.
- Prevent reassignment.

---

## How Solo Mode Differs from Multi-Worker Mode in Routing

### Solo Mode Routing

- One worker claims all tasks sequentially.
- No need for capability matching between workers.
- The worker must still check that it can perform the required capabilities.
- Tasks may be claimed in any order the worker chooses.
- Review tasks are handled by automated validation or human review.

### Multi-Worker Mode Routing

- Tasks are distributed across workers based on capability fit.
- Workers should not claim tasks outside their capabilities.
- Review tasks should be routed to a different worker.
- Coordination is needed to avoid duplicate claims.

### Hybrid Mode Routing

- Primary worker claims most implementation tasks.
- Support workers claim specialized tasks (research, review, verification).
- The primary worker may route tasks to support workers.

---

## How Review Tasks Are Routed

Review tasks (verifying another worker's completed work) must be routed to:

1. A different worker (not the implementing worker) — preferred.
2. Automated validation (`npm run check:dod`, `npm test`) — required.
3. Human review — for critical or security-sensitive tasks.

Review task routing rules:
- The implementing worker must not review their own work.
- The reviewer must have `verification` capability.
- The reviewer must read the task file, handoff, and verification evidence.
- The reviewer must independently confirm acceptance criteria.

---

## How Documentation Tasks Are Routed

Documentation tasks may be routed to:

1. A dedicated documentation maintainer (Claude preferred).
2. The implementing worker (as part of the implementation task).
3. Any worker with `documentation` capability.

Documentation tasks should:
- Reference the code or feature being documented.
- Include links to relevant ADRs or specs.
- Be reviewable by a different worker.

---

## How Blocked Tasks Are Escalated

When a task is blocked:

1. Worker documents the block in the task file and handoff.
2. Worker moves the task to `blocked/`.
3. Worker describes: what is blocked, why, and what is needed to unblock.
4. Human reviews blocked tasks and unblocks where possible.
5. If the block is due to worker incapability, reassignment is triggered.

---

## How Reassignment Is Triggered

Reassignment is triggered when:

1. **Worker is blocked** — Cannot proceed due to tool limitation or missing capability.
2. **Lock is stale** — Worker's lock expired without renewal.
3. **Human requests it** — Human owner wants a different worker.
4. **Better capability fit** — Another worker is significantly better suited.
5. **Review failure** — Review reveals issues the current worker cannot fix.
6. **Scope change** — Task now requires capabilities the current worker lacks.

See [`worker-switching-protocol.md`](./worker-switching-protocol.md) for the full reassignment process.

---

## Routing Decision Tree

```
Task in ready/
│
├─ Execution mode: solo?
│  └─ Solo worker claims any task (must check own capabilities)
│
├─ Execution mode: multi-worker?
│  ├─ Task requires verification?
│  │  └─ Route to worker with verification capability (not implementer)
│  ├─ Task requires research?
│  │  └─ Route to Gemini or Claude
│  ├─ Task requires code-implementation?
│  │  └─ Route to Codex or Windsurf
│  ├─ Task requires UI verification?
│  │  └─ Route to Antigravity
│  └─ Task requires coordination?
│     └─ Route to Hermes
│
└─ Execution mode: hybrid?
   ├─ Primary worker claims most tasks
   └─ Support workers claim specialized tasks
```

---

## Related Files

- [`assignment-model.md`](./assignment-model.md) — Full assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Execution mode definitions
- [`role-capability-matrix.md`](./role-capability-matrix.md) — Role-to-capability mapping
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment protocol
- [`task-lifecycle.md`](./task-lifecycle.md) — Task state machine
- [`state/capability-registry.json`](./state/capability-registry.json) — Machine-readable capability registry
