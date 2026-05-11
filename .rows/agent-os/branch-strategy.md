# Branch Strategy

> **All workers must follow these branch naming conventions.**

## Branch Naming Format

```
[type]/[worker]/[task-id]-short-description
```

## Types

| Type | Format | Example | When to Use |
|------|--------|---------|-------------|
| `agent` | `agent/[worker]/[task-id]-desc` | `agent/codex/TASK-0003-add-auth` | Feature implementation by a worker |
| `docs` | `docs/[task-id]-desc` | `docs/TASK-0004-api-docs` | Documentation-only changes |
| `fix` | `fix/[task-id]-desc` | `fix/TASK-0005-login-bug` | Bug fixes |

## Rules

- Branch names must be lowercase, using hyphens for spaces.
- The `task-id` is required (e.g., `TASK-0003`).
- The `short-description` should be 2-4 words summarizing the change.
- Workers must create their branch AFTER claiming a task and BEFORE starting work.
- Branches should be created from `main` (or the current default branch).
- In multi-worker and hybrid mode, pair the branch with a dedicated git worktree when parallel edits are expected.

## Examples

```
agent/windsurf/TASK-0001-initialize-project
agent/claude/TASK-0002-design-data-model
agent/codex/TASK-0003-implement-auth-endpoints
agent/gemini/TASK-0004-research-payment-providers
agent/antigravity/TASK-0005-verify-ui-flows
agent/hermes/TASK-0006-decompose-milestone-2
docs/TASK-0007-update-api-docs
fix/TASK-0008-fix-login-redirect
```

## Branch Lifecycle

1. **Create:** After claiming a task.
2. **Work:** Commit changes to this branch.
3. **PR:** Open a pull request to `main`.
4. **Review:** Independent reviewer approves.
5. **Merge:** Branch merged to `main`.
6. **Delete:** Branch deleted after merge.

## Related Files

- [`worker-contract.md`](./worker-contract.md) — Worker obligations
- [`task-lifecycle.md`](./task-lifecycle.md) — Task state machine
- [`file-ownership.md`](./file-ownership.md) — Collision avoidance
- [`execution-modes.md`](./execution-modes.md) — Execution modes
- [`worktree-strategy.md`](./worktree-strategy.md) — Parallel worker checkout strategy
