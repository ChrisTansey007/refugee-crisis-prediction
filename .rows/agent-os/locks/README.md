# Locks — Advisory File Locks

## Why Locks Exist

Multiple AI workers operating on the same repository can create conflicts when they modify the same files. Locks are a lightweight mechanism for workers to declare their intent to modify specific files, preventing collisions.

## How Locks Work

1. **Before modifying files,** a worker checks `locks/` for any lock covering those files.
2. **If no conflicting lock exists,** the worker creates a lock using [`lock-template.json`](./lock-template.json).
3. **The lock declares:** which task, which worker, which files, and when it expires.
4. **After the task is done or blocked,** the worker (or reviewer) removes the lock.

## Lock Properties

| Field | Description |
|-------|-------------|
| `task_id` | The task this lock is for |
| `claimed_by` | The worker holding the lock |
| `claimed_at` | When the lock was created |
| `branch` | The git branch for this work |
| `status` | `active` or `released` |
| `files_expected` | Files the worker intends to modify |
| `expires_at` | When the lock expires (prevents permanent blocking) |
| `notes` | Any additional context |

## Advisory but Required

Locks are **advisory** — no tooling enforces them automatically. However, they are **required by process**. A worker who ignores locks and causes a collision has violated the worker contract and should be escalated.

## Stale Locks

If a lock's `expires_at` has passed:
1. Do NOT delete the lock yourself.
2. Note it in your handoff.
3. Escalate to the human per [`../escalation-rules.md`](../escalation-rules.md).

## Related Files

- [`lock-template.json`](./lock-template.json) — Lock file template
- [`../file-ownership.md`](../file-ownership.md) — Collision avoidance
- [`../worker-contract.md`](../worker-contract.md) — Worker obligations
- [`../escalation-rules.md`](../escalation-rules.md) — Escalation rules
