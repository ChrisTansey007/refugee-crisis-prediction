# Skill: Claim Task

Use this skill when claiming a task from `agent-os/tasks/ready/`.

## Core Rule

Claim only tasks that are already in `ready/`, create a lock in `agent-os/locks/`, update the task file and worker state, then move the task to `in-progress/`.

## Steps

1. List and read ready tasks.
2. Confirm your capabilities fit the task.
3. Refresh the task's `Context Snapshot` if it is missing or stale.
4. Move the task to `claimed/`.
5. Create a lock in `agent-os/locks/` using `lock-template.json`.
6. Update the task file:

- `Status` to `claimed`, then `in-progress` when work begins
- `Current Claimed Worker`
- `Snapshot Freshness` if you refreshed context

7. Update `agent-os/state/worker-status.json`.
8. Create the branch for the task.
9. Move the task to `in-progress/` and begin work.

## Related Files

- [`session-close.md`](./session-close.md)
- [`enrich-task.md`](./enrich-task.md)
- [`../tasks/task-template.md`](../tasks/task-template.md)
- [`../locks/lock-template.json`](../locks/lock-template.json)
