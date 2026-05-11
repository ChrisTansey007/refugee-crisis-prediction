# File Ownership & Collision Avoidance

> **How workers avoid modifying the same files at the same time.**

## The Problem

Multiple AI workers operating on the same repository can create conflicts:
- Two workers modify the same file simultaneously.
- A worker modifies a file another worker depends on.
- Merge conflicts arise from overlapping changes.

## The Solution: Advisory Locks

Workers declare their intent to modify files by creating lock files in [`locks/`](./locks/). Locks are **advisory** (not enforced by tooling) but **required by process**.

## Before Modifying Files

1. **Check `locks/`** for any lock that covers files you intend to modify.
2. **If a lock exists and is not stale:** Do not modify those files. Choose a different task or escalate.
3. **If no lock exists:** Create your own lock before modifying files.

## Lock Contents

Each lock file (see [`locks/lock-template.json`](./locks/lock-template.json)) declares:
- `task_id` — The task being worked on.
- `claimed_by` — The worker holding the lock.
- `files_expected` — List of files the worker intends to modify.
- `expires_at` — When the lock expires (prevents permanent blocking).

## Collision Resolution

### Same File, Different Tasks
If two tasks need to modify the same file:
1. The tasks should be sequenced (one depends on the other).
2. Or the file should be refactored to reduce coupling.
3. Escalate to the human for prioritization.

### Stale Locks
If a lock's `expires_at` has passed:
1. Do NOT delete the lock yourself.
2. Note it in your handoff.
3. Escalate to the human.

### Merge Conflicts
If a merge conflict occurs:
1. The worker who detects it documents it in their handoff.
2. The human resolves the conflict or assigns a worker to resolve it.
3. Do not force-push to resolve conflicts.

## Best Practices

- **Keep tasks small.** Smaller tasks touch fewer files, reducing collision probability.
- **Declare files early.** List expected files in your lock as soon as you claim a task.
- **Update your lock.** If you discover you need additional files, update the lock.
- **Release promptly.** Remove your lock as soon as your task is done or blocked.
- **Communicate via handoffs.** If you see a potential conflict, note it in your handoff.

## Related Files

- [`locks/README.md`](./locks/README.md) — Full lock protocol
- [`locks/lock-template.json`](./locks/lock-template.json) — Lock file template
- [`escalation-rules.md`](./escalation-rules.md) — When to escalate
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment and lock handoff
