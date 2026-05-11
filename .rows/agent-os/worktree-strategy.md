# Worktree Strategy

> **Use git worktrees for parallel agent execution.** Each worker gets its own checkout, branch, and filesystem root to prevent collisions in multi-worker or hybrid mode.

## Why worktrees

A git worktree lets one repository expose multiple working directories that share history but isolate files. For ROWS, that means:

- Each worker can edit independently.
- Branches stay separate.
- Shared state in the main checkout is not clobbered by parallel edits.
- Reviewers can inspect worker output without reconstructing context.

## When to use a worktree

Use a worktree whenever:

- two or more workers will edit at the same time;
- a primary worker is paired with a support or review worker;
- a task is likely to touch overlapping areas of the repo;
- the human owner wants parallel implementation and verification.

Solo work can stay in the main checkout, but worktrees are still safe if you prefer isolation.

## Naming convention

Recommended layout:

```text
<repo-name>-<worker-name>
```

Examples:

- `rows-template-codex`
- `rows-template-claude`
- `rows-template-windsurf`

Recommended branch format:

```text
agent/<worker-name>/<task-id>-worktree
```

Examples:

- `agent/codex/TASK-0012-worktree`
- `agent/windsurf/TASK-0044-worktree`

## Standard setup flow

1. Read the task and confirm the branch strategy.
2. Choose a worker name and task ID.
3. Run `npm run setup:worktree -- <worker> <task-id>`.
4. Switch into the created worktree directory.
5. Claim the task and start work.
6. Commit only from inside that worktree.
7. When done, push the branch and hand off the worktree path if needed.

## Rules

- Never have two active workers editing the same checkout.
- Do not create nested worktrees inside an existing worktree.
- Do not commit from the main checkout when a worker-specific worktree exists for that task.
- Keep the main checkout clean so human review and coordination remain reliable.
- If the worktree path already exists, stop and verify whether it is still active before reusing it.

## Verification

Before starting work, confirm:

- the worktree path exists;
- the branch name matches the task;
- `git status` is clean inside the worktree before edits;
- the task file records the worker/branch relationship.

## Related Files

- [`branch-strategy.md`](./branch-strategy.md) — branch naming and lifecycle
- [`execution-modes.md`](./execution-modes.md) — when worktrees are expected
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — reassignment flow
- [`file-ownership.md`](./file-ownership.md) — collision avoidance rules
