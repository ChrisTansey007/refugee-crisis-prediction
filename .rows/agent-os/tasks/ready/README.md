# Ready

Tasks in this folder are **approved and claimable** by any worker.

## Who Can Add Tasks Here

- The human project owner ONLY.

## What Belongs Here

- Approved tasks that are ready for a worker to claim.
- Tasks with clear acceptance criteria and no blocking dependencies.

## How Tasks Leave Here

- **Claimed:** A worker moves the task to [`../claimed/`](../claimed/).
- **Un-approved:** Human moves the task back to [`../backlog/`](../backlog/).

## Rules

- Workers can ONLY claim tasks from this folder.
- Before claiming, workers MUST check [`../../locks/`](../../locks/) for conflicts.
- The human should ensure tasks here are well-defined and independently executable.

## Related Files

- [`../task-template.md`](../task-template.md) — Task file template
- [`../../worker-contract.md`](../../worker-contract.md) — Claiming process
