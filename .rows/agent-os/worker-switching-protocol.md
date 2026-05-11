# Worker Switching Protocol

> **How to reassign a task from one worker to another without losing continuity.**

---

## When a Task May Be Switched

A task may be switched from one worker to another when:

- The current worker is blocked (API unavailable, tool limitation, missing context).
- The lock is stale (expired and the worker has not renewed it).
- The human owner requests reassignment.
- Another worker is better suited for the task's capabilities.
- Review reveals major issues requiring a different approach.
- Scope changes require different capabilities than the current worker has.
- The current worker failed to produce evidence.
- The current worker created unclear or unsafe changes.
- The current worker is needed for a higher-priority task.

---

## Required Before Switching

### 1. Current Task File Is Updated

The task file must reflect:
- Current status (e.g., `blocked` or `in-progress`).
- What has been completed.
- What remains.
- Any issues encountered.

### 2. Current Lock Is Closed, Removed, or Marked Stale

- If the current worker can write: close and remove the lock.
- If the current worker is unavailable: the human or coordinator marks the lock as stale.
- The stale lock is noted in the reassignment record.

### 3. Handoff Is Written or Reconstructed

- The current worker writes a handoff before releasing the task.
- If the current worker is unavailable, the human or coordinator reconstructs a handoff from available evidence (task file, commit history, changed files).
- The handoff must include everything the next worker needs to continue.

### 4. Known Risks Are Recorded

- Any risks discovered during the current worker's session.
- Any edge cases not yet handled.
- Any assumptions the current worker was operating under.

### 5. Files Changed Are Listed

- Complete list of files modified, created, or deleted.
- Current state of each file (committed, uncommitted, in PR).

### 6. Verification State Is Recorded

- What verification has been performed.
- What verification evidence exists.
- What verification still needs to be done.

---

## New Worker Startup After Switch

The new worker MUST follow this sequence:

1. **Read `AGENTS.md`** — Understand the constitution.
2. **Read `agent-os/assignment-model.md`** — Understand the assignment model.
3. **Read the task file** — Understand the objective, acceptance criteria, and current state.
4. **Read the previous handoff** — Understand what was done and what remains.
5. **Read verification evidence** — Review any existing test output, screenshots, or reports.
6. **Inspect changed files** — Review the actual code changes made so far.
7. **State continuation plan** — Before making edits, state what you will do and any assumptions.
8. **Create a new lock** — Using the lock template, with updated `claimed_by` and `expires_at`.
9. **Continue work** — Pick up where the previous worker left off.

---

## Reassignment Record

Every reassignment must be documented using the template at [`reassignment/reassignment-template.md`](./reassignment/reassignment-template.md). The record includes:

- Task ID
- Previous worker
- New worker
- Requested by
- Reason for reassignment
- Current task status
- Current lock status
- Files already changed
- Handoff available
- Verification available
- Known risks
- Required reading for new worker
- Continuation instructions
- Approval status

Completed reassignment records are archived in [`reassignment/archive/`](./reassignment/archive/).

---

## Stale Lock Handling

If a lock's `expires_at` has passed:

1. The human or coordinator notes the stale lock.
2. A reassignment record is created.
3. The stale lock is removed or marked as `stale` in the reassignment record.
4. The new worker creates a fresh lock.
5. If the original worker returns, they must read the reassignment record and handoff before resuming.

---

## Continuity Protection

The switching protocol protects against:

- **Private-memory dependency:** All context is in repo files, not in a specific AI's chat memory.
- **Lost work:** Handoffs and task files capture what was done.
- **Duplicate work:** The new worker reads the previous handoff before starting.
- **File conflicts:** The old lock is removed before the new lock is created.
- **Verification gaps:** Verification state is recorded in the handoff.

---

## Examples

### Example 1: Worker Blocked

```
Task: TASK-0005 — Research payment providers
Previous worker: Gemini
New worker: Claude
Reason: Gemini API unavailable for extended period.
Handoff: Written by Gemini before going offline.
Lock: Gemini's lock expired. Removed by human.
Continuation: Claude reads Gemini's handoff, reviews research notes, continues from where Gemini stopped.
```

### Example 2: Human-Requested Reassignment

```
Task: TASK-0012 — Implement auth flow
Previous worker: Codex
New worker: Windsurf
Reason: Human owner wants Windsurf to handle the full-stack implementation.
Handoff: Codex writes handoff documenting backend work completed.
Lock: Codex removes lock. Windsurf creates new lock.
Continuation: Windsurf reads Codex's handoff, reviews backend code, implements remaining frontend.
```

### Example 3: Stale Lock Recovery

```
Task: TASK-0008 — Update API documentation
Previous worker: Claude (lock expired 3 days ago)
New worker: Hermes
Reason: Stale lock. Claude session ended without handoff.
Handoff: Reconstructed by human from commit history and task file.
Lock: Stale lock removed. Hermes creates new lock.
Continuation: Hermes reads reconstructed handoff, reviews changed files, continues documentation.
```

---

## Related Files

- [`assignment-model.md`](./assignment-model.md) — Full assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Execution mode definitions
- [`reassignment/reassignment-template.md`](./reassignment/reassignment-template.md) — Reassignment record template
- [`reassignment/README.md`](./reassignment/README.md) — Reassignment process overview
- [`escalation-rules.md`](./escalation-rules.md) — When to escalate
- [`locks/README.md`](./locks/README.md) — Lock protocol
