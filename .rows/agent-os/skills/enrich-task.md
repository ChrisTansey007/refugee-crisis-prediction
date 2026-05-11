# Skill: Enrich Task

Use this skill before a task moves from `backlog/` to `ready/`, or when a claimed task's context snapshot has gone stale.

## Purpose

Turn a task into an atomic unit by embedding the minimal context a cold-starting agent needs:

- why the task exists
- which decisions matter
- which constraints govern it
- which upstream facts should not be rediscovered from scratch

## Steps

1. Read the task file and its existing `Dependencies`, `Related ADRs`, `Related Decisions`, and `Required Reading`.
2. Read:

- `PROJECT_GOAL.md`
- `PROJECT_CONTEXT.md`
- any referenced ADRs or decisions
- upstream dependency tasks if they matter

3. Draft or refresh the `Context Snapshot` section manually, or use the helper:

```bash
node scripts/enrich-task.mjs agent-os/tasks/backlog/TASK-XXXX-sample.md
```

4. Confirm the snapshot includes:

- `Why This Task Exists`
- `Key Decisions`
- `Key Constraints`
- `Upstream Facts`
- `Required Context Links`
- `Snapshot Freshness`

5. If the task is being promoted to `ready/`, ensure the snapshot is present before promotion.

## Notes

- The snapshot is a compressed handoff from knowledge to work.
- It should be short enough to load fast, but specific enough that an agent does not need to re-navigate the whole repo to get oriented.
