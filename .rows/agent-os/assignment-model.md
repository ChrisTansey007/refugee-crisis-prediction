# Assignment Model

> **How tasks are assigned to workers in the ROWS system. The assignment hierarchy is: capability → role → preferred worker → active worker.**

---

## The Assignment Hierarchy

Tasks are NOT hardwired to specific AI tools. Instead, assignment flows through four layers:

```
capability → role → preferred worker → active worker
```

### Layer 1: Capability

A **capability** is a discrete skill or function that a task requires. Examples:

- `code-implementation`
- `test-writing`
- `architecture-planning`
- `research`
- `ui-browser-verification`
- `documentation`

Every task must declare its required capabilities. This is the primary routing key.

### Layer 2: Role

A **role** is a job description — a collection of capabilities organized around a responsibility. Examples:

- `backend-builder`
- `qa-verifier`
- `architect`
- `researcher`

A task declares one responsible role and may list supporting roles. The responsible role owns the task outcome.

### Layer 3: Preferred Worker

A **preferred worker** is a recommendation, not a hard requirement. It indicates which worker(s) are best suited for the task based on their known strengths. Examples:

- Codex for code-implementation
- Claude for architecture-planning
- Gemini for research
- Windsurf for repo-editing

Preferred workers are guidance. The system must function if a different worker claims the task.

### Layer 4: Active Worker

The **active worker** is the worker that has actually claimed the task. This is recorded in the task file and in `assignment-state.json`. Until claimed, the active worker is `none`.

---

## Why Tasks Should Not Be Hardwired to Tools

Hardwiring tasks to specific tools creates fragility:

- If the tool is unavailable, the task stalls.
- If a better tool emerges, migration is difficult.
- If the tool underperforms, there is no recourse.
- It encourages private-memory dependency on a specific session.

By routing through capabilities and roles, the repo remains tool-agnostic. Any worker with the required capabilities can claim any task.

---

## How a Task Can Be Performed by One Worker or Many

### One Worker (Solo Mode)

A single worker may perform all roles for a task. Example: Windsurf acting as both backend-builder and qa-verifier for a small task.

Rules:
- The worker must still produce verification evidence.
- The worker must still write a handoff.
- The worker must not self-close without independent review or human approval.

### Many Workers (Multi-Worker Mode)

Different workers perform different roles for the same task. Example: Codex implements, Antigravity verifies UI, Claude reviews.

Rules:
- Each worker claims the task for their role.
- Locks must be coordinated.
- Handoffs must reference each other.
- The responsible role coordinates completion.

---

## How Preferred Workers Are Chosen

Preferred workers are chosen based on:

1. **Known strengths** — documented in `role-capability-matrix.md` and worker files.
2. **Past performance** — which workers have successfully completed similar tasks.
3. **Availability** — which workers are currently idle or available.
4. **Tool characteristics** — some tools are better at local file editing, others at reasoning.
5. **Human preference** — the human owner may express preferences in `PROJECT_GOAL.md`.

Preferred workers are recorded in:
- The task file (`## Preferred workers`)
- `capability-registry.json` (per capability)
- `role-capability-matrix.md` (per role)

---

## How Active Workers Claim Work

1. Worker reads `AGENTS.md` and `assignment-model.md`.
2. Worker reads `assignment-state.json` to understand current mode and assignments.
3. Worker reads `capability-registry.json` to understand its own capabilities.
4. Worker scans `tasks/ready/` for tasks matching its capabilities.
5. Worker checks `locks/` for conflicts.
6. Worker moves task to `claimed/`, creates a lock, updates `worker-status.json`.
7. Worker updates the task file's `Current claimed worker` field.
8. Worker updates `assignment-state.json` with the new assignment.

---

## How Assignment State Is Recorded

Assignment state is recorded in:

