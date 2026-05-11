# Reassignment

> **How tasks are reassigned from one worker to another. Reassignment protects against private-memory dependency and worker unavailability.**

---

## Why Reassignment Exists

Reassignment exists because:

1. **Workers are replaceable.** No task should depend on a specific AI tool.
2. **Workers become unavailable.** APIs go down, sessions expire, tools change.
3. **Capability mismatches emerge.** A task may reveal that the current worker lacks needed skills.
4. **Human owners change their minds.** Priorities shift, preferences change.
5. **Review reveals issues.** A different worker may be needed to fix problems.
6. **Stale locks block progress.** A worker may abandon a task without cleanup.

---

## When Reassignment Is Allowed

Reassignment is allowed when:

- The current worker is blocked (API unavailable, tool limitation).
- The lock is stale (expired without renewal).
- The human owner requests it.
- Another worker is better suited (capability mismatch).
- Review reveals major issues requiring a different approach.
- Scope changes require different capabilities.
- The current worker failed to produce evidence.
- The current worker created unclear or unsafe changes.

---

## Who Can Request Reassignment

- **The current worker** — If blocked or recognizing a capability gap.
- **The human owner** — At any time, for any reason.
- **The Coordinator (Hermes)** — As a proposal for human approval.
- **A reviewer** — If review reveals issues the current worker cannot fix.

---

## How Stale Locks Are Handled

1. Stale lock is identified (expiration passed, worker unresponsive).
2. Coordinator or human notes the stale lock.
3. Reassignment record is created.
4. Stale lock is removed or marked as `stale`.
5. New worker creates a fresh lock.
6. If original worker returns, they must read the reassignment record.

---

## How Continuation Context Is Preserved

Continuation context is preserved through:

1. **Handoffs** — The previous worker (or human) writes what was done and what remains.
2. **Task files** — Always reflect current status and completion state.
3. **Reassignment records** — Document the reason, state, and instructions.
4. **Verification evidence** — Test output, screenshots, logs remain in the repo.
5. **Changed files** — Git history shows exactly what was modified.

---

## How Reassignment Protects Against Private-Memory Dependency

The #1 risk in multi-agent systems is that a task becomes dependent on context stored only in a specific AI's chat memory. Reassignment protects against this by:

1. **Requiring handoffs before reassignment.** All context must be written to files.
2. **Requiring the new worker to read repo files, not rely on chat history.**
3. **Making task state discoverable from repo files alone.**
4. **Banning the assumption that "the previous worker knows."**

If a worker cannot write a handoff (e.g., session crashed), the human or Coordinator reconstructs one from available evidence.

---

## Reassignment Process

1. Trigger identified (blocked, stale, human request, etc.).
2. Reassignment record created using [`reassignment-template.md`](./reassignment-template.md).
3. Current worker writes handoff (or human reconstructs).
4. Current lock closed, removed, or marked stale.
5. Task file updated with reassignment notes.
6. New worker reads: AGENTS.md, assignment-model.md, task file, previous handoff, verification evidence.
7. New worker creates new lock.
8. New worker continues work.

---

## Related Files

- [`reassignment-template.md`](./reassignment-template.md) — Reassignment record template
- [`archive/`](./archive/) — Completed reassignment records
- [`../worker-switching-protocol.md`](../worker-switching-protocol.md) — Full switching protocol
- [`../assignment-model.md`](../assignment-model.md) — Assignment hierarchy
- [`../escalation-rules.md`](../escalation-rules.md) — When to escalate