| File | What It Records |
|------|----------------|
| Task file | Responsible role, required capabilities, preferred workers, current claimed worker |
| `assignment-state.json` | Execution mode, active workers, current assignments, reassignment policy |
| `capability-registry.json` | All capabilities, their preferred workers, common roles, expected evidence |
| `worker-status.json` | Each worker's status, current task, active roles, best-for, unavailable-for |

---

## How Reassignment Works

See [`worker-switching-protocol.md`](./worker-switching-protocol.md) for the full protocol.

Summary:
1. Reassignment is triggered (blocked worker, stale lock, human request, etc.).
2. Current worker writes or reconstructs a handoff.
3. Current lock is closed, removed, or marked stale.
4. Reassignment record is created using [`reassignment/reassignment-template.md`](./reassignment/reassignment-template.md).
5. New worker reads the previous handoff, task file, and verification evidence.
6. New worker creates a new lock and continues work.

---

## How Solo Mode Differs from Multi-Worker Mode

| Aspect | Solo Mode | Multi-Worker Mode |
|--------|-----------|-------------------|
| Workers | One worker does everything | Multiple workers divide work |
| Roles | One worker performs all roles | Roles distributed across workers |
| Locks | Single lock per task | Multiple coordinated locks |
| Review | Must use automated validation or human approval | Different worker can review |
| Handoffs | Still required for continuity | Required for cross-worker continuity |
| Reassignment | Less frequent but still supported | More common |

---

## How Human Owners Can Override Assignment Decisions

Humans are the final authority. They may:

1. **Change execution mode** — Edit `assignment-state.json` mode field.
2. **Reassign a task** — Move the task file, update the lock, notify workers.
3. **Override preferred workers** — Edit the task file's preferred workers list.
4. **Block a worker** — Mark a worker as `unavailable_for` in `worker-status.json`.
5. **Force-close a task** — Move to `done/` after verifying independently.
6. **Approve solo-worker completion** — Act as the independent reviewer.

All human overrides should be documented in the task file or a handoff.

---

## Examples

### Example 1: Simple Task, Solo Mode

```
Task: TASK-0005 — Add login form validation

Required capabilities:
- code-implementation
- test-writing

Responsible role:
- frontend-builder

Preferred workers:
- Codex
- Windsurf

Current active worker:
- none (until claimed)

Execution mode: solo
```

A single worker (e.g., Windsurf) claims the task, implements the validation, writes tests, produces evidence, writes a handoff, and submits for human review.

### Example 2: Complex Task, Multi-Worker Mode

```
Task: TASK-0012 — Implement payment flow

Required capabilities:
- backend-implementation
- frontend-implementation
- test-writing
- ui-browser-verification
- security-review

Responsible role:
- backend-builder

Supporting roles:
- frontend-builder
- qa-verifier
- release-reviewer

Preferred workers:
- Codex (backend)
- Windsurf (frontend)
- Antigravity (UI verification)
- Claude (security review)

Current active worker:
- none (until claimed)

Execution mode: multi-worker
```

Codex claims and implements the backend. Windsurf claims and implements the frontend. Antigravity verifies the UI. Claude reviews security. The backend-builder (Codex) coordinates completion.

### Example 3: Reassignment

```
Task: TASK-0008 — Research payment providers

Original worker: Gemini (blocked — API unavailable)
New worker: Claude

Reassignment reason: Gemini API unavailable. Claude has research and long-context reasoning capabilities.

Handoff: Written by Gemini before reassignment.
Lock: Gemini's lock marked stale. Claude creates new lock.
```

---

## Related Files

- [`execution-modes.md`](./execution-modes.md) — Solo, multi-worker, and hybrid modes
- [`role-capability-matrix.md`](./role-capability-matrix.md) — Role-to-capability mapping
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment protocol
- [`task-routing-rules.md`](./task-routing-rules.md) — How tasks flow through the system
- [`state/assignment-state.json`](./state/assignment-state.json) — Current assignment state
- [`state/capability-registry.json`](./state/capability-registry.json) — Capability definitions
